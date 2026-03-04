import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from workflows.fraud_triage import FraudTriageWorkflow
from workflows.base_workflow import WorkflowState
from tools.mock_db import DB, get_account

# We will test against the mock database defined in tools/mock_db.py
# "acc_123" starts as "ACTIVE"
# "acc_999" starts as "FROZEN"


def test_fraud_triage_employee_freeze_account_success_mutates_db():
    # Setup context pointing to the active account
    context = {
        "actor": "employee",
        "action_to_take": "freeze_account",
        "account_id": "acc_123",
    }

    # Verify initial DB state
    assert get_account("acc_123")["status"] == "ACTIVE"

    wf = FraudTriageWorkflow(context)
    result = wf.run()

    # Assert workflow completed successfully
    assert result["status"] == WorkflowState.COMPLETED.value
    assert result["decision"] == "ALLOW"
    assert "RISK_EVALUATED -> EXECUTED" in result["audit_trail"]

    # Assert execution metadata captured the concrete tool return
    execution_result = result["execution_metadata"]["execution_result"]
    assert execution_result["success"] is True
    assert "successfully frozen" in execution_result["message"]

    # MOST IMPORTANTLY: Assert the Mock Database actually mutated!
    assert get_account("acc_123")["status"] == "FROZEN"


def test_fraud_triage_high_risk_employee_review_creates_ticket():
    # Setup context pointing to a high risk approval attempt
    context = {
        "actor": "employee",
        "action_to_take": "approve_high_risk",
        "transaction_amount": 15000,
        "account_id": "acc_123",
    }

    # Track initial ticket length
    initial_ticket_count = len(DB["escalation_tickets"])

    wf = FraudTriageWorkflow(context)
    result = wf.run()

    # Assert workflow routed to Escalation due to Sentinel
    assert result["status"] == WorkflowState.COMPLETED.value
    assert result["decision"] == "BLOCK"
    assert "RISK_EVALUATED -> ESCALATED" in result["audit_trail"]

    # Assert the ticket was created in execution metadata
    ticket = result["execution_metadata"]["escalation_ticket"]
    assert ticket["success"] is True
    assert ticket["ticket_id"].startswith("TKT-")

    # MOST IMPORTANTLY: Assert the Mock Database actually mutated to add the ticket
    assert len(DB["escalation_tickets"]) == initial_ticket_count + 1
    assert DB["escalation_tickets"][-1]["ticket_id"] == ticket["ticket_id"]
    assert DB["escalation_tickets"][-1]["reason"] == "Action Block by Sentinel Runtime"


def test_fraud_triage_corporate_account_freeze_success():
    # Setup context pointing to an active Corporate account
    context = {
        "actor": "employee",
        "action_to_take": "freeze_account",
        "account_id": "acc_456",
    }

    assert get_account("acc_456")["status"] == "ACTIVE"
    assert get_account("acc_456")["type"] == "Corporate"

    wf = FraudTriageWorkflow(context)
    result = wf.run()

    assert result["status"] == WorkflowState.COMPLETED.value
    assert result["decision"] == "ALLOW"

    execution_result = result["execution_metadata"]["execution_result"]
    assert execution_result["success"] is True

    # Verify corporate account was properly frozen
    assert get_account("acc_456")["status"] == "FROZEN"


def test_fraud_triage_vip_account_block_escalation():
    # Setup context pointing to an active VIP Centurion account for an unsafe action
    context = {
        "actor": "employee",
        "action_to_take": "approve_high_risk",
        "transaction_amount": 50000,
        "account_id": "acc_VIP",
    }

    assert get_account("acc_VIP")["status"] == "ACTIVE"
    assert get_account("acc_VIP")["type"] == "Centurion"

    initial_ticket_count = len(DB["escalation_tickets"])

    wf = FraudTriageWorkflow(context)
    result = wf.run()

    assert result["status"] == WorkflowState.COMPLETED.value
    assert result["decision"] == "BLOCK"

    ticket = result["execution_metadata"]["escalation_ticket"]
    assert ticket["success"] is True

    # Assert ticket was successfully created for the VIP account
    assert len(DB["escalation_tickets"]) == initial_ticket_count + 1
    assert DB["escalation_tickets"][-1]["ticket_id"] == ticket["ticket_id"]
