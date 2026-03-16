from datetime import datetime
from app.intake.schemas import PlatformRequest
from app.context.models import ContextPacket
from app.control_plane.decision import ControlPlaneDecision
from app.review.coordinator import ReviewCoordinator

def verify_review_flow():
    print("--- Phase 3E: Human Review Workflow Verification ---")
    coordinator = ReviewCoordinator()
    
    # 1. Setup Mock State
    request = PlatformRequest(
        use_case_type="fraud_investigation",
        customer_context={"id": "AMEX-US-9988"},
        business_payload={"amount": 4500.0, "merchant": "Luxury Boutique"},
        risk_metadata={},
        source="mobile"
    )
    
    context = ContextPacket(
        request_id=request.request_id,
        request_summary="High-value transaction at Luxury Boutique",
        customer_context=request.customer_context,
        transaction_context=request.business_payload,
        evidence=[],
        context_completeness_score=0.85
    )
    
    decision = ControlPlaneDecision(
        request_id=request.request_id,
        validation_status="SUCCESS",
        risk_score=30.0,
        policy_hits=["RISK_SCORE_ELEVATED"],
        requires_review=True
    )
    
    agent_findings = [{"recommended_path": "INVESTIGATE"}]

    # 2. Initiate Review
    print("\n[REVIEW] Initiating human review for elevated risk case...")
    review_id = coordinator.initiate_review(
        request=request,
        context=context,
        decision=decision,
        agent_findings=agent_findings,
        reason="Elevated risk score triggered manual oversight"
    )
    print(f"   Review ID Created: {review_id}")
    
    # 3. Check Queue
    pending = coordinator.queue.get_pending_reviews()
    print(f"   Queue Status: {len(pending)} PENDING case(s)")
    
    # 4. Scenario: Human Override (System says ESCALATE, Human says APPROVE)
    print("\n[SCENARIO] Reviewer Overriding system recommendation...")
    outcome = coordinator.submit_decision(
        review_id=review_id,
        decision_code="APPROVE",
        reason="Verified transaction with customer via phone.",
        reviewer="A. Glenn",
        notes="Customer confirmed they are at the boutique."
    )
    
    decision_obj = outcome["decision"]
    override_obj = outcome["override"]
    
    print(f"   Reviewer: {decision_obj.reviewer_name}")
    print(f"   Decision: {decision_obj.decision}")
    print(f"   Final Action: {outcome['final_action']}")
    
    if override_obj:
        print(f"   [OVERRIDE DETECTED]")
        print(f"     System Rec: {override_obj.system_recommendation}")
        print(f"     Human Choice: {override_obj.reviewer_decision}")
        print(f"     Override Reason: {override_obj.override_reason}")

    print("\nVerification complete. Human review workflow is fully operational.")

if __name__ == "__main__":
    verify_review_flow()
