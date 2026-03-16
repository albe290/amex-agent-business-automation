import time
from typing import Dict, Any, List
from app.runtime.models import RuntimeState, RuntimeCheckResult
from app.runtime.limits import RuntimeLimits
from app.runtime.budget import RuntimeBudget
from app.runtime.guardrails import RuntimeGuardrails
from app.runtime.retries import RetryPolicy
from app.runtime.fallback import RuntimeFallback, FallbackResult
from app.control_plane.decision import ControlPlaneDecision

class RuntimeCoordinator:
    """
    The 'Execution Referee'. Orchestrates governance checks during workflow execution.
    """
    
    def __init__(self):
        self.limits = RuntimeLimits()
        self.budget = RuntimeBudget()
        self.guardrails = RuntimeGuardrails()
        self.retries = RetryPolicy()
        self.fallback_handler = RuntimeFallback()

    def initialize_state(self, request_id: str, strategy: str) -> RuntimeState:
        return RuntimeState(request_id=request_id, strategy_path=strategy)

    def pre_step_check(self, state: RuntimeState) -> RuntimeCheckResult:
        """
        Checks limits and budget before executing the next step.
        """
        # 1. Update elapsed time
        state.elapsed_seconds = (RuntimeState.model_validate(state).start_time.utcnow() - state.start_time).total_seconds()
        
        # 2. Check Limits
        limit_check = self.limits.validate(state)
        if not limit_check.allowed:
            return limit_check
            
        # 3. Check Budget
        budget_check = self.budget.validate(state)
        if not budget_check.allowed:
            return budget_check
            
        return RuntimeCheckResult(allowed=True, reason_code="PRE_STEP_OK", message="Safe to proceed.")

    def validate_action(self, action_name: str, decision: ControlPlaneDecision) -> RuntimeCheckResult:
        """
        Applies guardrails to specific action requests.
        """
        return self.guardrails.validate_action(action_name, decision)

    def handle_violation(self, check_result: RuntimeCheckResult) -> FallbackResult:
        """
        Invokes the fallback strategy when a check fails.
        """
        return self.fallback_handler.generate_fallback(check_result.reason_code, check_result.message)
