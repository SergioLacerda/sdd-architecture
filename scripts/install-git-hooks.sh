#!/bin/bash
#
# Git Hooks Installer
# 
# Installs all SDD Architecture git hooks from scripts/git-hooks/:
# - pre-commit: Informational ADR-008 guidance
# - pre-push: Full health + governance validation
# - post-merge: Cache warm-up
#
# Usage:
#   bash scripts/install-git-hooks.sh
#

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HOOKS_DIR="$PROJECT_ROOT/.git/hooks"
TEMPLATES_DIR="$PROJECT_ROOT/scripts/git-hooks"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${YELLOW}═════════════════════════════════════════${NC}"
echo -e "${YELLOW}  Git Hooks Installer (SDD Architecture)  ${NC}"
echo -e "${YELLOW}═════════════════════════════════════════${NC}\n"

# Check if .git directory exists
if [ ! -d "$PROJECT_ROOT/.git" ]; then
    echo -e "${RED}✗ Error: Not a git repository${NC}"
    echo "  Current directory: $PROJECT_ROOT"
    echo "  Solution: Initialize git first: git init"
    exit 1
fi

echo -e "${YELLOW}Project root: $PROJECT_ROOT${NC}\n"

# Install each hook
hooks=("pre-commit" "pre-push" "post-merge")
success_count=0
failed_count=0

for hook_name in "${hooks[@]}"; do
    hook_template="$TEMPLATES_DIR/$hook_name"
    hook_target="$HOOKS_DIR/$hook_name"

    if [ ! -f "$hook_template" ]; then
        echo -e "${RED}✗ Hook template not found: $hook_template${NC}"
        failed_count=$((failed_count + 1))
        continue
    fi

    if cp "$hook_template" "$hook_target" && chmod +x "$hook_target"; then
        echo -e "${GREEN}✓ Installed: $hook_name${NC}"
        success_count=$((success_count + 1))
    else
        echo -e "${RED}✗ Failed to install: $hook_name${NC}"
        failed_count=$((failed_count + 1))
    fi
done

echo ""

# Summary
if [ $success_count -eq ${#hooks[@]} ]; then
    echo -e "${GREEN}═════════════════════════════════════════${NC}"
    echo -e "${GREEN}  Installation Successful!                ${NC}"
    echo -e "${GREEN}═════════════════════════════════════════${NC}\n"
    
    echo -e "Installed hooks:"
    echo -e "  \u2713 pre-commit   - Validates governance before commit"
    echo -e "  \u2713 pre-push     - Full health check before push"
    echo -e "  \u2713 post-merge   - Updates cache after merge\n"
    
    echo -e "What happens next:"
    echo -e "  \u2022 git commit    \u2192 Runs pre-commit hook"
    echo -e "  \u2022 git push      \u2192 Runs pre-push hook"
    echo -e "  \u2022 git merge     \u2192 Runs post-merge hook\n"
    
    echo -e "To skip hooks (if absolutely necessary):"
    echo -e "  git commit --no-verify      (skip pre-commit)"
    echo -e "  git push --no-verify        (skip pre-push)"
    echo -e "  git merge --no-verify       (skip post-merge)\n"
    
    echo -e "To uninstall hooks:"
    echo -e "  bash scripts/uninstall-git-hooks.sh\n"
    
    exit 0
else
    echo -e "${YELLOW}═════════════════════════════════════════${NC}"
    echo -e "${YELLOW}  Installation Partial                    ${NC}"
    echo -e "${YELLOW}═════════════════════════════════════════${NC}\n"
    echo -e "Success: $success_count/${#hooks[@]} hooks installed"
    echo -e "Failed: $failed_count/${#hooks[@]} hooks\n"
    echo -e "Check that all hook files exist in .git/hooks/\n"
    exit 1
fi
