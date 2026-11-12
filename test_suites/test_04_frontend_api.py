"""
Unit and Integration Test Suite 4: Frontend API Endpoints & Health Check
Tests:
1. /api/health endpoint
2. /api/matrices capability matrix
3. /api/palantir/ontology schema definition
4. /api/benchmarks TCO report
5. /api/actions/execute operational ERP write-back handler
6. /api/reconciliation/run dual-system test
7. Verification that all 7 downloadable .docx files are accessible (HTTP 200)
"""

import unittest
import os
import sys
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from frontend.server import app, DOC_MAP

class TestFrontendAPIAndEndpoints(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def test_health_check(self):
        resp = self.client.get("/api/health")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["status"], "UP")
        self.assertEqual(data["port"], 11991)

    def test_get_matrices(self):
        resp = self.client.get("/api/matrices")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("categories", data)
        self.assertGreater(len(data["categories"]), 0)

    def test_get_palantir_ontology(self):
        resp = self.client.get("/api/palantir/ontology")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("ontology", data)
        self.assertEqual(data["ontology"]["apiName"], "enterprise_supply_chain_ontology")

    def test_get_benchmarks(self):
        resp = self.client.get("/api/benchmarks")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("benchmarks", data)
        self.assertIn("tco_model", data)

    def test_execute_operational_action(self):
        payload = {
            "order_id": "ORD-TEST-99",
            "source_warehouse": "WH-ATLANTA",
            "quantity": 20.0,
            "reason": "Test unit verification"
        }
        resp = self.client.post("/api/actions/execute", json=payload)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["status"], "SUCCESS")
        self.assertEqual(data["order_id"], "ORD-TEST-99")
        self.assertIn("act_", data["audit_action_id"])
        self.assertEqual(data["erp_status"], "SAP_EXPEDITE_DISPATCHED_200_OK")

    def test_reconciliation_run(self):
        resp = self.client.get("/api/reconciliation/run")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["status"], "CERTIFIED_PASS")
        self.assertEqual(data["parity_percentage"], "100.0%")
        self.assertEqual(data["row_discrepancy"], 0)

    def test_all_docx_downloads_exist(self):
        for doc_key, doc_path in DOC_MAP.items():
            self.assertTrue(os.path.exists(doc_path), f"File missing for key '{doc_key}': {doc_path}")
            resp = self.client.get(f"/api/download/{doc_key}")
            self.assertEqual(resp.status_code, 200, f"Failed download for key '{doc_key}'")
            self.assertGreater(len(resp.content), 10000, f"File too small for key '{doc_key}'")

if __name__ == '__main__':
    unittest.main()
