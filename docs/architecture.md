# Architecture

## Philosophy

This platform is built around a single principle: **governance before autonomy**.

In most AI agent projects, the agent is the center — prompts go in, results come out. This works for demos. It fails in production.

In a financial context, an agent acting without constraint is a liability. A governed agent operating within a clearly defined policy boundary is an asset.

Every architectural decision in this platform flows from that principle.

---

## Architectural Layers

```
┌────────────────────────────────────────────────────────┐
│                    API / Event Layer                    │
│  Inbound requests, async events, webhook triggers       │
└────────────────────────────────────────────────────────┘
                          │
┌────────────────────────────────────────────────────────┐
│                    Intake Layer                         │
│  Schema validation, normalization, source tagging       │
└────────────────────────────────────────────────────────┘
                          │
┌────────────────────────────────────────────────────────┐
│                    Context Layer                         │
│  Policy retrieval, prior case lookup, evidence assembly │
└────────────────────────────────────────────────────────┘
                          │
┌────────────────────────────────────────────────────────┐
│               Control Plane (Governance Core)           │
│  Validation → Risk Scoring → Policy Evaluation         │
│  Output: ControlPlaneDecision (deterministic)          │
└────────────────────────────────────────────────────────┘
                          │
┌────────────────────────────────────────────────────────┐
│                    Strategy Router                      │
│  AUTOMATE / INVESTIGATE / ESCALATE / BLOCK             │
└────────────────────────────────────────────────────────┘
          │                            │
┌─────────────────┐          ┌──────────────────┐
│  Agent Runtime  │          │  Review Workflow  │
│  (AI Execution) │          │  (Human Oversight)│
└────────┬────────┘          └────────┬─────────┘
         │                            │
┌────────────────────────────────────────────────────────┐
│             Runtime Governance                          │
│  Step limits, budget controls, retry policies           │
└────────────────────────────────────────────────────────┘
                          │
┌────────────────────────────────────────────────────────┐
│         Audit + Evaluation + Event Bus                  │
│  Immutable trace, quality scorecards, outcome events    │
└────────────────────────────────────────────────────────┘
                          │
┌────────────────────────────────────────────────────────┐
│               Observability Dashboard                    │
│  Real-time React console (Vite + Tailwind)              │
└────────────────────────────────────────────────────────┘
```

---

## Major Components

| Component | Location | Responsibility |
|---|---|---|
| Intake | `app/intake/` | Schema normalization |
| Context | `app/context/` | Evidence retrieval and assembly |
| Control Plane | `app/control_plane/` | Deterministic governance |
| Strategy Router | `app/strategy/` | Path selection |
| AI Agents | `app/agents/` | Execution via CrewAI |
| Runtime | `app/runtime/` | Step/budget/retry guardrails |
| Review | `app/review/` | Human-in-the-loop workflow |
| Evals | `app/evals/` | Quality measurement |
| Events | `app/events/` | Async pipeline |
| Audit | `app/audit/` | Immutable trace |

---

## Why Architecture-First?

Most AI projects are framework-first: "I used CrewAI" or "I used LangChain." This platform is architecture-first: the framework serves the system design, not the other way around.

The separation into `control_plane`, `strategy`, `review`, and `runtime` layers makes it:
- **Auditable** — every decision has a traceable path
- **Replaceable** — swap CrewAI for any AI runtime without touching governance
- **Testable** — each layer can be unit tested independently
- **Scalable** — add Kafka, persistent queues, or vector databases without restructuring

---

## Design Tradeoffs

| Decision | Alternative | Why This Choice |
|---|---|---|
| Deterministic control plane | LLM-only routing | Auditability, reproducibility, compliance |
| In-memory event queue | Kafka/SQS | Simplicity for demo; maps directly to real infra |
| Pydantic contracts | Plain dicts | Schema enforcement, serialization, validation |
| Strategy enum routing | LLM decides path | Prevents hallucinated routing decisions |
