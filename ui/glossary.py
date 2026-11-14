"""
Statistical & Glaciological Glossary and Scientific Limitations (Sections 5.2 & 11).
"""
from typing import List, Dict, Any

GLOSSARY_TERMS: List[Dict[str, str]] = [
    {
        "term": "Sen's Slope (Theil-Sen Estimator)",
        "definition": "A non-parametric robust trend rate calculated as the median of all pairwise slopes between time points. Unlike ordinary linear regression, it is not distorted by single-month outlier spikes.",
    },
    {
        "term": "Mann-Kendall Test (tau and p-value)",
        "definition": "A rank-based statistical test that evaluates whether a series moves monotonically upward or downward over time without assuming a normal distribution.",
    },
    {
        "term": "Hamed-Rao Modified Mann-Kendall",
        "definition": "An autocorrelation-corrected Mann-Kendall test (Hamed and Rao, 1998). Because monthly temperature and snow anomalies persist from one month to the next (lag-1 memory), standard tests underestimate variance; Hamed-Rao scales variance by n/n* to prevent false positives.",
    },
    {
        "term": "Deseasonalized Anomaly",
        "definition": "The departure of each monthly observation from the long-term mean for that specific calendar month (for example, comparing May 2022 against the 1981 to 2026 May mean).",
    },
    {
        "term": "Benjamini-Hochberg FDR Control",
        "definition": "False Discovery Rate control (Benjamini and Hochberg, 1995) applied across spatial grid cells so simultaneous hypothesis testing does not inflate regional significance claims.",
    },
    {
        "term": "Equilibrium Line Altitude (ELA and 0 °C Isotherm)",
        "definition": "The altitude separating the upper glacier accumulation zone (net annual snow gain) from the lower ablation zone (net annual ice melt).",
    },
]

SCIENTIFIC_LIMITATIONS: List[Dict[str, Any]] = [
    {
        "title": "Reanalysis Grid Resolution vs. Valley Glacier Scale",
        "issue": "MERRA-2 (0.5° x 0.625°, ~50 km) and GLDAS-2.1 (0.25°, ~27 km) grid cells average across steep ridge-to-valley topography and cannot resolve individual glacier tongues (1 to 5 km wide).",
        "how_we_handle_it": "We apply cosine-latitude area weighting, RGI v6.0 glacier-polygon masking, and lapse-rate elevation-band disaggregation (<3,500 m to >5,500 m), and cross-check against 5 km MODIS products.",
    },
    {
        "title": "Optical Record Length and Cloud Cover Gaps",
        "issue": "Satellite optical records (MODIS Terra MOD10CM/MOD11C3 and GPM IMERG) start in 2000 (26 years), and winter/monsoon cloud cover obscures optical pixels over high terrain.",
        "how_we_handle_it": "We flag cloud-interpolated months, warn whenever selected windows fall below the 25 to 30 year climatological benchmark, and pair optical series with 45-year MERRA-2 reanalysis (1981 to 2026).",
    },
    {
        "title": "Serial Autocorrelation in Monthly Cryosphere Records",
        "issue": "Snowpack, soil moisture, and temperature anomalies exhibit strong lag-1 autocorrelation (r1 = 0.25 to 0.55), which causes standard Mann-Kendall and OLS tests to overstate statistical significance.",
        "how_we_handle_it": "All primary verdicts use the Hamed-Rao (1998) variance inflation factor (VIF) adjustment on deseasonalized anomalies.",
    },
    {
        "title": "Surface Snow Cover Area vs. Total Glacier Mass Balance",
        "issue": "MODIS MOD10CM measures 2D surface snow cover fraction (%) rather than ice thickness or geodetic mass balance.",
        "how_we_handle_it": "We evaluate MODIS snow cover alongside GLDAS Snow Water Equivalent (SWE, mm) and Meteomatics snow depth, and explicitly distinguish surface area trends from volumetric mass balance.",
    },
    {
        "title": "Spatial Grid Simulation and Multiple-Testing Sensitivity",
        "issue": "Sub-basin 10x10 spatial grids combine SRTM hypsometry with regional signal-to-noise scaling; under strict Benjamini-Hochberg FDR thresholds (p <= k/m * alpha), moderate-SNR grids can yield 0% FDR-passing cells even when the basin-mean series is significant.",
        "how_we_handle_it": "We report both raw significant cells and BH-FDR adjusted cells, and rely on the basin-aggregated Hamed-Rao test for the primary regional verdict.",
    },
    {
        "title": "Statistical Detection vs. Physical Attribution",
        "issue": "Non-parametric trend tests (Mann-Kendall, Sen's slope) prove whether a monotonic shift exceeds background variability, but cannot by themselves prove physical causation.",
        "how_we_handle_it": "We pair statistical detection with physical covariates (NAO, ENSO, OMI aerosols) and out-of-sample Random Forest driver attribution while noting attribution caveats.",
    },
]
