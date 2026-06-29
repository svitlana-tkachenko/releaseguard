from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel

from releaseguard.core.orchestrator import run_pipeline
from releaseguard.utils.report_writer import write_markdown_report

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
    requirement_text = load_requirement(text, file)

    console.print(
        Panel.fit(
            "ReleaseGuard is evaluating the requirement...",
            title="ReleaseGuard",
            subtitle="MVP Pipeline",
        )
    )

    report = run_pipeline(requirement_text=requirement_text)
    output_path = write_markdown_report(report)

    console.print(f"[green]Report generated:[/green] {output_path}")
    console.print(f"[bold]Verdict:[/bold] {report.release_decision.verdict.value}")
    console.print(f"[bold]Readiness Score:[/bold] {report.release_decision.readiness_score}/100")
    console.print(
        f"[bold]Manual Review Required:[/bold] {report.release_decision.manual_review_required}"
    )


if __name__ == "__main__":
    app()
