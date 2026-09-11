"""
API Integration Tests using FastAPI TestClient
"""
import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "Project ORCA" in data["service"]

def test_api_chat_flow():
    payload = {
        "user_id": "test_user_api",
        "message": "Check marine weather for fishing",
        "coordinates": [8.5, 78.2],
        "vessel_profile": {
            "type": "trawler",
            "max_safe_wind_kmh": 40.0,
            "max_safe_wave_m": 2.5
        }
    }
    response = client.post("/v1/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "reply" in data
    assert "provenance" in data
    assert data["provenance"]["confidence"] >= 0.65

def test_api_pfz_analytics_flow():
    payload = {
        "bbox": [78.0, 8.0, 79.5, 9.5],
        "target_date": "2026-08-30",
        "min_chlorophyll_threshold": 0.3
    }
    response = client.post("/v1/analytics/pfz", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == "FeatureCollection"
    assert len(data["features"]) > 0
    assert "provenance" in data

def test_api_wind_vectors_flow():
    payload = {
        "bbox": [78.0, 8.0, 79.5, 9.5],
        "target_date": "2026-08-30"
    }
    response = client.post("/v1/analytics/wind-vectors", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "vectors" in data
    assert len(data["vectors"]) > 0
    assert "scientific_color" in data["vectors"][0]
    assert data["provenance"]["confidence"] >= 0.8
