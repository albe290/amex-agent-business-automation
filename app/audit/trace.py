from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime
from monitoring.metrics import event_bus

class AuditTrace(BaseModel):
    """
    Mutable trace of a single platform execution.
    Captured for internal audit and explainability.
    """
    request_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    strategy_path: str
    control_plane_result: Dict[str, Any]
    agent_outputs: List[Dict[str, Any]] = Field(default_factory=list)
    context_completeness: Optional[float] = None
    evidence_count: int = 0
    final_outcome: str
    requires_human_review: bool = False
    review_decision: Optional[Dict[str, Any]] = None

class AuditLogger:
    """
    Utility to record traces to the audit log.
    In production, this would write to an immutable database or Kafka topic.
    """
    async def log_trace(self, trace: AuditTrace):
        # Placeholder for audit logging mechanism
        print(f"[AUDIT] Logging trace for request {trace.request_id} with outcome {trace.final_outcome}")
        
        # Emit to real-time dashboard
        await event_bus.emit("TRANSACTION_COMPLETED", {
            "request_id": trace.request_id,
            "strategy": trace.strategy_path,
            "outcome": trace.final_outcome,
            "requires_review": trace.requires_human_review
        })
