import os
import docx
from docx.shared import Inches, Pt, RGBColor
from doc_helper import create_styled_document, add_heading_1, add_heading_2, add_heading_3, add_callout, add_custom_table

def build_migrations_doc():
    doc = create_styled_document(
        "Palantir to Databricks Comprehensive Enterprise Migration Blueprint",
        "Technical Playbook, Architectural Mappings, Pipeline Conversion, Ontology Translation, Risk Mitigation, and Cost Optimization"
    )
    
    add_callout(
        doc,
        "Migrating from Palantir Foundry to Databricks is fundamentally a transformation from an all-in-one proprietary operational application stack to an open, scalable enterprise Data Intelligence Platform. The migration must preserve data lineage, security classifications, and business semantics while refactoring proprietary Foundry constructs (Ontology, Actions, Workshop) into modern Lakehouse components (Unity Catalog, DLT, Databricks Apps, Mosaic AI).",
        "MIGRATION EXECUTIVE SUMMARY"
    )
    
    add_heading_1(doc, "1. Executive Overview & Migration Rationale")
    doc.add_paragraph(
        "Enterprises seeking to migrate from Palantir to Databricks commonly pursue several strategic business objectives:"
    )
    doc.add_paragraph(
        "1. Elimination of Proprietary Vendor Lock-In: Transitioning data assets to open standards (Delta Lake, Apache Iceberg, Apache Spark, MLflow) so enterprise data remains portable and accessible across multi-vendor tools.\n"
        "2. Dramatic Total Cost of Ownership (TCO) Reduction: Replacing expensive fixed multi-million dollar annual platform fees and high proprietary compute premiums (FCUs) with pure consumption-based, auto-scaling Databricks serverless compute.\n"
        "3. Modern Unified AI & Machine Learning Ecosystem: Unlocking the power of open-source frameworks, PyTorch, Hugging Face, Mosaic AI, and serverless LLMs without proprietary platform wrapper constraints.\n"
        "4. Seamless Ecosystem Interoperability: Direct query access for power BI tools (Power BI, Tableau, ThoughtSpot, Databricks AI/BI) and cloud-native services without passing through Foundry gateways."
    )
    
    add_heading_1(doc, "2. End-to-End Architectural Component Mapping")
    doc.add_paragraph(
        "The following matrix defines the exact 1-to-1 and 1-to-N technical mappings between Palantir Foundry components and their target Databricks Lakehouse equivalents:"
    )
    
    headers_map = ["Palantir Foundry Component", "Databricks Lakehouse Equivalent", "Migration Strategy & Technical Details"]
    data_map = [
        ["Foundry Datasets / Files", "Delta Lake Tables & Unity Catalog Volumes", "Export raw/Parquet data via Foundry APIs or Delta export; register into Unity Catalog schemas; convert to Delta with Liquid Clustering."],
        ["Data Connection & Magritte Agents", "Lakeflow Connect, Auto Loader, Partner Connect", "Replace Magritte agent connectors with native Databricks Lakeflow Connectors (SAP, Salesforce) and cloud storage Auto Loader."],
        ["Code Repositories (PySpark/SQL)", "Databricks Repos / Asset Bundles (DABs), Notebooks", "Direct translation of PySpark/SQL logic; strip proprietary Foundry transform decorators (`@transform`, `@input`); parameterize via DABs."],
        ["Pipeline Builder (Low-Code ETL)", "Delta Live Tables (DLT) & Lakeflow Pipelines", "Re-implement visual pipelines into declarative SQL/Python DLT syntax with built-in expectations (`@dlt.table`, `@dlt.expect`)."],
        ["Foundry Ontology (Objects & Links)", "Unity Catalog Three-Level Namespace + Semantic Views", "Map Object Types to curated Gold Delta tables with primary keys; map Link Types to foreign-key constraints or semantic layers (dbt / Cube)."],
        ["Ontology Actions & Write-Backs", "Databricks Apps (FastAPI / Streamlit) & Reverse ETL", "Refactor TypeScript Action functions into Python microservices hosted on Databricks Apps or reverse-ETL triggers (FiveTran, Hightouch) writing to source APIs."],
        ["Palantir Workshop / Slate Apps", "Databricks Apps (Streamlit / Dash) + AI/BI Dashboards", "Rebuild operational UI cockpits using Python Streamlit on Databricks Apps; replace BI dashboards with native Databricks AI/BI."],
        ["Contour & Quiver Analytics", "Databricks SQL & AI/BI Genie Spaces", "Convert point-and-click cohort analyses into Databricks SQL queries; configure AI/BI Genie for natural language data exploration."],
        ["Palantir AIP (Logic, Assist, Agents)", "Mosaic AI Agent Framework, Vector Search, Model Serving", "Migrate AIP chains into Mosaic AI Agent Framework; replace Foundry vector indices with Mosaic AI Vector Search endpoints."],
        ["Markings & Purpose-Based Access", "Unity Catalog Row Filters, Column Masks & ABAC", "Translate Palantir Markings into Unity Catalog Attribute-Based Access Control (ABAC) tags, dynamic column masking, and row-level security."],
        ["Foundry Builds & Job Scheduler", "Lakeflow Jobs (Databricks Workflows)", "Map Foundry multi-stage schedules into Databricks Lakeflow Jobs DAGs with automated alerts, concurrency policies, and cluster sizing."]
    ]
    add_custom_table(doc, headers_map, data_map, [Inches(1.8), Inches(2.0), Inches(2.7)])
    
    add_heading_1(doc, "3. Phased Migration Methodology (6-Phase Framework)")
    doc.add_paragraph(
        "A structured 6-phase migration roadmap designed to minimize operational risk and eliminate business disruption:"
    )
    
    headers_meth = ["Phase", "Duration", "Key Workstreams", "Deliverables & Checkpoints"]
    data_meth = [
        ["Phase 1: Discovery, Assessment & Inventory", "Weeks 1 - 4", "• Catalog all Foundry datasets, builds, repositories, and apps.\n• Identify data dependencies, ingestion frequencies, and consumer personas.\n• TCO analysis and Databricks architecture blueprinting.", "Comprehensive Migration Inventory, Pipeline Dependency Graph, Target Architecture Blueprint."],
        ["Phase 2: Lakehouse & Governance Foundation", "Weeks 4 - 8", "• Deploy Unity Catalog metastore, catalogs, and storage credentials.\n• Configure SSO, SCIM sync, and network security (PrivateLink).\n• Establish target Medallion schemas (Bronze/Silver/Gold).", "Production-ready Databricks Workspace & Unity Catalog Metastore; IAM & Network sign-off."],
        ["Phase 3: Historic Data Extraction & Ingestion Cutover", "Weeks 8 - 12", "• Bulk export historical data from Foundry to Cloud Storage (S3/ADLS/GCS).\n• Convert extracted Parquet files into Delta Lake tables.\n• Deploy Lakeflow Connect & Auto Loader pipelines for live ingestion.", "Historical data validated in Delta Lake; dual-ingestion verified in parallel."],
        ["Phase 4: Code & Transformation Pipeline Refactoring", "Weeks 12 - 18", "• Refactor Foundry PySpark transforms into Databricks Asset Bundles / DLT.\n• Replace proprietary Foundry decorators with native Spark code.\n• Implement Delta Live Tables data quality expectations.\n• Recreate scheduled DAGs in Databricks Workflows.", "100% automated pipelines running in Databricks; automated data reconciliation tests passing."],
        ["Phase 5: Semantic Layer, Apps & AI Migration", "Weeks 16 - 22", "• Map Foundry Object Types to Gold Delta views and semantic models.\n• Rebuild critical Workshop operational applications using Databricks Apps.\n• Transition AIP agents to Mosaic AI Agent Framework & Vector Search.\n• Build Databricks AI/BI Dashboards and Genie spaces.", "Databricks Apps operational; Mosaic AI agents deployed; user acceptance testing (UAT) completed."],
        ["Phase 6: Parallel Run, Validation & Decommissioning", "Weeks 20 - 24+", "• Execute dual-run parallel processing for 30 days.\n• Verify data integrity, query latency, and output consistency.\n• Cut over operational users to Databricks.\n• Archive historical Foundry artifacts and decommission Foundry tenant.", "Final Cutover Sign-Off; Foundry contract decommissioning; migration completion report."]
    ]
    add_custom_table(doc, headers_meth, data_meth, [Inches(1.2), Inches(1.0), Inches(2.3), Inches(2.0)])
    
    add_heading_1(doc, "4. Code & Pipeline Conversion: Step-by-Step Refactoring")
    doc.add_paragraph(
        "Palantir Foundry uses proprietary Python decorators (`@transform`, `@transform_df`) and build abstractions. In Databricks, these are refactored into native PySpark, Delta Live Tables (DLT), or Databricks Asset Bundles (DABs)."
    )
    
    add_heading_2(doc, "4.1 PySpark Refactoring Pattern")
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
    
    add_heading_2(doc, "4.2 Refactoring Palantir Ontology & Operational Actions")
    doc.add_paragraph(
        "Rebuilding the Palantir operational write-back loop in Databricks requires decoupling the semantic storage from the interactive action service:"
    )
    doc.add_paragraph(
        "• Data State: Store the entity digital twin as an ACID Delta Lake table in Unity Catalog (`gold.enterprise.customer_master`).\n"
        "• Read Queries: Serve real-time data to UI applications via Databricks SQL Serverless or Unity Catalog REST APIs.\n"
        "• Action Execution (Write-Back): Host a Databricks App (FastAPI / Streamlit) running within the customer VPC. When a user or agent clicks 'Approve Procurement' or 'Schedule Maintenance', the App executes a Python handler that updates the target ERP via REST/ODBC and records the state change into a Delta Lake audit table with ACID transactional consistency."
    )
    
    add_heading_1(doc, "5. Migration Risk Matrix & Mitigation Strategies")
    headers_risk = ["Identified Risk Category", "Potential Business Impact", "Severity", "Proactive Mitigation Strategy"]
    data_risk = [
        ["Data Drift & Discrepancies", "Inconsistent reports between Foundry and Databricks during cutover", "High", "Implement automated daily Bitwise/checksum row-level reconciliation pipelines using open-source `Great Expectations` or DLT expectations."],
        ["Proprietary Dependency Lock-In", "Difficulty extracting custom transforms locked in proprietary Palantir libraries", "Medium", "Identify proprietary Foundry helper functions early in Discovery; develop standard PySpark equivalent utility libraries in Databricks."],
        ["End-User Operational Friction", "Business operators accustomed to Workshop UI push back against new interfaces", "High", "Involve business operational champions in co-designing Databricks Apps (Streamlit) early; replicate exact UI layouts and color coding to ensure user familiarity."],
        ["Security & Entitlement Gaps", "Data exposed improperly due to misconfigured Unity Catalog permissions", "Critical", "Automate script-based translation of Foundry Marking entitlements into Unity Catalog ABAC tag assignments; validate with InfoSec before production cutover."],
        ["Extended Parallel Run Costs", "Paying for both Palantir enterprise licenses and Databricks compute simultaneously", "Medium", "Establish strict milestone deadlines and timebox dual-run testing to a maximum of 30 days per operational domain."]
    ]
    add_custom_table(doc, headers_risk, data_risk, [Inches(1.5), Inches(1.8), Inches(0.9), Inches(2.3)])
    
    add_heading_1(doc, "6. Post-Migration TCO Optimization & Expected ROI")
    doc.add_paragraph(
        "Enterprises completing migrations from Palantir to Databricks typically achieve substantial structural cost reductions and architectural agility:"
    )
    doc.add_paragraph(
        "• Direct Licensing Savings: Reduction in software platform licensing expenditure by 40% to 65% by moving from high fixed annual platform contracts to consumption-based Databricks Units (DBUs).\n"
        "• Professional Services Optimization: Elimination of required continuous Forward Deployed Engineering (FDE) retainers; work is transitioned to internal data engineering teams using standard Python and SQL skill sets.\n"
        "• Storage & Compute Efficiency: Delta Lake with Photon vectorized execution and Liquid Clustering reduces cloud compute consumption by 30-50% compared to legacy Spark setups.\n"
        "• Talent Acquisition & Agility: Standard open-source Apache Spark, Python, SQL, and MLflow skill sets are vastly more abundant in the global talent market than proprietary Palantir Foundry engineers."
    )
    
    output_path = "/Users/josekurian/GoogleAutomation/AIPalatirToDatabricks/Migrations/Palantir_to_Databricks_Migration_Guide.docx"
    doc.save(output_path)
    print(f"Saved: {output_path}")

if __name__ == "__main__":
    build_migrations_doc()
