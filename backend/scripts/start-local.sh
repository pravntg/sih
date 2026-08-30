#!/usr/bin/env bash
set -euo pipefail

echo "==> Starting ORCA Backend Services locally..."

# Verify Python environment
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH."
    exit 1
fi

export ENVIRONMENT="development"
export PORT="${PORT:-8000}"

echo "==> Starting service on port ${PORT}..."
# Stub for local server initialization
if [ -f "src/main.py" ]; then
    python3 -m src.main
else
    echo "Backend src/main.py skeleton ready for implementation."
fi
