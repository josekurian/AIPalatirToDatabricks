# Prototype 10: Multi-Echelon Supply Chain Disruption & Inventory Rebalancing
**Industry**: Automotive & Industrial  
**Tech Stack**: PySpark, Delta Lake UniForm, Apache Iceberg, Lakebase Write-Back  

---

## 1. Executive Business Problem
Geopolitical supplier delays cause stock-outs at regional assembly plants while central warehouses are overstocked.

## 2. Technical Lakehouse Solution
Automated inventory reallocation pipeline that generates transfer orders and writes directly to enterprise ERPs.

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
