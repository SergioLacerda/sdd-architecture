#!/bin/bash
# SPEC Pre-commit Hook Setup

# This script installs the SPEC compliance pre-commit hook
# Run this once to set up compliance checking on every commit

HOOK_FILE=".git/hooks/pre-commit"

if [ -f "$HOOK_FILE" ]; then
    echo "⚠️  $HOOK_FILE already exists"
    echo "Backing up to $HOOK_FILE.backup"
    cp "$HOOK_FILE" "$HOOK_FILE.backup"
fi

cat > "$HOOK_FILE" << 'HOOK_CONTENT'
#!/bin/bash
# Pre-commit hook for SPEC compliance validation
# Prevents commits that violate SPEC enforcement rules

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m'

echo -e "${YELLOW}🔍 SPEC Compliance Check (Pre-commit)${NC}"

ERRORS=0

# Rule 1: Check for old paths in CANONICAL/
echo -e "${YELLOW}→ Checking for invalid paths in CANONICAL/${NC}"
if git diff --cached docs/ia/CANONICAL/ 2>/dev/null | grep -E "(docs/specs|/runtime/|/REALITY/|/DEVELOPMENT/)" > /dev/null; then
    echo -e "${RED}❌ ERROR: Invalid paths in CANONICAL/${NC}"
    echo "   Should use: /docs/ia/CANONICAL/ paths"
    echo "   Do not use: /docs/specs/, /runtime/, /REALITY/, /DEVELOPMENT/"
    ERRORS=$((ERRORS + 1))
fi

# Rule 2: Check for project-specific files in CANONICAL/
echo -e "${YELLOW}→ Checking for project-specific files in CANONICAL/${NC}"
if git diff --cached docs/ia/CANONICAL/ 2>/dev/null | grep -E "(rpg-narrative-server|game-master)" > /dev/null; then
    echo -e "${RED}❌ ERROR: Project-specific content in CANONICAL/${NC}"
    echo "   Use [PROJECT_NAME] placeholder for reusability"
    ERRORS=$((ERRORS + 1))
fi

# Rule 3: Warn if modifying ARCHIVE/
echo -e "${YELLOW}→ Checking ARCHIVE/ immutability${NC}"
if git diff --cached docs/ia/ARCHIVE/ --name-only 2>/dev/null | grep -q "."; then
    echo -e "${YELLOW}⚠️  WARNING: ARCHIVE/ changes detected${NC}"
    echo "   ARCHIVE/ should be read-only (only moves allowed)"
fi

# Rule 4: Lint Python files if changed
echo -e "${YELLOW}→ Checking Python syntax${NC}"
PY_FILES=$(git diff --cached --name-only 2>/dev/null | grep "\.py$" || true)
if [ ! -z "$PY_FILES" ]; then
    for file in $PY_FILES; do
        if [ -f "$file" ]; then
            if ! python3 -m py_compile "$file" 2>/dev/null; then
                echo -e "${RED}❌ Python syntax error in $file${NC}"
                ERRORS=$((ERRORS + 1))
            fi
        fi
    done
fi

# Summary
echo ""
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✅ SPEC Compliance Check PASSED${NC}"
    exit 0
else
    echo -e "${RED}❌ SPEC Compliance Check FAILED ($ERRORS errors)${NC}"
    echo "   Fix errors and try again, or use: git commit --no-verify"
    exit 1
fi
HOOK_CONTENT

chmod +x "$HOOK_FILE"
echo "✅ Pre-commit hook installed at $HOOK_FILE"
echo ""
echo "Hook will validate on every commit:"
echo "  • CANONICAL/ has valid paths"
echo "  • No project names in CANONICAL/"
echo "  • ARCHIVE/ not modified"
echo "  • Python files have valid syntax"
