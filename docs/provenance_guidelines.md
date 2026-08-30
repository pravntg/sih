# Provenance Guidelines & Metadata Standards

Project ORCA adheres to strict provenance standards. No claim, insight, recommendation, or model artifact may exist without a traceable provenance chain.

---

## 1. Code & Infrastructure Level Provenance

Every commit and pull request modifying algorithms, data processing logic, prompts, or model configurations must include provenance metadata in the commit trailer:

```text
provenance:{task_id:"<task-id>", datasets_used:["<dataset-id-1>", "<dataset-id-2>"], model_versions:["<model-version>"]}
```

### Commit Examples
```text
feat(pfz): integrate SST gradient contour calculation

Implement contour gradient detection over Sentinel-3 L2 data.

provenance:{task_id:"task-pfz-01", datasets_used:["dataset:sentinel3_sst"], model_versions:["pfz_v0.4"]}
```

---

## 2. Recommendation & API Output Provenance

Every recommendation served via API or agent response must return an immutable machine-readable provenance block:

```json
{
  "recommendation_id": "rec-e389d-47a1",
  "task_id": "task-uuid-001",
  "trace_id": "trace-uuid-001",
  "created_at": "2026-08-30T10:00:00Z",
  "user_context": {
    "user_id": "user-882",
    "coordinates": [9.761, 78.123],
    "vessel_profile": {
      "type": "motorized_skiff",
      "max_safe_wind_kmh": 30
    }
  },
  "agent_chain": [
    {
      "agent": "planner",
      "version": "v1.0"
    },
    {
      "agent": "pfz_agent",
      "version": "v0.4",
      "model_version": "pfz_gradient_model_v0.4",
      "confidence_score": 0.82
    }
  ],
  "evidence": [
    {
      "dataset_id": "dataset:sentinel3_sst",
      "file_id": "S3A_SL_2_WST____20260830T041200.nc",
      "acquisition_timestamp": "2026-08-30T04:12:00Z",
      "metric": "sst_gradient",
      "value": 1.4,
      "units": "degC/km"
    },
    {
      "dataset_id": "dataset:modis_chl",
      "file_id": "AQUA_MODIS.20260830T060000.L2.OC.nc",
      "acquisition_timestamp": "2026-08-30T06:00:00Z",
      "metric": "chl_a_concentration",
      "value": 0.48,
      "units": "mg/m^3"
    }
  ],
  "confidence": 0.82,
  "explanation": "PFZ identified along sharp SST thermal boundary with co-occurring chlorophyll front."
}
```

---

## 3. UI Display Requirements

The frontend must provide:
1. A summary card showing the primary dataset source, timestamp of acquisition, and confidence rating.
2. A "View Full Provenance" modal/drawer containing the complete structured evidence list and model version.
