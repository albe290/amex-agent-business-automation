# Chapter 10: The Performance Lab (The `app/evals/` Layer)

## 1️⃣ Big Picture: The Performance Lab

Imagine our factory is building thousands of robots every day. Before we let those robots handle real credit cards and millions of dollars, we need to know: **Are they actually smart?** Do they follow the rules? Do they make the same decision every time?

Welcome to the **Performance Lab**.

Think of this as the "Testing & Quality Control" wing of the factory. Here, we run our robots through "Flight Simulators" (scenarios). We give them fake transactions, some safe and some dangerous, and we watch how they react. If a robot fails a test, it goes back to the drawing board before it ever touches a real customer.

In this chapter, we’ll meet:
1.  **The Lab Paperwork (`models.py`)**: The standardized forms for recording test cases and results.
2.  **The Test Exam (`scenarios.py`)**: A set of pre-written "What If?" situations used to challenge the robots.
3.  **The Lab Instruments (`metrics.py`)**: Mathematical tools that measure success rates and speed.
4.  **The Scoring Sheet (`scorecard.py`)**: Translates raw numbers into a final grade (Strong, Fair, or Poor).
5.  **The Main Experiment (`evaluation.py`)**: The engine that actually runs the tests and compares robot answers to the "Golden Truth."
6.  **The Lab Results (`reporter.py`)**: Generates a beautiful summary report for the factory managers.

---

## 2️⃣ Teach the Code

### 10.1 models.py – The Lab Paperwork

To run a scientific experiment, you need standardized forms. The `models.py` file defines the "Test Sheets" and "Result Slips" used in the Lab.

### A. Full File Ingestion: `app/evals/models.py`

```python
1: from pydantic import BaseModel, Field
2: from typing import List, Dict, Any, Optional
3: 
4: class EvalCase(BaseModel):
5:     """
6:     Defines a test scenario with inputs and expected outcomes.
7:     """
8:     case_id: str
9:     scenario_type: str  # e.g., 'SAFE_AUTOMATION', 'ELEVATED_RISK'
10:     request_payload: Dict[str, Any]
11:     expected_validation_status: str = "SUCCESS"
12:     expected_strategy: str
13:     expected_review_required: bool
14:     expected_policy_hits: List[str] = Field(default_factory=list)
15: 
16: class EvalResult(BaseModel):
17:     """
18:     Captures the actual performance vs expected outcomes for a case.
19:     """
20:     case_id: str
21:     scenario_type: str
22:     actual_validation_status: str
23:     actual_strategy: str
24:     actual_review_required: bool
25:     actual_policy_hits: List[str]
26:     passed: bool
27:     failure_reasons: List[str] = Field(default_factory=list)
28:     latency_ms: float = 0.0
29: 
30: class MetricSnapshot(BaseModel):
31:     """
32:     Aggregated performance signals across an evaluation run.
33:     """
34:     total_cases: int
35:     pass_rate: float
36:     automation_rate: float
37:     review_rate: float
38:     escalation_rate: float
39:     block_rate: float
40:     override_rate: float = 0.0
41:     strategy_match_rate: float
42:     policy_hit_precision: float
43: 
44: class Scorecard(BaseModel):
45:     """
46:     High-level qualitative summary of platform health.
47:     """
48:     governance_score: str  # POOR, FAIR, STRONG
49:     routing_quality: str
50:     human_alignment: str
51:     operational_efficiency: str
52:     summary_notes: str
```

### B. File Purpose
The `models.py` file ensures that every test is recorded exactly the same way. It defines:
*   **EvalCase**: The "Question" (What is the input? What is the correct answer?).
*   **EvalResult**: The "Answer Sheet" (What did the robot actually do? Did it get the question right?).
*   **MetricSnapshot**: The "Class Average" (How did all the robots do as a group?).
*   **Scorecard**: The "Final Grade" (Is the factory healthy?).

### C. Line-by-Line Explanation

**Line 4: `EvalCase`**
*   **The Question:** This is the input to our experiment.
*   **Line 12 (`expected_strategy`):** This is the **Teacher's Key**. We tell the lab exactly which strategy the robot *should* choose for this test.

**Line 16: `EvalResult`**
*   **The Grade:** This records the robot's performance.
*   **Line 26 (`passed`):** A simple True/False. Did the robot's choice match the Teacher's Key?
*   **Line 28 (`latency_ms`):** We also track how fast the robot thought (in milliseconds). In the Lab, slow robots are penalized!

**Line 30: `MetricSnapshot`**
*   **The Statistics:** This aggregates thousands of tests into percentages (e.g., 95% Pass Rate).

**Line 44: `Scorecard`**
*   **The Report Card:** This turns numbers into words. Instead of "0.98 accuracy," it says **"STRONG Governance."**

---

### 10.2 scenarios.py – The Test Exam

Now that we have the forms, we need some actual questions! The `scenarios.py` file is the **Test Exam**. It contains a library of "Baseline Scenarios" that every robot must pass.

### A. Full File Ingestion: `app/evals/scenarios.py`

```python
1: from typing import List
2: from app.evals.models import EvalCase
3: 
4: def get_baseline_scenarios() -> List[EvalCase]:
5:     """
6:     Returns the core set of evaluation scenarios for the platform.
7:     """
8:     return [
9:         EvalCase(
10:             case_id="SCENARIO_1_SAFE",
11:             scenario_type="SAFE_AUTOMATION",
12:             request_payload={
13:                 "use_case_type": "dispute_inquiry",
14:                 "customer_context": {"id": "CUST-101"},
15:                 "business_payload": {"amount": 50.0}  # Risk score 10 -> AUTOMATE
16:             },
17:             expected_strategy="AUTOMATE",
18:             expected_review_required=False,
19:             expected_policy_hits=[]
20:         ),
...
34:         EvalCase(
35:             case_id="SCENARIO_3_ESCALATE",
36:             scenario_type="HIGH_RISK",
37:             request_payload={
38:                 "use_case_type": "fraud_dispute",
39:                 "customer_context": {"id": "CUST-303"},
40:                 "business_payload": {"amount": 12000.0} # Risk score 60 + Policy Flag -> ESCALATE
41:             },
42:             expected_strategy="ESCALATE",
43:             expected_review_required=True,
44:             expected_policy_hits=["HIGH_VALUE_TRANSACTION"]
45:         ),
...
58:     ]
```

### B. File Purpose
The `scenarios.py` file provides a **Golden Dataset**. It includes:
*   **Safe Scenarios**: Easy tests where the robot should just "Automate."
*   **High Risk Scenarios**: Hard tests involving large amounts of money where the robot *must* escalate.
*   **Security Scenarios**: Tests where a robot must catch a policy violation (like PII in a note).

### C. Line-by-Line Explanation

**Line 10: `case_id="SCENARIO_1_SAFE"`**
*   **Test #1:** A small $50 dispute. 
*   **The Expectation (Line 17):** The robot should realize this is safe and choose "AUTOMATE."

**Line 35: `case_id="SCENARIO_3_ESCALATE"`**
*   **Test #3:** A massive $12,000 fraud dispute.
*   **The Expectation (Line 42-43):** The robot **must** choose "ESCALATE" and mark "review_required=True." If it tries to automate this, it fails the test!

---

### 10.3 metrics.py – The Lab Instruments

Once the tests are finished, we need to crunch the numbers. The `metrics.py` file contains the **Lab Instruments**—the calculators that turn thousands of outcomes into a single health signal.

### A. Full File Ingestion: `app/evals/metrics.py`

```python
1: from typing import List
2: from app.evals.models import EvalResult, MetricSnapshot
3: 
4: class PlatformMetrics:
5:     """
6:     Calculates operational and quality metrics from evaluation results.
7:     """
8:     
9:     def calculate_snapshot(self, results: List[EvalResult]) -> MetricSnapshot:
10:         total = len(results)
11:         if total == 0:
12:             return MetricSnapshot(...)
13:             
17:         passes = sum(1 for r in results if r.passed)
18:         
19:         # Routing distribution
20:         automations = sum(1 for r in results if r.actual_strategy == "AUTOMATE")
21:         escalations = sum(1 for r in results if r.actual_strategy == "ESCALATE")
22:         blocks = sum(1 for r in results if r.actual_validation_status == "FAILED" or r.actual_strategy == "BLOCK")
23:         reviews = sum(1 for r in results if r.actual_review_required)
24:         
25:         strategy_matches = sum(1 for r in results if not any("Strategy mismatch" in f for f in r.failure_reasons))
26:         
30:         return MetricSnapshot(
31:             total_cases=total,
32:             pass_rate=passes / total,
33:             automation_rate=automations / total,
34:             review_rate=reviews / total,
35:             escalation_rate=escalations / total,
36:             block_rate=blocks / total,
37:             strategy_match_rate=strategy_matches / total,
38:             policy_hit_precision=100.0 # Placeholder
39:         )
```

### B. File Purpose
The `PlatformMetrics` tool acts as a **Statistical Analyzer**. It calculates two types of scores:
1.  **Quality Scores**: How often the robots were correct (`pass_rate`).
2.  **Operational Scores**: How much of the work is being automated vs requiring humans (`automation_rate`).

### C. Line-by-Line Explanation

**Line 17: `passes = sum(...)`**
*   **The Math:** Total up every robot that got its question right.

**Lines 20-23: Distribution Tracking**
*   **The Math:** Count how many times the system chose to Automate, Escalate, Block, or Review. This helps factory managers see if the system is becoming too "cautious" or too "loose."

**Line 30-38: The Snapshot**
*   **The Output:** Packages everything into a single `MetricSnapshot` so it can be sent to the principal (the CEO or Compliance Officer).

---

### 🏁 Friendly Recap (The Lab Setup)

You've just learned how we **Set Up the Experiment**!

You now understand:
1.  How **Standardized Forms** (models) keep our test data scientific.
2.  How the **Golden Dataset** (scenarios) provides the "Right Answers" for the test.
3.  How **Lab Instruments** (metrics) convert thousands of robot actions into percentages.

### 10.4 scorecard.py – The Scoring Sheet

While Percentages (like 92%) are great for scientists, managers need to know: **"Is this good or bad?"** The `scorecard.py` file is the **Scoring Sheet**. It takes raw numbers and converts them into human-friendly "Quality Ratings."

### A. Full File Ingestion: `app/evals/scorecard.py`

```python
1: from app.evals.models import MetricSnapshot, Scorecard
2: 
3: class PlatformScorecard:
4:     """
5:     Transforms quantitative metrics into qualitative quality ratings.
6:     """
7:     
8:     def generate(self, metrics: MetricSnapshot) -> Scorecard:
9:         # 1. Governance Score
10:         gov_val = "STRONG"
11:         if metrics.pass_rate < 0.8: gov_val = "FAIR"
12:         if metrics.pass_rate < 0.5: gov_val = "POOR"
13:         
14:         # 2. Routing Quality
15:         rout_val = "STRONG"
16:         if metrics.strategy_match_rate < 0.8: rout_val = "FAIR"
17:         if metrics.strategy_match_rate < 0.5: rout_val = "POOR"
18:         
19:         # 3. Operational Efficiency
20:         # High automation + low fallback = Strong
21:         eff_val = "STRONG"
22:         if metrics.automation_rate < 0.3: eff_val = "FAIR"
23:         
24:         return Scorecard(
25:             governance_score=gov_val,
26:             routing_quality=rout_val,
27:             human_alignment="STRONG", # Placeholder
28:             operational_efficiency=eff_val,
29:             summary_notes=f"Platform processed {metrics.total_cases} cases with a {metrics.pass_rate*100:.1f}% success rate."
30:         )
```

### B. File Purpose
The `PlatformScorecard` acts as the **Final Judge**. It looks at the pass rate and the strategy match rate and decides if the system is ready for launch.
*   **Strong**: Ready for deployment.
*   **Fair**: Needs more testing or better prompts.
*   **Poor**: Stop! The robots are too confused.

### C. Line-by-Line Explanation

**Lines 10-12: Governance Score**
*   **The Logic:** If the robots are wrong more than 20% of the time (`pass_rate < 0.8`), the Governance rating drops to "FAIR." If they are wrong more than half the time, it becomes "POOR."

**Lines 15-17: Routing Quality**
*   **The Logic:** This checks if the robots are choosing the correct strategy (Automate vs investigate). Even if a robot gets a final answer right, if it chose the wrong "Path" to get there, its Routing Quality score drops.

**Lines 21-22: Efficiency Check**
*   **The Logic:** A factory is only useful if it automates things. If our robots are escalating *everything* to humans (`automation_rate < 0.3`), the system isn't efficient, so we mark it as "FAIR."

---

### 10.5 evaluation.py – The Main Experiment

We have the exam, the instruments, and the scoring sheet. Now we need someone to actually **Run the Test**. The `evaluation.py` file is the **Main Experiment**. It takes our "Golden Dataset" and feeds it through the whole factory as if it were real life.

### A. Full File Ingestion: `app/evals/evaluation.py`

```python
5: class AgentEvaluator:
6:     """
7:     Simulates running the agent against a 'golden dataset'
8:     to evaluate its accuracy and compliance safety.
9:     """
10: 
11:     def __init__(self):
12:         self.orchestrator = AgentOrchestrator()
13: 
14:     def evaluate_golden_dataset(self, dataset: list) -> dict:
...
20:         for case in dataset:
21:             context = case["context"]
22:             expected_decision = case["expected_decision"]
23: 
25:             result = self.orchestrator.process_request(workflow, context)
...
39:             if actual_decision == expected_decision:
40:                 passed += 1
41:             else:
42:                 failed += 1
...
50:         return {
51:             "total_cases": total,
52:             "passed": passed,
53:             "failed": failed,
54:             "accuracy_percent": round(accuracy, 2),
55:             "evaluation_time_seconds": round(duration, 4),
56:         }
```

### B. File Purpose
The `AgentEvaluator` is the **Flight Simulator Pilot**. It initializes the real factory logic (`AgentOrchestrator`) and starts throwing "Practice Scenarios" at it. It records how many the robot gets right and how many it fails.

### C. Line-by-Line Explanation

**Line 12: `self.orchestrator = AgentOrchestrator()`**
*   **The Setup:** This brings in the *entire* factory (all the robots, tools, and judges we've learned about so far).

**Line 25: `result = self.orchestrator.process_request(...)`**
*   **The Experiment:** We give the factory a fake case and wait for it to finish.

**Lines 39-42: The Grading**
*   **The Check:** If the `actual_decision` from the factory matches the `expected_decision` from our Golden Dataset, we count it as a "PASS."

---

### 10.6 reporter.py – The Lab Results

Finally, after the experiment is done, we need to show the world. The `reporter.py` file is the **Lab Results**. It takes the results, the metrics, and the scorecard and prints out a professional executive summary.

### A. Full File Ingestion: `app/evals/reporter.py`

```python
9:     def print_summary(self, results: List[EvalResult], metrics: MetricSnapshot, scorecard: Scorecard, insights: List[str]):
10:         print("\n" + "="*50)
11:         print(" PLATFORM EVALUATION SUMMARY")
12:         print("="*50)
...
23:         print(f"   Pass Rate:        {metrics.pass_rate*100:.1f}%")
24:         print(f"   Automation Rate:  {metrics.automation_rate*100:.1f}%")
...
31:         print(f"   Governance:       {scorecard.governance_score}")
32:         print(f"   Routing Quality:  {scorecard.routing_quality}")
33:         print(f"   Efficiency:       {scorecard.operational_efficiency}")
```

### B. File Purpose
The `EvalReporter` provides the **Human Summary**. It formats the raw data into a clean ASCII table that managers can read in their terminal or log files to verify the health of the system.

---

### 🏁 Friendly Recap (Chapter 10 Completed!)

Congratulations! You've just mastered the **Performance Lab**!

In this chapter, you learned:
1.  How the **Golden Dataset** (scenarios.py) provides the ground truth for our experiments.
2.  How the **Lab Instruments** (metrics.py) calculate success and automation rates.
3.  How the **Scoring Sheet** (scorecard.py) gives our robots a human-readable grade.
4.  Why we run an **Experiment** (evaluation.py) before every new release to ensure safety.

**Our factory is verified, safe, and efficient. But how do we actually *run* the entire factory building from the outside? In the next chapter, we're heading to the "Control Room"—the project root files like `main.py` and `server.py`—to see how it all comes together!**
