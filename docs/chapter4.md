# Chapter 4: The Judge’s Bench (The `app/control_plane/` Layer)

## 1️⃣ Big Picture: The Judge’s Bench

Imagine our factory has a high-security room at the very center. Behind a heavy oak door sits **The Judge**.

While the **Front Counter** (Chapter 2) takes the orders and the **Research Library** (Chapter 3) gathers the facts, they don't actually make decisions. They are just "Information Gatherers."

The **Judge’s Bench** is where the actual logic happens. This is the brain that looks at the research folder and says:
*   "This transaction is 100% safe. **Approve it.**"
*   "Wait, this looks weird. **Send it to a human for review.**"
*   "This is definitely a trick! **Block it immediately.**"

The Judge handles the **Governance**. In other words, they make sure our AI follows the bank's laws perfectly, every single time. 

---

## 2️⃣ Teach the Code

### 4.1 coordinator.py – The Presiding Judge

Every courtroom needs someone in charge to call the witnesses and manage the proceedings. The **Coordinator** is that person. They don't do the "Scoring" themselves, but they call the **Scanner**, the **Math Expert**, and the **Law Expert** in the right order.

### A. Full File Ingestion: `app/control_plane/coordinator.py`

```python
1: from typing import Dict, Any
2: from app.control_plane.validator import ControlPlaneValidator
3: from app.control_plane.risk import RiskEngine
4: from app.control_plane.policy import PolicyEngine
5: from app.control_plane.decision import ControlPlaneDecision
6: from app.intake.schemas import PlatformRequest
7: 
8: class ControlPlaneCoordinator:
9:     """
10:     Orchestrates the governance flow within the Control Plane.
11:     Runs validation, risk scoring, and policy evaluation to produce a Decision.
12:     """
13:     
14:     def __init__(self):
15:         self.validator = ControlPlaneValidator()
16:         self.risk_engine = RiskEngine()
17:         self.policy_engine = PolicyEngine()
18: 
19:     def process_request(self, request: PlatformRequest) -> ControlPlaneDecision:
20:         """
21:         End-to-end execution of the control plane logic.
22:         """
23:         # 1. Input Validation
24:         is_valid, reason = self.validator.validate_input(str(request.business_payload))
25:         if not is_valid:
26:             return ControlPlaneDecision(
27:                 validation_status="FAILED",
28:                 risk_score=100.0,
29:                 policy_hits=["SECURITY_VALIDATION_FAILURE"],
30:                 requires_review=True,
31:                 block_reason=reason
32:             )
33: 
34:         # 2. Risk Scoring
35:         risk_score = self.risk_engine.calculate_score(
```

*(Note: File stops at line 35 of 59 for this segment. Remaining lines will follow in the next segment.)*

### B. File Purpose
The `coordinator.py` file is the **Orchestrator** of the Judge's Bench. It takes a raw request from the front counter and passes it through three distinct security checkpoints before making a final verdict.

### C. Line-by-Line Explanation

**Line 1: `from typing import Dict, Any`**
*   **Purpose:** Standard organizational labels for our digital folders.

**Line 2: `from app.control_plane.validator import ControlPlaneValidator`**
*   **What it does:** Recruits the **Document Inspector**. 
*   **Meaning:** This tool scans the text for "Bad Words" or "Malicious Code."

**Line 3: `from app.control_plane.risk import RiskEngine`**
*   **What it does:** Recruits the **Math Expert**.
*   **Meaning:** This tool calculates a "Danger Score."

**Line 4: `from app.control_plane.policy import PolicyEngine`**
*   **What it does:** Recruits the **Law Expert**.
*   **Meaning:** This tool checks the internal bank policies (the rules).

**Line 5: `from app.control_plane.decision import ControlPlaneDecision`**
*   **What it represents:** The **Final Verdict Form**. 
*   **Meaning:** This is the output that tells the rest of the factory what the Judge decided.

**Line 6: `from app.intake.schemas import PlatformRequest`**
*   **What it represents:** The **Standard Order Form** we learned about in Chapter 2.

**Line 7: `(Empty Line)`**

**Line 8: `class ControlPlaneCoordinator:`**
*   **What the computer does:** Defines the "Presiding Judge" role.

**Lines 9-12: `""" ... """`**
*   **Meaning:** A note explaining that this role orchestrates the "Governance Flow." (Governance is just factory-talk for "Making sure we follow the rules").

**Line 13: `(Empty Line)`**

**Line 14: `def __init__(self):`**
*   **What the computer does:** Prepares the courtroom.
*   **Meaning:** This runs the very first time we call a Judge to their bench.

**Lines 15-17: Initializing tools**
*   **What the computer does:** Hires the Validator, Risk Engine, and Policy Engine and keeps them standing by in the room.

**Line 18: `(Empty Line)`**

**Line 19: `def process_request(self, request: PlatformRequest) -> ControlPlaneDecision:`**
*   **What the computer does:** Defines the "Hearing."
*   **Input:** The order form (`PlatformRequest`).
*   **Output:** The final verdict (`ControlPlaneDecision`).

**Lines 20-22: `""" ... """`**
*   **Meaning:** A note explaining that this is the full, end-to-end process.

**Line 23: `# 1. Input Validation`**
*   **Meaning:** Comment: The first test—Is the paperwork dangerous?

**Line 24: `is_valid, reason = self.validator.validate_input(str(request.business_payload))`**
*   **What the computer does:** Hands the "Business Payload" (the transaction details) to the Inspector.
*   **Significance:** `str(...)` turns the data into a long string of text so the inspector can read it.

**Line 25: `if not is_valid:`**
*   **What the computer does:** Checks if the Inspector found anything scary.

**Line 26: `return ControlPlaneDecision(`**
*   **What the computer does:** If the inspector says "Danger!", the Judge ends the hearing immediately and fills out an "Emergency Block" form.

**Lines 27-31: Filling the "Emergency Block"**
*   **Meaning:** We set the status to "FAILED," give it a maximum Risk Score of 100, and write down the reason the inspector gave us.

**Line 32: `)`**
*   **What the computer does:** Closes the emergency form and sends it out.

**Line 33: `(Empty Line)`**

**Line 34: `# 2. Risk Scoring`**
*   **Meaning:** Comment: The second test—How much danger are we objectively in?

**Line 35: `risk_score = self.risk_engine.calculate_score(`**
*   **What the computer does:** Hands the data to the Math Expert.

---

### 🏁 Friendly Recap (Coordinator Part 1)

You've just seen the **Initial Security Screen** of our factory!

You now understand:
1.  How the **Coordinator** gathers all the experts in one room.
2.  How we **Security Scan** the input before we even look at the numbers.
3.  How the Judge can **Stop the Trial** immediately if the data looks malicious.

### A. Full File Ingestion: `app/control_plane/coordinator.py` (Final)

```python
36:             request.business_payload, 
37:             request.risk_metadata,
38:             request.customer_context
39:         )
40: 
41:         # 3. Policy Evaluation
42:         flags = []
43:         if request.business_payload.get("amount", 0) > 5000:
44:             flags.append("HIGH_VALUE_TRANSACTION")
45:             
46:         requires_review, policy_hits, allowed_actions = self.policy_engine.evaluate(
47:             risk_score, 
48:             flags
49:         )
50: 
51:         # 4. Final Decision Construction
52:         return ControlPlaneDecision(
53:             validation_status="SUCCESS",
54:             risk_score=risk_score,
55:             policy_hits=policy_hits,
56:             allowed_actions=allowed_actions,
57:             requires_review=requires_review
58:         )
59: 
```

### C. Line-by-Line Explanation (Final)

**Lines 36-38: Passing the details**
*   **What the computer does:** Tells the Math Expert everything it needs: what was bought, any old risk notes, and the customer's profile.
*   **Result:** The expert uses this to decide a number between 0 and 100.

**Line 39: `        )`**
*   **What the computer does:** Finishes the math calculation.

**Line 40: `(Empty Line)`**

**Line 41: `# 3. Policy Evaluation`**
*   **Meaning:** Comment: The final test—What does the Law Book say about this score?

**Line 42: `        flags = []`**
*   **What the computer does:** Starts a blank list of "Specific Rules" we might have broken.

**Line 43: `        if request.business_payload.get("amount", 0) > 5000:`**
*   **What the computer does:** Checks the price tag.
*   **Rule:** If the amount is over $5,000, we trigger a special alarm.

**Line 44: `            flags.append("HIGH_VALUE_TRANSACTION")`**
*   **What the computer does:** Adds the "High Value" alarm to our list.

**Line 45: `            `**
*   **What the computer does:** Extra spacing.

**Line 46: `        requires_review, policy_hits, allowed_actions = self.policy_engine.evaluate(`**
*   **What the computer does:** Asks the Law Expert to look at our Risk Score and our list of Alarms.
*   **Result:** The expert tells us: 1. If a human needs to look at it (`requires_review`), 2. Which rules we hit (`policy_hits`), and 3. What the robots are allowed to do next (`allowed_actions`).

**Lines 47-49: Inputs for the Law Expert**
*   **What the computer does:** Provides the math score and the flags we found.

**Line 50: `(Empty Line)`**

**Line 51: `# 4. Final Decision Construction`**
*   **Meaning:** Comment: Writing the Official Verdict.

**Line 52: `        return ControlPlaneDecision(`**
*   **What the computer does:** Starts filling out the final, official form.

**Lines 53-57: Filling the Verdict Form**
*   **What the computer does:** Records that the security scan passed ("SUCCESS"), writes down the math score, the list of rule hits, the allowed actions, and whether a human is needed.

**Line 58: `        )`**
*   **What the computer does:** Seals the envelope.

**Line 59: `(Empty Line)`**

---

### 🏁 Friendly Recap (Coordinator Completed!)

You have just mastered the **Brain of the Factory**!

You now understand:
1.  How the Judge **Orchestrates** three different experts.
2.  How we check for **High Value** transactions (>$5,000).
3.  How we produce a **Final Verdict** that coordinates the entire system.

### 4.2 policy.py – The Corporate Law Book

The **Policy Engine** is the literal "Law Book" of the Judge's Bench. It doesn't do any math; it just has a list of rules that say: "If the danger is X, then we must do Y."

### A. Full File Ingestion: `app/control_plane/policy.py`

```python
1: from typing import List, Tuple
2: 
3: class PolicyEngine:
4:     """
5:     Business boundary engine that maps risk scores to decisions.
6:     Migrated from legacy security/policy_engine.py.
7:     """
8:     
9:     def __init__(self, allow_threshold: float = 40.0, review_threshold: float = 75.0):
10:         self.allow_threshold = allow_threshold
11:         self.review_threshold = review_threshold
12: 
13:     def evaluate(self, risk_score: float, flags: List[str]) -> Tuple[bool, List[str], List[str]]:
14:         """
15:         Determines the governance outcome.
16:         Returns: (requires_review, policy_hits, allowed_actions)
17:         """
18:         policy_hits = []
19:         allowed_actions = []
20:         requires_review = False
21: 
22:         # 1. Hard flag logic (Priority)
23:         if "HIGH_VALUE_TRANSACTION" in flags:
24:             policy_hits.append("HIGH_VALUE_TRANSACTION")
25:             if risk_score > 50:
26:                 requires_review = True
27: 
28:         # 2. Score-based thresholds
29:         if risk_score >= self.review_threshold:
30:             requires_review = True
31:             policy_hits.append("RISK_SCORE_CRITICAL")
32:             allowed_actions = ["ESCALATE_TO_HUMAN", "BLOCK_TRANSACTION"]
33:         elif risk_score >= self.allow_threshold:
34:             requires_review = True
35:             policy_hits.append("RISK_SCORE_ELEVATED")
36:             allowed_actions = ["PROCEED_WITH_HUMAN_REVIEW", "INVESTIGATE_VIA_AI"]
37:         else:
38:             policy_hits.append("RISK_SCORE_NOMINAL")
39:             allowed_actions = ["AUTOMATE_APPROVAL", "LOG_AS_SAFE"]
40: 
41:         return requires_review, policy_hits, allowed_actions
42: 
```

### B. File Purpose
The `policy.py` file defines the **Safety Boundaries** for the entire factory. It takes the numeric Risk Score (0 to 100) and transforms it into business actions. It ensures that the AI never makes an expensive decision without a human checking the work if the risk is too high.

### C. Line-by-Line Explanation

**Line 1: `from typing import List, Tuple`**
*   **Purpose:** Standard organizational tools.

**Line 3: `class PolicyEngine:`**
*   **What the computer does:** Defines the role of the **Law Expert**.

**Line 9: `def __init__(self, allow_threshold: float = 40.0, review_threshold: float = 75.0):`**
*   **What the computer does:** Sets the "Danger Limits."
*   **Threshold 1 (40.0):** Anything below this is considered "Safe" and can be handled by robots.
*   **Threshold 2 (75.0):** Anything above this is considered "Critical" and needs a human immediately.

**Line 13: `def evaluate(self, risk_score: float, flags: List[str]) -> Tuple[bool, List[str], List[str]]:`**
*   **What the computer does:** Starts the Review.
*   **Input:** The risk score (math) and the flags (specific alarms).

**Line 18: `policy_hits = []`**
*   **Definition:** A notepad to write down which laws we triggered.

**Line 19: `allowed_actions = []`**
*   **Definition:** A notepad to write down what the robots are allowed to do.

**Line 20: `requires_review = False`**
*   **Definition:** A checkbox. By default, we assume a human isn't needed... until we find a reason.

**Line 23: `if "HIGH_VALUE_TRANSACTION" in flags:`**
*   **What the computer does:** Checks if the "Big Money" alarm was triggered by the Coordinator.

**Line 25: `if risk_score > 50:`**
*   **The Law:** If it's a "Big Money" deal AND the risk is even slightly high (>50), we must call a human.

**Line 29: `if risk_score >= self.review_threshold:`**
*   **What the computer does:** Checks if the risk is "CRITICAL" (>= 75).
*   **The Law:** If it is, the robots are ONLY allowed to Escalate to a Human or Block the deal.

**Line 33: `elif risk_score >= self.allow_threshold:`**
*   **What the computer does:** Checks if the risk is "ELEVATED" (>= 40).
*   **The Law:** If it's in this middle zone, we need a human, but we can also ask the AI to do a deeper "Investigation" first.

**Line 37: `else:`**
*   **What the computer does:** For anything below 40 ("NOMINAL").
*   **The Law:** The robots are allowed to **Automate Approval** and log the case as safe.

**Line 41: `return ...`**
*   **What the computer does:** Hands the Judge the final list of laws, actions, and the "Human Needed" checkbox status.

---

### 🏁 Friendly Recap (The Law Book)

You've just learned how to **Set Boundaries** for AI!

You now understand:
1.  How **Thresholds** (40 and 75) create "Safety Zones."
2.  How the Law Expert converts a "Scary Number" into a **List of Actions**.
3.  Why we use **Human-in-the-Loop** logic for any transaction that gets too risky.

### 4.3 risk.py – The Math Expert

If the Judge's Bench is a courtroom, then the **Risk Engine** is the expert accountant or mathematician. It looks at the numbers and calculated exactly how much danger we are in.

### A. Full File Ingestion: `app/control_plane/risk.py`

```python
1: from typing import Dict, Any, Optional
2: 
3: # Known trusted merchant categories for context scoring
4: TRUSTED_MERCHANT_PREFIXES = {"Office", "Grocery", "Pharmacy", "Gas", "Coffee", "Restaurant"}
5: 
6: class RiskEngine:
7:     """
8:     Deterministic risk scoring engine for financial transactions.
9:     Scores are based on payload signals, risk metadata, and context completeness.
10:     """
11:     
12:     def __init__(self, default_risk: float = 10.0):
13:         self.default_risk = default_risk
14: 
15:     def calculate_score(
16:         self,
17:         business_payload: Dict[str, Any],
18:         risk_metadata: Dict[str, Any],
19:         customer_context: Optional[Dict[str, Any]] = None
20:     ) -> float:
21:         """
22:         Calculates a risk score (0-100) based on payload, metadata, and context signals.
23:         Higher score = higher risk.
24:         """
25:         score = risk_metadata.get("last_fraud_score", self.default_risk)
26:         
27:         # 1. Transaction Amount logic
28:         amount = business_payload.get("amount", 0.0)
29:         if amount > 10000.0:
30:             score += 50.0  # High value penalty
31:         elif amount > 1000.0:
32:             score += 20.0  # Moderate value penalty
33:             
34:         # 2. Velocity / Metadata signals
35:         if risk_metadata.get("velocity_flags", 0) > 2:
```

*(Note: File stops at line 35 of 55 for this segment. Remaining lines will follow in the next segment.)*

### B. File Purpose
The `risk.py` file is the **Scoring Department**. It looks at things like the amount of money, how often the customer is shopping, and how old their account is to calculate a final "Danger Score" from 0 to 100.

### C. Line-by-Line Explanation

**Line 1: `from typing import Dict, Any, Optional`**
*   **Purpose:** Organization labels.

**Line 4: `TRUSTED_MERCHANT_PREFIXES = {"Office", "Grocery", "Pharmacy", "Gas", "Coffee", "Restaurant"}`**
*   **What it represents:** The **"Safe Shops" list**. 
*   **Meaning:** If a customer is buying coffee or groceries, it's usually less scary than if they are buying $10,000 worth of gift cards at a random shop.

**Line 6: `class RiskEngine:`**
*   **What the computer does:** Defines the role of the **Math Expert**.

**Line 12: `def __init__(self, default_risk: float = 10.0):`**
*   **Purpose:** The "Base Fear." 
*   **Meaning:** Even in a perfect transaction, we start with a risk of 10.0 because there is always a *tiny* chance of a problem.

**Line 15: `def calculate_score(...)`**
*   **What the computer does:** Starts the math calculation.
*   **Inputs:** Business details, risk notes, and customer history.

**Line 25: `score = risk_metadata.get("last_fraud_score", self.default_risk)`**
*   **What the computer does:** Looks at the customer's *previous* score. If they were suspicious yesterday, we start with that high number today.

**Line 27: `# 1. Transaction Amount logic`**
*   **Meaning:** Comment: The first math rule—Big money equals big risk.

**Lines 29-32: Adding "Money Penalties"**
*   **The Rule:** 
    *   Over $10,000? Add **50 points** of danger.
    *   Over $1,000? Add **20 points** of danger.

**Line 34: `# 2. Velocity / Metadata signals`**
*   **Meaning:** Comment: The second math rule—Is the customer acting too fast?

**Line 35: `if risk_metadata.get("velocity_flags", 0) > 2:`**
*   **Definition:** "Velocity" is how many transactions happen in a short time. 
*   **The Rule:** If they have more than 2 "Velocity Flags" (too many transactions in an hour), it's highly suspicious.

---

### 🏁 Friendly Recap (Risk Part 1)

You've just learned how to **Calculate Danger** like a bank analyst!

You now understand:
1.  How we use **Trusted Prefixes** to identify "Safe Shops."
2.  Why we start with a **Default Risk** of 10.0 (Safety first!).
3.  How **Large Amounts** and **High Velocity** automatically change our math score.

### A. Full File Ingestion: `app/control_plane/risk.py` (Final)

```python
36:             score += 30.0
37:             
38:         # 3. New Account logic
39:         if business_payload.get("account_age_days", 365) < 30:
40:             score += 15.0
41: 
42:         # 4. Missing context penalty — empty context = unknown risk
43:         context = customer_context or {}
44:         if not context or not context.get("customer_id"):
45:             score += 25.0  # Cannot automate without known customer context
46: 
47:         # 5. Unknown merchant penalty — unknown merchants are treated conservatively
48:         merchant = business_payload.get("merchant", "")
49:         is_trusted = any(merchant.startswith(prefix) for prefix in TRUSTED_MERCHANT_PREFIXES)
50:         if not is_trusted and merchant:
51:             score += 15.0
52: 
53:         # Cap at 100
54:         return min(max(score, 0.0), 100.0)
55: 
```

### C. Line-by-Line Explanation (Final)

**Line 36: `score += 30.0`**
*   **What the computer does:** Slaps a heavy 30-point penalty on the transaction if the velocity is too high.

**Line 38: `# 3. New Account logic`**
*   **Meaning:** Comment: The third math rule—New customers are riskier than old friends.

**Line 39: `if business_payload.get("account_age_days", 365) < 30:`**
*   **What the computer does:** Checks how old the account is.
*   **The Rule:** If the account is less than 30 days old, add **15 points** of danger.

**Line 42: `# 4. Missing context penalty`**
*   **Meaning:** Comment: The fourth math rule—If we don't know who you are, we don't trust you.

**Line 43: `context = customer_context or {}`**
*   **What the computer does:** Checks the Research Folder for the customer's history.

**Line 44: `if not context or not context.get("customer_id"):`**
*   **What the computer does:** Looks for a "Customer ID."
*   **The Rule:** If the ID is missing, we add **25 points** of danger. We can't safely automate a transaction for a "Ghost."

**Line 47: `# 5. Unknown merchant penalty`**
*   **Meaning:** Comment: The fifth math rule—Is this a shop we know?

**Line 49: `is_trusted = any(merchant.startswith(prefix) for prefix in TRUSTED_MERCHANT_PREFIXES)`**
*   **What the computer does:** Checks the merchant's name against our "Safe Shops" list from the start of the file.

**Line 50: `if not is_trusted and merchant:`**
*   **The Rule:** If the shop is NOT on the safe list, add **15 points** of danger.

**Line 54: `return min(max(score, 0.0), 100.0)`**
*   **What the computer does:** The "Safety Net." 
*   **Meaning:** Even if we find a million reasons to be scared, the maximum score we can give is 100. If we find zero reasons and the score is below zero, we pull it back up to 0.

---

### 🏁 Friendly Recap (Risk Engine Completed!)

You've just witnessed the **Analytical Brain** of a financial giant!

You now understand:
1.  How **Account Age** affects trust.
2.  Why **Anonymous Transactions** (missing IDs) are treated as high risk.
3.  How we use **Capping** (0 to 100) to keep our data neat and predictable.

### 4.4 validator.py – The Document Inspector

The **Control Plane Validator** is the final layer of our security screening. Think of it as the **X-Ray Scanner** at an airport. It doesn't care about the money or the math; it only cares if you are carrying "Contraband"—like malicious code or private secrets.

### A. Full File Ingestion: `app/control_plane/validator.py`

```python
1: import re
2: from typing import Tuple
3: 
4: class ControlPlaneValidator:
5:     """
6:     Sanity and Security layer for the Control Plane.
7:     Checks for prompt injection, sensitive data leakage, and MITRE ATLAS patterns.
8:     """
9:     
10:     @staticmethod
11:     def validate_input(content: str) -> Tuple[bool, str]:
12:         """
13:         Scan input for malicious patterns or policy violations.
14:         """
15:         # Basic injection detection
16:         injection_patterns = [
17:             r"ignore previous instructions",
18:             r"system prompt",
19:             r"override policy",
20:             r"ignore all amex protocols",
21:             r"bypass.*tool",
22:             r"internal system credentials",
23:             r"print.*account balance",
24:         ]
25:         for pattern in injection_patterns:
26:             if re.search(pattern, content, re.IGNORECASE):
27:                 return False, f"Rule Violation: Potential malicious pattern detected ('{pattern}')"
28: 
29:         # Check for PII or sensitive patterns in intake
30:         sensitive_patterns = [r"ssn", r"password", r"secret_key"]
31:         for pattern in sensitive_patterns:
32:             if re.search(pattern, content.lower(), re.IGNORECASE):
33:                 return False, "Privacy Violation: Sensitive PII detected in input"
34: 
35:         return True, "Success"
36: 
37:     @staticmethod
38:     def validate_output(result: str) -> Tuple[bool, str]:
39:         """
40:         Scan agent output for sensitive data leakage.
41:         """
42:         sensitive_patterns = [r"ssn", r"password", r"secret_key"]
43:         for pattern in sensitive_patterns:
44:             if re.search(pattern, result.lower(), re.IGNORECASE):
45:                 return False, "Data Leakage: Sensitive patterns detected in output"
46:         
47:         return True, "Success"
48: 
```

### B. File Purpose
The `validator.py` file is our **Security Guard**. Its job is twofold:
1.  **Stop "Hackers":** It blocks anyone trying to trick the AI with commands like "Ignore your rules."
2.  **Protect Privacy:** It makes sure no one accidentally sends a password or a Social Security Number (SSN) into our system, and it makes sure the AI doesn't accidentally reveal them back to the user.

### C. Line-by-Line Explanation

**Line 1: `import re`**
*   **Definition:** "RE" stands for **Regular Expressions**. 
*   **Meaning:** This is a high-powered search tool that lets the computer look for specific "Shapes" of text (like "anything that looks like an email address").

**Line 4: `class ControlPlaneValidator:`**
*   **What the computer does:** Defines the role of the **Document Inspector**.

**Line 10: `@staticmethod`**
*   **Meaning:** This is a technical tag that means: "This tool is a standalone machine. You don't need to 'prepare the courtroom' (initialize) to use it."

**Line 11: `def validate_input(content: str) -> Tuple[bool, str]:`**
*   **What the computer does:** Starts the "Input Scan."

**Lines 16-24: `injection_patterns = [...]`**
*   **What it represents:** The **"Most Wanted" list**. 
*   **Meaning:** These are common tricks people use to try and "Brainwash" an AI (called Prompt Injection). We are literally looking for phrases like "ignore previous instructions."

**Line 25: `for pattern in injection_patterns:`**
*   **What the computer does:** Checks the transaction details against every single trick on our "Most Wanted" list.

**Line 27: `return False, f"Rule Violation: ..."`**
*   **The Result:** If we find a match, the Inspector shouts "Stop!" and records exactly which trick was tried.

**Line 30: `sensitive_patterns = [r"ssn", r"password", r"secret_key"]`**
*   **What it represents:** The **Privacy Shield**. 
*   **Meaning:** We are looking for "Sensitive PII" (Personally Identifiable Information) like Social Security Numbers.

**Line 33: `return False, "Privacy Violation: ..."`**
*   **The Result:** If a user tries to send a password into the AI, we stop them for their own safety.

**Line 38: `def validate_output(result: str) -> Tuple[bool, str]:`**
*   **What it represents:** The **Exit Scan**.
*   **Importance:** Even if the input was safe, we check the AI's *answer* before showing it to the customer. We want to make sure the AI doesn't accidentally "leak" a secret key it was using internally.

---

### 🏁 Friendly Recap (Chapter 4 Completed!)

Give yourself a high-five! You've just explored the **Highest Security Room** in the factory.

In this chapter, you learned:
1.  How the **Coordinator** manages the entire trial.
2.  How the **Law Book** (`policy.py`) defines the safety thresholds.
3.  How the **Math Expert** (`risk.py`) calculates the danger score.
4.  How the **Scanner** (`validator.py`) blocks hackers and protects privacy.

### 4.5 decision.py – The Final Verdict Paperwork

If the Judge is going to send a decision to the rest of the factory, they can't just shout it across the hall. They need a formal **Verdict Form** so that the Robots in the next room know exactly what they are allowed to do.

### A. Full File Ingestion: `app/control_plane/decision.py`

```python
1: from pydantic import BaseModel, Field
2: from typing import List, Optional
3: 
4: class ControlPlaneDecision(BaseModel):
5:     """
6:     The deterministic output of the Control Plane.
7:     This contract governs whether the request proceeds to the intelligent agentic layer.
8:     """
9:     validation_status: str = Field(..., description="SUCCESS or FAILED")
10:     risk_score: float = Field(..., ge=0, le=100, description="Normalized risk score (0-100)")
11:     policy_hits: List[str] = Field(default_factory=list, description="List of specific corporate policies triggered")
12:     allowed_actions: List[str] = Field(default_factory=list, description="Actions the system is permitted to take based on policy")
13:     requires_review: bool = Field(default=False, description="Whether human-in-the-loop intervention is mandatory")
14:     block_reason: Optional[str] = Field(None, description="Reason for blocking, if validation_status is FAILED")
15: 
16:     model_config = {
17:         "json_schema_extra": {
18:             "example": {
19:                 "validation_status": "SUCCESS",
20:                 "risk_score": 15.5,
21:                 "policy_hits": ["HIGH_VALUE_TRANSACTION"],
22:                 "allowed_actions": ["PROCEED_TO_AI_INVESTIGATION", "LOG_AUDIT"],
23:                 "requires_review": False
24:             }
25:         }
26:     }
```

### B. File Purpose
The `decision.py` file defines the **Official Template** for every decision the Judge makes. Because it uses **Pydantic** (just like the Order Form in Chapter 2), it ensures that the Judge never "forgets" to fill in a required box, like the risk score or the allowed actions.

### C. Line-by-Line Explanation

**Line 1: `from pydantic import BaseModel, Field`**
*   **Purpose:** The standard "Smart Form" construction kit.

**Line 4: `class ControlPlaneDecision(BaseModel):`**
*   **What it represents:** The **Official Verdict Form** template.

**Line 9: `validation_status: str = Field(..., description="SUCCESS or FAILED")`**
*   **Meaning:** The very first box. Did the security scan pass?

**Line 10: `risk_score: float = Field(..., ge=0, le=100...)`**
*   **The Labels:** `ge=0` (Greater than or Equal to 0) and `le=100` (Less than or Equal to 100).
*   **Why it exists:** This prevents the Math Expert from accidentally writing "150%" or "-5" on the form. It enforces the 0-100 scale.

**Line 11: `policy_hits: List[str] ...`**
*   **Meaning:** A list of every law the transaction triggered.

**Line 12: `allowed_actions: List[str] ...`**
*   **Meaning:** The "Handcuffs" or "Keys." This tells the Robots what they are actually allowed to do (e.g., "You can investigate, but you cannot spend money").

**Line 13: `requires_review: bool ...`**
*   **Meaning:** The "Human Needed" checkbox.

**Line 14: `block_reason: Optional[str] ...`**
*   **Meaning:** If the Judge says "FAILED," they must write a short note here explaining why.

**Lines 16-25: `model_config` and `example`**
*   **Purpose:** The "Cheat Sheet." It shows developers exactly what a perfectly filled-out verdict looks like.

---

### 🏁 Friendly Recap (Verdict Paperwork)

You've just learned how the Judge communicates with the factory!

You now understand:
1.  How **Pydantic** ensures the verdict is complete and accurate.
2.  How we enforce the **0-100 Risk Scale** right on the form.
3.  Why **Allowed Actions** are crucial for keeping the AI bounded.

### 4.6 policy_loader.py – Opening and Reading the Laws

The Judge doesn't memorize every single law. Instead, they have a **Law Book** sitting on their desk. The `policy_loader.py` file is the Judge's "Eyes"—it’s the tool that opens the book, reads the settings, and makes sure they are up-to-date.

### A. Full File Ingestion: `app/control_plane/policy_loader.py`

```python
1: # risk/policy_loader.py
2: import sys
3: import yaml
4: import os
5: 
6: 
7: def load_policy():
8:     policy_path = os.path.abspath(
9:         os.path.join(os.path.dirname(__file__), "..", "config", "policy.yaml")
10:     )
11: 
12:     if not os.path.exists(policy_path):
13:         print(f"[!] Warning: policy.yaml not found at {policy_path}")
14:         return {}
15: 
16:     with open(policy_path, "r") as f:
17:         try:
18:             return yaml.safe_load(f) or {}
19:         except yaml.YAMLError as e:
20:             print(f"[!] Error parsing policy.yaml: {e}")
21:             return {}
22: 
23: 
24: POLICY = load_policy()
```

### B. File Purpose
The `policy_loader.py` file is the **Bridge** between a simple text file (`policy.yaml`) and the Python code. It allows us to change the bank's rules (like lowering the risk threshold) without having to rewrite any code. We just update the text file, and this loader handles the rest.

### C. Line-by-Line Explanation

**Line 3: `import yaml`**
*   **Definition:** **YAML** is a human-friendly format for writing lists and settings. 
*   **Meaning:** This library lets the computer understand the "Lists" we write in our configuration files.

**Line 7: `def load_policy():`**
*   **What it represents:** The "Fetch" action.

**Lines 8-10: Finding the path**
*   **What the computer does:** Calculates exactly where the `policy.yaml` file is hidden in the building (inside the `app/config/` folder).
*   **Significance:** `os.path.abspath` and `os.path.join` are tools that help the computer find files correctly whether it's running on Windows, Mac, or Linux.

**Line 12: `if not os.path.exists(policy_path):`**
*   **Purpose:** Safety Check. What if someone deleted the law book?
*   **The Result:** If the book is missing, the Judge prints a warning and returns an empty list (`{}`).

**Line 16: `with open(policy_path, "r") as f:`**
*   **What the computer does:** Physically "Opens" the file in "Read" (`"r"`) mode.

**Line 18: `return yaml.safe_load(f) or {}`**
*   **What the computer does:** Reads the human-friendly YAML lists and turns them into a "Dictionary" (the computer's version of a list) that Python can understand.

**Lines 19-21: `except yaml.YAMLError as e:`**
*   **What the computer does:** If there is a "Typo" in the file that makes it unreadable, the computer catches the error and stays calm instead of crashing.

**Line 24: `POLICY = load_policy()`**
*   **What the computer does:** Actually triggers the search and storage. 
*   **Importance:** Now, any other file in the courtroom can just say `import POLICY` to see the current laws of the land.

---

### 🏁 Friendly Recap (The Law Reader)

You've just learned how to keep your AI **Flexible**!

You now understand:
1.  How **YAML** lets humans write rules easily.
2.  How the computer **Locates** files in different folders.
3.  How we use **Safety Checks** to prevent the system from crashing if a file is missing or contains a typo.

### 4.7 scoring_engine.py – The Math Behind the Risk

The `scoring_engine.py` is the **Heart of the Math Expert**. While the `risk.py` file we saw earlier handles the general transaction data, this file specifically looks at how to translate **AI Logic** and **Legacy Bank Rules** into a single, clean number.

### A. Full File Ingestion: `app/control_plane/scoring_engine.py`

```python
1: from risk.policy_loader import POLICY
2: import json
3: 
4: 
5: def calculate_risk_score(transaction_data: dict, result_text: str) -> int:
6:     account_id = str(transaction_data.get("account_id", "")).lower()
7:     amount = float(transaction_data.get("amount", 0))
8:     result_text = result_text.lower()
9: 
10:     # Load defaults and limits
11:     global_limits = POLICY.get("global_limits", {})
12:     risk_score = global_limits.get("default_risk_score", 10)
13: 
14:     # 1. Global transaction limit
15:     if amount >= global_limits.get("max_transaction_amount", 100000.0):
16:         risk_score += 80
17: 
18:     # 2. Account risk rules
19:     account_risk = POLICY.get("account_risk", {})
20:     if account_id in account_risk:
21:         risk_score += account_risk[account_id]
22: 
23:     # 2.5 Deterministic keyword rules
24:     if "suspicious" in result_text:
25:         risk_score += 40
26: 
27:     # 3. AI Structured Signals (Lowest priority additive penalties)
28:     # Parse the strictly formatted JSON output
29:     try:
30:         # Strip potential markdown output (e.g. ```json ... ```)
31:         clean_text = result_text.strip()
32:         if clean_text.startswith("```json"):
33:             clean_text = clean_text[7:]
34:         elif clean_text.startswith("```"):
35:             clean_text = clean_text[3:]
```

*(Note: File stops at line 35 of 69 for this segment. Remaining lines will follow in the next segment.)*

### B. File Purpose
The `scoring_engine.py` is responsible for **Data Normalization**. It takes messy information—like the text an AI wrote or a customer's ID—and converts it into a standardized score. Think of it as a "Scale" that weighs all the different danger signals together.

### C. Line-by-Line Explanation

**Line 1: `from risk.policy_loader import POLICY`**
*   **What it does:** Brings in the **Law Book** we just learned to load.

**Line 2: `import json`**
*   **Meaning:** Brings in the tool used to read "Computer Packages" (JSON objects).

**Line 5: `def calculate_risk_score(...)`**
*   **Purpose:** The main calculation action. 
*   **Input:** The raw transaction data and the text written by the AI robots.

**Line 11: `global_limits = POLICY.get("global_limits", {})`**
*   **What the computer does:** Reaches into the Law Book and finds the "Big System Limits" (like the maximum transaction allowed for *anyone*).

**Line 12: `risk_score = global_limits.get("default_risk_score", 10)`**
*   **Meaning:** Starts with the default "Safety Penalty" of 10 points.

**Line 15: `if amount >= global_limits.get("max_transaction_amount", 100000.0):`**
*   **The Rule:** If a transaction is over $100,000, we add a massive **80-point** penalty immediately. That’s too much money for an automated system!

**Line 20: `if account_id in account_risk:`**
*   **Meaning:** Checks the "Blacklist." If this specific customer has a history of problems, we add their personal risk penalty to the score.

**Line 24: `if "suspicious" in result_text:`**
*   **The Keyword Scan:** If the AI robot even *mentions* the word "suspicious" in its report, we add **40 points** of danger.

**Lines 31-35: Cleaning the AI's "Handwriting"**
*   **What the computer does:** Sometimes AI robots write their answers between triple backticks (```). This code "strips" those extra marks away so we can read the raw data inside.

---

### 🏁 Friendly Recap (Scoring Engine Part 1)

You've just learned how to **Listen to AI Alarms**!

You now understand:
1.  How the engine uses **Global Limits** to stop massive transactions.
2.  How the **Blacklist** (account risk) allows us to be extra careful with specific customers.
3.  How we **Clean Data** so that the computer can read AI reports accurately.

### A. Full File Ingestion: `app/control_plane/scoring_engine.py` (Final)

```python
36:         if clean_text.endswith("```"):
37:             clean_text = clean_text[:-3]
38: 
39:         analysis = json.loads(clean_text)
40:         risk_level = analysis.get("risk_level", "low").lower()
41:         action = analysis.get("recommended_action", "approve").lower()
42: 
43:         # Apply AI Risk Policy Additions
44:         ai_signals = POLICY.get("ai_signals_penalty", {})
45: 
46:         if risk_level == "high":
47:             risk_score += ai_signals.get("severe risk", 40)
48: 
49:         if action in ["freeze", "deny"]:
50:             risk_score += ai_signals.get("freeze", 30)
51: 
52:     except json.JSONDecodeError:
53:         print(
54:             "[!] Risk Engine Warning: AI failed to return valid JSON. Falling back to textual parsing."
55:         )
56:         # Graceful fallback: legacy textual parsing
57:         ai_signals = POLICY.get("ai_signals_penalty", {})
58:         for signal, penalty in ai_signals.items():
59:             if signal in result_text.lower():
60:                 risk_score += penalty
61: 
62:     # Cap risk score at 100
63:     risk_score = min(risk_score, 100)
64: 
65:     # 4. Convert Risk Score back to frontend Compliance Score (higher = better)
66:     compliance_score = max(100 - risk_score, 0)
67: 
68:     return compliance_score
69: 
```

### C. Line-by-Line Explanation (Final)

**Line 39: `analysis = json.loads(clean_text)`**
*   **What the computer does:** Turns the cleaned text into a digital "Package" of information that we can easily search.

**Line 40: `risk_level = analysis.get("risk_level", "low").lower()`**
*   **What the computer does:** Checks what the AI robot said about the "Risk Level." If the AI forgot to say, we assume "low" for now.

**Line 41: `action = analysis.get("recommended_action", "approve").lower()`**
*   **What the computer does:** Checks what the AI robot recommended we do with the money.

**Line 44: `ai_signals = POLICY.get("ai_signals_penalty", {})`**
*   **What the computer does:** Reaches into the Law Book and finds the "AI Penalty List."

**Lines 46-47: Severe Risk Logic**
*   **The Rule:** If the AI specifically says risk is "high," add **40 points** of danger.

**Lines 49-50: Freeze/Deny Logic**
*   **The Rule:** If the AI recommends "freezing" or "denying" the account, add **30 points** of danger.

**Lines 52-55: `except json.JSONDecodeError:`**
*   **The Safety Net:** If the AI robot writes something the computer can't understand (garbage text), the code prints a warning and stays running.

**Lines 57-60: Legacy Fallback**
*   **What the computer does:** If the JSON parsing failed, the computer just does a simple "Word Search" for our penalty keywords like "severe risk" or "freeze" in the text.

**Line 63: `risk_score = min(risk_score, 100)`**
*   **The Cap:** Makes sure the score never goes above 100%.

**Line 66: `compliance_score = max(100 - risk_score, 0)`**
*   **The Flip:** This is a neat trick! Humans like high scores (like 100/100 on a test). But for Risk, a 100 is bad. 
*   **Meaning:** We subtract the Risk Score from 100 to get a **Compliance Score**. 
    *   0% Risk = **100% Compliance** (Great!)
    *   100% Risk = **0% Compliance** (Very Bad!)

**Line 68: `return compliance_score`**
*   **What the computer does:** Hands the final score to the Judge.

---

### 🏁 Friendly Recap (Scoring Engine Completed!)

You've just learned how to **Listen to AI Insights**!

You now understand:
1.  How we use **Structured Data** (JSON) to get precise answers from AI.
2.  How we have a **Fallback Plan** if the AI acts weird.
3.  Why we **Flip the Score** to make it easier for humans to read.

### 4.8 scoring_engine_pattern.py – A Blueprint for Future Judges

As our factory grows, we might need different Judges for different countries or different departments. The `scoring_engine_pattern.py` file is the **Master Blueprint**. It shows exactly how every scoring engine should be built so that we never forget the safety rules.

### A. Full File Ingestion: `app/control_plane/scoring_engine_pattern.py`

```python
1: from risk.policy_loader import POLICY
2: import json
3: 
4: 
5: def calculate_risk_score(transaction_data: dict, result_text: str) -> int:
6:     """A production-grade, additive risk scoring engine pattern."""
7:     risk_score = POLICY.get("global_limits", {}).get("default_risk_score", 10)
8: 
9:     # 1. Deterministic Hard Rules (Highest Priority Penalties)
10:     amount = float(transaction_data.get("amount", 0))
11:     if amount >= POLICY.get("global_limits", {}).get(
12:         "max_transaction_amount", 100000.0
13:     ):
14:         risk_score += 80  # Don't return, penalize heavily
15: 
16:     # 2. Account Risk Overrides (Additive)
17:     account_id = str(transaction_data.get("account_id", "")).lower()
18:     risk_score += POLICY.get("account_risk", {}).get(account_id, 0)
19: 
20:     # 3. Textual Keyword Deterministic Triggers
21:     if "suspicious" in result_text.lower():
22:         risk_score += 40
23: 
24:     # 4. AI Structured Signals (Lowest Priority)
25:     try:
26:         clean_text = (
27:             result_text.strip().removeprefix("```json").removesuffix("```").strip()
28:         )
29:         analysis = json.loads(clean_text)
30:         if analysis.get("risk_level", "low").lower() == "high":
31:             risk_score += POLICY.get("ai_signals_penalty", {}).get("severe risk", 40)
32:         if analysis.get("recommended_action", "approve").lower() in ["freeze", "deny"]:
33:             risk_score += POLICY.get("ai_signals_penalty", {}).get("freeze", 30)
34:     except json.JSONDecodeError:
35:         pass  # Optional: fallback logic here
36: 
37:     return max(100 - min(risk_score, 100), 0)
38: 
```

### B. File Purpose
The `scoring_engine_pattern.py` file is a **Reference Guide**. It doesn't have all the complex fallback logic of the main engine, but it shows the "Skeleton" of how risk scoring works. It's used to make sure that even if a new developer joins the factory, they know the 4-step process:
1.  Check hard rules.
2.  Check the account history.
3.  Check keywords.
4.  Check AI signals.

### C. Line-by-Line Explanation

**Lines 5-7: The Standard Start**
*   **What it does:** Every Judge starts the hearing the same way: by getting the default risk from the Law Book.

**Lines 9-14: Step 1 - Hard Rules**
*   **Significance:** Hard rules are non-negotiable. If you spend too much money, you get a penalty, no matter who you are.

**Lines 16-18: Step 2 - Account History**
*   **Significance:** We always check if we've seen this person before and if they were problematic in the past.

**Lines 20-22: Step 3 - Keyword Scan**
*   **Significance:** We always scan the report for red-flag words like "suspicious."

**Lines 24-35: Step 4 - AI Structured Signals**
*   **What the computer does:** Uses a very clean, "One-Liner" approach (`removeprefix(...).removesuffix(...)`) to clean the AI's data.
*   **Purpose:** This shows a more modern, compact way to do the data cleaning compared to the longer version we saw earlier.

**Line 37: `return max(100 - min(risk_score, 100), 0)`**
*   **What the computer does:** Performs the final "Flip" to turn Risk into Compliance in one single, elegant mathematical line.

---

### 🏁 Friendly Recap (Chapter 4 Completed!)

Give yourself a massive round of applause! You've just finished exploring the **Judge's Bench**—the brain of our entire factory.

In this chapter, you learned:
1.  How the **Coordinator** manages the entire trial.
2.  How the **Policy Engine** and **Loader** handle the bank's rules.
3.  How the **Risk Engine** and **Scoring Engines** calculate the exact amount of danger.
4.  How we use **Pydantic** to create a foolproof **Verdict Form** (`decision.py`).

**The Judge has spoken. The paperwork is filed. The barriers are set. Now, how do we actually get the work done? In the next chapter, we're heading to the "Traffic Tower" to see how we plan the mission!**
