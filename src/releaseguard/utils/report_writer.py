from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from releaseguard.schemas.models import ReleaseGuardReport


def write_markdown_report(
    report: ReleaseGuardReport,
    output_path: Path = Path("output/reports/releaseguard_report.md"),
) -> Path:
    env = Environment(
        loader=FileSystemLoader("templates"),
        autoescape=False,
        trim_blocks=True,
        lstrip_blocks=True,
    )

    template = env.get_template("release_report.md.j2")
    content = template.render(report=report)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")

    return output_path
