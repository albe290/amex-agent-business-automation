import sys
import os

# 1. Dynamically append the Sentinel Runtime project dir to path
SENTINEL_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "sentinel-runtime")
)
if SENTINEL_DIR not in sys.path:
    sys.path.insert(0, SENTINEL_DIR)

# 2. Import Sentinel's native Risk structures
try:
    from validator.schemas import Step, Constraints
    from validator.policy_loader import PolicyConfig
    from validator.risk import score_step
    from validator.guardrails import load_policy
except ImportError as e:
    print(
        f"[FATAL] Could not connect to the Sentinel Runtime codebase at {SENTINEL_DIR}. Ensure it exists."
    )
    raise e


class SentinelClient:
    def __init__(self):
        # 3. Load the central yaml policy from Sentinel
        policy_path = os.path.join(SENTINEL_DIR, "policy", "policy.yaml")
        self.policy_config = load_policy(policy_path)

    def evaluate(self, action: str, context: dict) -> str:
        """
        Evaluates the risk of an action based on context,
        using the actual native sentinel-runtime Risk Engine!
        """
        actor = context.get("actor", "customer")
        amount = context.get("transaction_amount", 0)

        # Build the exact data model Sentinel expects
        step = Step(
            id="req_x1",
            tool=action,
            args=context,
            reason="Amex Agent Automated Workflow Execution",
        )

        # Determine environmental risk parameters based on actor
        # If it's a customer, we limit their damage scope natively
        data_sensitivity = "internal" if actor == "employee" else "confidential"
        constraints = Constraints(data_sensitivity=data_sensitivity, max_steps=1)

        # Hit the native Risk Core!
        print(
            f"\n[Sentinel Client] Crossing boundary to sentinel-runtime native score_step()..."
        )
        decision = score_step(step, constraints, self.policy_config)

        print(
            f"[Sentinel Risk Result] Action: {decision.action} | Level: {decision.level} | Score: {decision.score} | Reason: {decision.reason}"
        )

        # Sentinel returns ALLOW, REVIEW, or BLOCK natively
        return decision.action
