import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from runner.orchestrator import AgentOrchestrator
from tools.mock_db import DB


class TestValidationOrchestrator:

    def setup_method(self):
        self.orchestrator = AgentOrchestrator()

    def test_schema_validator_fails_missing_actor(self):
        context = {
            "action_to_take": "freeze_account",
            "account_id": "acc_123",
            # Missing actor
        }

        result = self.orchestrator.process_request("fraud_triage", context)
        assert result["status"] == "FAILED"
        assert result["error_type"] == "schema_error"

    def test_financial_rules_blocks_large_transaction(self):
        context = {
            "action_to_take": "approve_high_risk",
            "actor": "employee",
            "account_id": "acc_123",
            "transaction_amount": 150000.0,  # > $100k
        }

        result = self.orchestrator.process_request("fraud_triage", context)
        assert result["status"] == "FAILED"
        assert result["error_type"] == "financial_rule_violation"

    def test_financial_rules_blocks_centurion_freeze(self):
        context = {
            "action_to_take": "freeze_account",
            "actor": "employee",
            "account_id": "acc_VIP",  # Centurion card
            "transaction_amount": 500.0,
        }

        result = self.orchestrator.process_request("fraud_triage", context)
        assert result["status"] == "FAILED"
        assert result["error_type"] == "financial_rule_violation"

    def test_compliance_validator_blocks_customer_freeze(self):
        context = {
            "action_to_take": "freeze_account",
            "actor": "customer",  # Customer actor attempting to freeze
            "account_id": "acc_123",
            "transaction_amount": 0.0,
        }

        result = self.orchestrator.process_request("fraud_triage", context)
        assert result["status"] == "FAILED"
        assert result["error_type"] == "compliance_violation"

    def test_end_to_end_successful_orchestration(self):
        # Valid input that should pass validation and hit the workflow
        context = {
            "action_to_take": "freeze_account",
            "actor": "employee",
            "account_id": "acc_123",  # Active basic account
            "transaction_amount": 0.0,
        }
        result = self.orchestrator.process_request("fraud_triage", context)

        # It should jump straight to the COMPLETED workflow state, since it passed validation
        assert result["status"] == "completed"
        assert result["decision"] == "ALLOW"
