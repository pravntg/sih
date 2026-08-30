# Contributing to Project ORCA

All contributors (human developers and autonomous agents) must adhere strictly to the rules defined in [`docs/agents.md`](file:///d:/coding/Github/SIH26/docs/agents.md) and [`docs/`](file:///d:/coding/Github/SIH26/docs/).

---

## 1. Branch Naming Conventions

All feature and bugfix work must be done on dedicated branches following this pattern:
```text
dev/<task-id>-<short-description>
```
Examples:
- `dev/task-001-pfz-microservice`
- `dev/bootstrap-init`

---

## 2. Commit Message & Provenance Requirement

Every commit must include provenance metadata trailer in the commit message format:
```text
<type>(<scope>): <summary>

Detailed description of the change.

provenance:{task_id:"<task-id>", datasets_used:["<dataset-id-or-file>"], model_versions:["<model-version>"]}
```

If no models or datasets are affected (e.g. documentation or infra skeleton), specify empty arrays:
`provenance:{task_id:"task-001", datasets_used:[], model_versions:[]}`.

---

## 3. Pull Request Guidelines

1. Every PR must be opened using [`PULL_REQUEST_TEMPLATE.md`](file:///d:/coding/Github/SIH26/PULL_REQUEST_TEMPLATE.md).
2. Ensure unit tests pass locally with test coverage >= 70% (80% for high-risk modules).
3. Ensure zero lint errors and zero SCA critical/high security vulnerabilities.
4. For frontend PRs, confirm alignment with [`docs/ui/palette.json`](file:///d:/coding/Github/SIH26/docs/ui/palette.json) and verified Stitch UI artifacts from `orca.ui.designs`.
5. No direct merges to `main` or autonomous production flag updates. Merging to staging requires Manager approval; staging to `main` requires SRE and Manager sign-off.
