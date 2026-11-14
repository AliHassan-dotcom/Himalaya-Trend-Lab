"""
Machine Learning Lab package for Himalaya Trend Lab (Layer 4).
Exposes Non-Linear GPR Trend & Changepoint Detection, Explainable Random Forest
Driver Importance, Hybrid Time-Series Forecasting, Unsupervised Spatial Regime
Clustering, Isolation Forest GLOF Hazard Detection, and Pre-Trained Model Artifacts.
"""
from ml.nonlinear_trend import fit_nonlinear_gpr_and_changepoint
from ml.driver_importance import (
    DRIVER_FEATURE_LABELS,
    train_driver_importance_model,
)
from ml.forecaster import train_and_forecast_series
from ml.clustering_hazard import (
    run_spatial_regime_clustering,
    detect_compound_glof_hazards,
)
from ml.train_models import (
    MODEL_DIR,
    METRICS_PATH,
    train_and_save_all_models,
    load_training_metrics_report,
)

__all__ = [
    "fit_nonlinear_gpr_and_changepoint",
    "DRIVER_FEATURE_LABELS",
    "train_driver_importance_model",
    "train_and_forecast_series",
    "run_spatial_regime_clustering",
    "detect_compound_glof_hazards",
    "MODEL_DIR",
    "METRICS_PATH",
    "train_and_save_all_models",
    "load_training_metrics_report",
]
