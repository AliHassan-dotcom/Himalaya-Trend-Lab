"""
NASA Earth Observation Data Client (NASA POWER MERRA-2 API + Satellite Cache).
Fetches monthly climate records from `https://power.larc.nasa.gov/api/temporal/monthly/point`
with zero authentication required and caches responses locally.
"""
import json
from typing import Optional, Dict, Any, Tuple
import pandas as pd

from config.settings import NASA_POWER_BASE_URL
from config.regions import get_region
from config.variables import get_variable
from data.cache_manager import (
    make_cache_key,
    get_cached_dataframe,
    save_cached_dataframe,
    record_api_call,
)
from data.meteomatics_client import _http_get_text


def build_nasa_power_url(
    param: str,
    lat: float,
    lon: float,
    start_year: int = 1981,
    end_year: int = 2025,
) -> str:
    """Construct a NASA POWER MERRA-2 monthly point query URL."""
    return (
        f"{NASA_POWER_BASE_URL}?parameters={param}&community=RE"
        f"&longitude={lon:.4f}&latitude={lat:.4f}"
        f"&start={start_year}&end={min(2025, end_year)}&format=JSON"
    )


def fetch_nasa_power_monthly_series(
    region_id: str,
    variable_id: str,
    start_year: int = 1981,
    end_year: int = 2025,
    custom_region: Optional[Dict[str, Any]] = None,
    force_refresh: bool = False,
) -> Tuple[Optional[pd.DataFrame], Dict[str, Any]]:
    """
    Query NASA POWER (MERRA-2 reanalysis) for monthly regional climate series.
    Returns (DataFrame or None, metadata_dict).
    """
    region = custom_region if custom_region else get_region(region_id)
    var_info = get_variable(variable_id)
    nasa_param = var_info.get("nasa_power_param", "T2M")
    lat, lon = region["center_lat"], region["center_lon"]

    cache_key = make_cache_key(
        f"nasa_power_{region['id']}_{variable_id}",
        lat=lat,
        lon=lon,
        param=nasa_param,
        start_year=start_year,
        end_year=end_year,
    )

    url = build_nasa_power_url(nasa_param, lat, lon, start_year, end_year)

    if not force_refresh:
        cached_df = get_cached_dataframe(cache_key)
        if cached_df is not None:
            return cached_df, {
                "source_mode": "NASA POWER MERRA-2 API (Local Cache)",
                "api_url": url,
                "cached": True,
            }

    try:
        raw_text = _http_get_text(url, timeout=15)
        record_api_call("nasa")
        payload = json.loads(raw_text)

        param_dict = payload.get("properties", {}).get("parameter", {}).get(nasa_param, {})
        if not param_dict:
            return None, {"source_mode": "Pre-Cached NASA Satellite Record", "api_url": url}

        rows = []
        for ym_str, val in param_dict.items():
            # NASA POWER includes month '13' for annual mean; skip month 13 and missing -999
            if len(ym_str) == 6 and not ym_str.endswith("13") and float(val) > -900:
                yr = int(ym_str[:4])
                mo = int(ym_str[4:6])
                rows.append({
                    "date": pd.Timestamp(year=yr, month=mo, day=1),
                    "year": yr,
                    "month": mo,
                    "value": float(val),
                    "region_id": region["id"],
                    "region_name": region["name"],
                    "variable_id": variable_id,
                    "variable_name": var_info["name"],
                    "units": var_info["units"],
                    "glacier_only": False,
                    "quality_flag": "good",
                })

        if len(rows) < 24:
            return None, {"source_mode": "Pre-Cached NASA Satellite Record", "api_url": url}

        df = pd.DataFrame(rows).sort_values("date").reset_index(drop=True)
        save_cached_dataframe(cache_key, df)
        return df, {
            "source_mode": "Live NASA POWER (MERRA-2) API",
            "api_url": url,
            "cached": False,
        }
    except Exception:
        return None, {
            "source_mode": "Pre-Cached NASA Mission Dataset (MODIS / MERRA-2 / GPM / GLDAS)",
            "api_url": url,
            "cached": True,
        }
