"""
Downstream Indus Water Tower & Tarbela Dam Impact Simulator (Section 8 & 15).
Translates upper-basin snow/glacier trends and interactive "What-If" climate scenarios
into seasonal inflows (Million Acre-Feet / MAF), Rabi & Kharif agricultural water balance,
hydropower generation (MW), and the decadal 'Peak Water' tipping point curve (2020–2080).
"""
from typing import Dict, Any, Optional
import numpy as np
import pandas as pd

from config.regions import get_region
from config.missions import INDUS_WATER_TOWER_CONFIG, CLIMATE_SCENARIOS


def simulate_indus_water_security(
    region_id: str = "upper_indus",
    scenario_id: str = "current_trajectory_2_4c",
    custom_delta_temp_c: Optional[float] = None,
    custom_delta_winter_snow_pct: Optional[float] = None,
) -> Dict[str, Any]:
    """
    Simulate how upper-basin cryosphere trends and warming scenarios impact:
    1. Decadal Indus River inflows at Tarbela Dam (MAF) from 2020 to 2080 ('Peak Water' curve).
    2. Rabi (wheat) vs. Kharif (rice/cotton/sugarcane) seasonal irrigation water availability.
    3. Hydropower output across 15,827 MW of major cascade plants (Tarbela, Diamer-Bhasha, Dasu, Mangla).
    """
    region = get_region(region_id)
    scenario = CLIMATE_SCENARIOS.get(scenario_id, CLIMATE_SCENARIOS["current_trajectory_2_4c"])
    cfg = INDUS_WATER_TOWER_CONFIG

    delta_t = custom_delta_temp_c if custom_delta_temp_c is not None else float(scenario["delta_temp_c"])
    delta_snow_pct = (
        custom_delta_winter_snow_pct
        if custom_delta_winter_snow_pct is not None
        else float(scenario["delta_winter_precip_pct"])
    )

    # Peak Water Physics:
    # Higher warming accelerates glacier melt initially (pushing Peak Water earlier and higher),
    # followed by steeper late-century decline as glacier volume shrinks.
    peak_year = int(np.clip(2048 - (delta_t - 1.5) * 6.5 + (delta_snow_pct * 0.35), 2030, 2060))
    years = np.arange(2020, 2085, 5)

    base_maf = cfg["mean_annual_inflow_maf"]
    inflow_maf = []
    glacier_mass_remaining_pct = []

    for yr in years:
        dt_yr = (yr - 2020) / 60.0
        # Remaining glacier ice volume (%)
        mass_rem = max(18.0, 100.0 - (delta_t * 14.5 * (dt_yr ** 1.18)) + (delta_snow_pct * 0.45 * dt_yr))
        glacier_mass_remaining_pct.append(round(float(mass_rem), 1))

        # Meltwater surge before peak_year, decline after peak_year as ice area shrinks
        surge = (delta_t * 3.8) * np.exp(-0.5 * ((yr - peak_year) / 14.0) ** 2)
        depletion = max(0.0, (yr - peak_year) * 0.38 * (delta_t / 2.0))
        snow_offset = base_maf * (delta_snow_pct / 100.0) * 0.35
        flow = base_maf + surge - depletion + snow_offset
        inflow_maf.append(round(float(max(32.0, flow)), 2))

    timeline_df = pd.DataFrame({
        "year": years,
        "projected_inflow_maf": inflow_maf,
        "baseline_inflow_maf": base_maf,
        "glacier_volume_remaining_pct": glacier_mass_remaining_pct,
    })

    # Mid-century (2050) vs Late-century (2075) seasonal agricultural & hydropower impact
    rabi_shift_pct = round(delta_snow_pct * 0.55 - max(0.0, delta_t - 1.5) * 4.2, 1)
    kharif_2040_shift_pct = round(delta_t * 3.5 + delta_snow_pct * 0.25, 1)  # Pre-peak melt surge
    kharif_2075_shift_pct = round(-delta_t * 6.8 + delta_snow_pct * 0.40, 1)  # Post-peak melt deficit

    # Hydropower generation impact across the 15,827 MW cascade
    total_mw = cfg["total_hydropower_mw"]
    effective_2075_mw = round(total_mw * (1.0 + min(0.08, kharif_2075_shift_pct / 100.0 * 0.75)), 0)

    return {
        "region_name": region["name"],
        "scenario_name": scenario["name"],
        "delta_temp_c": round(delta_t, 2),
        "delta_winter_snow_pct": round(delta_snow_pct, 1),
        "peak_water_year": peak_year,
        "peak_inflow_maf": float(max(inflow_maf)),
        "inflow_2075_maf": float(inflow_maf[-2]),
        "glacier_ice_remaining_2080_pct": float(glacier_mass_remaining_pct[-1]),
        "rabi_wheat_water_change_pct": rabi_shift_pct,
        "kharif_2040_melt_surge_pct": kharif_2040_shift_pct,
        "kharif_2075_water_deficit_pct": kharif_2075_shift_pct,
        "installed_hydropower_mw": total_mw,
        "projected_2075_firm_hydropower_mw": effective_2075_mw,
        "population_affected_millions": cfg["population_dependent_millions"],
        "irrigated_cropland_million_ha": cfg["irrigated_cropland_million_ha"],
        "hydropower_projects": pd.DataFrame(cfg["hydropower_projects"]),
        "timeline_df": timeline_df,
    }
