from dataclasses import dataclass

from releaseguard.schemas.models import Verdict


@dataclass
class BaselineResult:
    gaps: list[str]
    risks: list[str]
    verdict: str
    readiness_score: int


def run_single_prompt_baseline(requirement: str) -> BaselineResult:
    """
    Simple one-step baseline that simulates a generic single-prompt requirement review.

    This intentionally does not use the multi-step ReleaseGuard pipeline.
    It gives us a comparison point for evaluation.
    """
    lower_text = requirement.lower()

    gaps: list[str] = []
    risks: list[str] = []

    if "acceptance criteria" not in lower_text:
        gaps.append("missing acceptance criteria")

    if "error" not in lower_text and "failure" not in lower_text and "invalid" not in lower_text:
        gaps.append("missing failure behavior")

    readiness_score = 72
    verdict = Verdict.MANUAL_REVIEW.value

    if "delete" in lower_text and "account" in lower_text:
        risks.extend(["privacy risk", "data retention risk"])
        readiness_score = 55
        verdict = Verdict.NO_SHIP.value

    elif "login" in lower_text or "password" in lower_text or "oauth" in lower_text:
        risks.append("security risk")
        readiness_score = 65
        verdict = Verdict.MANUAL_REVIEW.value

    elif "payment" in lower_text or "checkout" in lower_text or "subscription" in lower_text:
        risks.append("payment risk")
        readiness_score = 65
        verdict = Verdict.MANUAL_REVIEW.value

    elif "upload" in lower_text or "avatar" in lower_text or "file" in lower_text:
        risks.append("file upload risk")
        readiness_score = 65
        verdict = Verdict.MANUAL_REVIEW.value

    elif "admin" in lower_text:
        risks.append("authorization risk")
        readiness_score = 65
        verdict = Verdict.MANUAL_REVIEW.value

    elif "export" in lower_text and "data" in lower_text:
        risks.append("privacy risk")
        readiness_score = 65
        verdict = Verdict.MANUAL_REVIEW.value

    elif "dark mode" in lower_text or "light mode" in lower_text:
        risks.append("visual regression risk")
        readiness_score = 82
        verdict = Verdict.SHIP_WITH_CAUTION.value

    elif "newsletter" in lower_text or "subscribe" in lower_text:
        risks.append("email validation risk")
        readiness_score = 70
        verdict = Verdict.MANUAL_REVIEW.value

    if not risks:
        risks.append("general product risk")

    return BaselineResult(
        gaps=gaps,
        risks=risks,
        verdict=verdict,
        readiness_score=readiness_score,
    )
