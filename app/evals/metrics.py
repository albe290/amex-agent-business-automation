from typing import List
from app.evals.models import EvalResult, MetricSnapshot

class PlatformMetrics:
    """
    Calculates operational and quality metrics from evaluation results.
    """
    
    def calculate_snapshot(self, results: List[EvalResult]) -> MetricSnapshot:
        total = len(results)
        if total == 0:
            return MetricSnapshot(
                total_cases=0, pass_rate=0, automation_rate=0, review_rate=0, 
                escalation_rate=0, block_rate=0, strategy_match_rate=0, policy_hit_precision=0
            )
            
        passes = sum(1 for r in results if r.passed)
        
        # Routing distribution
        automations = sum(1 for r in results if r.actual_strategy == "AUTOMATE")
        escalations = sum(1 for r in results if r.actual_strategy == "ESCALATE")
        blocks = sum(1 for r in results if r.actual_validation_status == "FAILED" or r.actual_strategy == "BLOCK")
        reviews = sum(1 for r in results if r.actual_review_required)
        
        strategy_matches = sum(1 for r in results if not any("Strategy mismatch" in f for f in r.failure_reasons))
        
        # Simple policy precision: Ratio of actual hits vs total possible in suite
        # (In a real system, this would compare against a 'Gold Standard' for policy labeling)
        
        return MetricSnapshot(
            total_cases=total,
            pass_rate=passes / total,
            automation_rate=automations / total,
            review_rate=reviews / total,
            escalation_rate=escalations / total,
            block_rate=blocks / total,
            strategy_match_rate=strategy_matches / total,
            policy_hit_precision=100.0 # Placeholder for baseline calibration
        )
