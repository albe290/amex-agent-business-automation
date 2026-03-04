import pytest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from rag.retriever import PolicyRetriever


@pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="OPENAI_API_KEY not set")
def test_policy_retriever_financial_rules():
    retriever = PolicyRetriever()

    # Ensure vector store was created by ingestion.py
    assert (
        len(retriever.documents) > 0
    ), "Vector store is empty. Did you run ingestion.py?"

    # Search for an explicitly known policy
    results = retriever.search(
        "What happens if a customer transaction is over $5000?", top_k=1
    )

    assert len(results) == 1

    # We should expect the escalation matrix to be returned
    assert "escalation_matrix.md" in results[0]
    assert "OVER $5,000" in results[0] or "OVER $5000" in results[0]


@pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="OPENAI_API_KEY not set")
def test_policy_retriever_empty_handling():
    # If a vector_store isn't generated, it should fail gracefully
    retriever = PolicyRetriever()
    retriever.documents = []  # Force empty

    results = retriever.search("Test empty", top_k=1)
    assert len(results) == 1
    assert "No policies retrieved" in results[0]
