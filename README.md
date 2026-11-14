# Himalaya Trend Lab — Be a Data Detective for Pakistan's Glaciers

**2026 NASA Space Apps Challenge** | **Challenge:** *Be An Earth System Trend Detective*  
**Prepared By:** Ali Hassan | **Version:** 1.0

---

## 1. Mission Overview
Pakistan is home to **7,253 glaciers** across the Karakoram, Hindu Kush, and Western Himalaya—more glacial ice than anywhere on Earth outside the polar regions. While these glaciers sustain **240 million people** downstream via the Indus River (`64.5 MAF` mean annual inflow at Tarbela Dam and `15,827 MW` of hydropower), rapid warming and rising freezing levels also trigger catastrophic **Glacial Lake Outburst Floods (GLOFs)**, such as the May 7, 2022 Shisper Glacier outburst flood that destroyed the Hassanabad Bridge on the Karakoram Highway.

**Himalaya Trend Lab** is an interactive scientific workbench and cinematic scrollytelling web application that empowers researchers, students, and disaster planners to interrogate **45 years (1981–2026)** of NASA satellite observations and Meteomatics high-mountain weather data—separating genuine long-term cryosphere trends from seasonal cycles, autocorrelation, and short-term weather noise.

---

## 2. Six-Layer System Architecture

```text
Himalaya Trend Lab/
├── config/                  # Layer 1: 9 Basins, 15 Glaciers, 10 Variables, Missions & Scenarios
│   ├── settings.py          # Global paths, .env credentials loader, statistical α thresholds
│   ├── regions.py           # 9 Pakistan river basins/ranges + custom bounding-box builder
│   ├── glaciers.py          # 15 iconic glaciers & GLOF lakes + infrastructure exposure ledger
│   ├── variables.py         # 5 Detective Questions + 10 NASA/Meteomatics variables
│   └── missions.py          # 3 Gamified Missions, Indus Water Tower config, IPCC scenarios
├── data/                    # Layer 2: Multi-Sensor APIs, 7-Day Forecasts & Local Disk Cache
│   ├── meteomatics_client.py# Live Meteomatics Weather API client (HTTP Basic Auth)
│   ├── nasa_client.py       # Live NASA POWER (MERRA-2) monthly API client
│   ├── forecast_client.py   # 7-day glacier weather & snowmelt GLOF radar client
│   ├── cache_manager.py     # MD5 CSV disk cache (data/cached/) + 1,000 queries/day quota tracker
│   └── generator.py         # Physically coupled 1981–2026 baseline assimilation & 10x10 spatial grids
├── analytics/               # Layer 3: Statistical, Glaciological & Hydrological Impact Engine
│   ├── seasonal.py          # 12-month climatology removal, STL decomposition, Dominance Ratio
│   ├── trend_tests.py       # Theil-Sen slope + 95% CI, OLS, Original/Seasonal/Hamed-Rao Mann-Kendall
│   ├── spatial_trends.py    # Benjamini-Hochberg FDR grid stippling & 4 vertical elevation bands
│   ├── freezing_level.py    # 0°C isotherm & ELA vertical migration + Dark-Ice soot albedo melt
│   ├── water_security.py    # Indus Water Tower & Tarbela Dam Peak Water simulator (2020–2080)
│   ├── teleconnections.py   # NAO, ENSO, IOD attribution + Multi-Sensor cross-validation
│   └── verdict.py           # Plain-language verdict engine answering the 4 challenge questions
├── ml/                      # Layer 4: Pre-Trained Scikit-Learn Machine Learning Suite
│   ├── nonlinear_trend.py   # Gaussian Process Regression (RBF + WhiteKernel) + Changepoint scan
│   ├── driver_importance.py # Random Forest & HistGradientBoosting multi-driver attribution
│   ├── forecaster.py        # 36-Month Hybrid Ridge + Gradient Boosting forecaster (2026–2029)
│   ├── clustering_hazard.py # K-Means (k=3) + PCA regime clustering & Isolation Forest GLOF detector
│   ├── train_models.py      # Offline training pipeline generating 37 .joblib artifacts
│   └── trained_models/      # Serialized .joblib models + training_metrics.json
├── public/ & ui/            # Layer 5A: Cinematic Scrollytelling UI & SVG Visualization Engine
├── exports/                 # Layer 5B: CSV Exporter, 1-Page PDF Report & Detective Certificate PDF
├── tests/                   # Layer 6A: Automated Pytest statistical verification suite
├── docs/                    # Layer 6B: NASA Space Apps Submission Answers & 7-Slide / 30s Script
└── app.py                   # Main FastAPI Web Server & REST API
```

---

## 3. Core Mathematical & Glaciological Equations

1. **12-Month Climatology & Deseasonalized Anomaly Extraction:**
   $$\bar{x}_m = \frac{1}{N_m} \sum_{y} x_{y,m}, \qquad A_{y,m} = x_{y,m} - \bar{x}_m$$
2. **Non-Parametric Theil–Sen Robust Slope Estimator:**
   $$\beta_{\text{Sen}} = \text{median}\left( \frac{A_j - A_i}{t_j - t_i} \right) \quad \forall \, i < j, \qquad \text{Slope}_{\text{decade}} = 10 \cdot \beta_{\text{Sen}}$$
3. **Hamed–Rao (1998) Autocorrelation-Adjusted Mann–Kendall Variance:**
   $$\text{Var}^*(S) = \text{Var}(S) \cdot \left[ 1 + \frac{2}{n(n-1)(n-2)} \sum_{k=1}^{n-1} (n-k)(n-k-1)(n-k-2)\rho_k \right]$$
4. **Benjamini–Hochberg False Discovery Rate (FDR) Spatial Grid Stippling:**
   $$p_{(k)} \le \frac{k}{m} \alpha \quad (\alpha = 0.05)$$
5. **Upward $0^\circ\text{C}$ Freezing Isotherm Migration:**
   $$\Delta H_{0^\circ\text{C}} = \frac{\Delta T_{\text{decade}} \cdot D}{\Gamma_{\text{lapse}}} \times 1000\text{ m} \quad (\Gamma_{\text{lapse}} = 6.5^\circ\text{C/km})$$

---

## 4. Quick Start & Running Locally

### 1. Start the Server
```powershell
cd "d:\Himalaya Trend lab"
python -m uvicorn app:app --host 127.0.0.1 --port 8000 --reload
```
*(Or simply run `python app.py`.)*

### 2. Open in Browser
Navigate to **http://127.0.0.1:8000** in Chrome or Edge.

### 3. Run the Automated Statistical Test Suite
```powershell
python -m pytest tests/test_statistics.py -v
```

### 4. Re-Train All 37 Machine Learning `.joblib` Artifacts (Optional)
```powershell
python -m ml.train_models
```

---

## 5. Submission Pack Documents
- **Official Submission Form Answers:** [`docs/SUBMISSION_ANSWERS.md`](file:///d:/Himalaya%20Trend%20lab/docs/SUBMISSION_ANSWERS.md)
- **7-Slide Judge Deck & 30-Second Video Script:** [`docs/DEMO_SLIDES_AND_SCRIPT.md`](file:///d:/Himalaya%20Trend%20lab/docs/DEMO_SLIDES_AND_SCRIPT.md)
- **Pre-Trained ML Evaluation Metrics:** [`ml/trained_models/training_metrics.json`](file:///d:/Himalaya%20Trend%20lab/ml/trained_models/training_metrics.json)
