#!/usr/bin/env python3
"""
Enterprise Test Suite Runner & Verification Certifier
Runs all unit and integration test suites, measures execution times,
and generates a formal verification report and JSON test certificate.
"""

import unittest
import time
import json
import os
import sys

def run_all_enterprise_tests():
    print("=" * 80)
    print("🧪 EXECUTING FULL PALANTIR TO DATABRICKS ENTERPRISE TEST SUITE")
    print("=" * 80)

    test_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_suites")
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=test_dir, pattern="test_*.py")

    start_time = time.time()
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    duration = time.time() - start_time

    print("=" * 80)
    print(f"📊 TEST EXECUTION SUMMARY:")
    print(f"   • Tests Executed: {result.testsRun}")
    print(f"   • Successes:      {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"   • Failures:       {len(result.failures)}")
    print(f"   • Errors:         {len(result.errors)}")
    print(f"   • Duration:       {duration:.3f} seconds")
    print(f"   • Result Status:  {'✅ ALL TESTS PASSED (100%)' if result.wasSuccessful() else '❌ TESTS FAILED'}")
    print("=" * 80)

    # Output Certificate
    cert = {
        "suite_run_id": f"test_run_{time.strftime('%Y%m%d_%H%M%S')}",
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "tests_run": result.testsRun,
        "failures": len(result.failures),
        "errors": len(result.errors),
        "duration_seconds": round(duration, 3),
        "status": "PASS" if result.wasSuccessful() else "FAIL",
        "tested_components": [
            "Foundry to DLT Code Converters",
            "Ontology to Unity Catalog DDL Translator",
            "Bitwise SHA-256 and Statistical Parity Reconciliation Engine",
            "Mosaic AI Compound Agent with Human-In-The-Loop ($50k) Guardrails",
            "Operational Kinetic ERP Write-Back Microservice",
            "FastAPI Frontend Server & Health Check (Port 11991)",
            "Download Endpoints for All 7 Generated .docx Guides",
            "200 Hands-On Labs Curriculum & Sequential Order Verification"
        ]
    }

    report_path = os.path.join(test_dir, "test_execution_certificate.json")
    with open(report_path, "w") as f:
        json.dump(cert, f, indent=2)

    print(f"Certificate successfully written to: {report_path}")
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_all_enterprise_tests()
    sys.exit(0 if success else 1)
