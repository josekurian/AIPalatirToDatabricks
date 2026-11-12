"""
Session 2: @transform_df / Code Repositories to Native PySpark & DABs
Deconstructs Foundry @transform_df into clean, testable PySpark modules.
"""

from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from pyspark.sql.window import Window

def cleanse_and_harmonize_customers(raw_customers: DataFrame, crm_accounts: DataFrame) -> DataFrame:
    """
    Step-by-step refactoring of Foundry Code Repository transforms.
    Removes proprietary decorators (@transform_df, Input, Output) and implements native Spark APIs.
    """
    # 1. Cleanse customer master fields
    clean_cust = raw_customers.select(
        F.col("customer_id"),
        F.trim(F.col("customer_name")).alias("customer_name"),
        F.lower(F.trim(F.col("primary_email"))).alias("primary_email"),
        F.col("country_code"),
        F.col("tax_id")
    ).filter(F.col("customer_id").isNotNull())

    # 2. Join with CRM accounts
    unified = clean_cust.join(
        crm_accounts.select("account_id", "credit_tier", "annual_revenue"),
        clean_cust.customer_id == crm_accounts.account_id,
        how="left"
    ).drop("account_id")

    # 3. Add audit tracking
    return unified.withColumn("migrated_at", F.current_timestamp())
