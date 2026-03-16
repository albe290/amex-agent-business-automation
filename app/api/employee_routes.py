from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from runner.orchestrator import AgentOrchestrator
from monitoring.metrics import metrics

router = APIRouter()
orchestrator = AgentOrchestrator()


class AgentRequest(BaseModel):
    account_id: str
    action_to_take: str
    transaction_amount: float = 0.0


@router.post("/triage")
async def employee_fraud_triage(request: AgentRequest):
    """
    Endpoint for internal L1 reviewers to securely route cases to the Agent.
    """
    metrics.increment("api_requests_total")

    context = {
        "actor": "employee",
        "account_id": request.account_id,
        "action_to_take": request.action_to_take,
        "transaction_amount": request.transaction_amount,
    }

    result = orchestrator.process_request("fraud_triage", context)

    if result.get("status") == "FAILED":
        raise HTTPException(status_code=400, detail=result.get("message"))

    decision = result.get("decision", "unknown")
    if decision == "ALLOW":
        metrics.increment("agent_decisions_allow")
    elif decision == "BLOCK":
        metrics.increment("agent_decisions_block")
    elif decision == "REVIEW":
        metrics.increment("agent_decisions_review")
        metrics.increment("fraud_escalations")

    return result
