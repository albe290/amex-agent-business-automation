# Evaluation and Scorecards

The evaluation layer answers: **how do we know this platform is actually working correctly?**

Without measurement, governance is just policy documents. With measurement, governance becomes provable.

---

## Evaluation Strategy

The platform uses two evaluation modes:

| Mode | When | Purpose |
|---|---|---|
| **Offline Eval** | On-demand simulation | Validate scenarios against expected outcomes |
| **Online Eval** | Post-decision | Measure live platform behavior over time |

---

## Offline Evaluation Scenarios

Defined in `app/evals/scenarios.py`. Each scenario specifies:
- A `PlatformRequest` input
- An `expected_outcome` (AUTOMATE / ESCALATE / BLOCK)
- Whether human review is expected

### Baseline scenario suite

| Scenario | Expected Path | Risk Level |
|---|---|---|
| Low-risk expense approval | AUTOMATE | Low |
| High-value transaction | ESCALATE | High |
| Policy violation (AML) | BLOCK | Critical |
| Incomplete context | INVESTIGATE or ESCALATE | Medium |

---

## Phase 4 Results

```
OVERALL PASS RATE: 100.0% (4/4 cases passed)

METRICS:
  Automation Rate:  25%
  Review Rate:      50%
  Escalation Rate:  25%
  Block Rate:       25%
  Strategy Match:   100%

SCORECARD:
  Governance:        STRONG
  Routing Quality:   STRONG
  Efficiency:        FAIR

INSIGHTS:
  PLATFORM_STABLE — Metrics within optimal bounds.
  OPTIMIZE_REVIEW — High review rate suggests threshold tuning opportunity.
```

---

## Scorecard Grades

| Grade | Meaning |
|---|---|
| `STRONG` | Metrics within optimal enterprise bounds |
| `FAIR` | Functional but optimization recommended |
| `WEAK` | Significant risk or quality issues |

---

## Key Metrics Calculated

| Metric | Formula | Target |
|---|---|---|
| Automation Rate | `automated / total` | 40–60% |
| Review Rate | `reviewed / total` | < 30% |
| Strategy Match Rate | `correct_path / total` | > 95% |
| Human Override Rate | `overrides / reviews` | < 20% |

---

## How Evals Improve the Platform

The eval loop creates a feedback cycle:

```
Eval Run → Scorecard → Diagnostic Insights
    → Threshold Tuning → Re-eval → Improved Scorecard
```

High override rates signal over-escalation. High block rates on low-risk cases signal validator miscalibration. These insights are actionable, not just observable.
