"""
Potential Fishing Zone (PFZ) Data Models & GeoJSON Schema
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import date
from .provenance import ProvenanceRecord

class PfzRequest(BaseModel):
    bbox: List[float] = Field(..., min_length=4, max_length=4, description="[min_lon, min_lat, max_lon, max_lat]")
    target_date: Optional[date] = Field(default_factory=date.today)
    min_chlorophyll_threshold: float = Field(0.3, description="Chlorophyll-a front threshold in mg/m^3")
    sst_gradient_threshold: float = Field(0.5, description="SST thermal gradient threshold in degC/km")
    vessel_range_km: Optional[float] = Field(50.0, description="Operational search radius from base")

class PfzPolygonProperties(BaseModel):
    zone_id: str
    sst_mean_deg_c: float
    sst_gradient_deg_c_per_km: float
    chl_mean_mg_m3: float
    depth_range_meters: List[float]
    recommended_target_species: List[str]
    confidence_score: float
    validity_window_hours: int = 24
    safety_rating: str = "safe"

class GeoJsonGeometry(BaseModel):
    type: str = "Polygon"
    coordinates: List[List[List[float]]]

class PfzFeature(BaseModel):
    type: str = "Feature"
    geometry: GeoJsonGeometry
    properties: PfzPolygonProperties

class PfzGeoJsonResponse(BaseModel):
    type: str = "FeatureCollection"
    features: List[PfzFeature]
    provenance: ProvenanceRecord
    metadata: Dict[str, Any] = Field(default_factory=dict)
