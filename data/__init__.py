"""
Unified Data Ingestion & Caching Layer for Himalaya Trend Lab.
Coordinates pre-cached baseline series, live Meteomatics Weather API queries,
live NASA POWER (MERRA-2) queries, spatial trend grids, and 7-day GLOF forecasts.
"""
from typing import Dict, Any, Optional, Tuple
import pandas as pd

from config.regions import PRESET_REGIONS, get_region
from config.variables import VARIABLES_CATALOGUE, get_variable
from data.cache_manager import (
    make_cache_key,
    get_cached_dataframe,
    save_cached_dataframe,
    get_quota_status,
)
from data.generator import (
    generate_teleconnection_series,
    generate_regional_series,
    generate_multivariate_series,
    generate_spatial_grid_data,
)
from data.meteomatics_client import (
    build_meteomatics_url,
    fetch_meteomatics_monthly_series,
)
from data.nasa_client import (
    build_nasa_power_url,
    fetch_nasa_power_monthly_series,
)
from data.forecast_client import (
    fetch_glacier_7day_forecast,
    get_all_glaciers_radar_summary,
)


def load_investigation_series(
    region_id: str,
    variable_id: str,
    start_year: Optional[int] = None,
    end_year: Optional[int] = None,
    glacier_only: bool = False,
    custom_region: Optional[Dict[str, Any]] = None,
    prefer_live_api: str = "cached",  # "cached", "meteomatics", or "nasa_power"
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Primary data loader for Detective Mode, Compare Mode, and Demo Walkthroughs.
    1. Checks if user requested live Meteomatics or NASA POWER API fetch.
    2. Otherwise loads or generates the calibrated pre-cached monthly series
       and stores it in `data/cached/` for instant zero-latency execution.
    """
    region = custom_region if custom_region else get_region(region_id)
    var_info = get_variable(variable_id)
    s_year = max(1981, start_year or var_info["start_year"])
    e_year = min(2026, end_year or var_info["end_year"])

    # Option 1: Live Meteomatics API fetch
    if prefer_live_api == "meteomatics":
        live_df, meta = fetch_meteomatics_monthly_series(
            region_id=region["id"],
            variable_id=variable_id,
            start_year=s_year,
            end_year=e_year,
            custom_region=custom_region,
        )
        if live_df is not None and len(live_df) >= 24:
            tele = generate_teleconnection_series(s_year, e_year)
            merged = pd.merge(live_df, tele[["date", "nao_index", "enso_index", "iod_index"]], on="date", how="left")
            return merged, meta

    # Option 2: Live NASA POWER (MERRA-2) API fetch
    elif prefer_live_api == "nasa_power":
        live_df, meta = fetch_nasa_power_monthly_series(
            region_id=region["id"],
            variable_id=variable_id,
            start_year=s_year,
            end_year=e_year,
            custom_region=custom_region,
        )
        if live_df is not None and len(live_df) >= 24:
            tele = generate_teleconnection_series(s_year, e_year)
            merged = pd.merge(live_df, tele[["date", "nao_index", "enso_index", "iod_index"]], on="date", how="left")
            return merged, meta

    # Default / Fallback: Pre-cached calibrated dataset
    cache_key = make_cache_key(
        f"series_{region['id']}_{variable_id}",
        s_year=s_year,
        e_year=e_year,
        glacier_only=glacier_only,
    )
    cached_df = get_cached_dataframe(cache_key)
    if cached_df is None:
        cached_df = generate_regional_series(
            region_id=region["id"],
            variable_id=variable_id,
            start_year=s_year,
            end_year=e_year,
            glacier_only=glacier_only,
            custom_region=custom_region,
        )
        save_cached_dataframe(cache_key, cached_df)

    mm_url = build_meteomatics_url(
        f"{s_year}-01-01T00:00:00Z",
        f"{e_year}-10-01T00:00:00Z",
        "P1M",
        var_info["meteomatics_param"],
        region["center_lat"],
        region["center_lon"],
    )
    nasa_url = build_nasa_power_url(
        var_info["nasa_power_param"],
        region["center_lat"],
        region["center_lon"],
        s_year,
        e_year,
    )

    metadata = {
        "source_mode": f"Pre-Cached NASA & Meteomatics Assimilation ({var_info['source_mission']})",
        "meteomatics_url": mm_url,
        "nasa_power_url": nasa_url,
        "glacier_mask_active": glacier_only,
        "cached": True,
    }
    return cached_df, metadata


def prewarm_core_caches() -> int:
    """
    Pre-compute and save CSV caches for key preset regions and walkthrough demos
    so the first app load is instantaneous.
    """
    count = 0
    core_pairs = [
        ("karakoram", "snow_cover_modis"),
        ("hindu_kush", "snow_cover_modis"),
        ("western_himalaya", "snow_cover_modis"),
        ("hunza", "t2m_merra2"),
        ("upper_indus", "precip_imerg"),
        ("chitral", "swe_gldas"),
        ("astore", "lst_modis"),
        ("neelum", "snow_depth_meteomatics"),
        ("gilgit", "runoff_gldas"),
    ]
    for r_id, v_id in core_pairs:
        load_investigation_series(r_id, v_id, glacier_only=False)
        count += 1
    return count


__all__ = [
    "load_investigation_series",
    "generate_teleconnection_series",
    "generate_regional_series",
    "generate_multivariate_series",
    "generate_spatial_grid_data",
    "build_meteomatics_url",
    "fetch_meteomatics_monthly_series",
    "build_nasa_power_url",
    "fetch_nasa_power_monthly_series",
    "fetch_glacier_7day_forecast",
    "get_all_glaciers_radar_summary",
    "get_quota_status",
    "prewarm_core_caches",
]
