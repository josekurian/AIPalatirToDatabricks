# Prototype 08: Telecom Churn Prediction & Proactive Retention Agent
**Industry**: Telecommunications  
**Tech Stack**: Python, XGBoost, Agent Bricks, Mosaic AI, Twilio Webhook  

---

## 1. Executive Business Problem
Customer service representatives fail to identify high-value subscribers at risk of porting their numbers to competitors.

## 2. Technical Lakehouse Solution
Agent Bricks autonomous agent that flags churn risk > 0.85 and dispatches proactive billing discount offers.

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
