# tools/escalation_tools.py
from tools.mock_db import add_escalation_ticket


def create_review_ticket(reason: str, context: dict) -> dict:
    """
    Concrete tool execution function.
    Interacts with the simulated ServiceNow / JIRA system to route for manual review.
    """
    ticket_payload = {
        "status": "OPEN",
        "reason": reason,
        "workflow_id": context.get("workflow_id", "unknown"),
        "actor": context.get("actor", "system"),
        "related_account": context.get("account_id", "unknown"),
        "transaction_amount": context.get("transaction_amount", None),
    }

    ticket_id = add_escalation_ticket(ticket_payload)

    return {
        "success": True,
        "ticket_id": ticket_id,
        "message": f"Escalation ticket {ticket_id} created successfully.",
    }
