-- ==============================================================================
-- Unity Catalog Lakehouse Federation: Oracle Database & Snowflake External Connections
-- Enables zero-copy querying of Oracle and Snowflake in-place before cutover.
-- ==============================================================================

-- 1. Create Connection to Oracle Database (Exadata / On-Prem / OCI)
CREATE CONNECTION IF NOT EXISTS oracle_erp_gateway
TYPE ORACLE
OPTIONS (
    host 'oracle-exadata.corp.internal',
    port '1521',
    user secret('enterprise_secrets', 'oracle_service_user'),
    password secret('enterprise_secrets', 'oracle_service_password'),
    databaseName 'ORCLPDB1.corp.internal'
);

-- Register Federated Foreign Catalog for Oracle
CREATE FOREIGN CATALOG IF NOT EXISTS oracle_legacy_erp
USING CONNECTION oracle_erp_gateway
OPTIONS (database 'ORCLPDB1');

-- 2. Create Connection to Snowflake Data Cloud
CREATE CONNECTION IF NOT EXISTS snowflake_warehouse_gateway
TYPE SNOWFLAKE
OPTIONS (
    host 'company-prod.snowflakecomputing.com',
    user secret('enterprise_secrets', 'snowflake_service_user'),
    password secret('enterprise_secrets', 'snowflake_service_password'),
    sfWarehouse 'COMPUTE_WH',
    sfRole 'ACCOUNTADMIN'
);

-- Register Federated Foreign Catalog for Snowflake
CREATE FOREIGN CATALOG IF NOT EXISTS snowflake_legacy_dw
USING CONNECTION snowflake_warehouse_gateway
OPTIONS (database 'ENTERPRISE_ANALYTICS');

-- 3. Zero-Copy Cross-Platform Hybrid Validation View
CREATE OR REPLACE VIEW enterprise_operations.gold.v_tri_platform_order_reconciliation AS
SELECT 
    p.order_id,
    p.order_total_usd AS palantir_order_total,
    o.total_amount    AS oracle_order_total,
    s.gross_sales_usd AS snowflake_order_total,
    (p.order_total_usd - o.total_amount) AS palantir_oracle_diff,
    (p.order_total_usd - s.gross_sales_usd) AS palantir_snowflake_diff
FROM enterprise_operations.gold.fact_supply_order p
LEFT JOIN oracle_legacy_erp.sales.orders o ON p.order_id = o.order_id
LEFT JOIN snowflake_legacy_dw.curated.fact_sales s ON p.order_id = s.order_id;
