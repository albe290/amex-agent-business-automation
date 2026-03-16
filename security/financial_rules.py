from validators.policy_engine import get_policy_engine
from tools.mock_db import get_account


def check_financial_rules(action: str, context: dict) -> tuple[bool, str]:
    """
    Applies deterministic business rules before sentinel evaluation.
    This acts as a fast-fail mechanism using the centralized policy.yaml.
    """
    # 1. Enrich context for policy engine
    account_id = context.get("account_id")
    account_info = get_account(account_id)
    if account_info:
        context["account_type"] = account_info.get("type", "Standard")

    # 2. Evaluate via Policy Engine
    engine = get_policy_engine()
    decision, reason, score = engine.evaluate_intent(action, context)

    # 3. Store result for downstream (sentinel compatibility)
    context["last_policy_decision"] = decision
    context["last_policy_reason"] = reason
    context["last_policy_score"] = score

    if decision == "BLOCK":
        return False, f"Policy Violation: {reason}"

    return True, f"Policy Check: {decision} ({reason})"
