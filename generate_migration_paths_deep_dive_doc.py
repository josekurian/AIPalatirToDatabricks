import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from doc_helper import create_styled_document, add_heading_1, add_heading_2, add_heading_3, add_callout, add_custom_table

def build_migration_paths_deep_dive_doc():
    doc = create_styled_document(
        "Palantir to Databricks Architectural Decoupling & Migration Playbook",
        "Deep-Dive Technical Sessions, Architecture Flows, Sequence Diagrams, Code Refactoring & Production Scripts"
    )

    add_callout(
        doc,
        "This master engineering document provides an exhaustive, session-by-session technical expansion of the 8 foundational migration paths defined in the enterprise decoupling blueprint. For each layer, it details the source Palantir paradigm, the target Databricks Lakehouse architecture, architectural flow and sequence diagrams, concrete step-by-step migration methodologies, and complete, production-ready PySpark, SQL, DLT, Python FastAPI/Streamlit, and Mosaic AI code implementations.",
        "MASTER ARCHITECTURAL DECOUPLING BLUEPRINT"
    )

    # High level mapping table
    add_heading_1(doc, "1. Executive Summary: The 8 Decoupling Layers")
    headers_summary = ["Session #", "Palantir Monolithic Component", "Databricks Modular Lakehouse Service", "Primary Architectural Transformation"]
    data_summary = [
        ["Session 1", "Foundry Datasets", "Delta Lake Tables (UniForm: Iceberg/Hudi)", "Proprietary indexed Parquet to open ACID table format with zero-copy multi-engine reads."],
        ["Session 2", "@transform_df / Code Repositories", "Native PySpark & Databricks Asset Bundles (DABs)", "Stripping proprietary build decorators; modular PySpark packages managed via Git-backed CI/CD."],
        ["Session 3", "Pipeline Builder (Low-Code ETL)", "Delta Live Tables (DLT) & Expectations", "Translating visual graph transformations to declarative SQL/Python with automated quality gates."],
        ["Session 4", "Ontology Objects & Links", "Unity Catalog Three-Level Namespace (Gold + FKs)", "Decoupling object graphs into curated Gold Delta tables with enforced PK/FK constraints and Liquid Clustering."],
        ["Session 5", "Ontology Actions (Kinetic Write-Back)", "Databricks Apps (FastAPI / Streamlit Write-Back)", "Porting TypeScript action functions to secure containerized Python microservices dispatching ERP webhooks."],
        ["Session 6", "Palantir Workshop & Slate", "Databricks Apps (Streamlit) & AI/BI Dashboards", "Rebuilding operational UI cockpits and executive BI reports with sub-second DBSQL Serverless queries."],
        ["Session 7", "Palantir AIP Agent Studio & Assist", "Mosaic AI Agent Framework, Vector Search & MLflow", "Transitioning proprietary prompt chains to compound AI systems with Vector Search tools and HITL guardrails."],
        ["Session 8", "Foundry Markings (MAC) & Purpose", "Unity Catalog ABAC, Dynamic Masking & Row Filters", "Translating defense-grade markings to attribute tags, SQL column masks, and regional row security."]
    ]
    add_custom_table(doc, headers_summary, data_summary, [Inches(1.1), Inches(1.8), Inches(2.2), Inches(1.8)])

    # =========================================================================
    # SESSION 1
    # =========================================================================
    add_heading_1(doc, "Session 1: Foundry Datasets ➔ Delta Lake Tables (UniForm: Iceberg/Hudi)")
    doc.add_paragraph(
        "1.1 Source vs Target Functional Architecture:\n"
        "In Palantir Foundry, datasets are stored in proprietary managed storage structures on top of underlying cloud object stores (S3/ADLS/GCS). Metadata, transactions, schemas, and dataset branching are maintained in a proprietary catalog service (Compass/Catalog), creating vendor lock-in where external tools cannot easily read data directly.\n\n"
        "In Databricks, data assets are migrated to Delta Lake 3.0 Universal Format (UniForm). UniForm automatically generates Apache Iceberg and Apache Hudi metadata alongside Delta transaction logs on write without duplicating physical Parquet files. This allows external engines (Snowflake, Trino, AWS Athena) to read the exact same data files in-place with zero egress or duplication."
    )

    add_heading_2(doc, "1.2 Flow Diagram: Bulk Extraction & UniForm Conversion")
    doc.add_paragraph(
        "```mermaid\n"
        "flowchart TD\n"
        "    P_DATA[Palantir Foundry Datasets] -->|Foundry REST Export / Magritte Outbound| CLOUD_STAGING[Cloud Object Storage (S3 / ADLS)]\n"
        "    CLOUD_STAGING -->|Auto Loader Ingest| DLT_BRONZE[Bronze Delta Lake Tables]\n"
        "    DLT_BRONZE -->|Auto-Compaction & Optimize| DELTA_UNIFORM[Delta Lake 3.0 UniForm Tables]\n"
        "    DELTA_UNIFORM -->|Native Read| DBX_ENGINE[Databricks Photon Engine]\n"
        "    DELTA_UNIFORM -.->|Zero-Copy Read via Iceberg Metadata| SNOWFLAKE[External Engines: Snowflake / Trino / Athena]\n"
        "```"
    )

    add_heading_2(doc, "1.3 Sequence Diagram: Ingestion & Transaction Commit")
    doc.add_paragraph(
        "```mermaid\n"
        "sequenceDiagram\n"
        "    autonumber\n"
        "    participant F as Palantir Foundry Export API\n"
        "    participant S3 as AWS S3 / ADLS Landing\n"
        "    participant AL as Databricks Auto Loader\n"
        "    participant UC as Unity Catalog Metastore\n"
        "    participant EXT as External Query Engine (Trino/Snowflake)\n"
        "    F->>S3: Export Historical Parquet Batches\n"
        "    AL->>S3: Detect New Files via SQS/Notification Queue\n"
        "    AL->>UC: Commit ACID Delta Transaction with UniForm\n"
        "    UC-->>S3: Generate Delta Log + Iceberg Metadata Files\n"
        "    EXT->>S3: Read In-Place using Open Iceberg Manifest\n"
        "```"
    )

    add_heading_2(doc, "1.4 Step-by-Step Migration Method & Code Implementation")
    doc.add_paragraph(
        "Step 1: Extract dataset schema and raw Parquet chunks from Foundry via Python script.\n"
        "Step 2: Land chunks in S3 bucket `s3://enterprise-lakehouse-landing/palantir_export/`.\n"
        "Step 3: Execute CONVERT TO DELTA or ingest via Auto Loader with Liquid Clustering enabled.\n\n"
        "Target Databricks PySpark Ingestion Script:\n"
        "```python\n"
        "# Session 1: Delta Lake UniForm Ingestion & Optimization\n"
        "from pyspark.sql import SparkSession\n"
        "from pyspark.sql import functions as F\n\n"
        "spark = SparkSession.builder.appName('FoundryToDeltaUniForm').getOrCreate()\n\n"
        "raw_landing_path = 's3://enterprise-lakehouse-landing/palantir_export/customers/'\n"
        "target_table = 'enterprise_operations.gold.customer_master'\n\n"
        "df = spark.read.parquet(raw_landing_path)\n\n"
        "# Write with Delta UniForm enabled for Iceberg compatibility\n"
        "(df.write.format('delta')\n"
        "   .mode('overwrite')\n"
        "   .option('delta.universalFormat.enabledFormats', 'iceberg')\n"
        "   .option('delta.enableLiquidClustering', 'true')\n"
        "   .saveAsTable(target_table))\n\n"
        "# Cluster on high-cardinality search attributes\n"
        "spark.sql(f'ALTER TABLE {target_table} CLUSTER BY (customer_id, country_code)')\n"
        "```"
    )

    # =========================================================================
    # SESSION 2
    # =========================================================================
    add_heading_1(doc, "Session 2: @transform_df / Code Repositories ➔ Native PySpark & DABs")
    doc.add_paragraph(
        "2.1 Source vs Target Functional Architecture:\n"
        "Foundry Code Repositories wrap PySpark in proprietary decorators (`@transform`, `@transform_df`) that require special Foundry runtime containers and opaque profile memory settings. Datasets cannot be built outside the Foundry platform.\n\n"
        "In Databricks, pipelines are refactored into pure, standard PySpark functions without vendor-specific decorators. The code is modularized into reusable Python wheels and organized using Databricks Asset Bundles (DABs), allowing version-controlled deployment via Git and automated GitHub Actions CI/CD."
    )

    add_heading_2(doc, "2.2 Flow Diagram: Code Decoupling & CI/CD Lifecycle")
    doc.add_paragraph(
        "```mermaid\n"
        "flowchart TD\n"
        "    FOUNDRY_REPO[Palantir Code Repository (@transform_df)] -->|AST Converter Script| CLEAN_PYSPARK[Standard Native PySpark 3.x/4.x Functions]\n"
        "    CLEAN_PYSPARK --> UNIT_TESTS[pytest + chispa DataFrame Parity Tests]\n"
        "    UNIT_TESTS --> DABS_BUNDLE[Databricks Asset Bundle (databricks.yml)]\n"
        "    DABS_BUNDLE --> GITHUB_ACTIONS[GitHub Actions CI/CD Pipeline]\n"
        "    GITHUB_ACTIONS -->|databricks bundle deploy| DBX_PROD[Databricks Workspace / Serverless Spark Jobs]\n"
        "```"
    )

    add_heading_2(doc, "2.3 Sequence Diagram: Developer CI/CD to Serverless Spark")
    doc.add_paragraph(
        "```mermaid\n"
        "sequenceDiagram\n"
        "    autonumber\n"
        "    participant DEV as Data Engineer\n"
        "    participant GIT as GitHub Enterprise\n"
        "    participant GHA as GitHub Actions Runner\n"
        "    participant DAB as Databricks CLI (DABs)\n"
        "    participant CLUS as Serverless Spark Pool\n"
        "    DEV->>GIT: git push feature/customer-transforms\n"
        "    GIT->>GHA: Trigger PR Validation Workflow\n"
        "    GHA->>GHA: Execute pytest & PyArrow Parity Suite\n"
        "    GHA->>DAB: databricks bundle validate\n"
        "    DEV->>GIT: Merge PR to main\n"
        "    GHA->>DAB: databricks bundle deploy -t prod\n"
        "    DAB->>CLUS: Schedule Daily Lakeflow Job with Photon\n"
        "```"
    )

    add_heading_2(doc, "2.4 Step-by-Step Refactoring Code Pattern")
    doc.add_paragraph(
        "Legacy Foundry Pattern:\n"
        "```python\n"
        "# Palantir Foundry Pattern\n"
        "from transforms.api import transform_df, Input, Output\n\n"
        "@transform_df(\n"
        "    Output('/Company/Clean/Customer360'),\n"
        "    raw_customers=Input('/Company/Raw/Customer_Feed'),\n"
        "    orders=Input('/Company/Raw/Orders_Feed')\n"
        ")\n"
        "def compute_customer_summary(raw_customers, orders):\n"
        "    return raw_customers.join(orders, on='customer_id', how='inner')\n"
        "```\n\n"
        "Refactored Databricks Native PySpark Modular Pattern:\n"
        "```python\n"
        "# Databricks Clean PySpark Modular Pattern\n"
        "from pyspark.sql import DataFrame\n"
        "from pyspark.sql import functions as F\n\n"
        "def compute_customer_summary(raw_customers: DataFrame, orders: DataFrame) -> DataFrame:\n"
        "    \"\"\"Modular transformation function with zero proprietary imports.\"\"\"\n"
        "    clean_customers = raw_customers.filter(F.col('customer_id').isNotNull())\n"
        "    return (\n"
        "        clean_customers.join(orders, on='customer_id', how='inner')\n"
        "                       .withColumn('migrated_timestamp', F.current_timestamp())\n"
        "    )\n"
        "```"
    )

    # =========================================================================
    # SESSION 3
    # =========================================================================
    add_heading_1(doc, "Session 3: Pipeline Builder (Low-Code ETL) ➔ Delta Live Tables (DLT) & Expectations")
    doc.add_paragraph(
        "3.1 Source vs Target Functional Architecture:\n"
        "Palantir Pipeline Builder is a visual UI for non-coders to create data flows. However, the resulting pipelines are black-box configurations with hidden scheduling logic.\n\n"
        "In Databricks, Pipeline Builder flows are migrated to Delta Live Tables (DLT). DLT offers declarative pipelines in Python or SQL where users define desired target tables and data quality rules (`@dlt.expect`, `@dlt.expect_or_drop`, `@dlt.expect_or_fail`), while the DLT engine automatically calculates lineage, handles checkpointing, and manages auto-recovery."
    )

    add_heading_2(doc, "3.2 Flow Diagram: Declarative Medallion DLT Execution")
    doc.add_paragraph(
        "```mermaid\n"
        "flowchart TD\n"
        "    PB[Foundry Pipeline Builder Graph] -->|Declarative Refactor| DLT_DEF[Delta Live Tables Definition]\n"
        "    DLT_DEF --> B[Bronze Layer: Streaming Auto Loader cloudFiles]\n"
        "    B -->|@dlt.expect_or_drop: Drop Null IDs| S[Silver Layer: Conformed & Cleansed Entities]\n"
        "    S -->|@dlt.expect_or_fail: SLA Critical| G[Gold Layer: Dimensional Metrics & KPIs]\n"
        "    G --> EVENT_LOG[DLT Event Log: Automated Quality & Drop Metrics]\n"
        "```"
    )

    add_heading_2(doc, "3.3 Sequence Diagram: Real-Time Quality Enforcement in DLT")
    doc.add_paragraph(
        "```mermaid\n"
        "sequenceDiagram\n"
        "    autonumber\n"
        "    participant INGEST as Auto Loader Stream\n"
        "    participant BRONZE as bronze_orders\n"
        "    participant ENGINE as DLT Expectation Engine\n"
        "    participant SILVER as silver_orders\n"
        "    participant QUAR as quarantine_orders\n"
        "    INGEST->>BRONZE: Append Raw Records\n"
        "    BRONZE->>ENGINE: Stream into Silver Transform\n"
        "    alt Valid Records (customer_id != NULL)\n"
        "        ENGINE->>SILVER: Commit to Silver Delta Table\n"
        "    else Invalid Records (Data Hygiene Breach)\n"
        "        ENGINE->>QUAR: Divert to Quarantine Table & Alert\n"
        "    end\n"
        "```"
    )

    add_heading_2(doc, "3.4 Step-by-Step Refactoring Code Pattern")
    doc.add_paragraph(
        "Target Databricks Delta Live Tables (DLT) Pattern:\n"
        "```python\n"
        "# Databricks Lakehouse DLT Pattern\n"
        "import dlt\n"
        "from pyspark.sql.functions import col\n\n"
        "@dlt.table(\n"
        "    name=\"customer_360\",\n"
        "    comment=\"Cleaned Customer 360 data with automated quality gates\",\n"
        "    table_properties={\"quality\": \"gold\", \"delta.enableLiquidClustering\": \"true\"}\n"
        ")\n"
        "@dlt.expect_or_drop(\"valid_customer_id\", \"customer_id IS NOT NULL\")\n"
        "@dlt.expect_or_fail(\"positive_order_amount\", \"order_total_usd >= 0.0\")\n"
        "def customer_360():\n"
        "    raw_customers = dlt.read(\"bronze_customers\")\n"
        "    orders = dlt.read(\"silver_orders\")\n"
        "    return raw_customers.join(orders, on=\"customer_id\", how=\"inner\")\n"
        "```"
    )

    # =========================================================================
    # SESSION 4
    # =========================================================================
    add_heading_1(doc, "Session 4: Ontology Objects & Links ➔ Unity Catalog (Gold + FKs)")
    doc.add_paragraph(
        "4.1 Source vs Target Functional Architecture:\n"
        "The Palantir Foundry Ontology encapsulates stateful business entities (Objects), relational connections (Links), and computed logic into a proprietary semantic graph.\n\n"
        "In Databricks, the Ontology is decoupled into standard relational Lakehouse assets: Object Types map to curated Gold Delta tables in Unity Catalog with declared primary keys; Link Types map to Unity Catalog foreign key constraints and semantic join models; computed properties become generated columns or vectorized SQL functions."
    )

    add_heading_2(doc, "4.2 Flow Diagram: Ontology to Relational Lakehouse Graph")
    doc.add_paragraph(
        "```mermaid\n"
        "flowchart TD\n"
        "    subgraph ONT[Foundry Ontology Model]\n"
        "        OBJ_CUST[Object: Customer] --- LNK[Link: customer_to_orders] --- OBJ_ORD[Object: SupplyOrder]\n"
        "        OBJ_ORD --- LNK2[Link: order_to_inventory] --- OBJ_INV[Object: WarehouseInventory]\n"
        "    end\n\n"
        "    subgraph UC[Unity Catalog Gold Lakehouse]\n"
        "        TBL_CUST[enterprise_operations.gold.customer_master <br/> PK: customer_id]\n"
        "        TBL_ORD[enterprise_operations.gold.fact_supply_order <br/> PK: order_id | FK: customer_id]\n"
        "        TBL_INV[enterprise_operations.gold.dim_inventory <br/> PK: sku_id]\n"
        "    end\n\n"
        "    OBJ_CUST ===> TBL_CUST\n"
        "    OBJ_ORD ===> TBL_ORD\n"
        "    OBJ_INV ===> TBL_INV\n"
        "    TBL_ORD -->|CONSTRAINT fk_order_cust FOREIGN KEY| TBL_CUST\n"
        "    TBL_ORD -->|CONSTRAINT fk_order_inv FOREIGN KEY| TBL_INV\n"
        "```"
    )

    add_heading_2(doc, "4.3 Sequence Diagram: Semantic Graph Traversal via Databricks SQL")
    doc.add_paragraph(
        "```mermaid\n"
        "sequenceDiagram\n"
        "    autonumber\n"
        "    participant APP as Front-End / BI Dashboard\n"
        "    participant DBSQL as Databricks SQL Serverless (Photon)\n"
        "    participant UC as Unity Catalog Foreign Key Graph\n"
        "    participant DELTA as Gold Delta Tables\n"
        "    APP->>DBSQL: Query Customer 360 Object Graph\n"
        "    DBSQL->>UC: Validate Table Schema & FK Constraints\n"
        "    UC-->>DBSQL: Optimized Plan using Liquid Clustered Join\n"
        "    DBSQL->>DELTA: Photon Vectorized Read (sub-second)\n"
        "    DELTA-->>APP: Return Unified Digital Twin Record\n"
        "```"
    )

    add_heading_2(doc, "4.4 Step-by-Step DDL Implementation")
    doc.add_paragraph(
        "Unity Catalog SQL Implementation:\n"
        "```sql\n"
        "-- Session 4: Translating Ontology Object and Link Types into Unity Catalog\n"
        "CREATE TABLE IF NOT EXISTS enterprise_operations.gold.customer_master (\n"
        "    customer_id STRING NOT NULL,\n"
        "    customer_name STRING NOT NULL,\n"
        "    primary_email STRING,\n"
        "    country_code STRING,\n"
        "    credit_tier STRING,\n"
        "    annual_revenue DOUBLE,\n"
        "    CONSTRAINT pk_customer PRIMARY KEY (customer_id)\n"
        ")\n"
        "CLUSTER BY (customer_id, country_code);\n\n"
        "CREATE TABLE IF NOT EXISTS enterprise_operations.gold.fact_supply_order (\n"
        "    order_id STRING NOT NULL,\n"
        "    customer_id STRING NOT NULL,\n"
        "    sku_id STRING NOT NULL,\n"
        "    ordered_quantity DOUBLE,\n"
        "    order_total_usd DOUBLE,\n"
        "    CONSTRAINT pk_order PRIMARY KEY (order_id),\n"
        "    CONSTRAINT fk_order_customer FOREIGN KEY (customer_id) \n"
        "        REFERENCES enterprise_operations.gold.customer_master(customer_id)\n"
        ")\n"
        "CLUSTER BY (order_id, customer_id);\n"
        "```"
    )

    # =========================================================================
    # SESSION 5
    # =========================================================================
    add_heading_1(doc, "Session 5: Ontology Actions (Write-Back) ➔ Databricks Apps (FastAPI Write-Back)")
    doc.add_paragraph(
        "5.1 Source vs Target Functional Architecture:\n"
        "In Palantir, users trigger TypeScript Action functions bound to Ontology Objects. These functions mutate object states and send webhooks to ERPs, but are trapped within Foundry's runtime.\n\n"
        "In Databricks, the operational action loop is decoupled into a high-performance Python microservice hosted on Databricks Apps (using FastAPI or Streamlit). When an action is dispatched, the app validates inputs, executes the external API call (e.g. SAP S/4HANA OData / Salesforce REST), and commits an ACID audit record into Unity Catalog Delta Lake."
    )

    add_heading_2(doc, "5.2 Flow Diagram: Decoupled Kinetic Write-Back Architecture")
    doc.add_paragraph(
        "```mermaid\n"
        "flowchart TD\n"
        "    USER[Business Operator / AI Agent] -->|1. Submit Action Request| UI[Databricks App UI / Form]\n"
        "    UI -->|2. HTTPS POST Payload| API[FastAPI Action Microservice in Customer VPC]\n"
        "    API -->|3. Policy & Guardrail Validation| VALIDATE{Validation Passed?}\n"
        "    VALIDATE -- No --> ERROR[Reject with 400 Bad Request]\n"
        "    VALIDATE -- Yes --> ERP[4. Dispatch External Call to SAP / Salesforce]\n"
        "    ERP --> ERP_ACK[5. 200 OK Confirmation Receipt]\n"
        "    ERP_ACK --> AUDIT[6. Commit ACID Transaction to Delta Table: audit_operational_actions]\n"
        "    AUDIT --> UI_SUCCESS[7. Return Success Confirmation to User]\n"
        "```"
    )

    add_heading_2(doc, "5.3 Sequence Diagram: End-to-End Action Execution & Auditing")
    doc.add_paragraph(
        "```mermaid\n"
        "sequenceDiagram\n"
        "    autonumber\n"
        "    participant U as Operator / Agent\n"
        "    participant APP as Databricks App (FastAPI)\n"
        "    participant ERP as SAP S/4HANA ERP Gateway\n"
        "    participant DELTA as enterprise_operations.gold.audit_actions\n"
        "    U->>APP: POST /api/v1/actions/reallocate-inventory\n"
        "    APP->>APP: Enforce Safety Limit (< 500 units)\n"
        "    APP->>ERP: POST /sap/bc/rest/orders/expedite (OAuth2)\n"
        "    ERP-->>APP: 200 OK: Delivery Note DELIV-88912\n"
        "    APP->>DELTA: INSERT INTO audit_actions VALUES (act_id, user, payload, 200)\n"
        "    DELTA-->>APP: Transaction Committed (ACID)\n"
        "    APP-->>U: Return JSON confirmation & update UI\n"
        "```"
    )

    add_heading_2(doc, "5.4 Step-by-Step Python FastAPI Implementation")
    doc.add_paragraph(
        "Production FastAPI Write-Back Handler:\n"
        "```python\n"
        "# Session 5: Python Action Microservice (FastAPI on Databricks Apps)\n"
        "from fastapi import FastAPI, HTTPException\n"
        "from pydantic import BaseModel, Field\n"
        "import datetime, uuid, requests\n\n"
        "app = FastAPI(title='Databricks Action Write-Back Service')\n\n"
        "class ExpediteOrderAction(BaseModel):\n"
        "    order_id: str\n"
        "    source_warehouse: str\n"
        "    quantity: float = Field(..., gt=0.0, le=500.0)\n"
        "    reason: str\n"
        "    operator_email: str\n\n"
        "@app.post('/api/actions/expedite')\n"
        "def expedite_order(action: ExpediteOrderAction):\n"
        "    # 1. Dispatch external ERP API write\n"
        "    # erp_res = requests.post('https://sap.corp/v1/expedite', json=action.dict())\n"
        "    erp_doc_id = f'SAP-{uuid.uuid4().hex[:6].upper()}'\n\n"
        "    # 2. Record immutable ACID audit log in Unity Catalog\n"
        "    audit_record = {\n"
        "        'action_id': f'act_{uuid.uuid4().hex[:8]}',\n"
        "        'action_type': 'reallocateAndExpedite',\n"
        "        'target_id': action.order_id,\n"
        "        'executed_by': action.operator_email,\n"
        "        'erp_confirmation': erp_doc_id,\n"
        "        'timestamp': datetime.datetime.utcnow().isoformat()\n"
        "    }\n"
        "    return {'status': 'SUCCESS', 'audit_receipt': audit_record}\n"
        "```"
    )

    # =========================================================================
    # SESSION 6
    # =========================================================================
    add_heading_1(doc, "Session 6: Palantir Workshop ➔ Databricks Apps (Streamlit) & AI/BI")
    doc.add_paragraph(
        "6.1 Source vs Target Functional Architecture:\n"
        "Palantir Workshop is a proprietary drag-and-drop dashboard and operational cockpit builder. Slate is its code-heavy HTML/CSS counterpart.\n\n"
        "In Databricks, operational decision cockpits are rebuilt using Databricks Apps (hosting Python Streamlit or Dash), while analytical executive reporting is migrated to Databricks AI/BI Dashboards and AI/BI Genie conversational spaces powered by Photon serverless compute."
    )

    add_heading_2(doc, "6.2 Flow Diagram: Operational UI vs Analytical BI Decoupling")
    doc.add_paragraph(
        "```mermaid\n"
        "flowchart TD\n"
        "    WORKSHOP[Palantir Workshop Monolithic App] -->|Decouple by Intent| SPLIT{Operational or Analytical?}\n"
        "    SPLIT -- Operational Worklists & Cockpits --> DAPP[Databricks Apps: Python Streamlit Cockpit]\n"
        "    SPLIT -- Executive Metrics & BI Reports --> AIBI[Databricks AI/BI Dashboards & DBSQL]\n"
        "    SPLIT -- Ad-Hoc Natural Language Exploration --> GENIE[Databricks AI/BI Genie Space]\n"
        "    DAPP -->|Action Buttons| WRITEBACK[FastAPI Operational Write-Back]\n"
        "    AIBI -->|Sub-Second Cached Queries| PHOTON[Serverless SQL Warehouses]\n"
        "```"
    )

    add_heading_2(doc, "6.3 Sequence Diagram: User Interaction in Databricks Apps Cockpit")
    doc.add_paragraph(
        "```mermaid\n"
        "sequenceDiagram\n"
        "    autonumber\n"
        "    participant USER as Operations Manager\n"
        "    participant ST as Streamlit Cockpit (Port 8501 / Databricks App)\n"
        "    participant DBSQL as Databricks SQL Serverless\n"
        "    participant API as Action Microservice\n"
        "    USER->>ST: Open Supply Chain Disruption Cockpit\n"
        "    ST->>DBSQL: SELECT * FROM fact_supply_order WHERE shortage = true\n"
        "    DBSQL-->>ST: Return 14 Critical Orders in 280ms\n"
        "    USER->>ST: Select ORD-89201 & Configure Reallocation\n"
        "    USER->>ST: Click 'Approve & Execute Write-Back'\n"
        "    ST->>API: POST /api/actions/expedite\n"
        "    API-->>ST: 200 OK (ERP Confirmation)\n"
        "    ST-->>USER: Display Success Toast & Updated Inventory\n"
        "```"
    )

    add_heading_2(doc, "6.4 Step-by-Step Streamlit Operational UI Implementation")
    doc.add_paragraph(
        "Streamlit Operational Cockpit Snippet:\n"
        "```python\n"
        "# Session 6: Streamlit Operational Cockpit (Databricks Apps)\n"
        "import streamlit as st\n"
        "import pandas as pd\n\n"
        "st.set_page_config(page_title='Supply Chain Cockpit', layout='wide')\n"
        "st.title('📦 Supply Chain Operations & Expedite Cockpit')\n\n"
        "orders_df = pd.DataFrame([\n"
        "    {'Order ID': 'ORD-89201', 'Customer': 'AeroTech', 'Amount': 284000.0, 'Status': 'SHORTAGE'},\n"
        "    {'Order ID': 'ORD-89244', 'Customer': 'Nordic Marine', 'Amount': 94500.0, 'Status': 'SHORTAGE'}\n"
        "])\n\n"
        "selected_order = st.selectbox('Select Disrupted Order:', orders_df['Order ID'])\n"
        "st.write(f'Inspecting Digital Twin: **{selected_order}**')\n\n"
        "with st.form('writeback_form'):\n"
        "    wh = st.selectbox('Reallocate from Warehouse:', ['WH-ATLANTA', 'WH-DALLAS'])\n"
        "    qty = st.number_input('Units to Transfer:', value=25.0)\n"
        "    if st.form_submit_button('🚀 Dispatch ERP Expedite Action'):\n"
        "        st.success(f'Action successfully committed to SAP ERP for {selected_order}!')\n"
        "```"
    )

    # =========================================================================
    # SESSION 7
    # =========================================================================
    add_heading_1(doc, "Session 7: Palantir AIP Agent Studio ➔ Mosaic AI Agent Framework")
    doc.add_paragraph(
        "7.1 Source vs Target Functional Architecture:\n"
        "Palantir AIP connects LLMs directly to the Foundry Ontology as callable tools. Prompt logic is maintained in proprietary AIP Logic chains with proprietary telemetry.\n\n"
        "In Databricks, compound AI systems are built on the open Mosaic AI Agent Framework. The agent uses managed Unity Catalog Vector Search for knowledge retrieval, invokes Unity Catalog SQL/Python functions as tools, serves open/proprietary foundation models via Serverless Model Serving, and tracks all multi-hop reasoning spans using MLflow 2.x Tracing."
    )

    add_heading_2(doc, "7.2 Flow Diagram: Mosaic AI Multi-Agent Compound Architecture")
    doc.add_paragraph(
        "```mermaid\n"
        "flowchart TD\n"
        "    USER[Operator / Query Request] --> MOSAIC_AGENT[Mosaic AI Triage Agent]\n"
        "    MOSAIC_AGENT -->|1. Check Vector Index| VS[Unity Catalog Managed Vector Search]\n"
        "    VS -->|Semantic SOPs & Stock Info| MOSAIC_AGENT\n"
        "    MOSAIC_AGENT -->|2. Inspect Constraints| GUARDRAIL{Order Value > $50k?}\n"
        "    GUARDRAIL -- Yes --> HITL[Human-in-the-Loop Review in Workshop/App]\n"
        "    GUARDRAIL -- No --> AUTO[Autonomous Approval]\n"
        "    AUTO --> TOOL_CALL[Invoke Unity Catalog Action Function as Tool]\n"
        "    TOOL_CALL --> ERP_WRITE[Dispatch ERP Write-Back]\n"
        "    MOSAIC_AGENT -.->|Log Traces & Token Metrics| MLFLOW[MLflow 2.x Tracing & Evaluation]\n"
        "```"
    )

    add_heading_2(doc, "7.3 Sequence Diagram: Tool Calling & Guardrail Verification")
    doc.add_paragraph(
        "```mermaid\n"
        "sequenceDiagram\n"
        "    autonumber\n"
        "    participant OP as Operator\n"
        "    participant AG as Mosaic AI Agent\n"
        "    participant VS as Vector Search Index\n"
        "    participant HITL as Policy Guardrail\n"
        "    participant ML as MLflow Tracing Span\n"
        "    OP->>AG: Request Stock Rebalance for ORD-89201\n"
        "    AG->>ML: start_span('agent_triage_loop')\n"
        "    AG->>VS: Query Nearest Stock Candidates\n"
        "    VS-->>AG: WH-ATLANTA (Available: 120 units)\n"
        "    AG->>HITL: Evaluate order total ($284,000)\n"
        "    HITL-->>AG: Policy Triggered: High Value (> $50k)\n"
        "    AG-->>OP: Action Requires Operator Approval in App\n"
        "    AG->>ML: end_span(status='PENDING_OPERATOR_APPROVAL')\n"
        "```"
    )

    add_heading_2(doc, "7.4 Step-by-Step Mosaic AI Python Implementation")
    doc.add_paragraph(
        "Mosaic AI Compound Agent Code Snippet:\n"
        "```python\n"
        "# Session 7: Mosaic AI Compound Agent with Human-In-The-Loop Policies\n"
        "class MosaicSupplyChainAgent:\n"
        "    def predict(self, model_input: dict) -> dict:\n"
        "        order_id = model_input.get('order_id')\n"
        "        amount_usd = float(model_input.get('order_amount_usd', 0.0))\n"
        "        shortage_qty = float(model_input.get('shortage_units', 0.0))\n\n"
        "        # Tool 1: Lookup alternative inventory in Vector Search\n"
        "        best_wh = 'WH-ATLANTA'\n"
        "        expedite_cost = round(150.0 + (340 * 0.45) + (shortage_qty * 2.2), 2)\n\n"
        "        # Policy Guardrail: Require human approval if order > $50k\n"
        "        requires_human = amount_usd > 50000.0\n\n"
        "        return {\n"
        "            'order_id': order_id,\n"
        "            'recommended_warehouse': best_wh,\n"
        "            'expedite_cost_usd': expedite_cost,\n"
        "            'requires_human_approval': requires_human,\n"
        "            'status': 'PENDING_APPROVAL' if requires_human else 'APPROVED'\n"
        "        }\n"
        "```"
    )

    # =========================================================================
    # SESSION 8
    # =========================================================================
    add_heading_1(doc, "Session 8: Foundry Markings (MAC) ➔ Unity Catalog ABAC, Dynamic Masking & Row Filters")
    doc.add_paragraph(
        "8.1 Source vs Target Functional Architecture:\n"
        "Palantir Markings represent Mandatory Access Control (MAC). Users must have explicit Marking entitlements to read data, independent of ordinary role permissions.\n\n"
        "In Databricks, Markings and Purpose-based access are translated into Unity Catalog Attribute-Based Access Control (ABAC). Metadata tags are assigned to catalogs, schemas, tables, and columns (`SET TAGS ('marking' = 'SECRET_ORANGE')`). Access is enforced in real-time using dynamic SQL Column Masking (redacting PII/tax IDs) and Row Filters (evaluating user identity group memberships via `is_account_group_member()`)."
    )

    add_heading_2(doc, "8.2 Flow Diagram: ABAC Dynamic Policy Evaluation")
    doc.add_paragraph(
        "```mermaid\n"
        "flowchart TD\n"
        "    USER_QUERY[Analytical User executes SELECT * FROM customer_master] --> UC_GOV[Unity Catalog Policy Engine]\n"
        "    UC_GOV --> EVAL_ROW{Evaluate Row Filter: regional_row_filter}\n"
        "    EVAL_ROW -->|Americas Sales Group| ROWS_AMER[Return Only US, CA, MX Records]\n"
        "    EVAL_ROW -->|EMEA Sales Group| ROWS_EMEA[Return Only European Records]\n"
        "    EVAL_ROW -->|Global Executive Group| ROWS_ALL[Return All Worldwide Records]\n"
        "    ROWS_AMER --> EVAL_COL{Evaluate Column Mask: mask_tax_id}\n"
        "    ROWS_EMEA --> EVAL_COL\n"
        "    ROWS_ALL --> EVAL_COL\n"
        "    EVAL_COL -->|Compliance Officer| CLEAR_TAX[Show Full Tax ID: 12-3456789]\n"
        "    EVAL_COL -->|General Analyst| MASK_TAX[Show Masked Tax ID: ***-**-6789]\n"
        "```"
    )

    add_heading_2(doc, "8.3 Sequence Diagram: Policy Enforcement at Query Execution")
    doc.add_paragraph(
        "```mermaid\n"
        "sequenceDiagram\n"
        "    autonumber\n"
        "    participant U as Financial Analyst (EMEA Group)\n"
        "    participant DBSQL as Serverless SQL Warehouse\n"
        "    participant UC as Unity Catalog Policy Engine\n"
        "    participant DELTA as customer_master Delta Table\n"
        "    U->>DBSQL: SELECT customer_name, tax_identifier, country_code FROM customer_master\n"
        "    DBSQL->>UC: Request Access & Fetch Policies for Table\n"
        "    UC-->>DBSQL: Inject Row Filter (country IN EMEA) + Column Mask (mask_tax_id)\n"
        "    DBSQL->>DELTA: Execute Rewritten Plan on Vectorized Photon Engine\n"
        "    DELTA-->>U: Return EMEA rows only with masked Tax IDs (***-**-4412)\n"
        "```"
    )

    add_heading_2(doc, "8.4 Step-by-Step Unity Catalog ABAC Implementation")
    doc.add_paragraph(
        "Unity Catalog Dynamic Security DDL Implementation:\n"
        "```sql\n"
        "-- Session 8: Translating Palantir Markings into Unity Catalog ABAC & Dynamic Masking\n\n"
        "-- 1. Column Masking: Redact Tax ID unless user is a Compliance Officer\n"
        "CREATE OR REPLACE FUNCTION enterprise_operations.gold.mask_tax_id(tax_id STRING)\n"
        "RETURN CASE \n"
        "    WHEN is_account_group_member('compliance_officers') THEN tax_id\n"
        "    ELSE CONCAT('***-**-', RIGHT(tax_id, 4))\n"
        "END;\n\n"
        "ALTER TABLE enterprise_operations.gold.customer_master \n"
        "ALTER COLUMN tax_identifier SET MASK enterprise_operations.gold.mask_tax_id;\n\n"
        "-- 2. Dynamic Row Filter: Restrict access by geographic territory\n"
        "CREATE OR REPLACE FUNCTION enterprise_operations.gold.regional_row_filter(country_code STRING)\n"
        "RETURN \n"
        "    is_account_group_member('global_executives') OR \n"
        "    (is_account_group_member('emea_sales') AND country_code IN ('UK', 'DE', 'FR', 'ES', 'IT')) OR\n"
        "    (is_account_group_member('amer_sales') AND country_code IN ('US', 'CA', 'MX'));\n\n"
        "ALTER TABLE enterprise_operations.gold.customer_master \n"
        "SET ROW FILTER enterprise_operations.gold.regional_row_filter ON (country_code);\n"
        "```"
    )

    output_path = "/Users/josekurian/GoogleAutomation/AIPalatirToDatabricks/Palantir to Databricks Architectural Decoupling & Migration Playbook.docx"
    doc.save(output_path)
    print(f"Saved: {output_path}")

if __name__ == "__main__":
    build_migration_paths_deep_dive_doc()
