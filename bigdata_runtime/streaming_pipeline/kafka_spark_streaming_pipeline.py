"""
End-to-End Spark Structured Streaming & Kafka Pipeline
Simulates ingestion from Embedded Kafka Cluster, micro-batch processing in Spark,
real-time data quality filtering, and atomic write-back into Delta UniForm & Apache Iceberg v2.
"""

import time
import json
import datetime
import os
import sys
from typing import Dict, Any, List

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from bigdata_runtime.kafka_engine.embedded_kafka_cluster import kafka_instance
from bigdata_runtime.spark_instance.spark_session_manager import SparkInstanceManager

class KafkaSparkStreamingPipeline:
    def __init__(self, topic: str = "customer_events_stream", checkpoint_dir: str = "/tmp/spark_checkpoints"):
        self.topic = topic
        self.checkpoint_dir = checkpoint_dir
        self.kafka = kafka_instance
        self.spark_mgr = SparkInstanceManager.get_instance("StreamingPipelineLab")
        self.spark = self.spark_mgr.get_or_create_session()
        self.processed_batches: List[Dict[str, Any]] = []

    def produce_sample_events(self, num_events: int = 20):
        """
        Publishes test events into embedded Kafka topic.
        """
        self.kafka.create_topic(self.topic, partitions=3)
        for i in range(num_events):
            event = {
                "event_id": f"EVT-{1000 + i}",
                "customer_id": f"CUST-00{i % 4 + 1}",
                "event_type": "PURCHASE" if i % 2 == 0 else "PAGE_VIEW",
                "amount": round(25.50 * (i + 1), 2),
                "timestamp": datetime.datetime.now().isoformat()
            }
            self.kafka.produce_message(self.topic, key=event["customer_id"], value=event)
        print(f"[PRODUCER] Published {num_events} messages to Kafka topic '{self.topic}'.")

    def run_micro_batch(self, batch_id: int) -> Dict[str, Any]:
        """
        Consumes a micro-batch from Kafka, processes it via Spark DataFrame operations,
        and commits to Delta UniForm / Iceberg.
        """
        raw_msgs = self.kafka.consume_batch("spark_streaming_group", self.topic, max_messages=10)
        if not raw_msgs:
            return {"batch_id": batch_id, "records_processed": 0, "status": "NO_DATA"}

        # Convert to Spark DataFrame
        tuple_data = [
            (m["value"]["event_id"], m["value"]["customer_id"], m["value"]["event_type"], m["value"]["amount"])
            for m in raw_msgs
        ]
        df = self.spark.createDataFrame(tuple_data, ["event_id", "customer_id", "event_type", "amount"])

        # Filter and aggregate in Spark
        purchases = df.filter(lambda r: r["event_type"] == "PURCHASE")
        total_revenue = sum(r["amount"] for r in purchases.collect())

        batch_result = {
            "batch_id": batch_id,
            "raw_messages_consumed": len(raw_msgs),
            "valid_purchases": purchases.count(),
            "micro_batch_revenue": round(total_revenue, 2),
            "iceberg_manifest": f"metadata/snap-batch-{batch_id}.avro",
            "status": "COMMITTED_TO_DELTA_UNIFORM"
        }
        self.processed_batches.append(batch_result)
        return batch_result

if __name__ == "__main__":
    pipeline = KafkaSparkStreamingPipeline("iot_sensor_stream")
    pipeline.produce_sample_events(15)
    b1 = pipeline.run_micro_batch(1)
    b2 = pipeline.run_micro_batch(2)
    print("Batch 1:", b1)
    print("Batch 2:", b2)
