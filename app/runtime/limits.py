from app.runtime.models import RuntimeState, RuntimeCheckResult

class RuntimeLimits:
    """
    Enforces hard execution boundaries for the platform.
    """
    
    def __init__(self, max_steps: int = 5, max_tool_calls: int = 3, max_seconds: float = 60.0):
        self.max_steps = max_steps
        self.max_tool_calls = max_tool_calls
        self.max_seconds = max_seconds

    def validate(self, state: RuntimeState) -> RuntimeCheckResult:
        """
        Checks if the current state is within execution limits.
        """
        if state.step_count >= self.max_steps:
            return RuntimeCheckResult(
                allowed=False,
                reason_code="STEP_LIMIT_EXCEEDED",
                message=f"Maximum execution steps ({self.max_steps}) reached."
            )
            
        if state.tool_calls >= self.max_tool_calls:
            return RuntimeCheckResult(
                allowed=False,
                reason_code="TOOL_CALL_LIMIT_EXCEEDED",
                message=f"Maximum tool calls ({self.max_tool_calls}) reached."
            )
            
        if state.elapsed_seconds >= self.max_seconds:
            return RuntimeCheckResult(
                allowed=False,
                reason_code="TIME_LIMIT_EXCEEDED",
                message=f"Maximum runtime duration ({self.max_seconds}s) exceeded."
            )
            
        return RuntimeCheckResult(allowed=True, reason_code="LIMIT_OK", message="Within limits.")
