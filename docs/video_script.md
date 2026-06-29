# ReleaseGuard Video Script

## 0:00–0:30 — Intro

Hi, my project is called ReleaseGuard.

ReleaseGuard is a multi-agent release readiness evaluator for software requirements.

The core question it answers is simple:

Can this feature safely ship?

It is built for QA engineers, product teams, engineering managers, and teams using AI-assisted development tools.

The goal is to catch unclear requirements, missing risks, and weak test coverage before development starts.

---

## 0:30–1:10 — Problem

AI-assisted development makes it easier to generate code, tests, and pull requests very quickly.

But faster code generation does not automatically mean better software quality.

Many production bugs start before code is written.

They start with unclear requirements, missing acceptance criteria, undefined failure behavior, missing privacy expectations, or weak release readiness decisions.

ReleaseGuard shifts quality review earlier in the lifecycle by evaluating the requirement itself.

---

## 1:10–2:00 — How ReleaseGuard Works

ReleaseGuard uses a structured multi-step pipeline.

First, input guardrails check the requirement for length, prompt injection patterns, and possible PII.

Then the Requirement Analyzer detects gaps, assumptions, and ambiguity.

Next, the Risk and Security Auditor identifies product, privacy, security, compliance, and operational risks.

The Test Strategist generates functional, negative, edge-case, API, accessibility, and security test ideas.

Finally, the Release Judge calculates a readiness score and produces a verdict: SHIP, SHIP_WITH_CAUTION, MANUAL_REVIEW, or NO_SHIP.

The final output is a deterministic Markdown report with an audit trail.

---

## 2:00–2:50 — Demo

For the demo, I use a privacy-sensitive account deletion requirement.

The input says:

As a user, I want to delete my account permanently from the settings page.

ReleaseGuard evaluates this requirement and identifies missing information around data retention, confirmation behavior, account deletion policy, privacy risk, and compliance expectations.

Because account deletion is high risk and the requirement is incomplete, ReleaseGuard returns a NO_SHIP verdict.

It also generates test ideas and an audit trail, so the decision is traceable instead of just being a generic AI response.

---

## 2:50–3:40 — Evaluation

I evaluated ReleaseGuard against a labeled dataset of 10 software requirements.

The dataset includes account deletion, password reset, checkout discount codes, OAuth login, avatar upload, admin user search, dark mode, newsletter signup, and personal data export.

Each example includes expected gaps, expected risks, expected severity, and an expected release verdict.

I compared ReleaseGuard against a simplified single-step baseline.

ReleaseGuard achieved:

* 90 percent verdict accuracy
* 90 percent average gap recall
* 96.67 percent average risk recall

The single-step baseline achieved:

* 40 percent verdict accuracy
* 33.33 percent average gap recall
* 31.67 percent average risk recall

This shows that the structured multi-step pipeline performs better than a one-pass review on this labeled dataset.

---

## 3:40–4:25 — Course Concepts

This project demonstrates several AI agent concepts.

It uses specialized agent roles, structured orchestration, security-aware input guardrails, evaluation metrics, baseline comparison, and reproducible local execution.

The current MVP includes an optional Gemini-powered Requirement Analyzer and deterministic rule-based fallback, so the behavior remains testable and measurable even without an API key.

A future version can replace or augment the deterministic agents with Google ADK-powered LLM agents while keeping the same schemas, scoring logic, guardrails, and evaluation framework.

---

## 4:25–5:00 — Wrap-Up

ReleaseGuard is not just a test case generator.

Its goal is to produce a traceable release readiness decision before development starts.

The project turns requirement review into a measurable quality signal.

For teams building with AI-assisted development tools, ReleaseGuard helps answer an important question before code is written:

Is this feature actually ready to build and eventually ship?

Thank you.

