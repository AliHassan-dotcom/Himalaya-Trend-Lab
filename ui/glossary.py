"""
Interactive Statistical & Glaciological Glossary and Scientific Limitations (Sections 5.2 & 11).
"""
from typing import List, Dict

GLOSSARY_TERMS: List[Dict[str, str]] = [
    {
        "term": "Sen's Slope (Theil–Sen Estimator)",
        "definition": "A non-parametric robust trend rate calculated as the median of all pairwise slopes between time points. Unlike ordinary linear regression, it is not distorted by extreme outlier months.",
    },
    {
        "term": "Mann–Kendall Test (τ & p-value)",
        "definition": "A rank-based statistical test that checks whether a variable consistently moves upward or downward over time without assuming a bell-curve normal distribution.",
    },
    {
        "term": "Hamed–Rao Modified Mann–Kendall",
        "definition": "An autocorrelation-corrected Mann–Kendall test. Because a warm or snowy month often persists into the next month (lag-1 memory), standard tests can produce false positives; Hamed–Rao adjusts the variance to prevent over-claiming.",
    },
    {
        "term": "Deseasonalized Anomaly",
        "definition": "The departure of a month's value from its long-term average for that specific calendar month (e.g., comparing May 2022 only against typical Mays).",
    },
    {
        "term": "Benjamini–Hochberg FDR Stippling",
        "definition": "False Discovery Rate control applied across spatial map pixels so random noise across hundreds of grid cells does not masquerade as significant regional change.",
    },
    {
        "term": "Equilibrium Line Altitude (ELA / 0°C Isotherm)",
        "definition": "The mountain altitude separating the upper glacier accumulation zone (net snow gain) from the lower ablation zone (net ice melt).",
    },
]

SCIENTIFIC_LIMITATIONS: List[str] = [
    "Many optical satellite records (MODIS, GPM IMERG) begin in 2000; 25-year records can be too short to detect weak multi-decadal precipitation signals.",
    "Steep Karakoram and Himalayan relief creates topographic shadowing, cloud gaps, and orographic precipitation uncertainty.",
    "Optical snow cover fraction (MOD10CM) measures surface snow area rather than ice thickness or total glacier mass.",
    "A statistically significant trend proves that a physical change is occurring above noise, not its causal attribution.",
]
