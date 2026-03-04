from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from runner.orchestrator import AgentOrchestrator
from monitoring.metrics import metrics

router = APIRouter()
orchestrator = AgentOrchestrator()


class CustomerActionRequest(BaseModel):
    account_id: str
    action_to_take: str
    transaction_amount: float = 0.0


@router.post("/self-service")
async def customer_self_service(request: CustomerActionRequest):
    """
    Endpoint for the customer-facing mobile app chatbot to route intents to the Agent.
    """
    metrics.increment("api_requests_total")

    context = {
        "actor": "customer",
        "account_id": request.account_id,
        "action_to_take": request.action_to_take,
        "transaction_amount": request.transaction_amount,
    }

    # Send through exactly the same orchestrator, but the validation layer
    # will heavily constrain what the "customer" actor is allowed to do.
    result = orchestrator.process_request("fraud_triage", context)

    if result.get("status") == "FAILED":
        raise HTTPException(
            status_code=403,
            detail=f"Customer request blocked by Compliance Validator: {result.get('message')}",
        )

    decision = result.get("decision", "unknown")
    if decision == "ALLOW":
        metrics.increment("agent_decisions_allow")
    elif decision in ["BLOCK", "REVIEW"]:
        # Customers don't get detailed security error traces, we mask them here.
        return {
            "success": False,
            "message": "We could not process this request automatically. Please call support.",
        }

    return result
