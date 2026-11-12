"""
Oracle CDC (GoldenGate / Debezium) Ingestion via Databricks Auto Loader
Streams real-time Oracle redo log mutations (INSERT, UPDATE, DELETE) into Bronze Delta Lake
and applies SCD Type 1 & Type 2 upserts.
"""

import dlt
from pyspark.sql import functions as F

@dlt.table(
    name="bronze_oracle_cdc_stream",
    comment="Raw streaming ingest of Oracle redo logs from Kafka / Cloud Storage",
    table_properties={"quality": "bronze"}
)
def bronze_oracle_cdc_stream():
    return (
        spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "json")
        .option("cloudFiles.schemaLocation", "/mnt/checkpoints/oracle_cdc_schema")
        .load("/mnt/raw_landing/oracle_cdc/")
    )

# Apply CDC Changes automatically handling In-Order Updates and Soft Deletes
dlt.create_streaming_table(
    name="silver_oracle_customers_conformed",
    comment="Cleansed customer records maintaining latest CDC state from Oracle",
    table_properties={"quality": "silver"}
)

dlt.apply_changes(
    target="silver_oracle_customers_conformed",
    source="bronze_oracle_cdc_stream",
    keys=["customer_id"],
    sequence_by=F.col("op_timestamp"),
    apply_as_deletes=F.expr("op_type = 'D'"),
    except_column_list=["op_type", "op_timestamp"]
)
