# ReleaseGuard: Multi-Agent Release Readiness Evaluator

## Project Track

**Agents for Business**

ReleaseGuard is a business-focused AI quality engineering tool designed to help product and engineering teams evaluate whether a software feature is ready to move forward before development begins.

The core question ReleaseGuard answers is:

> Can this feature safely ship?

---

## Project Summary

ReleaseGuard is a multi-step release readiness platform that evaluates software requirements before implementation.

It takes a requirement, user story, product specification, API requirement, bug fix description, or pull request summary as input and produces a structured **Ship / No Ship** report.

The report includes:

* requirement gaps
* risky assumptions
* product, privacy, security, compliance, and operational risks
* functional, negative, edge-case, API, accessibility, and security test ideas
* readiness score
* Ship / No Ship verdict
* audit trail

The goal is to move quality review earlier in the development lifecycle, before unclear or risky requirements become expensive defects.

---

## Problem

AI-assisted development makes it easier to generate code, tests, and pull requests quickly.

However, faster code generation does not automatically mean better software quality.

Many production issues begin before code is written:

* unclear requirements
* missing acceptance criteria
* undefined failure behavior
* missing privacy or security expectations
* incomplete test strategy
* weak release readiness decisions

ReleaseGuard addresses this problem by evaluating the requirement itself before development starts.

---

## Solution

ReleaseGuard uses a structured multi-step pipeline to evaluate requirements.

The current MVP runs locally from the command line. The Requirement Analyzer can use Gemini Flash when GOOGLE_API_KEY is configured, while the rule-based fallback keeps evaluation reproducible and measurable without an API key.

Pipeline:

```text
Raw Requirement
    ↓
Input Guardrails
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

Each stage has a focused responsibility.

This is intentionally different from a single generic prompt that tries to do everything at once.

---

## Agent Roles

### 1. Input Guardrails

Checks the requirement before analysis.

Current checks include:

* input length limit
* prompt injection pattern detection
* PII pattern detection
* audit trail integration
* security/privacy findings for suspicious input

### 2. Requirement Analyzer

Detects requirement quality issues such as:

* missing acceptance criteria
* undefined failure behavior
* missing rollback behavior
* missing access control expectations
* ambiguous user flows
* risky assumptions

### 3. Risk & Security Auditor

Classifies risks across categories such as:

* product risk
* security risk
* privacy risk
* compliance risk
* operational risk

### 4. Test Strategist

Generates structured test coverage ideas, including:

* functional tests
* negative tests
* edge cases
* API tests
* accessibility tests
* security tests

### 5. Release Judge

Calculates readiness score and produces the final verdict:

* SHIP
* SHIP_WITH_CAUTION
* MANUAL_REVIEW
* NO_SHIP

### 6. Report Assembler

Creates a deterministic Markdown report that can be reviewed by QA, engineering, product, or leadership.

---

## Course Concepts Demonstrated

ReleaseGuard demonstrates several concepts from the Google AI Agents course:

* multi-agent style architecture
* specialized agent roles
* structured orchestration
* security-aware agent workflow
* input guardrails
* evaluation dataset
* baseline comparison
* measurable quality metrics
* local CLI execution
* reproducible reports

The current MVP includes an optional Gemini-powered Requirement Analyzer when GOOGLE_API_KEY is configured, while preserving deterministic rule-based fallback so outputs can still be tested, evaluated, and reproduced consistently.

Future versions can replace or augment the deterministic agents with Google ADK-powered LLM agents while preserving the same schemas, scoring logic, guardrails, and evaluation framework.

---

## Evaluation

ReleaseGuard was evaluated against a labeled dataset of 10 software requirements.

The dataset includes requirements across multiple product and risk areas:

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

Each example includes expected gaps, expected risks, expected severity, and expected release verdict.

---

## Evaluation Metrics

ReleaseGuard was compared against a simplified single-step baseline.

| Metric              | ReleaseGuard Pipeline | Single-Step Baseline |
| ------------------- | --------------------: | -------------------: |
| Dataset size        |       10 requirements |      10 requirements |
| Verdict accuracy    |                90.00% |               40.00% |
| Average gap recall  |                90.00% |               33.33% |
| Average risk recall |                96.67% |               31.67% |

---

## Key Finding

The structured ReleaseGuard pipeline significantly outperformed the simplified single-step baseline.

Improvements:

* +50 percentage points in verdict accuracy
* +56.67 percentage points in average gap recall
* +65 percentage points in average risk recall

This suggests that decomposing release readiness review into focused stages produces better coverage than a direct one-step review.

---

## Demo Scenario

The demo requirement is a privacy-sensitive account deletion feature.

Input:

```text
Feature: Permanent account deletion

As a user, I want to delete my account permanently from the settings page.

The user should be able to start deletion from account settings and confirm the action before the account is removed.
```

ReleaseGuard identifies this feature as high risk because account deletion requires clear policies around:

* data retention
* confirmation behavior
* irreversible actions
* compliance expectations
* privacy risk
* user recovery expectations
* auditability

The generated report produces a **NO_SHIP** verdict until the missing requirements are clarified.

---

## Example CLI Usage

```bash
uv run releaseguard --file data/samples/account_deletion.md
```

Example output:

```text
Report generated: output/reports/releaseguard_report.md
Verdict: NO_SHIP
Readiness Score: 33/100
Manual Review Required: True
```

---

## Repository Artifacts

The repository includes:

* source code
* modular agent-style pipeline
* schemas
* CLI
* evaluation dataset
* evaluation runner
* baseline comparison
* tests
* demo input
* generated demo report
* architecture documentation
* evaluation results documentation

Important files:

```text
README.md
specs/architecture.md
docs/evaluation_results.md
docs/demo/account_deletion_report.md
data/evaluations/requirements.json
data/samples/account_deletion.md
src/releaseguard/
tests/
```

---

## Limitations

Current MVP limitations:

* Requirement Analyzer is optionally Gemini-powered; other agents remain rule-based
* no live Google ADK integration yet
* no web UI
* no cloud deployment
* no GitHub, Jira, or CI/CD integration yet
* small evaluation dataset
* limited domain coverage

These limitations are intentional for the MVP.

The goal was to build a measurable, testable, reproducible release readiness evaluator first.

---

## Future Work

Future improvements may include:

* Google ADK-powered LLM agents
* larger labeled evaluation dataset
* GitHub pull request readiness checks
* Jira story quality review
* CI/CD release gate integration
* VS Code extension
* web dashboard
* PDF export
* multi-LLM evaluation mode
* company-specific quality rules
* human-in-the-loop review workflow

---

## Business Value

ReleaseGuard helps teams reduce the risk of shipping unclear, incomplete, or unsafe features.

It is especially useful for:

* QA Engineers
* AI Evaluation Engineers
* Product Managers
* Engineering Managers
* teams using AI coding agents
* startups shipping fast with limited QA capacity

The business value is not simply generating test cases.

The value is producing a traceable release readiness decision before development starts.

---

## Conclusion

ReleaseGuard turns requirement review into a measurable quality signal.

Instead of asking a generic AI model for test ideas, ReleaseGuard decomposes the release readiness problem into focused stages: requirement analysis, risk review, test strategy, scoring, verdict generation, and audit trail.

The MVP demonstrates that this structured approach can outperform a simplified single-step baseline on a labeled evaluation dataset.

ReleaseGuard is a practical AI quality engineering tool for modern software teams building with or around AI-assisted development.

