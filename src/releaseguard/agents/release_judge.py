from releaseguard.schemas.models import (
    CategoryScores,
    ReleaseDecision,
    RequirementAnalysis,
    RiskSecurityAnalysis,
    Severity,
    TestStrategy,
    Verdict,
)


SEVERITY_PENALTY = {
    Severity.LOW: 5,
    Severity.MEDIUM: 10,
    Severity.HIGH: 20,
    Severity.CRITICAL: 35,
}


def judge_release(
    requirement_analysis: RequirementAnalysis,
    risk_analysis: RiskSecurityAnalysis,
    test_strategy: TestStrategy,
) -> ReleaseDecision:
    gap_penalty = sum(SEVERITY_PENALTY[gap.severity] for gap in requirement_analysis.gaps)
    risk_penalty = sum(SEVERITY_PENALTY[finding.severity] for finding in risk_analysis.findings)

    p0_count = sum(1 for test in test_strategy.test_cases if test.priority == "P0")
    coverage_bonus = min(20, p0_count * 3)

    requirement_quality = max(0, 100 - gap_penalty)
    risk_security = max(0, 100 - risk_penalty)
    test_coverage = min(100, 55 + coverage_bonus)

    readiness_score = int((requirement_quality * 0.35) + (risk_security * 0.4) + (test_coverage * 0.25))

    has_critical = any(gap.severity == Severity.CRITICAL for gap in requirement_analysis.gaps) or any(
        finding.severity == Severity.CRITICAL for finding in risk_analysis.findings
    )

    if has_critical or readiness_score < 60:
        verdict = Verdict.NO_SHIP
    elif readiness_score < 75:
        verdict = Verdict.MANUAL_REVIEW
    elif readiness_score < 90:
        verdict = Verdict.SHIP_WITH_CAUTION
    else:
        verdict = Verdict.SHIP

    manual_review_required = verdict in {Verdict.NO_SHIP, Verdict.MANUAL_REVIEW}

    rationale = (
        "Release decision is based on requirement quality, risk/security severity, "
        "and generated test coverage. Critical risks or unresolved high-severity gaps "
        "prevent a confident Ship recommendation."
    )

    return ReleaseDecision(
        readiness_score=readiness_score,
        category_scores=CategoryScores(
            requirement_quality=requirement_quality,
            risk_security=risk_security,
            test_coverage=test_coverage,
            release_confidence=readiness_score,
        ),
        verdict=verdict,
        rationale=rationale,
        manual_review_required=manual_review_required,
    )
