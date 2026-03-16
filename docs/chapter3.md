# Chapter 3: The Research Library (The `app/context/` Layer)

## 1️⃣ Big Picture: The Research Library

Imagine our factory has a massive, high-tech **Research Library** hidden in the back. 

When a "Customer Order" (from Chapter 2) arrives, it's just a piece of paper with a few facts. But our Robots need more than that to make a smart decision. They need to know the customer's history, the company's laws, and what happened in similar cases last week.

The **Research Library** is the department that gathers all this evidence. 
1.  **The Librarian (`builder.py`)**: This is the manager of the library. They don't do the research themselves, but they tell the other librarians exactly what to look for.
2.  **The Book Finder (`retriever.py`)**: They run into the stacks and grab every book that might be relevant.
3.  **The Expert Grader (`ranker.py`)**: They look at the pile of books and throw away the ones that aren't actually useful.
4.  **The Highlighter (`enricher.py`)**: they go through the remaining books and highlight the most important parts for the robots to read.

**What breaks if the Library is closed?**
If the library is missing, the robots are essentially "blind." They might see a request for a $5,000 credit increase, but they won't know if the customer is a billionaire or a broke student. Without context, the AI is just guessing—and in a bank, guessing is dangerous.

---

## 2️⃣ Teach the Code

### A. Full File Ingestion: `app/context/builder.py`

```python
1: from typing import List, Dict, Any, Optional
2: from app.context.models import ContextPacket, RetrievedEvidence, EnrichedEvidence
3: from app.context.retriever import ContextRetriever
4: from app.context.ranker import EvidenceRanker
5: from app.context.enricher import ContextEnricher
6: from app.intake.schemas import PlatformRequest
7: 
8: class ContextBuilder:
9:     """
10:     Orchestrates the retrieval, ranking, and enrichment of business context.
11:     Produces the final ContextPacket for downstream consumption.
12:     """
13:     
14:     def __init__(self):
15:         self.retriever = ContextRetriever()
16:         self.ranker = EvidenceRanker()
17:         self.enricher = ContextEnricher()
18: 
19:     def build_context(self, request: PlatformRequest) -> ContextPacket:
20:         """
21:         Assembles the ContextPacket from multiple platform sources.
22:         """
23:         request_id = request.request_id
24:         
25:         # 1. Define Query Terms (Simplified logic for Phase 3C)
26:         query_terms = [request.use_case_type]
27:         if "merchant" in request.business_payload:
28:             query_terms.append(request.business_payload["merchant"])
29:         if "amount" in request.business_payload:
30:             query_terms.append("luxury" if request.business_payload["amount"] > 3000 else "transaction")
31: 
32:         # 2. Retrieve Raw Evidence
33:         customer_id = request.customer_context.get("id", "UNKNOWN")
34:         raw_evidence = self.retriever.fetch_evidence(query_terms, customer_id)
35:         
```

*(Note: File stops at line 35 of 80 for this segment. I will explain the rest in the next part.)*

### B. File Purpose
The `builder.py` file is the **Librarian-in-Chief**. Its job is to manage the flow of information. It takes the "Order Form," sends out the "Search Team," and then packages all the findings into a neat "Briefing Folder" (the ContextPacket) for the robots.

### C. Line-by-Line Explanation

**Line 1: `from typing import List, Dict, Any, Optional`**
*   **What the computer does:** Brings in tools to label different kinds of lists and containers.
*   **Why it exists:** To keep the research organized so we don't mix up a single fact with a list of facts.

**Line 2: `from app.context.models import ContextPacket, RetrievedEvidence, EnrichedEvidence`**
*   **What the computer does:** Goes to the "Storage Room" (`models.py`) and brings out three specific containers.
*   **Meaning:** `ContextPacket` is the final briefing folder. `RetrievedEvidence` is a raw book. `EnrichedEvidence` is a book with highlights.

**Line 3: `from app.context.retriever import ContextRetriever`**
*   **What the computer does:** Recruits the "Book Finder."

**Line 4: `from app.context.ranker import EvidenceRanker`**
*   **What the computer does:** Recruits the "Expert Grader."

**Line 5: `from app.context.enricher import ContextEnricher`**
*   **What the computer does:** Recruits the "Highlighter."

**Line 6: `from app.intake.schemas import PlatformRequest`**
*   **What the computer does:** Brings in the "Order Form" template we learned about in Chapter 2.
*   **Connection:** We need to know what the form looks like to read it!

**Line 7: `(Empty Line)`**

**Line 8: `class ContextBuilder:`**
*   **What the computer does:** Declares the "Librarian-in-Chief" role.
*   **Significance:** This is the manager who will run the whole department.

**Lines 9-12: `""" ... """`**
*   **Meaning:** A note explaining that this manager "orchestrates" (conducts) the research and makes the final "Briefing Folder."

**Line 13: `(Empty Line)`**

**Line 14: `def __init__(self):`**
*   **What the computer does:** The "Morning Routine." This is what the manager does the moment they walk into the library.

**Lines 15-17: `self.retriever = ...`, `self.ranker = ...`, `self.enricher = ...`**
*   **What the computer does:** The manager picks up their three main tools and keeps them ready at their desk.
*   **Meaning:** `self` means "the manager's own tool."

**Line 18: `(Empty Line)`**

**Line 19: `def build_context(self, request: PlatformRequest) -> ContextPacket:`**
*   **What the computer does:** Defines the "Main Action": Building the folder.
*   **Word-by-word:** `def` (Plan) `build_context` (Name) `request: PlatformRequest` (Input: The order form) `-> ContextPacket` (Output: The final briefing folder).

**Lines 20-22: `""" ... """`**
*   **Meaning:** A note explaining that this plan assembles all the proof together.

**Line 23: `request_id = request.request_id`**
*   **What the computer does:** Copies the "Receipt Number" from the order form.
*   **Why it exists:** To make sure the research folder has the same ID as the customer's request.

**Line 24: `(Empty Line)`**

**Line 25: `# 1. Define Query Terms (Simplified logic for Phase 3C)`**
*   **Meaning:** Comment: We are deciding what words to type into our search engine.

**Line 26: `query_terms = [request.use_case_type]`**
*   **What the computer does:** Starts a list of search words with the main goal (e.g., "credit_limit_increase").

**Line 27-28: `if "merchant" in request.business_payload: ...`**
*   **What the computer does:** Checks if the order says which store the customer is at. If yes, add the store's name to our search list.
*   **Why it exists:** To find out if this specific store has a history of fraud.

**Line 29-30: `if "amount" in request.business_payload: ...`**
*   **What the computer does:** Checks the price.
*   **Logic:** If the price is over $3,000, add the word "luxury" to our search. Otherwise, just use the word "transaction."
*   **Why it exists:** Luxury purchases need different rules than buying a coffee.

**Line 31: `(Empty Line)`**

**Line 32: `# 2. Retrieve Raw Evidence`**
*   **Meaning:** Comment: Time to go into the stacks!

**Line 33: `customer_id = request.customer_context.get("id", "UNKNOWN")`**
*   **What the computer does:** Looks for the Customer's Name (ID). If they can't find it, they just write down "UNKNOWN."

**Line 34: `raw_evidence = self.retriever.fetch_evidence(query_terms, customer_id)`**
*   **What the computer does:** Hands the search words to the "Book Finder" and tells them to come back with a pile of raw books.
*   **Meaning:** `raw_evidence` is that initial, messy pile of information.

**Line 35: `(Empty Line)`**

### D. Define Terms
*   **Orchestrate:** To coordinate many different parts so they work together perfectly (like a conductor of an orchestra).
*   **Context:** The "Full Story" or background information that makes a single fact make sense.
*   **Input (`request`):** The data being handed *into* a function.
*   **Output (`ContextPacket`):** The finished product being handed *out* of a function.
*   **Query Terms:** The specific keywords you type into a search bar to find something.

---

## 3️⃣ Agentic AI Behavior

This code provides the **Knowledge Base** for our Agent.

A basic AI and a "Governed Agent" have one huge difference: **Grounding**.
*   A basic AI "hallucinates" (makes things up) because it has no reference material.
*   Our **Governed Agent** uses this `ContextBuilder` to "Ground" itself in reality. Before it speaks, it looks at the `ContextPacket` to see the actual laws and actual customer history.

By performing this research first, the AI transforms from a "Chatbot" into an **Evidence-Based Analyst**. 

---

## 4️⃣ Friendly Recap

You've just learned how the factory's "Manager of Research" starts a new investigation!

You now understand:
1.  How the manager recruits **specialized tools** to find, rank, and highlight data.
2.  How the manager creates **smart search terms** based on the price and the store.
3.  How we connect the customer's ID to every piece of evidence we find.

You're seeing the "Brain" of the AI platform being built, layer by layer. 

### A. Full File Ingestion: `app/context/builder.py` (Continued)

```python
36:         # 3. Rank and Filter
37:         ranked_evidence = self.ranker.rank_and_filter(raw_evidence)
38:         
39:         # 4. Enrich Evidence
40:         enriched_evidence = self.enricher.enrich_evidence(ranked_evidence)
41:         
42:         # 5. Missing Context Detection
43:         missing_fields, gaps, completeness = self._detect_gaps(request, enriched_evidence)
44:         
45:         # 6. Extract Lists for Legacy Components
46:         policies = [e.source_id for e in enriched_evidence if e.source_type == "policy"]
47:         cases = [e.source_id for e in enriched_evidence if e.source_type == "case_history"]
48: 
49:         # 7. Assemble Packet
50:         return ContextPacket(
51:             request_id=request_id,
52:             request_summary=f"Context-grounded analysis for {request.use_case_type} at {request.business_payload.get('merchant', 'Unknown')}",
53:             customer_context=request.customer_context,
54:             transaction_context=request.business_payload,
55:             evidence=enriched_evidence,
56:             policy_references=policies,
57:             prior_cases=cases,
58:             missing_fields=missing_fields,
59:             context_completeness_score=completeness,
60:             retrieval_gaps=gaps
61:         )
62: 
63:     def _detect_gaps(self, request: PlatformRequest, enriched: List[EnrichedEvidence]) -> tuple:
64:         missing_fields = []
65:         gaps = []
66:         
67:         # Check for essential source types
68:         source_types = {e.source_type for e in enriched}
69:         if "customer" not in source_types:
70:             missing_fields.append("customer_risk_profile")
```

*(Note: File stops at line 70 of 80 for this segment. I will explain the final 10 lines in the next part.)*

### C. Line-by-Line Explanation (Continued)

**Line 36: `# 3. Rank and Filter`**
*   **Meaning:** Comment: We are about to sort through the big pile of books we found.

**Line 37: `ranked_evidence = self.ranker.rank_and_filter(raw_evidence)`**
*   **What the computer does:** Hands the "Raw Evidence" pile to the **Expert Grader** (ranker).
*   **Meaning:** The Grader throws away low-quality info and keeps only the most relevant facts.
*   **Why it exists:** AI gets confused if you give it too much "noise." We only want the high-quality signal.

**Line 38: `(Empty Line)`**

**Line 39: `# 4. Enrich Evidence`**
*   **Meaning:** Comment: Time to start highlighting!

**Line 40: `enriched_evidence = self.enricher.enrich_evidence(ranked_evidence)`**
*   **What the computer does:** Hands the filtered books to the **Highlighter** (enricher).
*   **Meaning:** The Highlighter adds extra metadata (labels) to the facts to make them easier for robots to understand.

**Line 41: `(Empty Line)`**

**Line 42: `# 5. Missing Context Detection`**
*   **Meaning:** Comment: Checking if we missed something important.

**Line 43: `missing_fields, gaps, completeness = self._detect_gaps(request, enriched_evidence)`**
*   **What the computer does:** Triggers a "Search Audit." 
*   **Meaning:** It compares what we *found* vs what we *needed* and calculates a "Completeness Score."
*   **Why it exists:** If the library is missing the Customer's Risk report, we need to flag it so the Robots be extra careful.

**Line 44: `(Empty Line)`**

**Line 45: `# 6. Extract Lists for Legacy Components`**
*   **Meaning:** Comment: Making easy-to-read lists for older systems.

**Lines 46-47: `policies = [...]`, `cases = [...]`**
*   **What the computer does:** Scans the highlighted evidence and makes two separate lists: one for "Company Policies" and one for "Past Cases."
*   **Symbol-by-symbol:** `[` and `]` create a new list. `for e in enriched_evidence` means "Look at every item one by one." `if e.source_type == "policy"` is the filter.

**Line 48: `(Empty Line)`**

**Line 49: `# 7. Assemble Packet`**
*   **Meaning:** Comment: Time to put everything in the briefing folder!

**Line 50: `return ContextPacket(`**
*   **What the computer does:** Creates the final **ContextPacket** object and hands it back to the manager.
*   **Word-by-word:** `return` (Give back the result) `ContextPacket` (The type of folder).

**Lines 51-60: `request_id=request_id, ...`**
*   **What the computer does:** Fills out the different pockets of the briefing folder.
*   **Significance:** It puts the summary, the customer info, the actual evidence, and the "Gap Report" into one single package.
*   **Connection:** This is the EXACT folder that the AI Robots will read in the next chapter.

**Line 61: `)`**
*   **What the computer does:** Closes the folder assembly.

**Line 62: `(Empty Line)`**

**Line 63: `def _detect_gaps(self, request: PlatformRequest, enriched: List[EnrichedEvidence]) -> tuple:`**
*   **What the computer does:** Defines a "Secret Internal Plan" for checking for gaps.
*   **Symbol-by-symbol:** The `_` at the start of `_detect_gaps` tells other programmers: "This is a private, internal tool for the Librarian only."
*   **Meaning:** `-> tuple` means this plan will return a small group of answers at once.

**Lines 64-65: `missing_fields = []`, `gaps = []`**
*   **What the computer does:** Starts with two empty "Error Lists."

**Line 66: `(Empty Line)`**

**Line 67: `# Check for essential source types`**
*   **Meaning:** Comment: Making sure we have the "Must-Have" books.

**Line 68: `source_types = {e.source_type for e in enriched}`**
*   **What the computer does:** Makes a unique list of all the *types* of info we found (e.g., "Policy," "History").
*   **Symbol-by-symbol:** `{` and `}` create a "Set" which automatically removes duplicates.

**Line 69: `if "customer" not in source_types:`**
*   **What the computer does:** Checks if the "Customer Record" building block is missing.

**Line 70: `missing_fields.append("customer_risk_profile")`**
*   **What the computer does:** If missing, write "customer_risk_profile" on our "Missing Items" list.

*(Stop segment - lines 36-70 explained)*

### D. Define Terms
*   **Ranking:** The act of sorting items so the most important ones are at the top and the junk is at the bottom.
*   **Metadata:** "Data about data." Labels that explain what a piece of information is (like the genre on the spine of a book).
*   **Gap Detection:** A security check to see if we are missing critical information needed to make a safe decision.
*   **Tuple:** A small, fixed-size group of items that computers treat as a single unit (like a pair of coordinates).
*   **Set (`{}`):** A special list that is guaranteed to have no repeat items.

---

### 🏁 Friendly Recap (Part 2)

You just learned how the research is **processed and packaged**!

You now understand:
1.  Why we **Rank and Filter** information (to stop the AI from getting confused).
2.  How we find **Gaps** in our knowledge (to keep the system safe).
3.  How we **Assemble the Folder** that will be handed to the robots.

We only have 10 lines left in this file before we graduate from the Librarian's office!

### A. Full File Ingestion: `app/context/builder.py` (Final)

```python
71:             gaps.append("NO_CUSTOMER_RECORD_FOUND")
72:             
73:         if "policy" not in source_types:
74:             gaps.append("NO_MATCHING_POLICY_FOUND")
75:             
76:         # Calculate a simple completeness score
77:         completeness = len(source_types) / 3.0 # Assuming 3 core types: policy, case, customer
78:         
79:         return missing_fields, gaps, min(completeness, 1.0)
80: 
```

### C. Line-by-Line Explanation (Final)

**Line 71: `            gaps.append("NO_CUSTOMER_RECORD_FOUND")`**
*   **What the computer does:** Adds a specific "Red Flag" to our report.
*   **Why it exists:** To alert the robots: "Caution! We are making a decision about a person we have never seen before."

**Line 72: `(Empty Line)`**

**Line 73: `        if "policy" not in source_types:`**
*   **What the computer does:** Checks if we forgot to bring the "Company Rulebook" (Policy) to the meeting.

**Line 74: `            gaps.append("NO_MATCHING_POLICY_FOUND")`**
*   **What the computer does:** Adds a "No Rules Found" flag. 
*   **Connection:** This is a high-risk situation. If the AI doesn't know the rules, it might make an illegal decision!

**Line 75: `(Empty Line)`**

**Line 76: `# Calculate a simple completeness score`**
*   **Meaning:** Comment: Time to give our research a grade.

**Line 77: `        completeness = len(source_types) / 3.0 # Assuming 3 core types: policy, case, customer`**
*   **What the computer does:** Simple math. It divides the number of things we *found* by the 3 things we *wanted*.
*   **Meaning:** If we found all 3, the score is 1.0 (100%). If we only found 1, the score is 0.33 (33%).

**Line 78: `(Empty Line)`**

**Line 79: `        return missing_fields, gaps, min(completeness, 1.0)`**
*   **What the computer does:** Hands the three final check-up results back to the manager.
*   **Symbol-by-symbol:** `min(..., 1.0)` is a safety check to make sure the score never goes higher than 100%, even if we found extra books.

**Line 80: `(Empty Line)`**
*   **Why it exists:** Final spacing at the end of the file.

---

### 🏁 Friendly Recap (Builder.py Completed!)

You have officially finished documentation for the **Librarian-in-Chief**! 

You now understand:
1.  How the manager identifies **Gaps** in their knowledge.
2.  How the factory calculates a **Completeness Score** (The Research Grade).
3.  How we ensure the robots never walk into a situation "blind."

Next, we'll look at the **Storage Shelves** of our library (`models.py`) to see exactly how these evidence folders are shaped!

## 3.2 enricher.py – The Expert Highlighter

Imagine you're a robot trying to read a 500-page bank manual. It would take you a long time to find the important stuff! 

The **Enricher** is like a specialized librarian who has a bright yellow highlighter and a pack of sticky notes. They read the raw books and:
1.  **Highlight** the money amounts.
2.  **Label** the risky parts with a "Warning" sticker.
3.  **Summarize** the long paragraphs into a single sentence.

By the time the robots get the book, all the hard work is done! They can just look at the highlights and make a decision in seconds.

### A. Full File Ingestion: `app/context/enricher.py`

```python
1: from typing import List, Dict, Any
2: from app.context.models import RetrievedEvidence, EnrichedEvidence
3: 
4: class ContextEnricher:
5:     """
6:     Transforms raw evidence into formatted business insights.
7:     """
8:     
9:     def enrich_evidence(self, raw_evidence: List[RetrievedEvidence]) -> List[EnrichedEvidence]:
10:         """
11:         Converts raw evidence into structured EnrichedEvidence objects.
12:         """
13:         enriched_list = []
14:         
15:         for item in raw_evidence:
16:             # Mock enrichment logic: extraction and tagging
17:             summary = f"Summary of {item.title}: {item.content[:100]}..."
18:             key_facts = self._extract_facts(item.content)
19:             risk_signals = self._detect_risk_signals(item.content)
20:             
21:             enriched_list.append(EnrichedEvidence(
22:                 source_type=item.source_type,
23:                 source_id=item.source_id,
24:                 summary=summary,
25:                 key_facts=key_facts,
26:                 risk_signals=risk_signals,
27:                 policy_tags=item.metadata.get("tags", [])
28:             ))
29:             
30:         return enriched_list
31: 
32:     def _extract_facts(self, content: str) -> List[str]:
33:         # Placeholder for NER or regex-based extraction
34:         facts = []
35:         if "$" in content:
```

*(Note: File stops at line 35 of 48 for this segment. Remaining lines will follow in the next segment.)*

### B. File Purpose
The `enricher.py` file takes the "Raw Books" and turns them into "High-Value Briefs." It extracts specific facts (like money or stores) and marks potential risks so the AI doesn't have to "guess" what the important parts are.

### C. Line-by-Line Explanation

**Line 1: `from typing import List, Dict, Any`**
*   **What the computer does:** Brings in the labels for lists and containers.
*   **Why it exists:** To keep our organization system consistent.

**Line 2: `from app.context.models import RetrievedEvidence, EnrichedEvidence`**
*   **What the computer does:** Brings in the "Before" and "After" containers.
*   **Meaning:** `RetrievedEvidence` is the raw book. `EnrichedEvidence` is the book after we've highlighted it.

**Line 3: `(Empty Line)`**

**Line 4: `class ContextEnricher:`**
*   **What the computer does:** Defines the "Expert Highlighter" role.

**Lines 5-7: `""" ... """`**
*   **Meaning:** A note explaining that this role transforms raw info into smart "insights."

**Line 8: `(Empty Line)`**

**Line 9: `def enrich_evidence(self, raw_evidence: List[RetrievedEvidence]) -> List[EnrichedEvidence]:`**
*   **What the computer does:** Defines the "Highlighting Plan."
*   **Input:** A list of raw books.
*   **Output:** A list of highlighted books.

**Lines 10-12: `""" ... """`**
*   **Meaning:** A note explaining that we are structuring the information.

**Line 13: `enriched_list = []`**
*   **What the computer does:** Clears off a spot on the desk for our newly highlighted books.

**Line 14: `(Empty Line)`**

**Line 15: `for item in raw_evidence:`**
*   **What the computer does:** Picks up the first raw book in the pile. We will repeat the next steps for every book in the stack.

**Line 16: `# Mock enrichment logic: extraction and tagging`**
*   **Meaning:** Comment: We are teaching the computer how to summarize and label.

**Line 17: `summary = f"Summary of {item.title}: {item.content[:100]}..."`**
*   **What the computer does:** Shortens the book. It takes the first 100 characters of the content and adds "..." at the end.
*   **Symbol-by-symbol:** `[:100]` means "take from the start up to the 100th letter."

**Line 18: `key_facts = self._extract_facts(item.content)`**
*   **What the computer does:** Asks the "Fact Extraction" tool to find items like $ symbols or city names.

**Line 19: `risk_signals = self._detect_risk_signals(item.content)`**
*   **What the computer does:** Asks the "Risk Detection" tool to find scary words like "dispute."

**Line 20: `(Empty Line)`**

**Line 21: `enriched_list.append(EnrichedEvidence(`**
*   **What the computer does:** Starts filling out a new "Highlighted Form" (`EnrichedEvidence`) and adds it to our finished pile (`enriched_list`).

**Lines 22-26: Filling the form**
*   **What the computer does:** Copies the ID and source from the raw book, then adds our new summary, facts, and risks.

**Line 27: `policy_tags=item.metadata.get("tags", [])`**
*   **What the computer does:** Checks the raw book's metadata for any existing "Tags." If none exist, use an empty list `[]`.

**Line 28: `))`**
*   **What the computer does:** Closes the final form.

**Line 29: `(Empty Line)`**

**Line 30: `return enriched_list`**
*   **What the computer does:** Hands the finished pile of highlighted books back to the Librarian-in-Chief.

**Line 31: `(Empty Line)`**

**Line 32: `def _extract_facts(self, content: str) -> List[str]:`**
*   **What the computer does:** Defines the "Search for Facts" tool. 
*   **Meaning:** This tool looks for "Nouns" and "Numbers" that are important for business.

**Line 33: `# Placeholder for NER or regex-based extraction`**
*   **Meaning:** Comment: This is a placeholder for even smarter tools we might add later.

**Line 34: `facts = []`**
*   **What the computer does:** Starts a blank list of findings.

**Line 35: `if "$" in content:`**
*   **What the computer does:** Scans the text for a money symbol.

---

### 🏁 Friendly Recap (Enricher Part 1)

You've just seen how we **highlight** the most important parts of a long document!

You now understand:
1.  How we **loop** through a pile of books one by one.
2.  How we **shorten** long text into a quick summary.
3.  How we **detect** specific symbols like the "$" sign to find financial facts.

### A. Full File Ingestion: `app/context/enricher.py` (Final)

```python
36:             facts.append("Contains financial thresholds")
37:         if "NYC" in content:
38:             facts.append("Involves NYC location")
39:         return facts
40: 
41:     def _detect_risk_signals(self, content: str) -> List[str]:
42:         signals = []
43:         if "dispute" in content.lower():
44:             signals.append("PRIOR_DISPUTE_HISTORY")
45:         if "high-risk" in content.lower():
46:             signals.append("POLICY_HIGH_RISK_WARNING")
47:         return signals
48: 
```

### C. Line-by-Line Explanation (Final)

**Line 36: `            facts.append("Contains financial thresholds")`**
*   **What the computer does:** If a "$" was found, it adds this specific text to our list of findings.
*   **Why it exists:** To let the AI know that this document has something to do with money rules.

**Lines 37-38: `if "NYC" in content: ...`**
*   **What the computer does:** Scans for the text "NYC." If found, it adds a "location" fact.
*   **Significance:** Different cities have different tax laws or fraud patterns.

**Line 39: `        return facts`**
*   **What the computer does:** Finishes the search and hands the list of facts back to the main librarian.

**Line 40: `(Empty Line)`**

**Line 41: `    def _detect_risk_signals(self, content: str) -> List[str]:`**
*   **What the computer does:** Defines the "Risk Radar" tool.
*   **Meaning:** This tool looks for "Scary Words" that suggest we should be careful.

**Line 42: `        signals = []`**
*   **What the computer does:** Starts a blank list of "Warning Red Flags."

**Line 43: `        if "dispute" in content.lower():`**
*   **What the computer does:** Scans for the word "dispute."
*   **Symbol-by-symbol:** `.lower()` makes the text lowercase so it finds both "Dispute" and "DISPUTE."

**Line 44: `            signals.append("PRIOR_DISPUTE_HISTORY")`**
*   **What the computer does:** Adds a "Prior Dispute" warning to our report.

**Line 45: `        if "high-risk" in content.lower():`**
*   **What the computer does:** Scans for the specific phrase "high-risk."

**Line 46: `            signals.append("POLICY_HIGH_RISK_WARNING")`**
*   **What the computer does:** Adds a "Policy Warning" flag.

**Line 47: `        return signals`**
*   **What the computer does:** Hands the list of red flags back to the manager.

**Line 48: `(Empty Line)`**

---

### 🏁 Friendly Recap (Enricher Completed!)

You have just mastered the **Risk Radar** of our research library!

You now understand:
1.  How we scan for **Financial Symbols** ($) and **Locations** (NYC).
2.  How the computer catches **Scary Words** like "dispute" and turns them into formal warnings.
3.  Why we use **private tools** (starting with `_`) to handle the messy work behind the scenes.

## 3.3 retriever.py – The Book Finder

If the Librarian-in-Chief is the manager, the **Retriever** is the person with the running shoes. 

When the manager says, "Find me everything about 'luxury transactions' and 'Account 123'," the Retriever doesn't just look in one place. They sprint to three different rooms:
1.  **The Policy Room**: Where the company's laws are kept.
2.  **The Case Room**: Where the history of every customer is stored.
3.  **The Customer Profile Room**: Where we keep the facts about the person making the request.

The Retriever's goal is to bring back a "Messy Pile" of books for the others to sort out later.

### A. Full File Ingestion: `app/context/retriever.py`

```python
1: from typing import List, Dict, Any
2: from app.context.models import RetrievedEvidence
3: from app.context.sources import POLICY_STORE, CASE_STORE, CUSTOMER_STORE
4: 
5: class ContextRetriever:
6:     """
7:     Handles fetching candidate evidence from multiple platform sources.
8:     Integrated with Policy, Case, and Customer data.
9:     """
10:     
11:     def fetch_evidence(self, query_terms: List[str], customer_id: str) -> List[RetrievedEvidence]:
12:         """
13:         Retrieves raw evidence objects from all available sources.
14:         """
15:         results = []
16:         
17:         # 1. Retrieve matching Policies (Keyword mock)
18:         for policy in POLICY_STORE:
19:             for term in query_terms:
20:                 if term.lower() in policy["content"].lower() or term.lower() in policy["title"].lower():
21:                     results.append(RetrievedEvidence(
22:                         source_type="policy",
23:                         source_id=policy["source_id"],
24:                         title=policy["title"],
25:                         content=policy["content"],
26:                         relevance_score=0.9, # Mocked score
27:                         metadata={"tags": policy.get("tags", [])}
28:                     ))
29:                     break # Don't duplicate for multiple terms
30:                     
31:         # 2. Retrieve Prior Cases
32:         for case in CASE_STORE:
33:             if case.get("customer_id") == customer_id:
34:                 results.append(RetrievedEvidence(
35:                     source_type="case_history",
```

*(Note: File stops at line 35 of 55 for this segment. Remaining lines will follow in the next segment.)*

### B. File Purpose
The `retriever.py` file is the "Search Engine" of the Research Library. It looks through the three big data stores (Policy, Cases, Customers) and pulls out anything that matches the words we are looking for.

### C. Line-by-Line Explanation

**Line 1: `from typing import List, Dict, Any`**
*   **Purpose:** Standard organizational labels.

**Line 2: `from app.context.models import RetrievedEvidence`**
*   **What the computer does:** Brings in the empty "Raw Book" container.
*   **Why it exists:** We need a standard way to carry information from the storage room back to the manager's desk.

**Line 3: `from app.context.sources import POLICY_STORE, CASE_STORE, CUSTOMER_STORE`**
*   **What the computer does:** Opens the doors to our three main "Storage Rooms" (the data stores).

**Line 4: `(Empty Line)`**

**Line 5: `class ContextRetriever:`**
*   **What the computer does:** Defines the "Book Finder" role.

**Lines 6-9: `""" ... """`**
*   **Meaning:** A note explaining that this role fetches "Candidate Evidence" (possible proof) from multiple sources.

**Line 10: `(Empty Line)`**

**Line 11: `def fetch_evidence(self, query_terms: List[str], customer_id: str) -> List[RetrievedEvidence]:`**
*   **What the computer does:** Defines the "Sprinting Plan."
*   **Inputs:** `query_terms` (the keywords) and `customer_id` (the person).
*   **Output:** A list of raw evidence books.

**Lines 12-14: `""" ... """`**
*   **Meaning:** A note explaining that we are getting "Raw" objects.

**Line 15: `results = []`**
*   **What the computer does:** Starts a blank list to hold the books we find.

**Line 16: `(Empty Line)`**

**Line 17: `# 1. Retrieve matching Policies (Keyword mock)`**
*   **Meaning:** Comment: We are entering the **Policy Room** first.

**Line 18: `for policy in POLICY_STORE:`**
*   **What the computer does:** Picks up the first law book in the Policy Room and prepares to look inside.

**Line 19: `for term in query_terms:`**
*   **What the computer does:** Takes the first keyword (like "luxury") and prepares to search for it.

**Line 20: `if term.lower() in policy["content"].lower() or term.lower() in policy["title"].lower():`**
*   **What the computer does:** The "Keyword Search." It checks if the keyword is written anywhere in the book's title or the book's content.
*   **Symbol-by-symbol:** `or` means if the word is in the title OR the content, it's a match!

**Line 21: `results.append(RetrievedEvidence(`**
*   **What the computer does:** If it's a match, we put a copy of this policy into our "Found Books" pile.

**Lines 22-27: Filling the "Found Book" data**
*   **What the computer does:** Records the type ("policy"), the ID, the title, and the content. It also gives it a "Relevance Score" of 0.9 (meaning we are 90% sure this is useful).

**Line 28: `))`**
*   **What the computer does:** Closes the book container.

**Line 29: `break # Don't duplicate for multiple terms`**
*   **What the computer does:** If we already found the word "luxury" in this book, we don't need to check for the word "NYC" too. We already have the book! Move to the next book.

**Line 30: `(Empty Line)`**

**Line 31: `# 2. Retrieve Prior Cases`**
*   **Meaning:** Comment: Moving to the **Case Room**.

**Line 32: `for case in CASE_STORE:`**
*   **What the computer does:** Picks up the first "Case File" from the shelf.

**Line 33: `if case.get("customer_id") == customer_id:`**
*   **What the computer does:** Checks the name on the file. If it matches the customer we are currently investigating, we want it!

**Line 34: `results.append(RetrievedEvidence(`**
*   **What the computer does:** Puts a copy of the customer's history into our pile.

**Line 35: `source_type="case_history",`**
*   **What the computer does:** Labels this book as a "Case History."

---

### 🏁 Friendly Recap (Retriever Part 1)

You've just seen how the factory **searches through its memory**!

You now understand:
1.  How we **loop through all policies** to find matching keywords.
2.  How we check **Customer IDs** to find relevant history.
3.  Why we use a **standard container** (`RetrievedEvidence`) to carry everything.

### A. Full File Ingestion: `app/context/retriever.py` (Final)

```python
36:                     source_id=case["source_id"],
37:                     title=case["title"],
38:                     content=case["content"],
39:                     relevance_score=0.95
40:                 ))
41:                 
42:         # 3. Retrieve Customer Context
43:         customer = CUSTOMER_STORE.get(customer_id)
44:         if customer:
45:             results.append(RetrievedEvidence(
46:                 source_type="customer",
47:                 source_id=customer_id,
48:                 title="Customer Profile",
49:                 content=str(customer),
50:                 relevance_score=1.0,
51:                 metadata=customer
52:             ))
53:             
54:         return results
55: 
```

### C. Line-by-Line Explanation (Final)

**Lines 36-39: Filling the Case File**
*   **What the computer does:** Records the specific ID of the old case, its title, and its content.
*   **Relevance Score (0.95):** We give this a very high score (95%) because if we found a file with the *exact* same Customer ID, it's almost certainly relevant!

**Line 40: `                ))`**
*   **What the computer does:** Closes the container for that specific case.

**Line 41: `(Empty Line)`**

**Line 42: `# 3. Retrieve Customer Context`**
*   **Meaning:** Comment: Entering the final room—the **Customer Profile Room**.

**Line 43: `customer = CUSTOMER_STORE.get(customer_id)`**
*   **What the computer does:** Looks for the customer's master record using their ID.
*   **Meaning:** `.get` is like checking an index card box for a specific name.

**Line 44: `if customer:`**
*   **What the computer does:** Checks if we actually found a record. (Sometimes a customer doesn't have a profile yet).

**Line 45: `results.append(RetrievedEvidence(`**
*   **What the computer does:** If found, we make one final copy of their profile.

**Line 46: `source_type="customer",`**
*   **What the computer does:** Labels it as a "Customer" book.

**Lines 47-49: Naming the Profile**
*   **What the computer does:** We call it the "Customer Profile" and convert all the facts about them into text (`str(customer)`) so the robots can read them.

**Line 50: `relevance_score=1.0,`**
*   **What the computer does:** Gives it a perfect score!
*   **Why:** You can't make a decision about a customer without knowing who they are. Their profile is 100% relevant.

**Line 51: `metadata=customer`**
*   **What the computer does:** Saves the original raw data too, just in case.

**Line 52: `))`**
*   **What the computer does:** Closes the final book container.

**Line 53: `(Empty Line)`**

**Line 54: `return results`**
*   **What the computer does:** Hand the entire pile of "Raw Books" back to the main Librarian.

**Line 55: `(Empty Line)`**

---

### 🏁 Friendly Recap (Retriever Completed!)

You have finished documenting the factory's **Search Engine**!

You now understand:
1.  How we find **Past Cases** for specific customers.
2.  How we look up the **Customer's Master Record**.
3.  How we use **Relevance Scores** (0.9 to 1.0) to tell the others which books are the most important.

## 3.4 ranker.py – The Expert Grader

Imagine the "Book Finder" (Retriever) comes back with a pile of 50 books. Some of them are perfect, but some of them are just "kind of" useful. For example, if you're looking for "NYC Luxury," the Retriever might bring back a book about "Luxury cars in California" by mistake.

The **Ranker** is like an expert grader who looks at the pile and:
1.  **Sorts** the books from most useful to least useful.
2.  **Throws away** the junk (books with low scores).
3.  **Limits** the pile to the Top 5 most important books.

This keeps our robots from getting "Information Overload." Just like a good student, our AI only focus on the best notes!

### A. Full File Ingestion: `app/context/ranker.py`

```python
1: from typing import List
2: from app.context.models import RetrievedEvidence
3: 
4: class EvidenceRanker:
5:     """
6:     Sorts and filters retrieved evidence to ensure context quality.
7:     """
8:     
9:     def rank_and_filter(self, evidence: List[RetrievedEvidence], top_k: int = 5) -> List[RetrievedEvidence]:
10:         """
11:         Sorts evidence by relevance score and trims to top_k.
12:         """
13:         # 1. Sort by score
14:         sorted_evidence = sorted(evidence, key=lambda x: x.relevance_score, reverse=True)
15:         
16:         # 2. Filter out duplicates or extremely low scores (threshold mock)
17:         filtered = [e for e in sorted_evidence if e.relevance_score > 0.5]
18:         
19:         # 3. Trim to Top K
20:         return filtered[:top_k]
21: 
```

### B. File Purpose
The `ranker.py` file is the "Quality Control" for our research. It ensures that the information we feed to the AI robots is actually relevant and high-quality.

### C. Line-by-Line Explanation

**Line 1: `from typing import List`**
*   **Purpose:** Standardorganizational label for a list of items.

**Line 2: `from app.context.models import RetrievedEvidence`**
*   **What the computer does:** Brings in the "Found Book" container.

**Line 3: `(Empty Line)`**

**Line 4: `class EvidenceRanker:`**
*   **What the computer does:** Defines the "Expert Grader" role.

**Lines 5-7: `""" ... """`**
*   **Meaning:** A note explaining that this role ensures "Context Quality."

**Line 8: `(Empty Line)`**

**Line 9: `def rank_and_filter(self, evidence: List[RetrievedEvidence], top_k: int = 5) -> List[RetrievedEvidence]:`**
*   **What the computer does:** Defines the "Grading Plan."
*   **Input:** The big pile of raw books.
*   **Setting (`top_k = 5`):** By default, we only want to keep the top 5 books.

**Lines 10-12: `""" ... """`**
*   **Meaning:** A note explaining that we are sorting and trimming.

**Line 13: `# 1. Sort by score`**
*   **Meaning:** Comment: Put the best books at the top.

**Line 14: `sorted_evidence = sorted(evidence, key=lambda x: x.relevance_score, reverse=True)`**
*   **What the computer does:** Sorts the pile.
*   **Symbol-by-symbol:** `sorted(...)` is the tool. `key=lambda x: x.relevance_score` tells it to look at the scores we gave in the Retriever. `reverse=True` means put the HIGHEST scores first.

**Line 15: `(Empty Line)`**

**Line 16: `# 2. Filter out duplicates or extremely low scores (threshold mock)`**
*   **Meaning:** Comment: Throwing away the junk.

**Line 17: `filtered = [e for e in sorted_evidence if e.relevance_score > 0.5]`**
*   **What the computer does:** Only keeps books with a score higher than 0.5 (50%).
*   **Why it exists:** If a book only has a 10% chance of being useful, it's better to ignore it than to confuse the AI.

**Line 18: `(Empty Line)`**

**Line 19: `# 3. Trim to Top K`**
*   **Meaning:** Comment: Limiting the pile.

**Line 20: `return filtered[:top_k]`**
*   **What the computer does:** Cuts the list at the Top 5 mark and hands it back to the manager.
*   **Symbol-by-symbol:** `[:top_k]` means "take from index 0 up to 5."

**Line 21: `(Empty Line)`**

---

### 🏁 Friendly Recap (Ranker Completed!)

You've just learned how the factory **controls information quality**!

You now understand:
1.  How we **Sort** data from best to worst.
2.  How we **Filter** out low-quality information.
3.  Why we **Limit** our notes to the Top 5 (to prevent Information Overload).

## 3.5 models.py – The Room of Rules

Imagine our factory library has a very strict rule: you aren't allowed to just carry books around in your hands. You MUST use official **Loading Trays**.

The **Models** file defines exactly what these trays look like. 
1.  **The Raw Tray (`RetrievedEvidence`)**: A deep tray for holding messy, raw books.
2.  **The High-Value Tray (`EnrichedEvidence`)**: A tray with special slots for "Summaries" and "Warning Stickers."
3.  **The Master Briefing Folder (`ContextPacket`)**: The final, gold-embossed folder that holds everything together.

By using these strict "Trays," we make sure that a Book Finder (Retriever) and a Highlighter (Enricher) never get confused. They are always speaking the same language.

### A. Full File Ingestion: `app/context/models.py`

```python
1: from pydantic import BaseModel, Field
2: from typing import List, Dict, Any, Optional
3: 
4: class RetrievedEvidence(BaseModel):
5:     """
6:     Raw data retrieved from a source.
7:     """
8:     source_type: str  # e.g., 'policy', 'case_history', 'customer'
9:     source_id: str
10:     title: str
11:     content: str
12:     relevance_score: float = 0.0
13:     metadata: Dict[str, Any] = Field(default_factory=dict)
14: 
15: class EnrichedEvidence(BaseModel):
16:     """
17:     Transformed evidence with extracted facts and risk signals.
18:     """
19:     source_type: str
20:     source_id: str
21:     summary: str
22:     key_facts: List[str]
23:     risk_signals: List[str]
24:     policy_tags: List[str]
25: 
```

*(Note: File stops at line 25 of 40 for this segment. Remaining lines will follow in the next segment.)*

### B. File Purpose
The `models.py` file acts as the "DNA" or the "Master Blueprint" for all the data being moved around in the library. It uses a tool called **Pydantic** to make sure that if we say something is a "Number," it truly is a number.

### C. Line-by-Line Explanation

**Line 1: `from pydantic import BaseModel, Field`**
*   **What the computer does:** Brings in the "Safety Guard" tools.
*   **Why it exists:** `BaseModel` allows us to create these strict "Trays." If someone tries to put a "Picture" into a slot meant for "Text," Pydantic will stop them and raise an alarm.

**Line 4: `class RetrievedEvidence(BaseModel):`**
*   **What it represents:** The "Raw Loading Tray." It's the very first container we use.

**Line 8: `source_type: str`**
*   **Meaning:** A label saying where the book came from (e.g., "policy").
*   **Constraint:** Must be a string (text).

**Lines 9-11: `source_id`, `title`, `content`**
*   **Meaning:** The basic facts about the book: its identification number, its name, and the actual words inside it.

**Line 12: `relevance_score: float = 0.0`**
*   **Meaning:** The "Quality Grade" (0.0 to 1.0).
*   **Constraint:** `float` means it can be a decimal (like 0.95).

**Line 13: `metadata: Dict[str, Any] = Field(default_factory=dict)`**
*   **Meaning:** The "Extra Pockets." This holds any extra facts that don't fit in the main slots.
*   **Word-by-word:** `default_factory=dict` means if we don't have any extra facts, just leave the pocket empty `{}`.

**Line 15: `class EnrichedEvidence(BaseModel):`**
*   **What it represents:** The "Value-Added Tray." This is what the Highlighter (Enricher) produces.

**Line 21: `summary: str`**
*   **Meaning:** The short version of the book created by the Highlighter.

**Lines 22-24: `key_facts`, `risk_signals`, `policy_tags`**
*   **Meaning:** These are **Lists** of strings.
*   **Significance:** Instead of one long paragraph, we now have a specific list of "Findings" (Facts) and "Warnings" (Risk Signals).

---

### 🏁 Friendly Recap (Models Part 1)

You've just learned how the factory **structures its information**!

You now understand:
1.  Why we use **Loading Trays** (to prevent mistakes).
2.  The difference between a **Raw Book** (`RetrievedEvidence`) and a **Highlighted One** (`EnrichedEvidence`).
3.  How **Pydantic** acts as a safety guard to make sure the data is always correct.

### A. Full File Ingestion: `app/context/models.py` (Final)

```python
26: class ContextPacket(BaseModel):
27:     """
28:     The final handoff object for the platform.
29:     """
30:     request_id: str
31:     request_summary: str
32:     customer_context: Dict[str, Any]
33:     transaction_context: Dict[str, Any]
34:     evidence: List[EnrichedEvidence] = Field(default_factory=list)
35:     policy_references: List[str] = Field(default_factory=list)
36:     prior_cases: List[str] = Field(default_factory=list)
37:     missing_fields: List[str] = Field(default_factory=list)
38:     context_completeness_score: float = 0.0
39:     retrieval_gaps: List[str] = Field(default_factory=list)
40: 
```

### C. Line-by-Line Explanation (Final)

**Line 26: `class ContextPacket(BaseModel):`**
*   **What it represents:** The "Master Briefing Folder." This is the ultimate container that gets handed to the robots.

**Line 30: `request_id: str`**
*   **Why it exists:** To make sure even if 1,000 requests are happening at once, we never give the wrong research folder to the wrong robot!

**Line 31: `request_summary: str`**
*   **Meaning:** A human-readable one-sentence summary of what we are doing.

**Lines 32-33: `customer_context` and `transaction_context`**
*   **Meaning:** These are **Dictionaries** (labeled pockets) that hold the original facts from the order form.

**Line 34: `evidence: List[EnrichedEvidence] = Field(default_factory=list)`**
*   **Meaning:** The main pocket! This holds all the highlighted books we created earlier.

**Lines 35-36: `policy_references` and `prior_cases`**
*   **Meaning:** Quick-reference lists of all the IDs for policies and old cases.
*   **Why:** Robots are lazy—they like having a "Cheat Sheet" list so they don't have to scan every book to find an ID.

**Line 37: `missing_fields: List[str] = Field(default_factory=list)`**
*   **Meaning:** The "Missing Item List." If we couldn't find a customer's risk profile, it goes here.

**Line 38: `context_completeness_score: float = 0.0`**
*   **Meaning:** The "Research Grade" (0.0 to 1.0) we calculated at the end of the Manager's plan.

**Line 39: `retrieval_gaps: List[str] = Field(default_factory=list)`**
*   **Meaning:** The "Warning Log." It records specific failures, like "NO_CUSTOMER_RECORD_FOUND."

**Line 40: `(Empty Line)`**
*   **Why it exists:** Final spacing.

---

### 🏁 Friendly Recap (Models Completed!)

You have finished the **Blueprint for Success**!

You now understand:
1.  How the **Master Briefing Folder** (`ContextPacket`) is organized.
2.  Why we use **Dictionaries** and **Lists** to group information.
3.  How **Defaults** (`default_factory=list`) ensure that even if we find NOTHING, the folder isn't "broken"—it's just empty.

## 3.6 sources.py – The Storage Vault

Imagine walk into the library's basement. Behind a heavy steel door, you see the **Storage Vault**.

This vault isn't empty—it's filled with the actual books, records, and files that we use for research. 
1.  **The Policy Shelf (`POLICY_STORE`)**: Where we keep the official bank laws.
2.  **The Case Shelf (`CASE_STORE`)**: Where we keep folders on specific investigations.
3.  **The Customer Cabinet (`CUSTOMER_STORE`)**: Where we keep a roll-top desk for every customer.

In this project, we are using "Mock Data" (simulated data). It's like having plastic display food in a restaurant window—it looks real, it has all the same info, but it's just for practice!

### A. Full File Ingestion: `app/context/sources.py`

```python
1: from typing import List, Dict, Any
2: 
3: # Mock Data Repositories
4: POLICY_STORE = [
5:     {
6:         "source_id": "POL_402",
7:         "title": "Luxury Item Transaction Policy",
8:         "content": "Transactions over $4,000 for luxury items (watches, jewelry) in high-risk zones (NYC, LA) require manual verification if the account is less than 180 days old.",
9:         "tags": ["LUXURY", "NYC", "THRESHOLD"]
10:     },
11:     {
12:         "source_id": "POL_AML_03",
13:         "title": "Anti-Money Laundering - High Velocity",
14:         "content": "Successive transactions exceeding $2,000 within a 2-hour window must be flagged for SAR review.",
15:         "tags": ["AML", "VELOCITY"]
16:     }
17: ]
18: 
19: CASE_STORE = [
20:     {
21:         "source_id": "CASE_9988",
22:         "title": "Prior Dispute - Luxury WatchNYC",
23:         "content": "Customer disputed $5,000 charge at same merchant 3 months ago. Dispute was resolved in customer favor due to stolen card.",
24:         "customer_id": "AMEX-US-9988"
25:     }
26: ]
27: 
28: CUSTOMER_STORE = {
29:     "AMEX-US-9988": {
30:         "tier": "PLATINUM",
31:         "account_age_days": 120,
32:         "risk_rating": "MEDIUM",
33:         "primary_location": "NYC"
34:     }
35: }
36: 
```

### B. File Purpose
The `sources.py` file is our **Database**. Since we don't want to set up a complex database server just for this lesson, we store our records right here in a simple text file. This makes it easy for the **Retriever** to find everything.

### C. Line-by-Line Explanation

**Lines 4-17: `POLICY_STORE`**
*   **What it represents:** The bank's rules.
*   **Inside the brackets:** Each `{}` is a single rule.
*   **Significance:** Notice the **content** (Line 8). It contains keywords like "over $4,000" and "high-risk zones." This is exactly what the Retriever looks for!

**Lines 19-26: `CASE_STORE`**
*   **What it represents:** History logs.
*   **Connection:** Notice the **customer_id** (Line 24). It matches "AMEX-US-9988." When we search for that customer, this is the file the Retriever will grab.

**Lines 28-35: `CUSTOMER_STORE`**
*   **What it represents:** User profiles.
*   **Symbol-by-symbol:** This is a **Dictionary** (`{}`). The "Key" is the customer's ID ("AMEX-US-9988"), and the "Value" is all their info (Tier, Age, Risk).
*   **Why it exists:** This allows us to find a customer instantly by their name, just like flipping to a specific page in a Rolodex.

---

### 🏁 Friendly Recap (Sources Completed!)

You have finished the **Storage Vault**!

You now understand:
1.  How we simulate a **Database** using simple lists and dictionaries.
2.  What a **Policy**, **Case**, and **Customer Record** actually look like.
3.  Why we use **Keywords** inside the content (to help the searcher find them).

## 3.7 ingestion.py – The Data Intake Pipe

Imagine our library isn't just a building—it's connected to a **High-Speed Vacuum Pipe**. 

New laws, new customer records, and new risk manuals are constantly flying through this pipe. But before we can put them on the shelves, we need to process them. 
*   **The Sorter (`read_markdown_files`)**: Picks up the papers and removes the staples.
*   **The Translator (`get_embedding`)**: Translates the words into a secret "Number Language" (Vectors) that the robots can understand even faster.
*   **The Organizer (`run_ingestion`)**: Puts the final books onto the metal shelves.

This is how we keep the library up-to-date!

### A. Full File Ingestion: `app/context/ingestion.py`

```python
1: import os
2: import json
3: import glob
4: import datetime
5: from openai import OpenAI
6: 
7: # Initialize OpenAI Client
8: client = OpenAI()
9: 
10: # Configuration
11: KNOWLEDGE_BASE_DIR = os.path.join(os.path.dirname(__file__), "knowledge_base")
12: VECTOR_STORE_PATH = os.path.join(os.path.dirname(__file__), "vector_store.json")
13: 
14: BANNER = """
15: ============================================================
16:       SECURE FINANCIAL AI AGENT - POLICY INGESTION
17: ============================================================
18: Status: [ACTIVE]
19: Department: Cybersecurity & Compliance
20: """
21: 
22: 
23: def read_markdown_files():
24:     """Reads all Markdown files and extracts a clean summary."""
25:     documents = []
26:     pattern = os.path.join(KNOWLEDGE_BASE_DIR, "**", "*.md")
27:     for filepath in glob.glob(pattern, recursive=True):
28:         with open(filepath, "r", encoding="utf-8") as f:
29:             content = f.read()
30:             filename = os.path.basename(filepath)
31: 
32:             # Extract first line as summary/title
33:             summary = content.split("\n")[0].replace("# ", "").strip()
34: 
35:             documents.append({"source": filename, "text": content, "summary": summary})
```

*(Note: File stops at line 35 of 96 for this segment. Remaining lines will follow in the next segment.)*

### B. File Purpose
The `ingestion.py` file is a standalone utility. You run it once to take your raw text files (Markdown) and turn them into a "Searchable Database" (Vector Store) that the platform can use.

### C. Line-by-Line Explanation

**Lines 1-4: Imports**
*   **Purpose:** Bringing in basic system tools for files (`os`), data format (`json`), searching folders (`glob`), and time (`datetime`).

**Line 5: `from openai import OpenAI`**
*   **What it does:** Recruits the "Translator" from OpenAI.
*   **Connection:** We use this to turn words into numbers.

**Line 8: `client = OpenAI()`**
*   **What it does:** Wakes up the OpenAI connection.

**Lines 11-12: Paths**
*   **Meaning:** Telling the pipe where our raw files are (`knowledge_base` folder) and where to save the final database (`vector_store.json`).

**Lines 14-20: `BANNER`**
*   **Purpose:** A professional greeting that appears on the screen when you run the pipe.

**Line 23: `def read_markdown_files():`**
*   **What it represents:** The "Papers Sorter" tool.

**Line 25: `documents = []`**
*   **Meaning:** A blank list to hold the raw files we find.

**Line 26: `pattern = ... "**", "*.md"`**
*   **What the computer does:** Tells the searcher to look for any file ending in `.md` (Markdown).
*   **Symbol-by-symbol:** `**` means "look inside every sub-folder too."

**Line 27: `for filepath in glob.glob(pattern, recursive=True):`**
*   **What the computer does:** Actually starts walking through the folders and picking up the files.

**Line 28: `with open(filepath, "r", encoding="utf-8") as f:`**
*   **What the computer does:** Opens each file so we can read the words inside.

**Line 29: `content = f.read()`**
*   **What the computer does:** Copies all the words in the file into a variable named `content`.

**Line 33: `summary = content.split("\n")[0].replace("# ", "").strip()`**
*   **What the computer does:** Extracts the "Title" of the book. 
*   **Meaning:** It takes the very first line of the file and removes the `#` symbol.

**Line 35: `documents.append(...)`**
*   **What the computer does:** Adds our findings (file name, full text, and title) to our master list.

---

### 🏁 Friendly Recap (Ingestion Part 1)

You've just seen how we **find and read** all the laws of the factory!

You now understand:
1.  How we use **OpenAI** as a background translator.
2.  How we **scan all folders** automatically looking for `.md` files.
3.  How we **extract the first line** of a file to use as a title.

### A. Full File Ingestion: `app/context/ingestion.py` (Continued)

```python
36:     return documents
37: 
38: 
39: def get_embedding(text: str) -> list[float]:
40:     """Calls OpenAI to generate a vector embedding."""
41:     try:
42:         response = client.embeddings.create(input=text, model="text-embedding-3-small")
43:         return response.data[0].embedding
44:     except Exception as e:
45:         print(f" [!] Error: {str(e)}")
46:         return []
47: 
48: 
49: def run_ingestion():
50:     print(BANNER)
51:     documents = read_markdown_files()
52:     print(f"[*] Discovered {len(documents)} high-value policy documents.")
53: 
54:     # Create a wrapper object for the vector store to look "Enterprise"
55:     enterprise_store = {
56:         "project": "Secure Financial AI Agent",
57:         "last_updated": datetime.datetime.now().isoformat(),
58:         "total_chunks": len(documents),
59:         "department": "Global Risk & Safety",
60:         "data": [],
61:     }
62: 
63:     for i, doc in enumerate(documents):
64:         print(f"[#] Processing Chunk {i+1}: {doc['source']}...")
65:         vector = get_embedding(doc["text"])
66: 
```

*(Note: File stops at line 66 of 96 for this segment. Remaining lines will follow in the next segment.)*

### C. Line-by-Line Explanation (Continued)

**Line 39: `def get_embedding(text: str) -> list[float]:`**
*   **What it represents:** The "Translator" tool.
*   **The Secret:** Computers are bad at understanding words, but they are great at understanding numbers! This tool turns a paragraph of text into a giant list of numbers (a Vector).

**Line 42: `response = client.embeddings.create(input=text, model="text-embedding-3-small")`**
*   **What the computer does:** Sends the text to OpenAI and asks for the translation.
*   **Significance:** `text-embedding-3-small` is the name of the translation engine.

**Line 43: `return response.data[0].embedding`**
*   **What the computer does:** Picks up the list of numbers and brings it back to the factory.

**Lines 44-46: `except Exception as e: ...`**
*   **Purpose:** Safety Net. If the internet is down and we can't talk to OpenAI, don't crash the factory—just return an empty list.

**Line 49: `def run_ingestion():`**
*   **What it represents:** The "Master Plan" for our ingestion pipe.

**Line 51: `documents = read_markdown_files()`**
*   **What the computer does:** Triggers the "Sorter" we learned about in the last segment.

**Line 55: `enterprise_store = {`**
*   **What it represents:** The "Shipping Crate." 
*   **Why it exists:** We don't just throw the files into the database. We wrap them in a professional-looking package with labels like "Last Updated" and "Department."

**Line 57: `"last_updated": datetime.datetime.now().isoformat(),`**
*   **Meaning:** Records the exact second the database was created.

**Line 63: `for i, doc in enumerate(documents):`**
*   **What the computer does:** Starts a loop. 
*   **Meaning:** `i` is the counter (File #1, File #2). `doc` is the actual file contents.

**Line 64: `print(f"[#] Processing Chunk {i+1}: {doc['source']}...")`**
*   **What the computer does:** Shows a progress bar on the screen for the human operator.

**Line 65: `vector = get_embedding(doc["text"])`**
*   **What the computer does:** Calls the "Translator" to turn the current file into numbers.

---

### 🏁 Friendly Recap (Ingestion Part 2)

You've just learned how the **AI Brain** translates information!

You now understand:
1.  What an **Embedding** is (turning words into a list of numbers).
2.  How we use **OpenAI** to do the translation.
3.  How we organize our findings into an **"Enterprise Store"** format with professional labels.

### A. Full File Ingestion: `app/context/ingestion.py` (Final)

```python
67:         if vector:
68:             enterprise_store["data"].append(
69:                 {
70:                     "id": f"CHUNK-{1000 + i}",
71:                     "source": doc["source"],
72:                     "summary": doc["summary"],
73:                     "text_preview": doc["text"][:100].replace("\n", " ") + "...",
74:                     "metadata": {
75:                         "author": "Compliance Safety Team",
76:                         "compliance_level": "High",
77:                     },
78:                     "embedding": vector,
79:                     "text": doc["text"],
80:                 }
81:             )
82: 
83:     # Save the vector store with professional formatting
84:     with open(VECTOR_STORE_PATH, "w", encoding="utf-8") as f:
85:         json.dump(enterprise_store, f, indent=4)
86: 
87:     print(f"\n[SUCCESS] Vector Store created for presentation: {VECTOR_STORE_PATH}")
88:     print("=" * 60)
89: 
90: 
91: if __name__ == "__main__":
92:     if not os.getenv("OPENAI_API_KEY"):
93:         print("[X] ERROR: OPENAI_API_KEY environment variable not found.")
94:     else:
95:         run_ingestion()
96: 
```

### C. Line-by-Line Explanation (Final)

**Line 67: `if vector:`**
*   **What it does:** Checks if our translation was successful. If the translator failed, we don't save a broken book.

**Line 68: `enterprise_store["data"].append(`**
*   **What it represents:** Placing the translated book into the "Shipping Crate."

**Lines 70-73: Filling the Book Labels**
*   **What the computer does:** Gives the book a unique ID (like "CHUNK-1001"), records the source file name, the summary, and a tiny "Preview" of the first 100 letters.

**Lines 74-77: `metadata`**
*   **Meaning:** Adding professional stickers like "Author: Compliance Safety Team."

**Line 78: `"embedding": vector,`**
*   **Meaning:** This is the most important part! It's the list of numbers (the translation) our robots will use to find this book later.

**Line 79: `"text": doc["text"],`**
*   **Meaning:** We keep the original English text too, so the robots can read the full details once they find the right book.

**Lines 84-85: `with open(VECTOR_STORE_PATH, "w"...) as f: json.dump(...)`**
*   **What the computer does:** The "Vault Lock." It takes our digital shipping crate and writes it permanently to the computer's hard drive as a `.json` file.
*   **Meaning:** `indent=4` makes the file look neat and tidy if a human opens it.

**Line 87: `print(f"\n[SUCCESS] ...")`**
*   **Purpose:** Celebtation! It tells the user that the vacuum pipe is finished.

**Line 91: `if __name__ == "__main__":`**
*   **Meaning:** The "Start Button." This tells Python: "Only run the vacuum pipe if I double-click THIS file."

**Line 92: `if not os.getenv("OPENAI_API_KEY"):`**
*   **Purpose:** Safety Check. Before we start, make sure we have the "Key" to the OpenAI translation office.

**Line 95: `run_ingestion()`**
*   **What it does:** Actually pulls the lever and starts the entire process.

---

### 🏁 Friendly Recap (Chapter 3 Completed!)

Congratulations! You've just explored the entire **Research Library** of our agentic factory.

In this chapter, you learned:
1.  How the **Librarian-in-Chief** (`builder.py`) manages the whole research plan.
2.  How the **Expert Highlighter** (`enricher.py`) marks imports facts.
3.  How the **Book Finder** (`retriever.py`) sprints through different storage rooms.
4.  How the **Expert Grader** (`ranker.py`) ensures only the best notes reach our robots.
5.  How we use **Strict Loading Trays** (`models.py`) to move data safely.
6.  How the **High-Speed Vacuum Pipe** (`ingestion.py`) pulls new research into the vault.

**You're now a master of how AI "knows" things! In the next chapter, we'll look at the "Factory Workers" themselves: the Agents!**
