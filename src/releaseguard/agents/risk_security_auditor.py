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

    if "upload" in lower_text and (
        "avatar" in lower_text or "image" in lower_text or "file" in lower_text
    ):
        findings.extend(
            [
                RiskFinding(
                    title="File upload security risk",
                    description="File upload features can introduce malicious content, unsafe file parsing, and storage abuse.",
                    severity=Severity.HIGH,
                    category="security",
                ),
                RiskFinding(
                    title="Malware or unsafe content risk",
                    description="Uploaded files require validation, scanning, and strict file-type enforcement.",
                    severity=Severity.HIGH,
                    category="security",
                ),
                RiskFinding(
                    title="Content validation risk",
                    description="The requirement does not define validation rules for uploaded images or files.",
                    severity=Severity.HIGH,
                    category="product",
                ),
            ]
        )
        mitigations.append("Define file size, allowed formats, content validation, malware scanning, and rejection behavior.")

    if "admin" in lower_text and ("user" in lower_text or "users" in lower_text or "email" in lower_text):
        findings.extend(
            [
                RiskFinding(
                    title="Authorization risk",
                    description="Admin search requires strict role-based access control.",
                    severity=Severity.HIGH,
                    category="security",
                ),
                RiskFinding(
                    title="PII exposure risk",
                    description="Searching users by email exposes sensitive personal data if access controls are weak.",
                    severity=Severity.HIGH,
                    category="privacy",
                ),
                RiskFinding(
                    title="Access control risk",
                    description="The requirement does not define who can search user records and under what conditions.",
                    severity=Severity.HIGH,
                    category="security",
                ),
            ]
        )
        mitigations.append("Define admin roles, access controls, audit logging, and PII handling requirements.")

    if "export" in lower_text and "data" in lower_text:
        findings.extend(
            [
                RiskFinding(
                    title="Privacy risk",
                    description="Personal data export requires careful identity verification and access control.",
                    severity=Severity.CRITICAL,
                    category="privacy",
                ),
                RiskFinding(
                    title="Data access control risk",
                    description="Generated export files may expose personal data if links are persistent or shareable.",
                    severity=Severity.CRITICAL,
                    category="security",
                ),
                RiskFinding(
                    title="Compliance risk",
                    description="Data export features may be subject to privacy and regulatory requirements.",
                    severity=Severity.CRITICAL,
                    category="compliance",
                ),
            ]
        )
        mitigations.append("Define identity verification, export expiration, audit logging, and access control requirements.")

    if ("newsletter" in lower_text or "subscribe" in lower_text) and "email" in lower_text:
        findings.extend(
            [
                RiskFinding(
                    title="PII handling risk",
                    description="Newsletter signup collects email addresses and requires privacy-aware handling.",
                    severity=Severity.MEDIUM,
                    category="privacy",
                ),
                RiskFinding(
                    title="Email validation risk",
                    description="The requirement does not define invalid, duplicate, or disposable email behavior.",
                    severity=Severity.MEDIUM,
                    category="product",
                ),
                RiskFinding(
                    title="Consent risk",
                    description="Marketing signup should define consent, opt-in, and unsubscribe expectations.",
                    severity=Severity.MEDIUM,
                    category="compliance",
                ),
            ]
        )
        mitigations.append("Define email validation, consent, unsubscribe, and privacy notice behavior.")

    if "dark mode" in lower_text or "light mode" in lower_text:
        findings.extend(
            [
                RiskFinding(
                    title="Accessibility risk",
                    description="Theme switching can introduce contrast and readability issues.",
                    severity=Severity.LOW,
                    category="product",
                ),
                RiskFinding(
                    title="Visual regression risk",
                    description="Light and dark themes may render components inconsistently across screens.",
                    severity=Severity.LOW,
                    category="product",
                ),
            ]
        )
        mitigations.append("Define contrast requirements, persistence behavior, and visual regression coverage.")

    if "profile" in lower_text and "name" in lower_text:
        findings.extend(
            [
                RiskFinding(
                    title="Input validation risk",
                    description="Profile names require validation for length, unsupported characters, and empty values.",
                    severity=Severity.MEDIUM,
                    category="product",
                ),
                RiskFinding(
                    title="Display consistency risk",
                    description="Updated names must display consistently across profile, navigation, and account surfaces.",
                    severity=Severity.LOW,
                    category="product",
                ),
            ]
        )
        mitigations.append("Define input validation rules and display consistency expectations.")

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
