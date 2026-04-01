import requests
import json

def generate_ddr(inspection_text, thermal_text, images_data):
    prompt = f"""
Generate a structured DDR report.

Inspection:
{inspection_text[:1000]}

Thermal:
{thermal_text[:1000]}
"""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "tinyllama",
                "prompt": prompt,
                "stream": False
            },
            timeout=20
        )

        result = response.json().get("response", "")

        return {
            "property_issue_summary": result[:200],
            "area_wise_observations": [],
            "probable_root_cause": "Generated",
            "severity_assessment": {"level": "Medium"},
            "recommended_actions": ["Check manually"],
            "additional_notes": result,
            "missing_or_unclear_information": []
        }

    except Exception as e:
        return {
            "property_issue_summary": "Error",
            "area_wise_observations": [],
            "probable_root_cause": "Timeout",
            "severity_assessment": {"level": "Low"},
            "recommended_actions": ["Retry"],
            "additional_notes": str(e),
            "missing_or_unclear_information": []
        }