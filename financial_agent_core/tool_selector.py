from typing import List, Dict

AVAILABLE_TOOLS = {
    "fraud": ["freeze_account", "unlock_account", "create_escalation_ticket"],
    "credit": ["approve_credit_limit", "run_credit_check", "deny_credit"],
    "transactions": ["process_refund", "validate_merchant", "reverse_transaction"],
}


def get_available_tools(agent_type: str) -> List[str]:
    """
    Returns the strict subset of tools available to a specific agent type.
    """
    if agent_type == "customer":
        # Customers have a highly restricted subset of tools
        return ["run_credit_check", "process_refund"]

    elif agent_type == "employee":
        # Employees get everything, but their actions are still
        # heavily constrained by the Sentinel risk engine during execution.
        all_tools = []
        for tools in AVAILABLE_TOOLS.values():
            all_tools.extend(tools)
        return all_tools

    return []


def format_tool_descriptions(tool_names: List[str]) -> str:
    """Returns a formatted string of tools for the LLM system prompt."""
    descriptions = {
        "freeze_account": "Freezes an account immediately. Use in cases of high fraud intent.",
        "unlock_account": "Unfreezes an account.",
        "create_escalation_ticket": "Routes the issue to a human reviewer.",
        "process_refund": "Refunds a specific transaction.",
        "validate_merchant": "Checks if a merchant ID is known for fraud.",
        "run_credit_check": "Returns the FICO score of the account.",
        "approve_credit_limit": "Approves a requested credit limit increase.",
        "deny_credit": "Denies a credit limit increase.",
    }

    formatted = []
    for tool in tool_names:
        desc = descriptions.get(tool, "No description available.")
        formatted.append(f"- {tool}: {desc}")

    return "\n".join(formatted)
