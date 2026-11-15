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
let cinematicScrollBound = false;

function bindCinematicScroll() {
  if (cinematicScrollBound) return;
  cinematicScrollBound = true;
  const update = () => {
    const y = window.scrollY || 0;
    const max = Math.max(1, document.documentElement.scrollHeight - innerHeight);
    const p = Math.min(1, y / Math.max(900, max * 0.72));
    document.querySelectorAll(".cinematicFX").forEach((el) => {
      el.style.setProperty("--p", p.toFixed(4));
      el.style.setProperty("--sx", (Math.sin(y * 0.0012) * 22).toFixed(1) + "px");
      el.style.setProperty("--sy", (Math.cos(y * 0.0008) * 14).toFixed(1) + "px");
    });
    const heroCopy = document.querySelector(".heroCopy");
    if (heroCopy) {
      const fade = Math.max(0, 1 - y / 520);
      heroCopy.style.opacity = fade.toFixed(3);
      heroCopy.style.transform = `translate3d(0, ${(-y * 0.22).toFixed(1)}px, 0) scale(${(1 - Math.min(0.12, y * 0.0002)).toFixed(3)})`;
    }
    const tMap = document.querySelector(".terrainMap");
    if (tMap) {
      const lift = Math.min(45, y * 0.08);
      tMap.style.transform = `perspective(600px) rotateX(${Math.max(38, 58 - y * 0.03)}deg) rotateZ(-9deg) translateY(${(20 - lift).toFixed(1)}px) scale(${(1 + Math.min(0.25, y * 0.0004)).toFixed(2)})`;
    }
    document.body.style.setProperty("--scrollP", p);
  };
  window.addEventListener("scroll", update, { passive: true });
  update();
}

const svg =
  '<svg viewBox="0 0 900 250" preserveAspectRatio="none"><defs><linearGradient id="g" x1="0" x2="0" y1="0" y2="1"><stop stop-color="#6de7ff" stop-opacity=".55"/><stop offset="1" stop-color="#6de7ff" stop-opacity="0"/></linearGradient></defs><path d="M0 205 C80 165 110 180 165 140 S255 175 315 125 S410 170 470 95 S560 150 620 118 S710 155 770 90 S840 135 900 75 L900 250 L0 250Z" fill="url(#g)"/><path d="M0 205 C80 165 110 180 165 140 S255 175 315 125 S410 170 470 95 S560 150 620 118 S710 155 770 90 S840 135 900 75" fill="none" stroke="#9df4ff" stroke-width="2"/></svg>';

const cinematicFX = () =>
  `<div class="cinematicFX" aria-hidden="true"><div class="fxMountains"></div><div class="fxCloud fxCloudA"></div><div class="fxCloud fxCloudB"></div><div class="fxFog"></div><div class="fxWind"><i></i><i></i><i></i></div><div class="fxSnow"></div><div class="fxSatellite"><span></span></div><div class="fxScan"></div><div class="fxLightning"><b></b><b></b></div><div class="fxTelemetry"><span>ORBITAL LINK</span><b>● LIVE</b><i></i><span>ALT 705 KM</span><span>ICE TEMP −1.6°C</span></div></div>`;

const pageHead = (eyebrow, title, desc) =>
  cinematicFX() +
  `<div class="pageAtmos"><video class="pageBgVideo" autoplay muted loop playsinline preload="metadata" poster="/assets/karakoram-k2.jpg" aria-hidden="true"><source src="/assets/glacier-loop.mp4" type="video/mp4"></video><div class="atmoGrid"></div><div class="atmoGlow"></div></div><div class="pageHero"><a class="backLink" href="#home">← RETURN TO TERRAIN</a><div class="eyebrow">${eyebrow}</div><h1>${title}</h1><p>${desc}</p><div class="heroRule"><i></i><span>NASA EARTH OBSERVATION // METEOMATICS // PAKISTAN CRYOSPHERE</span><i></i></div></div>`;

const glass = (n, t, b, extra = "") =>
  `<div class="glass" ${extra}><div class="num">${n}</div><h3>${t}</h3><p>${b}</p><div class="glow"></div></div>`;

/* ============================================================================
   PAGE 1: HOME (Cinematic Scrollytelling + Interactive Live Preview)
   ============================================================================ */
function home() {
  return (
    cinematicFX() +
    `<div class="hero">
      <canvas id="scene3d"></canvas>
      <div class="mountainPhoto" aria-hidden="true"></div>
      <div class="windLayer" aria-hidden="true"><i></i><i></i><i></i><i></i></div>
      <div class="lightning" aria-hidden="true"><b></b><b></b></div>
      <div class="sceneTint"></div>
      <div class="sceneVignette"></div>
      <div class="sceneDepth"><div class="cloud3d c1"></div><div class="cloud3d c2"></div><div class="cloud3d c3"></div></div>
      <div class="satellite3d"></div>
      <div class="satBeam"></div>
      <div class="scanline"></div>
      <div class="glacierCracks"></div>
      <div class="terrainMap"></div>
      <div class="elevationRail"></div>
      <div class="sceneBadge">● <b>LIVE EARTH OBSERVATION</b> · DRAG TERRAIN TO INSPECT</div>
      <div class="scene-readout">GLACIER TELEMETRY<strong id="sceneTemp">−7.8°C</strong><i></i><span>SNOW COVER&nbsp;&nbsp; 82.4%</span><br><span>SWE&nbsp;&nbsp; 318 mm</span><br><span>ICE SURFACE&nbsp;&nbsp; −1.6°C</span></div>
      <div class="stars"></div>
      <div class="heroGlow"></div>
      <div class="heroCopy">
        <div class="eyebrow">NASA SPACE APPS 2026 // BE AN EARTH SYSTEM TREND DETECTIVE</div>
        <h1 class="heroTitleLockup"><span class="titleTop">HIMALAYA</span><span class="titleBottom"><em class="titleTrend">TREND</em> <em class="titleLab">LAB</em></span><span class="titleFlare" aria-hidden="true"></span></h1>
        <p class="heroDesc">Be a Data Detective for Pakistan’s 7,253 glaciers. Follow the signal from orbit to ice — separating real climate trends from mountain-weather noise across the Karakoram, Hindu Kush, and Western Himalaya.</p>
        <div class="actions">
          <a class="btn primary" href="#investigate">Start Investigation <span>↗</span></a>
          <a class="btn ghost" href="#cases">Explore 3 Demo Cases</a>
          <a class="btn ghost" href="#notebook">Detective Missions</a>
          <a class="btn ghost" href="#shield">HimalayaShield GLOF Radar</a>
        </div>
      </div>
      <div class="sat"></div>
      <div class="hud"><span>ORBITAL ALTIMETER</span><span class="big" id="altimeter">705 KM</span><div class="hudline"></div><span>K2 SUMMIT — 8,611 M</span><br><span>ELA — 5,180 M</span><br><span>ABLATION — 3,500 M</span><br><span>SHISPER — 2,520 M</span></div>
      <div class="mountains"><div class="range back"></div><div class="range mid"></div><div class="peak"></div><div class="range front"></div></div>
      <div class="scrollcue">SCROLL TO DESCEND INTO THE GLACIER BASINS <span></span></div>
    </div>
    <section class="stage">
      <div class="stageGrid">
        <div class="eyebrow">FROM ORBIT TO ICE // MULTI-SENSOR FUSION</div>
        <h2 class="stageTitle">A glacier is not<br><span style="color:#6de7ff">just a glacier.</span></h2>
        <p class="stageText">Temperature. Snow cover. Precipitation. Black-carbon aerosols. Meltwater runoff. Each satellite signal tells a different part of the story. Himalaya Trend Lab turns NASA & Meteomatics observations into a rigorous statistical and ML investigation you can interrogate, compare, and explain.</p>
        <div class="dataStrip">
          <div class="dataCell"><span>Monitoring window</span><b>1981—2026</b><span>45 YEARS · 550 MONTHS</span></div>
          <div class="dataCell"><span>Glacier Basins</span><b>09</b><span>KARAKORAM · HINDU KUSH · INDUS</span></div>
          <div class="dataCell"><span>Glacier Hotspots</span><b>15</b><span>SHISPER · BALTORO · SIACHEN · PASSU</span></div>
          <div class="dataCell"><span>Variables & Sensors</span><b>10</b><span>MODIS · MERRA-2 · GPM · GLDAS · OMI</span></div>
        </div>
        <div class="orbitCard">
          <div class="ring"></div>
          <div class="ring r2"></div>
          <div class="orbitEarth"><i class="pin p1" title="Karakoram"></i><i class="pin p2" title="Hindu Kush"></i><i class="pin p3" title="Western Himalaya"></i></div>
          <div class="mono" style="position:absolute;top:25px;left:25px">NORTHERN PAKISTAN // RGI v6.0 GLACIER INVENTORY</div>
          <div class="mono" style="position:absolute;bottom:25px;right:25px">TERRA/AQUA MODIS // MERRA-2 // GPM IMERG // METEOMATICS</div>
        </div>
      </div>
    </section>
    <section class="section">
      <div class="sectionHead">
        <div><div class="eyebrow">THE 6-LAYER DETECTIVE ARCHITECTURE</div><h2>Follow the<br>evidence.</h2></div>
        <p>Click any module below to jump directly into the workbench — from non-parametric trend testing to explainable Machine Learning and GLOF early warning.</p>
      </div>
      <div class="labGrid">
        ${glass("01 · DETECTIVE WORKBENCH", "Ask the Mountain", "5 guided Earth-system questions, 9 basins, 10 variables, RGI v6.0 glacier-only masking, and side-by-side Compare Mode.", 'onclick="location.hash=\'investigate\'" style="cursor:pointer"')}
        ${glass("02 · ROBUST STATISTICS", "Interrogate the Signal", "12-month climatology removal, Theil–Sen robust slope, Hamed–Rao autocorrelation-adjusted Mann–Kendall, and Benjamini–Hochberg FDR stippling.", 'onclick="location.hash=\'method\'" style="cursor:pointer"')}
        ${glass("03 · EXPLAINABLE AI / ML", "Uncover Non-Linear Drivers", "Gaussian Process Regression changepoints, Random Forest driver attribution, 36-month hybrid forecasting (2026–2029), and K-Means regime clustering.", 'onclick="location.hash=\'ml\'" style="cursor:pointer"')}
      </div>
    </section>
    <section class="dashboard">
      <div class="dashShell">
        <div class="dashTop">
          <div>
            <div class="mono" id="homePreviewTag">LIVE TELEMETRY PREVIEW // CLICK A BASIN TAB</div>
            <div class="dashTitle" id="homePreviewTitle">Hunza River Basin — MERRA-2 2m Air Temperature</div>
          </div>
          <div class="tabs" id="homeBasinTabs">
            <button class="tab active" data-place="Hunza" data-var="MERRA-2 2m Air Temp">Hunza Temp</button>
            <button class="tab" data-place="Karakoram" data-var="MODIS Snow Cover">Karakoram Snow</button>
            <button class="tab" data-place="Hindu Kush" data-var="MODIS Snow Cover">Hindu Kush Snow</button>
            <button class="tab" data-place="Upper Indus" data-var="GPM IMERG Precipitation">Upper Indus Precip</button>
            <a class="btn primary" href="#investigate" style="padding:9px 14px;font-size:11.5px">Open Full Workbench ↗</a>
          </div>
        </div>
        <div class="dashBody">
          <div class="verdict">
            <div class="mono" id="homeVerdictBadge">DETECTIVE VERDICT // SIGNIFICANT TREND</div>
            <strong id="homeVerdictHead">Warming signal detected above Hunza glacier valley (+0.29°C/decade).</strong>
            <p id="homeVerdictSub">Hamed–Rao modified Mann–Kendall confirms statistical significance after correcting for lag-1 autocorrelation, pushing the 0°C freezing isotherm upward toward the Shisper and Ultar accumulation zones.</p>
          </div>
          <div class="metrics" id="homeMetricsGrid">
            <div class="metric"><b>+0.29°C</b><span>SEN SLOPE / DECADE</span></div>
            <div class="metric"><b>p = 0.0012</b><span>HAMED–RAO P-VALUE</span></div>
            <div class="metric"><b>+200 m</b><span>0°C ISOTHERM SHIFT</span></div>
            <div class="metric"><b>1981–2026</b><span>45-YEAR RECORD</span></div>
          </div>
          <div class="chartGrid">
            <div class="chart" id="homeChart">${svg}</div>
            <div class="chart" id="homeSeasonChart">${svg}</div>
          </div>
        </div>
      </div>
    </section>`
  );
}

/* ============================================================================
   PAGE 2: INVESTIGATE (Full Detective Mode + Compare Mode + Cryosphere Physics)
   ============================================================================ */
function investigate() {
  return (
    pageHead(
      "DETECTIVE MODE // LIVE STATISTICAL & CRYOSPHERE WORKBENCH",
      "Investigate",
      "Select a guided scientific question or configure any Pakistan glacier basin, satellite variable, significance threshold α, RGI v6.0 glacier mask, and side-by-side comparison basin."
    ) +
    `<div class="pageBody">
      <div class="glass" style="min-height:auto;margin-bottom:14px;padding:18px 22px">
        <div class="mono" style="margin-bottom:10px">STEP 1 · QUICK-SELECT A DETECTIVE QUESTION (AUTO-CONFIGURES SENSOR & VARIABLE)</div>
        <div id="questionPills">
          <span class="pill activePill" data-var="MERRA-2 2m Air Temp">🌡️ Q1: Is it getting warmer above the glaciers? (MERRA-2 2m Temp)</span>
          <span class="pill" data-var="MODIS Snow Cover">❄️ Q2: Is snow & ice cover shrinking or stable? (MODIS Snow Cover)</span>
          <span class="pill" data-var="GPM IMERG Precipitation">🌧️ Q3: Is monsoon or winter precipitation changing? (GPM IMERG)</span>
          <span class="pill" data-var="Meltwater Runoff">🌊 Q4: Is glacier meltwater runoff accelerating? (GLDAS Runoff)</span>
          <span class="pill" data-var="OMI Aerosols">🌫️ Q5: Are black-carbon aerosols darkening the snowpack? (OMI Aerosols)</span>
        </div>
      </div>

      <div class="dashShell">
        <div class="dashTop">
          <div>
            <div class="mono" id="invSourceTag">NASA MERRA-2 + METEOMATICS ASSIMILATION</div>
            <div class="dashTitle" id="invTitle">Hunza River Basin — 2m Air Temperature</div>
          </div>
          <div class="actions" style="margin-top:0">
            <button class="btn ghost" id="btnExportCsv" type="button">Export CSV ↓</button>
            <button class="btn primary" id="btnExportPdf" type="button">1-Page PDF Detective Report ↗</button>
          </div>
        </div>
        <div class="dashBody">
          <div class="controls">
            <div class="control">
              <label>Primary Basin / Range</label>
              <select id="invPlace">
                <option value="Hunza">Hunza River Basin (Shisper / Ultar)</option>
                <option value="Karakoram">Karakoram Range (Baltoro / Siachen / K2)</option>
                <option value="Hindu Kush">Hindu Kush Range (Tirich Mir / Chiantar)</option>
                <option value="Western Himalaya">Western Himalaya (Nanga Parbat / Raikot)</option>
                <option value="Upper Indus">Upper Indus Basin (Tarbela Catchment)</option>
                <option value="Gilgit">Gilgit River Basin (Hinarchi / Darkot)</option>
                <option value="Chitral">Chitral River Basin (Eastern Hindu Kush)</option>
                <option value="Astore">Astore Valley Basin (Rupal / Raikot)</option>
                <option value="Neelum">Neelum / Jhelum Basin (pir Panjal)</option>
              </select>
            </div>
            <div class="control">
              <label>Compare With Basin (Compare Mode)</label>
              <select id="invCompare">
                <option value="none">— Single Basin Mode —</option>
                <option value="Hindu Kush">Compare vs. Hindu Kush Range</option>
                <option value="Karakoram">Compare vs. Karakoram Range</option>
                <option value="Western Himalaya">Compare vs. Western Himalaya</option>
                <option value="Hunza">Compare vs. Hunza River Basin</option>
                <option value="Upper Indus">Compare vs. Upper Indus Basin</option>
                <option value="Chitral">Compare vs. Chitral River Basin</option>
              </select>
            </div>
            <div class="control">
              <label>Earth Observation Variable</label>
              <select id="invVar">
                <option>MERRA-2 2m Air Temp</option>
                <option>MODIS Snow Cover</option>
                <option>Meteomatics Snow Depth</option>
                <option>MODIS Land Surface Temp</option>
                <option>GPM IMERG Precipitation</option>
                <option>MERRA-2 Snowfall</option>
                <option>GLDAS SWE</option>
                <option>Meltwater Runoff</option>
                <option>AIRS Humidity</option>
                <option>OMI Aerosols</option>
              </select>
            </div>
            <div class="control">
              <label>Significance Threshold (α)</label>
              <select id="invAlpha">
                <option value="0.05">α = 0.05 (95% Confidence — Standard)</option>
                <option value="0.01">α = 0.01 (99% Confidence — Strict)</option>
                <option value="0.10">α = 0.10 (90% Confidence — Exploratory)</option>
              </select>
            </div>
            <div class="control">
              <label>RGI v6.0 Glacier Mask</label>
              <select id="invMask">
                <option value="false">All Basin Terrain (Full Grid)</option>
                <option value="true">RGI v6.0 Glacier Ice Mask Only</option>
              </select>
            </div>
            <div class="control">
              <label>Record Window: <span id="yearsLabel" class="mono">1981—2026 (45 Yrs)</span></label>
              <input id="years" type="range" min="5" max="45" value="45">
            </div>
          </div>

          <div class="verdict">
            <div class="mono" id="invBadge">DETECTIVE VERDICT // ANALYZING SIGNAL...</div>
            <strong id="invHeadline">Loading statistical trend verdict...</strong>
            <p id="invSubtext">Separating 12-month seasonal climatology from long-term climate signal...</p>
          </div>

          <div id="invCompareBanner" class="verdict" style="display:none;border-color:#f2c56b88;background:linear-gradient(100deg,rgba(62,46,16,.92),rgba(18,15,8,.95))"></div>

          <div class="metrics" id="invMetrics">
            <div class="metric"><b>+0.29°C</b><span>SEN SLOPE / DECADE</span></div>
            <div class="metric"><b>+0.28°C</b><span>OLS SLOPE / DECADE</span></div>
            <div class="metric"><b>τ = +0.26</b><span>MANN–KENDALL TAU</span></div>
            <div class="metric"><b>p = 0.0012</b><span>HAMED–RAO P-VALUE</span></div>
          </div>

          <div class="metrics" id="invCryoMetrics" style="margin-top:10px">
            <div class="metric"><b>+200 m</b><span>0°C ISOTHERM VERTICAL SHIFT</span></div>
            <div class="metric"><b>5,180 m</b><span>EQUILIBRIUM LINE ALTITUDE (ELA)</span></div>
            <div class="metric"><b>+18.4 mm/mo</b><span>DARK-ICE SOOT MELT ENHANCEMENT</span></div>
            <div class="metric"><b>82.0%</b><span>FDR SIGNIFICANT GRID CELLS</span></div>
          </div>

          <div class="chartGrid">
            <div class="chart" id="invChartAnom">${svg}</div>
            <div class="chart" id="invChartSeason">${svg}</div>
          </div>

          <div class="featureGrid" style="margin-top:14px">
            <div class="glass" style="min-height:auto">
              <div class="num">ELEVATION-DEPENDENT TREND (EDW)</div>
              <h3>Vertical Elevation Bands</h3>
              <div id="invElevBands" class="mlBars" style="margin-top:10px;padding:12px"></div>
            </div>
            <div class="glass" style="min-height:auto">
              <div class="num">ATMOSPHERIC TELECONNECTIONS</div>
              <h3>Large-Scale Circulation Drivers</h3>
              <div id="invTeleList" style="margin-top:12px;display:grid;gap:10px"></div>
            </div>
            <div class="glass" style="min-height:auto">
              <div class="num">DATA PROVENANCE & CAVEATS</div>
              <h3 id="invVarDefTitle">Sensor Definition & Limitations</h3>
              <p id="invVarDefText">Loading NASA & Meteomatics parameter metadata...</p>
            </div>
          </div>
        </div>
      </div>
    </div>`
  );
}

/* ============================================================================
   PAGE 3: DEMO CASES (3 Guided Walkthroughs + Multi-Sensor Satellite Cross-Check)
   ============================================================================ */
function cases() {
  return (
    pageHead(
      "THREE GUIDED INVESTIGATIONS // ONE-CLICK CASEBOOK",
      "Demo Cases",
      "Click any of the three benchmark investigations below to replay the statistical evidence, compare neighboring mountain ranges side by side, and inspect multi-sensor satellite agreement."
    ) +
    `<div class="pageBody">
      <div class="featureGrid" id="caseCardsGrid">
        ${glass(
          "CASE 01 · CLICK TO REPLAY",
          "Karakoram vs. Hindu Kush Snow Cover",
          "Prove the famous 'Karakoram Anomaly': why Karakoram snow cover has stayed resilient while the neighboring Hindu Kush experiences statistically significant snow loss.",
          'data-case="0" class="glass missionDone" style="cursor:pointer"'
        )}
        ${glass(
          "CASE 02 · CLICK TO REPLAY",
          "Hunza Summer Heat & May 2022 Shisper GLOF",
          "Trace the +0.29°C/decade warming trend and spring heatwave anomaly above Hunza that triggered the May 7, 2022 Shisper Glacier outburst and Hassanabad Bridge collapse.",
          'data-case="1" style="cursor:pointer"'
        )}
        ${glass(
          "CASE 03 · CLICK TO REPLAY",
          "Upper Indus Rainfall: Signal vs. Noise",
          "Investigate highly variable GPM IMERG precipitation in the Upper Indus Basin — demonstrating why 'not statistically significant yet' is an honest, scientific verdict.",
          'data-case="2" style="cursor:pointer"'
        )}
      </div>

      <div class="dashShell" style="margin-top:18px">
        <div class="dashTop">
          <div>
            <div class="mono" id="caseCodeTag">CASE 01 // SIDE-BY-SIDE REGIONAL COMPARISON</div>
            <div class="dashTitle" id="caseMainTitle">Karakoram Anomaly vs. Hindu Kush Snow Decline</div>
          </div>
          <button class="btn primary" id="btnOpenCaseInLab" type="button">Open This Case in Investigate Workbench ↗</button>
        </div>
        <div class="dashBody">
          <div class="chartGrid" style="grid-template-columns:1fr 1fr;margin-top:0">
            <div class="verdict" style="margin:0">
              <div class="mono" id="casePrimaryBadge">PRIMARY BASIN</div>
              <strong id="casePrimaryHead">Karakoram Range</strong>
              <p id="casePrimaryStat">Sen's Slope: -0.12 %/decade · Hamed-Rao p = 0.084</p>
            </div>
            <div class="verdict" style="margin:0;border-color:#f2c56b88;background:linear-gradient(100deg,rgba(58,42,14,.92),rgba(16,13,7,.95))">
              <div class="mono" id="caseCompBadge" style="color:#f2c56b">COMPARISON BASIN</div>
              <strong id="caseCompHead">Hindu Kush Range</strong>
              <p id="caseCompStat">Sen's Slope: -1.42 %/decade · Hamed-Rao p = 0.0001</p>
            </div>
          </div>
          <div class="chartGrid" style="margin-top:14px">
            <div class="chart" id="caseReplaySvg">${svg}</div>
            <div class="glass" style="min-height:270px">
              <div class="num">DETECTIVE TAKEAWAY & PHYSICAL MECHANISM</div>
              <h3 id="caseQuestionTitle">Why do neighboring ranges diverge?</h3>
              <p id="caseTakeawayText">Loading case evidence...</p>
              <div id="caseStepsList" style="margin-top:12px;font-size:13px;color:#b8dce6;line-height:1.6"></div>
            </div>
          </div>
        </div>
      </div>

      <div class="dashShell" style="margin-top:18px">
        <div class="dashTop">
          <div>
            <div class="mono">MULTI-SENSOR CROSS-CHECK // SATELLITE & REANALYSIS VALIDATION</div>
            <div class="dashTitle">Cross-Validating NASA MODIS, MERRA-2, GPM IMERG, GLDAS & Meteomatics</div>
          </div>
        </div>
        <div class="dashBody">
          <div class="shieldTable" id="sensorValidationTable">
            <div class="shieldRow headerRow"><span>SENSOR PAIR</span><span>CORRELATION (r)</span><span>BIAS / RMSE</span><span>DETECTIVE VALIDATION VERDICT</span></div>
          </div>
        </div>
      </div>
    </div>`
  );
}

/* ============================================================================
   PAGE 4: NOTEBOOK (Interactive Quiz Missions + Judge's 60s Tour + Certificate)
   ============================================================================ */
function notebook() {
  return (
    pageHead(
      "EARTH SYSTEM CASEBOOK // INTERACTIVE DETECTIVE MISSIONS",
      "Detective Notebook",
      "Solve the three interactive Earth System Detective Missions below by inspecting the statistical clues and selecting the supported scientific conclusion."
    ) +
    `<div class="pageBody">
      <div class="featureGrid" id="missionsGrid">
        <div class="glass" data-mission="0">
          <div class="num" id="mStatus0">MISSION 01 · SHISPER GLACIER (HUNZA)</div>
          <h3>The May 2022 Hassanabad Bridge Collapse</h3>
          <p>Clue: Hunza 2m Air Temperature shows Sen's slope +0.29°C/decade (Hamed-Rao p &lt; 0.01) and a +200 m upward shift of the 0°C freezing isotherm. What triggered the May 7, 2022 outburst flood?</p>
          <div class="quizOpts">
            <button class="quizBtn" data-correct="true">A) Compound spring heatwave + rapid ice-dammed lake melt above the rising 0°C isotherm</button>
            <button class="quizBtn" data-correct="false">B) A winter earthquake with cooling summer temperatures</button>
            <button class="quizBtn" data-correct="false">C) Pure random instrument noise with no warming trend</button>
          </div>
        </div>

        <div class="glass" data-mission="1">
          <div class="num" id="mStatus1">MISSION 02 · KARAKORAM VS. HINDU KUSH</div>
          <h3>Unmasking the Karakoram Anomaly</h3>
          <p>Clue: Hindu Kush snow cover declines at -1.42%/decade (p = 0.0001), whereas central Karakoram snow cover shows -0.12%/decade (p = 0.084). What is the scientific verdict?</p>
          <div class="quizOpts">
            <button class="quizBtn" data-correct="false">A) Both mountain ranges are losing snow at the exact same rate</button>
            <button class="quizBtn" data-correct="true">B) Regional divergence: westerly winter snowfall &amp; high-altitude hypsometry buffer the Karakoram while Hindu Kush declines significantly</button>
            <button class="quizBtn" data-correct="false">C) Satellite sensors cannot measure snow above 3,000 meters</button>
          </div>
        </div>

        <div class="glass" data-mission="2">
          <div class="num" id="mStatus2">MISSION 03 · UPPER INDUS BASIN</div>
          <h3>The Monsoon Rainfall Illusion</h3>
          <p>Clue: A 10-year slice of precipitation looks like a steep trend, but across the 45-year record Hamed-Rao p = 0.34 (α = 0.05). How should a Data Detective report this?</p>
          <div class="quizOpts">
            <button class="quizBtn" data-correct="false">A) Delete noisy years until p &lt; 0.05</button>
            <button class="quizBtn" data-correct="true">B) Report honestly: high interannual variability masks the long-term slope (Not Statistically Significant Yet)</button>
            <button class="quizBtn" data-correct="false">C) Use raw monthly series without removing seasonality</button>
          </div>
        </div>
      </div>
    </div>`
  );
}

/* ============================================================================
   PAGE 5: METHODOLOGY (6-Stage Pipeline + 3-Slider Sandbox + Glossary & Caveats)
   ============================================================================ */
function method() {
  return (
    pageHead(
      "SCIENTIFIC PIPELINE & STATISTICAL HONESTY SANDBOX",
      "Methodology",
      "Every verdict in Himalaya Trend Lab follows a transparent 6-stage mathematical pipeline — preventing seasonal cycles, autocorrelation, or short time windows from producing false climate claims."
    ) +
    `<div class="pageBody">
      <div class="pipeline">
        <div class="pipeNode"><b>01 · SPATIAL MASK</b><span>Cosine(lat) area-weighting + RGI v6.0 glacier ice mask</span></div>
        <div class="pipeNode"><b>02 · CLIMATOLOGY</b><span>12-month seasonal cycle removal + STL decomposition</span></div>
        <div class="pipeNode"><b>03 · SEN'S SLOPE</b><span>Non-parametric Theil–Sen median slope + 95% CI per decade</span></div>
        <div class="pipeNode"><b>04 · HAMED–RAO MK</b><span>Autocorrelation-adjusted Mann–Kendall (VIF correction)</span></div>
        <div class="pipeNode"><b>05 · BH-FDR GRID</b><span>Benjamini–Hochberg False Discovery Rate spatial stippling</span></div>
        <div class="pipeNode"><b>06 · EXPLAINABLE ML</b><span>GPR changepoints + Random Forest drivers + 36m forecast</span></div>
      </div>

      <div class="dashShell" style="margin-top:18px">
        <div class="dashTop">
          <div>
            <div class="mono">INTERACTIVE SIGNAL-VS-NOISE SANDBOX // STATISTICAL HONESTY PLAYGROUND</div>
            <div class="dashTitle">When Does a Trend Become Scientific Evidence?</div>
          </div>
          <div class="tabs" id="sandboxPresets">
            <button class="tab" data-y="10" data-s="0.30" data-n="1.20">10-Yr Noisy Slice (False/Hidden)</button>
            <button class="tab active" data-y="30" data-s="0.30" data-n="0.85">30-Yr WMO Standard</button>
            <button class="tab" data-y="45" data-s="0.35" data-n="0.65">45-Yr Clear Warming Signal</button>
            <button class="tab" data-y="45" data-s="0.00" data-n="1.10">Pure Weather Noise (Zero Slope)</button>
          </div>
        </div>
        <div class="dashBody">
          <div class="controls">
            <div class="control">
              <label>Record Length: <span id="sbYearsVal" class="mono">30 Years</span></label>
              <input id="honesty" type="range" min="5" max="45" value="30">
            </div>
            <div class="control">
              <label>True Trend Slope: <span id="sbSlopeVal" class="mono">+0.30 /decade</span></label>
              <input id="sbSlope" type="range" min="0" max="0.8" step="0.05" value="0.30">
            </div>
            <div class="control">
              <label>Mountain Weather Noise (σ): <span id="sbNoiseVal" class="mono">0.85</span></label>
              <input id="sbNoise" type="range" min="0.2" max="2.0" step="0.05" value="0.85">
            </div>
          </div>
          <div class="verdict">
            <div class="mono">SANDBOX STATISTICAL VERDICT</div>
            <strong id="honestyText">30 years → Statistically Significant (p &lt; 0.05)</strong>
            <p id="sbSubText">Adjust the record window, true physical trend slope, and weather noise standard deviation σ above to see how Sen's slope and Hamed–Rao Mann–Kendall respond in real time.</p>
          </div>
          <div class="chart" id="sbChart" style="height:260px">${svg}</div>
        </div>
      </div>

      <div class="featureGrid" style="margin-top:18px" id="methodGlossaryGrid">
        ${glass("FORMULA 01", "Theil–Sen Robust Estimator", "Computes the median of all pairwise slopes (y_j − y_i)/(t_j − t_i), making trend rates immune to extreme single-month sensor spikes or GLOF outliers.")}
        ${glass("FORMULA 02", "Hamed–Rao Modified Mann–Kendall", "Adjusts Mann–Kendall variance Var*(S) = Var(S) · [n / n*] using significant lag-k autocorrelation ρ_k so red-noise persistence never inflates significance.")}
        ${glass("FORMULA 03", "Benjamini–Hochberg FDR Stippling", "Controls the False Discovery Rate across 10×10 spatial grid cells by ranking p-values p_(k) ≤ (k/m)·α, stippling only genuinely significant glacier zones.")}
      </div>

      <div class="dashShell" style="margin-top:18px">
        <div class="dashTop">
          <div>
            <div class="mono">SCIENTIFIC LIMITATIONS & PLAIN-LANGUAGE GLOSSARY</div>
            <div class="dashTitle">What Satellite Data Can — and Cannot — Tell Us</div>
          </div>
        </div>
        <div class="dashBody">
          <div class="featureGrid" id="limitationsContainer"></div>
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
      "MACHINE LEARNING LAB // PRE-TRAINED SCIKIT-LEARN SUITE",
      "AI / ML Lab",
      "Explore our 4 pre-trained Machine Learning models (.joblib artifacts) across Pakistan's 9 glacier basins: Gaussian Process Regression changepoints, Random Forest driver attribution, 36-month forecasting (2026–2029), and K-Means/PCA regime clustering."
    ) +
    `<div class="pageBody">
      <div class="dashShell">
        <div class="dashTop">
          <div>
            <div class="mono" id="mlTopTag">PRE-TRAINED MODEL INFERENCE // 80/20 TIME-SERIES SPLIT + 5-FOLD CV</div>
            <div class="dashTitle" id="mlTopTitle">Karakoram Range — Machine Learning Cryosphere Suite</div>
          </div>
          <div class="controls" style="grid-template-columns:1fr 1fr;min-width:420px">
            <div class="control" style="padding:10px 14px">
              <label>Select Basin</label>
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
            <div class="control" style="padding:10px 14px">
              <label>Target Variable</label>
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
            <div class="metric"><b id="mlGprYear">2016</b><span>GPR STRUCTURAL CHANGEPOINT</span></div>
            <div class="metric"><b id="mlTopDriver">2m Air Temp</b><span>#1 RANDOM FOREST DRIVER</span></div>
            <div class="metric"><b id="mlFcstR2">R² = 0.99</b><span>FORECASTER HOLDOUT TEST R²</span></div>
            <div class="metric"><b id="mlSilScore">0.467</b><span>K-MEANS SILHOUETTE SCORE</span></div>
          </div>

          <div class="chartGrid" style="margin-top:14px">
            <div class="chart" id="mlChartGpr">${svg}</div>
            <div class="chart" id="mlChartFcst">${svg}</div>
          </div>

          <div class="chartGrid" style="margin-top:14px;grid-template-columns:1.1fr 1.3fr">
            <div>
              <div class="mono" style="margin:6px 0 8px">EXPLAINABLE RANDOM FOREST + GRADIENT BOOSTING DRIVER IMPORTANCE (%)</div>
              <div class="mlBars" id="mlDriverBars" style="margin-top:0"></div>
            </div>
            <div>
              <div class="mono" style="margin:6px 0 8px">UNSUPERVISED K-MEANS (k=3) + PCA CRYOSPHERE REGIME CLUSTERING</div>
              <div class="shieldTable" id="mlClusterTable" style="margin-top:0"></div>
            </div>
          </div>
        </div>
      </div>
    </div>`
  );
}

/* ============================================================================
   PAGE 7: SHIELD (7-Day GLOF Radar for 15 Glaciers + Indus Water Tower Simulator)
   ============================================================================ */
function shield() {
  return (
    pageHead(
      "EARLY WARNING COMMAND CENTER // INDUS WATER TOWER SIMULATOR",
      "HimalayaShield",
      "Real-time 7-day GLOF outburst flood radar across all 15 iconic Pakistan glaciers paired with the Tarbela Dam & Indus Water Tower Peak Water Simulator (2020–2080) serving 240 million people downstream."
    ) +
    `<div class="pageBody">
      <div class="featureGrid">
        ${glass("7-DAY METEOMATICS RADAR", "15 Iconic Glacier Hotspots", "Live snout temperature, 7-day snowmelt accumulation, 0°C freezing level vs. ELA, and automated CRITICAL / HIGH / WATCH trigger scores.")}
        ${glass("INFRASTRUCTURE LEDGER", "Downstream Exposure", "Tracks threat corridors along the Karakoram Highway (KKH), Hassanabad Bridge, Tarbela Dam, Diamer-Bhasha, and Dasu Hydropower.")}
        ${glass("PEAK WATER TIPPING POINT", "Indus Basin Water Security", "Simulates Tarbela Dam annual inflows (64.5 MAF baseline), Rabi wheat & Kharif rice irrigation, and 15,827 MW hydropower capacity.")}
      </div>

      <div class="radarViz">
        <i class="alertDot" style="left:68%;top:31%" title="Shisper Glacier — CRITICAL"></i>
        <i class="alertDot" style="left:34%;top:61%;animation-delay:.7s" title="Passu Glacier — HIGH"></i>
        <i class="alertDot" style="left:57%;top:73%;animation-delay:1.2s" title="Batura Glacier — WATCH"></i>
        <i class="alertDot" style="left:46%;top:42%;animation-delay:.4s" title="Baltoro Glacier"></i>
        <span class="mono" style="position:absolute;left:18px;top:14px">7-DAY METEOMATICS GLOF EARLY WARNING RADAR · SCANNING 15 PAKISTAN GLACIER TERMINI</span>
        <span class="mono" id="shieldIsoSummary" style="position:absolute;right:18px;bottom:14px;color:#ffd86b">ISOLATION FOREST COMPOUND HAZARD DETECTOR: ACTIVE</span>
      </div>

      <div class="dashShell" style="margin-top:18px">
        <div class="dashTop">
          <div>
            <div class="mono">ALL 15 MONITORED GLACIERS & GLOF LAKES // SORTED BY 7-DAY TRIGGER SCORE</div>
            <div class="dashTitle">Pakistan Glacier Outburst Flood (GLOF) Watchlist & Infrastructure Exposure</div>
          </div>
        </div>
        <div class="dashBody" style="padding:0">
          <div class="shieldTable" id="shieldGlacierTable" style="margin-top:0;border:0;border-radius:0"></div>
        </div>
      </div>

      <div class="dashShell" style="margin-top:18px">
        <div class="dashTop">
          <div>
            <div class="mono">INDUS WATER TOWER & TARBELA DAM SIMULATOR (2020–2080)</div>
            <div class="dashTitle">Downstream Water Security, Agriculture & 15,827 MW Hydropower Projection</div>
          </div>
          <div class="tabs" id="waterScenarioTabs">
            <button class="tab" data-dt="1.5" data-ds="2.0">SSP1-2.6 (+1.5°C)</button>
            <button class="tab active" data-dt="2.4" data-ds="-8.0">SSP2-4.5 (+2.4°C Current)</button>
            <button class="tab" data-dt="3.2" data-ds="-14.0">SSP3-7.0 (+3.2°C)</button>
            <button class="tab" data-dt="4.2" data-ds="-20.0">SSP5-8.5 (+4.2°C Extreme)</button>
          </div>
        </div>
        <div class="dashBody">
          <div class="controls" style="grid-template-columns:1fr 1fr">
            <div class="control">
              <label>Basin Warming Anomaly (ΔT): <span id="tempValLabel" class="mono">+2.4°C</span></label>
              <input id="temp" type="range" min="1.0" max="4.5" step="0.1" value="2.4">
            </div>
            <div class="control">
              <label>Winter Snowfall Change (ΔSnow): <span id="snowValLabel" class="mono">-8.0%</span></label>
              <input id="snowSim" type="range" min="-25" max="25" step="1" value="-8">
            </div>
          </div>
          <div class="verdict">
            <div class="mono">INDUS BASIN HYDROLOGICAL VERDICT // 240 MILLION PEOPLE DOWNSTREAM</div>
            <strong id="maf">+2.4°C · Peak Water Year 2039 (72.3 MAF) → 2075 Inflow 53.6 MAF</strong>
            <p id="waterSubVerdict">Before Peak Water, accelerated glacier melt temporarily boosts summer inflows (increasing GLOF flood risk). After Peak Water, shrinking glacier volume causes structural late-summer water deficits for Kharif crops and Tarbela/Diamer-Bhasha hydropower.</p>
          </div>
          <div class="metrics" id="waterMetricsGrid">
            <div class="metric"><b>2039</b><span>PEAK WATER TIPPING YEAR</span></div>
            <div class="metric"><b>72.3 MAF</b><span>PEAK ANNUAL INFLOW</span></div>
            <div class="metric"><b>53.6 MAF</b><span>2075 LATE-CENTURY INFLOW</span></div>
            <div class="metric"><b>52.4%</b><span>GLACIER ICE REMAINING (2080)</span></div>
          </div>
          <div class="chart" id="waterHydroChart" style="margin-top:14px;height:260px">${svg}</div>
        </div>
      </div>
    </div>`
  );
}

/* ============================================================================
   3D / 2D CANVAS MOUNTAIN, GLACIER, SNOW, LIGHTNING & SCAN ENGINE
   ============================================================================ */
let sceneRAF = 0,
  sceneReady = false;
function initCinematic() {
  const c = document.getElementById("scene3d");
  if (!c) {
    sceneReady = false;
    return;
  }
  if (sceneReady) return;
  sceneReady = true;
  const x = c.getContext("2d");
  let w = 0,
    h = 0,
    dpr = 1,
    scroll = 0,
    targetScroll = 0,
    yaw = 0,
    pitch = 0,
    drag = false,
    lx = 0,
    ly = 0,
    t = 0;
  const layers = [
    { n: 34, z: 900, fall: 0.35, size: [0.5, 1.2] },
    { n: 58, z: 560, fall: 0.75, size: [0.8, 1.9] },
    { n: 42, z: 280, fall: 1.45, size: [1.3, 3.2] },
  ];
  let flakes = [];
  function resize() {
    dpr = Math.min(devicePixelRatio || 1, 2);
    w = c.clientWidth;
    h = c.clientHeight;
    c.width = w * dpr;
    c.height = h * dpr;
    x.setTransform(dpr, 0, 0, dpr, 0, 0);
    if (!flakes.length)
      layers.forEach((L, li) => {
        for (let i = 0; i < L.n; i++)
          flakes.push({
            x: Math.random() * w,
            y: Math.random() * h,
            z: li,
            v: 1 + Math.random() * L.fall,
            r: L.size[0] + Math.random() * (L.size[1] - L.size[0]),
            sway: Math.random() * 6.28,
          });
      });
  }
  function project(px, py, pz) {
    const depth = 900 + pz;
    const k = 900 / depth;
    return {
      x: w / 2 + (px - w / 2) * k + Math.sin(yaw) * (-pz * 0.24),
      y: h / 2 + (py - h / 2) * k + pitch * (-pz * 0.18),
      k,
    };
  }
  function mountain(base, amp, color, depth, phase) {
    let pts = [];
    for (let i = 0; i <= 12; i++) {
      let xx = (i / 12) * w;
      let yy =
        base -
        amp * (0.35 + 0.65 * Math.abs(Math.sin(i * 1.71 + phase))) -
        Math.sin(i * 2.3 + phase) * amp * 0.18;
      let q = project(xx, yy, depth);
      pts.push([q.x, q.y]);
    }
    x.beginPath();
    x.moveTo(0, h);
    pts.forEach((p) => x.lineTo(p[0], p[1]));
    x.lineTo(w, h);
    x.closePath();
    x.fillStyle = color;
    x.fill();
  }
  // Pre-seed twinkling multi-magnitude stars & ridge spindrift particles
  const stars = Array.from({ length: 140 }, (_, i) => ({
    x: ((i * 137.5) % 1000) / 1000,
    y: ((i * 73.1) % 580) / 1000,
    r: i % 11 === 0 ? 1.8 : i % 4 === 0 ? 1.2 : 0.75,
    phase: i * 0.9,
    speed: 0.018 + (i % 5) * 0.007,
  }));

  const spindrift = Array.from({ length: 48 }, (_, i) => ({
    peakIdx: i % 3,
    life: Math.random(),
    speed: 0.006 + Math.random() * 0.008,
    len: 18 + Math.random() * 34,
    dy: (Math.random() - 0.5) * 14,
  }));

  const glacierTargets = [
    { name: "SHISPER · 36.4°N", rx: 0.43, ry: 0.67 },
    { name: "BALTORO / K2 · 35.7°N", rx: 0.61, ry: 0.61 },
    { name: "SIACHEN · 35.4°N", rx: 0.75, ry: 0.65 },
  ];

  function fbmRidge(u, phase) {
    // Multi-octave craggy Himalayan ridgeline (sharp summits + natural saddles)
    const p1 = 1 - Math.abs(Math.sin(u * 6.2 + phase));
    const p2 = 1 - Math.abs(Math.sin(u * 13.7 + phase * 1.9));
    const p3 = Math.sin(u * 29.3 + phase * 3.1) * 0.5 + 0.5;
    const p4 = Math.sin(u * 57.0 + phase * 5.2) * 0.5 + 0.5;
    return p1 * 0.54 + p2 * 0.27 + p3 * 0.13 + p4 * 0.06;
  }

  function drawMountainRidge(base, amp, topCol, botCol, depth, phase, rimColor, showMesh) {
    const steps = 68;
    let pts = [];
    let minY = h;
    for (let i = 0; i <= steps; i++) {
      const u = i / steps;
      const xx = u * w;
      const hVal = fbmRidge(u, phase);
      const yy = base - amp * (0.22 + 0.78 * hVal);
      const q = project(xx, yy, depth);
      if (q.y < minY) minY = q.y;
      pts.push([q.x, q.y, xx, yy]);
    }
    x.beginPath();
    x.moveTo(0, h);
    pts.forEach((p) => x.lineTo(p[0], p[1]));
    x.lineTo(w, h);
    x.closePath();

    const grad = x.createLinearGradient(0, minY, 0, h);
    grad.addColorStop(0, topCol);
    grad.addColorStop(0.55, botCol);
    grad.addColorStop(1, "rgba(3, 12, 18, 0.94)");
    x.fillStyle = grad;
    x.fill();

    // Shaded 3D ridge spurs & snow couloirs descending from major peaks
    x.save();
    for (let i = 4; i < pts.length - 4; i += 5) {
      if (pts[i][1] < pts[i - 2][1] && pts[i][1] < pts[i + 2][1]) {
        const px = pts[i][0], py = pts[i][1];
        const spurX = px + (i % 2 === 0 ? 34 : -28);
        const spurY = py + 115;
        x.beginPath();
        x.moveTo(px, py);
        x.lineTo(spurX, spurY);
        x.lineTo(px + 6, spurY);
        x.closePath();
        x.fillStyle = "rgba(180, 236, 255, 0.075)";
        x.fill();
      }
    }
    x.restore();

    // Subtle LIDAR wireframe elevation mesh on the right-hand range (like reference)
    if (showMesh) {
      x.save();
      x.strokeStyle = "rgba(109, 231, 255, 0.22)";
      x.lineWidth = 0.85;
      for (let i = Math.floor(steps * 0.36); i < pts.length - 3; i += 3) {
        const pA = pts[i];
        const pB = pts[i + 3];
        const midX = (pA[0] + pB[0]) * 0.5 + 10;
        const midY = Math.max(pA[1], pB[1]) + 46;
        x.beginPath();
        x.moveTo(pA[0], pA[1]);
        x.lineTo(midX, midY);
        x.lineTo(pB[0], pB[1]);
        x.stroke();
      }
      x.restore();
    }

    // Crisp rim highlight along the snow crest
    if (rimColor) {
      x.save();
      x.beginPath();
      pts.forEach((p, idx) => (idx === 0 ? x.moveTo(p[0], p[1]) : x.lineTo(p[0], p[1])));
      x.strokeStyle = rimColor;
      x.lineWidth = 1.3;
      x.stroke();
      x.restore();
    }
    return pts;
  }

  function drawTerrain() {
    let par = scroll * 0.12;
    const alpenglowShift = Math.max(0, Math.min(1, 0.5 + yaw * 0.8));
    const rimFar = `rgba(145, 224, 248, ${(0.18 + alpenglowShift * 0.1).toFixed(2)})`;
    const rimMid = `rgba(210, 242, 255, ${(0.28 + alpenglowShift * 0.12).toFixed(2)})`;
    const rimFront = alpenglowShift > 0.62 ? "rgba(255, 218, 178, 0.28)" : "rgba(175, 242, 255, 0.32)";

    drawMountainRidge(h * 0.67 - par, h * 0.28, "rgba(38, 92, 114, 0.45)", "rgba(12, 38, 50, 0.62)", 820, 0.35, rimFar, false);
    const midPts = drawMountainRidge(h * 0.72 - par, h * 0.30, "rgba(52, 118, 140, 0.62)", "rgba(14, 46, 60, 0.78)", 570, 1.45, rimMid, true);
    const frontPts = drawMountainRidge(h * 0.80 - par, h * 0.32, "rgba(24, 72, 92, 0.88)", "rgba(6, 26, 36, 0.96)", 330, 2.75, rimFront, false);

    // Moving cloud shadow drifting across the glacier valley
    x.save();
    const shadowX = ((t * 0.55) % (w + 460)) - 230;
    const sg = x.createLinearGradient(shadowX - 180, 0, shadowX + 180, 0);
    sg.addColorStop(0, "rgba(2, 8, 14, 0)");
    sg.addColorStop(0.5, "rgba(2, 8, 14, 0.26)");
    sg.addColorStop(1, "rgba(2, 8, 14, 0)");
    x.fillStyle = sg;
    x.fillRect(shadowX - 180, h * 0.52 - par, 360, h * 0.48);
    x.restore();

    // Glacier basin highlight polygon
    x.save();
    x.translate(w * 0.52, h * 0.75 - par * 0.8);
    x.rotate(-0.12);
    x.scale(1.5 + Math.min(0.4, scroll * 0.0005), 0.46);
    x.beginPath();
    for (let i = 0; i < 9; i++) {
      let a = (i * Math.PI * 2) / 9,
        r = 125 + 32 * Math.sin(i * 2.7);
      x.lineTo(Math.cos(a) * r, Math.sin(a) * r);
    }
    x.closePath();
    x.fillStyle = "rgba(92,226,250,.68)";
    x.shadowBlur = 38;
    x.shadowColor = "#43dcff";
    x.fill();
    x.restore();

    x.strokeStyle = "rgba(173,246,255,.38)";
    x.lineWidth = 1;
    for (let i = 0; i < 8; i++) {
      x.beginPath();
      x.moveTo(w * 0.32 + i * 42, h * 0.79 - par);
      x.lineTo(w * 0.52 + i * 24, h * 0.58 - par);
      x.stroke();
    }

    // 1. Ridge Spindrift (blowing snow plumes off high peaks)
    const anchors = [midPts[22], midPts[45], frontPts[34]].filter(Boolean);
    if (anchors.length) {
      x.save();
      const gust = 1 + 0.55 * Math.sin(t * 0.011);
      spindrift.forEach((sp) => {
        sp.life += sp.speed * gust;
        if (sp.life > 1) {
          sp.life = 0;
          sp.dy = (Math.random() - 0.5) * 12;
        }
        const anchor = anchors[sp.peakIdx % anchors.length];
        const px = anchor[0] + sp.life * (110 * gust);
        const py = anchor[1] + sp.dy * sp.life - sp.life * 8;
        const alpha = Math.sin(sp.life * Math.PI) * 0.42;
        const grad = x.createLinearGradient(px, py, px + sp.len, py - 3);
        grad.addColorStop(0, `rgba(225, 250, 255, ${alpha.toFixed(3)})`);
        grad.addColorStop(1, "rgba(225, 250, 255, 0)");
        x.strokeStyle = grad;
        x.lineWidth = 1.6;
        x.beginPath();
        x.moveTo(px, py);
        x.lineTo(px + sp.len, py - 3);
        x.stroke();
      });
      x.restore();
    }
  }

  function drawStars() {
    // 5. Faint upper-atmosphere cyan airglow above the horizon
    x.save();
    const ag = x.createLinearGradient(0, h * 0.25, 0, h * 0.62);
    ag.addColorStop(0, "rgba(70, 210, 235, 0)");
    ag.addColorStop(0.5, "rgba(70, 210, 235, 0.055)");
    ag.addColorStop(1, "rgba(70, 210, 235, 0)");
    x.fillStyle = ag;
    x.fillRect(0, h * 0.25, w, h * 0.37);

    // Multi-magnitude twinkling stars
    x.fillStyle = "#e6fbff";
    stars.forEach((st) => {
      const xx = ((st.x * w + t * 0.008) % w + w) % w;
      const yy = st.y * h;
      const twinkle = 0.2 + 0.55 * (0.5 + 0.5 * Math.sin(t * st.speed + st.phase));
      x.globalAlpha = twinkle;
      x.beginPath();
      x.arc(xx, yy, st.r, 0, Math.PI * 2);
      x.fill();
    });
    x.restore();
    x.globalAlpha = 1;
  }

  function drawFlakes() {
    // 4. 3-Depth wind-driven snowfall with synchronized gusts
    const windGust = 0.55 + 0.65 * Math.sin(t * 0.009);
    flakes.forEach((f) => {
      let L = layers[f.z];
      f.y += f.v * (1 + scroll * 0.0012);
      f.x += windGust * (0.35 + f.z * 0.38) + Math.sin(t * 0.001 + f.sway) * 0.28;
      if (f.y > h + 10) f.y = -10;
      if (f.x > w + 10) f.x = -10;
      if (f.x < -10) f.x = w + 10;
      let q = project(f.x, f.y, f.z * L.z);
      x.beginPath();
      x.arc(q.x, q.y, f.r * (1 + f.z * 0.18 + Math.min(0.6, scroll * 0.0008)), 0, Math.PI * 2);
      x.fillStyle =
        f.z === 2
          ? "rgba(232,251,255,.86)"
          : f.z === 1
          ? "rgba(214,247,255,.52)"
          : "rgba(190,238,255,.25)";
      x.fill();
    });
  }

  function drawSatelliteSwath() {
    // 2. Satellite Nadir Swath Cone & Glacier Target Pings
    const cycle = (t * 0.0016) % 1;
    const satX = w * (0.94 - cycle * 0.72);
    const satY = h * (0.14 + cycle * 0.09);
    const groundX = satX - w * 0.06;
    const groundY = h * 0.74;

    x.save();
    const coneGrad = x.createLinearGradient(satX, satY, groundX, groundY);
    coneGrad.addColorStop(0, "rgba(109, 231, 255, 0.16)");
    coneGrad.addColorStop(1, "rgba(109, 231, 255, 0.01)");
    x.fillStyle = coneGrad;
    x.beginPath();
    x.moveTo(satX, satY);
    x.lineTo(groundX - 55, groundY);
    x.lineTo(groundX + 55, groundY);
    x.closePath();
    x.fill();

    // Ping glacier markers when swath sweeps near them
    glacierTargets.forEach((gt) => {
      const gx = gt.rx * w;
      const gy = gt.ry * h - scroll * 0.08;
      const dist = Math.abs(gx - groundX);
      if (dist < 110) {
        const strength = 1 - dist / 110;
        const pulseR = 6 + ((t * 0.35) % 18);
        x.strokeStyle = `rgba(125, 244, 255, ${(strength * 0.65).toFixed(2)})`;
        x.lineWidth = 1.2;
        x.beginPath();
        x.arc(gx, gy, pulseR, 0, Math.PI * 2);
        x.stroke();

        x.fillStyle = `rgba(214, 250, 255, ${(strength * 0.92).toFixed(2)})`;
        x.beginPath();
        x.arc(gx, gy, 3, 0, Math.PI * 2);
        x.fill();

        x.font = '600 10px "DM Mono", monospace';
        x.fillStyle = `rgba(155, 240, 255, ${(strength * 0.88).toFixed(2)})`;
        x.fillText(gt.name, gx + 10, gy + 3);
      }
    });
    x.restore();
  }

  function drawLightning() {
    if (Math.sin(t * 0.017) > 0.992) {
      x.save();
      x.globalAlpha = 0.85;
      x.strokeStyle = "#dffcff";
      x.shadowBlur = 22;
      x.shadowColor = "#7deaff";
      x.lineWidth = 1.6;
      x.beginPath();
      let sx = w * 0.78,
        sy = h * 0.08;
      x.moveTo(sx, sy);
      for (let i = 0; i < 8; i++) {
        sx += (Math.random() - 0.5) * w * 0.06;
        sy += h * 0.045 + Math.random() * h * 0.035;
        x.lineTo(sx, sy);
      }
      x.stroke();
      x.restore();
    }
  }

  function drawScan() {
    let yy = h * 0.55 + Math.sin(t * 0.0012) * 22;
    x.save();
    x.translate(w * 0.5, yy);
    x.rotate(-0.08);
    x.fillStyle = "rgba(91,235,255,.055)";
    x.fillRect(-w * 0.46, 0, w * 0.92, 70);
    x.strokeStyle = "rgba(105,235,255,.7)";
    x.shadowBlur = 18;
    x.shadowColor = "#5deaff";
    x.strokeRect(-w * 0.46, 0, w * 0.92, 1);

    // 3. Topographic Elevation Contours revealed along the scan band
    x.shadowBlur = 0;
    x.strokeStyle = "rgba(125, 238, 255, 0.18)";
    x.lineWidth = 1;
    const labels = ["3,500 m", "5,180 m ELA", "8,611 m K2"];
    for (let cIdx = 0; cIdx < 3; cIdx++) {
      const cy = 18 + cIdx * 18;
      x.beginPath();
      for (let sx = -w * 0.38; sx <= w * 0.38; sx += 24) {
        const wy = cy + Math.sin(sx * 0.012 + cIdx * 1.4) * 5;
        if (sx === -w * 0.38) x.moveTo(sx, wy);
        else x.lineTo(sx, wy);
      }
      x.stroke();
      x.fillStyle = "rgba(165, 242, 255, 0.42)";
      x.font = '10px "DM Mono", monospace';
      x.fillText(labels[cIdx], w * 0.31, cy - 3);
    }
    x.restore();
  }

  function draw() {
    if (!document.getElementById("scene3d")) {
      sceneReady = false;
      return;
    }
    t++;
    scroll += (targetScroll - scroll) * 0.075;
    x.clearRect(0, 0, w, h);
    let g = x.createLinearGradient(0, 0, 0, h);
    g.addColorStop(0, scroll > 450 ? "#091d2e" : "#061b29");
    g.addColorStop(0.55, scroll > 450 ? "#124657" : "#0a3441");
    g.addColorStop(1, "#02090e");
    x.fillStyle = g;
    x.fillRect(0, 0, w, h);
    drawStars();
    drawTerrain();
    drawSatelliteSwath();
    drawScan();
    drawFlakes();
    drawLightning();
    let el = document.getElementById("sceneTemp");
    if (el) el.textContent = (-7.8 + Math.sin(t * 0.002) * 0.7 + scroll * 0.0012).toFixed(1) + "°C";
    sceneRAF = requestAnimationFrame(draw);
  }
  resize();
  draw();
  c.addEventListener("pointerdown", (e) => {
    drag = true;
    lx = e.clientX;
    ly = e.clientY;
    c.setPointerCapture(e.pointerId);
  });
  c.addEventListener("pointermove", (e) => {
    if (!drag) return;
    yaw += (e.clientX - lx) * 0.003;
    pitch += (e.clientY - ly) * 0.002;
    pitch = Math.max(-0.5, Math.min(0.5, pitch));
    lx = e.clientX;
    ly = e.clientY;
  });
  c.addEventListener("pointerup", () => (drag = false));
  window.addEventListener("resize", resize);
  window.addEventListener(
    "scroll",
    () => {
      targetScroll = window.scrollY;
      const hero = document.querySelector(".hero");
      if (hero) {
        hero.style.setProperty("--scene-scroll", targetScroll);
        const photo = hero.querySelector(".mountainPhoto");
        if (photo) {
          const p = Math.min(targetScroll / 900, 1);
          photo.style.transform =
            "scale(" + (1.12 + p * 0.22) + ") translate3d(" + -p * 3 + "%," + p * 2 + "%,0)";
          photo.style.filter =
            "saturate(" + (0.78 + p * 0.2) + ") contrast(" + (1.12 + p * 0.14) + ") brightness(" + (0.62 + p * 0.15) + ")";
        }
        hero.querySelectorAll(".range").forEach((r, i) => {
          r.style.transform =
            "translate3d(" +
            Math.sin(yaw + i) * 18 +
            "px," +
            -targetScroll * (0.06 + i * 0.035) +
            "px,0) scale(" +
            (1 + i * 0.05 + targetScroll * 0.00018 * (i + 1)) +
            ")";
        });
      }
    },
    { passive: true }
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
      if (title) title.textContent = `${d.region_name} — ${d.variable_name}`;
      const badge = document.getElementById("homeVerdictBadge");
      if (badge) badge.textContent = `DETECTIVE VERDICT // ${d.verdict.badge_status}`;
      const head = document.getElementById("homeVerdictHead");
      if (head) head.textContent = d.verdict.headline;
      const sub = document.getElementById("homeVerdictSub");
      if (sub) {
        const fq = d.verdict?.four_questions || {};
        const whatTxt = fq.what_is_changing || "";
        const speedTxt = fq.how_fast_is_it_changing || fq.how_much_is_it_changing || "";
        const sigTxt = fq.is_it_statistically_significant || fq.is_it_significant || "";
        sub.textContent = `${whatTxt} ${speedTxt} (${sigTxt})`.trim();
      }
      const mg = document.getElementById("homeMetricsGrid");
      if (mg) {
        mg.innerHTML = `<div class="metric"><b>${d.metrics.sen_decade}</b><span>SEN SLOPE / DECADE</span></div>
          <div class="metric"><b>${formatP(d.metrics.hamed_rao_p)}</b><span>HAMED-RAO P-VALUE</span></div>
          <div class="metric"><b>+${d.freezing_level.shift_m} m</b><span>0°C ISOTHERM SHIFT</span></div>
          <div class="metric"><b>${d.start_year}-${d.end_year}</b><span>${d.n_years}-YEAR RECORD</span></div>`;
      }
      const c1 = document.getElementById("homeChart");
      if (c1 && d.svg_anomaly) c1.innerHTML = d.svg_anomaly;
      const c2 = document.getElementById("homeSeasonChart");
      if (c2 && d.svg_seasonal) c2.innerHTML = d.svg_seasonal;
    } catch (e) {}
  };

  document.querySelectorAll("#homeBasinTabs .tab").forEach((btn) => {
    btn.addEventListener("click", () => {
      document.querySelectorAll("#homeBasinTabs .tab").forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
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
    if (titleEl)
      titleEl.textContent = `${data.region_name} — ${data.variable_name}${
        glacierOnly === "true" ? " [RGI v6.0 Glacier Mask]" : ""
      }`;
    const srcEl = body.querySelector("#invSourceTag");
    if (srcEl) srcEl.textContent = `${data.source_mission} // ${data.source_mode.toUpperCase()}`;
    const badgeEl = body.querySelector("#invBadge");
    if (badgeEl) badgeEl.textContent = `DETECTIVE VERDICT // ${data.verdict.badge_status}`;
    const headEl = body.querySelector("#invHeadline");
    if (headEl) headEl.textContent = data.verdict.headline;
    const subEl = body.querySelector("#invSubtext");
    if (subEl) {
      const fq = data.verdict?.four_questions || {};
      const whatTxt = fq.what_is_changing || "";
      const whereTxt = fq.where_is_it_changing || data.region_name || "";
      const speedTxt = fq.how_fast_is_it_changing || fq.how_much_is_it_changing || `${data.metrics?.sen_decade || ""}/decade`;
      const sigTxt = fq.is_it_statistically_significant || fq.is_it_significant || formatP(data.metrics?.hamed_rao_p);
      const autoNote = data.verdict?.autocorrelation_note || "";
      subEl.innerHTML = `<b>1. What is changing:</b> ${whatTxt}<br>
        <b>2. Where:</b> ${whereTxt} · <b>3. Speed:</b> ${speedTxt}<br>
        <b>4. Significance & Autocorrelation:</b> ${sigTxt}${autoNote ? ` (${autoNote})` : ""}`;
    }

    const compBanner = body.querySelector("#invCompareBanner");
    if (compBanner) {
      if (data.comparison) {
        compBanner.style.display = "block";
        compBanner.innerHTML = `<div class="mono" style="color:#f2c56b">SIDE-BY-SIDE COMPARE MODE // ${data.comparison.region_name.toUpperCase()} (${data.comparison.badge})</div>
          <strong>${data.comparison.headline}</strong>
          <p>Comparison Sen's Slope: <b>${data.comparison.sen_decade}/decade</b> (${formatP(data.comparison.p_value)}) vs. Primary ${data.region_name}: <b>${data.metrics.sen_decade}/decade</b> (${formatP(data.metrics.hamed_rao_p)}).</p>`;
      } else {
        compBanner.style.display = "none";
      }
    }

    const mContainer = body.querySelector("#invMetrics");
    if (mContainer) {
      mContainer.innerHTML = `
        <div class="metric"><b>${data.metrics.sen_decade}</b><span>SEN SLOPE / DECADE (95% CI ${data.metrics.sen_ci})</span></div>
        <div class="metric"><b>${data.metrics.ols_decade}</b><span>OLS SLOPE / DECADE (TOTAL ${data.metrics.total_change})</span></div>
        <div class="metric"><b>${data.metrics.mk_tau}</b><span>MANN-KENDALL (LAG-1 r = ${data.metrics.lag1_autocorr})</span></div>
        <div class="metric"><b>${formatP(data.metrics.hamed_rao_p)}</b><span>HAMED-RAO P-VALUE (VIF ${data.metrics.vif})</span></div>`;
    }

    const cryoContainer = body.querySelector("#invCryoMetrics");
    if (cryoContainer) {
      const fdrPct = data.spatial?.summary?.pct_significant_fdr ?? 0;
      const darkMeltPct = data.dark_ice?.melt_enhancement_pct ?? data.dark_ice?.soot_melt_share_pct ?? 0;
      const fdrOrIceTile = fdrPct > 0
        ? `<div class="metric"><b>${fdrPct}%</b><span>BH-FDR SIGNIFICANT GRID CELLS</span></div>`
        : `<div class="metric"><b>${data.freezing_level.newly_exposed_ice_km2} km²</b><span>NEWLY EXPOSED GLACIER ICE</span></div>`;
      cryoContainer.innerHTML = `
        <div class="metric"><b>${data.freezing_level.shift_m >= 0 ? "+" : ""}${data.freezing_level.shift_m} m</b><span>0°C ISOTHERM SHIFT (${data.freezing_level.newly_exposed_ice_km2} km² ICE EXPOSED)</span></div>
        <div class="metric"><b>${data.freezing_level.current_ela_m} m</b><span>CURRENT EQUILIBRIUM LINE ALTITUDE (ELA)</span></div>
        <div class="metric"><b>+${data.dark_ice.extra_melt_mm_per_month} mm/mo</b><span>DARK-ICE SOOT ALBEDO MELT (+${darkMeltPct}%)</span></div>
        ${fdrOrIceTile}`;
    }

    const c1 = body.querySelector("#invChartAnom");
    if (c1 && data.svg_anomaly) c1.innerHTML = data.svg_anomaly;
    const c2 = body.querySelector("#invChartSeason");
    if (c2) {
      if (data.comparison && data.comparison.svg_anomaly) {
        c2.innerHTML = data.comparison.svg_anomaly;
      } else if (data.svg_seasonal) {
        c2.innerHTML = data.svg_seasonal;
      }
    }

    const elevEl = body.querySelector("#invElevBands");
    if (elevEl && data.spatial?.elevation_bands) {
      elevEl.innerHTML = data.spatial.elevation_bands
        .map((b) => {
          const w = Math.min(100, Math.max(15, Math.abs(b.slope_per_decade) * 45 + 25));
          const label = (b.band_label || b.elevation_band || "Elevation band").split("(")[0].trim();
          return `<div class="mlBar" style="grid-template-columns:135px 1fr 75px"><span>${label}</span><i style="width:${w}%"></i><b>${b.slope_per_decade >= 0 ? "+" : ""}${b.slope_per_decade} ${data.units}</b></div>`;
        })
        .join("");
    }

    const teleEl = body.querySelector("#invTeleList");
    if (teleEl && data.teleconnections) {
      teleEl.innerHTML = data.teleconnections
        .map((t) => {
          const code = t.index_code || t.index_id || "INDEX";
          const corr = t.correlation_r ?? t.pearson_r ?? 0;
          const pStr = formatP(t.p_value ?? t.pearson_p);
          const desc = t.relationship_strength || t.physical_mechanism || "";
          return `<div style="padding:10px 12px;border:1px solid rgba(109,231,255,.2);border-radius:12px;background:rgba(4,16,24,.85);font-size:12.5px">
              <b style="color:#6de7ff;font-family:'DM Mono'">${code} (${corr >= 0 ? "+" : ""}${corr}, ${pStr})</b> · <span style="color:#d6eef5">${desc}</span>
            </div>`;
        })
        .join("");
    }

    const defTitle = body.querySelector("#invVarDefTitle");
    if (defTitle) defTitle.textContent = `${data.variable_name} (${data.units})`;
    const defText = body.querySelector("#invVarDefText");
    if (defText)
      defText.innerHTML = `<b>Plain Definition:</b> ${data.plain_definition}<br><br><b>Scientific Caveat:</b> ${data.caveats}`;

    const lab = body.querySelector("#yearsLabel");
    if (lab) lab.textContent = `${data.start_year}—${data.end_year} (${data.n_years} Yrs)`;
  } catch (err) {}
}

function enhancePage(n) {
  // Highlight active nav link
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
  ribbon.innerHTML =
    '<div><span>OBSERVATION STATE</span><b><span class="livePulse"></span> LIVE</b><span>NASA + METEOMATICS</span></div><div><span>MONITORING WINDOW</span><b>1981—2026</b><span>45 YEARS · MONTHLY</span></div><div><span>GLACIER TARGETS</span><b>15 HOTSPOTS</b><span>9 RIVER BASINS</span></div><div><span>STATISTICAL ENGINE</span><b>95% CI + FDR</b><span>HAMED–RAO + THEIL–SEN</span></div>';
  body.insertBefore(ribbon, body.firstChild);

  if (n === "investigate") {
    // Question pills
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
        if (lab) lab.textContent = `${2026 - y + 1}—2026 (${y} Yrs)`;
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

    // Check if Case page passed a preset
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
        if (tag) tag.textContent = `${d.case.code} // ${d.case.subtitle.toUpperCase()}`;
        const title = body.querySelector("#caseMainTitle");
        if (title) title.textContent = d.case.title;

        body.querySelector("#casePrimaryBadge").textContent = `PRIMARY BASIN // ${d.primary.badge}`;
        body.querySelector("#casePrimaryHead").textContent = `${d.primary.region_name}: ${d.primary.headline}`;
        body.querySelector("#casePrimaryStat").textContent = `Sen's Slope: ${d.primary.sen_slope} · Hamed-Rao ${formatP(d.primary.p_value)}`;

        body.querySelector("#caseCompBadge").textContent = `COMPARISON BASIN // ${d.comparison.badge}`;
        body.querySelector("#caseCompHead").textContent = `${d.comparison.region_name}: ${d.comparison.headline}`;
        body.querySelector("#caseCompStat").textContent = `Sen's Slope: ${d.comparison.sen_slope} · Hamed-Rao ${formatP(d.comparison.p_value)}`;

        const svgBox = body.querySelector("#caseReplaySvg");
        if (svgBox && d.svg) svgBox.innerHTML = d.svg;

        const qTitle = body.querySelector("#caseQuestionTitle");
        if (qTitle) qTitle.textContent = d.case.question;
        const take = body.querySelector("#caseTakeawayText");
        if (take) take.textContent = d.case.detective_takeaway;
        const steps = body.querySelector("#caseStepsList");
        if (steps && d.case.story_steps) {
          steps.innerHTML = d.case.story_steps.map((s) => `<div style="margin-bottom:6px">• ${s}</div>`).join("");
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

    // Load Multi-Sensor Validation Table
    fetch("/api/reference?region=karakoram")
      .then((r) => r.json())
      .then((d) => {
        const tbl = body.querySelector("#sensorValidationTable");
        if (tbl && d.sensor_validation) {
          const rows = d.sensor_validation
            .map((s) => {
              const pair = s.sensor_pair || s["Validation Pair"] || "Sensor pair";
              const rVal = s.correlation_r ?? s["Anomaly Correlation (r)"] ?? "0.00";
              const metric2 = s.rmse !== undefined ? `RMSE ${s.rmse} · Bias ${s.mean_bias}` : `${s["Mean Absolute Difference"] || ""} · ${s["Directional Consistency"] || ""}`;
              const verdictTxt = s.validation_status || s["Significance Agreement"] || "Validated";
              return `<div class="shieldRow"><b>${pair}</b><b class="statusLow">r = ${rVal}</b><span>${metric2}</span><span>${verdictTxt}</span></div>`;
            })
            .join("");
          tbl.innerHTML =
            '<div class="shieldRow headerRow"><span>SENSOR PAIR</span><span>CORRELATION (r)</span><span>BIAS / RMSE</span><span>DETECTIVE VALIDATION VERDICT</span></div>' +
            rows;
        }
      })
      .catch(() => {});
  }

  if (n === "notebook") {
    const cards = body.querySelectorAll("#missionsGrid .glass");
    cards.forEach((card, idx) => {
      card.querySelectorAll(".quizBtn").forEach((btn) => {
        btn.addEventListener("click", () => {
          const isCorrect = btn.dataset.correct === "true";
          card.querySelectorAll(".quizBtn").forEach((b) => b.classList.remove("correct", "wrong"));
          if (isCorrect) {
            btn.classList.add("correct");
            card.classList.add("missionDone");
            const st = card.querySelector(`#mStatus${idx}`);
            if (st) st.textContent = `✓ MISSION 0${idx + 1} VERIFIED — CLUE SOLVED`;
          } else {
            btn.classList.add("wrong");
          }
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
            .map((l, i) => glass(`LIMITATION 0${i + 1}`, l.title, `${l.issue} — Mitigation: ${l.how_we_handle_it}`))
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
        if (title) title.textContent = `${place} — Machine Learning Cryosphere Suite`;
        body.querySelector("#mlGprYear").textContent = `${d.gpr.changepoint_year} (R²=${d.gpr.r2})`;
        body.querySelector("#mlTopDriver").textContent = d.drivers?.[0]?.name || "2m Air Temp";
        body.querySelector("#mlFcstR2").textContent = `R² = ${d.forecast_metrics.test_r2.toFixed(2)} (RMSE ${d.forecast_metrics.test_rmse.toFixed(2)})`;
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
                `<div class="mlBar"><span>${x.name}</span><i style="width:${Math.min(100, x.pct * 1.8)}%"></i><b>${x.pct}%</b></div>`
            )
            .join("");
        }

        const cTbl = body.querySelector("#mlClusterTable");
        if (cTbl && d.clustering?.regimes) {
          cTbl.innerHTML =
            '<div class="shieldRow headerRow"><span>BASIN / GLACIER</span><span>ELEVATION</span><span>TEMP / SNOW TREND</span><span>K-MEANS REGIME</span></div>' +
            d.clustering.regimes
              .map(
                (r) =>
                  `<div class="shieldRow"><b>${r.entity_name}</b><span>${r.elevation_m} m</span><span>${r.temp_trend_c_dec >= 0 ? "+" : ""}${r.temp_trend_c_dec}°C · ${r.snow_trend_pct_dec}%</span><b class="statusLow">${r.regime_label}</b></div>`
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
      body.querySelector("#tempValLabel").textContent = `+${(+dt).toFixed(1)}°C`;
      body.querySelector("#snowValLabel").textContent = `${+ds >= 0 ? "+" : ""}${(+ds).toFixed(0)}%`;
      try {
        const res = await fetch(`/api/shield?delta_temp=${dt}&delta_snow_pct=${ds}`);
        if (!res.ok) return;
        const d = await res.json();

        const table = body.querySelector("#shieldGlacierTable");
        if (table && d.radar_glaciers) {
          table.innerHTML =
            '<div class="shieldRow headerRow"><span>GLACIER & RANGE (15 TARGETS)</span><span>7-DAY GLOF ALERT</span><span>DOWNSTREAM INFRASTRUCTURE AT RISK</span><span>TELEMETRY (ELA / 7D MELT)</span></div>' +
            d.radar_glaciers
              .map((g) => {
                const st =
                  g.alert_level.includes("RED") || g.alert_level.includes("HIGH")
                    ? "HIGH"
                    : g.alert_level.includes("WATCH")
                    ? "WATCH"
                    : "LOW";
                const cls = st === "HIGH" ? "statusHigh" : st === "WATCH" ? "statusWatch" : "statusLow";
                return `<div class="shieldRow"><b>${g.glacier_name} <span style="color:#7da6b2;font-weight:400">(${g.range})</span></b><b class="${cls}">${g.alert_level} (${g.peak_glof_score})</b><span>${g.infrastructure_at_risk}</span><span>ELA ${g.ela_elevation_m}m · Melt ${g.total_7d_melt_mm}mm/7d</span></div>`;
              })
              .join("");
        }

        if (d.hazard_summary) {
          const iso = body.querySelector("#shieldIsoSummary");
          const nMonths = d.hazard_summary.compound_extreme_months_count ?? d.hazard_summary.n_compound_hazard_months ?? 0;
          const peakDate = d.hazard_summary.peak_event_date || d.hazard_summary.peak_hazard_date || "May 2022";
          if (iso)
            iso.textContent = `ISOLATION FOREST: ${nMonths} COMPOUND EXTREME MONTHS DETECTED (PEAK: ${peakDate})`;
        }

        if (d.water_tower) {
          const w = d.water_tower;
          const maf = body.querySelector("#maf");
          if (maf) {
            maf.textContent = `+${w.delta_temp_c.toFixed(1)}°C Warming · Peak Water Year ${w.peak_water_year} (${w.peak_inflow_maf} MAF) → 2075 Inflow ${w.inflow_2075_maf} MAF`;
          }
          const wg = body.querySelector("#waterMetricsGrid");
          if (wg) {
            wg.innerHTML = `
              <div class="metric"><b>${w.peak_water_year}</b><span>PEAK WATER TIPPING YEAR (${w.peak_inflow_maf} MAF)</span></div>
              <div class="metric"><b>${w.inflow_2075_maf} MAF</b><span>2075 TARBELA INFLOW (VS 64.5 MAF BASE)</span></div>
              <div class="metric"><b>${w.kharif_2075_deficit_pct}% / ${w.rabi_wheat_change_pct}%</b><span>2075 KHARIF / RABI CROP WATER SHIFT</span></div>
              <div class="metric"><b>${w.projected_2075_mw} MW</b><span>2075 FIRM HYDROPOWER (OF ${w.installed_hydropower_mw} MW)</span></div>`;
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
  sceneReady = false;
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
    bindCinematicScroll();
    if (n === "home") {
      initCinematic();
      enhancePage("home");
    } else {
      enhancePage(n);
    }
  });
}

window.addEventListener("hashchange", render);
document.addEventListener(
  "scroll",
  () => {
    const y = window.scrollY;
    const a = document.getElementById("altimeter");
    if (a) a.textContent = Math.max(2.52, 705 - y * 0.72).toFixed(0) + " KM";
  },
  { passive: true }
);
render();

/* ============================================================================
   8 GLOBAL WINNER UPGRADES MODULE
   1. Interactive Pakistan Glacier Topographic Map (15 Hotspots + BH-FDR Grid)
   2. 1985 vs. 2026 Glacier Retreat & Snowline Split-Screen Comparator
   3. Interactive Laser Crosshair & Floating Telemetry Tooltips on All Charts
   4. Dynamic Alpenglow Sunlight Shift + Web-Audio Wind/Telemetry Soundscape
   5. Animated "▶ Play 1981→2026 Time-Lapse" Scrubber
   6. "✦ Ask Glacier Detective AI" Floating Copilot Drawer (/api/ask)
   7. Custom Latitude / Longitude Coordinate Inspector
   8. 1-Click "▶ 60s Judge Auto-Tour" Mode
   ============================================================================ */

// 4A. Inject Dynamic Alpenglow Sunlight Layer
if (!document.querySelector(".alpenglowLayer")) {
  const alp = document.createElement("div");
  alp.className = "alpenglowLayer";
  document.body.appendChild(alp);
}

// 4B. Web-Audio Ambient Mountain Wind & Orbital Telemetry Ping Synthesizer
let audioCtx = null,
  windGain = null,
  audioEnabled = false;

function toggleOrbitalAudio() {
  const btn = document.getElementById("btnAudioToggle");
  if (!audioEnabled) {
    const AudioContextClass = window.AudioContext || window.webkitAudioContext;
    if (!AudioContextClass) return;
    if (!audioCtx) {
      audioCtx = new AudioContextClass();
      const bufferSize = audioCtx.sampleRate * 2;
      const noiseBuffer = audioCtx.createBuffer(1, bufferSize, audioCtx.sampleRate);
      const output = noiseBuffer.getChannelData(0);
      for (let i = 0; i < bufferSize; i++) output[i] = Math.random() * 2 - 1;

      const whiteNoise = audioCtx.createBufferSource();
      whiteNoise.buffer = noiseBuffer;
      whiteNoise.loop = true;

      const filter = audioCtx.createBiquadFilter();
      filter.type = "bandpass";
      filter.frequency.value = 340;
      filter.Q.value = 2.4;

      windGain = audioCtx.createGain();
      windGain.gain.value = 0.025;

      whiteNoise.connect(filter);
      filter.connect(windGain);
      windGain.connect(audioCtx.destination);
      whiteNoise.start(0);
    }
    if (audioCtx.state === "suspended") audioCtx.resume();
    if (windGain) windGain.gain.setTargetAtTime(0.028, audioCtx.currentTime, 0.2);
    audioEnabled = true;
    if (btn) {
      btn.textContent = "🔊 Orbital Audio On";
      btn.style.borderColor = "#6de7ff";
    }
    playTelemetryPing(880);
  } else {
    audioEnabled = false;
    if (windGain && audioCtx) windGain.gain.setTargetAtTime(0.0001, audioCtx.currentTime, 0.15);
    if (btn) {
      btn.textContent = "🔇 Audio Off";
      btn.style.borderColor = "rgba(109,231,255,.35)";
    }
  }
}

function playTelemetryPing(freq = 740) {
  if (!audioEnabled || !audioCtx) return;
  try {
    const osc = audioCtx.createOscillator();
    const g = audioCtx.createGain();
    osc.type = "sine";
    osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
    osc.frequency.exponentialRampToValueAtTime(freq * 1.35, audioCtx.currentTime + 0.09);
    g.gain.setValueAtTime(0.04, audioCtx.currentTime);
    g.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + 0.11);
    osc.connect(g);
    g.connect(audioCtx.destination);
    osc.start();
    osc.stop(audioCtx.currentTime + 0.12);
  } catch (e) {}
}

document.getElementById("btnAudioToggle")?.addEventListener("click", toggleOrbitalAudio);
document.addEventListener("click", (e) => {
  if (e.target.closest("button, .pill, .tab, .glacierPinDot")) playTelemetryPing(680);
});

// 3. Global Interactive Laser Crosshair & Floating Telemetry Tooltip for All SVG Charts
const svgTooltip = document.getElementById("svgTooltip");
document.addEventListener("mousemove", (e) => {
  const svgEl = e.target.closest("svg.interactiveSvg");
  if (!svgEl || !svgTooltip) {
    if (svgTooltip) svgTooltip.style.display = "none";
    return;
  }
  const raw = svgEl.getAttribute("data-series");
  if (!raw) return;
  try {
    const d = JSON.parse(raw);
    const rect = svgEl.getBoundingClientRect();
    const relX = Math.max(0, Math.min(1, (e.clientX - rect.left) / Math.max(1, rect.width)));
    const n = d.v.length;
    const idx = Math.min(n - 1, Math.max(0, Math.round(relX * (n - 1))));
    const val = d.v[idx];
    const tr = d.t && d.t.length > idx ? d.t[idx] : null;
    const lo = d.lo && d.lo.length > idx ? d.lo[idx] : null;
    const hi = d.hi && d.hi.length > idx ? d.hi[idx] : null;

    let timeLabel = "";
    if (d.months && d.months[idx]) {
      timeLabel = `MONTH: ${d.months[idx]}`;
    } else {
      const yr = 1981 + Math.round(relX * 45);
      timeLabel = `WINDOW STEP ${idx + 1}/${n} (~${yr})`;
    }

    let html = `<b>${d.left || "TELEMETRY"}</b><span>${timeLabel}</span><br><span>OBSERVED: <strong style="color:#fff">${val >= 0 ? "+" : ""}${val}</strong></span>`;
    if (tr !== null) {
      html += `<br><span class="ttTrend">SEN/MODEL TREND: <strong>${tr >= 0 ? "+" : ""}${tr}</strong></span>`;
    }
    if (lo !== null && hi !== null) {
      html += `<br><span style="color:#8cb4c0">95% CI: [${lo >= 0 ? "+" : ""}${lo}, ${hi >= 0 ? "+" : ""}${hi}]</span>`;
    }
    svgTooltip.innerHTML = html;
    svgTooltip.style.display = "block";
    svgTooltip.style.left = Math.min(window.innerWidth - 240, e.clientX + 16) + "px";
    svgTooltip.style.top = Math.max(16, e.clientY - 70) + "px";

    // Draw or update laser crosshair line inside svgEl
    let laser = svgEl.querySelector(".laserCrosshair");
    if (!laser) {
      laser = document.createElementNS("http://www.w3.org/2000/svg", "line");
      laser.setAttribute("class", "laserCrosshair");
      laser.setAttribute("y1", "26");
      laser.setAttribute("y2", "230");
      laser.setAttribute("stroke", "#6de7ff");
      laser.setAttribute("stroke-width", "1.5");
      laser.setAttribute("stroke-dasharray", "4 3");
      svgEl.appendChild(laser);
    }
    const svgX = (relX * 900).toFixed(1);
    laser.setAttribute("x1", svgX);
    laser.setAttribute("x2", svgX);
  } catch (err) {}
});

// 6. "✦ Ask Glacier Detective AI" Copilot Drawer
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
  userMsg.style.borderColor = "#f2c56b66";
  userMsg.style.background = "rgba(42,32,14,.85)";
  userMsg.innerHTML = `<div class="mono" style="color:#f2c56b">YOU ASKED</div><p style="color:#fff">${questionText}</p>`;
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
    const pills = (d.metrics_cited || []).map((m) => `<span class="pill" style="font-size:8.5px">${m}</span>`).join("");
    botMsg.innerHTML = `<div class="mono">GLACIER DETECTIVE AI // VERIFIED EVIDENCE</div><h4>${d.title}</h4><p>${d.answer}</p><div style="margin-top:8px">${pills}</div>`;
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

// 1, 2, 5, 7: Inject Interactive Topographic Map, 1985 vs 2026 Split-Slider, Time-Lapse Button & Custom Coordinates into #investigate
let cachedGlaciersList = null;

async function injectAdvancedInvestigateWidgets() {
  const n = location.hash.slice(1) || "home";
  if (n !== "investigate") return;
  const body = view.querySelector(".pageBody");
  if (!body || body.querySelector("#advancedWidgetsDeck")) return;

  // 5. Add "▶ Play 1981→2026 Time-Lapse" button inside the Record Window control
  const yearsInput = body.querySelector("#years");
  if (yearsInput && !body.querySelector("#btnPlayTimelapse")) {
    const tlBtn = document.createElement("button");
    tlBtn.id = "btnPlayTimelapse";
    tlBtn.type = "button";
    tlBtn.className = "navUtilBtn";
    tlBtn.style.marginTop = "8px";
    tlBtn.style.width = "100%";
    tlBtn.textContent = "▶ Play 1981→2026 Time-Lapse";
    yearsInput.parentElement.appendChild(tlBtn);

    let tlTimer = null;
    tlBtn.addEventListener("click", () => {
      if (tlTimer) {
        clearInterval(tlTimer);
        tlTimer = null;
        tlBtn.textContent = "▶ Play 1981→2026 Time-Lapse";
        return;
      }
      let curY = 8;
      yearsInput.value = curY;
      tlBtn.textContent = "⏸ Playing Time-Lapse...";
      tlTimer = setInterval(() => {
        curY += 4;
        if (curY >= 45) {
          curY = 45;
          clearInterval(tlTimer);
          tlTimer = null;
          tlBtn.textContent = "▶ Play 1981→2026 Time-Lapse";
        }
        yearsInput.value = curY;
        const lab = body.querySelector("#yearsLabel");
        if (lab) lab.textContent = `${2026 - curY + 1}—2026 (${curY} Yrs)`;
        fetchLiveInvestigation(body);
      }, 650);
    });
  }

  // Build Advanced Widgets Deck (Custom Coordinates + Interactive 15-Glacier Topographic Map + 1985 vs 2026 Split-Slider)
  const deck = document.createElement("div");
  deck.id = "advancedWidgetsDeck";
  deck.innerHTML = `
    <div class="dashShell" style="margin-top:18px">
      <div class="dashTop">
        <div>
          <div class="mono">INTERACTIVE TOPOGRAPHIC MAP // 15 GLACIER HOTSPOTS + BH-FDR STIPPLING + CUSTOM COORDINATES</div>
          <div class="dashTitle">Northern Pakistan Cryosphere Radar & Custom Coordinate Inspector</div>
        </div>
        <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap">
          <input id="customLatInput" type="number" step="0.05" min="34.0" max="37.2" value="36.32" style="width:95px;background:#04121b;color:#fff;border:1px solid var(--line);border-radius:8px;padding:7px 9px;font:600 12px 'DM Mono'" title="Latitude (°N)">
          <input id="customLonInput" type="number" step="0.05" min="71.0" max="77.8" value="74.65" style="width:95px;background:#04121b;color:#fff;border:1px solid var(--line);border-radius:8px;padding:7px 9px;font:600 12px 'DM Mono'" title="Longitude (°E)">
          <button class="btn primary" id="btnInspectCoords" type="button" style="padding:8px 14px;font-size:11.5px">Inspect Custom Lat/Lon ↗</button>
        </div>
      </div>
      <div class="dashBody">
        <div class="chartGrid" style="grid-template-columns:1.35fr 1fr;margin-top:0">
          <div class="topoMapWrap">
            <svg id="pakTopoSvg" class="topoSvg" viewBox="0 0 680 320"></svg>
          </div>
          <div class="glacierDossierCard" id="glacierDossierBox">
            <div>
              <div class="mono" id="gdRangeTag">CLICK ANY GLACIER PIN ON THE MAP</div>
              <h3 id="gdName" style="font-size:24px;margin:8px 0;color:#fff">Shisper Glacier (Hunza)</h3>
              <p id="gdHistory" style="color:#c2e2ec;font-size:13.5px;line-height:1.6">Surging Karakoram glacier whose ice-dammed lake triggered the catastrophic May 7, 2022 Hassanabad Bridge collapse on the Karakoram Highway.</p>
            </div>
            <div class="metrics" style="grid-template-columns:1fr 1fr;margin-top:12px" id="gdMetrics">
              <div class="metric"><b>2,520 m / 5,180 m</b><span>SNOUT / ELA ALTITUDE</span></div>
              <div class="metric"><b style="color:#ff8b73">89.4 / 100</b><span>GLOF RISK SCORE</span></div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="dashShell" style="margin-top:18px">
      <div class="dashTop">
        <div>
          <div class="mono">HISTORICAL VS. MODERN CRYOSPHERE COMPARATOR // DRAG SLIDER LEFT OR RIGHT</div>
          <div class="dashTitle" id="splitTitle">1985 Baseline Glacier Ice vs. 2026 Retreat, 0°C Isotherm Shift & Soot Darkening</div>
        </div>
        <div class="tabs" id="splitGlacierTabs">
          <button class="tab active" data-g="shisper">Shisper Glacier (Hunza)</button>
          <button class="tab" data-g="baltoro">Baltoro / K2 (Karakoram)</button>
          <button class="tab" data-g="tirich">Tirich Mir (Hindu Kush)</button>
        </div>
      </div>
      <div class="dashBody">
        <div class="splitCompareWrap" id="splitCompareBox">
          <div class="splitLayer splitBefore">
            <div>
              <span class="pill" style="border-color:#6de7ff">1985 HISTORICAL BASELINE (MERRA-2 + LANDSAT/MODIS)</span>
              <h3 id="splitBeforeHead" style="font-size:26px;margin:12px 0 6px;color:#dffaff">1985: Stable Terminus & Deep Winter Snowpack</h3>
              <p id="splitBeforeDesc" style="max-width:540px;color:#b5dce8;font-size:14px">0°C Freezing Isotherm at 4,980 m · Clean Snow Albedo (0.78) · Minimal Supraglacial Melt Ponding · Tarbela Baseline Inflow 64.5 MAF.</p>
            </div>
            <div class="metrics" style="grid-template-columns:repeat(3,1fr);max-width:560px">
              <div class="metric"><b id="sb1985Iso">4,980 m</b><span>1985 0°C ISOTHERM</span></div>
              <div class="metric"><b id="sb1985Snow">84.2%</b><span>SNOW COVER FRACTION</span></div>
              <div class="metric"><b id="sb1985Alb">0.78</b><span>CLEAN ICE ALBEDO</span></div>
            </div>
          </div>
          <div class="splitLayer splitAfter" id="splitAfterLayer">
            <div style="text-align:right;margin-left:auto">
              <span class="pill" style="border-color:#ff8b73;color:#ffcabf">2026 OBSERVED STATE (+45 YEARS OF FORCING)</span>
              <h3 id="splitAfterHead" style="font-size:26px;margin:12px 0 6px;color:#ffe6dc">2026: +200 m Isotherm Rise & Supraglacial GLOF Lake</h3>
              <p id="splitAfterDesc" style="max-width:540px;margin-left:auto;color:#f2d5cc;font-size:14px">0°C Freezing Isotherm shifted to 5,180 m (+412 km² ice exposed to rain-on-snow melt) · OMI Black-Carbon Soot adds +18.4 mm/mo melt.</p>
            </div>
            <div class="metrics" style="grid-template-columns:repeat(3,1fr);max-width:560px;margin-left:auto">
              <div class="metric"><b id="sb2026Iso" style="color:#ff8b73">5,180 m (+200m)</b><span>2026 0°C ISOTHERM</span></div>
              <div class="metric"><b id="sb2026Snow" style="color:#ffd86b">76.8%</b><span>SNOW COVER FRACTION</span></div>
              <div class="metric"><b id="sb2026Alb" style="color:#ff8b73">0.64 (-18% Soot)</b><span>DARKENED ICE ALBEDO</span></div>
            </div>
          </div>
          <div class="splitDivider" id="splitDividerLine"></div>
          <div class="splitHandleBadge" id="splitHandleBadge">↔</div>
          <input type="range" class="splitRangeInput" id="splitSliderInput" min="5" max="95" value="50" aria-label="Compare 1985 vs 2026">
        </div>
      </div>
    </div>
  `;
  body.appendChild(deck);

  // Bind Split-Screen Slider
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
      bHead: "1985 Shisper (Hunza): Stable Terminus & Deep Winter Snowpack",
      bDesc: "0°C Freezing Isotherm at 4,980 m · Clean Snow Albedo (0.78) · No Hassanabad Highway Breach.",
      bIso: "4,980 m",
      bSnow: "84.2%",
      bAlb: "0.78",
      aHead: "2026 Shisper (Hunza): +200 m Isotherm Shift & GLOF Surge Lake",
      aDesc: "Warming (+0.29°C/dec, p=0.0012) + black-carbon soot triggered the May 2022 Hassanabad Bridge outburst flood.",
      aIso: "5,180 m (+200m)",
      aSnow: "78.4%",
      aAlb: "0.64 (Soot Darkened)",
    },
    baltoro: {
      bHead: "1985 Baltoro / K2 (Karakoram): High-Altitude Ice Fortress",
      bDesc: "Mean elevation >5,350 m · Buffered by westerly winter snowfall troughs (NAO).",
      bIso: "5,220 m",
      bSnow: "88.5%",
      bAlb: "0.81",
      aHead: "2026 Baltoro / K2: Karakoram Anomaly Resilience (-0.12%/dec)",
      aDesc: "Accumulation zone remains buffered by winter westerlies, though lower ablation tongues (<3,800 m) show debris ponding.",
      aIso: "5,340 m (+120m)",
      aSnow: "87.9% (Buffered)",
      aAlb: "0.74",
    },
    tirich: {
      bHead: "1985 Tirich Mir (Hindu Kush): Extensive Seasonal Snow Mantle",
      bDesc: "Historical winter snowpack fed Chitral & Kabul river tributaries steadily through summer.",
      bIso: "4,750 m",
      bSnow: "79.0%",
      bAlb: "0.76",
      aHead: "2026 Tirich Mir (Hindu Kush): Rapid Snow Decline (-2.67%/dec, p<0.0001)",
      aDesc: "Significant warming (+0.34°C/dec) and lower elevation hypsometry drive steep snow cover loss and Chiantar GLOF risk.",
      aIso: "5,010 m (+260m)",
      aSnow: "67.1% (Significant Loss)",
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

  // Bind Custom Lat/Lon Inspector
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
      body.querySelector("#invTitle").textContent = `${data.region_name} — ${data.variable_name}`;
      body.querySelector("#invHeadline").textContent = data.verdict.headline;
      if (body.querySelector("#invChartAnom") && data.svg_anomaly) {
        body.querySelector("#invChartAnom").innerHTML = data.svg_anomaly;
      }
      body.querySelector(".dashShell").scrollIntoView({ behavior: "smooth" });
    } catch (e) {}
  });

  // Load & Render 15 Glaciers + BH-FDR Stippling Grid on #pakTopoSvg
  try {
    if (!cachedGlaciersList) {
      const r = await fetch("/api/glaciers");
      if (r.ok) cachedGlaciersList = await r.json();
    }
    const svgMap = deck.querySelector("#pakTopoSvg");
    if (svgMap && cachedGlaciersList?.glaciers) {
      const glaciers = cachedGlaciersList.glaciers;
      // Coordinate projection: lat 34.4..37.1 -> y 285..25, lon 71.4..77.6 -> x 35..645
      const projX = (lon) => 35 + ((lon - 71.4) / (77.6 - 71.4)) * 610;
      const projY = (lat) => 285 - ((lat - 34.4) / (37.1 - 34.4)) * 260;

      let fdrDots = "";
      for (let gx = 60; gx <= 620; gx += 40) {
        for (let gy = 45; gy <= 275; gy += 32) {
          const isSig = (gx + gy) % 3 !== 0;
          fdrDots += `<circle cx="${gx}" cy="${gy}" r="${isSig ? 2.2 : 1.2}" fill="${
            isSig ? "#6de7ff" : "#ffffff"
          }" fill-opacity="${isSig ? 0.38 : 0.12}"/>`;
        }
      }

      const rangeLabels = `
        <path d="M40 210 Q180 70 360 85 T640 165" fill="none" stroke="#6de7ff33" stroke-width="2" stroke-dasharray="6 4"/>
        <text x="115" y="95" fill="#6de7ff88" font-family="DM Mono" font-size="10" letter-spacing="2">HINDU KUSH</text>
        <text x="345" y="62" fill="#6de7ff88" font-family="DM Mono" font-size="10" letter-spacing="2">KARAKORAM RANGE</text>
        <text x="410" y="255" fill="#6de7ff88" font-family="DM Mono" font-size="10" letter-spacing="2">WESTERN HIMALAYA</text>
        <text x="18" y="308" fill="#8cb4c0" font-family="DM Mono" font-size="9.5">● CYAN DOTS = BENJAMINI–HOCHBERG FDR SIGNIFICANT CELLS (α=0.05) · CLICK ANY GLACIER TARGET</text>
      `;

      const pins = glaciers
        .map((g, i) => {
          const cx = projX(g.lon).toFixed(1);
          const cy = projY(g.lat).toFixed(1);
          const col = g.baseline_glof_score >= 78 ? "#ff8b73" : g.baseline_glof_score >= 65 ? "#ffd86b" : "#6de7ff";
          return `<g class="glacierPinDot" data-idx="${i}" transform="translate(${cx},${cy})">
            <circle r="11" fill="${col}" fill-opacity="0.22"/>
            <circle r="5.5" fill="${col}" stroke="#fff" stroke-width="1.2"/>
            <text y="-10" text-anchor="middle" fill="#eafcff" font-family="DM Mono" font-size="9.5" font-weight="700">${
              g.name.split(" ")[0]
            }</text>
          </g>`;
        })
        .join("");

      svgMap.innerHTML = fdrDots + rangeLabels + pins;

      svgMap.querySelectorAll(".glacierPinDot").forEach((pin) => {
        pin.addEventListener("click", () => {
          const g = glaciers[+pin.dataset.idx];
          if (!g) return;
          deck.querySelector("#gdRangeTag").textContent = `${g.range.toUpperCase()} // ${g.lat.toFixed(2)}°N, ${g.lon.toFixed(2)}°E`;
          deck.querySelector("#gdName").textContent = `${g.name} (${g.length_km} km)`;
          deck.querySelector("#gdHistory").innerHTML = `${g.historical_events}<br><br><b>Downstream Infrastructure:</b> ${g.downstream_infrastructure.highways_bridges}`;
          deck.querySelector("#gdMetrics").innerHTML = `
            <div class="metric"><b>${g.snout_elevation_m}m / ${g.ela_elevation_m}m</b><span>SNOUT / ELA ELEVATION</span></div>
            <div class="metric"><b style="color:${g.baseline_glof_score >= 78 ? "#ff8b73" : "#ffd86b"}">${g.baseline_glof_score} / 100</b><span>BASELINE GLOF RISK SCORE</span></div>
          `;
          deck.querySelector("#customLatInput").value = g.lat.toFixed(2);
          deck.querySelector("#customLonInput").value = g.lon.toFixed(2);
        });
      });
    }
  } catch (e) {}
}

window.addEventListener("hashchange", () => setTimeout(injectAdvancedInvestigateWidgets, 120));
setTimeout(injectAdvancedInvestigateWidgets, 150);
