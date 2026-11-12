-- ==============================================================================
-- Databricks Unity Catalog Enterprise Metastore DDL & Governance Blueprint
-- Catalog: enterprise_operations | Schemas: bronze, silver, gold
-- ==============================================================================

-- 1. Create Catalogs & Schemata
CREATE CATALOG IF NOT EXISTS enterprise_operations
COMMENT 'Primary enterprise catalog for supply chain, finance, and CRM';

USE CATALOG enterprise_operations;

CREATE SCHEMA IF NOT EXISTS bronze
COMMENT 'Raw landing zone ingested via Auto Loader and Lakeflow Connect';

CREATE SCHEMA IF NOT EXISTS silver
COMMENT 'Enriched, cleansed, and validated conforming tables';

CREATE SCHEMA IF NOT EXISTS gold
COMMENT 'Business domain entities, metrics, and semantic object models';

-- 2. Create Unity Catalog Volumes for Unstructured Ingestion
CREATE VOLUME IF NOT EXISTS enterprise_operations.bronze.unstructured_invoices
COMMENT 'Raw PDF/TIFF invoices and logistics bills of lading';

-- 3. Row-Level Security Functions & Column Masking Filters
CREATE OR REPLACE FUNCTION enterprise_operations.gold.mask_tax_id(tax_id STRING)
RETURN CASE 
    WHEN is_account_group_member('compliance_officers') THEN tax_id
    ELSE CONCAT('***-**-', RIGHT(tax_id, 4))
END;

CREATE OR REPLACE FUNCTION enterprise_operations.gold.customer_region_filter(country_code STRING)
RETURN 
    is_account_group_member('global_executives') OR 
    (is_account_group_member('emea_sales') AND country_code IN ('DE', 'FR', 'UK', 'IT', 'ES')) OR
    (is_account_group_member('amer_sales') AND country_code IN ('US', 'CA', 'MX'));

-- 4. Gold Delta Table Definitions with Unity Catalog Governance
CREATE TABLE IF NOT EXISTS enterprise_operations.gold.dim_customer (
    customer_id STRING NOT NULL,
    customer_name STRING,
    primary_email STRING,
    country_code STRING,
    city STRING,
    tax_identifier STRING MASK enterprise_operations.gold.mask_tax_id,
    credit_tier STRING,
    annual_revenue DOUBLE,
    ontology_sync_status STRING,
    created_timestamp TIMESTAMP,
    last_updated_at TIMESTAMP,
    CONSTRAINT pk_dim_customer PRIMARY KEY (customer_id)
)
CLUSTER BY (country_code, credit_tier)
WITH ROW FILTER enterprise_operations.gold.customer_region_filter ON (country_code)
COMMENT 'Curated Enterprise Customer Master (Migrated from Foundry Ontology Object: Customer)';

CREATE TABLE IF NOT EXISTS enterprise_operations.gold.dim_inventory (
    inventory_asset_id STRING NOT NULL,
    warehouse_id STRING NOT NULL,
    sku_id STRING NOT NULL,
    available_stock DOUBLE,
    safety_stock_threshold DOUBLE,
    reorder_in_progress BOOLEAN,
    last_snapshot_at TIMESTAMP,
    CONSTRAINT pk_dim_inventory PRIMARY KEY (inventory_asset_id)
)
CLUSTER BY (warehouse_id, sku_id)
COMMENT 'Curated Warehouse Inventory (Migrated from Foundry Ontology Object: WarehouseInventory)';

CREATE TABLE IF NOT EXISTS enterprise_operations.gold.fact_supply_order (
    order_id STRING NOT NULL,
    customer_id STRING NOT NULL,
    sku_id STRING NOT NULL,
    warehouse_id STRING,
    ordered_quantity DOUBLE,
    order_total_usd DOUBLE,
    requested_delivery_date TIMESTAMP,
    fulfillment_status STRING,
    stock_shortage_flag BOOLEAN,
    high_value_order BOOLEAN,
    delivery_risk_score DOUBLE,
    last_updated_at TIMESTAMP,
    CONSTRAINT pk_fact_supply_order PRIMARY KEY (order_id),
    CONSTRAINT fk_order_customer FOREIGN KEY (customer_id) REFERENCES enterprise_operations.gold.dim_customer(customer_id)
)
CLUSTER BY (fulfillment_status, warehouse_id)
COMMENT 'Curated Supply Chain Orders (Migrated from Foundry Ontology Object: SupplyOrder)';

-- 5. Audit Log Table for Operational Write-Backs (Action Logging)
CREATE TABLE IF NOT EXISTS enterprise_operations.gold.audit_operational_actions (
    action_id STRING NOT NULL,
    action_type STRING NOT NULL,
    target_entity_id STRING NOT NULL,
    executed_by_user_or_agent STRING NOT NULL,
    payload_json STRING,
    execution_status STRING,
    latency_ms BIGINT,
    executed_at TIMESTAMP
)
CLUSTER BY (action_type, execution_status)
COMMENT 'Immutable audit log recording kinetic operational write-backs executed by Databricks Apps or Agents';
