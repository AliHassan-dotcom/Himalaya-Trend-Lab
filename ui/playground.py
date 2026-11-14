"""
Interactive 'Signal-vs-Noise' Statistical Honesty Sandbox payload builder.
"""
from typing import Dict, Any
from config.missions import SIGNAL_NOISE_PRESETS
from analytics.trend_tests import simulate_signal_vs_noise
from ui.charts import render_series_svg


def run_sandbox_simulation(
    years: int = 30,
    true_slope_per_decade: float = 0.30,
    noise_std: float = 0.85,
    missing_pct: float = 2.0,
) -> Dict[str, Any]:
    """Run live synthetic Mann-Kendall & Sen's slope simulation for the Methodology sandbox."""
    sim = simulate_signal_vs_noise(
        years=years,
        true_slope_per_decade=true_slope_per_decade,
        noise_std=noise_std,
        missing_pct=missing_pct,
    )
    res = sim["analysis"]
    mk = res["primary_mk"]
    sens = res["sens_slope"]
    s_df = res["series"]

    svg_anom = render_series_svg(
        values=s_df["anomaly"].tolist(),
        trend=s_df["anomaly_trend_sens"].tolist(),
        ci_low=s_df["anomaly_ci_low"].tolist(),
        ci_high=s_df["anomaly_ci_high"].tolist(),
        label_left=f"SYNTHETIC ANOMALY ({years} YRS) · SEN SLOPE {sens['slope_per_decade']:+.2f}/DEC",
        label_right=f"p = {mk['p_value']:.4f}",
    )

    return {
        "years": years,
        "true_slope_per_decade": true_slope_per_decade,
        "recovered_sens_slope": sens["slope_per_decade"],
        "ci_low_decade": sens["ci_low_decade"],
        "ci_high_decade": sens["ci_high_decade"],
        "p_value": mk["p_value"],
        "tau": mk["tau"],
        "significant": mk["significant"],
        "verdict_text": (
            f"{years} years → Statistically Significant (p = {mk['p_value']:.4f} < 0.05 · Sen's slope {sens['slope_per_decade']:+.2f}/dec)"
            if mk["significant"]
            else f"{years} years → Not Significant Yet (p = {mk['p_value']:.4f} >= 0.05 · Signal buried in noise)"
        ),
        "svg": svg_anom,
        "presets": SIGNAL_NOISE_PRESETS,
    }
