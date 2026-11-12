# Databricks Unified Platform (UP) Architecture & Capability Blueprint

The **Databricks Unified Platform (Data Intelligence Platform)** unifies data engineering, streaming, governance, operational applications, semantic AI/BI, and compound AI agents into a single managed architecture built on open standards.

```
flowchart TD
    subgraph UP_LAYER["Databricks Unified Platform Core (UP)"]
        UC["Unity Catalog (UC)<br/>Unified Governance, Lineage, ABAC & Iceberg UniForm"]
        LK["Lakehouse Core (LK)<br/>Photon Vector Engine, Delta Lake & Liquid Clustering"]
        LF["Lakeflow (LF)<br/>Lakeflow Connect (CDC), Lakeflow Pipelines & Jobs"]
        LB["Lakebase / Databricks Apps (LB)<br/>Operational State Store, App Hosting & ACID Write-Back"]
        AB["Agent Bricks / Mosaic AI (AB)<br/>Compound AI Agents, Evaluation & Model Serving"]
        GENIE["Databricks Genie (Genie)<br/>OntoRank Semantic Layer, Metric Views & AI/BI NLP-to-SQL"]
    end

    LF --> LK
    LK --> UC
    UC --> LB
    UC --> AB
    UC --> GENIE
    GENIE <--> AB
    LB <--> LK
```

## Modular Structure
- `/UP`: Unified Platform orchestrator, bundle automation, and deployment harnesses.
- `/Genie`: Databricks Genie spaces, OntoRank semantic weighting, UC Pages, and AI/BI NLP-to-SQL.
- `/LB`: Lakebase / Databricks Apps operational microservices, ACID Delta state stores, and REST write-back.
- `/AB`: Agent Bricks / Mosaic AI compound agents, vector search indexes, and evaluation frameworks.
- `/LF`: Lakeflow Connect (CDC ingestion), Lakeflow Pipelines (DLT), and multi-task Lakeflow DAG orchestration.
- `/LK`: Lakehouse core engine, Delta UniForm with Apache Iceberg v2, Liquid Clustering, and Photon optimization.
- `/UC`: Unity Catalog enterprise governance, dynamic row filters, column masks, ABAC tags, and foreign catalogs.
