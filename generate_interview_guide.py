import os
import docx
from docx.shared import Inches, Pt, RGBColor
from doc_helper import create_styled_document, add_heading_1, add_heading_2, add_heading_3, add_callout, add_custom_table

def build_interview_guide():
    doc = create_styled_document(
        "Palantir to Databricks Migration Consultant Technical Interview Preparation Guide",
        "Mastering Enterprise Architecture, Migration Mechanics, Code Refactoring, System Design, Scenario Case Studies, and Executive Behavioral Interviews"
    )

    add_callout(
        doc,
        "This guide is curated specifically for Principal Data Architects, Senior Migration Consultants, and Enterprise Advisory Leads preparing for rigorous technical and architectural interviews focusing on Palantir-to-Databricks transitions. It delivers deep, verifiable technical answers across all migration vectors, system design blueprints, code refactoring patterns, and executive scenario responses.",
        "INTERVIEW MASTERY MISSION"
    )

    add_heading_1(doc, "1. Interview Structure & Core Competency Matrix")
    doc.add_paragraph(
        "Interviews for Senior Migration Consultants typically encompass four distinct evaluation rounds: Technical Deep-Dive & Architecture, Live System Design & Migration Scenarios, Code & Pipeline Refactoring, and Executive Stakeholder & Change Management."
    )

    headers_eval = ["Interview Round", "Key Focus Areas", "What the Interview Panel Looks For", "Passing Criteria"]
    data_eval = [
        ["Round 1: Architectural Deep Dive", "Foundry vs. Lakehouse, Unity Catalog, Photon, Delta Lake UniForm, Medallion Architecture", "Clear understanding of both platforms' internal architectures without bias.", "Ability to articulate trade-offs, storage layouts, and governance models."],
        ["Round 2: System Design & Scenarios", "Enterprise cutover strategies, parallel run design, zero-downtime streaming, ERP write-backs", "Structured thinking, risk mitigation frameworks, operational continuity.", "End-to-end design addressing data drift, networking, and rollback plans."],
        ["Round 3: Hands-on Code Refactoring", "Converting `@transform_df` to DLT, TypeScript Actions to Databricks Apps, Markings to ABAC", "Fluency in PySpark, SQL, DLT syntax, REST APIs, and Unity Catalog DDL.", "Clean, performant code with automated tests and quality expectations."],
        ["Round 4: Executive Behavioral & TCO", "Handling FDE lock-in, convincing skeptical business users, CFO cost defense, FinOps", "Executive presence, political agility, consultative influence, cost modeling.", "Clear articulation of business value, ROI, and empathetic change management."]
    ]
    add_custom_table(doc, headers_eval, data_eval, [Inches(1.5), Inches(1.8), Inches(1.8), Inches(1.4)])

    add_heading_1(doc, "2. Top 20 Technical Q&A: Architectural Deep-Dive")

    questions_and_answers = [
        (
            "Q1: What is the fundamental architectural difference between Palantir Foundry and Databricks?",
            "Answer: Palantir Foundry is an 'Ontology-first operational decision application platform' built from the top down. It tightly couples proprietary data storage, a stateful business object model (Ontology), kinetic write-back actions, and UI builders (Workshop). Databricks is an 'Open Data Intelligence Platform & Lakehouse' built from the bottom up on open standards (Delta Lake, Apache Spark, MLflow, Unity Catalog). While Palantir focuses on operational decision loops in business cockpits, Databricks provides a unified, open, high-throughput engine for analytics, data engineering, and generative AI across multi-cloud environments without vendor lock-in."
        ),
        (
            "Q2: How do you translate the Palantir Foundry Ontology into Databricks?",
            "Answer: The Foundry Ontology cannot be ported as a monolithic proprietary object; it must be decoupled into three modular Lakehouse layers:\n"
            "1. Entity State: Palantir Object Types map directly to curated Delta Lake Gold tables in Unity Catalog with primary key constraints, optimized via Liquid Clustering.\n"
            "2. Semantic Relationships: Link Types map to Unity Catalog foreign key constraints and semantic metrics layers (dbt Semantic Layer or Cube).\n"
            "3. Kinetic Operational Actions (Write-Backs): Action Types and TypeScript functions map to Python microservices running inside Databricks Apps (FastAPI or Streamlit), which interact with external systems of record (SAP, Salesforce) and write immutable audit records back to Unity Catalog Delta tables."
        ),
        (
            "Q3: How do you migrate Palantir Markings and Purpose-based security into Databricks Unity Catalog?",
            "Answer: Palantir Markings represent Mandatory Access Control (MAC). In Databricks, this is translated to Attribute-Based Access Control (ABAC) in Unity Catalog:\n"
            "1. Classification Tagging: Use `ALTER TABLE ... SET TAGS ('marking' = 'SECRET_ORANGE', 'purpose' = 'FINANCIAL_AUDIT')`.\n"
            "2. Dynamic Row Filtering: Implement SQL UDFs (`CREATE FUNCTION customer_filter ... RETURN is_account_group_member(...)`) bound to tables via `WITH ROW FILTER`.\n"
            "3. Dynamic Column Masking: Protect PII or confidential fields using `CREATE FUNCTION mask_field ... MASK ...` returning hashes or redacted values for unauthorized personas."
        ),
        (
            "Q4: What is the exact mapping between Palantir transforms and Databricks pipelines?",
            "Answer:\n"
            "• Foundry Code Repositories (@transform_df, PySpark, SQL) -> Databricks Delta Live Tables (DLT) or Databricks Asset Bundles (DABs) running on Serverless Spark.\n"
            "• Pipeline Builder (Visual low-code ETL) -> Declarative Delta Live Tables (DLT) with expectations (`@dlt.expect_or_drop`).\n"
            "• Contour / Quiver -> Databricks SQL Queries, AI/BI Dashboards, and AI/BI Genie Spaces.\n"
            "• Foundry Builds & Schedules -> Databricks Lakeflow Jobs (Workflows) with multi-task DAG dependencies."
        ),
        (
            "Q5: Why does Databricks offer superior price-performance over Palantir's Spark execution?",
            "Answer: Palantir Foundry executes standard open-source Apache Spark wrapped inside proprietary build containers. Databricks utilizes the Photon Engine—a completely rewritten, vectorized C++ query execution engine optimized for modern CPU architectures (SIMD instruction sets, NVMe cache, vectorized column batches). Combined with Delta Lake features like Liquid Clustering, deletion vectors, and auto-compaction, Photon delivers 3x to 5x higher throughput on star-schema analytical workloads while consuming significantly fewer worker nodes."
        ),
        (
            "Q6: How do you address the operational 'write-back' capability that Palantir Workshop provides?",
            "Answer: In Palantir, users click Workshop buttons that trigger TypeScript functions updating ERPs and object states. In Databricks, this is implemented using Databricks Apps—secure, containerized web applications (Streamlit, Dash, or FastAPI) running directly within the Databricks workspace and governed by Unity Catalog OAuth tokens. When a user submits an action, the Python backend dispatches authenticated REST calls to the target system of record and commits an ACID transaction into a Unity Catalog Delta audit table."
        ),
        (
            "Q7: What is Delta Lake UniForm and why is it critical during an enterprise migration?",
            "Answer: Universal Format (UniForm) allows Delta Lake tables to generate Iceberg and Hudi metadata on write without duplicating the underlying Parquet data files. During a migration, this allows third-party query engines (Trino, Snowflake, AWS Athena) to read the newly migrated Lakehouse tables immediately as native Iceberg tables, proving zero lock-in and eliminating cross-platform migration silos."
        ),
        (
            "Q8: How does Palantir AIP compare to Databricks Mosaic AI?",
            "Answer: Palantir AIP connects LLMs directly to the Foundry Ontology as tool-calling agents with strict human-in-the-loop guardrails. Databricks Mosaic AI is a broader, open, developer-centric compound AI system comprising: Mosaic AI Agent Framework (LangChain/LlamaIndex integration), Vector Search (auto-syncing with Delta tables), Model Serving (serverless hosting for open and proprietary models), and Agent Evaluation (automated LLM-as-a-judge quality/toxicity benchmarking)."
        ),
        (
            "Q9: How do you migrate data out of Palantir Foundry safely?",
            "Answer: Palantir does not provide an automated 'export everything' button. Extraction strategies include:\n"
            "1. Foundry REST APIs / Data Export Gateway: Programmatically pulling datasets into cloud object storage in Parquet format.\n"
            "2. Magritte Outbound Connectors: Configuring outbound syncs from Foundry to target cloud storage buckets (S3/ADLS/GCS).\n"
            "3. Spark Direct Access / ODBC/JDBC Federation: Querying Foundry datasets via external Spark jobs with secure bearer tokens."
        ),
        (
            "Q10: What is the typical duration and phase structure of an enterprise Palantir migration?",
            "Answer: A standard enterprise migration spans 24 weeks across 6 phases: 1. Discovery & Inventory (W1-4), 2. Foundation & Governance (W4-8), 3. Ingestion & Historical Extraction (W8-12), 4. Transformation Refactoring (W12-18), 5. Apps, Semantic & AI Migration (W16-22), and 6. Parallel Run, Data Reconciliation & Decommissioning (W20-24+)."
        )
    ]

    for q, a in questions_and_answers:
        add_heading_2(doc, q)
        doc.add_paragraph(a)

    add_heading_1(doc, "3. System Design Scenarios & Practical Case Studies")

    add_heading_2(doc, "Scenario 1: Zero-Downtime Migration of a Global Mission-Critical Pipeline")
    doc.add_paragraph(
        "Context: An enterprise runs a mission-critical supply chain tracking pipeline in Palantir Foundry ingesting 100 million transactions daily from SAP and Kafka. Downtime SLA is 0%.\n\n"
        "Architectural Solution Blueprint:\n"
        "1. Dual-Ingest Setup: Replicate the Kafka topic consumer and deploy Databricks Auto Loader alongside existing Magritte agents.\n"
        "2. Parallel DLT Pipeline: Deploy Delta Live Tables pipeline writing to `enterprise_operations.silver.transactions`.\n"
        "3. Dual-Run Data Reconciliation: Run daily automated reconciliation scripts comparing Foundry output Parquet datasets with Delta Lake tables using checksum hashing and primary key verification.\n"
        "4. Operational App Cutover: Spin up Databricks App (Streamlit) pointing to Delta Gold tables. Perform pilot validation with 10% of users, gradually scaling to 100%.\n"
        "5. Final Decommission: Deprecate Foundry transforms after 30 days of 100% parity verification."
    )

    add_heading_2(doc, "Scenario 2: Handling Complex Foundry TypeScript Action Write-Backs")
    doc.add_paragraph(
        "Context: A healthcare customer uses Palantir Workshop to allocate organ donations. When a doctor clicks 'Accept Allocation', a TypeScript function executes complex business logic, checks patient compatibility, and writes to an external Oracle EHR system.\n\n"
        "Architectural Solution Blueprint:\n"
        "1. Refactor Logic to Python Service: Port TypeScript compatibility logic into a Python class hosted within a containerized Databricks App (FastAPI).\n"
        "2. State Consistency via Delta ACID: The Databricks App executes the external Oracle REST write and writes a corresponding record to `healthcare.audit.organ_allocations` in Delta Lake in a single atomic transaction block.\n"
        "3. Real-Time UI Feedback: Provide the doctor with instant status confirmation via Streamlit / React front-end."
    )

    add_heading_1(doc, "4. Code Refactoring Exercises (Foundry -> Databricks DLT)")
    doc.add_paragraph(
        "Interview Question: 'Convert the following proprietary Foundry transform into an enterprise-grade Databricks Delta Live Table pipeline with data quality rules.'\n\n"
        "Original Foundry Code:\n"
        "```python\n"
        "from transforms.api import transform_df, Input, Output\n\n"
        "@transform_df(\n"
        "    Output('/Clean/Orders'),\n"
        "    raw=Input('/Raw/SAP_Orders'),\n"
        "    cust=Input('/Clean/Customers')\n"
        ")\n"
        "def compute(raw, cust):\n"
        "    return raw.join(cust, 'customer_id').filter(raw.amount > 0)\n"
        "```\n\n"
        "Candidate's Ideal Databricks DLT Solution:\n"
        "```python\n"
        "import dlt\n"
        "from pyspark.sql import functions as F\n\n"
        "@dlt.table(\n"
        "    name='gold_orders',\n"
        "    comment='Cleaned orders with customer enrichment',\n"
        "    table_properties={\n"
        "        'quality': 'gold',\n"
        "        'delta.enableLiquidClustering': 'true'\n"
        "    }\n"
        ")\n"
        "@dlt.expect_or_drop('valid_customer_id', 'customer_id IS NOT NULL')\n"
        "@dlt.expect_or_fail('positive_order_amount', 'amount > 0')\n"
        "def gold_orders():\n"
        "    raw = dlt.read('silver_sap_orders')\n"
        "    cust = dlt.read('silver_customers')\n"
        "    return (\n"
        "        raw.join(cust, on='customer_id', how='inner')\n"
        "           .withColumn('migrated_at', F.current_timestamp())\n"
        "    )\n"
        "```"
    )

    add_heading_1(doc, "5. Executive Stakeholder Scenarios & Objection Handling")
    headers_objections = ["Stakeholder Objection / Challenge", "Best Practice Consultant Response (The 'Winning Formula')"]
    data_objections = [
        [
            "The Business VP says: 'Palantir built all our Workshop apps. Our people love them and don't want to change. Why should we risk switching?'",
            "'We completely respect how vital those workflows are to your daily operations. That is why our strategy does not ask your operators to change how they work. We build Databricks Apps with Streamlit that match the exact same forms, buttons, and layouts your team uses today. The difference is under the hood: your data is no longer locked in a proprietary silo. It updates faster, connects directly to all enterprise BI tools, and saves the company over $2M annually that can be reinvested into custom business features.'"
        ],
        [
            "The CFO asks: 'Palantir charges us a fixed contract. Databricks is consumption-based. Won't our costs explode with runaway queries?'",
            "'That is a common concern that we proactively solve on day one using Unity Catalog System Tables and automated FinOps cluster policies. We enforce auto-termination within 15 minutes of inactivity, cap compute sizes per department, and set programmatic budget alerts. Furthermore, because Databricks scales to zero when not running, you never pay for idle servers overnight or on weekends, unlike fixed platform contracts.'"
        ],
        [
            "The Chief InfoSec Officer (CISO) says: 'Palantir has DoD IL5 and IL6 security with Markings. Can Databricks match that level of defense-grade security?'",
            "'Yes. Databricks provides FedRAMP High, DoD IL5, HIPAA, and SOC 2 Type II compliance. With Unity Catalog Attribute-Based Access Control (ABAC), dynamic column masking, and row-level filtering, we implement the exact same Mandatory Access Controls (MAC) that Palantir Markings provide. Furthermore, because data resides in your own dedicated AWS/Azure cloud storage buckets, you retain 100% cryptographic control over your encryption keys via customer-managed keys (CMK).'"
        ]
    ]
    add_custom_table(doc, headers_objections, data_objections, [Inches(2.2), Inches(4.3)])

    add_heading_1(doc, "6. Candidate Checklist for Interview Day")
    doc.add_paragraph(
        "Before your technical and architectural interviews, ensure you have mastered:\n"
        "✔ Exact syntax of Delta Live Tables (`@dlt.table`, `@dlt.expect`, `dlt.read()` vs `dlt.read_stream()`).\n"
        "✔ Unity Catalog three-level namespace and dynamic security DDL (`ROW FILTER`, `COLUMN MASK`).\n"
        "✔ The 6-phase migration methodology and duration breakdown (24 weeks).\n"
        "✔ 3-year TCO financial rationale and numbers (e.g., 50%+ cost reduction, $6.8M cumulative savings).\n"
        "✔ Concrete architecture of Databricks Apps (hosting Streamlit for operational write-backs).\n"
        "✔ Mosaic AI components (Vector Search, Agent Framework, Model Serving, Evaluation).\n"
        "✔ Executive storytelling: how to articulate the business transition from proprietary lock-in to an open, scalable Data Intelligence Platform."
    )

    output_path = "/Users/josekurian/GoogleAutomation/AIPalatirToDatabricks/Palantir to Databricks Migration Consultant technical Interview Preparation Guide.docx"
    doc.save(output_path)
    print(f"Saved: {output_path}")

if __name__ == "__main__":
    build_interview_guide()
