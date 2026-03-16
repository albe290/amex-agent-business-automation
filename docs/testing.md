# Testing Strategy

## Philosophy

Tests in this platform are not just quality gates. They are **governance proof**.

The test suite validates:
- Normal platform behavior under expected inputs
- Correct decisions under elevated risk signals
- Safe behavior under adversarial or degraded inputs

A clean test run means the platform can be trusted, not just demonstrated.

---

## Test Structure

```
tests/
├── fixtures/          Shared request and event data
├── unit/              Single-component tests
├── integration/       Multi-layer flow tests
└── failure/           Adversarial and edge-case tests
```

---

## Current Coverage

```
======================== 45 passed in 0.49s ========================

Unit Tests (24):
  test_control_plane.py   — 9 tests
  test_strategy_router.py — 6 tests
  test_event_models.py    — 9 tests

Integration Tests (9):
  test_end_to_end_flow.py    — 3 tests
  test_review_path_flow.py   — 3 tests
  test_event_pipeline_flow.py — 3 tests

Failure Tests (12):
  test_malformed_input.py   — 4 tests
  test_policy_violation.py  — 4 tests
  test_missing_context.py   — 4 tests
```

---

## Key Test Categories

### Unit Tests
Test one component in isolation. No side effects, no dependencies.

**Strongest examples:**
- `test_low_risk_routes_to_automate` — routing is deterministic
- `test_routing_is_deterministic` — same input = same output, 10 iterations
- `test_risk_score_is_bounded` — score never exceeds 0–100

### Integration Tests
Test multiple layers together. Simulate real request flows.

**Strongest examples:**
- `test_safe_request_completes_as_automate` — full governed happy path
- `test_elevated_risk_completes_as_escalate` — high-value routing validated
- `test_lifecycle_transitions_flow_correctly` — event state machine proven

### Failure Tests
Adversarial inputs — prove safe behavior under bad conditions.

**Strongest examples:**
- `test_missing_context_does_not_automate` — empty context is escalated, not approved
- `test_high_value_transaction_policy_is_triggered` — $10K+ always hits policy
- `test_missing_required_field_raises_validation_error` — schema enforcement proven

---

## A Test That Found a Real Bug

During test implementation, `test_missing_context_does_not_automate` failed on first run.

**Root cause:** `RiskEngine` scored empty `customer_context` as low risk (score=10), routing to `AUTOMATE`.

**Fix:** Added missing-context penalty (+25) and unknown-merchant penalty (+15) to `RiskEngine.calculate_score`.

**Impact:** The platform now correctly treats unknown/incomplete context as elevated risk, preventing unsafe automation.

This is an example of tests not just verifying behavior, but **improving governance**.

---

## Running the Tests

```bash
# Run all tests
python -m pytest tests/ -v --tb=short

# Run by layer
python -m pytest tests/unit/ -v
python -m pytest tests/integration/ -v
python -m pytest tests/failure/ -v
```
