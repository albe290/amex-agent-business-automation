# Transaction Escalation Matrix

## Customer Transactions
1. For any customer transaction reported as anomalous OVER $5,000, the action `freeze_account` should be evaluated for immediate security response.
2. For any customer transaction UNDER $5,000, automated remediation is prioritized.

## Employee Actions
1. If an employee is handling a fraud triage ticket, they are authorized to `freeze_account` to secure the customer's funds, provided the account level is not 'Centurion' or 'VIP'.
2. If an employee attempts to `approve_high_risk` transaction that is OVER $100,000, the transaction is strictly BLOCKED by the global governance limit.
3. If an employee attempts to `approve_high_risk` transaction UNDER $100,000, it is subject to Sentinel Risk Evaluation and may trigger a `REVIEW`.
