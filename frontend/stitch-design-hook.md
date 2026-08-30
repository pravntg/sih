# Stitch UI Design Build Hook

> [!IMPORTANT]
> **Stitch MCP UI Verification Rule**
> Frontend MUST fetch and verify `orca.ui.designs` artifact from Stitch MCP prior to build.

---

## Verification Protocol

1. **Fetch Latest Design Artifact**:
   - Subscribe or query Stitch MCP topic `orca.ui.designs`.
   - Retrieve signed design JSON / layout spec.

2. **Verify Checksum & Digital Signature**:
   - Validate checksum against `docs/ui/manifest.json`.
   - Confirm all color tokens strictly map to [`docs/ui/palette.json`](file:///d:/coding/Github/SIH26/docs/ui/palette.json).

3. **Gating Check**:
   - If visual diff or token discrepancy is detected, fail the frontend CI build immediately.
