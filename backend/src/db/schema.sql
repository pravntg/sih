-- Project ORCA — Database Schema (PostgreSQL + PostGIS + TimescaleDB)

-- Enable PostGIS Extension
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. Ocean Observations (SST Grids & Metadata)
CREATE TABLE IF NOT EXISTS ocean_observations_sst (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    dataset_id VARCHAR(64) NOT NULL DEFAULT 'dataset:sentinel3_sst',
    file_id VARCHAR(255) NOT NULL,
    acquisition_time TIMESTAMPTZ NOT NULL,
    bounding_box GEOMETRY(Polygon, 4326),
    sst_raster_uri VARCHAR(512),
    mean_temp_c NUMERIC(5, 2),
    gradient_max NUMERIC(5, 2),
    cloud_mask_pct NUMERIC(5, 2),
    freshness_status VARCHAR(32) DEFAULT 'fresh',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Ocean Observations (Chlorophyll Grids & Boundaries)
CREATE TABLE IF NOT EXISTS ocean_observations_chl (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    dataset_id VARCHAR(64) NOT NULL DEFAULT 'dataset:modis_chl',
    file_id VARCHAR(255) NOT NULL,
    acquisition_time TIMESTAMPTZ NOT NULL,
    bounding_box GEOMETRY(Polygon, 4326),
    chl_raster_uri VARCHAR(512),
    chl_mean_mg_m3 NUMERIC(5, 3),
    front_count INT DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. Potential Fishing Zone (PFZ) Polygons & Advisories
CREATE TABLE IF NOT EXISTS pfz_advisories (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    zone_code VARCHAR(32) NOT NULL UNIQUE,
    polygon_geom GEOMETRY(Polygon, 4326) NOT NULL,
    sst_mean_deg_c NUMERIC(4, 2),
    sst_gradient NUMERIC(4, 2),
    chl_mean_mg_m3 NUMERIC(4, 2),
    depth_min_m NUMERIC(6, 1),
    depth_max_m NUMERIC(6, 1),
    target_species TEXT[],
    confidence_score NUMERIC(3, 2) NOT NULL,
    valid_from TIMESTAMPTZ NOT NULL,
    valid_until TIMESTAMPTZ NOT NULL,
    provenance_snapshot JSONB NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Spatial Indexes
CREATE INDEX IF NOT EXISTS idx_pfz_advisories_geom ON pfz_advisories USING GIST (polygon_geom);
CREATE INDEX IF NOT EXISTS idx_sst_bbox ON ocean_observations_sst USING GIST (bounding_box);
CREATE INDEX IF NOT EXISTS idx_chl_bbox ON ocean_observations_chl USING GIST (bounding_box);

-- 4. Immutable Provenance Store & Audit Trail
CREATE TABLE IF NOT EXISTS provenance_store (
    recommendation_id VARCHAR(64) PRIMARY KEY,
    task_id VARCHAR(64) NOT NULL,
    trace_id VARCHAR(64) NOT NULL,
    user_id VARCHAR(64),
    confidence_score NUMERIC(3, 2) NOT NULL,
    evidence_payload JSONB NOT NULL,
    agent_chain_payload JSONB NOT NULL,
    explanation TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_provenance_task ON provenance_store (task_id);
CREATE INDEX IF NOT EXISTS idx_provenance_trace ON provenance_store (trace_id);
