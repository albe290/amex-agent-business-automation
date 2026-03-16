from typing import List, Dict, Any
from app.context.models import RetrievedEvidence, EnrichedEvidence

class ContextEnricher:
    """
    Transforms raw evidence into formatted business insights.
    """
    
    def enrich_evidence(self, raw_evidence: List[RetrievedEvidence]) -> List[EnrichedEvidence]:
        """
        Converts raw evidence into structured EnrichedEvidence objects.
        """
        enriched_list = []
        
        for item in raw_evidence:
            # Mock enrichment logic: extraction and tagging
            summary = f"Summary of {item.title}: {item.content[:100]}..."
            key_facts = self._extract_facts(item.content)
            risk_signals = self._detect_risk_signals(item.content)
            
            enriched_list.append(EnrichedEvidence(
                source_type=item.source_type,
                source_id=item.source_id,
                summary=summary,
                key_facts=key_facts,
                risk_signals=risk_signals,
                policy_tags=item.metadata.get("tags", [])
            ))
            
        return enriched_list

    def _extract_facts(self, content: str) -> List[str]:
        # Placeholder for NER or regex-based extraction
        facts = []
        if "$" in content:
            facts.append("Contains financial thresholds")
        if "NYC" in content:
            facts.append("Involves NYC location")
        return facts

    def _detect_risk_signals(self, content: str) -> List[str]:
        signals = []
        if "dispute" in content.lower():
            signals.append("PRIOR_DISPUTE_HISTORY")
        if "high-risk" in content.lower():
            signals.append("POLICY_HIGH_RISK_WARNING")
        return signals
