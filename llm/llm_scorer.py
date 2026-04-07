import os

def build_prompt(analysis):
    return f"""
You are a senior security engineer analyzing software dependencies.

Analyze the following dependency risk data:
Name: {analysis['name']}
Version Spec: {analysis['version_spec']}
Resolved Version: {analysis['resolved_version']}
Latest Version: {analysis['latest_version']}

Outdated: {analysis['is_outdated']}
Version Gap: {analysis['version_gap']} ({analysis['gap_risk']})

Vulnerable: {analysis['is_vulnerable']}
Vulnerabilities: {analysis['matched_vulnerabilities']}\

Preliminary Risk Level: {analysis['risk_level']}
Reasons: {analysis['reasons']}

---
Your task:
1. Assign a final risk score (0-10)
2. Explain the real-world risk
3. Prioritize urgency
4. Suggest clear action

Respond ONLY in JSON format:

{{
    "final_risk_score:" number,
    "priority" : " LOW | MEDIUM | HIGH | CRITICAL "
    "summary: "...",
    "detailed_analysis: "...",
    "recommendation" : "..."
}}
"""

def call_llm(prompt):
    from openai import OpenAI

    client = OpenAI(api_key="")

    response = client.chat.completions.create(
        model= "gpt-5.4-mini",
        messages = [
            {"role": "system", "content": " You are a security expert."},
            {"role": "user", "content": prompt}
        ],
        temperature= 0.3
    )

    return response.choices[0].message.content

import json
def parse_llm_response(response_text):
    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        return {
            "final_risk_score": None,
            "priority": "UNKNOWN",
            "summary" : "FAILED TO PARSE LLM RESPONSE",
            "detailed_analysis" : response_text,
            "recommendation": "MANUAL REVIEW REQUIRED"
        }
    
def score_dependency(analysis):
    prompt = build_prompt(analysis)

    raw_response = call_llm(prompt)

    parsed = parse_llm_response(raw_response)

    return parsed