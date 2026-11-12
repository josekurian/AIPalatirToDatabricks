"""
Unit and Integration Test Suite 9: AI Multi-Platform Transpilers & Tri-Platform Reconciliation
Tests:
1. AI Transpiler Agent converting Oracle PL/SQL to vectorized PySpark
2. AI Transpiler Agent converting Snowflake ZEROIFNULL, IFF, DATEADD to DBSQL
3. Tri-Platform Reconciliation Agent verifying Oracle, Snowflake, and Databricks data streams
4. Detection of cross-platform drift in numeric values
"""

import unittest
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from multi_platform_ai_migration.ai_agents_code_transpilers.ai_transpiler_agent import AIMultiPlatformTranspilerAgent
from multi_platform_ai_migration.ai_automated_reconciliation.ai_multi_source_reconciliation import AIMultiSourceReconciliationAgent

class TestMultiPlatformAIMigration(unittest.TestCase):

    def setUp(self):
        self.transpiler = AIMultiPlatformTranspilerAgent()
        self.reconciler = AIMultiSourceReconciliationAgent()

    def test_oracle_plsql_transpilation(self):
        sample_plsql = "PROCEDURE update_credit IS BEGIN NULL; END;"
        pyspark_code = self.transpiler.transpile_oracle_plsql_to_pyspark(sample_plsql)
        
        self.assertIn("from pyspark.sql import functions as F", pyspark_code)
        self.assertIn("spark.table('enterprise_operations.silver.oracle_customers')", pyspark_code)
        self.assertIn("saveAsTable('enterprise_operations.gold.customer_master')", pyspark_code)

    def test_snowflake_sql_transpilation(self):
        snow_query = "SELECT order_id, ZEROIFNULL(discount_val), IFF(amount > 100, 'HIGH', 'LOW'), DATEADD(month, 3, created_date) FROM sales"
        dbsql_query = self.transpiler.transpile_snowflake_to_dbsql(snow_query)
        
        self.assertIn("COALESCE(discount_val, 0)", dbsql_query)
        self.assertIn("CASE WHEN amount > 100 THEN 'HIGH' ELSE 'LOW' END", dbsql_query)
        self.assertIn("ADD_MONTHS(created_date, 3)", dbsql_query)
        self.assertNotIn("ZEROIFNULL", dbsql_query)
        self.assertNotIn("IFF", dbsql_query)

    def test_tri_platform_reconciliation_exact_parity(self):
        ora = [{"id": "C-1", "val": 1000.0}, {"id": "C-2", "val": 2500.0}]
        snow = [{"id": "C-1", "val": 1000.0}, {"id": "C-2", "val": 2500.0}]
        dbx = [{"id": "C-1", "val": 1000.0}, {"id": "C-2", "val": 2500.0}]

        res = self.reconciler.reconcile_tri_platform(ora, snow, dbx, "id")
        self.assertEqual(res["status"], "PASS")
        self.assertEqual(res["overall_parity_percentage"], 100.0)
        self.assertEqual(res["cross_platform_mismatches"], 0)

    def test_tri_platform_reconciliation_detects_drift(self):
        ora = [{"id": "C-1", "val": 1000.0}, {"id": "C-2", "val": 2500.0}]
        snow = [{"id": "C-1", "val": 1000.0}, {"id": "C-2", "val": 9999.0}] # Drifting row
        dbx = [{"id": "C-1", "val": 1000.0}, {"id": "C-2", "val": 2500.0}]

        res = self.reconciler.reconcile_tri_platform(ora, snow, dbx, "id")
        self.assertEqual(res["status"], "FAIL")
        self.assertEqual(res["cross_platform_mismatches"], 1)
        self.assertEqual(res["overall_parity_percentage"], 50.0)

if __name__ == '__main__':
    unittest.main()
