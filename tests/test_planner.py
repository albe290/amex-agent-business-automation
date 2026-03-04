import pytest
import os
import sys

# Add the project root to the python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from financial_agent_core.planner import DeterministicPlanner
from tools.mock_db import reset_db


# These tests REQUIRE an OpenAI API Key
@pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="OPENAI_API_KEY not set")
def test_hybrid_planner_fraud_triage_routing():
    reset_db()
    planner = DeterministicPlanner()

    # Natural language prompt acting as an employee
    test_prompt = "I'm a customer support agent. A user is calling about a weird charge on their target card. It looks like a huge purchase for $12000 that they didn't make. I need to handle this immediately."

    # 1. Provide the initial context (we know we are an employee running the system)
    context = {"actor": "employee"}

    # 2. Fire the hybrid system!
    result = planner.handle_request(user_prompt=test_prompt, context=context)

    # 3. Assert our control plane is deterministic!
    assert "status" in result
    assert result["status"] == "completed"

    # We expect the LLM to extract the intent and NOT flag it for human verification
    assert (
        context.get(
            "intent_classification",
            result.get("classification", context.get("intent_classification")),
        )["intent"]
        == "fraud_triage"
    )
    assert context["intent_classification"]["requires_human_verification"] is False


@pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="OPENAI_API_KEY not set")
def test_hybrid_planner_fails_gracefully_on_unknown():
    reset_db()
    planner = DeterministicPlanner()

    # Natural language prompt that isn't supported yet
    test_prompt = "Can you please re-issue my missing debit card?"

    context = {"actor": "customer"}

    # Fire the hybrid system
    result = planner.handle_request(user_prompt=test_prompt, context=context)

    # The ReasoningEngine should extract something like 'card_replacement'
    # The DeterministicPlanner doesn't have that in WORKFLOW_MAP and should explicitly reject.
    assert "status" in result
    assert result["status"] == "failed"
    assert result["reason"] == "unsupported_intent"
    assert result["classification"]["intent"] != "fraud_triage"
