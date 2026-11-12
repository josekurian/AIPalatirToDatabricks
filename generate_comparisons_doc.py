import os
import docx
from docx.shared import Inches, Pt, RGBColor
from doc_helper import create_styled_document, add_heading_1, add_heading_2, add_heading_3, add_callout, add_custom_table

def build_comparisons_doc():
    doc = create_styled_document(
        "Palantir vs. Databricks: Comprehensive Architectural Comparison & Capability Matrix",
        "In-Depth Evaluation of Philosophy, Storage, Governance, Ontology vs. Lakehouse, Generative AI, TCO, and Strategic Fit"
    )
    
    add_callout(
        doc,
        "Palantir is an 'Operational Decision Application' platform built from the top down (Ontology -> Actions -> Operations), whereas Databricks is an 'Open Data Intelligence & Lakehouse' platform built from the bottom up (Storage -> Unified Engine -> Governance -> AI & Apps). Choosing between them depends on whether your organization prioritizes rapid closed-loop operational workflows or an open, scalable enterprise data foundation.",
        "CORE ARCHITECTURAL THESIS"
    )
    
    add_heading_1(doc, "1. Executive Philosophy & Strategic Positioning")
    doc.add_paragraph(
        "While both Palantir (Foundry/AIP) and Databricks (Data Intelligence Platform/Mosaic AI) compete for enterprise AI budgets, their foundational design philosophies and architectural entry points differ fundamentally:"
    )
    doc.add_paragraph(
        "• Palantir's Vision: The digital twin of business operations. Palantir treats data as a means to an operational end. Its target is decision intelligence, operational write-backs, human-in-the-loop workflows, and rapid assembly of business-facing applications through its proprietary Ontology.\n"
        "• Databricks' Vision: The unified open Lakehouse. Databricks treats data as an enterprise-wide asset governed under open formats (Delta Lake, Apache Iceberg) and standardized protocols. Its focus is high-throughput data engineering, distributed analytics, native data science, and customizable compound AI systems."
    )
    
    add_heading_1(doc, "2. High-Level Architectural Comparison Matrix")
    headers_high = ["Dimension", "Palantir (Foundry + AIP)", "Databricks (Lakehouse + Mosaic AI)", "Strategic Winner / Context"]
    data_high = [
        ["Primary Paradigm", "Ontology-driven operational applications and decision cockpits", "Open Lakehouse & Data Intelligence Platform", "Context-dependent: Palantir for operational UI; Databricks for open data ecosystem"],
        ["Storage Strategy", "Proprietary managed format on top of S3/ADLS/GCS; federated connectors", "Open formats: Delta Lake, Apache Iceberg (UniForm), Apache Hudi on cloud storage", "Databricks: 100% open, prevents vendor lock-in"],
        ["Compute & Processing Engine", "Embedded Apache Spark, custom microservices, proprietary indexing engines", "Photon vectorized C++ engine, Apache Spark (Serverless & classic pools)", "Databricks: Superior raw processing throughput and scalability"],
        ["Semantic & Business Layer", "Foundry Ontology (Objects, Links, Actions, Functions, kinetic write-backs)", "Unity Catalog (Metastore, Schemata, ABAC) + Semantic Partners / Metric Views", "Palantir: Mature operational Ontology & bi-directional write-back"],
        ["Application Development", "Palantir Workshop (low-code), Slate, AIP Agent Studio (turnkey app builders)", "Databricks Apps (Streamlit/FastAPI/Dash), AI/BI Genie, Dashboards", "Palantir: Highly turnkey UI; Databricks: Open code-based custom apps"],
        ["Generative AI & Agent Framework", "Palantir AIP (AIP Logic, AIP Assist, Ontology-bound agent tools)", "Mosaic AI (Agent Framework, Vector Search, Model Serving, Evaluation, Gateway)", "Tie: Palantir faster for non-coder agent apps; Databricks superior for ML flexibility"],
        ["Governance & Security Model", "Marking-based access control, Purpose-based classification, granular provenance", "Unity Catalog (ABAC, RBAC, Row Filters, Column Masking, Clean Rooms, Lineage)", "Databricks for standard enterprise governance; Palantir for defense/compartmentalized security"],
        ["Deployment Flexibility", "Multi-cloud, on-premise, edge, and air-gapped nodes (via Palantir Apollo)", "Multi-cloud SaaS (AWS, Azure, GCP) across standard VPC configurations", "Palantir: Superior for air-gapped/classified sovereign edge deployment"],
        ["Ecosystem Openness", "Proprietary closed ecosystem; data exports available via APIs/ODBC/Spark", "100% open-source standards (Delta Lake, MLflow, Spark, open REST APIs)", "Databricks: Zero vendor lock-in, broad industry ecosystem"],
        ["Pricing & TCO Model", "Enterprise license contracts + Foundry Compute Units (FCUs) + FDE engineering cost", "Consumption-based Databricks Units (DBUs) + underlying cloud VM/storage costs", "Databricks: Highly transparent, predictable, lower entry barrier"]
    ]
    add_custom_table(doc, headers_high, data_high, [Inches(1.2), Inches(2.0), Inches(2.0), Inches(1.3)])
    
    add_heading_1(doc, "3. Deep-Dive Domain Capability Comparisons")
    
    add_heading_2(doc, "3.1 Data Ingestion, Storage & Table Formats")
    headers_store = ["Capability", "Palantir Foundry", "Databricks Lakehouse", "Architectural Trade-Off Analysis"]
    data_store = [
        ["Underlying Format", "Managed Parquet / proprietary metadata index layer", "Delta Lake (Open Source) with UniForm (Iceberg/Hudi)", "Databricks tables can be read directly by Snowflake, Trino, Athena without duplication."],
        ["Streaming Ingestion", "Stream pipelines via Kafka, Kinesis, Magritte agent streaming", "Auto Loader + Spark Structured Streaming + Lakeflow Connect", "Databricks Auto Loader provides industry-leading cost-efficiency for streaming millions of files."],
        ["Data Federation", "Virtual Tables via ODBC/JDBC & REST adaptors", "Lakehouse Federation (Snowflake, BigQuery, Postgres, Synapse)", "Both platforms support zero-copy federation; Databricks federates directly at the query optimization layer."]
    ]
    add_custom_table(doc, headers_store, data_store, [Inches(1.3), Inches(1.8), Inches(1.8), Inches(1.6)])
    
    add_heading_2(doc, "3.2 Data Governance, Lineage & Compliance")
    headers_gov = ["Governance Vector", "Palantir Foundry", "Databricks Unity Catalog", "Comparison Insights"]
    data_gov = [
        ["Lineage Tracking", "Granular transform-level provenance graph across all transforms and apps", "Automated column and table level lineage across SQL, DLT, notebooks, and dashboards", "Both provide world-class automated lineage graphs."],
        ["Security Paradigm", "Markings, Mandatory Access Control (MAC), Purpose-Based Access", "RBAC, Attribute-Based Access Control (ABAC), Dynamic Row/Col masking", "Palantir is optimized for national defense classification; Databricks is optimized for commercial enterprise IAM."],
        ["Data Sharing & Clean Rooms", "Cross-tenancy sharing via Apollo and Foundry Sync", "Delta Sharing (Open protocol) + Databricks Clean Rooms", "Delta Sharing allows secure data sharing to any external client without requiring a Databricks account."]
    ]
    add_custom_table(doc, headers_gov, data_gov, [Inches(1.3), Inches(1.8), Inches(1.8), Inches(1.6)])
    
    add_heading_2(doc, "3.3 The Semantic Layer: Palantir Ontology vs. Databricks Unity Catalog")
    doc.add_paragraph(
        "The semantic layer is the most contested battleground between Palantir and Databricks. While Palantir built its Ontology over 15 years to represent stateful business objects and execute operational write-backs, Databricks has traditionally relied on relational metadata in Unity Catalog, now augmenting it with semantic metric definitions and Databricks Apps."
    )
    headers_sem = ["Feature", "Palantir Ontology", "Databricks Lakehouse Alternative", "Maturity Differential"]
    data_sem = [
        ["Entity Modeling", "Object Types with property validation, schemas, and primary keys", "Unity Catalog Tables/Views + Semantic Modeling Partners (Cube, dbt)", "Palantir has native, out-of-the-box object modeling; Databricks relies on SQL schemas."],
        ["Relationships", "Semantic Link Types with graph traversals", "Foreign Key constraints in Unity Catalog + GraphFrames in Spark", "Palantir allows non-technical users to navigate links visually in Workshop."],
        ["Kinetic Actions & Write-Back", "Action Types with TypeScript functions writing directly to source systems", "Databricks Apps (REST APIs to Salesforce/SAP) or Lakeflow reverse-ETL connectors", "Palantir is distinctly superior for operational closed-loop write-backs."],
        ["Calculated Functions", "Functions on Objects cached in high-performance memory engines", "Unity Catalog SQL/Python User Defined Functions (UDFs) & Photon execution", "Databricks offers superior compute scale; Palantir offers lower-latency cached UI reads."]
    ]
    add_custom_table(doc, headers_sem, data_sem, [Inches(1.3), Inches(1.8), Inches(1.8), Inches(1.6)])
    
    add_heading_2(doc, "3.4 Generative AI & Autonomous Agent Frameworks")
    doc.add_paragraph(
        "• Palantir AIP: Connects LLMs directly to the Foundry Ontology as callable tools. Business analysts build multi-agent workflows in AIP Agent Studio where agents can inspect inventory, calculate risk, and request human approval to trigger Actions. Excellent for rapid operational business automation with pre-built guardrails.\n"
        "• Databricks Mosaic AI: Provides a comprehensive, code-first and low-code framework for engineering custom AI systems. Mosaic AI Agent Framework integrates with open-source tools (LangChain, LlamaIndex), provides managed Vector Search, hosts custom-tuned open models (Llama 3, DBRX) on Serverless Model Serving, and delivers automated LLM-as-a-judge evaluation pipelines."
    )
    
    add_heading_2(doc, "3.5 Application Development & Operational Cockpits")
    doc.add_paragraph(
        "• Palantir Workshop & Slate: Industry benchmark for drag-and-drop operational application building. Business users can build complex dashboards, workflow queues, and decision cockpits in days without writing front-end JavaScript.\n"
        "• Databricks Apps & AI/BI: Databricks now offers Databricks Apps (hosting Python Streamlit, Dash, Gradio, FastAPI) and serverless AI/BI Dashboards/Genie. While Databricks provides ultimate flexibility for developers, Palantir retains an advantage in out-of-the-box WYSIWYG application building for operational non-developers."
    )
    
    add_heading_1(doc, "4. Total Cost of Ownership (TCO) & Commercial Comparison")
    doc.add_paragraph(
        "Financial models diverge significantly between the two platforms:\n"
        "1. Palantir Pricing Dynamics: Platform licensing typically involves substantial base commitments plus platform compute usage (FCUs). Forward Deployed Engineering (FDE) services can add multi-million dollar annual professional services fees. The platform delivers high ROI for complex, high-value mission-critical operational challenges, but has a higher cost of entry.\n"
        "2. Databricks Pricing Dynamics: Purely consumption-based pricing (Databricks Units - DBUs) layered on top of commodity cloud infrastructure. Compute scales to zero when not in use. Databricks provides extensive cost transparency via System Tables, making it significantly more cost-effective for general-purpose enterprise data warehousing, ETL, and ML."
    )
    
    add_heading_1(doc, "5. Strategic Decision Framework: When to Choose Which Platform")
    headers_dec = ["Business Scenario / Requirement", "Recommended Primary Platform", "Strategic Rationale"]
    data_dec = [
        ["Operational Closed-Loop Decision Workflows", "Palantir Foundry / AIP", "Native Ontology Actions allow business operators to make decisions and write back directly to ERP/CRM systems within unified cockpits."],
        ["Enterprise Open Data Lakehouse & Warehousing", "Databricks Lakehouse", "Open Delta Lake formats eliminate vendor lock-in; Photon engine delivers unmatched TCO and price-performance for BI and SQL."],
        ["Defense, Intelligence & Sovereign Air-Gapped Deployments", "Palantir Gotham / Foundry", "Proven DoD IL5/IL6 accreditation and Apollo autonomous air-gapped deployment architecture."],
        ["Broad Custom Machine Learning & GenAI Development", "Databricks Mosaic AI", "Full ML lifecycle governance (MLflow, Vector Search, fine-tuning, Model Serving) with complete code flexibility."],
        ["Rapid Turnkey No-Code Application Assembly", "Palantir Workshop", "Enables business analysts to construct polished, operational enterprise applications in hours without front-end development teams."],
        ["Hybrid Coexistence Strategy", "Both (Databricks as Lakehouse + Palantir as UI/Ontology)", "Databricks acts as the centralized data lakehouse/ETL engine; Palantir connects via Lakehouse Federation/Delta to power operational front-end apps."]
    ]
    add_custom_table(doc, headers_dec, data_dec, [Inches(1.8), Inches(1.8), Inches(2.9)])
    
    output_path = "/Users/josekurian/GoogleAutomation/AIPalatirToDatabricks/Comparisons/Palantir_vs_Databricks_Comparison_Matrix.docx"
    doc.save(output_path)
    print(f"Saved: {output_path}")

if __name__ == "__main__":
    build_comparisons_doc()
