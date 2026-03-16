# 📘 BlueShield: The Governed Agentic AI Platform
## *A Beginner's Guide to Building Autonomous, Safe, and Smart Systems*

## 🏢 Chapter 1: The Factory Entrance (The Project Root)
*Where it all begins. We look at the project's purpose and its high-level structure.*
*   **README.md** – The Factory Map
*   **SHOWCASE.md** – The Project Highlights

---

## 🏗️ Chapter 2: The Front Counter (The `app/intake/` Layer)
*This is where orders enter the factory. We make sure every request is signed and standard.*
*   **schemas.py** – The Standard Order Form

---

## 📚 Chapter 3: The Research Library (The `app/context/` Layer)
*This department gathers evidence. It looks up history, rules, and facts to help the robots.*
*   **models.py** – Designing the Library Shelves
*   **builder.py** – Assembling the Fact Folder
*   **retriever.py** – The Librarian Finding Information
*   **ranker.py** – Sorting the Most Relevant Facts
*   **enricher.py** – Highlighting Important Details
*   **sources.py** – The List of Information Sources
*   **ingestion.py** – Bringing in New Books

---

## ⚖️ Chapter 4: The Judge’s Bench (The `app/control_plane/` Layer)
*This is the brain of the operation. It makes the final decision on risk and safety.*
*   **models.py** – The Judge's Paperwork
*   **coordinator.py** – The Judge Managing the Courtroom
*   **decision.py** – The Final Verdict Paperwork
*   **risk.py** – The Danger Calculator
*   **scoring_engine.py** – The Math Behind the Risk
*   **policy.py** – The Corporate Law Book
*   **policy_loader.py** – Opening and Reading the Laws
*   **validator.py** – The Document Inspector

---

## 🚦 Chapter 5: The Traffic Tower (The `app/strategy/` Layer)
*This area plans the route. It decides which robots need to be called and in what order.*
*   **router.py** – Picking the Right Path for the Work
*   **planner.py** – Creating the Step-by-Step To-Do List
*   **financial_crew.py** – Calling the Whole Team to Action
*   **fraud_tasks.py** – Specialized Assignments for Fraud
*   **risk_tasks.py** – Specialized Assignments for Risk
*   **compliance_tasks.py** – Specialized Assignments for Compliance

---

## 🤖 Chapter 6: The Robot Squad (The `app/agents/` Layer)
*Meet the workers! Each robot has a specialized job, from spotting fraud to writing reports.*
*   **models.py** – The Anatomy of a Robot
*   **analyst_agent.py** – The Data Specialist
*   **writer_agent.py** – The Report Writer
*   **fraud_agent.py** – The Fraud Spotter
*   **risk_agent.py** – The Danger Measurer
*   **compliance_agent.py** – The Rule Enforcer
*   **dispute_agent.py** – The Argument Handler
*   **rewards_agent.py** – The Bonus Giver
*   **summary_agent.py** – The Simplifier

---

## 🛠️ Chapter 7: The Power Tools (The `app/actions/` & `tools/` Layer)
*These are the tools our robots use to actually change things in the real world.*
*   **transaction_service.py** – The Main Assembly Line
*   **executor.py** – The Final Packaging Station
*   **mock_db.py** – The Simulated Warehouse
*   **account_lookup_tool.py** – The Digital Magnifying Glass
*   **fraud_detection_tool.py** – The Counterfeit Detector
*   **audit_logger.py** – The Official Ledger

---

## 🕵️ Chapter 8: The Safety Inspectors (The `app/review/` Layer)
*The human-in-the-loop layer that double-checks robot work and tracks disagreements.*
*   **models.py** – The Inspector's Paperwork
*   **packet.py** – The Evidence Briefing
*   **queue.py** – The Waiting Room
*   **coordinator.py** – The Inspector General
*   **approval.py** – The Verdict Stamper
*   **overrides.py** – The Disagreement Log

---

## 🛤️ Chapter 9: The Safety Rails (The `app/runtime/` Layer)
*The rules that keep our robots from running too fast or getting lost.*
*   **models.py** – The Referee's Notebook
*   **limits.py** – The Speed Limits
*   **budget.py** – The Wallet (Token Control)
*   **guardrails.py** – The Safety Barriers
*   **retries.py** – The Second Chance
*   **fallback.py** – The Emergency Exit
*   **coordinator.py** – The Execution Referee

---

## 🧪 Chapter 10: The Performance Lab (The `app/evals/` Layer)
*How we test our robots against hard scenarios to measure their IQ and safety.*
*   **models.py** – The Lab Paperwork
*   **scenarios.py** – The Test Exam
*   **metrics.py** – The Lab Instruments
*   **scorecard.py** – The Scoring Sheet
*   **evaluation.py** – The Main Experiment
*   **reporter.py** – The Lab Results

---

## 🎮 Chapter 11: The Control Room (The Root & API Layer)
*How we start the factory and feed it its first instructions.*
*   **main.py** – The Manual Start Switch
*   **server.py** – The Automated Receptionist (FastAPI)
*   **docker-compose.yml** – The Factory Blueprint
*   **.env.example** – The Factory Settings

---

## 💓 Chapter 12: The Observation Deck (The `monitoring/` Layer)
*Watching the factory's pulse. We monitor health, speed, and cost from here.*
*   **metrics.py** – Watching the Factory’s Heartbeat

---

## 💂 Chapter 13: The Guard Towers (The `security/` Layer)
*The security team. They inspect every word to make sure no one is trying to trick the AI.*
*   **validator.py** – The Security Guard
*   **policy_engine.py** – The Security Rulebook
*   **compliance_validator.py** – The Regulatory Inspector
*   **tool_guard.py** – The Tool Locker Key
*   **financial_rules.py** – The Banking Laws

---

## 📺 Chapter 14: The Visual Console (The `dashboard/` Layer)
*The visual screens. How humans watch the entire factory in beautiful graphs and charts.*

---

---

## 🎯 Bonus: Core Engine Study Guide
*The "Execution Spine" of the platform analyzed via the 4-Question Framework.*
*   **[core_engine_study_guide.md](file:///c:/Users/Almlb/OneDrive/Desktop/Code/amex-agent-business-automation/docs/core_engine_study_guide.md)** – Deep Dive: The 5 Files That Run BlueShield
    1.  `app/intake/schemas.py`
    2.  `app/control_plane/coordinator.py`
    3.  `app/strategy/router.py`
    4.  `app/events/consumer.py`
    5.  `app/review/coordinator.py`

## 🏁 Graduation
*You are now a Governed AI Engineer!*
