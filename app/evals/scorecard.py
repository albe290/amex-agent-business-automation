from app.evals.models import MetricSnapshot, Scorecard

class PlatformScorecard:
    """
    Transforms quantitative metrics into qualitative quality ratings.
    """
    
    def generate(self, metrics: MetricSnapshot) -> Scorecard:
        # 1. Governance Score
        gov_val = "STRONG"
        if metrics.pass_rate < 0.8: gov_val = "FAIR"
        if metrics.pass_rate < 0.5: gov_val = "POOR"
        
        # 2. Routing Quality
        rout_val = "STRONG"
        if metrics.strategy_match_rate < 0.8: rout_val = "FAIR"
        if metrics.strategy_match_rate < 0.5: rout_val = "POOR"
        
        # 3. Operational Efficiency
        # High automation + low fallback = Strong
        eff_val = "STRONG"
        if metrics.automation_rate < 0.3: eff_val = "FAIR"
        
        return Scorecard(
            governance_score=gov_val,
            routing_quality=rout_val,
            human_alignment="STRONG", # Placeholder for human review correlation
            operational_efficiency=eff_val,
            summary_notes=f"Platform processed {metrics.total_cases} cases with a {metrics.pass_rate*100:.1f}% success rate."
        )
