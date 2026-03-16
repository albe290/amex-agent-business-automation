# Chapter 9: The Safety Rails (The `app/runtime/` Layer)

## 1️⃣ Big Picture: The Safety Rails

In our factory, we have conductors and robots working at high speeds. But what happens if a robot gets "stuck" in a loop, tries to spend too much money, or attempts a dangerous action (like sending a final payment) without human approval?

This is where the **Safety Rails** come in.

Think of this as the **Sensor Room** of the factory. Every single move a robot makes is monitored in real-time. If a robot moves too fast, spends too much, or breaks a rule, the Safety Rails immediately pull the emergency brake.

In this chapter, we’ll meet:
1.  **The Referee's Notebook (`models.py`)**: Tracks every step and every penny spent in real-time.
2.  **The Speed Limits (`limits.py`)**: Ensures we don't take too many steps or spend too much time.
3.  **The Wallet (`budget.py`)**: Monitors the "Token Cost" (the electricity of AI).
4.  **The Safety Barriers (`guardrails.py`)**: Blocks specific dangerous actions before they happen.
5.  **The Second Chance (`retries.py`)**: Decides if a robot error is worth a retry.
6.  **The Emergency Exit (`fallback.py`)**: The safe "Plan B" used when a robot is blocked.
7.  **The Execution Referee (`coordinator.py`)**: The master monitor who runs all these checks before every robot move.

---

## 2️⃣ Teach the Code

### 9.1 models.py – The Referee's Notebook

To enforce rules, we need a way to track what is happening *right now*. The `models.py` file defines the "Notebook" used by the Referee to log execution progress.

### A. Full File Ingestion: `app/runtime/models.py`

```python
1: from pydantic import BaseModel, Field
2: from typing import Optional, List, Dict, Any
3: from datetime import datetime
4: 
5: class RuntimeCheckResult(BaseModel):
6:     """
7:     Standardized result for a runtime governance check.
8:     """
9:     allowed: bool
10:     reason_code: str
11:     message: str
12: 
13: class RuntimeState(BaseModel):
14:     """
15:     Tracks the active execution state of a platform request.
16:     Used for limit enforcement and budget monitoring.
17:     """
18:     request_id: str
19:     strategy_path: str
20:     status: str = "INITIALIZED"
21:     
22:     # Execution Counters
23:     step_count: int = 0
24:     tool_calls: int = 0
25:     retries_used: int = 0
26:     
27:     # Budget Tracking
28:     model_calls: int = 0
29:     tokens_estimated: int = 0
30:     budget_used_usd: float = 0.0
31:     
32:     # Temporal Tracking
33:     start_time: datetime = Field(default_factory=datetime.utcnow)
34:     elapsed_seconds: float = 0.0
35:     
36:     # Governance Flags
37:     governance_violations: List[str] = Field(default_factory=list)
38:     fallback_triggered: bool = False
39:     fallback_reason: Optional[str] = None
40: 
```

### B. File Purpose
The `RuntimeState` is the **Main Dashboard** for a single transaction. It tracks:
*   **Counters**: How many times the robot has thought (`step_count`) or used a tool (`tool_calls`).
*   **Budget**: How much money (`budget_used_usd`) the AI has spent.
*   **Safety Status**: If any rules have been broken (`governance_violations`).

### C. Line-by-Line Explanation

**Line 5: `RuntimeCheckResult`**
*   **The Checkmark:** Whenever the Referee checks a rule, they return this form. It says `allowed: True` (Go) or `allowed: False` (Stop).

**Line 13: `RuntimeState`**
*   **The Notebook:** This is the big object that stays "alive" while the robots are working.
*   **Line 23-25:** We count every step, tool used, and retry.
*   **Line 30 (`budget_used_usd`):** We track the actual cost in dollars!
*   **Line 33 (`start_time`):** We record exactly when the mission started so we can measure speed.

---

### 9.2 limits.py – The Speed Limits

Just like a highway has speed limits, our AI Factory has **Execution Limits**. The `limits.py` file define the maximum "Oversight" boundaries.

### A. Full File Ingestion: `app/runtime/limits.py`

```python
1: from app.runtime.models import RuntimeState, RuntimeCheckResult
2: 
3: class RuntimeLimits:
4:     """
5:     Enforces hard execution boundaries for the platform.
6:     """
7:     
8:     def __init__(self, max_steps: int = 5, max_tool_calls: int = 3, max_seconds: float = 60.0):
9:         self.max_steps = max_steps
10:         self.max_tool_calls = max_tool_calls
11:         self.max_seconds = max_seconds
12: 
13:     def validate(self, state: RuntimeState) -> RuntimeCheckResult:
14:         """
15:         Checks if the current state is within execution limits.
16:         """
17:         if state.step_count >= self.max_steps:
18:             return RuntimeCheckResult(
19:                 allowed=False,
20:                 reason_code="STEP_LIMIT_EXCEEDED",
21:                 message=f"Maximum execution steps ({self.max_steps}) reached."
22:             )
...
31:         if state.elapsed_seconds >= self.max_seconds:
32:             return RuntimeCheckResult(
33:                 allowed=False,
34:                 reason_code="TIME_LIMIT_EXCEEDED",
35:                 message=f"Maximum runtime duration ({self.max_seconds}s) exceeded."
36:             )
37:             
38:         return RuntimeCheckResult(allowed=True, reason_code="LIMIT_OK", message="Within limits.")
```

### B. File Purpose
The `RuntimeLimits` class is the **Stopwatch**. It ensures that if a robot gets confused and asks the same question 50 times, we stop it before it wastes resources.

### C. Line-by-Line Explanation

**Line 8: `__init__(...)`**
*   **Setting the Rules:** We define the max steps (5), tool calls (3), and seconds (60s).

**Line 17: `if state.step_count >= self.max_steps:`**
*   **The First Check:** If the robot has thought more than 5 times, we return a "False" check (Line 19) and block the next move.

**Line 31: `if state.elapsed_seconds >= self.max_seconds:`**
*   **The Time Check:** If the mission is taking longer than 60 seconds, we pull the plug. Efficiency is safety!

---

### 9.3 budget.py – The Wallet

In the world of AI, every word the robot thinks costs a tiny amount of money (tokens). The `budget.py` file is our **Wallet**.

### A. Full File Ingestion: `app/runtime/budget.py`

```python
1: from app.runtime.models import RuntimeState, RuntimeCheckResult
2: 
3: class RuntimeBudget:
4:     """
5:     Monitors and enforces resource consumption budgets.
6:     """
7:     
8:     def __init__(self, max_model_calls: int = 3, max_usd: float = 0.50):
9:         self.max_model_calls = max_model_calls
10:         self.max_usd = max_usd
11: 
12:     def validate(self, state: RuntimeState) -> RuntimeCheckResult:
13:         """
14:         Checks if the execution is within cost and call budgets.
15:         """
16:         if state.model_calls >= self.max_model_calls:
...
23:         if state.budget_used_usd >= self.max_usd:
24:             return RuntimeCheckResult(
25:                 allowed=False,
26:                 reason_code="COST_BUDGET_EXCEEDED",
27:                 message=f"Estimated cost budget (${self.max_usd}) exceeded."
28:             )
29:             
30:         return RuntimeCheckResult(allowed=True, reason_code="BUDGET_OK", message="Within budget.")
```

### C. Line-by-Line Explanation

**Line 8: `__init__(...)`**
*   **Setting the Budget:** We decide that no single transaction can cost more than **$0.50** (50 cents).

**Line 23: `if state.budget_used_usd >= self.max_usd:`**
*   **The Money Check:** If the AI is being too "talkative" and spending too much money, we stop it immediately. This prevents a "Runaway AI" from spending the bank's entire budget.

---

### 🏁 Friendly Recap (Data & Boundaries)

You've just met the **Referee and their Notebook**!

You now understand:
1.  How the **Referee's Notebook** (models.py) tracks every move and every penny.
2.  Why **Speed Limits** (limits.py) are used to prevent AI loops.
3.  How the **Wallet** (budget.py) ensures the factory remains profitable.

### 9.4 guardrails.py – The Safety Barriers

While Limits and Budgets look at *quantity* (how much, how long), **Guardrails** look at *quality* (what action). The `guardrails.py` file is our **Safety Barriers**. It blocks specific robot actions if they are too dangerous to perform without a human signature.

### A. Full File Ingestion: `app/runtime/guardrails.py`

```python
1: from typing import Dict, Any
2: from app.runtime.models import RuntimeCheckResult
3: from app.control_plane.decision import ControlPlaneDecision
4: 
5: class RuntimeGuardrails:
6:     """
7:     Enforces real-time action safety and policy boundaries.
8:     """
9:     
10:     def validate_action(self, action_name: str, decision: ControlPlaneDecision) -> RuntimeCheckResult:
11:         """
12:         Validates if a specific action is allowed given the control plane decision.
13:         """
14:         # Rule 1: Block autonomous outbound actions if review is required
15:         outbound_actions = ["SEND_PAYMENT", "NOTIFY_CUSTOMER", "OFFER_REFUND"]
16:         if action_name in outbound_actions and decision.requires_review:
17:             return RuntimeCheckResult(
18:                 allowed=False,
19:                 reason_code="GUARDRAIL_BLOCK_REVIEW_REQUIRED",
20:                 message=f"Action '{action_name}' blocked. Human review is required."
21:             )
22: 
23:         # Rule 2: Block high-risk actions entirely (optional policy)
24:         if decision.risk_score > 90 and action_name == "PRE_APPROVE_DISPUTE":
...
31:         return RuntimeCheckResult(allowed=True, reason_code="GUARDRAIL_OK", message="Action permitted.")
```

### B. File Purpose
The `RuntimeGuardrails` class acts as a **Proximity Sensor**. If a robot tries to "touch" an outbound payment while the system is in "Review Only" mode, it gets a "False" check result and is physically blocked from completing the action.

### C. Line-by-Line Explanation

**Line 15: `outbound_actions = [...]`**
*   **The Danger Zone:** We list the actions that send money or emails to customers.

**Line 16: `if action_name in outbound_actions and decision.requires_review:`**
*   **The Barrier:** If the robot wants to do a dangerous action, but the **Judge** (Control Plane) said we need a human review, we block the robot! robots are never allowed to spend money autonomously if a case is flagged for a human eye.

---

### 9.5 retries.py – The Second Chance

In a factory, sometimes a tool slips or a robot fumbles. In the AI world, sometimes a model doesn't answer or a network connection fails. The `retries.py` file is the **Second Chance**. It decides if an error is just a "fumble" (worth trying again) or a "breakage" (stop immediately).

### A. Full File Ingestion: `app/runtime/retries.py`

```python
3: class RetryPolicy:
...
8:     def __init__(self, max_retries: int = 2):
9:         self.max_retries = max_retries
10: 
11:     def should_retry(self, state: RuntimeState, error_code: str) -> bool:
...
19:         retryable_codes = ["RETRIEVAL_TIMEOUT", "MODEL_PARSING_ERROR", "TRANSIENT_NETWORK_FAILURE"]
20:         
21:         return error_code in retryable_codes
```

**Line 19: `retryable_codes = [...]`**
*   **The List of Fumbles:** We define errors that are "transient" (temporary). If the model had a parsing error, we give the robot one more try to get its formatting right.

---

### 9.6 fallback.py – The Emergency Exit

If a robot is blocked by a budget, a limit, or a guardrail, we can't just let the whole factory crash. We need a safe way to exit. The `fallback.py` file is the **Emergency Exit**.

### A. Full File Ingestion: `app/runtime/fallback.py`

```python
13: class RuntimeFallback:
14:     """
15:     Logic for safely exiting failed or blocked executions.
16:     """
17:     
18:     def generate_fallback(self, reason_code: str, message: str) -> FallbackResult:
19:         """
20:         Maps a violation code to a safe platform output.
21:         """
22:         if "LIMIT" in reason_code or "BUDGET" in reason_code:
23:             return FallbackResult(
24:                 fallback_type="ESCALATE_TO_REVIEW",
25:                 reason=f"Execution halted: {message}",
26:                 safe_output={"status": "INCOMPLETE", "note": "Resource limits reached"}
27:             )
...
36:         return FallbackResult(
37:             fallback_type="TERMINATE_UNSAFE",
38:             reason=f"Safety termination: {message}",
39:             requires_review=True
40:         )
```

### B. File Purpose
The `RuntimeFallback` ensures our factory "fails safe." Instead of doing something unpredictable, it Escalates the case to a human or Terminates the task cleanly.

---

### 🏁 Friendly Recap (Safety & Recovery)

You've just learned how to **Prevent and Recover** from mistakes!

You now understand:
1.  How **Safety Barriers** (guardrails.py) block dangerous financial actions.
2.  How the **Second Chance** (retries.py) helps robots recover from minor fumbles.
3.  Why the **Emergency Exit** (fallback.py) ensures the factory always exits in a "Safe" state.

### 9.7 coordinator.py – The Execution Referee

We have all the rules in place. Now we need one master official to watch the clock, check the wallet, and blow the whistle if a guardrail is hit. The `coordinator.py` is the **Execution Referee**.

### A. Full File Ingestion: `app/runtime/coordinator.py`

```python
11: class RuntimeCoordinator:
12:     """
13:     The 'Execution Referee'. Orchestrates governance checks during workflow execution.
14:     """
15:     
16:     def __init__(self):
17:         self.limits = RuntimeLimits()
18:         self.budget = RuntimeBudget()
19:         self.guardrails = RuntimeGuardrails()
20:         self.retries = RetryPolicy()
21:         self.fallback_handler = RuntimeFallback()
...
26:     def pre_step_check(self, state: RuntimeState) -> RuntimeCheckResult:
27:         """
28:         Checks limits and budget before executing the next step.
29:         """
...
34:         limit_check = self.limits.validate(state)
35:         if not limit_check.allowed:
36:             return limit_check
37:             
38:         # 3. Check Budget
39:         budget_check = self.budget.validate(state)
40:         if not budget_check.allowed:
41:             return budget_check
42:             
43:         return RuntimeCheckResult(allowed=True, reason_code="PRE_STEP_OK", message="Safe to proceed.")
```

### B. File Purpose
The `RuntimeCoordinator` is the **Main Orchestrator of Safety**. It is responsible for making sure that *every* governance check happens at the right time. It doesn't write the rules; it just enforces them by calling the other experts (Limits, Budget, etc.).

### C. Line-by-Line Explanation

**Lines 16-21: The Referee's Gear**
*   **What it does:** Initializes the whole safety squad: the Limits stopwatch, the Budget wallet, the Guardrail barriers, the Retry whistle, and the Fallback emergency exit.

**Line 26: `pre_step_check(...)`**
*   **The Action:** Before a robot takes even one step of a plan, the Referee shouts "WAIT!" and runs two checks:
    1.  **Limits (Line 34):** Are we moving too fast?
    2.  **Budget (Line 39):** are we spending too much?

**Line 43: `return RuntimeCheckResult(allowed=True...)`**
*   **The Green Light:** If both checks pass, the Referee waves the green flag and says "Safe to proceed."

---

### 🏁 Friendly Recap (Chapter 9 Completed!)

Congratulations! You've just mastered the **Safety Rails** of the factory!

In this chapter, you learned:
1.  How the **Referee's Notebook** (models.py) tracks execution math in real-time.
2.  How **Speed Limits** (limits.py) and **Budgets** (budget.py) prevent runaway robots.
3.  How **Guardrails** (guardrails.py) block specific dangerous financial moves.
4.  Why the **Coordinator** is necessary to blow the whistle before every single step.

**The transaction is moving, the robots are working, and the safety rails are watching. But how do we know if the factory is actually *succeeding*? How do we measure the quality of our robots' brains? In the next chapter, we're heading to the "Performance Lab"—the `app/evals/` layer!**
