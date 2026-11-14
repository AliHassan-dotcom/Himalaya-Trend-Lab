"""
Non-Linear Trend Modeling (Gaussian Process Regression) & Structural Regime
Changepoint Detection for Himalaya Trend Lab (Layer 4 ML).
Trains a GaussianProcessRegressor (RBF + WhiteKernel) on deseasonalized anomalies
and detects the structural changepoint year where the trend regime shifted.
"""
from typing import Dict, Any, Optional
import numpy as np
import pandas as pd
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, WhiteKernel, ConstantKernel
from sklearn.metrics import r2_score, mean_squared_error

from analytics.seasonal import deseasonalize_series


def fit_nonlinear_gpr_and_changepoint(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Train a Gaussian Process Regression (GPR) model on the deseasonalized anomaly
    series to capture non-linear climate acceleration, and run a piece-wise
    two-regime structural break scan to identify the exact changepoint year.
    """
    seasonal_pack = deseasonalize_series(df)
    s_df = seasonal_pack["series"].copy()

    t_years = s_df["year"].values + (s_df["month"].values - 0.5) / 12.0
    y_anom = s_df["anomaly"].values.astype(float)
    n = len(t_years)

    # Normalize time for stable GPR kernel optimization
    t_mean = float(np.mean(t_years))
    t_std = float(np.std(t_years)) if np.std(t_years) > 0 else 1.0
    X = ((t_years - t_mean) / t_std).reshape(-1, 1)

    kernel = (
        ConstantKernel(1.0, (1e-4, 1e3))
        * RBF(length_scale=1.5, length_scale_bounds=(0.2, 25.0))
        + WhiteKernel(noise_level=0.5, noise_level_bounds=(1e-4, 25.0))
    )
    gpr = GaussianProcessRegressor(
        kernel=kernel,
        alpha=1e-4,
        normalize_y=True,
        random_state=42,
        n_restarts_optimizer=2,
    )
    gpr.fit(X, y_anom)

    y_pred, y_std = gpr.predict(X, return_std=True)
    gpr_r2 = float(r2_score(y_anom, y_pred))
    gpr_rmse = float(np.sqrt(mean_squared_error(y_anom, y_pred)))

    s_df["gpr_nonlinear_trend"] = np.round(y_pred, 4)
    s_df["gpr_ci_low"] = np.round(y_pred - 1.96 * y_std, 4)
    s_df["gpr_ci_high"] = np.round(y_pred + 1.96 * y_std, 4)

    # Structural Regime Changepoint Detection (Two-Segment Piecewise Regression Scan)
    # Scans candidate years in the middle 60% of the record to minimize residual sum of squares (RSS)
    min_idx = int(n * 0.20)
    max_idx = int(n * 0.80)
    best_idx = n // 2
    best_rss = float("inf")
    best_slope_before = 0.0
    best_slope_after = 0.0

    # Full single-line RSS for F-test comparison
    p_full = np.polyfit(t_years, y_anom, 1)
    rss_single = float(np.sum((y_anom - np.polyval(p_full, t_years)) ** 2))

    for idx in range(min_idx, max_idx, 3):
        t1, y1 = t_years[:idx], y_anom[:idx]
        t2, y2 = t_years[idx:], y_anom[idx:]
        if len(t1) < 12 or len(t2) < 12:
            continue
        p1 = np.polyfit(t1, y1, 1)
        p2 = np.polyfit(t2, y2, 1)
        rss = float(np.sum((y1 - np.polyval(p1, t1)) ** 2) + np.sum((y2 - np.polyval(p2, t2)) ** 2))
        if rss < best_rss:
            best_rss = rss
            best_idx = idx
            best_slope_before = float(p1[0] * 10.0)  # per decade
            best_slope_after = float(p2[0] * 10.0)   # per decade

    changepoint_year = int(s_df["year"].iloc[best_idx])
    rss_reduction_pct = 100.0 * max(0.0, (rss_single - best_rss) / max(1e-6, rss_single))
    acceleration_ratio = round(best_slope_after - best_slope_before, 4)

    return {
        "model": gpr,
        "series": s_df,
        "gpr_r2": round(gpr_r2, 4),
        "gpr_rmse": round(gpr_rmse, 4),
        "learned_kernel": str(gpr.kernel_),
        "changepoint_year": changepoint_year,
        "slope_before_decade": round(best_slope_before, 4),
        "slope_after_decade": round(best_slope_after, 4),
        "slope_acceleration_decade": acceleration_ratio,
        "rss_improvement_pct": round(rss_reduction_pct, 2),
        "regime_shift_detected": bool(rss_reduction_pct > 4.0),
    }
