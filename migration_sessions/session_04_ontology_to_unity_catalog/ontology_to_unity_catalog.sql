-- ==============================================================================
-- Session 4: Foundry Ontology to Unity Catalog (Gold Delta + Primary/Foreign Keys)
-- ==============================================================================

USE CATALOG enterprise_operations;
USE SCHEMA gold;

-- Customer Object Type -> Gold Delta Table
CREATE TABLE IF NOT EXISTS enterprise_operations.gold.customer_master (
    customer_id STRING NOT NULL,
    customer_name STRING NOT NULL,
    primary_email STRING,
    country_code STRING,
    credit_tier STRING,
    annual_revenue DOUBLE,
    last_updated_at TIMESTAMP,
    CONSTRAINT pk_customer_master PRIMARY KEY (customer_id)
)
CLUSTER BY (customer_id, country_code)
COMMENT 'Curated digital twin Customer entity (Migrated from Palantir Object: Customer)';

-- SupplyOrder Object Type -> Gold Delta Table with Foreign Key
CREATE TABLE IF NOT EXISTS enterprise_operations.gold.fact_supply_order (
    order_id STRING NOT NULL,
    customer_id STRING NOT NULL,
    sku_id STRING NOT NULL,
    ordered_quantity DOUBLE,
    order_total_usd DOUBLE,
    requested_delivery_date TIMESTAMP,
    fulfillment_status STRING,
    CONSTRAINT pk_fact_supply_order PRIMARY KEY (order_id),
    CONSTRAINT fk_order_customer FOREIGN KEY (customer_id) 
        REFERENCES enterprise_operations.gold.customer_master(customer_id)
)
CLUSTER BY (order_id, customer_id)
COMMENT 'Curated digital twin Supply Order entity (Migrated from Palantir Object: SupplyOrder)';
