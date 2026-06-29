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

| Metric | ReleaseGuard Pipeline | Single-Step Baseline |
|---|---:|---:|
| Dataset size | 10 requirements | 10 requirements |
| Verdict accuracy | 90.00% | 40.00% |
| Average gap recall | 90.00% | 33.33% |
| Average risk recall | 96.67% | 31.67% |

---

## What the Evaluation Measures

### Verdict Accuracy

Measures whether the final release decision matches the expected labeled verdict.

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

## Baseline Comparison

The MVP compares ReleaseGuard's structured multi-step pipeline against a simplified single-step baseline.

The baseline performs a direct one-pass requirement review without the specialized ReleaseGuard stages.

ReleaseGuard performs better because it separates the quality review into focused steps:

1. Requirement analysis
2. Risk and security review
3. Test strategy generation
4. Release judgment
5. Deterministic scoring

This comparison helps demonstrate that the architecture is not just more complex, but measurably more effective on the labeled dataset.

---

## Key Finding

The ReleaseGuard pipeline significantly outperformed the single-step baseline:

- +50 percentage points in verdict accuracy
- +56.67 percentage points in average gap recall
- +65 percentage points in average risk recall

The strongest detection areas are:

- privacy-sensitive flows
- account deletion
- data export
- file upload
- admin access
- authentication-related requirements

---

## Known Limitation

The Requirement Analyzer can use Gemini Flash when GOOGLE_API_KEY is configured.

The Risk Auditor, Test Strategist, and Release Judge remain rule-based to preserve reproducible, testable evaluation. The evaluation dataset runs in rule-based mode so results remain deterministic and reproducible without an API key.

The current baseline is a simplified single-step rule system, not a live LLM baseline.

---

## Why This Matters

ReleaseGuard is designed around a practical quality engineering problem:

AI-assisted development makes it easier to generate code quickly, but teams still need a reliable way to evaluate whether the original requirement is clear, testable, secure, and ready to ship.

This evaluation protocol turns release readiness from a subjective review conversation into a measurable quality signal.
