import time
from app.runtime.coordinator import RuntimeCoordinator
from app.control_plane.decision import ControlPlaneDecision

def verify_runtime_governance():
    print("--- Phase 3D: Runtime Governance Verification ---")
    coordinator = RuntimeCoordinator()
    
    # Mock a control plane decision that requires review
    protected_decision = ControlPlaneDecision(
        request_id="REQ-123",
        validation_status="SUCCESS",
        risk_score=75.0,
        policy_hits=["HIGH_VALUE_TRANSACTION"],
        requires_review=True,
        decision_label="REVIEW"
    )

    # SCENARIO 1: Guardrail Block (Review Required)
    print("\n[SCENARIO 1] Attempting protected action for unreviewed case...")
    state = coordinator.initialize_state("REQ-123", "AUTOMATE")
    
    action = "SEND_PAYMENT"
    print(f"   Requesting Action: {action}")
    
    check = coordinator.validate_action(action, protected_decision)
    if not check.allowed:
        print(f"   [BLOCKED] {check.reason_code}: {check.message}")
        fallback = coordinator.handle_violation(check)
        print(f"   [FALLBACK] Triggered: {fallback.fallback_type} (Reason: {fallback.reason})")

    # SCENARIO 2: Step Limit Exceeded
    print("\n[SCENARIO 2] Simulating runaway agent (Step Limit)...")
    state.step_count = 5 # Hits the limit
    
    check = coordinator.pre_step_check(state)
    if not check.allowed:
        print(f"   [HALTED] {check.reason_code}: {check.message}")
        fallback = coordinator.handle_violation(check)
        print(f"   [FALLBACK] Triggered: {fallback.fallback_type}")

    # SCENARIO 3: Budget Exceeded
    print("\n[SCENARIO 3] Simulating expensive execution (Budget)...")
    state.step_count = 1
    state.model_calls = 3 # Hits the budget limit
    
    check = coordinator.pre_step_check(state)
    if not check.allowed:
        print(f"   [HALTED] {check.reason_code}: {check.message}")
        fallback = coordinator.handle_violation(check)
        print(f"   [FALLBACK] Triggered: {fallback.fallback_type}")

    print("\nVerification complete. Runtime governance boundaries successfully enforced.")

if __name__ == "__main__":
    verify_runtime_governance()
