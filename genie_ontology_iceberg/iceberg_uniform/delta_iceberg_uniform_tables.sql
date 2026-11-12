-- ============================================================================
-- Databricks Delta Lake UniForm with Apache Iceberg Metadata Generation
-- Replaces Palantir Proprietary Datasets & Oracle Exadata Warehouse Storage
-- ============================================================================

-- 1. Create Enterprise Gold Customer Master with Iceberg UniForm enabled
CREATE TABLE IF NOT EXISTS gold.enterprise.customer_master (
    customer_id STRING NOT NULL,
    customer_name STRING,
    segment STRING,
    country_code STRING,
    lifetime_value DOUBLE,
    churn_risk_score DOUBLE,
    is_vip_account BOOLEAN,
    last_activity_date DATE,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    CONSTRAINT pk_customer_master PRIMARY KEY(customer_id)
)
USING DELTA
TBLPROPERTIES (
    'delta.universalFormat.enabledFormats' = 'iceberg',
    'delta.enableIcebergCompatV2' = 'true',
    'delta.autoOptimize.optimizeWrite' = 'true',
    'delta.autoOptimize.autoCompact' = 'true',
    'governance.domain' = 'Sales',
    'governance.tier' = 'certified_gold'
)
CLUSTER BY (country_code, segment);

-- 2. Create Enterprise Gold Fact Transactions with Iceberg UniForm
CREATE TABLE IF NOT EXISTS gold.finance.fact_transactions (
    transaction_id STRING NOT NULL,
    customer_id STRING NOT NULL,
    transaction_date DATE NOT NULL,
    product_line STRING NOT NULL,
    transaction_type STRING NOT NULL, -- 'RECURRING', 'EXPANSION', 'ONE_TIME'
    gross_amount DOUBLE NOT NULL,
    discount_amount DOUBLE DEFAULT 0.0,
    net_amount DOUBLE NOT NULL,
    cost_of_goods_sold DOUBLE NOT NULL,
    currency STRING DEFAULT 'USD',
    status STRING NOT NULL,           -- 'SETTLED', 'PENDING', 'REFUNDED'
    is_test_record BOOLEAN DEFAULT FALSE,
    ingested_at TIMESTAMP,
    CONSTRAINT pk_fact_transactions PRIMARY KEY(transaction_id),
    CONSTRAINT fk_tx_to_customer FOREIGN KEY(customer_id) REFERENCES gold.enterprise.customer_master(customer_id)
)
USING DELTA
TBLPROPERTIES (
    'delta.universalFormat.enabledFormats' = 'iceberg',
    'delta.enableIcebergCompatV2' = 'true',
    'governance.domain' = 'Finance',
    'governance.tier' = 'certified_gold'
)
CLUSTER BY (transaction_date, product_line);

-- 3. Create Enterprise Gold Product Catalog with Iceberg UniForm
CREATE TABLE IF NOT EXISTS gold.products.catalog (
    sku_id STRING NOT NULL,
    product_name STRING NOT NULL,
    product_family STRING NOT NULL,
    unit_price DOUBLE NOT NULL,
    base_cost DOUBLE NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    CONSTRAINT pk_product_catalog PRIMARY KEY(sku_id)
)
USING DELTA
TBLPROPERTIES (
    'delta.universalFormat.enabledFormats' = 'iceberg',
    'governance.domain' = 'Products',
    'governance.tier' = 'certified_gold'
)
CLUSTER BY (product_family);
