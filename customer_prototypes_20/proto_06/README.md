# Prototype 06: Automated Anti-Money Laundering (AML) & Graph Ring Detection
**Industry**: FinTech & Payments  
**Tech Stack**: PySpark GraphFrames, Java Network Engine, Lakebase State Store  

---

## 1. Executive Business Problem
Syndicate money-laundering rings cycle stolen funds across mule accounts to defeat relational Oracle queries.

## 2. Technical Lakehouse Solution
Graph analytics identifying cyclic loops and strongly connected components with ACID write-back into Lakebase.

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
