from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


class Severity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class Verdict(str, Enum):
    SHIP = "SHIP"
    SHIP_WITH_CAUTION = "SHIP_WITH_CAUTION"
    NO_SHIP = "NO_SHIP"
    MANUAL_REVIEW = "MANUAL_REVIEW"


class RequirementInput(BaseModel):
    text: str = Field(..., min_length=10)
    source: str = "manual_input"


class RequirementGap(BaseModel):
    title: str
    description: str
    severity: Severity


class Assumption(BaseModel):
    description: str
    risk_if_wrong: str
    severity: Severity


class RiskFinding(BaseModel):
    title: str
    description: str
    severity: Severity
    category: Literal["product", "security", "privacy", "compliance", "operational"]


class TestCase(BaseModel):
    title: str
    description: str
    priority: Literal["P0", "P1", "P2"]
    test_type: Literal["functional", "negative", "edge", "api", "accessibility", "security"]


class RequirementAnalysis(BaseModel):
    feature_summary: str
    gaps: list[RequirementGap]
    assumptions: list[Assumption]
    ambiguity_notes: list[str]
    clarity_score: int = Field(..., ge=0, le=100)


class RiskSecurityAnalysis(BaseModel):
    findings: list[RiskFinding]
    recommended_mitigations: list[str]


class TestStrategy(BaseModel):
    test_cases: list[TestCase]
    coverage_notes: list[str]


class CategoryScores(BaseModel):
    requirement_quality: int = Field(..., ge=0, le=100)
    risk_security: int = Field(..., ge=0, le=100)
    test_coverage: int = Field(..., ge=0, le=100)
    release_confidence: int = Field(..., ge=0, le=100)


class ReleaseDecision(BaseModel):
    readiness_score: int = Field(..., ge=0, le=100)
    category_scores: CategoryScores
    verdict: Verdict
    rationale: str
    manual_review_required: bool


class AuditTrailItem(BaseModel):
    step: str
    summary: str


class ReleaseGuardReport(BaseModel):
    requirement: RequirementInput
    requirement_analysis: RequirementAnalysis
    risk_security_analysis: RiskSecurityAnalysis
    test_strategy: TestStrategy
    release_decision: ReleaseDecision
    audit_trail: list[AuditTrailItem]
