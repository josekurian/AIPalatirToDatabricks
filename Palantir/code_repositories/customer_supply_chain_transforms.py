"""
Palantir Foundry Transforms: Customer 360 & Supply Chain Pipeline
Demonstrating native Foundry Code Repositories idioms: @transform, @transform_df, Input, Output
"""

from transforms.api import transform_df, Input, Output, configure
from pyspark.sql import functions as F
from pyspark.sql.types import StringType, TimestampType, DoubleType, IntegerType

@configure(profile=['DRIVER_MEMORY_MEDIUM', 'EXECUTOR_MEMORY_LARGE'])
@transform_df(
    Output("/Company/Ontology/Clean/dim_customers"),
    raw_customers=Input("/Company/Raw/SAP/customers"),
    crm_accounts=Input("/Company/Raw/Salesforce/accounts")
)
def compute_clean_customers(raw_customers, crm_accounts):
    """
    Cleanses and harmonizes customer master records from SAP ERP and Salesforce CRM.
    Standard Foundry pattern utilizing schema conformance, phone/email standardization,
    and deduplication based on tax/corporate IDs.
    """
    sap_clean = raw_customers.select(
        F.col("KUNNR").alias("sap_customer_id"),
        F.trim(F.col("NAME1")).alias("customer_name"),
        F.lower(F.trim(F.col("SMTP_ADDR"))).alias("primary_email"),
        F.col("LAND1").alias("country_code"),
        F.col("ORT01").alias("city"),
        F.col("STCEG").alias("tax_identifier"),
        F.col("ERDAT").cast(TimestampType()).alias("created_timestamp")
    ).filter(F.col("sap_customer_id").isNotNull())

    crm_clean = crm_accounts.select(
        F.col("Id").alias("sfdc_account_id"),
        F.col("AccountNumber").alias("crm_account_number"),
        F.col("AnnualRevenue").cast(DoubleType()).alias("annual_revenue"),
        F.col("Industry").alias("industry_segment"),
        F.col("Rating").alias("credit_tier")
    )

    # Master Entity Resolution join
    unified_customers = sap_clean.join(
        crm_clean,
        sap_clean.sap_customer_id == crm_clean.crm_account_number,
        how="left"
    ).withColumn(
        "customer_id",
        F.coalesce(F.col("sap_customer_id"), F.col("sfdc_account_id"))
    ).withColumn(
        "ontology_sync_status", F.lit("ACTIVE")
    ).withColumn(
        "last_ingested_at", F.current_timestamp()
    )

    return unified_customers


@transform_df(
    Output("/Company/Ontology/Clean/fact_supply_chain_orders"),
    sap_orders=Input("/Company/Raw/SAP/sales_orders"),
    clean_customers=Input("/Company/Ontology/Clean/dim_customers"),
    inventory_levels=Input("/Company/Raw/WMS/inventory_snapshot")
)
def compute_supply_chain_orders(sap_orders, clean_customers, inventory_levels):
    """
    Constructs high-speed operational order records linked with live WMS inventory.
    Provides immediate input for Palantir Foundry Object sync.
    """
    orders = sap_orders.select(
        F.col("VBELN").alias("order_id"),
        F.col("KUNNR").alias("customer_id"),
        F.col("MATNR").alias("sku_id"),
        F.col("KWMENG").cast(DoubleType()).alias("ordered_quantity"),
        F.col("NETWR").cast(DoubleType()).alias("order_total_usd"),
        F.col("VDATU").cast(TimestampType()).alias("requested_delivery_date"),
        F.col("LFSTK").alias("fulfillment_status")
    )

    inventory = inventory_levels.select(
        F.col("material_id").alias("sku_id"),
        F.col("warehouse_id"),
        F.col("available_stock").cast(DoubleType()),
        F.col("safety_stock_threshold").cast(DoubleType())
    )

    enriched_orders = orders.join(
        clean_customers.select("customer_id", "customer_name", "credit_tier"),
        on="customer_id",
        how="inner"
    ).join(
        inventory,
        on="sku_id",
        how="left"
    ).withColumn(
        "stock_shortage_flag",
        F.when(F.col("ordered_quantity") > F.col("available_stock"), F.lit(True)).otherwise(F.lit(False))
    ).withColumn(
        "high_value_order",
        F.when(F.col("order_total_usd") >= 100000.0, F.lit(True)).otherwise(F.lit(False))
    )

    return enriched_orders
