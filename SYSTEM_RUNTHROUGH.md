# Project ORCA — End-to-End System Run-Through & Architecture Guide

Welcome to the comprehensive system walkthrough for **Project ORCA (Agentic Marine Intelligence Platform — AMIP)**. This document details every component, directory, data flow, API contract, and operational rule implemented across the platform.

---

## 1. System Overview & Problem Statement

Project ORCA provides an end-to-end operational intelligence platform for coastal fishers, vessel masters, and maritime authorities. It ingests multi-source earth observation satellite feeds and ocean forecasts to provide:
1. **Potential Fishing Zone (PFZ) Analytics**: Automated detection of thermal gradients and chlorophyll-a fronts indicating high-pelagic fish concentration zones.
2. **Conversational Marine Advisory Assistant**: Evidence-first reasoning engine providing vessel-specific voyage clearances, wave/wind threshold evaluations, and safety guidance.
3. **Strict Provenance & Zero-Hallucination Governance**: Every recommendation is bound to verifiable observational datasets (Sentinel-3 SST, MODIS Chl, INCOIS OSF) with traceable timestamps and confidence scores.
4. **Stitch MCP UI/UX Integration**: High-density utilitarian interface following strict non-negotiable palette constraints (`#0D2B45`, `#5A7D9A`, `#8DBFB7`, `#DCC7AA`, `#F4F6F6`, `#0B1220`, white inverse, solid fills, 0 gradients, max 8px border-radius).

---

## 2. Directory Layout & "What is Where"

```text
SIH26/
├── backend/                        # Python FastAPI Backend & Analytics Services
│   ├── api/
│   │   └── openapi.yml             # OpenAPI 3.0 specification for all endpoints
│   ├── scripts/
│   │   └── start-local.sh          # Local backend bootstrap script
│   ├── src/
│   │   ├── api/routes/
│   │   │   ├── analytics.py        # POST /v1/analytics/pfz endpoint
│   │   │   ├── chat.py             # POST /v1/chat marine advisory endpoint
│   │   │   └── health.py           # GET /health system liveness check
│   │   ├── db/
│   │   │   └── schema.sql          # PostGIS + Timescale spatial database schema
│   │   ├── models/
│   │   │   ├── chat.py             # ChatRequest, ChatResponse, SafetyStatus, VesselProfile
│   │   │   ├── pfz.py              # PfzRequest, PfzGeoJsonResponse, GeoJSON Feature models
│   │   │   └── provenance.py       # ProvenanceRecord, EvidenceItem, AgentChainStep
│   │   ├── pipeline/
│   │   │   └── satellite_ingest.py # Sentinel-3 SST & MODIS Chlorophyll raster ingest
│   │   ├── services/
│   │   │   ├── marine_chat_service.py # Reasoning & safety evaluator service
│   │   │   ├── pfz_service.py      # PFZ thermal/chlorophyll front compute engine
│   │   │   └── provenance_service.py  # Evidence validation & anti-hallucination auditor
│   │   ├── config.py               # Pydantic V2 settings & threshold configurations
│   │   └── main.py                 # FastAPI application entrypoint with CORS
│   ├── tests/                      # 13 Test suites (95% overall code coverage)
│   │   ├── test_api.py             # Integration test for /health, /chat, /analytics/pfz
│   │   ├── test_chat_service.py    # Vessel safety thresholds & ambiguity tests
│   │   ├── test_pfz_service.py     # Polygon closure & gradient computation tests
│   │   ├── test_pipeline.py        # Ingest pipeline & cloud-mask fallback tests
│   │   ├── test_provenance.py      # Provenance validation & evidence check tests
│   │   └── run_unittests.py        # Standalone runner without third-party dependencies
│   ├── Dockerfile                  # Container definition with GDAL & geospatial tools
│   ├── docker-compose.yml          # PostgreSQL+PostGIS, Redis, and MinIO S3 services
│   └── requirements.txt            # Python dependencies
│
├── frontend/                       # Client Web Application (Stitch Design Integrated)
│   ├── design/
│   │   └── manifest.json           # Local pointer to Stitch design assets
│   ├── public/                     # Public assets
│   ├── scripts/
│   │   └── verify-palette.js       # Automated design & 5-color palette scanner
│   ├── src/
│   │   └── app.js                  # Leaflet map logic, live chat, & provenance modal
│   ├── styles/
│   │   ├── main.css                # Stitch Marine Intelligence System stylesheet
│   │   └── variables.css           # CSS custom properties mapped to palette
│   ├── index.html                  # Interactive dashboard client
│   ├── package.json                # Frontend package definition
│   └── stitch-design-hook.md       # Pre-build Stitch verification hook
│
├── infra/                          # Infrastructure as Code & Feature Flags
│   ├── helm/                       # Helm chart manifests (Chart.yaml, values.yaml)
│   ├── k8s/                        # Kubernetes Deployment manifests
│   ├── terraform/                  # Cloud infrastructure skeleton (RDS PostGIS & S3)
│   ├── feature_flags.yml           # Safe-mode toggles and canary percentages
│   └── README.md
│
├── ops/                            # Operational Governance & Dev Loop Monitor
│   ├── cycle-monitor/
│   │   ├── monitor.py              # 120-minute cycle monitor with Stitch alerting
│   │   └── stitch_handler.py       # Automated Manager review heuristics & PR gating
│   └── runbook.md                  # SRE emergency incident & rollback playbooks
│
├── docs/                           # Authoritative Documentation (Canonical Source)
│   ├── ui/
│   │   ├── manifest.json           # Active Stitch MCP project & screen links
│   │   ├── palette.json            # Exact 5-color hex specifications
│   │   └── tokens.json             # Typography, spacing, and border-radius tokens
│   ├── agents.md                   # Agent behavioral policies & 2-hour dev loop
│   ├── datasets_catalog.md         # Sentinel, MODIS, GEBCO, INCOIS metadata
│   ├── project_initialisation_prompt.md # Bootstrap prompt & Stitch topic schemas
│   ├── provenance_guidelines.md    # Evidence schemas & UI card requirements
│   ├── rollout_and_rollback.md     # 5% canary & automated rollback triggers
│   └── README.md                   # Canonical docs index
│
├── .github/workflows/
│   └── ci.yml                      # CI pipeline (Palette check, Pytest coverage, SCA)
├── scripts/
│   ├── bootstrap.sh                # Initial directory smoke checks
│   └── run_all_tests.py            # End-to-end automated test runner
├── CONTRIBUTING.md                 # Commit provenance & branch conventions
├── PULL_REQUEST_TEMPLATE.md        # PR template with provenance & risk rating
├── pytest.ini                      # Pytest discovery settings
└── README.md                       # Comprehensive project landing guide
```

---

## 3. Stitch MCP Design System Integration

The front-end design was created and validated directly using the **Stitch MCP Server**:
- **Stitch Project ID**: `15311932679871051742`
- **Design System Name**: `Marine Intelligence System` (`assets/fd814b84a29740d39d043b0fa90c508e`)
- **Stitch Screen ID**: `21a4ddc3cb4f4ded8fdc42cbcdf85355`
- **Topic Namespace**: `orca.ui.designs`

### Visual Hierarchy & Tonal Layering
- **Level 0 (Base)**: `#F4F6F6` (Salt Air) representing clean surface background.
- **Level 1 (Panels/Cards)**: `#FFFFFF` (Pure White) data panels framed with a 1px solid border of `#DCC7AA` (Sandy Shore).
- **Level 2 (Navigation)**: `#0D2B45` (Deep Sea) global header providing the structural anchor.
- **Actions**: Solid `#5A7D9A` (Ocean Mist) with 4px corner radius.
- **Safe & PFZ Overlays**: `#8DBFB7` (Seafoam) solid alpha polygons with crisp `#0D2B45` borders.
- **Typography**: Inter sans-serif with `data-mono` tracking for GPS coordinates, wave heights, and SST gradients.

---

## 4. Key Features & How They Work

### Feature 1: Potential Fishing Zone (PFZ) Analytics Engine
- **Endpoint**: `POST /v1/analytics/pfz`
- **Methodology**: Ingests Sentinel-3 SLSTR Level 2 Sea Surface Temperature (SST) rasters and MODIS Aqua Chlorophyll-a concentration layers. It computes spatial gradient contours (>= 0.5 °C/km) co-located with phytoplankton blooms (>= 0.3 mg/m³).
- **Output**: Standard GeoJSON `FeatureCollection` with bounded depth profiles, target pelagic species (Yellowfin Tuna, Mackerel, Sardines), validity windows (24h), and attached provenance.

### Feature 2: Conversational Marine Advisory AI
- **Endpoint**: `POST /v1/chat`
- **Methodology**: Evaluates real-time weather and wave forecast telemetry against vessel risk profiles (`motorized_skiff`, `trawler`, `artisanal_catamaran`, `deep_sea_liner`).
- **Safety Categorization**:
  - `SAFE TO SAIL` (Green / Seafoam badge)
  - `CAUTION ADVISED` (Ocean Mist badge)
  - `DANGER — HIGH RISK` (Deep Sea badge with explicit delay instructions)
  - `CLARIFICATION NEEDED` (Triggers 1 concise clarifying question if coordinates are omitted).

### Feature 3: Immutable Provenance Inspector
- Every response from the backend contains an immutable `provenance` block declaring:
  - `task_id` and `trace_id`
  - Exact `dataset_id` (e.g. `dataset:sentinel3_sst`, `dataset:incois_osf`)
  - File acquisition timestamps and calculated metric scalars
  - Model and algorithm versioning (e.g. `pfz_v0.4`, `marine_chat_v1.0`)
  - Confidence scalar in range `[0.0, 1.0]`.

---

## 5. Running the Complete System Locally

### Step 1: Start Backend API
```bash
py -m uvicorn src.main:app --app-dir backend --port 8000 --reload
```
API Documentation: **[http://localhost:8000/docs](http://localhost:8000/docs)**

### Step 2: Start Frontend Dashboard
```bash
py -m http.server 5173 --directory frontend
```
Client Dashboard: **[http://localhost:5173](http://localhost:5173)**

### Step 3: Run All Verification Suites
```bash
py scripts/run_all_tests.py
```
This runs palette validation, 13 backend unit tests, 120-minute dev-loop monitor, and contract checks in under 3 seconds.
