"""
Seasonal cycle removal module for Himalaya Trend Lab (Section 7.2).
In high-mountain glacier regions, the annual seasonal cycle is often 10x to 30x
larger than the decadal trend. Removing the seasonal cycle (monthly climatology
or STL decomposition) is essential to reveal the underlying climate signal.
"""
from typing import Dict, Any
import numpy as np
import pandas as pd

MONTH_NAMES = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
]


def compute_monthly_climatology(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute the 12-month climatological baseline (mean, std, IQR, min, max)
    across all available years in the series.
    """
    grouped = df.groupby("month")["value"]
    clim = pd.DataFrame({
        "month": range(1, 13),
        "month_name": MONTH_NAMES,
        "clim_mean": [grouped.get_group(m).mean() if m in grouped.groups else np.nan for m in range(1, 13)],
        "clim_std": [grouped.get_group(m).std(ddof=1) if m in grouped.groups else np.nan for m in range(1, 13)],
        "clim_q25": [grouped.get_group(m).quantile(0.25) if m in grouped.groups else np.nan for m in range(1, 13)],
        "clim_q75": [grouped.get_group(m).quantile(0.75) if m in grouped.groups else np.nan for m in range(1, 13)],
        "clim_min": [grouped.get_group(m).min() if m in grouped.groups else np.nan for m in range(1, 13)],
        "clim_max": [grouped.get_group(m).max() if m in grouped.groups else np.nan for m in range(1, 13)],
    })
    return clim.round(3)


def deseasonalize_series(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Remove the 12-month seasonal cycle from a monthly time series:
    1. Classical Monthly Climatology Anomaly: `anomaly = value - clim_mean(month)`
    2. STL (Seasonal-Trend decomposition using LOESS) via statsmodels when n >= 24.
    Returns an enriched DataFrame, the 12-month climatology table, and seasonal diagnostics.
    """
    out = df.sort_values("date").copy().reset_index(drop=True)
    clim_df = compute_monthly_climatology(out)

    month_to_mean = dict(zip(clim_df["month"], clim_df["clim_mean"]))
    out["seasonal_cycle"] = out["month"].map(month_to_mean)
    out["anomaly"] = (out["value"] - out["seasonal_cycle"]).round(4)

    # Optional STL decomposition (Section 7.2)
    if len(out) >= 24:
        try:
            from statsmodels.tsa.seasonal import STL
            series_clean = pd.Series(out["value"].values, index=pd.to_datetime(out["date"]))
            stl_res = STL(series_clean, period=12, robust=True).fit()
            out["stl_trend"] = np.round(stl_res.trend.values, 4)
            out["stl_seasonal"] = np.round(stl_res.seasonal.values, 4)
            out["stl_resid"] = np.round(stl_res.resid.values, 4)
        except Exception:
            out["stl_trend"] = out["anomaly"].rolling(12, center=True, min_periods=1).mean().round(4)
            out["stl_seasonal"] = out["seasonal_cycle"]
            out["stl_resid"] = out["anomaly"] - out["stl_trend"]
    else:
        out["stl_trend"] = out["anomaly"]
        out["stl_seasonal"] = out["seasonal_cycle"]
        out["stl_resid"] = 0.0

    # Seasonal diagnostics explaining why deseasonalization matters
    peak_row = clim_df.loc[clim_df["clim_mean"].idxmax()]
    trough_row = clim_df.loc[clim_df["clim_mean"].idxmin()]
    seasonal_range = float(peak_row["clim_mean"] - trough_row["clim_mean"])
    anomaly_std = float(out["anomaly"].std(ddof=1)) if len(out) > 1 else 1.0
    dominance_ratio = round(seasonal_range / max(1e-6, anomaly_std), 2)

    diagnostics = {
        "peak_month_name": str(peak_row["month_name"]),
        "peak_month_value": round(float(peak_row["clim_mean"]), 2),
        "trough_month_name": str(trough_row["month_name"]),
        "trough_month_value": round(float(trough_row["clim_mean"]), 2),
        "seasonal_peak_to_trough_range": round(seasonal_range, 2),
        "anomaly_std": round(anomaly_std, 3),
        "seasonal_dominance_ratio": dominance_ratio,
    }

    return {
        "series": out,
        "climatology": clim_df,
        "diagnostics": diagnostics,
    }
