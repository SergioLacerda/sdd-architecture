# Compliance Automation Setup Guide

**Status:** ✅ Implemented  
**Date:** 2026-04-19

---

## 📋 Overview

Three layers of compliance automation have been implemented to enforce SPEC governance rules:

1. **Pre-commit Hook** — Local validation before commits
2. **Pytest Tests** — CI/CD validation during merge
3. **GitHub Actions** — Automated enforcement gates

---

## 🔧 Setup Instructions

### Step 1: Install Pre-commit Hook (Local)

```bash
# From project root
bash scripts/setup-precommit-hook.sh

# Or manually:
mkdir -p .git/hooks
chmod +x scripts/setup-precommit-hook.sh
cp scripts/setup-precommit-hook.sh .git/hooks/pre-commit
```

**What it validates:**
- ✅ No invalid paths in CANONICAL/ (/runtime/, /specs/, etc.)
- ✅ No project-specific names in CANONICAL/ (use [PROJECT_NAME])
- ✅ ARCHIVE/ not modified (read-only)
- ✅ Python syntax valid

**How it works:**
- Runs automatically before every commit
- Blocks commit if violations found
- Override with: `git commit --no-verify` (not recommended)

---

### Step 2: Run Pytest Compliance Tests (Local)

```bash
# Run all SPEC compliance tests
pytest tests/architecture/test_spec_compliance.py -v

# Run specific test
pytest tests/architecture/test_spec_compliance.py::test_canonical_paths_valid -v

# Run with detailed output
pytest tests/architecture/test_spec_compliance.py -vv -s
```

**Test Rules:**
- `test_canonical_paths_valid` — Rule 1: Valid paths
- `test_no_project_names_in_canonical` — Rule 2: No project names
- `test_canonical_identical_across_projects` — Rule 3: Identical CANONICAL/
- `test_custom_folders_structure` — Rule 4: custom/ structure
- `test_enforcement_rules_documented` — Rule 5: Enforcement docs
- `test_spec_compliance_summary` — All rules combined

---

### Step 3: GitHub Actions Workflow (Automatic)

Workflow file: `.github/workflows/spec-enforcement.yml`

**Triggers:**
- On every pull request (if docs/ia/ changed)
- On push to main (if docs/ia/ changed)

**Jobs:**
1. `spec-compliance` — Runs pytest tests
2. `canonical-path-validation` — Checks paths
3. `no-project-names-in-canonical` — Checks names
4. `archive-immutability` — Checks ARCHIVE/ read-only
5. `custom-isolation` — Checks folder isolation
6. `enforcement-documentation` — Checks ENFORCEMENT_RULES.md

**How to view results:**
```bash
# On GitHub:
# Go to repo → Pull Requests → Your PR → Checks tab

# Or in terminal:
gh pr checks <PR_NUMBER>
```

---

## 📊 Compliance Rules Enforced

### Rule 1: CANONICAL/ Paths Must Be Valid
**Pattern:** Paths must start with `/EXECUTION/spec/CANONICAL/`

**Invalid:**
- `/runtime/execution_state.md` ❌
- `/docs/specs/architecture.md` ❌
- `specs/` ❌

**Valid:**
- `/EXECUTION/spec/CANONICAL/specifications/architecture.md` ✅
- `/EXECUTION/spec/CANONICAL/rules/ia-rules.md` ✅

### Rule 2: No Project-Specific Names in CANONICAL/
**Reason:** CANONICAL/ must be reusable across all projects

**Invalid:**
- "rpg-narrative-server integration" ❌
- "game-master-api specific" ❌

**Valid:**
- "[PROJECT_NAME] integration" ✅
- "Each project should" ✅

### Rule 3: CANONICAL/ Identical Across Projects
**Reason:** Ensures 100% reuse and consistency

**Check:** If multiple projects exist, their CANONICAL/ must be identical

### Rule 4: custom/ Folders Must Have Structure
**Required structure:**
```
custom/[PROJECT_NAME]/
├── README.md
├── INTEGRATION_RESULTS.md
├── development/
│   ├── execution-state/
│   ├── checkpoints/
│   └── ...
└── reality/
    ├── current-system-state/
    ├── limitations/
    └── observations/
```

### Rule 5: Enforcement Rules Must Be Documented
**File:** `/EXECUTION/spec/CANONICAL/rules/ENFORCEMENT_RULES.md`

**Required sections:**
- Pre-commit Hook
- Architecture Tests
- CI/CD Gates
- Manual Review

---

## 🔍 Interpreting Results

### Pre-commit Hook Success
```
✅ SPEC Compliance Check PASSED
```

### Pre-commit Hook Failure
```
❌ ERROR: Invalid paths in CANONICAL/
   Should use: /EXECUTION/spec/CANONICAL/ paths
   Do not use: /docs/specs/, /runtime/, /REALITY/, /DEVELOPMENT/
```

**Fix:**
1. Edit the file to use correct paths
2. Stage changes: `git add docs/ia/CANONICAL/...`
3. Commit again

### Pytest Test Failure
```
FAILED tests/architecture/test_spec_compliance.py::test_canonical_paths_valid
ERROR: Invalid paths found in CANONICAL/:
  /EXECUTION/spec/CANONICAL/rules/ia-rules.md:15 - Invalid path '/runtime/' 
    → Should be /docs/ia/custom/[PROJECT]/development/
```

**Fix:**
1. Identify file and line from error
2. Replace invalid path
3. Re-run: `pytest tests/architecture/test_spec_compliance.py`

### GitHub Actions Failure
```
❌ Canonical path validation failed
   Check logs at: https://github.com/.../actions/runs/...
```

**Fix:**
1. Click "Details" link to see full logs
2. Fix issues locally
3. Push again

---

## 🚀 Workflow Examples

### Scenario 1: Adding New Spec

**Goal:** Add `/EXECUTION/spec/CANONICAL/specifications/observability.md`

```bash
# 1. Create file
touch docs/ia/CANONICAL/specifications/observability.md

# 2. Add valid paths in file
# Good: references /EXECUTION/spec/CANONICAL/...
# Bad: references /specs/... or /runtime/...

# 3. Stage changes
git add docs/ia/CANONICAL/specifications/observability.md

# 4. Commit (pre-commit hook runs automatically)
git commit -m "Add observability specification"

# 5. If hook fails:
#    - Fix paths in file
#    - Stage again: git add ...
#    - Retry commit
```

### Scenario 2: Specializing for Project

**Goal:** Document `custom/rpg-narrative-server/` state

```bash
# 1. Update custom/rpg-narrative-server/reality/
nano docs/ia/custom/rpg-narrative-server/reality/current-system-state/services.md

# 2. Stage changes (CANONICAL/ untouched)
git add docs/ia/custom/rpg-narrative-server/reality/

# 3. Commit
git commit -m "Update RPG server state documentation"

# 4. Pre-commit hook checks:
#    ✓ Not modifying CANONICAL/
#    ✓ Not adding project names to CANONICAL/
#    ✓ custom/ isolation OK
```

### Scenario 3: CI/CD Gate Failure

**Goal:** Push to PR, gate fails

```bash
# 1. Make changes locally
# 2. Commit and push
git push origin feature-branch

# 3. GitHub Actions workflow runs automatically
# 4. Check status at: https://github.com/.../pull/...

# If gate fails:
# - Read error message
# - Fix locally
# - Commit and push again
# - Gate re-runs automatically
```

---

## 📈 Monitoring Compliance

### Check Local Compliance
```bash
# Run all tests
pytest tests/architecture/test_spec_compliance.py -v

# Check individual rule
pytest tests/architecture/test_spec_compliance.py::test_canonical_paths_valid -v
```

### Check Project Compliance History
```bash
# See all SPEC-related commits
git log --oneline --grep="SPEC\|compliance\|CANONICAL" -- docs/ia/

# See who violated rules (and fixed them)
git log --oneline -- docs/ia/CANONICAL/rules/

# See enforcement gate results
gh run list -w spec-enforcement.yml
```

### Generate Compliance Report
```bash
# Run all tests and generate report
pytest tests/architecture/test_spec_compliance.py -v --tb=short > compliance_report.txt

# Open report
cat compliance_report.txt
```

---

## 🛠️ Troubleshooting

### Pre-commit Hook Not Running

**Symptom:** Commit succeeds even with invalid paths

**Cause:** Hook not installed or not executable

**Fix:**
```bash
# Check hook exists
ls -la .git/hooks/pre-commit

# Make executable
chmod +x .git/hooks/pre-commit

# Re-install if needed
bash scripts/setup-precommit-hook.sh
```

### Pytest Tests Not Found

**Symptom:** `ModuleNotFoundError: No module named 'tests'`

**Fix:**
```bash
# Ensure pytest is installed
pip install pytest

# Run from project root
cd /path/to/project
pytest tests/architecture/test_spec_compliance.py -v
```

### GitHub Actions Not Triggered

**Symptom:** Workflow doesn't run on PR

**Cause:** Workflow file syntax error or not on main branch

**Fix:**
1. Check workflow file syntax: `.github/workflows/spec-enforcement.yml`
2. Ensure file has valid YAML
3. Push to branch and create PR
4. Check Actions tab for errors

---

## 📝 Best Practices

1. **Always commit with pre-commit hook enabled**
   - Catches violations early
   - Prevents bad commits

2. **Run tests before pushing**
   ```bash
   pytest tests/architecture/test_spec_compliance.py
   ```

3. **Review compliance errors carefully**
   - Don't bypass (--no-verify) without understanding

4. **Update ENFORCEMENT_RULES.md when adding new rules**
   - Keeps documentation in sync with automation

5. **Monitor GitHub Actions**
   - Check that gates are passing
   - Review failed checks promptly

---

## 📞 Support

**Question:** What if I need to bypass a rule?

**Answer:** Use `git commit --no-verify` ONLY with explicit approval. Add explanation to commit message.

**Question:** How to disable specific test?

**Answer:** Edit `tests/architecture/test_spec_compliance.py` and modify the test (not recommended).

**Question:** How to update rules?

**Answer:** 
1. Update enforcement logic in `tests/architecture/test_spec_compliance.py`
2. Update `.github/workflows/spec-enforcement.yml`
3. Document in `/EXECUTION/spec/CANONICAL/rules/ENFORCEMENT_RULES.md`

---

**Framework:** SPEC v1.0  
**Compliance Level:** Automated + Manual  
**Status:** ✅ Production-Ready
