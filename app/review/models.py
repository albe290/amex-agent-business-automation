from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class ReviewPacket(BaseModel):
    """
    Structured evidence packet for human review.
    Contains everything a human needs to make an informed decision.
    """
    review_id: str
    request_id: str
    strategy_selected: str
    risk_score: float
    policy_hits: List[str]
    requires_review_reason: str
    request_summary: str
    agent_recommendation: str
    supporting_evidence: List[str]
    context_completeness_score: float
    suggested_next_action: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ReviewDecision(BaseModel):
    """
    Captured decision from a human reviewer.
    """
    review_id: str
    reviewer_name: str
    decision: str  # APPROVE, REJECT, SEND_BACK, OVERRIDE
    decision_reason: str
    notes: Optional[str] = None
    approved_action: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class OverrideRecord(BaseModel):
    """
    Explicit log of a reviewer overriding a system recommendation.
    """
    review_id: str
    system_recommendation: str
    reviewer_decision: str
    override_reason: str
    impact_level: str = "MEDIUM" # LOW, MEDIUM, HIGH

class ReviewQueueItem(BaseModel):
    """
    Metadata for tracking a case in the review queue.
    """
    review_id: str
    request_id: str
    status: str = "PENDING" # PENDING, IN_REVIEW, CLOSED
    priority: int = 1 # 1 (High) to 3 (Low)
    assigned_to: Optional[str] = None
