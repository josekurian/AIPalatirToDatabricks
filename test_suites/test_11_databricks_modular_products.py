import unittest
from UP.scripts.unified_platform_orchestrator import UnifiedPlatformOrchestrator
from Genie.scripts.genie_space_automation import GenieSpaceManager
from LB.scripts.lakebase_operational_store import LakebaseStateManager
from AB.scripts.agent_bricks_mosaic_runtime import AgentBricksRuntime
from LF.scripts.lakeflow_pipeline_automation import LakeflowPipelineManager
from LK.scripts.lakehouse_iceberg_engine import LakehouseStorageEngine
from UC.scripts.unity_catalog_governance_automation import UnityCatalogGovernanceManager

class TestDatabricksModularProducts(unittest.TestCase):

    def test_up_orchestrator_deployment_and_health(self):
        """Verifies /UP orchestrator deploys all 6 product pillars with 100% health."""
        up = UnifiedPlatformOrchestrator()
        dep_res = up.deploy_unified_platform("prod")
        self.assertEqual(dep_res["status"], "COMPLETED")
        self.assertEqual(dep_res["modules_deployed"], 6)

        health = up.verify_platform_health()
        for mod, status in health.items():
            self.assertEqual(status, "HEALTHY")

    def test_genie_nlp_sql_generation_and_escalation(self):
        """Verifies /Genie translates natural language to certified SQL and escalates ambiguity."""
        genie = GenieSpaceManager("Revenue Space", "Finance")
        genie.register_uc_page("Consumption Revenue Recognition", "Finance", True, "SELECT SUM(net_amount) FROM gold.finance.fact_transactions")
        
        # Test matched certified prompt
        res1 = genie.process_natural_language_prompt("What is our recurring ARR?")
        self.assertEqual(res1["status"], "SQL_GENERATED")
        self.assertGreaterEqual(res1["confidence_score"], 0.90)
        self.assertTrue(res1["is_certified"])

        # Test unmapped prompt escalates
        res2 = genie.process_natural_language_prompt("Explain obscure metric 99")
        self.assertEqual(res2["status"], "AMBIGUOUS_ESCALATED")
        self.assertEqual(res2["action"], "ESCALATED_TO_STEWARD_REVIEW_QUEUE")

    def test_lakebase_acid_write_back(self):
        """Verifies /LB manages operational key-value state and audit trails."""
        lb = LakebaseStateManager()
        commit_res = lb.put_state("ORDER-100", {"status": "PENDING", "amount": 2500}, "api_client")
        self.assertEqual(commit_res["status"], "ACID_COMMITTED")
        self.assertEqual(commit_res["version"], 1)

        # Execute action update
        action_res = lb.execute_operational_action("APPROVE_ORDER", "ORDER-100", {"status": "APPROVED"}, "manager_dan")
        self.assertEqual(action_res["action_executed"], "APPROVE_ORDER")
        updated = lb.get_state("ORDER-100")
        self.assertEqual(updated["status"], "APPROVED")
        self.assertEqual(updated["_version"], 2)

    def test_agent_bricks_autonomous_and_guardrail_enforcement(self):
        """Verifies /AB autonomously approves under threshold and enforces HITL above."""
        ab = AgentBricksRuntime("ProcurementAgent", 50000.0)
        res_auto = ab.execute_agent_loop("Procure parts", {"item_id": "P-1", "amount_usd": 12000.0})
        self.assertEqual(res_auto["decision"], "AUTONOMOUS_APPROVED")

        res_guardrail = ab.execute_agent_loop("Procure server rack", {"item_id": "SRV-9", "amount_usd": 150000.0})
        self.assertEqual(res_guardrail["decision"], "ESCALATED_HUMAN_IN_THE_LOOP")

    def test_lakeflow_pipeline_expectations(self):
        """Verifies /LF filters records violating data quality expectations."""
        lf = LakeflowPipelineManager("cdc_stream")
        records = [
            {"customer_id": "C-1", "net_amount": 100.0},
            {"customer_id": None, "net_amount": 50.0},
            {"customer_id": "C-2", "net_amount": -10.0}
        ]
        res = lf.run_pipeline_simulation(records)
        self.assertEqual(res["total_input_records"], 3)
        self.assertEqual(res["valid_records_promoted"], 1)
        self.assertEqual(res["records_dropped_by_expectations"], 2)

    def test_lakehouse_uniform_iceberg_generation(self):
        """Verifies /LK commits Delta records and generates Apache Iceberg manifests."""
        lk = LakehouseStorageEngine()
        write_res = lk.write_uniform_iceberg_batch([
            {"id": "A1", "region": "US", "val": 50},
            {"id": "A2", "region": "EU", "val": 75}
        ])
        self.assertEqual(write_res["status"], "COMMITTED_DELTA_AND_ICEBERG")
        self.assertTrue(write_res["uniform_iceberg_enabled"])
        
        scan_records = lk.execute_iceberg_federated_read()
        self.assertEqual(len(scan_records), 2)

    def test_unity_catalog_abac_and_data_masking(self):
        """Verifies /UC dynamically redacts columns and filters rows based on roles."""
        uc = UnityCatalogGovernanceManager("gold")
        
        # Test classified row rejection
        denied_res = uc.evaluate_user_access("customers", ["STANDARD_ANALYST"], {"customer_id": "C-1", "region": "CLASSIFIED"})
        self.assertEqual(denied_res["access"], "DENIED_BY_ROW_FILTER")

        # Test sensitive SSN column masking
        granted_res = uc.evaluate_user_access("customers", ["STANDARD_ANALYST"], {"customer_id": "C-2", "ssn_tax_id": "123-45-6789", "region": "PUBLIC"})
        self.assertEqual(granted_res["access"], "GRANTED")
        self.assertEqual(granted_res["data"]["ssn_tax_id"], "XXX-XX-XXXX")

if __name__ == '__main__':
    unittest.main()
