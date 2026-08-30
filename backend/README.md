# Project ORCA — Backend Services

This directory contains the microservices, data ingest pipelines, geospatial analytics (PFZ), and agent reasoning engine for Project ORCA.

---

## Architecture & Responsibilities

- **PFZ Microservice**: Consumes SST (Sentinel-3) and Chlorophyll (MODIS/OLCI) to compute Potential Fishing Zone polygons and thermal fronts.
- **Chat & Agent Service**: Conversational reasoning engine integrating multi-turn marine advice, safety threshold checks, and provenance verification.
- **Telemetry & GeoDB**: PostgreSQL with PostGIS extension and TimescaleDB for spatial and time-series telemetry.

---

## Local Development & Setup

### 1. Prerequisites
- Docker & Docker Compose
- Python 3.11+
- GDAL / PROJ (for geospatial processing)

### 2. Running Locally with Docker Compose
```bash
cd backend
docker-compose up -d
```

### 3. Running Services Directly
```bash
./scripts/start-local.sh
```

### 4. Running Tests
```bash
pytest tests/ -v --cov=src --cov-report=term-missing
```
*(Target: >= 70% coverage for general modules, >= 80% for risk-critical analytics)*
