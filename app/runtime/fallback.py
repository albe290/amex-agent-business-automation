from pydantic import BaseModel
from typing import Optional, Dict, Any

class FallbackResult(BaseModel):
    """
    Structured outcome of a runtime failure or block.
    """
    fallback_type: str  # e.g., 'ESCALATE_TO_REVIEW', 'RETURN_PARTIAL_RESULT'
    reason: str
    safe_output: Optional[Dict[str, Any]] = None
    requires_review: bool = True

class RuntimeFallback:
    """
    Logic for safely exiting failed or blocked executions.
    """
    
    def generate_fallback(self, reason_code: str, message: str) -> FallbackResult:
        """
        Maps a violation code to a safe platform output.
        """
        if "LIMIT" in reason_code or "BUDGET" in reason_code:
            return FallbackResult(
                fallback_type="ESCALATE_TO_REVIEW",
                reason=f"Execution halted: {message}",
                safe_output={"status": "INCOMPLETE", "note": "Resource limits reached"}
            )
            
        if "GUARDRAIL" in reason_code:
            return FallbackResult(
                fallback_type="ESCALATE_TO_REVIEW",
                reason=f"Action blocked by guardrail: {message}",
                safe_output={"status": "BLOCKED", "note": "Policy restriction enforced"}
            )
            
        return FallbackResult(
            fallback_type="TERMINATE_UNSAFE",
            reason=f"Safety termination: {message}",
            requires_review=True
        )
