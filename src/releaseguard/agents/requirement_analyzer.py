from releaseguard.schemas.models import (
    Assumption,
    RequirementAnalysis,
    RequirementGap,
    RequirementInput,
    Severity,
)


def analyze_requirement(requirement: RequirementInput) -> RequirementAnalysis:
    text = requirement.text.strip()
    lower_text = text.lower()

    gaps: list[RequirementGap] = []
    assumptions: list[Assumption] = []
    ambiguity_notes: list[str] = []

    feature_summary = text if len(text) <= 180 else f"{text[:177]}..."

    if "acceptance criteria" not in lower_text:
        gaps.append(
            RequirementGap(
                title="Missing acceptance criteria",
                description="The requirement does not define clear acceptance criteria for expected behavior.",
                severity=Severity.HIGH,
            )
        )

    if "error" not in lower_text and "failure" not in lower_text and "invalid" not in lower_text:
        gaps.append(
            RequirementGap(
                title="Missing failure behavior",
                description="The requirement does not describe invalid, failed, or interrupted user flows.",
                severity=Severity.MEDIUM,
            )
        )

    if "delete" in lower_text and "account" in lower_text:
        gaps.append(
            RequirementGap(
                title="Undefined account deletion policy",
                description="The requirement does not define retention, recovery, audit, export, or grace-period behavior.",
                severity=Severity.CRITICAL,
            )
        )
        assumptions.append(
            Assumption(
                description="Account deletion is expected to be permanent.",
                risk_if_wrong="Users may lose data unexpectedly or the product may violate privacy/compliance expectations.",
                severity=Severity.HIGH,
            )
        )

    if "login" in lower_text or "password" in lower_text or "oauth" in lower_text:
        gaps.append(
            RequirementGap(
                title="Authentication edge cases not defined",
                description="The requirement does not fully define failed login, lockout, token expiration, or abuse prevention behavior.",
                severity=Severity.HIGH,
            )
        )

    if len(text.split()) < 12:
        ambiguity_notes.append("The requirement is very short and likely underspecified.")

    if not assumptions:
        assumptions.append(
            Assumption(
                description="The implementation will follow standard product security and usability expectations.",
                risk_if_wrong="Implicit assumptions may lead to gaps that are only discovered late in development.",
                severity=Severity.MEDIUM,
            )
        )

    penalty = sum(
        {
            Severity.LOW: 5,
            Severity.MEDIUM: 10,
            Severity.HIGH: 18,
            Severity.CRITICAL: 30,
        }[gap.severity]
        for gap in gaps
    )
    clarity_score = max(0, 100 - penalty)

    return RequirementAnalysis(
        feature_summary=feature_summary,
        gaps=gaps,
        assumptions=assumptions,
        ambiguity_notes=ambiguity_notes,
        clarity_score=clarity_score,
    )
