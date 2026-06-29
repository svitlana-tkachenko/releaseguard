import json
import os
import re

from google import genai
from google.genai import types

from releaseguard.schemas.models import RequirementAnalysis, RequirementInput


SYSTEM_PROMPT = """
You are a senior QA engineer and AI evaluation specialist.

Analyze the software requirement for release readiness before development begins.

Return ONLY valid JSON matching this exact schema:

{
  "feature_summary": "one concise sentence",
  "gaps": [
    {
      "title": "short gap title",
      "description": "specific explanation",
      "severity": "LOW | MEDIUM | HIGH | CRITICAL"
    }
  ],
  "assumptions": [
    {
      "description": "assumption being made",
      "risk_if_wrong": "what could go wrong",
      "severity": "LOW | MEDIUM | HIGH | CRITICAL"
    }
  ],
  "ambiguity_notes": ["specific ambiguity or missing detail"],
  "clarity_score": 0
}

Scoring guidance:
- 90-100: clear, testable, low ambiguity
- 70-89: mostly clear, some missing edge cases
- 40-69: incomplete, requires manual review
- 0-39: unsafe or unclear enough to block release planning

Focus on:
- acceptance criteria
- failure behavior
- privacy and compliance expectations
- security and authorization
- edge cases
- rollback or recovery behavior
- observability and auditability
- testability

Do not include markdown.
Do not include commentary outside JSON.
"""


def _extract_json(raw_text: str) -> str:
    cleaned = raw_text.strip()

    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?", "", cleaned).strip()
        cleaned = re.sub(r"```$", "", cleaned).strip()

    start = cleaned.find("{")
    end = cleaned.rfind("}")

    if start == -1 or end == -1 or end <= start:
        raise ValueError("LLM response did not contain a JSON object.")

    return cleaned[start : end + 1]


def analyze_requirement_with_llm(requirement: RequirementInput) -> RequirementAnalysis:
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY is not configured.")

    model_name = os.environ.get("MODEL_NAME", "gemini-2.5-flash")

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model=model_name,
        contents=f"{SYSTEM_PROMPT}\n\nRequirement:\n{requirement.text}",
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.2,
        ),
    )

    raw_text = response.text or ""
    parsed = json.loads(_extract_json(raw_text))

    return RequirementAnalysis.model_validate(parsed)
