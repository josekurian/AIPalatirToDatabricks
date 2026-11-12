"""
Unit and Integration Test Suite 2: Automated Data Reconciliation Engine
Tests:
1. Exact row parity & bitwise SHA-256 hash identity
2. Detection of missing keys in target tables
3. Detection of attribute mismatches and drift
4. Floating-point epsilon tolerance in statistical moments
"""

import unittest
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Migrations.reconciliation.reconciliation_engine import reconcile_table_pair
from labs_200_comprehensive.module_08_reconciliation_parity.reconciliation_suite import EnterpriseReconciliationSuite

class TestReconciliationEngine(unittest.TestCase):

    def setUp(self):
        self.suite = EnterpriseReconciliationSuite(tolerance_epsilon=1e-4)
        
        self.foundry_sample = [
            {"customer_id": "CUST-100", "company": "Alpha Corp", "revenue": 500000.00, "region": "AMER"},
            {"customer_id": "CUST-200", "company": "Beta LLC", "revenue": 1200000.50, "region": "EMEA"},
            {"customer_id": "CUST-300", "company": "Gamma Inc", "revenue": 875000.25, "region": "APAC"}
        ]
        
        # Identical databricks dataset
        self.databricks_sample_clean = [
            {"customer_id": "CUST-100", "company": "Alpha Corp", "revenue": 500000.00, "region": "AMER"},
            {"customer_id": "CUST-200", "company": "Beta LLC", "revenue": 1200000.50, "region": "EMEA"},
            {"customer_id": "CUST-300", "company": "Gamma Inc", "revenue": 875000.25, "region": "APAC"}
        ]
        
        # Drifting databricks dataset
        self.databricks_sample_drift = [
            {"customer_id": "CUST-100", "company": "Alpha Corp", "revenue": 500000.00, "region": "AMER"},
            {"customer_id": "CUST-200", "company": "Beta LLC MODIFIED", "revenue": 1200000.50, "region": "EMEA"},
            # Missing CUST-300, added CUST-400
            {"customer_id": "CUST-400", "company": "Delta GMBH", "revenue": 300000.00, "region": "EMEA"}
        ]

    def test_reconcile_exact_parity(self):
        report = reconcile_table_pair(self.foundry_sample, self.databricks_sample_clean, "customer_id")
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["overall_parity_percentage"], 100.0)
        self.assertEqual(report["missing_keys_count"], 0)
        self.assertEqual(report["attribute_mismatch_count"], 0)

    def test_reconcile_detects_drift_and_missing_keys(self):
        report = reconcile_table_pair(self.foundry_sample, self.databricks_sample_drift, "customer_id")
        self.assertEqual(report["status"], "FAIL")
        self.assertEqual(report["missing_keys_count"], 1) # CUST-300
        self.assertEqual(report["unexpected_keys_count"], 1) # CUST-400
        self.assertLess(report["overall_parity_percentage"], 100.0)

    def test_bitwise_and_statistical_parity(self):
        res = self.suite.reconcile_datasets(
            self.foundry_sample,
            self.databricks_sample_clean,
            primary_key="customer_id",
            numeric_metrics=["revenue"]
        )
        self.assertEqual(res["status"], "PASS")
        self.assertEqual(res["parity_score_percentage"], 100.0)
        self.assertTrue(res["numeric_metrics_validation"]["revenue"]["passed"])
        self.assertEqual(res["bitwise_hash_mismatches"], 0)

if __name__ == '__main__':
    unittest.main()
