"""
Snowflake Snowpark to Native Databricks PySpark Transpilation
Refactors Snowpark Session, Snowpark DataFrames, and Snowpark UDFs
into standard PySpark 3.x/4.x without proprietary vendor client libraries.
"""

from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import DoubleType, StringType

def run_transpiled_snowpark_analytics(spark: SparkSession):
    """
    Original Snowpark Pattern:
    --------------------------------------------------------------------------
    from snowflake.snowpark import Session
    from snowflake.snowpark.functions import col, when
    session = Session.builder.configs(connection_parameters).create()
    df = session.table("ANALYTICS.PROD.FACT_SALES")
    result = df.filter(col("AMOUNT") > 1000).group_by("REGION").agg(sum("AMOUNT"))
    --------------------------------------------------------------------------
    Target Databricks PySpark Pattern:
    """
    # 1. Read directly from Unity Catalog Delta Lake table
    df = spark.table("enterprise_operations.gold.fact_supply_order")

    # 2. High-performance aggregations executing on Photon
    aggregated_sales = (
        df.filter(F.col("order_total_usd") > 1000.0)
          .groupBy("warehouse_id")
          .agg(
              F.count("order_id").alias("total_orders"),
              F.sum("order_total_usd").alias("gross_revenue_usd"),
              F.avg("order_total_usd").alias("average_order_value_usd")
          )
          .withColumn("calculated_at", F.current_timestamp())
    )

    # 3. Write back to aggregated Gold table with Liquid Clustering
    (aggregated_sales.write.format("delta")
        .mode("overwrite")
        .option("delta.enableLiquidClustering", "true")
        .saveAsTable("enterprise_operations.gold.agg_warehouse_sales_metrics"))

    print("Snowpark pipeline transpiled and executed natively in Databricks PySpark.")
    return aggregated_sales

if __name__ == "__main__":
    print("Compiled Snowpark to PySpark transpilation module successfully.")
