# Prototype 19: Connected Vehicle Fleet Battery Health & EV Thermal Degradation
**Industry**: Electric Vehicles (EV)  
**Tech Stack**: PySpark Streaming, Apache Kafka, Delta Liquid Clustering, Genie AI/BI  

---

## 1. Executive Business Problem
Fleet EV battery packs degrade unpredictably in extreme temperatures, voiding manufacturer warranties.

## 2. Technical Lakehouse Solution
Streaming sensor ingestion tracking State of Health (SOH) and degradation curves with Genie executive Q&A.

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
