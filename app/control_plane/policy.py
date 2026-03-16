from typing import List, Tuple

class PolicyEngine:
    """
    Business boundary engine that maps risk scores to decisions.
    Migrated from legacy security/policy_engine.py.
    """
    
    def __init__(self, allow_threshold: float = 40.0, review_threshold: float = 75.0):
        self.allow_threshold = allow_threshold
        self.review_threshold = review_threshold

    def evaluate(self, risk_score: float, flags: List[str]) -> Tuple[bool, List[str], List[str]]:
        """
        Determines the governance outcome.
        Returns: (requires_review, policy_hits, allowed_actions)
        """
        policy_hits = []
        allowed_actions = []
        requires_review = False

        # 1. Hard flag logic (Priority)
        if "HIGH_VALUE_TRANSACTION" in flags:
            policy_hits.append("HIGH_VALUE_TRANSACTION")
            if risk_score > 50:
                requires_review = True

        # 2. Score-based thresholds
        if risk_score >= self.review_threshold:
            requires_review = True
            policy_hits.append("RISK_SCORE_CRITICAL")
            allowed_actions = ["ESCALATE_TO_HUMAN", "BLOCK_TRANSACTION"]
        elif risk_score >= self.allow_threshold:
            requires_review = True
            policy_hits.append("RISK_SCORE_ELEVATED")
            allowed_actions = ["PROCEED_WITH_HUMAN_REVIEW", "INVESTIGATE_VIA_AI"]
        else:
            policy_hits.append("RISK_SCORE_NOMINAL")
            allowed_actions = ["AUTOMATE_APPROVAL", "LOG_AS_SAFE"]

        return requires_review, policy_hits, allowed_actions
