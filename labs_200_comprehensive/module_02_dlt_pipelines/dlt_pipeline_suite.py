"""
Comprehensive Production Scripts for Module 2: Delta Live Tables (Labs 026 - 050)
Translates visual Pipeline Builder and multi-stage builds into declarative DLT syntax.
"""

import dlt
from pyspark.sql import functions as F
from pyspark.sql.types import DoubleType, TimestampType

# Lab 026 & 027: Bronze Auto Loader Streaming Ingestion
@dlt.table(
    name="bronze_erp_sales_orders",
    comment="Raw streaming ingest via Auto Loader (cloudFiles)",
    table_properties={"quality": "bronze"}
)
def bronze_erp_sales_orders():
    return (
        spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "json")
        .option("cloudFiles.schemaLocation", "/mnt/checkpoints/bronze_orders")
        .load("/mnt/raw_landing/erp/orders/")
    )

# Lab 028, 029 & 030: Silver Tier with Strict Data Quality Expectations
@dlt.table(
    name="silver_sales_orders",
    comment="Cleaned sales orders with automated hygiene enforcement",
    table_properties={"quality": "silver"}
)
@dlt.expect_or_drop("valid_order_id", "order_id IS NOT NULL")
@dlt.expect_or_fail("positive_amount", "order_amount >= 0.0")
@dlt.expect("valid_customer_reference", "customer_id IS NOT NULL")
def silver_sales_orders():
    return (
        dlt.read_stream("bronze_erp_sales_orders")
        .select(
            F.col("order_id").cast("string"),
            F.col("customer_id").cast("string"),
            F.col("order_amount").cast(DoubleType()),
            F.col("order_date").cast(TimestampType()),
            F.col("status").alias("order_status")
        )
    )

# Lab 038: Gold Tier with Delta Liquid Clustering
@dlt.table(
    name="gold_customer_360",
    comment="Gold business entity: Cleaned Customer 360 data with Liquid Clustering",
    table_properties={
        "quality": "gold",
        "delta.enableLiquidClustering": "true"
    }
)
@dlt.expect_or_drop("valid_customer_id", "customer_id IS NOT NULL")
def gold_customer_360():
    customers = dlt.read("silver_customers")
    orders = dlt.read("silver_sales_orders")
    return customers.join(orders, on="customer_id", how="inner")
