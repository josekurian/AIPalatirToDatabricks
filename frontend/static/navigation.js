/* =============================================================================
 * Menu-Driven Navigation Router & Overview Engine
 * -----------------------------------------------------------------------------
 * Single source of truth (NAV) for every menu and sub-menu in the portal.
 *
 *   Project Overview (#/project-overview)
 *     └── Menu Overview        (#/<menu-id>-page)
 *           └── Sub-menu page  (#/<sub-menu-key>)  = Sub-menu Overview + working area
 *
 * Every page in the portal is reachable only through these menus and sub-menus.
 * The sidebar is generated from NAV, so a page cannot exist without a menu entry.
 * Loaded after the main inline script in index.html; it wraps loadView(),
 * loadLabsModule(), onMenuClick() and toggleMenu() so existing links route here.
 * ========================================================================== */
(function () {
    'use strict';

    const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => (
        { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]
    ));

    // Full Tailwind class strings (kept literal so the Tailwind CDN JIT picks them up)
    const THEME = {
        blue:    { icon: 'text-blue-400',    eyebrow: 'text-blue-600',    chip: 'bg-blue-50 text-blue-700 border-blue-200',          btn: 'bg-blue-600 hover:bg-blue-700',       hover: 'hover:border-blue-500',    grad: 'from-slate-900 via-blue-950 to-slate-900' },
        emerald: { icon: 'text-emerald-400', eyebrow: 'text-emerald-600', chip: 'bg-emerald-50 text-emerald-700 border-emerald-200', btn: 'bg-emerald-600 hover:bg-emerald-700', hover: 'hover:border-emerald-500', grad: 'from-slate-900 via-emerald-950 to-slate-900' },
        amber:   { icon: 'text-amber-400',   eyebrow: 'text-amber-600',   chip: 'bg-amber-50 text-amber-800 border-amber-200',       btn: 'bg-amber-600 hover:bg-amber-700',     hover: 'hover:border-amber-500',   grad: 'from-slate-900 via-amber-950 to-slate-900' },
        indigo:  { icon: 'text-indigo-400',  eyebrow: 'text-indigo-600',  chip: 'bg-indigo-50 text-indigo-700 border-indigo-200',    btn: 'bg-indigo-600 hover:bg-indigo-700',   hover: 'hover:border-indigo-500',  grad: 'from-slate-900 via-indigo-950 to-slate-900' },
        cyan:    { icon: 'text-cyan-400',    eyebrow: 'text-cyan-600',    chip: 'bg-cyan-50 text-cyan-800 border-cyan-200',          btn: 'bg-cyan-600 hover:bg-cyan-700',       hover: 'hover:border-cyan-500',    grad: 'from-slate-900 via-cyan-950 to-slate-900' },
        purple:  { icon: 'text-purple-400',  eyebrow: 'text-purple-600',  chip: 'bg-purple-50 text-purple-700 border-purple-200',    btn: 'bg-purple-600 hover:bg-purple-700',   hover: 'hover:border-purple-500',  grad: 'from-slate-900 via-purple-950 to-slate-900' },
        rose:    { icon: 'text-rose-400',    eyebrow: 'text-rose-600',    chip: 'bg-rose-50 text-rose-700 border-rose-200',          btn: 'bg-rose-600 hover:bg-rose-700',       hover: 'hover:border-rose-500',    grad: 'from-slate-900 via-rose-950 to-slate-900' },
    };

    // Folders the backend source viewer is allowed to open (mirrors SOURCE_ROOTS in server.py)
    const BROWSABLE_ROOTS = [
        'customer_prototypes_20', 'migration_sessions', 'bigdata_runtime', 'databricks_live_workspace',
        'genie_ontology_iceberg', 'multi_platform_ai_migration', 'Palantir', 'Databricks',
        'AB', 'Genie', 'LB', 'LF', 'LK', 'UC', 'UP',
        'Migrations/code_converters', 'Migrations/reconciliation', 'Migrations/validation_suite', 'api_100_testing_suite',
    ];
    const isBrowsable = (p) => BROWSABLE_ROOTS.some((r) => p === r || p.startsWith(r + '/'));

    // =========================================================================
    // NAV REGISTRY: every menu, every sub-menu, and each one's Overview content
    // =========================================================================
    const NAV = [
        // ---------------------------------------------------------------------
        {
            id: 'menu-overview', title: 'Platform Architecture', icon: 'ph-chart-polar', color: 'blue',
            tagline: 'Architectural blueprint, financial case and migration strategy',
            summary: 'Explains why and how enterprises move from Palantir Foundry, Oracle Exadata and Snowflake to the open Databricks Data Intelligence Platform. Start here to understand the target architecture, the 3-year business case, the scored capability comparison, and the two flagship implementation plans (Genie & Ontology, Oracle & Snowflake AI migration).',
            highlights: [
                'Side-by-side architecture of Palantir\'s closed digital-twin stack vs. the open Lakehouse',
                '3-year TCO model and performance benchmarks backed by JSON reports',
                'Weighted capability scoring across governance, AI, BI, apps and cost',
                'Semantic layer plan: Genie AI/BI, OntoRank, Metric Views and UniForm Iceberg v2',
                'Tri-platform AI migration plan for Oracle PL/SQL and Snowflake workloads',
            ],
            children: [
                {
                    key: 'overview-architecture', kind: 'view', title: 'Architectural Comparison',
                    summary: 'A layer-by-layer comparison of the Palantir Foundry stack (Ontology, Pipeline Builder, Workshop, AIP, Apollo) against its Databricks equivalents (Unity Catalog, Lakeflow/DLT, Databricks Apps, Mosaic AI, Asset Bundles).',
                    capabilities: ['See each Foundry component mapped to its Databricks replacement', 'Read the end-to-end reference topology diagrams', 'Understand where coupling exists and how it is decoupled', 'Identify open-standard formats (Delta, Iceberg, MLflow) used at each layer'],
                    steps: ['Review the component mapping table first', 'Study the topology diagrams to see data flow', 'Use the TCO and Matrix sub-menus to quantify the decision'],
                    assets: ['Palantir', 'Databricks', 'Palantir to Databricks Architectural Decoupling & Migration Playbook.docx'],
                    apis: ['GET /api/palantir/ontology'],
                },
                {
                    key: 'overview-tco', kind: 'view', title: '3-Year TCO & Benchmarks',
                    summary: 'The financial and performance business case: licensing, compute, storage and staffing costs over 3 years, plus benchmark results for query latency, pipeline throughput and concurrency.',
                    capabilities: ['Compare 3-year cost of ownership line by line', 'See projected net savings and payback period', 'Review query and pipeline benchmark charts', 'Export the numbers into executive presentations'],
                    steps: ['Read the headline savings KPIs', 'Inspect the per-category cost breakdown chart', 'Cross-check benchmark results against your own SLAs'],
                    assets: ['Comparisons/benchmarks/benchmark_and_tco_report.json'],
                    apis: ['GET /api/benchmarks'],
                },
                {
                    key: 'overview-matrix', kind: 'view', title: 'Scored Capability Matrix',
                    summary: 'A weighted scoring matrix that rates Palantir and Databricks on each enterprise capability category (governance, data engineering, AI/ML, BI, operational apps, openness, cost) to support an objective platform decision.',
                    capabilities: ['View weighted scores per capability category', 'Understand the rationale behind each score', 'Spot categories where Palantir parity requires extra design', 'Download the full comparison matrix document'],
                    steps: ['Scan the overall weighted totals', 'Drill into categories that matter most to your program', 'Use the Comparison Matrix .docx for stakeholder review'],
                    assets: ['Comparisons/matrices', 'Comparisons/Palantir_vs_Databricks_Comparison_Matrix.docx'],
                    apis: ['GET /api/matrices'],
                },
                {
                    key: 'overview-genie-ontology', kind: 'view', title: 'Genie & Ontology Plan',
                    summary: 'Implementation plan for rebuilding Palantir\'s Ontology semantics on Databricks: Unity Catalog business pages, Metric Views, the OntoRank authority resolver, data-steward review queues, Genie AI/BI spaces and Delta UniForm (Iceberg v2) tables.',
                    capabilities: ['Understand how Ontology object types become governed UC assets', 'See Metric View SQL and OntoRank resolution logic', 'Learn the steward review workflow for semantic certification', 'Review UniForm Iceberg table DDL and PySpark pipeline'],
                    steps: ['Read the semantic architecture section', 'Walk through the SQL and PySpark samples', 'Download the Genie & Ontology .docx plan for the full design'],
                    assets: ['genie_ontology_iceberg', 'Databricks_Genie_and_Ontology_Implementation_Plan.docx'],
                    apis: [],
                },
                {
                    key: 'overview-oracle-snowflake-ai', kind: 'view', title: 'Oracle & Snowflake AI Plan',
                    summary: 'AI-assisted migration plan for Oracle (PL/SQL, GoldenGate/Debezium CDC) and Snowflake (SnowSQL, Snowpark, Streams) into Databricks, including Lakehouse Federation, AI transpiler agents and automated multi-source reconciliation.',
                    capabilities: ['See PL/SQL → PySpark and Snowpark → PySpark transpilation', 'Understand CDC ingestion with DLT', 'Use Lakehouse Federation for phased coexistence', 'Orchestrate tri-platform cutover with Lakeflow Jobs'],
                    steps: ['Start with the phased migration roadmap', 'Review the transpiler and CDC code samples', 'Use the reconciliation section to plan parity sign-off'],
                    assets: ['multi_platform_ai_migration', 'AI-Enabled Multi-Platform Migration Implementation Plan.docx'],
                    apis: [],
                },
            ],
        },
        // ---------------------------------------------------------------------
        {
            id: 'menu-200-labs', title: '200 Hands-On Labs Track', icon: 'ph-flask', color: 'emerald',
            tagline: '10 progressive modules · 200 step-by-step engineering labs',
            summary: 'A complete practical curriculum that takes an engineer from refactoring Foundry transforms to running a certified production cutover on Databricks. Each module contains labs with objectives, step-by-step instructions, code, and verification criteria.',
            highlights: [
                'Labs are ordered so each module builds on the previous one',
                'Every lab includes objectives, steps, code and a verification checklist',
                'Covers engineering, governance, security, BI, AI and cutover',
                'Full curriculum is also available as a downloadable .docx guide',
            ],
            children: [
                ['mod_001_025', 'Module 1: PySpark Refactoring (001-025)', 'Convert Foundry Code Repository transforms (@transform_df, Input/Output) into modular, testable PySpark on Databricks.', ['Replace Foundry decorators with plain PySpark functions', 'Parameterise paths via Unity Catalog three-level names', 'Add unit tests with local Spark sessions']],
                ['mod_026_050', 'Module 2: DLT Pipelines (026-050)', 'Rebuild Pipeline Builder graphs as declarative Delta Live Tables / Lakeflow pipelines with expectations and medallion layers.', ['Author bronze/silver/gold DLT tables', 'Enforce data-quality expectations', 'Run streaming and batch pipelines incrementally']],
                ['mod_051_075', 'Module 3: Unity Catalog Ontology (051-075)', 'Model Palantir Ontology object types, links and properties as governed Unity Catalog tables, views, tags and lineage.', ['Translate object types into UC DDL', 'Model link types as foreign keys and views', 'Apply tags, comments and lineage']],
                ['mod_076_100', 'Module 4: Operational Actions & Apps (076-100)', 'Replace Ontology Actions and Workshop with Databricks Apps, FastAPI write-back services and audited operational tables.', ['Build write-back services with audit trails', 'Host operational UIs as Databricks Apps', 'Implement approval and guardrail logic']],
                ['mod_101_125', 'Module 5: Security & ABAC (101-125)', 'Translate Palantir Markings and mandatory access controls into Unity Catalog ABAC, row filters and column masks.', ['Map Markings to UC tags and policies', 'Create row-level filters and column masks', 'Audit access with system tables']],
                ['mod_126_150', 'Module 6: SQL & Photon BI (126-150)', 'Migrate Contour/Quiver analytics to Databricks SQL Warehouses, Photon, AI/BI dashboards and Genie spaces.', ['Tune queries on Photon warehouses', 'Build AI/BI dashboards', 'Publish Genie natural-language spaces']],
                ['mod_151_175', 'Module 7: Mosaic AI & MLflow (151-175)', 'Re-implement AIP agents and models with Mosaic AI Agent Framework, Model Serving, Vector Search and MLflow.', ['Track and register models with MLflow', 'Serve agents and models on Mosaic AI', 'Evaluate agents with human-in-the-loop guardrails']],
                ['mod_176_190', 'Module 8: Data Parity Reconciliation (176-190)', 'Prove migrated data matches the source using row counts, SHA-256 hashing and statistical tolerance checks.', ['Run bitwise hash comparisons', 'Apply epsilon tolerances to aggregates', 'Produce parity certification reports']],
                ['mod_191_195', 'Module 9: Lakeflow & DABs (191-195)', 'Orchestrate jobs with Lakeflow and promote code across environments using Databricks Asset Bundles and CI/CD.', ['Define jobs and tasks in Lakeflow', 'Package projects as Asset Bundles', 'Promote dev → staging → prod']],
                ['mod_196_200', 'Module 10: Production Cutover (196-200)', 'Execute the final cutover: freeze, final sync, parity sign-off, consumer switch-over and Palantir decommissioning.', ['Plan the cutover runbook', 'Run final parity sign-off', 'Decommission legacy pipelines safely']],
            ].map(([modId, title, summary, caps]) => ({
                key: 'lab-' + modId, kind: 'lab', modId, title, summary,
                capabilities: caps.concat(['Expand any lab to see objectives, steps, code and verification']),
                steps: ['Read this module overview', 'Expand each lab card in order and follow its steps', 'Complete the verification checklist before moving to the next lab'],
                assets: ['frontend/static/labs_200_curriculum.json', 'Palantir to Databricks 200 Hands-On Labs Step by Steps Instructions.docx'],
                apis: [],
            })),
        },
        // ---------------------------------------------------------------------
        {
            id: 'menu-interactive', title: 'Interactive Cockpits', icon: 'ph-browsers', color: 'amber',
            tagline: 'Live tools you can run directly in the browser',
            summary: 'Hands-on, interactive cockpits backed by real API endpoints on this server. Dispatch the 100 testing APIs, simulate operational ERP write-backs with guardrails, transpile Foundry code live, and run multi-source data parity checks.',
            highlights: [
                '100 categorised testing APIs with single and batch execution',
                'Operational write-back simulator with human-in-the-loop guardrails',
                'Live Foundry → DLT and Ontology → Unity Catalog code converter',
                'Reconciliation runner producing a parity certification result',
            ],
            children: [
                {
                    key: 'cockpit-100-apis', kind: 'view', title: '100 Testing APIs Console',
                    summary: 'An API test bench exposing 100 enterprise testing APIs grouped into 10 architectural categories (transpilation, reconciliation, Iceberg, Genie, OntoRank, security, Lakebase, Lakeflow and more).',
                    capabilities: ['Browse the API catalog by category', 'Dispatch a single API and inspect the JSON response', 'Run all 100 APIs in one batch with latency tracking'],
                    steps: ['Pick an API from the dropdown', 'Click dispatch and review the response panel', 'Use "Run All" for a full regression sweep'],
                    assets: ['api_100_testing_suite'],
                    apis: ['GET /api/v1/testing-apis/catalog', 'POST /api/v1/testing-apis/dispatch/{api_id}', 'POST /api/v1/testing-apis/run-all'],
                },
                {
                    key: 'cockpit-operational-app', kind: 'view', title: 'Databricks Operational App',
                    summary: 'Simulates a Palantir Workshop operational action rebuilt as a Databricks App: select an order and warehouse, then trigger an audited ERP write-back.',
                    capabilities: ['Simulate a kinetic write-back action', 'See how actions are audited into Unity Catalog', 'Understand guardrails for high-value transactions'],
                    steps: ['Select an order and source warehouse', 'Execute the write-back', 'Review the confirmation and audit note'],
                    assets: ['Databricks/databricks_apps', 'migration_sessions/session_05_actions_to_databricks_apps'],
                    apis: ['POST /api/actions/execute'],
                },
                {
                    key: 'cockpit-code-converter', kind: 'view', title: 'Code Converter Playground',
                    summary: 'Paste Palantir Foundry transform code or Ontology JSON and convert it to Databricks DLT Python or Unity Catalog SQL DDL using the project\'s converters.',
                    capabilities: ['Convert Foundry transforms to DLT pipelines', 'Convert Ontology definitions to Unity Catalog DDL', 'Edit input and re-run instantly'],
                    steps: ['Choose the conversion type', 'Paste or edit the source code', 'Click convert and copy the generated output'],
                    assets: ['Migrations/code_converters'],
                    apis: ['POST /api/convert'],
                },
                {
                    key: 'cockpit-reconciliation', kind: 'view', title: 'Live Parity Runner',
                    summary: 'Runs the reconciliation engine to compare source and target datasets with row counts, SHA-256 hashing and statistical tolerance, returning a certification status.',
                    capabilities: ['Trigger a live reconciliation run', 'Review parity percentage and row discrepancies', 'Understand certification criteria'],
                    steps: ['Click the run button', 'Inspect the parity result card', 'Use Module 8 labs for deeper reconciliation practice'],
                    assets: ['Migrations/reconciliation', 'Migrations/validation_suite'],
                    apis: ['GET /api/reconciliation/run'],
                },
            ],
        },
        // ---------------------------------------------------------------------
        {
            id: 'menu-solutions', title: 'Solutions & Prototypes', icon: 'ph-buildings', color: 'indigo',
            tagline: 'Industry prototypes, migration sessions and reference code',
            summary: 'Working, runnable reference material: 20 industry customer prototypes, 8 guided migration sessions that map each Foundry capability to Databricks, and the side-by-side Palantir (source) and Databricks (target) reference implementations.',
            highlights: [
                '20 industry prototypes, each with README, pipeline code and SQL',
                '8 migration sessions, one per Foundry capability',
                'Browse every source file directly in the portal',
                'Palantir source vs. Databricks target reference estates',
            ],
            children: [
                {
                    key: 'solutions-prototypes', kind: 'custom', title: '20 Customer Prototypes',
                    summary: 'Twenty industry-specific prototypes (manufacturing, banking, healthcare, supply chain, energy, telecom, retail and more). Each describes the business problem, the Databricks solution, the tech stack, and ships runnable code and SQL.',
                    capabilities: ['Filter prototypes by industry or keyword', 'Read the problem statement and solution design', 'Open each prototype\'s README, pipeline and SQL in the code viewer'],
                    steps: ['Search or filter to find a relevant industry', 'Expand a prototype card for problem and solution', 'Open the source files to reuse in your own workspace'],
                    assets: ['customer_prototypes_20'],
                    apis: ['GET /api/v1/prototypes', 'GET /api/v1/source/file?path=…'],
                },
                {
                    key: 'solutions-migration-sessions', kind: 'custom', title: '8 Migration Sessions',
                    summary: 'Eight guided sessions, each migrating one Palantir Foundry capability to its Databricks equivalent with a ready-to-run code artefact.',
                    capabilities: ['See the Foundry → Databricks mapping for each capability', 'Open the session code artefact', 'Follow the recommended session order'],
                    steps: ['Work through the sessions in order 1 → 8', 'Open each code artefact and read the inline comments', 'Practise the matching lab module afterwards'],
                    assets: ['migration_sessions'],
                    apis: ['GET /api/v1/source/tree?root=migration_sessions'],
                },
                {
                    key: 'solutions-reference-assets', kind: 'custom', title: 'Source vs. Target Reference Code',
                    summary: 'The reference Palantir estate (Ontology spec, transforms, Workshop, AIP agent, Apollo manifest) next to its migrated Databricks implementation (UC DDL, DLT, Apps, Mosaic AI agent, Lakeflow job, Asset Bundle).',
                    capabilities: ['Compare each source artefact to its migrated target', 'Browse every file in both estates', 'Use as templates for real migrations'],
                    steps: ['Review the artefact mapping table', 'Open a Palantir file, then its Databricks counterpart', 'Copy patterns into your own project'],
                    assets: ['Palantir', 'Databricks'],
                    apis: ['GET /api/v1/source/tree?root=Palantir', 'GET /api/v1/source/tree?root=Databricks'],
                },
            ],
        },
        // ---------------------------------------------------------------------
        {
            id: 'menu-platform', title: 'Platform Runtimes & Products', icon: 'ph-cpu', color: 'cyan',
            tagline: 'Databricks product modules, live workspace and big-data runtime',
            summary: 'The runtime side of the project: Python automation modules for each Databricks product pillar, the connection to your live Databricks workspace (Unity Catalog, Delta Sharing), and the local Spark + Kafka streaming runtime used by the labs and tests.',
            highlights: [
                '7 product modules: UP, UC, LK, LF, LB, AB and Genie',
                'Live workspace status, Delta Sharing and Unity Catalog scan',
                'Local Spark session, embedded Kafka cluster and streaming pipeline',
                'All modules are covered by the automated test suites',
            ],
            children: [
                {
                    key: 'platform-modular-products', kind: 'custom', title: 'Databricks Modular Products',
                    summary: 'Automation modules for each pillar of the Databricks Unified Platform: Unified Platform orchestrator (UP), Unity Catalog (UC), Lakehouse storage (LK), Lakeflow (LF), Lakebase (LB), Agent Bricks / Mosaic AI (AB) and Genie.',
                    capabilities: ['Understand what each product pillar does in the migration', 'See how the pillars depend on each other', 'Open each module\'s Python implementation'],
                    steps: ['Study the platform dependency diagram', 'Read the pillar cards in dependency order', 'Open the code for the pillar you are implementing'],
                    assets: ['UP', 'UC', 'LK', 'LF', 'LB', 'AB', 'Genie'],
                    apis: [],
                },
                {
                    key: 'platform-live-workspace', kind: 'custom', title: 'Live Databricks Workspace',
                    summary: 'Connection status for the configured Databricks workspace (AWS us-east-2), plus Delta Sharing configuration and a Unity Catalog scan. Add a Personal Access Token to enable live calls.',
                    capabilities: ['Check workspace connection and token status', 'Inspect Delta Sharing shares and recipient', 'Review the Unity Catalog scan summary', 'Open the workspace with one click'],
                    steps: ['Review connection status', 'Optionally add a PAT token for live calls', 'Inspect Delta Sharing and the UC scan'],
                    assets: ['databricks_live_workspace'],
                    apis: ['GET /api/v1/workspace/status', 'GET /api/v1/workspace/delta-sharing', 'GET /api/v1/workspace/unity-catalog-scan', 'POST /api/v1/workspace/set-token'],
                },
                {
                    key: 'platform-bigdata-runtime', kind: 'custom', title: 'Big Data Runtime (Spark & Kafka)',
                    summary: 'A local big-data runtime for labs and tests: a managed Spark session, an embedded Kafka cluster, and a Kafka → Spark Structured Streaming → Delta pipeline.',
                    capabilities: ['Understand the local streaming architecture', 'Open the Spark, Kafka and pipeline code', 'Learn the configuration variables'],
                    steps: ['Review the runtime data-flow diagram', 'Open each component\'s code', 'Run test suite 13 to exercise the runtime'],
                    assets: ['bigdata_runtime'],
                    apis: [],
                },
            ],
        },
        // ---------------------------------------------------------------------
        {
            id: 'menu-advisory', title: 'Academy & Certifications', icon: 'ph-graduation-cap', color: 'purple',
            tagline: 'Certification prep, consulting playbooks, interviews and test results',
            summary: 'Professional enablement for architects, consultants and engineers: Databricks certification paths and practice tests, the consultant engagement playbook, a senior technical interview guide, and the automated test suites that certify this project.',
            highlights: [
                'Official Databricks certification tracks and practice resources',
                'Consultant discovery, alignment and cutover playbook',
                'Technical interview scenarios for migration roles',
                'Automated test suite results and certificate',
            ],
            children: [
                {
                    key: 'certifications-training', kind: 'view', title: 'Certifications & Practice Tests',
                    summary: 'Curated Databricks certification tracks (Data Engineer Associate/Professional, Generative AI Engineer, Platform Administrator and more) with exam guides, free training and practice tests.',
                    capabilities: ['Choose a certification track', 'Follow the recommended learning path', 'Take practice tests to check readiness'],
                    steps: ['Select the certification that matches your role', 'Complete the linked training', 'Attempt the practice tests'],
                    assets: [], apis: [],
                },
                {
                    key: 'advisory-playbook', kind: 'view', title: 'Consultant Strategy Playbook',
                    summary: 'The consulting engagement framework: discovery workstreams, stakeholder alignment, TCO rationalisation, delivery waves and production cutover protocols.',
                    capabilities: ['Plan a 4-week discovery', 'Align business and technical stakeholders', 'Structure migration waves and cutover'],
                    steps: ['Read the engagement phases', 'Adapt the discovery checklist to your client', 'Download the full Consultant Playbook .docx'],
                    assets: ['Palantir to Databricks Migration Consultant.docx'], apis: [],
                },
                {
                    key: 'advisory-interview', kind: 'view', title: 'Technical Interview Guide',
                    summary: 'Interview preparation for Palantir → Databricks migration roles: architecture differences, Ontology → Unity Catalog mapping, Markings → ABAC, and scenario-based questions.',
                    capabilities: ['Practise architecture and design questions', 'Review model answers', 'Prepare scenario-based case studies'],
                    steps: ['Read questions by topic', 'Answer before revealing the model answer', 'Download the full Interview Guide .docx'],
                    assets: ['Palantir to Databricks Migration Consultant technical Interview Preparation Guide.docx'], apis: [],
                },
                {
                    key: 'test-suites-runner', kind: 'view', title: 'Automated Test Suites',
                    summary: 'Results of the project\'s automated unit, integration and stress test suites, including converters, reconciliation, Mosaic AI guardrails, frontend APIs, curriculum, runtimes and live workspace client.',
                    capabilities: ['See which components are covered by tests', 'Review the latest pass/fail certificate', 'Learn how to re-run the suite locally'],
                    steps: ['Review the suite list', 'Check the latest certificate', 'Run "python3 run_tests.py" to regenerate it'],
                    assets: ['test_suites', 'run_tests.py'],
                    apis: ['GET /api/v1/test-certificate'],
                },
            ],
        },
        // ---------------------------------------------------------------------
        {
            id: 'menu-downloads', title: 'Document Deliverables', icon: 'ph-file-doc', color: 'rose',
            tagline: '11 professionally formatted Word (.docx) guides',
            summary: 'Every written deliverable produced by the project, ready for executive briefings, client workshops and engineer onboarding. Each document has its own overview page describing its audience and contents before you download it.',
            highlights: [
                'Start with the Master Compendium for the full picture',
                'Implementation plans for Genie/Ontology and Oracle/Snowflake',
                'Playbooks, curriculum and interview guides for delivery teams',
                'Platform guides for Palantir, Databricks and the migration',
            ],
            children: [
                ['master-compendium', 'Enterprise Master Compendium', 'Executives & program leads', 'The unified guide summarising every capability in this project: architecture, multi-source migration matrix, AI innovations, labs, tooling and final recommendations.', ['Executive summary and recommendations', 'Multi-platform migration matrix', 'Capability catalogue across all menus']],
                ['genie-ontology-plan', 'Genie & Ontology Implementation Plan', 'Architects & data stewards', 'Detailed plan for the semantic layer: Unity Catalog pages, Metric Views, OntoRank, steward review queues, Genie spaces and UniForm Iceberg v2.', ['Semantic architecture', 'Metric View and OntoRank design', 'Rollout and governance plan']],
                ['ai-migration-plan', 'AI-Enabled Multi-Platform Migration Plan', 'Migration leads & engineers', 'Plan for AI-assisted migration of Oracle and Snowflake workloads, including transpiler agents, CDC, federation and automated reconciliation.', ['Phased tri-platform roadmap', 'AI transpiler agents', 'Reconciliation and cutover']],
                ['decoupling-playbook', 'Architectural Decoupling & Migration Playbook', 'Architects', 'How to untangle tightly coupled Foundry systems into open Lakehouse layers, with migration paths for each Foundry capability.', ['Coupling analysis', 'Per-capability migration paths', 'Target-state reference architecture']],
                ['200-labs-guide', '200 Hands-On Labs Guide', 'Engineers & trainers', 'The complete 200-lab curriculum with step-by-step instructions, code and verification criteria for all 10 modules.', ['10 modules / 200 labs', 'Step-by-step instructions', 'Verification checklists']],
                ['consultant-playbook', 'Consultant Strategy Playbook', 'Consultants & engagement managers', 'Engagement framework covering discovery, stakeholder alignment, TCO justification, delivery waves and cutover.', ['Discovery workstream', 'Stakeholder alignment', 'Delivery and cutover protocols']],
                ['interview-guide', 'Technical Interview Preparation Guide', 'Candidates & hiring managers', 'Interview questions and model answers for Palantir → Databricks migration consultant roles.', ['Architecture questions', 'Security and governance scenarios', 'Case studies']],
                ['migration-guide', 'Palantir to Databricks Migration Guide', 'Engineering teams', 'Practical migration guide covering datasets, transforms, Ontology, actions, apps and AI components.', ['Component-by-component migration', 'Validation approach', 'Common pitfalls']],
                ['comparison-matrix', 'Palantir vs. Databricks Comparison Matrix', 'Decision makers', 'Detailed capability comparison and scoring across all enterprise categories.', ['Capability-by-capability comparison', 'Weighted scoring', 'Decision guidance']],
                ['palantir-guide', 'Palantir Implementation Guide', 'Teams assessing the source estate', 'Reference guide to the Palantir Foundry source estate: Ontology, Code Repositories, Workshop, AIP and Apollo.', ['Foundry component overview', 'Source artefact inventory', 'Assessment checklist']],
                ['databricks-guide', 'Databricks Implementation Guide', 'Platform & engineering teams', 'Reference guide to the Databricks target platform: Unity Catalog, DLT, Lakeflow, Apps, Mosaic AI and Asset Bundles.', ['Target platform components', 'Deployment patterns', 'Operational best practices']],
            ].map(([docKey, title, audience, summary, contents]) => ({
                key: 'doc-' + docKey, kind: 'doc', docKey, title, audience, summary,
                capabilities: contents.map((c) => 'Contains: ' + c).concat(['Download as an editable Word document']),
                steps: ['Read this overview to confirm the document fits your need', 'Click Download to save the .docx', 'Open in Microsoft Word or Google Docs'],
                assets: [], apis: ['GET /api/download/' + docKey],
            })),
        },
    ];

    // Build lookup index: key -> entry
    const INDEX = { 'project-overview': { type: 'home' } };
    NAV.forEach((menu, mIdx) => {
        INDEX[menu.id + '-page'] = { type: 'menu', menu, mIdx };
        menu.children.forEach((child, idx) => { INDEX[child.key] = { type: 'child', menu, child, idx, mIdx }; });
    });

    // Capture original renderers from index.html before overriding them
    const origLoadView = window.loadView;
    const origLoadLabsModule = window.loadLabsModule;

    // =========================================================================
    // ROUTER
    // =========================================================================
    let booted = false;

    function currentKey() {
        const k = decodeURIComponent((location.hash || '').replace(/^#\/?/, ''));
        return INDEX[k] ? k : 'project-overview';
    }

    function go(key) {
        if (!INDEX[key]) key = 'project-overview';
        const hash = '#/' + key;
        if (location.hash === hash) render(key); else location.hash = hash;
    }

    window.addEventListener('hashchange', () => { if (booted) render(currentKey()); });

    function render(key) {
        const entry = INDEX[key];
        const ws = document.getElementById('workspace-dynamic-view');
        if (!entry || !ws) return;

        if (entry.type === 'home') {
            origLoadView('project-overview');
            enhanceHome(ws);
        } else if (entry.type === 'menu') {
            renderMenuOverview(entry, ws);
        } else {
            const c = entry.child;
            if (c.kind === 'lab') origLoadLabsModule(c.modId);
            else if (c.kind === 'view') origLoadView(c.key);
            else ws.innerHTML = '';

            ws.insertAdjacentHTML('afterbegin', subMenuOverviewPanel(entry));
            if (c.kind === 'doc') ws.insertAdjacentHTML('beforeend', docBody(entry));
            if (c.kind === 'custom') {
                const holder = document.createElement('div');
                holder.className = 'space-y-6';
                ws.appendChild(holder);
                (CUSTOM_VIEWS[c.key] || (() => {}))(holder);
            }
            ws.insertAdjacentHTML('beforeend', pagerFooter(entry));
        }

        setBreadcrumb(entry);
        syncSidebar(key, entry);
        const main = document.getElementById('main-content');
        if (main) main.scrollTop = 0;
        const pageTitle = entry.type === 'home' ? 'Project Overview'
            : entry.type === 'menu' ? entry.menu.title + ' Overview' : entry.child.title;
        document.title = pageTitle + ' | Palantir → Databricks Modernization Hub';
    }

    // =========================================================================
    // SIDEBAR (generated from NAV)
    // =========================================================================
    function renderSidebar() {
        const nav = document.querySelector('#left-sidebar nav');
        if (!nav) return;
        nav.id = 'sidebar-nav';
        nav.innerHTML = `
            <a href="#/project-overview" data-key="project-overview" class="nav-menu-link flex items-center gap-2 px-3 py-2 rounded text-slate-200 hover:text-white hover:bg-slate-800/60 font-bold transition">
                <i class="ph-bold ph-house text-sky-400"></i> Project Overview
            </a>
            <div class="px-3 pt-3 pb-1 text-[10px] uppercase tracking-wider text-slate-500 font-bold">Menus</div>
            ${NAV.map((m) => {
                const t = THEME[m.color];
                return `
                <div data-menu="${m.id}">
                    <div class="flex items-center">
                        <a href="#/${m.id}-page" data-key="${m.id}-page" class="nav-menu-link flex-1 flex items-center gap-2 px-3 py-2 rounded text-slate-300 hover:text-white hover:bg-slate-800/60 font-semibold transition">
                            <i class="ph-bold ${m.icon} ${t.icon}"></i>
                            <span class="flex-1">${esc(m.title)}</span>
                            <span class="text-[9px] px-1.5 py-0.5 rounded bg-slate-800 text-slate-400 border border-slate-700">${m.children.length}</span>
                        </a>
                        <button type="button" title="Expand / collapse" onclick="NavRouter.toggle('${m.id}')" class="p-1.5 rounded text-slate-500 hover:text-white hover:bg-slate-800/60">
                            <i id="icon-${m.id}" class="ph-bold ph-caret-down transition-transform -rotate-90"></i>
                        </button>
                    </div>
                    <div id="${m.id}" class="hidden mt-0.5 mb-1 ml-5 pl-2 border-l border-slate-800 space-y-0.5">
                        <a href="#/${m.id}-page" data-key="${m.id}-page" class="sidebar-sub-item flex items-center gap-1.5 px-3 py-1.5 rounded text-slate-400 hover:text-white transition italic">
                            <i class="ph ph-info"></i> Menu Overview
                        </a>
                        ${m.children.map((c) => `
                            <a href="#/${c.key}" data-key="${c.key}" class="sidebar-sub-item block px-3 py-1.5 rounded text-slate-400 hover:text-white transition">${esc(c.title)}</a>
                        `).join('')}
                    </div>
                </div>`;
            }).join('')}
        `;
    }

    function setMenuOpen(menuId, open) {
        const panel = document.getElementById(menuId);
        const icon = document.getElementById('icon-' + menuId);
        if (!panel) return;
        panel.classList.toggle('hidden', !open);
        if (icon) icon.classList.toggle('-rotate-90', !open);
    }

    function toggle(menuId) {
        const panel = document.getElementById(menuId);
        if (panel) setMenuOpen(menuId, panel.classList.contains('hidden'));
    }

    function syncSidebar(key, entry) {
        document.querySelectorAll('#sidebar-nav [data-key]').forEach((el) => {
            el.classList.remove('active', 'bg-slate-800', 'text-white');
        });
        document.querySelectorAll(`#sidebar-nav [data-key="${key}"]`).forEach((el) => {
            el.classList.add(el.classList.contains('sidebar-sub-item') ? 'active' : 'bg-slate-800');
            el.classList.add('text-white');
        });
        const activeMenu = entry.menu ? entry.menu.id : null;
        NAV.forEach((m) => {
            const header = document.querySelector(`#sidebar-nav a.nav-menu-link[data-key="${m.id}-page"]`);
            if (header && m.id === activeMenu) header.classList.add('bg-slate-800', 'text-white');
            setMenuOpen(m.id, m.id === activeMenu);
        });
    }

    function setBreadcrumb(entry) {
        const cat = document.getElementById('breadcrumb-category');
        const act = document.getElementById('breadcrumb-active');
        if (!cat || !act) return;
        if (entry.type === 'home') {
            cat.textContent = 'Enterprise Modernization Hub';
            act.textContent = 'Project Capabilities Overview';
        } else {
            cat.innerHTML = `<a href="#/${entry.menu.id}-page" class="hover:text-blue-600 hover:underline">${esc(entry.menu.title)}</a>`;
            act.textContent = entry.type === 'menu' ? 'Menu Overview' : entry.child.title;
        }
    }

    // =========================================================================
    // PAGE BUILDING BLOCKS
    // =========================================================================
    function assetChip(path) {
        if (isBrowsable(path)) {
            return `<button type="button" onclick="NavRouter.openSource('${esc(path)}')" class="inline-flex items-center gap-1 px-2 py-1 rounded border border-slate-200 bg-slate-50 hover:bg-blue-50 hover:border-blue-300 text-[11px] font-mono text-slate-700 text-left">
                <i class="ph ph-folder-open text-blue-600"></i>${esc(path)}</button>`;
        }
        return `<span class="inline-flex items-center gap-1 px-2 py-1 rounded border border-slate-200 bg-white text-[11px] font-mono text-slate-600"><i class="ph ph-file-text text-slate-400"></i>${esc(path)}</span>`;
    }

    function subMenuOverviewPanel(entry) {
        const { menu, child: c, idx } = entry;
        const t = THEME[menu.color];
        const assets = c.assets || [];
        const apis = c.apis || [];
        return `
        <section data-nav-overview class="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
            <div class="px-6 py-5 bg-gradient-to-r ${t.grad} text-white">
                <div class="flex flex-wrap items-center gap-2 text-[11px]">
                    <span class="px-2 py-0.5 rounded bg-white/10 border border-white/20 font-bold uppercase tracking-wider">Sub-menu Overview</span>
                    <a href="#/${menu.id}-page" class="text-slate-300 hover:text-white hover:underline"><i class="ph-bold ${menu.icon} mr-1"></i>${esc(menu.title)}</a>
                    <span class="text-slate-500">•</span>
                    <span class="text-slate-400">Sub-menu ${idx + 1} of ${menu.children.length}</span>
                    ${c.audience ? `<span class="text-slate-500">•</span><span class="text-slate-300">Audience: ${esc(c.audience)}</span>` : ''}
                </div>
                <h1 class="text-2xl md:text-3xl font-black mt-2 tracking-tight">${esc(c.title)}</h1>
                <p class="text-sm text-slate-300 mt-2 max-w-4xl leading-relaxed">${esc(c.summary)}</p>
            </div>
            <div data-nav-overview-body class="grid grid-cols-1 md:grid-cols-3 divide-y md:divide-y-0 md:divide-x divide-slate-100">
                <div class="p-5">
                    <h3 class="text-[11px] font-bold uppercase tracking-wider ${t.eyebrow} mb-2"><i class="ph-bold ph-lightning mr-1"></i>What you can do here</h3>
                    <ul class="space-y-1.5 text-xs text-slate-700">
                        ${(c.capabilities || []).map((x) => `<li class="flex gap-2"><i class="ph-bold ph-check text-emerald-500 mt-0.5"></i><span>${esc(x)}</span></li>`).join('')}
                    </ul>
                </div>
                <div class="p-5">
                    <h3 class="text-[11px] font-bold uppercase tracking-wider ${t.eyebrow} mb-2"><i class="ph-bold ph-path mr-1"></i>How to use this page</h3>
                    <ol class="space-y-1.5 text-xs text-slate-700">
                        ${(c.steps || []).map((x, i) => `<li class="flex gap-2"><span class="w-4 h-4 shrink-0 rounded-full bg-slate-900 text-white text-[9px] font-bold flex items-center justify-center mt-0.5">${i + 1}</span><span>${esc(x)}</span></li>`).join('')}
                    </ol>
                </div>
                <div class="p-5 space-y-3">
                    <div>
                        <h3 class="text-[11px] font-bold uppercase tracking-wider ${t.eyebrow} mb-2"><i class="ph-bold ph-folder-simple mr-1"></i>Source assets</h3>
                        <div class="flex flex-wrap gap-1.5">${assets.length ? assets.map(assetChip).join('') : '<span class="text-xs text-slate-400">Content is embedded in this page.</span>'}</div>
                    </div>
                    ${apis.length ? `
                    <div>
                        <h3 class="text-[11px] font-bold uppercase tracking-wider ${t.eyebrow} mb-2"><i class="ph-bold ph-plugs-connected mr-1"></i>Backing APIs</h3>
                        <div class="space-y-1">${apis.map((a) => `<code class="block text-[11px] bg-slate-900 text-emerald-300 px-2 py-1 rounded">${esc(a)}</code>`).join('')}</div>
                    </div>` : ''}
                </div>
            </div>
            <div class="px-6 py-2.5 bg-slate-50 border-t border-slate-100 flex items-center justify-between text-[11px] text-slate-500">
                <span><i class="ph-bold ph-arrow-down mr-1"></i>The working area for this sub-menu is below.</span>
                <button type="button" onclick="NavRouter.toggleOverview(this)" class="font-semibold text-slate-600 hover:text-slate-900">Hide overview details</button>
            </div>
        </section>`;
    }

    function pagerFooter(entry) {
        const { menu, idx } = entry;
        const prev = menu.children[idx - 1];
        const next = menu.children[idx + 1];
        const t = THEME[menu.color];
        return `
        <nav class="flex flex-wrap items-stretch justify-between gap-3 pt-2" aria-label="Sub-menu navigation">
            ${prev ? `<a href="#/${prev.key}" class="flex-1 min-w-[180px] bg-white border border-slate-200 rounded-xl px-4 py-3 ${t.hover} transition">
                <div class="text-[10px] uppercase font-bold text-slate-400"><i class="ph-bold ph-arrow-left mr-1"></i>Previous sub-menu</div>
                <div class="text-sm font-bold text-slate-800 mt-0.5">${esc(prev.title)}</div></a>` : '<div class="flex-1 min-w-[180px]"></div>'}
            <a href="#/${menu.id}-page" class="min-w-[180px] bg-slate-900 text-white rounded-xl px-4 py-3 text-center hover:bg-slate-800 transition">
                <div class="text-[10px] uppercase font-bold text-slate-400">Back to menu</div>
                <div class="text-sm font-bold mt-0.5"><i class="ph-bold ${menu.icon} mr-1"></i>${esc(menu.title)} Overview</div></a>
            ${next ? `<a href="#/${next.key}" class="flex-1 min-w-[180px] bg-white border border-slate-200 rounded-xl px-4 py-3 text-right ${t.hover} transition">
                <div class="text-[10px] uppercase font-bold text-slate-400">Next sub-menu<i class="ph-bold ph-arrow-right ml-1"></i></div>
                <div class="text-sm font-bold text-slate-800 mt-0.5">${esc(next.title)}</div></a>` : '<div class="flex-1 min-w-[180px]"></div>'}
        </nav>`;
    }

    // ---------------------------------------------------------------------
    // MENU OVERVIEW PAGE (one per menu, generated from NAV)
    // ---------------------------------------------------------------------
    function renderMenuOverview(entry, ws) {
        const { menu: m, mIdx } = entry;
        const t = THEME[m.color];
        const prevMenu = NAV[mIdx - 1];
        const nextMenu = NAV[mIdx + 1];

        let extraStats = '';
        if (m.id === 'menu-200-labs' && typeof allModulesData !== 'undefined' && allModulesData.length) {
            const total = allModulesData.reduce((s, x) => s + (x.total_labs || (x.labs || []).length || 0), 0);
            extraStats = `<span class="px-2.5 py-1 rounded bg-white/10 border border-white/20 text-xs font-bold">${total} labs loaded</span>`;
        }

        ws.innerHTML = `
        <div class="space-y-6">
            <section class="bg-gradient-to-r ${t.grad} text-white p-6 md:p-8 rounded-2xl shadow-xl border border-white/10">
                <div class="flex flex-wrap items-center gap-2">
                    <span class="px-2.5 py-1 rounded bg-white/10 border border-white/20 text-xs font-bold uppercase tracking-wider">Menu Overview</span>
                    <span class="px-2.5 py-1 rounded bg-white/10 border border-white/20 text-xs font-bold">Menu ${mIdx + 1} of ${NAV.length}</span>
                    <span class="px-2.5 py-1 rounded bg-white/10 border border-white/20 text-xs font-bold">${m.children.length} sub-menus</span>
                    ${extraStats}
                </div>
                <h1 class="text-3xl md:text-4xl font-black mt-3 tracking-tight flex items-center gap-3"><i class="ph-bold ${m.icon} ${t.icon}"></i>${esc(m.title)}</h1>
                <p class="text-sm font-semibold text-slate-200 mt-1">${esc(m.tagline)}</p>
                <p class="text-sm text-slate-300 mt-3 max-w-4xl leading-relaxed">${esc(m.summary)}</p>
            </section>

            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <section class="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
                    <h2 class="text-sm font-bold text-slate-900 mb-3"><i class="ph-bold ph-target mr-1 ${t.eyebrow}"></i>What this menu covers</h2>
                    <ul class="space-y-2 text-xs text-slate-700">
                        ${m.highlights.map((h) => `<li class="flex gap-2"><i class="ph-bold ph-check-circle text-emerald-500 mt-0.5"></i><span>${esc(h)}</span></li>`).join('')}
                    </ul>
                </section>
                <section class="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
                    <h2 class="text-sm font-bold text-slate-900 mb-3"><i class="ph-bold ph-path mr-1 ${t.eyebrow}"></i>Recommended path through the sub-menus</h2>
                    <ol class="space-y-1.5 text-xs">
                        ${m.children.map((c, i) => `<li><a href="#/${c.key}" class="flex items-center gap-2 text-slate-700 hover:text-blue-600">
                            <span class="w-5 h-5 shrink-0 rounded-full bg-slate-900 text-white text-[10px] font-bold flex items-center justify-center">${i + 1}</span>
                            <span class="font-semibold">${esc(c.title)}</span></a></li>`).join('')}
                    </ol>
                </section>
            </div>

            <section>
                <h2 class="text-sm font-bold text-slate-900 mb-3">Sub-menus in ${esc(m.title)}</h2>
                <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
                    ${m.children.map((c, i) => `
                    <a href="#/${c.key}" class="group bg-white p-5 rounded-xl border border-slate-200 shadow-sm ${t.hover} hover:shadow-md transition flex flex-col">
                        <div class="flex items-center justify-between">
                            <span class="text-[10px] px-2 py-0.5 rounded border font-bold ${t.chip}">Sub-menu ${i + 1}</span>
                            ${c.audience ? `<span class="text-[10px] text-slate-500">${esc(c.audience)}</span>` : ''}
                        </div>
                        <h3 class="text-sm font-bold text-slate-900 mt-2">${esc(c.title)}</h3>
                        <p class="text-xs text-slate-600 mt-1.5 leading-relaxed flex-1">${esc(c.summary)}</p>
                        <ul class="mt-3 space-y-1 text-[11px] text-slate-600">
                            ${(c.capabilities || []).slice(0, 3).map((x) => `<li class="flex gap-1.5"><i class="ph-bold ph-dot-outline ${t.eyebrow}"></i>${esc(x)}</li>`).join('')}
                        </ul>
                        <span class="mt-3 pt-3 border-t border-slate-100 text-xs font-bold ${t.eyebrow}">Open sub-menu overview <i class="ph-bold ph-arrow-right ml-1 group-hover:translate-x-1 transition-transform inline-block"></i></span>
                    </a>`).join('')}
                </div>
            </section>

            <nav class="flex flex-wrap items-stretch justify-between gap-3 pt-2" aria-label="Menu navigation">
                ${prevMenu ? `<a href="#/${prevMenu.id}-page" class="flex-1 min-w-[180px] bg-white border border-slate-200 rounded-xl px-4 py-3 hover:border-slate-400 transition">
                    <div class="text-[10px] uppercase font-bold text-slate-400"><i class="ph-bold ph-arrow-left mr-1"></i>Previous menu</div>
                    <div class="text-sm font-bold text-slate-800 mt-0.5">${esc(prevMenu.title)}</div></a>` : '<div class="flex-1 min-w-[180px]"></div>'}
                <a href="#/project-overview" class="min-w-[180px] bg-slate-900 text-white rounded-xl px-4 py-3 text-center hover:bg-slate-800 transition">
                    <div class="text-[10px] uppercase font-bold text-slate-400">Back to</div>
                    <div class="text-sm font-bold mt-0.5"><i class="ph-bold ph-house mr-1"></i>Project Overview</div></a>
                ${nextMenu ? `<a href="#/${nextMenu.id}-page" class="flex-1 min-w-[180px] bg-white border border-slate-200 rounded-xl px-4 py-3 text-right hover:border-slate-400 transition">
                    <div class="text-[10px] uppercase font-bold text-slate-400">Next menu<i class="ph-bold ph-arrow-right ml-1"></i></div>
                    <div class="text-sm font-bold text-slate-800 mt-0.5">${esc(nextMenu.title)}</div></a>` : '<div class="flex-1 min-w-[180px]"></div>'}
            </nav>
        </div>`;
    }

    // ---------------------------------------------------------------------
    // PROJECT OVERVIEW enhancements (complete capability map of all menus)
    // ---------------------------------------------------------------------
    function enhanceHome(ws) {
        // Make the (previously non-clickable) 20 Customer Prototypes pillar route through its menu
        ws.querySelectorAll('h3').forEach((h) => {
            if (h.textContent.trim() === '20 Customer Prototypes') {
                const card = h.closest('div.bg-white');
                if (card) {
                    card.classList.add('cursor-pointer');
                    card.onclick = () => go('solutions-prototypes');
                }
            }
        });

        // Live test-certificate badge
        fetch('/api/v1/test-certificate').then((r) => (r.ok ? r.json() : null)).then((cert) => {
            if (!cert) return;
            const passed = cert.tests_run - cert.failures - cert.errors;
            const walker = document.createTreeWalker(ws, NodeFilter.SHOW_TEXT);
            const hits = [];
            while (walker.nextNode()) {
                if (/\d+\s*\/\s*\d+\s+Verified Production Tests/.test(walker.currentNode.nodeValue)) hits.push(walker.currentNode);
            }
            hits.forEach((n) => {
                n.nodeValue = n.nodeValue.replace(/\d+\s*\/\s*\d+(\s+Verified Production Tests)/, `${passed}/${cert.tests_run}$1`);
            });
        }).catch(() => {});

        const totalSub = NAV.reduce((s, m) => s + m.children.length, 0);
        const html = `
        <section data-capability-map class="space-y-4">
            <div class="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
                <div class="flex flex-wrap items-center justify-between gap-3">
                    <div>
                        <h2 class="text-base font-black text-slate-900 flex items-center gap-2"><i class="ph-bold ph-map-trifold text-blue-600"></i>Complete Capability Map</h2>
                        <p class="text-xs text-slate-600 mt-1 max-w-3xl">Everything in this portal is organised into <b>${NAV.length} menus</b> and <b>${totalSub} sub-menus</b>. Every menu opens a Menu Overview, and every sub-menu opens with its own Sub-menu Overview before the working area.</p>
                    </div>
                    <div class="flex items-center gap-1.5 text-[11px] font-semibold text-slate-600">
                        <span class="px-2 py-1 rounded bg-slate-900 text-white"><i class="ph-bold ph-house mr-1"></i>Project Overview</span>
                        <i class="ph-bold ph-caret-right text-slate-400"></i>
                        <span class="px-2 py-1 rounded bg-slate-100 border border-slate-200">Menu Overview</span>
                        <i class="ph-bold ph-caret-right text-slate-400"></i>
                        <span class="px-2 py-1 rounded bg-slate-100 border border-slate-200">Sub-menu Overview + Workspace</span>
                    </div>
                </div>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
                ${NAV.map((m, i) => {
                    const t = THEME[m.color];
                    return `
                    <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm ${t.hover} transition flex flex-col">
                        <a href="#/${m.id}-page" class="group">
                            <div class="flex items-center justify-between">
                                <span class="text-[10px] px-2 py-0.5 rounded border font-bold ${t.chip}">Menu ${i + 1} · ${m.children.length} sub-menus</span>
                                <i class="ph-bold ${m.icon} text-xl ${t.eyebrow}"></i>
                            </div>
                            <h3 class="text-sm font-bold text-slate-900 mt-2 group-hover:underline">${esc(m.title)}</h3>
                            <p class="text-[11px] font-semibold text-slate-500">${esc(m.tagline)}</p>
                        </a>
                        <ul class="mt-3 space-y-1 text-xs flex-1">
                            ${m.children.map((c) => `<li><a href="#/${c.key}" class="flex items-start gap-1.5 text-slate-600 hover:text-blue-600"><i class="ph-bold ph-caret-right text-[10px] mt-1 ${t.eyebrow}"></i>${esc(c.title)}</a></li>`).join('')}
                        </ul>
                        <a href="#/${m.id}-page" class="mt-3 pt-3 border-t border-slate-100 text-xs font-bold ${t.eyebrow}">Open ${esc(m.title)} overview <i class="ph-bold ph-arrow-right ml-1"></i></a>
                    </div>`;
                }).join('')}
            </div>
        </section>`;

        const pillars = ws.querySelector('.grid.lg\\:grid-cols-3');
        if (pillars) pillars.insertAdjacentHTML('afterend', html);
        else ws.insertAdjacentHTML('beforeend', html);
    }

    // ---------------------------------------------------------------------
    // DOCUMENT sub-menu body
    // ---------------------------------------------------------------------
    function docBody(entry) {
        const c = entry.child;
        const t = THEME[entry.menu.color];
        return `
        <section class="bg-white p-6 rounded-xl border border-slate-200 shadow-sm flex flex-wrap items-center justify-between gap-4">
            <div class="flex items-center gap-4">
                <div class="w-14 h-14 rounded-xl bg-blue-50 text-blue-700 flex items-center justify-center text-3xl"><i class="ph-bold ph-microsoft-word-logo"></i></div>
                <div>
                    <div class="text-[11px] uppercase font-bold text-slate-400">Microsoft Word document</div>
                    <div class="text-base font-bold text-slate-900">${esc(c.title)}</div>
                    <div class="text-xs text-slate-500">Intended audience: ${esc(c.audience)}</div>
                </div>
            </div>
            <a href="/api/download/${esc(c.docKey)}" class="px-5 py-2.5 ${t.btn} text-white font-bold rounded-lg text-sm shadow transition flex items-center gap-2">
                <i class="ph-bold ph-download-simple"></i> Download .docx
            </a>
        </section>`;
    }

    // =========================================================================
    // CUSTOM SUB-MENU VIEWS (new capability pages)
    // =========================================================================
    const card = (inner, extra = '') => `<section class="bg-white p-6 rounded-xl border border-slate-200 shadow-sm ${extra}">${inner}</section>`;
    const codeBtn = (path, label = 'View code') => `<button type="button" onclick="NavRouter.openSource('${esc(path)}')" class="inline-flex items-center gap-1 px-2.5 py-1 rounded bg-slate-900 hover:bg-slate-700 text-white text-[11px] font-semibold"><i class="ph-bold ph-code"></i>${esc(label)}</button>`;
    const loading = '<div class="text-xs text-slate-500 flex items-center gap-2"><i class="ph-bold ph-spinner animate-spin"></i>Loading…</div>';
    const errorBox = (msg) => `<div class="text-xs text-rose-700 bg-rose-50 border border-rose-200 rounded p-3">${esc(msg)}</div>`;

    async function getJSON(url, opts) {
        const r = await fetch(url, opts);
        if (!r.ok) throw new Error(`${r.status} ${r.statusText}`);
        return r.json();
    }

    async function runMermaid(container) {
        try { await mermaid.run({ nodes: container.querySelectorAll('.mermaid') }); } catch (e) { /* diagram is optional */ }
    }

    const CUSTOM_VIEWS = {
        // ---------------------------------------------------------------
        'solutions-prototypes': async (el) => {
            el.innerHTML = card(loading);
            let data;
            try { data = await getJSON('/api/v1/prototypes'); } catch (e) { el.innerHTML = card(errorBox('Could not load prototypes: ' + e.message)); return; }
            const protos = data.prototypes;
            const industries = [...new Set(protos.map((p) => p.industry))].sort();
            el.innerHTML = `
                ${card(`
                    <div class="flex flex-wrap items-center gap-3">
                        <div class="flex items-center bg-slate-50 border border-slate-200 rounded-lg px-3 py-1.5 flex-1 min-w-[220px]">
                            <i class="ph ph-magnifying-glass text-slate-400 mr-2"></i>
                            <input id="proto-search" type="text" placeholder="Search prototypes, tech stack, problem…" class="bg-transparent text-xs text-slate-800 w-full focus:outline-none">
                        </div>
                        <select id="proto-industry" class="border border-slate-200 rounded-lg px-3 py-1.5 text-xs text-slate-700 bg-white">
                            <option value="">All industries (${industries.length})</option>
                            ${industries.map((i) => `<option>${esc(i)}</option>`).join('')}
                        </select>
                        <span id="proto-count" class="text-xs font-semibold text-slate-500"></span>
                    </div>`)}
                <div id="proto-grid" class="grid grid-cols-1 lg:grid-cols-2 gap-4"></div>`;

            const grid = el.querySelector('#proto-grid');
            const draw = () => {
                const q = el.querySelector('#proto-search').value.toLowerCase();
                const ind = el.querySelector('#proto-industry').value;
                const list = protos.filter((p) => (!ind || p.industry === ind) &&
                    (!q || [p.title, p.industry, p.tech_stack, p.problem, p.solution].join(' ').toLowerCase().includes(q)));
                el.querySelector('#proto-count').textContent = `${list.length} of ${protos.length} prototypes`;
                grid.innerHTML = list.map((p) => `
                    <article class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm hover:border-indigo-400 transition space-y-3">
                        <div class="flex items-center justify-between gap-2">
                            <span class="text-[10px] font-mono font-bold px-2 py-0.5 rounded bg-indigo-50 text-indigo-700 border border-indigo-200">${esc(p.id)}</span>
                            <span class="text-[10px] font-semibold text-slate-500">${esc(p.industry)}</span>
                        </div>
                        <h3 class="text-sm font-bold text-slate-900">${esc(p.title)}</h3>
                        <div class="flex flex-wrap gap-1">${p.tech_stack.split(',').map((s) => `<span class="text-[10px] px-1.5 py-0.5 rounded bg-slate-100 text-slate-700">${esc(s.trim())}</span>`).join('')}</div>
                        <div class="grid grid-cols-1 gap-2 text-xs">
                            <div class="bg-rose-50 border border-rose-100 rounded p-2.5"><div class="text-[10px] uppercase font-bold text-rose-700">Problem</div><div class="text-slate-700 mt-0.5">${esc(p.problem)}</div></div>
                            <div class="bg-emerald-50 border border-emerald-100 rounded p-2.5"><div class="text-[10px] uppercase font-bold text-emerald-700">Databricks solution</div><div class="text-slate-700 mt-0.5">${esc(p.solution)}</div></div>
                        </div>
                        <div class="flex flex-wrap gap-1.5 pt-1">${(p.files || []).map((f) => codeBtn(`customer_prototypes_20/${p.id}/${f}`, f)).join('')}</div>
                    </article>`).join('') || '<div class="text-xs text-slate-500">No prototypes match the filter.</div>';
            };
            el.querySelector('#proto-search').addEventListener('input', draw);
            el.querySelector('#proto-industry').addEventListener('change', draw);
            draw();
        },

        // ---------------------------------------------------------------
        'solutions-migration-sessions': (el) => {
            const sessions = [
                ['session_01_datasets_to_delta', 'Foundry Datasets', 'Delta Lake + UniForm (Iceberg)', 'step_by_step_uniform_migration.py', 'Move Foundry datasets into Delta tables with UniForm Iceberg metadata for open, zero-copy access.', 'lab-mod_001_025'],
                ['session_02_repositories_to_pyspark_dabs', 'Code Repositories', 'Modular PySpark + Asset Bundles', 'pyspark_modular_transform.py', 'Refactor Foundry transforms into modular PySpark packaged and deployed with Databricks Asset Bundles.', 'lab-mod_001_025'],
                ['session_03_pipeline_builder_to_dlt', 'Pipeline Builder', 'Delta Live Tables / Lakeflow', 'dlt_declarative_pipeline.py', 'Recreate Pipeline Builder graphs as declarative DLT pipelines with expectations.', 'lab-mod_026_050'],
                ['session_04_ontology_to_unity_catalog', 'Ontology', 'Unity Catalog', 'ontology_to_unity_catalog.sql', 'Model object types, properties and links as governed Unity Catalog tables and views.', 'lab-mod_051_075'],
                ['session_05_actions_to_databricks_apps', 'Ontology Actions', 'Databricks Apps (FastAPI)', 'fastapi_action_service.py', 'Implement write-back actions as an audited FastAPI service hosted on Databricks Apps.', 'lab-mod_076_100'],
                ['session_06_workshop_to_streamlit_aibi', 'Workshop', 'Streamlit Apps + AI/BI', 'streamlit_cockpit_app.py', 'Rebuild Workshop operational UIs as Streamlit apps and AI/BI dashboards.', 'lab-mod_126_150'],
                ['session_07_aip_to_mosaic_ai', 'AIP / AIP Logic', 'Mosaic AI Agent Framework', 'mosaic_ai_agent.py', 'Port AIP agents to Mosaic AI with tools, evaluation and human-in-the-loop guardrails.', 'lab-mod_151_175'],
                ['session_08_markings_to_abac_rls', 'Markings & Permissions', 'Unity Catalog ABAC / RLS', 'abac_security_ddl.sql', 'Translate Markings into ABAC policies, row filters and column masks.', 'lab-mod_101_125'],
            ];
            el.innerHTML = card(`
                <h2 class="text-sm font-bold text-slate-900 mb-3"><i class="ph-bold ph-arrows-left-right text-indigo-600 mr-1"></i>Foundry → Databricks session map</h2>
                <div class="overflow-x-auto">
                    <table class="w-full text-xs">
                        <thead><tr class="text-left text-[10px] uppercase text-slate-500 border-b border-slate-200">
                            <th class="p-2">#</th><th class="p-2">Palantir Foundry</th><th class="p-2">Databricks target</th><th class="p-2">What you do</th><th class="p-2">Artefact</th><th class="p-2">Practice</th></tr></thead>
                        <tbody>
                        ${sessions.map(([dir, from, to, file, desc, lab], i) => `
                            <tr class="border-b border-slate-100 align-top">
                                <td class="p-2 font-bold text-slate-400">${i + 1}</td>
                                <td class="p-2 font-semibold text-rose-700">${esc(from)}</td>
                                <td class="p-2 font-semibold text-emerald-700">${esc(to)}</td>
                                <td class="p-2 text-slate-600">${esc(desc)}</td>
                                <td class="p-2">${codeBtn(`migration_sessions/${dir}/${file}`, file)}</td>
                                <td class="p-2"><a href="#/${lab}" class="text-blue-600 hover:underline whitespace-nowrap">${esc(INDEX[lab].child.title.split(':')[0])} →</a></td>
                            </tr>`).join('')}
                        </tbody>
                    </table>
                </div>`);
        },

        // ---------------------------------------------------------------
        'solutions-reference-assets': async (el) => {
            const mapping = [
                ['Ontology definitions', 'Palantir/ontology_definitions/enterprise_ontology_spec.json', 'Unity Catalog DDL', 'Databricks/unity_catalog/unity_catalog_ddl.sql'],
                ['Code Repository transforms', 'Palantir/code_repositories/customer_supply_chain_transforms.py', 'DLT pipeline', 'Databricks/dlt_pipelines/supply_chain_dlt_pipeline.py'],
                ['Workshop application', 'Palantir/workshop_specs/supply_chain_workshop_spec.json', 'Databricks App', 'Databricks/databricks_apps/app.py'],
                ['Ontology action functions', 'Palantir/ontology_definitions/action_functions.ts', 'App write-back service', 'Databricks/databricks_apps/app.yaml'],
                ['AIP agent', 'Palantir/aip_agents/supply_chain_agent_spec.json', 'Mosaic AI agent', 'Databricks/mosaic_ai/supply_chain_mosaic_agent.py'],
                ['Apollo deployment manifest', 'Palantir/apollo_manifests/apollo_deployment_manifest.yaml', 'Asset Bundle + Lakeflow job', 'Databricks/dabs/databricks.yml'],
            ];
            el.innerHTML = card(`
                <h2 class="text-sm font-bold text-slate-900 mb-3"><i class="ph-bold ph-git-diff text-indigo-600 mr-1"></i>Source → target artefact mapping</h2>
                <div class="overflow-x-auto"><table class="w-full text-xs">
                    <thead><tr class="text-left text-[10px] uppercase text-slate-500 border-b border-slate-200"><th class="p-2">Palantir source</th><th class="p-2"></th><th class="p-2">Databricks target</th></tr></thead>
                    <tbody>${mapping.map(([a, ap, b, bp]) => `
                        <tr class="border-b border-slate-100">
                            <td class="p-2"><div class="font-semibold text-rose-700">${esc(a)}</div><div class="mt-1">${codeBtn(ap, ap.split('/').pop())}</div></td>
                            <td class="p-2 text-slate-400"><i class="ph-bold ph-arrow-right"></i></td>
                            <td class="p-2"><div class="font-semibold text-emerald-700">${esc(b)}</div><div class="mt-1">${codeBtn(bp, bp.split('/').pop())}</div></td>
                        </tr>`).join('')}
                    </tbody></table></div>`) + `<div id="ref-trees" class="grid grid-cols-1 md:grid-cols-2 gap-4">${card(loading)}</div>`;
            const trees = el.querySelector('#ref-trees');
            try {
                const [pal, dbx] = await Promise.all([getJSON('/api/v1/source/tree?root=Palantir'), getJSON('/api/v1/source/tree?root=Databricks')]);
                const list = (title, color, d) => card(`
                    <h3 class="text-sm font-bold ${color} mb-2">${title} <span class="text-slate-400 font-normal">(${d.total} files)</span></h3>
                    <div class="space-y-1">${d.files.map((f) => `<button type="button" onclick="NavRouter.openSource('${esc(f.path)}')" class="w-full text-left text-[11px] font-mono px-2 py-1 rounded hover:bg-slate-100 text-slate-700 flex justify-between"><span>${esc(f.path)}</span><span class="text-slate-400">${(f.size_bytes / 1024).toFixed(1)} KB</span></button>`).join('')}</div>`);
                trees.innerHTML = list('Palantir source estate', 'text-rose-700', pal) + list('Databricks target estate', 'text-emerald-700', dbx);
            } catch (e) { trees.innerHTML = card(errorBox('Could not load file trees: ' + e.message)); }
        },

        // ---------------------------------------------------------------
        'platform-modular-products': async (el) => {
            const products = [
                ['UP', 'Unified Platform Orchestrator', 'UP/scripts/unified_platform_orchestrator.py', 'Deploys and health-checks all six product pillars as one platform per environment.'],
                ['UC', 'Unity Catalog Governance', 'UC/scripts/unity_catalog_governance_automation.py', 'Catalogs, schemas, grants, ABAC tags, lineage and UniForm Iceberg governance.'],
                ['LK', 'Lakehouse Storage Engine', 'LK/scripts/lakehouse_iceberg_engine.py', 'Delta Lake storage with Photon, liquid clustering and Iceberg v2 compatibility.'],
                ['LF', 'Lakeflow Pipelines & Jobs', 'LF/scripts/lakeflow_pipeline_automation.py', 'Lakeflow Connect CDC ingestion, declarative pipelines and job orchestration.'],
                ['LB', 'Lakebase Operational Store', 'LB/scripts/lakebase_operational_store.py', 'Low-latency operational state and ACID write-back for Databricks Apps.'],
                ['AB', 'Agent Bricks / Mosaic AI', 'AB/scripts/agent_bricks_mosaic_runtime.py', 'Compound AI agents, evaluation, model serving and HITL guardrails.'],
                ['Genie', 'Genie AI/BI Spaces', 'Genie/scripts/genie_space_automation.py', 'Natural-language-to-SQL over certified UC pages with ambiguity escalation.'],
            ];
            el.innerHTML = card(`
                <h2 class="text-sm font-bold text-slate-900 mb-3"><i class="ph-bold ph-graph text-cyan-600 mr-1"></i>Platform dependency diagram</h2>
                <div class="mermaid text-xs bg-slate-50 p-4 rounded-lg border border-slate-100 overflow-x-auto">
flowchart LR
    LF["LF · Lakeflow"] --> LK["LK · Lakehouse Storage"]
    LK --> UC["UC · Unity Catalog"]
    UC --> LB["LB · Lakebase / Apps"]
    UC --> AB["AB · Agent Bricks"]
    UC --> GENIE["Genie · AI/BI"]
    UP["UP · Unified Orchestrator"] -.deploys.-> LF
    UP -.deploys.-> UC
    UP -.deploys.-> AB
                </div>`) + `
                <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
                    ${products.map(([code, name, path, desc]) => `
                    <article class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm hover:border-cyan-400 transition flex flex-col">
                        <div class="flex items-center gap-2"><span class="px-2 py-0.5 rounded bg-cyan-50 text-cyan-800 border border-cyan-200 text-[11px] font-black font-mono">/${code}</span><h3 class="text-sm font-bold text-slate-900">${esc(name)}</h3></div>
                        <p class="text-xs text-slate-600 mt-2 flex-1">${esc(desc)}</p>
                        <div class="mt-3 flex flex-wrap gap-1.5">${codeBtn(path, path.split('/').pop())}${code === 'UP' ? codeBtn('UP/README.md', 'README.md') : ''}</div>
                    </article>`).join('')}
                </div>`;
            runMermaid(el);
        },

        // ---------------------------------------------------------------
        'platform-live-workspace': async (el) => {
            el.innerHTML = card(loading);
            const draw = async () => {
                let status, sharing, scan;
                try {
                    [status, sharing, scan] = await Promise.all([
                        getJSON('/api/v1/workspace/status'),
                        getJSON('/api/v1/workspace/delta-sharing'),
                        getJSON('/api/v1/workspace/unity-catalog-scan'),
                    ]);
                } catch (e) { el.innerHTML = card(errorBox('Could not reach workspace APIs: ' + e.message)); return; }
                const ok = status.token_configured;
                const kv = (k, v, mono = true) => `<div><div class="text-[10px] uppercase font-bold text-slate-400">${esc(k)}</div><div class="${mono ? 'font-mono' : ''} text-xs text-slate-800 font-semibold break-all mt-0.5">${esc(v)}</div></div>`;
                el.innerHTML = card(`
                    <div class="flex flex-wrap items-center justify-between gap-3 pb-3 border-b border-slate-100">
                        <div class="flex items-center gap-3">
                            <span class="w-3 h-3 rounded-full ${ok ? 'bg-emerald-500' : 'bg-amber-400'} animate-pulse"></span>
                            <div><div class="text-sm font-bold text-slate-900">Connection status: ${esc(status.status)}</div>
                            <div class="text-xs text-slate-500">${esc(status.instructions || (ok ? 'Token configured – live calls enabled.' : ''))}</div></div>
                        </div>
                        <a href="${esc(status.workspace_host)}" target="_blank" rel="noopener" class="px-3.5 py-1.5 bg-red-600 hover:bg-red-700 text-white rounded-lg text-xs font-bold flex items-center gap-1.5"><i class="ph-bold ph-arrow-square-out"></i>Open workspace</a>
                    </div>
                    <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mt-4">
                        ${kv('Workspace ID', status.workspace_id)}${kv('Cloud / Region', `${status.cloud_provider} / ${status.region}`)}
                        ${kv('User', status.user_email)}${kv('SDK client ready', String(status.sdk_client_ready))}
                    </div>`) + `
                <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
                    ${card(`
                        <h3 class="text-sm font-bold text-slate-900 mb-3"><i class="ph-bold ph-share-network text-cyan-600 mr-1"></i>Delta Sharing</h3>
                        <div class="grid grid-cols-2 gap-3">${kv('Status', sharing.status)}${kv('Sharing type', sharing.sharing_type)}${kv('Recipient', sharing.recipient_name)}${kv('Open sharing ID', sharing.open_sharing_id)}</div>
                        <div class="mt-3 space-y-2">${(sharing.shares_accessible || []).map((s) => `
                            <div class="border border-slate-200 rounded p-3 text-xs"><div class="font-bold text-slate-800">${esc(s.share_name)} ${s.uniform_iceberg_enabled ? '<span class="ml-1 text-[10px] px-1.5 py-0.5 rounded bg-purple-50 text-purple-700 border border-purple-200">UniForm Iceberg</span>' : ''}</div>
                            <div class="mt-1 font-mono text-slate-600">${(s.tables || []).map(esc).join('<br>')}</div></div>`).join('')}</div>
                        <div class="mt-3">${codeBtn('databricks_live_workspace/delta_sharing/delta_sharing_setup.sql', 'delta_sharing_setup.sql')}</div>`)}
                    ${card(`
                        <h3 class="text-sm font-bold text-slate-900 mb-3"><i class="ph-bold ph-database text-cyan-600 mr-1"></i>Unity Catalog scan</h3>
                        <div class="grid grid-cols-2 gap-3">${kv('Mode', scan.mode)}${kv('Status', scan.status)}${kv('Governed tables', scan.governed_tables)}${kv('Metric views', scan.metric_views)}</div>
                        <div class="mt-3 flex flex-wrap gap-1.5">${(scan.catalogs || []).map((c) => `<span class="px-2 py-1 rounded bg-slate-100 text-slate-700 text-[11px] font-mono">${esc(c)}</span>`).join('')}</div>
                        <div class="mt-4 pt-3 border-t border-slate-100">
                            <label class="text-[11px] font-bold text-slate-600">Personal Access Token (enables live calls; kept in server memory only)</label>
                            <div class="flex gap-2 mt-1">
                                <input id="pat-input" type="password" autocomplete="off" placeholder="dapi…" class="flex-1 border border-slate-300 rounded px-2 py-1.5 text-xs">
                                <button id="pat-save" type="button" class="px-3 py-1.5 bg-cyan-600 hover:bg-cyan-700 text-white rounded text-xs font-bold">Apply</button>
                            </div>
                            <div id="pat-msg" class="text-[11px] mt-1 text-slate-500"></div>
                        </div>`)}
                </div>`;
                el.querySelector('#pat-save').onclick = async () => {
                    const token = el.querySelector('#pat-input').value.trim();
                    const msg = el.querySelector('#pat-msg');
                    if (!token) { msg.textContent = 'Enter a token first.'; return; }
                    try {
                        await getJSON('/api/v1/workspace/set-token', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ token }) });
                        msg.textContent = 'Token applied. Refreshing status…';
                        draw();
                    } catch (e) { msg.textContent = 'Failed: ' + e.message; }
                };
            };
            draw();
        },

        // ---------------------------------------------------------------
        'platform-bigdata-runtime': (el) => {
            const comps = [
                ['Spark Session Manager', 'bigdata_runtime/spark_instance/spark_session_manager.py', 'Creates and manages a local Spark session (SPARK_MASTER, shuffle partitions) used by labs and tests.', 'ph-lightning'],
                ['Embedded Kafka Cluster', 'bigdata_runtime/kafka_engine/embedded_kafka_cluster.py', 'In-process Kafka broker for topics, producers and consumers (KAFKA_BROKER_PORT).', 'ph-broadcast'],
                ['Kafka → Spark Streaming Pipeline', 'bigdata_runtime/streaming_pipeline/kafka_spark_streaming_pipeline.py', 'Structured Streaming from Kafka into bronze/silver Delta tables with checkpointing.', 'ph-flow-arrow'],
            ];
            el.innerHTML = card(`
                <h2 class="text-sm font-bold text-slate-900 mb-3"><i class="ph-bold ph-flow-arrow text-cyan-600 mr-1"></i>Runtime data flow</h2>
                <div class="mermaid text-xs bg-slate-50 p-4 rounded-lg border border-slate-100 overflow-x-auto">
flowchart LR
    P["Producers"] --> K["Embedded Kafka<br/>topic: streaming_test_topic"]
    K --> S["Spark Structured Streaming"]
    S --> B["Bronze Delta"]
    B --> SV["Silver Delta"]
    SV --> T["Tests / Labs"]
                </div>`) + `
                <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                    ${comps.map(([name, path, desc, icon]) => `
                    <article class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm hover:border-cyan-400 transition flex flex-col">
                        <div class="w-10 h-10 rounded-lg bg-cyan-50 text-cyan-700 flex items-center justify-center text-xl"><i class="ph-bold ${icon}"></i></div>
                        <h3 class="text-sm font-bold text-slate-900 mt-3">${esc(name)}</h3>
                        <p class="text-xs text-slate-600 mt-1 flex-1">${esc(desc)}</p>
                        <div class="mt-3">${codeBtn(path, path.split('/').pop())}</div>
                    </article>`).join('')}
                </div>` + card(`
                    <h3 class="text-sm font-bold text-slate-900 mb-2">Configuration (.env)</h3>
                    <pre class="text-[11px]">KAFKA_BROKER_PORT=9092\nSPARK_MASTER=local[2]\nSPARK_SQL_SHUFFLE_PARTITIONS=2</pre>
                    <p class="text-xs text-slate-600 mt-2">Exercise the runtime with <code class="bg-slate-100 px-1 rounded">python3 -m unittest test_suites/test_13_bigdata_runtime_instances.py</code>.</p>`);
            runMermaid(el);
        },
    };

    // =========================================================================
    // SOURCE VIEWER MODAL
    // =========================================================================
    function ensureModal() {
        let m = document.getElementById('nav-source-modal');
        if (m) return m;
        m = document.createElement('div');
        m.id = 'nav-source-modal';
        m.className = 'fixed inset-0 z-50 hidden bg-slate-950/70 flex items-center justify-center p-4';
        m.innerHTML = `
            <div class="bg-white text-slate-900 rounded-xl shadow-2xl w-full max-w-5xl max-h-[88vh] flex flex-col">
                <div class="flex items-center justify-between px-5 py-3 border-b border-slate-200">
                    <div class="flex items-center gap-2 min-w-0">
                        <button id="nav-source-back" type="button" class="hidden p-1 rounded hover:bg-slate-100" title="Back to folder"><i class="ph-bold ph-arrow-left"></i></button>
                        <i class="ph-bold ph-code text-blue-600"></i><span id="nav-source-title" class="font-mono text-xs font-bold truncate"></span>
                    </div>
                    <button type="button" onclick="NavRouter.closeSource()" class="p-1.5 rounded hover:bg-slate-100" title="Close"><i class="ph-bold ph-x"></i></button>
                </div>
                <div id="nav-source-body" class="overflow-auto p-4 text-xs"></div>
            </div>`;
        m.addEventListener('click', (e) => { if (e.target === m) closeSource(); });
        document.addEventListener('keydown', (e) => { if (e.key === 'Escape') closeSource(); });
        document.body.appendChild(m);
        return m;
    }

    async function openSource(path, fromFolder) {
        const m = ensureModal();
        const title = m.querySelector('#nav-source-title');
        const body = m.querySelector('#nav-source-body');
        const back = m.querySelector('#nav-source-back');
        m.classList.remove('hidden');
        title.textContent = path;
        body.innerHTML = loading;
        back.classList.toggle('hidden', !fromFolder);
        back.onclick = () => openSource(fromFolder);
        const isFile = /\.[a-z0-9]+$/i.test(path);
        try {
            if (isFile) {
                const d = await getJSON('/api/v1/source/file?path=' + encodeURIComponent(path));
                body.innerHTML = `<pre class="text-[11px] leading-relaxed whitespace-pre">${esc(d.content)}</pre>`;
            } else {
                const d = await getJSON('/api/v1/source/tree?root=' + encodeURIComponent(path));
                body.innerHTML = `<div class="text-[11px] text-slate-500 mb-2">${d.total} viewable files</div>` +
                    d.files.map((f) => `<button type="button" data-p="${esc(f.path)}" class="nav-src-file w-full text-left font-mono text-[11px] px-2 py-1 rounded hover:bg-slate-100 flex justify-between"><span>${esc(f.path)}</span><span class="text-slate-400">${(f.size_bytes / 1024).toFixed(1)} KB</span></button>`).join('');
                body.querySelectorAll('.nav-src-file').forEach((b) => { b.onclick = () => openSource(b.dataset.p, path); });
            }
        } catch (e) { body.innerHTML = errorBox('Unable to open: ' + e.message); }
    }

    function closeSource() {
        const m = document.getElementById('nav-source-modal');
        if (m) m.classList.add('hidden');
    }

    function toggleOverview(btn) {
        const body = btn.closest('[data-nav-overview]').querySelector('[data-nav-overview-body]');
        const hidden = body.classList.toggle('hidden');
        btn.textContent = hidden ? 'Show overview details' : 'Hide overview details';
    }

    // =========================================================================
    // WIRE-UP: override legacy entry points so every link routes via menus
    // =========================================================================
    window.loadView = function (key) {
        if (!booted) { booted = true; render(currentKey()); return; }   // first call comes from initPortal()
        go(INDEX[key] ? key : 'project-overview');
    };
    window.loadLabsModule = (modId) => go('lab-' + modId);
    window.onMenuClick = (menuId, key) => go(key || menuId + '-page');
    window.toggleMenu = toggle;

    window.NavRouter = { NAV, INDEX, go, toggle, openSource, closeSource, toggleOverview };

    renderSidebar();
})();
