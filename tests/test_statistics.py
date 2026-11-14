"""
Synthetic Series & Scientific Validation Unit Tests (Section 10).
Tests:
1. Pure white noise returns "not significant" (p >= 0.05).
2. Known linear trend (+0.50 / decade) is recovered by Sen's slope and returns "significant" (p < 0.001).
3. Strong seasonal cycle + weak trend is isolated accurately by climatology removal.
4. Autocorrelated red noise triggers Hamed-Rao variance inflation factor (VIF > 1.0).
5. Benjamini-Hochberg False Discovery Rate (FDR) controls false positives on spatial grids.
6. Rule-based plain-language verdict generator produces accurate badges.
"""
import numpy as np
import pandas as pd

from config.regions import get_region
from config.variables import get_variable
from analytics.seasonal import deseasonalize_series
from analytics.trend_tests import (
    mann_kendall_original,
    mann_kendall_hamed_rao,
    compute_sens_slope,
    run_full_trend_analysis,
)
from analytics.spatial_trends import benjamini_hochberg_fdr
from analytics.verdict import generate_plain_language_verdict


def test_pure_noise_returns_not_significant():
    """Verify that pure stationary Gaussian noise returns not significant (Section 10)."""
    rng = np.random.default_rng(12345)
    y_noise = rng.normal(0.0, 1.0, 300)
    res_orig = mann_kendall_original(y_noise, alpha=0.05)
    res_mod = mann_kendall_hamed_rao(y_noise, alpha=0.05)

    assert res_orig["significant"] is False
    assert res_orig["p_value"] >= 0.05
    assert res_mod["significant"] is False
    assert abs(res_orig["tau"]) < 0.10


def test_known_linear_trend_recovered_by_sens_slope():
    """Verify that a synthetic series with +0.50/decade slope is accurately recovered."""
    rng = np.random.default_rng(99)
    n_months = 360  # 30 years
    t_years = 1995.0 + np.arange(n_months) / 12.0
    true_slope_decade = 0.50
    y = 5.0 + (true_slope_decade / 10.0) * (t_years - 1995.0) + rng.normal(0.0, 0.15, n_months)

    sens = compute_sens_slope(t_years, y, alpha=0.05)
    mk = mann_kendall_hamed_rao(y, alpha=0.05)

    assert mk["significant"] is True
    assert mk["p_value"] < 0.001
    assert abs(sens["slope_per_decade"] - true_slope_decade) < 0.04
    assert sens["ci_low_decade"] > 0.40


def test_seasonal_cycle_removal_isolates_anomaly_trend():
    """Verify that removing a huge seasonal cycle (+-15°C) reveals a subtle +0.30°C/decade trend."""
    dates = pd.date_range("2000-01-01", periods=240, freq="MS")
    t_decades = np.arange(len(dates)) / 120.0
    seasonal = 15.0 * np.cos(2 * np.pi * (dates.month.values - 7) / 12.0)
    true_trend = 0.30 * t_decades

    df = pd.DataFrame({
        "date": dates,
        "year": dates.year.values,
        "month": dates.month.values,
        "value": 10.0 + seasonal + true_trend,
        "quality_flag": "good",
    })

    out = deseasonalize_series(df)
    anom = out["series"]["anomaly"].values
    t_years = dates.year.values + (dates.month.values - 0.5) / 12.0
    sens = compute_sens_slope(t_years, anom)

    assert out["diagnostics"]["seasonal_peak_to_trough_range"] > 28.0
    assert abs(sens["slope_per_decade"] - 0.30) < 0.01


def test_hamed_rao_autocorrelation_inflation():
    """Verify Hamed-Rao detects strong positive AR(1) serial correlation and inflates variance."""
    rng = np.random.default_rng(7)
    n = 240
    ar_series = np.zeros(n)
    phi = 0.70
    for i in range(1, n):
        ar_series[i] = phi * ar_series[i - 1] + rng.normal(0, 0.5)

    res = mann_kendall_hamed_rao(ar_series, alpha=0.05)
    assert res["autocorrelation_detected"] is True
    assert res["lag1_autocorr"] > 0.40
    assert res["variance_inflation_factor"] > 1.30


def test_benjamini_hochberg_fdr_control():
    """Verify Benjamini-Hochberg FDR distinguishes true small p-values from random noise p-values."""
    p_grid = np.array([
        [0.0001, 0.0005, 0.0020],
        [0.0420, 0.2500, 0.6800],
        [0.8100, 0.9200, 0.4500],
    ])
    fdr = benjamini_hochberg_fdr(p_grid, alpha=0.05)
    sig_mask = fdr["significant_mask"]

    # First row has strong true signals (p <= 0.002) -> should pass FDR
    assert bool(sig_mask[0, 0]) is True
    assert bool(sig_mask[0, 1]) is True
    # Borderline p=0.042 out of 9 tests fails BH threshold (4/9 * 0.05 = 0.0222)
    assert bool(sig_mask[1, 0]) is False


def test_verdict_generator_rules():
    """Verify plain-language verdict generator outputs deterministic statuses."""
    dates = pd.date_range("1990-01-01", periods=360, freq="MS")
    t_dec = np.arange(len(dates)) / 120.0
    df = pd.DataFrame({
        "date": dates,
        "year": dates.year.values,
        "month": dates.month.values,
        "value": 5.0 + 10.0 * np.cos(2 * np.pi * dates.month.values / 12.0) + 0.40 * t_dec,
        "quality_flag": "good",
    })
    analysis = run_full_trend_analysis(df, alpha=0.05)
    verdict = generate_plain_language_verdict(
        analysis,
        get_region("hunza"),
        get_variable("t2m_merra2"),
    )
    assert verdict["badge_status"] == "SIGNIFICANT INCREASE"
    assert "statistically significant" in verdict["headline"]
    assert len(verdict["four_questions"]) == 4
