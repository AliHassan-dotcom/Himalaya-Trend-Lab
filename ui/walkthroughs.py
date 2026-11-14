"""
Three Guided Demo Walkthrough Cases for Himalaya Trend Lab (Section 5.4).
1. Karakoram vs. Hindu Kush Snow Cover (The Karakoram Anomaly)
2. Summer Temperature Above Hunza Glacier Valley (Clear Warming + Shisper 2022)
3. Upper Indus Precipitation (Teaching "No Statistically Significant Trend Yet")
"""
from typing import Dict, Any, List

DEMO_WALKTHROUGHS: List[Dict[str, Any]] = [
    {
        "case_id": "case_01_karakoram_anomaly",
        "code": "Case 01",
        "subtitle": "Regional cryosphere comparison (2000 to 2026)",
        "title": "Karakoram vs. Hindu Kush Snow Cover",
        "region_id": "karakoram",
        "compare_region_id": "hindu_kush",
        "variable_id": "snow_cover_modis",
        "question": "Why does central Karakoram snow cover remain resilient while the neighboring Hindu Kush declines?",
        "summary": (
            "Demonstrates regional divergence: central Karakoram high-altitude snow cover remains "
            "buffered (-0.35%/decade), whereas the neighboring Hindu Kush shows a steep, "
            "statistically significant decline (-2.45%/decade, p < 0.0001)."
        ),
        "takeaway": "Neighboring mountain ranges can trend at markedly different rates due to winter westerly tracks and elevation hypsometry.",
        "detective_takeaway": (
            "MODIS Terra MOD10CM (2000 to 2026) and MERRA-2 records show that winter westerly troughs (positive NAO phase) "
            "deliver snow accumulation to the high-altitude Karakoram (mean elevation 5,350 m), whereas lower-elevation Hindu Kush "
            "catchments experience rain-on-snow transition and statistically significant snow cover loss."
        ),
        "story_steps": [
            "1. Remove 12-month seasonal snow cycle (winter peak ~86%, summer trough ~34%) before computing trends.",
            "2. Apply Hamed-Rao modified Mann-Kendall to account for lag-1 month-to-month snow persistence.",
            "3. Compare Sen's slope across RGI v6.0 glacier zones in Karakoram vs. Hindu Kush.",
        ],
    },
    {
        "case_id": "case_02_hunza_heat",
        "code": "Case 02",
        "subtitle": "Forensic attribution of the May 7, 2022 outburst flood",
        "title": "Hunza Air Temperature and the 2022 Shisper GLOF",
        "region_id": "hunza",
        "compare_region_id": "astore",
        "variable_id": "t2m_merra2",
        "question": "How did multi-decadal warming and a spring heatwave trigger the May 2022 Hassanabad Bridge collapse?",
        "summary": (
            "Removing the 23.6 °C winter-to-summer seasonal swing reveals a clear +0.35 °C/decade "
            "warming trend (p < 0.0001) that elevated the 0 °C isotherm prior to the May 2022 Shisper Glacier outburst flood."
        ),
        "takeaway": "Deseasonalizing monthly records is required in mountain basins where seasonal swings are 20x larger than the decadal trend.",
        "detective_takeaway": (
            "Across the 1981 to 2026 MERRA-2 record, Hunza 2m air temperature increased significantly, lifting the summer 0 °C freezing "
            "isotherm by ~200 m. In March to May 2022, a +3.4 °C spring temperature anomaly accelerated meltwater ponding behind Shisper "
            "Glacier's ice dam, culminating in the May 7, 2022 outburst flood (>5,000 m³/s) at Hassanabad Bridge."
        ),
        "story_steps": [
            "1. Subtract 1981 to 2026 calendar-month climatology to isolate temperature anomalies.",
            "2. Confirm monotonic warming via Theil-Sen median slope and 95% confidence interval.",
            "3. Evaluate upward migration of the 0 °C freezing isotherm relative to Shisper ELA (5,180 m).",
        ],
    },
    {
        "case_id": "case_03_indus_precip",
        "code": "Case 03",
        "subtitle": "Separating interannual weather noise from secular trend",
        "title": "Upper Indus Precipitation: Signal vs. Noise",
        "region_id": "upper_indus",
        "compare_region_id": "western_himalaya",
        "variable_id": "precip_imerg",
        "question": "Does a noisy precipitation record constitute a statistically significant climate trend?",
        "summary": (
            "Shows a slight upward tendency (+1.10 mm/month/decade), but the 95% confidence interval "
            "crosses zero and Hamed-Rao Mann-Kendall returns p >= 0.05 (No significant trend yet)."
        ),
        "takeaway": "In hydrometeorology, reporting 'no statistically significant trend detected yet' is an essential scientific safeguard against over-claiming.",
        "detective_takeaway": (
            "Extreme single-year monsoon intrusions (such as July-August 2010 and August 2022) create high interannual variance "
            "(sigma = 16.5 mm/month) in Upper Indus GPM IMERG records. Because the 95% confidence interval spans zero and adjusted "
            "p >= 0.05, a long-term monotonic shift cannot yet be distinguished from natural variability."
        ),
        "story_steps": [
            "1. Inspect deseasonalized monthly precipitation anomalies including the 2010 and 2022 extremes.",
            "2. Compare OLS parametric slope (sensitive to 2022 outliers) against robust Theil-Sen median slope.",
            "3. Verify that the 95% confidence interval crosses zero and Hamed-Rao p >= alpha.",
        ],
    },
]
