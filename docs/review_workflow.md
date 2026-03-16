# Review Workflow

The review workflow is the platform's **human-in-the-loop layer**. It operationalizes human oversight — not as a vague concept, but as a governed, audited process.

---

## What Triggers a Review?

A case enters the review workflow when any of the following are true:

| Trigger | Source |
|---|---|
| Risk score ≥ 70 | Risk Engine |
| `HIGH_VALUE_TRANSACTION` policy hit | Policy Engine |
| PII detected in payload | Validator |
| AI agent requests escalation | Agent output |
| Runtime fallback triggered | Runtime Guardrails |

---

## Review Workflow Steps

```
1. Control Plane sets requires_review = True
2. Strategy Router returns ESCALATE
3. Review Coordinator creates a ReviewPacket
4. Packet placed in ReviewQueue
5. Reviewer views recommendation, evidence, and risk signals
6. Reviewer makes one of three decisions:
      APPROVE  → case proceeds with action
      REJECT   → case is blocked
      SEND_BACK → more information requested
7. Decision recorded in ReviewRecord
8. If reviewer overrides AI recommendation → OverrideRecord created
9. Audit log updated with full reviewer trace
```

---

## Review Packet Contents

```python
class ReviewPacket(BaseModel):
    packet_id: str
    request_id: str
    risk_score: float
    policy_hits: List[str]
    ai_recommendation: str       # What the platform recommends
    evidence_summary: str        # Context used for the recommendation
    created_at: datetime
    priority: str                # HIGH / MEDIUM / LOW
```

---

## Why Overrides Matter

When a reviewer approves a case the system flagged for block — or rejects a case the system recommended to automate — that is an **override**.

Overrides are first-class records in this platform. They serve as:

1. **Calibration data** — frequent overrides in one direction signal a mis-tuned threshold
2. **Audit evidence** — prove that human judgment was applied, not rubber-stamping
3. **Evaluation signal** — tracked in Phase 4 scorecards as `human_override_rate`

---

## Queue Health Metrics

The review queue exposes:
- **Queue depth** — how many cases are waiting
- **MTTR** (Mean Time to Review) — average queue age in hours
- **Override rate** — % of reviews that disagreed with the AI recommendation

These metrics are displayed live on the Observability Dashboard.
