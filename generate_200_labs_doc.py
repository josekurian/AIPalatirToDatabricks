import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from doc_helper import create_styled_document, add_heading_1, add_heading_2, add_heading_3, add_callout, add_custom_table

def build_200_labs_document():
    doc = create_styled_document(
        "Palantir to Databricks Migration: 200 Hands-On Technical Labs Guide",
        "Comprehensive Curriculum: Apache Spark, Delta Live Tables, Unity Catalog, Python, SQL, MLflow & Operational Decoupling"
    )

    add_callout(
        doc,
        "This master handbook provides 200 production-grade, step-by-step hands-on labs designed for Data Architects, Migration Engineers, and Databricks Practitioners. It covers the complete technical refactoring lifecycle: converting proprietary Palantir Foundry patterns (@transform, @transform_df, Pipeline Builder, Magritte, Ontology, Actions, Workshop) into modern, open Databricks Lakehouse equivalents (PySpark, DLT, Unity Catalog, Databricks Apps, Mosaic AI, MLflow).",
        "ENTERPRISE LABS CURRICULUM OVERVIEW"
    )

    # Section 1: Executive Curriculum Architecture
    add_heading_1(doc, "1. Curriculum Architecture & Skill Set Taxonomy")
    doc.add_paragraph(
        "The 200 labs are divided into 10 cohesive technical modules spanning the foundational to advanced enterprise patterns. Each lab specifies its objective, architectural context, migration mapping, step-by-step instructions, and expected output."
    )

    headers_mod = ["Module", "Lab Range", "Core Focus & Technology Stack", "Key Migration Mapping"]
    data_mod = [
        ["Module 1", "Labs 001 - 025", "Foundry @transform & @transform_df to Native PySpark Refactoring", "Stripping Foundry decorators, refactoring Input/Output locators to Spark DataFrames"],
        ["Module 2", "Labs 026 - 050", "Delta Live Tables (DLT) & Declarative Pipeline Engineering", "Migrating visual Pipeline Builder & multi-stage builds into DLT with data quality expectations"],
        ["Module 3", "Labs 051 - 075", "Decoupling Palantir Ontology to Unity Catalog Delta Lake", "Mapping Object Types to Gold Delta tables with Liquid Clustering and foreign key constraints"],
        ["Module 4", "Labs 076 - 100", "Palantir Kinetic Actions & Write-Backs to Databricks Apps", "Porting TypeScript Action functions to Python FastAPI / Streamlit with ACID Delta audit logging"],
        ["Module 5", "Labs 101 - 125", "Enterprise Security: Palantir Markings to Unity Catalog ABAC", "Translating Mandatory Access Control (MAC) Markings to SQL Row Filters and dynamic Column Masks"],
        ["Module 6", "Labs 126 - 150", "Enterprise SQL Engineering, DBSQL Photon & AI/BI Migration", "Converting Contour cohorts and Quiver time-series to DBSQL Serverless, Dashboards & Genie"],
        ["Module 7", "Labs 151 - 175", "Mosaic AI & MLflow: Migrating Palantir AIP to Compound AI", "Porting AIP Agent Studio to Mosaic AI Agent Framework, Vector Search & Model Serving"],
        ["Module 8", "Labs 176 - 190", "Automated Data Reconciliation & Dual-Run Parity Suites", "Bitwise checksums, Great Expectations, row-level hashing, and schema drift detection"],
        ["Module 9", "Labs 191 - 195", "Orchestration & CI/CD: Foundry Builds to Lakeflow & DABs", "Databricks Asset Bundles (DABs), multi-task Lakeflow DAGs, and Git-backed workflows"],
        ["Module 10", "Labs 196 - 200", "Production Cutover, Zero-Downtime Migration & FinOps", "Parallel run cutover execution, tenant decommissioning, and FinOps System Tables"]
    ]
    add_custom_table(doc, headers_mod, data_mod, [Inches(1.1), Inches(1.1), Inches(2.5), Inches(1.8)])

    # Section 2: Code & Pipeline Conversion Deep-Dive
    add_heading_1(doc, "2. Code & Pipeline Conversion: Step-by-Step Refactoring")
    doc.add_paragraph(
        "Palantir Foundry uses proprietary Python decorators (`@transform`, `@transform_df`) and build abstractions. In Databricks, these are refactored into native PySpark, Delta Live Tables (DLT), or Databricks Asset Bundles (DABs)."
    )

    add_heading_2(doc, "2.1 PySpark Refactoring Pattern")
    doc.add_paragraph(
        "Foundry Pattern:\n"
        "```python\n"
        "# Palantir Foundry Pattern\n"
        "from transforms.api import transform_df, Input, Output\n\n"
        "@transform_df(\n"
        "    Output(\"/Company/Clean/Customer360\"),\n"
        "    raw_customers=Input(\"/Company/Raw/Customer_Feed\"),\n"
        "    orders=Input(\"/Company/Raw/Orders_Feed\")\n"
        ")\n"
        "def compute_customer_summary(raw_customers, orders):\n"
        "    return raw_customers.join(orders, on='customer_id', how='inner')\n"
        "```\n\n"
        "Target Databricks Delta Live Tables (DLT) Pattern:\n"
        "```python\n"
        "# Databricks Lakehouse DLT Pattern\n"
        "import dlt\n"
        "from pyspark.sql.functions import col\n\n"
        "@dlt.table(\n"
        "    name=\"customer_360\",\n"
        "    comment=\"Cleaned Customer 360 data\",\n"
        "    table_properties={\"quality\": \"gold\"}\n"
        ")\n"
        "@dlt.expect_or_drop(\"valid_customer_id\", \"customer_id IS NOT NULL\")\n"
        "def customer_360():\n"
        "    raw_customers = dlt.read(\"bronze_customers\")\n"
        "    orders = dlt.read(\"silver_orders\")\n"
        "    return raw_customers.join(orders, on=\"customer_id\", how=\"inner\")\n"
        "```"
    )

    add_heading_2(doc, "2.2 Refactoring Palantir Ontology & Operational Actions")
    doc.add_paragraph(
        "Rebuilding the Palantir operational write-back loop in Databricks requires decoupling the semantic storage from the interactive action service:\n"
        "• Data State: Store the entity digital twin as an ACID Delta Lake table in Unity Catalog (`gold.enterprise.customer_master`).\n"
        "• Read Queries: Serve real-time data to UI applications via Databricks SQL Serverless or Unity Catalog REST APIs.\n"
        "• Action Execution (Write-Back): Host a Databricks App (FastAPI / Streamlit) running within the customer VPC. When a user or agent clicks 'Approve Procurement' or 'Schedule Maintenance', the App executes a Python handler that updates the target ERP via REST/ODBC and records the state change into a Delta Lake audit table with ACID transactional consistency."
    )

    add_heading_2(doc, "2.3 Migration Risk Matrix & Mitigation Strategies")
    headers_risk = ["Identified Risk Category", "Potential Business Impact", "Severity", "Proactive Mitigation Strategy"]
    data_risk = [
        ["Data Drift & Discrepancies", "Inconsistent reports between Foundry and Databricks during cutover", "High", "Implement automated daily Bitwise/checksum row-level reconciliation pipelines using open-source Great Expectations or DLT expectations."],
        ["Proprietary Dependency Lock-In", "Difficulty extracting custom transforms locked in proprietary Palantir libraries", "Medium", "Identify proprietary Foundry helper functions early in Discovery; develop standard PySpark equivalent utility libraries in Databricks."],
        ["End-User Operational Friction", "Business operators accustomed to Workshop UI push back against new interfaces", "High", "Involve business operational champions in co-designing Databricks Apps (Streamlit) early; replicate exact UI layouts and color coding to ensure user familiarity."],
        ["Security & Entitlement Gaps", "Data exposed improperly due to misconfigured Unity Catalog permissions", "Critical", "Automate script-based translation of Foundry Marking entitlements into Unity Catalog ABAC tag assignments; validate with InfoSec before production cutover."],
        ["Extended Parallel Run Costs", "Paying for both Palantir enterprise licenses and Databricks compute simultaneously", "Medium", "Establish strict milestone deadlines and timebox dual-run testing to a maximum of 30 days per operational domain."]
    ]
    add_custom_table(doc, headers_risk, data_risk, [Inches(1.5), Inches(1.8), Inches(0.9), Inches(2.3)])

    # Detailed specifications for the 200 Hands-on Labs
    add_heading_1(doc, "3. The 200 Hands-On Technical Labs (Step-by-Step Instructions)")

    # Define the 10 modules with their 200 labs
    modules_labs_data = [
        ("Module 1: Foundry @transform to Native PySpark Refactoring (Labs 001 - 025)", [
            ("Lab 001", "Refactoring Basic @transform_df to Native PySpark DataFrame Transformation",
             "Foundry uses @transform_df with Input/Output paths. Step 1: Strip decorators. Step 2: Accept SparkSession. Step 3: Replace inputs with spark.read.table() or read.parquet(). Step 4: Write output with df.write.format('delta').saveAsTable()."),
            ("Lab 002", "Handling Foundry Incremental Builds with Spark Structured Streaming",
             "Foundry incremental transforms store state bookmarks. Step 1: Replace incremental input with spark.readStream.table(). Step 2: Implement writeStream.format('delta').outputMode('append').option('checkpointLocation', path).start()."),
            ("Lab 003", "Refactoring Foundry Profile Configurations to Spark Cluster Sizing",
             "Translate @configure(profile=['EXECUTOR_MEMORY_LARGE']) into Spark configuration settings (spark.executor.memory 16g, spark.executor.cores 4) in cluster policy or DABs."),
            ("Lab 004", "Eliminating Foundry Type System Boilerplate and Using Native PySpark Types",
             "Replace foundry.transforms.types with pyspark.sql.types (StructType, StructField, StringType, TimestampType, DoubleType)."),
            ("Lab 005", "Refactoring Foundry Dataset Branch Merging to Git-Backed Spark Repositories",
             "Translate Palantir dataset branching into Git feature branches managed via Databricks Repos and workspace directories."),
            ("Lab 006", "Refactoring Foundry Cross-Dataset Joins with Broadcast Hash Joins",
             "Optimize large-to-small dataset joins by applying pyspark.sql.functions.broadcast() to replicate Foundry memory joins."),
            ("Lab 007", "Porting Foundry Window Aggregations to PySpark WindowSpec",
             "Convert Foundry window expressions into pyspark.sql.window.Window.partitionBy().orderBy() with row_number() and lead/lag."),
            ("Lab 008", "Handling Foundry Null Safety & String Cleansing UDFs",
             "Replace proprietary transform helpers with native PySpark string functions (coalesce, trim, lower, regexp_replace)."),
            ("Lab 009", "Refactoring Foundry Schema Evolution and Enforcement",
             "Migrate Foundry schema change rules to Delta Lake's native schema enforcement and mergeSchema option."),
            ("Lab 010", "Handling Foundry DateTime Partitioning to Delta Liquid Clustering",
             "Convert legacy Hive-style partitioning (year/month/day) into Delta Lake Liquid Clustering via CLUSTER BY (event_date)."),
            ("Lab 011", "Refactoring Foundry Complex Nested JSON Parsing",
             "Translate Foundry JSON unnesting into from_json() with explicit schema and explode() expressions."),
            ("Lab 012", "Refactoring Foundry Array Transformations to Native Spark Higher-Order Functions",
             "Migrate transform(), filter(), and aggregate() functions operating on array columns in PySpark."),
            ("Lab 013", "Handling Foundry Multi-Output Transforms (@transform with Multiple Outputs)",
             "Refactor single transforms emitting multiple datasets into separate DLT tables or PySpark multi-destination writes."),
            ("Lab 014", "Refactoring Foundry Regex Text Classification Pipelines",
             "Implement performant regex pattern matching and tokenization using native Spark functions without custom Python UDFs."),
            ("Lab 015", "Porting Foundry Lookup Tables and Caching Strategies",
             "Replace Foundry in-memory lookup caching with Delta Lake file caching and Spark broadcast variables."),
            ("Lab 016", "Refactoring Foundry Deduplication Logic with dropDuplicates & Windowing",
             "Translate Foundry primary key deduplication into df.dropDuplicates(['entity_id']) or qualified row_number ranking."),
            ("Lab 017", "Handling Foundry Decimal & Currency Precision Rules",
             "Ensure financial math precision using DecimalType(18, 4) in Spark without floating point truncation."),
            ("Lab 018", "Refactoring Foundry Geohash and Coordinate Transformations",
             "Implement spatial point calculations and geohash encoding using open PySpark spatial libraries."),
            ("Lab 019", "Migrating Foundry PySpark Custom Java UDFs to Vectorized Pandas UDFs",
             "Rewrite slow Java/Python UDFs into Apache Arrow-powered @pandas_udf for 10x-50x processing acceleration."),
            ("Lab 020", "Refactoring Foundry Union Operations and Schema Alignment",
             "Translate multi-source dataset unions to df.unionByName(allowMissingColumns=True) in PySpark."),
            ("Lab 021", "Handling Foundry Dynamic Partition Overwrites",
             "Configure spark.sql.sources.partitionOverwriteMode=dynamic to safely overwrite targeted date partitions."),
            ("Lab 022", "Refactoring Foundry Error Trapping and Dead-Letter Queue (DLQ) Pipelines",
             "Capture malformed records into a dedicated _rescued_data column and write to a quarantine Delta table."),
            ("Lab 023", "Migrating Foundry PySpark Unit Tests to pytest and chispa",
             "Set up pytest suites using chispa.assert_df_equality to validate DataFrame schemas and record parity."),
            ("Lab 024", "Refactoring Foundry File Ingestion Metadata Columns",
             "Replace Foundry _build_id and _dataset_path metadata with _metadata.file_name and _metadata.file_modification_time."),
            ("Lab 025", "Building an End-to-End Modular PySpark ETL Package",
             "Package refactored pipelines into installable Python wheels (.whl) deployed via Databricks Asset Bundles.")
        ]),
        ("Module 2: Delta Live Tables (DLT) & Declarative Pipeline Engineering (Labs 026 - 050)", [
            ("Lab 026", "Migrating Basic Foundry Pipeline Builder to @dlt.table Syntax",
             "Translate visual drag-and-drop transformation graphs into declarative Python DLT table definitions."),
            ("Lab 027", "Implementing Streaming Ingest with Auto Loader in DLT",
             "Configure spark.readStream.format('cloudFiles') with schema inference to ingest raw JSON/Parquet automatically."),
            ("Lab 028", "Applying Data Quality Expectations: @dlt.expect (Track Quality Metrics)",
             "Define business hygiene metrics that track quality rules without dropping offending records in pipeline logs."),
            ("Lab 029", "Applying Data Quality Expectations: @dlt.expect_or_drop (Hygiene Enforcement)",
             "Automatically drop invalid records (e.g., null primary keys, negative amounts) before promoting to Silver."),
            ("Lab 030", "Applying Data Quality Expectations: @dlt.expect_or_fail (Critical SLA Enforcement)",
             "Halt pipeline execution immediately upon detecting catastrophic corruptions (e.g., missing mandatory tax IDs)."),
            ("Lab 031", "Implementing Composite & Multi-Rule Expectations in DLT",
             "Define expectation dictionaries evaluating multiple business conditions simultaneously in Silver tables."),
            ("Lab 032", "Building a Medallion Architecture: Bronze Streaming Ingestion",
             "Establish raw, append-only landing zone Delta tables with full audit history and schema evolution enabled."),
            ("Lab 033", "Building a Medallion Architecture: Silver Conformed & Cleansed Tier",
             "Perform deduplication, standardization, and master foreign key lookups in a curated Silver DLT layer."),
            ("Lab 034", "Building a Medallion Architecture: Gold Business Aggregations",
             "Construct high-performance analytical aggregates and semantic metrics ready for BI and executive dashboards."),
            ("Lab 035", "Managing Change Data Capture (CDC) with dlt.apply_changes (SCD Type 1)",
             "Replicate source database updates by continuously overwriting existing records with the latest row state."),
            ("Lab 036", "Managing Change Data Capture (CDC) with dlt.apply_changes (SCD Type 2)",
             "Maintain historical record versions with __START_AT and __END_AT validity intervals for regulatory compliance."),
            ("Lab 037", "Configuring DLT Pipeline Modes: Triggered vs Continuous",
             "Evaluate latency and cost trade-offs: Triggered pipelines for batch cost reduction, Continuous for real-time SLAs."),
            ("Lab 038", "Enabling Delta Liquid Clustering in DLT Tables",
             "Add 'delta.enableLiquidClustering': 'true' in table_properties to eliminate partition skew and optimize query speed."),
            ("Lab 039", "Migrating Foundry Multi-Dataset Schedules to DLT DAG Dependencies",
             "Interlink DLT tables using dlt.read() and dlt.read_stream() to establish automated execution order."),
            ("Lab 040", "Configuring DLT Maintenance Tasks: Auto-Optimize and VACUUM",
             "Manage file compaction and retention settings to prevent small-file sprawl and optimize cloud storage costs."),
            ("Lab 041", "Querying DLT Event Logs for Operational Auditing & Quality Metrics",
             "Analyze event_log Delta tables to extract detailed records of dropped rows, data quality percentages, and duration."),
            ("Lab 042", "Deploying DLT Pipelines across Multiple Environments (Dev/Stage/Prod)",
             "Parameterize catalog and target schemas dynamically using DLT pipeline configuration variables."),
            ("Lab 043", "Integrating Custom Python Libraries into DLT Pipelines",
             "Attach private enterprise helper packages and proprietary utility wheels to DLT cluster environments."),
            ("Lab 044", "Handling Schema Evolution Automatically in DLT Auto Loader",
             "Configure cloudFiles.schemaEvolutionMode='addNewColumns' to gracefully accommodate upstream ERP schema changes."),
            ("Lab 045", "Implementing Advanced Error Quarantine Tables in DLT",
             "Split invalid records into a dedicated quarantine table using inverse expectation conditions for inspection."),
            ("Lab 046", "Optimizing DLT Compute: Enhanced Autoscaling & Serverless DLT",
             "Deploy Serverless DLT pipelines to eliminate cluster startup overhead and scale compute dynamically to zero."),
            ("Lab 047", "Migrating Foundry Time-Series Resampling into DLT Windows",
             "Resample high-frequency IoT streaming telemetry into clean 5-minute rolling averages in Gold DLT tables."),
            ("Lab 048", "Creating Dynamic Temporary Views in DLT Pipelines with @dlt.view",
             "Build intermediate compute steps without persisting intermediate Delta storage to reduce pipeline cost."),
            ("Lab 049", "Monitoring DLT Pipeline Alerts via PagerDuty and Webhooks",
             "Configure automated notification hooks triggering alerts upon pipeline failure or expectation breaches."),
            ("Lab 050", "End-to-End Migration of an Enterprise Foundry Supply Chain Pipeline to DLT",
             "Execute a complete real-world pipeline migration covering ingestion, transformation, quality gates, and Gold tables.")
        ]),
        ("Module 3: Decoupling Palantir Ontology to Unity Catalog Delta Lake (Labs 051 - 075)", [
            ("Lab 051", "Extracting Palantir Ontology Metadata Specifications to JSON",
             "Use Palantir Foundry REST APIs to export Object Types, Link Types, Action Types, and Property schemas."),
            ("Lab 052", "Mapping Ontology Object Types to Unity Catalog Three-Level Namespace",
             "Translate Foundry Object models into catalog.schema.table naming standards (e.g., enterprise.gold.dim_customer)."),
            ("Lab 053", "Defining Primary Key Constraints in Unity Catalog Delta Tables",
             "Apply NOT NULL and CONSTRAINT pk_name PRIMARY KEY (id) to mirror Foundry Object primary keys."),
            ("Lab 054", "Mapping Ontology Link Types (1:1, 1:N) to Foreign Key Constraints",
             "Implement ALTER TABLE ... ADD CONSTRAINT fk_name FOREIGN KEY REFERENCES to encode semantic link relationships."),
            ("Lab 055", "Translating Ontology Many-to-Many (N:M) Link Types to Associative Delta Tables",
             "Construct bridge tables with dual foreign keys to represent complex multi-object relationships."),
            ("Lab 056", "Implementing Liquid Clustering on High-Cardinality Ontology Join Keys",
             "Apply CLUSTER BY (customer_id, country_code) to ensure sub-second object lookup latencies."),
            ("Lab 057", "Mapping Ontology Calculated Properties to Unity Catalog Generated Columns",
             "Create persistent generated columns (e.g., total_cost AS (quantity * unit_price)) for compute-free reads."),
            ("Lab 058", "Mapping Ontology Real-Time Sync to Delta Lake Streaming Append/Merge",
             "Build streaming MERGE INTO pipelines updating Gold Delta tables within seconds of source system mutations."),
            ("Lab 059", "Building Semantic Views on Gold Delta Tables for Graph Navigation",
             "Construct SQL relational views performing pre-joined multi-hop graph traversals across entity links."),
            ("Lab 060", "Governing Unstructured Entity Attachments with Unity Catalog Volumes",
             "Migrate Foundry file attachments (PDFs, images) into Unity Catalog Volumes with POSIX-compliant paths."),
            ("Lab 061", "Synchronizing Unity Catalog Table Comments with Ontology Business Descriptions",
             "Apply COMMENT ON TABLE and COMMENT ON COLUMN statements mirroring Foundry human-readable metadata."),
            ("Lab 062", "Translating Foundry Object Backing Datasets to Managed vs External Tables",
             "Evaluate architectural trade-offs: Managed tables for performance vs External tables for cloud bucket isolation."),
            ("Lab 063", "Mapping Dynamic Object Statuses to Categorical State Enums in Delta",
             "Standardize operational states (ACTIVE, PENDING, SUSPENDED) using SQL CHECK constraints or expectation rules."),
            ("Lab 064", "Building Historical Audit Tables with Delta Lake Time Travel",
             "Leverage RESTORE and VERSION AS OF queries to inspect historical digital twin states without custom logic."),
            ("Lab 065", "Implementing Unity Catalog Tagging for Object Classification",
             "Apply SET TAGS ('tier' = 'critical_asset', 'domain' = 'supply_chain') across tables for discovery."),
            ("Lab 066", "Translating Foundry Geolocation Properties to Delta H3 Hexagonal Hierarchies",
             "Index spatial object coordinates using Uber H3 grid indexes in PySpark for high-speed spatial querying."),
            ("Lab 067", "Migrating Ontology Hierarchy Structures to Recursive CTEs in Databricks SQL",
             "Traverse parent-child operational hierarchies (e.g., Bill of Materials, org charts) using WITH RECURSIVE SQL."),
            ("Lab 068", "Implementing Automated Delta Table Compaction (OPTIMIZE) for Object Queries",
             "Configure automated background compaction to ensure 100MB-1GB file sizing for point object lookups."),
            ("Lab 069", "Translating Foundry Functions on Objects to Unity Catalog SQL Functions",
             "Convert TypeScript object functions into native SQL scalar UDFs (CREATE FUNCTION enterprise.gold.risk_score...)."),
            ("Lab 070", "Translating Foundry Python Object Functions to Unity Catalog Python UDFs",
             "Register vectorized Python functions in Unity Catalog for complex mathematical or ML scoring logic."),
            ("Lab 071", "Mapping Foundry Media Sets to Unity Catalog Multimodal Volumes",
             "Catalog audio, video, and medical imaging data alongside structured entity records in unified schemas."),
            ("Lab 072", "Implementing Cross-Workspace Object Sharing via Open Delta Sharing",
             "Share curated Gold entity tables securely with external partners without requiring vendor account provisioning."),
            ("Lab 073", "Validating Constraint Violations with Unity Catalog System Tables",
             "Inspect system.information_schema.check_constraints to verify schema enforcement across all entity models."),
            ("Lab 074", "Building a Semantic Layer Integration with Cube / dbt Semantic Layer",
             "Expose Unity Catalog Gold Delta tables to external semantic metrics engines for self-service BI."),
            ("Lab 075", "End-to-End Digital Twin Migration: Enterprise Supply Chain Master Model",
             "Execute full migration of a multi-object enterprise ontology into production Unity Catalog tables.")
        ]),
        ("Module 4: Palantir Kinetic Actions & Write-Backs to Databricks Apps (Labs 076 - 100)", [
            ("Lab 076", "Analyzing Foundry TypeScript Action Functions & State Mutation Patterns",
             "Deconstruct Action Type parameters, validation logic, object property edits, and webhook payloads."),
            ("Lab 077", "Architecting the Decoupled Operational Action Loop in Databricks",
             "Design the 3-tier architecture: UI (Streamlit) -> API Handler (FastAPI) -> System of Record & Audit Delta Table."),
            ("Lab 078", "Building a Databricks App with Python Streamlit for Operational Cockpits",
             "Create interactive layouts, KPI metrics cards, and filtered object worklists deployed on Serverless Apps."),
            ("Lab 079", "Implementing Secure SSO Authentication in Databricks Apps using OIDC/OAuth",
             "Extract authenticated user identity, groups, and email tokens directly from Databricks App headers."),
            ("Lab 080", "Creating the Operational Action Execution Handler in FastAPI",
             "Build containerized REST microservices receiving action parameters and enforcing validation logic."),
            ("Lab 081", "Executing Kinetic Write-Backs to SAP ERP via RFC / REST Gateway",
             "Dispatch authenticated HTTPS POST calls updating sales order statuses in enterprise SAP instances."),
            ("Lab 082", "Executing Kinetic Write-Backs to Salesforce CRM via REST API",
             "Update account tiers, credit limits, and contact records programmatically from Databricks Apps."),
            ("Lab 083", "Recording ACID Operational Action Audit Logs in Unity Catalog Delta Tables",
             "Commit every executed user action into an immutable enterprise_operations.gold.audit_actions table."),
            ("Lab 084", "Implementing Pessimistic & Optimistic Concurrency Control in Action Handlers",
             "Prevent simultaneous conflicting updates to the same entity using Delta Lake conditional update syntax."),
            ("Lab 085", "Building Action Approval & Human-in-the-Loop Workflow Queues",
             "Implement tiered approval states (PENDING_APPROVAL -> APPROVED) with role-based action gating."),
            ("Lab 086", "Integrating Reverse-ETL Connectors for Bulk Action Syncing",
             "Deploy FiveTran or Hightouch reverse-ETL pipelines syncing Gold Delta tables back into warehouse ERPs."),
            ("Lab 087", "Handling Action Failure, Retries, and Exponential Backoff",
             "Implement resilient webhook dispatching with dead-letter queue persistence for failed ERP calls."),
            ("Lab 088", "Building Responsive Form Validations in Streamlit Applications",
             "Enforce parameter constraints (e.g., maximum budget threshold, mandatory justification reason) in the UI."),
            ("Lab 089", "Designing Geospatial Map Layers in Databricks Apps with PyDeck",
             "Replicate Palantir Gaia/geospatial tracking maps showing warehouse facilities and delivery routes."),
            ("Lab 090", "Implementing Real-Time Notification Webhooks on Action Execution (Slack/Teams)",
             "Broadcast urgent action execution alerts to operations teams via Slack or Microsoft Teams webhooks."),
            ("Lab 091", "Deploying Databricks Apps via Databricks CLI and app.yaml Configuration",
             "Package application code, requirements.txt, and environment parameters for automated cloud deployment."),
            ("Lab 092", "Enforcing Unity Catalog Permissions within Databricks Apps via Service Principals",
             "Execute backend Delta reads and writes under tightly scoped Azure/AWS Service Principal credentials."),
            ("Lab 093", "Building Interactive Action History & Reversal Cockpits",
             "Allow authorized managers to inspect executed action timelines and trigger compensating reversal actions."),
            ("Lab 094", "Implementing Real-Time In-Memory Caching for Sub-Second Cockpit Reads",
             "Cache frequently queried master entities using Redis or Streamlit caching (@st.cache_data) with TTL."),
            ("Lab 095", "Translating Palantir Slate Custom Web Apps to React / FastAPI on Databricks",
             "Build enterprise-grade React front-ends connecting to Databricks SQL Serverless backends."),
            ("Lab 096", "Building Batch Action Execution (Bulk Approval & Reallocation)",
             "Enable operations leads to multi-select 50+ shortage orders and execute batched ERP rebalances."),
            ("Lab 097", "Monitoring Databricks App Latency & Error Rates with Databricks Lakehouse Monitoring",
             "Track application API response times, user engagement, and error budgets automatically."),
            ("Lab 098", "Handling High-Concurrency User Traffic in Operational Databricks Apps",
             "Configure autoscaling worker replicas in Databricks Apps to maintain sub-second response times under load."),
            ("Lab 099", "Implementing File Upload & Invoice Attachment Handlers in Databricks Apps",
             "Allow field users to attach photo receipts or invoices that are saved directly into Unity Catalog Volumes."),
            ("Lab 100", "End-to-End Operational Write-Back Migration: Global Expedite & Rebalance Cockpit",
             "Deliver a complete, production-ready operational app replacing Palantir Workshop for supply chain expedite.")
        ]),
        ("Module 5: Enterprise Security: Palantir Markings to Unity Catalog ABAC (Labs 101 - 125)", [
            ("Lab 101", "Auditing Palantir Mandatory Access Control (MAC) Markings & Access Policies",
             "Extract all dataset and column marking tags, organizations, and user group entitlement rosters."),
            ("Lab 102", "Translating Markings to Unity Catalog Attribute-Based Access Control (ABAC) Tags",
             "Define standardized governance tags using ALTER TABLE ... SET TAGS ('marking' = 'SECRET_ORANGE')."),
            ("Lab 103", "Implementing Dynamic Row Filtering with is_account_group_member()",
             "Restrict row access dynamically based on user identity provider group memberships."),
            ("Lab 104", "Implementing Regional Geographic Row Filters for Multi-National Sales Data",
             "Enforce country-level row segmentation allowing EMEA users to view only European entity records."),
            ("Lab 105", "Creating Dynamic Column Masking Functions for Social Security & Tax IDs",
             "Implement SQL UDFs redacting sensitive identifiers to last 4 digits for unauthorized analytical users."),
            ("Lab 106", "Creating Conditional Masking Functions for Financial Compensation & Executive Pay",
             "Mask executive salary columns with NULL values unless the session user belongs to the executive HR group."),
            ("Lab 107", "Translating Palantir Purpose-Based Access Control into Dynamic Session Verification",
             "Enforce session-level purpose attestations before allowing analytical queries to return sensitive tables."),
            ("Lab 108", "Managing Fine-Grained Permissions on Unity Catalog Volumes",
             "Grant READ VOLUME and WRITE VOLUME privileges scoped to specific compliance officer roles."),
            ("Lab 109", "Automating User Provisioning & Group Synchronization with SCIM (Okta / Azure AD)",
             "Configure enterprise IdP SCIM connectors to synchronize users and security groups automatically."),
            ("Lab 110", "Configuring AWS IAM Roles & Azure Managed Identities for Storage Credentials",
             "Eliminate hardcoded access keys by configuring IAM instance profiles and Managed Identity credentials."),
            ("Lab 111", "Enforcing Network Isolation with AWS PrivateLink & Azure VNet Injection",
             "Isolate Databricks control plane and data plane communication within private VPC network routes."),
            ("Lab 112", "Implementing Unity Catalog Clean Rooms for Secure Multi-Party Data Sharing",
             "Collaborate on joint customer analytics with external partners without exposing underlying raw datasets."),
            ("Lab 113", "Auditing Data Access Lineage using Unity Catalog System Tables",
             "Query system.access.audit and system.access.table_lineage to trace every query executed across sensitive tables."),
            ("Lab 114", "Implementing Cryptographic Data Hashing (SHA-256) for Regulatory Privacy (GDPR/HIPAA)",
             "Apply deterministic pseudonymization hashes to customer identifiers across all Silver tables."),
            ("Lab 115", "Enforcing Customer-Managed Encryption Keys (CMEK) for Managed Disks & Storage",
             "Configure AWS KMS or Azure Key Vault encryption keys ensuring complete cryptographic tenancy control."),
            ("Lab 116", "Translating Foundry Project-Based Permissions to Unity Catalog Schemas",
             "Map department project folders into isolated schemas with strictly enforced GRANT USAGE privileges."),
            ("Lab 117", "Implementing Break-Glass Emergency Access Procedures in Unity Catalog",
             "Configure audited temporary privilege elevation workflows for high-severity operational incidents."),
            ("Lab 118", "Auditing Column-Level Lineage for PII Data Flow Verification",
             "Visualize end-to-end data flow in Unity Catalog to verify that masked PII never leaks into downstream Gold tables."),
            ("Lab 119", "Enforcing Strict Table Immutability & Append-Only Policies for Compliance Tables",
             "Revoke DELETE and UPDATE privileges on regulatory audit tables to prevent tampering."),
            ("Lab 120", "Configuring IP Access Lists for Workspace & SQL Warehouse Network Ingress",
             "Restrict workspace and serverless endpoint access strictly to corporate VPN and office IP CIDR blocks."),
            ("Lab 121", "Implementing Data Retention Rules and Automated Purging (VACUUM & Retention Limits)",
             "Enforce GDPR 'Right to be Forgotten' policies by executing targeted Delta table vacuuming and purges."),
            ("Lab 122", "Creating Automated Security Compliance Verification Scripts",
             "Run automated security scanning scripts checking for unmasked PII columns or permissive ACLs."),
            ("Lab 123", "Configuring Unity Catalog External Locations with Least-Privilege IAM Scopes",
             "Scope cloud bucket access paths to exact subdirectories to prevent cross-catalog data exposure."),
            ("Lab 124", "Simulating Unauthorized Access Attempts & Verifying ABAC Enforcement",
             "Execute automated penetration tests validating that unauthorized roles cannot view restricted rows or columns."),
            ("Lab 125", "End-to-End Enterprise Security Migration: National Defense & Banking Grade ABAC",
             "Deploy complete enterprise security model translating 50+ Palantir Markings to Unity Catalog ABAC.")
        ]),
        ("Module 6: Enterprise SQL Engineering, DBSQL Photon & AI/BI Migration (Labs 126 - 150)", [
            ("Lab 126", "Migrating Palantir Contour Cohort Analyses to Databricks SQL Views",
             "Translate interactive point-and-click cohort filter paths into clean, performant SQL analytical queries."),
            ("Lab 127", "Migrating Palantir Quiver Time-Series Transforms to SQL Windowing Functions",
             "Convert time-series interpolation, rolling trends, and anomalies into native DBSQL analytics."),
            ("Lab 128", "Deploying Databricks SQL Serverless Warehouses with Auto-Stop Policies",
             "Configure instant-on Serverless SQL Warehouses scaling elastically to 10+ clusters with 10-minute auto-stop."),
            ("Lab 129", "Benchmarking DBSQL Photon Query Performance against Legacy Foundry Queries",
             "Execute TPC-DS benchmark queries measuring execution time, CPU utilization, and I/O throughput."),
            ("Lab 130", "Building Interactive AI/BI Dashboards in Databricks",
             "Assemble executive KPI dashboards featuring interactive parameterized filters, charts, and drill-downs."),
            ("Lab 131", "Configuring AI/BI Genie Spaces for Conversational Self-Service Analytics",
             "Curate trusted Gold tables, add semantic descriptions, and set up Genie spaces for natural language questions."),
            ("Lab 132", "Optimizing Query Execution Plans with Photon Vectorized Operators",
             "Analyze EXPLAIN FORMATTED plans to ensure operators execute in Photon native vectorized C++ code."),
            ("Lab 133", "Implementing Materialized Views in Databricks SQL",
             "Create CREATE MATERIALIZED VIEW statements with incremental refresh schedules to accelerate dashboard queries."),
            ("Lab 134", "Implementing Streaming Tables in Databricks SQL",
             "Build append-only streaming aggregations directly in DBSQL without writing PySpark pipelines."),
            ("Lab 135", "Translating Foundry Workbook Formulas to DBSQL Scalar Expressions",
             "Convert Excel-style spreadsheet formulas into standardized SQL CASE WHEN and mathematical expressions."),
            ("Lab 136", "Configuring Scheduled Dashboard Email Subscriptions & PDF Snapshots",
             "Automate daily PDF snapshots of executive supply chain cockpits delivered to leadership inboxes."),
            ("Lab 137", "Setting Up Real-Time SQL Query Alerts for Critical Metric Breaches",
             "Configure threshold alerts notifying operations teams when supply chain shortage counts exceed 20."),
            ("Lab 138", "Optimizing Star-Schema Joins with Delta Lake Liquid Clustering",
             "Eliminate expensive sort-merge joins by clustering fact and dimension tables on common foreign keys."),
            ("Lab 139", "Implementing High-Concurrency Query Caching & Result Cache Invalidation",
             "Leverage DBSQL result caching to deliver sub-10ms response times for repeated dashboard queries."),
            ("Lab 140", "Connecting Third-Party BI Tools (Power BI / Tableau) to Databricks SQL via Partner Connect",
             "Configure DirectQuery connections from Power BI Desktop to Serverless DBSQL using OAuth credentials."),
            ("Lab 141", "Translating Palantir Funnel Analyses to SQL Sessionization Models",
             "Model user conversion and procurement funnels using windowed sessionization queries in DBSQL."),
            ("Lab 142", "Implementing Geospatial Spatial Joins (ST_Contains) in Databricks SQL",
             "Join customer point locations with geographic delivery zones using spatial SQL functions."),
            ("Lab 143", "Creating Parameterized SQL Queries with Dynamic Date Ranges and Dropdowns",
             "Build reusable queries accepting user-selected parameters to power interactive analytical forms."),
            ("Lab 144", "Translating Foundry Data Validation Workbooks to Great Expectations SQL Rules",
             "Automate data hygiene validation checks executed directly against Delta tables in DBSQL."),
            ("Lab 145", "Optimizing Complex Aggregations with GROUP BY GROUPING SETS & ROLLUP",
             "Generate multi-dimensional summary reports across region, product category, and quarter in a single query pass."),
            ("Lab 146", "Configuring Fine-Grained Query Profile Inspection & Bottleneck Analysis",
             "Diagnose slow queries using Query Profile visualizer to identify data skew, spilling, or missing indexes."),
            ("Lab 147", "Migrating Proprietary Foundry Aggregation Metrics to Standard SQL Metric Definitions",
             "Standardize corporate metrics (e.g., Gross Margin, On-Time In-Full Delivery) into reusable SQL expressions."),
            ("Lab 148", "Implementing Zero-Copy Data Federation Queries to External Cloud Warehouses",
             "Query external Snowflake and PostgreSQL tables in-place using Unity Catalog Lakehouse Federation."),
            ("Lab 149", "Building Multi-Tenant BI Reporting with Dynamic Row-Level Security in DBSQL",
             "Ensure multi-client dashboards automatically filter data according to the viewer's corporate account ID."),
            ("Lab 150", "End-to-End BI Migration: Transitioning 100+ Palantir Contour & Quiver Reports to DBSQL",
             "Execute full migration of enterprise reporting estate to Databricks AI/BI Dashboards and Genie.")
        ]),
        ("Module 7: Mosaic AI & MLflow: Migrating Palantir AIP to Compound AI (Labs 151 - 175)", [
            ("Lab 151", "Deconstructing Palantir AIP: Agent Studio, AIP Logic, and AIP Mesh",
             "Analyze prompt templates, tool bindings, retrieval strategies, and evaluation gates in Palantir AIP."),
            ("Lab 152", "Setting Up Databricks Mosaic AI Model Serving with Foundation Models",
             "Deploy serverless pay-per-token foundation model endpoints (Meta Llama 3.1 70B, DBRX, Claude, GPT-4)."),
            ("Lab 153", "Building a Managed Vector Search Index in Unity Catalog",
             "Create a real-time auto-syncing Vector Search endpoint indexed against an enterprise knowledge base Delta table."),
            ("Lab 154", "Implementing Hybrid Search (Lexical Keyword + Dense Vector Similarity)",
             "Combine full-text search with embedding cosine similarity to maximize retrieval precision for technical documents."),
            ("Lab 155", "Building a Retrieval-Augmented Generation (RAG) Chain with LangChain & Databricks",
             "Construct context-augmented QA chains retrieving supply chain manuals and standard operating procedures."),
            ("Lab 156", "Porting Palantir AIP Agent Tools to Unity Catalog Functions as Tools",
             "Register SQL and Python functions in Unity Catalog as callable tools for autonomous AI agents."),
            ("Lab 157", "Implementing Autonomous Multi-Agent Workflows with Mosaic AI Agent Framework",
             "Build multi-agent collaboration systems where a triage agent delegates work to a procurement specialist agent."),
            ("Lab 158", "Implementing Strict Human-in-the-Loop (HITL) Guardrails in Mosaic AI Agents",
             "Enforce programmatic policies halting agent execution when financial impact exceeds defined thresholds."),
            ("Lab 159", "Logging Multi-Agent Chains and Traces with MLflow 2.x Tracing",
             "Capture detailed spans, latency breakdown, prompt inputs, and token usage for every agent invocation."),
            ("Lab 160", "Automating LLM Evaluation with Mosaic AI Agent Evaluation (LLM-as-a-Judge)",
             "Run automated evaluation pipelines assessing answer groundedness, relevance, safety, and hallucination rates."),
            ("Lab 161", "Deploying Fine-Tuning Pipelines on Databricks with Mosaic AI Training",
             "Fine-tune domain-specific language models using enterprise training datasets logged in Delta Lake."),
            ("Lab 162", "Deploying Mosaic AI Gateway for Rate Limiting, Cost Tracking & PII Redaction",
             "Route all enterprise LLM calls through a governed gateway enforcing spend quotas and PII scrubbing."),
            ("Lab 163", "Migrating Palantir AIP Assist Interactive Workflows to AI/BI Genie Spaces",
             "Transition conversational data querying into governed Genie spaces backed by curated Unity Catalog semantics."),
            ("Lab 164", "Building Structured Output Agents with Pydantic & Instructor",
             "Force LLM agents to return strictly validated JSON schemas matching enterprise API payloads."),
            ("Lab 165", "Implementing Document Chunking & Ingestion Pipelines for Unstructured PDF/Word Manuals",
             "Extract text, split into semantically coherent chunks with overlap, and compute embedding vectors in PySpark."),
            ("Lab 166", "Packaging Mosaic AI Agents as MLflow PyFunc Models",
             "Wrap multi-agent code into standard MLflow models deployed to serverless low-latency REST endpoints."),
            ("Lab 167", "Implementing Semantic Caching to Reduce LLM API Spend",
             "Cache identical semantic questions using Vector Search lookups to bypass redundant foundation model queries."),
            ("Lab 168", "Building Guardrail Classifiers with Llama Guard & NeMo Guardrails",
             "Inspect user prompts and model completions to block prompt injection attacks and toxic outputs."),
            ("Lab 169", "Tracking Agent Token Costs and FinOps Metrics in MLflow",
             "Aggregate input/output token counts per department and log cost attribution to Unity Catalog system tables."),
            ("Lab 170", "Migrating Traditional Scikit-Learn / XGBoost Models to MLflow Model Registry",
             "Register classical predictive models alongside LLMs under unified Unity Catalog model governance."),
            ("Lab 171", "Implementing Real-Time Feature Store Lookups with Unity Catalog Feature Engineering",
             "Serve low-latency feature vectors to operational ML models during real-time scoring invocations."),
            ("Lab 172", "Running A/B Performance Testing on Competing Foundation Models in Production",
             "Route live user queries between competing LLMs to benchmark speed, quality, and user satisfaction."),
            ("Lab 173", "Deploying Local Open-Source Small Language Models (SLMs) for Edge Inference",
             "Host lightweight models (Mistral 7B, Llama 3 8B) on single-GPU instances for cost-effective edge processing."),
            ("Lab 174", "Building Continuous Evaluation Regression CI/CD Gates in GitHub Actions",
             "Block automated production deployments if model evaluation scores drop below 90% quality thresholds."),
            ("Lab 175", "End-to-End Enterprise AI Migration: Production Autonomous Supply Chain Agent",
             "Deploy full compound AI system replacing Palantir AIP with Mosaic AI Agent Framework and Vector Search.")
        ]),
        ("Module 8: Automated Data Reconciliation & Dual-Run Parity Suites (Labs 176 - 190)", [
            ("Lab 176", "Designing the Enterprise Dual-Run Parallel Architecture",
             "Establish dual-ingest pipelines running Palantir Foundry and Databricks Lakehouse concurrently."),
            ("Lab 177", "Building Automated Row Count Parity Verification Pipelines",
             "Compare row counts across 100+ table pairs daily, alerting on any discrepancies greater than 0%."),
            ("Lab 178", "Implementing Primary Key Set Difference Checks (Missing & Unexpected Records)",
             "Identify records present in Foundry but missing in Databricks, or unexpected phantom records in target tables."),
            ("Lab 179", "Implementing Bitwise Checksum Hashing Across Key Business Attributes",
             "Compute SHA-256 row hashes across concatenated business columns to verify bitwise data identity."),
            ("Lab 180", "Calculating Statistical Distribution Parity for Numeric Financial Columns",
             "Compare sum, mean, standard deviation, min, and max across currency and revenue metrics between systems."),
            ("Lab 181", "Handling Timestamp & Timezone Discrepancies Across Platforms",
             "Reconcile UTC normalization and timestamp precision differences between Foundry and Spark engines."),
            ("Lab 182", "Handling Floating Point Precision Tolerances in Scientific Metrics",
             "Implement epsilon thresholding (abs(source - target) < 1e-6) for high-precision double columns."),
            ("Lab 183", "Automating Great Expectations Validation Suites in Databricks",
             "Configure automated test suites checking nullability, uniqueness, and value range constraints on Delta tables."),
            ("Lab 184", "Building Automated Schema Drift Detection & Reconciliation Alerts",
             "Detect unannounced upstream schema modifications and alert data engineering teams before pipelines fail."),
            ("Lab 185", "Creating Automated Daily Data Parity HTML Executive Dashboards",
             "Generate automated daily visual parity scorecards published to enterprise Slack and email distribution lists."),
            ("Lab 186", "Building Targeted Data Repair & Catch-Up Sync Scripts",
             "Automate incremental catch-up scripts to repair identified discrepancies without triggering full reloads."),
            ("Lab 187", "Simulating Source System Outages & Validating Pipeline Resiliency",
             "Test pipeline recovery and checkpoint replay capabilities during simulated network and ERP disconnects."),
            ("Lab 188", "Benchmarking End-to-End Latency from Source Ingestion to Gold Presentation",
             "Measure end-to-end data processing duration to verify Databricks satisfies all legacy Foundry SLAs."),
            ("Lab 189", "Generating Formal Cutover Audit Certificates and Reconciliation Proofs",
             "Produce digitally signed JSON and PDF audit certificates attesting to 100% data parity for InfoSec sign-off."),
            ("Lab 190", "End-to-End Enterprise Parity Certification: 100 Million Row Dual-Run Validation",
             "Execute full 30-day parallel reconciliation run across enterprise core financial and supply chain datasets.")
        ]),
        ("Module 9: Orchestration & CI/CD: Foundry Builds to Lakeflow & DABs (Labs 191 - 195)", [
            ("Lab 191", "Deconstructing Foundry Build Schedules and Dataset Dependency Graphs",
             "Map complex multi-stage Foundry build schedules into directed acyclic graphs (DAGs)."),
            ("Lab 192", "Building Multi-Task Lakeflow Jobs (Workflows) with Task Dependencies",
             "Configure JSON and YAML multi-task workflows orchestrating DLT pipelines, SQL tasks, and Python jobs."),
            ("Lab 193", "Setting Up Databricks Asset Bundles (DABs) for Infrastructure-as-Code (IaC)",
             "Define workspaces, pipelines, compute clusters, and jobs in declarative databricks.yml manifests."),
            ("Lab 194", "Building GitHub Actions CI/CD Release Pipelines for DABs Deployment",
             "Automate linting, unit testing, bundle validation, and deployment across Dev, Staging, and Production."),
            ("Lab 195", "Configuring Automated Pipeline SLA Monitoring, Retries & Escalation Policies",
             "Enforce automated retry policies, timeout limits, and pager escalation routing in Lakeflow Jobs.")
        ]),
        ("Module 10: Production Cutover, Zero-Downtime Migration & FinOps (Labs 196 - 200)", [
            ("Lab 196", "Executing Zero-Downtime Production Cutover Playbook",
             "Switch upstream DNS, API gateways, and user traffic from Palantir Workshop to Databricks Apps seamlessly."),
            ("Lab 197", "Configuring Rollback Procedures and Emergency Fallback Mechanisms",
             "Maintain standby failover synchronization to Palantir for 72 hours post-cutover in the event of anomalies."),
            ("Lab 198", "Implementing FinOps Cost Attribution via Unity Catalog System Tables",
             "Query system.billing.usage to track DBU consumption, dollar cost per business unit, and cluster efficiency."),
            ("Lab 199", "Archiving Historical Palantir Foundry Datasets into Cold Cloud Storage",
             "Export and archive historical Foundry project versions into cost-effective S3 Glacier / Azure Archive tiers."),
            ("Lab 200", "Decommissioning Palantir Foundry Tenant & Contract Off-Ramp Sign-Off",
             "Revoke network interconnects, terminate cloud instances, and execute formal contractual platform off-ramp.")
        ])
    ]

    for mod_title, labs in modules_labs_data:
        add_heading_1(doc, mod_title)
        for lab_id, lab_name, lab_desc in labs:
            add_heading_2(doc, f"{lab_id}: {lab_name}")
            doc.add_paragraph(lab_desc)

    output_path = "/Users/josekurian/GoogleAutomation/AIPalatirToDatabricks/Palantir to Databricks 200 Hands-On Labs Step by Steps Instructions.docx"
    doc.save(output_path)
    print(f"Saved: {output_path}")

if __name__ == "__main__":
    build_200_labs_document()
