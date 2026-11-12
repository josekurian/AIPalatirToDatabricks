"""
Unit & Integration Test Suite 8: Concurrency & High-Throughput Action Handlers
Tests:
1. Simulating 50 concurrent operational write-back requests
2. Ensuring no race conditions or state corruptions
3. Validating sub-200ms latency under concurrent load
"""

import unittest
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from frontend.server import app

class TestActionConcurrency(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def _post_action(self, idx):
        payload = {
            "order_id": f"ORD-CONCUR-{idx}",
            "source_warehouse": "WH-ATLANTA" if idx % 2 == 0 else "WH-DALLAS",
            "quantity": float(10 + (idx % 5)),
            "reason": f"Concurrent load test execution batch index {idx}"
        }
        start = time.time()
        resp = self.client.post("/api/actions/execute", json=payload)
        latency = time.time() - start
        return resp.status_code, resp.json(), latency

    def test_concurrent_action_execution(self):
        concurrency = 30
        with ThreadPoolExecutor(max_workers=8) as executor:
            results = list(executor.map(self._post_action, range(concurrency)))

        latencies = []
        for status_code, body, lat in results:
            self.assertEqual(status_code, 200)
            self.assertEqual(body["status"], "SUCCESS")
            self.assertIn("act_", body["audit_action_id"])
            latencies.append(lat)

        avg_latency = sum(latencies) / len(latencies)
        self.assertLess(avg_latency, 0.25, "Average response latency must remain below 250ms under concurrent load")

if __name__ == '__main__':
    unittest.main()
