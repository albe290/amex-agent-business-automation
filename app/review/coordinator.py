from typing import List, Dict, Any, Optional
from app.review.models import ReviewPacket, ReviewDecision, OverrideRecord
from app.review.packet import ReviewPacketBuilder
from app.review.queue import ReviewQueue
from app.review.approval import ReviewApprovalHandler
from app.review.overrides import OverrideTracker
from app.intake.schemas import PlatformRequest
from app.context.models import ContextPacket
from app.control_plane.decision import ControlPlaneDecision

class ReviewCoordinator:
    """
    Top-level controller for the Human Review lifecycle.
    """
    
    def __init__(self):
        self.packet_builder = ReviewPacketBuilder()
        self.queue = ReviewQueue()
        self.approval_handler = ReviewApprovalHandler()
        self.override_tracker = OverrideTracker()

    def initiate_review(
        self, 
        request: PlatformRequest, 
        context: ContextPacket, 
        decision: ControlPlaneDecision,
        agent_findings: List[Dict[str, Any]],
        reason: str
    ) -> str:
        """
        Creates a review packet and places it in the queue.
        Returns the review_id.
        """
        packet = self.packet_builder.build_packet(request, context, decision, agent_findings, reason)
        self.queue.enqueue_review(packet)
        return packet.review_id

    def submit_decision(
        self, 
        review_id: str, 
        decision_code: str, 
        reason: str, 
        reviewer: str,
        notes: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Processes a human decision, checks for overrides, and updates the queue.
        """
        packet = self.queue.get_packet(review_id)
        if not packet:
            raise ValueError(f"Review case {review_id} not found.")
            
        # 1. Capture Decision
        decision = self.approval_handler.process_decision(packet, decision_code, reason, reviewer, notes)
        
        # 2. Track Overrides
        override = self.override_tracker.detect_and_log(packet, decision)
        
        # 3. Update Status
        self.queue.update_status(review_id, status="CLOSED")
        
        return {
            "decision": decision,
            "override": override,
            "final_action": decision.approved_action
        }
