# Transaction Escalation Matrix

## Customer Transactions
1. For any customer transaction reported as anomalous OVER $5,000, the action `freeze_account` must be explicitly DENIED by the system until a human reviews it.
2. For any customer transaction UNDER $5,000, `freeze_account` is ALLOWED immediately.

## Employee Actions
1. If an employee is handling a fraud triage ticket, they are ALLOWED to `freeze_account` unconditionally to secure the customer's funds.
2. If an employee attempts to `approve_high_risk` transaction that is OVER $10,000, the transaction must be escalated to a manager queue (REVIEW).
3. If an employee attempts to `approve_high_risk` transaction UNDER $10,000, it is ALLOWED.
