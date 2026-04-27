#!/bin/bash
set -euo pipefail

echo "🚀 SDD Architecture - Initial Setup"
echo "===================================="
echo ""

# Check Python version
echo "✓ Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
REQUIRED_VERSION="3.10"

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

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo ""
    echo "📦 Creating virtual environment (.venv)..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "✓ Activating virtual environment..."
source .venv/bin/activate 2>/dev/null || source .venv/Scripts/activate

# Install CLI dependencies
echo ""
echo "✓ Installing dependencies into virtualenv from _core/pyproject.toml..."
if [ -f "_core/pyproject.toml" ]; then
    pip install --upgrade pip -q
    pip install -q -e "./_core[dev]"
    echo "  ✅ Installed runtime and dev dependencies"
else
    echo "  ERROR: _core/pyproject.toml not found"
    exit 1
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Run the wizard:     ./wizard.sh"
echo "  2. Run the tests:      make test"
echo "  3. View docs:          cat _spec/README.md"
echo ""
