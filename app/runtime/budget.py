from app.runtime.models import RuntimeState, RuntimeCheckResult

class RuntimeBudget:
    """
    Monitors and enforces resource consumption budgets.
    """
    
    def __init__(self, max_model_calls: int = 3, max_usd: float = 0.50):
        self.max_model_calls = max_model_calls
        self.max_usd = max_usd

    def validate(self, state: RuntimeState) -> RuntimeCheckResult:
        """
        Checks if the execution is within cost and call budgets.
        """
        if state.model_calls >= self.max_model_calls:
            return RuntimeCheckResult(
                allowed=False,
                reason_code="MODEL_CALL_BUDGET_EXCEEDED",
                message=f"Maximum model calls ({self.max_model_calls}) reached."
            )
            
        if state.budget_used_usd >= self.max_usd:
            return RuntimeCheckResult(
                allowed=False,
                reason_code="COST_BUDGET_EXCEEDED",
                message=f"Estimated cost budget (${self.max_usd}) exceeded."
            )
            
        return RuntimeCheckResult(allowed=True, reason_code="BUDGET_OK", message="Within budget.")
