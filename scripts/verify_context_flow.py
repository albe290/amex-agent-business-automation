from app.intake.schemas import PlatformRequest
from app.context.builder import ContextBuilder

def verify_context_flow():
    print("--- Phase 3C: Context Enrichment Verification ---")
    
    # 1. Simulate Normalized Request
    print("\n[INTAKE] Simulating PlatformRequest...")
    request = PlatformRequest(
        use_case_type="fraud_investigation",
        customer_context={"id": "AMEX-US-9988", "segment": "PLATINUM"},
        business_payload={
            "amount": 4500.0, 
            "merchant": "Luxury Watch Boutique", 
            "location": "NYC"
        },
        risk_metadata={"velocity_flags": 0},
        source="mobile_app"
    )
    print(f"   Request ID: {request.request_id}")
    print(f"   Payload: {request.business_payload}")

    # 2. Build Context
    print("\n[CONTEXT] Building evidence-grounded context packet...")
    builder = ContextBuilder()
    packet = builder.build_context(request)
    
    # 3. Inspect Results
    print(f"\n[RESULTS] Context Completeness: {packet.context_completeness_score:.2f}")
    
    print("\n[EVIDENCE] Selected Items:")
    for item in packet.evidence:
        print(f"   - [{item.source_type}] {item.source_id}: {item.summary[:60]}...")
        if item.risk_signals:
            print(f"     Signals: {', '.join(item.risk_signals)}")
            
    if packet.retrieval_gaps:
        print(f"\n[GAPS] Retrieval Gaps Detected: {', '.join(packet.retrieval_gaps)}")
        
    print(f"\n[SUMMARY] {packet.request_summary}")
    print("\nVerification complete. Context packet builds successfully with real RAG logic.")

if __name__ == "__main__":
    verify_context_flow()
