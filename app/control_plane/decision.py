from pydantic import BaseModel, Field
from typing import List, Optional

class ControlPlaneDecision(BaseModel):
    """
    The deterministic output of the Control Plane.
    This contract governs whether the request proceeds to the intelligent agentic layer.
    """
    validation_status: str = Field(..., description="SUCCESS or FAILED")
    risk_score: float = Field(..., ge=0, le=100, description="Normalized risk score (0-100)")
    policy_hits: List[str] = Field(default_factory=list, description="List of specific corporate policies triggered")
    allowed_actions: List[str] = Field(default_factory=list, description="Actions the system is permitted to take based on policy")
    requires_review: bool = Field(default=False, description="Whether human-in-the-loop intervention is mandatory")
    block_reason: Optional[str] = Field(None, description="Reason for blocking, if validation_status is FAILED")

    model_config = {
        "json_schema_extra": {
            "example": {
                "validation_status": "SUCCESS",
                "risk_score": 15.5,
                "policy_hits": ["HIGH_VALUE_TRANSACTION"],
                "allowed_actions": ["PROCEED_TO_AI_INVESTIGATION", "LOG_AUDIT"],
                "requires_review": False
            }
        }
    }
