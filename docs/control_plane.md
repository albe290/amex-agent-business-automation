# Control Plane

The Control Plane is the governance core of the platform. It runs before any AI agent acts and produces a deterministic, auditable decision.

---

## Why a Control Plane?

In a regulated financial environment, you cannot trust an AI agent to decide its own boundaries. The control plane separates governance from execution:

- **Governance** → Control Plane (deterministic, auditable)
- **Execution** → AI Agents (intelligent, bounded)

This is the key architectural separation. Without it, the agent is both judge and actor — a pattern that creates audit risk and policy failures in production.

---

## Control Plane Components

### 1. Validator (`app/control_plane/validator.py`)
Performs input integrity checks:
- Schema completeness
- Prompt injection detection
- Content policy compliance

### 2. Risk Engine (`app/control_plane/risk.py`)
Calculates a normalized risk score (0–100) based on:
- Transaction amount thresholds
- Prior fraud score from risk metadata
- Velocity signals
- Missing customer context (penalized +25)
- Unknown merchant (penalized +15)
- New account age

**Design note:** Missing context is scored as elevated risk — the system cannot safely automate what it doesn't know.

### 3. Policy Engine (`app/control_plane/policy.py`)
Evaluates active corporate policies:
- `HIGH_VALUE_TRANSACTION` (amount > $5,000)
- `RISK_SCORE_CRITICAL` (score > 80)
- `AML_SECTION_3` (AML compliance hit)
- `SECURITY_VALIDATION_FAILURE`

Returns: `requires_review`, `policy_hits`, `allowed_actions`

### 4. Coordinator (`app/control_plane/coordinator.py`)
Orchestrates the full pipeline and returns a `ControlPlaneDecision`.

---

## Output Contract: ControlPlaneDecision

```python
class ControlPlaneDecision(BaseModel):
    validation_status: str     # "SUCCESS" or "FAILED"
    risk_score: float          # 0.0 - 100.0
    policy_hits: List[str]     # Policies triggered
    allowed_actions: List[str] # What the system may do
    requires_review: bool      # Human review mandatory?
    block_reason: Optional[str]
```

Every downstream component — strategy router, audit, dashboard — consumes this contract. Nothing acts without it.

---

## Risk Score Thresholds

| Score | Routing | Meaning |
|---|---|---|
| 0–19 | AUTOMATE | Safe for full automation |
| 20–69 | INVESTIGATE | AI analysis required |
| 70–100 | ESCALATE | Human review required |
| Any + `requires_review=True` | ESCALATE | Policy override |
| `validation_status=FAILED` | BLOCK | Stop immediately |
