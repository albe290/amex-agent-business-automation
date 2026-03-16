from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class EvalCase(BaseModel):
    """
    Defines a test scenario with inputs and expected outcomes.
    """
    case_id: str
    scenario_type: str  # e.g., 'SAFE_AUTOMATION', 'ELEVATED_RISK'
    request_payload: Dict[str, Any]
    expected_validation_status: str = "SUCCESS"
    expected_strategy: str
    expected_review_required: bool
    expected_policy_hits: List[str] = Field(default_factory=list)

class EvalResult(BaseModel):
    """
    Captures the actual performance vs expected outcomes for a case.
    """
    case_id: str
    scenario_type: str
    actual_validation_status: str
    actual_strategy: str
    actual_review_required: bool
    actual_policy_hits: List[str]
    passed: bool
    failure_reasons: List[str] = Field(default_factory=list)
    latency_ms: float = 0.0

class MetricSnapshot(BaseModel):
    """
    Aggregated performance signals across an evaluation run.
    """
    total_cases: int
    pass_rate: float
    automation_rate: float
    review_rate: float
    escalation_rate: float
    block_rate: float
    override_rate: float = 0.0
    strategy_match_rate: float
    policy_hit_precision: float

class Scorecard(BaseModel):
    """
    High-level qualitative summary of platform health.
    """
    governance_score: str  # POOR, FAIR, STRONG
    routing_quality: str
    human_alignment: str
    operational_efficiency: str
    summary_notes: str
