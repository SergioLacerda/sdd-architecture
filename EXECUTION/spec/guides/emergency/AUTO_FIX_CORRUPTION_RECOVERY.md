# 🚨 EMERGENCY PROCEDURE — Auto-Fix Corruption Recovery

**When Auto-Fix Mode Breaks Files**

---

## 🚨 Symptom

**After running `validate-ia-first.py --fix`:**

```bash
$ python docs/ia/SCRIPTS/validate-ia-first.py --fix docs/ia

✅ Fixed 25 files

# But then you notice:
$ cat docs/ia/CANONICAL/ia-rules.md

⚠️ File is corrupted:
  - Missing sections
  - Invalid markdown
  - Broken links
  - Headers deleted
```

**Impact:** Multiple files corrupted. Data loss risk. Need rollback.

---

## ⏱️ IMMEDIATE RECOVERY (5 minutes)

### Step 1: STOP & Assess Damage
```bash
# Don't make new commits!
# Check what changed:
git diff --stat HEAD

# How many files affected?
git diff HEAD docs/ia/ | wc -l

# See details:
git diff HEAD docs/ia/CANONICAL/
```

### Step 2: Identify Corrupted Files
```bash
# Show all modified files
git status

# Review each one:
git diff HEAD -- docs/ia/CANONICAL/ia-rules.md
git diff HEAD -- docs/ia/CANONICAL/specifications/
# ... etc
```

### Step 3: Revert Auto-Fix (Safest Path)
```bash
# Revert ONLY the docs/ia/ folder to previous state
git checkout HEAD -- docs/ia/

# Verify reverted:
git status
# Should show: nothing to commit, working tree clean

# Or if files still modified:
git reset --hard HEAD
```

### Step 4: Verify Integrity
```bash
# Run validation WITHOUT --fix mode
python docs/ia/SCRIPTS/validate-ia-first.py --audit docs/ia

# Expected: Should pass or show specific issues
# If crash: Auto-fix script itself is broken
```

---

## 🔍 ROOT CAUSE ANALYSIS

### Why Did Auto-Fix Break Files?

### Issue #1: Script Had Bug in This Mode

**Symptoms:**
- Files missing text
- Random sections deleted
- Headers malformed

**Fix:**
```bash
# Review auto-fix logic:
cat docs/ia/SCRIPTS/validate-ia-first.py | grep -A 20 "def auto_fix"

# If logic is wrong:
#   1. Don't run --fix until fixed
#   2. Use --audit mode only
#   3. Manual fixes until script corrected
```

### Issue #2: Input Files Were Invalid

**Symptoms:**
- Auto-fix tried to parse broken file
- Mangled the output

**Fix:**
```bash
# Check git log - what changed before auto-fix?
git log --oneline docs/ia/ | head -5

# Was a bad file committed?
# If yes: Revert that commit too
git revert <bad-commit-hash>
```

### Issue #3: Concurrent Modifications

**Symptoms:**
- Multiple people ran auto-fix simultaneously
- Merge conflicts created
- Files got corrupted in merge

**Fix:**
```bash
# Never run --fix in parallel!
# Add lock file:
touch docs/ia/AUTO_FIX_IN_PROGRESS

# Before running:
if [ -f docs/ia/AUTO_FIX_IN_PROGRESS ]; then
  echo "Auto-fix already running!"
  exit 1
fi

# After running:
rm docs/ia/AUTO_FIX_IN_PROGRESS
```

---

## 🛡️ PREVENTION & RECOVERY

### Prevent Auto-Fix Corruption

**Use --audit mode first (no changes):**
```bash
# 1. Run in audit-only mode
python docs/ia/SCRIPTS/validate-ia-first.py --audit docs/ia

# 2. Review what WOULD be changed:
python docs/ia/SCRIPTS/validate-ia-first.py --dry-run docs/ia

# 3. Only then, if safe:
python docs/ia/SCRIPTS/validate-ia-first.py --fix docs/ia
```

### Backup Before Auto-Fix

```bash
# Create backup branch
git checkout -b auto-fix-backup-$(date +%Y%m%d-%H%M%S)
git checkout main

# Now safe to test auto-fix:
python docs/ia/SCRIPTS/validate-ia-first.py --fix docs/ia

# If broken:
git reset --hard HEAD
git checkout auto-fix-backup-...
git push -f origin auto-fix-backup-...
```

### Team Coordination

**Only ONE person runs auto-fix:**
```bash
# In team chat/standup:
"I'm running auto-fix on docs/ia now. Don't commit to docs/ia for 5 min."

# Wait for ACK from team
# Run auto-fix
# Commit results
# Tell team: "Auto-fix done, docs/ia updated"
```

---

## ✅ VERIFICATION

**After recovery, verify integrity:**
```bash
# 1. Check file syntax
find docs/ia -name "*.md" -exec python -c "import markdown; markdown.markdown(open('{}').read())" \;

# 2. Check links
grep -r "\[.*\](.*\.md)" docs/ia | grep -v ".md)" | head -10

# 3. Run validation
python docs/ia/SCRIPTS/validate-ia-first.py --audit docs/ia

# 4. Commit recovery
git commit -m "EMERGENCY: Recovered from auto-fix corruption, reverted to HEAD"
```

---

## 📊 DAMAGE ASSESSMENT

**After revert, document:**

```markdown
# Auto-Fix Corruption Report

**Date:** 2026-04-19  
**Duration:** 10 minutes (2:30 PM - 2:40 PM)  
**Impact:** 25 files corrupted, all recovered  

**Root Cause:**
- [Identified cause]

**Affected Files:**
- docs/ia/CANONICAL/ia-rules.md
- docs/ia/CANONICAL/specifications/architecture.md
- ... [list all]

**Resolution:**
- Reverted to HEAD
- Verified integrity
- Identified root cause
- No data loss

**Prevention:**
- [What we'll do differently]

---

**Filed Issue:** #XXX (Link to issue tracking corruption prevention)
```

---

## 🔗 RELATED

- [validate-ia-first.py](../../SCRIPTS/validate-ia-first.py)
- [IA_FIRST_SPECIFICATION.md](../../IA_FIRST_SPECIFICATION.md)

---

**Recovery Time:** 5-15 minutes  
**Severity:** 🔴 CRITICAL (data corruption risk)  
**Frequency:** Should be rare (script should be tested)
