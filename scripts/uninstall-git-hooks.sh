#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "[DEPRECATED] Use: python scripts/git_hooks.py uninstall"
python3 "$SCRIPT_DIR/git_hooks.py" uninstall
