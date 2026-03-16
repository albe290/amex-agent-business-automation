import sys
import os
from datetime import datetime

# Add the project root to sys.path to allow imports from app.*
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.intake.schemas import PlatformRequest
from app.control_plane.decision import ControlPlaneDecision
from app.context.builder import ContextBuilder, ContextPacket
from app.strategy.router import StrategyRouter, StrategyPath
from app.audit.trace import AuditTrace, AuditLogger

from app.control_plane.coordinator import ControlPlaneCoordinator

from app.strategy.planner import StrategyPlanner
from app.agents.analyst_agent import AnalystAgent
from app.agents.writer_agent import WriterAgent
from app.actions.executor import ActionExecutor
from app.review.queue import ReviewQueue

def run_platform_flow():
    print("--- Starting End-to-End Platform Flow Verification ---")

    # 1. Intake
    print("\n[INTAKE] Normalizing request...")
    request = PlatformRequest(
        use_case_type="fraud_investigation",
        customer_context={"id": "AMEX-US-9988", "segment": "PLATINUM"},
        business_payload={"amount": 4500.0, "merchant": "Luxury Watch Boutique", "location": "NYC", "account_age_days": 120},
        risk_metadata={"velocity_flags": 0, "last_fraud_score": 10},
        source="mobile_app"
    )
    print(f"   Normalized Request ID: {request.request_id}")

    # 2. Context Builder
    print("\n[CONTEXT] Building evidence-grounded context packet...")
    context_builder = ContextBuilder()
    context = context_builder.build_context(request)
    print(f"   Context Completeness: {context.context_completeness_score:.2f}")
    # print(f"   Policies: {', '.join(context.policy_context)}")

    # 3. Control Plane Decision
    print("\n[CONTROL PLANE] Running real validation and risk scoring...")
    coordinator = ControlPlaneCoordinator()
    decision = coordinator.process_request(request)
    print(f"   Risk Score: {decision.risk_score}")
    print(f"   Validation: {decision.validation_status}")
    print(f"   Policy Hits: {', '.join(decision.policy_hits)}")
    print(f"   Requires Review: {decision.requires_review}")

    # 4. Strategy Routing & Planning
    print("\n[STRATEGY] Selecting execution path and building plan...")
    path = StrategyRouter.select_path(decision)
    print(f"   Selected Path: {path.value}")
    
    planner = StrategyPlanner()
    plan = planner.build_plan(path, context.dict())
    print(f"   Plan Steps: {[step['step'] for step in plan]}")

    # 5. Agent Execution
    print("\n[AGENTS] Executing bounded worker tasks with context packets...")
    analyst = AnalystAgent()
    writer = WriterAgent()
    
    agent_results = []
    for step in plan:
        if step.get("agent") == "analyst_agent":
            analysis = analyst.run_deep_dive(context)
            print(f"   Analyst: Findings: {analysis.findings[:1]}... Confidence: {analysis.confidence}")
            agent_results.append(analysis.dict())
        elif step.get("agent") == "writer_agent":
            report = writer.generate_report(agent_results, context.request_summary)
            print(f"   Writer: Recommendation: {report.final_recommendation}")
            agent_results.append(report.dict())

    # 6. Action or Review
    print("\n[OUTCOME] Resolving final platform outcome...")
    if decision.requires_review:
        print("   Escalating to human review queue...")
        queue = ReviewQueue()
        packet = queue.create_escalation(request.request_id, decision.dict(), agent_results)
        print(f"   Review Packet Created: Risk {packet.risk_score}, Recommendation {packet.recommendation}")
    else:
        print("   Executing automated action...")
        executor = ActionExecutor()
        output = executor.execute(request.request_id, agent_results)
        print(f"   Platform Output: {output.status} - {output.message}")

    # 7. Audit Trace
    print("\n[AUDIT] Recording full platform execution trace...")
    trace = AuditTrace(
        request_id=request.request_id,
        strategy_path=path.value,
        control_plane_result=decision.dict(),
        agent_outputs=agent_results,
        context_completeness=context.context_completeness_score,
        evidence_count=len(context.evidence),
        final_outcome="STRATEGY_EXECUTED",
        requires_human_review=decision.requires_review
    )
    logger = AuditLogger()
    logger.log_trace(trace)

    print("\nVerification complete. End-to-end path resolved.")

if __name__ == "__main__":
    run_platform_flow()
