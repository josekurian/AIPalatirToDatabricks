-- ============================================================================
-- Databricks Delta Sharing & Open Sharing Setup
-- WorkspaceID: 7474649578236440
-- OpenSharingID: aws:us-east-2:0a6cc551-4c15-44a3-8a44-5090cee441c9
-- User: hybridgenai@gmail.com
-- ============================================================================

-- 1. Create Recipient for Open Delta Sharing
CREATE RECIPIENT IF NOT EXISTS recipient_hybridgenai_shared
USING ID 'aws:us-east-2:0a6cc551-4c15-44a3-8a44-5090cee441c9'
COMMENT 'Databricks-to-Databricks open delta sharing recipient for migration parity audit';

-- 2. Create the Enterprise Migration Share
CREATE SHARE IF NOT EXISTS palantir_oracle_migration_share
COMMENT 'Bi-directional open share for Palantir and Oracle modernized Delta tables';

-- 3. Add Delta UniForm & Iceberg Tables to Share
ALTER SHARE palantir_oracle_migration_share
ADD TABLE gold.enterprise.customer_master
COMMENT 'Cleaned Customer 360 master table with UniForm Iceberg compatibility';

ALTER SHARE palantir_oracle_migration_share
ADD TABLE gold.finance.fact_transactions
COMMENT 'Gold Financial settled transactions for multi-platform parity reconciliation';

-- 4. Grant Access on Share to the Recipient
GRANT SELECT ON SHARE palantir_oracle_migration_share
TO RECIPIENT recipient_hybridgenai_shared;

-- 5. Inspect Share Status & Active Recipients
DESCRIBE SHARE palantir_oracle_migration_share;
DESCRIBE RECIPIENT recipient_hybridgenai_shared;
