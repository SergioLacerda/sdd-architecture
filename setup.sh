#!/bin/bash
set -e

echo "🚀 SDD Architecture - Initial Setup"
echo "===================================="
echo ""

# Check Python version
echo "✓ Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
REQUIRED_VERSION="3.8"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" = "$REQUIRED_VERSION" ]; then
    echo "  Found Python $PYTHON_VERSION ✅"
else
    echo "  ERROR: Python $REQUIRED_VERSION or higher required (found $PYTHON_VERSION)"
    exit 1
fi

# Check pip
echo "✓ Checking pip..."
if ! command -v pip3 &> /dev/null; then
    echo "  ERROR: pip3 not found. Please install pip."
    exit 1
fi
pip3 --version | sed 's/^/  /'

# Install CLI dependencies
echo ""
echo "✓ Installing CLI dependencies from _core/requirements-cli.txt..."
if [ -f "_core/requirements-cli.txt" ]; then
    pip3 install -q -r _core/requirements-cli.txt
    echo "  ✅ Installed: typer, click, rich, msgpack, PyYAML"
else
    echo "  ERROR: _core/requirements-cli.txt not found"
    exit 1
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Run the wizard:     ./wizard.sh"
echo "  2. Run the tests:      cd _core && python3 run-all-tests.py"
echo "  3. View docs:          cat _spec/README.md"
echo ""
