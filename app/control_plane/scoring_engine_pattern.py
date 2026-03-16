from risk.policy_loader import POLICY
import json


def calculate_risk_score(transaction_data: dict, result_text: str) -> int:
    """A production-grade, additive risk scoring engine pattern."""
    risk_score = POLICY.get("global_limits", {}).get("default_risk_score", 10)

    # 1. Deterministic Hard Rules (Highest Priority Penalties)
    amount = float(transaction_data.get("amount", 0))
    if amount >= POLICY.get("global_limits", {}).get(
        "max_transaction_amount", 100000.0
    ):
        risk_score += 80  # Don't return, penalize heavily

    # 2. Account Risk Overrides (Additive)
    account_id = str(transaction_data.get("account_id", "")).lower()
    risk_score += POLICY.get("account_risk", {}).get(account_id, 0)

    # 3. Textual Keyword Deterministic Triggers
    if "suspicious" in result_text.lower():
        risk_score += 40

    # 4. AI Structured Signals (Lowest Priority)
    try:
        clean_text = (
            result_text.strip().removeprefix("```json").removesuffix("```").strip()
        )
        analysis = json.loads(clean_text)
        if analysis.get("risk_level", "low").lower() == "high":
            risk_score += POLICY.get("ai_signals_penalty", {}).get("severe risk", 40)
        if analysis.get("recommended_action", "approve").lower() in ["freeze", "deny"]:
            risk_score += POLICY.get("ai_signals_penalty", {}).get("freeze", 30)
    except json.JSONDecodeError:
        pass  # Optional: fallback logic here

    return max(100 - min(risk_score, 100), 0)
