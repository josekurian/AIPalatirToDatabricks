-- ========================================================================
-- Automated Translation of Foundry Ontology: enterprise_supply_chain_ontology
-- Target: Databricks Unity Catalog (Gold Layer)
-- ========================================================================

CREATE TABLE IF NOT EXISTS enterprise_operations.gold.gold_customer (
    customer_id STRING NOT NULL,
    customer_name STRING,
    primary_email STRING,
    country_code STRING,
    city STRING,
    credit_tier STRING,
    annual_revenue DOUBLE,
    ontology_sync_status STRING,
    CONSTRAINT pk_gold_customer PRIMARY KEY (customer_id)
)
USING DELTA
COMMENT 'Enterprise Customer - Migrated from Palantir Ontology';

CREATE TABLE IF NOT EXISTS enterprise_operations.gold.gold_supplyorder (
    order_id STRING NOT NULL,
    customer_id STRING,
    sku_id STRING,
    warehouse_id STRING,
    ordered_quantity DOUBLE,
    order_total_usd DOUBLE,
    requested_delivery_date TIMESTAMP,
    fulfillment_status STRING,
    stock_shortage_flag BOOLEAN,
    high_value_order BOOLEAN,
    CONSTRAINT pk_gold_supplyorder PRIMARY KEY (order_id)
)
USING DELTA
COMMENT 'Supply Chain Order - Migrated from Palantir Ontology';

CREATE TABLE IF NOT EXISTS enterprise_operations.gold.gold_warehouseinventory (
    inventory_asset_id STRING NOT NULL,
    warehouse_id STRING,
    sku_id STRING,
    available_stock DOUBLE,
    safety_stock_threshold DOUBLE,
    reorder_in_progress BOOLEAN,
    CONSTRAINT pk_gold_warehouseinventory PRIMARY KEY (inventory_asset_id)
)
USING DELTA
COMMENT 'Warehouse Inventory Asset - Migrated from Palantir Ontology';

ALTER TABLE enterprise_operations.gold.gold_customer ADD CONSTRAINT fk_customer_to_supply_orders FOREIGN KEY (customer_id) REFERENCES enterprise_operations.gold.gold_supplyorder(customer_id);
ALTER TABLE enterprise_operations.gold.gold_supplyorder ADD CONSTRAINT fk_order_to_inventory_asset FOREIGN KEY (sku_id) REFERENCES enterprise_operations.gold.gold_warehouseinventory(sku_id);