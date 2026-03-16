import os
import yaml
from typing import Dict, Any, Tuple


class PolicyEngine:
    def __init__(self, policy_path: str = None):
        if not policy_path:
            policy_path = os.path.join(
                os.path.dirname(__file__), "..", "config", "policy.yaml"
            )

        self.policy_path = policy_path
        self.policy = self._load_policy()

    def _load_policy(self) -> Dict[str, Any]:
        """Loads and parses the YAML policy file."""
        if not os.path.exists(self.policy_path):
            print(
                f"[!] Warning: Policy file not found at {self.policy_path}. Using safe defaults."
            )
            return {}

        with open(self.policy_path, "r") as f:
            try:
                return yaml.safe_load(f)
            except yaml.YAMLError as e:
                print(f"[!] Error parsing policy YAML: {e}")
                return {}

    def evaluate_intent(
        self, action: str, context: Dict[str, Any]
    ) -> Tuple[str, str, int]:
        """
        Evaluates an agent intent against the policy.
        Returns: (Decision, Reason, RiskScore)
        Decision can be: ALLOW, REVIEW, BLOCK
        """
        # 1. Global Transaction Limit Check
        amount = context.get("transaction_amount", 0.0)
        max_amt = self.policy.get("global_limits", {}).get(
            "max_transaction_amount", 100000.0
        )

        if amount >= max_amt:
            return (
                "BLOCK",
                f"Transaction amount ${amount} exceeds global limit ${max_amt}",
                100,
            )

        # 2. Action Specific Rules
        action_rules = self.policy.get("actions", {}).get(action)
        if not action_rules:
            # If action is not in policy, we default to REVIEW for safety
            return (
                "REVIEW",
                f"Action '{action}' is not explicitly defined in policy.",
                50,
            )

        # 3. Account Type Restrictions
        restricted_types = action_rules.get("restricted_account_types", [])
        account_type = context.get("account_type", "Standard")

        if account_type in restricted_types:
            return (
                "BLOCK",
                f"Action '{action}' is restricted for account type '{account_type}'.",
                90,
            )

        # 4. Risk Scoring
        base_risk = action_rules.get("base_risk", 10)
        # Mocking some dynamic risk adjustment based on amount
        dynamic_risk = int(amount / 100) if amount > 0 else 0
        final_score = base_risk + dynamic_risk

        # 5. Threshold Decision
        thresholds = self.policy.get("risk_thresholds", {})
        allow_t = thresholds.get("allow", 30)
        review_t = thresholds.get("review", 60)

        if final_score < allow_t:
            return "ALLOW", "Action meets safety thresholds.", final_score
        elif final_score < review_t:
            return (
                "REVIEW",
                "Action requires human oversight (risk elevated).",
                final_score,
            )
        else:
            return "BLOCK", "Action blocked: high risk score detected.", final_score


# Singleton instance for the validator layer
_engine = None


def get_policy_engine():
    global _engine
    if _engine is None:
        _engine = PolicyEngine()
    return _engine
