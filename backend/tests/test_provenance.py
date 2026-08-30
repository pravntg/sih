"""
Tests for Provenance Verification Service
"""
import pytest
from datetime import datetime, timezone
from src.models.provenance import ProvenanceRecord, EvidenceItem
from src.services.provenance_service import provenance_service

def test_validate_valid_provenance():
    now_utc = datetime.now(timezone.utc)
    record = ProvenanceRecord(
        task_id="task-prov-01",
        confidence=0.88,
        explanation="Valid satellite evidence",
        evidence=[
            EvidenceItem(
                dataset_id="dataset:sentinel3_sst",
                acquisition_timestamp=now_utc,
                metric="sst_gradient",
                value=0.82,
                units="degC/km"
            )
        ]
    )
    assert provenance_service.validate_provenance_record(record) is True

def test_validate_invalid_provenance_empty_evidence():
    now_utc = datetime.now(timezone.utc)
    # Testing that pydantic or validation rejects empty or invalid evidence
    with pytest.raises(Exception):
        ProvenanceRecord(
            task_id="task-prov-invalid",
            confidence=0.5,
            explanation="No evidence provided",
            evidence=[]
        )
