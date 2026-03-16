from typing import List
from app.evals.models import EvalResult, MetricSnapshot, Scorecard

class EvalReporter:
    """
    Generates human-readable reports from evaluation runs.
    """
    
    def print_summary(self, results: List[EvalResult], metrics: MetricSnapshot, scorecard: Scorecard, insights: List[str]):
        print("\n" + "="*50)
        print(" PLATFORM EVALUATION SUMMARY")
        print("="*50)
        
        print(f"\n[RESULTS] Total Cases: {metrics.total_cases}")
        print(f"   Passes: {sum(1 for r in results if r.passed)}")
        print(f"   Fails:  {sum(1 for r in results if not r.passed)}")
        
        for r in results:
            if not r.passed:
                print(f"     - FAIL {r.case_id}: {', '.join(r.failure_reasons)}")
        
        print("\n[CORE METRICS]")
        print(f"   Pass Rate:        {metrics.pass_rate*100:.1f}%")
        print(f"   Automation Rate:  {metrics.automation_rate*100:.1f}%")
        print(f"   Review Rate:      {metrics.review_rate*100:.1f}%")
        print(f"   Escalation Rate:  {metrics.escalation_rate*100:.1f}%")
        print(f"   Block Rate:       {metrics.block_rate*100:.1f}%")
        print(f"   Strategy Match:   {metrics.strategy_match_rate*100:.1f}%")
        
        print("\n[QUALITY SCORECARD]")
        print(f"   Governance:       {scorecard.governance_score}")
        print(f"   Routing Quality:  {scorecard.routing_quality}")
        print(f"   Efficiency:       {scorecard.operational_efficiency}")
        
        print("\n[STRATEGIC INSIGHTS]")
        for insight in insights:
            print(f"   - {insight}")
            
        print("\n" + "="*50 + "\n")
