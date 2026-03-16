# Interview Walkthrough

## The One-Line Answer

> "I built a governed agentic AI platform for financial workflow automation that combines deterministic policy controls, human review workflows, event-driven processing, and real-time observability."

---

## Project Summary (GitHub / Resume / LinkedIn)

> Built a governed agentic AI platform for financial workflow automation that combines standardized intake, context enrichment, deterministic control-plane decisions, strategy routing, bounded agent execution, runtime guardrails, human review workflows, evaluation scorecards, event-driven processing, and operational dashboard visibility. Designed to reflect production-minded AI engineering in a regulated enterprise environment.

---

## Resume Bullets (Pick 2–4)

- Designed and built a governed agentic AI platform for financial workflow automation with deterministic control-plane validation, risk scoring, strategy routing, human review workflows, and audit traceability.
- Engineered an event-driven AI decision platform with context enrichment, runtime guardrails, evaluation scorecards, and dashboard visibility for safe, explainable automation.
- Re-architected a framework-centric agent project into a production-oriented AI platform with modular governance, bounded execution, review queue orchestration, and deployment-ready service topology.
- Implemented policy-aware escalation logic, runtime safety controls, and human-in-the-loop review to improve oversight and operational visibility in a regulated financial workflow.

---

## Interview Talk Track

**Q: Tell me about this project.**

> This project solves the problem of unsafe, opaque, and inconsistent automation in regulated financial workflows.
>
> Instead of building it as a simple AI app, I designed it as a governed platform with clear architectural separation between intake, context, control plane, strategy, execution, runtime governance, review, audit, evaluation, and visibility.
>
> The control plane is the most important part because it applies deterministic validation, risk scoring, and policy boundaries before agents act. That prevents the system from relying purely on model behavior.
>
> I also added a first-class human review workflow so high-risk, ambiguous, or customer-impacting decisions can be reviewed and overridden safely.
>
> On top of that, I added evaluation scorecards, event-driven workflow simulation, failure testing, and a professional dashboard so the platform is measurable, explainable, and operationally visible.

---

## Angle-by-Angle Talk Track

### Why this architecture?

> I made a deliberate choice to separate governance from execution. Most AI agent projects put the LLM at the center — prompts go in, decisions come out. That's fine for demos but it's not auditable or predictable in production.
>
> By having a Control Plane — with a validator, risk engine, and policy evaluator — run before any AI agent, the system can prove its decisions. The Control Plane is deterministic. You can test it. You can tune it. You can explain it to a compliance team.
>
> The agents operate inside that boundary. They get richer context and use tools, but they can't override the governance layer.

### How does the control plane work?

> The control plane is three components in sequence: input validation, risk scoring, and policy evaluation.
>
> The risk engine produces a score from 0 to 100 based on transaction amount, prior fraud signals, velocity flags, and context completeness. Critically, if we don't know who the customer is, it scores higher, not lower. The policy engine checks that score against corporate rules and either allows the action, flags it for review, or blocks it.
>
> The output is a `ControlPlaneDecision` — a Pydantic model with a validation status, risk score, policy hits, allowed actions, and a `requires_review` flag. Downstream components consume that contract. Nothing acts without it.

### How does the review workflow work?

> When the control plane sets `requires_review = True`, the strategy router returns ESCALATE. A review packet is created with the risk signals, the AI's recommendation, and the evidence summary. It goes into a queue.
>
> A reviewer sees the recommendation and either approves, rejects, or sends it back for more context. If the reviewer disagrees with the AI — an override — that's a first-class record. We track override rate in the evaluation scorecard. A high override rate in one direction tells us the system is miscalibrated.

### How does the event pipeline work?

> The platform processes work asynchronously through a producer-consumer pipeline. A producer wraps incoming payloads into events, places them in a queue, and a consumer worker picks them up. Each event has a lifecycle state: RECEIVED → QUEUED → PROCESSING → COMPLETED or REVIEW_PENDING or BLOCKED.
>
> The publisher emits final outcomes to the event bus, which updates the real-time dashboard. The current implementation is in-memory but maps directly to Kafka or SQS — same producer-consumer-publisher model.

### How is the platform evaluated?

> I built an offline evaluation layer that runs test scenarios through the platform and scores outcomes against expected paths. The scorecard grades governance and routing quality.
>
> On first run I got a 100% scenario pass rate with a STRONG governance grade. The eval layer also generates diagnostic insights — if the review rate is too high, it suggests tuning the risk threshold. That creates a feedback loop between measurement and improvement.

### How is the platform tested?

> There are 45 tests across three layers: unit tests for individual components, integration tests for full governed flows, and failure scenario tests that prove the system fails safely.
>
> The failure tests actually found a real governance gap — the risk engine was auto-approving requests with empty customer context. The fix: missing context now adds 25 points to the risk score. That came from the test, not from code review.

### How would you scale this to production?

> The main infrastructure changes would be: replace the in-memory event queue with Kafka or SQS, upgrade the lifecycle state store to DynamoDB or Redis, add OpenTelemetry for distributed tracing, and build a proper approval UI for reviewers with RBAC.
>
> The business logic — the control plane, strategy router, review workflow, agents — stays the same. The architectural separation means you're only swapping infrastructure, not redesigning the platform.

---

## The One Differentiator

> "Most AI portfolio projects show that you can make LLMs do things. This one shows you can make LLMs do things **safely**, within governance boundaries, with human oversight where required, and with measurable quality.
>
> That's the difference between an AI demo and an AI platform."
