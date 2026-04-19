# 🚨 EMERGENCY PROCEDURE — CI/CD Gate Failure

**When All PRs Are Blocked by Spec Enforcement**

---

## 🚨 Symptom

**All PRs fail spec-enforcement gate:**

```
❌ spec-enforcement job failed
   CI/CD Check: Spec validation failed
   Exit code: 1
   
   All PRs blocked, even valid ones
```

**Real examples:**
```bash
❌ Your PR: "fix: typo in README"
   Reason: "File outside allowed path"
   But: README.md is allowed!

❌ Your PR: "docs: Update architecture"
   Reason: "validate-ia-first.py crashed"
   But: Script never ran successfully
```

**Impact:** Entire team blocked. No PRs can merge.

---

## ⏱️ IMMEDIATE TRIAGE (5 minutes)

### Step 1: Check CI/CD Logs

```bash
# Go to GitHub Actions (or your CI/CD):
# https://github.com/user/repo/actions

# Find the failing spec-enforcement job
# Click on it → View details

# Read the error message carefully:
# ├─ Is it syntax error?
# ├─ Is it validation rule violation?
# ├─ Is it runtime crash?
# └─ Is it environment issue?
```

### Step 2: Determine If Flaky (Intermittent)

```bash
# Look at job history
# Did it pass 5 minutes ago?
# Did it fail 5 times in a row?

# If passes/fails randomly → FLAKY TEST
# If fails consistently → REAL ISSUE
```

### Step 3: Classify Issue Type

**Type A: Flaky (Intermittent Failure)**
```
→ Solution: Re-run the job (see below)
```

**Type B: Real Breach (Consistent Failure)**
```
→ Solution: Fix the actual issue or bypass (see below)
```

**Type C: Script Broken**
```
→ Solution: Hotfix the script or disable gate (see below)
```

---

## 🔧 IF FLAKY (Re-Run & Continue)

**Intermittent failures are normal CI/CD behavior:**

```bash
# GitHub UI:
# 1. Go to failing job
# 2. Click "Re-run job" button
# 3. Wait for job to complete

# Expected outcome:
# ✅ Job passes on retry → Problem solved (flaky)
#    Just re-run before merging if it fails again

# 📝 Document:
# Add comment to PR: "Flaky test - re-ran successfully"
```

---

## 🔧 IF REAL BREACH (Fix or Bypass)

### Option A: Fix the Actual Issue (Recommended)

```bash
# Example: Path validation failure
# Error: "docs/ia/custom/my-project/ not allowed"
# Fix: Move file to allowed location, or update config

# Steps:
1. Identify what violated the rule
2. Fix the PR to comply
3. Push fix
4. Re-run job

# Example:
git mv docs/ia/custom/my-project/BAD_LOCATION.md /EXECUTION/spec/CANONICAL/
git commit -m "fix: Move doc to allowed location"
git push
```

### Option B: Verify Change Is Actually Valid

```bash
# Maybe the rule is wrong, or exception applies

# Step 1: Read spec-enforcement rules
cat .github/workflows/spec-enforcement.yml

# Step 2: Check if exception documented
grep -r "exception\|allow\|bypass" /EXECUTION/spec/CANONICAL/rules/

# Step 3: If valid exception exists:
# Add flag to PR or request maintainer approval

# Step 4: Contact repo maintainer
# "This change is valid per ADR-X, but gate blocked it"
```

---

## 🚨 IF SCRIPT BROKEN (Emergency Bypass)

**If spec-enforcement job crashes:**

```bash
# You'll see:
# ❌ spec-enforcement job error
#    Traceback: ...
#    Script crashed, not rule violation
```

**Immediate action:**

### Path 1: Hotfix the Script (5-15 min)

```bash
# Identify which script crashed:
# └─ Is it validate-ia-first.py?
# └─ Is it setup-wizard.py?
# └─ Is it generate-specializations.py?

# Quick fix:
1. Clone/checkout script
2. Find the bug (syntax error, import missing, etc.)
3. Fix it
4. Test locally: python script.py --test
5. Commit fix: git commit -m "fix: Script crash in CI/CD"
6. Push
7. Re-run job
```

### Path 2: Emergency Bypass (As Last Resort)

```bash
# If script fix takes >30 minutes:

# Temporarily disable the failing job:
# In: .github/workflows/spec-enforcement.yml
# Change:  if: true
# To:      if: false
#
# Commit: git commit -m "EMERGENCY: Disable spec-enforcement job due to crash"
# Push
# Now PRs can merge

# ⚠️ YOU MUST:
# 1. File urgent issue: "Script broken in CI/CD"
# 2. Fix script immediately
# 3. Re-enable job: git commit -m "fix: Re-enable spec-enforcement after fix"
# 4. Verify: Run job manually, confirm it passes
```

---

## 📊 GATE FAILURE DECISION TREE

```
CI/CD Gate Failure
│
├─ Job passes on re-run?
│  ├─ YES → Flaky test, just re-run before merge
│  └─ NO → Go to next
│
├─ Script crashes (traceback)?
│  ├─ YES → Go to "SCRIPT BROKEN" section
│  └─ NO → Go to next
│
├─ Rule violation?
│  ├─ Is it legit breach?
│  │  ├─ YES → Fix PR to comply with rule
│  │  └─ NO → Go to next
│  │
│  └─ Is there documented exception?
│     ├─ YES → Request exception approval
│     └─ NO → Fix PR or file issue to adjust rule
│
└─ Unknown error?
   └─ Contact repo maintainer with full logs
```

---

## ✅ VERIFICATION

**After resolving, verify gate passes:**

```bash
# Run locally:
python docs/ia/SCRIPTS/validate-ia-first.py --audit docs/ia

# Or wait for:
✅ spec-enforcement job passed

# Only then merge PR
```

---

## 📋 PREVENTION

**To prevent gate failures:**

1. **Test locally before committing**
   ```bash
   python docs/ia/SCRIPTS/validate-ia-first.py --audit docs/ia/
   ```

2. **Run spec tests in feature branch**
   ```bash
   git checkout -b test-spec
   [make changes]
   # Wait for CI/CD to pass
   # If passes: merge to main
   # If fails: investigate before merging
   ```

3. **Monitor job health**
   - Are jobs consistently flaky?
   - Are failures increasing?
   - Report to repo maintainer

---

## 🔗 RELATED

- [spec-enforcement.yml](.github/workflows/spec-enforcement.yml)
- [validate-ia-first.py](../../SCRIPTS/validate-ia-first.py)
- [IA_FIRST_SPECIFICATION.md](../../IA_FIRST_SPECIFICATION.md)

---

**Recovery Time:** 2-30 minutes  
**Severity:** 🔴 CRITICAL (blocks all PRs)  
**Frequency:** Rare (should not happen if well-maintained)
