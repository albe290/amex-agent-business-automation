import pytest
import sys
import os

# Add the project root to the python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from workflows.fraud_triage import FraudTriageWorkflow
from workflows.base_workflow import WorkflowState


def test_fraud_triage_customer_freeze_account_denied():
    context = {"actor": "customer", "action_to_take": "freeze_account"}
    wf = FraudTriageWorkflow(context)
    result = wf.run()

    assert result["status"] == WorkflowState.COMPLETED.value
    assert result["decision"] == "ALLOW"

    # Assert deterministic sequence
    audit_trail = result["audit_trail"]
    assert "INIT -> INTENT_VALIDATED" in audit_trail
    assert "RISK_EVALUATED -> EXECUTED" in audit_trail
    assert "EXECUTED -> COMPLETED" in audit_trail
    assert not any("ESCALATED" in step for step in audit_trail)


def test_fraud_triage_employee_freeze_account_allowed():
    context = {"actor": "employee", "action_to_take": "freeze_account"}
    wf = FraudTriageWorkflow(context)
    result = wf.run()

    assert result["status"] == WorkflowState.COMPLETED.value
    assert result["decision"] == "ALLOW"

    # Assert deterministic sequence
    audit_trail = result["audit_trail"]
    assert "RISK_EVALUATED -> EXECUTED" in audit_trail
    assert "EXECUTED -> COMPLETED" in audit_trail
    assert not any("ESCALATED" in step for step in audit_trail)


def test_fraud_triage_high_risk_employee_review():
    context = {
        "actor": "employee",
        "action_to_take": "approve_high_risk",
        "transaction_amount": 15000,
    }
    wf = FraudTriageWorkflow(context)
    result = wf.run()

    assert result["status"] == WorkflowState.COMPLETED.value
    assert result["decision"] == "BLOCK"

    # Assert deterministic sequence
    audit_trail = result["audit_trail"]
    assert "RISK_EVALUATED -> ESCALATED" in audit_trail
    assert "ESCALATED -> COMPLETED" in audit_trail


def test_audit_log_format():
    context = {"actor": "employee", "action_to_take": "freeze_account"}
    wf = FraudTriageWorkflow(context)
    wf.run()

    assert len(wf.audit_log) > 0
    first_entry = wf.audit_log[0]
    assert "workflow_id" in first_entry
    assert "timestamp" in first_entry
    assert "from_state" in first_entry
    assert "to_state" in first_entry
    assert first_entry["actor"] == "employee"
