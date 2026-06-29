# ReleaseGuard

**ReleaseGuard** is a multi-agent release readiness platform that evaluates software requirements before development begins and produces a structured **Ship / No Ship** report.

The goal is simple:

> Can this feature safely ship?

ReleaseGuard helps identify requirement gaps, product risks, security concerns, missing test coverage, and release blockers before a single line of code is written.

---

## Problem

AI-assisted development makes it easier than ever to generate code, tests, and pull requests quickly.

But faster development creates a new quality problem:

* Are the requirements complete?
* Are edge cases defined?
* Are security and privacy risks visible?
* Is the feature testable?
* Is the team ready to ship?

Many bugs are not caused by bad code. They start with unclear, incomplete, or risky requirements.

ReleaseGuard shifts quality review earlier in the development lifecycle.

---

## What ReleaseGuard Does

ReleaseGuard takes a software requirement as input and produces a structured release readiness report.

Input examples:

* User story
* Product requirement
* Feature specification
* API requirement
* Bug fix description
* Pull request summary

Output includes:

* Requirement gaps
* Flagged assumptions
* Product and security risks
* Functional, negative, edge, API, and accessibility test ideas
* Readiness score
* Ship / No Ship verdict
* Audit trail

---

## Current MVP

The current MVP runs locally from the command line.

It includes:

* Modular Python pipeline
* Pydantic schemas
* Deterministic scoring engine
* Markdown report generation
* Evaluation dataset
* Automated tests
* Measured evaluation results

The current version uses deterministic rule-based agent logic. Future versions can replace or augment these agents with LLM-powered Google ADK agents while preserving the same schemas, scoring, and evaluation framework.

---

## Architecture

```text
Raw Requirement Text
        ↓
Orchestrator
        ↓
Requirement Analyzer
        ↓
Risk & Security Auditor
        ↓
Test Strategist
        ↓
Release Judge
        ↓
Report Assembler
        ↓
Release Readiness Report
```

### Core Components

| Component               | Responsibility                                                           |
| ----------------------- | ------------------------------------------------------------------------ |
| Requirement Analyzer    | Detects gaps, assumptions, ambiguity, and clarity issues                 |
| Risk & Security Auditor | Identifies product, security, privacy, compliance, and operational risks |
| Test Strategist         | Generates structured test coverage ideas                                 |
| Release Judge           | Calculates readiness score and produces Ship / No Ship verdict           |
| Report Assembler        | Generates deterministic Markdown report                                  |
| Evaluator               | Runs labeled requirements through the pipeline and calculates metrics    |

---

## Example CLI Usage

```bash
uv run releaseguard --text "As a user, I want to delete my account permanently from the settings page."
```

Example output:

```text
Report generated: output/reports/releaseguard_report.md
Verdict: NO_SHIP
Readiness Score: 33/100
Manual Review Required: True
```

---

## Example Report Sections

ReleaseGuard generates a Markdown report with:

* Verdict
* Readiness score
* Input requirement
* Feature summary
* Requirement gaps
* Flagged assumptions
* Risk and security findings
* Recommended mitigations
* Test strategy
* Category scores
* Decision rationale
* Audit trail

---

## Evaluation Results

ReleaseGuard was evaluated against a labeled dataset of 10 software requirements.

| Metric | ReleaseGuard Pipeline | Single-Step Baseline |
|---|---:|---:|
| Dataset size | 10 requirements | 10 requirements |
| Verdict accuracy | 90.00% | 40.00% |
| Average gap recall | 90.00% | 33.33% |
| Average risk recall | 96.67% | 31.67% |

ReleaseGuard's structured multi-step pipeline significantly outperformed the simplified single-step baseline.

The dataset includes requirements across multiple product areas:

* account deletion
* password reset
* profile update
* checkout discount code
* OAuth login
* newsletter signup
* avatar upload
* admin user search
* dark mode toggle
* personal data export

See: `docs/evaluation_results.md`

---

## Run Tests

```bash
uv run pytest
```

Current test coverage validates:

* pipeline execution
* Ship / No Ship logic
* account deletion risk detection
* audit trail generation
* Markdown report creation

---

## Run Evaluation

```bash
uv run python -m releaseguard.core.evaluator
```

This generates:

```text
output/evaluations/eval_report.md
```

---

## Project Structure

```text
releaseguard/
├── data/
│   └── evaluations/
├── docs/
├── specs/
├── src/
│   └── releaseguard/
│       ├── agents/
│       ├── core/
│       ├── schemas/
│       └── utils/
├── templates/
├── tests/
├── README.md
└── pyproject.toml
```

---

## Why Multi-Step Evaluation?

A single prompt can generate a list of test cases.

ReleaseGuard is designed to do something more useful:

```text
Requirement
→ Gap detection
→ Risk classification
→ Test strategy
→ Readiness scoring
→ Ship / No Ship verdict
→ Audit trail
```

The core value is not generating more text.

The core value is producing a traceable quality decision.

---

## Kaggle Capstone Alignment

ReleaseGuard demonstrates several concepts from the Google AI Agents course:

* Multi-agent architecture
* Structured agent workflow
* Agent-like specialized roles
* Security-aware design
* Evaluation dataset
* Measurable quality metrics
* Local CLI execution
* Deterministic guardrails

---

## Known Limitations

Current MVP limitations:

* Agents are deterministic and rule-based
* No live Google ADK integration yet
* No web UI
* No cloud deployment
* No GitHub or Jira integration
* Evaluation dataset is intentionally small
* Domain coverage is limited to selected software requirement patterns

These limitations are intentional for the MVP scope.

---

## Future Work

Potential future versions may include:

* Google ADK-powered LLM agents
* GitHub pull request readiness checks
* Jira story quality review
* CI/CD release gate integration
* VS Code extension
* Web dashboard
* Apple app
* PDF export
* Multi-LLM evaluation mode
* Organization-specific quality rules

---

## Status

ReleaseGuard is currently an MVP built for the Kaggle AI Agents Capstone.

It is designed as a portfolio project for AI Quality Engineering, AI Evaluation Engineering, and modern software QA workflows.


---

## Security Guardrails

ReleaseGuard includes lightweight input guardrails for safer agent-style evaluation.

Current guardrails include:

- input length limit
- prompt injection pattern detection
- PII pattern detection
- audit trail integration
- additional security/privacy findings when suspicious input is detected

These checks help prevent the pipeline from blindly trusting user-provided requirement text.


---

## Demo

The repository includes a sample requirement and a generated ReleaseGuard report.

Demo input: `data/samples/account_deletion.md`

Generated report: `docs/demo/account_deletion_report.md`

This demo shows how ReleaseGuard evaluates a privacy-sensitive account deletion feature and produces a structured release readiness report with gaps, risks, test ideas, readiness score, verdict, and audit trail.
