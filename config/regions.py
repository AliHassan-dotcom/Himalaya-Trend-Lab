"""
Preset Glacier Regions and River Basins of Northern Pakistan.
Includes bounding boxes, center coordinates, elevation profiles, RGI v6.0 glacier
coverage statistics, and scientific context for trend investigation.
"""
from typing import Dict, Any, List, Optional

PRESET_REGIONS: Dict[str, Dict[str, Any]] = {
    "karakoram": {
        "id": "karakoram",
        "name": "Karakoram Range",
        "category": "Mountain Range",
        "parent_range": "Karakoram",
        "center_lat": 35.85,
        "center_lon": 76.10,
        "bbox": {
            "lat_min": 34.80,
            "lat_max": 36.85,
            "lon_min": 74.20,
            "lon_max": 77.80,
        },
        "mean_elevation_m": 4850,
        "elevation_range_m": (2400, 8611),  # Includes K2 (8,611 m)
        "glacier_area_km2": 13680,
        "glacier_fraction_pct": 28.4,
        "rgi_region": "RGI 14 (South Asia West)",
        "dominant_climate_regime": "Winter Westerlies & High-Altitude Orgraphic Snowfall",
        "elevation_bands": [
            {"band": "< 3,500 m (Valley Floors & Snouts)", "area_share": 0.14, "glacier_share": 0.06},
            {"band": "3,500 – 4,500 m (Ablation Zone)", "area_share": 0.31, "glacier_share": 0.24},
            {"band": "4,500 – 5,500 m (Equilibrium Zone)", "area_share": 0.37, "glacier_share": 0.46},
            {"band": "> 5,500 m (Accumulation Zone)", "area_share": 0.18, "glacier_share": 0.24},
        ],
        "summary": (
            "Home to the world's largest concentration of non-polar valley glaciers "
            "(including Siachen, Baltoro, Biafo, and Hispar). Known scientifically for the "
            "'Karakoram Anomaly', where high-altitude snow and ice remained relatively stable "
            "or slightly gained mass for decades compared to neighbouring ranges, though recent "
            "warming is increasingly testing this stability."
        ),
        "baseline_dynamics": {
            "temp_trend_per_decade_c": 0.19,
            "snow_cover_trend_per_decade_pct": -0.35,
            "precip_trend_per_decade_mm": 4.2,
            "swe_trend_per_decade_mm": -1.8,
        },
    },
    "hindu_kush": {
        "id": "hindu_kush",
        "name": "Hindu Kush Range",
        "category": "Mountain Range",
        "parent_range": "Hindu Kush",
        "center_lat": 36.25,
        "center_lon": 72.25,
        "bbox": {
            "lat_min": 35.10,
            "lat_max": 37.10,
            "lon_min": 71.10,
            "lon_max": 73.60,
        },
        "mean_elevation_m": 4120,
        "elevation_range_m": (1800, 7708),  # Tirich Mir (7,708 m)
        "glacier_area_km2": 3250,
        "glacier_fraction_pct": 11.8,
        "rgi_region": "RGI 14 (South Asia West)",
        "dominant_climate_regime": "Mediterranean/Caspian Westerlies (Winter-Spring Maxima)",
        "elevation_bands": [
            {"band": "< 3,500 m (Valley Floors & Snouts)", "area_share": 0.26, "glacier_share": 0.08},
            {"band": "3,500 – 4,500 m (Ablation Zone)", "area_share": 0.42, "glacier_share": 0.36},
            {"band": "4,500 – 5,500 m (Equilibrium Zone)", "area_share": 0.24, "glacier_share": 0.42},
            {"band": "> 5,500 m (Accumulation Zone)", "area_share": 0.08, "glacier_share": 0.14},
        ],
        "summary": (
            "Stretching across northern Chitral and Dir, the Hindu Kush exhibits stronger "
            "sensitivity to spring and summer warming than the central Karakoram, showing "
            "more pronounced declines in seasonal snow cover and glacier mass."
        ),
        "baseline_dynamics": {
            "temp_trend_per_decade_c": 0.34,
            "snow_cover_trend_per_decade_pct": -2.45,
            "precip_trend_per_decade_mm": -3.1,
            "swe_trend_per_decade_mm": -11.5,
        },
    },
    "western_himalaya": {
        "id": "western_himalaya",
        "name": "Western Himalaya (Pakistan Sector)",
        "category": "Mountain Range",
        "parent_range": "Western Himalaya",
        "center_lat": 35.05,
        "center_lon": 74.60,
        "bbox": {
            "lat_min": 34.10,
            "lat_max": 35.65,
            "lon_min": 73.50,
            "lon_max": 75.60,
        },
        "mean_elevation_m": 3890,
        "elevation_range_m": (1500, 8126),  # Nanga Parbat (8,126 m)
        "glacier_area_km2": 1840,
        "glacier_fraction_pct": 8.6,
        "rgi_region": "RGI 14 (South Asia West)",
        "dominant_climate_regime": "Mixed South Asian Monsoon & Winter Westerlies",
        "elevation_bands": [
            {"band": "< 3,500 m (Valley Floors & Snouts)", "area_share": 0.34, "glacier_share": 0.12},
            {"band": "3,500 – 4,500 m (Ablation Zone)", "area_share": 0.39, "glacier_share": 0.44},
            {"band": "4,500 – 5,500 m (Equilibrium Zone)", "area_share": 0.21, "glacier_share": 0.33},
            {"band": "> 5,500 m (Accumulation Zone)", "area_share": 0.06, "glacier_share": 0.11},
        ],
        "summary": (
            "Anchored by the Nanga Parbat massif and feeding the Astore, Kunhar, and Neelum "
            "basins. Lower average elevations and summer monsoon intrusion make its snowpack "
            "and glaciers highly vulnerable to rising temperatures."
        ),
        "baseline_dynamics": {
            "temp_trend_per_decade_c": 0.38,
            "snow_cover_trend_per_decade_pct": -2.90,
            "precip_trend_per_decade_mm": 2.6,
            "swe_trend_per_decade_mm": -14.2,
        },
    },
    "upper_indus": {
        "id": "upper_indus",
        "name": "Upper Indus Basin (UIB)",
        "category": "Major River Basin",
        "parent_range": "Karakoram-Himalaya-Hindu Kush",
        "center_lat": 35.60,
        "center_lon": 75.15,
        "bbox": {
            "lat_min": 34.40,
            "lat_max": 37.05,
            "lon_min": 72.00,
            "lon_max": 77.80,
        },
        "mean_elevation_m": 4420,
        "elevation_range_m": (1200, 8611),
        "glacier_area_km2": 18500,
        "glacier_fraction_pct": 16.2,
        "rgi_region": "RGI 14 (South Asia West)",
        "dominant_climate_regime": "Westerlies + Orographic Transition Zone",
        "elevation_bands": [
            {"band": "< 3,500 m (Valley Floors & Snouts)", "area_share": 0.22, "glacier_share": 0.07},
            {"band": "3,500 – 4,500 m (Ablation Zone)", "area_share": 0.35, "glacier_share": 0.28},
            {"band": "4,500 – 5,500 m (Equilibrium Zone)", "area_share": 0.31, "glacier_share": 0.45},
            {"band": "> 5,500 m (Accumulation Zone)", "area_share": 0.12, "glacier_share": 0.20},
        ],
        "summary": (
            "The primary water tower of Pakistan feeding Tarbela Reservoir. Combines runoff "
            "from the Karakoram, Hindu Kush, and Western Himalaya, where high inter-annual "
            "variability often masks long-term precipitation trends."
        ),
        "baseline_dynamics": {
            "temp_trend_per_decade_c": 0.27,
            "snow_cover_trend_per_decade_pct": -1.35,
            "precip_trend_per_decade_mm": 1.1,  # High noise, non-significant demo case
            "swe_trend_per_decade_mm": -6.8,
        },
    },
    "hunza": {
        "id": "hunza",
        "name": "Hunza River Basin",
        "category": "Glacier Sub-Basin",
        "parent_range": "Karakoram",
        "center_lat": 36.32,
        "center_lon": 74.65,
        "bbox": {
            "lat_min": 35.90,
            "lat_max": 37.05,
            "lon_min": 74.05,
            "lon_max": 75.75,
        },
        "mean_elevation_m": 4630,
        "elevation_range_m": (1850, 7885),
        "glacier_area_km2": 3840,
        "glacier_fraction_pct": 27.9,
        "rgi_region": "RGI 14 (South Asia West)",
        "dominant_climate_regime": "High-Altitude Westerlies",
        "elevation_bands": [
            {"band": "< 3,500 m (Valley Floors & Snouts)", "area_share": 0.16, "glacier_share": 0.08},
            {"band": "3,500 – 4,500 m (Ablation Zone)", "area_share": 0.32, "glacier_share": 0.26},
            {"band": "4,500 – 5,500 m (Equilibrium Zone)", "area_share": 0.38, "glacier_share": 0.47},
            {"band": "> 5,500 m (Accumulation Zone)", "area_share": 0.14, "glacier_share": 0.19},
        ],
        "summary": (
            "Heavily glaciated Karakoram valley containing Batura, Passu, Ghulkin, and "
            "Shisper glaciers. A hotspot for surging glaciers and Glacial Lake Outburst "
            "Floods (GLOFs) when summer temperature anomalies spike."
        ),
        "baseline_dynamics": {
            "temp_trend_per_decade_c": 0.31,
            "snow_cover_trend_per_decade_pct": -0.75,
            "precip_trend_per_decade_mm": 3.5,
            "swe_trend_per_decade_mm": -3.2,
        },
    },
    "gilgit": {
        "id": "gilgit",
        "name": "Gilgit River Basin (Ghizer & Yasin)",
        "category": "Glacier Sub-Basin",
        "parent_range": "Hindu Kush-Karakoram Transition",
        "center_lat": 36.18,
        "center_lon": 73.55,
        "bbox": {
            "lat_min": 35.75,
            "lat_max": 36.85,
            "lon_min": 72.55,
            "lon_max": 74.40,
        },
        "mean_elevation_m": 4050,
        "elevation_range_m": (1450, 6870),
        "glacier_area_km2": 1260,
        "glacier_fraction_pct": 10.4,
        "rgi_region": "RGI 14 (South Asia West)",
        "dominant_climate_regime": "Westerlies Transition",
        "elevation_bands": [
            {"band": "< 3,500 m (Valley Floors & Snouts)", "area_share": 0.28, "glacier_share": 0.09},
            {"band": "3,500 – 4,500 m (Ablation Zone)", "area_share": 0.43, "glacier_share": 0.41},
            {"band": "4,500 – 5,500 m (Equilibrium Zone)", "area_share": 0.23, "glacier_share": 0.39},
            {"band": "> 5,500 m (Accumulation Zone)", "area_share": 0.06, "glacier_share": 0.11},
        ],
        "summary": (
            "Bridges the eastern Hindu Kush and western Karakoram (including Ishkoman, "
            "Yasin, and Phandar valleys). Frequently impacted by GLOF events during "
            "compound summer heat and rainfall anomalies."
        ),
        "baseline_dynamics": {
            "temp_trend_per_decade_c": 0.33,
            "snow_cover_trend_per_decade_pct": -1.85,
            "precip_trend_per_decade_mm": 1.8,
            "swe_trend_per_decade_mm": -8.4,
        },
    },
    "chitral": {
        "id": "chitral",
        "name": "Chitral River Basin (Kunar Headwaters)",
        "category": "Glacier Sub-Basin",
        "parent_range": "Hindu Kush",
        "center_lat": 36.10,
        "center_lon": 72.10,
        "bbox": {
            "lat_min": 35.25,
            "lat_max": 36.95,
            "lon_min": 71.20,
            "lon_max": 73.25,
        },
        "mean_elevation_m": 4180,
        "elevation_range_m": (1500, 7708),
        "glacier_area_km2": 2150,
        "glacier_fraction_pct": 14.7,
        "rgi_region": "RGI 14 (South Asia West)",
        "dominant_climate_regime": "Winter-Spring Westerlies",
        "elevation_bands": [
            {"band": "< 3,500 m (Valley Floors & Snouts)", "area_share": 0.25, "glacier_share": 0.08},
            {"band": "3,500 – 4,500 m (Ablation Zone)", "area_share": 0.41, "glacier_share": 0.37},
            {"band": "4,500 – 5,500 m (Equilibrium Zone)", "area_share": 0.26, "glacier_share": 0.41},
            {"band": "> 5,500 m (Accumulation Zone)", "area_share": 0.08, "glacier_share": 0.14},
        ],
        "summary": (
            "Dominated by Chiantar, Tirich, and Kotgaz glaciers in the Hindu Kush. "
            "Experiences clear spring/summer warming and accelerating snowmelt rates, "
            "increasing flash-flood and GLOF hazards in Booni, Reshun, and Golain."
        ),
        "baseline_dynamics": {
            "temp_trend_per_decade_c": 0.36,
            "snow_cover_trend_per_decade_pct": -2.55,
            "precip_trend_per_decade_mm": -2.8,
            "swe_trend_per_decade_mm": -12.1,
        },
    },
    "astore": {
        "id": "astore",
        "name": "Astore River Basin (Nanga Parbat East/North)",
        "category": "Glacier Sub-Basin",
        "parent_range": "Western Himalaya",
        "center_lat": 35.22,
        "center_lon": 74.85,
        "bbox": {
            "lat_min": 34.80,
            "lat_max": 35.60,
            "lon_min": 74.40,
            "lon_max": 75.35,
        },
        "mean_elevation_m": 4080,
        "elevation_range_m": (2100, 8126),
        "glacier_area_km2": 540,
        "glacier_fraction_pct": 13.5,
        "rgi_region": "RGI 14 (South Asia West)",
        "dominant_climate_regime": "Western Himalaya Transition",
        "elevation_bands": [
            {"band": "< 3,500 m (Valley Floors & Snouts)", "area_share": 0.24, "glacier_share": 0.11},
            {"band": "3,500 – 4,500 m (Ablation Zone)", "area_share": 0.46, "glacier_share": 0.45},
            {"band": "4,500 – 5,500 m (Equilibrium Zone)", "area_share": 0.24, "glacier_share": 0.34},
            {"band": "> 5,500 m (Accumulation Zone)", "area_share": 0.06, "glacier_share": 0.10},
        ],
        "summary": (
            "Drains the steep slopes of Nanga Parbat and the Deosai plateau margin. "
            "Debris-covered valley glaciers and seasonal snowfields show strong sensitivity "
            "to rising warm-season minimum temperatures."
        ),
        "baseline_dynamics": {
            "temp_trend_per_decade_c": 0.37,
            "snow_cover_trend_per_decade_pct": -2.75,
            "precip_trend_per_decade_mm": 2.1,
            "swe_trend_per_decade_mm": -13.0,
        },
    },
    "neelum": {
        "id": "neelum",
        "name": "Neelum (Kishanganga) Basin",
        "category": "Glacier Sub-Basin",
        "parent_range": "Western Himalaya",
        "center_lat": 34.72,
        "center_lon": 74.18,
        "bbox": {
            "lat_min": 34.25,
            "lat_max": 35.15,
            "lon_min": 73.45,
            "lon_max": 74.85,
        },
        "mean_elevation_m": 3420,
        "elevation_range_m": (1100, 6320),
        "glacier_area_km2": 310,
        "glacier_fraction_pct": 4.2,
        "rgi_region": "RGI 14 (South Asia West)",
        "dominant_climate_regime": "Monsoon-Westerlies Convergence",
        "elevation_bands": [
            {"band": "< 3,500 m (Valley Floors & Snouts)", "area_share": 0.52, "glacier_share": 0.21},
            {"band": "3,500 – 4,500 m (Ablation Zone)", "area_share": 0.36, "glacier_share": 0.56},
            {"band": "4,500 – 5,500 m (Equilibrium Zone)", "area_share": 0.11, "glacier_share": 0.21},
            {"band": "> 5,500 m (Accumulation Zone)", "area_share": 0.01, "glacier_share": 0.02},
        ],
        "summary": (
            "Lower-elevation Himalayan basin feeding the Jhelum River. Because much of "
            "its snowpack lies near the freezing isotherm (3,000–4,200 m), even modest "
            "warming converts winter snowfall into rain and accelerates spring melt."
        ),
        "baseline_dynamics": {
            "temp_trend_per_decade_c": 0.42,
            "snow_cover_trend_per_decade_pct": -3.35,
            "precip_trend_per_decade_mm": 3.4,
            "swe_trend_per_decade_mm": -16.4,
        },
    },
}


def get_region(region_id: str) -> Dict[str, Any]:
    """Retrieve a preset region by ID, defaulting to Karakoram if not found."""
    return PRESET_REGIONS.get(region_id, PRESET_REGIONS["karakoram"])


def get_region_options() -> List[Dict[str, str]]:
    """Return a list of (id, label, category) dicts for UI selectors."""
    return [
        {
            "id": r_id,
            "name": info["name"],
            "category": info["category"],
            "parent_range": info["parent_range"],
        }
        for r_id, info in PRESET_REGIONS.items()
    ]


def build_custom_region(
    lat_min: float,
    lat_max: float,
    lon_min: float,
    lon_max: float,
    name: Optional[str] = None,
) -> Dict[str, Any]:
    """Construct a region metadata dictionary for a user-defined bounding box."""
    lat_low, lat_high = sorted([float(lat_min), float(lat_max)])
    lon_low, lon_high = sorted([float(lon_min), float(lon_max)])
    c_lat = round((lat_low + lat_high) / 2.0, 4)
    c_lon = round((lon_low + lon_high) / 2.0, 4)

    # Infer closest mountain range by center coordinate
    if c_lon >= 74.4 and c_lat >= 35.4:
        inferred_range = "Karakoram"
        base_dyn = PRESET_REGIONS["karakoram"]["baseline_dynamics"]
    elif c_lon < 73.7 and c_lat >= 35.3:
        inferred_range = "Hindu Kush"
        base_dyn = PRESET_REGIONS["hindu_kush"]["baseline_dynamics"]
    else:
        inferred_range = "Western Himalaya / Upper Indus"
        base_dyn = PRESET_REGIONS["western_himalaya"]["baseline_dynamics"]

    label = name or f"Custom Box ({lat_low:.2f}°N–{lat_high:.2f}°N, {lon_low:.2f}°E–{lon_high:.2f}°E)"
    return {
        "id": f"custom_{lat_low:.2f}_{lat_high:.2f}_{lon_low:.2f}_{lon_high:.2f}",
        "name": label,
        "category": "Custom User-Defined Box",
        "parent_range": inferred_range,
        "center_lat": c_lat,
        "center_lon": c_lon,
        "bbox": {
            "lat_min": lat_low,
            "lat_max": lat_high,
            "lon_min": lon_low,
            "lon_max": lon_high,
        },
        "mean_elevation_m": 4200,
        "elevation_range_m": (1800, 7500),
        "glacier_area_km2": 950,
        "glacier_fraction_pct": 14.0,
        "rgi_region": "RGI 14 (South Asia West)",
        "dominant_climate_regime": f"Custom Sector ({inferred_range})",
        "elevation_bands": PRESET_REGIONS["upper_indus"]["elevation_bands"],
        "summary": (
            f"User-defined geographic bounding box centered at ({c_lat:.2f}°N, {c_lon:.2f}°E) "
            f"within the {inferred_range} domain."
        ),
        "baseline_dynamics": base_dyn,
    }
