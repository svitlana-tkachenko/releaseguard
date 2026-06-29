from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel

app = typer.Typer(help="ReleaseGuard: AI release readiness evaluation CLI")
console = Console()


def load_requirement(text: Optional[str], file: Optional[Path]) -> str:
    if text and file:
        raise typer.BadParameter("Use either --text or --file, not both.")

    if file:
        if not file.exists():
            raise typer.BadParameter(f"File not found: {file}")
        content = file.read_text(encoding="utf-8").strip()
    elif text:
        content = text.strip()
    else:
        raise typer.BadParameter("Provide a requirement using --text or --file.")

    if len(content) < 10:
        raise typer.BadParameter("Requirement is too short to evaluate.")

    return content


@app.command()
def run(
    text: Optional[str] = typer.Option(None, "--text", "-t", help="Raw requirement text."),
    file: Optional[Path] = typer.Option(None, "--file", "-f", help="Path to a requirement file."),
) -> None:
    """
    Run a ReleaseGuard requirement evaluation.
    """
    requirement = load_requirement(text, file)

    console.print(
        Panel.fit(
            "ReleaseGuard is evaluating the requirement...",
            title="ReleaseGuard",
            subtitle="MVP CLI",
        )
    )

    # Temporary mock analysis.
    # Later this will be replaced by the multi-agent pipeline.
    lower_requirement = requirement.lower()

    gaps = []
    risks = []

    if "delete" in lower_requirement or "account" in lower_requirement:
        gaps.append("Data retention and recovery behavior is not defined.")
        risks.append("Account deletion may involve privacy, security, and compliance risk.")

    if "login" in lower_requirement or "password" in lower_requirement:
        gaps.append("Authentication failure states are not fully specified.")
        risks.append("Missing rate limiting or abuse prevention requirements.")

    if not gaps:
        gaps.append("Acceptance criteria are not detailed enough for release readiness.")

    if not risks:
        risks.append("No explicit risk handling requirements were provided.")

    readiness_score = 62 if risks else 78
    verdict = "NO SHIP" if readiness_score < 70 else "SHIP WITH CAUTION"

    report = f"""# ReleaseGuard Report

## Input Requirement

{requirement}

## Requirement Gaps

{chr(10).join(f"- {gap}" for gap in gaps)}

## Risk & Security Findings

{chr(10).join(f"- {risk}" for risk in risks)}

## Readiness Score

{readiness_score}/100

## Verdict

{verdict}

## Rationale

This is a mock MVP report. The current CLI validates input, applies basic deterministic checks, and generates a structured Markdown report. The next step is replacing mock analysis with the ReleaseGuard multi-agent pipeline.
"""

    output_dir = Path("output/reports")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / "releaseguard_report.md"
    output_path.write_text(report, encoding="utf-8")

    console.print(f"[green]Report generated:[/green] {output_path}")
    console.print(f"[bold]Verdict:[/bold] {verdict}")
    console.print(f"[bold]Readiness Score:[/bold] {readiness_score}/100")


if __name__ == "__main__":
    app()
