"""
Interactive Detective Casebook Missions, Downstream Indus Water Tower Parameters,
"What-If" Climate Scenarios, Global Climate Teleconnection Metadata,
"Dark Ice" Albedo & Black-Carbon Melt Config, "Signal-vs-Noise" Playground Presets,
and the 1-Click Judge's 60-Second Executive Tour.
"""
from typing import Dict, Any, List

# 1. Gamified "Earth System Detective Casebook" Missions
DETECTIVE_MISSIONS: List[Dict[str, Any]] = [
    {
        "id": "mission_shisper_2022",
        "title": "Mission 1: The May 2022 Hassanabad Bridge Collapse",
        "difficulty": "Field Detective",
        "badge_name": "GLOF Forensic Analyst",
        "region_id": "hunza",
        "glacier_id": "shisper",
        "variable_id": "t2m_merra2",
        "mystery_brief": (
            "On May 7, 2022, a massive Glacial Lake Outburst Flood (GLOF) burst from "
            "Shisper Glacier in Hunza Valley and swept away the concrete Hassanabad Bridge "
            "on the Karakoram Highway. Was this an isolated freak accident, or part of a "
            "statistically significant long-term warming trend combined with an extreme spring heat anomaly?"
        ),
        "investigation_steps": [
            "Load the Hunza River Basin 2m Air Temperature (NASA MERRA-2 / Meteomatics) series.",
            "Remove the seasonal cycle to inspect the deseasonalized anomaly timeline.",
            "Check the Mann-Kendall p-value, Sen's slope per decade, and the Isolation Forest compound anomaly flag."
        ],
        "quiz_question": "What does the deseasonalized trend analysis reveal about Hunza Valley temperatures?",
        "quiz_options": [
            "A statistically significant warming trend (~+0.3°C/decade, p < 0.05) that supercharged spring ice-dam melt.",
            "A statistically significant cooling trend across all elevations.",
            "Zero temperature change since 1981; the bridge collapsed purely from winter snowfall."
        ],
        "correct_option_index": 0,
        "scientific_debrief": (
            "Correct! Removing the seasonal cycle reveals a clear, statistically significant "
            "long-term warming trend in Hunza (~+0.31°C/decade, p < 0.01). When a record-breaking "
            "March–May 2022 spring heatwave rode on top of this warming baseline, meltwater "
            "rapidly overtopped Shisper Glacier's ice dam."
        ),
    },
    {
        "id": "mission_karakoram_anomaly",
        "title": "Mission 2: Unmasking the 'Karakoram Anomaly'",
        "difficulty": "Senior Scientist",
        "badge_name": "Cryosphere Contrast Specialist",
        "region_id": "karakoram",
        "compare_region_id": "hindu_kush",
        "glacier_id": "baltoro",
        "variable_id": "snow_cover_modis",
        "mystery_brief": (
            "For decades, glaciologists noticed something baffling: while glaciers in the "
            "Hindu Kush and Western Himalaya were rapidly losing snow cover and retreating, "
            "neighbouring glaciers in the central Karakoram (like Baltoro) remained remarkably "
            "stable. Can you prove this regional divergence statistically?"
        ),
        "investigation_steps": [
            "Compare NASA MODIS Snow Cover Fraction between the Karakoram Range and the Hindu Kush Range.",
            "Examine Sen's slope (% per decade) and the Hamed-Rao Modified Mann-Kendall test for both ranges.",
            "Inspect the Elevation-Band breakdown (>4,500 m vs. <3,500 m) and NAO Winter Westerlies correlation."
        ],
        "quiz_question": "How does snow cover trend in the Hindu Kush compare to the central Karakoram?",
        "quiz_options": [
            "Hindu Kush shows a sharp, statistically significant snow cover decline (>2%/decade), while the Karakoram shows a much smaller change due to high-altitude winter westerlies.",
            "Both ranges have gained 15% snow cover per decade.",
            "Snow cover in the Hindu Kush is increasing twice as fast as in the Karakoram."
        ],
        "correct_option_index": 0,
        "scientific_debrief": (
            "Spot on! Because over 55% of the Karakoram lies above 4,500 m and receives "
            "heavy winter snowfall from North Atlantic Oscillation (NAO) Westerlies, its high "
            "accumulation zone buffered losses for decades - whereas the lower, warmer Hindu Kush "
            "and Western Himalaya suffer steep, statistically significant snow losses."
        ),
    },
    {
        "id": "mission_indus_precip_noise",
        "title": "Mission 3: The Upper Indus Rainfall Illusion",
        "difficulty": "Chief Data Detective",
        "badge_name": "Statistical Integrity Guardian",
        "region_id": "upper_indus",
        "glacier_id": "biafo",
        "variable_id": "precip_imerg",
        "mystery_brief": (
            "A local newspaper claims that total rainfall in the Upper Indus Basin has "
            "permanently increased by 20% over the last two decades based on a single wet "
            "monsoon year. As an Earth System Trend Detective, test whether the long-term "
            "monthly precipitation trend is actually statistically significant!"
        ),
        "investigation_steps": [
            "Load Total Precipitation (NASA GPM IMERG / MERRA-2) for the Upper Indus Basin.",
            "Check the Mann-Kendall p-value and 95% confidence interval on Sen's slope.",
            "Observe whether the 95% confidence interval crosses zero."
        ],
        "quiz_question": "What is the scientifically honest verdict for Upper Indus Basin total precipitation?",
        "quiz_options": [
            "There is a slight upward tendency, but the trend is NOT statistically significant (p >= 0.05) due to large year-to-year variability.",
            "The trend is 100% proven with p = 0.00001.",
            "Seasonal removal is unnecessary for precipitation data."
        ],
        "correct_option_index": 0,
        "scientific_debrief": (
            "Bravo! In science, 'no statistically significant trend detected yet' is a vital, "
            "valid conclusion. High inter-annual variability (El Niño/La Niña swings and sporadic "
            "monsoon bursts) produces wide confidence intervals that cross zero (p > 0.05)."
        ),
    },
]


# 2. Downstream "Indus Water Tower" & Tarbela Dam Baseline Parameters
INDUS_WATER_TOWER_CONFIG: Dict[str, Any] = {
    "mean_annual_inflow_maf": 64.5,          # Tarbela / Besham mean annual flow (Million Acre-Feet)
    "meltwater_contribution_pct": 72.0,      # ~72% of Upper Indus flow comes from snow + glacier melt
    "irrigated_cropland_million_ha": 18.2,   # Indus Basin Irrigation System (IBIS) command area
    "population_dependent_millions": 240.0,  # Downstream population relying on Indus basin water
    "hydropower_projects": [
        {"name": "Tarbela Dam (Existing + T4/T5)", "capacity_mw": 4888, "basin": "Upper Indus"},
        {"name": "Diamer-Bhasha Dam (Under Construction)", "capacity_mw": 4500, "basin": "Upper Indus"},
        {"name": "Dasu Hydropower Project", "capacity_mw": 4320, "basin": "Upper Indus"},
        {"name": "Mangla / Neelum-Jhelum System", "capacity_mw": 2119, "basin": "Western Himalaya / Neelum"},
    ],
    "total_hydropower_mw": 15827,
    "crop_seasons": {
        "rabi": {
            "name": "Rabi Season (Oct–Mar: Wheat, Barley, Gram)",
            "snowmelt_dependency_pct": 65.0,
            "critical_months": [3, 4, 5],
        },
        "kharif": {
            "name": "Kharif Season (Apr–Sep: Rice, Cotton, Sugarcane, Maize)",
            "glacier_melt_dependency_pct": 78.0,
            "critical_months": [6, 7, 8],
        },
    },
}


# 3. Interactive "What-If" Climate Scenario Presets
CLIMATE_SCENARIOS: Dict[str, Dict[str, Any]] = {
    "paris_1_5c": {
        "id": "paris_1_5c",
        "name": "Paris Target (+1.5°C Warming / Stable Winter Snow)",
        "delta_temp_c": 1.5,
        "delta_winter_precip_pct": 2.0,
        "delta_summer_rain_pct": 5.0,
        "description": "Strong global mitigation limiting regional mountain warming to +1.5°C above baseline.",
    },
    "current_trajectory_2_4c": {
        "id": "current_trajectory_2_4c",
        "name": "Current Trajectory (+2.4°C Warming / -8% Snowfall Shift)",
        "delta_temp_c": 2.4,
        "delta_winter_precip_pct": -8.0,
        "delta_summer_rain_pct": 14.0,
        "description": "Mid-century projection under current policy pledges; freezing line rises ~370 m.",
    },
    "high_emissions_3_5c": {
        "id": "high_emissions_3_5c",
        "name": "High Emissions SSP5-8.5 (+3.5°C Warming / -18% Snowfall Shift)",
        "delta_temp_c": 3.5,
        "delta_winter_precip_pct": -18.0,
        "delta_summer_rain_pct": 25.0,
        "description": "Severe warming scenario pushing the summer 0°C isotherm up by >530 m and accelerating GLOF risk.",
    },
    "westerlies_surge": {
        "id": "westerlies_surge",
        "name": "Enhanced NAO Westerlies (+1.8°C / +15% Winter Snow)",
        "delta_temp_c": 1.8,
        "delta_winter_precip_pct": 15.0,
        "delta_summer_rain_pct": 4.0,
        "description": "Tests whether stronger winter westerly snowfall can continue buffering Karakoram glaciers against warming.",
    },
}


# 4. Global Climate Teleconnection Indices Metadata
TELECONNECTION_INDICES: Dict[str, Dict[str, str]] = {
    "nao": {
        "id": "nao",
        "name": "North Atlantic Oscillation (NAO)",
        "primary_season": "Winter–Spring (DJFM)",
        "mechanism": (
            "Positive winter NAO phases strengthen the mid-latitude subtropical westerly "
            "jet stream, steering moisture from the Mediterranean and Caspian Seas directly "
            "into the Karakoram and Hindu Kush as high-altitude snowfall."
        ),
    },
    "enso": {
        "id": "enso",
        "name": "El Niño–Southern Oscillation (ENSO / Niño 3.4)",
        "primary_season": "Summer Monsoon (JJAS) & Winter",
        "mechanism": (
            "El Niño events typically suppress the South Asian summer monsoon over the "
            "Western Himalaya while altering winter westerly storm tracks; La Niña often "
            "enhances monsoon moisture intrusion into northern Pakistan (as in summer 2022)."
        ),
    },
    "iod": {
        "id": "iod",
        "name": "Indian Ocean Dipole (IOD)",
        "primary_season": "Late Spring–Summer (MJJA)",
        "mechanism": (
            "Positive IOD warms the western Indian Ocean and Arabian Sea, pumping warm, "
            "humid air masses northward up the Indus valley that accelerate snowmelt."
        ),
    },
}


# 5. "Dark Ice" Albedo & Black-Carbon / Dust Radiative Forcing Config
DARK_ICE_ALBEDO_CONFIG: Dict[str, float] = {
    "clean_snow_albedo": 0.78,               # Fresh high-altitude snow reflects 78% of sunlight
    "aged_snow_albedo": 0.58,                # Metamorphosed summer snowpack
    "bare_glacier_ice_albedo": 0.34,         # Exposed dirty glacier ice in ablation zone
    "albedo_drop_per_0_1_aod": 0.042,        # Albedo reduction per +0.1 Aerosol Optical Depth (soot/dust)
    "mean_summer_insolation_wm2": 295.0,     # High-altitude Karakoram/Himalaya summer solar flux (W/m²)
    "latent_heat_fusion_j_per_kg": 334000.0, # Energy required to melt 1 kg (1 mm over 1 m²) of ice
}


# 6. Interactive "Signal-vs-Noise" Statistical Playground Presets
SIGNAL_NOISE_PRESETS: List[Dict[str, Any]] = [
    {
        "id": "short_noisy_record",
        "name": "Why 8 Years Is Too Short (Hidden Trend)",
        "years": 8,
        "true_slope_per_decade": 0.30,
        "noise_std": 0.85,
        "seasonal_amplitude": 11.0,
        "missing_pct": 12.0,
        "lesson": (
            "Even though a real warming trend (+0.30/decade) exists in the synthetic generator, "
            "an 8-year record with high inter-annual variability yields p > 0.05 ('Not Significant')."
        ),
    },
    {
        "id": "forty_year_proof",
        "name": "How 40 Years Unlocks Statistical Proof",
        "years": 40,
        "true_slope_per_decade": 0.30,
        "noise_std": 0.85,
        "seasonal_amplitude": 11.0,
        "missing_pct": 2.0,
        "lesson": (
            "With the exact same slope (+0.30/decade) and noise level, extending the satellite record "
            "to 40 years shrinks the confidence interval and achieves p < 0.001!"
        ),
    },
    {
        "id": "pure_mountain_noise",
        "name": "Pure Random Weather Swings (Zero True Trend)",
        "years": 25,
        "true_slope_per_decade": 0.00,
        "noise_std": 1.15,
        "seasonal_amplitude": 9.5,
        "missing_pct": 5.0,
        "lesson": (
            "Demonstrates that Mann-Kendall and Hamed-Rao Modified MK protect scientists from "
            "claiming false trends when looking at random year-to-year weather fluctuations."
        ),
    },
]


# 7. 1-Click "Judge's 60-Second Executive Tour" Steps (Mapped to NASA Rubric)
JUDGE_EXECUTIVE_TOUR_STEPS: List[Dict[str, str]] = [
    {
        "pillar": "1. Relevance & Scientific Rigor",
        "title": "Seasonal Removal + Hamed-Rao Modified Mann-Kendall",
        "highlight": (
            "Directly fulfills 'Be An Earth System Trend Detective': removes the massive mountain "
            "seasonal cycle, computes Sen's robust slope per decade, and corrects for lag-1 serial "
            "autocorrelation using Hamed-Rao Modified Mann-Kendall."
        ),
        "target_tab": "Detective Mode & Results",
    },
    {
        "pillar": "2. Regional Contrast Discovery",
        "title": "The 'Karakoram Anomaly' vs. Hindu Kush Retreat",
        "highlight": (
            "Proves the challenge's central thesis - that neighbouring mountain ranges can behave "
            "differently - by contrasting central Karakoram stability (Baltoro/Siachen) against rapid "
            "snow loss in the Hindu Kush (Chitral) and Western Himalaya (Astore/Neelum)."
        ),
        "target_tab": "Compare & Spatial Maps",
    },
    {
        "pillar": "3. Creativity & AI/ML Innovation",
        "title": "Explainable ML Driver Lab + Dark-Ice Albedo & 0°C Isotherm",
        "highlight": (
            "Combines Gaussian Process non-linear trend/changepoint detection, Random Forest driver "
            "attribution, K-Means regime clustering, 0°C freezing-line elevation migration, and "
            "black-carbon/dust albedo melt acceleration."
        ),
        "target_tab": "AI / ML Lab & Cryosphere Physics",
    },
    {
        "pillar": "4. Real-World Impact (240 Million People)",
        "title": "HimalayaShield Live 7-Day GLOF Radar & Indus Water Tower Simulator",
        "highlight": (
            "Links glacier trends to 15 real GLOF hotspots (like Shisper Glacier / Hassanabad Bridge), "
            "live 7-day Meteomatics melt forecasts, and downstream Tarbela Dam water security (64.5 MAF) "
            "for Rabi/Kharif crops and 15,827 MW of hydropower."
        ),
        "target_tab": "HimalayaShield & Indus Water Tower",
    },
    {
        "pillar": "5. Presentation & Educational Honesty",
        "title": "Gamified Detective Missions & Signal-vs-Noise Playground",
        "highlight": (
            "Teaches students why 'no statistically significant trend yet' is a valid scientific "
            "finding through interactive mystery missions and a live Signal-vs-Noise statistical sandbox."
        ),
        "target_tab": "Detective Missions & Statistical Sandbox",
    },
]
