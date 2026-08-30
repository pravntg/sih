"""
Stitch MCP Message Handler & 2-Hour Developer-Manager Loop Controller
Subscribes to orca.* topics and coordinates automated gating, PR reviews, and audit trails.
"""
import json
import logging
from typing import Dict, Any
from datetime import datetime, timezone

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("stitch_handler")

TOPICS = {
    "DEV_REQUEST": "orca.tasks.developer.request",
    "DEV_STATUS": "orca.tasks.developer.status",
    "MGR_REQUEST": "orca.reviews.manager.request",
    "MGR_RESPONSE": "orca.reviews.manager.response",
    "UI_DESIGNS": "orca.ui.designs",
    "ALERTS_OPS": "orca.alerts.ops",
    "LOGS_AUDIT": "orca.logs.audit"
}

class StitchLoopController:
    def __init__(self):
        self.coverage_threshold = 70.0
        self.high_risk_coverage_threshold = 80.0

    def evaluate_pr_review_request(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Manager Agent Automated Gating:
        - Unit tests pass
        - Coverage >= threshold
        - Lint errors == 0
        - SCA critical == 0 & high == 0
        - Provenance snapshot present
        """
        task_id = message.get("task_id", "unknown")
        coverage = message.get("coverage", 0.0)
        lint = message.get("lint", {})
        ci = message.get("ci", {})
        security = message.get("security_scan", {})
        provenance = message.get("provenance_snapshot", {})

        reasons = []

        # 1. CI Gating
        if ci.get("unit") != "pass":
            reasons.append({"reason": "Unit tests must all pass."})

        # 2. Coverage Gating
        if coverage < self.coverage_threshold:
            reasons.append({"reason": f"Coverage {coverage}% is below threshold {self.coverage_threshold}%."})

        # 3. Lint Gating
        if lint.get("errors", 0) > 0:
            reasons.append({"reason": f"Linting has {lint.get('errors')} unresolved error(s)."})

        # 4. Security Gating
        if security.get("critical", 0) > 0 or security.get("high", 0) > 0:
            reasons.append({"reason": "Critical or High SCA security vulnerabilities found."})

        # 5. Provenance Presence
        if not provenance.get("datasets") and not provenance.get("model_versions"):
            reasons.append({"reason": "Provenance snapshot must declare datasets_used and model_versions."})

        now_utc = datetime.now(timezone.utc).isoformat()

        if reasons:
            decision = "request_changes"
            next_step = "Please address requested checklist and update PR."
        else:
            decision = "approve_for_staging"
            next_step = "Merge to staging permitted under safe-mode feature flag."

        response = {
            "topic": TOPICS["MGR_RESPONSE"],
            "task_id": task_id,
            "decision": decision,
            "changes_requested": reasons,
            "created_at": now_utc,
            "next_step": next_step
        }

        logger.info(f"Manager Review Decision for {task_id}: {decision}")
        return response

    def create_audit_record(self, event_type: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Creates an immutable audit log record for orca.logs.audit."""
        return {
            "topic": TOPICS["LOGS_AUDIT"],
            "event": event_type,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "payload": payload
        }

stitch_controller = StitchLoopController()
