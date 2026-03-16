from typing import List, Dict, Any, Optional
from app.context.models import ContextPacket, RetrievedEvidence, EnrichedEvidence
from app.context.retriever import ContextRetriever
from app.context.ranker import EvidenceRanker
from app.context.enricher import ContextEnricher
from app.intake.schemas import PlatformRequest

class ContextBuilder:
    """
    Orchestrates the retrieval, ranking, and enrichment of business context.
    Produces the final ContextPacket for downstream consumption.
    """
    
    def __init__(self):
        self.retriever = ContextRetriever()
        self.ranker = EvidenceRanker()
        self.enricher = ContextEnricher()

    def build_context(self, request: PlatformRequest) -> ContextPacket:
        """
        Assembles the ContextPacket from multiple platform sources.
        """
        request_id = request.request_id
        
        # 1. Define Query Terms (Simplified logic for Phase 3C)
        query_terms = [request.use_case_type]
        if "merchant" in request.business_payload:
            query_terms.append(request.business_payload["merchant"])
        if "amount" in request.business_payload:
            query_terms.append("luxury" if request.business_payload["amount"] > 3000 else "transaction")

        # 2. Retrieve Raw Evidence
        customer_id = request.customer_context.get("id", "UNKNOWN")
        raw_evidence = self.retriever.fetch_evidence(query_terms, customer_id)
        
        # 3. Rank and Filter
        ranked_evidence = self.ranker.rank_and_filter(raw_evidence)
        
        # 4. Enrich Evidence
        enriched_evidence = self.enricher.enrich_evidence(ranked_evidence)
        
        # 5. Missing Context Detection
        missing_fields, gaps, completeness = self._detect_gaps(request, enriched_evidence)
        
        # 6. Extract Lists for Legacy Components
        policies = [e.source_id for e in enriched_evidence if e.source_type == "policy"]
        cases = [e.source_id for e in enriched_evidence if e.source_type == "case_history"]

        # 7. Assemble Packet
        return ContextPacket(
            request_id=request_id,
            request_summary=f"Context-grounded analysis for {request.use_case_type} at {request.business_payload.get('merchant', 'Unknown')}",
            customer_context=request.customer_context,
            transaction_context=request.business_payload,
            evidence=enriched_evidence,
            policy_references=policies,
            prior_cases=cases,
            missing_fields=missing_fields,
            context_completeness_score=completeness,
            retrieval_gaps=gaps
        )

    def _detect_gaps(self, request: PlatformRequest, enriched: List[EnrichedEvidence]) -> tuple:
        missing_fields = []
        gaps = []
        
        # Check for essential source types
        source_types = {e.source_type for e in enriched}
        if "customer" not in source_types:
            missing_fields.append("customer_risk_profile")
            gaps.append("NO_CUSTOMER_RECORD_FOUND")
            
        if "policy" not in source_types:
            gaps.append("NO_MATCHING_POLICY_FOUND")
            
        # Calculate a simple completeness score
        completeness = len(source_types) / 3.0 # Assuming 3 core types: policy, case, customer
        
        return missing_fields, gaps, min(completeness, 1.0)
