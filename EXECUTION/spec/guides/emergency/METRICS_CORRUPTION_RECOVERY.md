# 🚨 EMERGENCY PROCEDURE — Metrics Corruption Recovery

**When Metrics Data Is Wrong or Impossible**

---

## 🚨 Symptom

**METRICS.md shows impossible or corrupted values:**

```bash
$ cat docs/ia/METRICS.md

# Onboarding Time
- Current: -45 minutes ❌ (IMPOSSIBLE!)
- Target: 10 minutes

# Context Efficiency
- Savings: 450% ❌ (Over 100%!)
- Token waste: -50KB (Negative!)

# Success Rate
- Setup wizard: 125% ❌ (Can't exceed 100%!)

❌ DATA IS CORRUPTED
```

**Impact:** Metrics are meaningless. Can't trust data. Can't measure improvements.

---

## ⏱️ IMMEDIATE ASSESSMENT (5 minutes)

### Step 1: Check Git History

```bash
# When did data become corrupt?
git log --oneline -p docs/ia/METRICS.md | head -50

# Look for:
# - Last "reasonable" values
# - When impossible values appeared
# - Who made the changes

# Example:
# abc123 fix: Update METRICS  
#   - Context: 50KB (✅ reasonable)
# def456 fix: Update metrics  
#   - Context: -100KB (❌ impossible - START HERE)
```

### Step 2: Identify Corrupted Data

```bash
# Which metrics are broken?
grep -E "^- [^:]+: .*-[0-9]|[0-9]{3}%" docs/ia/METRICS.md

# Output: Shows all impossible values
```

### Step 3: Find Last Good State

```bash
# Get version before corruption:
git show def455:docs/ia/METRICS.md > /tmp/metrics-before.md

# Compare:
diff -u /tmp/metrics-before.md docs/ia/METRICS.md

# Review changes carefully
```

---

## 🔧 RECOVERY OPTIONS

### Option A: Revert to Last Known Good (Fastest)

```bash
# Find clean commit (before corruption):
git log --oneline docs/ia/METRICS.md | grep -v "corrupt\|fix data\|broken" | head -1

# Example output: abc123 "docs: Baseline metrics for Q2 2026"

# Revert:
git checkout abc123 -- docs/ia/METRICS.md

# Verify:
cat docs/ia/METRICS.md | grep -E "^- " | head -10
# Should show reasonable values

# Commit:
git commit -m "EMERGENCY: Recovered METRICS from backup (corrupted data)"
```

### Option B: Manual Correction (If you know the real values)

```bash
# Edit METRICS.md:
vim docs/ia/METRICS.md

# Fix impossible values:
# ❌ - Onboarding Time: -45 minutes
# ✅ - Onboarding Time: 285 seconds

# ❌ - Context Savings: 450%
# ✅ - Context Savings: 45%

# ❌ - Success Rate: 125%
# ✅ - Success Rate: 95%

# Add note about recovery:
# [RECOVERED] These values were corrupted, re-baselined manually

git commit -m "EMERGENCY: Manual recovery of corrupted metrics"
```

### Option C: Re-Baseline from Scratch

```bash
# If you can't trust ANY recent data:

# 1. Backup current (corrupted) file:
cp docs/ia/METRICS.md /tmp/metrics-corrupted-backup.md

# 2. Create fresh baseline:
cat > docs/ia/METRICS.md << 'EOF'
# 📊 METRICS — Baseline Recovered

**Recovery Date:** 2026-04-19  
**Previous State:** Corrupted  
**Method:** Re-baseline from observed reality

## 1. Setup Wizard Timing

**Current Measurement:**
- Need to run with new developer
- Time pending actual measurement

**Target:**
- < 10 minutes for full onboarding
- < 5 minutes for experienced dev

## 2. Context Efficiency

**Current Measurement:**
- Need to measure token consumption
- Pending implementation of metrics collection

**Target:**
- 40% reduction from baseline
- 50KB average context per task type

---

[Continue with actual measurements once collected]
EOF

# 3. Commit:
git commit -m "EMERGENCY: Re-baselined METRICS after data corruption (fresh start)"
```

---

## 📊 PREVENTION

**To prevent metrics corruption:**

1. **Collect data programmatically**
   ```bash
   # Instead of manual editing:
   python docs/ia/SCRIPTS/collect_metrics.py --update METRICS.md
   # Reduces manual error
   ```

2. **Validate before committing**
   ```bash
   # Script to validate METRICS:
   python -c "
   import re
   with open('docs/ia/METRICS.md') as f:
       for line in f:
           # Check no negative percentages
           if re.search(r'-\d+%', line):
               raise ValueError(f'Negative percentage found: {line}')
           # Check no >100% success rates
           if re.search(r'(\d{3,}|[1-9]\d\d)%', line):
               raise ValueError(f'Over 100% found: {line}')
   print('✅ Metrics valid')
   "
   ```

3. **Lock METRICS from manual edits**
   ```bash
   # Use pre-commit hook:
   # If METRICS.md changed and not via collection script: BLOCK
   
   # This forces use of: python collect_metrics.py
   ```

4. **Backup METRICS weekly**
   ```bash
   # Automated backup:
   cp docs/ia/METRICS.md .backups/METRICS-$(date +%Y%m%d).md
   # So you can recover to any previous week
   ```

---

## ✅ VERIFICATION

**After recovery, verify metrics:**

```bash
# 1. Check all values are reasonable
grep ":" docs/ia/METRICS.md | while read line; do
  if echo "$line" | grep -qE "-[0-9]|[0-9]{3}%"; then
    echo "❌ Invalid: $line"
  else
    echo "✅ Valid: $line"
  fi
done

# 2. Sanity check values
# - Times should be in seconds or minutes (not negative)
# - Percentages should be 0-100%
# - Context sizes should be > 0 KB

# 3. Commit and document:
git commit -m "EMERGENCY: Verified metrics recovery"

# 4. File issue:
# "METRICS corruption incident - recovery completed"
# Include:
#   - What was corrupted
#   - How you fixed it
#   - Why it happened
#   - Prevention for future
```

---

## 📋 INCIDENT REPORT

**After recovery, document:**

```markdown
# Metrics Corruption Incident Report

**Date:** 2026-04-19  
**Duration:** 30 minutes  
**Data Loss:** None (recovered from backup)

## What Happened
- Metrics.md received invalid values (-45 min, 450%)
- Data became unreliable

## Root Cause
- [Manual editing error? Collection script bug? Merge conflict?]

## Recovery Method
- Reverted to commit abc123
- Verified all values now reasonable

## Prevention
- Implement automated collection script
- Add validation pre-commit hook
- Weekly backups
- Lock METRICS from manual edits

## Lessons Learned
- [What we learned]

---

**Follow-up Issue:** #XXX (Link to prevention implementation)
```

---

## 🔗 RELATED

- [METRICS.md](../../METRICS.md)
- [collect_metrics.py](../../SCRIPTS/collect_metrics.py) (when implemented)

---

**Recovery Time:** 5-30 minutes  
**Severity:** 🟠 HIGH (metrics unreliable, but not blocking)  
**Frequency:** Should be rare (with proper validation)
