# amex-agent-business-automation
"The Amex Agent Business Automation project is a secure, policy-driven AI runtime. It integrates with the Sentinel risk engine to evaluate and govern agent actions (like account freezes) using RAG-retrieved policies. It features deterministic workflows and safety validators to ensure safe, context-aware execution of business automations."

# Amex Agent Business Automation 🚀

[![Status: Completed](https://img.shields.io/badge/Status-Completed-success)](#)
[![Python version](https://img.shields.io/badge/python-3.10%2B-blue)](#)
[![Business Focus](https://img.shields.io/badge/ROI-High-gold)](#)

## 📌 Executive Summary
The **Amex Agent Business Automation** project is a secure, policy-driven AI runtime designed to automate highly critical, volume-heavy operational processes like fraud triage and credit underwriting. 

By integrating deterministic workflows with LLM decision-making, policy retrieval (RAG), and a strict safety validator (Sentinel), this system acts as a **Level 1 autonomous agent** capable of making rapid, compliant decisions at scale.

### 💰 The Business Problem (The "Million Dollar Problem")
Financial institutions face massive operational costs associated with manual review processes. 
- **High Volume & Slow Response:** Human analysts take minutes to hours to review suspicious transactions or credit requests, leading to increased fraud losses and poor customer experiences.
- **Operational Overhead:** Maintaining large teams of L1 support and compliance officers is expensive.
- **Inconsistent Decisioning:** Human analysts can misinterpret complex, evolving financial rules, leading to costly compliance fines.

### 💡 The Solution & ROI
This AI agent mitigates these problems by bringing the cost-per-decision down to near-zero while enforcing 100% compliance with internal policies.
1. **Automated Fraud Triage:** Instantly processes transaction anomalies. High-risk intents trigger immediate account freezes (preventing losses), while ambiguous cases are intelligently escalated.
2. **Speed to Action:** Reduces time-to-resolution from days/hours down to milliseconds.
3. **Guaranteed Safety:** The integration with the **Sentinel Runtime Risk Engine** guarantees that the AI cannot hallucinate its way into executing unauthorized, high-risk actions. If an action breaches risk thresholds, it is automatically blocked or escalated to a human.

**Estimated Business Impact:** Translates to potentially **millions of dollars saved annually** through combined fraud loss prevention and a drastic reduction in manual operational overhead.

![Amex ROI Dashboard](assets/roi_dashboard.png)

---

## 🏗️ Architecture & Core Components

```mermaid
graph TD
    User([Customer or Employee]) --> API[FastAPI Entry Point]
    API --> Orchestrator[Agent Orchestrator]
    
    subgraph "Phase 4: Intelligence Layer"
        Orchestrator --> Retriever[RAG Retriever]
        Retriever --> VectorDB[(Vector Store JSON)]
        Orchestrator --> Planner[Reasoning Planner]
    end
    
    subgraph "Phase 1: Safety Layer"
        Orchestrator --> Schema[Schema Validator]
        Orchestrator --> Financial[Financial Rule Engine]
        Orchestrator --> Compliance[Compliance Validator]
    end
    
    subgraph "Phase 3: Risk Evaluation"
        Orchestrator --> Sentinel[Sentinel Runtime Risk Engine]
    end
    
    Orchestrator --> Decision{Decision Handler}
    Decision -- ALLOW --> Workflow[Concrete Workflow Execution]
    Decision -- BLOCK --> Fail[Audit Log / Fail]
    Decision -- REVIEW --> Escalation[Human Review Ticket]
```

1. **Stateful Workflows (`workflows/`)**: Deterministic state machines (e.g., `FraudTriageWorkflow`) that guide the LLM through a strict sequence: Intent Validation -> Context Retrieval -> Risk Evaluation -> Execution.
2. **Policy Retrieval (RAG) (`rag/`)**: Dynamically loads real-time compliance policies and rules to inform the agent's context.
3. **Sentinel Risk Engine (`runner/sentinel_client.py`)**: A dedicated safety layer that scores the risk of the agent's intended action (e.g., `freeze_account`) and issues hard `ALLOW`, `REVIEW`, or `BLOCK` verdicts.
4. **Concrete Tools (`tools/`)**: The actual atomic functions the agent uses to interact with the system (e.g., `mock_db`, `credit_tools`, `escalation_tools`).
5. **Validators (`validator/`)**: Pre-execution checks that ensure data structures and inputs meet strict financial rules and compliance schemas before any tool is triggered.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- An OpenAI API Key (or equivalent LLM provider, depending on configuration)

### 🖼️ Visual Demonstration

### 🎥 Live Video Demonstration
Check out the full walkthrough of the Amex Agent in action: 
**[Watch the Live Demo Recording](https://1drv.ms/v/c/656ad0e98a3b6fab/IQBEezzZOPX3RIW8fCLyI_wwAQKfjAcJW7n5AtJCiLczB94?e=8kBjLY)**

To see the agent in action via text logs, we have also provided a [Detailed Showcase](SHOWCASE.md). Below are the "Money Shots" of our safe automation system:

### 1. The Autonomous Orchestrator (Live Demo)
This screenshot shows the agent processing a fraud triage request, retrieving policy context via RAG, and generating a reasoning plan before execution.
![Live Demo Placeholder](assets/demo_execution.png)

### 2. 100% Safety Compliance (Unit Tests)
Validating the "Trust but Verify" model. This shows our 10+ core safety and compliance tests passing, ensuring every edge case is governed.
![Testing Placeholder](assets/safety_tests.png)

### 3. Policy Intelligence (RAG Ingestion)
Demonstrating how the agent "learns" Amex policies by ingesting markdown documents into a high-speed vector store.
![RAG Ingestion Placeholder](assets/rag_ingestion.png)

---

## 🛠️ Installation & Usage

1. **Clone the repository:**
   ```bash
   git clone <YOUR_GITHUB_REPOSITORY_URL>
   cd amex-agent-business-automation
   ```

2. **Set up the virtual environment:**
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt  # (Ensure you generate a requirements.txt if you haven't)
   # Or install testing tools:
   pip install pytest
   ```

### Running Tests
The project features a comprehensive test suite that validates the agent's behavior, RAG retrieval, and the Sentinel runtime's ability to block unsafe actions.

```bash
pytest
```

To run a specific test suite (e.g., concrete execution and sentinel integration):
```bash
pytest tests/test_concrete_execution.py -v
```

---

## 🛡️ Security & Compliance First
This project isn't just an LLM wrapper; it's a **business-first AI deployment** built around the principles of deterministic safety. The LLM acts as the *reasoning engine*, but the system's *actions* are rigidly bounded by code, eliminating the risk of catastrophic AI malfunctions in a production financial environment.
