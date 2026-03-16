from typing import Dict, Any, Optional

# Known trusted merchant categories for context scoring
TRUSTED_MERCHANT_PREFIXES = {"Office", "Grocery", "Pharmacy", "Gas", "Coffee", "Restaurant"}

class RiskEngine:
    """
    Deterministic risk scoring engine for financial transactions.
    Scores are based on payload signals, risk metadata, and context completeness.
    """
    
    def __init__(self, default_risk: float = 10.0):
        self.default_risk = default_risk

    def calculate_score(
        self,
        business_payload: Dict[str, Any],
        risk_metadata: Dict[str, Any],
        customer_context: Optional[Dict[str, Any]] = None
    ) -> float:
        """
        Calculates a risk score (0-100) based on payload, metadata, and context signals.
        Higher score = higher risk.
        """
        score = risk_metadata.get("last_fraud_score", self.default_risk)
        
        # 1. Transaction Amount logic
        amount = business_payload.get("amount", 0.0)
        if amount > 10000.0:
            score += 50.0  # High value penalty
        elif amount > 1000.0:
            score += 20.0  # Moderate value penalty
            
        # 2. Velocity / Metadata signals
        if risk_metadata.get("velocity_flags", 0) > 2:
            score += 30.0
            
        # 3. New Account logic
        if business_payload.get("account_age_days", 365) < 30:
            score += 15.0

        # 4. Missing context penalty — empty context = unknown risk
        context = customer_context or {}
        if not context or not context.get("customer_id"):
            score += 25.0  # Cannot automate without known customer context

        # 5. Unknown merchant penalty — unknown merchants are treated conservatively
        merchant = business_payload.get("merchant", "")
        is_trusted = any(merchant.startswith(prefix) for prefix in TRUSTED_MERCHANT_PREFIXES)
        if not is_trusted and merchant:
            score += 15.0

        # Cap at 100
        return min(max(score, 0.0), 100.0)
