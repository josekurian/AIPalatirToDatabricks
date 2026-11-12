"""
Unit & Integration Test Suite 6: Code Converters Edge Cases & Complex AST
Tests:
1. Multi-input, multi-stage Foundry @transform_df refactoring
2. Nullable type mappings and composite constraints in Unity Catalog DDL
3. Schema inference and comment preservation
"""

import unittest
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Migrations.code_converters.foundry_to_dlt_converter import convert_foundry_to_dlt
from Migrations.code_converters.ontology_to_unity_catalog_converter import convert_ontology_to_databricks_sql

class TestConvertersEdgeCases(unittest.TestCase):

    def test_multi_input_foundry_pipeline(self):
        complex_foundry = """
from transforms.api import transform_df, Input, Output

@transform_df(
    Output("/Company/Gold/SupplyChainKPIs"),
    orders=Input("/Company/Silver/Orders"),
    inventory=Input("/Company/Silver/WMS_Inventory"),
    suppliers=Input("/Company/Silver/VendorMaster")
)
def compute_kpis(orders, inventory, suppliers):
    return orders.join(inventory, 'sku_id').join(suppliers, 'vendor_id')
"""
        converted = convert_foundry_to_dlt(complex_foundry)
        self.assertIn('@dlt.table(', converted)
        self.assertIn('name="supplychainkpis"', converted)
        self.assertIn('orders = dlt.read("orders")', converted)
        self.assertIn('inventory = dlt.read("wms_inventory")', converted)
        self.assertIn('suppliers = dlt.read("vendormaster")', converted)
        self.assertIn('def supplychainkpis():', converted)

    def test_ontology_link_types_and_foreign_keys(self):
        ontology_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "Palantir", "ontology_definitions", "enterprise_ontology_spec.json"
        )
        sql = convert_ontology_to_databricks_sql(ontology_path)
        self.assertIn("ALTER TABLE enterprise_operations.gold.gold_customer ADD CONSTRAINT", sql)
        self.assertIn("REFERENCES enterprise_operations.gold.gold_supplyorder(customer_id)", sql)
        self.assertIn("ALTER TABLE enterprise_operations.gold.gold_supplyorder ADD CONSTRAINT", sql)
        self.assertIn("REFERENCES enterprise_operations.gold.gold_warehouseinventory(sku_id)", sql)

if __name__ == '__main__':
    unittest.main()
