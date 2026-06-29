from releaseguard.agents.release_judge import judge_release
from releaseguard.agents.requirement_analyzer import analyze_requirement
from releaseguard.agents.risk_security_auditor import audit_risk_and_security
from releaseguard.agents.test_strategist import design_tests
from releaseguard.core.guardrails import run_input_guardrails
from releaseguard.schemas.models import (
    AuditTrailItem,
    ReleaseGuardReport,
    RequirementInput,
    RiskFinding,
    Severity,
)


def run_pipeline(requirement_text: str, source: str = "manual_input") -> ReleaseGuardReport:
    guardrail_result = run_input_guardrails(requirement_text)

    if not guardrail_result.is_allowed:
        raise ValueError(guardrail_result.summary)

    requirement = RequirementInput(text=requirement_text, source=source)

    audit_trail = [
        AuditTrailItem(
            step="Input Guardrails",
            summary=guardrail_result.summary,
        )
    ]

    requirement_analysis = analyze_requirement(requirement)
    audit_trail.append(
        AuditTrailItem(
            step="Requirement Analyzer",
            summary=(
                f"Found {len(requirement_analysis.gaps)} gaps and "
                f"{len(requirement_analysis.assumptions)} assumptions."
            ),
        )
    )

    risk_security_analysis = audit_risk_and_security(requirement, requirement_analysis)

    if "prompt_injection_suspected" in guardrail_result.flags:
        risk_security_analysis.findings.append(
            RiskFinding(
                title="Prompt injection attempt detected",
                description="The input contains language commonly used to override or manipulate agent instructions.",
                severity=Severity.HIGH,
                category="security",
            )
        )

    if any(flag.startswith("pii_detected") for flag in guardrail_result.flags):
        risk_security_analysis.findings.append(
            RiskFinding(
                title="Potential PII detected",
                description="The input appears to contain personal or sensitive information that should be handled carefully.",
                severity=Severity.MEDIUM,
                category="privacy",
            )
        )

    audit_trail.append(
        AuditTrailItem(
            step="Risk & Security Auditor",
            summary=f"Found {len(risk_security_analysis.findings)} risk/security findings.",
        )
    )

    test_strategy = design_tests(requirement, requirement_analysis, risk_security_analysis)
    audit_trail.append(
        AuditTrailItem(
            step="Test Strategist",
            summary=f"Generated {len(test_strategy.test_cases)} test ideas.",
        )
    )

    release_decision = judge_release(
        requirement_analysis,
        risk_security_analysis,
        test_strategy,
    )
    audit_trail.append(
        AuditTrailItem(
            step="Release Judge",
            summary=(
                f"Calculated readiness score {release_decision.readiness_score}/100 "
                f"with verdict {release_decision.verdict.value}."
            ),
        )
    )

    if 40 <= release_decision.readiness_score <= 70:
        audit_trail.append(
            AuditTrailItem(
                step="Conditional Critique",
                summary="Score falls into the uncertain range; manual review is recommended for MVP.",
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
