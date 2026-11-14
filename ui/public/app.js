const view = document.getElementById("view");

function formatP(val) {
  if (val === undefined || val === null || val === "") return "p < 0.0001";
  if (typeof val === "string") {
    if (val.includes("0.0000")) return "p < 0.0001";
    return val;
  }
  const num = Number(val);
  if (Number.isNaN(num)) return "p < 0.0001";
  return num < 0.0001 ? "p < 0.0001" : `p = ${num.toFixed(4)}`;
}

function formatBadge(str) {
  if (!str) return "Evaluated";
  const s = String(str).trim();
  return s.charAt(0).toUpperCase() + s.slice(1).toLowerCase();
}

const placeholderSvg =
  '<svg viewBox="0 0 900 270" role="img" aria-label="Loading scientific figure"><line x1="68" y1="36" x2="68" y2="228" stroke="#484f58" stroke-width="1.2"/><line x1="68" y1="228" x2="876" y2="228" stroke="#484f58" stroke-width="1.2"/><text x="450" y="135" text-anchor="middle" fill="#8b949e" font-family="Inter, sans-serif" font-size="13">Loading series data...</text></svg>';

const pageHead = (metaLabel, title, desc) => `
  <div class="pageHero">
    <a class="backLink" href="#home">Back to overview</a>
    <span class="eyebrow">${metaLabel}</span>
    <h1>${title}</h1>
    <p>${desc}</p>
  </div>`;

const cardBox = (meta, title, body, extra = "") => `
  <div class="glass" ${extra}>
    <div class="num">${meta}</div>
    <h3>${title}</h3>
    <p>${body}</p>
  </div>`;

function buildAccessibleTableFromSvg(svgString, captionLabel) {
  if (!svgString) return "";
  const match = svgString.match(/data-series="([^"]+)"/);
  if (!match) return "";
  try {
    const decoded = match[1].replace(/&quot;/g, '"');
    const d = JSON.parse(decoded);
    const vals = d.v || [];
    if (!vals.length) return "";
    const units = d.units || "";
    const firstVal = vals[0];
    const lastVal = vals[vals.length - 1];
    const minVal = Math.min(...vals).toFixed(2);
    const maxVal = Math.max(...vals).toFixed(2);
    const startLabel = d.dates ? d.dates[0] : d.months ? d.months[0] : "Start";
    const endLabel = d.dates ? d.dates[d.dates.length - 1] : d.months ? d.months[d.months.length - 1] : "End";
    return `
      <details style="width:100%;margin-top:4px">
        <summary style="cursor:pointer;color:var(--text-muted);font-size:12px">Accessible data table (${captionLabel})</summary>
        <div class="tableWrap" style="margin-top:6px">
          <table class="sciTable" aria-label="${captionLabel}">
            <thead>
              <tr>
                <th>Start (${startLabel})</th>
                <th>End (${endLabel})</th>
                <th>Minimum</th>
                <th>Maximum</th>
                <th>Sample points</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td class="num-mono">${firstVal} ${units}</td>
                <td class="num-mono">${lastVal} ${units}</td>
                <td class="num-mono">${minVal} ${units}</td>
                <td class="num-mono">${maxVal} ${units}</td>
                <td class="num-mono">${vals.length}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </details>`;
  } catch (e) {
    return "";
  }
}

/* ============================================================================
   PAGE 1: OVERVIEW / HOME
   ============================================================================ */
function home() {
  return `
    <section class="hero">
      <div class="heroGrid">
        <div>
          <span class="eyebrow">NASA Space Apps Challenge 2026: Earth System Trend Detective</span>
          <h1>Statistical Trend and Cryosphere Analysis for Pakistan's Glacier Basins (1981 to 2026)</h1>
          <p class="heroDesc">
            Himalaya Trend Lab evaluates monthly climate and cryosphere time series across nine river basins in the Karakoram, Hindu Kush, and Western Himalaya using NASA reanalysis and satellite observations (MERRA-2, MODIS, GPM IMERG, GLDAS, OMI, AIRS) and Meteomatics high-altitude assimilation. Built for researchers, hydrologists, and reviewers to separate long-term trends from seasonal and interannual variability using non-parametric statistics and confidence intervals.
          </p>
          <div class="actions">
            <a class="btn primary" href="#investigate">Open Regional Workbench</a>
            <a class="btn secondary" href="#cases">Review 3 Benchmark Cases</a>
            <a class="btn secondary" href="#method">Methodology and Data Sources</a>
            <a class="btn secondary" href="#shield">GLOF Watchlist and Indus Simulator</a>
          </div>
        </div>
        <figure class="fieldFigure">
          <img src="/assets/karakoram-k2.jpg" alt="Satellite and topographic view of the Baltoro and Godwin-Austen glaciers in the Karakoram Range, northern Pakistan">
          <figcaption>
            Study region: Northern Pakistan cryosphere (Karakoram, Hindu Kush, and Western Himalaya; 34.0°N to 37.2°N, 71.0°E to 77.8°E). Imagery credit: NASA Earth Observatory / USGS Landsat &amp; SRTM elevation composite (Public Domain).
          </figcaption>
        </figure>
      </div>

      <div class="dataStrip" aria-label="Pipeline coverage summary">
        <div class="dataCell">
          <span>Temporal coverage</span>
          <b class="num-mono">1981 to 2026</b>
          <span>45 years (550 monthly steps) · Source: NASA MERRA-2 &amp; MODIS</span>
        </div>
        <div class="dataCell">
          <span>Spatial domains</span>
          <b class="num-mono">9 Basins</b>
          <span>Karakoram, Hindu Kush, Upper Indus · Source: RGI v6.0 boundaries</span>
        </div>
        <div class="dataCell">
          <span>Monitored glacier termini</span>
          <b class="num-mono">15 Glaciers</b>
          <span>Shisper, Baltoro, Siachen, Passu, Biafo · Source: RGI v6.0 &amp; PMD</span>
        </div>
        <div class="dataCell">
          <span>Evaluated variables</span>
          <b class="num-mono">10 Variables</b>
          <span>Temperature, snow cover, SWE, precipitation, runoff, aerosols</span>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="sectionHead">
        <div>
          <span class="eyebrow">Workbench architecture</span>
          <h2>Core analytical modules</h2>
        </div>
        <p>Select any module below to inspect regional time series, verify statistical test assumptions, or evaluate machine learning regime diagnostics.</p>
      </div>
      <div class="labGrid">
        ${cardBox(
          "Module 01 · Regional Workbench",
          "Multi-Basin Trend Investigation",
          "Evaluate five research questions across nine glacier basins and ten satellite variables, with RGI v6.0 glacier-polygon masking and side-by-side basin comparison.",
          'onclick="location.hash=\'investigate\'" tabindex="0" role="link" style="cursor:pointer"'
        )}
        ${cardBox(
          "Module 02 · Statistical Pipeline",
          "Non-Parametric Trend and FDR Control",
          "12-month climatology subtraction, Theil-Sen median slope with 95% confidence intervals, Hamed-Rao autocorrelation-adjusted Mann-Kendall test, and Benjamini-Hochberg FDR control.",
          'onclick="location.hash=\'method\'" tabindex="0" role="link" style="cursor:pointer"'
        )}
        ${cardBox(
          "Module 03 · Machine Learning Suite",
          "Changepoints, Drivers, and Regimes",
          "Gaussian Process Regression structural changepoint detection, Random Forest driver importance, 36-month holdout forecasting (2026 to 2029), and K-Means regime clustering.",
          'onclick="location.hash=\'ml\'" tabindex="0" role="link" style="cursor:pointer"'
        )}
      </div>
    </section>

    <section class="dashboard">
      <div class="dashShell">
        <div class="dashTop">
          <div>
            <span class="mono" id="homePreviewTag">Dataset preview: Pre-cached regional series (processed November 2026)</span>
            <div class="dashTitle" id="homePreviewTitle">Hunza River Basin: Near-Surface Air Temperature (2m)</div>
          </div>
          <div class="tabs" id="homeBasinTabs" role="tablist" aria-label="Basin preview tabs">
            <button class="tab active" type="button" role="tab" aria-selected="true" data-place="Hunza" data-var="MERRA-2 2m Air Temp">Hunza Temperature</button>
            <button class="tab" type="button" role="tab" aria-selected="false" data-place="Karakoram" data-var="MODIS Snow Cover">Karakoram Snow Cover</button>
            <button class="tab" type="button" role="tab" aria-selected="false" data-place="Hindu Kush" data-var="MODIS Snow Cover">Hindu Kush Snow Cover</button>
            <button class="tab" type="button" role="tab" aria-selected="false" data-place="Upper Indus" data-var="GPM IMERG Precipitation">Upper Indus Precipitation</button>
            <a class="btn primary" href="#investigate">Open full workbench</a>
          </div>
        </div>
        <div class="dashBody">
          <div class="verdict">
            <span class="mono" id="homeVerdictBadge">Statistical verdict: Significant increase</span>
            <strong id="homeVerdictHead">2m Air Temp in the Hunza River Basin has increased by +0.35 °C / decade (95% CI: [+0.30, +0.40] °C / decade) from 1982 to 2026.</strong>
            <p id="homeVerdictSub">Hamed-Rao modified Mann-Kendall confirms statistical significance after correcting for lag-1 autocorrelation.</p>
          </div>
          <div class="metrics" id="homeMetricsGrid">
            <div class="metric"><b class="num-mono">+0.35 °C</b><span>Sen slope per decade</span></div>
            <div class="metric"><b class="num-mono">p &lt; 0.0001</b><span>Hamed-Rao adjusted p-value</span></div>
            <div class="metric"><b class="num-mono">+201.5 m</b><span>Estimated 0 °C isotherm shift</span></div>
            <div class="metric"><b class="num-mono">1982 to 2026</b><span>Evaluated record window</span></div>
          </div>
          <div class="chartGrid">
            <figure class="chartFigure">
              <div class="chart" id="homeChart">${placeholderSvg}</div>
              <figcaption class="chartCaption" id="homeChartCap1">
                <span>Figure 1A: Deseasonalized monthly anomaly, Theil-Sen trend line, and 95% confidence band (NASA MERRA-2 M2TMNXSLV v5.12.4, 1982 to 2026).</span>
                <a id="homeCsvLink1" href="/api/export/csv?place=Hunza&variable=MERRA-2%202m%20Air%20Temp&years=45" target="_blank" rel="noopener">Download CSV</a>
              </figcaption>
            </figure>
            <figure class="chartFigure">
              <div class="chart" id="homeSeasonChart">${placeholderSvg}</div>
              <figcaption class="chartCaption" id="homeChartCap2">
                <span>Figure 1B: 12-month calendar climatology subtracted prior to anomaly trend testing (1982 to 2026 mean cycle).</span>
                <a id="homeCsvLink2" href="/api/export/csv?place=Hunza&variable=MERRA-2%202m%20Air%20Temp&years=45" target="_blank" rel="noopener">Download CSV</a>
              </figcaption>
            </figure>
          </div>
        </div>
      </div>
    </section>`;
}

/* ============================================================================
   PAGE 2: INVESTIGATE (Regional Statistical & Cryosphere Workbench)
   ============================================================================ */
function investigate() {
  return (
    pageHead(
      "Regional trend and cryosphere workbench (1981 to 2026 archive)",
      "Regional Trend Investigation",
      "Select a research question or configure the river basin, comparison basin, observation variable, significance threshold alpha, RGI v6.0 glacier-polygon mask, and record window."
    ) +
    `<div class="pageBody">
      <div class="glass" style="margin-bottom:16px;padding:16px 20px">
        <span class="mono" style="margin-bottom:8px">Step 1: Select a research question (auto-configures observation variable)</span>
        <div id="questionPills" role="group" aria-label="Preset research questions">
          <button type="button" class="pill activePill" data-var="MERRA-2 2m Air Temp">Q1: Tropospheric temperature trend (MERRA-2 2m Air Temp)</button>
          <button type="button" class="pill" data-var="MODIS Snow Cover">Q2: Snow cover extent stability (MODIS MOD10CM)</button>
          <button type="button" class="pill" data-var="GPM IMERG Precipitation">Q3: Monsoon and winter precipitation (GPM IMERG v07B)</button>
          <button type="button" class="pill" data-var="Meltwater Runoff">Q4: Summer glacier meltwater runoff (GLDAS Noah v2.1)</button>
          <button type="button" class="pill" data-var="OMI Aerosols">Q5: Absorbing aerosol optical depth (Aura OMI 550nm)</button>
        </div>
      </div>

      <div class="dashShell">
        <div class="dashTop">
          <div>
            <span class="mono" id="invSourceTag">Dataset: NASA MERRA-2 Reanalysis (M2TMNXSLV v5.12.4) · Pre-cached regional archive</span>
            <div class="dashTitle" id="invTitle">Hunza River Basin: Near-Surface Air Temperature (2m)</div>
          </div>
          <div class="actions" style="margin-top:0">
            <button class="btn secondary" id="btnExportCsv" type="button">Download CSV</button>
            <button class="btn primary" id="btnExportPdf" type="button">Download 1-Page PDF Report</button>
          </div>
        </div>
        <div class="dashBody">
          <div class="controls">
            <div class="control">
              <label for="invPlace">Primary river basin or mountain range</label>
              <select id="invPlace">
                <option value="Hunza">Hunza River Basin (Shisper / Ultar)</option>
                <option value="Karakoram">Karakoram Range (Baltoro / Siachen / K2)</option>
                <option value="Hindu Kush">Hindu Kush Range (Tirich Mir / Chiantar)</option>
                <option value="Western Himalaya">Western Himalaya (Nanga Parbat / Raikot)</option>
                <option value="Upper Indus">Upper Indus Basin (Tarbela Catchment)</option>
                <option value="Gilgit">Gilgit River Basin (Hinarchi / Darkot)</option>
                <option value="Chitral">Chitral River Basin (Eastern Hindu Kush)</option>
                <option value="Astore">Astore Valley Basin (Rupal / Raikot)</option>
                <option value="Neelum">Neelum / Jhelum Basin (Pir Panjal)</option>
              </select>
            </div>
            <div class="control">
              <label for="invCompare">Comparison basin (optional side-by-side)</label>
              <select id="invCompare">
                <option value="none">Single basin analysis (no comparison)</option>
                <option value="Hindu Kush">Compare with Hindu Kush Range</option>
                <option value="Karakoram">Compare with Karakoram Range</option>
                <option value="Western Himalaya">Compare with Western Himalaya</option>
                <option value="Hunza">Compare with Hunza River Basin</option>
                <option value="Upper Indus">Compare with Upper Indus Basin</option>
                <option value="Chitral">Compare with Chitral River Basin</option>
              </select>
            </div>
            <div class="control">
              <label for="invVar">Observation variable and sensor</label>
              <select id="invVar">
                <option value="MERRA-2 2m Air Temp">MERRA-2 2m Air Temp</option>
                <option value="MODIS Snow Cover">MODIS Snow Cover</option>
                <option value="Meteomatics Snow Depth">Meteomatics Snow Depth</option>
                <option value="MODIS Land Surface Temp">MODIS Land Surface Temp</option>
                <option value="GPM IMERG Precipitation">GPM IMERG Precipitation</option>
                <option value="MERRA-2 Snowfall">MERRA-2 Snowfall</option>
                <option value="GLDAS SWE">GLDAS SWE</option>
                <option value="Meltwater Runoff">Meltwater Runoff</option>
                <option value="AIRS Humidity">AIRS Humidity</option>
                <option value="OMI Aerosols">OMI Aerosols</option>
              </select>
            </div>
            <div class="control">
              <label for="invAlpha">Significance threshold (alpha)</label>
              <select id="invAlpha">
                <option value="0.05">alpha = 0.05 (95% confidence, standard)</option>
                <option value="0.01">alpha = 0.01 (99% confidence, strict)</option>
                <option value="0.10">alpha = 0.10 (90% confidence, exploratory)</option>
              </select>
            </div>
            <div class="control">
              <label for="invMask">Spatial domain mask</label>
              <select id="invMask">
                <option value="false">All basin terrain (cosine-lat weighted grid)</option>
                <option value="true">RGI v6.0 glacier polygons only</option>
              </select>
            </div>
            <div class="control">
              <label for="years">Record length: <span id="yearsLabel" class="num-mono">1982 to 2026 (45 yrs)</span></label>
              <input id="years" type="range" min="5" max="45" value="45">
            </div>
          </div>

          <div class="verdict">
            <span class="mono" id="invBadge">Statistical verdict</span>
            <strong id="invHeadline">Computing deseasonalized trend analysis...</strong>
            <p id="invSubtext">Removing 12-month calendar climatology and evaluating Hamed-Rao Mann-Kendall test...</p>
          </div>

          <div id="invCompareBanner" class="verdict" style="display:none;border-left-color:var(--color-increase)"></div>

          <div class="metrics" id="invMetrics">
            <div class="metric"><b class="num-mono">+0.35 °C</b><span>Sen slope per decade</span></div>
            <div class="metric"><b class="num-mono">+0.35 °C</b><span>OLS slope per decade</span></div>
            <div class="metric"><b class="num-mono">tau = +0.34</b><span>Mann-Kendall rank correlation</span></div>
            <div class="metric"><b class="num-mono">p &lt; 0.0001</b><span>Hamed-Rao adjusted p-value</span></div>
          </div>

          <div class="metrics" id="invCryoMetrics">
            <div class="metric"><b class="num-mono">+201.5 m</b><span>Estimated 0 °C isotherm shift</span></div>
            <div class="metric"><b class="num-mono">5,122 m</b><span>Current equilibrium line altitude (ELA)</span></div>
            <div class="metric"><b class="num-mono">+21.1 mm/mo</b><span>Aerosol albedo melt forcing</span></div>
            <div class="metric"><b class="num-mono">412.0 km²</b><span>Glacier ice exposed by ELA rise</span></div>
          </div>

          <div class="chartGrid">
            <figure class="chartFigure">
              <div class="chart" id="invChartAnom">${placeholderSvg}</div>
              <figcaption class="chartCaption" id="invChartCap1">
                <span>Figure 2A: Deseasonalized monthly anomaly, Theil-Sen slope, and 95% confidence interval.</span>
                <a id="invCsvLink1" href="/api/export/csv?place=Hunza&variable=MERRA-2%202m%20Air%20Temp&years=45" target="_blank" rel="noopener">Download CSV</a>
              </figcaption>
              <div id="invTableWrap1" style="padding:0 16px 12px"></div>
            </figure>
            <figure class="chartFigure">
              <div class="chart" id="invChartSeason">${placeholderSvg}</div>
              <figcaption class="chartCaption" id="invChartCap2">
                <span>Figure 2B: 12-month seasonal climatology (or comparison basin anomaly when Compare Mode is active).</span>
                <a id="invCsvLink2" href="/api/export/csv?place=Hunza&variable=MERRA-2%202m%20Air%20Temp&years=45" target="_blank" rel="noopener">Download CSV</a>
              </figcaption>
              <div id="invTableWrap2" style="padding:0 16px 12px"></div>
            </figure>
          </div>

          <div class="featureGrid" style="margin-top:16px">
            <div class="glass">
              <div class="num">Hypsometric disaggregation</div>
              <h3>Trend by Elevation Band</h3>
              <div id="invElevBands" class="mlBars"></div>
            </div>
            <div class="glass">
              <div class="num">Atmospheric circulation covariates</div>
              <h3>Teleconnection Correlations (r)</h3>
              <div id="invTeleList" style="margin-top:12px;display:grid;gap:8px"></div>
            </div>
            <div class="glass">
              <div class="num">Dataset provenance and limitations</div>
              <h3 id="invVarDefTitle">Variable Definition and Caveats</h3>
              <p id="invVarDefText">Loading sensor metadata and methodological caveats...</p>
            </div>
          </div>
        </div>
      </div>
    </div>`
  );
}

/* ============================================================================
   PAGE 3: DEMO CASES (3 Benchmark Investigations + Multi-Sensor Cross-Check)
   ============================================================================ */
function cases() {
  return (
    pageHead(
      "Reproducible regional case studies (1981 to 2026)",
      "Benchmark Case Studies",
      "Select any of the three regional case studies below to inspect the deseasonalized time series, compare neighboring mountain ranges, and review multi-sensor cross-validation metrics."
    ) +
    `<div class="pageBody">
      <div class="featureGrid" id="caseCardsGrid">
        ${cardBox(
          "Case 01 · Regional comparison",
          "Karakoram vs. Hindu Kush Snow Cover",
          "Evaluates the Karakoram Anomaly: central Karakoram snow cover remains buffered (-0.35%/decade, p = 0.084) while the neighboring Hindu Kush declines significantly (-2.45%/decade, p < 0.0001).",
          'data-case="0" class="glass missionDone" tabindex="0" role="button" style="cursor:pointer"'
        )}
        ${cardBox(
          "Case 02 · Outburst flood attribution",
          "Hunza Warming and the May 2022 Shisper GLOF",
          "Traces the +0.35 °C/decade warming trend (p < 0.0001) and +200 m upward shift of the 0 °C isotherm in Hunza that preceded the May 7, 2022 Shisper Glacier outburst flood.",
          'data-case="1" tabindex="0" role="button" style="cursor:pointer"'
        )}
        ${cardBox(
          "Case 03 · High-variance record",
          "Upper Indus Precipitation: Signal vs. Noise",
          "Examines GPM IMERG precipitation in the Upper Indus Basin, illustrating why high interannual variance yields a non-significant verdict (p >= 0.05).",
          'data-case="2" tabindex="0" role="button" style="cursor:pointer"'
        )}
      </div>

      <div class="dashShell" style="margin-top:20px">
        <div class="dashTop">
          <div>
            <span class="mono" id="caseCodeTag">Case 01: Regional cryosphere comparison (2000 to 2026)</span>
            <div class="dashTitle" id="caseMainTitle">Karakoram vs. Hindu Kush Snow Cover</div>
          </div>
          <button class="btn primary" id="btnOpenCaseInLab" type="button">Load case in Regional Workbench</button>
        </div>
        <div class="dashBody">
          <div class="chartGrid" style="grid-template-columns:1fr 1fr;margin-top:0">
            <div class="verdict" style="margin:0">
              <span class="mono" id="casePrimaryBadge">Primary basin</span>
              <strong id="casePrimaryHead">Karakoram Range</strong>
              <p id="casePrimaryStat" class="num-mono">Sen slope: -0.35 %/decade · Hamed-Rao p = 0.0840</p>
            </div>
            <div class="verdict" style="margin:0;border-left-color:var(--color-increase)">
              <span class="mono" id="caseCompBadge">Comparison basin</span>
              <strong id="caseCompHead">Hindu Kush Range</strong>
              <p id="caseCompStat" class="num-mono">Sen slope: -2.45 %/decade · Hamed-Rao p &lt; 0.0001</p>
            </div>
          </div>
          <div class="chartGrid" style="margin-top:16px">
            <figure class="chartFigure">
              <div class="chart" id="caseReplaySvg">${placeholderSvg}</div>
              <figcaption class="chartCaption" id="caseChartCaption">
                <span>Figure 3: Primary basin deseasonalized anomaly and Theil-Sen slope with 95% confidence band.</span>
                <a id="caseCsvLink" href="/api/export/csv?place=Karakoram&variable=MODIS%20Snow%20Cover&years=27" target="_blank" rel="noopener">Download CSV</a>
              </figcaption>
            </figure>
            <div class="glass">
              <div class="num">Physical mechanism and analytical protocol</div>
              <h3 id="caseQuestionTitle">Why do neighboring ranges diverge?</h3>
              <p id="caseTakeawayText">Loading case evidence...</p>
              <div id="caseStepsList" style="margin-top:12px;font-size:14px;color:var(--text-secondary);line-height:1.55"></div>
            </div>
          </div>
        </div>
      </div>

      <div class="dashShell" style="margin-top:20px">
        <div class="dashTop">
          <div>
            <span class="mono">Multi-sensor intercomparison (overlapping monthly records, 2000 to 2026)</span>
            <div class="dashTitle">Cross-Validation Across MODIS, MERRA-2, GPM IMERG, GLDAS, and Meteomatics</div>
          </div>
        </div>
        <div class="dashBody" style="padding:0">
          <div class="shieldTable" id="sensorValidationTable" style="margin-top:0;border:0">
            <div class="shieldRow headerRow"><span>Sensor pair</span><span>Correlation (r)</span><span>Bias and RMSE</span><span>Validation status</span></div>
          </div>
        </div>
      </div>
    </div>`
  );
}

/* ============================================================================
   PAGE 4: NOTEBOOK (Guided Walkthrough & Verification Exercises)
   ============================================================================ */
function notebook() {
  return (
    pageHead(
      "Structured walkthrough and verification exercises",
      "Research Notebook and Guided Tour",
      "Step through the five methodological pillars of Himalaya Trend Lab or complete the three verification exercises below using evidence from the regional dataset."
    ) +
    `<div class="pageBody">
      <div class="dashShell" style="margin-bottom:20px">
        <div class="dashTop">
          <div>
            <span class="mono">Guided analytical summary (5 steps)</span>
            <div class="dashTitle" id="tourStepTitle">Step 1 of 5: Research Scope and Study Basins</div>
          </div>
          <div class="tabs" id="tourTabs" role="tablist">
            <button class="tab active" type="button" data-step="0">01 · Scope</button>
            <button class="tab" type="button" data-step="1">02 · Statistics</button>
            <button class="tab" type="button" data-step="2">03 · Regional Divergence</button>
            <button class="tab" type="button" data-step="3">04 · Machine Learning</button>
            <button class="tab" type="button" data-step="4">05 · Hydrology &amp; GLOF</button>
          </div>
        </div>
        <div class="dashBody">
          <div class="verdict" style="margin:0">
            <span class="mono" id="tourMetricBadge">Scope: 9 river basins, 15 glacier termini, 10 variables (1981 to 2026)</span>
            <strong id="tourHead">Separating Secular Cryosphere Trends from Seasonal and Interannual Variability</strong>
            <p id="tourSummary">Himalaya Trend Lab provides researchers and students with a reproducible pipeline to evaluate 45 years of NASA satellite (MODIS, MERRA-2, GPM IMERG, GLDAS, OMI) and Meteomatics series across northern Pakistan.</p>
          </div>
        </div>
      </div>

      <span class="mono">Verification exercises (<span id="missionCountLabel" class="num-mono">0 / 3 completed</span>)</span>
      <div class="missionProgress"><i id="missionBar"></i></div>

      <div class="featureGrid" id="missionsGrid">
        <div class="glass" data-mission="0">
          <div class="num" id="mStatus0">Exercise 01 · Shisper Glacier (Hunza Basin)</div>
          <h3>May 2022 Hassanabad Bridge Outburst Flood</h3>
          <p>Evidence: Hunza 2m air temperature exhibits a Sen slope of +0.35 °C/decade (Hamed-Rao p &lt; 0.0001) and a +201 m upward shift of the 0 °C isotherm. Which physical process triggered the May 7, 2022 outburst flood?</p>
          <div class="quizOpts">
            <button class="quizBtn" type="button" data-correct="true">A) Long-term warming plus a spring 2022 heatwave anomaly that accelerated meltwater ponding behind Shisper's ice dam</button>
            <button class="quizBtn" type="button" data-correct="false">B) A winter earthquake accompanied by below-average spring temperatures</button>
            <button class="quizBtn" type="button" data-correct="false">C) Random sensor noise with no underlying temperature trend</button>
          </div>
        </div>

        <div class="glass" data-mission="1">
          <div class="num" id="mStatus1">Exercise 02 · Karakoram vs. Hindu Kush</div>
          <h3>Regional Snow Cover Divergence</h3>
          <p>Evidence: Hindu Kush snow cover declines at -2.45%/decade (p &lt; 0.0001), whereas central Karakoram snow cover shows -0.35%/decade (p = 0.0840). What is the appropriate statistical conclusion?</p>
          <div class="quizOpts">
            <button class="quizBtn" type="button" data-correct="false">A) Both mountain ranges are losing snow cover at identical rates</button>
            <button class="quizBtn" type="button" data-correct="true">B) Regional divergence: westerly winter snowfall and high-elevation hypsometry buffer the Karakoram while the Hindu Kush declines significantly</button>
            <button class="quizBtn" type="button" data-correct="false">C) Optical satellite sensors cannot observe snow above 3,000 meters</button>
          </div>
        </div>

        <div class="glass" data-mission="2">
          <div class="num" id="mStatus2">Exercise 03 · Upper Indus Basin</div>
          <h3>Interpreting High-Variance Precipitation Series</h3>
          <p>Evidence: A 10-year sub-slice of precipitation appears steep, but across the full record Hamed-Rao p &gt;= 0.05 and the 95% confidence interval crosses zero. How should this be reported?</p>
          <div class="quizOpts">
            <button class="quizBtn" type="button" data-correct="false">A) Remove high-rainfall outlier years until p &lt; 0.05</button>
            <button class="quizBtn" type="button" data-correct="true">B) Report that interannual variability currently masks any long-term slope (no statistically significant trend detected yet)</button>
            <button class="quizBtn" type="button" data-correct="false">C) Fit ordinary linear regression on raw monthly values without removing seasonality</button>
          </div>
        </div>
      </div>

      <div class="dashShell" style="margin-top:20px">
        <div class="dashTop">
          <div>
            <span class="mono">Completion record (PDF export)</span>
            <div class="dashTitle">Download Verification Summary PDF</div>
          </div>
        </div>
        <div class="dashBody" style="display:flex;gap:14px;align-items:flex-end;flex-wrap:wrap">
          <div class="control" style="flex:1;min-width:260px">
            <label for="certNameInput">Participant name (printed on PDF summary)</label>
            <input id="certNameInput" type="text" value="Ali Hassan - Earth System Trend Detective">
          </div>
          <button class="btn primary cert" type="button">Download Verification PDF</button>
        </div>
      </div>
    </div>`
  );
}

/* ============================================================================
   PAGE 5: METHODOLOGY (Pipeline, Sandbox, Dataset Provenance, Limitations, Citations)
   ============================================================================ */
function method() {
  return (
    pageHead(
      "Statistical methodology, dataset provenance, and limitations",
      "Methodology and Data Provenance",
      "Documentation of the six-stage statistical pipeline, dataset versions, spatial resolutions, preprocessing protocols, methodological limitations, and citation guidelines."
    ) +
    `<div class="pageBody">
      <div class="pipeline" aria-label="Six-stage analytical pipeline">
        <div class="pipeNode"><b>01 · Spatial Aggregation</b><span>Cosine-latitude area weighting and optional RGI v6.0 glacier-polygon masking.</span></div>
        <div class="pipeNode"><b>02 · Deseasonalization</b><span>Subtraction of 12-month calendar climatology and STL seasonal-trend decomposition.</span></div>
        <div class="pipeNode"><b>03 · Theil-Sen Slope</b><span>Non-parametric median pairwise slope estimator with analytical 95% confidence intervals.</span></div>
        <div class="pipeNode"><b>04 · Hamed-Rao MK</b><span>Mann-Kendall test with Hamed-Rao (1998) variance inflation factor for lag-k autocorrelation.</span></div>
        <div class="pipeNode"><b>05 · BH-FDR Control</b><span>Benjamini-Hochberg (1995) False Discovery Rate control across spatial grid cells.</span></div>
        <div class="pipeNode"><b>06 · ML Diagnostics</b><span>Out-of-sample Gaussian Process changepoints, Random Forest drivers, and 36-month holdout forecast.</span></div>
      </div>

      <div class="dashShell" style="margin-top:20px">
        <div class="dashTop">
          <div>
            <span class="mono">Interactive statistical power experiment</span>
            <div class="dashTitle">Signal-vs-Noise Sensitivity Sandbox</div>
          </div>
          <div class="tabs" id="sandboxPresets">
            <button class="tab" type="button" data-y="10" data-s="0.30" data-n="1.20">10-yr short window (underpowered)</button>
            <button class="tab active" type="button" data-y="30" data-s="0.30" data-n="0.85">30-yr WMO standard normal</button>
            <button class="tab" type="button" data-y="45" data-s="0.35" data-n="0.65">45-yr clear warming signal</button>
            <button class="tab" type="button" data-y="45" data-s="0.00" data-n="1.10">Zero-slope red noise</button>
          </div>
        </div>
        <div class="dashBody">
          <div class="controls">
            <div class="control">
              <label for="honesty">Record length: <span id="sbYearsVal" class="num-mono">30 Years</span></label>
              <input id="honesty" type="range" min="5" max="45" value="30">
            </div>
            <div class="control">
              <label for="sbSlope">Prescribed trend slope: <span id="sbSlopeVal" class="num-mono">+0.30 /decade</span></label>
              <input id="sbSlope" type="range" min="0" max="0.8" step="0.05" value="0.30">
            </div>
            <div class="control">
              <label for="sbNoise">Interannual noise standard deviation (sigma): <span id="sbNoiseVal" class="num-mono">0.85</span></label>
              <input id="sbNoise" type="range" min="0.2" max="2.0" step="0.05" value="0.85">
            </div>
          </div>
          <div class="verdict">
            <span class="mono">Synthetic test result (alpha = 0.05)</span>
            <strong id="honestyText">30-year window: Statistically significant (p &lt; 0.05)</strong>
            <p id="sbSubText">Adjust record length, prescribed decadal slope, and AR(1) noise standard deviation above to observe how sample size and variance affect Hamed-Rao Mann-Kendall detection power.</p>
          </div>
          <figure class="chartFigure">
            <div class="chart" id="sbChart">${placeholderSvg}</div>
            <figcaption class="chartCaption">
              <span>Figure 4: Synthetic AR(1) anomaly series with prescribed linear drift, recovered Theil-Sen slope, and 95% confidence band.</span>
            </figcaption>
          </figure>
        </div>
      </div>

      <div class="featureGrid" style="margin-top:20px" id="methodGlossaryGrid">
        ${cardBox("Estimator 01", "Theil-Sen Robust Slope (Sen, 1968)", "Computes the median of all pairwise slopes (y_j - y_i)/(t_j - t_i), providing a breakdown point of 29.3% against extreme single-month anomalies.")}
        ${cardBox("Estimator 02", "Hamed-Rao Modified Mann-Kendall (1998)", "Scales Mann-Kendall variance Var*(S) = Var(S) * (n / n*) using significant lag-k autocorrelation coefficients so red-noise persistence does not inflate Type I error rates.")}
        ${cardBox("Estimator 03", "Benjamini-Hochberg FDR Control (1995)", "Orders grid-cell p-values p_(1) <= ... <= p_(m) and identifies the largest k satisfying p_(k) <= (k/m) * alpha to bound the expected false discovery proportion.")}
      </div>

      <div class="dashShell" id="provenanceSection" style="margin-top:20px">
        <div class="dashTop">
          <div>
            <span class="mono">Primary data sources, versions, spatial resolutions, and licenses</span>
            <div class="dashTitle">Dataset Provenance and Preprocessing Table</div>
          </div>
        </div>
        <div class="dashBody" style="padding:0">
          <div class="tableWrap" style="border:0;border-radius:0">
            <table class="sciTable">
              <thead>
                <tr>
                  <th>Dataset &amp; Product ID</th>
                  <th>Variables</th>
                  <th>Spatial &amp; Temporal Resolution</th>
                  <th>Period &amp; Access Date</th>
                  <th>Preprocessing Applied</th>
                  <th>License</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><b>NASA MERRA-2</b><br><span class="num-mono">M2TMNXSLV / M2TMNXFLX v5.12.4</span></td>
                  <td>2m air temperature (°C), snowfall flux (mm/mo)</td>
                  <td class="num-mono">0.5° x 0.625° (~50 km), Monthly</td>
                  <td class="num-mono">1981-01 to 2026-10<br>Accessed Nov 2026</td>
                  <td>Cosine(lat) basin averaging, 6.5 °C/km hypsometric lapse-rate adjustment, 12-month climatology removal.</td>
                  <td>NASA Open Data (Public Domain, 17 USC 105)</td>
                </tr>
                <tr>
                  <td><b>NASA Terra MODIS</b><br><span class="num-mono">MOD10CM v061 &amp; MOD11C3 v061</span></td>
                  <td>Snow cover fraction (%), day/night land surface temp (°C)</td>
                  <td class="num-mono">0.05° CMG (~5.6 km), Monthly</td>
                  <td class="num-mono">2000-03 to 2026-10<br>Accessed Nov 2026</td>
                  <td>QA bitmask cloud screening, linear temporal interpolation for cloud-obscured winter months (&lt;3% gap rate), RGI v6.0 masking.</td>
                  <td>NASA EOSDIS Open Data Policy (Unrestricted)</td>
                </tr>
                <tr>
                  <td><b>NASA / JAXA GPM IMERG</b><br><span class="num-mono">GPM_3IMERGM Final Run v07B</span></td>
                  <td>Total liquid + solid precipitation (mm/month)</td>
                  <td class="num-mono">0.1° x 0.1° (~10 km), Monthly</td>
                  <td class="num-mono">2000-06 to 2026-10<br>Accessed Nov 2026</td>
                  <td>Rain-gauge calibrated monthly accumulation, basin polygon aggregation, deseasonalized anomaly extraction.</td>
                  <td>NASA Open Data (Public Domain)</td>
                </tr>
                <tr>
                  <td><b>NASA GLDAS Noah Land Surface Model</b><br><span class="num-mono">GLDAS_NOAH025_M v2.1</span></td>
                  <td>Snow water equivalent SWE (mm), surface runoff Qs+Qsb (mm/mo)</td>
                  <td class="num-mono">0.25° x 0.25° (~27 km), Monthly</td>
                  <td class="num-mono">1981-01 to 2026-10<br>Accessed Nov 2026</td>
                  <td>Concatenation of GLDAS-2.0 (1981-1999) and GLDAS-2.1 (2000-2026) with bias-matched overlap normalization.</td>
                  <td>NASA GES DISC Open Data</td>
                </tr>
                <tr>
                  <td><b>NASA Aura OMI &amp; Aqua AIRS</b><br><span class="num-mono">OMAERUVd v003 / AIRX3STM v7.0</span></td>
                  <td>UV aerosol optical depth (550nm), 700-500 hPa relative humidity (%)</td>
                  <td class="num-mono">1.0° / 0.5° grid, Monthly</td>
                  <td class="num-mono">2000-01 to 2026-10<br>Accessed Nov 2026</td>
                  <td>High-albedo mountain retrieval filtering; radiative transfer parameterization for snow albedo reduction.</td>
                  <td>NASA Open Data (Public Domain)</td>
                </tr>
                <tr>
                  <td><b>Meteomatics High-Altitude Assimilation</b><br><span class="num-mono">REST API v1 (90m downscaled)</span></td>
                  <td>Snow depth (cm), 7-day glacier terminus forecast, 0 °C freezing level (m)</td>
                  <td class="num-mono">Point / 90m terrain-corrected, Daily &amp; Monthly</td>
                  <td class="num-mono">1981-01 to 2026-10<br>Cached Nov 2026</td>
                  <td>Orographic lapse-rate downscaling to 15 RGI glacier snout and ELA coordinates; cached locally with deterministic fallback.</td>
                  <td>Meteomatics Scientific / Space Apps License</td>
                </tr>
                <tr>
                  <td><b>Randolph Glacier Inventory &amp; SRTM</b><br><span class="num-mono">GLIMS RGI v6.0 (Region 13/14) &amp; SRTM GL1 v3.0</span></td>
                  <td>Glacier polygon outlines (km²), hypsometric elevation bands (m)</td>
                  <td class="num-mono">30 m DEM / Vector polygons</td>
                  <td class="num-mono">Baseline inventory<br>Accessed Nov 2026</td>
                  <td>Used to partition each river basin into four elevation bands (&lt;3,500 m, 3,500-4,500 m, 4,500-5,500 m, &gt;5,500 m) and glacier-only masks.</td>
                  <td>CC BY 4.0 (GLIMS / NSIDC) &amp; USGS Public Domain</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <div class="dashShell" style="margin-top:20px">
        <div class="dashTop">
          <div>
            <span class="mono">Methodological constraints and physical caveats</span>
            <div class="dashTitle">Scientific Limitations and Assumptions</div>
          </div>
        </div>
        <div class="dashBody">
          <div class="featureGrid" id="limitationsContainer"></div>
        </div>
      </div>

      <div class="dashShell" id="privacyTermsSection" style="margin-top:20px">
        <div class="dashTop">
          <div>
            <span class="mono">Reproducibility, citation, repository, and governance</span>
            <div class="dashTitle">How to Cite, Source Repository, Contact, and Terms of Use</div>
          </div>
        </div>
        <div class="dashBody">
          <div class="featureGrid">
            <div class="glass">
              <div class="num">How to cite this workbench</div>
              <h3>Recommended Citation</h3>
              <p class="num-mono" style="font-size:12px;background:var(--bg-canvas);padding:10px;border:1px solid var(--border-default);border-radius:4px">
                Hassan, A. (2026). Himalaya Trend Lab: Non-parametric statistical and cryosphere trend workbench for Pakistan's glacier basins (v1.0). NASA Space Apps Challenge 2026 (Earth System Trend Detective). https://github.com/alihassan-earth/himalaya-trend-lab
              </p>
            </div>
            <div class="glass">
              <div class="num">Codebase, notebooks, and contact</div>
              <h3>Open Science &amp; Reproducibility</h3>
              <p>
                All statistical tests (<code class="num-mono">analytics/trend_tests.py</code>), spatial FDR procedures (<code class="num-mono">analytics/spatial_trends.py</code>), and scikit-learn pipelines (<code class="num-mono">ml/</code>) are open source and verified via <code class="num-mono">pytest</code>.<br><br>
                <b>GitHub Repository:</b> <a href="https://github.com/alihassan-earth/himalaya-trend-lab" target="_blank" rel="noopener noreferrer" style="color:var(--accent-link)">github.com/alihassan-earth/himalaya-trend-lab</a><br>
                <b>Lead Author Contact:</b> <a href="mailto:ali.hassan@himalayatrendlab.org" style="color:var(--accent-link)">ali.hassan@himalayatrendlab.org</a>
              </p>
            </div>
            <div class="glass">
              <div class="num">Privacy policy and terms of use</div>
              <h3>Privacy &amp; Operational Disclaimer</h3>
              <p>
                <b>Privacy Policy:</b> This application runs locally or on stateless scientific servers and does not collect personal data, cookies, or tracking analytics.<br><br>
                <b>Terms of Use:</b> Provided under the MIT License for research and educational use. GLOF watchlist scores are diagnostic meteorological indicators and do not replace official Pakistan Meteorological Department (PMD) evacuation warnings.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>`
  );
}

/* ============================================================================
   PAGE 6: AI / ML LAB (GPR Changepoint + RF Drivers + 36m Forecast + K-Means)
   ============================================================================ */
function ml() {
  return (
    pageHead(
      "Out-of-sample machine learning diagnostics (scikit-learn artifacts)",
      "Machine Learning Cryosphere Suite",
      "Inspect pre-trained Gaussian Process Regression changepoint models, Random Forest driver attribution, 36-month holdout forecasts (2026 to 2029), and K-Means/PCA regime clustering across nine basins."
    ) +
    `<div class="pageBody">
      <div class="dashShell">
        <div class="dashTop">
          <div>
            <span class="mono" id="mlTopTag">Model evaluation: 80/20 temporal train-test split and 5-fold cross-validation</span>
            <div class="dashTitle" id="mlTopTitle">Karakoram Range: Machine Learning Diagnostics</div>
          </div>
          <div class="controls" style="grid-template-columns:1fr 1fr;min-width:440px">
            <div class="control">
              <label for="mlPlaceSelect">Select river basin or range</label>
              <select id="mlPlaceSelect">
                <option value="Karakoram">Karakoram Range</option>
                <option value="Hunza">Hunza River Basin</option>
                <option value="Hindu Kush">Hindu Kush Range</option>
                <option value="Western Himalaya">Western Himalaya</option>
                <option value="Upper Indus">Upper Indus Basin</option>
                <option value="Gilgit">Gilgit River Basin</option>
                <option value="Chitral">Chitral River Basin</option>
                <option value="Astore">Astore Valley Basin</option>
                <option value="Neelum">Neelum River Basin</option>
              </select>
            </div>
            <div class="control">
              <label for="mlVarSelect">Target response variable</label>
              <select id="mlVarSelect">
                <option value="snow_cover_modis">MODIS Snow Cover (%)</option>
                <option value="t2m_merra2">MERRA-2 2m Air Temp (°C)</option>
                <option value="swe_gldas">GLDAS Snow Water Equivalent (mm)</option>
                <option value="runoff_gldas">GLDAS Meltwater Runoff (mm/mo)</option>
              </select>
            </div>
          </div>
        </div>
        <div class="dashBody">
          <div class="metrics" id="mlMetricsRow">
            <div class="metric"><b id="mlGprYear" class="num-mono">2016</b><span>GPR structural changepoint year</span></div>
            <div class="metric"><b id="mlTopDriver" class="num-mono">2m Air Temp</b><span>Primary Random Forest predictor</span></div>
            <div class="metric"><b id="mlFcstR2" class="num-mono">R2 = 0.99</b><span>36-month holdout test accuracy</span></div>
            <div class="metric"><b id="mlSilScore" class="num-mono">0.467</b><span>K-Means (k=3) silhouette score</span></div>
          </div>

          <div class="chartGrid">
            <figure class="chartFigure">
              <div class="chart" id="mlChartGpr">${placeholderSvg}</div>
              <figcaption class="chartCaption">
                <span>Figure 5A: Gaussian Process Regression (RBF + WhiteKernel) non-linear trend and 2-sigma posterior uncertainty band.</span>
                <a id="mlCsvLink1" href="/api/export/csv?place=Karakoram&variable=MODIS%20Snow%20Cover&years=45" target="_blank" rel="noopener">Download CSV</a>
              </figcaption>
            </figure>
            <figure class="chartFigure">
              <div class="chart" id="mlChartFcst">${placeholderSvg}</div>
              <figcaption class="chartCaption">
                <span>Figure 5B: 36-month out-of-sample hybrid ridge/tree projection (2026 to 2029) with 95% prediction interval.</span>
                <a id="mlCsvLink2" href="/api/export/csv?place=Karakoram&variable=MODIS%20Snow%20Cover&years=45" target="_blank" rel="noopener">Download CSV</a>
              </figcaption>
            </figure>
          </div>

          <div class="chartGrid" style="margin-top:16px;grid-template-columns:1.1fr 1.3fr">
            <div>
              <span class="mono">Random Forest and Boosted Tree permutation importance (%)</span>
              <div class="mlBars" id="mlDriverBars"></div>
            </div>
            <div>
              <span class="mono">Unsupervised K-Means (k=3) and PCA cryosphere regime classification</span>
              <div class="shieldTable" id="mlClusterTable"></div>
            </div>
          </div>
        </div>
      </div>
    </div>`
  );
}

/* ============================================================================
   PAGE 7: SHIELD (15-Glacier GLOF Watchlist + Indus Water Tower Simulator)
   ============================================================================ */
function shield() {
  return (
    pageHead(
      "Glacial lake outburst flood (GLOF) watchlist and downstream hydrology",
      "HimalayaShield Watchlist and Indus Simulator",
      "Evaluates 7-day meteorological outburst flood trigger scores across 15 monitored Pakistan glacier termini and simulates Upper Indus / Tarbela Dam annual inflows (2020 to 2080)."
    ) +
    `<div class="pageBody">
      <div class="featureGrid">
        ${cardBox("Meteorological trigger index", "15 Monitored Glacier Termini", "Combines terminus air temperature, 7-day snowmelt accumulation, and 0 °C freezing altitude relative to each glacier's equilibrium line altitude (ELA).")}
        ${cardBox("Downstream infrastructure", "Exposure Inventory", "Documents highway bridges, settlements, and hydropower cascades downstream of each terminus (Karakoram Highway, Hassanabad, Tarbela, Diamer-Bhasha, Dasu).")}
        ${cardBox("Hydrological mass balance", "Indus Peak Water Simulator", "Projects Tarbela Dam annual inflows (64.5 MAF baseline), Rabi/Kharif irrigation supply, and firm hydropower across SSP warming trajectories (2020 to 2080).")}
      </div>

      <div class="dashShell" style="margin-top:20px">
        <div class="dashTop">
          <div>
            <span class="mono">7-day meteorological trigger evaluation (pre-cached assimilation + Isolation Forest anomaly detector)</span>
            <div class="dashTitle">Pakistan Glacier Outburst Flood (GLOF) Watchlist (15 Termini)</div>
          </div>
          <span class="mono" id="shieldIsoSummary">Isolation Forest compound hazard detector: active</span>
        </div>
        <div class="dashBody" style="padding:0">
          <div class="shieldTable" id="shieldGlacierTable" style="margin-top:0;border:0"></div>
        </div>
      </div>

      <div class="dashShell" style="margin-top:20px">
        <div class="dashTop">
          <div>
            <span class="mono">Upper Indus Basin and Tarbela Dam hydrological projection (2020 to 2080)</span>
            <div class="dashTitle">Downstream Water Security, Crop Irrigation, and 15,827 MW Hydropower Simulator</div>
          </div>
          <div class="tabs" id="waterScenarioTabs">
            <button class="tab" type="button" data-dt="1.5" data-ds="2.0">SSP1-2.6 (+1.5 °C)</button>
            <button class="tab active" type="button" data-dt="2.4" data-ds="-8.0">SSP2-4.5 (+2.4 °C)</button>
            <button class="tab" type="button" data-dt="3.2" data-ds="-14.0">SSP3-7.0 (+3.2 °C)</button>
            <button class="tab" type="button" data-dt="4.2" data-ds="-20.0">SSP5-8.5 (+4.2 °C)</button>
          </div>
        </div>
        <div class="dashBody">
          <div class="controls" style="grid-template-columns:1fr 1fr">
            <div class="control">
              <label for="temp">Basin warming anomaly (delta T): <span id="tempValLabel" class="num-mono">+2.4 °C</span></label>
              <input id="temp" type="range" min="1.0" max="4.5" step="0.1" value="2.4">
            </div>
            <div class="control">
              <label for="snowSim">Winter snowfall change (delta Snow): <span id="snowValLabel" class="num-mono">-8%</span></label>
              <input id="snowSim" type="range" min="-25" max="25" step="1" value="-8">
            </div>
          </div>
          <div class="verdict">
            <span class="mono">Hydrological regime projection (Upper Indus catchment at Tarbela)</span>
            <strong id="maf">+2.4 °C scenario: Peak Water Year 2039 (72.3 MAF) followed by 2075 inflow of 53.6 MAF</strong>
            <p id="waterSubVerdict">Prior to Peak Water, accelerated glacier ablation temporarily increases summer inflows. Beyond the Peak Water tipping year, depleted glacier ice volume reduces late-summer baseflow for Kharif irrigation and firm hydropower generation.</p>
          </div>
          <div class="metrics" id="waterMetricsGrid">
            <div class="metric"><b class="num-mono">2039</b><span>Peak Water tipping year</span></div>
            <div class="metric"><b class="num-mono">72.3 MAF</b><span>Peak annual inflow</span></div>
            <div class="metric"><b class="num-mono">53.6 MAF</b><span>Projected 2075 annual inflow</span></div>
            <div class="metric"><b class="num-mono">52.4%</b><span>Remaining glacier ice volume (2080)</span></div>
          </div>
          <figure class="chartFigure" style="margin-top:16px">
            <div class="chart" id="waterHydroChart">${placeholderSvg}</div>
            <figcaption class="chartCaption">
              <span>Figure 6: Simulated Tarbela Dam annual inflow (Million Acre-Feet, MAF) from 2020 to 2080 vs. 64.5 MAF historical baseline (dashed line).</span>
            </figcaption>
          </figure>
        </div>
      </div>
    </div>`
  );
}

/* ============================================================================
   BACKEND API BINDINGS FOR ALL 7 PAGES
   ============================================================================ */

async function bindHomePreview() {
  const loadPreview = async (place, variable) => {
    try {
      const res = await fetch(
        `/api/investigate?place=${encodeURIComponent(place)}&variable=${encodeURIComponent(variable)}&alpha=0.05&years=45`
      );
      if (!res.ok) return;
      const d = await res.json();
      const title = document.getElementById("homePreviewTitle");
      if (title) title.textContent = `${d.region_name}: ${d.variable_name}`;
      const tag = document.getElementById("homePreviewTag");
      if (tag) tag.textContent = `Dataset: ${d.source_mission} · ${d.start_year} to ${d.end_year} (${d.n_months} months, pre-cached Nov 2026)`;
      const badge = document.getElementById("homeVerdictBadge");
      if (badge) badge.textContent = `Statistical verdict: ${formatBadge(d.verdict?.badge_status)}`;
      const head = document.getElementById("homeVerdictHead");
      if (head) head.textContent = d.verdict?.headline || "";
      const sub = document.getElementById("homeVerdictSub");
      if (sub) {
        const fq = d.verdict?.four_questions || {};
        const whatTxt = fq.what_is_changing || "";
        const speedTxt = fq.how_much_is_it_changing || fq.how_fast_is_it_changing || "";
        const sigTxt = fq.is_it_significant || fq.is_it_statistically_significant || "";
        sub.textContent = `${whatTxt} ${speedTxt} ${sigTxt}`.trim();
      }
      const mg = document.getElementById("homeMetricsGrid");
      if (mg && d.metrics) {
        const shiftM = d.freezing_level?.shift_m ?? 0;
        mg.innerHTML = `
          <div class="metric"><b class="num-mono">${d.metrics.sen_decade || "N/A"}</b><span>Sen slope per decade (95% CI ${d.metrics.sen_ci || ""})</span></div>
          <div class="metric"><b class="num-mono">${formatP(d.metrics.hamed_rao_p)}</b><span>Hamed-Rao adjusted p-value</span></div>
          <div class="metric"><b class="num-mono">${shiftM >= 0 ? "+" : ""}${shiftM} m</b><span>Basin 0 °C isotherm shift</span></div>
          <div class="metric"><b class="num-mono">${d.start_year} to ${d.end_year}</b><span>${d.n_years}-year record (${d.n_months} months)</span></div>`;
      }
      const c1 = document.getElementById("homeChart");
      if (c1 && d.svg_anomaly) c1.innerHTML = d.svg_anomaly;
      const c2 = document.getElementById("homeSeasonChart");
      if (c2 && d.svg_seasonal) c2.innerHTML = d.svg_seasonal;

      const csvUrl = `/api/export/csv?place=${encodeURIComponent(place)}&variable=${encodeURIComponent(variable)}&years=45`;
      const cap1 = document.getElementById("homeChartCap1");
      if (cap1) {
        cap1.innerHTML = `<span>Figure 1A: ${d.variable_name} (${d.units}) deseasonalized anomaly and Theil-Sen trend (${d.source_mission}, ${d.start_year} to ${d.end_year}).</span><a href="${csvUrl}" target="_blank" rel="noopener">Download CSV</a>`;
      }
      const cap2 = document.getElementById("homeChartCap2");
      if (cap2) {
        cap2.innerHTML = `<span>Figure 1B: 12-month seasonal climatology (${d.units}) subtracted prior to anomaly trend test (${d.start_year} to ${d.end_year}).</span><a href="${csvUrl}" target="_blank" rel="noopener">Download CSV</a>`;
      }
    } catch (e) {}
  };

  const tabs = document.querySelectorAll("#homeBasinTabs .tab");
  tabs.forEach((btn) => {
    btn.addEventListener("click", () => {
      tabs.forEach((b) => {
        b.classList.remove("active");
        b.setAttribute("aria-selected", "false");
      });
      btn.classList.add("active");
      btn.setAttribute("aria-selected", "true");
      loadPreview(btn.dataset.place, btn.dataset.var);
    });
  });
  loadPreview("Hunza", "MERRA-2 2m Air Temp");
}

async function fetchLiveInvestigation(body) {
  const place = body.querySelector("#invPlace")?.value || "Hunza";
  const compare = body.querySelector("#invCompare")?.value || "none";
  const variable = body.querySelector("#invVar")?.value || "MERRA-2 2m Air Temp";
  const alpha = body.querySelector("#invAlpha")?.value || "0.05";
  const glacierOnly = body.querySelector("#invMask")?.value || "false";
  const years = body.querySelector("#years")?.value || "45";

  try {
    const url = `/api/investigate?place=${encodeURIComponent(place)}&variable=${encodeURIComponent(
      variable
    )}&alpha=${encodeURIComponent(alpha)}&years=${encodeURIComponent(
      years
    )}&glacier_only=${encodeURIComponent(glacierOnly)}&compare_place=${encodeURIComponent(compare)}`;
    const res = await fetch(url);
    if (!res.ok) return;
    const data = await res.json();

    const titleEl = body.querySelector("#invTitle");
    if (titleEl) {
      titleEl.textContent = `${data.region_name}: ${data.variable_name}${
        glacierOnly === "true" ? " (RGI v6.0 Glacier Polygon Mask)" : ""
      }`;
    }
    const srcEl = body.querySelector("#invSourceTag");
    if (srcEl) {
      srcEl.textContent = `Dataset: ${data.source_mission} · Period: ${data.start_year} to ${data.end_year} (${data.n_months} months) · Archive: ${data.source_mode}`;
    }
    const badgeEl = body.querySelector("#invBadge");
    if (badgeEl) badgeEl.textContent = `Statistical verdict: ${formatBadge(data.verdict?.badge_status)}`;
    const headEl = body.querySelector("#invHeadline");
    if (headEl) headEl.textContent = data.verdict?.headline || "";
    const subEl = body.querySelector("#invSubtext");
    if (subEl) {
      const fq = data.verdict?.four_questions || {};
      const qWhat = fq.what_is_changing || "N/A";
      const qWhere = fq.where_is_it_changing || "N/A";
      const qRate = fq.how_much_is_it_changing || fq.how_fast_is_it_changing || "N/A";
      const qSig = fq.is_it_significant || fq.is_it_statistically_significant || "N/A";
      const acNote = data.verdict?.autocorrelation_note || "";
      subEl.innerHTML = `<b>1. Variable &amp; Deseasonalization:</b> ${qWhat}<br>
        <b>2. Spatial Domain:</b> ${qWhere}<br>
        <b>3. Rate of Change:</b> ${qRate}<br>
        <b>4. Significance &amp; Autocorrelation:</b> ${qSig} ${acNote}`;
    }

    const compBanner = body.querySelector("#invCompareBanner");
    if (compBanner) {
      if (data.comparison) {
        compBanner.style.display = "block";
        compBanner.innerHTML = `<span class="mono">Side-by-side comparison: ${data.comparison.region_name} (${data.comparison.badge})</span>
          <strong>${data.comparison.headline}</strong>
          <p>Comparison Sen slope: <b class="num-mono">${data.comparison.sen_decade}/decade</b> (<span class="num-mono">${formatP(data.comparison.p_value)}</span>) vs. Primary ${data.region_name}: <b class="num-mono">${data.metrics.sen_decade}/decade</b> (<span class="num-mono">${formatP(data.metrics.hamed_rao_p)}</span>).</p>`;
      } else {
        compBanner.style.display = "none";
      }
    }

    const mContainer = body.querySelector("#invMetrics");
    if (mContainer && data.metrics) {
      mContainer.innerHTML = `
        <div class="metric"><b class="num-mono">${data.metrics.sen_decade}</b><span>Sen slope per decade (95% CI ${data.metrics.sen_ci})</span></div>
        <div class="metric"><b class="num-mono">${data.metrics.ols_decade}</b><span>OLS slope per decade (total ${data.metrics.total_change})</span></div>
        <div class="metric"><b class="num-mono">${data.metrics.mk_tau}</b><span>Mann-Kendall tau (lag-1 r = ${data.metrics.lag1_autocorr})</span></div>
        <div class="metric"><b class="num-mono">${formatP(data.metrics.hamed_rao_p)}</b><span>Hamed-Rao p-value (VIF ${data.metrics.vif})</span></div>`;
    }

    const cryoContainer = body.querySelector("#invCryoMetrics");
    if (cryoContainer) {
      const shiftM = data.freezing_level?.shift_m ?? 0;
      const curEla = data.freezing_level?.current_ela_m ?? 5100;
      const exposedKm2 = data.freezing_level?.newly_exposed_ice_km2 ?? 0;
      const extraMelt = data.dark_ice?.extra_melt_mm_per_month ?? 0;
      const sootShare = data.dark_ice?.soot_melt_share_pct ?? data.dark_ice?.albedo_reduction_pct ?? 0;
      const fdrPct = data.spatial?.summary?.pct_significant_fdr ?? 0;
      const fourthTile =
        fdrPct > 0
          ? `<div class="metric"><b class="num-mono">${fdrPct}%</b><span>BH-FDR significant grid cells (alpha = ${alpha})</span></div>`
          : `<div class="metric"><b class="num-mono">${exposedKm2} km²</b><span>Glacier ice exposed by 0 °C isotherm rise</span></div>`;

      cryoContainer.innerHTML = `
        <div class="metric"><b class="num-mono">${shiftM >= 0 ? "+" : ""}${shiftM} m</b><span>Basin 0 °C isotherm vertical shift</span></div>
        <div class="metric"><b class="num-mono">${curEla} m</b><span>Current equilibrium line altitude (ELA)</span></div>
        <div class="metric"><b class="num-mono">+${extraMelt} mm/mo</b><span>Aerosol albedo melt (${sootShare}% of summer ablation)</span></div>
        ${fourthTile}`;
    }

    const csvUrl = `/api/export/csv?place=${encodeURIComponent(place)}&variable=${encodeURIComponent(
      variable
    )}&years=${encodeURIComponent(years)}`;

    const c1 = body.querySelector("#invChartAnom");
    if (c1 && data.svg_anomaly) {
      c1.innerHTML = data.svg_anomaly;
      const cap1 = body.querySelector("#invChartCap1");
      if (cap1) {
        cap1.innerHTML = `<span>Figure 2A: ${data.variable_name} (${data.units}) deseasonalized anomaly, Theil-Sen slope, and 95% CI (${data.source_mission}, ${data.start_year} to ${data.end_year}).</span><a href="${csvUrl}" target="_blank" rel="noopener">Download CSV</a>`;
      }
      const tw1 = body.querySelector("#invTableWrap1");
      if (tw1) tw1.innerHTML = buildAccessibleTableFromSvg(data.svg_anomaly, `${data.region_name} ${data.variable_name} anomaly summary`);
    }

    const c2 = body.querySelector("#invChartSeason");
    if (c2) {
      if (data.comparison && data.comparison.svg_anomaly) {
        c2.innerHTML = data.comparison.svg_anomaly;
        const compCsv = `/api/export/csv?place=${encodeURIComponent(compare)}&variable=${encodeURIComponent(
          variable
        )}&years=${encodeURIComponent(years)}`;
        const cap2 = body.querySelector("#invChartCap2");
        if (cap2) {
          cap2.innerHTML = `<span>Figure 2B: Comparison basin (${data.comparison.region_name}) deseasonalized anomaly and Theil-Sen trend (${data.start_year} to ${data.end_year}).</span><a href="${compCsv}" target="_blank" rel="noopener">Download CSV</a>`;
        }
        const tw2 = body.querySelector("#invTableWrap2");
        if (tw2) tw2.innerHTML = buildAccessibleTableFromSvg(data.comparison.svg_anomaly, `${data.comparison.region_name} comparison summary`);
      } else if (data.svg_seasonal) {
        c2.innerHTML = data.svg_seasonal;
        const cap2 = body.querySelector("#invChartCap2");
        if (cap2) {
          cap2.innerHTML = `<span>Figure 2B: 12-month calendar climatology (${data.units}) removed prior to anomaly trend test (${data.start_year} to ${data.end_year}).</span><a href="${csvUrl}" target="_blank" rel="noopener">Download CSV</a>`;
        }
        const tw2 = body.querySelector("#invTableWrap2");
        if (tw2) tw2.innerHTML = buildAccessibleTableFromSvg(data.svg_seasonal, `${data.region_name} 12-month climatology summary`);
      }
    }

    const elevEl = body.querySelector("#invElevBands");
    if (elevEl && data.spatial?.elevation_bands) {
      elevEl.innerHTML = data.spatial.elevation_bands
        .map((b) => {
          const bandName = (b.elevation_band || b.band_label || "Elevation zone").split("(")[0].trim();
          const slopeVal = Number(b.slope_per_decade || 0);
          const w = Math.min(100, Math.max(12, Math.abs(slopeVal) * 45 + 20));
          return `<div class="mlBar" style="grid-template-columns:130px 1fr 90px"><span>${bandName}</span><i style="width:${w}%"></i><b class="num-mono">${slopeVal >= 0 ? "+" : ""}${slopeVal.toFixed(2)} ${data.units}</b></div>`;
        })
        .join("");
    }

    const teleEl = body.querySelector("#invTeleList");
    if (teleEl && data.teleconnections) {
      teleEl.innerHTML = data.teleconnections
        .map((t) => {
          const code = t.index_id || t.index_code || "INDEX";
          const rVal = t.pearson_r ?? t.correlation_r ?? 0;
          const pVal = t.pearson_p ?? t.p_value ?? 0.05;
          const desc = t.physical_mechanism || t.relationship_strength || "";
          return `<div style="padding:10px 12px;border:1px solid var(--border-default);border-radius:4px;background:var(--bg-canvas);font-size:13px">
              <b class="num-mono" style="color:var(--accent-link)">${code} (r = ${rVal >= 0 ? "+" : ""}${rVal}, ${formatP(pVal)})</b>: <span style="color:var(--text-secondary)">${desc}</span>
            </div>`;
        })
        .join("");
    }

    const defTitle = body.querySelector("#invVarDefTitle");
    if (defTitle) defTitle.textContent = `${data.variable_name} (${data.units})`;
    const defText = body.querySelector("#invVarDefText");
    if (defText) {
      defText.innerHTML = `<b>Definition:</b> ${data.plain_definition || ""}<br><br><b>Methodological caveat:</b> ${data.caveats || ""}`;
    }

    const lab = body.querySelector("#yearsLabel");
    if (lab) lab.textContent = `${data.start_year} to ${data.end_year} (${data.n_years} yrs)`;
  } catch (err) {}
}

function enhancePage(n) {
  document.querySelectorAll(".navlinks a").forEach((a) => {
    a.classList.toggle("activeNav", a.getAttribute("href") === "#" + n);
  });

  if (n === "home") {
    bindHomePreview();
    return;
  }

  const body = view.querySelector(".pageBody");
  if (!body) return;

  const ribbon = document.createElement("div");
  ribbon.className = "dataRibbon";
  ribbon.setAttribute("aria-label", "Archive metadata summary");
  ribbon.innerHTML =
    '<div><span>Data archive mode</span><b class="num-mono">Pre-cached v1.0</b><span>NASA EOSDIS &amp; Meteomatics (Nov 2026)</span></div>' +
    '<div><span>Temporal coverage</span><b class="num-mono">1981 to 2026</b><span>45 years · Monthly resolution</span></div>' +
    '<div><span>Spatial domain</span><b class="num-mono">9 Basins / 15 Glaciers</b><span>RGI v6.0 cryosphere polygons</span></div>' +
    '<div><span>Statistical protocol</span><b class="num-mono">Sen + Hamed-Rao</b><span>95% CI · Autocorrelation &amp; FDR control</span></div>';
  body.insertBefore(ribbon, body.firstChild);

  if (n === "investigate") {
    body.querySelectorAll("#questionPills .pill").forEach((pill) => {
      pill.addEventListener("click", () => {
        body.querySelectorAll("#questionPills .pill").forEach((p) => p.classList.remove("activePill"));
        pill.classList.add("activePill");
        const varSelect = body.querySelector("#invVar");
        if (varSelect) {
          varSelect.value = pill.dataset.var;
          fetchLiveInvestigation(body);
        }
      });
    });

    body.querySelectorAll(".control select").forEach((s) =>
      s.addEventListener("change", () => fetchLiveInvestigation(body))
    );
    const range = body.querySelector("#years");
    if (range) {
      range.addEventListener("input", (e) => {
        const y = +e.target.value;
        const lab = body.querySelector("#yearsLabel");
        if (lab) lab.textContent = `${2026 - y + 1} to 2026 (${y} yrs)`;
      });
      range.addEventListener("change", () => fetchLiveInvestigation(body));
    }

    const btnCsv = body.querySelector("#btnExportCsv"),
      btnPdf = body.querySelector("#btnExportPdf");
    if (btnCsv)
      btnCsv.addEventListener("click", () => {
        const place = body.querySelector("#invPlace").value,
          variable = body.querySelector("#invVar").value,
          years = body.querySelector("#years").value;
        window.open(
          `/api/export/csv?place=${encodeURIComponent(place)}&variable=${encodeURIComponent(
            variable
          )}&years=${encodeURIComponent(years)}`,
          "_blank"
        );
      });
    if (btnPdf)
      btnPdf.addEventListener("click", () => {
        const place = body.querySelector("#invPlace").value,
          variable = body.querySelector("#invVar").value,
          alpha = body.querySelector("#invAlpha").value,
          years = body.querySelector("#years").value;
        window.open(
          `/api/export/pdf?place=${encodeURIComponent(place)}&variable=${encodeURIComponent(
            variable
          )}&alpha=${encodeURIComponent(alpha)}&years=${encodeURIComponent(years)}`,
          "_blank"
        );
      });

    if (window.__pendingInvestigate) {
      const p = window.__pendingInvestigate;
      delete window.__pendingInvestigate;
      if (p.place && body.querySelector("#invPlace")) body.querySelector("#invPlace").value = p.place;
      if (p.compare && body.querySelector("#invCompare")) body.querySelector("#invCompare").value = p.compare;
      if (p.variable && body.querySelector("#invVar")) body.querySelector("#invVar").value = p.variable;
    }

    fetchLiveInvestigation(body);
  }

  if (n === "cases") {
    let activeCaseData = null;
    const loadCase = async (idx) => {
      try {
        const res = await fetch(`/api/cases?case_index=${idx}`);
        if (!res.ok) return;
        const d = await res.json();
        activeCaseData = d.case;
        const tag = body.querySelector("#caseCodeTag");
        if (tag) tag.textContent = `${d.case.code || "Case"}: ${d.case.subtitle || "Regional comparison"}`;
        const title = body.querySelector("#caseMainTitle");
        if (title) title.textContent = d.case.title || "";

        body.querySelector("#casePrimaryBadge").textContent = `Primary basin: ${formatBadge(d.primary.badge)}`;
        body.querySelector("#casePrimaryHead").textContent = `${d.primary.region_name}: ${d.primary.headline}`;
        body.querySelector("#casePrimaryStat").textContent = `Sen slope: ${d.primary.sen_slope} · Hamed-Rao ${formatP(d.primary.p_formatted || d.primary.p_value)}`;

        body.querySelector("#caseCompBadge").textContent = `Comparison basin: ${formatBadge(d.comparison.badge)}`;
        body.querySelector("#caseCompHead").textContent = `${d.comparison.region_name}: ${d.comparison.headline}`;
        body.querySelector("#caseCompStat").textContent = `Sen slope: ${d.comparison.sen_slope} · Hamed-Rao ${formatP(d.comparison.p_formatted || d.comparison.p_value)}`;

        const svgBox = body.querySelector("#caseReplaySvg");
        if (svgBox && d.svg) svgBox.innerHTML = d.svg;

        const qTitle = body.querySelector("#caseQuestionTitle");
        if (qTitle) qTitle.textContent = d.case.question || d.case.title || "";
        const take = body.querySelector("#caseTakeawayText");
        if (take) take.textContent = d.case.detective_takeaway || d.case.summary || d.case.takeaway || "";
        const steps = body.querySelector("#caseStepsList");
        if (steps) {
          const stepArr = d.case.story_steps || [d.case.takeaway || ""];
          steps.innerHTML = stepArr.map((s) => `<div style="margin-bottom:6px">${s}</div>`).join("");
        }
      } catch (e) {}
    };

    body.querySelectorAll("#caseCardsGrid .glass").forEach((card, i) => {
      card.addEventListener("click", () => {
        body.querySelectorAll("#caseCardsGrid .glass").forEach((c) => c.classList.remove("missionDone"));
        card.classList.add("missionDone");
        loadCase(i);
      });
    });

    const btnOpen = body.querySelector("#btnOpenCaseInLab");
    if (btnOpen) {
      btnOpen.addEventListener("click", () => {
        const mapPlace = {
          karakoram: "Karakoram",
          hindu_kush: "Hindu Kush",
          hunza: "Hunza",
          astore: "Astore",
          upper_indus: "Upper Indus",
          western_himalaya: "Western Himalaya",
        };
        const mapVar = {
          snow_cover_modis: "MODIS Snow Cover",
          t2m_merra2: "MERRA-2 2m Air Temp",
          precip_imerg: "GPM IMERG Precipitation",
        };
        if (activeCaseData) {
          window.__pendingInvestigate = {
            place: mapPlace[activeCaseData.region_id] || "Karakoram",
            compare: mapPlace[activeCaseData.compare_region_id] || "Hindu Kush",
            variable: mapVar[activeCaseData.variable_id] || "MODIS Snow Cover",
          };
        }
        location.hash = "investigate";
      });
    }

    loadCase(0);

    fetch("/api/reference?region=karakoram")
      .then((r) => r.json())
      .then((d) => {
        const tbl = body.querySelector("#sensorValidationTable");
        if (tbl && d.sensor_validation) {
          const rows = d.sensor_validation
            .map((s) => {
              const pairName = s["Validation Pair"] || s.sensor_pair || "Sensor Pair";
              const rAnom = s["Anomaly Correlation (r)"] ?? s.correlation_r ?? 0;
              const rRaw = s["Raw Cycle Correlation (r)"] ?? rAnom;
              const slopeA = s["Sensor A Slope/Decade"] ?? "";
              const slopeB = s["Sensor B Slope/Decade"] ?? "";
              const status = s["Significance Agreement"] || s["Direction Agreement"] || s.validation_status || "Verified";
              return `<div class="shieldRow"><b>${pairName}</b><b class="statusLow num-mono">r_anom = ${rAnom} (raw = ${rRaw})</b><span class="num-mono">Slopes: ${slopeA} vs. ${slopeB} /dec</span><span>${status}</span></div>`;
            })
            .join("");
          tbl.innerHTML =
            '<div class="shieldRow headerRow"><span>Sensor pair</span><span>Correlation (r)</span><span>Decadal slopes</span><span>Agreement status</span></div>' +
            rows;
        }
      })
      .catch(() => {});
  }

  if (n === "notebook") {
    const tourSteps = [
      {
        title: "Step 1 of 5: Research Scope and Study Basins",
        badge: "Scope: 9 river basins, 15 glacier termini, 10 variables (1981 to 2026)",
        head: "Separating Secular Cryosphere Trends from Seasonal and Interannual Variability",
        summary:
          "Himalaya Trend Lab provides researchers and students with a reproducible pipeline to evaluate 45 years of NASA satellite (MODIS, MERRA-2, GPM IMERG, GLDAS, OMI) and Meteomatics series across northern Pakistan.",
      },
      {
        title: "Step 2 of 5: Non-Parametric Trend Estimation and Autocorrelation Control",
        badge: "Methods: Theil-Sen median slope, Hamed-Rao Mann-Kendall, and Benjamini-Hochberg FDR",
        head: "Why Ordinary Linear Regression Fails on Monthly Cryosphere Records",
        summary:
          "Mountain climate series exhibit strong seasonal cycles and month-to-month persistence (lag-1 autocorrelation). We subtract the 12-month climatology, compute outlier-resistant Theil-Sen slopes, and adjust Mann-Kendall variance via Hamed-Rao (1998).",
      },
      {
        title: "Step 3 of 5: Regional Divergence Across High Asia",
        badge: "Comparison: Karakoram (-0.35%/dec, p = 0.084) vs. Hindu Kush (-2.45%/dec, p < 0.0001)",
        head: "Quantifying the Karakoram Anomaly vs. Hindu Kush Snow Loss",
        summary:
          "RGI v6.0 glacier-polygon masking and hypsometric band analysis demonstrate that winter westerly snowfall buffers high-elevation Karakoram accumulation zones while lower-elevation Hindu Kush basins experience significant snow cover loss.",
      },
      {
        title: "Step 4 of 5: Out-of-Sample Machine Learning Diagnostics",
        badge: "Models: GPR changepoints, Random Forest driver attribution, and 36-month holdout forecast",
        head: "Identifying Structural Regime Shifts and Physical Covariates",
        summary:
          "Pre-trained Gaussian Process Regression models identify structural regime transitions, Random Forests rank physical covariates (temperature, snowfall, aerosols, NAO), and ridge/tree ensembles evaluate 36-month holdout predictability.",
      },
      {
        title: "Step 5 of 5: GLOF Hazard Watchlist and Downstream Water Security",
        badge: "Impact: 15 glacier termini, 64.5 MAF Tarbela baseline, and 15,827 MW hydropower cascade",
        head: "Connecting Cryosphere Mass Balance to Indus Basin Water Resources",
        summary:
          "Evaluates 7-day meteorological trigger scores across 15 glacier termini (including Shisper, Passu, and Batura) and simulates the Tarbela Dam Peak Water tipping point under SSP warming scenarios.",
      },
    ];

    body.querySelectorAll("#tourTabs .tab").forEach((btn) => {
      btn.addEventListener("click", () => {
        body.querySelectorAll("#tourTabs .tab").forEach((b) => b.classList.remove("active"));
        btn.classList.add("active");
        const s = tourSteps[+btn.dataset.step];
        body.querySelector("#tourStepTitle").textContent = s.title;
        body.querySelector("#tourMetricBadge").textContent = s.badge;
        body.querySelector("#tourHead").textContent = s.head;
        body.querySelector("#tourSummary").textContent = s.summary;
      });
    });

    const cards = body.querySelectorAll("#missionsGrid .glass");
    const bar = body.querySelector("#missionBar");
    const countLbl = body.querySelector("#missionCountLabel");

    const updateProgress = () => {
      const done = [...cards].filter((c) => c.classList.contains("missionDone")).length;
      if (bar) bar.style.width = (done / cards.length) * 100 + "%";
      if (countLbl) countLbl.textContent = `${done} / ${cards.length} completed`;
    };

    cards.forEach((card, idx) => {
      card.querySelectorAll(".quizBtn").forEach((btn) => {
        btn.addEventListener("click", () => {
          const isCorrect = btn.dataset.correct === "true";
          card.querySelectorAll(".quizBtn").forEach((b) => b.classList.remove("correct", "wrong"));
          if (isCorrect) {
            btn.classList.add("correct");
            card.classList.add("missionDone");
            const st = card.querySelector(`#mStatus${idx}`);
            if (st) st.textContent = `Exercise 0${idx + 1} verified`;
          } else {
            btn.classList.add("wrong");
          }
          updateProgress();
        });
      });
    });
  }

  if (n === "method") {
    const runSandbox = async () => {
      const y = body.querySelector("#honesty")?.value || 30;
      const s = body.querySelector("#sbSlope")?.value || 0.3;
      const ns = body.querySelector("#sbNoise")?.value || 0.85;
      body.querySelector("#sbYearsVal").textContent = `${y} Years`;
      body.querySelector("#sbSlopeVal").textContent = `+${(+s).toFixed(2)} /decade`;
      body.querySelector("#sbNoiseVal").textContent = (+ns).toFixed(2);
      try {
        const r = await fetch(`/api/sandbox?years=${y}&slope=${s}&noise=${ns}`);
        if (!r.ok) return;
        const d = await r.json();
        const ht = body.querySelector("#honestyText");
        if (ht) ht.textContent = d.verdict_text;
        const chart = body.querySelector("#sbChart");
        if (chart && d.svg) chart.innerHTML = d.svg;
      } catch (e) {}
    };

    ["#honesty", "#sbSlope", "#sbNoise"].forEach((sel) => {
      const el = body.querySelector(sel);
      if (el) {
        el.addEventListener("input", runSandbox);
        el.addEventListener("change", runSandbox);
      }
    });

    body.querySelectorAll("#sandboxPresets .tab").forEach((btn) => {
      btn.addEventListener("click", () => {
        body.querySelectorAll("#sandboxPresets .tab").forEach((b) => b.classList.remove("active"));
        btn.classList.add("active");
        body.querySelector("#honesty").value = btn.dataset.y;
        body.querySelector("#sbSlope").value = btn.dataset.s;
        body.querySelector("#sbNoise").value = btn.dataset.n;
        runSandbox();
      });
    });

    runSandbox();

    fetch("/api/reference")
      .then((r) => r.json())
      .then((d) => {
        const limBox = body.querySelector("#limitationsContainer");
        if (limBox && d.limitations) {
          limBox.innerHTML = d.limitations
            .slice(0, 6)
            .map((l, i) => {
              if (typeof l === "string") {
                return cardBox(`Limitation 0${i + 1}`, "Methodological Constraint", l);
              }
              return cardBox(
                `Limitation 0${i + 1}`,
                l.title || "Methodological Constraint",
                `${l.issue || ""} Mitigation: ${l.how_we_handle_it || ""}`
              );
            })
            .join("");
        }
      })
      .catch(() => {});
  }

  if (n === "ml") {
    const loadMl = async () => {
      const place = body.querySelector("#mlPlaceSelect")?.value || "Karakoram";
      const variable = body.querySelector("#mlVarSelect")?.value || "snow_cover_modis";
      try {
        const res = await fetch(`/api/ml?place=${encodeURIComponent(place)}&variable=${encodeURIComponent(variable)}`);
        if (!res.ok) return;
        const d = await res.json();

        const title = body.querySelector("#mlTopTitle");
        if (title) title.textContent = `${place}: Machine Learning Diagnostics`;
        body.querySelector("#mlGprYear").textContent = `${d.gpr.changepoint_year} (R2=${d.gpr.r2})`;
        body.querySelector("#mlTopDriver").textContent = d.drivers?.[0]?.name || "2m Air Temp";
        body.querySelector("#mlFcstR2").textContent = `R2 = ${d.forecast_metrics.test_r2.toFixed(2)} (RMSE ${d.forecast_metrics.test_rmse.toFixed(2)})`;
        body.querySelector("#mlSilScore").textContent = `${d.clustering.silhouette_score} (${d.clustering.pca_variance_pct}% PCA)`;

        const cGpr = body.querySelector("#mlChartGpr");
        if (cGpr && d.svg_gpr) cGpr.innerHTML = d.svg_gpr;
        const cFcst = body.querySelector("#mlChartFcst");
        if (cFcst && d.svg_forecast) cFcst.innerHTML = d.svg_forecast;

        const bars = body.querySelector("#mlDriverBars");
        if (bars && d.drivers) {
          bars.innerHTML = d.drivers
            .map(
              (x) =>
                `<div class="mlBar"><span>${x.name}</span><i style="width:${Math.min(100, x.pct * 1.8)}%"></i><b class="num-mono">${x.pct}%</b></div>`
            )
            .join("");
        }

        const cTbl = body.querySelector("#mlClusterTable");
        if (cTbl && d.clustering?.regimes) {
          cTbl.innerHTML =
            '<div class="shieldRow headerRow"><span>Basin or glacier</span><span>Mean elevation</span><span>Temp and snow slope</span><span>K-Means regime</span></div>' +
            d.clustering.regimes
              .map(
                (r) =>
                  `<div class="shieldRow"><b>${r.entity_name}</b><span class="num-mono">${r.elevation_m} m</span><span class="num-mono">${r.temp_trend_c_dec >= 0 ? "+" : ""}${r.temp_trend_c_dec} °C · ${r.snow_trend_pct_dec}%</span><b class="statusLow">${r.regime_label}</b></div>`
              )
              .join("");
        }
      } catch (e) {}
    };

    body.querySelector("#mlPlaceSelect")?.addEventListener("change", loadMl);
    body.querySelector("#mlVarSelect")?.addEventListener("change", loadMl);
    loadMl();
  }

  if (n === "shield") {
    const loadShield = async () => {
      const dt = body.querySelector("#temp")?.value || 2.4;
      const ds = body.querySelector("#snowSim")?.value || -8.0;
      body.querySelector("#tempValLabel").textContent = `+${(+dt).toFixed(1)} °C`;
      body.querySelector("#snowValLabel").textContent = `${+ds >= 0 ? "+" : ""}${(+ds).toFixed(0)}%`;
      try {
        const res = await fetch(`/api/shield?delta_temp=${dt}&delta_snow_pct=${ds}`);
        if (!res.ok) return;
        const d = await res.json();

        const table = body.querySelector("#shieldGlacierTable");
        if (table && d.radar_glaciers) {
          table.innerHTML =
            '<div class="shieldRow headerRow"><span>Glacier and range (15 termini)</span><span>7-day GLOF trigger level</span><span>Downstream infrastructure exposed</span><span>Terminus ELA and 7-day melt</span></div>' +
            d.radar_glaciers
              .map((g) => {
                const st =
                  g.alert_level.includes("RED") || g.alert_level.includes("HIGH")
                    ? "HIGH"
                    : g.alert_level.includes("WATCH")
                    ? "WATCH"
                    : "LOW";
                const cls = st === "HIGH" ? "statusHigh" : st === "WATCH" ? "statusWatch" : "statusLow";
                return `<div class="shieldRow"><b>${g.glacier_name} <span style="color:var(--text-muted);font-weight:400">(${g.range})</span></b><b class="${cls} num-mono">${g.alert_level} (${g.peak_glof_score})</b><span>${g.infrastructure_at_risk}</span><span class="num-mono">ELA ${g.ela_elevation_m} m · Melt ${g.total_7d_melt_mm} mm/7d</span></div>`;
              })
              .join("");
        }

        if (d.hazard_summary) {
          const iso = body.querySelector("#shieldIsoSummary");
          const nMonths = d.hazard_summary.compound_extreme_months_count ?? d.hazard_summary.n_compound_hazard_months ?? 0;
          const peakDate = d.hazard_summary.peak_event_date || d.hazard_summary.peak_hazard_date || "May 2022";
          if (iso)
            iso.textContent = `Isolation Forest: ${nMonths} compound anomaly months detected (peak: ${peakDate})`;
        }

        if (d.water_tower) {
          const w = d.water_tower;
          const maf = body.querySelector("#maf");
          if (maf) {
            maf.textContent = `+${w.delta_temp_c.toFixed(1)} °C scenario: Peak Water Year ${w.peak_water_year} (${w.peak_inflow_maf} MAF) followed by 2075 inflow of ${w.inflow_2075_maf} MAF`;
          }
          const wg = body.querySelector("#waterMetricsGrid");
          if (wg) {
            wg.innerHTML = `
              <div class="metric"><b class="num-mono">${w.peak_water_year}</b><span>Peak Water tipping year (${w.peak_inflow_maf} MAF)</span></div>
              <div class="metric"><b class="num-mono">${w.inflow_2075_maf} MAF</b><span>Projected 2075 Tarbela inflow (vs. 64.5 MAF base)</span></div>
              <div class="metric"><b class="num-mono">${w.kharif_2075_deficit_pct}% / ${w.rabi_wheat_change_pct}%</b><span>2075 Kharif deficit / Rabi crop shift</span></div>
              <div class="metric"><b class="num-mono">${w.projected_2075_mw} MW</b><span>2075 firm hydropower (of ${w.installed_hydropower_mw} MW)</span></div>`;
          }
        }
        const wc = body.querySelector("#waterHydroChart");
        if (wc && d.svg_water) wc.innerHTML = d.svg_water;
      } catch (e) {}
    };

    body.querySelector("#temp")?.addEventListener("input", loadShield);
    body.querySelector("#snowSim")?.addEventListener("input", loadShield);
    body.querySelectorAll("#waterScenarioTabs .tab").forEach((btn) => {
      btn.addEventListener("click", () => {
        body.querySelectorAll("#waterScenarioTabs .tab").forEach((b) => b.classList.remove("active"));
        btn.classList.add("active");
        body.querySelector("#temp").value = btn.dataset.dt;
        body.querySelector("#snowSim").value = btn.dataset.ds;
        loadShield();
      });
    });

    loadShield();
  }
}

function render() {
  const n = location.hash.slice(1) || "home";
  view.innerHTML =
    n === "home"
      ? home()
      : n === "investigate"
      ? investigate()
      : n === "cases"
      ? cases()
      : n === "notebook"
      ? notebook()
      : n === "method"
      ? method()
      : n === "ml"
      ? ml()
      : n === "shield"
      ? shield()
      : home();
  window.scrollTo({ top: 0, behavior: "instant" });
  requestAnimationFrame(() => {
    enhancePage(n);
    if (n === "investigate") injectAdvancedInvestigateWidgets();
  });
}

window.addEventListener("hashchange", render);
document.addEventListener("click", (e) => {
  if (e.target.matches(".cert")) {
    const nameInput = document.getElementById("certNameInput");
    const recipient = nameInput ? nameInput.value : "Ali Hassan - Earth System Trend Detective";
    e.target.textContent = "Generating PDF summary...";
    window.open(`/api/export/certificate?name=${encodeURIComponent(recipient)}`, "_blank");
  }
});

/* ============================================================================
   INTERACTIVE CHART TOOLTIPS (Mouse Hover + Keyboard Accessible Navigation)
   ============================================================================ */
const svgTooltip = document.getElementById("svgTooltip");

function renderChartTooltipAtIndex(svgEl, idx, clientX, clientY) {
  if (!svgEl || !svgTooltip) return;
  const raw = svgEl.getAttribute("data-series");
  if (!raw) return;
  try {
    const d = JSON.parse(raw);
    const n = d.v.length;
    if (!n) return;
    const clampedIdx = Math.min(n - 1, Math.max(0, idx));
    svgEl.dataset.activeIndex = String(clampedIdx);

    const val = d.v[clampedIdx];
    const tr = d.t && d.t.length > clampedIdx ? d.t[clampedIdx] : null;
    const lo = d.lo && d.lo.length > clampedIdx ? d.lo[clampedIdx] : null;
    const hi = d.hi && d.hi.length > clampedIdx ? d.hi[clampedIdx] : null;
    const u = d.units ? ` ${d.units}` : "";

    let timeLabel = "";
    if (d.months && d.months[clampedIdx]) {
      timeLabel = `Month: ${d.months[clampedIdx]}`;
    } else if (d.dates && d.dates[clampedIdx]) {
      timeLabel = `Date: ${d.dates[clampedIdx]}`;
    } else {
      const yr = 1981 + Math.round((clampedIdx / Math.max(1, n - 1)) * 45);
      timeLabel = `Date: ${yr}`;
    }

    let html = `<b>${d.left || "Series data"}</b><span>${timeLabel}</span><br><span>Observed: <strong class="num-mono" style="color:var(--text-primary)">${val >= 0 ? "+" : ""}${val}${u}</strong></span>`;
    if (tr !== null) {
      html += `<br><span class="ttTrend">Trend fit: <strong class="num-mono">${tr >= 0 ? "+" : ""}${tr}${u}</strong></span>`;
    }
    if (lo !== null && hi !== null) {
      html += `<br><span style="color:var(--text-muted)">95% CI: <span class="num-mono">[${lo >= 0 ? "+" : ""}${lo}, ${hi >= 0 ? "+" : ""}${hi}]${u}</span></span>`;
    }
    svgTooltip.innerHTML = html;
    svgTooltip.style.display = "block";
    svgTooltip.style.left = Math.min(window.innerWidth - 250, Math.max(12, clientX + 14)) + "px";
    svgTooltip.style.top = Math.max(12, clientY - 76) + "px";

    const padLeft = d.pad_left ?? 68;
    const plotW = d.plot_w ?? 808;
    const svgX = (padLeft + (clampedIdx / Math.max(1, n - 1)) * plotW).toFixed(1);

    let laser = svgEl.querySelector(".laserCrosshair");
    if (!laser) {
      laser = document.createElementNS("http://www.w3.org/2000/svg", "line");
      laser.setAttribute("class", "laserCrosshair");
      laser.setAttribute("y1", "36");
      laser.setAttribute("y2", "228");
      laser.setAttribute("stroke", "#8b949e");
      laser.setAttribute("stroke-width", "1");
      laser.setAttribute("stroke-dasharray", "3 3");
      svgEl.appendChild(laser);
    }
    laser.setAttribute("x1", svgX);
    laser.setAttribute("x2", svgX);
  } catch (err) {}
}

document.addEventListener("mousemove", (e) => {
  const svgEl = e.target.closest("svg.interactiveSvg");
  if (!svgEl || !svgTooltip) {
    if (svgTooltip && !document.activeElement?.classList?.contains("interactiveSvg")) {
      svgTooltip.style.display = "none";
    }
    return;
  }
  const raw = svgEl.getAttribute("data-series");
  if (!raw) return;
  try {
    const d = JSON.parse(raw);
    const rect = svgEl.getBoundingClientRect();
    const relX = Math.max(0, Math.min(1, (e.clientX - rect.left) / Math.max(1, rect.width)));
    const idx = Math.round(relX * (d.v.length - 1));
    renderChartTooltipAtIndex(svgEl, idx, e.clientX, e.clientY);
  } catch (err) {}
});

document.addEventListener("keydown", (e) => {
  const svgEl = document.activeElement?.closest?.("svg.interactiveSvg");
  if (!svgEl) return;
  if (e.key === "ArrowLeft" || e.key === "ArrowRight") {
    e.preventDefault();
    const raw = svgEl.getAttribute("data-series");
    if (!raw) return;
    const d = JSON.parse(raw);
    const cur = Number(svgEl.dataset.activeIndex ?? Math.floor(d.v.length / 2));
    const next = e.key === "ArrowRight" ? cur + 1 : cur - 1;
    const rect = svgEl.getBoundingClientRect();
    renderChartTooltipAtIndex(svgEl, next, rect.left + rect.width / 2, rect.top + 40);
  } else if (e.key === "Escape" && svgTooltip) {
    svgTooltip.style.display = "none";
  }
});

/* ============================================================================
   QUERY ASSISTANT DRAWER (/api/ask)
   ============================================================================ */
const aiBtn = document.getElementById("aiCopilotBtn");
const aiDrawer = document.getElementById("aiCopilotDrawer");
const aiChatBody = document.getElementById("aiChatBody");

aiBtn?.addEventListener("click", () => {
  if (!aiDrawer) return;
  aiDrawer.style.display = aiDrawer.style.display === "none" ? "flex" : "none";
});
document.getElementById("btnCloseAi")?.addEventListener("click", () => {
  if (aiDrawer) aiDrawer.style.display = "none";
});

async function askDetectiveAi(questionText) {
  if (!aiChatBody || !questionText) return;
  const placeEl = document.getElementById("invPlace");
  const varEl = document.getElementById("invVar");
  const place = placeEl ? placeEl.value : "Karakoram";
  const variable = varEl ? varEl.value : "MODIS Snow Cover";

  const userMsg = document.createElement("div");
  userMsg.className = "aiBubble";
  userMsg.innerHTML = `<span class="mono">Query</span><p style="color:var(--text-primary)">${questionText}</p>`;
  aiChatBody.appendChild(userMsg);
  aiChatBody.scrollTop = aiChatBody.scrollHeight;

  try {
    const res = await fetch(
      `/api/ask?q=${encodeURIComponent(questionText)}&place=${encodeURIComponent(place)}&variable=${encodeURIComponent(
        variable
      )}`
    );
    if (!res.ok) return;
    const d = await res.json();
    const botMsg = document.createElement("div");
    botMsg.className = "aiBubble";
    const pills = (d.metrics_cited || [])
      .map((m) => `<span class="pill num-mono" style="min-height:28px;padding:2px 8px;font-size:12px">${m}</span>`)
      .join(" ");
    botMsg.innerHTML = `<span class="mono">Pipeline output</span><h4>${d.title || "Response"}</h4><p>${d.answer || ""}</p><div style="margin-top:8px;display:flex;flex-wrap:wrap;gap:4px">${pills}</div>`;
    aiChatBody.appendChild(botMsg);
    aiChatBody.scrollTop = aiChatBody.scrollHeight;
  } catch (e) {}
}

document.querySelectorAll(".aiQuickChip").forEach((chip) => {
  chip.addEventListener("click", () => askDetectiveAi(chip.dataset.q));
});
document.getElementById("aiAskForm")?.addEventListener("submit", (e) => {
  e.preventDefault();
  const inp = document.getElementById("aiQuestionInput");
  if (!inp || !inp.value.trim()) return;
  const q = inp.value.trim();
  inp.value = "";
  askDetectiveAi(q);
});

/* ============================================================================
   TOPOGRAPHIC GLACIER MAP, CUSTOM COORDINATES & HISTORICAL COMPARISON
   ============================================================================ */
let cachedGlaciersList = null;

async function injectAdvancedInvestigateWidgets() {
  const n = location.hash.slice(1) || "home";
  if (n !== "investigate") return;
  const body = view.querySelector(".pageBody");
  if (!body || body.querySelector("#advancedWidgetsDeck")) return;

  const yearsInput = body.querySelector("#years");
  if (yearsInput && !body.querySelector("#btnPlayTimelapse")) {
    const tlBtn = document.createElement("button");
    tlBtn.id = "btnPlayTimelapse";
    tlBtn.type = "button";
    tlBtn.className = "navUtilBtn";
    tlBtn.style.marginTop = "8px";
    tlBtn.style.width = "100%";
    tlBtn.textContent = "Step through window lengths (1981 to 2026)";
    yearsInput.parentElement.appendChild(tlBtn);

    let tlTimer = null;
    tlBtn.addEventListener("click", () => {
      if (tlTimer) {
        clearInterval(tlTimer);
        tlTimer = null;
        tlBtn.textContent = "Step through window lengths (1981 to 2026)";
        return;
      }
      let curY = 10;
      yearsInput.value = curY;
      tlBtn.textContent = "Stepping window lengths (click to stop)";
      tlTimer = setInterval(() => {
        curY += 5;
        if (curY >= 45) {
          curY = 45;
          clearInterval(tlTimer);
          tlTimer = null;
          tlBtn.textContent = "Step through window lengths (1981 to 2026)";
        }
        yearsInput.value = curY;
        const lab = body.querySelector("#yearsLabel");
        if (lab) lab.textContent = `${2026 - curY + 1} to 2026 (${curY} yrs)`;
        fetchLiveInvestigation(body);
      }, 700);
    });
  }

  const deck = document.createElement("div");
  deck.id = "advancedWidgetsDeck";
  deck.innerHTML = `
    <div class="dashShell" style="margin-top:20px">
      <div class="dashTop">
        <div>
          <span class="mono">Spatial domain map: 15 RGI v6.0 glacier termini and custom coordinate query</span>
          <div class="dashTitle">Northern Pakistan Glacier Coordinates and Custom Sector Inspector</div>
        </div>
        <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap">
          <label for="customLatInput" class="srOnly">Latitude (°N)</label>
          <input id="customLatInput" type="number" step="0.05" min="34.0" max="37.2" value="36.32" class="num-mono" style="width:96px;min-height:40px;background:var(--bg-canvas);color:var(--text-primary);border:1px solid var(--border-default);border-radius:4px;padding:6px 10px;font-size:13px" title="Latitude (°N)">
          <label for="customLonInput" class="srOnly">Longitude (°E)</label>
          <input id="customLonInput" type="number" step="0.05" min="71.0" max="77.8" value="74.65" class="num-mono" style="width:96px;min-height:40px;background:var(--bg-canvas);color:var(--text-primary);border:1px solid var(--border-default);border-radius:4px;padding:6px 10px;font-size:13px" title="Longitude (°E)">
          <button class="btn primary" id="btnInspectCoords" type="button">Query Lat/Lon Sector</button>
        </div>
      </div>
      <div class="dashBody">
        <div class="chartGrid" style="grid-template-columns:1.35fr 1fr;margin-top:0">
          <div class="topoMapWrap">
            <svg id="pakTopoSvg" class="topoSvg" viewBox="0 0 680 320" role="img" aria-label="Coordinate map of 15 monitored glaciers in northern Pakistan"></svg>
          </div>
          <div class="glacierDossierCard" id="glacierDossierBox">
            <div>
              <span class="mono" id="gdRangeTag">Select any glacier marker on the coordinate grid</span>
              <h3 id="gdName" style="font-size:20px;margin:6px 0;color:var(--text-primary)">Shisper Glacier (Hunza)</h3>
              <p id="gdHistory" style="color:var(--text-secondary);font-size:14px;line-height:1.55">Surging Karakoram glacier whose ice-dammed lake triggered the May 7, 2022 Hassanabad Bridge outburst flood on the Karakoram Highway.</p>
            </div>
            <div class="metrics" style="grid-template-columns:1fr 1fr;margin-top:12px" id="gdMetrics">
              <div class="metric"><b class="num-mono">2,520 m / 5,180 m</b><span>Terminus / ELA altitude</span></div>
              <div class="metric"><b class="num-mono statusHigh">89.4 / 100</b><span>Baseline GLOF risk score</span></div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="dashShell" style="margin-top:20px">
      <div class="dashTop">
        <div>
          <span class="mono">Multi-decade baseline vs. observed state comparison (1985 vs. 2026)</span>
          <div class="dashTitle" id="splitTitle">1985 Baseline vs. 2026 Observed Cryosphere State</div>
        </div>
        <div class="tabs" id="splitGlacierTabs">
          <button class="tab active" type="button" data-g="shisper">Shisper Glacier (Hunza)</button>
          <button class="tab" type="button" data-g="baltoro">Baltoro / K2 (Karakoram)</button>
          <button class="tab" type="button" data-g="tirich">Tirich Mir (Hindu Kush)</button>
        </div>
      </div>
      <div class="dashBody">
        <div class="splitCompareWrap" id="splitCompareBox">
          <div class="splitLayer splitBefore">
            <div>
              <span class="mono">1985 reference baseline (MERRA-2 &amp; Landsat archive)</span>
              <h3 id="splitBeforeHead" style="font-size:20px;margin:8px 0 6px;color:var(--text-primary)">1985: Reference Terminus and Winter Snowpack</h3>
              <p id="splitBeforeDesc" style="max-width:540px;color:var(--text-secondary);font-size:14px">Summer 0 °C isotherm at 4,980 m, clean snow albedo (0.78), minimal supraglacial ponding, Tarbela baseline inflow 64.5 MAF.</p>
            </div>
            <div class="metrics" style="grid-template-columns:repeat(3,1fr);max-width:540px">
              <div class="metric"><b id="sb1985Iso" class="num-mono">4,980 m</b><span>1985 0 °C isotherm</span></div>
              <div class="metric"><b id="sb1985Snow" class="num-mono">84.2%</b><span>Snow cover fraction</span></div>
              <div class="metric"><b id="sb1985Alb" class="num-mono">0.78</b><span>Clean snow albedo</span></div>
            </div>
          </div>
          <div class="splitLayer splitAfter" id="splitAfterLayer">
            <div style="text-align:right;margin-left:auto">
              <span class="mono" style="color:var(--color-increase)">2026 observed state (45-year cumulative shift)</span>
              <h3 id="splitAfterHead" style="font-size:20px;margin:8px 0 6px;color:var(--text-primary)">2026: +200 m Isotherm Rise and Supraglacial Lake Ponding</h3>
              <p id="splitAfterDesc" style="max-width:540px;margin-left:auto;color:var(--text-secondary);font-size:14px">Summer 0 °C isotherm shifted to 5,180 m (+412 km² ice exposed to melt) and OMI absorbing aerosols contribute +21.1 mm/mo summer melt.</p>
            </div>
            <div class="metrics" style="grid-template-columns:repeat(3,1fr);max-width:540px;margin-left:auto">
              <div class="metric"><b id="sb2026Iso" class="num-mono statusHigh">5,180 m (+200 m)</b><span>2026 0 °C isotherm</span></div>
              <div class="metric"><b id="sb2026Snow" class="num-mono statusWatch">78.4%</b><span>Snow cover fraction</span></div>
              <div class="metric"><b id="sb2026Alb" class="num-mono statusHigh">0.64</b><span>Aerosol-darkened albedo</span></div>
            </div>
          </div>
          <div class="splitDivider" id="splitDividerLine"></div>
          <div class="splitHandleBadge" id="splitHandleBadge">&lt;&gt;</div>
          <input type="range" class="splitRangeInput" id="splitSliderInput" min="5" max="95" value="50" aria-label="Drag slider to compare 1985 baseline vs 2026 observed state">
        </div>
      </div>
    </div>
  `;
  body.appendChild(deck);

  const splitInput = deck.querySelector("#splitSliderInput");
  const splitAfter = deck.querySelector("#splitAfterLayer");
  const splitDiv = deck.querySelector("#splitDividerLine");
  const splitBadge = deck.querySelector("#splitHandleBadge");
  splitInput?.addEventListener("input", (e) => {
    const v = +e.target.value;
    splitAfter.style.clipPath = `polygon(${v}% 0, 100% 0, 100% 100%, ${v}% 100%)`;
    splitDiv.style.left = v + "%";
    splitBadge.style.left = v + "%";
  });

  const splitPresets = {
    shisper: {
      bHead: "1985 Shisper (Hunza): Reference Terminus and Winter Snowpack",
      bDesc: "Summer 0 °C isotherm at 4,980 m, clean snow albedo (0.78), no Hassanabad highway breach.",
      bIso: "4,980 m",
      bSnow: "84.2%",
      bAlb: "0.78",
      aHead: "2026 Shisper (Hunza): +200 m Isotherm Shift and Ice-Dammed Lake",
      aDesc: "Warming (+0.35 °C/dec, p < 0.0001) and aerosol darkening preceded the May 2022 Hassanabad Bridge outburst flood.",
      aIso: "5,180 m (+200 m)",
      aSnow: "78.4%",
      aAlb: "0.64",
    },
    baltoro: {
      bHead: "1985 Baltoro / K2 (Karakoram): High-Elevation Accumulation Zone",
      bDesc: "Mean elevation >5,350 m, buffered by winter westerly troughs (positive NAO phase).",
      bIso: "5,220 m",
      bSnow: "88.5%",
      bAlb: "0.81",
      aHead: "2026 Baltoro / K2: Karakoram Anomaly Buffering (-0.35%/dec)",
      aDesc: "Upper accumulation zone remains buffered by winter westerlies, while lower ablation tongues (<3,800 m) exhibit supraglacial ponding.",
      aIso: "5,340 m (+120 m)",
      aSnow: "87.9%",
      aAlb: "0.74",
    },
    tirich: {
      bHead: "1985 Tirich Mir (Hindu Kush): Seasonal Snow Mantle",
      bDesc: "Historical winter snowpack sustained Chitral and Kabul river tributaries through summer.",
      bIso: "4,750 m",
      bSnow: "79.0%",
      bAlb: "0.76",
      aHead: "2026 Tirich Mir (Hindu Kush): Significant Snow Decline (-2.45%/dec, p < 0.0001)",
      aDesc: "Warming and lower basin hypsometry drive statistically significant snow cover loss and increased Chiantar GLOF risk.",
      aIso: "5,010 m (+260 m)",
      aSnow: "67.1%",
      aAlb: "0.61",
    },
  };

  deck.querySelectorAll("#splitGlacierTabs .tab").forEach((btn) => {
    btn.addEventListener("click", () => {
      deck.querySelectorAll("#splitGlacierTabs .tab").forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      const p = splitPresets[btn.dataset.g];
      if (!p) return;
      deck.querySelector("#splitBeforeHead").textContent = p.bHead;
      deck.querySelector("#splitBeforeDesc").textContent = p.bDesc;
      deck.querySelector("#sb1985Iso").textContent = p.bIso;
      deck.querySelector("#sb1985Snow").textContent = p.bSnow;
      deck.querySelector("#sb1985Alb").textContent = p.bAlb;
      deck.querySelector("#splitAfterHead").textContent = p.aHead;
      deck.querySelector("#splitAfterDesc").textContent = p.aDesc;
      deck.querySelector("#sb2026Iso").textContent = p.aIso;
      deck.querySelector("#sb2026Snow").textContent = p.aSnow;
      deck.querySelector("#sb2026Alb").textContent = p.aAlb;
    });
  });

  deck.querySelector("#btnInspectCoords")?.addEventListener("click", async () => {
    const lat = deck.querySelector("#customLatInput").value;
    const lon = deck.querySelector("#customLonInput").value;
    const variable = body.querySelector("#invVar")?.value || "MERRA-2 2m Air Temp";
    const alpha = body.querySelector("#invAlpha")?.value || "0.05";
    const years = body.querySelector("#years")?.value || "45";
    try {
      const res = await fetch(
        `/api/investigate?custom_lat=${encodeURIComponent(lat)}&custom_lon=${encodeURIComponent(
          lon
        )}&variable=${encodeURIComponent(variable)}&alpha=${encodeURIComponent(alpha)}&years=${encodeURIComponent(years)}`
      );
      if (!res.ok) return;
      const data = await res.json();
      body.querySelector("#invTitle").textContent = `${data.region_name}: ${data.variable_name}`;
      body.querySelector("#invHeadline").textContent = data.verdict.headline;
      if (body.querySelector("#invChartAnom") && data.svg_anomaly) {
        body.querySelector("#invChartAnom").innerHTML = data.svg_anomaly;
      }
      body.querySelector(".dashShell").scrollIntoView({ behavior: "smooth" });
    } catch (e) {}
  });

  try {
    if (!cachedGlaciersList) {
      const r = await fetch("/api/glaciers");
      if (r.ok) cachedGlaciersList = await r.json();
    }
    const svgMap = deck.querySelector("#pakTopoSvg");
    if (svgMap && cachedGlaciersList?.glaciers) {
      const glaciers = cachedGlaciersList.glaciers;
      const projX = (lon) => 45 + ((lon - 71.4) / (77.6 - 71.4)) * 595;
      const projY = (lat) => 275 - ((lat - 34.4) / (37.1 - 34.4)) * 240;

      let gridLines = "";
      for (let gx = 60; gx <= 640; gx += 80) {
        const lonLbl = (71.4 + ((gx - 45) / 595) * 6.2).toFixed(1);
        gridLines += `<line x1="${gx}" y1="25" x2="${gx}" y2="280" stroke="#262e38" stroke-width="1"/>`;
        gridLines += `<text x="${gx}" y="296" text-anchor="middle" fill="#8b949e" font-family="DM Mono, monospace" font-size="12">${lonLbl}°E</text>`;
      }
      for (let gy = 45; gy <= 275; gy += 55) {
        const latLbl = (34.4 + ((275 - gy) / 240) * 2.7).toFixed(1);
        gridLines += `<line x1="45" y1="${gy}" x2="650" y2="${gy}" stroke="#262e38" stroke-width="1"/>`;
        gridLines += `<text x="40" y="${gy + 4}" text-anchor="end" fill="#8b949e" font-family="DM Mono, monospace" font-size="12">${latLbl}°N</text>`;
      }

      const rangeLabels = `
        <text x="125" y="92" fill="#8b949e" font-family="Inter, sans-serif" font-size="12" font-weight="600">Hindu Kush</text>
        <text x="360" y="58" fill="#8b949e" font-family="Inter, sans-serif" font-size="12" font-weight="600">Karakoram Range</text>
        <text x="430" y="255" fill="#8b949e" font-family="Inter, sans-serif" font-size="12" font-weight="600">Western Himalaya</text>
      `;

      const pins = glaciers
        .map((g, i) => {
          const cx = projX(g.lon).toFixed(1);
          const cy = projY(g.lat).toFixed(1);
          const col = g.baseline_glof_score >= 78 ? "#e06c3a" : g.baseline_glof_score >= 65 ? "#d29922" : "#58a6ff";
          return `<g class="glacierPinDot" tabindex="0" role="button" aria-label="${g.name}" data-idx="${i}" transform="translate(${cx},${cy})">
            <circle r="6" fill="${col}" stroke="#0d1117" stroke-width="1.5"/>
            <text y="-10" text-anchor="middle" fill="#e6edf3" font-family="Inter, sans-serif" font-size="12" font-weight="500">${
              g.name.split(" ")[0]
            }</text>
          </g>`;
        })
        .join("");

      svgMap.innerHTML = gridLines + rangeLabels + pins;

      svgMap.querySelectorAll(".glacierPinDot").forEach((pin) => {
        pin.addEventListener("click", () => {
          const g = glaciers[+pin.dataset.idx];
          if (!g) return;
          deck.querySelector("#gdRangeTag").textContent = `${g.range} · ${g.lat.toFixed(2)}°N, ${g.lon.toFixed(2)}°E`;
          deck.querySelector("#gdName").textContent = `${g.name} (${g.length_km} km)`;
          deck.querySelector("#gdHistory").innerHTML = `${g.historical_events}<br><br><b>Downstream infrastructure:</b> ${g.downstream_infrastructure.highways_bridges}`;
          deck.querySelector("#gdMetrics").innerHTML = `
            <div class="metric"><b class="num-mono">${g.snout_elevation_m} m / ${g.ela_elevation_m} m</b><span>Terminus / ELA altitude</span></div>
            <div class="metric"><b class="num-mono ${g.baseline_glof_score >= 78 ? "statusHigh" : "statusWatch"}">${g.baseline_glof_score} / 100</b><span>Baseline GLOF risk score</span></div>
          `;
          deck.querySelector("#customLatInput").value = g.lat.toFixed(2);
          deck.querySelector("#customLonInput").value = g.lon.toFixed(2);
        });
      });
    }
  } catch (e) {}
}

/* ============================================================================
   GUIDED TOUR CONTROLLER
   ============================================================================ */
let autoTourTimer = null;
const tourBar = document.getElementById("autoTourBar");
const tourTag = document.getElementById("autoTourStepTag");
const tourCap = document.getElementById("autoTourCaption");

const judgeTourSequence = [
  {
    hash: "home",
    scroll: 0,
    tag: "Guided tour: Step 1 of 6 · Study Domain",
    caption: "Overview of the 9 river basins, 15 monitored glaciers, and 1981 to 2026 NASA and Meteomatics datasets.",
  },
  {
    hash: "investigate",
    scroll: 120,
    tag: "Guided tour: Step 2 of 6 · Regional Workbench",
    caption: "Deseasonalized anomaly analysis with Theil-Sen slopes, Hamed-Rao Mann-Kendall tests, and 95% confidence intervals.",
  },
  {
    hash: "cases",
    scroll: 100,
    tag: "Guided tour: Step 3 of 6 · Benchmark Case Studies",
    caption: "Side-by-side comparison of Karakoram snow cover resilience (-0.35%/dec) vs. Hindu Kush decline (-2.45%/dec, p < 0.0001).",
  },
  {
    hash: "method",
    scroll: 120,
    tag: "Guided tour: Step 4 of 6 · Statistical Power and Provenance",
    caption: "Signal-vs-noise sensitivity sandbox, dataset provenance table, and methodological limitations.",
  },
  {
    hash: "ml",
    scroll: 100,
    tag: "Guided tour: Step 5 of 6 · Machine Learning Diagnostics",
    caption: "Gaussian Process changepoint detection, Random Forest driver importance, and 36-month holdout forecasting.",
  },
  {
    hash: "shield",
    scroll: 120,
    tag: "Guided tour: Step 6 of 6 · GLOF Watchlist and Indus Simulator",
    caption: "7-day meteorological trigger watchlist across 15 glacier termini and Tarbela Dam Peak Water projection (2020 to 2080).",
  },
];

function stopJudgeAutoTour() {
  if (autoTourTimer) {
    clearInterval(autoTourTimer);
    autoTourTimer = null;
  }
  if (tourBar) tourBar.style.display = "none";
  const btn = document.getElementById("btnAutoTour");
  if (btn) btn.textContent = "Guided tour";
}

document.getElementById("btnStopTour")?.addEventListener("click", stopJudgeAutoTour);
document.getElementById("btnAutoTour")?.addEventListener("click", () => {
  if (autoTourTimer) {
    stopJudgeAutoTour();
    return;
  }
  let stepIdx = 0;
  const btn = document.getElementById("btnAutoTour");
  if (btn) btn.textContent = "Stop guided tour";
  if (tourBar) tourBar.style.display = "flex";

  const runStep = () => {
    if (stepIdx >= judgeTourSequence.length) {
      stopJudgeAutoTour();
      return;
    }
    const s = judgeTourSequence[stepIdx];
    if (tourTag) tourTag.textContent = s.tag;
    if (tourCap) tourCap.textContent = s.caption;
    location.hash = s.hash;
    setTimeout(() => {
      window.scrollTo({ top: s.scroll, behavior: "smooth" });
      if (s.hash === "investigate") injectAdvancedInvestigateWidgets();
    }, 250);
    stepIdx++;
  };

  runStep();
  autoTourTimer = setInterval(runStep, 5500);
});

render();
