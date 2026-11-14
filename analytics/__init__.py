"""
Statistical, Glaciological & Impact Engine for Himalaya Trend Lab (Layer 3).
"""
from analytics.seasonal import (
    MONTH_NAMES,
    compute_monthly_climatology,
    deseasonalize_series,
)
from analytics.trend_tests import (
    mann_kendall_original,
    mann_kendall_hamed_rao,
    seasonal_mann_kendall,
    compute_sens_slope,
    compute_ols_trend,
    run_full_trend_analysis,
    simulate_signal_vs_noise,
)
from analytics.spatial_trends import (
    benjamini_hochberg_fdr,
    analyze_spatial_trend_grid,
    compute_elevation_band_trends,
)
from analytics.freezing_level import (
    compute_freezing_level_migration,
    compute_dark_ice_albedo_melt,
)
from analytics.water_security import (
    simulate_indus_water_security,
)
from analytics.teleconnections import (
    analyze_teleconnections,
    compute_multi_sensor_validation,
)
from analytics.verdict import (
    generate_plain_language_verdict,
)

__all__ = [
    "MONTH_NAMES",
    "compute_monthly_climatology",
    "deseasonalize_series",
    "mann_kendall_original",
    "mann_kendall_hamed_rao",
    "seasonal_mann_kendall",
    "compute_sens_slope",
    "compute_ols_trend",
    "run_full_trend_analysis",
    "simulate_signal_vs_noise",
    "benjamini_hochberg_fdr",
    "analyze_spatial_trend_grid",
    "compute_elevation_band_trends",
    "compute_freezing_level_migration",
    "compute_dark_ice_albedo_melt",
    "simulate_indus_water_security",
    "analyze_teleconnections",
    "compute_multi_sensor_validation",
    "generate_plain_language_verdict",
]
