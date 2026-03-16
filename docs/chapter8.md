# Chapter 8: The Safety Inspectors (The `app/review/` Layer)

## 1️⃣ Big Picture: The Safety Inspectors

In the previous chapters, our robots did all the hard work. They investigated transactions, checked credit scores, and decided if someone was trying to commit fraud. But even the smartest robots can make mistakes. Sometimes, a transaction is so complex or so expensive that we need a **Human** to double-check the work.

Meet the **Safety Inspectors**.

Think of this as the "High Alert" room in the factory. When our robots reach a 50/50 decision or a "REVIEW" verdict, they don't just guess. Instead, they package up all their notes and send them to a human expert.

In this chapter, we’ll meet the tools that manage this logic:
1.  **The Paperwork (`models.py`)**: The structured forms used for human decisions and overrides.
2.  **The Evidence Briefing (`packet.py`)**: Assembles all the robot notes into one easy-to-read document for the human.
3.  **The Waiting Room (`queue.py`)**: A list of all cases waiting for a human's attention.
4.  **The Inspector General (`coordinator.py`)**: The master controller who manages the whole review flow.
5.  **The Verdict Stamper (`approval.py`)**: Converts a human's "Yes/No" into a final computerized action.
6.  **The Disagreement Log (`overrides.py`)**: Keeps track of every time a human disagrees with a robot.

---

## 2️⃣ Teach the Code

### 8.1 models.py – The Inspector's Paperwork

Before an inspector can look at a case, we need a standard way to write down the facts. The `models.py` file defines the "Report Cards" and "Decision Forms" used in this layer.

### A. Full File Ingestion: `app/review/models.py`

```python
1: from pydantic import BaseModel, Field
2: from typing import List, Dict, Any, Optional
3: from datetime import datetime
4: 
5: class ReviewPacket(BaseModel):
6:     """
7:     Structured evidence packet for human review.
8:     Contains everything a human needs to make an informed decision.
9:     """
10:     review_id: str
11:     request_id: str
12:     strategy_selected: str
13:     risk_score: float
14:     policy_hits: List[str]
15:     requires_review_reason: str
16:     request_summary: str
17:     agent_recommendation: str
18:     supporting_evidence: List[str]
19:     context_completeness_score: float
20:     suggested_next_action: str
21:     created_at: datetime = Field(default_factory=datetime.utcnow)
22: 
23: class ReviewDecision(BaseModel):
24:     """
25:     Captured decision from a human reviewer.
26:     """
27:     review_id: str
28:     reviewer_name: str
29:     decision: str  # APPROVE, REJECT, SEND_BACK, OVERRIDE
30:     decision_reason: str
31:     notes: Optional[str] = None
32:     approved_action: str
33:     timestamp: datetime = Field(default_factory=datetime.utcnow)
34: 
35: class OverrideRecord(BaseModel):
36:     """
37:     Explicit log of a reviewer overriding a system recommendation.
38:     """
39:     review_id: str
40:     system_recommendation: str
41:     reviewer_decision: str
42:     override_reason: str
43:     impact_level: str = "MEDIUM" # LOW, MEDIUM, HIGH
44: 
45: class ReviewQueueItem(BaseModel):
46:     """
47:     Metadata for tracking a case in the review queue.
48:     """
49:     review_id: str
50:     request_id: str
51:     status: str = "PENDING" # PENDING, IN_REVIEW, CLOSED
52:     priority: int = 1 # 1 (High) to 3 (Low)
53:     assigned_to: Optional[str] = None
54: 
```

### B. File Purpose
The `models.py` file ensures that human investigations are **Standardized**. It defines four types of paperwork:
*   **ReviewPacket**: The "Briefing Folder" full of facts.
*   **ReviewDecision**: The "Final Verdict" signed by the human.
*   **OverrideRecord**: The "Disagreement Form" filled out if the human overrides the robot.
*   **ReviewQueueItem**: The "Sticky Note" used to track where a case is in the queue.

### C. Line-by-Line Explanation

**Lines 1-3: The Toolbox**
*   **What it does:** Brings in our usual Pydantic and formatting tools.

**Line 5: `ReviewPacket`**
*   **Meaning:** This is the massive **Folder of Evidence**.
*   **Line 13 (`risk_score`):** Includes the score from the Risk Engine.
*   **Line 18 (`supporting_evidence`):** Lists the specific books used from the Research Library.

**Line 23: `ReviewDecision`**
*   **Meaning:** This is the **Verdict Form**.
*   **Line 29 (`decision`):** The human picks one: Approve, Reject, Send Back, or Override.
*   **Line 30 (`decision_reason`):** The human *must* explain why they chose that.

**Line 35: `OverrideRecord`**
*   **Meaning:** This is a special log. If the robot said "BLOCK" but the human says "ALLOW," we use this form to track *why* the human disagreed with the machine. This helps us train our robots to be smarter!

**Line 45: `ReviewQueueItem`**
*   **Meaning:** A simple status tracker.
*   **Line 51 (`status`):** Tells us if the case is still "PENDING" or if a human is currently looking at it.

---

### 8.2 packet.py – The Evidence Briefing

Now that we have the blank forms, how do we fill them out? The `packet.py` file is the **Briefing Assistant**. Its job is to gather data from the Intake layer, the Library, the Control Plane, and the Robots, and squish them all into one `ReviewPacket`.

### A. Full File Ingestion: `app/review/packet.py`

```python
1: import uuid
2: from typing import List, Dict, Any
3: from app.review.models import ReviewPacket
4: from app.intake.schemas import PlatformRequest
5: from app.context.models import ContextPacket
6: from app.control_plane.decision import ControlPlaneDecision
7: from app.agents.models import AnalystOutput
8: 
9: class ReviewPacketBuilder:
10:     """
11:     Assembles a ReviewPacket from disparate platform state objects.
12:     """
13:     
14:     def build_packet(
15:         self, 
16:         request: PlatformRequest, 
17:         context: ContextPacket, 
18:         decision: ControlPlaneDecision,
19:         agent_findings: List[Dict[str, Any]],
20:         reason: str
21:     ) -> ReviewPacket:
22:         """
23:         Creates a clean, reviewer-friendly summary of the case state.
24:         """
25:         review_id = f"REV-{str(uuid.uuid4())[:8].upper()}"
26:         
27:         # 1. Summarize Agent Findings
28:         primary_recommendation = "No recommendation provided"
29:         if agent_findings:
30:             # Assume last agent output contains the high-level recommendation
31:             last_result = agent_findings[-1]
32:             if "recommended_path" in last_result:
33:                 primary_recommendation = last_result["recommended_path"]
34:             elif "final_recommendation" in last_result:
35:                 primary_recommendation = last_result["final_recommendation"]
36: 
37:         # 2. Extract evidence snippets
38:         evidence_titles = [e.title for e in context.evidence]
39:         
40:         return ReviewPacket(
41:             review_id=review_id,
42:             request_id=request.request_id,
43:             strategy_selected=decision.validation_status,
44:             risk_score=decision.risk_score,
45:             policy_hits=decision.policy_hits,
46:             requires_review_reason=reason,
47:             request_summary=context.request_summary,
48:             agent_recommendation=primary_recommendation,
49:             supporting_evidence=evidence_titles,
50:             context_completeness_score=context.context_completeness_score,
51:             suggested_next_action=primary_recommendation
52:         )
53: 
```

### B. File Purpose
The `ReviewPacketBuilder` acts as a **Data Collector**. It doesn't make decisions. Instead, it pulls the "Strategy Selected," the "Risk Score," and the "Agent Findings" into a single container so the human inspector doesn't have to hunt through six different files to find the truth.

### C. Line-by-Line Explanation

**Line 1: `import uuid`**
*   **What it does:** Generates a unique "Tracking Number" for the review case.

**Lines 3-7: Recruiting the Data Types**
*   **What it represents:** Bringing in the blueprints for every piece of data we need (Request, Library, Decision, Agent Output).

**Line 9: `class ReviewPacketBuilder:`**
*   **What it represents:** The **Briefing Assistant**.

**Line 25: `review_id = ...`**
*   **What the computer does:** Creates a unique ID like `REV-A1B2C3D4`.

**Lines 27-36: Summarizing Agent Findings**
*   **What it represents:** The assistant reads the notes from the **Robot Squad**. 
*   **Meaning:** It looks at the *last* thing a robot said (since that's usually the final conclusion) and saves it as the "Primary Recommendation."

**Line 38: `evidence_titles = ...`**
*   **What the computer does:** Makes a list of every book title the library robots found.

**Lines 40-52: Assembling the Folder**
*   **The Final Act:** It takes all those pieces and stuffs them into a `ReviewPacket` object.

---

### 🏁 Friendly Recap (The Briefing)

You've just learned how we **Prepare for a Human Review**!

You now understand:
1.  How **Standardized Forms** (models) keep our paperwork organized.
2.  How the **Packet Builder** automatically gathers data from throughout the factory.
3.  Why we track **Overrides** (disagreements) to make our AI better over time.

### 8.3 queue.py – The Waiting Room

Once a packet is built, it doesn't just float in the air. It needs to be stored in a list until a human has time to look at it. The `queue.py` file is our **Waiting Room**. It keeps track of all the "Review Items" and their current status.

### A. Full File Ingestion: `app/review/queue.py`

```python
1: from typing import List, Dict, Optional
2: from app.review.models import ReviewPacket, ReviewQueueItem
3: 
4: class ReviewQueue:
5:     """
6:     In-memory management of the human review queue.
7:     Operational interface for enqueuing and retrieving review cases.
8:     """
9:     
10:     def __init__(self):
11:         self._queue: Dict[str, ReviewQueueItem] = {}
12:         self._packets: Dict[str, ReviewPacket] = {}
13: 
14:     def enqueue_review(self, packet: ReviewPacket, priority: int = 2):
15:         """
16:         Adds a new review case to the platform queue.
17:         """
18:         item = ReviewQueueItem(
19:             review_id=packet.review_id,
20:             request_id=packet.request_id,
21:             priority=priority,
22:             status="PENDING"
23:         )
24:         self._queue[packet.review_id] = item
25:         self._packets[packet.review_id] = packet
26: 
27:     def get_pending_reviews(self) -> List[ReviewQueueItem]:
28:         """
29:         Returns all cases currently awaiting human action.
30:         """
31:         return [item for item in self._queue.values() if item.status == "PENDING"]
32: 
33:     def get_packet(self, review_id: str) -> Optional[ReviewPacket]:
34:         """
35:         Retrieves the full evidence packet for a specific review case.
36:         """
37:         return self._packets.get(review_id)
38: 
39:     def update_status(self, review_id: str, status: str, assigned_to: Optional[str] = None):
40:         """
41:         Transitions a case through the review lifecycle.
42:         """
43:         if review_id in self._queue:
44:             item = self._queue[review_id]
45:             item.status = status
46:             if assigned_to:
47:                 item.assigned_to = assigned_to
```

### B. File Purpose
The `ReviewQueue` manages the **Backlog**. It ensures that no review case is ever lost. It stores two things:
1.  **The Metadata (`_queue`)**: Like a sticky note showing the ID, Status, and Priority.
2.  **The Full Data (`_packets`)**: The complete Briefing Folder.

### C. Line-by-Line Explanation

**Lines 11-12: The Storage Shelves**
*   **What it does:** Creates two internal "Storage Areas."

**Line 14: `enqueue_review(...)`**
*   **The Action:** Adding a case to the Waiting Room. It automatically sets the status to "PENDING."

**Line 27: `get_pending_reviews()`**
*   **The Action:** A human can call this function to see a list of everything they need to work on.

**Line 33: `get_packet(review_id)`**
*   **The Action:** When an inspector picks a case, they use this function to "Open the Folder."

---

### 8.4 coordinator.py – The Inspector General

We have the forms, the briefing, and the waiting room. now we need a boss to run the show. The `coordinator.py` is the **Inspector General**. It is the main controller that manages the entire lifecycle of a human review, from the moment a robot asks for help to the moment the human signs the final verdict.

### A. Full File Ingestion: `app/review/coordinator.py`

```python
1: from typing import List, Dict, Any, Optional
2: from app.review.models import ReviewPacket, ReviewDecision, OverrideRecord
3: from app.review.packet import ReviewPacketBuilder
4: from app.review.queue import ReviewQueue
5: from app.review.approval import ReviewApprovalHandler
6: from app.review.overrides import OverrideTracker
7: from app.intake.schemas import PlatformRequest
8: from app.context.models import ContextPacket
9: from app.control_plane.decision import ControlPlaneDecision
10: 
11: class ReviewCoordinator:
12:     """
13:     Top-level controller for the Human Review lifecycle.
14:     """
15:     
16:     def __init__(self):
17:         self.packet_builder = ReviewPacketBuilder()
18:         self.queue = ReviewQueue()
19:         self.approval_handler = ReviewApprovalHandler()
20:         self.override_tracker = OverrideTracker()
21: 
22:     def initiate_review(
23:         self, 
24:         request: PlatformRequest, 
25:         context: ContextPacket, 
26:         decision: ControlPlaneDecision,
27:         agent_findings: List[Dict[str, Any]],
28:         reason: str
29:     ) -> str:
30:         """
31:         Creates a review packet and places it in the queue.
32:         Returns the review_id.
33:         """
34:         packet = self.packet_builder.build_packet(request, context, decision, agent_findings, reason)
35:         self.queue.enqueue_review(packet)
36:         return packet.review_id
37: 
38:     def submit_decision(
39:         self, 
40:         review_id: str, 
41:         decision_code: str, 
42:         reason: str, 
43:         reviewer: str,
44:         notes: Optional[str] = None
45:     ) -> Dict[str, Any]:
...
61:         
62:         return {
63:             "decision": decision,
64:             "override": override,
65:             "final_action": decision.approved_action
66:         }
```

### B. File Purpose
The `ReviewCoordinator` is the **Traffic Controller**. It doesn't do the data work or the review work; instead, it tells everyone else which file goes where.

### C. Line-by-Line Explanation

**Lines 16-20: The Command Center**
*   **What it does:** Initializes all the assistants (Builder, Queue, Handler, Tracker).

**Line 22: `initiate_review(...)`**
*   **The Scenario:** A robot says, "I need help!" 
*   **The Action:** The Coordinator tells the **Builder** to make a packet (Line 34) and tells the **Queue** to store it (Line 35).

**Line 38: `submit_decision(...)`**
*   **The Scenario:** A human has finished their review.
*   **Step 1 (Line 54):** Hand the human's decision to the **Approval Handler** (our Verdict Stamper).
*   **Step 2 (Line 57):** Check if this decision was an **Override** against the robot.
*   **Step 3 (Line 60):** Close the case in the Waiting Room.

---

### 🏁 Friendly Recap (Backlog & Boss)

You've just met the **Boss** and the **Waiting Room**!

You now understand:
1.  How the **Queue** prevents cases from being forgotten.
2.  How the **Coordinator** manages the start-to-finish lifecycle.
3.  Why we track every human decision to see if the AI needs more training.

### 8.5 approval.py – The Verdict Stamper

Once a human has looked at the briefing and made up their mind, we need to turn that human thought into a structured piece of data that the factory can handle. The `approval.py` file is our **Verdict Stamper**. It takes the human's "Yes/No/Maybe" and stamps it with an official "Approved Action."

### A. Full File Ingestion: `app/review/approval.py`

```python
1: from typing import Optional
2: from app.review.models import ReviewDecision, ReviewPacket
3: 
4: class ReviewApprovalHandler:
5:     """
6:     Logic for capturing and validating human reviewer decisions.
7:     """
8:     
9:     def process_decision(
10:         self, 
11:         packet: ReviewPacket, 
12:         decision_code: str, 
13:         reason: str, 
14:         reviewer: str,
15:         notes: Optional[str] = None
16:     ) -> ReviewDecision:
17:         """
18:         Creates a structured ReviewDecision record from human input.
19:         """
20:         # Determine the approved action
21:         # In a real system, this might map 'APPROVE' to the system's suggestion
22:         approved_action = packet.suggested_next_action
23:         if decision_code == "REJECT":
24:             approved_action = "TERMINATE"
25:         elif decision_code == "SEND_BACK":
26:             approved_action = "REQUEST_MORE_INFO"
27:             
28:         return ReviewDecision(
29:             review_id=packet.review_id,
30:             reviewer_name=reviewer,
31:             decision=decision_code,
32:             decision_reason=reason,
33:             notes=notes,
34:             approved_action=approved_action
35:         )
```

### B. File Purpose
The `ReviewApprovalHandler` translates **Human Input** into **System Instructions**. 
*   If a human says "REJECT," the system instruction becomes "TERMINATE."
*   If a human says "APPROVE," the system instruction becomes whatever the robot originally suggested (e.g., "Allow Transaction").

### C. Line-by-Line Explanation

**Line 9: `process_decision(...)`**
*   **The Action:** The human pushes a button. This function catches that button press.

**Lines 22-26: The Translation Table**
*   **Meaning:** This is where human words are turned into robot commands.
    *   **APPROVE** $\rightarrow$ Robot's Recommendation.
    *   **REJECT** $\rightarrow$ TERMINATE.
    *   **SEND_BACK** $\rightarrow$ REQUEST_MORE_INFO.

**Lines 28-35: Signing the Form**
*   **Output:** It creates a `ReviewDecision` object, which is the official signed verdict.

---

### 8.6 overrides.py – The Disagreement Log

Crucial for any high-security AI system is the ability to track when humans disagree with the machines. The `overrides.py` file is our **Disagreement Log**. It acts like a "Correction Tape" that notes when a human stepped in to fix a robot's mistake.

### A. Full File Ingestion: `app/review/overrides.py`

```python
1: from app.review.models import OverrideRecord, ReviewPacket, ReviewDecision
2: 
3: class OverrideTracker:
4:     """
5:     Identifies and logs deviations between system recommendations and human choices.
6:     """
7:     
8:     def detect_and_log(self, packet: ReviewPacket, decision: ReviewDecision) -> OverrideRecord:
9:         """
10:         Checks if the human decision overridden the system's suggested path.
11:         """
12:         system_suggested = packet.suggested_next_action
13:         human_chosen = decision.approved_action
14:         
15:         is_override = system_suggested != human_chosen
16:         
17:         if is_override:
18:             return OverrideRecord(
19:                 review_id=packet.review_id,
20:                 system_recommendation=system_suggested,
21:                 reviewer_decision=human_chosen,
22:                 override_reason=decision.decision_reason,
23:                 impact_level="HIGH" if decision.decision == "REJECT" else "MEDIUM"
24:             )
25:             
26:         return None # No override detected
```

### B. File Purpose
The `OverrideTracker` is the **System Teacher**. By logging every time a human changes a robot's decision, we can look back at the logs and say, "Hey, our robots are too strict on VIPs, we need to adjust their brains."

### C. Line-by-Line Explanation

**Lines 12-15: The Comparison**
*   **What it does:** Compares the "System Suggested" action against the "Human Chosen" action.
*   **Meaning:** If they are different, an **Override** has occurred!

**Lines 18-24: Documenting the Override**
*   **The Action:** If a disagreement is found, it fills out an `OverrideRecord`.
*   **Line 23 (`impact_level`):** If the robot wanted to allow a transaction but the human **Rejected** it, that’s a "HIGH" impact override because it involves blocking money.

---

### 🏁 Friendly Recap (Chapter 8 Completed!)

Congratulations! You've just mastered the **Safety Inspectors** layer!

In this chapter, you learned:
1.  How the **Packet Builder** assembles a briefing for human eyes.
2.  How the **Waiting Room** keeps track of the queue.
3.  How the **Inspector General** (coordinator) manages the start-to-finish lifecycle.
4.  Why **Overrides** are the secret to training smarter robots.

**The transaction has been analyzed, the robots have planned, the tools have moved, and the inspectors have reviewed it all. But how do we stay safe as things are actually running? In the next chapter, we're heading to the "Safety Rails" room—the `app/runtime/` layer!**
