# Prototype 04: Omnichannel Dynamic Pricing & Markdown Optimization
**Industry**: Retail & E-Commerce  
**Tech Stack**: PySpark, Databricks SQL Serverless, Photon Engine, Liquid Clustering  

---

## 1. Executive Business Problem
E-commerce catalog of 10M SKUs requires hourly price adjustments based on competitor price crawling and inventory levels.

## 2. Technical Lakehouse Solution
Photon-optimized aggregations with liquid clustering on category and store_id, reducing runtime by 78%.

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
