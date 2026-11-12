"""
Enterprise Hands-On Labs Script Repository: Mosaic AI & MLflow Compound Agents
Covers Labs 151 - 175: Migrating Palantir AIP to Databricks Mosaic AI Agent Framework,
Vector Search, MLflow 2.x Tracing, and Automated LLM Evaluation.
"""

import os
import json
from typing import Dict, Any, List
from pydantic import BaseModel, Field

class OrderContext(BaseModel):
    order_id: str
    customer_id: str
    sku_id: str
    order_amount_usd: float
    shortage_units: float

class MosaicSupplyChainCompoundAgent:
    """
    Compound AI System replicating Palantir AIP Agent Studio workflows.
    Integrates Vector Search tools, reasoning chains, and Human-in-the-Loop policies.
    """

    def __init__(self):
        self.foundation_model_endpoint = "databricks-meta-llama-3-1-70b-instruct"
        self.vector_search_index = "enterprise_operations.gold.inventory_vector_idx"

    def tool_lookup_inventory_vector_search(self, sku_id: str, units_needed: float) -> List[Dict[str, Any]]:
        """Tool 1: Queries Unity Catalog Vector Search index for available warehouse stock."""
        return [
            {"warehouse_id": "WH-ATLANTA", "sku_id": sku_id, "available_stock": 120.0, "distance_miles": 340},
            {"warehouse_id": "WH-DALLAS", "sku_id": sku_id, "available_stock": 85.0, "distance_miles": 820}
        ]

    def tool_calculate_shipping_premium(self, distance_miles: int, units: float) -> float:
        """Tool 2: Calculates expedited logistics freight surcharge."""
        return round(150.0 + (distance_miles * 0.45) + (units * 2.2), 2)

    def predict(self, model_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Agent reasoning loop with tool execution and Human-in-the-Loop guardrail enforcement.
        """
        order_id = model_input.get("order_id", "UNKNOWN")
        amount_usd = float(model_input.get("order_amount_usd", 0.0))
        sku_id = model_input.get("sku_id", "")
        shortage_units = float(model_input.get("shortage_units", 0.0))

        # Step 1: Tool execution
        candidates = self.tool_lookup_inventory_vector_search(sku_id, shortage_units)
        best_wh = candidates[0]
        expedite_cost = self.tool_calculate_shipping_premium(best_wh["distance_miles"], shortage_units)

        # Step 2: Policy & Guardrail Check (Human-in-the-loop if order > $50k)
        requires_human_approval = amount_usd > 50000.0

        decision_payload = {
            "order_id": order_id,
            "recommended_source_warehouse": best_wh["warehouse_id"],
            "reallocated_units": shortage_units,
            "estimated_expedite_cost_usd": expedite_cost,
            "requires_human_approval": requires_human_approval,
            "governance_status": "PENDING_OPERATOR_APPROVAL" if requires_human_approval else "AUTONOMOUSLY_APPROVED",
            "policy_rule": "HITL threshold triggered for orders exceeding $50,000 USD."
        }

        return decision_payload

if __name__ == "__main__":
    agent = MosaicSupplyChainCompoundAgent()
    sample_request = {
        "order_id": "ORD-77401",
        "customer_id": "CUST-992",
        "sku_id": "SKU-TURBINE-09",
        "order_amount_usd": 145000.0,
        "shortage_units": 30.0
    }
    decision = agent.predict(model_input=sample_request)
    print("Agent Evaluation Output:")
    print(json.dumps(decision, indent=2))
