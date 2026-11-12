# Project Architecture & Modernization Standards

## Default Frontend Layout Specification
**Standard:** Modern responsive layout featuring a **Left Panel Navigation Bar** with **expandable / collapsible menus and sub-menus**, sticky top header, breadcrumb path, and fluid content area.

### Layout Blueprint:
```
+-----------------------------------------------------------------------------------------+
| Top Header: Brand | Global Search | Health Check | System Status Indicator              |
+-------------------+---------------------------------------------------------------------+
| Left Sidebar      | Main Workspace / Content Area                                       |
| [Toggle Button]   |                                                                     |
|                   | Breadcrumb: Home > Category > Active View                           |
| ▶ Menu Group 1    |                                                                     |
|   ├─ Sub-menu 1.1 | [ Active Dashboard / Cockpit / Visualizer / Table View ]            |
|   ├─ Sub-menu 1.2 |                                                                     |
|   └─ Sub-menu 1.3 |                                                                     |
|                   |                                                                     |
| ▶ Menu Group 2    |                                                                     |
|   ├─ Sub-menu 2.1 |                                                                     |
|   └─ Sub-menu 2.2 |                                                                     |
|                   |                                                                     |
| ▶ Menu Group 3    |                                                                     |
|   ├─ Sub-menu 3.1 |                                                                     |
|   └─ Sub-menu 3.2 |                                                                     |
|                   |                                                                     |
| [Collapse/Expand] |                                                                     |
+-------------------+---------------------------------------------------------------------+
| Footer: Enterprise Metadata | Runtime Port (11991) | Security Status                    |
+-----------------------------------------------------------------------------------------+
```

### Core UI/UX Requirements:
1. **Left Navigation Panel**:
   - Fixed/sticky left panel with collapsible/expandable navigation hierarchy.
   - Primary Menu Categories with chevron toggles for accordion expansion.
   - Nested sub-menus for deep feature navigation.
   - Global toggle button to minimize sidebar into an icon-only rail or expand to full width.
2. **Interactive States**:
   - Highlight active route/tab and active sub-menu item with clear accent colors.
   - Persist menu open/close states in `localStorage` across page refreshes.
3. **Workspace Content Area**:
   - Fluid responsive canvas adjusting dynamically as sidebar expands/collapses.
   - Contextual breadcrumbs indicating the active section and sub-feature.

---

## Project Tracks & Deliverables Overview

### 1. `/Palantir`
- `Palantir_Implementation_Guide.docx` (Foundry, AIP, Apollo, Gotham)
- PySpark Code Repositories (`customer_supply_chain_transforms.py`)
- Ontology Digital Twin (`enterprise_ontology_spec.json`, `action_functions.ts`)
- AIP Agent Studio (`supply_chain_agent_spec.json`)
- Workshop Cockpit Specifications (`supply_chain_workshop_spec.json`)
- Apollo Fleet Manifest (`apollo_deployment_manifest.yaml`)

### 2. `/Databricks`
- `Databricks_Implementation_Guide.docx` (Lakehouse, Unity Catalog, Photon, Mosaic AI)
- Unity Catalog DDL with ABAC & dynamic masking (`unity_catalog_ddl.sql`)
- Delta Live Tables (DLT) streaming pipeline (`supply_chain_dlt_pipeline.py`)
- Lakeflow Multi-task DAG Orchestration (`supply_chain_orchestration.json`)
- Mosaic AI Agent with Vector Search (`supply_chain_mosaic_agent.py`)
- Databricks Apps interactive cockpit (`app.py`, `app.yaml`)
- Databricks Asset Bundles (`databricks.yml`)

### 3. `/Comparisons`
- `Palantir_vs_Databricks_Comparison_Matrix.docx` (10 architectural vectors & decision framework)
- Scored capability matrix (`detailed_capability_matrix.json`)
- Benchmark and 3-Year TCO simulator (`benchmark_and_tco_simulator.py`, `benchmark_and_tco_report.json`)

### 4. `/Migrations`
- `Palantir_to_Databricks_Migration_Guide.docx` (Technical playbook)
- `Palantir to Databricks Migration Consultant.docx` (Enterprise advisory playbook)
- `Palantir to Databricks Migration Consultant technical Interview Preparation Guide.docx` (Interview mastery)
- `Palantir to Databricks 200 Hands-On Labs Step by Steps Instructions.docx` (Comprehensive 200 labs curriculum)
- Automated Code Converters (`foundry_to_dlt_converter.py`, `ontology_to_unity_catalog_converter.py`)
- Automated Reconciliation & Parity Suite (`reconciliation_engine.py`)
- End-to-End Migration Cutover Script (`execute_migration_cutover.py`)

---

## 5. Enterprise Frontend Portal (Port 11991)
- **Framework**: FastAPI + Tailwind CSS + Phosphor Icons + Chart.js
- **Default Navigation Layout**: Collapsible Left Sidebar with expandable sub-menus, persistent active states, and fluid content area.
- **Port**: `11991` (`http://localhost:11991`)
