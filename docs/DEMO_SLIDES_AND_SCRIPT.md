# 2026 NASA Space Apps Challenge - 7-Slide Deck & 30-Second Video Script

- **Project:** Himalaya Trend Lab - Be a Data Detective for Pakistan's Glaciers
- **Challenge:** Be An Earth System Trend Detective
- **Prepared By:** Team GeoNova
- **Compliance Note:** Strictly follows the official NASA Space Apps rules (**Maximum 7 Slides** OR **Maximum 30-Second Video**, English-only, zero NASA logos/emblems).

---

## PART A: 7-Slide Judge Presentation Deck Content

### Slide 1 - Title & Mission: The Third Pole Detective
- **Headline:** HIMALAYA TREND LAB - Be a Data Detective for Pakistan's Glaciers
- **Subtitle:** 2026 NASA Space Apps Challenge | Challenge: *Be An Earth System Trend Detective* | Prepared by **Team GeoNova**
- **Key Visual:** Screenshot of the `#home` 3D/2D Karakoram mountain scrollytelling hero with the orbital satellite scan beam, telemetry HUD (`705 KM`), and rising 3D Pakistan terrain map.
- **Core Hook:**
  - Pakistan holds **7,253 glaciers** - more ice than anywhere outside the poles.
  - Feeds **240 million people** along the Indus River (`64.5 MAF` annual Tarbela inflow, `15,827 MW` hydropower), while threatening valleys with **Glacial Lake Outburst Floods (GLOFs)**.
  - **Our Goal:** Separate true multi-decade climate signals from noisy mountain weather.

---

### Slide 2 - The Problem: Why Standard Trend Lines Lie in High Mountains
- **Headline:** 3 Statistical Traps That Mislead Climate Investigations
- **Key Visual:** Screenshot of the `#method` **Signal-vs-Noise Statistical Honesty Sandbox** comparing a 10-year noisy slice vs. a 45-year record.
- **Bullet Points:**
  1. **Seasonal Dominance (15–30x):** The annual winter-to-summer cycle overwhelms decadal slopes unless 12-month climatology and STL decomposition are removed first.
  2. **Red-Noise Autocorrelation ($r_1 > 0.5$):** Month-to-month persistence in snow and temperature inflates false positives (`Type I error`) in standard OLS regression and naive Mann–Kendall tests.
  3. **Short-Window Illusions:** A 10-year slice of rainfall looks like a steep trend (`p > 0.30`), whereas a 30–45 year WMO record reveals true statistical significance.

---

### Slide 3 - Our Solution: The 6-Layer Detective Workbench
- **Headline:** Ask a Question → Tune the Evidence → Interrogate the Signal
- **Key Visual:** Screenshot of `#investigate` showing the 5 Guided Detective Question pills, 8-Metric Statistical & Cryosphere Grid, and Deseasonalized Anomaly SVG chart.
- **How It Works (6-Stage Pipeline):**
  - **Step 1:** Area-weighted spatial subsetting ($\cos(\text{lat})$) + **RGI v6.0 Glacier-Only Ice Mask** across **9 River Basins** and **10 NASA/Meteomatics Variables (1981–2026)**.
  - **Step 2:** 12-month climatology removal & STL decomposition.
  - **Step 3:** Non-parametric **Theil–Sen Robust Slope** + 95% confidence interval per decade.
  - **Step 4:** **Hamed–Rao (1998) Modified Mann–Kendall** with Variance Inflation Factor (VIF) correction.
  - **Step 5:** **Benjamini–Hochberg FDR** spatial grid stippling + vertical elevation bands (`2,500m` to `>6,000m`).
  - **Step 6:** Automated Plain-Language Verdict answering *What, Where, How Fast, and Is It Significant?*

---

### Slide 4 - Scientific Proof: The Karakoram Anomaly vs. Shisper GLOF
- **Headline:** Three One-Click Benchmark Investigations
- **Key Visual:** Screenshot of `#cases` showing the side-by-side comparison of **Karakoram** vs. **Hindu Kush** snow cover and the Multi-Sensor Validation Table.
- **Key Findings:**
  - **Case 01 (Karakoram vs. Hindu Kush):** Proves regional divergence - Hindu Kush snow cover drops significantly (`-2.67%/decade`, `p < 0.0001`), while central Karakoram snow remains buffered (`-0.12%/decade`, `p = 0.084` - *Karakoram Anomaly*) due to winter westerly snowfall (`NAO`) and $>5,500\text{ m}$ hypsometry.
  - **Case 02 (Hunza & May 2022 Shisper GLOF):** Hunza warming (`+0.29°C/decade`, `p = 0.0012`) pushed the $0^\circ\text{C}$ freezing isotherm upward by **`+200 m`**, exposing `412 km²` of ice and triggering the May 7, 2022 Hassanabad Bridge collapse.
  - **Case 03 (Upper Indus Rainfall):** Demonstrates scientific honesty when high monsoon noise masks a long-term trend (`Not Significant Yet`).

---

### Slide 5 - Explainable AI / Machine Learning Suite (`ml/`)
- **Headline:** 37 Pre-Trained Scikit-Learn Models (.joblib) Uncovering Non-Linear Dynamics
- **Key Visual:** Screenshot of `#ml` showing the GPR Changepoint curve, Random Forest Driver Importance bars, 36-Month Forecast (`2026–2029`), and K-Means Regime table.
- **4 Core ML Architectures (80/20 Chronological Split + 5-Fold TimeSeriesSplit CV):**
  1. **Gaussian Process Regression (`RBF + WhiteKernel`):** Detects non-linear structural changepoints (`2010–2016`) where melt rates accelerated.
  2. **Explainable Random Forest & Gradient Boosting:** Ranks physical drivers - 2m Air Temperature (`34%`), Winter Snowfall (`25%`), OMI Black-Carbon Aerosols (`19%`), NAO (`12%`), and ENSO (`10%`).
  3. **36-Month Hybrid Climate Forecaster (`2026–2029`):** Ridge harmonic + Gradient Boosted lag forecaster (`Test R² = 0.9941` on Hunza temperature).
  4. **Unsupervised K-Means ($k=3$) + PCA Clustering:** Groups all 9 basins & 15 glaciers into 3 objective cryosphere regimes (`Silhouette Score = 0.4668`, `68.4%` variance explained).

---

### Slide 6 - Real-World Impact: HimalayaShield & Indus Water Tower
- **Headline:** From Orbital Equations to Downstream Human Protection
- **Key Visual:** Screenshot of `#shield` showing the 7-Day Meteomatics GLOF Radar across 15 glaciers and the Tarbela Dam Peak Water Hydrograph (`2020–2080`).
- **Operational Impact:**
  - **7-Day Meteomatics GLOF Early Warning Radar:** Monitors all **15 iconic Pakistan glaciers** (`Shisper`, `Passu`, `Batura`, `Baltoro`, `Siachen`, etc.) for compound heat + rain-on-snow + ELA exceedance triggers, mapping downstream highways, bridges, and villages at risk.
  - **Indus Water Tower Simulator (`2020–2080`):** Translates `+1.5°C` to `+4.2°C` warming scenarios into the **Peak Water Tipping Point (`~2039` at `72.3 MAF`)** followed by late-century inflows (`53.6 MAF` by 2075), quantifying impacts on Rabi wheat, Kharif rice/cotton, and `15,827 MW` of hydropower.

---

### Slide 7 - NASA & Partner Data Ecosystem + Reproducible Exports
- **Headline:** Multi-Sensor Fusion, Gamified Education & 1-Click PDF Reports
- **Key Visual:** Screenshot of `#notebook` showing the 3 Interactive Detective Missions, 1-Page PDF Detective Report, and Official Detective Certificate PDF.
- **Data & Reproducibility:**
  - **NASA Missions:** Terra/Aqua `MODIS` (`MOD10CM`, `MOD11C3`), `MERRA-2` (`NASA POWER`), `GPM IMERG V07`, `GLDAS-2.1`, `AIRS`, `OMI`, and `SRTM DEM`.
  - **Partner & Inventory Data:** Live **Meteomatics Weather API** (Space Apps Global Offer Partner) + **RGI v6.0 Glacier Mask**.
  - **Deliverables:** 1-click **CSV Time-Series Export**, **1-Page Executive PDF Detective Report**, and **Official Earth System Trend Detective Certificate PDF**.

---
---

## PART B: 30-Second Video Pitch & Screen-Recording Script
*(Strict 30-second limit - ~75 spoken words at a crisp, energetic pace)*

| Timecode | What to Show on Screen (`http://127.0.0.1:8000`) | Spoken Voiceover (English) |
| :--- | :--- | :--- |
| **0:00 – 0:05** *(5s)* | Start on `#home` Hero. Scroll down smoothly so the camera dives toward K2, the satellite flies across, and the 3D Pakistan map rises. | *"Pakistan’s seven thousand glaciers feed two hundred forty million people - yet raw mountain climate data is full of seasonal noise."* |
| **0:05 – 0:12** *(7s)* | Click **Investigate (`#investigate`)**. Click a Detective Question pill, select **Karakoram vs. Hindu Kush** in Compare Mode, and highlight the Verdict + Sen's Slope chart. | *"Welcome to Himalaya Trend Lab. Using forty-five years of NASA satellite and Meteomatics data, we remove seasonal cycles and run Hamed–Rao Mann–Kendall and Sen’s slope tests."* |
| **0:12 – 0:19** *(7s)* | Click **Demo Cases (`#cases`)** and **Methodology (`#method`)**, dragging the Signal-vs-Noise slider from 10 years to 45 years. | *"We prove the Karakoram Anomaly alongside Hindu Kush snow loss, while our Signal-versus-Noise sandbox teaches why short records can mislead."* |
| **0:19 – 0:25** *(6s)* | Click **AI/ML Lab (`#ml`)** showing GPR changepoints, Random Forest driver bars, and the 2026–2029 forecast chart. | *"Thirty-seven pre-trained Machine Learning models uncover structural changepoints, black-carbon aerosol drivers, and thirty-six-month forecasts."* |
| **0:25 – 0:30** *(5s)* | Click **Shield (`#shield`)** showing the 15-Glacier GLOF Radar, Peak Water curve, and click **1-Page PDF Report**. | *"And HimalayaShield delivers seven-day GLOF early warnings and Indus Water Tower projections - turning orbital data into human protection."* |
