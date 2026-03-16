# Chapter 7: Power Tools & Actions (The `app/actions/` & `tools/` Layer)

## 1️⃣ Big Picture: The Power Tools Room

In the previous chapters, we met the robots and gave them their instruction manuals. But a robot with a plan is still just a robot standing in a room. To actually *change* anything—like freezing a stolen card or checking a bank balance—they need **Power Tools**.

In this chapter, we enter the **Power Tools Room**. 

Think of this as the part of the factory where the robots actually pick up hammers, screwdrivers, and scanners to interact with the real world (or in our case, our simulated "Warehouse").

Here’s what we’ll find:
1.  **The Main Assembly Line (`transaction_service.py`)**: The master machine that coordinates every step of a transaction.
2.  **The Packaging Station (`executor.py`)**: The machine that puts the final "Success" sticker on the finished work.
3.  **The Warehouse Storage (`mock_db.py`)**: Our simulated bank vault where all account data lives.
4.  **The Robot Toolbox (`tools/`)**: The specific tools (like the Account Lookup tool) that our robots use to reach into the warehouse.

---

## 2️⃣ Teach the Code

### 7.1 transaction_service.py – The Main Assembly Line

This is the most important file in the entire factory. It is the **Orchestrator**. It’s like the "Main Conductor" of an orchestra, making sure the Security Guard, the AI Robots, and the Risk Engines all play their part at the right time.

### A. Full File Ingestion: `app/actions/transaction_service.py`

```python
1: # services/transaction_service.py
2: import time
3: from fastapi import HTTPException
4: from pydantic import BaseModel
5: from typing import Optional
6: from crew.financial_crew import FinancialCrew
7: from security.validator import SecurityValidator
8: from monitoring.metrics import log_execution_metrics, event_bus
9: from risk.scoring_engine import calculate_risk_score
10: from tools.audit_logger import log_audit
11: 
12: 
13: class TransactionRequest(BaseModel):
14:     account_id: str
15:     merchant_id: str
16:     amount: float
17:     actor: str = "employee"
18:     custom_prompt: Optional[str] = None
19: 
20: 
21: class TransactionResponse(BaseModel):
22:     status: str
23:     message: str
24:     latency: str
25: 
26: 
27: class TransactionService:
28:     def __init__(self):
29:         self.validator = SecurityValidator()
...
```

*(Note: File is long, we will break it into three segments for clear teaching.)*

### B. File Purpose (Segment 1: The Setup)
The `TransactionService` is the **Final Gatekeeper**. It takes a raw request from the outside world and manages it until a final "Approve" or "Deny" decision is reached.

### C. Line-by-Line Explanation (Segment 1)

**Lines 2-10: Recruiting the Experts**
*   **What it does:** This file brings in everyone we've met so far:
    *   **FinancialCrew:** The Robot Squad leaders.
    *   **SecurityValidator:** The gate guard.
    *   **calculate_risk_score:** The math genius.
    *   **log_audit:** The stenographer who writes everything down.

**Line 13: `class TransactionRequest(BaseModel):`**
*   **The Order Form:** This defines what a customer request looks like: who they are, how much they’re spending, and where.

**Line 21: `class TransactionResponse(BaseModel):`**
*   **The Receipt:** This defines the final answer we give back to the customer.

**Line 27: `class TransactionService:`**
*   **The Master Conductor:** The brain of the assembly line.

---

### A. Full File Ingestion: `app/actions/transaction_service.py` (Segment 2)

```python
47:     async def process(self, req: TransactionRequest) -> TransactionResponse:
48:         user_prompt = (
49:             req.custom_prompt
50:             if req.custom_prompt
51:             else f"Analyze transaction for {req.account_id} at {req.merchant_id} for ${req.amount}"
52:         )
53: 
54:         await event_bus.emit(
55:             "CASE_INITIALIZED",
56:             {
57:                 "account_id": req.account_id,
58:                 "merchant_id": req.merchant_id,
59:                 "amount": req.amount,
60:             },
61:         )
62:         await event_bus.emit("SENTINEL_SCAN", {})
63: 
64:         # 1. Security Check
65:         is_safe, msg = self.validator.validate_prompt(user_prompt)
66:         if not is_safe:
67:             await event_bus.emit(
68:                 "SENTINEL_BLOCK", {"reason": msg or "prompt_injection_detected"}
69:             )
70:             raise HTTPException(status_code=403, detail=f"Security Block: {msg}")
71: 
...
```

### C. Line-by-Line Explanation (Segment 2)

**Line 47: `async def process(...)`**
*   **The Starting Pistol:** This is the function that actually *runs* the assembly line. It is `async`, meaning it can handle many things at once without waiting.

**Line 54: `await event_bus.emit("CASE_INITIALIZED", ...)`**
*   **The Radio Broadcast:** Every time a transaction starts, the Conductor picks up a radio and shouts, "NEW CASE STARTED!" so everyone else (like the Dashboard) can hear it.

**Line 65: `is_safe, msg = self.validator.validate_prompt(user_prompt)`**
*   **The Security Guard:** Before anything else happens, the Guard (Sentinel) checks the message. If it looks like a trick (Prompt Injection), the whole line stops immediately (Line 70).

---

### A. Full File Ingestion: `app/actions/transaction_service.py` (Segment 3)

```python
79:             crew_engine = FinancialCrew(transaction_data)
80:             result = crew_engine.run()
81: 
82:             latency = time.time() - start_time
83: 
84:             # 3. Output Check
85:             is_output_safe, output_msg = self.validator.validate_output(str(result))
...
90:             final_score = calculate_risk_score(transaction_data, str(result))
91: 
92:             if final_score >= 80:
93:                 policy_decision = "APPROVE"
...
109:             log_audit(transaction_data, final_score, policy_decision, str(result))
...
114:             return {
115:                 "status": external_response["status"],
116:                 "message": external_response["message"],
117:                 "latency": f"{latency:.2f}s",
118:             }
```

### C. Line-by-Line Explanation (Segment 3)

**Line 80: `result = crew_engine.run()`**
*   **The Robots Work:** This is where the **Robot Squad** (from Chapter 6) actually runs. They go into the library, use their tools, and come back with an answer.

**Line 90: `final_score = calculate_risk_score(...)`**
*   **The Math Genius:** Once the robots are done, we hand their notes to the Math Genius to calculate the final 0-100 risk score.

**Lines 92-97: The Policy Decision**
*   **The Verdict:** We use a simple rule:
    *   **80+ points:** High safety! **APPROVE**.
    *   **50-79 points:** Hmm, let's **REVIEW**.
    *   **Below 50:** Too risky. **BLOCK**.

**Line 109: `log_audit(...)`**
*   **Writing the History:** Everything that happened is written into the "Audit Log" (the factory's permanent record).

**Lines 114-118: The Final Handover**
*   **The receipt:** We hand the final decision (Approve/Deny) back to the customer and tell them how long it took (`latency`).

---

### 🏁 Friendly Recap (The Main Assembly Line)

You've just witnessed the **Master Conductor** in action!

You now understand:
1.  How the Conductor (TransactionService) coordinates Security, AI, and Math.
2.  Why the **Security Guard** (Sentinel) always goes first.
3.  How we translate robot thoughts into a final "Score" and "Verdict."

### 7.2 executor.py – The Final Packaging Station

Once the Conductors and the Robots are finished, we need to put the final result into a standard box that our customers can understand. The `executor.py` file is our **Packaging Station**. It takes the "strategic plan" results and wraps them in a final, clean "Mission Complete" label.

### A. Full File Ingestion: `app/actions/executor.py`

```python
1: from typing import Dict, Any, List
2: from pydantic import BaseModel
3: 
4: class PlatformOutput(BaseModel):
5:     """
6:     Standardized final output of the platform.
7:     """
8:     request_id: str
9:     status: str
10:     message: str
11:     data: Dict[str, Any]
12: 
13: class ActionExecutor:
14:     """
15:     The controlled execution layer.
16:     Turns agent recommendations into platform outcomes.
17:     """
18:     
19:     def execute(self, request_id: str, plan_results: List[Any]) -> PlatformOutput:
20:         # Final formatting and action logic
21:         return PlatformOutput(
22:             request_id=request_id,
23:             status="ACTION_COMPLETE",
24:             message="Strategic plan executed successfully.",
25:             data={"summary": "Agentic investigation complete. Path resolved."}
26:         )
21: 
```

### B. File Purpose
The `ActionExecutor` is the **Final Sign-Off**. It doesn't do the thinking; it just ensures the paperwork is filled out correctly before the case is closed.

### C. Line-by-Line Explanation

**Line 4: `class PlatformOutput(BaseModel):`**
*   **The Shipping Box:** This defines the final shape of the answer. It includes the ID (tracking number), the Status (Did it work?), and the Message.

**Line 13: `class ActionExecutor:`**
*   **The Packaging Station:** The place where the final box is assembled.

**Line 19: `def execute(self, request_id, plan_results):`**
*   **Input:** Receives the tracking ID and the notes from the robots.
*   **Output:** A perfectly packaged `PlatformOutput` box.

**Lines 21-26: Filling the Box**
*   **What it does:** It sets the status to **ACTION_COMPLETE** and writes a simple summary: "Investigation complete."

---

### 🏁 Friendly Recap (The Packaging Station)

You've just learned how to **Finish a Job**!

You now understand:
1.  Why we use a **Standard Output Box** (PlatformOutput) for every mission.
2.  The role of the **Executor** in providing the final sign-off.

### 7.3 mock_db.py – The Warehouse Storage

Our factory needs a place to store all the information about our customers. In a real bank, this would be a massive, complex database. In our learning factory, we use **`mock_db.py`**. Think of this as our **Warehouse Storage**. It’s a simple collection of "Folders" (dictionaries) where we keep all the account secrets.

### A. Full File Ingestion: `tools/mock_db.py`

```python
1: # tools/mock_db.py
2: import datetime
3: 
4: # A simple in-memory dictionary acting as our simulated Core Banking System / CRM
5: DB = {
6:     "accounts": {
7:         "acc_123": {
8:             "status": "ACTIVE",
9:             "balance": 5000.00,
10:             "owner": "John Doe",
11:             "type": "Personal",
12:         },
...
31:         "acc_vip": {
32:             "status": "ACTIVE",
33:             "balance": 950000.00,
34:             "owner": "Alice Rich",
35:             "type": "Centurion",
36:         },
...
97:     },
98:     "escalation_tickets": [],
99: }
100: 
101: 
102: def get_account(account_id: str) -> dict:
103:     return DB["accounts"].get(account_id.lower())
104: 
105: 
106: def update_account_status(account_id: str, new_status: str) -> bool:
107:     if account_id in DB["accounts"]:
108:         DB["accounts"][account_id]["status"] = new_status
109:         return True
110:     return False
```

*(Note: We are showing representative parts of the warehouse. The full file includes many more accounts.)*

### B. File Purpose
The `mock_db.py` file is our **Simulated Reality**. It holds the data that our robots will read (via the Lookup tools) and change (via the Freeze tools). If a customer's status is updated here, the whole factory sees it instantly.

### C. Line-by-Line Explanation

**Line 5: `DB = {`**
*   **The Warehouse Building:** This dictionary is the physical building where all data is stored.

**Lines 7-12: An Individual Folder**
*   **The Account:** Every customer has a unique ID (like `acc_123`).
*   **The Contents:** Inside the folder, we store their current **Status** (Active/Frozen), their **Balance**, and their **Type** (Personal/Corporate).

**Line 35: `type: "Centurion"`**
*   **The VIP Label:** This is the key piece of data that our "Tier-Aware" robots (from Chapter 6) are looking for!

**Line 102: `def get_account(account_id):`**
*   **The Retrieval Claw:** This function works like a robot claw that goes into the warehouse and pulls out a specific customer's folder.

**Line 106: `def update_account_status(account_id, new_status):`**
*   **The Status Stamper:** This tool allows us to stamp a new status (like "FROZEN") onto a customer's folder.

---

### 🏁 Friendly Recap (The Warehouse)

You've just learned how to **Store and Retrieve Data**!

You now understand:
1.  How a **Python Dictionary** can act as a simple "Warehouse" (Database).
2.  The importance of **Account Types** (like Centurion) for our AI logic.
3.  How we use **Getter** and **Setter** functions to safely touch the data.

### 7.4 The Robot Toolbox (`tools/`)

The robots can't reach into the Warehouse directly. Instead, they use **Power Tools**. These tools are like the "Input/Output" devices of our factory. We’ll look at three of the most important ones.

---

### 📦 account_lookup_tool.py – The Scanner

This tool allow a robot to "Scan" a customer's folder to see their balance and status.

### A. Full File Ingestion: `tools/account_lookup_tool.py`

```python
9: @tool("account_lookup_tool")
10: def account_lookup_tool(account_id: str):
11:     """Retrieves account details (status, balance, type) from the core banking system."""
12:     # Handle case-insensitive lookups
13:     account = get_account(account_id.lower())
...
23:     return json.dumps({"success": True, "data": account})
```

**Line 9: `@tool("account_lookup_tool")`**
*   **The Connection:** This special "decorator" tells the CrewAI robot squad that this is a tool they are allowed to use.

---

### 📦 fraud_detection_tool.py – The Action Button

This is a "Wrapper" tool. It doesn't do the work itself; instead, it provides a simple button for the robots to push, which then triggers the deeper logic in the factory.

### A. Full File Ingestion: `tools/fraud_detection_tool.py`

```python
14: @tool("freeze_account_tool")
15: def freeze_account_tool(account_id: str):
16:     """Freezes a financial account due to suspected fraud."""
17:     return json.dumps(_freeze(account_id))
```

**Line 17: `return json.dumps(_freeze(account_id))`**
*   **The Button:** When the Fraud Robot "pushes" this button, it calls the `_freeze` function (the actual logic) and returns the result in JSON format (computer-speak).

---

### 📦 audit_logger.py – The Factory Record

Every time the Conductors or Robots make a move, we need to write it down for the bank's owners to see later. The `audit_logger.py` is the **Factory Record Book**.

### A. Full File Ingestion: `tools/audit_logger.py`

```python
34: def log_audit(transaction: dict, score: int, decision: str, investigation: str):
...
47:     audit_record = {
48:         "timestamp": datetime.datetime.utcnow().isoformat(),
49:         "account_id": transaction.get("account_id"),
...
52:         "compliance_score": score,
53:         "decision": decision,
54:         "ai_investigation": investigation_data,
55:     }
56: 
57:     with open(LOG_FILE, "a") as f:
58:         f.write(json.dumps(audit_record) + "\n")
```

### C. Line-by-Line Explanation

**Line 34: `def log_audit(...)`**
*   **The Stenographer:** This function takes the final verdict, the risk score, and the robot's notes.

**Lines 47-55: Creating the Entry**
*   **What it represents:** Filling out a single row in the master record book. It includes the Time, the Account, and the **AI Investigation** (the robots' full reasoning).

**Line 58: `f.write(json.dumps(audit_record) + "\n")`**
*   **The Permanent Ink:** This line physically writes the record into the `audit_log.jsonl` file. The `"a"` (append) mode ensures that we never delete old records—we only add new ones!

---

### 🏁 Friendly Recap (Chapter 7 Completed!)

Give yourself a high-five! You've just mastered the **Real-World Actions** of our factory.

In this chapter, you learned:
1.  How the **Main Assembly Line** (TransactionService) coordinates security and AI.
2.  How the **Warehouse** (mock_db) keeps all our secrets safe.
3.  How **Power Tools** allow AI robots to interact with simulated databases.
4.  Why **Audit Logs** are crucial for ensuring every decision can be explained.

**The robots have their tools and they’ve finished their work. But what if we made a mistake? What if we need to double-check their logic? In the next chapter, we're heading to the "Safety Inspectors" room—the `app/review/` layer!**
