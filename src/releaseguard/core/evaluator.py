import json
from pathlib import Path
from statistics import mean
from typing import Any

from releaseguard.core.baseline import run_single_prompt_baseline
from releaseguard.core.orchestrator import run_pipeline


def _text_blob(items: list[Any]) -> str:
    return " ".join(str(item).lower() for item in items)


def _keyword_hit(expected: str, actual_text: str) -> bool:
    tokens = [token for token in expected.lower().replace("-", " ").split() if len(token) > 3]
    if not tokens:
        return expected.lower() in actual_text

    return any(token in actual_text for token in tokens)


def _recall(expected_items: list[str], actual_text: str) -> tuple[float, list[str]]:
    hits = [expected for expected in expected_items if _keyword_hit(expected, actual_text)]
    recall = len(hits) / len(expected_items) if expected_items else 1.0
    return recall, hits


def evaluate_dataset(
    dataset_path: Path = Path("data/evaluations/requirements.json"),
    output_path: Path = Path("output/evaluations/eval_report.md"),
) -> Path:
    dataset = json.loads(dataset_path.read_text(encoding="utf-8"))

    results = []

    for item in dataset:
        releaseguard_report = run_pipeline(item["requirement"])
        baseline_result = run_single_prompt_baseline(item["requirement"])

        expected_verdict = item["expected_verdict"]
        expected_gaps = item.get("expected_gaps", [])
        expected_risks = item.get("expected_risks", [])

        releaseguard_gap_text = _text_blob(
            [
                gap.title + " " + gap.description
                for gap in releaseguard_report.requirement_analysis.gaps
            ]
        )
        releaseguard_risk_text = _text_blob(
            [
                finding.title + " " + finding.description + " " + finding.category
                for finding in releaseguard_report.risk_security_analysis.findings
            ]
        )

        baseline_gap_text = _text_blob(baseline_result.gaps)
        baseline_risk_text = _text_blob(baseline_result.risks)

        releaseguard_gap_recall, releaseguard_gap_hits = _recall(
            expected_gaps,
            releaseguard_gap_text,
        )
        releaseguard_risk_recall, releaseguard_risk_hits = _recall(
            expected_risks,
            releaseguard_risk_text,
        )

        baseline_gap_recall, baseline_gap_hits = _recall(
            expected_gaps,
            baseline_gap_text,
        )
        baseline_risk_recall, baseline_risk_hits = _recall(
            expected_risks,
            baseline_risk_text,
        )

        results.append(
            {
                "id": item["id"],
                "title": item["title"],
                "expected_verdict": expected_verdict,
                "releaseguard_verdict": releaseguard_report.release_decision.verdict.value,
                "baseline_verdict": baseline_result.verdict,
                "releaseguard_score": releaseguard_report.release_decision.readiness_score,
                "baseline_score": baseline_result.readiness_score,
                "releaseguard_verdict_match": (
                    releaseguard_report.release_decision.verdict.value == expected_verdict
                ),
                "baseline_verdict_match": baseline_result.verdict == expected_verdict,
                "releaseguard_gap_recall": releaseguard_gap_recall,
                "baseline_gap_recall": baseline_gap_recall,
                "releaseguard_risk_recall": releaseguard_risk_recall,
                "baseline_risk_recall": baseline_risk_recall,
                "releaseguard_gap_hits": releaseguard_gap_hits,
                "baseline_gap_hits": baseline_gap_hits,
                "releaseguard_risk_hits": releaseguard_risk_hits,
                "baseline_risk_hits": baseline_risk_hits,
            }
        )

    releaseguard_verdict_accuracy = mean(
        1 if result["releaseguard_verdict_match"] else 0 for result in results
    )
    baseline_verdict_accuracy = mean(
        1 if result["baseline_verdict_match"] else 0 for result in results
    )

    releaseguard_avg_gap_recall = mean(result["releaseguard_gap_recall"] for result in results)
    baseline_avg_gap_recall = mean(result["baseline_gap_recall"] for result in results)

    releaseguard_avg_risk_recall = mean(result["releaseguard_risk_recall"] for result in results)
    baseline_avg_risk_recall = mean(result["baseline_risk_recall"] for result in results)

    lines = [
        "# ReleaseGuard Evaluation Report",
        "",
        "## Summary Metrics",
        "",
        "| Metric | ReleaseGuard Pipeline | Single-Prompt Baseline |",
        "|---|---:|---:|",
        f"| Dataset size | {len(results)} requirements | {len(results)} requirements |",
        f"| Verdict accuracy | {releaseguard_verdict_accuracy:.2%} | {baseline_verdict_accuracy:.2%} |",
        f"| Average gap recall | {releaseguard_avg_gap_recall:.2%} | {baseline_avg_gap_recall:.2%} |",
        f"| Average risk recall | {releaseguard_avg_risk_recall:.2%} | {baseline_avg_risk_recall:.2%} |",
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
                f"- ReleaseGuard verdict: {result['releaseguard_verdict']}",
                f"- Baseline verdict: {result['baseline_verdict']}",
                f"- ReleaseGuard score: {result['releaseguard_score']}/100",
                f"- Baseline score: {result['baseline_score']}/100",
                f"- ReleaseGuard verdict match: {result['releaseguard_verdict_match']}",
                f"- Baseline verdict match: {result['baseline_verdict_match']}",
                f"- ReleaseGuard gap recall: {result['releaseguard_gap_recall']:.2%}",
                f"- Baseline gap recall: {result['baseline_gap_recall']:.2%}",
                f"- ReleaseGuard risk recall: {result['releaseguard_risk_recall']:.2%}",
                f"- Baseline risk recall: {result['baseline_risk_recall']:.2%}",
                "- ReleaseGuard gap hits: "
                + (
                    ", ".join(result["releaseguard_gap_hits"])
                    if result["releaseguard_gap_hits"]
                    else "None"
                ),
                "- Baseline gap hits: "
                + (
                    ", ".join(result["baseline_gap_hits"])
                    if result["baseline_gap_hits"]
                    else "None"
                ),
                "- ReleaseGuard risk hits: "
                + (
                    ", ".join(result["releaseguard_risk_hits"])
                    if result["releaseguard_risk_hits"]
                    else "None"
                ),
                "- Baseline risk hits: "
                + (
                    ", ".join(result["baseline_risk_hits"])
                    if result["baseline_risk_hits"]
                    else "None"
                ),
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
