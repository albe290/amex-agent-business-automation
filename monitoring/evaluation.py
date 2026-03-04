import time
from runner.orchestrator import AgentOrchestrator


class AgentEvaluator:
    """
    Simulates running the agent against a 'golden dataset'
    to evaluate its accuracy and compliance safety before a real deployment.
    """

    def __init__(self):
        self.orchestrator = AgentOrchestrator()

    def evaluate_golden_dataset(self, dataset: list) -> dict:
        total = len(dataset)
        passed = 0
        failed = 0
        start_time = time.time()

        for case in dataset:
            context = case["context"]
            expected_decision = case["expected_decision"]
            workflow = case.get("workflow", "fraud_triage")

            result = self.orchestrator.process_request(workflow, context)

            # Use 'decision' if it survived validation, else use the 'status' (FAILED)
            actual_decision = (
                result.get("decision")
                if result.get("status") == "COMPLETED"
                else "BLOCK"
            )

            # If the orchestrator blocks it early via validation, Sentinel never sees it.
            # Both represent a "BLOCK" in the eyes of evaluation.
            if result.get("status") == "FAILED":
                actual_decision = "BLOCK"

            if actual_decision == expected_decision:
                passed += 1
            else:
                failed += 1
                print(
                    f"[Evaluation] FAILED: Context {context['account_id']} | Expected {expected_decision}, Got {actual_decision}"
                )

        duration = time.time() - start_time
        accuracy = (passed / total) * 100 if total > 0 else 0

        return {
            "total_cases": total,
            "passed": passed,
            "failed": failed,
            "accuracy_percent": round(accuracy, 2),
            "evaluation_time_seconds": round(duration, 4),
        }
