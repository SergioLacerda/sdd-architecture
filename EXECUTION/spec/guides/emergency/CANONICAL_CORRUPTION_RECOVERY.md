# 🚨 EMERGENCY PROCEDURE — CANONICAL Corruption Recovery

**When Core Architecture Rules Are Broken**

---

## 🚨 Symptom

**You see merge conflict markers in CANONICAL:**

```bash
$ cat docs/ia/CANONICAL/rules/ia-rules.md

<<<<<<< HEAD
Rule #5: Always use ports for infrastructure
||||||| merged common ancestors
[original content]
=======
Rule #5: DELETED - no longer needed
>>>>>>> feature-branch

❌ CANONICAL is corrupted
```

**Impact:** Architecture rules are ambiguous. Team doesn't know what rules apply.

---

## ⏱️ IMMEDIATE RECOVERY (5 minutes)

### Step 1: LOCK CANONICAL

**Notify entire team NOW:**
```bash
# Send to Slack/chat:
"🚨 CANONICAL corrupted - merge conflict in ia-rules.md"
"DO NOT COMMIT TO docs/ia/CANONICAL"
"Recovery in progress..."
```

### Step 2: Identify Scope

```bash
# Which files have conflicts?
git status | grep "both modified"

# Example output:
#   both modified:   docs/ia/CANONICAL/rules/ia-rules.md
#   both modified:   docs/ia/CANONICAL/decisions/ADR-001-architecture.md

# How many conflicts?
git diff --name-only --diff-filter=U | wc -l
```

### Step 3: Choose Recovery Strategy

**Strategy A: Revert to Last Known Good (Recommended)**
```bash
# Find last clean CANONICAL commit
git log --oneline docs/ia/CANONICAL/ | head -10

# Should show recent commit without conflicts
# Example: abc123 "docs: Update ADR-005 for new rules"

# Revert everything to that point
git reset --hard abc123

# Verify no conflicts:
git status
# Should show: nothing to commit
```

**Strategy B: Abort Merge (If in middle of merge)**
```bash
# Cancel the merge entirely
git merge --abort

# Verify:
git status
# Should show: on branch main, nothing to commit
```

---

## 🔧 MANUAL RESOLUTION (If automated fails)

**Only if you know what you're doing:**

```bash
# Open the conflicted file:
vim docs/ia/CANONICAL/rules/ia-rules.md

# See the conflict markers:
# <<<<<<< HEAD
#   [Your current version]
# =======
#   [Incoming version]
# >>>>>>> branch-name

# Decide:
# Option 1: Keep YOUR version (delete ======= ... >>>>>>> markers)
# Option 2: Keep INCOMING version (delete <<<<<<< ... ======= markers)
# Option 3: MERGE both versions (keep best of both)

# After editing, mark as resolved:
git add docs/ia/CANONICAL/rules/ia-rules.md

# Verify no other conflicts:
git diff --name-only --diff-filter=U

# If none: Complete the merge
git commit -m "Resolve CANONICAL merge conflict - manual resolution"
```

---

## ⚠️ SPECIAL CASE: CANONICAL Drift

**If merge conflict reveals major divergence:**

```
Example conflict:
  HEAD has:    "All infrastructure MUST use ports"
  Feature has: "Infrastructure can import directly"

This is ARCHITECTURAL DISAGREEMENT, not just merge conflict
```

**Recovery:**

1. **Do NOT commit the merge yet**
2. **Contact team lead immediately**
3. **Discuss which version is correct**
4. **Update ADR-003 to clarify**
5. **Then resolve conflict based on decision**

---

## ✅ VERIFICATION

**After resolving, verify CANONICAL integrity:**

```bash
# 1. Check no merge markers remain
grep -r "<<<<<<< HEAD" docs/ia/CANONICAL/
grep -r "=======" docs/ia/CANONICAL/
grep -r ">>>>>>> " docs/ia/CANONICAL/

# Should return nothing (no matches)

# 2. Validate structure
python docs/ia/SCRIPTS/validate_governance.py

# Expected output: "✅ All governance checks pass"

# 3. Validate ADRs
python docs/ia/SCRIPTS/validate_adrs.py

# Expected output: "✅ All ADRs valid"

# 4. Full audit
python docs/ia/SCRIPTS/validate-ia-first.py --audit docs/ia/CANONICAL/

# Expected: Passes or shows only pre-existing issues
```

---

## 📋 PREVENTION

**To prevent CANONICAL conflicts:**

1. **Minimal changes to CANONICAL**
   - Only modify CANONICAL when absolutely necessary
   - Use ADR process for rule changes
   - Small, focused commits

2. **Coordinate team changes**
   - If planning CANONICAL change: Announce in standup
   - Wait for ACK before committing
   - If conflict might occur: Communicate

3. **Merge strategy**
   ```bash
   # Use "ours" strategy to prefer main branch
   git merge -X ours feature-branch
   
   # This keeps CANONICAL from feature branch, uses main
   ```

4. **Frequent integration**
   - Regular merges of main into feature branches
   - Fewer accumulated changes = fewer conflicts
   - Catch conflicts early

---

## 🚨 WORST CASE: Complete CANONICAL Rebuild

**If corruption is too severe to fix:**

```bash
# Last resort: Restore entire CANONICAL from backup
git checkout main -- docs/ia/CANONICAL/

# Or from specific known-good commit:
git show abc123:docs/ia/CANONICAL/ > /tmp/canonical-backup/
# [manual review]
# [restore if looks good]

# Then commit:
git commit -m "EMERGENCY: Restored CANONICAL from backup (corruption recovery)"

# File issue:
# "CANONICAL was corrupted due to [reason]. Restored from backup."
```

---

## 🔗 RELATED

- [ADR-001: Clean Architecture](../../CANONICAL/decisions/ADR-001-clean-architecture.md)
- [ADR-003: Ports & Adapters](../../CANONICAL/decisions/ADR-003-ports-adapters-pattern.md)
- [ADR-005: Thread Isolation](../../CANONICAL/decisions/ADR-005-thread-isolation-mandatory.md)

---

**Recovery Time:** 5-30 minutes  
**Severity:** 🔴 CRITICAL (architecture rules ambiguous)  
**Frequency:** Should be rare (CANONICAL rarely changes)
