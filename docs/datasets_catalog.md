# Datasets Catalog

This catalog is the canonical source of observational, environmental, and spatial datasets accessible to Project ORCA agents and pipelines.

---

## 1. Governance & Licensing Rules

- **License Verification**: Every dataset has strict redistribution flags (`redistributable: true | false`).
- **Non-Redistributable Feeds**: For datasets marked `redistributable: false`, agents and APIs must only output derived metrics (e.g. spatial averages, gradients, anomaly bounds). Raw raster or binary file URLs MUST NOT be shared directly with users.
- **Freshness SLA**: Queries requiring operational advisory validation must verify that data freshness is within acceptable operational thresholds.

---

## 2. Core Datasets

### 2.1 Sentinel-3 SLSTR (Sea Surface Temperature)
- **ID**: `dataset:sentinel3_sst`
- **Product**: SST (Level 2 / Level 3 gridded)
- **Provider**: ESA / Copernicus
- **Spatial Resolution**: 1 km
- **Temporal Resolution**: Daily
- **Freshness SLA**: <= 12 hours
- **Redistributable**: `true` (Open Access with attribution)
- **Usage**: Primary input for Sea Surface Temperature gradient detection in Potential Fishing Zones (PFZ).

### 2.2 MODIS Aqua / Sentinel-3 OLCI (Chlorophyll-a)
- **ID**: `dataset:modis_chl` / `dataset:sentinel3_chl`
- **Product**: Chlorophyll-a concentration (mg/m³)
- **Provider**: NASA OceanColor / ESA Copernicus
- **Spatial Resolution**: 1 km / 300 m
- **Temporal Resolution**: Daily
- **Freshness SLA**: <= 24 hours
- **Redistributable**: `true`
- **Usage**: Primary input for phytoplankton bloom boundary and marine frontal zone detection.

### 2.3 GEBCO / NOAA Bathymetry
- **ID**: `dataset:gebco_bathymetry`
- **Product**: Global ocean bathymetry grid
- **Provider**: GEBCO
- **Spatial Resolution**: 15 arc-seconds
- **Freshness SLA**: Static / Annual
- **Redistributable**: `true`
- **Usage**: Depth masking, shallow water navigation safety checks, seabed contour alignment.

### 2.4 ECMWF / INCOIS Ocean State Forecasts
- **ID**: `dataset:incois_osf`
- **Product**: Significant Wave Height (SWH), Wave Direction, Ocean Currents, Wind Speed
- **Provider**: INCOIS / ECMWF
- **Temporal Resolution**: 3-hourly forecast (up to 72 hours)
- **Freshness SLA**: <= 6 hours
- **Redistributable**: `true`
- **Usage**: Voyage safety assessment, high-wave advisories, rough sea warnings.

---

## 3. Fallback Priority Matrix

When a primary feed is unavailable due to sensor delay or cloud occlusion:
1. `dataset:sentinel3_sst` → Fallback to `dataset:mur_sst` (Multi-scale Ultra-high Resolution SST blended).
2. `dataset:modis_chl` → Fallback to 8-day rolling composite or regional climatology baseline (annotate with `low_confidence`).
3. In all fallback cases, agent outputs must state `partial: true` with the fallback reason in the provenance record.
