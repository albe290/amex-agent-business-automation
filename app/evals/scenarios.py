from typing import List
from app.evals.models import EvalCase

def get_baseline_scenarios() -> List[EvalCase]:
    """
    Returns the core set of evaluation scenarios for the platform.
    """
    return [
        EvalCase(
            case_id="SCENARIO_1_SAFE",
            scenario_type="SAFE_AUTOMATION",
            request_payload={
                "use_case_type": "dispute_inquiry",
                "customer_context": {"id": "CUST-101"},
                "business_payload": {"amount": 50.0}  # Risk score 10 -> AUTOMATE
            },
            expected_strategy="AUTOMATE",
            expected_review_required=False,
            expected_policy_hits=[]
        ),
        EvalCase(
            case_id="SCENARIO_2_INVESTIGATE",
            scenario_type="ELEVATED_RISK",
            request_payload={
                "use_case_type": "fraud_dispute",
                "customer_context": {"id": "CUST-202"},
                "business_payload": {"amount": 4500.0} # Risk score 30 -> INVESTIGATE
            },
            expected_strategy="INVESTIGATE",
            expected_review_required=False,
            expected_policy_hits=[]
        ),
        EvalCase(
            case_id="SCENARIO_3_ESCALATE",
            scenario_type="HIGH_RISK",
            request_payload={
                "use_case_type": "fraud_dispute",
                "customer_context": {"id": "CUST-303"},
                "business_payload": {"amount": 12000.0} # Risk score 60 + Policy Flag -> ESCALATE
            },
            expected_strategy="ESCALATE",
            expected_review_required=True,
            expected_policy_hits=["HIGH_VALUE_TRANSACTION"]
        ),
        EvalCase(
            case_id="SCENARIO_4_BLOCK",
            scenario_type="PII_VIOLATION",
            request_payload={
                "use_case_type": "fraud_dispute",
                "customer_context": {"id": "CUST-404"},
                "business_payload": {"amount": 200.0, "note": "my password is secret"}
            },
            expected_validation_status="FAILED",
            expected_strategy="BLOCK",
            expected_review_required=True, # Validator sets review to True on fail
            expected_policy_hits=["SECURITY_VALIDATION_FAILURE"]
        )
    ]
