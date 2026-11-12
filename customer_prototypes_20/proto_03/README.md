# Prototype 03: Clinical Trial Patient Stratification & Adverse Event Early Warning
**Industry**: Healthcare & Life Sciences  
**Tech Stack**: PySpark, Unity Catalog ABAC, Delta Live Tables (DLT), HIPAA De-Identification  

---

## 1. Executive Business Problem
Multi-site clinical trial data must comply with HIPAA Safe Harbor and de-identify patient identifiers while tracking drug efficacy.

## 2. Technical Lakehouse Solution
DLT pipeline with dynamic masking, automated tokenization, and Genie NLP space for principal investigators.

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
