import asyncio
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.events.producer import producer
from app.events.consumer import consumer
from app.events.queue import event_queue
from app.events.lifecycle import lifecycle_manager

async def run_event_verification():
    print("\n" + "="*80)
    print("      PHASE 6: EVENT-DRIVEN PIPELINE VERIFICATION")
    print("="*80 + "\n")

    # Define Test Scenarios - aligned with PlatformRequest schema
    scenarios = [
        {
            "name": "Scenario 1: Safe Automation",
            "payload": {
                "request_id": "REQ-EVT-001",
                "use_case_type": "expense_approval",
                "customer_context": {"customer_id": "CUST_S01", "tier": "standard"},
                "business_payload": {
                    "amount": 45.50,
                    "merchant": "Office Essentials",
                    "domain": "OPERATIONS"
                },
                "risk_metadata": {"prior_score": 12},
                "source": "event_pipeline"
            }
        },
        {
            "name": "Scenario 2: Elevated Risk (Review Required)",
            "payload": {
                "request_id": "REQ-EVT-002",
                "use_case_type": "high_value_transaction",
                "customer_context": {"customer_id": "CUST_S02", "tier": "premium"},
                "business_payload": {
                    "amount": 12500.0,
                    "merchant": "Luxury Timepieces",
                    "domain": "HIGH_VALUE"
                },
                "risk_metadata": {"prior_score": 78, "flagged": True},
                "source": "event_pipeline"
            }
        },
        {
            "name": "Scenario 3: Policy Violation (Blocked)",
            "payload": {
                "request_id": "REQ-EVT-003",
                "use_case_type": "merchant_investigation",
                "customer_context": {"customer_id": "CUST_S03", "tier": "standard"},
                "business_payload": {
                    "amount": 999.0,
                    "merchant": "M_999",
                    "domain": "RETAIL",
                    "pii_present": True
                },
                "risk_metadata": {"prior_score": 91, "pii_flag": True},
                "source": "event_pipeline"
            }
        }
    ]

    print(f"[SYSTEM] Initializing asynchronous worker...")
    
    # 1. Produce events
    print(f"\n[PRODUCER] Ingesting {len(scenarios)} events into the queue...")
    for s in scenarios:
        print(f"\n--- {s['name']} ---")
        producer.produce(s['payload'])

    print(f"\n[QUEUE] Current Depth: {event_queue.get_depth()}")

    # 2. Consume and Process
    print(f"\n[CONSUMER] Starting worker loop for queued events...")
    # Run consumer until queue is empty
    await consumer.start(once=True)

    # 3. Final Report
    print("\n" + "="*80)
    print("      LIFECYCLE TRANSITION SUMMARY")
    print("="*80)
    
    for s in scenarios:
        req_id = s['payload']['request_id']
        # Find the event in the history that matches this request_id
        # In a real system, we'd use correlation_id
        matching_events = [e for e in event_queue.peek_history() if e.payload.get('request_id') == req_id]
        if matching_events:
            event = matching_events[0]
            history = lifecycle_manager.get_history(event.event_id)
            print(f"\nRequest: {req_id} ({s['name']})")
            print(f"  Event ID: {event.event_id}")
            print(f"  Final Status: {event.status.value}")
            print(f"  Transitions: {' -> '.join([h['to'].value for h in history])}")
        else:
            print(f"\n[ERROR] Event for {req_id} not found in history.")

    print("\n" + "="*80)
    print("      VERIFICATION COMPLETE: ASYNCHRONOUS PIPELINE RESOLVED")
    print("="*80 + "\n")

if __name__ == "__main__":
    asyncio.run(run_event_verification())
