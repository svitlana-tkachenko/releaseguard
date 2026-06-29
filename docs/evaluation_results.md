# ReleaseGuard Evaluation Results

## Evaluation Summary

ReleaseGuard was evaluated against a labeled dataset of 10 software requirements.

The dataset includes requirements across different product and risk categories:

- account deletion
- password reset
- profile update
- checkout discount code
- OAuth login
- newsletter signup
- avatar upload
- admin user search
- dark mode toggle
- personal data export

Each requirement includes expected gaps, expected risks, expected severity, and expected Ship / No Ship verdict.

---

## Current MVP Results

| Metric | Result |
|---|---:|
| Dataset size | 10 requirements |
| Verdict accuracy | 90.00% |
| Average gap recall | 90.00% |
| Average risk recall | 96.67% |

---

## What the Evaluation Measures

### Verdict Accuracy

Measures whether ReleaseGuard's final release decision matches the expected labeled verdict.

Example verdicts:

- SHIP
- SHIP_WITH_CAUTION
- MANUAL_REVIEW
- NO_SHIP

### Gap Recall

Measures whether ReleaseGuard detects expected requirement gaps, such as:

- missing acceptance criteria
- undefined failure behavior
- missing access control
- missing privacy requirements
- missing rollback behavior

### Risk Recall

Measures whether ReleaseGuard detects expected product, security, privacy, compliance, and operational risks.

---

## Key Finding

The MVP demonstrates that a structured multi-step release readiness pipeline can detect meaningful requirement gaps and product risks before implementation begins.

The strongest detection areas are:

- privacy-sensitive flows
- account deletion
- data export
- file upload
- admin access
- authentication-related requirements

---

## Known Limitation

The current MVP uses deterministic rule-based agent logic.

Future versions will replace or augment these rules with LLM-powered agents using Google ADK while preserving structured schemas, deterministic scoring, and reproducible evaluation.

---

## Why This Matters

ReleaseGuard is designed around a practical quality engineering problem:

AI-assisted development makes it easier to generate code quickly, but teams still need a reliable way to evaluate whether the original requirement is clear, testable, secure, and ready to ship.

This evaluation protocol turns release readiness from a subjective review conversation into a measurable quality signal.
