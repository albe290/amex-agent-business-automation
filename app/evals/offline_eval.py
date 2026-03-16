import time
from typing import List
from app.evals.models import EvalCase, EvalResult
from app.intake.schemas import PlatformRequest
from app.control_plane.coordinator import ControlPlaneCoordinator
from app.strategy.router import StrategyRouter

class OfflineEvalEngine:
    """
    The main test runner for processing evaluation scenarios through the platform.
    """
    
    def __init__(self):
        self.control_plane = ControlPlaneCoordinator()
        # No instantiation needed for StrategyRouter as it's static

    def run_case(self, case: EvalCase) -> EvalResult:
        """
        Runs a single evaluation case through the platform's core logic.
        """
        start_time = time.time()
        failure_reasons = []
        
        # 1. Prepare Request
        request = PlatformRequest(**case.request_payload)
        
        # 2. Run Control Plane
        decision = self.control_plane.process_request(request)
        
        # 3. Determine actual strategy
        strategy_path = StrategyRouter.select_path(decision)
        actual_strategy = strategy_path.value
        
        # 4. Score results
        # Status match
        if decision.validation_status != case.expected_validation_status:
            failure_reasons.append(f"Status mismatch: expected {case.expected_validation_status}, got {decision.validation_status}")
            
        # Strategy match
        if actual_strategy != case.expected_strategy:
            failure_reasons.append(f"Strategy mismatch: expected {case.expected_strategy}, got {actual_strategy}")
            
        # Review match
        if decision.requires_review != case.expected_review_required:
            failure_reasons.append(f"Review mismatch: expected {case.expected_review_required}, got {decision.requires_review}")

        # Policy Hits match (Partial/Subset check)
        for expected_hit in case.expected_policy_hits:
            if expected_hit not in decision.policy_hits:
                failure_reasons.append(f"Missing expected policy hit: {expected_hit}")

        latency = (time.time() - start_time) * 1000
        
        return EvalResult(
            case_id=case.case_id,
            scenario_type=case.scenario_type,
            actual_validation_status=decision.validation_status,
            actual_strategy=actual_strategy,
            actual_review_required=decision.requires_review,
            actual_policy_hits=decision.policy_hits,
            passed=len(failure_reasons) == 0,
            failure_reasons=failure_reasons,
            latency_ms=latency
        )

    def run_suite(self, cases: List[EvalCase]) -> List[EvalResult]:
        return [self.run_case(c) for c in cases]
