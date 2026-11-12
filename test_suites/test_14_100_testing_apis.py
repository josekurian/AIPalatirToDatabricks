import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from api_100_testing_suite.api_catalog import get_all_apis, get_api_by_id
from api_100_testing_suite.api_dispatcher import ApiTestingSuiteDispatcher

class Test100TestingAPIs(unittest.TestCase):
    def setUp(self):
        self.dispatcher = ApiTestingSuiteDispatcher()

    def test_catalog_contains_exactly_100_apis(self):
        """Verifies exactly 100 testing APIs are registered across 10 categories."""
        apis = get_all_apis()
        self.assertEqual(len(apis), 100)
        
        # Verify 10 distinct categories
        categories = set(a["category"] for a in apis)
        self.assertEqual(len(categories), 10)

    def test_all_100_api_ids_sequential_and_unique(self):
        """Verifies all API IDs are formatted '001' to '100' without gaps."""
        apis = get_all_apis()
        ids = [a["id"] for a in apis]
        self.assertEqual(len(ids), len(set(ids)))
        expected_ids = [f"{i:03d}" for i in range(1, 101)]
        self.assertEqual(ids, expected_ids)

    def test_dispatch_across_all_100_apis(self):
        """Dispatches all 100 APIs and verifies valid responses with latency and timestamps."""
        summary = self.dispatcher.run_all_100_apis()
        self.assertEqual(summary["total_apis_executed"], 100)
        self.assertEqual(summary["status"], "ALL_100_APIS_VERIFIED_PASS")

    def test_sample_api_categories(self):
        """Verifies deep response payloads for key milestone APIs."""
        # 001 Transpilation
        res1 = self.dispatcher.dispatch("001")
        self.assertEqual(res1["status"], "SUCCESS")
        self.assertIn("@dlt.table", res1["transpiled_code"])

        # 013 Reconciliation Tri-Platform
        res13 = self.dispatcher.dispatch("013")
        self.assertEqual(res13["status"], "ALL_PLATFORMS_ALIGNED")
        self.assertEqual(res13["oracle_vs_databricks_parity"], 1.0)

        # 021 Apache Iceberg UniForm
        res21 = self.dispatcher.dispatch("021")
        self.assertEqual(res21["status"], "TABLE_CREATED")
        self.assertTrue(res21["delta_uniform"])

        # 031 Genie NLP
        res31 = self.dispatcher.dispatch("031")
        self.assertEqual(res31["status"], "SQL_GENERATED")
        self.assertGreaterEqual(res31["confidence"], 0.95)

        # 041 OntoRank Scoring
        res41 = self.dispatcher.dispatch("041")
        self.assertEqual(res41["status"], "SCORED")
        self.assertGreater(res41["authority_score"], 0.95)

        # 053 AI Prompt Injection Defense
        res53 = self.dispatcher.dispatch("053")
        self.assertEqual(res53["status"], "THREAT_NEUTRALIZED")
        self.assertTrue(res53["threat_detected"])

        # 071 Agent Bricks Autonomous Approval
        res71 = self.dispatcher.dispatch("071")
        self.assertEqual(res71["status"], "APPROVED")
        self.assertEqual(res71["decision"], "AUTONOMOUS_APPROVED")

        # 100 Platform Stress Certification
        res100 = self.dispatcher.dispatch("100")
        self.assertEqual(res100["status"], "PASSED")
        self.assertTrue(res100["all_100_apis_passing"])

if __name__ == '__main__':
    unittest.main()
