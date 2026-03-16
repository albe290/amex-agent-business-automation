from typing import Dict, Any
from app.control_plane.validator import ControlPlaneValidator
from app.control_plane.risk import RiskEngine
from app.control_plane.policy import PolicyEngine
from app.control_plane.decision import ControlPlaneDecision
from app.intake.schemas import PlatformRequest

class ControlPlaneCoordinator:
    """
    Orchestrates the governance flow within the Control Plane.
    Runs validation, risk scoring, and policy evaluation to produce a Decision.
    """
    
    def __init__(self):
        self.validator = ControlPlaneValidator()
        self.risk_engine = RiskEngine()
        self.policy_engine = PolicyEngine()

    def process_request(self, request: PlatformRequest) -> ControlPlaneDecision:
        """
        End-to-end execution of the control plane logic.
        """
        # 1. Input Validation
        is_valid, reason = self.validator.validate_input(str(request.business_payload))
        if not is_valid:
            return ControlPlaneDecision(
                validation_status="FAILED",
                risk_score=100.0,
                policy_hits=["SECURITY_VALIDATION_FAILURE"],
                requires_review=True,
                block_reason=reason
            )

        # 2. Risk Scoring
        risk_score = self.risk_engine.calculate_score(
            request.business_payload, 
            request.risk_metadata,
            request.customer_context
        )

        # 3. Policy Evaluation
        flags = []
        if request.business_payload.get("amount", 0) > 5000:
            flags.append("HIGH_VALUE_TRANSACTION")
            
        requires_review, policy_hits, allowed_actions = self.policy_engine.evaluate(
            risk_score, 
            flags
        )

        # 4. Final Decision Construction
        return ControlPlaneDecision(
            validation_status="SUCCESS",
            risk_score=risk_score,
            policy_hits=policy_hits,
            allowed_actions=allowed_actions,
            requires_review=requires_review
        )
