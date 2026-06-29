from releaseguard.schemas.models import (
    RequirementAnalysis,
    RequirementInput,
    RiskSecurityAnalysis,
    TestCase,
    TestStrategy,
)


def design_tests(
    requirement: RequirementInput,
    analysis: RequirementAnalysis,
    risk_analysis: RiskSecurityAnalysis,
) -> TestStrategy:
    lower_text = requirement.text.lower()

    test_cases: list[TestCase] = [
        TestCase(
            title="Happy path validation",
            description="Verify that the feature works correctly for the primary expected user flow.",
            priority="P0",
            test_type="functional",
        ),
        TestCase(
            title="Invalid input handling",
            description="Verify that invalid, incomplete, or unexpected input is handled safely and clearly.",
            priority="P0",
            test_type="negative",
        ),
        TestCase(
            title="Interrupted flow handling",
            description="Verify behavior when the user abandons, refreshes, or interrupts the flow.",
            priority="P1",
            test_type="edge",
        ),
    ]

    if "delete" in lower_text and "account" in lower_text:
        test_cases.extend(
            [
                TestCase(
                    title="Account deletion confirmation",
                    description="Verify that account deletion requires clear confirmation before irreversible action.",
                    priority="P0",
                    test_type="functional",
                ),
                TestCase(
                    title="Deletion of account with active subscription",
                    description="Verify behavior when a user with an active subscription requests account deletion.",
                    priority="P0",
                    test_type="edge",
                ),
                TestCase(
                    title="Account deletion API authorization",
                    description="Verify that only the authenticated account owner can request deletion.",
                    priority="P0",
                    test_type="api",
                ),
                TestCase(
                    title="Screen reader support for deletion confirmation",
                    description="Verify that deletion warnings and confirmation controls are accessible to screen readers.",
                    priority="P1",
                    test_type="accessibility",
                ),
            ]
        )

    if "login" in lower_text or "password" in lower_text or "oauth" in lower_text:
        test_cases.extend(
            [
                TestCase(
                    title="Authentication failure handling",
                    description="Verify incorrect credentials, expired tokens, and denied OAuth permissions.",
                    priority="P0",
                    test_type="negative",
                ),
                TestCase(
                    title="Rate limiting behavior",
                    description="Verify repeated login or password attempts trigger abuse prevention behavior.",
                    priority="P0",
                    test_type="security",
                ),
            ]
        )

    coverage_notes = [
        "Test strategy is generated from requirement gaps and risk findings.",
        f"Detected {len(analysis.gaps)} requirement gap(s).",
        f"Detected {len(risk_analysis.findings)} risk/security finding(s).",
    ]

    return TestStrategy(test_cases=test_cases, coverage_notes=coverage_notes)
