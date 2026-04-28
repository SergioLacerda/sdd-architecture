# Cutover: v2.1 → v3.0 (Final Steps)

⚠️ **CRITICAL: Follow these steps exactly. No improvisation.**

---

## Pre-cutover Validation

Run these checks BEFORE any cutover steps:

```bash
# 1. Ensure all tests pass
pytest .sdd-migration/tests/ -v
# Expected: All pass ✅

# 2. Ensure output files exist
ls -la .sdd-migration/output/mandate.spec
ls -la .sdd-migration/output/guidelines.dsl
# Expected: Files exist, not empty

# 3. Ensure git working tree is clean
git status
# Expected: "working tree clean" (no uncommitted changes)

# 4. Ensure you're on main branch
git branch | grep "*"
# Expected: "* main"
```

If any check fails: **STOP. Do not proceed.**

---

## Cutover Steps (Manual)

### Step 1: Create .sdd-core/ directory

```bash
mkdir -p .sdd-core/CANONICAL
mkdir -p .sdd-guidelines
```

### Step 2: Copy migrated files

```bash
# Copy mandate spec
cp .sdd-migration/output/mandate.spec .sdd-core/CANONICAL/mandate.spec

# Copy guidelines
cp .sdd-migration/output/guidelines.dsl .sdd-guidelines/guidelines.dsl

# Copy schemas (reference)
cp .sdd-migration/output/*.schema.json .sdd-core/CANONICAL/ 2>/dev/null || true
```

### Step 3: Verify copied files

```bash
ls -la .sdd-core/CANONICAL/mandate.spec
ls -la .sdd-guidelines/guidelines.dsl

# Quick sanity check (files not empty)
wc -l .sdd-core/CANONICAL/mandate.spec
wc -l .sdd-guidelines/guidelines.dsl
```

### Step 4: Delete v2.1 structure

```bash
# BACKUP: Create marker before deletion
touch .sdd-migration/CUTOVER_BACKUP_$(date +%s)

# Delete legacy files (after backup)
rm -rf EXECUTION/spec/CANONICAL/rules/
rm -rf context/
```

### Step 5: Create v3.0 marker files

```bash
# Create metadata
cat > .sdd-metadata.json << 'EOF'
{
  "version": "3.0",
  "tier": "lite",
  "format": "msgpack-v1",
  "compiled": {
    "hash": "placeholder-computed-at-first-compile",
    "timestamp": "$(date -Iseconds)"
  },
  "migrated_from": "v2.1",
  "migration_date": "$(date)"
}
EOF

# Create README
cat > README-SDD-v3.0.md << 'EOF'
# SDD v3.0 (Migrated from v2.1)

This is SDD v3.0 - the refactored, production-ready architecture.

See `.sdd/` for full structure.
EOF
```

### Step 6: Git status check

```bash
git status

# Expected output should show:
# - New files: .sdd-core/CANONICAL/mandate.spec, etc
# - Deleted files: EXECUTION/spec/CANONICAL/rules/..., etc
# - No untracked files
```

### Step 7: Git add changes

```bash
git add .sdd-core/
git add .sdd-guidelines/
git add .sdd-metadata.json
git add README-SDD-v3.0.md

# Remove deleted files
git add -u
```

### Step 8: Review changes

```bash
git diff --cached --stat
# Should show mandate.spec, guidelines.dsl added, old files removed
```

### Step 9: Commit (single logical change)

```bash
git commit -m "v3.0: Migrate from v2.1 (staged rewrite)

This commit consolidates 9 months of v2.1 development into v3.0:

Content migrated:
  - MANDATE: 15 principles (EXECUTION/spec/CANONICAL/rules/ → .sdd-core/)
  - GUIDELINES: 10+ patterns (EXECUTION/spec/guides/ → .sdd-guidelines/)

Migration process:
  1. Extracted v2.1 content with tooling (.sdd-migration/tooling/)
  2. Validated parity (tests confirm no data loss)
  3. Converted to v3.0 DSL format
  4. Moved to .sdd-core/CANONICAL/ (new home)
  5. Cleaned up v2.1 structure

Testing:
  - All extraction tests pass
  - All validation tests pass
  - Agent loader compatible

Structure changes:
  - v2.1: Distributed (EXECUTION/spec/)
  - v3.0: Centralized (.sdd/)
  - v2.1: JSON / Markdown
  - v3.0: DSL / Compiled binary

Breaking changes: None (API unchanged)

Migration tool: .sdd-migration/tooling/migrate.py
Audit trail: .sdd-migration/reports/
"
```

### Step 10: Tag release

```bash
git tag v3.0.0 -m "v3.0.0 Release

- Centralized .sdd/ structure
- Wizard-driven setup
- Binary compiled MANDATE/GUIDELINES
- RTK telemetry deduplication
- Framework-ready OPERATIONS layer
"
```

### Step 11: Verify

```bash
# Check tag created
git tag -l v3.0.0

# Check log shows migration commit
git log --oneline -5

# Check structure in place
ls -la .sdd-core/CANONICAL/
ls -la .sdd-guidelines/
```

---

## Post-cutover Cleanup

### Option A: Keep .sdd-migration/ (for audit trail)

```bash
# Mark as "completed"
touch .sdd-migration/COMPLETED_$(date +%Y%m%d)

# Git ignore the output (already been moved)
echo ".sdd-migration/output/" >> .gitignore
git add .gitignore
git commit -m "chore: mark migration completed"
```

### Option B: Remove .sdd-migration/ (clean slate)

```bash
rm -rf .sdd-migration/
git rm -r .sdd-migration/
git commit -m "chore: remove migration tooling (completed)"
```

**Recommendation:** Keep for 2-3 weeks (audit trail), then remove.

---

## Validation Post-cutover

```bash
# Ensure .sdd-core/ is readable
ls .sdd-core/CANONICAL/
# Output: mandate.spec, guidelines.spec, (others)

# Ensure .sdd-guidelines/ is readable
ls .sdd-guidelines/
# Output: guidelines.dsl

# Ensure agent can load (test runner)
pytest tests/agents/test_loader_v3.py -v
# Should pass without errors

# Ensure git history is clean
git log --oneline --graph -10
# Should show linear history, migration commit clear
```

---

## Rollback (if needed, before push)

If something went wrong:

```bash
# Undo the commit (keep changes)
git reset --soft HEAD~1

# Review what went wrong
git status

# If needed, undo file deletions
git checkout EXECUTION/spec/  (restore v2.1)

# Start over or investigate
```

---

## Push to Remote

Once validated locally and ready:

```bash
# Push main + tag
git push origin main
git push origin v3.0.0

# GitHub: Create release from tag
# - Use RELEASE_v3.0.md as release notes
# - Link to MIGRATION_v2_to_v3.md for community

# Announce
```

---

## Success Indicators

- ✅ .sdd-core/CANONICAL/ exists with mandate.spec
- ✅ .sdd-guidelines/ exists with guidelines.dsl
- ✅ v2.1 structure removed (EXECUTION/spec/CANONICAL/rules/)
- ✅ Git tag v3.0.0 created
- ✅ git log shows migration commit
- ✅ Agent loader passes tests
- ✅ Team notified

**You're done!**

---

## Troubleshooting

**Q: Files didn't copy correctly?**
A: Check paths, re-run steps 2-3, verify with `ls -la`

**Q: Git commit failed?**
A: Check `git status`, ensure all changes staged, try again

**Q: Tag didn't create?**
A: Check tag exists: `git tag -l v3.0.0`, or create again: `git tag v3.0.0`

**Q: Something went very wrong?**
A: Revert: `git reset --hard HEAD~1`, investigate, try again

**Q: Need audit trail of what changed?**
A: Check `.sdd-migration/reports/` or `git show v3.0.0`
