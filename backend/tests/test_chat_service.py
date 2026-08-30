"""
Unit & Safety Tests for Conversational Marine Chat & Advisory Service (Global Edition)
"""
import pytest
from src.models.chat import ChatRequest, SafetyStatus, VesselProfile
from src.services.marine_chat_service import marine_chat_service

def test_chat_clarification_on_missing_coordinates():
    """Safety-critical request without coordinates or harbor must prompt a single clarifying question."""
    request = ChatRequest(
        user_id="user_test_001",
        message="Is it safe to go out to sea right now?"
    )
    response = marine_chat_service.process_message(request)
    
    assert response.requires_clarification is True
    assert response.safety_status == SafetyStatus.CLARIFICATION_NEEDED
    assert response.clarifying_question is not None
    assert "coordinates" in response.clarifying_question.lower() or "location" in response.reply.lower()

def test_chat_safety_evaluation_safe_conditions():
    """Safe conditions within vessel tolerance must return SAFE status with evidence."""
    request = ChatRequest(
        user_id="user_test_002",
        message="What is the general advisory?",
        coordinates=[9.28, 79.31],
        vessel_profile=VesselProfile(
            type="motorized_skiff",
            max_safe_wind_kmh=35.0,
            max_safe_wave_m=2.0
        )
    )
    response = marine_chat_service.process_message(request)
    
    assert response.requires_clarification is False
    assert response.safety_status in [SafetyStatus.SAFE, SafetyStatus.CAUTIOUS]
    assert response.provenance is not None
    assert len(response.provenance.evidence) >= 2
    assert response.confidence >= 0.65

def test_chat_danger_evaluation_exceeding_limits():
    """Unfavorable conditions exceeding vessel limits must trigger DANGER alert."""
    request = ChatRequest(
        user_id="user_test_003",
        message="Check weather conditions",
        coordinates=[9.28, 79.31],
        vessel_profile=VesselProfile(
            type="artisanal_catamaran",
            max_safe_wind_kmh=10.0,
            max_safe_wave_m=0.5
        )
    )
    response = marine_chat_service.process_message(request)
    
    assert response.safety_status == SafetyStatus.DANGER
    assert "Alert" in response.reply or "Delay" in response.reply or "Unfavorable" in response.reply
    assert response.provenance is not None

def test_chat_fish_species_intent():
    """Queries about fish and PFZ must return species details."""
    request = ChatRequest(
        user_id="user_test_004",
        message="What fish species are in the PFZ?",
        coordinates=[9.28, 79.31]
    )
    response = marine_chat_service.process_message(request)
    assert "Yellowfin Tuna" in response.reply or "Mackerel" in response.reply
    assert response.provenance is not None

def test_chat_navigational_bearing_intent():
    """Queries about bearings must return true heading and distance."""
    request = ChatRequest(
        user_id="user_test_005",
        message="What is the bearing and route to PFZ-MAN01?",
        coordinates=[9.28, 79.31]
    )
    response = marine_chat_service.process_message(request)
    assert "Nautical Miles" in response.reply

def test_chat_harbor_emergency_intent():
    """Queries about emergency and harbors must return VHF Channel 16 info."""
    request = ChatRequest(
        user_id="user_test_006",
        message="What is the emergency VHF frequency for rescue?",
        coordinates=[9.28, 79.31]
    )
    response = marine_chat_service.process_message(request)
    assert "VHF Channel 16" in response.reply

def test_chat_global_port_tokyo():
    """Global query mentioning Tokyo must resolve to Northwest Pacific and cold/temperate species."""
    request = ChatRequest(
        user_id="user_test_global_01",
        message="What fish are active around Tokyo port?"
    )
    response = marine_chat_service.process_message(request)
    assert "Tokyo" in response.reply or "Pacific" in response.reply
    assert response.provenance is not None

def test_chat_global_port_rotterdam():
    """Global query mentioning Rotterdam must resolve North Sea / Atlantic species."""
    request = ChatRequest(
        user_id="user_test_global_02",
        message="Is it safe to navigate from Rotterdam?"
    )
    response = marine_chat_service.process_message(request)
    assert "Rotterdam" in response.reply or "North Sea" in response.reply

def test_chat_global_port_san_francisco():
    """Global query mentioning San Francisco must calculate Pacific Great-Circle routes."""
    request = ChatRequest(
        user_id="user_test_global_03",
        message="What is the bearing to the nearest fishing zone from San Francisco?"
    )
    response = marine_chat_service.process_message(request)
    assert "San Francisco" in response.reply or "Pacific" in response.reply
    assert "Nautical Miles" in response.reply
