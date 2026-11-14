"""
SVG Chart Generators for the Hatchable Frontend (`#homeChart`, `.chart`).
Generates high-resolution responsive `<svg>` line, confidence-band, seasonal bar,
and multi-series charts with embedded telemetry data attributes (`data-series`)
for interactive laser-crosshair hover tooltips in the browser.
"""
import json
from typing import List, Optional
import numpy as np
import pandas as pd


def render_series_svg(
    values: List[float],
    trend: Optional[List[float]] = None,
    ci_low: Optional[List[float]] = None,
    ci_high: Optional[List[float]] = None,
    label_left: str = "MONTHLY ANOMALY + SEN'S SLOPE",
    label_right: str = "1981 → 2026",
    stroke_color: str = "#9df4ff",
    trend_color: str = "#f2c56b",
) -> str:
    """
    Render a responsive `<svg viewBox="0 0 900 250">` with:
    - Shaded 95% confidence interval band (if `ci_low` & `ci_high` provided)
    - Filled area gradient under the anomaly/value curve
    - Crisp polyline for the primary series
    - Dashed/solid line for Sen's slope / GPR trend
    - Embedded `data-series` JSON for interactive laser crosshair & hover tooltips
    """
    arr = np.array(values, dtype=float)
    if len(arr) < 2:
        return '<svg viewBox="0 0 900 250" preserveAspectRatio="none"></svg>'

    # Downsample to max 140 points for crisp SVG rendering and fast hover scrubbing
    step = max(1, len(arr) // 140)
    idx = np.arange(0, len(arr), step)
    s_vals = arr[idx]

    all_vals = [s_vals]
    s_trend = np.array(trend, dtype=float)[idx] if trend is not None and len(trend) == len(arr) else None
    s_low = np.array(ci_low, dtype=float)[idx] if ci_low is not None and len(ci_low) == len(arr) else None
    s_high = np.array(ci_high, dtype=float)[idx] if ci_high is not None and len(ci_high) == len(arr) else None

    if s_trend is not None:
        all_vals.append(s_trend)
    if s_low is not None:
        all_vals.append(s_low)
    if s_high is not None:
        all_vals.append(s_high)

    flat = np.concatenate(all_vals)
    vmin = float(np.nanmin(flat))
    vmax = float(np.nanmax(flat))
    span = max(1e-6, vmax - vmin)

    w = 900.0
    h = 250.0
    pad_top = 34.0
    pad_bot = 26.0
    usable_h = h - pad_top - pad_bot

    def to_xy(series_arr: np.ndarray) -> List[tuple]:
        n = len(series_arr)
        pts = []
        for i, val in enumerate(series_arr):
            x = (i / max(1, n - 1)) * w
            norm = (float(val) - vmin) / span
            y = pad_top + usable_h * (1.0 - norm)
            pts.append((round(x, 1), round(y, 1)))
        return pts

    val_pts = to_xy(s_vals)
    val_path = "M" + " L".join(f"{x} {y}" for x, y in val_pts)
    area_path = f"{val_path} L{w:.0f} {h:.0f} L0 {h:.0f}Z"

    ci_poly = ""
    if s_low is not None and s_high is not None:
        low_pts = to_xy(s_low)
        high_pts = to_xy(s_high)
        ci_coords = high_pts + list(reversed(low_pts))
        ci_d = "M" + " L".join(f"{x} {y}" for x, y in ci_coords) + "Z"
        ci_poly = f'<path d="{ci_d}" fill="#6de7ff" fill-opacity="0.13" stroke="none"/>'

    trend_svg = ""
    if s_trend is not None:
        t_pts = to_xy(s_trend)
        t_d = "M" + " L".join(f"{x} {y}" for x, y in t_pts)
        trend_svg = f'<path d="{t_d}" fill="none" stroke="{trend_color}" stroke-width="2.5" stroke-dasharray="7 4"/>'

    # Zero line if vmin < 0 < vmax
    zero_svg = ""
    if vmin < 0 < vmax:
        z_norm = (0.0 - vmin) / span
        zy = round(pad_top + usable_h * (1.0 - z_norm), 1)
        zero_svg = f'<line x1="0" y1="{zy}" x2="900" y2="{zy}" stroke="#ffffff22" stroke-width="1" stroke-dasharray="3 3"/>'

    hover_payload = {
        "v": [round(float(x), 2) for x in s_vals],
        "t": [round(float(x), 2) for x in s_trend] if s_trend is not None else [],
        "lo": [round(float(x), 2) for x in s_low] if s_low is not None else [],
        "hi": [round(float(x), 2) for x in s_high] if s_high is not None else [],
        "left": label_left,
        "right": label_right,
    }
    encoded = json.dumps(hover_payload).replace('"', "&quot;")

    return (
        f'<svg class="interactiveSvg" data-series="{encoded}" viewBox="0 0 900 250" preserveAspectRatio="none">'
        '<defs><linearGradient id="g" x1="0" x2="0" y1="0" y2="1">'
        f'<stop stop-color="{stroke_color}" stop-opacity=".46"/>'
        f'<stop offset="1" stop-color="{stroke_color}" stop-opacity="0"/>'
        "</linearGradient></defs>"
        f"{zero_svg}"
        f"{ci_poly}"
        f'<path d="{area_path}" fill="url(#g)"/>'
        f'<path d="{val_path}" fill="none" stroke="{stroke_color}" stroke-width="2.2"/>'
        f"{trend_svg}"
        f'<text x="14" y="20" fill="#6de7ff" font-family="DM Mono, monospace" font-size="11" letter-spacing="1.4">{label_left}</text>'
        f'<text x="886" y="20" text-anchor="end" fill="#8fa8b3" font-family="DM Mono, monospace" font-size="11" letter-spacing="1.4">{label_right}</text>'
        "</svg>"
    )


def render_climatology_svg(clim_df: pd.DataFrame, units: str) -> str:
    """Render 12-month seasonal climatology bar + curve SVG with interactive hover payload."""
    col = "clim_mean" if "clim_mean" in clim_df.columns else "mean"
    means = clim_df[col].values.astype(float)
    months = clim_df["month_name"].tolist()
    vmin = float(np.min(means))
    vmax = float(np.max(means))
    span = max(1e-6, vmax - vmin)

    bars = []
    pts = []
    for i, (m_name, val) in enumerate(zip(months, means)):
        x_center = 55 + i * 70
        norm = (val - vmin) / span
        bar_h = 25 + norm * 145
        y_top = 215 - bar_h
        pts.append((x_center, round(y_top, 1)))
        bars.append(
            f'<rect class="climBar" data-month="{m_name}" data-val="{val:.2f} {units}" '
            f'x="{x_center - 18}" y="{y_top:.1f}" width="36" height="{bar_h:.1f}" rx="5" fill="#19b9df" fill-opacity="0.34" stroke="#6de7ff" stroke-opacity="0.55"/>'
            f'<text x="{x_center}" y="236" text-anchor="middle" fill="#8fa8b3" font-family="DM Mono, monospace" font-size="10">{m_name}</text>'
            f'<text x="{x_center}" y="{max(34, y_top - 6):.1f}" text-anchor="middle" fill="#dff9ff" font-family="DM Mono, monospace" font-size="9.5">{val:.1f}</text>'
        )

    line_d = "M" + " L".join(f"{x} {y}" for x, y in pts)
    hover_payload = {
        "v": [round(float(x), 2) for x in means],
        "t": [round(float(x), 2) for x in means],
        "months": months,
        "left": f"12-MONTH SEASONAL CLIMATOLOGY ({units})",
        "right": "JAN → DEC CYCLE",
    }
    encoded = json.dumps(hover_payload).replace('"', "&quot;")

    return (
        f'<svg class="interactiveSvg" data-series="{encoded}" viewBox="0 0 900 250" preserveAspectRatio="none">'
        + "".join(bars)
        + f'<path d="{line_d}" fill="none" stroke="#f2c56b" stroke-width="2.2"/>'
        + f'<text x="14" y="20" fill="#6de7ff" font-family="DM Mono, monospace" font-size="11" letter-spacing="1.4">12-MONTH SEASONAL CLIMATOLOGY ({units})</text>'
        + '<text x="886" y="20" text-anchor="end" fill="#f2c56b" font-family="DM Mono, monospace" font-size="11" letter-spacing="1.4">REMOVED BEFORE TREND TEST</text>'
        + "</svg>"
    )
