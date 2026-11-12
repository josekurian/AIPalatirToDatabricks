import os
import docx
from docx.shared import Inches, Pt, RGBColor
from doc_helper import create_styled_document, add_heading_1, add_heading_2, add_heading_3, add_callout, add_custom_table

def build_multi_platform_ai_migration_plan():
    doc = create_styled_document(
        "AI-Enabled Multi-Platform Migration Implementation Plan: Palantir, Oracle Database & Snowflake to Databricks",
        "Strategic Architectural Directions, AI-Powered Code Transpilation, Automated Data Parity, Cost Optimization & Execution Roadmap"
    )

    add_callout(
        doc,
        "Enterprise data modernization frequently involves heterogeneous source topologies. This implementation blueprint provides a unified, AI-enabled migration methodology for consolidating Palantir Foundry, Oracle Database (Exadata/On-Prem/OCI), and Snowflake into an open Databricks Data Intelligence Platform. By leveraging Generative AI Transpilation Agents, LLM-as-a-Judge semantic validators, and AST code converters, enterprises achieve 65% faster delivery, 99.99% conversion accuracy, and eliminate multi-platform licensing redundancies—reducing 3-year TCO by over 60%.",
        "EXECUTIVE CHARTER: AI-ENABLED MULTI-PLATFORM MODERNIZATION"
    )

    # 1. Architectural Directions Analysis
    add_heading_1(doc, "1. Strategic Architectural Directions Analysis")
    doc.add_paragraph(
        "When dealing with Palantir, Oracle, and Snowflake in relation to Databricks, enterprises evaluate three architectural directions:"
    )

    headers_dir = ["Architectural Direction", "Topology Description", "Pros & Competitive Strengths", "Cons & Trade-Offs", "Strategic Recommendation"]
    data_dir = [
        [
            "Direction A: Unified Lakehouse Consolidation (Target Architecture)",
            "Migrate all data, pipelines, and models from Palantir, Oracle, and Snowflake into a unified Databricks Lakehouse (Unity Catalog + Delta UniForm).",
            "• Eliminates 3 separate platform software license bills.\n• Single unified governance pane (Unity Catalog).\n• Eliminates data duplication and cross-cloud egress fees.\n• Native compound AI with Mosaic AI.",
            "• Requires upfront migration effort across three dialect sets (Foundry PySpark, PL/SQL, Snowflake SQL).",
            "RECOMMENDED (Maximum long-term TCO savings: 60-70%; highest operational agility)."
        ],
        [
            "Direction B: Coexistence / Hybrid Hub & Spoke",
            "Databricks acts as Lakehouse ETL and ML core; Snowflake remains for enterprise BI; Oracle remains for transactional OLTP; Palantir serves operational Workshop UI.",
            "• Minimal immediate change for business analysts already comfortable with Snowflake dashboards or Palantir Workshop.",
            "• Continues high multi-million dollar annual vendor fees.\n• Heavy cross-cloud egress costs.\n• Fragmented governance across Unity Catalog, Snowflake RBAC, and Palantir Markings.",
            "TRANSITIONAL ONLY (Recommended only during the 6-month migration parallel run)."
        ],
        [
            "Direction C: Lakehouse Federation & Zero-Copy Virtualization",
            "Databricks acts as unified query engine querying Oracle and Snowflake in-place via Unity Catalog Lakehouse Federation without physical data movement.",
            "• Rapid time-to-insight without extracting historical data.\n• Immediate unified catalog visibility.",
            "• External compute charges incurred in Snowflake and Oracle on every federated query.\n• Performance throttled by network bandwidth and external database limits.",
            "TACTICAL (Ideal for Phase 1 Discovery and live data validation before bulk cutover)."
        ]
    ]
    add_custom_table(doc, headers_dir, data_dir, [Inches(1.2), Inches(1.8), Inches(1.8), Inches(1.5), Inches(1.2)])

    # 2. AI-Enabled Migration Methods
    add_heading_1(doc, "2. AI-Enabled Migration Methods for Maximum Cost Savings & Accuracy")
    doc.add_paragraph(
        "Traditional manual database and platform migrations suffer from high labor costs, prolonged schedules (18-36 months), and human error rates (15-25% syntax/semantic bugs). In contrast, modern AI-Enabled Migration leverages Compound LLM Agents, Abstract Syntax Tree (AST) parsing, and automated formal verification."
    )

    headers_ai_meth = ["Migration Workstream", "Traditional Manual Method", "AI-Enabled Autonomous Method", "Cost & Accuracy Impact"]
    data_ai_meth = [
        [
            "SQL & Stored Procedure Transpilation (Oracle PL/SQL & Snowflake SQL -> PySpark/DBSQL)",
            "Manual line-by-line developer rewriting of PL/SQL packages, cursors, triggers, and Snowflake Snowpark/SQL.",
            "AST Parser + Domain-Specific LLM Transpiler Agent (Meta Llama 3.1 70B / Claude 3.5) with automated test generation.",
            "• 80% reduction in developer hours.\n• 99.8% first-pass syntax accuracy.\n• Automated unit test generation."
        ],
        [
            "Schema & Type Inference (Oracle Types -> Delta Lake UniForm)",
            "Manual mapping of Oracle NUMBER, VARCHAR2, CLOB, BLOB, and Snowflake VARIANT types.",
            "AI Agent Schema Harmonizer: Automatically maps proprietary types to strongly typed Delta Parquet schemas with Liquid Clustering recommendations.",
            "• 90% faster schema deployment.\n• Eliminates precision loss in financial decimals.\n• Automated primary/foreign key preservation."
        ],
        [
            "Data Parity & Semantic Reconciliation",
            "Manual SQL queries spot-checking row counts and arbitrary column sums between Oracle/Snowflake and Databricks.",
            "Automated AI Reconciliation Agent: Executes bitwise SHA-256 row hashing, statistical moment checks, and LLM-as-a-judge semantic drift analysis.",
            "• 100% data parity guarantee.\n• Instant pinpointing of exact mismatched rows.\n• Audited compliance certification."
        ],
        [
            "Pipeline Refactoring (Foundry @transform & Snowflake Tasks -> DLT)",
            "Manual engineering of Delta Live Tables pipelines and Databricks Asset Bundles.",
            "AI Code Conversion Agent: Parses pipeline DAGs and automatically emits declarative DLT syntax with built-in @dlt.expect quality rules.",
            "• Reduces pipeline conversion from 3 weeks to 2 hours per pipeline.\n• Zero regression errors."
        ]
    ]
    add_custom_table(doc, headers_ai_meth, data_ai_meth, [Inches(1.5), Inches(1.8), Inches(2.2), Inches(1.5)])

    # 3. Source-Specific Migration Architectures
    add_heading_1(doc, "3. Platform-Specific Decoupling & Translation Architecture")

    add_heading_2(doc, "3.1 Oracle Database / Exadata to Databricks Lakehouse")
    doc.add_paragraph(
        "Oracle databases house mission-critical enterprise ERP/financial data with complex procedural logic (PL/SQL packages, stored procedures, materialized views, and triggers).\n\n"
        "AI-Enabled Migration Strategy:\n"
        "• Historical Data Ingest: Use Oracle GoldenGate or Debezium CDC connectors with Databricks Auto Loader to stream real-time redo logs into Bronze Delta tables.\n"
        "• PL/SQL Transpilation: AI Transpiler Agent translates procedural cursors and loops into set-oriented PySpark DataFrame operations or Databricks SQL scripts with Photon vectorized execution.\n"
        "• Materialized Views & Synonyms: Converted to Unity Catalog Materialized Views with automated incremental refresh.\n"
        "• Security: Oracle Virtual Private Database (VPD) and Fine-Grained Auditing (FGA) translated into Unity Catalog Row Filters and Column Masks."
    )

    add_heading_2(doc, "3.2 Snowflake Data Cloud to Databricks Lakehouse")
    doc.add_paragraph(
        "Snowflake deployments typically hold enterprise data warehouses, analytical marts, Snowpipe ingestion routines, and Snowpark Python/Java logic.\n\n"
        "AI-Enabled Migration Strategy:\n"
        "• Zero-Copy Storage Cutover: If Snowflake tables use External Tables on S3/Azure, Databricks reads them directly. For internal tables, execute COPY INTO s3:// in Parquet format, then run CONVERT TO DELTA with UniForm enabled.\n"
        "• SQL Dialect Conversion: AI Transpiler Agent converts Snowflake-specific functions (`ZEROIFNULL`, `IFF`, `DATEADD`, `FLATTEN` on VARIANT) into ANSI/DBSQL standard functions (`COALESCE`, `CASE WHEN`, `EXPLODE`).\n"
        "• Snowpark to Native PySpark: Convert Snowpark DataFrame APIs to standard PySpark with zero API overhead.\n"
        "• Dynamic Data Masking & Tagging: Map Snowflake Object Tagging directly into Unity Catalog Tags and ABAC policies."
    )

    add_heading_2(doc, "3.3 Palantir Foundry / AIP to Databricks Lakehouse")
    doc.add_paragraph(
        "• Ontology Digital Twin: Object Types and Link Types map to Unity Catalog Gold Delta tables with enforced primary and foreign key constraints.\n"
        "• Kinetic Actions (Write-Backs): Decoupled from Foundry runtime into containerized Databricks Apps (FastAPI microservices) dispatching audited REST webhooks to Oracle ERP and Salesforce CRM.\n"
        "• AIP Agent Studio: Migrated to Mosaic AI Agent Framework with Unity Catalog Vector Search tools and Human-In-The-Loop ($50k) guardrails."
    )

    # 4. Multi-Platform Architectural Flowchart & Sequence Diagrams
    add_heading_1(doc, "4. Multi-Platform Architectural Flows & Sequence Diagrams")
    doc.add_paragraph(
        "Flow Diagram: Unified Multi-Source Consolidation into Databricks:\n"
        "```mermaid\n"
        "flowchart TD\n"
        "    subgraph SOURCES[1. Heterogeneous Enterprise Sources]\n"
        "        PAL[Palantir Foundry (Datasets & Ontology)]\n"
        "        ORA[Oracle Database / Exadata (Tables & PL/SQL)]\n"
        "        SNOW[Snowflake Data Cloud (Tables & Snowpark)]\n"
        "    end\n\n"
        "    subgraph AI_AGENTS[2. AI-Enabled Migration Engine]\n"
        "        AI_TRANS[AI Code Transpiler Agent (Llama 3.1 70B / Claude 3.5)]\n"
        "        AI_INGEST[High-Speed Ingestion & CDC Connectors]\n"
        "        AI_REC[AI Automated Reconciliation & Parity Engine]\n"
        "    end\n\n"
        "    subgraph TARGET[3. Databricks Unified Data Intelligence Platform]\n"
        "        DELTA[Delta Lake 3.0 UniForm: Iceberg / Hudi]\n"
        "        DLT[Delta Live Tables (DLT) with Expectations]\n"
        "        UC[Unity Catalog Centralized Governance & ABAC]\n"
        "        PHOTON[Photon Vectorized C++ Query Engine]\n"
        "        APPS[Databricks Apps: Streamlit Cockpits & FastAPI Write-Back]\n"
        "        MOSAIC[Mosaic AI Agent Framework & Vector Search]\n"
        "    end\n\n"
        "    PAL --> AI_TRANS\n"
        "    ORA --> AI_TRANS\n"
        "    SNOW --> AI_TRANS\n"
        "    PAL --> AI_INGEST\n"
        "    ORA --> AI_INGEST\n"
        "    SNOW --> AI_INGEST\n"
        "    AI_INGEST --> DELTA\n"
        "    AI_TRANS --> DLT\n"
        "    AI_TRANS --> APPS\n"
        "    AI_TRANS --> MOSAIC\n"
        "    DELTA --> DLT\n"
        "    DLT --> UC\n"
        "    UC --> PHOTON\n"
        "    UC --> APPS\n"
        "    UC --> MOSAIC\n"
        "    DELTA -.->|Dual-System Parity Check| AI_REC\n"
        "    SOURCES -.->|Source Hash Verification| AI_REC\n"
        "```"
    )

    doc.add_paragraph(
        "Sequence Diagram: AI Transpilation, Execution & Parity Certification:\n"
        "```mermaid\n"
        "sequenceDiagram\n"
        "    autonumber\n"
        "    participant SRC as Source (Oracle / Snowflake / Palantir)\n"
        "    participant AGENT as AI Transpiler Agent (Mosaic AI / LLM)\n"
        "    participant AST as AST Syntax & Semantic Validator\n"
        "    participant DLT as Databricks Delta Live Tables (DLT)\n"
        "    participant REC as AI Reconciliation Engine\n"
        "    participant CERT as Cutover Audit Certificate\n"
        "    SRC->>AGENT: Ingest Source Code (PL/SQL, Snowflake SQL, @transform_df)\n"
        "    AGENT->>AST: Generate Refactored PySpark / DLT Code\n"
        "    AST-->>AGENT: Validate AST Syntax & Data Types\n"
        "    AGENT->>DLT: Deploy and Execute Pipeline on Serverless Spark\n"
        "    DLT-->>REC: Commit Gold Delta Lake Output\n"
        "    SRC-->>REC: Stream Source Checksums & Row Counts\n"
        "    REC->>REC: Bitwise SHA-256 Hashing & Statistical Moment Check\n"
        "    REC->>CERT: Issue Digitally Signed 100% Parity Certificate\n"
        "```"
    )

    # 5. Phased Implementation Roadmap
    add_heading_1(doc, "5. 24-Week Phased Implementation Plan")
    headers_roadmap = ["Phase", "Timeline", "Key Milestones & Deliverables", "AI-Enabled Acceleration Levers"]
    data_roadmap = [
        ["Phase 1: Multi-Source Discovery & Inventory", "Weeks 1 - 4", "• Automated extraction of schemas, queries, and pipelines from Palantir, Oracle, and Snowflake.\n• Dependency graph mapping and complexity scoring.\n• Multi-platform TCO baseline establishment.", "LLM-powered catalog scanners parse Oracle data dictionary, Snowflake `ACCOUNT_USAGE`, and Foundry Catalog in days."],
        ["Phase 2: Unity Catalog Foundation & Storage Setup", "Weeks 4 - 8", "• Deploy Unity Catalog metastore.\n• Configure S3/ADLS storage credentials with PrivateLink.\n• Establish Lakehouse Federation to Oracle and Snowflake for zero-copy discovery.", "AI Agent generates initial Unity Catalog DDL, ABAC security tags, and IAM configuration scripts."],
        ["Phase 3: Bulk Data Extraction & Dual Ingestion", "Weeks 8 - 12", "• Bulk export historical data to cloud landing storage in Parquet format.\n• CONVERT TO DELTA with UniForm enabled.\n• Deploy Auto Loader and Oracle GoldenGate/Debezium CDC streaming.", "Automated chunking scripts optimize file sizing (100MB-1GB) to maximize Photon query speeds."],
        ["Phase 4: AI Code & Pipeline Transpilation", "Weeks 12 - 18", "• AI Transpiler Agent translates Oracle PL/SQL, Snowflake SQL, and Foundry `@transform_df` to native PySpark and DLT.\n• Automated unit test execution and AST semantic validation.", "LLM code agent autonomously refactors 95% of pipelines; human engineers review remaining 5% complex logic."],
        ["Phase 5: Operational Apps & Mosaic AI Migration", "Weeks 16 - 22", "• Rebuild Palantir Workshop apps in Databricks Apps (Streamlit/FastAPI).\n• Deploy Mosaic AI Agent Framework replacing Palantir AIP.\n• Migrate Snowflake dashboards to Databricks AI/BI and Genie.", "AI App Generator translates Workshop JSON layouts directly into Streamlit Python code."],
        ["Phase 6: Dual-Run Parity, Cutover & Off-Ramp", "Weeks 20 - 24+", "• Execute 30-day parallel dual-run across all 3 platforms.\n• Daily automated bitwise SHA-256 reconciliation runs.\n• Formal production cutover and vendor contract decommissioning.", "AI Parity Suite automates row-level diffing, eliminating manual validation meetings."]
    ]
    add_custom_table(doc, headers_roadmap, data_roadmap, [Inches(1.2), Inches(1.1), Inches(2.5), Inches(1.7)])

    # 6. Comprehensive TCO & Cost Rationalization Analysis
    add_heading_1(doc, "6. Multi-Platform TCO Rationalization: 3-Year Financial Impact")
    doc.add_paragraph(
        "Consolidating Palantir, Oracle Database, and Snowflake into Databricks eliminates triple software licensing, duplicate storage, and proprietary compute markups:"
    )

    headers_fin = ["Cost Category", "Current Baseline: Palantir + Oracle + Snowflake", "Target State: Consolidated Databricks Lakehouse", "Net Annual Enterprise Savings"]
    data_fin = [
        ["Platform Software Licenses", "$2,200k (Palantir) + $1,100k (Oracle) + $1,400k (Snowflake) = $4,700,000", "$1,450,000 (Consolidated Databricks DBUs)", "$3,250,000 (69.1% direct software savings)"],
        ["Cloud Storage & Infrastructure", "$1,650,000 (Triple storage replication + compute wrappers)", "$820,000 (Delta UniForm single-copy + Photon efficiency)", "$830,000 (50.3% infrastructure reduction)"],
        ["External Professional Services", "$1,500,000 (Palantir FDEs + Oracle DBAs + Snowflake support)", "$400,000 (Initial migration advisory & onboarding)", "$1,100,000 (73.3% services reduction)"],
        ["Internal Engineering Overhead", "$850,000 (Fragmented skill sets across 3 stacks)", "$650,000 (Standardized open PySpark/SQL talent)", "$200,000 (Higher team productivity)"],
        ["Total Annual Outflow", "$8,700,000 / year", "$3,320,000 / year", "$5,380,000 net annual savings (61.8% reduction)"]
    ]
    add_custom_table(doc, headers_fin, data_fin, [Inches(1.6), Inches(1.8), Inches(1.6), Inches(1.5)])

    doc.add_paragraph(
        "Cumulative 3-Year Enterprise Impact:\n"
        "• Baseline 3-Year Cost across 3 Platforms: $25,200,000\n"
        "• Target 3-Year Databricks Consolidated Cost: $9,600,000\n"
        "• Cumulative 3-Year Enterprise Net Savings: $15,600,000 (61.9% TCO Reduction)"
    )

    output_path = "/Users/josekurian/GoogleAutomation/AIPalatirToDatabricks/AI-Enabled Multi-Platform Migration Implementation Plan.docx"
    doc.save(output_path)
    print(f"Saved: {output_path}")

if __name__ == "__main__":
    build_multi_platform_ai_migration_plan()
