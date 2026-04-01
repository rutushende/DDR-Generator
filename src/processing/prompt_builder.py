def build_prompt(inspection_text, thermal_text):
    return f"""
You are a professional building diagnostic expert.

Analyze both reports and generate a structured DDR.

RULES:
- Do NOT invent information
- Avoid duplication
- If missing → write "Not Available"

Inspection Report:
{inspection_text}

Thermal Report:
{thermal_text}

OUTPUT FORMAT (JSON):
{{
 "property_issue_summary": "",
 "area_wise_observations": [
   {{
     "area": "",
     "findings": [],
     "severity": "",
     "images": [],
     "source": ""
   }}
 ],
 "probable_root_cause": "",
 "severity_assessment": {{
   "level": "",
   "reasoning": "",
   "recommended_timeframe": ""
 }},
 "recommended_actions": [],
 "additional_notes": "",
 "missing_or_unclear_information": []
}}
"""
