"""
User Interface & Visualization package for Himalaya Trend Lab (Layer 5).
"""
from ui.charts import render_series_svg, render_climatology_svg
from ui.maps import build_spatial_map_payload
from ui.walkthroughs import DEMO_WALKTHROUGHS
from ui.missions_view import get_missions_payload
from ui.playground import run_sandbox_simulation
from ui.glossary import GLOSSARY_TERMS, SCIENTIFIC_LIMITATIONS

__all__ = [
    "render_series_svg",
    "render_climatology_svg",
    "build_spatial_map_payload",
    "DEMO_WALKTHROUGHS",
    "get_missions_payload",
    "run_sandbox_simulation",
    "GLOSSARY_TERMS",
    "SCIENTIFIC_LIMITATIONS",
]
