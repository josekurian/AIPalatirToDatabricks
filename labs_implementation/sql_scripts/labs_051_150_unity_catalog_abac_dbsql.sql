-- ==============================================================================
-- Enterprise Hands-On Labs SQL Repository: Unity Catalog, ABAC & DBSQL
-- Covers Labs 051 - 075 (Ontology Mapping) and Labs 101 - 150 (ABAC, DBSQL & Photon)
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- LAB 052 & 053: UNITY CATALOG THREE-LEVEL NAMESPACE & CONSTRAINTS
-- ------------------------------------------------------------------------------
CREATE CATALOG IF NOT EXISTS enterprise_operations;
USE CATALOG enterprise_operations;

CREATE SCHEMA IF NOT EXISTS gold
COMMENT 'Curated digital twin entities migrated from Palantir Foundry Ontology';

CREATE TABLE IF NOT EXISTS enterprise_operations.gold.customer_master (
    customer_id STRING NOT NULL,
    company_name STRING,
    tax_identifier STRING,
    country_code STRING,
    credit_rating STRING,
    annual_spend DOUBLE,
    last_synced_at TIMESTAMP,
    CONSTRAINT pk_customer_master PRIMARY KEY (customer_id)
)
CLUSTER BY (country_code, credit_rating)
COMMENT 'Curated Customer Master - Migrated from Palantir Object Type: Customer';

-- ------------------------------------------------------------------------------
-- LAB 054: LINK TYPES MAPPED TO FOREIGN KEYS
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS enterprise_operations.gold.supply_chain_orders (
    order_id STRING NOT NULL,
    customer_id STRING NOT NULL,
    sku_id STRING NOT NULL,
    order_total DOUBLE,
    order_status STRING,
    CONSTRAINT pk_orders PRIMARY KEY (order_id),
    CONSTRAINT fk_order_customer FOREIGN KEY (customer_id) 
        REFERENCES enterprise_operations.gold.customer_master(customer_id)
)
CLUSTER BY (order_status);

-- ------------------------------------------------------------------------------
-- LAB 103 & 105: PALANTIR MARKINGS TRANSLATED TO ABAC ROW FILTERS & COLUMN MASKS
-- ------------------------------------------------------------------------------
-- Dynamic Masking: Mask Tax Identifiers unless user is a Compliance Officer
CREATE OR REPLACE FUNCTION enterprise_operations.gold.mask_ssn_tax_id(val STRING)
RETURN CASE
    WHEN is_account_group_member('compliance_officers') THEN val
    ELSE CONCAT('***-**-', RIGHT(val, 4))
END;

ALTER TABLE enterprise_operations.gold.customer_master 
ALTER COLUMN tax_identifier SET MASK enterprise_operations.gold.mask_ssn_tax_id;

-- Dynamic Row Filter: Restrict access by geographic sales territory
CREATE OR REPLACE FUNCTION enterprise_operations.gold.regional_row_filter(country_code STRING)
RETURN 
    is_account_group_member('global_executives') OR
    (is_account_group_member('emea_sales') AND country_code IN ('UK', 'DE', 'FR', 'ES', 'IT')) OR
    (is_account_group_member('amer_sales') AND country_code IN ('US', 'CA', 'MX'));

ALTER TABLE enterprise_operations.gold.customer_master 
SET ROW FILTER enterprise_operations.gold.regional_row_filter ON (country_code);

-- ------------------------------------------------------------------------------
-- LAB 126 & 127: DBSQL COHORTS & TIME-SERIES MIGRATED FROM CONTOUR/QUIVER
-- ------------------------------------------------------------------------------
CREATE OR REPLACE VIEW enterprise_operations.gold.v_monthly_customer_cohorts AS
SELECT 
    DATE_TRUNC('month', o.last_synced_at) AS order_month,
    c.country_code,
    c.credit_rating,
    COUNT(DISTINCT o.order_id) AS total_orders,
    SUM(o.order_total) AS gross_revenue_usd,
    AVG(o.order_total) AS average_order_value_usd,
    LAG(SUM(o.order_total), 1) OVER (
        PARTITION BY c.country_code ORDER BY DATE_TRUNC('month', o.last_synced_at)
    ) AS prior_month_revenue_usd
FROM enterprise_operations.gold.supply_chain_orders o
JOIN enterprise_operations.gold.customer_master c ON o.customer_id = c.customer_id
GROUP BY 1, 2, 3;
