"""
Meteomatics Weather API Client (NASA Space Apps Global Offer).
Queries `https://api.meteomatics.com/<validdatetime>/<parameters>/<location>/csv`
using HTTP Basic Authentication (`METEOMATICS_USERNAME`, `METEOMATICS_PASSWORD`),
with automatic disk caching to protect the 1,000 queries/day limit.
"""
import base64
from io import StringIO
from typing import Optional, Dict, Any, Tuple
from urllib import request as urllib_request
import pandas as pd

from config.settings import (
    METEOMATICS_BASE_URL,
    METEOMATICS_USERNAME,
    METEOMATICS_PASSWORD,
    has_meteomatics_credentials,
)
from config.regions import get_region
from config.variables import get_variable
from data.cache_manager import (
    make_cache_key,
    get_cached_dataframe,
    save_cached_dataframe,
    record_api_call,
)


def _http_get_text(url: str, username: str = "", password: str = "", timeout: int = 15) -> str:
    """Perform HTTP GET with optional Basic Auth using httpx or stdlib urllib."""
    try:
        import httpx
        auth = (username, password) if username and password else None
        with httpx.Client(timeout=timeout, follow_redirects=True) as client:
            resp = client.get(url, auth=auth)
            resp.raise_for_status()
            return resp.text
    except ImportError:
        req = urllib_request.Request(url)
        if username and password:
            token = base64.b64encode(f"{username}:{password}".encode("utf-8")).decode("ascii")
            req.add_header("Authorization", f"Basic {token}")
        with urllib_request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8")


def build_meteomatics_url(
    start_iso: str,
    end_iso: str,
    step: str,
    parameters: str,
    lat: float,
    lon: float,
    fmt: str = "csv",
) -> str:
    """
    Construct a compliant Meteomatics REST API URL.
    Example:
    https://api.meteomatics.com/2000-01-01T00:00:00Z--2026-10-01T00:00:00Z:P1M/t_2m:C/36.32,74.65/csv
    """
    time_spec = f"{start_iso}--{end_iso}:{step}" if end_iso else start_iso
    return f"{METEOMATICS_BASE_URL}/{time_spec}/{parameters}/{lat:.4f},{lon:.4f}/{fmt}"


def fetch_meteomatics_monthly_series(
    region_id: str,
    variable_id: str,
    start_year: int = 2000,
    end_year: int = 2026,
    custom_region: Optional[Dict[str, Any]] = None,
    force_refresh: bool = False,
) -> Tuple[Optional[pd.DataFrame], Dict[str, Any]]:
    """
    Attempt to fetch monthly time-series data from the live Meteomatics API.
    Returns (DataFrame or None, metadata_dict).
    Automatically uses local cache first unless `force_refresh=True`.
    """
    region = custom_region if custom_region else get_region(region_id)
    var_info = get_variable(variable_id)
    mm_param = var_info.get("meteomatics_param", "t_2m:C")
    lat, lon = region["center_lat"], region["center_lon"]

    cache_key = make_cache_key(
        f"mm_monthly_{region['id']}_{variable_id}",
        lat=lat,
        lon=lon,
        param=mm_param,
        start_year=start_year,
        end_year=end_year,
    )

    if not force_refresh:
        cached_df = get_cached_dataframe(cache_key)
        if cached_df is not None:
            return cached_df, {
                "source_mode": "Meteomatics API (Local Cache)",
                "api_url": build_meteomatics_url(
                    f"{start_year}-01-01T00:00:00Z",
                    f"{end_year}-10-01T00:00:00Z",
                    "P1M",
                    mm_param,
                    lat,
                    lon,
                ),
                "cached": True,
            }

    url = build_meteomatics_url(
        start_iso=f"{start_year}-01-01T00:00:00Z",
        end_iso=f"{end_year}-10-01T00:00:00Z",
        step="P1M",
        parameters=mm_param,
        lat=lat,
        lon=lon,
        fmt="csv",
    )

    if not has_meteomatics_credentials():
        return None, {
            "source_mode": "Calibrated Pre-Cached Dataset (Add Meteomatics credentials in .env for live fetch)",
            "api_url": url,
            "cached": True,
        }

    try:
        csv_text = _http_get_text(url, METEOMATICS_USERNAME, METEOMATICS_PASSWORD, timeout=15)
        record_api_call("meteomatics")

        raw_df = pd.read_csv(StringIO(csv_text), sep=";")
        if "validdate" not in raw_df.columns or len(raw_df) < 12:
            return None, {"source_mode": "Fallback Dataset (Incomplete API response)", "api_url": url}

        raw_df["date"] = pd.to_datetime(raw_df["validdate"], utc=True).dt.tz_localize(None)
        val_col = [c for c in raw_df.columns if c not in ("validdate", "date", "lat", "lon")][0]

        df = pd.DataFrame({
            "date": raw_df["date"].dt.to_period("M").dt.to_timestamp(),
            "year": raw_df["date"].dt.year,
            "month": raw_df["date"].dt.month,
            "value": pd.to_numeric(raw_df[val_col], errors="coerce"),
            "region_id": region["id"],
            "region_name": region["name"],
            "variable_id": variable_id,
            "variable_name": var_info["name"],
            "units": var_info["units"],
            "glacier_only": False,
            "quality_flag": "good",
        }).dropna(subset=["value"])

        save_cached_dataframe(cache_key, df)
        return df, {
            "source_mode": "Live Meteomatics Weather API",
            "api_url": url,
            "cached": False,
        }
    except Exception as exc:
        return None, {
            "source_mode": f"Calibrated Pre-Cached Dataset (Meteomatics offline/limit: {type(exc).__name__})",
            "api_url": url,
            "cached": True,
        }
