"""
Spatial Trend Map & Stippling Payload Builder for the Hatchable Frontend.
"""
from typing import Dict, Any
from data import generate_spatial_grid_data
from analytics.spatial_trends import analyze_spatial_trend_grid, compute_elevation_band_trends


def build_spatial_map_payload(
    region_id: str,
    variable_id: str,
    base_slope_decade: float,
    base_p_value: float,
    alpha: float = 0.05,
    glacier_only: bool = False,
) -> Dict[str, Any]:
    """Build JSON-ready spatial grid stippling and elevation band breakdown."""
    raw_grid = generate_spatial_grid_data(region_id, variable_id, glacier_only=glacier_only)
    spatial_res = analyze_spatial_trend_grid(raw_grid, alpha=alpha, apply_fdr=True, glacier_only=glacier_only)
    elev_df = compute_elevation_band_trends(region_id, variable_id, base_slope_decade, base_p_value)

    return {
        "summary": spatial_res["summary"],
        "stipple_points": spatial_res["stipple_points"][:36],
        "elevation_bands": elev_df.to_dict(orient="records"),
    }
