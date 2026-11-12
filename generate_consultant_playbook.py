import os
import docx
from docx.shared import Inches, Pt, RGBColor
from doc_helper import create_styled_document, add_heading_1, add_heading_2, add_heading_3, add_callout, add_custom_table

def build_consultant_playbook():
    doc = create_styled_document(
        "Palantir to Databricks Migration Consultant Playbook",
        "Strategic Enterprise Advisory, Architecture Modernization, Cost Rationalization, and Cutover Delivery Framework"
    )

    add_callout(
        doc,
        "As a Migration Consultant leading a Palantir-to-Databricks initiative, your mandate is not merely a technical code lift-and-shift. You are steering an architectural modernization: decoupling proprietary lock-in, shifting from rigid all-in-one operational silos to an open Lakehouse and Data Intelligence Platform, preserving operational action loops via Databricks Apps, and capturing 40% to 65% in structural TCO reductions.",
        "CONSULTANT CHARTER & CORE MANDATE"
    )

    add_heading_1(doc, "1. Executive Advisory & Engagement Framework")
    doc.add_paragraph(
        "Migrating an enterprise from Palantir Foundry to Databricks represents a fundamental organizational and technical pivot. Palantir typically embeds Forward Deployed Engineers (FDEs) deeply into business units, while Databricks empowers customer-owned engineering teams on open standards. A successful consultant must align both C-suite business stakeholders and hands-on data engineers."
    )

    headers_stakeholders = ["Stakeholder Persona", "Primary Concerns / Motivations", "Consultant Positioning & Value Proposition"]
    data_stakeholders = [
        ["Chief Information / Technology Officer (CIO/CTO)", "Eliminating multi-million dollar vendor lock-in, multi-cloud flexibility, tech stack consolidation.", "Demonstrate open standards (Delta Lake, Apache Iceberg, MLflow), cloud independence, and alignment with modern AI ecosystems."],
        ["Chief Financial Officer (CFO)", "Massive annual licensing costs, unpredictable Foundry Compute Unit (FCU) spikes, expensive FDE retainers.", "Present detailed TCO financial model proving 40-65% software savings, scale-to-zero serverless billing, and transparent FinOps system tables."],
        ["Chief Data & Analytics Officer (CDAO)", "Data accessibility across BI tools, ML engineering agility, modern data governance.", "Highlight Unity Catalog cross-workspace governance, automated column lineage, and seamless interoperability with Power BI, Tableau, and Mosaic AI."],
        ["Business Operations Leads (Foundry Users)", "Fear of losing Palantir Workshop operational dashboards, decision cockpits, and ERP write-back actions.", "Reassure and demonstrate Databricks Apps (Python Streamlit/Dash) and AI/BI Genie, preserving equivalent operational workflows with superior flexibility."],
        ["Lead Data Engineers & Architects", "Complexity of rewriting transforms, preserving data pipelines, SLA guarantees during cutover.", "Provide automated code translation scripts (`@transform_df` -> DLT), declarative pipelines with expectations, and DABs CI/CD automation."]
    ]
    add_custom_table(doc, headers_stakeholders, data_stakeholders, [Inches(1.8), Inches(2.2), Inches(2.5)])

    add_heading_1(doc, "2. Pre-Migration Discovery, Audit & TCO Rationalization")
    doc.add_paragraph(
        "Before touching code or cloud infrastructure, the consultant must execute a thorough 4-week architectural discovery and inventory audit across the Palantir Foundry estate."
    )

    add_heading_2(doc, "2.1 The 4-Week Discovery Workstream")
    doc.add_paragraph(
        "• Workstream 1: Inventory Cataloging: Extract the complete catalog of Foundry datasets, build schedules, Code Repositories, Pipeline Builder graphs, Contour analyses, Quiver dashboards, Workshop applications, and AIP Agent specifications.\n"
        "• Workstream 2: Dependency & Provenance Mapping: Map dataset dependencies from upstream Magritte agents down to operational Workshop consumption points to establish migration waves.\n"
        "• Workstream 3: Security & Classification Mapping: Audit Palantir Markings, Mandatory Access Control (MAC) tags, and Purpose-based policies to prepare Unity Catalog ABAC and row/column security translation.\n"
        "• Workstream 4: FinOps Baseline Assessment: Audit annual Palantir software subscriptions, compute unit (FCU) consumption, cloud VM pass-through expenses, and FDE services retainers."
    )

    add_heading_2(doc, "2.2 Enterprise TCO Rationalization Model")
    headers_tco = ["Cost Category", "Current Palantir Baseline (Annual)", "Target Databricks Lakehouse (Annual)", "Consultant Net Financial Impact"]
    data_tco = [
        ["Platform Software License", "$2,200,000 (Fixed Enterprise Agreement)", "$950,000 (Consumption-based DBUs)", "$1,250,000 savings (57% direct licensing reduction)"],
        ["Cloud Storage & Compute", "$850,000 (Proprietary compute wrappers)", "$620,000 (Photon engine + Liquid Clustering)", "$230,000 savings (vectorized C++ efficiency)"],
        ["External Professional Services", "$1,200,000 (Dedicated FDE retainer)", "$300,000 (Initial onboarding advisory)", "$900,000 savings (empowers internal engineering)"],
        ["Internal Talent Headcount", "$300,000 (Proprietary skill premiums)", "$400,000 (Broader market Spark/Python talent)", "-$100,000 investment in customer internal team"],
        ["Total Annual Run-Rate", "$4,550,000 / year", "$2,270,000 / year", "$2,280,000 net annual savings (50.1% reduction)"]
    ]
    add_custom_table(doc, headers_tco, data_tco, [Inches(1.6), Inches(1.6), Inches(1.6), Inches(1.7)])

    add_heading_1(doc, "3. Architectural Target State: The Open Data Intelligence Platform")
    doc.add_paragraph(
        "The consultant must guide the client away from attempting to build a 1:1 replica of Foundry's black-box internals. Instead, architect a clean, modular Lakehouse solution:"
    )
    doc.add_paragraph(
        "1. Open Storage Foundation: Delta Lake with UniForm (allowing Apache Iceberg access) stored in customer-owned cloud object storage (S3/ADLS/GCS), eliminating data egress barriers.\n"
        "2. Centralized Governance (Unity Catalog): Single pane of glass for all structured data, unstructured files (Volumes), ML models, and metrics across all clouds and workspaces.\n"
        "3. Declarative Pipelines (Delta Live Tables & Lakeflow): Replacing proprietary Foundry transform logic with standard Python/SQL pipelines governed by data quality expectations (`@dlt.expect_or_drop`).\n"
        "4. Operational Front-End (Databricks Apps + AI/BI): Hosting Streamlit and FastAPI within the Databricks control plane to preserve operational user cockpits and trigger verified REST write-backs into ERP/CRM systems.\n"
        "5. Generative AI & Compound AI (Mosaic AI): Replacing Palantir AIP with Mosaic AI Agent Framework, managed Vector Search, and Model Serving endpoints under MLflow evaluation governance."
    )

    add_heading_1(doc, "4. Step-by-Step Delivery Playbook: 6-Phase Migration Methodology")
    headers_playbook = ["Phase", "Timeline", "Consultant Deliverables", "Exit Criteria & Quality Gates"]
    data_playbook = [
        ["Phase 1: Discovery & Strategy", "Weeks 1 - 4", "Migration Charter, Asset Inventory, Dependency Graph, Target Architecture Blueprint, TCO Business Case.", "Executive Steering Committee sign-off on scope, budget, and wave sequencing."],
        ["Phase 2: Foundation & Governance", "Weeks 4 - 8", "Unity Catalog Metastore deployment, SCIM IdP integration, VPC PrivateLink, Bronze/Silver/Gold schema hierarchy, ABAC/Masking rules.", "InfoSec approval of network topology, RBAC/ABAC policies, and service principal authentication."],
        ["Phase 3: Ingestion & Bulk Extraction", "Weeks 8 - 12", "Historical data bulk export from Foundry to S3/ADLS; Delta conversion; deployment of Lakeflow Connect & Auto Loader for streaming feeds.", "Historical data row-count parity validated; live parallel feeds ingesting without lag."],
        ["Phase 4: Transformation Refactoring", "Weeks 12 - 18", "Conversion of Foundry PySpark transforms into DLT pipelines; migration of Pipeline Builder workflows; Databricks Asset Bundles (DABs) CI/CD.", "Automated data reconciliation passing (zero critical field discrepancies); pipeline SLAs verified."],
        ["Phase 5: Apps, Semantic & AI Migration", "Weeks 16 - 22", "Rebuilding Workshop apps in Databricks Apps (Streamlit); AI/BI Dashboards & Genie spaces; AIP to Mosaic AI Agent Framework migration.", "User Acceptance Testing (UAT) sign-off from business operations leads; agent guardrail tests passed."],
        ["Phase 6: Parallel Run & Decommissioning", "Weeks 20 - 24+", "Dual-run production operation (30 days); end-user training cohorts; operational cutover; Foundry tenant archiving and contract off-ramp.", "Formal cutover certification sign-off; decommissioning of Foundry infrastructure; contract termination."]
    ]
    add_custom_table(doc, headers_playbook, data_playbook, [Inches(1.2), Inches(1.1), Inches(2.3), Inches(1.9)])

    add_heading_1(doc, "5. Translating Proprietary Palantir Paradigms into Databricks")

    add_heading_2(doc, "5.1 Decoupling the Palantir Ontology")
    doc.add_paragraph(
        "The consultant must guide architects on how to decouple the Palantir Ontology into modular Lakehouse services:\n"
        "• Object Types: Converted into curated, deduplicated Gold Delta tables in Unity Catalog with enforced primary key constraints and Liquid Clustering.\n"
        "• Link Types: Converted into declared foreign-key constraints in Unity Catalog or semantic join definitions in semantic partner layers (e.g., Cube, dbt semantic layer).\n"
        "• Actions & Write-Backs: Decoupled into Python microservice handlers running inside Databricks Apps (FastAPI/Streamlit). When an operational user approves an action, the app executes an audited API call to SAP/Salesforce and logs the event to a Delta audit table.\n"
        "• Functions on Objects: Translated to SQL User-Defined Functions (UDFs) or Python vectorized functions executed in sub-second latency by the Photon engine."
    )

    add_heading_2(doc, "5.2 Translating Palantir Markings to Unity Catalog ABAC")
    doc.add_paragraph(
        "Palantir Markings represent Mandatory Access Control (MAC). In Databricks, this is translated to Attribute-Based Access Control (ABAC):\n"
        "1. Tagging: Assign metadata tags to Unity Catalog catalogs, schemas, tables, and columns (e.g., `SET TAG 'classification' = 'ITAR'`).\n"
        "2. Dynamic Row Filtering: Apply SQL filter functions that evaluate `is_account_group_member()` or session attributes.\n"
        "3. Column Masking: Apply hashing or partial masking functions (e.g., SSN, PII, financial amounts) based on role entitlement."
    )

    add_heading_1(doc, "6. Risk Management, Change Management & Governance")
    headers_risks = ["Risk Vector", "Business Impact", "Severity", "Consultant Mitigation Blueprint"]
    data_risks = [
        ["End-User Workshop Attachment", "Operations staff resist moving away from familiar Palantir Workshop screens.", "High", "Deploy Databricks Apps (Streamlit) mimicking the exact UI layout, color schemes, and action workflows; conduct hands-on training workshops."],
        ["Data Reconciliation Failures", "Differences between Foundry Parquet outputs and Databricks Delta tables erode stakeholder trust.", "Critical", "Run automated dual-system reconciliation suites verifying bitwise row counts, primary key integrity, and numeric column distributions daily."],
        ["Extended Parallel Run Budget Overrun", "Paying dual platform bills for more than 60 days.", "Medium", "Establish strict, domain-by-domain cutover dates with pre-agreed acceptance criteria to prevent open-ended dual-run testing."],
        ["Loss of FDE Tribal Knowledge", "Palantir FDEs depart without documenting custom Python/TypeScript transform nuances.", "High", "Mandate comprehensive code walkthroughs during Phase 1 Discovery; reverse-engineer pipelines directly from Foundry Code Repositories Git histories."]
    ]
    add_custom_table(doc, headers_risks, data_risks, [Inches(1.5), Inches(1.8), Inches(0.9), Inches(2.3)])

    add_heading_1(doc, "7. Advisory Engagement Deliverables & Success Metrics")
    doc.add_paragraph(
        "A senior Migration Consultant should deliver the following tangible artifacts across the lifecycle:\n"
        "• Enterprise Migration Charter & Scope Statement\n"
        "• Comprehensive Foundry Asset & Dependency Inventory (Excel / CSV / DB Table)\n"
        "• 3-Year TCO & Cost Rationalization Business Case\n"
        "• Target Lakehouse Architecture Design Document (ADD)\n"
        "• Automated Pipeline Conversion Scripts (`@transform` -> DLT)\n"
        "• Unity Catalog Governance & ABAC Security Blueprint\n"
        "• Databricks Apps Operational Template Repository\n"
        "• Automated Data Parity & Reconciliation Report Suite\n"
        "• Production Cutover Audit Certificate & Off-Ramp Sign-Off"
    )

    output_path = "/Users/josekurian/GoogleAutomation/AIPalatirToDatabricks/Palantir to Databricks Migration Consultant.docx"
    doc.save(output_path)
    print(f"Saved: {output_path}")

if __name__ == "__main__":
    build_consultant_playbook()
