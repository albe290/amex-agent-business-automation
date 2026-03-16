from app.context.models import ContextPacket
from app.agents.models import AnalystOutput

class AnalystAgent:
    """
    Bounded worker for deep-dive investigation.
    """
    def run_deep_dive(self, context: ContextPacket) -> AnalystOutput:
        # Reasoning over the assembled evidence
        findings = [f"Analyzed {len(context.evidence)} evidence items."]
        for item in context.evidence:
            if item.risk_signals:
                findings.extend(item.risk_signals)

        return AnalystOutput(
            findings=findings,
            confidence=context.context_completeness_score,
            supporting_evidence=[{"id": e.source_id, "type": e.source_type} for e in context.evidence],
            recommended_path="INVESTIGATE"
        )
