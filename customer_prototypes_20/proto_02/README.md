# Prototype 02: Next-Best-Action Recommendation & Real-Time Scoring
**Industry**: Financial Services & Banking  
**Tech Stack**: Python, MLflow, Mosaic AI Model Serving, Unity Catalog Feature Store  

---

## 1. Executive Business Problem
Retail banking customers expect personalized loan offers at mobile login. Palantir models require external exports.

## 2. Technical Lakehouse Solution
Feature Store integration with sub-20ms Mosaic AI Model Serving endpoints and Databricks Apps interactive review.

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
