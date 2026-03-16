# Chapter 13: The Guard Towers (The `security/` Layer)

## 1️⃣ Big Picture: The Guard Towers

Running an AI Factory is exciting, but it’s also dangerous. There are people who might try to trick our robots into giving away passwords or freezing the wrong accounts. To protect ourselves, we have built the **Guard Towers**.

Think of this as the "Secret Service" for our factory. They aren't just checking badges at the front door; they are watching every word the robots hear (*input*) and every word the robots speak (*output*). If a request looks suspicious or breaks a banking law, the Guard Towers shut it down instantly.

In this chapter, we’ll meet the members of the security team:
1.  **The Security Guard (`validator.py`)**: The main inspector who scans for traps (prompt injections) and secret leaks (PII).
2.  **The Security Rulebook (`policy_engine.py`)**: A large book of "Laws" (YAML) that defines exactly what actions are allowed for which customers.
3.  **The Regulatory Inspector (`compliance_validator.py`)**: Enforces non-negotiable banking rules (like "Only employees can freeze accounts").
4.  **The Tool Locker Key (`tool_guard.py`)**: A safety switch that double-checks every tool call before it reaches the real bank vault.
5.  **The Banking Laws (`financial_rules.py`)**: A "Fast-Fail" system that checks account types and limits before a robot even starts thinking.

---

## 2️⃣ Teach the Code

### 13.1 validator.py – The Security Guard

The `validator.py` file is the primary interface for security. It is the "Sentinel" that stands between the internet and our AI agents.

### A. Full File Ingestion: `security/validator.py`

```python
8: class SecurityValidator:
9:     """
10:     Sentinel-based security layer that wraps the CrewAI orchestration.
11:     """
12: 
13:     def __init__(self):
14:         self.policy_engine = PolicyEngine()
15: 
16:     def validate_prompt(self, user_request: str):
...
23:         injection_patterns = [
24:             r"ignore previous instructions",
25:             r"system prompt",
26:             r"override policy",
...
32:         for pattern in injection_patterns:
33:             if re.search(pattern, user_request, re.IGNORECASE):
34:                 print(f"[Sentinel] BLOCK: Prompt injection detected.")
...
38:                 return False, "Prompt injection detected."
...
55:     def validate_output(self, result: str):
...
62:         sensitive_patterns = [r"ssn", r"password", r"secret_key"]
63:         for pattern in sensitive_patterns:
64:             if re.search(pattern, result.lower(), re.IGNORECASE):
...
69:                 return False, "Sensitive data detected in output."
```

### B. File Purpose
The `SecurityValidator` acts as a **Two-Way Filter**.
1.  **Incoming Scan (`validate_prompt`)**: It looks for "Adversarial Patterns"—words used to trick AI into breaking its rules (like "Ignore all previous instructions").
2.  **Outgoing Scan (`validate_output`)**: It looks for "Sensitive Leaks"—making sure the robot didn't accidentally blurt out someone's password or social security number.

### C. Line-by-Line Explanation

**Line 16: `validate_prompt(...)`**
*   **The Action:** The very first thing that happens when a request arrives.
*   **Line 23-31 (`injection_patterns`):** This is the **List of Forbidden Words**. If the request contains things like "override policy" or "bypass tool," the guard hits the alarm.

**Line 41: `check_compliance_constraints(...)`**
*   **The Deep Check:** The guard doesn't just look for bad words; it also asks the **Regulatory Inspector** (Chapter 13.3) if the request follows banking laws.

**Line 55: `validate_output(...)`**
*   **The Action:** The last thing that happens before a human sees a report.
*   **Line 62 (`sensitive_patterns`):** The guard checks if the robot accidentally leaked a "password" or "ssn."

---

### 13.2 policy_engine.py – The Security Rulebook

While the Guard looks for bad words, the **Rulebook** checks for bad *actions*. The `policy_engine.py` file reads a YAML file to decide if an action is safe or too risky.

### A. Full File Ingestion: `security/policy_engine.py`

```python
6: class PolicyEngine:
...
31:     def evaluate_intent(
32:         self, action: str, context: Dict[str, Any]
33:     ) -> Tuple[str, str, int]:
...
40:         amount = context.get("transaction_amount", 0.0)
41:         max_amt = self.policy.get("global_limits", {}).get(...)
45:         if amount >= max_amt:
46:             return ("BLOCK", f"Transaction amount ... exceeds limit", 100)
...
63:         restricted_types = action_rules.get("restricted_account_types", [])
64:         account_type = context.get("account_type", "Standard")
65: 
66:         if account_type in restricted_types:
67:             return ("BLOCK", f"Action restricted for account type...", 90)
...
84:         if final_score < allow_t:
85:             return "ALLOW", "Action meets safety thresholds.", final_score
```

### B. File Purpose
The `PolicyEngine` is the **Legal Department**. It translates corporate rules into math. 
*   If a transaction is over a certain limit, it's **Blocked**.
*   If an account type is too basic for a specific tool, it's **Blocked**.
*   It calculates a "Final Risk Score" to help the Judge make a decision.

### C. Line-by-Line Explanation

**Line 31: `evaluate_intent(...)`**
*   **What it represents:** A formal "Legal Review" of a robot's plan.

**Line 40: `amount = ...`**
*   **The Check:** First, we check the money. If a robot tries to move $1,000,000, and the limit is $100,000, the rulebook says "BLOCK" (Line 46).

**Line 63-66: Account Type Restrictions**
*   **The Check:** Some actions (like VIP Account Freezing) can't be done on a "Standard" account.

**Line 77-84: The Final Score**
*   **The Result:** It combines everything into a score. If the score is low (Line 84), it returns **"ALLOW."** If the score is high, it returns "BLOCK."

---

### 🏁 Friendly Recap (Guard & Rulebook)

You've just met the **Security Guard and the Lawbook**!

You now understand:
1.  How the **Validator** blocks prompt injections and data leaks.
2.  How the **Policy Engine** turns YAML rules into real-world blocking decisions.
3.  Why we check the **Risk Score** before a robot is allowed to move.

### 13.3 compliance_validator.py – The Regulatory Inspector

In the banking world, some rules are non-negotiable. It doesn’t matter if the robot thinks it’s safe; if the banking law says "No," the answer is "No." The `compliance_validator.py` file is the **Regulatory Inspector**.

### A. Full File Ingestion: `security/compliance_validator.py`

```python
1: def check_compliance_constraints(action: str, context: dict) -> tuple[bool, str]:
2:     """
3:     Validates the action against overarching banking compliance regulations.
4:     """
7:     actor = context.get("actor", "unknown")
8: 
9:     # Rule 1: Only internal employees can trigger account freezes.
11:     if action == "freeze_account" and actor != "employee":
12:         return (
13:             False,
14:             "Compliance Violation: Account freezes must be initiated by an authorized employee.",
15:         )
16: 
17:     # Rule 2: Escalations require a valid reason string
18:     if action == "create_escalation_ticket":
19:         reason = context.get("reason", "")
20:         if len(reason) < 10:
21:             return (
22:                 False,
23:                 "Compliance Violation: Escalations must include a descriptive reason (min 10 chars).",
24:             )
25: 
26:     return True, "Passed compliance checks"
```

### B. File Purpose
The `check_compliance_constraints` function is a **Hard Filter**. It enforces rules that protect the bank from legal trouble.
*   **Role Enforcement**: Ensuring only humans with the right job title can take drastic actions (like freezing money).
*   **Data Quality**: Ensuring that if a robot escalates a case, it provides a real reason, not just a 1-word note.

### C. Line-by-Line Explanation

**Line 11-12: The Employee Check**
*   **The Law:** If a robot tries to "freeze_account" but the person asking isn't an "employee," the inspector blocks it immediately. This prevents accidental freezes by customers or external systems.

**Line 18-20: The Reason Check**
*   **The Law:** You can't just escalate a case for "No Reason." If the reason is too short (less than 10 characters), the inspector sends the robot back to do more homework.

---

### 13.4 tool_guard.py – The Tool Locker Key

What if a robot tries to use a tool (like a "Counterfeit Detector") without permission? The `tool_guard.py` file is the **Tool Locker Key**. It intercepts every attempt to use a tool and checks with the Regulatory Inspector first.

### A. Full File Ingestion: `security/tool_guard.py`

```python
5: class ToolGuard:
6:     """
7:     Middleware that intercept tool calls to ensure they are safe.
8:     """
9: 
10:     def check_call(self, tool_name: str, args: dict, actor: str = "agent"):
11:         print(f"[Sentinel Tool Guard] Intercepting call: {tool_name}...")
12: 
13:         # Cross-reference with compliance validator
14:         is_safe, msg = check_compliance_constraints(tool_name, {"actor": actor, **args})
15: 
16:         if not is_safe:
17:             print(f"[Sentinel Tool Guard] BLOCK: {msg}")
...
19:             return False, msg
```

### B. File Purpose
The `ToolGuard` acts as **Middleware**. It sits between the robot’s fingers and the button it wants to press. Even if the robot has already "decided" to use a tool, the Tool Guard can still pull the "Emergency Stop" cable.

### C. Line-by-Line Explanation

**Line 10: `check_call(...)`**
*   **The Catch:** This function intercepts the call.

**Line 14: `check_compliance_constraints(...)`**
*   **The Collaboration:** The Tool Guard doesn't decide on its own; it asks its friend, the **Regulatory Inspector** (Chapter 13.3), to double-check the rules.

---

### 13.5 financial_rules.py – The Banking Laws

Standard financial checks (like checking an account balance) should be fast and deterministic. The `financial_rules.py` file provides a **Fast-Fail Layer** that checks basic banking data before the advanced AI security even starts.

### A. Full File Ingestion: `security/financial_rules.py`

```python
5: def check_financial_rules(action: str, context: dict) -> tuple[bool, str]:
10:     # 1. Enrich context for policy engine
11:     account_id = context.get("account_id")
12:     account_info = get_account(account_id)
13:     if account_info:
14:         context["account_type"] = account_info.get("type", "Standard")
15: 
16:     # 2. Evaluate via Policy Engine
17:     engine = get_policy_engine()
18:     decision, reason, score = engine.evaluate_intent(action, context)
...
25:     if decision == "BLOCK":
26:         return False, f"Policy Violation: {reason}"
```

### B. File Purpose
This file is the **Context Enricher**. It gathers extra info about the customer (like their "Account Type") and then feeds that info into the **Security Rulebook** (Chapter 13.2) to get a quick "Yes" or "No."

---

### 🏁 Friendly Recap (Chapter 13 Completed!)

Congratulations! You've just finished the **Guard Towers**!

In this chapter, you learned:
1.  How the **Validator** stands guard at the input and output gates.
2.  How the **Policy Engine** uses a YAML "Rulebook" to calculate risk.
3.  Why the **Compliance Validator** ensures we follow banking laws.
4.  How the **Tool Guard** protects the bank's digital tools from unauthorized use.

**Our factory is now safer than a real bank vault. But what about the humans? How can we watch all this security and robot work on a beautiful screen? We're heading to the "Visual Console"—the `dashboard/` layer—next!**
