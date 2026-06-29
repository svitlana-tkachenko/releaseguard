# ReleaseGuard MVP Scope

## MVP Objective

Build a local multi-agent release readiness system that evaluates software requirements before development begins and produces a structured Ship / No Ship report.

The MVP focuses on proving the core product idea:

**Can a multi-agent quality pipeline detect requirement gaps, risks, missing test coverage, and release blockers better than a single generic AI prompt?**

---

## In Scope

### 1. Local CLI Workflow

ReleaseGuard will run locally from the command line.

Input:

* raw requirement text
* markdown requirement file
* sample feature specification

Output:

* markdown release readiness report

---

### 2. Four-Agent Pipeline

The MVP includes four core agents:

1. Requirement Analyzer
2. Risk & Security Auditor
3. Test Strategist
4. Release Judge

Optional conditional agent:

5. Critique Agent

The Critique Agent runs only when the Release Judge produces an uncertain readiness score.

Trigger condition:

```text
40 <= readiness_score <= 70
```

---

### 3. Structured Output

ReleaseGuard will generate a structured report with:

* Requirement gaps
* Flagged assumptions
* Test cases
* Risk and security findings
* Readiness score
* Ship / No Ship verdict
* Decision rationale
* Audit trail

---

### 4. Deterministic Scoring

The readiness score will be calculated using deterministic Python logic.

The LLM agents identify findings.

The scoring engine calculates the final score based on:

* number of requirement gaps
* severity of risks
* missing security controls
* test coverage quality
* unresolved critical issues

---

### 5. Markdown Report Generation

The final report will be generated using a deterministic template.

The Report Assembler is not an LLM agent.

This reduces hallucination risk and makes the output more reproducible.

---

### 6. Evaluation Dataset

The MVP will include a small labeled evaluation dataset.

Initial dataset size:

```text
10-15 sample requirements
```

Each example should include:

* requirement text
* expected gaps
* expected risks
* expected verdict
* severity level

The evaluation will compare:

* single-prompt baseline
* multi-agent ReleaseGuard pipeline

Metrics:

* gap detection recall
* risk detection quality
* verdict accuracy
* consistency across repeated runs

---

### 7. Security Guardrails

The MVP will include basic security guardrails:

* no API keys committed to repository
* environment variables for secrets
* prompt injection pattern detection
* input length limits
* PII pattern detection
* manual review flag for uncertain outputs

---

## Out of Scope

The MVP will not include:

* web UI
* mobile app
* App Store version
* PDF export
* GitHub pull request integration
* Jira integration
* TestRail integration
* live cloud deployment
* multiple LLM providers
* real-time collaboration
* automated code generation
* full CI/CD integration
* browser extension
* VS Code extension

These are future enhancements, not Kaggle MVP requirements.

---

## Future Work

Potential future versions may include:

* GitHub Action for pull request readiness checks
* Jira story quality review
* TestRail export
* Markdown to PDF export
* web dashboard
* Apple app
* VS Code extension
* CI/CD release gate integration
* multi-LLM comparison mode
* custom organization-specific quality rules

---

## Definition of Done

The MVP is complete when:

1. A user can provide a software requirement as input.
2. ReleaseGuard runs the multi-agent pipeline.
3. Each core agent produces structured output.
4. The Release Judge produces a readiness score.
5. The system returns a Ship / No Ship verdict.
6. The final Markdown report is generated.
7. At least 10 sample requirements are evaluated.
8. A baseline single-prompt comparison exists.
9. The README explains architecture, setup, demo, and limitations.
10. The project can be demonstrated in a 5-minute Kaggle video.

---

## Success Criteria

ReleaseGuard succeeds as a Kaggle capstone if it demonstrates:

* clear real-world business value
* multi-agent architecture
* structured AI evaluation
* security-aware design
* measurable improvement over a single-prompt baseline
* a credible release readiness report
* a focused MVP that avoids unnecessary product sprawl

