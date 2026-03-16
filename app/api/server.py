# api/server.py
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from monitoring.metrics import event_bus
from services.transaction_service import TransactionRequest, transaction_service

from fastapi.staticfiles import StaticFiles
import os

from app.api.telemetry import router as telemetry_router

app = FastAPI(title="BlueShield Secure Financial Agent API")

# Register Telemetry Bridge
app.include_router(telemetry_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Serve Frontend Dashboard (New React Version)
dashboard_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "dashboard")
)
app.mount(
    "/console", StaticFiles(directory=dashboard_path, html=True), name="console"
)


# Real-time WebSocket connection manager
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("[WebSocket] Client connected")

    async def send_event(event):
        try:
            await websocket.send_json(event)
        except Exception:
            pass  # Handle closed connections gracefully

    # Subscribe this websocket to the central event bus
    # The TelemetryManager from telemetry.py also handles broad connections
    event_bus.subscribe(send_event)

    try:
        while True:
            # Keep the connection alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        print("[WebSocket] Client disconnected")


@app.post("/process_transaction")
async def process_transaction(req: TransactionRequest):
    return await transaction_service.process(req)


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "console_url": "http://127.0.0.1:8000/console/",
        "api_v1": "http://127.0.0.1:8000/telemetry/metrics"
    }


# Telemetry Bridge: Allows external processes (like main.py) to push events to the dashboard
class InternalEvent(BaseModel):
    type: str
    data: dict


@app.post("/internal/emit_event")
async def emit_internal_event(event: InternalEvent):
    await event_bus.emit(event.type, event.data)
    return {"status": "broadcasted"}


@app.post("/reset")
def reset_database():
    from tools.mock_db import reset_db

    reset_db()
    return {"status": "success", "message": "Database reset to initial state"}
