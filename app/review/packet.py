import uuid
from typing import List, Dict, Any
from app.review.models import ReviewPacket
from app.intake.schemas import PlatformRequest
from app.context.models import ContextPacket
from app.control_plane.decision import ControlPlaneDecision
from app.agents.models import AnalystOutput

class ReviewPacketBuilder:
    """
    Assembles a ReviewPacket from disparate platform state objects.
    """
    
    def build_packet(
        self, 
        request: PlatformRequest, 
        context: ContextPacket, 
        decision: ControlPlaneDecision,
        agent_findings: List[Dict[str, Any]],
        reason: str
    ) -> ReviewPacket:
        """
        Creates a clean, reviewer-friendly summary of the case state.
        """
        review_id = f"REV-{str(uuid.uuid4())[:8].upper()}"
        
        # 1. Summarize Agent Findings
        primary_recommendation = "No recommendation provided"
        if agent_findings:
            # Assume last agent output contains the high-level recommendation
            last_result = agent_findings[-1]
            if "recommended_path" in last_result:
                primary_recommendation = last_result["recommended_path"]
            elif "final_recommendation" in last_result:
                primary_recommendation = last_result["final_recommendation"]

        # 2. Extract evidence snippets
        evidence_titles = [e.title for e in context.evidence]
        
        return ReviewPacket(
            review_id=review_id,
            request_id=request.request_id,
            strategy_selected=decision.validation_status,
            risk_score=decision.risk_score,
            policy_hits=decision.policy_hits,
            requires_review_reason=reason,
            request_summary=context.request_summary,
            agent_recommendation=primary_recommendation,
            supporting_evidence=evidence_titles,
            context_completeness_score=context.context_completeness_score,
            suggested_next_action=primary_recommendation
        )
