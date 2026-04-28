#!/usr/bin/env bash
set -euo pipefail

echo "🚀 SDD Test Pipeline"
echo "===================="

FAILED=0

# 🧠 Detect Python
if command -v python3 >/dev/null 2>&1; then
    PYTHON=python3
elif command -v python >/dev/null 2>&1; then
    PYTHON=python
else
    echo "❌ Python not found"
    exit 1
fi

echo "✓ Using Python: $PYTHON"

# 🧠 Activate venv
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
elif [ -f ".venv/Scripts/activate" ]; then
    source .venv/Scripts/activate
else
    echo "⚠️  Virtualenv not found, running without it"
fi

run() {
    echo ""
    echo "▶ $1"
    if ! eval "$2"; then
        echo "❌ FAILED: $1"
        FAILED=1
    else
        echo "✅ OK: $1"
    fi
}

# 🧪 UNIT
if [ -d "tests/unit" ]; then
    run "Unit tests" "pytest tests/unit -q"
fi

# 🔗 INTEGRATION
if [ -d "tests/integration" ]; then
    run "Integration tests" "pytest tests/integration -q"
fi

# 🌍 E2E
if [ -d "tests/e2e" ]; then
    run "E2E tests" "pytest tests/e2e -q"
fi

# 📦 PACKAGE TESTS (auto-detect)
for pkg in sdd-*; do
    if [ -d "$pkg/tests" ]; then
        run "Package tests: $pkg" "pytest $pkg/tests -q"
    fi
done

# 🧠 ARCHITECTURE VALIDATION
if [ -f "tools/architecture/validate_imports.py" ]; then
    run "AST Architecture" "$PYTHON tools/architecture/validate_imports.py"
fi

# 📊 ARCHITECTURE SCORE
if [ -f "tools/architecture/score.py" ]; then
    run "Architecture Score" "$PYTHON tools/architecture/score.py"
fi

echo ""
if [ "$FAILED" -eq 0 ]; then
    echo "🎉 ALL CHECKS PASSED"
    exit 0
else
    echo "💥 FAILURES DETECTED"
    exit 1
fi