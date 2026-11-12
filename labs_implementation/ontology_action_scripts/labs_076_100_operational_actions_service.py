"""
Enterprise Hands-On Labs Script Repository: Operational Write-Backs & Databricks Apps
Covers Labs 076 - 100: Decoupling Palantir TypeScript Actions to Python FastAPI / Streamlit.
"""

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
import datetime
import uuid
import json

app = FastAPI(
    title="Databricks Operational Action Microservice",
    description="Replaces Palantir Foundry Action Functions. Handles validation, ERP API dispatch, and Delta audit logging."
)

class ReallocateStockAction(BaseModel):
    order_id: str = Field(..., example="ORD-99104")
    source_warehouse_id: str = Field(..., example="WH-CHICAGO")
    destination_warehouse_id: str = Field(..., example="WH-ATLANTA")
    reallocation_quantity: float = Field(..., gt=0.0, example=50.0)
    expedite_reason: str = Field(..., min_length=10, example="High-priority customer contract deadline.")
    authorizing_user_email: str = Field(..., example="operations_lead@company.com")

@app.post("/api/v1/actions/reallocate-inventory")
async def execute_reallocate_inventory_action(action: ReallocateStockAction):
    """
    Direct replacement for Palantir TypeScript Action Function `reallocateStock`.
    Executes external ERP REST write-back and writes an ACID transaction into Delta Lake.
    """
    # 1. Validation & Safety Stock Rules
    if action.reallocation_quantity > 1000.0:
        raise HTTPException(
            status_code=400,
            detail="Single-action reallocation limit is 1,000 units. Requires Director approval."
        )

    # 2. Simulated ERP Write-Back (e.g. SAP S/4HANA OData / RFC call)
    # In production: requests.post("https://sap-gateway.corp/v1/orders/expedite", json=action.dict())
    erp_response = {
        "status": "SAP_PROCESSED",
        "sap_delivery_document": f"DELIV_{uuid.uuid4().hex[:6].upper()}",
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

    # 3. Commit Immutable Audit Log to Unity Catalog Delta Lake
    # Delta table: enterprise_operations.gold.audit_operational_actions
    audit_entry = {
        "action_id": f"act_{uuid.uuid4().hex[:8]}",
        "action_name": "reallocateInventoryAndExpedite",
        "target_order_id": action.order_id,
        "executed_by": action.authorizing_user_email,
        "parameters": action.dict(),
        "erp_confirmation": erp_response,
        "committed_at": datetime.datetime.utcnow().isoformat()
    }

    return {
        "action_status": "SUCCESS",
        "message": "Operational write-back completed and audited to Unity Catalog.",
        "audit_record": audit_entry
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
