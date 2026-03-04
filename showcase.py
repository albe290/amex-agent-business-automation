import time
import json
from runner.orchestrator import AgentOrchestrator
from tools.mock_db import DB, get_account

YELLOW = "\033[93m"
GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
RESET = "\033[0m"


def print_header(title):
    print(
        f"\n{CYAN}========================================================================={RESET}"
    )
    print(f"{CYAN}   {title}   {RESET}")
    print(
        f"{CYAN}========================================================================={RESET}"
    )


def run_showcase():
    orchestrator = AgentOrchestrator()
    print_header("SECURE FINANCIAL AI AGENT - GUARDRails SHOWCASE")

    print(f"{YELLOW}[System] Starting up Financial AI Agent Orchestrator...{RESET}")
    time.sleep(1)

    # ---------------------------------------------------------
    # Scenario 1: Successful Fraud Triage (ALLOW)
    # ---------------------------------------------------------
    print_header("Scenario 1: Authorized Account Freeze (Standard Corporate)")
    print(
        f"Context: An employee suspects fraud on the Acme Corp account and requests a freeze."
    )

    context_1 = {
        "actor": "employee",
        "action_to_take": "freeze_account",
        "account_id": "acc_456",
        "transaction_amount": 0.0,
    }

    print(f"\nIncoming Agent Intent:\n{json.dumps(context_1, indent=2)}")
    print(f"\n{YELLOW}[Validator] Running Pre-Execution Checks...{RESET}")
    time.sleep(0.5)

    result_1 = orchestrator.process_request("fraud_triage", context_1)

    if result_1["status"] == "COMPLETED" and result_1["decision"] == "ALLOW":
        print(
            f"{GREEN}[PASS] Sentinel Risk Engine: Decision = ALLOW (Action is safe based on policy/schema).{RESET}"
        )
        print(
            f"{GREEN}[PASS] Concrete Execution: Account acc_456 successfully mutated to FROZEN.{RESET}"
        )
        print(f"Final Account Status in DB: {get_account('acc_456')['status']}")

    time.sleep(1.5)

    # ---------------------------------------------------------
    # Scenario 2: High-Risk Action Blocked by Compliance (FAILED)
    # ---------------------------------------------------------
    print_header("Scenario 2: Unauthorized Freeze Attempt (Centurion VIP)")
    print(
        f"Context: Employee attempts to freeze a highly sensitive Centurion (Black Card) account."
    )

    context_2 = {
        "actor": "employee",
        "action_to_take": "freeze_account",
        "account_id": "acc_VIP",
        "transaction_amount": 0.0,
    }

    print(f"\nIncoming Agent Intent:\n{json.dumps(context_2, indent=2)}")
    print(f"\n{YELLOW}[Validator] Running Pre-Execution Checks...{RESET}")
    time.sleep(0.5)

    result_2 = orchestrator.process_request("fraud_triage", context_2)

    print(f"{RED}[X] Financial Validator Override Triggered!{RESET}")
    print(f"{RED}Error Type: {result_2['error_type']}{RESET}")
    print(f"{RED}Detail: {result_2['message']}{RESET}")
    print(f"Final Account Status in DB: {get_account('acc_VIP')['status']} (Unchanged)")

    time.sleep(1.5)

    # ---------------------------------------------------------
    # Scenario 3: Sentinel Risk Engine Soft Block (REVIEW)
    # ---------------------------------------------------------
    print_header("Scenario 3: High Value Transaction Approval Escapation")
    print(
        f"Context: Employee attempts to authorize a $15,000 transaction on a standard account."
    )

    context_3 = {
        "actor": "employee",
        "action_to_take": "approve_high_risk",
        "account_id": "acc_123",
        "transaction_amount": 15000.0,
    }

    print(f"\nIncoming Agent Intent:\n{json.dumps(context_3, indent=2)}")
    print(f"\n{YELLOW}[Validator] Running Pre-Execution Checks (Passed){RESET}")
    print(f"{YELLOW}[Sentinel Risk Engine] Evaluating complex runtime risk...{RESET}")
    time.sleep(0.5)

    result_3 = orchestrator.process_request("fraud_triage", context_3)

    if result_3["status"] == "COMPLETED" and result_3["decision"] == "BLOCK":
        print(
            f"{YELLOW}[WARN] Sentinel Risk Engine: Decision = REVIEW/BLOCK (Threshold Exceeded).{RESET}"
        )
        print(
            f"{YELLOW}[WARN] Execution halted. Creating Zendesk Escalation Ticket...{RESET}"
        )
        ticket = result_3["execution_metadata"]["escalation_ticket"]
        print(f"Ticket ID: {ticket['ticket_id']} created for Human Analyst.")


if __name__ == "__main__":
    run_showcase()
