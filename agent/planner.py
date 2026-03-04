from agent.reasoning_engine import ReasoningEngine
from agent.intent_schema import IntentClassification
from workflows.fraud_triage import FraudTriageWorkflow

# Deterministic Mapping Array
WORKFLOW_MAP = {
    "fraud_triage": FraudTriageWorkflow,
    # "anomaly_detection": AnomalyDetectionWorkflow,
    # "credit_underwriting": CreditUnderwritingWorkflow
}


class DeterministicPlanner:
    def __init__(self):
        self.reasoner = ReasoningEngine()

    def handle_request(self, user_prompt: str, context: dict):
        """
        The Hybrid Core:
        1. Uses Reasoning (LLM) to classify intent
        2. Uses Control Plane (Python) to route deterministically to State Machines
        """
        # --- 1. LLM Layer (Reasoning) ---
        print(f"[Planner] Analyzing Intent from prompt: '{user_prompt}'")
        intent_schema: IntentClassification = self.reasoner.classify_intent(user_prompt)

        print(
            f"[Planner] Classified Intent: {intent_schema.intent} (Confidence: {intent_schema.confidence})"
        )
        print(f"[Planner] Extracted Entities: {intent_schema.extracted_entities}")

        # --- 2. Deterministic Layer (Control) ---
        if intent_schema.intent not in WORKFLOW_MAP:
            print(
                f"[Planner] Rejecting execution: Unknown or unsupported workflow intent '{intent_schema.intent}'"
            )
            return {
                "status": "failed",
                "reason": "unsupported_intent",
                "classification": intent_schema.model_dump(),
            }

        if intent_schema.requires_human_verification:
            print(
                f"[Planner] Routing explicitly to HUMAN REVIEW queue based on sensitivity."
            )
            return {
                "status": "escalated_pre_routing",
                "classification": intent_schema.model_dump(),
            }

        context["intent_classification"] = intent_schema.model_dump()

        # Merge extracted entities into the context
        if intent_schema.extracted_entities:
            context.update(intent_schema.extracted_entities)

        # --- 3. Route and Execute ---
        print(
            f"[Planner] Instantiating deterministic workflow: {WORKFLOW_MAP[intent_schema.intent].__name__}"
        )
        workflow_class = WORKFLOW_MAP[intent_schema.intent]
        workflow = workflow_class(context)

        # Trigger the state machine
        return workflow.run()
