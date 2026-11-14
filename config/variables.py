"""
Structured Earth Science Variable Catalogue & Guided Investigation Questions.
Covers all 5 themes from the Himalaya Trend Lab specification:
1. Snow
2. Temperature
3. Precipitation
4. Water (Hydrology)
5. Atmosphere
Plus static reference datasets (RGI/GLIMS Glacier Outlines & SRTM/ALOS Elevation).
"""
from typing import Dict, Any, List

# Guided Investigation Questions for "Detective Mode" (Section 5.1)
DETECTIVE_QUESTIONS: List[Dict[str, Any]] = [
    {
        "id": "warmer",
        "question": "Is it getting warmer?",
        "icon": "",
        "theme": "Temperature",
        "description": (
            "Investigate whether surface and near-surface air temperatures above "
            "Pakistan's glacier valleys show a statistically significant warming trend."
        ),
        "recommended_variables": ["t2m_merra2", "lst_modis"],
        "default_variable": "t2m_merra2",
    },
    {
        "id": "less_snow",
        "question": "Is there less snow?",
        "icon": "",
        "theme": "Snow",
        "description": (
            "Test whether snow cover fraction and snow depth across the Karakoram, "
            "Hindu Kush, and Western Himalaya are declining or remaining stable."
        ),
        "recommended_variables": ["snow_cover_modis", "snow_depth_meteomatics"],
        "default_variable": "snow_cover_modis",
    },
    {
        "id": "rainfall_changing",
        "question": "Is rainfall or snowfall changing?",
        "icon": "",
        "theme": "Precipitation",
        "description": (
            "Examine long-term total precipitation and snowfall trends, and discover "
            "why high year-to-year mountain variability often requires statistical testing."
        ),
        "recommended_variables": ["precip_imerg", "snowfall_merra2"],
        "default_variable": "precip_imerg",
    },
    {
        "id": "water_changing",
        "question": "Is water availability or melt changing?",
        "icon": "",
        "theme": "Water",
        "description": (
            "Analyze Snow Water Equivalent (SWE), glacier/snow melt runoff, and soil "
            "moisture feeding the Upper Indus and Jhelum river systems."
        ),
        "recommended_variables": ["swe_gldas", "runoff_gldas"],
        "default_variable": "swe_gldas",
    },
    {
        "id": "atmosphere_changing",
        "question": "Are atmospheric humidity & aerosols changing?",
        "icon": "",
        "theme": "Atmosphere",
        "description": (
            "Explore tropospheric relative humidity and aerosol optical depth (dust and "
            "black carbon that darken snow surfaces and accelerate melt)."
        ),
        "recommended_variables": ["humidity_airs", "aerosols_omi"],
        "default_variable": "aerosols_omi",
    },
]


# Complete Earth Science Variable Catalogue (Section 6)
VARIABLES_CATALOGUE: Dict[str, Dict[str, Any]] = {
    "snow_cover_modis": {
        "id": "snow_cover_modis",
        "name": "Snow Cover Fraction (SCF)",
        "short_name": "Snow Cover",
        "theme": "Snow",
        "units": "%",
        "decade_units": "% / decade",
        "source_mission": "NASA MODIS (Terra/Aqua) - MOD10CM / MYD10CM v6.1",
        "partner_source": "Meteomatics Snow Cover / Depth Assimilation",
        "nasa_power_param": "PRECSNO",  # Proxy fallback when syncing with NASA POWER
        "meteomatics_param": "snow_depth:cm",
        "start_year": 2000,
        "end_year": 2026,
        "spatial_resolution": "0.05° (~5 km)",
        "temporal_resolution": "Monthly",
        "plain_definition": (
            "The percentage of a mountain region's land area covered by snow during a "
            "given month, measured from space by NASA's Terra and Aqua satellites."
        ),
        "why_it_matters": (
            "Seasonal snow insulates glacier ice from summer sunlight (high albedo) and "
            "provides spring meltwater for crops and hydropower before glacier melt peaks."
        ),
        "caveats": (
            "Optical satellite sensors cannot see through thick clouds, and snow cover "
            "measures surface area rather than ice thickness or glacier mass."
        ),
        "color_scale": "Blues",
        "invert_hazard": True,  # Decline = higher hazard/loss
    },
    "snow_depth_meteomatics": {
        "id": "snow_depth_meteomatics",
        "name": "Snow Depth (High-Resolution Reanalysis)",
        "short_name": "Snow Depth",
        "theme": "Snow",
        "units": "cm",
        "decade_units": "cm / decade",
        "source_mission": "Meteomatics Weather API + NASA MERRA-2 Cryosphere Assimilation",
        "partner_source": "Meteomatics Global Offer (snow_depth:cm)",
        "nasa_power_param": "SNODP",
        "meteomatics_param": "snow_depth:cm",
        "start_year": 2000,
        "end_year": 2026,
        "spatial_resolution": "0.05° – 0.1°",
        "temporal_resolution": "Monthly",
        "plain_definition": (
            "Average thickness of the snowpack on the ground in centimeters, combining "
            "satellite snow detections with high-resolution mountain weather models."
        ),
        "why_it_matters": (
            "Shows not just whether the ground is white, but how deep the winter snow "
            "reservoir is across high-altitude accumulation zones."
        ),
        "caveats": (
            "Snow depth varies sharply over short distances due to wind redistribution, "
            "avalanches, and steep valley topography."
        ),
        "color_scale": "PuBu",
        "invert_hazard": True,
    },
    "t2m_merra2": {
        "id": "t2m_merra2",
        "name": "Near-Surface Air Temperature (2m)",
        "short_name": "Air Temperature (2m)",
        "theme": "Temperature",
        "units": "°C",
        "decade_units": "°C / decade",
        "source_mission": "NASA MERRA-2 Reanalysis (M2TMNXSLV v5.12.4) / NASA POWER",
        "partner_source": "Meteomatics Weather API (t_2m:C)",
        "nasa_power_param": "T2M",
        "meteomatics_param": "t_2m:C",
        "start_year": 1981,
        "end_year": 2026,
        "spatial_resolution": "0.5° x 0.625° (Downscaled with SRTM Lapse Rate)",
        "temporal_resolution": "Monthly",
        "plain_definition": (
            "The temperature of the air 2 meters above the mountain surface, providing the "
            "longest continuous climate record (1981–present) for Pakistan's northern ranges."
        ),
        "why_it_matters": (
            "Air temperature controls whether precipitation falls as snow or rain and sets "
            "the height of the summer freezing level where glaciers melt."
        ),
        "caveats": (
            "Global reanalysis grids average across valleys and peaks; elevation-band "
            "corrections are required to represent high glacier tongues accurately."
        ),
        "color_scale": "RdBu_r",
        "invert_hazard": False,  # Increase = warming/higher hazard
    },
    "lst_modis": {
        "id": "lst_modis",
        "name": "Land Surface Temperature (Day/Night Mean)",
        "short_name": "Land Surface Temp (LST)",
        "theme": "Temperature",
        "units": "°C",
        "decade_units": "°C / decade",
        "source_mission": "NASA MODIS (Terra) - MOD11C3 v6.1 Thermal Infrared",
        "partner_source": "Meteomatics Surface Skin Temperature (t_0m:C)",
        "nasa_power_param": "TS",
        "meteomatics_param": "t_0m:C",
        "start_year": 2000,
        "end_year": 2026,
        "spatial_resolution": "0.05° (~5 km)",
        "temporal_resolution": "Monthly",
        "plain_definition": (
            "The radiative 'skin' temperature of rock, snow, and glacier debris surfaces "
            "measured directly by thermal infrared sensors aboard NASA's Terra satellite."
        ),
        "why_it_matters": (
            "Directly captures heating of dark rock walls and debris-covered glacier tongues "
            "at 5 km resolution, complementing coarser air-temperature reanalyses."
        ),
        "caveats": (
            "Thermal infrared retrievals are only collected under clear-sky conditions, "
            "which can introduce a clear-sky bias during cloudy monsoon or winter months."
        ),
        "color_scale": "YlOrRd",
        "invert_hazard": False,
    },
    "precip_imerg": {
        "id": "precip_imerg",
        "name": "Total Precipitation (Rain + Snowfall)",
        "short_name": "Total Precipitation",
        "theme": "Precipitation",
        "units": "mm/month",
        "decade_units": "mm/month / decade",
        "source_mission": "NASA/JAXA GPM IMERG Final Run (GPM_3IMERGM v07)",
        "partner_source": "Meteomatics Weather API (precip_24h:mm)",
        "nasa_power_param": "PRECTOTCORR",
        "meteomatics_param": "precip_24h:mm",
        "start_year": 2000,
        "end_year": 2026,
        "spatial_resolution": "0.1° (~10 km)",
        "temporal_resolution": "Monthly",
        "plain_definition": (
            "Total monthly water equivalent falling from the sky as both rain and snow, "
            "estimated by NASA and JAXA's Global Precipitation Measurement constellation."
        ),
        "why_it_matters": (
            "Winter westerly storms nourish Karakoram and Hindu Kush glaciers, while intense "
            "summer monsoon cloudbursts can trigger flash floods and GLOFs."
        ),
        "caveats": (
            "Satellite radar and microwave sensors struggle to quantify light solid snowfall "
            "and steep orographic precipitation over high mountain ridges."
        ),
        "color_scale": "BrBG",
        "invert_hazard": False,
    },
    "snowfall_merra2": {
        "id": "snowfall_merra2",
        "name": "Solid Snowfall Precipitation",
        "short_name": "Snowfall Rate",
        "theme": "Precipitation",
        "units": "mm/month (WE)",
        "decade_units": "mm/month / decade",
        "source_mission": "NASA MERRA-2 Surface FluxDiagnostics (M2TMNXFLX v5.12.4)",
        "partner_source": "Meteomatics Fresh Snow Equivalent (fresh_snow_24h:cm)",
        "nasa_power_param": "PRECSNO",
        "meteomatics_param": "fresh_snow_24h:cm",
        "start_year": 1981,
        "end_year": 2026,
        "spatial_resolution": "0.5° x 0.625°",
        "temporal_resolution": "Monthly",
        "plain_definition": (
            "The portion of total monthly precipitation that falls specifically as solid "
            "snow (measured in millimeters of water equivalent)."
        ),
        "why_it_matters": (
            "Even if total precipitation stays constant, warming temperatures shift winter "
            "and spring storms from solid snowfall to liquid rain, starving glaciers of mass."
        ),
        "caveats": (
            "Partitioning between rain and snow in reanalysis depends on modeled freezing "
            "levels and sub-grid terrain elevation."
        ),
        "color_scale": "PuBuGn",
        "invert_hazard": True,
    },
    "swe_gldas": {
        "id": "swe_gldas",
        "name": "Snow Water Equivalent (SWE)",
        "short_name": "Snow Water Equivalent",
        "theme": "Water",
        "units": "mm",
        "decade_units": "mm / decade",
        "source_mission": "NASA GLDAS Noah Land Surface Model L4 (GLDAS_NOAH025_M v2.1)",
        "partner_source": "Meteomatics Hydrological Model (snow_water_equivalent:mm)",
        "nasa_power_param": "GWETPROF",
        "meteomatics_param": "snow_melt_24h:mm",
        "start_year": 2000,
        "end_year": 2026,
        "spatial_resolution": "0.25° (~25 km)",
        "temporal_resolution": "Monthly",
        "plain_definition": (
            "The depth of liquid water (in millimeters) that would result if the entire "
            "mountain snowpack melted instantaneously."
        ),
        "why_it_matters": (
            "SWE is the truest measure of seasonal water storage available for spring and "
            "summer irrigation across the Indus Basin."
        ),
        "caveats": (
            "Land surface models separate seasonal snowpack from deep multi-year glacier ice "
            "and rely on meteorological forcing quality."
        ),
        "color_scale": "GnBu",
        "invert_hazard": True,
    },
    "runoff_gldas": {
        "id": "runoff_gldas",
        "name": "Snowmelt & Surface Water Runoff",
        "short_name": "Meltwater Runoff",
        "theme": "Water",
        "units": "mm/month",
        "decade_units": "mm/month / decade",
        "source_mission": "NASA GLDAS Noah L4 (Qs_acc + Qsm_acc v2.1)",
        "partner_source": "Meteomatics Snowmelt Flux (snow_melt_24h:mm)",
        "nasa_power_param": "GWETTOP",
        "meteomatics_param": "snow_melt_24h:mm",
        "start_year": 2000,
        "end_year": 2026,
        "spatial_resolution": "0.25° (~25 km)",
        "temporal_resolution": "Monthly",
        "plain_definition": (
            "Combined monthly surface runoff from melting snow and rain flowing into "
            "headwater tributaries of the Indus River."
        ),
        "why_it_matters": (
            "Rising summer runoff can temporarily boost river flows ('peak water') while "
            "simultaneously escalating Glacial Lake Outburst Flood (GLOF) hazards."
        ),
        "caveats": (
            "Does not account for downstream dam regulation or deep groundwater routing."
        ),
        "color_scale": "Teal",
        "invert_hazard": False,
    },
    "humidity_airs": {
        "id": "humidity_airs",
        "name": "Relative Humidity (Near-Surface / Tropospheric)",
        "short_name": "Relative Humidity",
        "theme": "Atmosphere",
        "units": "%",
        "decade_units": "% / decade",
        "source_mission": "NASA Aqua AIRS L3 Monthly (AIRS3STM v7.0) / MERRA-2",
        "partner_source": "Meteomatics Weather API (relative_humidity_2m:p)",
        "nasa_power_param": "RH2M",
        "meteomatics_param": "relative_humidity_2m:p",
        "start_year": 2002,
        "end_year": 2026,
        "spatial_resolution": "1.0° (AIRS) / 0.5° (MERRA-2)",
        "temporal_resolution": "Monthly",
        "plain_definition": (
            "The amount of water vapor in the mountain air expressed as a percentage of "
            "saturation, retrieved by NASA's Atmospheric Infrared Sounder."
        ),
        "why_it_matters": (
            "Controls whether snow sublimates directly into dry air (cooling the glacier) "
            "or melts rapidly under humid, cloudy conditions."
        ),
        "caveats": (
            "Infrared sounders have coarser horizontal resolution over complex valleys."
        ),
        "color_scale": "YlGnBu",
        "invert_hazard": False,
    },
    "aerosols_omi": {
        "id": "aerosols_omi",
        "name": "Aerosol Optical Depth (AOD 550nm - Dust & Soot)",
        "short_name": "Aerosol Optical Depth",
        "theme": "Atmosphere",
        "units": "AOD Index",
        "decade_units": "AOD / decade",
        "source_mission": "NASA Aura OMI / MERRA-2 Aerosol Reanalysis (M2TMNXAER)",
        "partner_source": "Meteomatics Aerosol Optical Depth (aod_550nm:idx)",
        "nasa_power_param": "ALLSKY_SFC_SW_DWN",
        "meteomatics_param": "aod_550nm:idx",
        "start_year": 2000,
        "end_year": 2026,
        "spatial_resolution": "0.5° x 0.625°",
        "temporal_resolution": "Monthly",
        "plain_definition": (
            "A measure of airborne particles (mineral dust and black carbon soot) in the "
            "atmosphere column over the mountains."
        ),
        "why_it_matters": (
            "When dark soot and dust settle onto bright glacier snow, they lower surface "
            "albedo, causing the snowpack to absorb more solar energy and melt faster."
        ),
        "caveats": (
            "High surface reflectivity over bright snow makes satellite aerosol retrievals "
            "challenging without reanalysis assimilation."
        ),
        "color_scale": "Oranges",
        "invert_hazard": False,
    },
}


# Static Reference Datasets (Section 6 Table)
REFERENCE_DATASETS: List[Dict[str, str]] = [
    {
        "theme": "Glacier Reference",
        "variable": "Glacier Outlines & Area Mask",
        "source": "Randolph Glacier Inventory (RGI v6.0) / NASA GLIMS",
        "coverage": "Static Polygon Mask (South Asia West - Region 14)",
        "role": "Restricts grid calculations to glacierized pixels ('Glacier-Only Mask').",
    },
    {
        "theme": "Terrain",
        "variable": "Digital Elevation Model (DEM)",
        "source": "NASA SRTM (30m) / JAXA ALOS World 3D",
        "coverage": "Static Hypsometry (1,100 m – 8,611 m)",
        "role": "Powers elevation-band trend breakdown and temperature lapse-rate scaling.",
    },
]


def get_variable(variable_id: str) -> Dict[str, Any]:
    """Retrieve variable metadata by ID, defaulting to t2m_merra2."""
    return VARIABLES_CATALOGUE.get(variable_id, VARIABLES_CATALOGUE["t2m_merra2"])


def get_variables_by_theme(theme: str = "All") -> List[Dict[str, Any]]:
    """Return list of variable metadata dicts filtered by theme."""
    if not theme or theme == "All":
        return list(VARIABLES_CATALOGUE.values())
    return [v for v in VARIABLES_CATALOGUE.values() if v["theme"].lower() == theme.lower()]


def get_themes() -> List[str]:
    """Return ordered list of variable themes."""
    return ["Snow", "Temperature", "Precipitation", "Water", "Atmosphere"]
