## Description
<!-- Provide a summary of the changes introduced by this PR -->

## Task & Traceability
- **Task ID**: <!-- e.g. task-uuid-001 -->
- **Trace ID**: <!-- e.g. trace-uuid-001 -->
- **Risk Level**: `[low | medium | high]`
- **Safety Critical (`safety_flag: high`)**: `[true | false]`
- **Domain Approval Required**: `[true | false]`
- **Domain Sign-off**: <!-- Name/Role if required -->

## Provenance Metadata
```json
{
  "task_id": "<!-- task_id -->",
  "datasets_used": [
    <!-- "dataset:sentinel3_sst", "dataset:modis_chl" -->
  ],
  "model_versions": [
    <!-- "pfz_v0.4" -->
  ]
}
```

## Changes Made
- [ ] Added / Updated unit tests (Coverage: `__%`)
- [ ] Static analysis & linting pass with 0 errors
- [ ] Security SCA scan passes with 0 Critical / 0 High
- [ ] UI components validated against `orca.ui.designs` and `docs/ui/palette.json`

## Local Verification & Test Instructions
<!-- Steps to run unit and integration tests locally -->
```bash
# Example:
pytest tests/ -v
```

## Rollback Plan
<!-- Explicit steps to revert this PR if post-deploy metrics degrade -->
1. Disable feature flag: `flags.<feature_name>.enabled = false`
2. Revert commit / Redeploy previous stable container image `s3://...` or tag `vX.Y.Z-prev`.
