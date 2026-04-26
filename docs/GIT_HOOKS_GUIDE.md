# Git Hooks Guide

Complete reference for SDD Architecture git hooks system.

---

## Quick Setup

```bash
# Install all hooks
bash scripts/install-git-hooks.sh

# Verify installation
ls -la .git/hooks/pre-commit .git/hooks/pre-push .git/hooks/post-merge

# Uninstall (if needed)
bash scripts/uninstall-git-hooks.sh
```

---

## Hook Overview

### 🔒 Pre-Commit Hook

**When**: Before each `git commit`  
**What**: Validates governance compliance  
**If fails**: Commit is blocked  
**Skip**: `git commit --no-verify`

**Validation steps**:
1. Health check quick (200ms)
2. Governance compliance
3. Staged files check (JSON validity)

**Example**:
```bash
$ git commit -m "Fix bug"
[PRE-COMMIT] Starting governance validation...
→ Running health check (quick mode)...
✓ Health check passed
→ Validating governance compliance...
✓ Governance compliant
✓ Staged files compliant
[PRE-COMMIT] All checks passed. Commit allowed.
```

### 🚀 Pre-Push Hook

**When**: Before each `git push`  
**What**: Full health and governance validation  
**If fails**: Push is blocked  
**Skip**: `git push --no-verify`

**Validation steps**:
1. Health check full (force recheck, no cache)
2. Enforcement level check
3. Compliance percentage (must be 100%)
4. Summary with commit count

**Example**:
```bash
$ git push origin main
[PRE-PUSH] Starting final validation before push...
→ Running full health check (fresh, no cache)...
✓ Health check passed (10/10)
→ Verifying governance enforcement level...
✓ Enforcement mode: STANDARD
→ Checking compliance percentage...
✓ Fully compliant (100%)
→ Summary for branch 'main':
  Commits to push: 3
  Health: ✓ Healthy
  Governance: ✓ Compliant
  Enforcement: STANDARD
[PRE-PUSH] All checks passed. Push allowed.
```

### 🔄 Post-Merge Hook

**When**: After each `git merge` (successful)  
**What**: Clears stale cache, warms up new state  
**If fails**: Merge succeeds, but cache needs manual refresh  
**Skip**: N/A (runs automatically)

**Actions**:
1. Clear agent state cache
2. Warm up new cache with quick health check

**Example**:
```bash
$ git merge feature/new-feature
[POST-MERGE] Updating governance cache...
✓ Cache cleared
→ Warming up new cache state...
✓ Cache warmed
→ Merged from: feature/new-feature
[POST-MERGE] Cache updated successfully.
```

---

## Installation

### Step 1: Create Hooks

Hooks are already in `.git/hooks/`:
- `.git/hooks/pre-commit`
- `.git/hooks/pre-push`
- `.git/hooks/post-merge`

### Step 2: Install (Make Executable)

```bash
bash scripts/install-git-hooks.sh
```

This script:
1. Checks for .git directory
2. Makes each hook executable (chmod +x)
3. Verifies installation
4. Shows summary

### Step 3: Test

```bash
# Make a small change
echo "# test" >> test.txt

# Try to commit (should validate)
git add test.txt
git commit -m "test"

# Should see pre-commit hook output
```

---

## Validation Failures

### Pre-Commit Failure

**Symptom**:
```bash
$ git commit -m "message"
✗ Health check failed
```

**Fix**:
```bash
# See what's wrong
python3 _core/health_check.py --verbose

# Fix issues
# (Follow the output)

# Retry commit
git commit -m "message"
```

**Or, skip (not recommended)**:
```bash
git commit --no-verify -m "message"
```

### Pre-Push Failure

**Symptom**:
```bash
$ git push origin main
✗ Health check failed (7/10)
```

**Fix**:
```bash
# Force recheck (bypass cache)
python3 _core/health_check.py --force-recheck --verbose

# Fix governance
python3 _core/governance_compliance.py --fix-steps

# Retry push
git push origin main
```

### Post-Merge Failure

**Symptom**:
```bash
$ git merge feature/branch
[POST-MERGE] Updating governance cache...
✗ Cache cleared (but failed to warm up)
```

**Fix** (manual):
```bash
# Force health check to warm cache
python3 _core/health_check.py --force-recheck
```

---

## Skipping Hooks (When Necessary)

### Skip Pre-Commit Only

```bash
git commit --no-verify -m "message"
```

**Use when**:
- Emergency fix needed
- Governance validation is broken
- You're 100% sure the code is safe

**Why careful**: Bypasses governance validation!

### Skip Pre-Push Only

```bash
git push --no-verify origin main
```

**Use when**:
- Final push and health check broken
- CI/CD will catch issues anyway
- You've verified manually

**Why careful**: Pushes potentially broken code!

### Uninstall All Hooks

```bash
bash scripts/uninstall-git-hooks.sh
```

**Use when**:
- Hooks interfere with development
- Using custom hook system
- Troubleshooting hook issues

---

## Advanced Configuration

### Custom Hook Behavior

Edit `.git/hooks/pre-commit` to:

**Option 1: Skip governance (quick commits)**
```bash
# Comment out governance check
# python3 _core/governance_compliance.py --verify
```

**Option 2: Allow partial compliance**
```bash
# Change from "100%" to "80%"
if [[ "$COMPLIANCE" != "80%" ]]; then
    # still fail
fi
```

**Option 3: Add custom checks**
```bash
# After existing checks
echo "→ Running custom validation..."
# Your custom check here
```

---

## Hook State & Cache

### Cache Behavior

- **Pre-commit**: Uses cached health state (30-min TTL)
- **Pre-push**: Forces fresh check `--force-recheck`
- **Post-merge**: Clears cache, warms up new state

### Cache File

```bash
# Location
_core/.sdd/agent_state.json

# Manual clear
rm -f _core/.sdd/agent_state.json

# Force warm-up
python3 _core/health_check.py
```

---

## Integration with CI/CD

### GitHub Actions + Git Hooks

Hooks run locally:
```
developer → git commit → pre-commit hook → GitHub
                            ↓
                      (validates locally)

developer → git push → pre-push hook → GitHub Actions
                          ↓              ↓
                    (validates)      (validates)
```

### Best Practice

1. **Local (git hooks)**: Quick validation before push
2. **CI (GitHub Actions)**: Deep validation before merge
3. **Prod**: Final health check before deploy

---

## Troubleshooting

### Hook Not Running

**Symptom**: No output from hook

**Check**:
```bash
# Verify hook is executable
ls -la .git/hooks/pre-commit

# Should show: -rwxr-xr-x

# If not executable
chmod +x .git/hooks/pre-commit
```

### Hook Not Found

**Symptom**: "Command not found" error

**Cause**: Hook file missing or in wrong location

**Fix**:
```bash
# Check files exist
ls -la .git/hooks/pre-commit
ls -la .git/hooks/pre-push
ls -la .git/hooks/post-merge

# If missing, reinstall
bash scripts/install-git-hooks.sh
```

### Hook Runs Wrong Script

**Symptom**: Hook calls wrong health check

**Check**:
```bash
# View hook content
cat .git/hooks/pre-commit

# Check paths are absolute
# Should use: python3 _core/health_check.py
```

### Slow Hook Execution

**Symptom**: Commit takes 30+ seconds

**Optimize**:
```bash
# Pre-commit uses quick mode (200ms)
# Pre-push uses full validation (up to 1s)

# If still slow, check:
python3 tests/performance/benchmark.py
```

---

## FAQ

### Q: Do I have to use git hooks?
**A**: No, they're optional. Run `bash scripts/uninstall-git-hooks.sh` to disable.

### Q: Will hooks slow down my workflow?
**A**: No, <1s overhead per operation. Pre-commit is <200ms.

### Q: Can I customize hooks?
**A**: Yes, edit `.git/hooks/` files directly. Use with caution.

### Q: What if health check is broken?
**A**: Skip with `--no-verify`, fix health check, reinstall hooks.

### Q: Do hooks run in CI/CD?
**A**: No, only locally. CI/CD uses GitHub Actions workflows.

---

## Next Steps

1. **Install**: `bash scripts/install-git-hooks.sh`
2. **Test**: Make a commit and verify hook runs
3. **Document**: Add hook info to team wiki
4. **Monitor**: Check hook output in logs
5. **Optimize**: Run `python3 tests/performance/benchmark.py` if slow

---

**Last updated**: Phase 5, Step 4  
**Related**: health_check.py, governance_compliance.py, agent_handshake.py
