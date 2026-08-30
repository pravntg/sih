"""
Health & Liveness Check Endpoints
"""
from fastapi import APIRouter
from datetime import datetime, timezone
from ...config import settings

router = APIRouter(tags=["system"])

@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "Project ORCA Marine Backend",
        "environment": settings.ENVIRONMENT,
        "safe_mode": settings.FLAG_SAFE_MODE,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
