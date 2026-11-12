"""
Embedded In-Memory Apache Kafka Cluster Engine
Provides a lightweight, zero-external-dependency Kafka cluster instance with topic management,
partition offsets, consumer groups, and high-throughput publish/subscribe streaming mechanics.
"""

import time
import json
import threading
from typing import Dict, Any, List, Optional

class EmbeddedKafkaTopic:
    def __init__(self, topic_name: str, partitions: int = 3):
        self.topic_name = topic_name
        self.num_partitions = partitions
        self.partitions: List[List[Dict[str, Any]]] = [[] for _ in range(partitions)]
        self._lock = threading.Lock()

    def produce(self, key: str, value: Dict[str, Any], headers: Dict[str, str] = None) -> Dict[str, Any]:
        with self._lock:
            # Hash partitioner
            partition_idx = hash(key) % self.num_partitions
            partition = self.partitions[partition_idx]
            offset = len(partition)
            message = {
                "topic": self.topic_name,
                "partition": partition_idx,
                "offset": offset,
                "key": key,
                "value": value,
                "headers": headers or {},
                "timestamp_ms": int(time.time() * 1000)
            }
            partition.append(message)
            return message

    def fetch(self, partition_idx: int, offset: int, max_messages: int = 100) -> List[Dict[str, Any]]:
        with self._lock:
            if partition_idx >= self.num_partitions:
                return []
            partition = self.partitions[partition_idx]
            return partition[offset : offset + max_messages]

    def total_messages(self) -> int:
        with self._lock:
            return sum(len(p) for p in self.partitions)


class EmbeddedKafkaCluster:
    def __init__(self, cluster_id: str = "kafka-cluster-lab-01"):
        self.cluster_id = cluster_id
        self.topics: Dict[str, EmbeddedKafkaTopic] = {}
        self.consumer_group_offsets: Dict[str, Dict[str, Dict[int, int]]] = {} # group -> topic -> partition -> offset
        self._lock = threading.Lock()

    def create_topic(self, topic_name: str, partitions: int = 3) -> EmbeddedKafkaTopic:
        with self._lock:
            if topic_name not in self.topics:
                self.topics[topic_name] = EmbeddedKafkaTopic(topic_name, partitions)
            return self.topics[topic_name]

    def produce_message(self, topic_name: str, key: str, value: Dict[str, Any]) -> Dict[str, Any]:
        if topic_name not in self.topics:
            self.create_topic(topic_name)
        return self.topics[topic_name].produce(key, value)

    def consume_batch(self, group_id: str, topic_name: str, max_messages: int = 50) -> List[Dict[str, Any]]:
        with self._lock:
            if topic_name not in self.topics:
                return []
            topic = self.topics[topic_name]
            
            if group_id not in self.consumer_group_offsets:
                self.consumer_group_offsets[group_id] = {}
            if topic_name not in self.consumer_group_offsets[group_id]:
                self.consumer_group_offsets[group_id][topic_name] = {p: 0 for p in range(topic.num_partitions)}

            consumed = []
            for p in range(topic.num_partitions):
                curr_offset = self.consumer_group_offsets[group_id][topic_name][p]
                msgs = topic.fetch(p, curr_offset, max_messages)
                if msgs:
                    consumed.extend(msgs)
                    self.consumer_group_offsets[group_id][topic_name][p] = curr_offset + len(msgs)

            return consumed

    def get_cluster_metrics(self) -> Dict[str, Any]:
        with self._lock:
            return {
                "cluster_id": self.cluster_id,
                "topics_count": len(self.topics),
                "topics": {
                    t_name: {
                        "partitions": t.num_partitions,
                        "messages": t.total_messages()
                    }
                    for t_name, t in self.topics.items()
                },
                "active_consumer_groups": len(self.consumer_group_offsets)
            }

# Global singleton instance for labs and interactive demos
kafka_instance = EmbeddedKafkaCluster("enterprise-kafka-broker-9092")

if __name__ == "__main__":
    cluster = EmbeddedKafkaCluster()
    cluster.create_topic("iot_telemetry", 3)
    for i in range(10):
        cluster.produce_message("iot_telemetry", f"DEV-{i%3}", {"temp_c": 65 + i, "speed_rpm": 3000 + i*10})
    
    msgs = cluster.consume_batch("iot_analytics_group", "iot_telemetry", 20)
    print(f"Consumed {len(msgs)} messages from Kafka.")
    print("Metrics:", cluster.get_cluster_metrics())
