from releaseguard.schemas.models import (
    RequirementAnalysis,
    RequirementInput,
    RiskFinding,
    RiskSecurityAnalysis,
    Severity,
)


def audit_risk_and_security(
    requirement: RequirementInput,
    analysis: RequirementAnalysis,
) -> RiskSecurityAnalysis:
    lower_text = requirement.text.lower()

    findings: list[RiskFinding] = []
    mitigations: list[str] = []

    if "delete" in lower_text and "account" in lower_text:
        findings.append(
            RiskFinding(
                title="Privacy and compliance risk",
                description="Account deletion may affect personal data retention, audit logs, backups, and legal compliance requirements.",
                severity=Severity.CRITICAL,
                category="privacy",
            )
        )
        mitigations.append("Define data retention, backup deletion, export, audit, and recovery behavior before implementation.")

    if "login" in lower_text or "password" in lower_text or "oauth" in lower_text:
        findings.append(
            RiskFinding(
                title="Authentication abuse risk",
                description="Authentication-related features require rate limiting, lockout rules, token expiration, and abuse prevention.",
                severity=Severity.HIGH,
                category="security",
            )
        )
        mitigations.append("Add rate limiting, session/token expiration rules, lockout behavior, and monitoring requirements.")

    if "payment" in lower_text or "checkout" in lower_text or "subscription" in lower_text:
        findings.append(
            RiskFinding(
                title="Payment integrity risk",
                description="Payment flows require rollback behavior, duplicate charge prevention, and failure-state handling.",
                severity=Severity.CRITICAL,
                category="operational",
            )
        )
        mitigations.append("Define transaction rollback, retry, duplicate prevention, and reconciliation behavior.")

    for gap in analysis.gaps:
        if gap.severity in {Severity.HIGH, Severity.CRITICAL}:
            findings.append(
                RiskFinding(
                    title=f"Requirement-driven product risk: {gap.title}",
                    description=gap.description,
                    severity=gap.severity,
                    category="product",
                )
            )

    if not findings:
        findings.append(
            RiskFinding(
                title="General release risk",
                description="The requirement does not explicitly describe risk handling, monitoring, or rollback expectations.",
                severity=Severity.MEDIUM,
                category="product",
            )
        )
        mitigations.append("Add explicit risk handling, monitoring, and release rollback expectations.")

    return RiskSecurityAnalysis(
        findings=findings,
        recommended_mitigations=mitigations,
    )
