from risk.policy_loader import POLICY
import json


def calculate_risk_score(transaction_data: dict, result_text: str) -> int:
    account_id = str(transaction_data.get("account_id", "")).lower()
    amount = float(transaction_data.get("amount", 0))
    result_text = result_text.lower()

    # Load defaults and limits
    global_limits = POLICY.get("global_limits", {})
    risk_score = global_limits.get("default_risk_score", 10)

    # 1. Global transaction limit
    if amount >= global_limits.get("max_transaction_amount", 100000.0):
        risk_score += 80

    # 2. Account risk rules
    account_risk = POLICY.get("account_risk", {})
    if account_id in account_risk:
        risk_score += account_risk[account_id]

    # 2.5 Deterministic keyword rules
    if "suspicious" in result_text:
        risk_score += 40

    # 3. AI Structured Signals (Lowest priority additive penalties)
    # Parse the strictly formatted JSON output
    try:
        # Strip potential markdown output (e.g. ```json ... ```)
        clean_text = result_text.strip()
        if clean_text.startswith("```json"):
            clean_text = clean_text[7:]
        elif clean_text.startswith("```"):
            clean_text = clean_text[3:]
        if clean_text.endswith("```"):
            clean_text = clean_text[:-3]

        analysis = json.loads(clean_text)
        risk_level = analysis.get("risk_level", "low").lower()
        action = analysis.get("recommended_action", "approve").lower()

        # Apply AI Risk Policy Additions
        ai_signals = POLICY.get("ai_signals_penalty", {})

        if risk_level == "high":
            risk_score += ai_signals.get("severe risk", 40)

        if action in ["freeze", "deny"]:
            risk_score += ai_signals.get("freeze", 30)

    except json.JSONDecodeError:
        print(
            "[!] Risk Engine Warning: AI failed to return valid JSON. Falling back to textual parsing."
        )
        # Graceful fallback: legacy textual parsing
        ai_signals = POLICY.get("ai_signals_penalty", {})
        for signal, penalty in ai_signals.items():
            if signal in result_text.lower():
                risk_score += penalty

    # Cap risk score at 100
    risk_score = min(risk_score, 100)

    # 4. Convert Risk Score back to frontend Compliance Score (higher = better)
    compliance_score = max(100 - risk_score, 0)

    return compliance_score
