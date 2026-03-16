# Workflow Paths

The platform processes every request through one of four governed paths. The path is selected deterministically by the **Strategy Router** based on the **Control Plane Decision**.

---

## Path 1: Safe Automation (AUTOMATE)

**Triggered when:** Risk score < 20, no policy flags, valid context.

```
Request → Intake → Context → Control Plane
    → Strategy: AUTOMATE
    → AI Agents execute under Runtime Guardrails
    → Outcome published
    → Audit updated
    → Dashboard metrics updated
```

**Business meaning:** Low-risk routine work is handled fully automatically with no human involvement. Speed and efficiency are maximized.

---

## Path 2: Agent Investigation (INVESTIGATE)

**Triggered when:** Risk score 20–70, no critical policy flags.

```
Request → Intake → Context → Control Plane
    → Strategy: INVESTIGATE
    → AI Agents perform deep analysis
    → Runtime Guardrails enforce safe execution
    → Result summarized and submitted
    → Audit updated
```

**Business meaning:** Moderate-risk cases get comprehensive AI analysis before a decision is made. Confidence is built before action.

---

## Path 3: Human Escalation (ESCALATE)

**Triggered when:** Risk score ≥ 70, or `requires_review = True`, or policy hit.

```
Request → Intake → Context → Control Plane
    → Strategy: ESCALATE
    → Review Packet created
    → Placed in Review Queue
    → Reviewer approves / rejects / sends back
    → Override record created (if reviewer overrides AI recommendation)
    → Audit updated with reviewer decision
```

**Business meaning:** High-risk cases are not automated. A human reviews the AI's recommendation and makes the final call. The audit records both the AI recommendation and the human decision.

---

## Path 4: Policy Block (BLOCK)

**Triggered when:** Validation fails, severe policy violation, PII detected in restricted context.

```
Request → Intake → Context → Control Plane
    → Strategy: BLOCK
    → Action immediately denied
    → Block reason recorded
    → Audit updated
    → No AI agent execution
```

**Business meaning:** Some cases should never proceed to automation or review. The system stops immediately and records why.

---

## Path 5: Event-Driven Flow

**Triggered when:** Events arrive via the async Producer.

```
Event created by Producer
    → Placed in EventQueue (RECEIVED → QUEUED)
    → Consumer dequeues (QUEUED → PROCESSING)
    → Dispatcher routes to handler
    → Platform workflow executes (one of Paths 1–4)
    → Lifecycle updated (COMPLETED / REVIEW_PENDING / BLOCKED / FAILED)
    → Publisher emits OutcomeEvent
    → Dashboard and Audit updated
```

**Business meaning:** The platform can process work asynchronously from a queue, decoupling intake from execution. This enables batch processing, retry logic, and backpressure handling.
