-- ==============================================================================
-- Comprehensive Production Scripts for Module 3 & 5: Unity Catalog & ABAC
-- Covers Labs 051 - 075 (Ontology Mapping) & Labs 101 - 125 (Enterprise ABAC)
-- ==============================================================================

CREATE CATALOG IF NOT EXISTS enterprise_operations;
USE CATALOG enterprise_operations;

CREATE SCHEMA IF NOT EXISTS gold;

-- Lab 052 & 053: Object Types to Delta Tables with Constraints
CREATE TABLE IF NOT EXISTS enterprise_operations.gold.customer_master (
    customer_id STRING NOT NULL,
    company_name STRING NOT NULL,
    tax_identifier STRING,
    country_code STRING,
    credit_rating STRING,
    annual_spend DOUBLE,
    created_at TIMESTAMP,
    CONSTRAINT pk_customer_master PRIMARY KEY (customer_id)
)
CLUSTER BY (country_code, credit_rating)
COMMENT 'Curated Enterprise Customer Master (Migrated from Foundry Ontology Object: Customer)';

-- Lab 105: Dynamic Column Masking for Tax ID / SSN
CREATE OR REPLACE FUNCTION enterprise_operations.gold.mask_tax_id(tax_id STRING)
RETURN CASE 
    WHEN is_account_group_member('compliance_officers') THEN tax_id
    ELSE CONCAT('***-**-', RIGHT(tax_id, 4))
END;

ALTER TABLE enterprise_operations.gold.customer_master 
ALTER COLUMN tax_identifier SET MASK enterprise_operations.gold.mask_tax_id;

-- Lab 104: Dynamic Geographic Row Filtering
CREATE OR REPLACE FUNCTION enterprise_operations.gold.regional_row_filter(country_code STRING)
RETURN 
    is_account_group_member('global_executives') OR 
    (is_account_group_member('emea_sales') AND country_code IN ('UK', 'DE', 'FR', 'ES', 'IT')) OR
    (is_account_group_member('amer_sales') AND country_code IN ('US', 'CA', 'MX'));

ALTER TABLE enterprise_operations.gold.customer_master 
SET ROW FILTER enterprise_operations.gold.regional_row_filter ON (country_code);

-- Lab 083: Operational Action Audit Log Table
CREATE TABLE IF NOT EXISTS enterprise_operations.gold.audit_operational_actions (
    action_id STRING NOT NULL,
    action_type STRING NOT NULL,
    target_entity_id STRING NOT NULL,
    executed_by STRING NOT NULL,
    payload_json STRING,
    execution_status STRING,
    latency_ms BIGINT,
    executed_at TIMESTAMP
)
CLUSTER BY (action_type, execution_status)
COMMENT 'Immutable audit log recording kinetic operational write-backs executed by Databricks Apps or Agents';
