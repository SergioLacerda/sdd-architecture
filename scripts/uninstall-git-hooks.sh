#!/bin/bash
#
# Git Hooks Uninstaller
#
# Removes all SDD Architecture git hooks
#
# Usage:
#   bash scripts/uninstall-git-hooks.sh
#

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HOOKS_DIR="$PROJECT_ROOT/.git/hooks"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${YELLOW}Git Hooks Uninstaller${NC}\n"

# Check if .git directory exists
if [ ! -d "$PROJECT_ROOT/.git" ]; then
    echo -e "${RED}✗ Error: Not a git repository${NC}"
    exit 1
fi

# Remove each hook
hooks=("pre-commit" "pre-push" "post-merge")
removed_count=0

for hook_name in "${hooks[@]}"; do
    hook_file="$HOOKS_DIR/$hook_name"
    
    if [ -f "$hook_file" ]; then
        rm -f "$hook_file"
        echo -e "${GREEN}✓ Removed: $hook_name${NC}"
        removed_count=$((removed_count + 1))
    fi
done

echo ""
echo -e "${GREEN}Uninstallation complete!${NC}"
echo "Removed $removed_count hooks"
echo ""
echo "You can now:"
echo "  git commit    without pre-commit validation"
echo "  git push      without pre-push validation"
echo "  git merge     without post-merge cache update"
