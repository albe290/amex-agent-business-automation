from typing import List
from app.evals.models import MetricSnapshot

class EvalAnalyzer:
    """
    Analyzes evaluation metrics to provide strategic improvement insights.
    """
    
    def analyze(self, metrics: MetricSnapshot) -> List[str]:
        insights = []
        
        if metrics.review_rate > 0.4:
            insights.append("HIGH_REVIEW_RATE: System may be overly conservative. Consider tuning risk thresholds.")
            
        if metrics.automation_rate < 0.2:
            insights.append("LOW_AUTOMATION: Platform is under-leveraging agent capabilities for low-risk tasks.")
            
        if metrics.strategy_match_rate < 0.7:
             insights.append("LOW_STRATEGY_ALIGNMENT: Router logic deviates from expected business paths. Review Strategy Routing rules.")
             
        if metrics.block_rate > 0.3:
            insights.append("HIGH_BLOCK_RATE: Policy enforcement is highly restrictive. Verify if false-positive blocks are occurring.")
            
        if not insights:
            insights.append("PLATFORM_STABLE: Metrics are within optimal enterprise bounds.")
            
        return insights
