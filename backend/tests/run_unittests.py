"""
Standalone Python Unittest Runner
Validates all backend analytics, conversational safety models, and provenance rules.
"""
import unittest
import sys
import os
from datetime import date

# Ensure backend root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.pfz import PfzRequest
from src.services.pfz_service import pfz_service
from src.models.chat import ChatRequest, SafetyStatus, VesselProfile
from src.services.marine_chat_service import marine_chat_service
from src.pipeline.satellite_ingest import satellite_pipeline

class TestOrcaBackend(unittest.TestCase):

    def test_pfz_computation(self):
        req = PfzRequest(bbox=[78.5, 8.5, 79.8, 9.8], target_date=date.today())
        res = pfz_service.compute_pfz(req, task_id="task-test-pfz")
        
        self.assertEqual(res.type, "FeatureCollection")
        self.assertGreaterEqual(len(res.features), 1)
        self.assertGreaterEqual(res.provenance.confidence, 0.65)
        self.assertGreaterEqual(len(res.provenance.evidence), 2)
        
        # Check polygon coordinate closure
        for feat in res.features:
            ring = feat.geometry.coordinates[0]
            self.assertEqual(ring[0], ring[-1], "Polygon must be closed")

    def test_chat_clarification(self):
        req = ChatRequest(user_id="user1", message="Can I go out to sea right now?")
        res = marine_chat_service.process_message(req)
        self.assertTrue(res.requires_clarification)
        self.assertEqual(res.safety_status, SafetyStatus.CLARIFICATION_NEEDED)

    def test_chat_safety_evaluation(self):
        req = ChatRequest(
            user_id="user2",
            message="Check weather conditions",
            coordinates=[9.28, 79.31],
            vessel_profile=VesselProfile(type="trawler", max_safe_wind_kmh=35.0, max_safe_wave_m=2.0)
        )
        res = marine_chat_service.process_message(req)
        self.assertFalse(res.requires_clarification)
        self.assertIn(res.safety_status, [SafetyStatus.SAFE, SafetyStatus.CAUTIOUS])
        self.assertIsNotNone(res.provenance)
        self.assertGreaterEqual(res.provenance.confidence, 0.65)

    def test_satellite_ingest_pipeline(self):
        tile_res = satellite_pipeline.ingest_sentinel_sst_tile({"file_id": "test_s3.nc", "cloud_cover_pct": 10.0})
        self.assertEqual(tile_res["status"], "success")
        self.assertEqual(tile_res["dataset_id"], "dataset:sentinel3_sst")

if __name__ == "__main__":
    unittest.main(verbosity=2)
