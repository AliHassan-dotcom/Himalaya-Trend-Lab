"""
Rule-based Plain-Language Verdict Generator (Section 7.6).
Generates deterministic, reproducible scientific verdicts answering the 4 core questions:
1. What is changing?
2. Where is it changing?
3. How much is it changing (per decade and over the full record)?
4. Is the change statistically significant?
Also emits data-quality warnings for short records or cloud gaps.
"""
from typing import Dict, Any, List

from config.settings import MIN_YEARS_RECOMMENDED, MAX_MISSING_FRACTION_WARN


def generate_plain_language_verdict(
    analysis: Dict[str, Any],
    region_info: Dict[str, Any],
    var_info: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Generate a rule-based plain-language verdict and the 4 structured Detective Answers.
    """
    mk = analysis["primary_mk"]
    sens = analysis["sens_slope"]
    ols = analysis["ols_regression"]
    diag = analysis["seasonal_diagnostics"]

    alpha = analysis["alpha"]
    p_val = mk["p_value"]
    is_sig = mk["significant"]
    slope_dec = sens["slope_per_decade"]
    ci_low = sens["ci_low_decade"]
    ci_high = sens["ci_high_decade"]
    total_chg = sens["total_change_over_period"]

    var_name = var_info["name"]
    short_name = var_info["short_name"]
    units = var_info["units"]
    dec_units = var_info["decade_units"]
    reg_name = region_info["name"]
    start_yr = analysis["start_year"]
    end_yr = analysis["end_year"]
    n_years = analysis["n_years"]

    direction_word = "increased" if slope_dec > 0 else ("decreased" if slope_dec < 0 else "remained flat")
    tendency_word = "upward" if slope_dec > 0 else ("downward" if slope_dec < 0 else "flat")
    sign_prefix = "+" if slope_dec > 0 else ""

    # Format p-value cleanly
    p_str = "p < 0.0001" if p_val < 0.0001 else f"p = {p_val:.4f}"

    # Rule 1 & 2: Headline Verdict (Significant vs. Not Yet Significant)
    if is_sig:
        badge_status = "SIGNIFICANT INCREASE" if slope_dec > 0 else "SIGNIFICANT DECREASE"
        badge_color = "#dc2626" if (slope_dec > 0 and not var_info.get("invert_hazard", False)) or (slope_dec < 0 and var_info.get("invert_hazard", False)) else "#2563eb"
        headline = (
            f"{short_name} in the {reg_name} has {direction_word} by {sign_prefix}{slope_dec:.2f} {dec_units} "
            f"(95% CI: [{ci_low:+.2f}, {ci_high:+.2f}] {dec_units}) over {start_yr}–{end_yr}, "
            f"and the long-term trend is statistically significant ({p_str} < {alpha})."
        )
    else:
        badge_status = "NO SIGNIFICANT TREND YET"
        badge_color = "#64748b"
        headline = (
            f"{short_name} in the {reg_name} shows a slight {tendency_word} tendency "
            f"({sign_prefix}{slope_dec:.2f} {dec_units}, 95% CI: [{ci_low:+.2f}, {ci_high:+.2f}]), "
            f"but the trend is NOT yet statistically significant ({p_str} >= {alpha}). "
            f"Year-to-year mountain variability currently outweighs the long-term signal."
        )

    # Four Core Detective Questions (Section 1)
    four_questions = {
        "what_is_changing": (
            f"{var_name} ({units}), measured via {var_info['source_mission']}. "
            f"After removing the typical seasonal cycle (which swings by {diag['seasonal_peak_to_trough_range']:.1f} {units} "
            f"between {diag['trough_month_name']} and {diag['peak_month_name']}), the underlying anomaly shows a "
            f"{tendency_word} slope."
        ),
        "where_is_it_changing": (
            f"{reg_name} ({region_info['parent_range']}, mean elevation {region_info['mean_elevation_m']:,} m, "
            f"{region_info['glacier_area_km2']:,} km² of glacier ice / {region_info['glacier_fraction_pct']}% glacier cover)."
        ),
        "how_much_is_it_changing": (
            f"Sen's robust rate of change is {sign_prefix}{slope_dec:.3f} {dec_units} "
            f"(OLS linear slope: {ols['slope_per_decade']:+.3f} {dec_units}), corresponding to a cumulative shift of "
            f"{total_chg:+.2f} {units} across the {n_years:.1f}-year record ({start_yr}–{end_yr})."
        ),
        "is_it_significant": (
            f"{'Yes — Statistically Significant' if is_sig else 'No — Not Statistically Significant Yet'}: "
            f"{mk['test_name']} yields tau = {mk['tau']:+.3f} and {p_str} at threshold alpha = {alpha}. "
            f"The 95% confidence interval [{ci_low:+.3f}, {ci_high:+.3f}] "
            f"{'does not cross zero, confirming a robust monotonic shift.' if is_sig else 'crosses or borders zero, meaning random climate variability cannot yet be ruled out.'}"
        ),
    }

    # Autocorrelation & Data-Quality Warnings (Section 7.4 & 7.6)
    warnings: List[str] = []
    if n_years < MIN_YEARS_RECOMMENDED:
        warnings.append(
            f"Short Record Warning: The selected period spans {n_years:.1f} years ({start_yr}–{end_yr}). "
            f"Climatologists generally recommend at least {MIN_YEARS_RECOMMENDED}–30 years to separate long-term trends from decadal oscillations."
        )
    if analysis["cloud_gap_fraction"] > MAX_MISSING_FRACTION_WARN:
        warnings.append(
            f"Cloud Gap Note: {analysis['cloud_gap_fraction']*100:.1f}% of monthly optical satellite observations required cloud-gap interpolation."
        )

    mod_mk = analysis["mk_hamed_rao"]
    if mod_mk.get("autocorrelation_detected", False):
        autocorr_note = (
            f"Serial Autocorrelation Detected (Lag-1 r = {mod_mk['lag1_autocorr']:+.2f}): "
            f"Monthly climate memory inflated raw variance by {mod_mk['variance_inflation_factor']:.2f}x. "
            f"The Hamed-Rao Modified Mann-Kendall test automatically adjusted the p-value "
            f"(from raw p = {analysis['mk_original']['p_value']:.4f} to adjusted p = {mod_mk['p_value']:.4f}) to prevent false positives."
        )
    else:
        autocorr_note = (
            f"Low Serial Autocorrelation (Lag-1 r = {mod_mk['lag1_autocorr']:+.2f}, VIF = {mod_mk['variance_inflation_factor']:.2f}x): "
            f"Original and Hamed-Rao Modified Mann-Kendall tests closely agree."
        )

    return {
        "headline": headline,
        "badge_status": badge_status,
        "badge_color": badge_color,
        "four_questions": four_questions,
        "autocorrelation_note": autocorr_note,
        "warnings": warnings,
        "attribution_disclaimer": (
            "Scientific Note: A statistically significant trend proves that a physical change is occurring "
            "above background variability, but statistical trend tests alone detect change—not physical attribution."
        ),
    }
