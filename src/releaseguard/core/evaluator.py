import json
from pathlib import Path
from statistics import mean
from typing import Any

from releaseguard.core.orchestrator import run_pipeline


def _text_blob(items: list[Any]) -> str:
    return " ".join(str(item).lower() for item in items)


def _keyword_hit(expected: str, actual_text: str) -> bool:
    tokens = [token for token in expected.lower().replace("-", " ").split() if len(token) > 3]
    if not tokens:
        return expected.lower() in actual_text

    return any(token in actual_text for token in tokens)


def evaluate_dataset(
    dataset_path: Path = Path("data/evaluations/requirements.json"),
    output_path: Path = Path("output/evaluations/eval_report.md"),
) -> Path:
    dataset = json.loads(dataset_path.read_text(encoding="utf-8"))

    results = []

    for item in dataset:
        report = run_pipeline(item["requirement"])

        actual_verdict = report.release_decision.verdict.value
        expected_verdict = item["expected_verdict"]

        gap_text = _text_blob(
            [gap.title + " " + gap.description for gap in report.requirement_analysis.gaps]
        )
        risk_text = _text_blob(
            [
                finding.title + " " + finding.description + " " + finding.category
                for finding in report.risk_security_analysis.findings
            ]
        )

        expected_gaps = item.get("expected_gaps", [])
        expected_risks = item.get("expected_risks", [])

        gap_hits = [
            expected_gap
            for expected_gap in expected_gaps
            if _keyword_hit(expected_gap, gap_text)
        ]

        risk_hits = [
            expected_risk
            for expected_risk in expected_risks
            if _keyword_hit(expected_risk, risk_text)
        ]

        gap_recall = len(gap_hits) / len(expected_gaps) if expected_gaps else 1.0
        risk_recall = len(risk_hits) / len(expected_risks) if expected_risks else 1.0
        verdict_match = actual_verdict == expected_verdict

        results.append(
            {
                "id": item["id"],
                "title": item["title"],
                "expected_verdict": expected_verdict,
                "actual_verdict": actual_verdict,
                "readiness_score": report.release_decision.readiness_score,
                "gap_recall": gap_recall,
                "risk_recall": risk_recall,
                "verdict_match": verdict_match,
                "gap_hits": gap_hits,
                "risk_hits": risk_hits,
            }
        )

    verdict_accuracy = mean(1 if result["verdict_match"] else 0 for result in results)
    avg_gap_recall = mean(result["gap_recall"] for result in results)
    avg_risk_recall = mean(result["risk_recall"] for result in results)

    lines = [
        "# ReleaseGuard Evaluation Report",
        "",
        "## Summary Metrics",
        "",
        f"- Dataset size: {len(results)} requirements",
        f"- Verdict accuracy: {verdict_accuracy:.2%}",
        f"- Average gap recall: {avg_gap_recall:.2%}",
        f"- Average risk recall: {avg_risk_recall:.2%}",
        "",
        "## Requirement-Level Results",
        "",
    ]

    for result in results:
        lines.extend(
            [
                f"### {result['id']} — {result['title']}",
                "",
                f"- Expected verdict: {result['expected_verdict']}",
                f"- Actual verdict: {result['actual_verdict']}",
                f"- Readiness score: {result['readiness_score']}/100",
                f"- Verdict match: {result['verdict_match']}",
                f"- Gap recall: {result['gap_recall']:.2%}",
                f"- Risk recall: {result['risk_recall']:.2%}",
                f"- Gap hits: {', '.join(result['gap_hits']) if result['gap_hits'] else 'None'}",
                f"- Risk hits: {', '.join(result['risk_hits']) if result['risk_hits'] else 'None'}",
                "",
            ]
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")

    return output_path


def main() -> None:
    output_path = evaluate_dataset()
    print(f"Evaluation report generated: {output_path}")


if __name__ == "__main__":
    main()
