# Prototype 15: Hotel Room Dynamic Yield Management & Overbooking Optimizer
**Industry**: Hospitality & Travel  
**Tech Stack**: Python, Spark SQL, Lakebase Operational Store, Streamlit App  

---

## 1. Executive Business Problem
Global hotel chain loses $40M annually to unoptimized room prices and last-minute cancellation vacancies.

## 2. Technical Lakehouse Solution
Real-time pricing optimization with interactive revenue manager cockpit built on Databricks Apps.

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
