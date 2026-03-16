from typing import Optional
from app.review.models import ReviewDecision, ReviewPacket

class ReviewApprovalHandler:
    """
    Logic for capturing and validating human reviewer decisions.
    """
    
    def process_decision(
        self, 
        packet: ReviewPacket, 
        decision_code: str, 
        reason: str, 
        reviewer: str,
        notes: Optional[str] = None
    ) -> ReviewDecision:
        """
        Creates a structured ReviewDecision record from human input.
        """
        # Determine the approved action
        # In a real system, this might map 'APPROVE' to the system's suggestion
        approved_action = packet.suggested_next_action
        if decision_code == "REJECT":
            approved_action = "TERMINATE"
        elif decision_code == "SEND_BACK":
            approved_action = "REQUEST_MORE_INFO"
            
        return ReviewDecision(
            review_id=packet.review_id,
            reviewer_name=reviewer,
            decision=decision_code,
            decision_reason=reason,
            notes=notes,
            approved_action=approved_action
        )
