#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PYTHON="$SCRIPT_DIR/.venv/bin/python"

# Check if setup is needed (venv or typer missing)
if [ ! -x "$VENV_PYTHON" ] || ! "$VENV_PYTHON" -c "import typer" 2>/dev/null; then
    echo "⚠️  Dependencies not installed. Running setup..."
    echo ""
    bash "$SCRIPT_DIR/setup.sh"
    echo ""
fi

echo "🧙 SDD Wizard - Project Generator"
echo "=================================="
echo ""

cd "$SCRIPT_DIR/_core"

# Run the wizard with all passed arguments
"$VENV_PYTHON" .sdd-wizard/src/wizard.py "$@"
