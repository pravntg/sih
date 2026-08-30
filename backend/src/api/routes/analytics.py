"""
Analytics & PFZ API Endpoints
"""
from fastapi import APIRouter, HTTPException, Depends
from ...models.pfz import PfzRequest, PfzGeoJsonResponse
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
