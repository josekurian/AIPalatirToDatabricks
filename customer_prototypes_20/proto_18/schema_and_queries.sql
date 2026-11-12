-- ============================================================================
-- Customer Prototype: E-Commerce Customer Lifetime Value (CLV) & Tier Upgrade Engine
-- Table DDL with Delta UniForm & Apache Iceberg v2 Metadata Generation
-- ============================================================================

CREATE TABLE IF NOT EXISTS gold.proto_18.master_records (
    record_id STRING NOT NULL,
    entity_code STRING,
    metric_value DOUBLE,
    status STRING,
    created_at TIMESTAMP,
    CONSTRAINT pk_proto_18 PRIMARY KEY(record_id)
)
USING DELTA
TBLPROPERTIES (
    'delta.universalFormat.enabledFormats' = 'iceberg',
    'delta.enableIcebergCompatV2' = 'true',
    'governance.domain' = 'Retail',
    'governance.tier' = 'certified_gold'
)
CLUSTER BY (status);
