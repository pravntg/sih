# Authoritative Documentation & Specifications

All required background, design constraints, agent rules, dataset catalogs, and provenance requirements are contained under `docs/`. Consult these before producing or merging any code or design artifacts.

---

## Directory & File Index

1. [`agents.md`](file:///d:/coding/Github/SIH26/docs/agents.md) — Authoritative Agent Rules, Operational Policies, 2-Hour Dev-Review Loop, Rollback Criteria, and UI Constraints.
2. [`ui/`](file:///d:/coding/Github/SIH26/docs/ui/) — Design tokens, official color palette, and Stitch UI asset manifest.
   - [`palette.json`](file:///d:/coding/Github/SIH26/docs/ui/palette.json)
   - [`tokens.json`](file:///d:/coding/Github/SIH26/docs/ui/tokens.json)
   - [`manifest.json`](file:///d:/coding/Github/SIH26/docs/ui/manifest.json)
3. [`datasets_catalog.md`](file:///d:/coding/Github/SIH26/docs/datasets_catalog.md) — Canonical datasets catalog, acquisition sources, licensing, and freshness criteria.
4. [`provenance_guidelines.md`](file:///d:/coding/Github/SIH26/docs/provenance_guidelines.md) — Strict guidelines on capturing, embedding, and validating data and model provenance.
5. [`rollout_and_rollback.md`](file:///d:/coding/Github/SIH26/docs/rollout_and_rollback.md) — Deployment stages (Canary 5%), automated rollback triggers, and safe-degrade procedures.
6. [`project_initialisation_prompt.md`](file:///d:/coding/Github/SIH26/docs/project_initialisation_prompt.md) — Bootstrap prompt and Stitch orchestration topic definitions.
7. [`project_flow_and_tech_stack.md`](file:///d:/coding/Github/SIH26/docs/project_flow_and_tech_stack.md) — Comprehensive System Flowchart Guide, Technology Stack, and Live Observational Data Collection Fronts.
8. [`AppFlow.docx`](file:///d:/coding/Github/SIH26/docs/AppFlow.docx), [`BackendSchema.docx`](file:///d:/coding/Github/SIH26/docs/BackendSchema.docx), [`PRD.docx`](file:///d:/coding/Github/SIH26/docs/PRD.docx), [`TRD.docx`](file:///d:/coding/Github/SIH26/docs/TRD.docx) — Initial requirements and architectural documents.

> [!CAUTION]
> Do NOT edit any file under `/docs/` directly without Manager approval. Propose changes via PRs with `docs_change_proposal`.
