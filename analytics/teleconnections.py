"""
Global Climate Teleconnection Detective (NAO, ENSO, IOD) & Multi-Satellite
Cross-Validation Matrix (Section 10: NASA MODIS vs. MERRA-2 vs. GPM IMERG vs. Meteomatics).
"""
from typing import Dict, Any
import numpy as np
import pandas as pd
from scipy import stats

from config.missions import TELECONNECTION_INDICES
from data.generator import generate_multivariate_series
from analytics.seasonal import deseasonalize_series
from analytics.trend_tests import compute_sens_slope, mann_kendall_hamed_rao


def analyze_teleconnections(enriched_df: pd.DataFrame) -> pd.DataFrame:
    """
    Correlate deseasonalized regional climate anomalies against global atmospheric
    teleconnection indices:
    1. North Atlantic Oscillation (NAO - Winter Westerlies driver)
    2. El Niño–Southern Oscillation (ENSO / Niño 3.4 - Monsoon & temperature modulator)
    3. Indian Ocean Dipole (IOD - Arabian Sea moisture & spring warmth transport)
    """
    anom = enriched_df["anomaly"].values
    rows = []

    col_map = {
        "nao": "nao_index",
        "enso": "enso_index",
        "iod": "iod_index",
    }

    for key, meta in TELECONNECTION_INDICES.items():
        col = col_map[key]
        if col in enriched_df.columns:
            idx_vals = enriched_df[col].values
            valid = (~np.isnan(anom)) & (~np.isnan(idx_vals))
            if np.sum(valid) >= 12:
                r_pearson, p_pearson = stats.pearsonr(anom[valid], idx_vals[valid])
                r_spearman, p_spearman = stats.spearmanr(anom[valid], idx_vals[valid])
            else:
                r_pearson, p_pearson, r_spearman, p_spearman = 0.0, 1.0, 0.0, 1.0

            rows.append({
                "index_id": key.upper(),
                "index_name": meta["name"],
                "primary_season": meta["primary_season"],
                "pearson_r": round(float(r_pearson), 3),
                "pearson_p": round(float(p_pearson), 4),
                "spearman_rho": round(float(r_spearman), 3),
                "significant_coupling": bool(p_pearson < 0.05),
                "physical_mechanism": meta["mechanism"],
            })

    return pd.DataFrame(rows)


def compute_multi_sensor_validation(region_id: str) -> Dict[str, Any]:
    """
    Cross-validate independent satellite and reanalysis datasets over the same region (Section 10):
    - Pair 1 (Temperature): NASA MODIS Land Surface Temp (MOD11C3) vs. NASA MERRA-2 Air Temp (T2M)
    - Pair 2 (Cryosphere): NASA MODIS Snow Cover (MOD10CM) vs. Meteomatics Snow Depth & NASA GLDAS SWE
    - Pair 3 (Precipitation): NASA GPM IMERG (Satellite) vs. NASA MERRA-2 Snowfall
    """
    mv_df = generate_multivariate_series(region_id, start_year=2000, end_year=2026)
    t_years = mv_df["year"].values + (mv_df["month"].values - 0.5) / 12.0

    pairs = [
        {
            "validation_pair": "Temperature: NASA MODIS LST (MOD11C3) vs. NASA MERRA-2 Air Temp (T2M)",
            "var_a": "lst_modis",
            "var_b": "t2m_merra2",
            "sensor_a": "NASA Terra MODIS (5 km Thermal IR)",
            "sensor_b": "NASA MERRA-2 / Meteomatics (Reanalysis)",
            "units": "°C",
        },
        {
            "validation_pair": "Snowpack: NASA MODIS Snow Cover (MOD10CM) vs. Meteomatics Snow Depth",
            "var_a": "snow_cover_modis",
            "var_b": "snow_depth_meteomatics",
            "sensor_a": "NASA Terra/Aqua MODIS (Optical SCF %)",
            "sensor_b": "Meteomatics Cryosphere Assimilation (cm)",
            "units": "% vs cm",
        },
        {
            "validation_pair": "Water Storage: NASA GLDAS SWE vs. NASA MODIS Snow Cover",
            "var_a": "swe_gldas",
            "var_b": "snow_cover_modis",
            "sensor_a": "NASA GLDAS Noah L4 Model (mm SWE)",
            "sensor_b": "NASA MODIS Snow Cover (%)",
            "units": "mm vs %",
        },
    ]

    summary_rows = []
    for p in pairs:
        df_a = pd.DataFrame({"date": mv_df["date"], "year": mv_df["year"], "month": mv_df["month"], "value": mv_df[p["var_a"]]})
        df_b = pd.DataFrame({"date": mv_df["date"], "year": mv_df["year"], "month": mv_df["month"], "value": mv_df[p["var_b"]]})

        anom_a = deseasonalize_series(df_a)["series"]["anomaly"].values
        anom_b = deseasonalize_series(df_b)["series"]["anomaly"].values

        r_raw, _ = stats.pearsonr(mv_df[p["var_a"]].values, mv_df[p["var_b"]].values)
        r_anom, p_anom = stats.pearsonr(anom_a, anom_b)

        sens_a = compute_sens_slope(t_years, anom_a)
        sens_b = compute_sens_slope(t_years, anom_b)
        mk_a = mann_kendall_hamed_rao(anom_a)
        mk_b = mann_kendall_hamed_rao(anom_b)

        dir_agree = (np.sign(sens_a["slope_per_decade"]) == np.sign(sens_b["slope_per_decade"]))
        sig_agree = (mk_a["significant"] == mk_b["significant"])

        summary_rows.append({
            "Validation Pair": p["validation_pair"],
            "Sensor A": p["sensor_a"],
            "Sensor B": p["sensor_b"],
            "Raw Cycle Correlation (r)": round(float(r_raw), 3),
            "Anomaly Correlation (r)": round(float(r_anom), 3),
            "Sensor A Slope/Decade": round(sens_a["slope_per_decade"], 3),
            "Sensor B Slope/Decade": round(sens_b["slope_per_decade"], 3),
            "Direction Agreement": "AGREE" if dir_agree else "DIVERGE",
            "Significance Agreement": "BOTH SIGNIFICANT" if (mk_a["significant"] and mk_b["significant"]) else ("AGREE" if sig_agree else "MIXED"),
        })

    return {
        "validation_table": pd.DataFrame(summary_rows),
        "multivariate_df": mv_df,
    }
