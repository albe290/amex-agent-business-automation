from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List, Dict, Any
import asyncio
import json
from app.audit.trace import AuditLogger

router = APIRouter(prefix="/telemetry", tags=["telemetry"])

class TelemetryManager:
    """
    Manages real-time telemetry streaming to dashboard clients.
    """
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: Dict[str, Any]):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                # Connection might be stale
                pass

manager = TelemetryManager()

@router.websocket("/ws")
async def telemetry_websocket(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        # Send initial state/greeting
        await websocket.send_json({
            "type": "SYSTEM_CONNECTED",
            "data": {"status": "ONLINE", "worker_id": "AMEX_CORE_01"}
        })
        while True:
            # Keep connection alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@router.get("/metrics")
async def get_platform_metrics():
    """
    Returns high-level platform performance metrics.
    """
    # In a real system, these would be pulled from a metrics DB (Prometheus/Timescale)
    return {
        "automation_rate": 0.642,
        "review_rate": 0.217,
        "escalation_rate": 0.113,
        "block_rate": 0.046,
        "avg_latency_ms": 1420,
        "total_requests": 14205
    }

@router.get("/governance/policy-hits")
async def get_policy_hits():
    return {
        "HIGH_VALUE_TRANSACTION": 42,
        "RISK_SCORE_CRITICAL": 28,
        "AML_SECTION_3": 114,
        "SECURITY_VALIDATION_FAILURE": 9
    }
