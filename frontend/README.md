# Project ORCA — Frontend Application

This directory contains the user interfaces and client dashboards for Project ORCA (Marine Intelligence Platform).

---

## Authoritative UI/UX Design System Rules

> [!IMPORTANT]
> **Strict Styling Constraints:**
> - The UI must use ONLY the exact hex codes defined in [`docs/ui/palette.json`](file:///d:/coding/Github/SIH26/docs/ui/palette.json):
>   - **Deep Sea**: `#0D2B45`
>   - **Ocean Mist**: `#5A7D9A`
>   - **Seafoam**: `#8DBFB7`
>   - **Sandy Shore**: `#DCC7AA`
>   - **Salt Air**: `#F4F6F6`
>   - **Body Text**: `#0B1220`
>   - **Inverse Text**: `#FFFFFF`
> - **NO gradients anywhere**; solid fills only.
> - Rounded corners allowed up to a maximum of `8px`.
> - All frontend builds MUST verify and consume authoritative design assets from Stitch MCP (`orca.ui.designs`).

---

## Directory Structure

- `design/`: Local design manifest synced with Stitch MCP artifacts.
- `public/`: Static assets and favicon files.
- `src/`: Client source code and UI components.
- `styles/`: CSS tokens and variables mapped dynamically from `docs/ui/palette.json`.

---

## Build & Validation Hook

Before running frontend builds, execute the Stitch sync hook:
See [`stitch-design-hook.md`](file:///d:/coding/Github/SIH26/frontend/stitch-design-hook.md).
