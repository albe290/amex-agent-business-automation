# Governed Agentic AI Platform — Interactive Showcase Guide

This document demonstrates the **Governed Agentic AI Platform for Financial Workflow Automation** — a production-oriented system that combines deterministic governance, strategy routing, human review workflows, event-driven processing, and real-time observability.

---

## 🚀 Running the Platform

### Start the dashboard (observability console)

```bash
cd dashboard
npm run dev
# Open http://localhost:5173
```

### Run the event pipeline simulation

```bash
python scripts/verify_event_pipeline.py
```

### Run the full test suite

```bash
python -m pytest tests/ -v --tb=short
# Expected: 45 passed
```

---

## 🎭 Governed Workflow Scenarios

The platform processes every request through a deterministic control plane before any AI agent acts. The four core paths demonstrate how governance, risk scoring, and policy evaluation drive decisions.

---

### Scenario 1 — Safe Automation ✅

**Profile:** Known customer, low-risk transaction  
**Amount:** $42.00 — trusted merchant  
**Risk Score:** 12 (Low)  
**Policy Hits:** None  

**What happens:**
- Control Plane: `validation_status=SUCCESS`, `requires_review=False`
- Strategy Router: → **AUTOMATE**
- AI Agent executes under runtime guardrails
- Outcome: `COMPLETED` | Audit captured

**Demonstrates:** High-speed, governed automation for low-risk routine work.

---

### Scenario 2 — Human Escalation Required 🔶

**Profile:** New account, high-value transaction  
**Amount:** $8,500.00 — electronics purchase  
**Risk Score:** 78 (High)  
**Policy Hits:** `HIGH_VALUE_TRANSACTION`, `RISK_SCORE_CRITICAL`  

**What happens:**
- Control Plane: `validation_status=SUCCESS`, `requires_review=True`
- Strategy Router: → **ESCALATE**
- Review packet created and queued
- Human reviewer sees AI recommendation + evidence
- Outcome: `REVIEW_PENDING` | Override tracked if reviewer disagrees

**Demonstrates:** Structured human-in-the-loop oversight for high-value cases.

---

### Scenario 3 — Policy Block ⛔

**Profile:** PII detected / AML compliance hit  
**Amount:** Any  
**Risk Score:** 95 (Critical)  
**Policy Hits:** `SECURITY_VALIDATION_FAILURE`, `AML_SECTION_3_COMPLIANCE`  

**What happens:**
- Control Plane: `validation_status=FAILED`
- Strategy Router: → **BLOCK**
- No AI agent execution — action denied immediately
- Outcome: `BLOCKED` | Full audit record created

**Demonstrates:** Governance stopping unsafe actions before they reach any agent.

---

### Scenario 4 — Missing Context Investigation 🔍

**Profile:** Unknown customer, no prior case history  
**Amount:** $500.00 — unknown merchant  
**Risk Score:** 50 (elevated due to missing context penalty +25, unknown merchant +15)  
**Policy Hits:** None  

**What happens:**
- Control Plane: risk engine penalizes missing context
- Strategy Router: → **INVESTIGATE**
- Agents perform deeper analysis before action
- Outcome: `COMPLETED` with investigation notes

**Demonstrates:** The platform treats unknown context conservatively — a governance gap caught by the test suite and fixed.

---

## 📊 Dashboard Views

### Executive Overview
Real-time KPI cards — automation rate, review rate, risk captured, avg latency — with platform throughput trends and strategy distribution.

![Executive Overview](docs/screenshots/01_executive_overview.png)

---

### Governance & Risk
Live policy enforcement feed showing every rule triggered across the platform, with the risk profile matrix and strictness level.

![Governance & Risk](docs/screenshots/02_governance_risk.png)

---

### Review Queue
Active human review cases with age, reason, domain, and owner tracking. Includes override history and queue health metrics (MTTR, queue depth).

![Review Queue](docs/screenshots/03_review_queue.png)

---

### Evaluation & Scorecards
Platform quality benchmarks — Governance: **STRONG**, Routing: **STRONG** — with automation precision (96.4%), routing success (100%), and diagnostic insights.

![Evaluation & Scorecards](docs/screenshots/04_evaluation_scorecards.png)

---

## 🏛️ Platform Architecture

```
[Request / Event]
       │
       ▼
 [Intake Layer]       ← Schema validation
       │
       ▼
 [Context Layer]      ← Evidence retrieval
       │
       ▼
 [Control Plane]      ← Validate → Risk Score → Policy
       │
       ▼
 [Strategy Router]
  /    |    |    \
AUTO  INV  ESC  BLOCK
  │         │
[Agents]  [Review Queue] → [Human Decision]
  │
[Runtime Guardrails]
  │
[Audit + Evals + Dashboard]
```

---

## ✅ Test Results

```
======================== 45 passed in 0.49s ========================

Unit Tests:         24 passed  (Control Plane, Strategy, Event Models)
Integration Tests:   9 passed  (End-to-End, Review Path, Event Pipeline)
Failure Tests:      12 passed  (Malformed Input, Policy Violations, Missing Context)
```

**Key finding:** The failure test suite caught a real governance gap — the risk engine was auto-approving requests with empty customer context. Fixed in-place during Phase 7.

---

---

## 📚 Educational Integration: The BlueShield Book

This project is now fully documented for educational purposes. Every core file can be explored through our **15-Chapter Documentation Series** located in the `docs/` folder.

- **Start here**: **[Book Table of Contents](docs/book_toc.md)**
- **Deep Dive**: **[Core Engine Study Guide](CORE_ENGINE_STUDY_GUIDE.md)** — Learn how to speak about this project in technical interviews.

---

## 🏆 Evaluation Scorecard

```
OVERALL PASS RATE: 100% (4/4 scenarios)

Governance:       STRONG   Routing Quality:  STRONG
Automation Rate:  25%      Review Rate:      50%
Block Rate:       25%      Strategy Match:   100%
```

---

## 🔮 Production Scale Path

| Current | Production |
|---------|------------|
| In-memory event queue | Kafka / AWS SQS |
| Audit log (in-memory) | PostgreSQL + CloudWatch |
| Review queue (in-memory) | Redis priority queue |
| Eval results (JSON) | S3 + Athena |
| Docker Compose (local) | ECS / Kubernetes |
