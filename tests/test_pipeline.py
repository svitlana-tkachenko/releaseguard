from pathlib import Path

from releaseguard.core.orchestrator import run_pipeline
from releaseguard.schemas.models import Severity, Verdict
from releaseguard.utils.report_writer import write_markdown_report


def test_account_deletion_requirement_is_no_ship():
    report = run_pipeline(
        "As a user, I want to delete my account permanently from the settings page."
    )

    assert report.release_decision.verdict == Verdict.NO_SHIP
    assert report.release_decision.readiness_score < 60
    assert report.release_decision.manual_review_required is True

    critical_gaps = [
        gap for gap in report.requirement_analysis.gaps if gap.severity == Severity.CRITICAL
    ]

    assert critical_gaps


def test_basic_requirement_generates_structured_report():
    report = run_pipeline(
        "As a user, I want to update my profile name from account settings."
    )

    assert report.requirement.text
    assert report.requirement_analysis.feature_summary
    assert report.requirement_analysis.gaps
    assert report.risk_security_analysis.findings
    assert report.test_strategy.test_cases
    assert 0 <= report.release_decision.readiness_score <= 100
    assert report.release_decision.verdict in {
        Verdict.SHIP,
        Verdict.SHIP_WITH_CAUTION,
        Verdict.NO_SHIP,
        Verdict.MANUAL_REVIEW,
    }


def test_audit_trail_records_pipeline_steps():
    report = run_pipeline(
        "As a user, I want to reset my password using email verification."
    )

    steps = [item.step for item in report.audit_trail]

    assert "Requirement Analyzer" in steps
    assert "Risk & Security Auditor" in steps
    assert "Test Strategist" in steps
    assert "Release Judge" in steps


def test_markdown_report_writer_creates_file(tmp_path: Path):
    report = run_pipeline(
        "As a user, I want to delete my account permanently from the settings page."
    )

    output_path = tmp_path / "releaseguard_report.md"
    written_path = write_markdown_report(report, output_path=output_path)

    assert written_path.exists()

    content = written_path.read_text(encoding="utf-8")

    assert "# ReleaseGuard Report" in content
    assert "NO_SHIP" in content
    assert "Readiness Score" in content
    assert "Audit Trail" in content
