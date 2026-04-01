from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet

def build_pdf(report, output_path):
    doc = SimpleDocTemplate(output_path)
    styles = getSampleStyleSheet()
    elements = []

    # Title
    elements.append(Paragraph("DDR REPORT", styles['Title']))
    elements.append(Spacer(1, 20))

    # 1. Summary
    elements.append(Paragraph("1. Property Issue Summary", styles['Heading2']))
    elements.append(Paragraph(report.get("property_issue_summary", "Not Available"), styles['Normal']))
    elements.append(Spacer(1, 15))

    # 2. Area Observations
    elements.append(Paragraph("2. Area-wise Observations", styles['Heading2']))

    for obs in report.get("area_wise_observations", []):
        elements.append(Spacer(1, 10))
        elements.append(Paragraph(f"<b>Area:</b> {obs.get('area', 'Unknown')}", styles['Normal']))
        elements.append(Paragraph(f"<b>Severity:</b> {obs.get('severity', 'Low')}", styles['Normal']))

        for f in obs.get("findings", []):
            elements.append(Paragraph(f"- {f}", styles['Normal']))

        # Images
        for img in obs.get("images", []):
            try:
                elements.append(Image(img, width=300, height=200))
            except:
                elements.append(Paragraph("Image Not Available", styles['Normal']))

    elements.append(Spacer(1, 15))

    # 3. Root Cause
    elements.append(Paragraph("3. Probable Root Cause", styles['Heading2']))
    elements.append(Paragraph(report.get("probable_root_cause", "Not Available"), styles['Normal']))

    # 4. Severity
    elements.append(Spacer(1, 15))
    elements.append(Paragraph("4. Severity Assessment", styles['Heading2']))
    severity = report.get("severity_assessment", {})

    elements.append(Paragraph(f"Level: {severity.get('level', 'N/A')}", styles['Normal']))
    elements.append(Paragraph(f"Reasoning: {severity.get('reasoning', 'N/A')}", styles['Normal']))
    elements.append(Paragraph(f"Timeframe: {severity.get('recommended_timeframe', 'N/A')}", styles['Normal']))

    # 5. Actions
    elements.append(Spacer(1, 15))
    elements.append(Paragraph("5. Recommended Actions", styles['Heading2']))

    for action in report.get("recommended_actions", []):
        elements.append(Paragraph(f"- {action}", styles['Normal']))

    # 6. Notes
    elements.append(Spacer(1, 15))
    elements.append(Paragraph("6. Additional Notes", styles['Heading2']))
    elements.append(Paragraph(report.get("additional_notes", "Not Available"), styles['Normal']))

    # 7. Missing Info
    elements.append(Spacer(1, 15))
    elements.append(Paragraph("7. Missing or Unclear Information", styles['Heading2']))

    for item in report.get("missing_or_unclear_information", []):
        elements.append(Paragraph(f"- {item}", styles['Normal']))

    # Build PDF
    doc.build(elements)
