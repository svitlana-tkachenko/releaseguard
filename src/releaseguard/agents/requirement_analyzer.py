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
    is_simple_ui_preference = "dark mode" in lower_text or "light mode" in lower_text

    gaps: list[RequirementGap] = []
    assumptions: list[Assumption] = []
    ambiguity_notes: list[str] = []

    feature_summary = text if len(text) <= 180 else f"{text[:177]}..."

    if "acceptance criteria" not in lower_text and not is_simple_ui_preference:
        gaps.append(
            RequirementGap(
                title="Missing acceptance criteria",
                description="The requirement does not define clear acceptance criteria for expected behavior.",
                severity=Severity.HIGH,
            )
        )

    if (
        "error" not in lower_text
        and "failure" not in lower_text
        and "invalid" not in lower_text
        and not is_simple_ui_preference
    ):
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

    if "upload" in lower_text and (
        "avatar" in lower_text or "image" in lower_text or "file" in lower_text
    ):
        gaps.extend(
            [
                RequirementGap(
                    title="File size limits not defined",
                    description="The requirement does not define maximum file size or upload limits.",
                    severity=Severity.HIGH,
                ),
                RequirementGap(
                    title="Allowed file formats not defined",
                    description="The requirement does not specify allowed image/file formats.",
                    severity=Severity.HIGH,
                ),
                RequirementGap(
                    title="Unsafe file handling not defined",
                    description="The requirement does not describe validation, scanning, or rejection of unsafe uploads.",
                    severity=Severity.HIGH,
                ),
            ]
        )

    if "admin" in lower_text and ("user" in lower_text or "users" in lower_text or "email" in lower_text):
        gaps.extend(
            [
                RequirementGap(
                    title="Role permissions not defined",
                    description="The requirement does not define which admin roles can access this functionality.",
                    severity=Severity.HIGH,
                ),
                RequirementGap(
                    title="Audit logging not defined",
                    description="The requirement does not specify whether admin search activity should be logged.",
                    severity=Severity.HIGH,
                ),
                RequirementGap(
                    title="Empty and no-result states not defined",
                    description="The requirement does not define behavior for empty searches or no matching users.",
                    severity=Severity.MEDIUM,
                ),
            ]
        )

    if "export" in lower_text and "data" in lower_text:
        gaps.extend(
            [
                RequirementGap(
                    title="Identity verification not defined",
                    description="The requirement does not define how user identity is verified before exporting personal data.",
                    severity=Severity.CRITICAL,
                ),
                RequirementGap(
                    title="Export format not defined",
                    description="The requirement does not specify the format, scope, or structure of exported data.",
                    severity=Severity.HIGH,
                ),
                RequirementGap(
                    title="Download expiration not defined",
                    description="The requirement does not define expiration or access control for generated export files.",
                    severity=Severity.HIGH,
                ),
            ]
        )

    if ("newsletter" in lower_text or "subscribe" in lower_text) and "email" in lower_text:
        gaps.extend(
            [
                RequirementGap(
                    title="Invalid email behavior not defined",
                    description="The requirement does not define validation behavior for malformed or duplicate email addresses.",
                    severity=Severity.MEDIUM,
                ),
                RequirementGap(
                    title="Unsubscribe expectation not defined",
                    description="The requirement does not specify unsubscribe or preference management expectations.",
                    severity=Severity.MEDIUM,
                ),
                RequirementGap(
                    title="Privacy consent not defined",
                    description="The requirement does not define consent, privacy notice, or marketing opt-in behavior.",
                    severity=Severity.MEDIUM,
                ),
            ]
        )

    if is_simple_ui_preference:
        gaps.extend(
            [
                RequirementGap(
                    title="Contrast requirements not defined",
                    description="The requirement does not specify visual contrast expectations for light and dark themes.",
                    severity=Severity.LOW,
                ),
                RequirementGap(
                    title="Persistence behavior not defined",
                    description="The requirement does not define whether the selected theme persists across sessions.",
                    severity=Severity.LOW,
                ),
                RequirementGap(
                    title="System setting behavior not defined",
                    description="The requirement does not define whether the app follows system appearance settings.",
                    severity=Severity.LOW,
                ),
            ]
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
