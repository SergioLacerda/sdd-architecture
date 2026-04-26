# 🚨 EMERGENCY PROCEDURE — Pre-Commit Hook Failure

**When All Commits Are Blocked**

---

## 🚨 Symptom

**You cannot commit anything:**
```bash
$ git commit -m "fix: bug"

Pre-commit hook error:
  Traceback (most recent call last):
    File "docs/ia/SCRIPTS/validate-ia-first.py", line ...
  
  Exit code: 1
  ❌ COMMIT ABORTED
```

**Impact:** Entire development team blocked. No one can commit.

---

## ⏱️ IMMEDIATE RECOVERY (2 minutes)

### Step 1: Check Hook Status
```bash
# Verify pre-commit hook exists and is executable
cat .git/hooks/pre-commit
ls -la .git/hooks/pre-commit

# Expected: File exists, is executable (-rwxr-xr-x)
# If missing or corrupt: Reinstall (see below)
```

### Step 2: Diagnose Root Cause
```bash
# Option A: Try to run hook manually
.git/hooks/pre-commit

# Option B: Check if validate-ia-first.py is broken
python docs/ia/SCRIPTS/validate-ia-first.py --audit docs/ia

# Option C: Check if dependencies missing
pip list | grep questionary  # or other deps
```

### Step 3: Immediate Bypass (Emergency Only)
```bash
# Commit WITH bypass - but document why!
git commit --no-verify -m "EMERGENCY: [reason for bypass]"

# Example:
git commit --no-verify -m "EMERGENCY: Pre-commit broken, rollback CI/CD gate failure"
```

---

## 🔧 ROOT CAUSE & FIX

### Problem #1: validate-ia-first.py Crashed

**Symptom:** Script throws exception

**Fix:**
```bash
# Check script syntax
python -m py_compile docs/ia/SCRIPTS/validate-ia-first.py

# If syntax error:
#   → Edit the script to fix it
#   → Commit fix: git commit --no-verify -m "fix: validate-ia-first syntax"

# If runtime error (missing import, etc.):
#   → Check dependencies: pip install -r requirements-dev.txt
#   → Retry: python docs/ia/SCRIPTS/validate-ia-first.py --audit docs/ia
```

### Problem #2: Hook File Corrupted

**Symptom:** Hook exists but won't run

**Fix:**
```bash
# Restore from template
cp .pre-commit-config.yaml.template .pre-commit-config.yaml
pre-commit install

# Verify:
ls -la .git/hooks/pre-commit
```

### Problem #3: Dependencies Missing

**Symptom:** ImportError: No module named 'X'

**Fix:**
```bash
# Install all dev dependencies
pip install -r requirements-dev.txt

# Or specific package:
pip install questionary  # or whatever module failed
```

### Problem #4: Validation Rules Changed

**Symptom:** Previously valid files now fail validation

**Fix:**
```bash
# Check what changed in docs
git diff HEAD docs/ia/

# Review new validation rules:
cat docs/ia/IA_FIRST_SPECIFICATION.md

# If rules are too strict:
#   → Use --no-verify to bypass
#   → File issue to adjust rules
#   → Example: git commit --no-verify -m "EMERGENCY: Override overly-strict rule X"
```

---

## 📋 ESCALATION PATH

### If Hook Fix Fails (> 5 minutes)

**Contact repo maintainer:**
- Message: "Pre-commit hook broken, all commits blocked"
- Attach error output
- Ask for: Emergency bypass or hook repair

**Your options while waiting:**
1. Work locally with `--no-verify` (document each bypass)
2. Use branch without hook (not recommended)
3. Temporarily disable hook (requires maintainer)

### Temporary Hook Disable (Emergency Only)
```bash
# Make hook non-executable (disables it)
chmod -x .git/hooks/pre-commit

# Work around it:
git commit -m "EMERGENCY: Disabled pre-commit hook due to X"

# ⚠️ YOU MUST:
# 1. Document why in the commit message
# 2. File issue for hook repair
# 3. Re-enable when fixed: chmod +x .git/hooks/pre-commit
```

---

## ✅ VERIFICATION

**Hook is working when:**
```bash
# Try a dummy commit (that will fail validation)
echo "invalid" > docs/ia/test-invalid.md
git add docs/ia/test-invalid.md
git commit -m "test: should fail"

# Expected: Hook runs, validation fails, commit blocked
# (Not: Hook crashes or hangs)

# Cleanup:
git reset HEAD docs/ia/test-invalid.md
rm docs/ia/test-invalid.md
```

---

## 🛡️ PREVENTION

**To prevent this:**

1. **Weekly hook validation** (CI/CD job)
   ```bash
   # Runs: pre-commit run --all-files
   # Alerts if hook fails
   ```

2. **Monitor hook status in PRs**
   - If hook bypassed: Review why
   - If hook crashes: Investigate immediately

3. **Keep dependencies updated**
   ```bash
   pip install -r requirements-dev.txt --upgrade
   ```

---

## 🔗 RELATED

- [VALIDATION_QUIZ.md](../../guides/onboarding/VALIDATION_QUIZ.md)
- [IA_FIRST_SPECIFICATION.md](../../IA_FIRST_SPECIFICATION.md)
- [validate-ia-first.py](../../SCRIPTS/validate-ia-first.py)

---

**Recovery Time:** 2-15 minutes  
**Severity:** 🔴 CRITICAL (blocks all development)  
**Frequency:** Rare (should not happen if well-maintained)
