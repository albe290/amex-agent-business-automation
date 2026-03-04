# Weekly Security Governance Playbook 🛡️📅

This playbook outlines scenarios you can run weekly to demonstrate the power of the **Secure Financial AI Agent** and **Sentinel Runtime** integration. Each scenario involves a simple change to `policy.yaml` or `policy_finance.yaml` to trigger a different security outcome.

---

## 🟢 Week 1: The "New Tool" Onboarding
**Objective:** Demonstrate how a "Default Deny" policy protects the system when adding new capabilities.

1.  **Change:** Add a new tool name in `orchestrator.py` (e.g., `update_credit_limit`) but **DO NOT** add it to `policy_finance.yaml`.
2.  **Run:** Execute a request for this new tool.
3.  **Result:** The Sentinel Gateway will return `BLOCK` with the reason `Tool not defined in policy`.
4.  **Dashboard:** Shows a new blocked attack vector, proving the "Zero-Trust" stance.

---

## 🟡 Week 2: "Targeted Lockdown" (High-Value Accounts)
**Objective:** Show how to tighten security during a period of high fraud alerts.

1.  **Change:** In `sentinel-runtime/policy/policy_finance.yaml`, increase the `base_risk` of `freeze_account` from `15` to `55`.
2.  **Run:** Scenario 1 (Standard Freeze).
3.  **Result:** What was previously an **ALLOW** will now be a **REVIEW** or **BLOCK**.
4.  **Dashboard:** The "Avg Risk Score" will spike, and the "Steps Reviewed" counter will increase.

---

## 🔴 Week 3: "Privileged Escalation" (Actor Risk)
**Objective:** Differentiate between Human-in-the-Loop and Fully Autonomous agents.

1.  **Change:** In `policy_finance.yaml`, under `scoring.data_sensitivity`, increase the `internal` weight to `40`.
2.  **Run:** Any scenario where the `actor` is `employee`.
3.  **Result:** The total risk will exceed thresholds for standard employees, forcing human supervisor approval.
4.  **Dashboard:** Demonstrates "Role-Based AI Governance".

---

## 🏴‍☠️ Week 4: "Active Breach Response" (The Kill Switch)
**Objective:** Demonstrate an emergency shutdown of all AI automation.

1.  **Change:** In `policy_finance.yaml`, set the `allow` threshold to `0` and the `review` threshold to `0`.
2.  **Run:** Any showcase scenario.
3.  **Result:** **TOTAL BLOCK.** Every single agent action is halted across the board.
4.  **Dashboard:** A visual "Wall of Red," showing the ASOC in full mitigation mode.

---

## 🛡️ Week 5: "MITRE ATLAS Alignment"
**Objective:** Verify that defenses are holding against specific known techniques.

1.  **Change:** Modify the `shell_exec` risk score to `95`.
2.  **Run:** A simulated Red Team attack in the harness.
3.  **Result:** The Red Team panel will update to **STOPPED** for "Unauthorized Shell Access".
4.  **Dashboard:** Live verification that the "Financial Governance Protocol" is MITRE-compliant.
