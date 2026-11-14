"""
Catalogue of 15 Iconic Individual Glaciers & GLOF Hazard Hotspots of Pakistan.
Includes exact coordinates, snout & peak elevations, Equilibrium Line Altitude (ELA),
length, area, surge/retreat status, documented GLOF history, and the
Downstream Infrastructure & Community Vulnerability Ledger (KKH, bridges, hydropower, villages).
"""
from typing import Dict, Any, List

GLACIER_HOTSPOTS: Dict[str, Dict[str, Any]] = {
    "shisper": {
        "id": "shisper",
        "name": "Shisper Glacier & Hassanabad Lake",
        "basin_id": "hunza",
        "range": "Karakoram",
        "lat": 36.3650,
        "lon": 74.5680,
        "length_km": 16.5,
        "area_km2": 31.8,
        "snout_elevation_m": 2520,
        "ela_elevation_m": 4850,
        "peak_elevation_m": 7611,  # Shispare Peak
        "behavior_type": "Surging Glacier & Ice-Dammed GLOF Hotspot",
        "glof_risk_level": "Critical",
        "baseline_glof_score": 89,
        "downstream_infrastructure": {
            "highways_bridges": "Karakoram Highway (N-35) & Hassanabad Steel/Concrete Bridge",
            "power_water_assets": "Hassanabad 1.8 MW Micro-Hydel Powerhouse & Aliabad Irrigation Channels",
            "communities_at_risk": "Hassanabad, Murtazaabad & Lower Hunza river-terrace settlements (~8,500 residents)",
            "strategic_corridor": "CPEC Cross-Border Trade & Pakistan-China Fiber Optic Cable Route",
        },
        "historical_events": [
            "2018–2019: Rapid surge blocked the Muchuhar valley stream, forming a large ice-dammed supra-glacial/marginal lake.",
            "June 2019 & May 2020: Major Glacial Lake Outburst Floods (GLOFs) damaged Karakoram Highway infrastructure.",
            "May 7, 2022: Record spring heatwave (+6.2°C anomaly) triggered a catastrophic GLOF that destroyed the historic Hassanabad Bridge on the Karakoram Highway."
        ],
        "summary": (
            "Pakistan's most closely monitored GLOF hazard site in Hunza. When Shisper surges "
            "and blocks meltwater from the neighbouring Muchuhar glacier valley, rising spring "
            "temperatures rapidly fill and breach the ice dam above Hassanabad village."
        ),
    },
    "baltoro": {
        "id": "baltoro",
        "name": "Baltoro Glacier & Concordia (K2 Sector)",
        "basin_id": "karakoram",
        "range": "Karakoram",
        "lat": 35.7360,
        "lon": 76.3820,
        "length_km": 63.0,
        "area_km2": 754.0,
        "snout_elevation_m": 3410,
        "ela_elevation_m": 5180,
        "peak_elevation_m": 8611,  # K2
        "behavior_type": "Debris-Covered Giant / Karakoram Anomaly Core",
        "glof_risk_level": "Moderate",
        "baseline_glof_score": 52,
        "downstream_infrastructure": {
            "highways_bridges": "Askole–Shigar Valley Road & Braldu Suspension Bridges",
            "power_water_assets": "Shigar River Headworks & Skardu Basin Inflow System",
            "communities_at_risk": "Askole, Korphe, टेस्ट/Braldu Gorge & Shigar Valley (~42,000 residents)",
            "strategic_corridor": "Central Karakoram National Park (CKNP) & K2 International Trekking Corridor",
        },
        "historical_events": [
            "2000–2018: Classic example of the 'Karakoram Anomaly', maintaining near-neutral mass balance due to high elevation and thick supraglacial debris insulation.",
            "2020–2025: Expansion of supraglacial melt ponds near Urdukas and Gore II during extreme July–August heat anomalies."
        ],
        "summary": (
            "Draining K2 (8,611 m), Broad Peak, and the Gasherbrum massif into the Shigar/Indus "
            "River, Baltoro is one of the largest non-polar glaciers on Earth. Thick rock debris "
            "on its lower tongue insulates ice, while high accumulation zones capture winter westerlies."
        ),
    },
    "siachen": {
        "id": "siachen",
        "name": "Siachen Glacier (Eastern Karakoram)",
        "basin_id": "karakoram",
        "range": "Karakoram",
        "lat": 35.4210,
        "lon": 77.1090,
        "length_km": 76.0,
        "area_km2": 1056.0,
        "snout_elevation_m": 3620,
        "ela_elevation_m": 5250,
        "peak_elevation_m": 7742,  # Saltoro Kangri
        "behavior_type": "Continental Valley Glacier",
        "glof_risk_level": "Moderate",
        "baseline_glof_score": 48,
        "downstream_infrastructure": {
            "highways_bridges": "Shyok–Khaplu Valley Bridges & Indus Confluence Crossings",
            "power_water_assets": "Shyok River Tributary Inflows to Upper Indus / Tarbela System",
            "communities_at_risk": "Nubra–Shyok & Ghanche/Khaplu downstream floodplain communities",
            "strategic_corridor": "Eastern Karakoram High-Altitude Transboundary Water Headwaters",
        },
        "historical_events": [
            "1980–2024: Gradual snout thinning accompanied by rising summer minimum temperatures above 5,000 m."
        ],
        "summary": (
            "The longest glacier in the Karakoram (76 km) and second-longest in the non-polar "
            "world, feeding the Nubra and Shyok tributaries of the Upper Indus Basin."
        ),
    },
    "biafo": {
        "id": "biafo",
        "name": "Biafo Glacier (Snow Lake Corridor)",
        "basin_id": "karakoram",
        "range": "Karakoram",
        "lat": 35.8800,
        "lon": 75.6200,
        "length_km": 67.0,
        "area_km2": 560.0,
        "snout_elevation_m": 3120,
        "ela_elevation_m": 4950,
        "peak_elevation_m": 7285,  # Baintha Brakk
        "behavior_type": "High-Accumulation Basin Glacier",
        "glof_risk_level": "Moderate",
        "baseline_glof_score": 46,
        "downstream_infrastructure": {
            "highways_bridges": "Braldu Trail Bridges & Askole Access Link",
            "power_water_assets": "Biafo–Braldu Meltwater Channel feeding Shigar/Indus",
            "communities_at_risk": "Askole & Upper Braldu settlements (~4,200 residents)",
            "strategic_corridor": "Lukpe Lawo (Snow Lake) High-Altitude Water Reservoir",
        },
        "historical_events": [
            "Forms a 100+ km continuous glacial highway with Hispar Glacier across the Hispar La pass (5,128 m) at Lukpe Lawo (Snow Lake)."
        ],
        "summary": (
            "Fed by the vast Lukpe Lawo ('Snow Lake') high-altitude accumulation basin, Biafo "
            "is a prime benchmark for measuring winter westerly snowfall trends in the central Karakoram."
        ),
    },
    "hispar": {
        "id": "hispar",
        "name": "Hispar Glacier (Nagar Valley)",
        "basin_id": "hunza",
        "range": "Karakoram",
        "lat": 36.1200,
        "lon": 75.1500,
        "length_km": 49.0,
        "area_km2": 343.0,
        "snout_elevation_m": 3050,
        "ela_elevation_m": 4900,
        "peak_elevation_m": 7885,  # Distaghil Sar
        "behavior_type": "Debris-Mantled Tributary Surge System",
        "glof_risk_level": "High",
        "baseline_glof_score": 68,
        "downstream_infrastructure": {
            "highways_bridges": "Hispar–Nagar Valley Link Road & Huru Bridge",
            "power_water_assets": "Nagar Hydel Intakes & Terraced Gravity Irrigation Canals",
            "communities_at_risk": "Hispar, Hoper & Nagar Khas villages (~19,000 residents)",
            "strategic_corridor": "Hispar River Confluence with Hunza River (KKH Corridor)",
        },
        "historical_events": [
            "2015–2021: Tributary surges (Khani Basa & Yutmaru) altered surface melt drainage channels feeding the Hispar River."
        ],
        "summary": (
            "Flowing westward from Hispar Pass into the Nagar/Hunza basin, Hispar features "
            "heavy debris cover and active surging tributaries sensitive to warm-season rain-on-snow events."
        ),
    },
    "batura": {
        "id": "batura",
        "name": "Batura Glacier (Upper Hunza / Gojal)",
        "basin_id": "hunza",
        "range": "Karakoram",
        "lat": 36.5600,
        "lon": 74.6200,
        "length_km": 57.0,
        "area_km2": 290.0,
        "snout_elevation_m": 2560,
        "ela_elevation_m": 4820,
        "peak_elevation_m": 7795,  # Batura Sar
        "behavior_type": "Low-Snout Valley Glacier",
        "glof_risk_level": "High",
        "baseline_glof_score": 64,
        "downstream_infrastructure": {
            "highways_bridges": "Karakoram Highway (N-35) Batura Snout Embankment & Passu Bridges",
            "power_water_assets": "Gojal Irrigation Intakes & Cross-Border Optical Fiber Conduit",
            "communities_at_risk": "Passu, Khyber & Batura low-terrace settlements (~6,000 residents)",
            "strategic_corridor": "Direct KKH Terminus Contact Zone (2 km from Highway)",
        },
        "historical_events": [
            "Terminates immediately adjacent to the Karakoram Highway near Passu, making highway infrastructure sensitive to sub-glacial outburst channels."
        ],
        "summary": (
            "One of the largest glaciers outside the polar regions reaching down to 2,560 m "
            "elevation, where strong vertical temperature gradients drive rapid lower-tongue ablation."
        ),
    },
    "passu": {
        "id": "passu",
        "name": "Passu Glacier (Gojal / Upper Hunza)",
        "basin_id": "hunza",
        "range": "Karakoram",
        "lat": 36.4580,
        "lon": 74.8450,
        "length_km": 21.5,
        "area_km2": 58.4,
        "snout_elevation_m": 2610,
        "ela_elevation_m": 4780,
        "peak_elevation_m": 7478,  # Passu Sar
        "behavior_type": "Clean-Ice Retreating Tongue with Proglacial Lake",
        "glof_risk_level": "High",
        "baseline_glof_score": 74,
        "downstream_infrastructure": {
            "highways_bridges": "Karakoram Highway (N-35) Passu Section & Suspension Bridges",
            "power_water_assets": "Passu Community Hydel & Orchard Water Channels",
            "communities_at_risk": "Passu Village & Hussaini riverside terraces (~3,500 residents)",
            "strategic_corridor": "Upper Hunza Eco-Tourism & KKH Retaining Wall Zone",
        },
        "historical_events": [
            "Historical GLOF outbursts from the Passu proglacial lake have eroded agricultural terraces in Passu village and threatened the Karakoram Highway."
        ],
        "summary": (
            "Unlike debris-covered neighbours, Passu has a bright clean-ice tongue that responds "
            "rapidly to summer radiative warming and proglacial lake expansion."
        ),
    },
    "ghulkin": {
        "id": "ghulkin",
        "name": "Ghulkin Glacier (Upper Hunza)",
        "basin_id": "hunza",
        "range": "Karakoram",
        "lat": 36.4250,
        "lon": 74.8320,
        "length_km": 18.2,
        "area_km2": 32.0,
        "snout_elevation_m": 2510,
        "ela_elevation_m": 4720,
        "peak_elevation_m": 7388,  # Ultar / Bojohaghur massif
        "behavior_type": "Debris-Covered Conduit Outburst Glacier",
        "glof_risk_level": "High",
        "baseline_glof_score": 72,
        "downstream_infrastructure": {
            "highways_bridges": "KKH Ghulkin–Hussaini Causeway & Local Link Roads",
            "power_water_assets": "Ghulkin & Gulmit Meltwater Irrigation Networks",
            "communities_at_risk": "Ghulkin, Hussaini & Gulmit (Gojal headquarters, ~9,200 residents)",
            "strategic_corridor": "Attabad–Gojal Transport & Agricultural Belt",
        },
        "historical_events": [
            "2008: Five sequential englacially routed outburst floods in a single summer season disrupted Upper Hunza transport and irrigation."
        ],
        "summary": (
            "Steep debris-covered glacier whose snout sits directly above settled villages and "
            "orchards in Gojal, prone to sudden water-pocket drainage during heatwaves."
        ),
    },
    "hopar": {
        "id": "hopar",
        "name": "Hopar (Bualtar & Barpu) Glaciers",
        "basin_id": "hunza",
        "range": "Karakoram",
        "lat": 36.1850,
        "lon": 74.7650,
        "length_km": 22.0,
        "area_km2": 92.0,
        "snout_elevation_m": 2380,
        "ela_elevation_m": 4680,
        "peak_elevation_m": 7027,  # Spantik (Golden Peak)
        "behavior_type": "Rapid-Flow Surge Glacier",
        "glof_risk_level": "Moderate",
        "baseline_glof_score": 59,
        "downstream_infrastructure": {
            "highways_bridges": "Hopar–Nagar Access Road & Hispar River Bridges",
            "power_water_assets": "Hopar Valley Terraced Wheat/Apricot Irrigation Canals",
            "communities_at_risk": "Hopar cluster villages (Holshal, Ghoshushal, ~11,000 residents)",
            "strategic_corridor": "Lowest-Elevation Glacier Terminus Zone in Karakoram (2,380 m)",
        },
        "historical_events": [
            "Reaches one of the lowest elevations in the Karakoram (2,380 m), directly bordering agricultural terraces of Nagar Valley."
        ],
        "summary": (
            "Because its terminus sits below 2,400 m in Nagar Valley, Hopar experiences "
            "one of the longest summer melt seasons in northern Pakistan."
        ),
    },
    "hinarchi": {
        "id": "hinarchi",
        "name": "Hinarchi Glacier (Bagrot Valley)",
        "basin_id": "gilgit",
        "range": "Karakoram",
        "lat": 36.0420,
        "lon": 74.5620,
        "length_km": 17.8,
        "area_km2": 44.5,
        "snout_elevation_m": 2580,
        "ela_elevation_m": 4650,
        "peak_elevation_m": 7788,  # Rakaposhi South Face
        "behavior_type": "Avalanche-Fed Valley Glacier",
        "glof_risk_level": "High",
        "baseline_glof_score": 71,
        "downstream_infrastructure": {
            "highways_bridges": "Bagrot Valley Road, Taisot & Sinaker Bridges (towards Gilgit City)",
            "power_water_assets": "Bagrot Hydro-Electric Stations & UNDP Automated Early Warning Sensors",
            "communities_at_risk": "Chirah, Farfu, Bulchi & Danyore/Gilgit confluence (~28,000 residents)",
            "strategic_corridor": "Primary Fresh-Water & Agricultural Supplier to Gilgit Capital",
        },
        "historical_events": [
            "2021–2023: Supraglacial lake formation and flash floods in Bagrot Valley, a flagship UNDP/Ministry of Climate Change GLOF-II early-warning site."
        ],
        "summary": (
            "Fed by steep ice avalanches off the south face of Rakaposhi (7,788 m), Hinarchi "
            "supplies Bagrot and Gilgit valleys and exhibits high sensitivity to spring rain-on-snow."
        ),
    },
    "darkot": {
        "id": "darkot",
        "name": "Darkot & Gamubar Glaciers (Yasin / Ghizer)",
        "basin_id": "gilgit",
        "range": "Hindu Kush-Karakoram Transition",
        "lat": 36.6520,
        "lon": 73.4180,
        "length_km": 14.2,
        "area_km2": 36.0,
        "snout_elevation_m": 3180,
        "ela_elevation_m": 4620,
        "peak_elevation_m": 6870,
        "behavior_type": "Moraine-Dammed Lake System",
        "glof_risk_level": "High",
        "baseline_glof_score": 76,
        "downstream_infrastructure": {
            "highways_bridges": "Yasin–Gupis Highway, Darkot Bridge & Ishkoman Valley Roads",
            "power_water_assets": "Ghizer River Hydel Plants & Gupis/Punial Irrigation Intakes",
            "communities_at_risk": "Darkot, Hundur, Taus & Badswat villages (~24,000 residents)",
            "strategic_corridor": "Gilgit–Chitral Alternate Highway Corridor",
        },
        "historical_events": [
            "July 2018 & July 2021: Severe GLOF and debris-flow events in Ishkoman (Badswat) and Yasin valleys blocked the river and formed temporary lakes."
        ],
        "summary": (
            "Located in the Hindu Raj / eastern Hindu Kush transition zone where retreating "
            "glacier tongues leave behind unstable moraine-dammed lakes."
        ),
    },
    "chiantar": {
        "id": "chiantar",
        "name": "Chiantar Glacier (Broghil / Upper Yarkhun)",
        "basin_id": "chitral",
        "range": "Hindu Kush",
        "lat": 36.7350,
        "lon": 73.7900,
        "length_km": 34.0,
        "area_km2": 265.0,
        "snout_elevation_m": 3680,
        "ela_elevation_m": 4790,
        "peak_elevation_m": 6416,
        "behavior_type": "Retreating Hindu Kush Headwater Glacier",
        "glof_risk_level": "High",
        "baseline_glof_score": 73,
        "downstream_infrastructure": {
            "highways_bridges": "Upper Yarkhun Valley Track & Mastuj–Booni River Bridges",
            "power_water_assets": "Chitral/Mastuj River Headwaters & Micro-Hydel Intakes",
            "communities_at_risk": "Lashkargaz, Kishmanja, Brep & Mastuj (~31,000 residents)",
            "strategic_corridor": "Broghil National Park & Wakhan/Pamir Headwater Divide",
        },
        "historical_events": [
            "Primary glacial source of the Yarkhun/Chitral River; documented steady terminus retreat and negative mass balance since 2000."
        ],
        "summary": (
            "The largest glacier of the eastern Hindu Kush headwaters. Unlike central Karakoram "
            "giants, Chiantar shows clear, statistically significant snow-cover decline and thinning."
        ),
    },
    "tirich": {
        "id": "tirich",
        "name": "Tirich Mir & Reshun Glaciers (Chitral)",
        "basin_id": "chitral",
        "range": "Hindu Kush",
        "lat": 36.2850,
        "lon": 71.8800,
        "length_km": 29.0,
        "area_km2": 198.0,
        "snout_elevation_m": 3340,
        "ela_elevation_m": 4750,
        "peak_elevation_m": 7708,  # Tirich Mir
        "behavior_type": "Retreating High-Relief Hindu Kush Glacier",
        "glof_risk_level": "Critical",
        "baseline_glof_score": 84,
        "downstream_infrastructure": {
            "highways_bridges": "Chitral–Booni–Shandur Highway & Reshun Steel Bridge",
            "power_water_assets": "4.2 MW Reshun Hydropower Station & Golen Gol 108 MW Hydropower Plant",
            "communities_at_risk": "Reshun, Booni, Golain & Mulkhow valleys (~55,000 residents)",
            "strategic_corridor": "Upper & Lower Chitral Main Energy and Drinking Water Lifeline",
        },
        "historical_events": [
            "July 2015 & July 2019: Compound heatwaves and unseasonal monsoon cloudbursts triggered devastating GLOFs in Reshun, Booni, and Golain (Chitral)."
        ],
        "summary": (
            "Draining Tirich Mir (7,708 m, highest peak of the Hindu Kush), this system is "
            "acutely vulnerable when summer monsoon moisture intrudes westward into warm Hindu Kush valleys."
        ),
    },
    "raikot": {
        "id": "raikot",
        "name": "Raikot Glacier (Nanga Parbat North Face)",
        "basin_id": "astore",
        "range": "Western Himalaya",
        "lat": 35.3180,
        "lon": 74.5950,
        "length_km": 15.2,
        "area_km2": 39.0,
        "snout_elevation_m": 3180,
        "ela_elevation_m": 4600,
        "peak_elevation_m": 8126,  # Nanga Parbat
        "behavior_type": "Ultra-Steep Himalayan Icefall Glacier",
        "glof_risk_level": "High",
        "baseline_glof_score": 69,
        "downstream_infrastructure": {
            "highways_bridges": "Karakoram Highway (N-35) Raikot Bridge & Tato Mountain Road",
            "power_water_assets": "Direct Indus Gorge Inflow upstream of Diamer-Bhasha (4,500 MW) & Dasu (4,320 MW) Dams",
            "communities_at_risk": "Tato, Jhel, Fairy Meadows & Raikot Gorge (~6,800 residents)",
            "strategic_corridor": "Diamer-Bhasha Reservoir Upstream Sediment & Meltwater Input",
        },
        "historical_events": [
            "Drops nearly 5,000 vertical meters over just 15 km from the summit of Nanga Parbat (8,126 m) to Fairy Meadows (3,180 m)."
        ],
        "summary": (
            "One of the steepest vertical relief glaciers on Earth. Lower-elevation Himalayan "
            "warming has pushed its summer freezing line significantly higher over the past 30 years."
        ),
    },
    "rupal": {
        "id": "rupal",
        "name": "Rupal & Bazhin Glaciers (Astore / Nanga Parbat South)",
        "basin_id": "astore",
        "range": "Western Himalaya",
        "lat": 35.1620,
        "lon": 74.6250,
        "length_km": 17.5,
        "area_km2": 56.0,
        "snout_elevation_m": 3520,
        "ela_elevation_m": 4640,
        "peak_elevation_m": 8126,  # Nanga Parbat Rupal Face
        "behavior_type": "Monsoon-Exposed Himalayan Valley Glacier",
        "glof_risk_level": "High",
        "baseline_glof_score": 70,
        "downstream_infrastructure": {
            "highways_bridges": "Astore–Tarashing Valley Road & Gorikot Bridges",
            "power_water_assets": "Astore River Hydropower Stations & Indus Confluence Inflows",
            "communities_at_risk": "Tarashing, Rupal, Churit & Astore Valley (~38,000 residents)",
            "strategic_corridor": "Southern Nanga Parbat Monsoon Catchbasin",
        },
        "historical_events": [
            "Fed by the 4,600 m Rupal Face and exposed to direct South Asian summer monsoon moisture intrusion up the Astore River valley."
        ],
        "summary": (
            "Serves as the southern benchmark of the Western Himalaya in Pakistan, where "
            "rising temperatures and liquid summer rain accelerate seasonal snowpack loss."
        ),
    },
}


def get_glacier(glacier_id: str) -> Dict[str, Any]:
    """Retrieve a specific glacier hotspot by ID, defaulting to shisper."""
    return GLACIER_HOTSPOTS.get(glacier_id, GLACIER_HOTSPOTS["shisper"])


def get_glaciers_by_basin(basin_id: str = "All") -> List[Dict[str, Any]]:
    """Return list of glaciers belonging to a specific basin/range, or all glaciers."""
    if not basin_id or basin_id in ("All", "upper_indus"):
        return list(GLACIER_HOTSPOTS.values())
    matches = [
        g for g in GLACIER_HOTSPOTS.values()
        if g["basin_id"] == basin_id or g["range"].lower().replace(" ", "_") == basin_id
    ]
    return matches if matches else list(GLACIER_HOTSPOTS.values())
