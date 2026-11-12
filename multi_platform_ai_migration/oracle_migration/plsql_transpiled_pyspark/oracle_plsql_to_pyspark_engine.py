"""
Oracle PL/SQL to Databricks PySpark Transpilation
Refactors legacy Oracle stored procedures, row-level cursors, and credit rating evaluations
into high-throughput, vectorized PySpark DataFrame operations.
"""

from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window
from pyspark.sql.types import DoubleType, StringType

def process_oracle_customer_credit_evaluation(spark: SparkSession) -> int:
    """
    Original Oracle PL/SQL Logic:
    --------------------------------------------------------------------------
    CREATE OR REPLACE PACKAGE BODY pkg_customer_credit AS
      PROCEDURE evaluate_credit_limits IS
        CURSOR c_cust IS 
          SELECT customer_id, annual_revenue, credit_score, current_limit 
          FROM oracle_customers WHERE status = 'ACTIVE' FOR UPDATE;
      BEGIN
        FOR r IN c_cust LOOP
          IF r.credit_score >= 750 THEN
             UPDATE oracle_customers SET current_limit = r.annual_revenue * 0.25 
             WHERE customer_id = r.customer_id;
          ELSIF r.credit_score >= 650 THEN
             UPDATE oracle_customers SET current_limit = r.annual_revenue * 0.15 
             WHERE customer_id = r.customer_id;
          ELSE
             UPDATE oracle_customers SET current_limit = r.annual_revenue * 0.05 
             WHERE customer_id = r.customer_id;
          END IF;
        END LOOP;
        COMMIT;
      END evaluate_credit_limits;
    END pkg_customer_credit;
    --------------------------------------------------------------------------
    Target Databricks Vectorized PySpark Transformation:
    """
    source_table = "enterprise_operations.silver.oracle_customers"
    target_table = "enterprise_operations.gold.customer_master"

    df = spark.table(source_table).filter(F.col("status") == "ACTIVE")

    # Vectorized CASE WHEN statement executing across worker cores in parallel
    evaluated_df = df.withColumn(
        "credit_limit_usd",
        F.when(F.col("credit_score") >= 750, F.col("annual_revenue") * 0.25)
         .when(F.col("credit_score") >= 650, F.col("annual_revenue") * 0.15)
         .otherwise(F.col("annual_revenue") * 0.05)
    ).withColumn(
        "credit_tier",
        F.when(F.col("credit_score") >= 750, F.lit("PLATINUM"))
         .when(F.col("credit_score") >= 650, F.lit("GOLD"))
         .otherwise(F.lit("STANDARD"))
    ).withColumn(
        "evaluated_at", F.current_timestamp()
    )

    # Perform atomic Delta Lake MERGE (Upsert) into Gold Customer Master
    evaluated_df.createOrReplaceTempView("v_evaluated_customers")
    
    merge_query = f"""
    MERGE INTO {target_table} AS tgt
    USING v_evaluated_customers AS src
    ON tgt.customer_id = src.customer_id
    WHEN MATCHED THEN UPDATE SET
        tgt.credit_tier = src.credit_tier,
        tgt.annual_revenue = src.annual_revenue,
        tgt.last_updated_at = src.evaluated_at
    WHEN NOT MATCHED THEN INSERT (
        customer_id, customer_name, primary_email, country_code, credit_tier, annual_revenue, last_updated_at
    ) VALUES (
        src.customer_id, src.customer_name, src.primary_email, src.country_code, src.credit_tier, src.annual_revenue, src.evaluated_at
    )
    """
    spark.sql(merge_query)
    print("Transpiled Oracle PL/SQL package executed successfully as Delta Lake MERGE.")
    return evaluated_df.count()

if __name__ == "__main__":
    print("Compiled Oracle PL/SQL Transpiled PySpark module successfully.")
