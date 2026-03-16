from typing import List, Dict, Any

# Mock Data Repositories
POLICY_STORE = [
    {
        "source_id": "POL_402",
        "title": "Luxury Item Transaction Policy",
        "content": "Transactions over $4,000 for luxury items (watches, jewelry) in high-risk zones (NYC, LA) require manual verification if the account is less than 180 days old.",
        "tags": ["LUXURY", "NYC", "THRESHOLD"]
    },
    {
        "source_id": "POL_AML_03",
        "title": "Anti-Money Laundering - High Velocity",
        "content": "Successive transactions exceeding $2,000 within a 2-hour window must be flagged for SAR review.",
        "tags": ["AML", "VELOCITY"]
    }
]

CASE_STORE = [
    {
        "source_id": "CASE_9988",
        "title": "Prior Dispute - Luxury WatchNYC",
        "content": "Customer disputed $5,000 charge at same merchant 3 months ago. Dispute was resolved in customer favor due to stolen card.",
        "customer_id": "AMEX-US-9988"
    }
]

CUSTOMER_STORE = {
    "AMEX-US-9988": {
        "tier": "PLATINUM",
        "account_age_days": 120,
        "risk_rating": "MEDIUM",
        "primary_location": "NYC"
    }
}
