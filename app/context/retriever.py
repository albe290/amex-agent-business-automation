from typing import List, Dict, Any
from app.context.models import RetrievedEvidence
from app.context.sources import POLICY_STORE, CASE_STORE, CUSTOMER_STORE

class ContextRetriever:
    """
    Handles fetching candidate evidence from multiple platform sources.
    Integrated with Policy, Case, and Customer data.
    """
    
    def fetch_evidence(self, query_terms: List[str], customer_id: str) -> List[RetrievedEvidence]:
        """
        Retrieves raw evidence objects from all available sources.
        """
        results = []
        
        # 1. Retrieve matching Policies (Keyword mock)
        for policy in POLICY_STORE:
            for term in query_terms:
                if term.lower() in policy["content"].lower() or term.lower() in policy["title"].lower():
                    results.append(RetrievedEvidence(
                        source_type="policy",
                        source_id=policy["source_id"],
                        title=policy["title"],
                        content=policy["content"],
                        relevance_score=0.9, # Mocked score
                        metadata={"tags": policy.get("tags", [])}
                    ))
                    break # Don't duplicate for multiple terms
                    
        # 2. Retrieve Prior Cases
        for case in CASE_STORE:
            if case.get("customer_id") == customer_id:
                results.append(RetrievedEvidence(
                    source_type="case_history",
                    source_id=case["source_id"],
                    title=case["title"],
                    content=case["content"],
                    relevance_score=0.95
                ))
                
        # 3. Retrieve Customer Context
        customer = CUSTOMER_STORE.get(customer_id)
        if customer:
            results.append(RetrievedEvidence(
                source_type="customer",
                source_id=customer_id,
                title="Customer Profile",
                content=str(customer),
                relevance_score=1.0,
                metadata=customer
            ))
            
        return results
