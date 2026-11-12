"""
Databricks Delta Live Tables (DLT) Pipeline: Supply Chain & Customer 360
Refactored directly from Palantir Foundry Code Repositories (@transform_df).
Features native Auto Loader, DLT expectations, and automated Delta optimization.
"""

import dlt
from pyspark.sql import functions as F
from pyspark.sql.types import DoubleType, TimestampType

# ==============================================================================
# BRONZE LAYER (Auto Loader from Cloud Object Storage)
# ==============================================================================

@dlt.table(
    name="bronze_sap_customers",
    comment="Raw streaming ingest of SAP customers via Auto Loader",
    table_properties={"quality": "bronze"}
)
def bronze_sap_customers():
    return (
        spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "parquet")
        .option("cloudFiles.schemaLocation", "/mnt/checkpoints/bronze_sap_customers")
        .load("/mnt/raw_landing/sap/customers/")
    )

@dlt.table(
    name="bronze_crm_accounts",
    comment="Raw streaming ingest of Salesforce CRM accounts via Auto Loader",
    table_properties={"quality": "bronze"}
)
def bronze_crm_accounts():
    return (
        spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "json")
        .option("cloudFiles.schemaLocation", "/mnt/checkpoints/bronze_crm_accounts")
        .load("/mnt/raw_landing/salesforce/accounts/")
    )

@dlt.table(
    name="bronze_sap_orders",
    comment="Raw streaming ingest of SAP Sales Orders",
    table_properties={"quality": "bronze"}
)
def bronze_sap_orders():
    return (
        spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "parquet")
        .option("cloudFiles.schemaLocation", "/mnt/checkpoints/bronze_sap_orders")
        .load("/mnt/raw_landing/sap/sales_orders/")
    )

# ==============================================================================
# SILVER LAYER (Cleansed, Deduplicated & Conformed with Data Quality Expectations)
# ==============================================================================

@dlt.table(
    name="silver_customers",
    comment="Cleansed and deduplicated customer master records",
    table_properties={"quality": "silver"}
)
@dlt.expect_or_drop("valid_customer_id", "sap_customer_id IS NOT NULL")
@dlt.expect("valid_email_format", "primary_email RLIKE '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$'")
def silver_customers():
    raw_customers = dlt.read_stream("bronze_sap_customers")
    crm_accounts = dlt.read("bronze_crm_accounts")

    sap_clean = raw_customers.select(
        F.col("KUNNR").alias("sap_customer_id"),
        F.trim(F.col("NAME1")).alias("customer_name"),
        F.lower(F.trim(F.col("SMTP_ADDR"))).alias("primary_email"),
        F.col("LAND1").alias("country_code"),
        F.col("ORT01").alias("city"),
        F.col("STCEG").alias("tax_identifier"),
        F.col("ERDAT").cast(TimestampType()).alias("created_timestamp")
    )

    crm_clean = crm_accounts.select(
        F.col("Id").alias("sfdc_account_id"),
        F.col("AccountNumber").alias("crm_account_number"),
        F.col("AnnualRevenue").cast(DoubleType()).alias("annual_revenue"),
        F.col("Industry").alias("industry_segment"),
        F.col("Rating").alias("credit_tier")
    )

    return sap_clean.join(
        crm_clean,
        sap_clean.sap_customer_id == crm_clean.crm_account_number,
        how="left"
    ).withColumn(
        "customer_id", F.coalesce(F.col("sap_customer_id"), F.col("sfdc_account_id"))
    ).withColumn(
        "last_updated_at", F.current_timestamp()
    )

# ==============================================================================
# GOLD LAYER (Semantic Business Objects & Decision Datasets)
# ==============================================================================

@dlt.table(
    name="gold_fact_supply_order",
    comment="Gold business entity: Supply chain orders with delivery risk calculations",
    table_properties={
        "quality": "gold",
        "delta.enableLiquidClustering": "true"
    }
)
@dlt.expect_or_fail("positive_order_amount", "order_total_usd >= 0.0")
@dlt.expect_or_drop("valid_order_id", "order_id IS NOT NULL")
def gold_fact_supply_order():
    orders = dlt.read_stream("bronze_sap_orders").select(
        F.col("VBELN").alias("order_id"),
        F.col("KUNNR").alias("customer_id"),
        F.col("MATNR").alias("sku_id"),
        F.col("KWMENG").cast(DoubleType()).alias("ordered_quantity"),
        F.col("NETWR").cast(DoubleType()).alias("order_total_usd"),
        F.col("VDATU").cast(TimestampType()).alias("requested_delivery_date"),
        F.col("LFSTK").alias("fulfillment_status")
    )

    customers = dlt.read("silver_customers")

    return orders.join(
        customers.select("customer_id", "credit_tier"),
        on="customer_id",
        how="inner"
    ).withColumn(
        "high_value_order",
        F.when(F.col("order_total_usd") >= 100000.0, F.lit(True)).otherwise(F.lit(False))
    ).withColumn(
        # Delivery Risk calculation translated from Palantir Typescript Function
        "delivery_risk_score",
        F.lit(10.0) +
        F.when(F.col("high_value_order"), F.lit(25.0)).otherwise(F.lit(0.0)) +
        F.when(F.col("fulfillment_status") == "DELAYED", F.lit(15.0)).otherwise(F.lit(0.0))
    ).withColumn(
        "last_updated_at", F.current_timestamp()
    )
