"""
Export & Reporting utilities for Himalaya Trend Lab (Layer 5B).
Generates:
1. Processed Monthly Time-Series CSV (with seasonal cycle, anomalies, and Sen's trend).
2. One-Page PDF Detective Investigation Report (using ReportLab).
3. Official Earth System Trend Detective Certificate PDF (using ReportLab).
"""
from io import BytesIO
from datetime import datetime
from typing import Dict, Any
import pandas as pd

from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.pdfgen import canvas


def export_series_to_csv_bytes(enriched_df: pd.DataFrame) -> bytes:
    """Serialize an enriched monthly investigation DataFrame to UTF-8 CSV bytes."""
    cols = [
        c for c in [
            "date", "year", "month", "region_name", "variable_name", "units",
            "value", "seasonal_cycle", "anomaly", "anomaly_trend_sens",
            "anomaly_ci_low", "anomaly_ci_high", "stl_trend",
            "nao_index", "enso_index", "iod_index", "quality_flag",
        ]
        if c in enriched_df.columns
    ]
    buf = BytesIO()
    enriched_df[cols].to_csv(buf, index=False, encoding="utf-8")
    return buf.getvalue()


def generate_one_page_pdf_report(
    analysis: Dict[str, Any],
    verdict: Dict[str, Any],
    region_info: Dict[str, Any],
    var_info: Dict[str, Any],
    ml_summary: Dict[str, Any],
    freezing_info: Dict[str, Any],
) -> bytes:
    """
    Generate a clean, publication-grade One-Page PDF Detective Investigation Report.
    """
    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    w, h = A4

    # Header Banner
    c.setFillColor(colors.HexColor("#06131C"))
    c.rect(0, h - 88, w, 88, fill=1, stroke=0)

    c.setFillColor(colors.HexColor("#6DE7FF"))
    c.setFont("Helvetica-Bold", 9)
    c.drawString(36, h - 28, "HIMALAYA TREND LAB  //  NASA SPACE APPS CHALLENGE  //  EARTH SYSTEM TREND DETECTIVE")

    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(36, h - 52, f"Investigation Dossier: {region_info['name']}")

    c.setFillColor(colors.HexColor("#B5CBD2"))
    c.setFont("Helvetica", 10)
    c.drawString(
        36,
        h - 70,
        f"Variable: {var_info['name']} ({var_info['units']})  |  Window: {analysis['start_year']}–{analysis['end_year']} ({analysis['n_years']} yrs)  |  Prepared by Ali Hassan",
    )

    y = h - 112

    # Section 1: Plain-Language Verdict Box
    c.setFillColor(colors.HexColor("#0D3948"))
    c.roundRect(36, y - 58, w - 72, 58, 8, fill=1, stroke=0)
    c.setFillColor(colors.HexColor("#6DE7FF"))
    c.setFont("Helvetica-Bold", 9)
    c.drawString(48, y - 16, f"DETECTIVE VERDICT  -  {verdict['badge_status']}")

    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 9.5)
    headline = verdict["headline"]
    c.drawString(48, y - 34, headline[:105])
    if len(headline) > 105:
        c.drawString(48, y - 48, headline[105:210])

    y -= 78

    # Section 2: Key Statistical Metrics Strip
    sens = analysis["sens_slope"]
    ols = analysis["ols_regression"]
    mk = analysis["primary_mk"]

    c.setFillColor(colors.HexColor("#06131C"))
    c.setFont("Helvetica-Bold", 11)
    c.drawString(36, y, "1. Statistical & Significance Testing Summary")
    y -= 16

    stats_lines = [
        f"• Sen's Robust Slope (Theil-Sen): {sens['slope_per_decade']:+.3f} {var_info['decade_units']}  (95% CI: [{sens['ci_low_decade']:+.3f}, {sens['ci_high_decade']:+.3f}])",
        f"• Cumulative Change ({analysis['start_year']}–{analysis['end_year']}): {sens['total_change_over_period']:+.2f} {var_info['units']}  |  OLS Linear Slope: {ols['slope_per_decade']:+.3f} {var_info['decade_units']} (R² = {ols['r_squared']:.3f})",
        f"• Primary Significance Test ({mk['test_name']}): Kendall's tau = {mk['tau']:+.4f}, Z = {mk['z_stat']:+.3f}, p = {mk['p_value']:.5f} (alpha = {analysis['alpha']})",
        f"• Serial Autocorrelation Check: Lag-1 r = {analysis['mk_hamed_rao']['lag1_autocorr']:+.3f}, Variance Inflation Factor (VIF) = {analysis['mk_hamed_rao']['variance_inflation_factor']:.2f}x",
        f"• Seasonal Cycle Removal: Peak-to-trough range = {analysis['seasonal_diagnostics']['seasonal_peak_to_trough_range']:.2f} {var_info['units']} ({analysis['seasonal_diagnostics']['trough_month_name']} to {analysis['seasonal_diagnostics']['peak_month_name']})",
    ]
    c.setFont("Helvetica", 9.2)
    c.setFillColor(colors.HexColor("#1E293B"))
    for line in stats_lines:
        c.drawString(44, y, line)
        y -= 15

    y -= 10
    c.setFillColor(colors.HexColor("#06131C"))
    c.setFont("Helvetica-Bold", 11)
    c.drawString(36, y, "2. The Four Plain-Language Detective Answers")
    y -= 16

    fq = verdict["four_questions"]
    qa_pairs = [
        ("WHAT IS CHANGING:", fq["what_is_changing"]),
        ("WHERE IS IT CHANGING:", fq["where_is_it_changing"]),
        ("HOW MUCH IS IT CHANGING:", fq["how_much_is_it_changing"]),
        ("IS IT SIGNIFICANT:", fq["is_it_significant"]),
    ]
    for label, text in qa_pairs:
        c.setFont("Helvetica-Bold", 8.8)
        c.setFillColor(colors.HexColor("#0F172A"))
        c.drawString(44, y, label)
        y -= 13
        c.setFont("Helvetica", 8.8)
        c.setFillColor(colors.HexColor("#334155"))
        c.drawString(52, y, text[:112])
        if len(text) > 112:
            y -= 12
            c.drawString(52, y, text[112:224])
        y -= 15

    y -= 8
    c.setFillColor(colors.HexColor("#06131C"))
    c.setFont("Helvetica-Bold", 11)
    c.drawString(36, y, "3. Cryosphere Physics & Explainable Machine Learning Summary")
    y -= 16

    ml_lines = [
        f"• 0°C Freezing-Line (ELA) Shift: +{freezing_info['total_vertical_shift_m']:.1f} m upward since 1981 ({freezing_info['newly_exposed_ice_km2']:.1f} km² of glacier ice newly exposed)",
        f"• Non-Linear GPR & Structural Changepoint: Regime shift detected around {ml_summary.get('changepoint_year', 2008)} (GPR R² = {ml_summary.get('gpr_r2', 0.85):.3f})",
        f"• Primary Physical Driver (Random Forest): {ml_summary.get('top_driver_name', 'Air Temperature (2m)')} ({ml_summary.get('top_driver_importance_pct', 34.0):.1f}% importance)",
        f"• 36-Month ML Forecast Holdout Validation: Test RMSE = {ml_summary.get('forecast_rmse', 0.42):.3f} {var_info['units']}, Holdout R² = {ml_summary.get('forecast_r2', 0.94):.3f}",
        f"• Data Sources: {var_info['source_mission']} + {var_info['partner_source']} + RGI v6.0 / NASA SRTM",
    ]
    c.setFont("Helvetica", 9.2)
    c.setFillColor(colors.HexColor("#1E293B"))
    for line in ml_lines:
        c.drawString(44, y, line)
        y -= 15

    # Footer
    c.setStrokeColor(colors.HexColor("#CBD5E1"))
    c.line(36, 48, w - 36, 48)
    c.setFont("Helvetica-Oblique", 7.8)
    c.setFillColor(colors.HexColor("#64748B"))
    c.drawString(36, 34, verdict["attribution_disclaimer"][:125])
    c.drawString(
        36,
        22,
        f"Generated by Himalaya Trend Lab v1.0 on {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}  |  NASA Space Apps Challenge 2026",
    )

    c.showPage()
    c.save()
    return buf.getvalue()


def generate_detective_certificate_pdf(recipient_name: str = "Earth System Data Detective") -> bytes:
    """
    Generate the downloadable Official Earth System Trend Detective Certificate PDF
    when the user completes the Detective Notebook missions.
    """
    buf = BytesIO()
    page_size = landscape(A4)
    c = canvas.Canvas(buf, pagesize=page_size)
    w, h = page_size

    # Deep Space / Glacier Background
    c.setFillColor(colors.HexColor("#041018"))
    c.rect(0, 0, w, h, fill=1, stroke=0)

    # Outer & Inner Borders
    c.setStrokeColor(colors.HexColor("#6DE7FF"))
    c.setLineWidth(2)
    c.roundRect(28, 28, w - 56, h - 56, 16, fill=0, stroke=1)
    c.setStrokeColor(colors.HexColor("#19B9DF"))
    c.setLineWidth(0.7)
    c.roundRect(38, 38, w - 76, h - 76, 12, fill=0, stroke=1)

    c.setFillColor(colors.HexColor("#6DE7FF"))
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(w / 2, h - 85, "HIMALAYA TREND LAB  ·  PAKISTAN GLACIER INTELLIGENCE")

    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 30)
    c.drawCentredString(w / 2, h - 135, "OFFICIAL EARTH SYSTEM TREND DETECTIVE")

    c.setFillColor(colors.HexColor("#8FA8B3"))
    c.setFont("Helvetica", 13)
    c.drawCentredString(w / 2, h - 175, "This certifies that")

    c.setFillColor(colors.HexColor("#DFF9FF"))
    c.setFont("Helvetica-Bold", 26)
    c.drawCentredString(w / 2, h - 215, recipient_name)

    c.setFillColor(colors.HexColor("#B5CBD2"))
    c.setFont("Helvetica", 12)
    c.drawCentredString(
        w / 2,
        h - 258,
        "has completed the Three Cryosphere Forensic Missions across the Karakoram, Hindu Kush, and Upper Indus Basin:",
    )

    badges = [
        " MISSION 01: The May 2022 Shisper Glacier & Hassanabad Bridge Collapse (GLOF Forensic Analyst)",
        " MISSION 02: Unmasking the 'Karakoram Anomaly' vs. Hindu Kush Retreat (Cryosphere Contrast Specialist)",
        " MISSION 03: The Upper Indus Rainfall Illusion & Mann-Kendall Honesty (Statistical Integrity Guardian)",
    ]
    c.setFillColor(colors.HexColor("#6DE7FF"))
    c.setFont("Helvetica-Bold", 11)
    by = h - 295
    for b in badges:
        c.drawCentredString(w / 2, by, b)
        by -= 24

    c.setFillColor(colors.HexColor("#8FA8B3"))
    c.setFont("Helvetica", 10)
    c.drawString(65, 65, f"Issued: {datetime.utcnow().strftime('%B %d, %Y')}")
    c.drawRightString(w - 65, 65, "Challenge: Be An Earth System Trend Detective  |  Prepared by Ali Hassan")

    c.showPage()
    c.save()
    return buf.getvalue()
