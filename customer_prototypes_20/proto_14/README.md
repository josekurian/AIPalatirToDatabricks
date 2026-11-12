# Prototype 14: Insurance Underwriting Risk Engine & Catastrophe Loss Simulation
**Industry**: Property & Casualty Insurance  
**Tech Stack**: PySpark, Monte Carlo Simulations, Java Math Kernel, Unity Catalog  

---

## 1. Executive Business Problem
Hurricane disaster risk models running in Oracle Exadata take 14 hours per simulation batch.

## 2. Technical Lakehouse Solution
Massively parallel Monte Carlo simulation across 1,000 Spark worker nodes completing runs in under 12 minutes.

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
