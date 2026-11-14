"""
Mountain Hypsometry, 0°C Isotherm (Freezing Level) Migration Engine,
and 'Dark Ice' Albedo & Black-Carbon / Dust Melt Accelerator Calculator.
Calculates upward shift of the summer freezing line and Equilibrium Line Altitude (ELA),
newly exposed glacier ice (km²), and extra meltwater (mm/month) driven by aerosol darkening.
"""
from typing import Dict, Any, Optional
import numpy as np
import pandas as pd

from config.regions import get_region
from config.glaciers import get_glaciers_by_basin
from config.missions import DARK_ICE_ALBEDO_CONFIG

ENVIRONMENTAL_LAPSE_RATE_C_PER_KM = 6.5  # Standard mountain tropospheric lapse rate (°C / 1,000 m)


def compute_freezing_level_migration(
    region_id: str,
    temp_slope_per_decade_c: float,
    decades_elapsed: float = 4.5,
    custom_delta_temp_c: Optional[float] = None,
) -> Dict[str, Any]:
    """
    Calculate the upward shift of the summer 0°C isotherm (Freezing Level) and
    Equilibrium Line Altitude (ELA) over the historical record (or a custom scenario),
    and quantify the area of glacier ice (km²) newly exposed to summer melting.
    """
    region = get_region(region_id)
    delta_t_c = custom_delta_temp_c if custom_delta_temp_c is not None else (temp_slope_per_decade_c * decades_elapsed)

    # Vertical shift in meters: dZ = (dT / 6.5°C) * 1000m
    shift_per_decade_m = (temp_slope_per_decade_c / ENVIRONMENTAL_LAPSE_RATE_C_PER_KM) * 1000.0
    total_vertical_shift_m = (delta_t_c / ENVIRONMENTAL_LAPSE_RATE_C_PER_KM) * 1000.0

    # Baseline 1981 vs Current/Projected Summer Freezing Line (m)
    is_karakoram = "Karakoram" in region["parent_range"]
    baseline_ela_1981_m = 4920.0 if is_karakoram else 4580.0
    current_ela_m = baseline_ela_1981_m + total_vertical_shift_m

    # Estimate newly exposed glacier ice area (km²) within the equilibrium transition band (4,500–5,500 m)
    total_glacier_km2 = float(region["glacier_area_km2"])
    eq_band_glacier_share = float(region["elevation_bands"][2]["glacier_share"])  # 1,000m vertical band
    km2_per_vertical_meter = (total_glacier_km2 * eq_band_glacier_share) / 1000.0
    newly_exposed_ice_km2 = max(0.0, total_vertical_shift_m * km2_per_vertical_meter)
    newly_exposed_pct = 100.0 * newly_exposed_ice_km2 / max(1.0, total_glacier_km2)

    # Build glacier-by-glacier ELA migration table for glaciers in this basin
    glaciers = get_glaciers_by_basin(region_id)
    glacier_rows = []
    for g in glaciers:
        g_base_ela = float(g["ela_elevation_m"] - total_vertical_shift_m * 0.85)
        g_curr_ela = float(g["ela_elevation_m"] + (total_vertical_shift_m * 0.15 if custom_delta_temp_c else 0.0))
        if custom_delta_temp_c is not None:
            g_base_ela = float(g["ela_elevation_m"])
            g_curr_ela = float(g["ela_elevation_m"] + total_vertical_shift_m)

        exposed_g_km2 = round(g["area_km2"] * min(0.65, max(0.0, total_vertical_shift_m / 1800.0)), 2)
        glacier_rows.append({
            "glacier_name": g["name"],
            "range": g["range"],
            "snout_m": g["snout_elevation_m"],
            "baseline_ela_m": round(g_base_ela, 0),
            "shifted_ela_m": round(g_curr_ela, 0),
            "upward_shift_m": round(g_curr_ela - g_base_ela, 1),
            "peak_m": g["peak_elevation_m"],
            "newly_exposed_ice_km2": exposed_g_km2,
        })

    return {
        "region_name": region["name"],
        "delta_temp_c": round(float(delta_t_c), 2),
        "shift_per_decade_m": round(float(shift_per_decade_m), 1),
        "total_vertical_shift_m": round(float(total_vertical_shift_m), 1),
        "baseline_ela_m": round(baseline_ela_1981_m, 0),
        "current_ela_m": round(current_ela_m, 0),
        "total_glacier_area_km2": total_glacier_km2,
        "newly_exposed_ice_km2": round(newly_exposed_ice_km2, 1),
        "newly_exposed_pct": round(newly_exposed_pct, 2),
        "glacier_ela_table": pd.DataFrame(glacier_rows),
    }


def compute_dark_ice_albedo_melt(
    region_id: str,
    mean_aod: float = 0.22,
    aod_slope_per_decade: float = 0.024,
    custom_aod_multiplier: float = 1.0,
) -> Dict[str, Any]:
    """
    'Dark Ice' Albedo & Black-Carbon / Dust Melt Calculator.
    Quantifies how airborne soot and mineral dust (Aerosol Optical Depth at 550nm)
    darken mountain snow surfaces, reduce albedo, increase solar energy absorption (W/m²),
    and generate additional summer glacier meltwater (mm/month and Million Cubic Meters).
    """
    region = get_region(region_id)
    cfg = DARK_ICE_ALBEDO_CONFIG

    effective_aod = max(0.03, mean_aod * custom_aod_multiplier)
    aod_excess = max(0.0, effective_aod - 0.08)  # Above pristine background atmosphere (AOD ~ 0.08)

    # Albedo drop from pristine snow
    albedo_drop = (aod_excess / 0.10) * cfg["albedo_drop_per_0_1_aod"]
    effective_snow_albedo = max(cfg["bare_glacier_ice_albedo"], cfg["clean_snow_albedo"] - albedo_drop)

    # Extra absorbed shortwave solar radiation (W/m² = J / s / m²)
    extra_solar_wm2 = cfg["mean_summer_insolation_wm2"] * albedo_drop

    # Convert W/m² during daytime melt hours (~10 hrs/day * 30 days) into mm of ice melt per summer month
    seconds_active_per_month = 10.0 * 3600.0 * 30.0
    extra_energy_j_m2 = extra_solar_wm2 * seconds_active_per_month
    extra_melt_mm_per_month = extra_energy_j_m2 / cfg["latent_heat_fusion_j_per_kg"]

    # Over a 4-month ablation season (June–Sept) across the basin's glacierized area
    seasonal_extra_melt_mm = extra_melt_mm_per_month * 4.0
    glacier_area_m2 = float(region["glacier_area_km2"]) * 1e6
    extra_melt_volume_mcm = (seasonal_extra_melt_mm / 1000.0) * glacier_area_m2 / 1e6  # Million m³

    return {
        "region_name": region["name"],
        "effective_aod_550nm": round(effective_aod, 3),
        "aod_slope_per_decade": round(aod_slope_per_decade, 4),
        "clean_snow_albedo": cfg["clean_snow_albedo"],
        "darkened_snow_albedo": round(effective_snow_albedo, 3),
        "albedo_reduction_pct": round(albedo_drop * 100.0, 2),
        "extra_radiative_forcing_wm2": round(extra_solar_wm2, 2),
        "extra_melt_mm_per_month": round(extra_melt_mm_per_month, 1),
        "seasonal_extra_melt_mm": round(seasonal_extra_melt_mm, 1),
        "extra_melt_volume_mcm": round(extra_melt_volume_mcm, 1),
        "soot_melt_share_pct": round(min(42.0, 100.0 * extra_melt_mm_per_month / max(10.0, 85.0 + extra_melt_mm_per_month)), 1),
    }
