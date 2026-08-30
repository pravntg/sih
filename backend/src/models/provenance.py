"""
Provenance Data Models — Strict Compliance with docs/provenance_guidelines.md & agents.md
"""
from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field
from datetime import datetime, timezone
import uuid

class AgentChainStep(BaseModel):
    agent: str = Field(..., description="Agent name (e.g. planner, pfz_agent, advisory_synthesizer)")
    version: str = Field(..., description="Version of the agent logic")
    model_version: Optional[str] = Field(None, description="ML/LLM model version if applicable")
    confidence_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    params: Optional[Dict[str, Any]] = Field(default_factory=dict)

class EvidenceItem(BaseModel):
    dataset_id: str = Field(..., description="Canonical dataset ID from docs/datasets_catalog.md")
    file_id: Optional[str] = Field(None, description="Specific raster/telemetry file ID or slice")
    acquisition_timestamp: datetime = Field(..., description="UTC acquisition time of observational data")
    metric: str = Field(..., description="Metric calculated (e.g. sst_gradient, chl_a_mean, wave_height_swh)")
    value: float = Field(..., description="Calculated metric scalar")
    units: str = Field(..., description="Measurement unit (e.g. degC/km, mg/m^3, meters)")
    bbox: Optional[List[float]] = Field(None, description="[min_lon, min_lat, max_lon, max_lat]")
    note: Optional[str] = Field(None, description="License or derivation note")

class ProvenanceRecord(BaseModel):
    recommendation_id: str = Field(default_factory=lambda: f"rec-{uuid.uuid4().hex[:12]}")
    task_id: str = Field(..., description="Idempotent task identifier")
    trace_id: str = Field(default_factory=lambda: f"trace-{uuid.uuid4().hex[:12]}")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    user_context: Optional[Dict[str, Any]] = Field(default_factory=dict)
    agent_chain: List[AgentChainStep] = Field(default_factory=list)
    evidence: List[EvidenceItem] = Field(..., min_length=1, description="Provenance evidence items (must not be empty)")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Composite confidence score")
    explanation: str = Field(..., description="Human-readable explanation based strictly on evidence")
    partial: bool = Field(False, description="True if fallback or degraded mode was utilized")
    fallback_reason: Optional[str] = Field(None, description="Reason for fallback if partial=True")
