"""
Conversational Marine Advisory Data Models
"""
from typing import List, Optional, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field
from .provenance import ProvenanceRecord

class SafetyStatus(str, Enum):
    SAFE = "safe"
    CAUTIOUS = "cautious"
    DANGER = "danger"
    LOW_CONFIDENCE = "low_confidence"
    CLARIFICATION_NEEDED = "clarification_needed"

class VesselProfile(BaseModel):
    type: str = Field("motorized_skiff", description="Vessel category (skiff, trawler, catamaran, artisanal)")
    max_safe_wind_kmh: float = Field(25.0, description="Max safe wind speed threshold in km/h")
    max_safe_wave_m: float = Field(1.5, description="Max safe wave height in meters")
    engine_hp: Optional[int] = Field(None, description="Engine horsepower")

class ChatRequest(BaseModel):
    user_id: str = Field(..., description="User identifier")
    session_id: Optional[str] = Field(None, description="Session tracking ID")
    message: str = Field(..., description="User advisory or operational query")
    coordinates: Optional[List[float]] = Field(None, min_length=2, max_length=2, description="[latitude, longitude]")
    vessel_profile: Optional[VesselProfile] = Field(default_factory=VesselProfile)
    language: str = Field("en", description="ISO 639-1 language code (e.g. en, ta, ml, te, hi)")

class ChatResponse(BaseModel):
    reply: str = Field(..., description="Conversational advisory reply")
    safety_status: SafetyStatus = Field(..., description="Categorized safety rating")
    confidence: float = Field(..., ge=0.0, le=1.0)
    requires_clarification: bool = Field(False)
    clarifying_question: Optional[str] = Field(None)
    provenance: Optional[ProvenanceRecord] = Field(None)
    suggested_actions: List[str] = Field(default_factory=list)
