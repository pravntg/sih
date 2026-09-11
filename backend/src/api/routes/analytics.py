"""
Analytics, PFZ & Thermal Wind Vector API Endpoints
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from ...models.pfz import PfzRequest, PfzGeoJsonResponse, WindVectorResponse
from ...services.pfz_service import pfz_service
from ...config import settings

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.post("/pfz", response_model=PfzGeoJsonResponse)
async def compute_potential_fishing_zones(request: PfzRequest) -> PfzGeoJsonResponse:
    """
    Compute Potential Fishing Zone (PFZ) GeoJSON polygons based on satellite SST and Chlorophyll-a boundaries.
    """
    if not settings.FLAG_PFZ_LIVE_RECOMPUTATION and settings.FLAG_SAFE_MODE:
        raise HTTPException(
            status_code=503,
            detail="Live PFZ recomputation is disabled in safe mode; relying on cached regional advisories."
        )
    
    try:
        result = pfz_service.compute_pfz(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to compute PFZ analytics: {str(e)}")

@router.post("/wind-vectors", response_model=WindVectorResponse)
async def get_wind_vectors(request: PfzRequest) -> WindVectorResponse:
    """
    Calculate gridded U/V atmospheric vector streamlines using scientific oceanographic colormaps.
    """
    try:
        result = pfz_service.compute_wind_vectors(bbox=request.bbox)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to compute wind vector grid: {str(e)}")
