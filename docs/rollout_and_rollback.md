# Rollout, Gating & Rollback Policies

This document formalizes the deployment stages, gating criteria, and emergency rollback playbooks for Project ORCA.

---

## 1. Staged Rollout Pipeline

1. **Development & Cycle PR**: Tested in isolation during 2-hour cycles; requires green CI, SCA, and test coverage >= 70% (80% for high-risk).
2. **Staging Environment**: Approved by Manager Agent; deployed behind safe-mode feature flags (default disabled).
3. **Canary Release (5% Traffic)**: Released to a 5% canary cohort for a minimum 60-minute telemetry observation window.
4. **Full Production Rollout**: Requires Manager + SRE sign-off following green canary window.

---

## 2. Automated & Manual Rollback Triggers

An immediate automated rollback or feature flag disabling is triggered under any of the following conditions:

- **Error Rate Surge**: Core API error rate exceeds > 2% or increases > 3x over baseline within 30 minutes of deployment.
- **Safety False Alerts**: False-positive rate for High-severity safety alerts exceeds 10% in 24h, or any false negative in simulated danger events.
- **User Complaints / Flags**: > 5% of active users flag a new recommendation/advisory as incorrect within 24h.
- **Model Drift & Metric Degradation**: Model precision degrades > 10% compared to baseline or data drift exceeds threshold.
- **Data Truncation / Corruption**: Missing raster tiles or checksum failures resulting in partial or truncated outputs without graceful degradation.

---

## 3. Rollback Playbook & Execution

When a breach is detected:
1. **Manager Command**: Manager publishes an emergency command to Stitch topic `orca.alerts.ops`:
   ```json
   {
     "action": "rollback",
     "target": "service",
     "service": "<service_name>",
     "target_version": "<previous_stable_image>",
     "reason": "<breach_summary>"
   }
   ```
2. **Safe-Mode Toggle**: The service immediately switches to safe degraded mode:
   - Live dynamic recomputation is suspended.
   - Cached/historical baselines are used with explicit `partial: true` annotations.
   - Mass advisory broadcasts are paused until human operator verification.
3. **Audit Log Record**: An immutable record is published to `orca.logs.audit`.
