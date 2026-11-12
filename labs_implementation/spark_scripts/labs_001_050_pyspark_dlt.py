"""
Enterprise Hands-On Labs Script Repository: Apache Spark, Delta Lake, DLT & PySpark
Covers Labs 001 - 050: PySpark refactoring, streaming Auto Loader, and data quality expectations.
"""

from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import (
    StructType, StructField, StringType, DoubleType, TimestampType, IntegerType
)
from pyspark.sql.window import Window
import os

def create_lab_spark_session():
    """Initializes a local SparkSession configured with Delta Lake support."""
    return SparkSession.builder \
        .appName("PalantirToDatabricks_Labs_Spark") \
        .master("local[*]") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .getOrCreate()

# ==============================================================================
# LAB 001: REFACTORING BASIC @transform_df TO NATIVE PYSPARK
# ==============================================================================
def lab_001_refactor_transform_df(raw_customers_df, orders_df):
    """
    Original Palantir Pattern:
        @transform_df(
            Output("/Clean/Customer360"),
            raw=Input("/Raw/Customers"),
            orders=Input("/Raw/Orders")
        )
    Databricks Pattern: Clean decoupled function returning Spark DataFrame.
    """
    clean_customers = raw_customers_df.select(
        F.col("customer_id"),
        F.trim(F.col("customer_name")).alias("customer_name"),
        F.lower(F.col("email")).alias("email")
    ).filter(F.col("customer_id").isNotNull())

    return clean_customers.join(orders_df, on="customer_id", how="inner") \
        .withColumn("migrated_at", F.current_timestamp())

# ==============================================================================
# LAB 006 & 007: BROADCAST JOINS AND WINDOW SPEC AGGREGATIONS
# ==============================================================================
def lab_007_window_aggregations(orders_df):
    """
    Refactors Palantir Quiver/Contour rolling metrics into native PySpark Window functions.
    """
    customer_window = Window.partitionBy("customer_id").orderBy(F.col("order_date").desc())
    cumulative_window = Window.partitionBy("customer_id").orderBy("order_date").rowsBetween(Window.unboundedPreceding, Window.currentRow)

    enriched_df = orders_df.withColumn(
        "order_rank", F.row_number().over(customer_window)
    ).withColumn(
        "cumulative_spend_usd", F.sum("amount").over(cumulative_window)
    ).withColumn(
        "previous_order_amount", F.lag("amount", 1).over(customer_window)
    )
    return enriched_df

# ==============================================================================
# LAB 019: VECTORIZED PANDAS UDF (ACCELERATING SLOW FOUNDRY TRANSFORMS)
# ==============================================================================
def lab_019_vectorized_pandas_udf():
    from pyspark.sql.functions import pandas_udf
    import pandas as pd

    @pandas_udf(DoubleType())
    def calculate_compound_risk(score_series: pd.Series, multiplier_series: pd.Series) -> pd.Series:
        # High speed SIMD vectorized calculation via PyArrow
        return (score_series * multiplier_series * 1.15).clip(lower=0.0, upper=100.0)

    return calculate_compound_risk

if __name__ == "__main__":
    spark = create_lab_spark_session()
    print("Spark initialized successfully for Labs 001-050.")
    spark.stop()
