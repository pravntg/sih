"""
Unit & Integration Tests for Potential Fishing Zone (PFZ) Analytics Engine
"""
import pytest
from datetime import date
from src.models.pfz import PfzRequest
from src.services.pfz_service import pfz_service

def test_compute_pfz_valid_bounding_box():
    request = PfzRequest(
        bbox=[78.5, 8.5, 79.8, 9.8],
        target_date=date.today(),
        min_chlorophyll_threshold=0.3,
        sst_gradient_threshold=0.5
    )
    response = pfz_service.compute_pfz(request, task_id="test-task-pfz-01")
    
    assert response.type == "FeatureCollection"
    assert len(response.features) >= 1
    
    first_feature = response.features[0]
    assert first_feature.geometry.type == "Polygon"
    assert len(first_feature.geometry.coordinates[0]) >= 4
    assert first_feature.properties.sst_gradient_deg_c_per_km >= 0.5
    assert first_feature.properties.confidence_score >= 0.70
    
    # Provenance Validation
    assert response.provenance is not None
    assert len(response.provenance.evidence) >= 2
    assert response.provenance.confidence >= 0.65
    assert "Sentinel-3" in response.provenance.evidence[0].note or "Sentinel" in response.provenance.evidence[0].note

def test_compute_pfz_polygon_closure():
    """Verify that GeoJSON polygon rings are closed (first coord == last coord)"""
    request = PfzRequest(bbox=[75.0, 10.0, 76.0, 11.0])
    response = pfz_service.compute_pfz(request)
    
    for feature in response.features:
        ring = feature.geometry.coordinates[0]
        assert ring[0] == ring[-1], "Polygon linear ring must be closed"
