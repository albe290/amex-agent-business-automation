# 🧠 Core Engine Study Guide: The 5 Files That Run BlueShield

This guide dives into the "Execution Spine" of the platform. If these 5 files were removed, the factory would cease to function. This is designed to help engineers understand the high-level orchestration of a governed AI platform.

---

## 1. `app/intake/schemas.py` (The Front Door Contract)

### ❓ What problem does this file solve?
It solves the **Data Entropy** problem. In most AI projects, prompts are fed unstructured data strings. This file enforces a strict **PlatformRequest** schema (using Pydantic) that ensures every request—regardless of whether it came from a mobile app, a web dashboard, or a batch job—has a `request_id`, a `use_case_type`, and a validated `business_payload`.

### ❓ Why is this logic here instead of somewhere else?
By placing this at the "Intake" layer, we ensure **Fail-Fast validation**. If a request is missing a required field (like `business_payload`), the system rejects it at the boundary before any expensive AI models or database lookups are triggered.

### ❓ What are the inputs and outputs?
*   **Input**: Raw JSON or Dictionary data from an external source (API/Mobile).
*   **Output**: A validated `PlatformRequest` object that downstream layers can trust implicitly.

### ❓ What risk would happen if this file were removed?
The platform would suffer from **Type Instability**. Downstream components like the Control Plane would constantly crash because they wouldn't know if `amount` is a string, an integer, or missing entirely. The audit trail would also break because there would be no guaranteed `request_id`.

---

## 2. `app/control_plane/coordinator.py` (The Governed Brain)

### ❓ What problem does this file solve?
It solves the **Ungoverned Execution** problem. It prevents the system from blindly executing AI tasks. It acts as a mandatory "Checkpoint" that runs validation, calculates a mathematical risk score, and maps corporate policies to the request before a single agent is woken up.

### ❓ Why is this logic here instead of somewhere else?
It centralizes **Governance Orchestration**. Instead of every agent checking if they are allowed to run, the `ControlPlaneCoordinator` does it once at the start. This separation of concerns ensures that security logic is decoupled from agent logic.

### ❓ What are the inputs and outputs?
*   **Input**: A `PlatformRequest` (from Intake).
*   **Output**: A `ControlPlaneDecision`—a formal verdict containing a `risk_score`, `policy_hits`, and a `requires_review` flag.

### ❓ What risk would happen if this file were removed?
The system would be **Operationally Blind**. It would treat a $5.00 coffee purchase and a $50,000 wire transfer with the same level of caution, potentially leading to massive financial loss or regulatory violations.

---

## 3. `app/strategy/router.py` (The Traffic Tower)

### ❓ What problem does this file solve?
It solves the **Logic Branching** problem. Once the Control Plane provides a decision, the system needs to know *what to do next*. The Router is a deterministic engine that maps risk scores to execution paths (e.g., "If risk < 20, just automate it; if risk > 70, stop and ask a human").

### ❓ Why is this logic here instead of somewhere else?
It keeps the **Assembly Line deterministic**. We don't want an LLM (AI) to "decide" if a case needs review—that should be a hard business rule. By putting this in a standalone Python file, we ensure the routing is 100% predictable and auditable.

### ❓ What are the inputs and outputs?
*   **Input**: `ControlPlaneDecision` (the metadata about the request).
*   **Output**: A `StrategyPath` (An Enum: `AUTOMATE`, `INVESTIGATE`, `ESCALATE`, etc.).

### ❓ What risk would happen if this file were removed?
The system would become a **Dead End**. We would have a "Decision" (e.g., "High Risk"), but no logic to trigger the actual investigation. The robots would never know when to start work.

---

## 4. `app/events/consumer.py` (The Execution Engine)

### ❓ What problem does this file solve?
It solves the **Synchronization Bottleneck**. In a high-volume bank, you can't process requests one-by-one and make the customer wait. The Consumer runs as an asynchronous worker that pulls hundreds of events off a queue and processes them in the background, allowing the platform to scale.

### ❓ Why is this logic here instead of somewhere else?
It is the **Platform Heartbeat**. It separates the "API Receptionist" from the "Factory Floor." This logic lives here to ensure that if the AI takes 30 seconds to run, it doesn't block the API from accepting new orders.

### ❓ What are the inputs and outputs?
*   **Input**: Raw `PlatformEvent` objects from a queue (RabbitMQ/In-Memory).
*   **Output**: Final results published back to an outcome queue and persistent status updates in the `lifecycle_manager`.

### ❓ What risk would happen if this file were removed?
The factory would effectively **Stop Moving**. Even if requests are coming in, there would be no "engine" to pick them up and push them through the Control Plane or Strategy layers.

---

## 5. `app/review/coordinator.py` (The Human-in-the-Loop Hub)

### ❓ What problem does this file solve?
It solves the **Human-AI Isolation** problem. When the AI gets stuck or hits a high-risk limit, you need a safe way to hand off the work to a human. This file builds the "Context Packet" (the evidence), queues it for an analyst, and handles the most critical step of all: **The Human Override**.

### ❓ Why is this logic here instead of somewhere else?
It ensures **Auditability of Human Decisions**. By centralizing the submission of decisions here, we can track exactly *who* approved a risky transaction and *why* they overruled the AI's recommendation.

### ❓ What are the inputs and outputs?
*   **Input**: A request that "The Judge" flagged for review, plus all the evidence collected so far.
*   **Output**: A refined `ReviewPacket` for the dashboard and, eventually, a `ReviewDecision` that completes the workflow.

### ❓ What risk would happen if this file were removed?
The system would lose its **Safety Valve**. We would be forced to choose between "Fully Automated" (too dangerous) or "Fully Manual" (too slow). We would have no way to safely scale human expertise.
