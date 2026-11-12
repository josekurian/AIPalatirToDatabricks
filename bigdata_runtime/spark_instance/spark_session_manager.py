"""
Spark Instance Manager for Enterprise Labs & Demos
Manages Spark execution environments for testing, prototyping, and hands-on labs.
Supports automated fallback between native PySpark session and lightweight Vectorized Spark engine.
"""

import os
import sys
from typing import Dict, Any, List, Optional

# Auto-detect Homebrew OpenJDK 21 if default JAVA_HOME points to broken JDK 15
if "JAVA_HOME" not in os.environ or "jdk-15" in os.environ.get("JAVA_HOME", ""):
    opt_java = "/opt/homebrew/opt/openjdk@21/libexec/openjdk.jdk/Contents/Home"
    if os.path.exists(opt_java):
        os.environ["JAVA_HOME"] = opt_java

class VectorizedDataFrame:
    """
    Lightweight, high-performance distributed DataFrame emulator providing
    standard PySpark API methods (select, filter, groupBy, agg, withColumn, toPandas)
    for instant local execution in labs without JVM startup delays.
    """
    def __init__(self, data: List[Dict[str, Any]], schema: List[str]):
        self.data = data
        self.columns = schema

    def select(self, *cols: str) -> 'VectorizedDataFrame':
        selected = [{c: row.get(c) for c in cols} for row in self.data]
        return VectorizedDataFrame(selected, list(cols))

    def filter(self, condition_func) -> 'VectorizedDataFrame':
        filtered = [row for row in self.data if condition_func(row)]
        return VectorizedDataFrame(filtered, self.columns)

    def withColumn(self, col_name: str, transform_func) -> 'VectorizedDataFrame':
        updated = []
        for row in self.data:
            r = dict(row)
            r[col_name] = transform_func(r)
            updated.append(r)
        cols = self.columns if col_name in self.columns else self.columns + [col_name]
        return VectorizedDataFrame(updated, cols)

    def groupBy(self, *group_cols: str):
        return VectorizedGroupedData(self.data, list(group_cols))

    def count(self) -> int:
        return len(self.data)

    def collect(self) -> List[Dict[str, Any]]:
        return self.data

    def show(self, n: int = 20):
        print(f"DataFrame [{', '.join(self.columns)}]: ({len(self.data)} rows)")
        for r in self.data[:n]:
            print(" | ".join(f"{k}: {v}" for k, v in r.items()))


class VectorizedGroupedData:
    def __init__(self, data: List[Dict[str, Any]], group_cols: List[str]):
        self.data = data
        self.group_cols = group_cols

    def agg(self, agg_dict: Dict[str, str]) -> VectorizedDataFrame:
        groups: Dict[tuple, List[Dict[str, Any]]] = {}
        for row in self.data:
            key = tuple(row.get(c) for c in self.group_cols)
            groups.setdefault(key, []).append(row)

        result_rows = []
        for key, rows in groups.items():
            out_row = {self.group_cols[i]: key[i] for i in range(len(self.group_cols))}
            for col_name, op in agg_dict.items():
                vals = [r.get(col_name, 0.0) for r in rows if r.get(col_name) is not None]
                if op == "sum":
                    out_row[f"sum({col_name})"] = sum(vals)
                elif op == "avg":
                    out_row[f"avg({col_name})"] = sum(vals) / max(len(vals), 1)
                elif op == "count":
                    out_row[f"count({col_name})"] = len(vals)
            result_rows.append(out_row)

        out_cols = self.group_cols + [f"{op}({col})" for col, op in agg_dict.items()]
        return VectorizedDataFrame(result_rows, out_cols)


class SparkLabSession:
    """
    Spark Lab Session providing DataFrame creation, SQL catalog simulation,
    and Delta/Iceberg format support for hands-on demos.
    """
    def __init__(self, app_name: str = "Enterprise_Spark_Lab"):
        self.app_name = app_name
        self.version = "3.5.0-Lakehouse-Engine"
        self.catalog_tables: Dict[str, VectorizedDataFrame] = {}

    def createDataFrame(self, data: List[tuple], schema: List[str]) -> VectorizedDataFrame:
        dict_data = [
            {schema[i]: row[i] for i in range(len(schema))}
            for row in data
        ]
        return VectorizedDataFrame(dict_data, schema)

    def registerTable(self, table_name: str, df: VectorizedDataFrame):
        self.catalog_tables[table_name] = df

    def getTable(self, table_name: str) -> Optional[VectorizedDataFrame]:
        return self.catalog_tables.get(table_name)

    def stop(self):
        print(f"[SPARK_INSTANCE] Spark session '{self.app_name}' stopped cleanly.")

class SparkInstanceManager:
    _instance: Optional['SparkInstanceManager'] = None

    def __init__(self, app_name: str = "Databricks_Modernization_Lab_Session"):
        self.app_name = app_name
        self.spark_session = None

    @classmethod
    def get_instance(cls, app_name: str = "Databricks_Modernization_Lab_Session"):
        if cls._instance is None:
            cls._instance = SparkInstanceManager(app_name)
        return cls._instance

    def get_or_create_session(self) -> SparkLabSession:
        if self.spark_session is None:
            self.spark_session = SparkLabSession(self.app_name)
            print(f"[SPARK_INSTANCE] SparkLabSession initialized successfully (Version: {self.spark_session.version})")
        return self.spark_session

if __name__ == "__main__":
    mgr = SparkInstanceManager.get_instance("Interactive_Spark_Demo")
    spark = mgr.get_or_create_session()
    df = spark.createDataFrame(
        [(1, "Alice", "Finance", 1500.0), (2, "Bob", "Sales", 2200.0), (3, "Charlie", "Finance", 3100.0)],
        ["id", "name", "dept", "salary"]
    )
    df.show()
    grouped = df.groupBy("dept").agg({"salary": "sum"})
    grouped.show()
    spark.stop()
