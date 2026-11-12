# Prototype 13: Ad-Tech Clickstream Attribution & Multi-Touch Conversion Modeling
**Industry**: Digital Media & Advertising  
**Tech Stack**: PySpark, Delta Lake UniForm, Apache Iceberg, Databricks SQL Serverless  

---

## 1. Executive Business Problem
Marketing team relies on simplistic last-click attribution; third-party cookie phaseout blinds attribution pipelines.

## 2. Technical Lakehouse Solution
Markov chain multi-touch attribution on 100M daily impression logs querying Delta UniForm via Apache Iceberg.

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
