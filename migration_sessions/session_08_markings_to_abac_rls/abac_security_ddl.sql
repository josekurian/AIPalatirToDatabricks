-- ==============================================================================
-- Session 8: Palantir Markings (MAC) to Unity Catalog ABAC & Dynamic Masking
-- ==============================================================================

USE CATALOG enterprise_operations;
USE SCHEMA gold;

-- 1. Dynamic Column Masking Function
CREATE OR REPLACE FUNCTION enterprise_operations.gold.mask_tax_id(tax_id STRING)
RETURN CASE 
    WHEN is_account_group_member('compliance_officers') THEN tax_id
    ELSE CONCAT('***-**-', RIGHT(tax_id, 4))
END;

ALTER TABLE enterprise_operations.gold.customer_master 
ALTER COLUMN tax_identifier SET MASK enterprise_operations.gold.mask_tax_id;

-- 2. Dynamic Row Filtering Function
CREATE OR REPLACE FUNCTION enterprise_operations.gold.regional_row_filter(country_code STRING)
RETURN 
    is_account_group_member('global_executives') OR 
    (is_account_group_member('emea_sales') AND country_code IN ('UK', 'DE', 'FR', 'ES', 'IT')) OR
    (is_account_group_member('amer_sales') AND country_code IN ('US', 'CA', 'MX'));

ALTER TABLE enterprise_operations.gold.customer_master 
SET ROW FILTER enterprise_operations.gold.regional_row_filter ON (country_code);

-- 3. Classification Tags
ALTER TABLE enterprise_operations.gold.customer_master 
SET TAGS ('classification' = 'RESTRICTED_DATA', 'domain' = 'FINANCE');
