"""
Global application settings, API endpoints, statistical constants, and directory paths.
"""
import logging
import os
import tempfile
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IS_VERCEL = bool(os.environ.get("VERCEL"))
_TMP_ROOT = Path("/tmp") if os.name != "nt" else Path(tempfile.gettempdir())
_VERCEL_TMP_DIR = _TMP_ROOT / "himalaya_trend_lab"

if IS_VERCEL:
    os.environ.setdefault("MPLCONFIGDIR", str(_VERCEL_TMP_DIR / "matplotlib"))

try:
    from dotenv import load_dotenv
    load_dotenv(BASE_DIR / ".env")
except ImportError:
    try:
        env_path = BASE_DIR / ".env"
        if env_path.exists():
            for line in env_path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
    except Exception as exc:
        logging.warning("Skipping .env load: %s", exc)

BUNDLED_CACHE_DIR = BASE_DIR / "data" / "cached"
CACHE_DIR = (_VERCEL_TMP_DIR / "cached") if IS_VERCEL else BUNDLED_CACHE_DIR
EXPORT_DIR = (_VERCEL_TMP_DIR / "exports") if IS_VERCEL else (BASE_DIR / "exports" / "output")

for _dir in (CACHE_DIR, EXPORT_DIR):
    try:
        _dir.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        logging.warning("Could not create directory %s: %s", _dir, exc)

# Application Metadata
APP_TITLE = "Himalaya Trend Lab"
APP_SUBTITLE = "Be a Data Detective for Pakistan's Glaciers"
APP_VERSION = "1.0.0"
CHALLENGE_NAME = "Be An Earth System Trend Detective (NASA Space Apps 2026)"
AUTHOR_NAME = "Team GeoNova"

def _safe_float_env(name: str, default: float) -> float:
    raw = (os.environ.get(name) or "").strip()
    if not raw:
        return default
    try:
        return float(raw)
    except ValueError:
        logging.warning("Invalid float for env %s=%r; falling back to %s", name, raw, default)
        return default


# API Endpoints & Credentials
METEOMATICS_BASE_URL = (os.environ.get("METEOMATICS_BASE_URL") or "https://api.meteomatics.com").strip()
METEOMATICS_USERNAME = (os.environ.get("METEOMATICS_USERNAME") or "").strip()
METEOMATICS_PASSWORD = (os.environ.get("METEOMATICS_PASSWORD") or "").strip()

NASA_POWER_BASE_URL = (
    os.environ.get("NASA_POWER_BASE_URL") or "https://power.larc.nasa.gov/api/temporal/monthly/point"
).strip()

# Statistical & Trend Analysis Defaults
DEFAULT_ALPHA = _safe_float_env("DEFAULT_ALPHA", 0.05)
SIGNIFICANCE_LEVELS = [0.01, 0.05, 0.10]
MIN_YEARS_RECOMMENDED = 20          # Warn user when record is shorter than 20 years
MIN_YEARS_ABSOLUTE = 5              # Minimum years required to compute a trend
MAX_MISSING_FRACTION_WARN = 0.10    # Warn if >10% of monthly observations have gaps
FDR_ALPHA = 0.05                    # Benjamini-Hochberg False Discovery Rate for trend maps

# Caching Configuration (protects the 1,000 queries/day Meteomatics limit)
ENABLE_CACHE = (os.environ.get("ENABLE_CACHE") or "true").strip().lower() == "true"
CACHE_EXPIRY_DAYS = 7


def has_meteomatics_credentials() -> bool:
    """Return True if valid non-placeholder Meteomatics credentials are configured."""
    if not METEOMATICS_USERNAME or not METEOMATICS_PASSWORD:
        return False
    placeholders = {"your_meteomatics_username", "your_username", "username", ""}
    return METEOMATICS_USERNAME.lower() not in placeholders
