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
        "code": "CASE 01",
        "title": "Karakoram vs. Hindu Kush Snow Cover",
        "region_id": "karakoram",
        "compare_region_id": "hindu_kush",
        "variable_id": "snow_cover_modis",
        "summary": (
            "Proves regional divergence: central Karakoram high-altitude snow cover remains "
            "buffered (-0.35%/decade), whereas the neighbouring Hindu Kush shows a steep, "
            "statistically significant decline (-2.45%/decade, p < 0.001)."
        ),
        "takeaway": "Why local analysis matters: neighbouring mountain ranges can trend at very different rates.",
    },
    {
        "case_id": "case_02_hunza_heat",
        "code": "CASE 02",
        "title": "Hunza Summer Heat & Shisper GLOF",
        "region_id": "hunza",
        "compare_region_id": "astore",
        "variable_id": "t2m_merra2",
        "summary": (
            "Removing the 23.6°C winter-to-summer seasonal swing reveals a clear +0.31°C/decade "
            "warming trend (p < 0.01) that supercharged the May 2022 Shisper Glacier outburst flood."
        ),
        "takeaway": "Removing the seasonal cycle is essential in mountain regions where seasonality dwarfs the decadal slope.",
    },
    {
        "case_id": "case_03_indus_precip",
        "code": "CASE 03",
        "title": "Upper Indus Rainfall Illusion",
        "region_id": "upper_indus",
        "compare_region_id": "western_himalaya",
        "variable_id": "precip_imerg",
        "summary": (
            "Shows a slight upward tendency (+1.10 mm/month/decade), but the 95% confidence interval "
            "crosses zero and Hamed-Rao Mann-Kendall returns p >= 0.05 (Not Significant Yet)."
        ),
        "takeaway": "In Earth science, 'no statistically significant trend detected yet' is an honest, valid scientific conclusion.",
    },
]
