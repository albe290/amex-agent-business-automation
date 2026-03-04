from typing import Any, Dict
from pydantic import BaseModel, Field, ValidationError


class ActionRequestSchema(BaseModel):
    """Schema for incoming LLM action requests."""

    action_to_take: str = Field(..., description="The intended tool action.")
    actor: str = Field(
        ..., description="The initiator, e.g., 'employee' or 'customer'."
    )
    account_id: str = Field(..., description="The unique account identifier.")
    transaction_amount: float = Field(
        default=0.0, description="The monetary amount involved, if any."
    )


def validate_agent_action_request(context: Dict[str, Any]) -> tuple[bool, str]:
    """
    Validates that the execution context produced by the LLM reasoning engine
    matches the expected schema needed by the runtime.
    """
    try:
        validated_data = ActionRequestSchema(**context)
        return True, "Valid"
    except ValidationError as e:
        return False, f"Schema Validation Failed: {str(e)}"
