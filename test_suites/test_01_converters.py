"""
Unit and Integration Test Suite 1: Automated Code & AST Converters
Tests:
1. Foundry to DLT converter logic
2. Ontology to Unity Catalog SQL DDL generator
3. Schema conformance and regex validity
"""

import unittest
import os
import sys

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Migrations.code_converters.foundry_to_dlt_converter import convert_foundry_to_dlt
from Migrations.code_converters.ontology_to_unity_catalog_converter import convert_ontology_to_databricks_sql

class TestCodeConverters(unittest.TestCase):

    def setUp(self):
        self.sample_foundry_code = """
from transforms.api import transform_df, Input, Output

@transform_df(
    Output("/Company/Gold/Orders"),
    orders_feed=Input("/Company/Silver/RawOrders"),
    customers=Input("/Company/Silver/Customers")
)
def compute_orders(orders_feed, customers):
    return orders_feed.join(customers, on='customer_id', how='inner')
"""
        self.ontology_spec_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "Palantir", "ontology_definitions", "enterprise_ontology_spec.json"
        )

    def test_foundry_to_dlt_conversion(self):
        converted = convert_foundry_to_dlt(self.sample_foundry_code)
        
        # Verify DLT decorators and imports
        self.assertIn("import dlt", converted)
        self.assertIn('@dlt.table(', converted)
        self.assertIn('name="orders"', converted)
        self.assertIn('orders_feed = dlt.read("raworders")', converted)
        self.assertIn('customers = dlt.read("customers")', converted)
        self.assertNotIn("from transforms.api import", converted)
        self.assertNotIn("@transform_df", converted)

    def test_ontology_to_unity_catalog_sql(self):
        self.assertTrue(os.path.exists(self.ontology_spec_path))
        sql = convert_ontology_to_databricks_sql(self.ontology_spec_path)
        
        # Verify SQL DDL generation
        self.assertIn("CREATE TABLE IF NOT EXISTS enterprise_operations.gold.gold_customer", sql)
        self.assertIn("CREATE TABLE IF NOT EXISTS enterprise_operations.gold.gold_supplyorder", sql)
        self.assertIn("PRIMARY KEY (customer_id)", sql)
        self.assertIn("PRIMARY KEY (order_id)", sql)
        self.assertIn("FOREIGN KEY", sql)
        self.assertIn("USING DELTA", sql)

if __name__ == '__main__':
    unittest.main()
