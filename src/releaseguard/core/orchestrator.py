from releaseguard.agents.release_judge import judge_release
from releaseguard.agents.requirement_analyzer import analyze_requirement
from releaseguard.agents.risk_security_auditor import audit_risk_and_security
from releaseguard.agents.test_strategist import design_tests
from releaseguard.schemas.models import AuditTrailItem, ReleaseGuardReport, RequirementInput


def run_pipeline(requirement_text: str, source: str = "manual_input") -> ReleaseGuardReport:
    requirement = RequirementInput(text=requirement_text, source=source)

    requirement_analysis = analyze_requirement(requirement)

    risk_security_analysis = audit_risk_and_security(
        requirement=requirement,
        analysis=requirement_analysis,
    )

    test_strategy = design_tests(
        requirement=requirement,
        analysis=requirement_analysis,
        risk_analysis=risk_security_analysis,
    )

    release_decision = judge_release(
        requirement_analysis=requirement_analysis,
        risk_analysis=risk_security_analysis,
        test_strategy=test_strategy,
    )

    audit_trail = [
        AuditTrailItem(
            step="Requirement Analyzer",
            summary=f"Detected {len(requirement_analysis.gaps)} requirement gap(s).",
        ),
        AuditTrailItem(
            step="Risk & Security Auditor",
            summary=f"Detected {len(risk_security_analysis.findings)} risk/security finding(s).",
        ),
        AuditTrailItem(
            step="Test Strategist",
            summary=f"Generated {len(test_strategy.test_cases)} test case(s).",
        ),
        AuditTrailItem(
            step="Release Judge",
            summary=(
                f"Produced readiness score {release_decision.readiness_score}/100 "
                f"with verdict {release_decision.verdict.value}."
            ),
        ),
    ]

    if 40 <= release_decision.readiness_score <= 70:
        audit_trail.append(
            AuditTrailItem(
                step="Conditional Critique",
                summary="Score is in uncertain range. Manual review is recommended for MVP.",
            )
        )

    return ReleaseGuardReport(
        requirement=requirement,
        requirement_analysis=requirement_analysis,
        risk_security_analysis=risk_security_analysis,
        test_strategy=test_strategy,
        release_decision=release_decision,
        audit_trail=audit_trail,
    )
