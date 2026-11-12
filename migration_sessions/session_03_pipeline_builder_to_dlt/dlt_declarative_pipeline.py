"""
Session 3: Pipeline Builder to Delta Live Tables (DLT) & Expectations
Converts visual Pipeline Builder workflows into declarative Python DLT syntax with expectations.
"""

import dlt
from pyspark.sql import functions as F
from pyspark.sql.types import DoubleType, TimestampType

# Bronze Tier
@dlt.table(
    name="bronze_erp_orders",
    comment="Raw streaming ingest via Auto Loader",
    table_properties={"quality": "bronze"}
)
def bronze_erp_orders():
    return (
        spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "json")
        .option("cloudFiles.schemaLocation", "/mnt/checkpoints/bronze_orders")
        .load("/mnt/raw_landing/erp/orders/")
    )

# Silver Tier with Data Quality Expectations
@dlt.table(
    name="silver_orders_cleansed",
    comment="Cleaned orders with automated hygiene enforcement",
    table_properties={"quality": "silver"}
)
@dlt.expect_or_drop("valid_order_id", "order_id IS NOT NULL")
@dlt.expect_or_fail("positive_order_amount", "order_total_usd >= 0.0")
@dlt.expect("valid_customer_key", "customer_id IS NOT NULL")
def silver_orders_cleansed():
    return (
        dlt.read_stream("bronze_erp_orders")
        .select(
            F.col("order_id"),
            F.col("customer_id"),
            F.col("sku_id"),
            F.col("order_amount").cast(DoubleType()).alias("order_total_usd"),
            F.col("order_timestamp").cast(TimestampType())
        )
    )

# Gold Tier with Liquid Clustering
@dlt.table(
    name="gold_order_fulfillment",
    comment="Curated gold orders ready for operational cockpits",
    table_properties={"quality": "gold", "delta.enableLiquidClustering": "true"}
)
def gold_order_fulfillment():
    orders = dlt.read("silver_orders_cleansed")
    customers = dlt.read("silver_customers")
    return orders.join(customers, on="customer_id", how="inner")
