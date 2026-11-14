"""
Pre-Training & Serialization Pipeline for Himalaya Trend Lab (Layer 4 ML).
Trains all 4 ML model families across Pakistan's glacier basins, saves serialized
model artifacts (`.joblib`) in `ml/trained_models/`, and writes an official
`training_metrics.json` report.
"""
import json
from pathlib import Path
from typing import Dict, Any
import joblib

from config.regions import PRESET_REGIONS
from data import load_investigation_series
from ml.nonlinear_trend import fit_nonlinear_gpr_and_changepoint
from ml.driver_importance import train_driver_importance_model
from ml.forecaster import train_and_forecast_series
from ml.clustering_hazard import run_spatial_regime_clustering, detect_compound_glof_hazards

MODEL_DIR = Path(__file__).resolve().parent / "trained_models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)
METRICS_PATH = MODEL_DIR / "training_metrics.json"


def train_and_save_all_models() -> Dict[str, Any]:
    """
    Train and persist the complete ML suite:
    1. Spatial Regime Clustering (K-Means + PCA + StandardScaler) across all 9 basins & 15 glaciers.
    2. Regional Random Forest & HistGradientBoosting Driver Models (for all 9 basins).
    3. Regional Hybrid Ridge + Gradient Boosting Time-Series Forecasters.
    4. Gaussian Process Regression (GPR) Non-Linear Trend Models & Changepoints.
    5. Isolation Forest Compound Extreme GLOF Hazard Models.
    """
    summary_report: Dict[str, Any] = {
        "clustering": {},
        "driver_models": {},
        "forecasters": {},
        "nonlinear_gpr": {},
        "hazard_isolation_forest": {},
    }

    # 1. Train & Save Spatial Regime Clustering Model
    cluster_res = run_spatial_regime_clustering()
    joblib.dump(
        {
            "kmeans": cluster_res["kmeans_model"],
            "pca": cluster_res["pca_model"],
            "scaler": cluster_res["scaler"],
            "clustered_df": cluster_res["clustered_df"],
        },
        MODEL_DIR / "spatial_regime_clustering.joblib",
    )
    summary_report["clustering"] = {
        "n_entities_clustered": len(cluster_res["clustered_df"]),
        "silhouette_score": cluster_res["silhouette_score"],
        "pca_variance_explained_pct": cluster_res["pca_explained_variance_pct"],
    }

    # 2. Train & Save Regional Driver, Forecaster, GPR, and Isolation Forest Models
    core_targets = {
        "karakoram": ("snow_cover_modis", "t2m_merra2"),
        "hindu_kush": ("snow_cover_modis", "t2m_merra2"),
        "western_himalaya": ("snow_cover_modis", "t2m_merra2"),
        "hunza": ("snow_cover_modis", "t2m_merra2"),
        "upper_indus": ("swe_gldas", "precip_imerg"),
        "chitral": ("swe_gldas", "t2m_merra2"),
        "gilgit": ("snow_cover_modis", "runoff_gldas"),
        "astore": ("snow_cover_modis", "lst_modis"),
        "neelum": ("swe_gldas", "t2m_merra2"),
    }

    for r_id in PRESET_REGIONS.keys():
        driver_target, forecast_var = core_targets.get(r_id, ("snow_cover_modis", "t2m_merra2"))

        # A. Driver Importance Model (Random Forest + Gradient Boosting)
        drv = train_driver_importance_model(r_id, target_variable_id=driver_target)
        joblib.dump(
            {
                "rf_model": drv["rf_model"],
                "gb_model": drv["gb_model"],
                "importance_df": drv["importance_df"],
                "metrics": drv["metrics"],
            },
            MODEL_DIR / f"driver_rf_{r_id}_{driver_target}.joblib",
        )
        summary_report["driver_models"][r_id] = drv["metrics"]

        # B. Time-Series Forecaster + GPR Non-Linear Trend
        series_df, _ = load_investigation_series(r_id, forecast_var)
        fcst = train_and_forecast_series(series_df, horizon_months=36, holdout_months=36)
        joblib.dump(
            {
                "ridge_model": fcst["ridge_model"],
                "hgb_model": fcst["hgb_model"],
                "metrics": fcst["metrics"],
            },
            MODEL_DIR / f"forecaster_{r_id}_{forecast_var}.joblib",
        )
        summary_report["forecasters"][f"{r_id}_{forecast_var}"] = fcst["metrics"]

        gpr_res = fit_nonlinear_gpr_and_changepoint(series_df)
        joblib.dump(
            {
                "gpr_model": gpr_res["model"],
                "changepoint_year": gpr_res["changepoint_year"],
                "gpr_r2": gpr_res["gpr_r2"],
            },
            MODEL_DIR / f"gpr_{r_id}_{forecast_var}.joblib",
        )
        summary_report["nonlinear_gpr"][f"{r_id}_{forecast_var}"] = {
            "gpr_r2": gpr_res["gpr_r2"],
            "gpr_rmse": gpr_res["gpr_rmse"],
            "changepoint_year": gpr_res["changepoint_year"],
            "slope_before_decade": gpr_res["slope_before_decade"],
            "slope_after_decade": gpr_res["slope_after_decade"],
        }

        # C. Isolation Forest Compound GLOF Hazard Detector
        haz = detect_compound_glof_hazards(r_id)
        joblib.dump(
            {
                "isolation_forest": haz["isolation_forest_model"],
                "summary": haz["summary"],
            },
            MODEL_DIR / f"hazard_isoforest_{r_id}.joblib",
        )
        summary_report["hazard_isolation_forest"][r_id] = haz["summary"]

    METRICS_PATH.write_text(json.dumps(summary_report, indent=2), encoding="utf-8")
    return summary_report


def load_training_metrics_report() -> Dict[str, Any]:
    """Load saved training & evaluation metrics from disk (training if not yet generated)."""
    if METRICS_PATH.exists():
        try:
            return json.loads(METRICS_PATH.read_text(encoding="utf-8"))
        except Exception:
            pass
    return train_and_save_all_models()


if __name__ == "__main__":
    report = train_and_save_all_models()
    print("Trained and saved all ML models successfully!")
    print("Clustering Silhouette Score:", report["clustering"]["silhouette_score"])
    print("Hunza Forecaster Test R²:", report["forecasters"]["hunza_t2m_merra2"]["test_r2"])
    print("Karakoram Driver Model Test R²:", report["driver_models"]["karakoram"]["test_r2"])
