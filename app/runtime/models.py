from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class RuntimeCheckResult(BaseModel):
    """
    Standardized result for a runtime governance check.
    """
    allowed: bool
    reason_code: str
    message: str

class RuntimeState(BaseModel):
    """
    Tracks the active execution state of a platform request.
    Used for limit enforcement and budget monitoring.
    """
    request_id: str
    strategy_path: str
    status: str = "INITIALIZED"
    
    # Execution Counters
    step_count: int = 0
    tool_calls: int = 0
    retries_used: int = 0
    
    # Budget Tracking
    model_calls: int = 0
    tokens_estimated: int = 0
    budget_used_usd: float = 0.0
    
    # Temporal Tracking
    start_time: datetime = Field(default_factory=datetime.utcnow)
    elapsed_seconds: float = 0.0
    
    # Governance Flags
    governance_violations: List[str] = Field(default_factory=list)
    fallback_triggered: bool = False
    fallback_reason: Optional[str] = None
