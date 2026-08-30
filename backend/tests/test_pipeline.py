"""
Tests for Satellite Ingest Pipeline
"""
import pytest
from src.pipeline.satellite_ingest import satellite_pipeline

def test_ingest_sentinel_sst_success():
    res = satellite_pipeline.ingest_sentinel_sst_tile({
        "file_id": "S3A_SL_2_WST_2026.nc",
        "cloud_cover_pct": 5.0
    })
    assert res["status"] == "success"
    assert res["dataset_id"] == "dataset:sentinel3_sst"
    assert res["gradient_max"] > 0

def test_ingest_sentinel_sst_cloud_degraded():
    res = satellite_pipeline.ingest_sentinel_sst_tile({
        "file_id": "S3A_SL_2_WST_CLOUDY.nc",
        "cloud_cover_pct": 65.0
    })
    assert res["status"] == "degraded"
    assert res["reason"] == "cloud_occlusion"

def test_ingest_modis_chlorophyll():
    res = satellite_pipeline.ingest_modis_chlorophyll({
        "file_id": "AQUA_MODIS_CHL_2026.nc"
    })
    assert res["status"] == "success"
    assert res["dataset_id"] == "dataset:modis_chl"
    assert res["bloom_fronts"] >= 1
