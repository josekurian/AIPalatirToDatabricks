# Prototype 17: Pharmaceutical Adverse Drug Reaction (ADR) Pharmacovigilance
**Industry**: Biotech & Pharma  
**Tech Stack**: PySpark, Mosaic AI Agent Framework, MedDRA Ontology, Unity Catalog  

---

## 1. Executive Business Problem
FDA safety reports are buried in unstructured clinical trial notes and doctor survey free-text.

## 2. Technical Lakehouse Solution
Compound LLM agent extracting adverse drug events and linking them to MedDRA ontological concept IDs.

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
