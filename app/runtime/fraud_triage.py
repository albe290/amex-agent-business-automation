from workflows.base_workflow import BaseWorkflow, WorkflowState
from runner.sentinel_client import SentinelClient
from rag.retriever import PolicyRetriever
import time


from tools.fraud_tools import freeze_account
from tools.escalation_tools import create_review_ticket


class FraudTriageWorkflow(BaseWorkflow):
    def __init__(self, context):
        super().__init__(context)
        self.sentinel = SentinelClient()
        self.retriever = PolicyRetriever()

    def run(self):
        # Deterministic sequence: INIT -> INTENT_VALIDATED
        self.transition(WorkflowState.INTENT_VALIDATED)

        # Simulate LLM extracting intent
        self.context["intent"] = "fraud_report"

        # Deterministic sequence: Context retrieval via RAG
        self.transition(WorkflowState.CONTEXT_RETRIEVED)

        # Build a search query from the context to find relevant rules
        actor = self.context.get("actor", "unknown")
        amount = self.context.get("transaction_amount", "unknown")
        search_query = f"Rules regarding fraud and account freezing for {actor} transactions of amount {amount}"

        retrieved_policies = self.retriever.search(search_query, top_k=1)
        self.context["retrieved_policy"] = "\n".join(retrieved_policies)

        # Validation
        self.transition(WorkflowState.VALIDATED)

        # Risk Evaluation via Sentinel pipeline (Pre-checked by Orchestrator Gateway)
        action = self.context.get("action_to_take", "freeze_account")
        decision = self.context.get("sentinel_decision", "BLOCK")
        self.transition(WorkflowState.RISK_EVALUATED)
        self.context["sentinel_decision"] = decision
        self.context["final_action"] = action

        if decision == "ALLOW":
            self.execute()
            self.transition(WorkflowState.EXECUTED)
        elif decision == "REVIEW":
            self.escalate("Approval Required for action")
            self.transition(WorkflowState.ESCALATED)
        else:
            self.escalate(f"Action {decision.capitalize()} by Sentinel Runtime")
            self.transition(WorkflowState.ESCALATED)

        self.transition(WorkflowState.COMPLETED)

        return {
            "workflow_id": self.id,
            "status": self.state.value,
            "decision": decision,
            "audit_trail": self.get_audit_trail(),
            "execution_metadata": {
                "execution_result": self.context.get("execution_result"),
                "escalation_ticket": self.context.get("escalation_ticket"),
            },
        }

    def execute(self):
        action = self.context.get("final_action")
        account_id = self.context.get("account_id", "unknown")

        if action == "freeze_account":
            print(
                f"[Execution] Triggering concrete tool: freeze_account on {account_id}"
            )
            result = freeze_account(account_id)
            self.context["execution_result"] = result
        else:
            print(f"[Execution] No concrete tool mapped for {action}.")

    def escalate(self, reason):
        print(
            f"[Escalation] Triggering concrete tool: create_review_ticket due to {reason}"
        )
        ticket = create_review_ticket(reason, self.context)
        self.context["escalation_ticket"] = ticket
