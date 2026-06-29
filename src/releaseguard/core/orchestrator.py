import os

from dotenv import load_dotenv

from releaseguard.agents.llm_requirement_analyzer import analyze_requirement_with_llm
from releaseguard.agents.release_judge import judge_release
from releaseguard.agents.requirement_analyzer import analyze_requirement
from releaseguard.agents.risk_security_auditor import audit_risk_and_security
from releaseguard.agents.test_strategist import design_tests
from releaseguard.core.guardrails import run_input_guardrails
from releaseguard.schemas.models import (
    AuditTrailItem,
    ReleaseGuardReport,
    RequirementAnalysis,
    RequirementInput,
    RiskFinding,
    RiskSecurityAnalysis,
    Severity,
)

load_dotenv()


def _analyze_requirement(requirement: RequirementInput) -> tuple[RequirementAnalysis, str]:
    use_llm = bool(os.environ.get("GOOGLE_API_KEY"))

    if not use_llm:
        return analyze_requirement(requirement), "Requirement Analyzer (rule-based)"

    try:
        return analyze_requirement_with_llm(requirement), "Requirement Analyzer (Gemini)"
    except Exception as llm_error:
        label = (
            "Requirement Analyzer "
            f"(LLM failed: {type(llm_error).__name__}; rule-based fallback)"
        )
        return analyze_requirement(requirement), label


def _add_guardrail_findings(
    risk_security_analysis: RiskSecurityAnalysis,
    guardrail_flags: list[str],
) -> None:
    if "prompt_injection_suspected" in guardrail_flags:
        risk_security_analysis.findings.append(
            RiskFinding(
                title="Prompt injection attempt detected",
                description=(
                    "The input contains language commonly used to override or manipulate "
                    "agent instructions."
                ),
                severity=Severity.HIGH,
                category="security",
            )
        )

    if any(flag.startswith("pii_detected") for flag in guardrail_flags):
        risk_security_analysis.findings.append(
            RiskFinding(
                title="Potential PII detected",
                description=(
                    "The input appears to contain personal or sensitive information that "
                    "should be handled carefully."
                ),
                severity=Severity.MEDIUM,
                category="privacy",
            )
        )


def _build_conditional_critique(
    release_report: ReleaseGuardReport,
) -> AuditTrailItem | None:
    release_decision = release_report.release_decision

    if not 40 <= release_decision.readiness_score <= 70:
        return None

    scores = {
        "Requirement quality": release_decision.category_scores.requirement_quality,
        "Risk & security": release_decision.category_scores.risk_security,
        "Test coverage": release_decision.category_scores.test_coverage,
    }
    weakest_category = min(scores, key=scores.get)
    weakest_score = scores[weakest_category]

    blocking_gaps = [
        gap.title
        for gap in release_report.requirement_analysis.gaps
        if gap.severity == Severity.CRITICAL
    ]
    blocking_risks = [
        finding.title
        for finding in release_report.risk_security_analysis.findings
        if finding.severity == Severity.CRITICAL
    ]

    critique_parts = [
        f"Score {release_decision.readiness_score}/100 is in the uncertain range.",
        f"Weakest category: {weakest_category} ({weakest_score}/100).",
    ]

    if blocking_gaps:
        critique_parts.append(f"Blocking gaps to resolve: {'; '.join(blocking_gaps)}.")

    if blocking_risks:
        critique_parts.append(f"Blocking risks to mitigate: {'; '.join(blocking_risks)}.")

    critique_parts.append("Resolve the above before re-running evaluation.")

    return AuditTrailItem(
        step="Conditional Critique",
        summary=" ".join(critique_parts),
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

    requirement_analysis, analyzer_label = _analyze_requirement(requirement)
    audit_trail.append(
        AuditTrailItem(
            step=analyzer_label,
            summary=(
                f"Found {len(requirement_analysis.gaps)} gaps and "
                f"{len(requirement_analysis.assumptions)} assumptions."
            ),
        )
    )

    risk_security_analysis = audit_risk_and_security(requirement, requirement_analysis)
    _add_guardrail_findings(risk_security_analysis, guardrail_result.flags)

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

    report = ReleaseGuardReport(
        requirement=requirement,
        requirement_analysis=requirement_analysis,
        risk_security_analysis=risk_security_analysis,
        test_strategy=test_strategy,
        release_decision=release_decision,
        audit_trail=audit_trail,
    )

    critique = _build_conditional_critique(report)
    if critique:
        report.audit_trail.append(critique)

    return report
