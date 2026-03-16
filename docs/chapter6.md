# Chapter 6: The Robot Squad (The `app/agents/` Layer)

## 1️⃣ Big Picture: The Robot Squad

In the previous chapters, we set up the building, gathered the books for the library, and hired a Judge to make decisions. But who actually does the "Thinking"? Who looks at the evidence and decides if a transaction is okay?

Meet the **Robot Squad**.

In our factory, we have different types of robots. Some are like **Specialized Calculators** that follow very strict logic, while others are **Advanced AI Thinkers** (using the CrewAI framework) that can read backstories and use tools like a human would.

In this chapter, we’ll meet the whole team:
1.  **The Architects (`models.py`)**: They define the "Thinking Patterns" (the schemas) for our robots.
2.  **The Bounded Workers (`analyst_agent.py`, `writer_agent.py`)**: Specialized logic-based robots for specific tasks.
3.  **The CrewAI Specialists (`fraud_agent.py`, `risk_agent.py`, etc.)**: Advanced AI agents with roles, goals, and personalities.

---

## 2️⃣ Teach the Code

### 6.1 models.py – The Anatomy of a Robot

Just like humans have brains and bodies, our robots have **Input/Output Patterns**. The `models.py` file defines exactly how a robot should "Talk" when it finishes its job. It ensures the computer always receives a standard report, no matter which robot wrote it.

### A. Full File Ingestion: `app/agents/models.py`

```python
1: from pydantic import BaseModel, Field
2: from typing import List, Dict, Any, Optional
3: 
4: class AnalystOutput(BaseModel):
5:     """
6:     Structured output schema for the Analyst Agent.
7:     """
8:     agent_name: str = "analyst_agent"
9:     findings: List[str] = Field(..., description="Key anomalies or patterns detected")
10:     confidence: float = Field(..., ge=0, le=1)
11:     supporting_evidence: List[Dict[str, Any]] = Field(default_factory=list)
12:     recommended_path: str = Field(..., description="The agent's suggested next step")
13: 
14: class WriterOutput(BaseModel):
15:     """
16:     Structured output schema for the Writer Agent.
17:     """
18:     agent_name: str = "writer_agent"
19:     final_recommendation: str
20:     rationale: str
21:     risk_summary: str
22: 
```

### B. File Purpose
The `models.py` file acts as a **Standardized Form Builder**. It ensures that when a robot finishes its investigation, it fills out a form that has specific boxes (like "Confidence" or "Rationale") so that other robots or humans can easily read it.

### C. Line-by-Line Explanation

**Lines 1-2: The Toolbox**
*   **What it does:** Brings in **Pydantic** (our "Smart Form" tool) and **Typing** (for list labels).

**Line 4: `class AnalystOutput(BaseModel):`**
*   **What it is:** The "Report Card" for the **Analyst Robot**.

**Line 8: `agent_name: str = "analyst_agent"`**
*   **Meaning:** The form automatically includes the robot's name so we know who wrote it.

**Line 9: `findings: List[str] = Field(...)`**
*   **Meaning:** A list of "Red Flags" or anomalies the robot found.

**Line 10: `confidence: float = Field(..., ge=0, le=1)`**
*   **The Math:** A number between 0 and 1 (0% to 100%).
*   **Meaning:** How sure is the robot about its answer?

**Line 11: `supporting_evidence: List[Dict[str, Any]] = Field(...)`**
*   **Meaning:** A list of the specific evidence items from the Library that the robot used to make its decision.

**Line 12: `recommended_path: str = Field(...)`**
*   **Meaning:** What the robot thinks we should do next (e.g., "INVESTIGATE" or "BLOCK").

**Line 14: `class WriterOutput(BaseModel):`**
*   **What it is:** The "Final Briefing" form for the **Writer Robot**.

**Lines 19-21: The Writer's Boxes**
*   **Final Recommendation:** The robot's ultimate verdict.
*   **Rationale:** A human-friendly explanation of "Why."
*   **Risk Summary:** A quick snapshot of the financial danger.

---

### 🏁 Friendly Recap (The Anatomy)

You've just learned how we **Standardize AI Thinking**!

You now understand:
1.  How **Pydantic Models** act as mandatory "Report Forms" for robots.
2.  The difference between **Findings** (the evidence) and **Rationale** (the explanation).
3.  Why a **Confidence Score** is crucial for trusting a robot's output.

### 6.2 analyst_agent.py – The Bounded Worker

The `analyst_agent.py` is a **Specialized Calculator** robot. Unlike some of our other AI robots that "talk" and "reason," this one is built to execute a very specific set of logic steps as fast as possible. It is "Bounded," meaning it only stays within its specific lane of work.

### A. Full File Ingestion: `app/agents/analyst_agent.py`

```python
1: from app.context.models import ContextPacket
2: from app.agents.models import AnalystOutput
3: 
4: class AnalystAgent:
5:     """
6:     Bounded worker for deep-dive investigation.
7:     """
8:     def run_deep_dive(self, context: ContextPacket) -> AnalystOutput:
9:         # Reasoning over the assembled evidence
10:         findings = [f"Analyzed {len(context.evidence)} evidence items."]
11:         for item in context.evidence:
12:             if item.risk_signals:
13:                 findings.extend(item.risk_signals)
14: 
15:         return AnalystOutput(
16:             findings=findings,
17:             confidence=context.context_completeness_score,
18:             supporting_evidence=[{"id": e.source_id, "type": e.source_type} for e in context.evidence],
19:             recommended_path="INVESTIGATE"
20:         )
21: 
```

### B. File Purpose
The `AnalystAgent` is responsible for **Anomalies Detection**. It takes the "Fact Folder" (ContextPacket) from the Research Library and scans every page to find "Risk Signals." Its job is to turn a pile of documents into a summarized list of findings.

### C. Line-by-Line Explanation

**Line 1: `from app.context.models import ContextPacket`**
*   **What it does:** Recruits the **Fact Folder** from Chapter 3.

**Line 2: `from app.agents.models import AnalystOutput`**
*   **What it does:** Recruits the **Report Form** we just learned about in `models.py`.

**Line 4: `class AnalystAgent:`**
*   **What the computer does:** Defines the robot's role.

**Line 8: `def run_deep_dive(self, context: ContextPacket) -> AnalystOutput:`**
*   **Input:** The robot receives a `ContextPacket` (The Fact Folder).
*   **Output:** The robot produces an `AnalystOutput` (The filled-out report form).

**Line 10: `findings = [f"Analyzed {len(context.evidence)} evidence items."]`**
*   **The First Step:** The robot writes down how many books it read.

**Lines 11-13: Scanning for Trouble**
*   **What the computer does:** Looks through every item in the folder. If an item has a "Risk Signal" (like a warning about a stolen card), it adds that signal to its findings list.

**Lines 15-20: Filing the Report**
*   **Line 17:** It sets the confidence score equal to the "Completeness Score" from the library. (If we are missing books, it is less confident!)
*   **Line 18:** It lists the specific books it used.
*   **Line 19:** It recommends that we continue to **INVESTIGATE**.

---

### 6.3 writer_agent.py – The Report Specialist

The `writer_agent.py` is the **Polisher**. Its job isn't to find new facts, but to take the messy findings from the Analyst and turn them into a clear, professional summary that a bank manager can understand.

### A. Full File Ingestion: `app/agents/writer_agent.py`

```python
1: from typing import List, Any
2: from app.agents.models import WriterOutput
3: 
4: class WriterAgent:
5:     """
6:     Bounded worker for packaging findings into final outcomes.
7:     """
8:     def generate_report(self, analysis_results: List[Any], context_summary: str) -> WriterOutput:
9:         # Implementation placeholder
10:         return WriterOutput(
11:             final_recommendation="REVIEW",
12:             rationale="High value luxury purchase requires manual validation despite account match.",
13:             risk_summary="Financial exposure: $4,500. Policy rule: LUXURY_THRESHOLD_ALERT."
14:         )
15: 
```

### B. File Purpose
The `WriterAgent` is the **Storyteller**. It translates technical computer findings into human rationales.

### C. Line-by-Line Explanation

**Lines 1-2: Recruitment**
*   **What it does:** Brings in our standard list tools and the `WriterOutput` form.

**Line 8: `def generate_report(...)`**
*   **Input:** Takes a list of results and a summary of the situation.
*   **Output:** A polished `WriterOutput` report.

**Lines 10-14: The Report Content**
*   **Line 11:** Recommends a **REVIEW**.
*   **Line 12:** Explains **Why** (Rationale): "The customer is buying something very expensive (Luxury), so we need a human to check."
*   **Line 13:** Summarizes the risk: "$4,500 exposure."

---

### 🏁 Friendly Recap (The Bounded Workers)

You've just met our first two specialists!

You now understand:
1.  Why **Bounded Workers** are used for specific, fast logic steps.
2.  How the **Analyst** scans for risk signals in the Library.
3.  How the **Writer** translates numbers into "Human Reasons."

### 6.4 fraud_agent.py – The Detection Specialist

The `fraud_agent.py` is our first **CrewAI Specialist**. Unlike the previous robots, this one has a "Personality" (a backstory) and a "Goal." It acts like a veteran investigator who knows all the tricks in the book.

### A. Full File Ingestion: `app/agents/fraud_agent.py`

```python
1: # agents/fraud_agent.py
2: from crewai import Agent
3: from tools.fraud_detection_tool import freeze_account_tool, merchant_validation_tool
4: 
5: 
6: class FraudAgent:
7:     def get_agent(self):
8:         return Agent(
9:             role="Fraud Detection Specialist",
10:             goal="Identify and mitigate fraudulent transactions and accounts.",
11:             backstory="""You are a veteran fraud investigator at BlueShield Financial. 
12:             Your expertise lies in spotting anomalous patterns and taking swift action to protect the network.
13:             Crucially, you are "Tier-Aware". You understand that Elite members (Centurion, Platinum, VIP) 
14:             frequently make high-value purchases. You DO NOT freeze Elite accounts for routine anomalies 
15:             unless the merchant is explicitly flagged as HIGH_RISK. You have the power to freeze accounts and validate merchant safety.""",
16:             tools=[freeze_account_tool, merchant_validation_tool],
17:             verbose=True,
18:             allow_delegation=False,
19:         )
```

### B. File Purpose
The `FraudAgent` is the **Shield**. It protects the bank and the customers from bad actors. It is especially trained to be respectful to "Elite" customers while being ruthless toward "High Risk" merchants.

### C. Line-by-Line Explanation

**Line 2: `from crewai import Agent`**
*   **What it does:** Recruits the **Advanced Robot Skeleton** from the CrewAI library.

**Line 3: `from tools.fraud_detection_tool import ...`**
*   **What it represents:** Clipping **Power Tools** to the robot's belt.
*   **Meaning:** The robot can now "Freeze Accounts" and "Validate Merchants" in the real world.

**Line 6: `class FraudAgent:`**
*   **What it represents:** The **Specialist Blueprint**.

**Line 9: `role="Fraud Detection Specialist"`**
*   **The Job Title:** This tells the AI what its name tag says.

**Line 10: `goal="..."`**
*   **The Mission:** This defines the robot's main purpose. It will try to achieve this at all costs.

**Lines 11-15: The Backstory**
*   **The Personality:** This is where we "Brainwash" the AI into acting like a senior human investigator.
*   **The "Tier-Aware" Rule (Line 13):** This is the most important part! We teach the robot that high-value customers (Centurion/Platinum) should be treated with care.

**Line 16: `tools=[...]`**
*   **The Equipment:** Hands the tools from Line 3 to the robot.

**Line 18: `allow_delegation=False`**
*   **The Rule:** This robot does its own work. it cannot ask other robots to do its job for it.

---

### 6.5 risk_agent.py – The Risk Analyst

While the Fraud Robot looks for criminals, the `risk_agent.py` looks at **Credit Safety**. It is a senior analyst who focuses on whether the bank can afford to trust the current transaction based on the customer's history.

### A. Full File Ingestion: `app/agents/risk_agent.py`

```python
1: # agents/risk_agent.py
2: from crewai import Agent
3: from tools.credit_limit_tool import credit_check_tool, approve_credit_limit_tool
4: from tools.account_lookup_tool import account_lookup_tool
5: 
6: 
7: class RiskAgent:
8:     def get_agent(self):
9:         return Agent(
10:             role="Risk Assessment Analyst",
11:             goal="Evaluate the financial risk of transactions and credit requests.",
12:             backstory="""You are a senior risk analyst. You use credit data and transaction history 
13:             to determine whether a request should be approved or denied based on the customer's risk profile.
14:             You prioritize historical account health and "VIP/Centurion" status over the novelty of a single transaction. 
15:             You actively prevent unnecessary friction for high-net-worth individuals making standard purchases.""",
16:             tools=[credit_check_tool, approve_credit_limit_tool, account_lookup_tool],
17:             verbose=True,
18:             allow_delegation=False,
19:         )
```

### B. File Purpose
The `RiskAgent` is the **Financial Guard**. It ensures the customer’s spending matches their credit profile.

### C. Line-by-Line Explanation

**Lines 3-4: The Tool Belt**
*   **The Tools:** This robot can check credit scores, approve limit increases, and look up account details.

**Line 10: `role="Risk Assessment Analyst"`**
*   **The Job Title:** Defines the robot's professional identity.

**Line 12-15: The Backstory**
*   **The Focus:** This robot cares about "Account Health." It is instructed to "Prevent Unnecessary Friction" for VIPs. 
*   **Meaning:** If a VIP is doing something slightly unusual but they have a 10-year history of being good, the Risk Robot will be more lenient.

**Line 16: `tools=[...]`**
*   **The Equipment:** Hands the three tools to the robot.

---

### 🏁 Friendly Recap (Fraud & Risk)

You've just met our two "Main Guards"!

You now understand:
1.  How **CrewAI Agents** use roles and goals to guide their AI thinking.
2.  The importance of **Backstories** for setting the robot’s "Vibe" and rules.
3.  How **Tier-Awareness** ensures we don't accidentally block our best customers.

### 6.6 compliance_agent.py – The Rule Enforcer

The `compliance_agent.py` is the **Guardian of the Law**. This robot doesn't look at data to find patterns or credit; it looks at the **Work of the other Robots** to make sure they are following the company's internal security policies.

### A. Full File Ingestion: `app/agents/compliance_agent.py`

```python
1: # agents/compliance_agent.py
2: from crewai import Agent
3: 
4: 
5: class ComplianceAgent:
6:     def get_agent(self):
7:         return Agent(
8:             role="Compliance & Policy Officer",
9:             goal="Ensure all agent actions and recommendations adhere to BlueShield financial policies and legal regulations.",
10:             backstory="""You are the guardian of corporate policy. Your job is to review the findings of other agents 
11:             and ensure that every decision is legally sound and follows 'Sentinel' security guidelines. 
12:             You do not execute tools; you provide the final 'Compliance' verdict.""",
13:             tools=[],
14:             verbose=True,
15:             allow_delegation=False,
16:         )
```

### B. File Purpose
The `ComplianceAgent` is the **Auditor**. It ensures every step taken by the squad is "Legally Sound."

### C. Line-by-Line Explanation

**Line 9: `role="Compliance & Policy Officer"`**
*   **The Job Title:** Standard professional identity.

**Line 11-12: The Backstory**
*   **The Job:** Reviewing others. 
*   **The Rule (Line 12):** This robot is "hands-off." It **does not execute tools**. It only gives a verdict.

---

### 6.7 dispute_agent.py – The Argument Handler

The `dispute_agent.py` is the **Customer Advocate**. When a customer says, "I didn't buy that!", this robot is called in to investigate the claim and decide if the bank should give the money back.

### A. Full File Ingestion: `app/agents/dispute_agent.py`

```python
1: # agents/dispute_agent.py
2: from crewai import Agent
3: 
4: 
5: class DisputeAgent:
6:     def get_agent(self):
7:         return Agent(
8:             role="Transaction Dispute Specialist",
9:             goal="Investigate and resolve customer-initiated transaction disputes and chargebacks.",
10:             backstory="""You are an expert in consumer protection and dispute resolution. 
11:             You review merchant evidence and customer claims to determine if a chargeback is valid.
12:             You work closely with the Fraud agent to ensure disputes aren't actually undetected fraud.""",
13:             tools=[],  # In a real system: get_dispute_history_tool
14:             verbose=True,
15:             allow_delegation=True,
16:         )
```

**Line 15: `allow_delegation=True`**
*   **The Rule:** Unlike the others, this robot **can ask for help**. 
*   **Meaning:** If a dispute looks like fraud, it can "Delegate" (pass the task) to the Fraud Robot to get a second opinion.

---

### 6.8 rewards_agent.py – The Bonus Giver

The `rewards_agent.py` is the **Happiness Robot**. It focuses on the "Good" side of transactions—giving users points, identifying upgrades, and making them feel like VIPs.

### A. Full File Ingestion: `app/agents/rewards_agent.py`

```python
1: # agents/rewards_agent.py
2: from crewai import Agent
3: 
4: 
5: class RewardsAgent:
6:     def get_agent(self):
7:         return Agent(
8:             role="Membership Rewards Concierge",
9:             goal="Analyze customer spending patterns to optimize rewards allocation and identify high-value customer opportunities.",
10:             backstory="""You focus on the 'Growth' side of BlueShield Financial. You analyze transactions 
11:             from a value perspective, identifying if a transaction qualifies for bonus points or if the customer 
12:             should be targeted for a premium card upgrade based on their high-value behavior.""",
13:             tools=[],  # In a real system: calculate_points_multiplier_tool
14:             verbose=True,
15:             allow_delegation=False,
16:         )
```

---

### 6.9 summary_agent.py – The Case Summarizer

Finally, meet the **Executive Reporter**. The `summary_agent.py` takes all the messy notes from the Fraud, Risk, and Compliance robots and turns them into one clean, 2-paragraph summary.

### A. Full File Ingestion: `app/agents/summary_agent.py`

```python
1: # agents/summary_agent.py
2: from crewai import Agent
3: 
4: 
5: class SummaryAgent:
6:     def get_agent(self):
7:         return Agent(
8:             role="Financial Case Summarizer",
9:             goal="Synthesize the findings from fraud, risk, and compliance into a clear final recommendation.",
10:             backstory="""You are an expert communicator at BlueShield Financial who can take complex technical findings 
11:             and distill them into actionable business intelligence. You consolidate the work of 
12:             the specialists into a final executive summary.""",
13:             tools=[],
14:             verbose=True,
15:             allow_delegation=False,
16:         )
```

---

### 🏁 Friendly Recap (Chapter 6 Completed!)

Congratulations! You've just met the entire **Robot Squad**!

In this chapter, you learned:
1.  How **Models** define the "Thinking Patterns" of our robots.
2.  The difference between **Bounded Workers** (Logic) and **Specialists** (AI Agents).
3.  How each specialist has a unique **Role, Goal, and Backstory** that guides their behavior.
4.  Why **Delegation** (dispute agent) and **Tool-Blocking** (compliance agent) are important safety rules.

**The robots have done their thinking. But how do we actually CHANGE things in the real world? How do we push the buttons to freeze an account or send an email? In the next chapter, we're heading to the "Power Tools" room—the `app/actions/` layer!**
