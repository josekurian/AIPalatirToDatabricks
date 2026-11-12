# Prototype 01: Real-Time Telemetry & Anomaly Detection
**Industry**: Manufacturing & IoT  
**Tech Stack**: PySpark Streaming, Apache Kafka, Delta Lake UniForm, Apache Iceberg  

---

## 1. Executive Business Problem
Factory sensor data arrives via Kafka at 50,000 events/sec. Monolithic Oracle and Palantir pipelines introduce 45-minute batch lag.

## 2. Technical Lakehouse Solution
End-to-end Spark Structured Streaming with Delta Auto Loader, real-time z-score anomaly detection, and Iceberg v2 manifest sync.

---

## 3. Hands-On Step-by-Step Lab Instructions

### Step 1: Environment Setup & Catalog Initialization
Execute the SQL initialization script to provision Unity Catalog schemas and Delta UniForm tables:
```bash
python3 run_pipeline.py --step init
```

### Step 2: Ingest & Process Stream / Batch Data
Execute the PySpark pipeline engine to ingest simulated customer data, evaluate quality expectations, and cluster records:
```bash
python3 run_pipeline.py --step process
```

### Step 3: Run Algorithmic Analytics / Machine Learning
Run the analytical scoring and operational state updates:
```bash
python3 run_pipeline.py --step score
```

### Step 4: Verification & Parity Audit
Inspect the generated Apache Iceberg v2 metadata and verify zero data drift:
```bash
python3 run_pipeline.py --step verify
```
