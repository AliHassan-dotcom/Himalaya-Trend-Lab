"""
Scientific SVG Figure Generators for Himalaya Trend Lab.
Generates publication-style responsive `<svg>` line, confidence-band, and seasonal bar
figures with real X/Y axes, units, light gridlines, 12px+ tick labels, flat colorblind-safe
strokes (flat fills, no glow, no rounded bar tops), direct Sen's slope annotations,
keyboard accessibility, and embedded telemetry attributes (`data-series`).
"""
import html
import json
from typing import List, Optional
import numpy as np
import pandas as pd


def render_series_svg(
    values: List[float],
    trend: Optional[List[float]] = None,
    ci_low: Optional[List[float]] = None,
    ci_high: Optional[List[float]] = None,
    label_left: str = "Deseasonalized monthly anomaly and Sen slope",
    label_right: str = "1981 to 2026",
    stroke_color: str = "#58a6ff",
    trend_color: str = "#e06c3a",
    units: str = "",
    start_year: int = 1981,
    end_year: int = 2026,
    sen_annotation: str = "",
) -> str:
    """
    Render a scientific `<svg viewBox="0 0 900 270">` figure with:
    - Real Y-axis with 5 gridlines, tick marks, 12px numeric labels, and unit label
    - Real X-axis with year tick marks and 12px labels marking the period
    - Flat 95% confidence interval band (solid flat fill)
    - Flat polyline for observed anomaly/series
    - Dashed line for Sen's slope / model trend with direct on-chart label
    - Accessible `<title>`, `aria-label`, `tabindex="0"`, and `data-series` JSON
    """
    arr = np.array(values, dtype=float)
    if len(arr) < 2:
        return '<svg viewBox="0 0 900 270" role="img" aria-label="Empty chart"></svg>'

    # Downsample to max 140 points for crisp SVG rendering and responsive scrubbing
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
    pad_val = max(1e-4, (vmax - vmin) * 0.08)
    vmin -= pad_val
    vmax += pad_val
    span = max(1e-6, vmax - vmin)

    w = 900.0
    h = 270.0
    pad_left = 68.0
    pad_right = 24.0
    pad_top = 36.0
    pad_bot = 42.0
    plot_w = w - pad_left - pad_right
    plot_h = h - pad_top - pad_bot

    def to_xy(series_arr: np.ndarray) -> List[tuple]:
        n = len(series_arr)
        pts = []
        for i, val in enumerate(series_arr):
            x = pad_left + (i / max(1, n - 1)) * plot_w
            norm = (float(val) - vmin) / span
            y = pad_top + plot_h * (1.0 - norm)
            pts.append((round(x, 1), round(y, 1)))
        return pts

    # Y-axis gridlines and 12px tick labels
    grid_parts = []
    n_yticks = 5
    for ti in range(n_yticks):
        frac = ti / (n_yticks - 1)
        y_val = vmax - frac * span
        gy = round(pad_top + frac * plot_h, 1)
        grid_parts.append(
            f'<line x1="{pad_left}" y1="{gy}" x2="{w - pad_right}" y2="{gy}" stroke="#262e38" stroke-width="1"/>'
            f'<line x1="{pad_left - 5}" y1="{gy}" x2="{pad_left}" y2="{gy}" stroke="#484f58" stroke-width="1"/>'
            f'<text x="{pad_left - 8}" y="{gy + 4}" text-anchor="end" fill="#8b949e" font-family="DM Mono, monospace" font-size="12">{y_val:.1f}</text>'
        )

    # X-axis year ticks and 12px labels
    n_xticks = 6
    for xi in range(n_xticks):
        frac = xi / (n_xticks - 1)
        gx = round(pad_left + frac * plot_w, 1)
        yr_label = int(round(start_year + frac * (end_year - start_year)))
        y_axis_bottom = pad_top + plot_h
        grid_parts.append(
            f'<line x1="{gx}" y1="{y_axis_bottom}" x2="{gx}" y2="{y_axis_bottom + 5}" stroke="#484f58" stroke-width="1"/>'
            f'<text x="{gx}" y="{y_axis_bottom + 20}" text-anchor="middle" fill="#8b949e" font-family="DM Mono, monospace" font-size="12">{yr_label}</text>'
        )

    # Axes frame lines
    axes_svg = (
        f'<line x1="{pad_left}" y1="{pad_top}" x2="{pad_left}" y2="{pad_top + plot_h}" stroke="#484f58" stroke-width="1.2"/>'
        f'<line x1="{pad_left}" y1="{pad_top + plot_h}" x2="{w - pad_right}" y2="{pad_top + plot_h}" stroke="#484f58" stroke-width="1.2"/>'
    )

    # Zero reference line if vmin < 0 < vmax
    zero_svg = ""
    if vmin < 0 < vmax:
        z_norm = (0.0 - vmin) / span
        zy = round(pad_top + plot_h * (1.0 - z_norm), 1)
        zero_svg = f'<line x1="{pad_left}" y1="{zy}" x2="{w - pad_right}" y2="{zy}" stroke="#484f58" stroke-width="1" stroke-dasharray="4 4"/>'

    val_pts = to_xy(s_vals)
    val_path = "M" + " L".join(f"{x} {y}" for x, y in val_pts)

    ci_poly = ""
    if s_low is not None and s_high is not None:
        low_pts = to_xy(s_low)
        high_pts = to_xy(s_high)
        ci_coords = high_pts + list(reversed(low_pts))
        ci_d = "M" + " L".join(f"{x} {y}" for x, y in ci_coords) + "Z"
        ci_poly = f'<path d="{ci_d}" fill="{stroke_color}" fill-opacity="0.14" stroke="none"/>'

    trend_svg = ""
    slope_callout_svg = ""
    if s_trend is not None:
        t_pts = to_xy(s_trend)
        t_d = "M" + " L".join(f"{x} {y}" for x, y in t_pts)
        trend_svg = f'<path d="{t_d}" fill="none" stroke="{trend_color}" stroke-width="2.2" stroke-dasharray="6 4"/>'
        # Direct on-chart Sen slope annotation near end of trend line
        end_x, end_y = t_pts[-1]
        callout_text = sen_annotation
        if not callout_text and "SEN" in label_left.upper():
            parts = label_left.split(":", 1) if ":" in label_left else label_left.split(",", 1)
            callout_text = parts[-1].strip() if len(parts) > 1 else "Sen trend"
        if callout_text:
            cy = max(pad_top + 16, min(pad_top + plot_h - 10, end_y - 10))
            SafeCallout = html.escape(callout_text)
            slope_callout_svg = (
                f'<rect x="{end_x - 168}" y="{cy - 14}" width="164" height="20" rx="3" fill="#161b22" stroke="{trend_color}" stroke-width="1"/>'
                f'<text x="{end_x - 86}" y="{cy}" text-anchor="middle" fill="#e6edf3" font-family="DM Mono, monospace" font-size="12">{SafeCallout}</text>'
            )

    # Build date strings for each downsampled step
    n_pts = len(s_vals)
    dates_list = []
    for i in range(n_pts):
        frac = i / max(1, n_pts - 1)
        yr_float = start_year + frac * (end_year - start_year)
        yr_i = int(yr_float)
        mo_i = max(1, min(12, int(round((yr_float - yr_i) * 12)) + 1))
        dates_list.append(f"{yr_i}-{mo_i:02d}")

    hover_payload = {
        "v": [round(float(x), 3) for x in s_vals],
        "t": [round(float(x), 3) for x in s_trend] if s_trend is not None else [],
        "lo": [round(float(x), 3) for x in s_low] if s_low is not None else [],
        "hi": [round(float(x), 3) for x in s_high] if s_high is not None else [],
        "dates": dates_list,
        "units": units,
        "left": label_left,
        "right": label_right,
        "pad_left": pad_left,
        "plot_w": plot_w,
    }
    encoded = json.dumps(hover_payload).replace('"', "&quot;")
    safe_left = html.escape(label_left)
    safe_right = html.escape(label_right)
    unit_axis_svg = ""
    if units:
        safe_u = html.escape(units)
        unit_axis_svg = f'<text x="16" y="{pad_top + plot_h / 2:.0f}" transform="rotate(-90 16 {pad_top + plot_h / 2:.0f})" text-anchor="middle" fill="#8b949e" font-family="Inter, sans-serif" font-size="12">{safe_u}</text>'

    return (
        f'<svg class="interactiveSvg" tabindex="0" role="img" aria-label="{safe_left} ({safe_right})" data-series="{encoded}" viewBox="0 0 900 270">'
        f"<title>{safe_left} ({safe_right})</title>"
        + "".join(grid_parts)
        + axes_svg
        + zero_svg
        + ci_poly
        + f'<path d="{val_path}" fill="none" stroke="{stroke_color}" stroke-width="1.8"/>'
        + trend_svg
        + slope_callout_svg
        + unit_axis_svg
        + f'<text x="{pad_left}" y="22" fill="#e6edf3" font-family="Inter, sans-serif" font-size="12" font-weight="600">{safe_left}</text>'
        + f'<text x="{w - pad_right}" y="22" text-anchor="end" fill="#8b949e" font-family="DM Mono, monospace" font-size="12">{safe_right}</text>'
        + "</svg>"
    )


def render_climatology_svg(clim_df: pd.DataFrame, units: str) -> str:
    """
    Render 12-month seasonal climatology bar + curve SVG with real axes, 12px+ tick labels,
    flat bar fills (no rounded tops, no overlapping value labels above bars), and tooltip data.
    """
    col = "clim_mean" if "clim_mean" in clim_df.columns else "mean"
    means = clim_df[col].values.astype(float)
    months = clim_df["month_name"].tolist()
    vmin = float(np.min(means))
    vmax = float(np.max(means))
    span = max(1e-6, vmax - vmin)
    y_min = vmin - span * 0.12
    y_max = vmax + span * 0.12
    y_span = max(1e-6, y_max - y_min)

    w = 900.0
    h = 270.0
    pad_left = 68.0
    pad_right = 24.0
    pad_top = 36.0
    pad_bot = 42.0
    plot_w = w - pad_left - pad_right
    plot_h = h - pad_top - pad_bot
    y_bottom = pad_top + plot_h

    grid_parts = []
    n_yticks = 5
    for ti in range(n_yticks):
        frac = ti / (n_yticks - 1)
        val_tick = y_max - frac * y_span
        gy = round(pad_top + frac * plot_h, 1)
        grid_parts.append(
            f'<line x1="{pad_left}" y1="{gy}" x2="{w - pad_right}" y2="{gy}" stroke="#262e38" stroke-width="1"/>'
            f'<line x1="{pad_left - 5}" y1="{gy}" x2="{pad_left}" y2="{gy}" stroke="#484f58" stroke-width="1"/>'
            f'<text x="{pad_left - 8}" y="{gy + 4}" text-anchor="end" fill="#8b949e" font-family="DM Mono, monospace" font-size="12">{val_tick:.1f}</text>'
        )

    axes_svg = (
        f'<line x1="{pad_left}" y1="{pad_top}" x2="{pad_left}" y2="{y_bottom}" stroke="#484f58" stroke-width="1.2"/>'
        f'<line x1="{pad_left}" y1="{y_bottom}" x2="{w - pad_right}" y2="{y_bottom}" stroke="#484f58" stroke-width="1.2"/>'
    )

    bars = []
    pts = []
    col_step = plot_w / 12.0
    bar_w = 34.0
    for i, (m_name, val) in enumerate(zip(months, means)):
        x_center = round(pad_left + (i + 0.5) * col_step, 1)
        norm = (val - y_min) / y_span
        bar_h = max(4.0, norm * plot_h)
        y_top = round(y_bottom - bar_h, 1)
        pts.append((x_center, y_top))
        bars.append(
            f'<rect class="climBar" data-month="{m_name}" data-val="{val:.2f} {units}" '
            f'x="{x_center - bar_w / 2:.1f}" y="{y_top:.1f}" width="{bar_w:.0f}" height="{bar_h:.1f}" fill="#1f6feb" fill-opacity="0.45" stroke="#58a6ff" stroke-width="1"/>'
            f'<text x="{x_center}" y="{y_bottom + 20}" text-anchor="middle" fill="#8b949e" font-family="DM Mono, monospace" font-size="12">{m_name}</text>'
        )

    line_d = "M" + " L".join(f"{x} {y}" for x, y in pts)
    hover_payload = {
        "v": [round(float(x), 2) for x in means],
        "t": [round(float(x), 2) for x in means],
        "months": months,
        "units": units,
        "left": f"12-month seasonal climatology ({units})",
        "right": "Jan to Dec baseline cycle",
        "pad_left": pad_left,
        "plot_w": plot_w,
    }
    encoded = json.dumps(hover_payload).replace('"', "&quot;")
    safe_u = html.escape(units)

    return (
        f'<svg class="interactiveSvg" tabindex="0" role="img" aria-label="12-month seasonal climatology ({safe_u})" data-series="{encoded}" viewBox="0 0 900 270">'
        f"<title>12-month seasonal climatology ({safe_u})</title>"
        + "".join(grid_parts)
        + axes_svg
        + "".join(bars)
        + f'<path d="{line_d}" fill="none" stroke="#e06c3a" stroke-width="2"/>'
        + f'<text x="16" y="{pad_top + plot_h / 2:.0f}" transform="rotate(-90 16 {pad_top + plot_h / 2:.0f})" text-anchor="middle" fill="#8b949e" font-family="Inter, sans-serif" font-size="12">{safe_u}</text>'
        + f'<text x="{pad_left}" y="22" fill="#e6edf3" font-family="Inter, sans-serif" font-size="12" font-weight="600">12-month seasonal climatology ({safe_u})</text>'
        + f'<text x="{w - pad_right}" y="22" text-anchor="end" fill="#8b949e" font-family="DM Mono, monospace" font-size="12">Removed prior to trend test</text>'
        + "</svg>"
    )
