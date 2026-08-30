#!/usr/bin/env bash
set -euo pipefail

echo "========================================================"
echo "Project ORCA — Bootstrap Environment & Local Smoke Check"
echo "========================================================"

# 1. Check directories
echo "==> Validating required project directories..."
for dir in backend frontend infra docs docs/ui ops scripts; do
    if [ ! -d "$dir" ]; then
        echo "Error: Directory '$dir' is missing!"
        exit 1
    fi
done
echo "Directories verified."

# 2. Check authoritative docs
echo "==> Validating authoritative docs and UI tokens..."
if [ ! -f "docs/agents.md" ]; then
    echo "Error: docs/agents.md is missing!"
    exit 1
fi

if [ ! -f "docs/ui/palette.json" ]; then
    echo "Error: docs/ui/palette.json is missing!"
    exit 1
fi
echo "Authoritative docs verified."

# 3. Check configuration templates
echo "==> Validating configuration & templates..."
if [ ! -f "PULL_REQUEST_TEMPLATE.md" ]; then
    echo "Error: PULL_REQUEST_TEMPLATE.md is missing!"
    exit 1
fi

echo "========================================================"
echo "Bootstrap verification complete: All starter artifacts OK."
echo "========================================================"
