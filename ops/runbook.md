# Operational Runbook & Emergency Playbooks

This runbook outlines standard operating procedures (SOPs) and incident mitigation steps for SRE and on-call operators.

---

## 1. Reference Policies

- Rollback triggers and safety thresholds: [`docs/rollout_and_rollback.md`](file:///d:/coding/Github/SIH26/docs/rollout_and_rollback.md)
- Agent operational governance: [`docs/agents.md`](file:///d:/coding/Github/SIH26/docs/agents.md)

---

## 2. Emergency Rollback Execution

If an alert triggers on Stitch topic `orca.alerts.ops`:
1. Check affected service status:
   ```bash
   kubectl get pods -n orca-platform
   ```
2. Revert service to previous known-good deployment:
   ```bash
   kubectl rollout undo deployment/orca-backend-deployment -n orca-platform
   ```
3. Disable affected dynamic feature flags in `infra/feature_flags.yml`.
4. Publish incident audit record to `orca.logs.audit`.
