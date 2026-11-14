"""
Interactive 'Signal-vs-Noise' Statistical Honesty Sandbox payload builder.
"""
from typing import Dict, Any
from config.missions import SIGNAL_NOISE_PRESETS
from analytics.trend_tests import simulate_signal_vs_noise
from ui.charts import render_series_svg


def _fmt_p(p_val: float) -> str:
    return "p < 0.0001" if p_val < 0.0001 else f"p = {p_val:.4f}"


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
    p_str = _fmt_p(mk["p_value"])

    svg_anom = render_series_svg(
        values=s_df["anomaly"].tolist(),
        trend=s_df["anomaly_trend_sens"].tolist(),
        ci_low=s_df["anomaly_ci_low"].tolist(),
        ci_high=s_df["anomaly_ci_high"].tolist(),
        label_left=f"Synthetic anomaly ({years} yrs): Sen slope {sens['slope_per_decade']:+.2f}/decade",
        label_right=p_str,
        units="anomaly units",
        start_year=2026 - int(years) + 1,
        end_year=2026,
        sen_annotation=f"Sen: {sens['slope_per_decade']:+.2f}/dec",
    )

    return {
        "years": years,
        "true_slope_per_decade": true_slope_per_decade,
        "recovered_sens_slope": sens["slope_per_decade"],
        "ci_low_decade": sens["ci_low_decade"],
        "ci_high_decade": sens["ci_high_decade"],
        "p_value": mk["p_value"],
        "p_formatted": p_str,
        "tau": mk["tau"],
        "significant": mk["significant"],
        "verdict_text": (
            f"{years}-year window: Statistically significant ({p_str} < 0.05, recovered Sen slope {sens['slope_per_decade']:+.2f}/decade)"
            if mk["significant"]
            else f"{years}-year window: Not statistically significant yet ({p_str} >= 0.05, signal masked by noise)"
        ),
        "svg": svg_anom,
        "presets": SIGNAL_NOISE_PRESETS,
    }
