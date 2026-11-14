"""
Local disk cache manager for time-series, spatial grids, and 7-day forecasts.
Protects API quotas (1,000 queries/day on Meteomatics) and guarantees instant,
offline-resilient demos for NASA Space Apps judges.
"""
import hashlib
import json
import time
from pathlib import Path
from typing import Optional, Dict, Any
import pandas as pd

from config.settings import CACHE_DIR, ENABLE_CACHE, CACHE_EXPIRY_DAYS

STATS_FILE = CACHE_DIR / "cache_stats.json"


def _load_stats() -> Dict[str, int]:
    if STATS_FILE.exists():
        try:
            return json.loads(STATS_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"cache_hits": 0, "api_calls_meteomatics": 0, "api_calls_nasa": 0}


def _save_stats(stats: Dict[str, int]) -> None:
    try:
        STATS_FILE.write_text(json.dumps(stats, indent=2), encoding="utf-8")
    except Exception:
        pass


def record_cache_hit() -> None:
    stats = _load_stats()
    stats["cache_hits"] = stats.get("cache_hits", 0) + 1
    _save_stats(stats)


def record_api_call(provider: str = "meteomatics") -> None:
    stats = _load_stats()
    key = f"api_calls_{provider.lower()}"
    stats[key] = stats.get(key, 0) + 1
    _save_stats(stats)


def get_quota_status() -> Dict[str, Any]:
    """Return current API call counts and remaining daily Meteomatics quota."""
    stats = _load_stats()
    used = stats.get("api_calls_meteomatics", 0)
    return {
        "meteomatics_used": used,
        "meteomatics_limit": 1000,
        "meteomatics_remaining": max(0, 1000 - used),
        "nasa_calls": stats.get("api_calls_nasa", 0),
        "cache_hits": stats.get("cache_hits", 0),
    }


def make_cache_key(prefix: str, **kwargs: Any) -> str:
    """Create a deterministic filename-safe key for a given query."""
    serialized = json.dumps(kwargs, sort_keys=True, default=str)
    digest = hashlib.md5(serialized.encode("utf-8")).hexdigest()[:10]
    clean_prefix = "".join(c if c.isalnum() or c in ("_", "-") else "_" for c in prefix)
    return f"{clean_prefix}_{digest}"


def _is_expired(filepath: Path) -> bool:
    if not filepath.exists():
        return True
    age_seconds = time.time() - filepath.stat().st_mtime
    return age_seconds > (CACHE_EXPIRY_DAYS * 86400)


def get_cached_dataframe(cache_key: str) -> Optional[pd.DataFrame]:
    """Load a cached pandas DataFrame if caching is enabled and file is fresh."""
    if not ENABLE_CACHE:
        return None
    filepath = CACHE_DIR / f"{cache_key}.csv"
    if _is_expired(filepath):
        return None
    try:
        df = pd.read_csv(filepath, parse_dates=["date"])
        record_cache_hit()
        return df
    except Exception:
        return None


def save_cached_dataframe(cache_key: str, df: pd.DataFrame) -> Path:
    """Save a pandas DataFrame to the local cache directory."""
    filepath = CACHE_DIR / f"{cache_key}.csv"
    df.to_csv(filepath, index=False)
    return filepath


def get_cached_json(cache_key: str) -> Optional[Dict[str, Any]]:
    """Load a cached JSON dictionary if available and fresh."""
    if not ENABLE_CACHE:
        return None
    filepath = CACHE_DIR / f"{cache_key}.json"
    if _is_expired(filepath):
        return None
    try:
        data = json.loads(filepath.read_text(encoding="utf-8"))
        record_cache_hit()
        return data
    except Exception:
        return None


def save_cached_json(cache_key: str, payload: Dict[str, Any]) -> Path:
    """Save a JSON-serializable dictionary to the local cache directory."""
    filepath = CACHE_DIR / f"{cache_key}.json"
    filepath.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return filepath
