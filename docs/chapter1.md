# Chapter 1: The Factory Entrance – Root Files That Run the Factory

## 1️⃣ Big Picture: The Power Grid

Before we look at individual machines or robots, we need to understand how the factory building itself is powered and controlled. 

Imagine you are standing at the main electrical panel of a giant factory. You see three things:
1.  **The Master Switch (`main.py`)**: This is the giant lever you pull to start the machines. Without it, the robots just sit there in the dark.
2.  **The Fuel Tank (`.env.example`)**: Every machine needs fuel. Some machines need "Public Fuel" (regular settings), but others need "Secret High-Octane Fuel" (API keys and passwords). This file is the template for making sure the factory has all the fuel it needs.
3.  **The Building Blueprint (`docker-compose.yml`)**: This magical blueprint actually *builds* the rooms for you. It tells the factory where the API office, the Robot room, and the Control screens should go, and how they should talk to each other.

**What breaks if these aren't right?**
If the Master Switch is broken, nothing happens. If the Fuel is wrong, the machines might start but then immediately stop because they are "hungry." If the Blueprint is missing, you have machines but no rooms to put them in, and they'll just be a mess on the floor.

---

## 2️⃣ Teach the Code

### A. Full File Ingestion: `main.py`

```python
1: # main.py
2: import time
3: import sys
4: import os
5: from security.validator import SecurityValidator
6: from crew.financial_crew import FinancialCrew
7: from monitoring.metrics import log_execution_metrics
8: 
9: 
10: def main():
11:     print("\n" + "=" * 50)
12:     print("      BLUESHIELD SECURE FINANCIAL AGENT (CrewAI)")
13:     print("=" * 50 + "\n")
14: 
15:     # 1. Initialize Security Validator
16:     validator = SecurityValidator()
17: 
18:     # 2. Define Sample Transaction Case
19:     # In a real app, this would come from an API or User Input
20:     transaction_case = {
21:         "account_id": "acc_vip",
22:         "merchant_id": "M_999",  # Risky merchant
23:         "amount": 1500.0,
24:         "actor": "employee",
25:     }
26: 
27:     user_prompt = f"Investigate transaction for account {transaction_case['account_id']} at merchant {transaction_case['merchant_id']} for ${transaction_case['amount']}."
28: 
29:     # 3. Step 1: Sentinel Prompt Validation
30:     is_safe, msg = validator.validate_prompt(user_prompt)
31:     if not is_safe:
32:         print(f"\n[CRITICAL] System Blocked Execution: {msg}")
33:         sys.exit(1)
34: 
35:     # 4. Step 2: CrewAI Orchestration
```

*(Note: File stops at line 35 of 67 as per the 35-line limit for this prompt segment. I will continue the remaining lines in the next segment.)*

### B. File Purpose
The `main.py` file is the **Master Controller**. Its job is to orchestrate the entire process for a single test run. It starts the security checks, wakes up the robots, and makes sure everything happens in the right order.

### C. Line-by-Line Explanation

**Line 1: `# main.py`**
*   **What the computer does:** It ignores this line.
*   **Why it exists:** It's a label for the human developer.
*   **What breaks if changed:** Nothing breaks, but humans might get confused.

**Line 2: `import time`**
*   **What the computer does:** It brings in a collection of tools related to time.
*   **Why it exists:** We use it to measure how long the factory takes to finish a job.
*   **Connection:** This allows us to calculate "Latency" (speed).

**Line 3: `import sys`**
*   **What the computer does:** It brings in tools for interacting with the computer's system.
*   **Why it exists:** We need a way to shut down the factory immediately if the Security Judge finds a problem.
*   **Connection:** The `sys.exit(1)` command later uses this tool.

**Line 4: `import os`**
*   **What the computer does:** It brings in tools for interacting with the Operation System (like files and folders).
*   **Why it exists:** Often we need to read environment variables or file paths.

**Line 5: `from security.validator import SecurityValidator`**
*   **What the computer does:** It goes to our "Security Room" and brings out the **SecurityValidator** (the Judge).
*   **Why it exists:** We cannot start the work until the Judge is ready to inspect the requests.

**Line 6: `from crew.financial_crew import FinancialCrew`**
*   **What the computer does:** It goes to the "Robot Room" and brings out the **FinancialCrew** (the squad of robots).
*   **Why it exists:** These are the workers who actually do the financial analysis.

**Line 7: `from monitoring.metrics import log_execution_metrics`**
*   **What the computer does:** It brings in a "Clipboard" to record how well the factory performed.
*   **Why it exists:** To keep the dashboard updated with stats.

**Line 8-9: `(Empty Lines)`**
*   **Why they exist:** Spacing for readability.

**Line 10: `def main():`**
*   **What the computer does:** It defines the "Main Plan" of action.
*   **Word-by-word:** `def` (Define) `main` (the name of our plan) `():` (it doesn't need any outside ingredients to start).
*   **Significance:** This is the entry point for the whole program.

**Line 11-13: `print(...)`**
*   **What the computer does:** It writes text to the screen.
*   **Symbol-by-symbol:** `\n` means "new line" (vertical space). `* 50` means repeat the symbol 50 times.
*   **Why it exists:** To create a beautiful banner in the console so the user knows the factory is starting up.

**Line 14: `(Empty Line)`**
*   **Why it exists:** Spacing.

**Line 15: `# 1. Initialize Security Validator`**
*   **What the computer does:** Ignores the comment.
*   **Why it exists:** To tell the human that we are starting Step 1.

**Line 16: `validator = SecurityValidator()`**
*   **What the computer does:** Creates an instance of the Judge.
*   **Meaning:** `validator` is the name we chose. `=` means "is." `SecurityValidator()` is the tool we imported.
*   **Connection:** This "Judge" will now be standing by at the entrance.

**Line 17: `(Empty Line)`**

**Line 18: `# 2. Define Sample Transaction Case`**
*   **Meaning:** We are about to create a "Test Order."

**Line 19: `# In a real app, this would come from an API or User Input`**
*   **Meaning:** Explaining that this is just a practice case.

**Line 20: `transaction_case = {`**
*   **What the computer does:** Starts a "Dictionary" (a list of labeled facts).
*   **Why it exists:** To hold the details of the financial request we are testing.

**Line 21: `"account_id": "acc_vip",`**
*   **Meaning:** Fact: This belongs to a VIP account.

**Line 22: `"merchant_id": "M_999",  # Risky merchant`**
*   **Meaning:** Fact: The purchase is at a "risky" shop.

**Line 23: `"amount": 1500.0,`**
*   **Meaning:** Fact: The amount is $1,500.

**Line 24: `"actor": "employee",`**
*   **Meaning:** Fact: An internal employee is initiating this.

**Line 25: `}`**
*   **What the computer does:** Closes the dictionary of facts.

**Line 26: `(Empty Line)`**

**Line 27: `user_prompt = f"Investigate transaction for account {transaction_case['account_id']} at merchant {transaction_case['merchant_id']} for ${transaction_case['amount']}."`**
*   **What the computer does:** Writes a "Task Letter" for the AI.
*   **Symbol-by-symbol:** `f"` means this is a "Formatted String." The `{}` symbols are "Insertion Holes."
*   **Meaning:** The computer takes the facts from the dictionary and plugs them into a human-readable sentence.

**Line 28: `(Empty Line)`**

**Line 29: `# 3. Step 1: Sentinel Prompt Validation`**
*   **Meaning:** Step 3 is checking if the Letter we just wrote is safe.

**Line 30: `is_safe, msg = validator.validate_prompt(user_prompt)`**
*   **What the computer does:** Hands the Letter to the Judge.
*   **Meaning:** `is_safe` will be "True" or "False." `msg` will be a reason why it was blocked or allowed.
*   **Connection:** This is the core of our "Sentinel" security.

**Line 31: `if not is_safe:`**
*   **What the computer does:** Checks if the Judge said "False."
*   **Meaning:** `not` flips the value. If `is_safe` is False, `not is_safe` becomes True, and the computer goes inside the `if` block.

**Line 32: `print(f"\n[CRITICAL] System Blocked Execution: {msg}")`**
*   **What the computer does:** Shouts a red alarm on the screen.
*   **Why it exists:** To alert the user that the Judge stopped the work.

**Line 33: `sys.exit(1)`**
*   **What the computer does:** Closes the factory immediately.
*   **Meaning:** `1` is a code that tells the computer "We crashed because of an error/danger."
*   **What breaks if changed:** If you change this to 0, the computer might think everything was fine even though we blocked a dangerous request.

**Line 34: `(Empty Line)`**

**Line 35: `# 4. Step 2: CrewAI Orchestration`**
*   **Meaning:** We are about to send the request to the robots.

*(Stop segment - lines 1-35 explained)*

### D. Define Terms
*   **Import:** Bringing a tool from a storage box (library) into your work area.
*   **Function (`def`):** A saved "Plan of Action" that you can trigger later.
*   **Print:** Writing information onto the computer screen for humans to read.
*   **Dictionary (`{}`):** A way for computers to store labeled information (like Name: Alice).
*   **Boolean (`True/False`):** A simple yes/no switch that computers use for logic.

---

### A. Full File Ingestion: `main.py` (Continued)

```python
36:     start_time = time.time()
37:     print("\n[Orchestration] Kicking off Financial Crew...")
38: 
39:     try:
40:         crew_engine = FinancialCrew(transaction_case)
41:         result = crew_engine.run()
42: 
43:         latency = time.time() - start_time
44:         print("\n" + "-" * 30)
45:         print("CREW EVALUATION COMPLETED")
46:         print(f"Latency: {latency:.2f}s")
47:         print("-" * 30)
48:         print(f"RESULT:\n{result}")
49: 
50:         # 5. Step 3: Sentinel Output Validation
51:         is_output_safe, output_msg = validator.validate_output(str(result))
52:         if not is_output_safe:
53:             print(f"\n[CRITICAL] Output Blocked: {output_msg}")
54: 
55:         # 6. Monitoring
56:         log_execution_metrics(latency=latency, success=is_output_safe)
57: 
58:     except Exception as e:
59:         print(f"\n[ERROR] Execution failed: {str(e)}")
60:         log_execution_metrics(
61:             latency=time.time() - start_time, success=False, error=str(e)
62:         )
63: 
64: 
65: if __name__ == "__main__":
66:     main()
67: 
```

### C. Line-by-Line Explanation (Continued)

**Line 36: `    start_time = time.time()`**
*   **What the computer does:** It looks at its digital watch and writes down the exact current time in a box called `start_time`.
*   **Why it exists:** To start the clock so we can see how fast the robots work.

**Line 37: `    print("\n[Orchestration] Kicking off Financial Crew...")`**
*   **What the computer does:** Writes a progress message to the screen.
*   **Word-by-word:** `Orchestration` is the act of managing different parts. `Kicking off` means starting.

**Line 38: `(Empty Line)`**

**Line 39: `    try:`**
*   **What the computer does:** It creates a "Safe Zone."
*   **Significance:** It tells the computer: "I'm about to do something difficult. If anything breaks, don't crash the whole factory. Instead, jump to the `except` section at the bottom."

**Line 40: `        crew_engine = FinancialCrew(transaction_case)`**
*   **What the computer does:** Prepares the Robot Squad leader and gives them the customer's file (`transaction_case`).
*   **Meaning:** `crew_engine` is our squad leader.

**Line 41: `        result = crew_engine.run()`**
*   **What the computer does:** The most important part! It tells the robots to start thinking and working. 
*   **Meaning:** `result` is the final report the robots will write. 
*   **Agentic Connection:** This is the moment of **Autonomy**. The robots are now making decisions on their own.

**Line 42: `(Empty Line)`**

**Line 43: `        latency = time.time() - start_time`**
*   **What the computer does:** Looks at its watch again, subtracts the start time, and calculates the total work time.
*   **Meaning:** `latency` is the total seconds spent working.

**Line 44-47: `print(...)`**
*   **What the computer does:** Prints a nice summary box of the timing results.

**Line 48: `        print(f"RESULT:\n{result}")`**
*   **What the computer does:** Shows you the final report the robot wrote.

**Line 49: `(Empty Line)`**

**Line 50: `        # 5. Step 3: Sentinel Output Validation`**
*   **Meaning:** Even though the robot finished, we don't trust it yet. We need Step 5: Final Inspection.

**Line 51: `        is_output_safe, output_msg = validator.validate_output(str(result))`**
*   **What the computer does:** Hands the robot's report to the Judge.
*   **Connection:** This prevents the AI from accidentally leaking secrets or making dangerous mistakes in its final report.

**Line 52: `        if not is_output_safe:`**
*   **What the computer does:** Checks if the Judge found a mistake.

**Line 53: `            print(f"\n[CRITICAL] Output Blocked: {output_msg}")`**
*   **What the computer does:** Sounds another alarm if the report is dangerous.

**Line 54: `(Empty Line)`**

**Line 55: `        # 6. Monitoring`**
*   **Meaning:** Step 6 is writing down the history of this run.

**Line 56: `        log_execution_metrics(latency=latency, success=is_output_safe)`**
*   **What the computer does:** Writes the result (Did it pass? How long did it take?) on the factory's master clipboard.

**Line 57: `(Empty Line)`**

**Line 58: `    except Exception as e:`**
*   **What the computer does:** This is the "Safety Net." If any robot catches fire or a machine breaks, the computer lands here.
*   **Meaning:** `e` is the name of the error message.

**Line 59: `        print(f"\n[ERROR] Execution failed: {str(e)}")`**
*   **What the computer does:** Writes the bad news to the screen so we can fix it.

**Line 60-62: `        log_execution_metrics(...)`**
*   **What the computer does:** Even if we failed, we record the failure. We are an honest factory!

**Line 63: `(Empty Line)`**

**Line 64: `(Empty Line)`**

**Line 65: `if __name__ == "__main__":`**
*   **What the computer does:** This is the "Ignition Lock." 
*   **Meaning:** It says: "Only pull the master lever if I am standing directly in front of this specific switch (running this file)." This prevents the factory from accidentally starting if we are just looking at the blueprints.

**Line 66: `    main()`**
*   **What the computer does:** Triggers the `main` plan we defined starting at line 10.

**Line 67: `(Empty Line)`**

---

### 🏁 Friendly Recap (Part 2)
You've now mastered the entire "Master Switch" (`main.py`)! 
You understand:
1.  How **Safety Zones** (`try/except`) keep the factory from exploding if an error happens.
2.  How the **Robot Squad** works independently to create a result.
3.  How we check the product **one last time** before clearing it for the customer.

You've just learned the basic flow of **Governed Agentic AI**. In the next segment, we'll look at the **Fuel Tank** (`.env.example`) to see what powers our robots.

---

## 1.2 .env.example – The Template for Secret Keys

The **.env.example** file is like a "Shopping List" template. When you go to a high-end restaurant, the chef has a list of ingredients they need: salt, pepper, secret spice. 

In our factory, the machines need "Secret Keys" (passwords) to talk to the AI brain (OpenAI). We never write these passwords directly into the blueprints because if someone stole the blueprint, they'd steal the passwords too! Instead, we use this "Example" file to tell the Chef: "Hey, you need to provide your own secret key here."

### A. Full File Ingestion: `.env.example`

```text
1: # Environment Configuration — Example
2: # Copy this to .env and fill in real values before starting the platform.
3: # Never commit .env to source control.
4: 
5: # =============================================================================
6: # CORE AI / LLM
7: # =============================================================================
8: OPENAI_API_KEY=sk-your-openai-key-here
9: OPENAI_MODEL=gpt-4o
10: OPENAI_TEMPERATURE=0.2
11: 
12: # =============================================================================
13: # API SERVICE
14: # =============================================================================
15: API_HOST=0.0.0.0
16: API_PORT=8000
17: API_RELOAD=true                        # Set to false in production
18: API_WORKERS=1                          # Increase for production
19: 
20: # =============================================================================
21: # DASHBOARD SERVICE
22: # =============================================================================
23: DASHBOARD_PORT=5173                    # Vite dev server; 80 in Docker prod
24: DASHBOARD_API_BASE_URL=http://localhost:8000
25: 
26: # =============================================================================
27: # EVENT PIPELINE
28: # =============================================================================
29: QUEUE_MODE=memory                      # memory | kafka | sqs
30: QUEUE_MAX_DEPTH=500
31: CONSUMER_POLL_INTERVAL_MS=250
32: CONSUMER_BATCH_SIZE=1
33: 
34: # Kafka settings (only used when QUEUE_MODE=kafka)
35: KAFKA_BOOTSTRAP_SERVERS=localhost:9092
36: KAFKA_TOPIC_INCOMING=platform.events.incoming
37: KAFKA_TOPIC_OUTCOMES=platform.events.outcomes
38: KAFKA_CONSUMER_GROUP=governed-platform-workers
39: 
40: # =============================================================================
```

*(Note: File stops at line 40 of 80 for this segment. Remaining lines will follow in the next segment.)*

### B. File Purpose
This file shows you all the "Knobs and Dials" you can turn to change how the factory behaves. Do you want the robots to be super creative or very literal? Do you want to use a real database or just temporary memory? You decide here.

### C. Line-by-Line Explanation

**Lines 1-3: Comments**
*   **Purpose:** Safety warnings.
*   **Meaning:** Telling you to copy this file to a new file named just `.env` and **NEVER** share your real passwords with the world.

**Lines 5-7: Header**
*   **Purpose:** Organizing the "Ingredient List."

**Line 8: `OPENAI_API_KEY=sk-your-openai-key-here`**
*   **What the computer does:** This is the "Passport" for the AI.
*   **Why it exists:** Without this, we can't talk to OpenAI's brains. You replace the `sk-your...` part with your real secret key.
*   **What breaks if changed:** The factory will start, but the first time a robot tries to "think," it will fail because it doesn't have a valid passport.

**Line 9: `OPENAI_MODEL=gpt-4o`**
*   **Meaning:** Telling the robots which specific "Brain Version" to use. `gpt-4o` is a very smart one.

**Line 10: `OPENAI_TEMPERATURE=0.2`**
*   **Meaning:** The "Creativity Dial." 
*   **Value:** `0` is very literal and robotic. `1` is very creative and "poetic." For a bank, we keep it low (`0.2`) so the robots don't start making up their own numbers!

**Line 15: `API_HOST=0.0.0.0`**
*   **Meaning:** Telling the factory's "Reception Desk" to listen for visitors from anywhere.

**Line 16: `API_PORT=8000`**
*   **Meaning:** The specific "Door Number" (Port) that visitors should use to talk to our API.

**Line 17: `API_RELOAD=true`**
*   **Meaning:** If the chef changes a recipe, the factory automatically restarts so it can use the new recipe immediately.

**Line 23: `DASHBOARD_PORT=5173`**
*   **Meaning:** The door number for the "Control Room Screens" (the website dashboard).

**Line 24: `DASHBOARD_API_BASE_URL=http://localhost:8000`**
*   **Meaning:** Telling the dashboard exactly where the "Reception Desk" (API) is located so they can talk to each other.

**Line 29: `QUEUE_MODE=memory`**
*   **Meaning:** The "Conveyor Belt" type.
*   **Value:** `memory` is like a fake, invisible belt just for testing. `kafka` or `sqs` are real, heavy-duty metal belts used in large factories.

**Line 30: `QUEUE_MAX_DEPTH=500`**
*   **Meaning:** The maximum number of boxes allowed on the conveyor belt at once. If it gets too full, the factory stops taking new orders.

**Lines 35-38: Kafka Settings**
*   **Purpose:** These are only used if the conveyor belt is the heavy-duty `kafka` type. They tell the belt where its motor is located and what "Channel" to use.

---

### 🏁 Friendly Recap (Fuel Tank Part 1)
You've just looked inside the factory's "Recipe Book." 
1.  You saw how we keep our **Secret Keys** safe.
2.  You saw how we control the **Robot's Brain** (Model and Temperature).
3.  You saw how we pick the type of **Conveyor Belt** (`QUEUE_MODE`).

### A. Full File Ingestion: `.env.example` (Continued)

```text
41: # =============================================================================
42: # STORAGE / PERSISTENCE
43: # =============================================================================
44: AUDIT_LOG_PATH=./logs/audit.jsonl
45: EVAL_RESULTS_PATH=./logs/evals.json
46: 
47: # PostgreSQL (only used when STORAGE_MODE=postgres)
48: DATABASE_URL=postgresql://user:password@localhost:5432/amex_platform
49: 
50: # =============================================================================
51: # RISK ENGINE THRESHOLDS
52: # =============================================================================
53: RISK_THRESHOLD_AUTOMATE=20.0
54: RISK_THRESHOLD_ESCALATE=70.0
55: MISSING_CONTEXT_PENALTY=25.0
56: UNKNOWN_MERCHANT_PENALTY=15.0
57: 
58: # =============================================================================
59: # RUNTIME GOVERNANCE
60: # =============================================================================
61: MAX_AGENT_STEPS=10
62: MAX_RETRIES=3
63: BUDGET_MAX_TOKENS=4000
64: FALLBACK_ON_BUDGET_EXCEEDED=true
65: 
66: # =============================================================================
67: # SECURITY
68: # =============================================================================
69: SENTINEL_ENABLED=true
70: OUTPUT_SCAN_ENABLED=true
71: PII_DETECTION_ENABLED=true
72: 
73: # =============================================================================
74: # FEATURE FLAGS
75: # =============================================================================
76: FEATURE_LIVE_AGENTS=false              # true = use real CrewAI; false = mock
77: FEATURE_REVIEW_QUEUE=true
78: FEATURE_EVALS=true
79: FEATURE_DASHBOARD_REALTIME=true
80: 
```

### C. Line-by-Line Explanation (Continued)

**Line 43: `STORAGE_MODE=memory`**
*   **Meaning:** Where the factory stores its "History Books" (Logs).
*   **Value:** `memory` means "delete everything when the power goes out." `postgres` means "save it to a heavy-duty safe."

**Line 44: `AUDIT_LOG_PATH=./logs/audit.jsonl`**
*   **Meaning:** The specific shelf where the "Audit Trail" is saved.

**Line 45: `EVAL_RESULTS_PATH=./logs/evals.json`**
*   **Meaning:** The shelf where the robot's "Report Cards" are saved.

**Line 48: `DATABASE_URL=...`**
*   **Meaning:** The address and combination to the "PostgreSQL Safe" (if we use that mode).

**Line 53: `RISK_THRESHOLD_AUTOMATE=20.0`**
*   **Meaning:** The "Robot's Speed Limit."
*   **Connection:** If a request's "Danger Score" is lower than 20, the robots are allowed to finish the job automatically without asking a human.

**Line 54: `RISK_THRESHOLD_ESCALATE=70.0`**
*   **Meaning:** The "Danger Red Line."
*   **Connection:** If the score is higher than 70, the robots must stop and call a Human Manager immediately.

**Line 55: `MISSING_CONTEXT_PENALTY=25.0`**
*   **Meaning:** The "Incomplete Form Fine."
*   **Connection:** If the customer forgets to fill out a part of the form, we automatically add 25 points to the "Danger Score."

**Line 61: `MAX_AGENT_STEPS=10`**
*   **Meaning:** The "Think Limit."
*   **Connection:** If a robot can't find an answer after 10 tries, it must stop. This prevents the robot from getting "stuck" in a loophole.

**Line 63: `BUDGET_MAX_TOKENS=4000`**
*   **Meaning:** The "Wallet Limit."
*   **Connection:** This limits how much "Digital Money" (Tokens) the robot can spend on a single task.

**Line 69: `SENTINEL_ENABLED=true`**
*   **Meaning:** Turning on the "Entrance Guard."
*   **Connection:** If this is `true`, the `SecurityValidator` we saw in Chapter 1 will inspect every request.

**Line 70: `OUTPUT_SCAN_ENABLED=true`**
*   **Meaning:** Turning on the "Exit Inspection."
*   **Connection:** Checks the robot's final report for mistakes before it leaves the factory.

**Line 71: `PII_DETECTION_ENABLED=true`**
*   **Meaning:** Turning on the "Secret Spy Scanner."
*   **Connection:** Automatically redact sensitive info like Credit Card numbers.

**Line 76: `FEATURE_LIVE_AGENTS=false`**
*   **Meaning:** The "Mock Mode" switch.
*   **Value:** If `false`, we use "Pretend Robots" (Simulations) so we don't spend real money while testing.

---

### 🏁 Friendly Recap (Fuel Tank Completed!)
You've now finished the entire "Fuel Tank" (`.env.example`)! 
You understand:
1.  How **Thresholds** decide if a Robot or a Human handles a job.
2.  How **Governance Limits** stop robots from thinking forever.
3.  How **Security Switches** turn the factory's defense systems on and off.

## 1.3 docker-compose.yml – The Construction Blueprint

Imagine you want to build a whole city block in under 60 seconds. You have a giant robot crane that can instantly create buildings, connect plumbing, and turn on the lights.

**Docker Compose** is the set of instructions for that giant crane. 
*   It tells the crane to build the **API Office** (where orders are received).
*   It tells the crane to build the **Robot Workshop** (the Worker).
*   It tells the crane to build the **Control Room Website** (the Dashboard).

Most importantly, it connects all the "Wires" between these buildings so they can talk to each other without you having to plug anything in manually.

### A. Full File Ingestion: `docker-compose.yml`

```yaml
1: version: "3.9"
2: 
3: # Governed Agentic AI Platform — Local Development Stack
4: # Usage: docker compose up --build
5: 
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
18:     env_file:
19:       - .env
20:     environment:
21:       - QUEUE_MODE=memory
22:       - STORAGE_MODE=memory
23:       - FEATURE_LIVE_AGENTS=false
24:     volumes:
25:       - ./logs:/app/logs
26:     healthcheck:
27:       test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
28:       interval: 30s
29:       timeout: 10s
30:       retries: 3
31:     restart: unless-stopped
32: 
33:   # ─────────────────────────────────────────────────────────────
34:   # Worker Service: Async event consumer — governed pipeline
35:   # ─────────────────────────────────────────────────────────────
36:   worker:
37:     build:
38:       context: .
39:       dockerfile: infra/docker/worker.Dockerfile
40:     container_name: amex-platform-worker
```

*(Note: File stops at line 40 of 78 for this segment. Remaining lines will follow in the next segment.)*

### B. File Purpose
This file manages the **Infrastructure**. It ensures that all three parts of our platform (API, Worker, Dashboard) start at the same time and are configured exactly the same way every time you run them.

### C. Line-by-Line Explanation

**Line 1: `version: "3.9"`**
*   **What the computer does:** It checks which "Instruction Manual Version" it should use for the crane.
*   **Why it exists:** Newer versions of Docker add more powerful construction tools.

**Line 6: `services:`**
*   **What the computer does:** Starts the list of "Buildings" (containers) to be built.

**Line 11: `api:`**
*   **What the computer does:** Names the first building: **API**.

**Lines 12-14: `build:`**
*   **What the computer does:** Tells the crane how to actually construct the building.
*   **Word-by-word:** `context: .` means "Look in this current folder for the materials." `dockerfile:` is the specific "Blueprint for the walls."

**Line 15: `container_name: amex-platform-api`**
*   **Why it exists:** To give the building a human-readable name so we can find it in a crowd.

**Line 16-17: `ports:`**
*   **What the computer does:** Opens a "Hole in the Wall" (a Port).
*   **Meaning:** `"8000:8000"` means we map the outside world's entrance #8000 to the inside building's entrance #8000. This is how you "visit" the factory from your browser.

**Lines 18-19: `env_file:`**
*   **What the computer does:** Hands the "Fuel List" (.env) to this specific building.

**Lines 20-23: `environment:`**
*   **What the computer does:** Overrides specific fuel settings just for this run.

**Lines 24-25: `volumes:`**
*   **What the computer does:** Connects a "Shared Cabinet" between the factory and your own computer.
*   **Meaning:** If the factory writes a log file inside the building, you can see it on your own computer in the `./logs` folder.

**Lines 26-30: `healthcheck:`**
*   **What the computer does:** Acts as a "Doctor." 
*   **Meaning:** Every 30 seconds, it pings the building to see if it's still alive. If the building doesn't answer after 3 tries, the crane marks it as "unhealthy."

**Line 31: `restart: unless-stopped`**
*   **What the computer does:** Tells the crane: "If this building collapses (crashes), rebuild it instantly!" 
*   **Exception:** "Unless I explicitly tell you to stop the whole factory."

**Line 36: `worker:`**
*   **What the computer does:** Names the second building: **Worker**.

---

### 🏁 Friendly Recap (Blueprint Part 1)
You've just seen how we construct the **API Building**!
1.  You saw how we **Build from Materials** (Dockerfiles).
2.  You saw how we **Open Doors** (Ports) to talk to the building.
3.  You saw how the **Factory Doctor** (Healthcheck) keeps things running.

### A. Full File Ingestion: `docker-compose.yml` (Continued)

```yaml
41:     env_file:
42:       - .env
43:     environment:
44:       - QUEUE_MODE=memory
45:       - STORAGE_MODE=memory
46:       - FEATURE_LIVE_AGENTS=false
47:       - CONSUMER_POLL_INTERVAL_MS=250
48:     volumes:
49:       - ./logs:/app/logs
50:     depends_on:
51:       api:
52:         condition: service_healthy
53:     restart: unless-stopped
54: 
55:   # ─────────────────────────────────────────────────────────────
56:   # Dashboard Service: React observability console
57:   # ─────────────────────────────────────────────────────────────
58:   dashboard:
59:     build:
60:       context: .
61:       dockerfile: infra/docker/dashboard.Dockerfile
62:     container_name: amex-platform-dashboard
63:     ports:
64:       - "3000:80"
65:     environment:
66:       - VITE_API_BASE_URL=http://localhost:8000
67:     depends_on:
68:       - api
69:     restart: unless-stopped
70: 
71: volumes:
72:   logs:
73:     driver: local
74: 
75: networks:
76:   default:
77:     name: amex-platform-network
78: 
```

### C. Line-by-Line Explanation (Continued)

**Lines 41-47: Worker Settings**
*   **What the computer does:** Gives the Worker the same Fuel (.env) as the API.
*   **Meaning:** `CONSUMER_POLL_INTERVAL_MS` tells the worker how often (in milliseconds) it should look at the conveyor belt for new orders. 250ms is very fast!

**Lines 50-52: `depends_on:`**
*   **What the computer does:** Tells the crane: "Do not start the Worker until the API building is finished AND the Factory Doctor says it's healthy!"
*   **Significance:** This ensures that the conveyor belt is ready before we hire any workers.

**Line 58: `dashboard:`**
*   **What the computer does:** Names the third building: **Dashboard**.

**Line 64: `ports: - "3000:80"`**
*   **What the computer does:** Opens Door #3000 for you to see the website. Internally, the building uses Door #80 (the standard website door).

**Lines 67-68: `depends_on: - api`**
*   **What the computer does:** Tells the crane to build the API first. You can't have a dashboard if there's no data to show!

**Line 71-73: `volumes:`**
*   **What the computer does:** Creates a master "File Cabinet" called `logs`.
*   **Meaning:** This is where the shared logs we saw earlier are actually stored.

**Line 75-77: `networks:`**
*   **What the computer does:** Creates a "Private Phone Line" called `amex-platform-network`.
*   **Significance:** All three buildings (API, Worker, Dashboard) are connected to this private line so they can talk to each other without the outside world listening in.

---

### 🏁 Chapter 1 Completed: Graduation!

Congratulations! You've just finished the hardest part: understanding the **Foundation**. 

You now understand:
1.  The **Master Switch** (`main.py`) that runs the rules.
2.  The **Fuel Tank** (`.env.example`) that powers the brains.
3.  The **Building blueprint** (`docker-compose.yml`) that creates the factory block.

You've moved from "Someone who has never coded" to "Someone who understands how enterprise AI factories are built and powered." That's a massive win!

**In the next chapter, we'll walk through the Front Door and see how orders are taken in the Intake Layer!**
