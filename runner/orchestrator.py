import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from workflows.fraud_triage import FraudTriageWorkflow
from workflows.credit_underwriting import CreditUnderwritingWorkflow
from validators.schema_validator import validate_agent_action_request
from validators.financial_rules import check_financial_rules
from validators.compliance_validator import check_compliance_constraints
from rag.retriever import PolicyRetriever
from financial_agent_core.planner import DecisionPlanner, format_plan_for_prompt


class AgentOrchestrator:
    """
    The main entry point for requests to the Automation runtime.
    Routes requests to workflows and applies pre-execution validators.
    """

    def __init__(self):
        self.retriever = PolicyRetriever()
        self.planner = DecisionPlanner()
        self.workflows = {
            "fraud_triage": FraudTriageWorkflow,
            "credit_underwriting": CreditUnderwritingWorkflow,
        }

    def process_request(self, workflow_name: str, context: dict) -> dict:
        """
        Main routing method.
        Phase 1: Validation & Safety
        Phase 4: Policy Intelligence (RAG)
        """
        print(f"[Orchestrator] Processing request for workflow: {workflow_name}")

        # --- STEP 0: RAG Policy Retrieval ---
        query = (
            f"{context.get('action_to_take')} for account {context.get('account_id')}"
        )
        policies = self.retriever.search(query)
        context["policy_context"] = policies
        print(f"[Orchestrator] Policy Intelligence Retrieved ({len(policies)} chunks)")

        # --- STEP 0.5: Advanced Reasoning (Planning) ---
        plan = self.planner.generate_plan(workflow_name, policies, context)
        context["execution_plan"] = plan
        print(format_plan_for_prompt(plan))

        # 1. Schema Validation (Did the LLM format the request correctly?)
        is_valid_schema, schema_msg = validate_agent_action_request(context)
        if not is_valid_schema:
            return self._fail("schema_error", schema_msg)

        action = context.get("action_to_take")

        # 2. Financial Rules Validation (Deterministic checks)
        is_valid_financials, fin_msg = check_financial_rules(action, context)
        if not is_valid_financials:
            return self._fail("financial_rule_violation", fin_msg)

        # 3. Compliance Constraints (Hard compliance overrides)
        is_compliant, comp_msg = check_compliance_constraints(action, context)
        if not is_compliant:
            return self._fail("compliance_violation", comp_msg)

        # 4. Route to Stateful Workflow
        workflow_class = self.workflows.get(workflow_name)
        if not workflow_class:
            return self._fail("routing_error", f"Unknown workflow: {workflow_name}")

        workflow = workflow_class(context)
        result = workflow.run()

        return result

    def _fail(self, error_type: str, message: str) -> dict:
        print(f"[Orchestrator] Request failed at validation layer: {message}")
        return {
            "status": "FAILED",
            "error_type": error_type,
            "message": message,
            "execution_metadata": {},
        }
