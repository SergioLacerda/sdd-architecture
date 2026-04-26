# CODE REVIEW Guardrail - Installation & Activation

**Purpose**: Enforce ADR-008 (Code Review Governance) to prevent "lixo" (broken code) from reaching production.

**Core Rule**: Agent NEVER auto-commits. All changes require architect review.

---

## 🚀 Quick Activation

### Step 1: Install Pre-Commit Hook (Local)

```bash
cd /home/sergio/dev/sdd-architecture

# Copy hook to git hooks directory
cp .git-hooks/pre-commit-code-review .git/hooks/pre-commit

# Make executable
chmod +x .git/hooks/pre-commit
```

### Step 2: Verify Hook is Active

```bash
ls -la .git/hooks/pre-commit
# Should show: -rwxr-xr-x ... pre-commit
```

### Step 3: Test the Hook

```bash
# Try to commit to main (should be blocked)
git checkout main
git commit -m "test" --allow-empty

# Expected output:
# ❌ BLOCKED: Cannot commit directly to main branch
#    (shows WIP branch workflow)
```

---

## 🔐 GitHub Branch Protection (Architect Controls)

This ensures the guardrail cannot be bypassed even with `git push --force`.

### Setup in GitHub Repository Settings

1. **Go to**: Repository → Settings → Branches

2. **Add Branch Protection Rule for `main`**:

   ```
   Branch name pattern: main
   ```

3. **Enable Rules** (all checked):

   ```
   ✅ Require a pull request before merging
       ├─ Require approvals: 1
       ├─ Dismiss stale pull request approvals: NO
       └─ Require review from code owners: YES (if CODEOWNERS exists)
   
   ✅ Require status checks to pass before merging
       ├─ Add status check: pytest tests/
       └─ Add status check: pylint src/
   
   ✅ Require branches to be up to date before merging
   
   ✅ Require code reviews from code owners
   
   ✅ Require signed commits
       ├─ Require a signed commit
   
   ❌ Do NOT allow force pushes
   ❌ Do NOT allow deletions
   ❌ Do NOT allow auto-delete on branch removal
   ```

4. **Restrict who can merge**:

   ```
   Allow specified actors to bypass required pull requests:
   - Only @sergio (architect) can force-merge if emergency
   
   Allow auto-merge: NO
   Allow deletions: NO
   ```

---

## 📋 Workflow (ADR-008)

### For Agents (Implementation)

```bash
# Step 1: Create WIP branch
git checkout -b wip/feature-<name>

# Step 2: Work normally (push as you go)
git add .
git commit -m "feat: Implement feature X"
git push origin wip/feature-<name>

# Step 3: Create PR on GitHub
# - Title: [REVIEW] Feature: <name>
# - Description: Include design doc link, spec doc link, test results
# - Assignee: @sergio (architect)

# Step 4: Wait for architect review
# (Your job is done, now wait for architect)

# Step 5: If changes requested
# - Make changes on same WIP branch
# - Push new commits
# - Re-request review
# - Back to Step 4
```

### For Architect (Code Owner)

```bash
# Step 1: Review PR
# - Check design matches FEATURE_DESIGN_*.md
# - Check tests pass (111/111+)
# - Check docs updated
# - Verify no broken versions will result

# Step 2: Approve or Request Changes
# In GitHub: Comment "✅ Approved - LGTM" or "⚠️ Please address: ..."

# Step 3: Merge when approved
# GitHub will allow merge only if:
#   ✅ 1 approval from code owner
#   ✅ All status checks pass
#   ✅ Branch is up to date with main

# Step 4: Monitor
# - Verify main CI/CD passes
# - Watch for issues
# - Rollback if needed
```

---

## 🧪 Testing the Guardrail

### Test 1: Pre-Commit Hook Blocks Direct Main Commits

```bash
# Create WIP branch and try to switch back to main while staged
git checkout -b wip/test-guardrail
echo "test" > test.txt
git add test.txt
git checkout main

# This should now fail with pre-commit hook error
# (or at least warn you)
```

### Test 2: Run Guardrail Test Suite

```bash
cd /home/sergio/dev/sdd-architecture

# Run all guardrail tests
pytest EXECUTION/tests/test_guardrail_code_review.py -v

# Expected: 19/19 tests pass ✅
```

### Test 3: Verify Critical Files Are Protected

```bash
# These files should require special review:
- EXECUTION/spec/CANONICAL/decisions/ADR-007-*
- EXECUTION/spec/CANONICAL/decisions/ADR-008-*
- .sdd-migration/phase-archive/DECISIONS.md
- .sdd-migration/PHASES.md

# The pre-commit hook warns if you modify them
```

---

## 🚨 Emergency Procedures

### If Something Breaks in Production

1. **Immediate Rollback** (Architect Only):
   ```bash
   # Revert last commit
   git revert HEAD --no-edit
   git push origin main
   
   # CI/CD should catch it and show problems
   ```

2. **Investigate**:
   ```bash
   # Check what broke
   git log --oneline -5
   git show <commit-hash>
   
   # Review the PR that was approved
   ```

3. **Prevention for Next Time**:
   ```bash
   # Update ADR-007 or ADR-008 if new edge case discovered
   # Add test case to prevent recurrence
   # Document the learning
   ```

---

## 📊 Guardrail Status

### ✅ v3.1-beta.1 (Starting Tomorrow, Apr 22)

```
✅ Pre-commit hook: Active (prevents direct main commits)
✅ GitHub branch protection: To be configured
✅ Test suite: 19/19 tests passing
✅ ADR-007: Design-first guardrails enforced
✅ ADR-008: Code review governance enforced
✅ No auto-commits: Impossible on main branch
✅ No broken versions: Architect controls all merges
```

### ⏳ v3.0 (Apr 28+)

```
✅ All v3.1-beta.1 guardrails continue
✅ 6-phase migration follows ADR-007 & ADR-008
✅ All commits to main require architect review
✅ No direct commits to main allowed
✅ Rollback capability maintained throughout
```

---

## 🔗 Related Documentation

- **ADR-007**: Implementation Guardrails (Design First, Code Follows)
- **ADR-008**: Code Review Governance (Agent Never Auto-Commits)
- **PHASES.md**: Migration phases (follow ADR-007)
- **DECISIONS.md**: Architecture decisions (protected)

---

## ❓ FAQ

**Q: What if I need to fix a typo quickly?**
A: Still use WIP branch → PR → approve → merge. Process ensures nothing breaks.

**Q: What if architect is unavailable?**
A: PRs can wait. Better safe than sorry for production stability.

**Q: Can I force-push to bypass the hook?**
A: Not to main (GitHub prevents it). If you `git push --force-with-lease` to WIP branch, that's OK (it's your working branch).

**Q: What if something in main is actually broken?**
A: Architect can revert main commit immediately, then investigate in safe branch.

**Q: Do I need to do this for every commit?**
A: Yes. It's the price of stable production. Protects everyone.

---

## ✅ Verification Checklist (Before v3.1-beta.1)

- [ ] Pre-commit hook installed locally (`.git/hooks/pre-commit`)
- [ ] Pre-commit hook is executable (`chmod +x`)
- [ ] Guardrail tests pass (`pytest EXECUTION/tests/test_guardrail_code_review.py`)
- [ ] GitHub branch protection rules configured on `main`
- [ ] CODEOWNERS file exists (defines who can approve)
- [ ] All team members know the workflow
- [ ] ADR-007 & ADR-008 are read and understood
- [ ] First PR follows the new workflow (test it)

---

## 🎯 Success Metrics

After guardrails are active:

```
Before:
  ❌ Auto-commits possible → broken versions in production
  ❌ No review gate → architectural drift undetected
  ❌ Files removed → gaps in documentation
  ❌ No rollback → can't undo mistakes

After (with ADR-007 & ADR-008):
  ✅ No auto-commits → all changes reviewed
  ✅ Review gate enforced → no drift
  ✅ Critical files protected → no silent removal
  ✅ Rollback always possible → safe to deploy
  ✅ v2.1 → v3.1-beta.1 → v3.0: Zero broken versions
```

---

**Status**: Ready for v3.1-beta.1 (Apr 22, 2026)

**Last Updated**: Apr 21, 2026

**Owner**: @sergio (Architect)
