from tools.fraud_tools import freeze_account, unlock_account
from tools.escalation_tools import create_review_ticket
from tools.audit_logger import log_action


class DecisionHandler:
    """
    Parses the verdicts from Sentinel and the Validation layer
    to trigger actual concrete tool executions or human escalations.
    """

    def __init__(self, workflow_id: str, context: dict):
        self.workflow_id = workflow_id
        self.context = context

    def handle_allow(self, action: str):
        """Execute the intended action directly since it was deemed safe."""
        account_id = self.context.get("account_id")
        result = {"success": False, "message": "Unknown action or failure."}

        try:
            if action == "freeze_account":
                result = freeze_account(account_id)
            elif action == "unlock_account":
                result = unlock_account(account_id)
            else:
                result = {
                    "success": False,
                    "message": f"Tool {action} not mapped for execution.",
                }
        except Exception as e:
            result = {"success": False, "message": f"Execution Error: {str(e)}"}

        # Write to secure audit log
        log_action(
            self.workflow_id,
            self.context.get("actor", "unknown"),
            action,
            "ALLOW",
            self.context,
        )
        return result

    def handle_block(self, action: str, reason: str):
        """Firmly block the action. Do not allow execution."""
        log_action(
            self.workflow_id,
            self.context.get("actor", "unknown"),
            action,
            "BLOCK",
            self.context,
        )

        return {
            "success": False,
            "message": f"Hard Block on action '{action}'. Reason: {reason}",
        }

    def handle_review(self, action: str):
        """Escalate to a human reviewer."""
        log_action(
            self.workflow_id,
            self.context.get("actor", "unknown"),
            action,
            "REVIEW",
            self.context,
        )
        reason = f"Automated escalation for high-risk action: {action}"

        ticket = create_review_ticket(reason, self.context)
        return {
            "success": True,
            "escalation_ticket": ticket,
            "message": "Routed for human review.",
        }
