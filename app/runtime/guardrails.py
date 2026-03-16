from typing import Dict, Any
from app.runtime.models import RuntimeCheckResult
from app.control_plane.decision import ControlPlaneDecision

class RuntimeGuardrails:
    """
    Enforces real-time action safety and policy boundaries.
    """
    
    def validate_action(self, action_name: str, decision: ControlPlaneDecision) -> RuntimeCheckResult:
        """
        Validates if a specific action is allowed given the control plane decision.
        """
        # Rule 1: Block autonomous outbound actions if review is required
        outbound_actions = ["SEND_PAYMENT", "NOTIFY_CUSTOMER", "OFFER_REFUND"]
        if action_name in outbound_actions and decision.requires_review:
            return RuntimeCheckResult(
                allowed=False,
                reason_code="GUARDRAIL_BLOCK_REVIEW_REQUIRED",
                message=f"Action '{action_name}' blocked. Human review is required."
            )

        # Rule 2: Block high-risk actions entirely (optional policy)
        if decision.risk_score > 90 and action_name == "PRE_APPROVE_DISPUTE":
             return RuntimeCheckResult(
                allowed=False,
                reason_code="GUARDRAIL_BLOCK_HIGH_RISK",
                message="Pre-approval blocked due to critical risk score."
            )

        return RuntimeCheckResult(allowed=True, reason_code="GUARDRAIL_OK", message="Action permitted.")
