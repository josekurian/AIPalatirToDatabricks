# Prototype 09: Algorithmic Fraud Detection & Card-Not-Present Transaction Shield
**Industry**: Payment Processing  
**Tech Stack**: Scala Streaming Engine, Kafka, Redis/Lakebase, Unity Catalog  

---

## 1. Executive Business Problem
Credit card fraud rules in Oracle PL/SQL cause 12% false positives and cannot evaluate rolling 10-minute velocity.

## 2. Technical Lakehouse Solution
High-throughput Scala/Spark streaming engine calculating sliding window transaction velocity in <5ms.

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
