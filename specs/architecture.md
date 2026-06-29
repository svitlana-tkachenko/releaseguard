# ReleaseGuard Architecture

## Architecture Overview

ReleaseGuard uses a focused multi-agent pipeline to evaluate software requirements before development begins.

The system does not try to generate code or replace QA teams. Its goal is to answer one high-value product question:

**Can this feature safely ship?**

ReleaseGuard produces a traceable release readiness report that connects requirement gaps, risks, test coverage, scoring, and final Ship / No Ship recommendation.

---

## MVP Architecture

```text
Raw Requirement Text
        ↓
Orchestrator Agent
manages state, routing, and retry trigger
        ↓
A1 Requirement Analyzer
detects gaps, assumptions, ambiguity, and clarity score
        ↓
A2 Risk & Security Auditor
classifies product risk, security risk, severity, and compliance concerns
        ↓
A3 Test Strategist
generates functional, negative, edge-case, API, and accessibility test ideas
        ↓
A4 Release Judge
produces readiness score, category breakdown, and Ship / No Ship verdict
        ↓
Conditional Critique Agent
runs only if score is between 40 and 70
        ↓
Report Assembler
deterministic Python formatter
        ↓
Release Readiness Report
```

---

## Agent Responsibilities

### Orchestrator Agent

The Orchestrator controls the workflow.

Responsibilities:

* Accept raw requirement text
* Validate input
* Manage state between agents
* Pass typed outputs from one step to the next
* Trigger the Critique Agent only when needed
* Send final structured data to the Report Assembler

The Orchestrator is responsible for routing, not analysis.

---

### A1 Requirement Analyzer

The Requirement Analyzer evaluates the quality of the original requirement.

Responsibilities:

* Summarize the feature
* Detect missing acceptance criteria
* Identify ambiguity
* List assumptions
* Assign requirement clarity score

Output:

* Feature summary
* Requirement gaps
* Assumptions
* Ambiguity notes
* Clarity score

---

### A2 Risk & Security Auditor

The Risk & Security Auditor identifies product, security, privacy, and compliance risks.

Responsibilities:

* Classify risk severity
* Identify missing security requirements
* Flag privacy concerns
* Detect compliance-sensitive areas
* Highlight unsafe assumptions

Output:

* Risk findings
* Security findings
* Severity levels
* Compliance concerns
* Recommended mitigations

---

### A3 Test Strategist

The Test Strategist creates structured test coverage from the requirement and risk findings.

Responsibilities:

* Generate functional test cases
* Generate negative test cases
* Generate edge cases
* Suggest API validation ideas
* Suggest accessibility checks
* Prioritize test coverage

Output:

* Functional tests
* Negative tests
* Edge cases
* API checks
* Accessibility checks
* Coverage notes

---

### A4 Release Judge

The Release Judge evaluates all previous findings and produces the release decision.

Responsibilities:

* Merge agent outputs
* Identify unresolved gaps
* Score release readiness from 0 to 100
* Produce category-level scores
* Decide Ship / No Ship
* Explain rationale

Output:

* Readiness score
* Category score breakdown
* Ship / No Ship verdict
* Decision rationale
* Manual review flag if needed

---

### Conditional Critique Agent

The Critique Agent only runs when the Release Judge produces an uncertain score.

Trigger condition:

```text
40 <= readiness_score <= 70
```

Responsibilities:

* Review the Judge output
* Identify weak sections
* Request one refinement pass
* Improve final decision quality

The Critique Agent runs only once to avoid infinite loops and overengineering.

---

### Report Assembler

The Report Assembler is not an LLM agent.

It is deterministic Python logic that formats structured outputs into a Markdown report.

Responsibilities:

* Apply report template
* Format scores and sections
* Preserve traceability
* Generate final Markdown report

---

## Design Decisions

### Why sequential instead of fully parallel?

The MVP uses a sequential pipeline because each step depends on the previous one.

Requirement analysis informs risk analysis.

Risk analysis informs test strategy.

All findings inform the final release judgment.

This makes the system easier to debug, easier to explain, and more realistic to finish within the Kaggle deadline.

---

### Why not use a Planner and Dispatcher?

The MVP has a fixed workflow.

Dynamic planning and dispatching would add complexity without improving the core release readiness decision.

---

### Why is the Report Assembler deterministic?

Report formatting does not require LLM reasoning.

Using deterministic formatting reduces hallucination risk and makes the output more stable and reproducible.

---

### Why include a conditional Critique Agent?

The Critique Agent demonstrates agentic self-review without creating unnecessary complexity.

It only runs when the release decision is uncertain.

This makes the retry loop easy to explain and easy to demo.

---

## Core Product Differentiator

ReleaseGuard does not simply generate test cases.

It produces a traceable release decision.

The value chain is:

```text
Requirement
→ Gap detection
→ Risk classification
→ Test coverage
→ Readiness score
→ Ship / No Ship verdict
→ Audit trail
```

This makes ReleaseGuard an AI-native quality gate for modern software teams.

