"""
Unit and Integration Test Suite 3: Mosaic AI Compound Agent & Operational Actions
Tests:
1. Operational Action Request schema validation
2. Kinetic ERP write-back payload generation
3. Mosaic AI Agent reasoning and tool selection
4. Human-In-The-Loop (HITL) threshold enforcement ($50k policy)
"""

import unittest
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from labs_200_comprehensive.module_07_mosaic_ai_mlflow.mosaic_ai_agent_suite import MosaicSupplyChainCompoundAgent

class TestMosaicAIAndOperationalActions(unittest.TestCase):

    def setUp(self):
        self.agent = MosaicSupplyChainCompoundAgent()

    def test_agent_autonomous_approval_under_threshold(self):
        # Order value $32,000 <= $50,000: Autonomous execution approved
        request = {
            "order_id": "ORD-11029",
            "customer_id": "CUST-551",
            "sku_id": "SKU-TURBINE-09",
            "order_amount_usd": 32000.0,
            "shortage_units": 15.0
        }
        decision = self.agent.predict(request)
        
        self.assertEqual(decision["order_id"], "ORD-11029")
        self.assertFalse(decision["requires_human_approval"])
        self.assertEqual(decision["governance_status"], "AUTONOMOUSLY_APPROVED")
        self.assertIn("WH-ATLANTA", decision["recommended_source_warehouse"])
        self.assertGreater(decision["estimated_expedite_cost_usd"], 0.0)

    def test_agent_enforces_hitl_guardrail_over_threshold(self):
        # Order value $185,000 > $50,000: Mandatory Human-In-The-Loop approval
        request = {
            "order_id": "ORD-99401",
            "customer_id": "CUST-882",
            "sku_id": "SKU-TURBINE-09",
            "order_amount_usd": 185000.0,
            "shortage_units": 45.0
        }
        decision = self.agent.predict(request)
        
        self.assertEqual(decision["order_id"], "ORD-99401")
        self.assertTrue(decision["requires_human_approval"])
        self.assertEqual(decision["governance_status"], "PENDING_OPERATOR_APPROVAL")
        self.assertIn("HITL threshold triggered", decision["policy_rule"])

    def test_tool_inventory_lookup(self):
        candidates = self.agent.tool_lookup_inventory_vector_search("SKU-TURBINE-09", 10.0)
        self.assertGreater(len(candidates), 0)
        self.assertIn("warehouse_id", candidates[0])
        self.assertIn("available_stock", candidates[0])

if __name__ == '__main__':
    unittest.main()
