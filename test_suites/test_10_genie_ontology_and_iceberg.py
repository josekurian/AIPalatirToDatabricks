import unittest
import os
from genie_ontology_iceberg.iceberg_uniform.pyspark_iceberg_uniform_pipeline import (
    IcebergUniFormManager, generate_sample_transactions
)
from genie_ontology_iceberg.ontorank_engine.ontorank_resolver import OntoRankEngine

class TestGenieOntologyAndIceberg(unittest.TestCase):
    def setUp(self):
        self.iceberg_mgr = IcebergUniFormManager("gold.finance.fact_transactions", "transaction_id")
        self.ontorank = OntoRankEngine()

    def test_iceberg_uniform_write_and_metadata_generation(self):
        """Verifies Delta writes generate compliant Apache Iceberg v2 snapshots zero-copy."""
        tx_data = generate_sample_transactions()
        write_res = self.iceberg_mgr.write_delta_batch(tx_data)
        
        self.assertEqual(write_res["status"], "COMMITTED")
        self.assertEqual(write_res["records_upserted"], 3)
        self.assertEqual(write_res["total_records_in_table"], 3)
        
        # Verify Iceberg metadata spec
        meta = self.iceberg_mgr.get_iceberg_metadata()
        self.assertEqual(meta["format_version"], 2)
        self.assertEqual(meta["table_identifier"], "gold.finance.fact_transactions")
        self.assertGreaterEqual(meta["snapshots_count"], 1)
        self.assertTrue(meta["latest_manifest"].endswith(".avro"))

    def test_iceberg_external_zero_copy_scan(self):
        """Verifies external engines can read records via Iceberg metadata."""
        tx_data = generate_sample_transactions()
        self.iceberg_mgr.write_delta_batch(tx_data)
        
        records = self.iceberg_mgr.execute_iceberg_external_scan()
        self.assertEqual(len(records), 3)
        tx_ids = [r["transaction_id"] for r in records]
        self.assertIn("TX-1001", tx_ids)
        self.assertIn("TX-1002", tx_ids)

    def test_ontorank_authority_scoring_and_resolution(self):
        """Verifies OntoRank resolves certified definitions with highest authority score."""
        # Candidate 1: Certified Lead Steward
        self.ontorank.register_definition(
            def_id="DEF-FIN-01",
            metric_name="ARR",
            domain="Finance",
            author="Dana Whitlock",
            author_seniority=1.0,
            sql_template="SELECT SUM(net_amount) FROM gold.finance.fact_transactions WHERE transaction_type = 'RECURRING'",
            is_certified=True,
            monthly_executions=15000,
            days_since_update=2
        )
        
        # Candidate 2: Inferred Uncertified snippet
        self.ontorank.register_definition(
            def_id="DEF-SALES-02",
            metric_name="ARR",
            domain="Sales",
            author="Junior Analyst",
            author_seniority=0.4,
            sql_template="SELECT SUM(gross_amount) * 1.1 FROM raw.crm_pipeline",
            is_certified=False,
            monthly_executions=300,
            days_since_update=45
        )

        res = self.ontorank.resolve_metric_query("Show me total ARR", "ARR")
        self.assertEqual(res["status"], "RESOLVED_AUTHORITATIVE")
        self.assertEqual(res["selected_definition"]["def_id"], "DEF-FIN-01")
        self.assertGreater(res["authority_score"], 0.85)

    def test_ontorank_unmapped_metric_routes_to_steward_queue(self):
        """Verifies unknown metrics are queued for stewards rather than hallucinating."""
        res = self.ontorank.resolve_metric_query("Show me unmodeled metric", "UNKNOWN_KPI")
        self.assertEqual(res["status"], "QUEUED_FOR_STEWARD")
        self.assertEqual(len(self.ontorank.review_queue), 1)
        self.assertEqual(self.ontorank.review_queue[0]["metric_name"], "UNKNOWN_KPI")

    def test_steward_approval_promotes_to_certified(self):
        """Verifies steward promotion elevates an inferred metric to certified authority."""
        self.ontorank.register_definition(
            def_id="DEF-INFER-99",
            metric_name="CHURN_RATE",
            domain="Customer Success",
            author="Auto-Inferred Agent",
            author_seniority=0.3,
            sql_template="SELECT AVG(churn_risk_score) FROM gold.enterprise.customer_master",
            is_certified=False,
            monthly_executions=1200,
            days_since_update=1
        )

        initial_score = self.ontorank.definitions["DEF-INFER-99"]["authority_score"]
        
        # Steward promotes definition
        promote_res = self.ontorank.steward_approve_and_certify("DEF-INFER-99", "Dana Whitlock")
        self.assertEqual(promote_res["status"], "PROMOTED_AND_CERTIFIED")
        new_score = promote_res["new_authority_score"]
        
        # Authority score must jump due to certification weight (+0.40)
        self.assertGreater(new_score, initial_score)
        self.assertTrue(self.ontorank.definitions["DEF-INFER-99"]["is_certified"])

if __name__ == '__main__':
    unittest.main()
