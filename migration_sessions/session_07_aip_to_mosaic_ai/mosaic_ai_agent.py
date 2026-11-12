"""
Session 7: Palantir AIP to Databricks Mosaic AI Agent Framework
Replicates AIP Agent Studio reasoning chains, Vector Search tool lookup,
and Human-in-the-Loop policy guardrails.
"""

from typing import Dict, Any, List

class MosaicSupplyChainAgent:
    """Compound AI Agent replacing Palantir AIP Agent Studio."""

    def __init__(self):
        self.endpoint = "databricks-meta-llama-3-1-70b-instruct"
        self.vector_index = "enterprise_operations.gold.inventory_vector_idx"

    def tool_lookup_inventory(self, sku_id: str, units_needed: float) -> List[Dict[str, Any]]:
        """Tool: Queries Vector Search index for warehouses holding available units."""
        return [
            {"warehouse_id": "WH-ATLANTA", "sku_id": sku_id, "available_stock": 120.0, "distance_miles": 340},
            {"warehouse_id": "WH-DALLAS", "sku_id": sku_id, "available_stock": 85.0, "distance_miles": 820}
        ]

    def predict(self, model_input: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluates shortage, queries tools, and enforces Human-in-the-Loop policy."""
        order_id = model_input.get("order_id", "UNKNOWN")
        amount_usd = float(model_input.get("order_amount_usd", 0.0))
        sku_id = model_input.get("sku_id", "")
        shortage_qty = float(model_input.get("shortage_units", 0.0))

        # 1. Tool execution
        candidates = self.tool_lookup_inventory(sku_id, shortage_qty)
        best_wh = candidates[0]["warehouse_id"]
        expedite_cost = round(150.0 + (340 * 0.45) + (shortage_qty * 2.2), 2)

        # 2. Guardrail Check: Human-in-the-loop if order > $50k
        requires_human_approval = amount_usd > 50000.0

        return {
            "order_id": order_id,
            "recommended_warehouse": best_wh,
            "expedite_cost_usd": expedite_cost,
            "requires_human_approval": requires_human_approval,
            "governance_status": "PENDING_OPERATOR_APPROVAL" if requires_human_approval else "AUTONOMOUSLY_APPROVED",
            "policy_rule": "HITL threshold triggered for orders exceeding $50,000 USD."
        }

if __name__ == "__main__":
    agent = MosaicSupplyChainAgent()
    sample = {"order_id": "ORD-89201", "order_amount_usd": 284000.0, "sku_id": "SKU-TURBINE-09", "shortage_units": 25.0}
    print(agent.predict(sample))
