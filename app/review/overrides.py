from app.review.models import OverrideRecord, ReviewPacket, ReviewDecision

class OverrideTracker:
    """
    Identifies and logs deviations between system recommendations and human choices.
    """
    
    def detect_and_log(self, packet: ReviewPacket, decision: ReviewDecision) -> OverrideRecord:
        """
        Checks if the human decision overridden the system's suggested path.
        """
        system_suggested = packet.suggested_next_action
        human_chosen = decision.approved_action
        
        is_override = system_suggested != human_chosen
        
        if is_override:
            return OverrideRecord(
                review_id=packet.review_id,
                system_recommendation=system_suggested,
                reviewer_decision=human_chosen,
                override_reason=decision.decision_reason,
                impact_level="HIGH" if decision.decision == "REJECT" else "MEDIUM"
            )
            
        return None # No override detected
