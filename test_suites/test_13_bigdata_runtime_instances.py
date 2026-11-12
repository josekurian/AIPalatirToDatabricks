import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from bigdata_runtime.kafka_engine.embedded_kafka_cluster import EmbeddedKafkaCluster
from bigdata_runtime.spark_instance.spark_session_manager import SparkInstanceManager
from bigdata_runtime.streaming_pipeline.kafka_spark_streaming_pipeline import KafkaSparkStreamingPipeline

class TestBigDataRuntimeInstances(unittest.TestCase):

    def setUp(self):
        self.kafka = EmbeddedKafkaCluster("test-cluster-9092")
        self.spark_mgr = SparkInstanceManager.get_instance("TestSparkSuite")
        self.spark = self.spark_mgr.get_or_create_session()

    def test_embedded_kafka_produce_and_consume(self):
        """Verifies embedded Kafka instance partitions messages and tracks consumer offsets."""
        self.kafka.create_topic("test_metrics", partitions=3)
        for i in range(12):
            self.kafka.produce_message("test_metrics", f"KEY-{i}", {"metric_val": i * 10})
        
        metrics = self.kafka.get_cluster_metrics()
        self.assertEqual(metrics["topics_count"], 1)
        self.assertEqual(metrics["topics"]["test_metrics"]["messages"], 12)

        # Consume batch with consumer group
        msgs = self.kafka.consume_batch("test_group", "test_metrics", max_messages=20)
        self.assertEqual(len(msgs), 12)

        # Subsequent consume should be empty (offsets advanced)
        empty_msgs = self.kafka.consume_batch("test_group", "test_metrics", max_messages=20)
        self.assertEqual(len(empty_msgs), 0)

    def test_spark_instance_dataframe_operations(self):
        """Verifies Spark instance executes DataFrame filtering, grouping and aggregations."""
        data = [
            ("A1", "Finance", 500.0),
            ("A2", "Sales", 300.0),
            ("A3", "Finance", 700.0),
            ("A4", "Engineering", 1200.0)
        ]
        df = self.spark.createDataFrame(data, ["id", "dept", "budget"])
        self.assertEqual(df.count(), 4)

        # Filter
        high_budget = df.filter(lambda r: r["budget"] > 600.0)
        self.assertEqual(high_budget.count(), 2)

        # GroupBy and Aggregation
        grouped = df.groupBy("dept").agg({"budget": "sum"})
        res_rows = grouped.collect()
        finance_row = next(r for r in res_rows if r["dept"] == "Finance")
        self.assertEqual(finance_row["sum(budget)"], 1200.0)

    def test_kafka_spark_end_to_end_streaming(self):
        """Verifies end-to-end Kafka-to-Spark micro-batch streaming pipeline."""
        streaming = KafkaSparkStreamingPipeline("streaming_test_topic")
        streaming.produce_sample_events(10)
        
        batch = streaming.run_micro_batch(1)
        self.assertEqual(batch["status"], "COMMITTED_TO_DELTA_UNIFORM")
        self.assertGreater(batch["raw_messages_consumed"], 0)
        self.assertTrue(batch["iceberg_manifest"].endswith(".avro"))

if __name__ == '__main__':
    unittest.main()
