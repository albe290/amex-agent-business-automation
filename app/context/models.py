from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class RetrievedEvidence(BaseModel):
    """
    Raw data retrieved from a source.
    """
    source_type: str  # e.g., 'policy', 'case_history', 'customer'
    source_id: str
    title: str
    content: str
    relevance_score: float = 0.0
    metadata: Dict[str, Any] = Field(default_factory=dict)

class EnrichedEvidence(BaseModel):
    """
    Transformed evidence with extracted facts and risk signals.
    """
    source_type: str
    source_id: str
    summary: str
    key_facts: List[str]
    risk_signals: List[str]
    policy_tags: List[str]

class ContextPacket(BaseModel):
    """
    The final handoff object for the platform.
    """
    request_id: str
    request_summary: str
    customer_context: Dict[str, Any]
    transaction_context: Dict[str, Any]
    evidence: List[EnrichedEvidence] = Field(default_factory=list)
    policy_references: List[str] = Field(default_factory=list)
    prior_cases: List[str] = Field(default_factory=list)
    missing_fields: List[str] = Field(default_factory=list)
    context_completeness_score: float = 0.0
    retrieval_gaps: List[str] = Field(default_factory=list)
