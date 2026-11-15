"""
Global application settings, API endpoints, statistical constants, and directory paths.
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

try:
    from dotenv import load_dotenv
    load_dotenv(BASE_DIR / ".env")
except ImportError:
    env_path = BASE_DIR / ".env"
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
CACHE_DIR = BASE_DIR / "data" / "cached"
EXPORT_DIR = BASE_DIR / "exports" / "output"

CACHE_DIR.mkdir(parents=True, exist_ok=True)
EXPORT_DIR.mkdir(parents=True, exist_ok=True)

# Application Metadata
APP_TITLE = "Himalaya Trend Lab"
APP_SUBTITLE = "Be a Data Detective for Pakistan's Glaciers"
APP_VERSION = "1.0.0"
CHALLENGE_NAME = "Be An Earth System Trend Detective (NASA Space Apps 2026)"
AUTHOR_NAME = "Team GeoNova"

# API Endpoints & Credentials
METEOMATICS_BASE_URL = "https://api.meteomatics.com"
METEOMATICS_USERNAME = os.getenv("METEOMATICS_USERNAME", "").strip()
METEOMATICS_PASSWORD = os.getenv("METEOMATICS_PASSWORD", "").strip()

NASA_POWER_BASE_URL = "https://power.larc.nasa.gov/api/temporal/monthly/point"

# Statistical & Trend Analysis Defaults
DEFAULT_ALPHA = float(os.getenv("DEFAULT_ALPHA", "0.05"))
SIGNIFICANCE_LEVELS = [0.01, 0.05, 0.10]
MIN_YEARS_RECOMMENDED = 20          # Warn user when record is shorter than 20 years
MIN_YEARS_ABSOLUTE = 5              # Minimum years required to compute a trend
MAX_MISSING_FRACTION_WARN = 0.10    # Warn if >10% of monthly observations have gaps
FDR_ALPHA = 0.05                    # Benjamini-Hochberg False Discovery Rate for trend maps

# Caching Configuration (protects the 1,000 queries/day Meteomatics limit)
ENABLE_CACHE = os.getenv("ENABLE_CACHE", "true").lower() == "true"
CACHE_EXPIRY_DAYS = 7


def has_meteomatics_credentials() -> bool:
    """Return True if valid non-placeholder Meteomatics credentials are configured."""
    if not METEOMATICS_USERNAME or not METEOMATICS_PASSWORD:
        return False
    placeholders = {"your_meteomatics_username", "your_username", "username", ""}
    return METEOMATICS_USERNAME.lower() not in placeholders
