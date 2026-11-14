"""
Statistical Trend Estimation & Significance Testing Engine (Sections 7.3 & 7.4).
Implements:
- Sen's Slope (Theil-Sen robust estimator) per decade + 95% confidence interval
- Ordinary Least Squares (OLS) linear regression slope + t-test + 95% confidence interval
- Original Mann-Kendall non-parametric monotonic trend test
- Hamed-Rao (1998) Modified Mann-Kendall test for serially autocorrelated climate data
- Hirsch-Slack Seasonal Mann-Kendall test on raw monthly data
- Interactive Signal-vs-Noise Synthetic Simulator
"""
from typing import Dict, Any, Optional
import numpy as np
import pandas as pd
from scipy import stats

from analytics.seasonal import deseasonalize_series


def _mann_kendall_s_and_var(y: np.ndarray) -> Dict[str, float]:
    """Compute Mann-Kendall S statistic, tie-adjusted variance Var(S), and Kendall's tau."""
    x = np.asarray(y, dtype=float)
    x = x[~np.isnan(x)]
    n = len(x)
    if n < 3:
        return {"n": n, "s": 0.0, "var_s": 1.0, "tau": 0.0}

    # Vectorized pairwise sign matrix: j > i
    diff = x[None, :] - x[:, None]
    iu = np.triu_indices(n, k=1)
    s = float(np.sum(np.sign(diff[iu])))

    # Tie correction for variance
    _, counts = np.unique(x, return_counts=True)
    tie_term = np.sum(counts * (counts - 1) * (2 * counts + 5))
    var_s = float((n * (n - 1) * (2 * n + 5) - tie_term) / 18.0)
    var_s = max(1e-9, var_s)

    denom = 0.5 * n * (n - 1)
    tau = float(s / denom) if denom > 0 else 0.0
    return {"n": n, "s": s, "var_s": var_s, "tau": tau}


def _z_and_p_from_s(s: float, var_s: float) -> Dict[str, float]:
    """Compute continuity-corrected Z-score and two-sided p-value from S and Var(S)."""
    if s > 0:
        z = (s - 1.0) / np.sqrt(var_s)
    elif s < 0:
        z = (s + 1.0) / np.sqrt(var_s)
    else:
        z = 0.0
    p_val = float(2.0 * (1.0 - stats.norm.cdf(abs(z))))
    return {"z": float(z), "p_value": p_val}


def mann_kendall_original(y: np.ndarray, alpha: float = 0.05) -> Dict[str, Any]:
    """
    Standard non-parametric Mann-Kendall test for monotonic trend (assuming independent observations).
    """
    base = _mann_kendall_s_and_var(y)
    zp = _z_and_p_from_s(base["s"], base["var_s"])
    sig = zp["p_value"] < alpha
    direction = "increasing" if base["s"] > 0 else ("decreasing" if base["s"] < 0 else "no trend")
    return {
        "test_name": "Original Mann-Kendall Test",
        "n": base["n"],
        "s_stat": round(base["s"], 1),
        "var_s": round(base["var_s"], 2),
        "tau": round(base["tau"], 4),
        "z_stat": round(zp["z"], 4),
        "p_value": round(zp["p_value"], 6),
        "significant": bool(sig),
        "direction": direction if sig else f"non-significant ({direction} tendency)",
    }


def mann_kendall_hamed_rao(
    y: np.ndarray,
    alpha: float = 0.05,
    max_lag: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Hamed & Rao (1998) Modified Mann-Kendall test accounting for serial autocorrelation.
    Monthly climate and cryosphere series exhibit positive lag-1 autocorrelation, which
    can artificially inflate significance in the standard MK test. Hamed-Rao estimates
    the effective sample size Correction Factor (n / n_s*) from detrended rank autocorrelations.
    """
    x = np.asarray(y, dtype=float)
    x = x[~np.isnan(x)]
    n = len(x)
    base = _mann_kendall_s_and_var(x)
    if n < 10:
        orig = mann_kendall_original(x, alpha=alpha)
        orig["test_name"] = "Hamed-Rao Modified Mann-Kendall"
        orig["variance_inflation_factor"] = 1.0
        orig["lag1_autocorr"] = 0.0
        orig["autocorrelation_detected"] = False
        return orig

    # Detrend series using Sen's median slope before checking rank autocorrelation
    t = np.arange(n, dtype=float)
    res_theil = stats.theilslopes(x, t)
    detrended = x - res_theil.slope * t
    ranks = stats.rankdata(detrended)
    ranks_centered = ranks - np.mean(ranks)
    denom = np.sum(ranks_centered ** 2)

    # Lag-1 autocorrelation of detrended series
    lag1_r = float(np.sum(ranks_centered[:-1] * ranks_centered[1:]) / denom) if denom > 0 else 0.0
    sig_bound = 1.96 / np.sqrt(n)  # 95% significance threshold for autocorrelation

    if max_lag is None:
        max_lag = min(12, max(3, n // 4))

    correction_sum = 0.0
    for k in range(1, max_lag + 1):
        if n - k <= 2 or denom <= 0:
            break
        rho_k = float(np.sum(ranks_centered[:-k] * ranks_centered[k:]) / denom)
        if abs(rho_k) > sig_bound:
            weight = (n - k) * (n - k - 1) * (n - k - 2)
            correction_sum += weight * rho_k

    n_denom = n * (n - 1) * (n - 2)
    vif = 1.0 + (2.0 / n_denom) * correction_sum if n_denom > 0 else 1.0
    # Bound variance inflation factor to positive physical range
    vif = float(np.clip(vif, 0.5, 10.0))

    modified_var_s = base["var_s"] * vif
    zp = _z_and_p_from_s(base["s"], modified_var_s)
    sig = zp["p_value"] < alpha
    direction = "increasing" if base["s"] > 0 else ("decreasing" if base["s"] < 0 else "no trend")

    return {
        "test_name": "Hamed-Rao Modified Mann-Kendall (Autocorrelation-Adjusted)",
        "n": n,
        "s_stat": round(base["s"], 1),
        "var_s_original": round(base["var_s"], 2),
        "var_s_modified": round(modified_var_s, 2),
        "variance_inflation_factor": round(vif, 3),
        "lag1_autocorr": round(lag1_r, 3),
        "autocorrelation_detected": bool(abs(lag1_r) > sig_bound),
        "tau": round(base["tau"], 4),
        "z_stat": round(zp["z"], 4),
        "p_value": round(zp["p_value"], 6),
        "significant": bool(sig),
        "direction": direction if sig else f"non-significant ({direction} tendency)",
    }


def seasonal_mann_kendall(df: pd.DataFrame, alpha: float = 0.05) -> Dict[str, Any]:
    """
    Hirsch, Slack & Smith (1982) Seasonal Mann-Kendall test.
    Computes S_m and Var(S_m) separately within each of the 12 calendar months
    so winter is only compared to winter and summer only to summer.
    """
    s_total = 0.0
    var_total = 0.0
    n_total = 0
    denom_total = 0.0

    for m in range(1, 13):
        sub = df[df["month"] == m]["value"].dropna().values
        if len(sub) >= 3:
            res_m = _mann_kendall_s_and_var(sub)
            s_total += res_m["s"]
            var_total += res_m["var_s"]
            n_total += res_m["n"]
            denom_total += 0.5 * res_m["n"] * (res_m["n"] - 1)

    var_total = max(1e-9, var_total)
    zp = _z_and_p_from_s(s_total, var_total)
    tau = s_total / denom_total if denom_total > 0 else 0.0
    sig = zp["p_value"] < alpha

    return {
        "test_name": "Seasonal Mann-Kendall Test (Hirsch-Slack)",
        "n": n_total,
        "s_stat": round(s_total, 1),
        "var_s": round(var_total, 2),
        "tau": round(float(tau), 4),
        "z_stat": round(zp["z"], 4),
        "p_value": round(zp["p_value"], 6),
        "significant": bool(sig),
    }


def compute_sens_slope(
    t_years: np.ndarray,
    y: np.ndarray,
    alpha: float = 0.05,
) -> Dict[str, Any]:
    """
    Compute Sen's non-parametric robust slope (Theil-Sen estimator) and 100*(1-alpha)%
    confidence interval, scaled to rate of change per decade.
    """
    res = stats.theilslopes(y, t_years, alpha=alpha)
    slope_yr = float(res.slope)
    intercept = float(res.intercept)
    low_yr = float(res.low_slope)
    high_yr = float(res.high_slope)

    span_years = float(t_years[-1] - t_years[0]) if len(t_years) > 1 else 1.0
    total_change = slope_yr * span_years

    # Fitted trend line and confidence band around the median time
    t_mid = float(np.median(t_years))
    y_mid = float(np.median(y))
    fitted_line = y_mid + slope_yr * (t_years - t_mid)
    band_low = y_mid + low_yr * (t_years - t_mid)
    band_high = y_mid + high_yr * (t_years - t_mid)

    return {
        "slope_per_year": round(slope_yr, 5),
        "slope_per_decade": round(slope_yr * 10.0, 4),
        "ci_low_decade": round(low_yr * 10.0, 4),
        "ci_high_decade": round(high_yr * 10.0, 4),
        "intercept": round(intercept, 4),
        "total_change_over_period": round(total_change, 3),
        "fitted_line": np.round(fitted_line, 4),
        "ci_band_low": np.round( np.minimum(band_low, band_high), 4),
        "ci_band_high": np.round(np.maximum(band_low, band_high), 4),
    }


def compute_ols_trend(
    t_years: np.ndarray,
    y: np.ndarray,
    alpha: float = 0.05,
) -> Dict[str, Any]:
    """
    Compute Ordinary Least Squares (OLS) linear regression slope, Student's t-test
    p-value, R², and 100*(1-alpha)% confidence interval per decade (Section 7.3 & 7.4).
    """
    n = len(y)
    reg = stats.linregress(t_years, y)
    dof = max(1, n - 2)
    t_crit = float(stats.t.ppf(1.0 - alpha / 2.0, dof))
    t_stat = float(reg.slope / reg.stderr) if reg.stderr and reg.stderr > 0 else 0.0

    ci_low_yr = reg.slope - t_crit * reg.stderr
    ci_high_yr = reg.slope + t_crit * reg.stderr
    fitted = reg.intercept + reg.slope * t_years

    return {
        "slope_per_year": round(float(reg.slope), 5),
        "slope_per_decade": round(float(reg.slope * 10.0), 4),
        "ci_low_decade": round(float(ci_low_yr * 10.0), 4),
        "ci_high_decade": round(float(ci_high_yr * 10.0), 4),
        "std_err_decade": round(float(reg.stderr * 10.0), 4),
        "t_stat": round(t_stat, 4),
        "p_value": round(float(reg.pvalue), 6),
        "r_value": round(float(reg.rvalue), 4),
        "r_squared": round(float(reg.rvalue ** 2), 4),
        "significant": bool(reg.pvalue < alpha),
        "fitted_line": np.round(fitted, 4),
    }


def run_full_trend_analysis(
    df: pd.DataFrame,
    alpha: float = 0.05,
    use_modified_mk: bool = True,
) -> Dict[str, Any]:
    """
    Execute the complete Himalaya Trend Lab statistical pipeline on a monthly series:
    1. Deseasonalize (12-month climatology + STL decomposition).
    2. Compute Sen's Slope & 95% confidence interval on deseasonalized anomalies (and raw offset).
    3. Compute OLS Regression & t-test on deseasonalized anomalies.
    4. Run Hamed-Rao Modified Mann-Kendall (primary), Original Mann-Kendall, and Seasonal MK.
    5. Package enriched DataFrame + statistics dictionary.
    """
    seasonal_pack = deseasonalize_series(df)
    enriched_df = seasonal_pack["series"]
    clim_df = seasonal_pack["climatology"]
    diag = seasonal_pack["diagnostics"]

    # Fractional calendar year coordinate
    t_years = enriched_df["year"].values + (enriched_df["month"].values - 0.5) / 12.0
    anomalies = enriched_df["anomaly"].values
    raw_values = enriched_df["value"].values
    mean_baseline = float(np.nanmean(raw_values))

    sens = compute_sens_slope(t_years, anomalies, alpha=alpha)
    ols = compute_ols_trend(t_years, anomalies, alpha=alpha)

    mk_orig = mann_kendall_original(anomalies, alpha=alpha)
    mk_mod = mann_kendall_hamed_rao(anomalies, alpha=alpha)
    mk_seasonal = seasonal_mann_kendall(enriched_df, alpha=alpha)

    primary_mk = mk_mod if use_modified_mk else mk_orig

    # Attach trend lines to enriched_df for interactive plotting
    enriched_df["anomaly_trend_sens"] = sens["fitted_line"]
    enriched_df["anomaly_ci_low"] = sens["ci_band_low"]
    enriched_df["anomaly_ci_high"] = sens["ci_band_high"]
    enriched_df["anomaly_trend_ols"] = ols["fitted_line"]

    # Raw-scale trend line (baseline mean + anomaly Sen's trend)
    enriched_df["raw_trend_sens"] = np.round(mean_baseline + sens["fitted_line"], 4)
    enriched_df["raw_ci_low"] = np.round(mean_baseline + sens["ci_band_low"], 4)
    enriched_df["raw_ci_high"] = np.round(mean_baseline + sens["ci_band_high"], 4)

    n_points = len(enriched_df)
    n_years = round(float(t_years[-1] - t_years[0]), 1) if n_points > 1 else 0.0
    cloud_interp_fraction = float(np.mean(enriched_df.get("quality_flag", "good") != "good"))

    return {
        "series": enriched_df,
        "climatology": clim_df,
        "seasonal_diagnostics": diag,
        "sens_slope": sens,
        "ols_regression": ols,
        "primary_mk": primary_mk,
        "mk_original": mk_orig,
        "mk_hamed_rao": mk_mod,
        "mk_seasonal": mk_seasonal,
        "alpha": alpha,
        "use_modified_mk": use_modified_mk,
        "n_months": n_points,
        "n_years": n_years,
        "start_year": int(enriched_df["year"].min()),
        "end_year": int(enriched_df["year"].max()),
        "mean_value": round(mean_baseline, 3),
        "cloud_gap_fraction": round(cloud_interp_fraction, 4),
    }


def simulate_signal_vs_noise(
    years: int = 25,
    true_slope_per_decade: float = 0.30,
    noise_std: float = 0.85,
    seasonal_amplitude: float = 11.0,
    missing_pct: float = 2.0,
    alpha: float = 0.05,
    seed: int = 42,
) -> Dict[str, Any]:
    """
    Interactive 'Signal-vs-Noise' Statistical Honesty Sandbox generator.
    Demonstrates live how record length (years), noise, seasonal amplitude, and
    cloud gaps govern whether a real physical trend passes statistical significance.
    """
    rng = np.random.default_rng(seed)
    dates = pd.date_range("1985-01-01", periods=int(years * 12), freq="MS")
    n = len(dates)
    t_years = dates.year.values + (dates.month.values - 0.5) / 12.0
    t_decades = (t_years - t_years[0]) / 10.0

    true_signal = true_slope_per_decade * t_decades
    seasonal = seasonal_amplitude * np.cos(2 * np.pi * (dates.month.values - 7.0) / 12.0)

    # AR(1) mountain weather noise
    noise = np.zeros(n)
    phi = 0.32
    eps = rng.normal(0.0, noise_std * np.sqrt(1 - phi ** 2), n)
    for i in range(1, n):
        noise[i] = phi * noise[i - 1] + eps[i]

    y = 10.0 + true_signal + seasonal + noise

    # Simulate missing satellite cloud gaps
    if missing_pct > 0:
        gap_mask = rng.random(n) < (missing_pct / 100.0)
        y_gapped = y.copy()
        y_gapped[gap_mask] = np.nan
        y_interp = pd.Series(y_gapped).interpolate(limit_direction="both").values
    else:
        y_interp = y

    df_sim = pd.DataFrame({
        "date": dates,
        "year": dates.year.values,
        "month": dates.month.values,
        "value": np.round(y_interp, 4),
        "true_signal": np.round(true_signal, 4),
        "quality_flag": "good",
    })

    # Compare naive raw regression vs. proper deseasonalized trend analysis
    raw_ols = compute_ols_trend(t_years, y_interp, alpha=alpha)
    full_res = run_full_trend_analysis(df_sim, alpha=alpha, use_modified_mk=True)

    return {
        "analysis": full_res,
        "raw_naive_ols": raw_ols,
        "true_slope_per_decade": true_slope_per_decade,
        "recovered_sens_slope": full_res["sens_slope"]["slope_per_decade"],
        "slope_error": round(abs(full_res["sens_slope"]["slope_per_decade"] - true_slope_per_decade), 4),
    }
