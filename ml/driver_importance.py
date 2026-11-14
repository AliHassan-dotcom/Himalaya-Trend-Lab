"""
Explainable ML Driver Detective for Himalaya Trend Lab (Layer 4 ML).
Trains a Random Forest Regressor & HistGradientBoosting Regressor using
TimeSeriesSplit cross-validation to quantify which physical Earth-system drivers
(Air Temp, Surface Temp, Snowfall, Total Precip, Humidity, Aerosols, NAO, ENSO, IOD)
drive cryosphere/hydrological anomalies in each glacier region.
"""
from typing import Dict, Any, List
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, HistGradientBoostingRegressor
from sklearn.inspection import permutation_importance
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

from data.generator import generate_multivariate_series
from analytics.seasonal import deseasonalize_series

DRIVER_FEATURE_LABELS: Dict[str, str] = {
    "t2m_merra2": "Air Temperature (2m, MERRA-2)",
    "lst_modis": "Land Surface Temp (MODIS LST)",
    "precip_imerg": "Total Precipitation (GPM IMERG)",
    "snowfall_merra2": "Solid Snowfall Rate (MERRA-2)",
    "humidity_airs": "Relative Humidity (AIRS)",
    "aerosols_omi": "Black-Carbon & Dust Aerosols (OMI AOD)",
    "nao_index": "North Atlantic Oscillation (Winter Westerlies)",
    "enso_index": "El Niño–Southern Oscillation (ENSO)",
    "iod_index": "Indian Ocean Dipole (IOD)",
}


def train_driver_importance_model(
    region_id: str,
    target_variable_id: str = "snow_cover_modis",
    glacier_only: bool = False,
) -> Dict[str, Any]:
    """
    Train an explainable Random Forest Regressor (plus Gradient Boosting benchmark)
    on deseasonalized monthly anomalies to identify the dominant physical drivers
    of `target_variable_id` in `region_id`.
    Performs chronological train/test evaluation and 5-fold TimeSeriesSplit CV.
    """
    mv_df = generate_multivariate_series(
        region_id=region_id,
        start_year=2000,
        end_year=2026,
        glacier_only=glacier_only,
    )

    # Deseasonalize all meteorological variables so ML learns physical anomaly relationships
    # rather than trivial seasonal co-variation
    anom_df = pd.DataFrame({"date": mv_df["date"], "year": mv_df["year"], "month": mv_df["month"]})
    all_vars = [
        "snow_cover_modis", "snow_depth_meteomatics", "swe_gldas", "runoff_gldas",
        "t2m_merra2", "lst_modis", "precip_imerg", "snowfall_merra2",
        "humidity_airs", "aerosols_omi",
    ]
    for col in all_vars:
        tmp = pd.DataFrame({
            "date": mv_df["date"],
            "year": mv_df["year"],
            "month": mv_df["month"],
            "value": mv_df[col],
        })
        anom_df[col] = deseasonalize_series(tmp)["series"]["anomaly"].values

    for tele_col in ["nao_index", "enso_index", "iod_index"]:
        anom_df[tele_col] = mv_df[tele_col].values

    if target_variable_id not in anom_df.columns:
        target_variable_id = "snow_cover_modis"

    # Candidate explanatory features (excluding the target itself and closely redundant target proxies)
    feature_cols: List[str] = [
        c for c in DRIVER_FEATURE_LABELS.keys()
        if c != target_variable_id
    ]

    # Add 1-month lagged temperature and snowfall anomalies to capture snowpack memory
    X_df = anom_df[feature_cols].copy()
    X_df["t2m_lag1"] = anom_df["t2m_merra2"].shift(1).bfill()
    X_df["snowfall_lag1"] = anom_df["snowfall_merra2"].shift(1).bfill()

    feature_names_map = dict(DRIVER_FEATURE_LABELS)
    feature_names_map["t2m_lag1"] = "Prior-Month Air Temp Memory (Lag-1)"
    feature_names_map["snowfall_lag1"] = "Prior-Month Snowfall Accumulation (Lag-1)"

    all_feature_cols = list(X_df.columns)
    X = X_df.values
    y = anom_df[target_variable_id].values

    # Chronological 80% Train / 20% Holdout Test Split
    split_idx = int(len(X) * 0.80)
    X_train, X_test = X[:split_idx], X[split_idx:]
    y_train, y_test = y[:split_idx], y[split_idx:]

    # 1. Train Random Forest Regressor
    rf = RandomForestRegressor(
        n_estimators=200,
        max_depth=8,
        min_samples_leaf=3,
        random_state=42,
        n_jobs=1,
    )
    rf.fit(X_train, y_train)

    y_train_pred = rf.predict(X_train)
    y_test_pred = rf.predict(X_test)
    full_pred = rf.predict(X)

    # 2. Train HistGradientBoosting Regressor for ensemble comparison
    gb = HistGradientBoostingRegressor(max_iter=150, max_depth=5, learning_rate=0.06, random_state=42)
    gb.fit(X_train, y_train)
    gb_test_pred = gb.predict(X_test)

    # 3. 5-Fold TimeSeriesSplit Cross-Validation
    tscv = TimeSeriesSplit(n_splits=5)
    cv_r2_scores = []
    for tr_idx, val_idx in tscv.split(X):
        rf_cv = RandomForestRegressor(n_estimators=100, max_depth=7, min_samples_leaf=3, random_state=42, n_jobs=1)
        rf_cv.fit(X[tr_idx], y[tr_idx])
        cv_r2_scores.append(float(r2_score(y[val_idx], rf_cv.predict(X[val_idx]))))

    # 4. Permutation Importance + Impurity Feature Importance
    perm = permutation_importance(rf, X_test, y_test, n_repeats=10, random_state=42, n_jobs=1)
    raw_imp = 0.65 * rf.feature_importances_ + 0.35 * np.maximum(0.0, perm.importances_mean)
    imp_pct = 100.0 * raw_imp / max(1e-9, np.sum(raw_imp))

    # Compute sign of physical relationship (Pearson r with target)
    driver_rows = []
    for idx, col in enumerate(all_feature_cols):
        r_val = float(np.corrcoef(X[:, idx], y)[0, 1])
        driver_rows.append({
            "feature_id": col,
            "driver_name": feature_names_map.get(col, col),
            "importance_pct": round(float(imp_pct[idx]), 2),
            "correlation_r": round(r_val, 3),
            "effect_direction": "Positive (+)" if r_val >= 0 else "Negative (-)",
        })

    importance_df = pd.DataFrame(driver_rows).sort_values("importance_pct", ascending=False).reset_index(drop=True)
    top_driver = importance_df.iloc[0]

    anom_df["actual_anomaly"] = np.round(y, 4)
    anom_df["rf_predicted_anomaly"] = np.round(full_pred, 4)
    anom_df["split"] = ["Train (80%)" if i < split_idx else "Test Holdout (20%)" for i in range(len(X))]

    metrics = {
        "train_r2": round(float(r2_score(y_train, y_train_pred)), 4),
        "test_r2": round(float(r2_score(y_test, y_test_pred)), 4),
        "gb_test_r2": round(float(r2_score(y_test, gb_test_pred)), 4),
        "cv_mean_r2": round(float(np.mean(cv_r2_scores)), 4),
        "test_rmse": round(float(np.sqrt(mean_squared_error(y_test, y_test_pred))), 4),
        "test_mae": round(float(mean_absolute_error(y_test, y_test_pred)), 4),
        "n_train_months": len(X_train),
        "n_test_months": len(X_test),
        "top_driver_name": str(top_driver["driver_name"]),
        "top_driver_importance_pct": float(top_driver["importance_pct"]),
    }

    return {
        "rf_model": rf,
        "gb_model": gb,
        "importance_df": importance_df,
        "predictions_df": anom_df[["date", "year", "month", "actual_anomaly", "rf_predicted_anomaly", "split"]],
        "metrics": metrics,
        "target_variable_id": target_variable_id,
        "region_id": region_id,
    }
