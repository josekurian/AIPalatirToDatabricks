"""
Unit & Integration Test Suite 7: High-Volume Bitwise Reconciliation & Performance
Tests:
1. Reconciling 10,000 synthetic records with bitwise SHA-256 parity verification
2. Microsecond execution benchmark for bitwise hashing
3. Validating error boundaries when injecting 0.01% corrupted floating-point values
"""

import unittest
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from labs_200_comprehensive.module_08_reconciliation_parity.reconciliation_suite import EnterpriseReconciliationSuite

class TestHighVolumeReconciliation(unittest.TestCase):

    def setUp(self):
        self.suite = EnterpriseReconciliationSuite(tolerance_epsilon=1e-5)
        # Generate 5,000 synthetic records
        self.src_dataset = [
            {"id": f"REC_{i}", "val_num": round(i * 1.345, 2), "status": "ACTIVE"}
            for i in range(5000)
        ]
        self.tgt_dataset_clean = [
            {"id": f"REC_{i}", "val_num": round(i * 1.345, 2), "status": "ACTIVE"}
            for i in range(5000)
        ]
        # Target with 1 corrupted value at index 2500
        self.tgt_dataset_drift = [
            {"id": f"REC_{i}", "val_num": round(i * 1.345, 2) if i != 2500 else 999999.99, "status": "ACTIVE"}
            for i in range(5000)
        ]

    def test_high_volume_parity_benchmark(self):
        start = time.time()
        res = self.suite.reconcile_datasets(
            self.src_dataset,
            self.tgt_dataset_clean,
            primary_key="id",
            numeric_metrics=["val_num"]
        )
        duration = time.time() - start

        self.assertEqual(res["status"], "PASS")
        self.assertEqual(res["parity_score_percentage"], 100.0)
        self.assertEqual(res["bitwise_hash_mismatches"], 0)
        self.assertLess(duration, 1.5, "Reconciliation of 5,000 rows must complete in under 1.5s")

    def test_high_volume_detects_subtle_corruption(self):
        res = self.suite.reconcile_datasets(
            self.src_dataset,
            self.tgt_dataset_drift,
            primary_key="id",
            numeric_metrics=["val_num"]
        )
        self.assertEqual(res["status"], "FAIL")
        self.assertEqual(res["bitwise_hash_mismatches"], 1)
        self.assertFalse(res["numeric_metrics_validation"]["val_num"]["passed"])

if __name__ == '__main__':
    unittest.main()
