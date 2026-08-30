Agents.md — Agent Rules, Policies & UI Style Guide

Agentic Marine Intelligence Platform — authoritative rules for agents, feature generation, failure handling, rollback, and strict UI colour/style constraints.

Purpose: this file defines strict, enforceable policies for all autonomous agents and developer workflows so agents do not hallucinate, do not alter existing features silently, and recover safely when failures occur. It also defines the exact UI palette and styling rules — no gradients, only solid colours using the exact hex codes shown in the attached design image.

1. Quick reference — approved colour palette (use only these hex codes)
Deep Sea — #0D2B45 (primary dark)
Ocean Mist — #5A7D9A (primary mid)
Seafoam — #8DBFB7 (accent / positive)
Sandy Shore — #DCC7AA (neutral / panel background)
Salt Air — #F4F6F6 (surface background / white replacement)

UI rule: The UI must strictly adhere to these exact hex values. No tinting, no lightening/darkening (no programmatic color transforms). No additional colours beyond these five and black/near-black for text (#0B1220 recommended) and translucent overlays for accessibility only. Any addition must be reviewed and approved by product + design.

2. UI style constraints (non-negotiable)
No gradients anywhere in the UI (backgrounds, buttons, cards, headers). Use solid fills only.
Hard edges and solid boundaries — rounded corners allowed (max 8px), but elements must have crisp borders if separation needed.
No “AI-looking” UI treatments — i.e., avoid neon glows, animated shimmering, or “futuristic” glyphs. Use human-centered, utilitarian layout: clear labels, consistent spacing, and readable typography.
Typography:
Primary headings: system font stack or a neutral sans-serif (e.g., Inter / Roboto) — medium weight.
Body text color: #0B1220 (or #0D2B45 when appropriate); never use palette colours for primary body text unless contrast ratio is maintained.
Contrast & accessibility:
All text must meet WCAG AA contrast against its background. If a palette colour fails contrast for small text, use #0B1220 on light backgrounds or #FFFFFF on dark backgrounds.
Borders & separators:
Use 1px solid borders where needed. Border colour options: #0D2B45 at 10–20% opacity over #F4F6F6, or #DCC7AA for neutral separation — but never introduce a new hue.
Icons & imagery:
Icons should be simple, flat, and single-colour (monochrome). Use the palette sparingly for icon states (e.g., #8DBFB7 for positive). Avoid decorative AI-styled illustrations.
Map / visualization overlays:
Map tiles may be neutral; overlay layers (PFZ, advisories) must use the palette and solid polygons/lines (no gradient heatmaps). PFZ polygons — use #8DBFB7 with 30–40% fill alpha and #0D2B45 100% stroke for outline.

Sample CSS variables (copy into design system):

:root{
  --color-deep-sea: #0D2B45;
  --color-ocean-mist: #5A7D9A;
  --color-seafoam: #8DBFB7;
  --color-sandy-shore: #DCC7AA;
  --color-salt-air: #F4F6F6;
  --text-default: #0B1220;
  --border: rgba(13, 43, 69, 0.08);
}
3. Agent behaviour: core principles (always enforce)
Provenance-first: no statement of fact about observational data, model output, or recommendation may be returned without at least one provenance entry (dataset id/file/time and model/version). A provenance object must include:
dataset id (catalog id), acquisition timestamp, product name (e.g., SST), file id or URL (if license allows), and processing level; plus model version and confidence score.
No hallucination policy:
Agents must never invent dataset names, timestamps, or file IDs. If an agent does not find an explicit dataset/file that supports a claim, it must:
(A) ask a clarifying question, or
(B) respond with an explicit statement of uncertainty ("I do not have data to support that claim") and follow with recommended next steps.
Minimum evidence threshold:
For any operational recommendation (e.g., "safe to go out to sea"), the combined evidence confidence must be above a configurable threshold (default 0.65). If below threshold, agent should respond with conservative advice and label the recommendation low_confidence.
Explainability:
Every conclusion must include a short human-readable rationale (2–4 bullets) and a machine-readable evidence list (dataset/file/time, metric used, value).
Ask instead of guessing:
If required input is missing (vessel profile, coordinates, desired time), agent prompts for it — do not assume defaults that materially affect safety.
Deterministic outputs:
Given the same inputs and dataset versions, agent outputs must be deterministic (same recommendation_id, same content). Non-determinism must be recorded (random seeds or inference logs).
Limited creativity:
Answers must be factual, concise, and avoid speculative phrasing. Avoid storytelling language. Keep suggestions action-oriented.
4. Data & model rules
Dataset catalog governance:
Agents consult the canonical datasets catalog only. Each dataset entry must include license flags (redistributable) and a freshness timestamp.
If a dataset is flagged non-redistributable, agents may use derived aggregated metrics (mean, anomaly) but must not expose direct raw download links.
Model registry:
Agents must reference model_registry entries with name + version when using a model. The registry entry must contain evaluation metrics for the current model vs baseline.
Fallback selection:
If primary dataset/model is unavailable, the agent picks the best fallback according to a deterministic priority list. All fallbacks used must be included in provenance.
Confidence computation:
Confidence = f(model_confidence, data_freshness_score, cross-source_agreement). Compute and expose the components and final scalar [0..1].
No silent parameter drift:
Agents must not change default parameters (e.g., PFZ chlorophyll threshold, wave safety cutoffs) without a change recorded in the config changelog and an approved migration in version control. Any parameter changes must be annotated in provenance for new results.
5. Interaction rules (conversational safety & UX)
Clarifying questions:
If a user query can meaningfully change the answer (location ambiguity, vessel type), the agent asks 1 succinct clarifying question rather than guessing.
Multi-turn context safety:
Agents must bind critical values (coords, vessel profile) to the session; if user updates them, agent must confirm before using them for risk-critical decisions.
Language policy:
Detect language automatically; reply in the same language. For translations, use the translation module only; always include a short English canonical statement when safety-critical instructions are given, to avoid translation ambiguity.
No precise step-by-step procedural instructions for dangerous activities:
Agents may provide high-level safety advice but must not provide prescriptive instructions that could increase risk (e.g., "launch now at 06:00" without explicit confirmation and matching safety criteria).
User overrides / corrections:
Users can flag recommendations as incorrect. Every flagged recommendation generates a review ticket and is used in retraining datasets.
6. Feature generation & change-control rules (agents must obey)
Agents must not autonomously modify product features:
Agents are allowed to propose new features (issue PRs, create backlog tickets) but must not merge code, create DB schema changes, or alter runtime config.
Feature proposal must contain:
Motivation, impact, data dependencies, necessary migrations, UI mocks, test plan, and rollback plan.
CI gating:
Any new feature must pass automated tests (unit + integration + acceptance scenarios) and a safety review (domain expert sign-off) prior to deployment.
Schema migrations:
No agent should apply DB migrations. Migration artifacts may be generated but human operator must approve and run migrations.
Runtime config changes:
Agents may suggest tuning values (thresholds), but applying changes requires an authenticated admin action logged in config_changes with reason and rollback instructions.
7. Rollback, failure handling & recovery (operational rules)
7.1 Rollback triggers (automatic)

An automated rollback (or partial disable) MUST be triggered automatically when one or more of the following thresholds are reached for a deployment/model/feature within a defined monitoring window (24 hours unless noted):

Safety-critical alert failure: False-positive rate for HIGH severity alerts > 10% (24h window) OR false-negative discovery for simulated incidents > 5% → auto-disable auto-broadcasting for this model and create human review ticket.
User complaint surge: > 5% of active users flag recommendations as incorrect for a new model within 24h.
Model drift: data drift score > configured threshold (e.g., population shift beyond X sigma) OR model eval metrics degrade > 10% vs baseline → roll back to previous stable model.
System stability: error rate of relevant API endpoints > 5% (P95) or task queue error rate > 5% for 30 consecutive minutes.
Resource exhaustion: queue depth exceeds emergency threshold AND backpressure cannot be resolved within 10 minutes.
7.2 Rollback actions (automated + manual)
Automated immediate actions (system will):
Flip feature flag(s) to disable the affected agent/model behavior (safe default).
Re-deploy last stable container image for the agent/model (automated rollback pipeline), if safe to do so.
Publish a system message in the status channel and create an incident ticket with full provenance and logs.
Suspend mass notifications until human review approves re-enable.
Manual follow-up:
On-call SRE + Domain lead investigate. Use provenance to trace datasets, model versions, parameters.
If a DB migration caused the problem, follow migration rollback playbook (idempotent down migration or restore from backup depending on change). Prefer no destructive down-migration — design forward/backward compatible migrations.
If rollback fails, activate incident escalation path (paged human-in-loop).
Post-mortem & measures:
Run root-cause analysis (RCA) within 48 hours and schedule fixes and tests. Update regression suites with reproduction steps.
7.3 Safe defaults & degraded-mode behaviour

When features are disabled due to rollback or data unavailability:

App should display clear, actionable information: "We are temporarily using cached data; live PFZ recomputation unavailable."
For safety-critical queries: default to conservative advice (e.g., avoid voyage) and recommend contacting local authorities.
Agents must annotate results with partial: true, reason: "fallback: cached data" and confidence lowered accordingly.
8. Observability & provenance requirements
Traceability:
Every agent action must log: trace_id, task_id, user_id, input_snapshot, output_snapshot, datasets_used, model_version, confidence, timestamp.
Provenance record:
Immutable provenance per recommendation saved in DB + JSON snapshot to object store.
UI must display a condensed provenance card with source names, timestamps and a "View full provenance" link.
Monitoring dashboards:
Model health: precision/recall, confidence distribution, drift metrics.
Agent health: latency, error rate, queue length, DLQ counts.
Alert metrics: delivery success rates by channel, false-positive/negative counts from user feedback.
Audit logs:
Config changes, dataset onboarding, approvals, rollbacks must be logged with actor id and timestamp.
9. Testing & validation rules (pre-release requirements)
Unit tests for each agent function with mock datasets and edge-case checks.
Integration tests for planner → agent → synthesizer end-to-end flows.
Domain acceptance tests with historical data and labelled ground-truth (PFZ ground truth, adverse event logs).
Chaos tests simulate:
Data feed loss, corrupted files, Stitch MCP outages, backpressure spikes.
Agents must degrade gracefully and the system must trigger rollback conditions in detection scenarios.
User acceptance / pilot:
Before model full release, run pilot with representative users and require domain sign-off for safety-critical behaviour.
10. Security, privacy & compliance rules
PII minimization — store only absolutely necessary user PII (phone/email). Users may request deletion; agents must respect privacy flags.
Encrypted-at-rest & in-transit — all stores and APIs must use TLS and provider-managed encryption keys or Vault.
Dataset licensing — respect license redistributable flags; when not redistributable, do not include raw file URLs in outbound messages.
Access control — agent actions that modify datasets, configs, or feature flags require RBAC checks (admin or dataset-owner role).
Secrets — no hard-coded keys in agent code. Use secrets manager.
## Continuous Dev-Review Loop Policies (mandatory)

1. Two-agent loop: Developer agent and Manager agent operate in repeating 2-hour cycles. Developer executes feature work; Manager reviews and issues directives at each cycle boundary. Both agents must obey these timing constraints and produce required artifacts each cycle.

2. Task & messaging contracts:
   - All tasks use `task_id` and `idempotency_key`.
   - Planner publishes tasks to `amip.tasks.developer.request`.
   - Developer reports status to `amip.tasks.developer.status`.
   - Developer forwards PRs to `amip.reviews.manager.request`.
   - Manager replies on `amip.reviews.manager.response`.

3. PR & CI requirements (must be enforced by CI):
   - Unit tests pass and coverage > configured threshold.
   - Lint = 0 errors.
   - SCA critical/high = 0.
   - UI snapshot matches `amip.ui.designs`.

4. Merge & deploy policy:
   - Developer may create PRs and artifacts but MAY NOT merge to `main` or flip feature flags in production.
   - Manager approves for staging; SRE performs production merges per policy.

5. Rollback policy:
   - If any defined safety or stability threshold breaches during staging/prod, Manager must trigger rollback and suspend mass notifications.
   - Rollback steps must be present in every PR.

6. Provenance for changes:
   - Every PR/commit that affects data, models, or recommendations must include `provenance:{task_id,datasets_used,model_versions}` and create an audit log record.

7. Human-in-the-loop for safety-critical features:
   - Any feature with `safety_flag:"high"` must have at least one domain expert approval before Manager signs off.

8. No autonomous production changes:
   - No agent may modify production feature flags, merge to `main`, or run DB schema migrations without Manager and SRE authorization.

9. CI / Canary gating:
   - New changes deploy to canary (5% traffic) with telemetry monitoring for the cycle window; Manager must watch canary metrics before full rollout.

10. Audit & feedback:
   - Negative user feedback tagged to a recommendation creates a review ticket that is prioritized in the backlog for Manager review.

11. Developer workflow & governance
Propose → Review → Merge:
Any proposed agent change must include tests, documentation updates (this file), a migration plan (if required), and a rollback plan.
Canary & progressive rollout:
Deploy new agent models/features first to canary group (5% of users), monitor key metrics for a configurable period, then progressively increase traffic.
Feature flags:
All behavioral changes must be behind feature flags; flags must support immediate global disable.
Change log & versioning:
Maintain a change log linking PRs to provenance changes. Model/version schema: <name>_v<semver>.
Human-in-the-loop:
Safety-critical changes require signoff from at least one domain expert and one SRE engineer.
12. Example JSON provenance schema (required in every recommendation)
{
  "recommendation_id":"rec-uuid",
  "created_at":"2026-08-30T09:00:00Z",
  "user_context":{"user_id":"u-123","coords":[9.761,78.123],"vessel_profile":{"type":"skiff","max_wind_kmh":25}},
  "agent_chain":[
    {"name":"planner","version":"v1.2.1","params":{...}},
    {"name":"data_discovery","version":"v1.0","datasets":[{"id":"ds-uuid","product":"SST","file_id":"file-uuid","acquired_at":"2026-08-30T05:30:00Z"}]},
    {"name":"pfz_agent","version":"pfz_v0.4","model_metrics":{"auc":0.88},"used_params":{"chl_threshold":0.3}}
  ],
  "evidence":[
    {"dataset_id":"ds-uuid","file_id":"file-uuid","metric":"chl_mean","value":0.45,"units":"mg/m3","bbox":[...]}
  ],
  "confidence":0.73,
  "explanation":"PFZ detected due to elevated chlorophyll and SST gradient. Conservative safety rating applied."
}
13. Edge-case examples & mandated agent outputs
Missing data → "status":"partial","reason":"sst_unavailable","confidence":0.42","recommendation":"defer; no reliable PFZ computation available; consider local buoy data or wait until 08:00 UTC."
Low confidence → "status":"low_confidence","recommendation":"conservative: avoid voyage", "suggestion":"Would you like me to notify you if conditions improve?"
License restricts raw data → "evidence":[{"dataset_id":"ds-uuid","product":"SST","note":"raw file access restricted by license; using derived SST anomaly metric"}]

Agents must produce these structured outputs (machine-readable) as well as the short human-text replies.

14. Enforcement & audits
Automated linting:
A CI job enforces that all agent code writes provenance and includes confidence in outputs. PRs failing these checks must be rejected.
Periodic audits:
Weekly audit for recent recommendations to check for missing provenance or hallucination flags.
User feedback loop:
Every negative feedback must be triaged within 24 hours and aggregated for model retraining decisions.
15. Appendix — checklist before any model/feature release
 Unit + integration tests passing
 Domain acceptance test signed by 1 domain expert
 CI canary deployment set up
 Feature flag created for immediate disable
 Rollback runbook attached to PR
 Provenance & trace logging validated
 Monitoring dashboards added & alert thresholds set
 Licensing verification for all datasets used
 Pilot user plan and communication prepared
Final notes (tone & governance)

This document is the authority for agent behaviour and UI style. Any deviation (especially adding colours or gradients, or enabling agents to auto-modify runtime features) is prohibited without documented approval. Agents must behave conservatively, be transparent, and always prioritize human safety and explainability over delivering a neat-sounding answer.