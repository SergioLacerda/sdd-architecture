#!/usr/bin/env bash
set -euo pipefail

echo "🚀 SDD Workspace Setup"
echo "======================"

#######################################
# 🧠 Detect Python
#######################################
if command -v python3 >/dev/null 2>&1; then
    PYTHON=python3
elif command -v python >/dev/null 2>&1; then
    PYTHON=python
else
    echo "❌ Python not found"
    exit 1
fi

echo "✓ Using Python: $PYTHON"

#######################################
# 🧠 Create venv
#######################################
if [ ! -d ".venv" ]; then
    echo "✓ Creating virtual environment..."
    $PYTHON -m venv .venv
fi

#######################################
# 🧠 Activate venv
#######################################
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
elif [ -f ".venv/Scripts/activate" ]; then
    source .venv/Scripts/activate
else
    echo "❌ Could not activate virtualenv"
    exit 1
fi

echo "✓ Virtualenv activated"

#######################################
# 🧠 Upgrade pip
#######################################
python -m pip install --upgrade pip -q

#######################################
# 🧠 Install packages (ordered)
#######################################
echo ""
echo "📦 Installing SDD packages..."

# 🔥 ordem explícita (evita problemas de dependência)
ORDERED_PACKAGES=(
    "packages/core/sdd_core"
    "packages/core/sdd_compiler"
    "packages/features/sdd_integration"
    "packages/interfaces/sdd_wizard"
    "packages/interfaces/sdd_cli"
)

for pkg in "${ORDERED_PACKAGES[@]}"; do
    if [ -f "$pkg/pyproject.toml" ]; then
        echo "  → Installing $pkg"
        python -m pip install -e "$pkg"
    else
        echo "  ⚠ Skipping $pkg (no pyproject.toml)"
    fi
done

#######################################
# 🧠 Install any remaining packages
#######################################
for pkg in packages/*/*; do
    if [ -f "$pkg/pyproject.toml" ]; then
        skip=false
        for ordered in "${ORDERED_PACKAGES[@]}"; do
            if [ "$pkg" = "$ordered" ]; then
                skip=true
                break
            fi
        done

        if [ "$skip" = false ]; then
            echo "  → Installing (extra) $pkg"
            python -m pip install -e "$pkg"
        fi
    fi
done

#######################################
# 🧠 Install dev dependencies (root)
#######################################
if [ -f "pyproject.toml" ]; then
    echo ""
    echo "🧪 Installing dev dependencies..."
    python -m pip install -e ".[dev]"
fi

#######################################
# 🧠 Validate imports
#######################################
echo ""
echo "🔍 Validating Python imports..."

check_import() {
    MODULE=$1
    if python -c "import $MODULE" >/dev/null 2>&1; then
        echo "  ✓ $MODULE OK"
    else
        echo "  ❌ $MODULE FAILED"
        exit 1
    fi
}

check_import sdd_core
check_import sdd_wizard
check_import sdd_cli

#######################################
# 🧠 Validate CLI
#######################################
echo ""
echo "🔍 Validating CLI..."

if command -v sdd >/dev/null 2>&1; then
    echo "  ✓ sdd command available"
else
    echo "  ❌ sdd CLI not found"
    exit 1
fi

#######################################
# 🧠 Validate CLI execution
#######################################
echo ""
echo "🔍 Testing CLI..."

if sdd --help >/dev/null 2>&1; then
    echo "  ✓ CLI responding"
else
    echo "  ❌ CLI not responding"
    exit 1
fi

#######################################
# 🧠 Done
#######################################
echo ""
echo "🎉 SDD setup completed successfully!"
echo ""
echo "Next steps:"
echo ""
echo "source .venv/bin/activate"
echo ""
echo "  sdd setup run"
echo "  sdd test run"
echo "  sdd lint run"
echo "  sdd wizard run"