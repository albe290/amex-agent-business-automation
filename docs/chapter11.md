# Chapter 11: The Control Room (The Base Layer)

## 1️⃣ Big Picture: The Control Room

We’ve explored every wing of our AI Factory: the Security Gateway, the Research Library, the Robot Squad, the Safety Rails, and the Performance Lab. Now, we need to visit the **Control Room**.

This is the main computer console where we actually "Turn On" the factory. It’s where we feed the factory its very first instruction (the "Transaction Request") and where we watch the final results come out.

In this chapter, we’ll meet the master switches:
1.  **The Manual Start Switch (`main.py`)**: A simple command-line tool that runs one transaction through the entire system so we can see it work.
2.  **The Automated Receptionist (`app/api/server.py`)**: A professional API that listens for thousands of requests from the outside world and manages the real-time Dashboard.
3.  **The Factory Blueprint (`docker-compose.yml`)**: A master plan that tells the computers how to set up the API, the robots, and the dashboard all at once.
4.  **The Factory Settings (`.env.example`)**: The "secret" list of passwords and keys (like your OpenAI API Key) that the factory needs to run.

---

## 2️⃣ Teach the Code

### 11.1 main.py – The Manual Start Switch

If you want to test the factory manually, you use the `main.py` file. It’s the simplest way to see the "Big Picture" in action.

### A. Full File Ingestion: `main.py`

```python
10: def main():
11:     print("\n" + "=" * 50)
12:     print("      BLUESHIELD SECURE FINANCIAL AGENT (CrewAI)")
13:     print("=" * 50 + "\n")
14: 
15:     # 1. Initialize Security Validator
16:     validator = SecurityValidator()
20:     transaction_case = {
21:         "account_id": "acc_vip",
22:         "merchant_id": "M_999",  # Risky merchant
23:         "amount": 1500.0,
24:         "actor": "employee",
25:     }
26: 
27:     user_prompt = f"Investigate transaction for account {transaction_case['account_id']} at merchant {transaction_case['merchant_id']} for ${transaction_case['amount']}."
28: 
29:     # 2. Sentinel Prompt Validation
30:     is_safe, msg = validator.validate_prompt(user_prompt)
31:     if not is_safe:
32:         print(f"\n[CRITICAL] System Blocked Execution: {msg}")
33:         sys.exit(1)
34: 
35:     # 3. CrewAI Orchestration
40:     crew_engine = FinancialCrew(transaction_case)
41:     result = crew_engine.run()
...
51:     is_output_safe, output_msg = validator.validate_output(str(result))
...
56:     log_execution_metrics(latency=latency, success=is_output_safe)
```

### B. File Purpose
The `main.py` file script is a **Demo Entry Point**. It hard-codes a single transaction (Line 20) and then pushes it through the three main steps of our platform:
1.  **Safety First**: Validate the prompt.
2.  **Robot Work**: Run the Financial Crew.
3.  **Safety Last**: Validate the final report.

### C. Line-by-Line Explanation

**Line 16: `validator = SecurityValidator()`**
*   **The Guard:** Before anything happens, we hire the **Security Guard** we met in Chapter 4.

**Line 20: `transaction_case = { ... }`**
*   **The Input:** We create a "Fake" transaction. This one looks slightly risky because of the "M_999" merchant ID.

**Line 30: `is_safe, msg = validator.validate_prompt(user_prompt)`**
*   **The First Check:** We ask the guard if our request is safe. If there’s a "PROMPT_INJECTION" hidden in the note, the factory stops here!

**Line 40: `crew_engine = FinancialCrew(...)`**
*   **The Kick-Off:** We wake up the **Robot Squad** and tell them to get to work.

**Line 51: `validator.validate_output(...)`**
*   **The Final Check:** Once the robots finish their report, the guard checks it one last time to make sure no secrets were leaked.

---

### 11.2 server.py – The Automated Receptionist

In a real bank, we don't run `main.py` manually. Instead, we use a **Web Server**. The `app/api/server.py` file is a professional receptionist that stays awake 24/7, waiting for requests from other computers.

### A. Full File Ingestion: `app/api/server.py`

```python
13: app = FastAPI(title="BlueShield Secure Financial Agent API")
14: 
18: app.add_middleware(
19:     CORSMiddleware,
...
24: )
...
37: @app.websocket("/ws")
38: async def websocket_endpoint(websocket: WebSocket):
39:     await websocket.accept()
...
50:     event_bus.subscribe(send_event)
...
60: @app.post("/process_transaction")
61: async def process_transaction(req: TransactionRequest):
62:     return await transaction_service.process(req)
```

### B. File Purpose
The `server.py` file turns our factory into a **Public Service**. 
*   It provides a "Doorway" (`/process_transaction`) where other apps can send data.
*   It provides a "Window" (`/ws`) where our Dashboard can watch the robots working in real-time.

### C. Line-by-Line Explanation

**Line 13: `app = FastAPI(...)`**
*   **The Framework:** We use "FastAPI," which is like a high-speed telecommunications system for Python.

**Line 37: `@app.websocket("/ws")`**
*   **The Live Wire:** This creates a special "Always-On" connection. Our dashboard uses this wire to show you little green and red lights as the robots finish their tasks.

**Line 60: `@app.post("/process_transaction")`**
*   **The Main Door:** This is where the bank sends its data. When a transaction hits this door, the server immediately calls the `transaction_service` to start the assembly line.

---

### 🏁 Friendly Recap (The Control Room)

You've just learned how to **Start the Factory**!

You now understand:
1.  How **`main.py`** is used for quick manual tests.
2.  How **`server.py`** allows external apps and dashboards to talk to our robots.
3.  Why the **Control Room** is the final piece of the puzzle that connects everything else.

### 11.3 docker-compose.yml – The Factory Blueprint

In a real production environment, you don't want to start the API, the database, and the dashboard one by one. The `docker-compose.yml` file is the **Factory Blueprint**. It tells the computer exactly how to "Construct" the entire factory in one go.

### A. Full File Ingestion: `docker-compose.yml`

```yaml
6: services:
7: 
8:   # ─────────────────────────────────────────────────────────────
9:   # API Service: FastAPI — handles intake, control plane, telemetry
10:   # ─────────────────────────────────────────────────────────────
11:   api:
12:     build:
13:       context: .
14:       dockerfile: infra/docker/api.Dockerfile
15:     container_name: amex-platform-api
16:     ports:
17:       - "8000:8000"
...
36:   # ─────────────────────────────────────────────────────────────
37:   # Worker Service: Async event consumer — governed pipeline
38:   # ─────────────────────────────────────────────────────────────
39:   worker:
40:     build:
41:       context: .
42:       dockerfile: infra/docker/worker.Dockerfile
...
58:   # ─────────────────────────────────────────────────────────────
59:   # Dashboard Service: React observability console
60:   # ─────────────────────────────────────────────────────────────
61:   dashboard:
62:     build:
...
64:     ports:
65:       - "3000:80"
```

### B. File Purpose
This file manages **Containerization**. It ensures that "it works on my machine" also means "it works on your machine" by packaging the code into isolated boxes (containers).
*   **API**: The doorway for data.
*   **Worker**: The engine where the robots actually live.
*   **Dashboard**: The glass window for humans.

### C. Line-by-Line Explanation

**Lines 11-17: The API Tower**
*   **Meaning:** We build the API container and open port `8000` so we can talk to it.

**Lines 36-40: The Robot Workshop (Worker)**
*   **Meaning:** This container doesn't have a port because it doesn't talk to the outside world. Instead, it just pulls work from internal queues and executes robot missions.

**Lines 58-65: The Viewing Deck (Dashboard)**
*   **Meaning:** This container serves the React website on port `3000`. This is where you go to see the "Live View" of your factory.

---

### 11.4 .env.example – The Factory Settings

Every factory needs electricity (API Keys) and specific settings (Modes). The `.env.example` file is the **Factory Settings** template.

### A. File Purpose
Before the factory can run, you must copy this file to a new file named `.env` and fill in your private details.
*   **`OPENAI_API_KEY`**: The "Fuel" for your robots' brains.
*   **`STORAGE_MODE`**: Tells the factory if it should save data in a real database or just in temporary memory.

---

### 🏁 Friendly Recap (Chapter 11 Completed!)

Congratulations! You've just mastered the **Control Room**!

In this chapter, you learned:
1.  How **`main.py`** provides a manual CLI interface.
2.  How **`server.py`** provides an automated API interface.
3.  How **`docker-compose.yml`** orchestrates all the factory's wings into one unified building.
4.  Why **`.env`** is the "Secret Key" that brings the AI to life.

**The factory is powered on and running. But how do we *watch* it work? How do we measure the heart rate and health of our robots? In the next chapter, we're heading to the "Observation Deck"—the `monitoring/` layer—next!**
