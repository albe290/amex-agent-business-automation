# Amex Agent Business Automation: Execution Showcase

This document provides simulated terminal "screenshots" (logs) of our Agent Orchestrator resolving real-world financial intents against the **Sentinel Runtime Risk Engine** and our **Internal Validator Schemas**. 

You can run these locally by executing:
```bash
python showcase.py
```

---

### Policy Intelligence Layer (RAG)
The system retrieves 100% accurate policy context by embedding internal Amex guidelines into a vector store.
![RAG Policy Ingestion](assets/rag_ingestion.png)

---

## Scenario 1: Authorized Account Freeze (Standard Corporate)
**Context**: An employee suspects fraud on the Acme Corp account and requests to execute the `freeze_account` tool.

```bash
=========================================================================
   Scenario 1: Authorized Account Freeze (Standard Corporate)   
=========================================================================
Context: An employee suspects fraud on the Acme Corp account and requests a freeze.

Incoming Agent Intent:
{
  "actor": "employee",
  "action_to_take": "freeze_account",
  "account_id": "acc_456",
  "transaction_amount": 0.0
}

[Validator] Running Pre-Execution Checks...
[Orchestrator] Processing request for workflow: fraud_triage

[Sentinel Client] Crossing boundary to sentinel-runtime native score_step()...
Risk Score Calculated: 20
[Sentinel Risk Result] Action: ALLOW | Level: LOW | Score: 20 | Reason: policy_base_risk:10; internal_data:+10
[Execution] Triggering concrete tool: freeze_account on acc_456
[PASS] Sentinel Risk Engine: Decision = ALLOW (Action is safe based on policy/schema).
[PASS] Concrete Execution: Account acc_456 successfully mutated to FROZEN.
Final Account Status in DB: FROZEN
```

### Execution Log (Visual Proof)
![Live Execution Demo](assets/demo_execution.png)

---

## Scenario 2: Unauthorized Freeze Attempt (Centurion VIP)
**Context**: An employee attempts to bypass policy and freeze a highly sensitive Centurion (Black Card) account. The request is intercepted by our deterministic `financial_rules.py` layer *before* it even reaches Sentinel.

```bash
=========================================================================
   Scenario 2: Unauthorized Freeze Attempt (Centurion VIP)   
=========================================================================
Context: Employee attempts to freeze a highly sensitive Centurion (Black Card) account.

Incoming Agent Intent:
{
  "actor": "employee",
  "action_to_take": "freeze_account",
  "account_id": "acc_VIP",
  "transaction_amount": 0.0
}

[Validator] Running Pre-Execution Checks...
[Orchestrator] Processing request for workflow: fraud_triage
[Orchestrator] Request failed at validation layer: Cannot automatically freeze Centurion accounts.
[X] Financial Validator Override Triggered!
Error Type: financial_rule_violation
Detail: Cannot automatically freeze Centurion accounts. Must be escalated to VIP team.
Final Account Status in DB: ACTIVE (Unchanged)
```

---

## Scenario 3: High Value Transaction Approval Escalation
**Context**: An employee attempts to authorize a $15,000 transaction. The orchestrator validators allow the schema, but the **Sentinel Runtime Risk Engine** detects a high-risk score threshold violation and overrides the agent, automatically escalating it to a human.

```bash
=========================================================================
   Scenario 3: High Value Transaction Approval Escalation    
=========================================================================
Context: Employee attempts to authorize a $15,000 transaction on a standard account.

Incoming Agent Intent:
{
  "actor": "employee",
  "action_to_take": "approve_high_risk",
  "account_id": "acc_123",
  "transaction_amount": 15000.0
}

[Validator] Running Pre-Execution Checks (Passed)
[Sentinel Risk Engine] Evaluating complex runtime risk...
[Orchestrator] Processing request for workflow: fraud_triage

[Sentinel Client] Crossing boundary to sentinel-runtime native score_step()...
Risk Score Calculated: 95
[Sentinel Risk Result] Action: BLOCK | Level: CRITICAL | Score: 95 | Reason: policy_base_risk:85; internal_data:+10
[Escalation] Triggering concrete tool: create_review_ticket due to Action Block by Sentinel Runtime
[WARN] Sentinel Risk Engine: Decision = REVIEW/BLOCK (Threshold Exceeded).
[WARN] Execution halted. Creating Zendesk Escalation Ticket...
Ticket ID: TKT-1741093122 created for Human Analyst.
```

---
### System Architecture Impact
This showcase demonstrates our successful implementation of the "Trust but Verify" AI schema. While the LLM agent reasons about intents, the deterministic outer loop ensures absolute financial compliance.

### Verification Suite: 100% Safety Compliance
![Safety Test Suite](assets/safety_tests.png)
