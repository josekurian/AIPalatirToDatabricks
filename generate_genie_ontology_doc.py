import os
import docx
from docx.shared import Inches, Pt, RGBColor
from doc_helper import (
    create_styled_document, add_heading_1, add_heading_2, add_heading_3,
    add_callout, add_custom_table
)

def build_databricks_genie_ontology_plan():
    doc = create_styled_document(
        "Databricks Genie & Enterprise Ontology Modernization & Implementation Plan",
        "Deep-Dive Architecture, Unified Semantics, OntoRank Engine, Trusted Assets, Review Queues & Comparative Migration Playbook (Palantir vs Oracle vs Databricks)"
    )

    add_callout(
        doc,
        "Databricks Genie Ontology represents the next generation of business-aware semantic modeling for the Lakehouse. By synthesizing Modeled Context (Unity Catalog Metric Views, certified Pages, hierarchical Domains) with Inferred Context (mined from dashboards, SQL execution logs, and BI queries) and prioritizing them with the OntoRank authority algorithm, Genie eliminates conflicting metric definitions and delivers authoritative Natural Language Analytics (NLP-to-SQL) directly to business users. This blueprint details the complete implementation plan, architecture, code assets, and comparative migration methodologies from Palantir Ontology and Oracle Data Warehouses.",
        "EXECUTIVE CHARTER: NEXT-GENERATION ENTERPRISE SEMANTICS & GENIE ONTOLOGY"
    )

    # 1. Executive Summary & Core Paradigm
    add_heading_1(doc, "1. Executive Summary: The Rise of the Databricks Genie Ontology")
    doc.add_paragraph(
        "Modern enterprise analytics has long suffered from the 'Semantic Divide'—the gap between physical database schemas (tables, columns, partitions) and dynamic business semantics (ARR, churn, gross margin, customer cohorts). Historically, organizations either locked their semantics inside proprietary application silos (Palantir Foundry Ontology) or rigid multi-dimensional semantic engines (Oracle BI / OBIEE / RPD)."
    )
    doc.add_paragraph(
        "Databricks Genie and the Genie Ontology bridge this chasm natively on top of open Delta Lake tables. Unlike static data catalogs or isolated semantic layers, Databricks Genie Ontology is a self-learning, multi-modal semantic operating system. It operates on three foundational principles:"
    )
    doc.add_paragraph(
        "1. Open Standards & Unity Catalog Anchoring: All entity definitions, relationships, and metrics reside within Unity Catalog, governed by role-based and attribute-based access controls (RBAC/ABAC) without proprietary data lock-in."
    )
    doc.add_paragraph(
        "2. Dual-Engine Context Synthesis: The ontology automatically combines human-certified 'Modeled Context' (Metric Views, governed Pages, Domains) with continuously learned 'Inferred Context' (query patterns, execution frequency, dashboard filters)."
    )
    doc.add_paragraph(
        "3. OntoRank Algorithmic Authority: Utilizing authority-weighted graph traversal inspired by PageRank, OntoRank arbitrates conflicting enterprise definitions, guaranteeing that AI agents and business executives always receive verified, single-source-of-truth answers."
    )

    # 2. Key Architectural Pillars of Databricks Genie Ontology
    add_heading_1(doc, "2. Key Architectural Pillars & Feature Breakdown")
    doc.add_paragraph(
        "The Databricks Genie Ontology architecture comprises five core modular components:"
    )

    headers_pillars = ["Ontology Pillar", "Technical Mechanism", "Operational Functionality", "Enterprise Impact"]
    data_pillars = [
        [
            "1. Domain Clusters & Visual Graph",
            "Hierarchical namespace grouping in Unity Catalog (e.g., Products, Finance, Customer Success, Sales, Security & Compliance).",
            "Visual domain bubbles depicting size (asset count), reach (conversations resolved), and inferred vs modeled state.",
            "Allows business units to govern their departmental sub-ontologies while enabling cross-domain federated joins."
        ],
        [
            "2. Unity Catalog Pages",
            "Markdown-based business definition documents bound directly to tables, views, and schemas in Unity Catalog.",
            "Documents business logic, edge cases, acronyms (e.g., 'ARR = Annual Recurring Revenue net of churn'), and canonical SQL examples.",
            "Serves as the deterministic ground truth for Genie's NLP-to-SQL translation, eliminating hallucinations."
        ],
        [
            "3. Metric Views & Trusted Assets",
            "Declarative SQL/YAML metric definitions in Unity Catalog with built-in dimensions, measures, and join paths.",
            "Designates certified Gold tables and pre-computed aggregations as official 'Trusted Assets' for AI agent exploration.",
            "Guarantees mathematical consistency; prevents ad-hoc, divergent SQL calculations across executive users."
        ],
        [
            "4. OntoRank Authority Engine",
            "Graph-based authority scoring algorithm factoring asset certification, author seniority, usage frequency, and freshness.",
            "Resolves semantic conflicts (e.g., when Finance and Sales define 'Customer Churn' differently) by calculating page authority.",
            "Ensures executive-level queries are served only with top-ranked, certified definitions while logging edge cases."
        ],
        [
            "5. Steward Review Queue & Admin",
            "Active governance console highlighting unmapped queries, high-frequency user prompts, and low-confidence inferences.",
            "Provides data stewards with a one-click workflow to approve inferred snippets and promote them into certified UC Pages.",
            "Continuous closed-loop learning; ontology accuracy improves organically as enterprise usage increases."
        ]
    ]
    add_custom_table(doc, headers_pillars, data_pillars, [Inches(1.5), Inches(1.8), Inches(1.8), Inches(1.4)])

    # 3. Comprehensive Comparison: Databricks Genie vs Palantir Ontology vs Oracle Data Warehouses
    add_heading_1(doc, "3. Tri-Platform Capability & Migration Comparison Matrix")
    doc.add_paragraph(
        "To formulate an effective enterprise migration strategy, organizations must evaluate Databricks Genie Ontology against Palantir Foundry's Operational Ontology and Oracle's Enterprise Data Warehouse / OBIEE Semantic Layer across critical architectural dimensions."
    )

    headers_comp = ["Evaluation Dimension", "Palantir Foundry / AIP Ontology", "Oracle Enterprise DW / OBIEE RPD", "Databricks Lakehouse & Genie Ontology", "Migration Advantage / Strategic Shift"]
    data_comp = [
        [
            "Storage & Data Architecture",
            "Monolithic, proprietary binary storage; data copied into Foundry cluster.",
            "Relational Exadata / EE tables; multi-dimensional OLAP cubes.",
            "Open Delta Lake (UniForm) + Parquet/Iceberg; zero-copy in-place storage.",
            "Databricks eliminates vendor lock-in and multi-million dollar annual storage markup."
        ],
        [
            "Semantic Modeling",
            "Ontology Object Types, Link Types, and Action Interfaces defined in Workshop.",
            "Three-tier RPD (Physical, Business Model & Mapping, Presentation Layer).",
            "Unity Catalog Metric Views, Certified Pages, Tag-based Relations & Domains.",
            "Simpler, declarative, Git-integrated semantic layer governed in a single catalog."
        ],
        [
            "AI & Natural Language Querying",
            "Palantir AIP Agent Studio; LLM prompts bound to proprietary ontology functions.",
            "Oracle Select AI / Autonomous Database AI; basic SQL generation prompts.",
            "Databricks Genie AI/BI + OntoRank engine + Mosaic AI Agent Framework.",
            "Autonomous conflict resolution via OntoRank; context learning from query logs."
        ],
        [
            "Operational Actions & Write-Back",
            "Proprietary Action Types with Foundry Transaction Manager & edit hooks.",
            "Stored procedures, PL/SQL packages, Oracle APEX forms, GoldenGate CDC.",
            "Databricks Apps (FastAPI / Streamlit) executing ACID Delta Lake `MERGE` & REST APIs.",
            "Fully open Python ecosystem running inside customer cloud VPC without proprietary runtime."
        ],
        [
            "Security & Governance Model",
            "Foundry Markings (Mandatory Access Control) & proprietary granular ACLs.",
            "Virtual Private Database (VPD), Database Vault, OCI IAM policies.",
            "Unity Catalog ABAC, Row Filters, Column Masks, System Tables, Lineage.",
            "Unified enterprise security spanning data, AI models, notebooks, and dashboards."
        ],
        [
            "Cost & Licensing Model",
            "High 7-figure fixed platform subscription + proprietary compute units.",
            "Per-core CPU licensing, Exadata hardware maintenance, and support contracts.",
            "Flexible consumption-based Databricks Units (DBUs) with serverless scale-to-zero.",
            "60% to 70% reduction in annual platform expenditure."
        ]
    ]
    add_custom_table(doc, headers_comp, data_comp, [Inches(1.1), Inches(1.4), Inches(1.3), Inches(1.4), Inches(1.3)])

    # 4. End-to-End Implementation Plan (Phased Roadmap)
    add_heading_1(doc, "4. Phased Implementation Plan for Databricks Genie & Enterprise Ontology")
    doc.add_paragraph(
        "Deploying an enterprise-grade Databricks Genie Ontology requires a structured, multi-phase execution methodology spanning architecture, data modeling, AI context configuration, and governance."
    )

    headers_phases = ["Phase & Timeline", "Key Milestones & Deliverables", "Technical Activities & Artifacts", "Sign-Off Criteria"]
    data_phases = [
        [
            "Phase 1: Discovery & Semantic Cataloging\n(Weeks 1-3)",
            "• Inventory existing Palantir Object Types and Oracle RPD presentation models.\n• Identify top 50 executive business questions.\n• Map departmental domains.",
            "• Run automated schema scrapers.\n• Catalog existing Snowflake/Oracle semantic views.\n• Establish Lakehouse Federation connections.",
            "• Complete Semantic Inventory matrix.\n• Architectural approval of UC catalog structure."
        ],
        [
            "Phase 2: Lakehouse Modeling & Trusted Assets\n(Weeks 4-7)",
            "• Deploy Gold Delta UniForm tables.\n• Implement Unity Catalog Foreign Keys.\n• Create Unity Catalog Metric Views for core KPIs.",
            "• PySpark DLT pipelines for bronze-to-gold.\n• SQL DDL defining primary/foreign key constraints.\n• YAML Metric View specifications for ARR, churn, GM.",
            "• 100% of core entities validated in Unity Catalog.\n• Data quality expectations passing at 99.9%."
        ],
        [
            "Phase 3: Genie Space & Context Injection\n(Weeks 8-10)",
            "• Establish departmental Genie Spaces.\n• Draft and certify Unity Catalog Pages.\n• Author Genie space instructions and benchmark SQL pairs.",
            "• Deploy Markdown UC Pages with business definitions.\n• Configure 15-20 few-shot question-SQL benchmarks.\n• Set up global default filters (e.g., exclude test rows).",
            "• Genie benchmark accuracy exceeds 92% on gold evaluation suite."
        ],
        [
            "Phase 4: OntoRank Tuning & Review Queue Setup\n(Weeks 11-13)",
            "• Activate OntoRank weighting algorithm.\n• Configure Steward Review Queue workflows.\n• Integrate query execution log mining.",
            "• Connect System Tables (`system.query.history`).\n• Establish steward escalation policies in Slack/Teams.\n• Train data stewards on promotion workflows.",
            "• 0 conflicting definitions on core metrics.\n• Review queue triage SLA under 24 hours."
        ],
        [
            "Phase 5: Operational Pilot & Dual-Run\n(Weeks 14-16)",
            "• Roll out Genie to 100 business pilot users.\n• Automated dual-run parity testing against Palantir Workshop and Oracle BI.",
            "• Execute SHA-256 fingerprint reconciliation.\n• Capture user feedback and low-confidence prompts.\n• Refine UC Pages based on real interactions.",
            "• 95%+ user satisfaction reach.\n• 100% numerical parity against legacy reports."
        ],
        [
            "Phase 6: Cutover & Legacy Decommissioning\n(Weeks 17-18)",
            "• Full enterprise go-live across all domains.\n• Sunset Palantir Workshop applications and Oracle BI dashboards.\n• Decommission redundant infrastructure.",
            "• Final license termination notices.\n• Backup legacy RPD and Foundry metadata for compliance.\n• Activate production SLA monitoring.",
            "• 100% of executive reporting migrated to Databricks.\n• Full realization of multi-million dollar license savings."
        ]
    ]
    add_custom_table(doc, headers_phases, data_phases, [Inches(1.2), Inches(1.8), Inches(2.2), Inches(1.3)])

    # 5. Technical Architecture & Component Implementation
    add_heading_1(doc, "5. Technical Implementation Details & Code Blueprints")
    doc.add_paragraph(
        "Below are the production-grade architectural patterns and code assets required to implement Databricks Genie Ontology and transition from legacy Palantir and Oracle paradigms."
    )

    add_heading_2(doc, "5.1 Unity Catalog Metric View Definition Pattern")
    doc.add_paragraph(
        "Metric Views provide the immutable mathematical backbone that prevents Genie from hallucinating calculations. Below is the production SQL specification for an Enterprise Revenue Metric View:"
    )
    doc.add_paragraph(
        "```sql\n"
        "-- Unity Catalog Metric View: enterprise_revenue_metrics\n"
        "CREATE OR REPLACE VIEW gold.finance.enterprise_revenue_metrics\n"
        "AS\n"
        "SELECT\n"
        "    customer_id,\n"
        "    region,\n"
        "    product_line,\n"
        "    DATE_TRUNC('month', transaction_date) AS fiscal_month,\n"
        "    SUM(net_amount) AS monthly_revenue,\n"
        "    SUM(CASE WHEN transaction_type = 'RECURRING' THEN net_amount ELSE 0 END) AS arr,\n"
        "    COUNT(DISTINCT customer_id) AS active_subscribers,\n"
        "    SUM(cost_of_goods_sold) AS total_cogs,\n"
        "    (SUM(net_amount) - SUM(cost_of_goods_sold)) / NULLIF(SUM(net_amount), 0) AS gross_margin_pct\n"
        "FROM gold.finance.fact_transactions\n"
        "WHERE status = 'SETTLED' AND is_test_record = FALSE\n"
        "GROUP BY customer_id, region, product_line, DATE_TRUNC('month', transaction_date);\n"
        "\n"
        "-- Tag as Certified Trusted Asset\n"
        "ALTER VIEW gold.finance.enterprise_revenue_metrics\n"
        "SET TAGS ('governance_tier' = 'certified_gold', 'semantic_type' = 'metric_view', 'owner' = 'finance_stewards');\n"
        "```"
    )

    add_heading_2(doc, "5.2 Unity Catalog Page: Business Context & Ground Truth")
    doc.add_paragraph(
        "Unity Catalog Pages provide human-authored domain context that maps synonyms, edge-case business rules, and benchmark query pairs:"
    )
    doc.add_paragraph(
        "```markdown\n"
        "# Unity Catalog Page: Consumption Revenue Recognition\n"
        "**Domain**: Finance & Revenue Operations | **Status**: Certified | **Owner**: Dana Whitlock (Lead Financial Architect)\n"
        "\n"
        "## Core Definitions\n"
        "- **ARR (Annual Recurring Revenue)**: Calculated strictly as the run-rate of recurring subscription contracts and baseline committed platform usage. Excludes one-off professional services and implementation credits.\n"
        "- **Active Customer**: Any account that generated non-zero billable consumption events in the trailing 30 days.\n"
        "- **Fiscal Calendar**: Company fiscal year begins February 1st. Q1 = Feb-Apr, Q2 = May-Jul, Q3 = Aug-Oct, Q4 = Nov-Jan.\n"
        "\n"
        "## Genie Query Instructions & Guardrails\n"
        "1. When a user asks for 'Revenue' without specifying product line, always query `gold.finance.enterprise_revenue_metrics`.\n"
        "2. Always apply `is_test_record = FALSE` to eliminate QA sandbox transactions.\n"
        "3. If a question is ambiguous between 'Booking Value' and 'Recognized Revenue', clarify with the user or default to 'Recognized Revenue' while noting the assumption.\n"
        "\n"
        "## Benchmark Question-SQL Pair\n"
        "- **Prompt**: 'Show me top 5 customers by ARR in North America for Q3'\n"
        "- **Certified SQL**:\n"
        "```sql\n"
        "SELECT customer_id, SUM(arr) AS total_arr\n"
        "FROM gold.finance.enterprise_revenue_metrics\n"
        "WHERE region = 'North America' AND fiscal_month BETWEEN '2026-08-01' AND '2026-10-31'\n"
        "GROUP BY customer_id\n"
        "ORDER BY total_arr DESC\n"
        "LIMIT 5;\n"
        "```\n"
        "```"
    )

    add_heading_2(doc, "5.3 OntoRank Authority Algorithm & Review Queue Orchestration")
    doc.add_paragraph(
        "The OntoRank engine continuously processes telemetry from Databricks system tables (`system.query.history`, `system.access.table_lineage`) to determine the authority score of every snippet, page, and metric. When multiple definitions of a metric exist, OntoRank scores each candidate definition based on:"
    )
    doc.add_paragraph(
        "$$\\text{AuthorityScore}(D) = w_1 \\cdot \\text{Cert}(D) + w_2 \\cdot \\text{Seniority}(U) + w_3 \\cdot \\log(1 + \\text{ExecCount}(D)) + w_4 \\cdot \\text{Freshness}(D)$$"
    )
    doc.add_paragraph(
        "Where $\\text{Cert}(D)$ is a binary certification flag (1.0 for Certified Gold assets), $\\text{Seniority}(U)$ reflects the author's domain governance role, $\\text{ExecCount}(D)$ represents monthly query executions by enterprise users, and $\\text{Freshness}(D)$ penalizes stale definitions older than 90 days. High-ambiguity queries where no definition achieves a threshold score ($\ge 0.85$) are automatically routed to the Steward Review Queue."
    )

    # 6. Comparative Migration Activities: Palantir vs Oracle vs Databricks
    add_heading_1(doc, "6. Comparative Migration Activities: Palantir & Oracle to Databricks")
    doc.add_paragraph(
        "Migrating an enterprise from legacy Palantir and Oracle architectures requires distinct, highly specialized migration tracks:"
    )

    headers_mig_act = ["Migration Track", "Source Paradigm (Palantir / Oracle)", "Databricks Genie & Lakehouse Equivalent", "AI Automation Method & Tooling", "Validation & Quality Gate"]
    data_mig_act = [
        [
            "Track 1: Schema & Data Migration",
            "• Palantir Foundry Datasets & Schema definitions.\n• Oracle Exadata partitioned tables & LOBs.",
            "• Delta Lake Tables with Liquid Clustering (`CLUSTER BY`).\n• UniForm Iceberg compatibility enabled.",
            "• Automated Schema Transpiler Agent converts Oracle DDL to Spark SQL.\n• Auto Loader for parallelized parity loads.",
            "• Row-level SHA-256 fingerprinting.\n• Bitwise checksum validation across partitions."
        ],
        [
            "Track 2: Logic & Pipeline Transpilation",
            "• Palantir `@transform_df` / `@transform` Python pipelines.\n• Oracle PL/SQL stored procedures & packages.",
            "• Native PySpark DataFrames.\n• Delta Live Tables (DLT) with expectations.\n• Databricks Workflows DAGs.",
            "• AST Parser + LLM Transpiler converts `@transform` to DLT decorators.\n• PL/SQL cursor vectorizer eliminates row loops.",
            "• Automated regression test suite comparing output DataFrames across 1,000 edge-case test runs."
        ],
        [
            "Track 3: Semantic Layer Migration",
            "• Palantir Object Types, Link Types & Properties.\n• Oracle BI / OBIEE RPD (Physical, BMM, Presentation).",
            "• Unity Catalog Gold Tables + Foreign Keys.\n• Unity Catalog Metric Views & Domains.\n• Genie Certified Pages.",
            "• Semantic Exporter extracts RPD XML and Foundry Ontology metadata $\\rightarrow$ generates UC Metric Views and Pages.",
            "• OntoRank benchmark test verifying NLP queries against 50 certified standard queries."
        ],
        [
            "Track 4: UI & Operational Actions",
            "• Palantir Workshop dashboards and Action Buttons.\n• Oracle APEX forms and OBIEE interactive dashboards.",
            "• Databricks AI/BI Dashboards.\n• Databricks Apps (FastAPI / Streamlit) for operational write-back.",
            "• Component-level transpiler converts Workshop widgets to Streamlit controls; binds actions to Delta `MERGE` endpoints.",
            "• End-to-end user latency < 200ms; ACID audit logging in `gold.audit.action_history`."
        ],
        [
            "Track 5: Security & Entitlements",
            "• Palantir Markings (MAC classification tags).\n• Oracle Database Vault & VPD row security policies.",
            "• Unity Catalog ABAC Tags, Dynamic Row Filters & Column Masking functions.",
            "• Security Transpiler maps Foundry Markings to UC tag policies (`ALTER TABLE ... SET TAGS`).",
            "• Automated penetration test & entitlement audit across 20 synthetic organizational personas."
        ]
    ]
    add_custom_table(doc, headers_mig_act, data_mig_act, [Inches(1.1), Inches(1.5), Inches(1.4), Inches(1.5), Inches(1.0)])

    # 7. Financial TCO & ROI Comparison
    add_heading_1(doc, "7. Financial TCO & Return on Investment (ROI) Analysis")
    doc.add_paragraph(
        "Consolidating Palantir Ontology, Oracle Data Warehouses, and isolated BI layers into Databricks Genie and Lakehouse yields dramatic cost savings by removing redundant proprietary compute, maintenance fees, and administrative sprawl."
    )

    headers_tco = ["Cost Category", "Legacy Tri-Platform (Palantir + Oracle + Snowflake)", "Consolidated Databricks Genie Lakehouse", "Annual Delta ($)", "3-Year Cumulative Savings"]
    data_tco = [
        [
            "Core Software Licensing",
            "$3,600,000 (Palantir) + $1,800,000 (Oracle) + $2,100,000 (Snowflake) = $7,500,000",
            "$0 (Decommissioned in favor of Databricks DBU consumption)",
            "-$7,500,000",
            "-$22,500,000"
        ],
        [
            "Databricks Serverless Compute (DBUs + Cloud)",
            "$0",
            "$2,450,000 (Includes Serverless SQL, Genie, Photon, and Mosaic AI)",
            "+$2,450,000",
            "+$7,350,000"
        ],
        [
            "Remaining Oracle Core OLTP Support",
            "$0",
            "$400,000 (Retained strictly for high-throughput ERP transactions)",
            "+$400,000",
            "+$1,200,000"
        ],
        [
            "Infrastructure & Cloud Cross-Egress",
            "$1,200,000",
            "$250,000 (Eliminated cross-cloud egress between AWS/GCP and Palantir)",
            "-$950,000",
            "-$2,850,000"
        ],
        [
            "Engineering & Administration (FTEs)",
            "$1,800,000 (12 FTEs across Palantir, Oracle DBA, and Snowflake teams)",
            "$600,000 (4 FTEs managing consolidated Databricks Lakehouse & Genie)",
            "-$1,200,000",
            "-$3,600,000"
        ],
        [
            "One-Time Migration Investment (Amortized)",
            "$0",
            "$550,000 (Year 1 only)",
            "+$550,000",
            "+$550,000"
        ],
        [
            "Total Enterprise TCO",
            "$10,500,000 / year",
            "$4,250,000 / year (Year 1) | $3,700,000 / year (Run-rate)",
            "-$6,250,000 / year",
            "-$19,850,000 Net Savings (63.0% Reduction)"
        ]
    ]
    add_custom_table(doc, headers_tco, data_tco, [Inches(1.2), Inches(1.8), Inches(1.6), Inches(1.0), Inches(1.4)])

    # 8. Governance, Risk Mitigation & Cutover Checklist
    add_heading_1(doc, "8. Governance, Risk Mitigation & Production Cutover Checklist")
    doc.add_paragraph(
        "To ensure zero operational disruption during the transition to Databricks Genie Ontology, enterprise teams must adhere to this go-live checklist:"
    )

    checklist_items = [
        ("Semantic Drift Prevention", "Implement daily automated Bitwise and statistical parity pipelines between legacy reports and Genie-generated SQL."),
        ("User Trust & Change Management", "Conduct role-based Genie training for business analysts; provide 1-click side-by-side SQL explanations to build confidence."),
        ("Steward Governance SLA", "Establish a formal SLA requiring data stewards to review unmapped prompts in the Review Queue within 24 business hours."),
        ("Entitlement Parity Verification", "Validate that Unity Catalog Dynamic Row Filters replicate 100% of Palantir Mandatory Access Control markings prior to user access cutover."),
        ("Disaster Recovery & Fallback", "Maintain read-only snapshots of legacy Oracle RPD and Palantir Ontologies for a 45-day hypercare window post go-live.")
    ]

    for title, desc in checklist_items:
        add_heading_3(doc, f"✓ {title}")
        doc.add_paragraph(desc)

    output_path = "/Users/josekurian/GoogleAutomation/AIPalatirToDatabricks/Databricks_Genie_and_Ontology_Implementation_Plan.docx"
    doc.save(output_path)
    print(f"Document successfully created at: {output_path} (Size: {os.path.getsize(output_path)} bytes)")

if __name__ == "__main__":
    build_databricks_genie_ontology_plan()
