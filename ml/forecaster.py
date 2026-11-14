"""
Multi-Year Climate Time-Series ML Forecaster for Himalaya Trend Lab (Layer 4 ML).
Trains a Hybrid Ridge + HistGradientBoosting Autoregressive Forecaster using:
- Fourier seasonal harmonics (annual + semi-annual sin/cos waves)
- Secular & quadratic time trend features
- Lagged observations (lags 1, 2, 3, 6, 12 months) & rolling 12-month momentum
Evaluates on a 36-month holdout test set (reporting RMSE, MAE, MAPE, R²)
and forecasts the next 36 months (3 years) with calibrated 95% prediction intervals.
"""
from typing import Dict, Any
import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error


def _build_time_features(dates: pd.DatetimeIndex, start_year: int) -> np.ndarray:
    """Create deterministic calendar and Fourier harmonic features for any timestamps."""
    years = dates.year.values
    months = dates.month.values
    t_dec = (years + (months - 0.5) / 12.0 - start_year) / 10.0

    angle1 = 2.0 * np.pi * months / 12.0
    angle2 = 4.0 * np.pi * months / 12.0
    angle3 = 6.0 * np.pi * months / 12.0

    return np.column_stack([
        t_dec,
        np.sin(angle1),
        np.cos(angle1),
        np.sin(angle2),
        np.cos(angle2),
        np.sin(angle3),
        np.cos(angle3),
    ])


def _assemble_lag_matrix(values: np.ndarray, time_feats: np.ndarray) -> np.ndarray:
    """Combine deterministic time/Fourier features with autoregressive lag features."""
    s = pd.Series(values)
    lag1 = s.shift(1).bfill().values
    lag2 = s.shift(2).bfill().values
    lag3 = s.shift(3).bfill().values
    lag6 = s.shift(6).bfill().values
    lag12 = s.shift(12).bfill().values
    roll12 = s.rolling(12, min_periods=1).mean().bfill().values

    return np.column_stack([time_feats, lag1, lag2, lag3, lag6, lag12, roll12])


def train_and_forecast_series(
    df: pd.DataFrame,
    horizon_months: int = 36,
    holdout_months: int = 36,
) -> Dict[str, Any]:
    """
    Train the ML time-series forecaster on historical monthly observations,
    validate on the final `holdout_months` (3 years), and recursively project
    `horizon_months` (3 years) into the future with 95% prediction intervals.
    """
    s_df = df.sort_values("date").copy().reset_index(drop=True)
    dates = pd.DatetimeIndex(s_df["date"])
    y = s_df["value"].values.astype(float)
    start_year = int(dates.year.min())
    n = len(y)

    holdout = min(holdout_months, max(12, n // 5))
    split_idx = n - holdout

    time_feats = _build_time_features(dates, start_year)
    X_all = _assemble_lag_matrix(y, time_feats)

    # Skip first 12 months where lag-12 was backfilled
    train_start = min(12, split_idx // 4)
    X_train, y_train = X_all[train_start:split_idx], y[train_start:split_idx]
    X_test, y_test = X_all[split_idx:], y[split_idx:]

    # Ensemble: 60% Ridge Autoregression (preserves linear trend extrapolation) + 40% HistGradientBoosting
    ridge = Ridge(alpha=1.2, random_state=42)
    hgb = HistGradientBoostingRegressor(max_iter=120, max_depth=4, learning_rate=0.05, random_state=42)

    ridge.fit(X_train, y_train)
    hgb.fit(X_train, y_train)

    train_pred = 0.65 * ridge.predict(X_train) + 0.35 * hgb.predict(X_train)
    test_pred = 0.65 * ridge.predict(X_test) + 0.35 * hgb.predict(X_test)
    full_hist_pred = 0.65 * ridge.predict(X_all) + 0.35 * hgb.predict(X_all)

    # Compute holdout validation metrics
    test_rmse = float(np.sqrt(mean_squared_error(y_test, test_pred)))
    test_mae = float(mean_absolute_error(y_test, test_pred))
    test_r2 = float(r2_score(y_test, test_pred))
    denom_mape = np.maximum(1.0, np.abs(y_test))
    test_mape = float(np.mean(np.abs((y_test - test_pred) / denom_mape)) * 100.0)

    # Refit on 100% of historical data before generating future 36-month recursive projection
    ridge_full = Ridge(alpha=1.2, random_state=42).fit(X_all[train_start:], y[train_start:])
    hgb_full = HistGradientBoostingRegressor(max_iter=120, max_depth=4, learning_rate=0.05, random_state=42).fit(
        X_all[train_start:], y[train_start:]
    )

    last_date = dates[-1]
    future_dates = pd.date_range(last_date + pd.DateOffset(months=1), periods=horizon_months, freq="MS")
    future_time_feats = _build_time_features(future_dates, start_year)

    history_buffer = list(y)
    future_preds = []
    future_ci_low = []
    future_ci_high = []

    for h in range(horizon_months):
        tf = future_time_feats[h]
        lag1 = history_buffer[-1]
        lag2 = history_buffer[-2]
        lag3 = history_buffer[-3]
        lag6 = history_buffer[-6]
        lag12 = history_buffer[-12]
        roll12 = float(np.mean(history_buffer[-12:]))

        x_step = np.array([[*tf, lag1, lag2, lag3, lag6, lag12, roll12]])
        pred_step = float(0.65 * ridge_full.predict(x_step)[0] + 0.35 * hgb_full.predict(x_step)[0])
        history_buffer.append(pred_step)
        future_preds.append(pred_step)

        # Prediction interval widens modestly with forecast horizon
        step_sd = test_rmse * np.sqrt(1.0 + 0.025 * (h + 1))
        future_ci_low.append(pred_step - 1.96 * step_sd)
        future_ci_high.append(pred_step + 1.96 * step_sd)

    hist_table = pd.DataFrame({
        "date": dates,
        "year": dates.year,
        "month": dates.month,
        "actual": np.round(y, 3),
        "ml_fitted": np.round(full_hist_pred, 3),
        "segment": ["Train" if i < split_idx else "Test Holdout" for i in range(n)],
    })

    forecast_table = pd.DataFrame({
        "date": future_dates,
        "year": future_dates.year,
        "month": future_dates.month,
        "forecast": np.round(future_preds, 3),
        "ci_low_95": np.round(future_ci_low, 3),
        "ci_high_95": np.round(future_ci_high, 3),
        "segment": "ML Forecast",
    })

    return {
        "ridge_model": ridge_full,
        "hgb_model": hgb_full,
        "history_df": hist_table,
        "forecast_df": forecast_table,
        "metrics": {
            "train_r2": round(float(r2_score(y_train, train_pred)), 4),
            "test_r2": round(test_r2, 4),
            "test_rmse": round(test_rmse, 3),
            "test_mae": round(test_mae, 3),
            "test_mape_pct": round(test_mape, 2),
            "holdout_months": holdout,
            "horizon_months": horizon_months,
            "forecast_end_year": int(future_dates.year.max()),
            "projected_mean_change": round(float(np.mean(future_preds) - np.mean(y[-36:])), 3),
        },
    }
