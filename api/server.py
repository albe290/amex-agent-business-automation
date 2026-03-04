from fastapi import FastAPI
import uvicorn
from api.customer_routes import router as customer_router
from api.employee_routes import router as employee_router
from monitoring.metrics import metrics

app = FastAPI(
    title="Amex Agent Business Automation API",
    description="A secure, policy-driven AI runtime for processing financial workflows.",
    version="1.0.0",
)

# Register routes
app.include_router(
    customer_router, prefix="/api/v1/customer", tags=["Customer Self-Service"]
)
app.include_router(
    employee_router, prefix="/api/v1/employee", tags=["Employee Automation"]
)


@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "Amex Agent Automation Runtime is healthy."}


@app.get("/metrics")
async def get_system_metrics():
    """Expose high-level performance metrics."""
    return metrics.get_metrics()


if __name__ == "__main__":
    uvicorn.run("api.server:app", host="0.0.0.0", port=8000, reload=True)
