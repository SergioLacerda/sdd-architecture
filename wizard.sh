#!/bin/bash
set -e

# Check if setup is needed
if ! python3 -c "import typer" 2>/dev/null; then
    echo "⚠️  Dependencies not installed. Running setup..."
    echo ""
    ./setup.sh
    echo ""
fi

echo "🧙 SDD Wizard - Project Generator"
echo "=================================="
echo ""

cd _core

# Run the wizard with all passed arguments
python3 .sdd-wizard/src/wizard.py "$@"
