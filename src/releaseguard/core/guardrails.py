import re
from dataclasses import dataclass, field


@dataclass
class GuardrailResult:
    is_allowed: bool = True
    flags: list[str] = field(default_factory=list)
    summary: str = "Input passed guardrail checks."


PROMPT_INJECTION_PATTERNS = [
    "ignore previous instructions",
    "disregard previous instructions",
    "forget your instructions",
    "reveal your prompt",
    "system prompt",
    "developer message",
    "jailbreak",
    "override instructions",
    "act as",
]

PII_PATTERNS = {
    "email": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
    "phone": re.compile(r"\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"),
    "ssn": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    "credit_card_like": re.compile(r"\b(?:\d[ -]*?){13,16}\b"),
}


def run_input_guardrails(requirement_text: str, max_chars: int = 5000) -> GuardrailResult:
    lower_text = requirement_text.lower()
    flags: list[str] = []

    if len(requirement_text) > max_chars:
        return GuardrailResult(
            is_allowed=False,
            flags=["length_limit_exceeded"],
            summary=f"Input blocked because it exceeds the {max_chars} character limit.",
        )

    for pattern in PROMPT_INJECTION_PATTERNS:
        if pattern in lower_text:
            flags.append("prompt_injection_suspected")
            break

    for label, regex in PII_PATTERNS.items():
        if regex.search(requirement_text):
            flags.append(f"pii_detected:{label}")

    if flags:
        return GuardrailResult(
            is_allowed=True,
            flags=flags,
            summary="Input allowed with guardrail flags: " + ", ".join(flags),
        )

    return GuardrailResult()
