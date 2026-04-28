# Troubleshooting Guide

Comprehensive troubleshooting reference for SDD Architecture health checks, governance, and agent operations.

---

## Quick Troubleshooting (Under 2 minutes)

### Problem: "Health check failed"
```bash
# 1. See what's wrong
python3 packages/health_check.py --verbose

# 2. Check specific category  
python3 packages/health_check.py --category governance

# 3. Get auto-fix steps
python3 packages/governance_compliance.py --fix-steps
```

### Problem: Agent won't start
```bash
# 1. Check health status
python3 packages/agent_handshake.py

# 2. Clear cache
rm -f packages/.sdd/agent_state.json

# 3. Retry
python3 packages/agent_handshake.py --verbose
```

### Problem: Can't commit changes
```bash
# 1. Bypass git hook (if needed)
git commit --no-verify

# 2. Fix governance
python3 packages/governance_compliance.py --verify

# 3. Retry commit
git commit -m "message"
```

---

## Troubleshooting by Symptom

### 🔴 "All checks failing / 0/10 passing"

**Symptom**: Complete health check failure, nothing works

**Diagnosis**:
```bash
python3 packages/health_check.py --verbose
```
Look for "git/.git" or "packages/" failures.

**Root Causes** (in order of likelihood):
1. Not a Git repository
2. Corrupted project structure
3. Files deleted

**Fix Steps**:
```bash
# Option 1: Initialize Git (if needed)
git init
git remote add origin <url>
python3 packages/health_check.py

# Option 2: Restore structure (if needed)
git pull origin main
python3 packages/health_check.py --verbose

# Option 3: Complete reset (last resort)
cd /tmp && git clone <repo-url> backup
rm -rf /path/to/project
cp -r backup /path/to/project
python3 packages/health_check.py
```

**Verification**:
```bash
python3 packages/health_check.py | grep "🟢"
# Should see: 10/10 passing (🟢 Healthy)
```

---

### 🟡 "Some checks failing / 6-9/10 passing"

**Symptom**: Partial failures, some features work

**Diagnosis**:
```bash
python3 packages/health_check.py --verbose
```
Look for specific failures (marked with ✗).

**Most Common (5 scenarios)**:

#### Scenario 1: Missing Config Directory
```bash
# Symptom: ✗ Config directory missing
# Fix:
mkdir -p packages/.sdd/
python3 packages/health_check.py
```

#### Scenario 2: Governance Config Invalid
```bash
# Symptom: ✗ Governance config invalid / missing
# Diagnosis:
python3 packages/governance_compliance.py --verify

# Fix:
python3 packages/governance_compliance.py --fix-steps
# Follow the generated steps
```

#### Scenario 3: Python Version Too Old
```bash
# Symptom: ✗ Python version < 3.8
# Check current:
python3 --version

# Fix: Upgrade Python
# Ubuntu/Debian:
sudo apt-get install python3.10

# macOS:
brew install python@3.10
```

#### Scenario 4: Missing Seedling Files
```bash
# Symptom: ✗ Seedling templates missing
# Check what's missing:
ls -la packages/.sdd-wizard/templates/

# Fix: Restore from Phase 2
git checkout origin/main -- packages/.sdd-wizard/

# Or pull latest:
git pull origin main
```

#### Scenario 5: Broken Git Remote
```bash
# Symptom: ✗ Remote configured (but nothing else)
# Check:
git remote -v

# Fix:
git remote remove origin
git remote add origin <correct-url>
git fetch origin
```

**Verification**:
```bash
python3 packages/health_check.py
# Should show: 10/10 passing (🟢 Healthy)
```

---

### Governance-Specific Issues

#### Problem: "Governance validation failed"

**Symptom**: Git push/commit blocked by governance

```bash
git push
# ❌ Governance validation failed: 2 policy violations
```

**Diagnosis**:
```bash
python3 packages/governance_compliance.py --verify
# Output shows which policies are violated
```

**Root Causes** (with fixes):

| Policy | Failure | Fix |
|--------|---------|-----|
| governance-core.json exists | File missing | `mkdir -p packages/.sdd` |
| Valid JSON format | Invalid JSON | `python3 -m json.tool packages/.sdd/governance-core.json` |
| Active seedling defined | No seedling | Edit governance-core.json, set "active_seedling" |
| Authority roles assigned | Empty roles | Add "architect", "governance", "operations" to authority field |
| Enforcement level set | No level | Set enforcement_level to "STRICT", "STANDARD", or "PERMISSIVE" |
| PHASE 0 completed | Not run | Run `python3 EXECUTION/SCRIPTS/phase-0-agent-onboarding.py` |
| Health check passes | Failures | `python3 packages/health_check.py --force-recheck` |

**Fix Steps**:
```bash
# 1. Get detailed violations
python3 packages/governance_compliance.py --verify

# 2. Get auto-fix steps
python3 packages/governance_compliance.py --fix-steps

# 3. Review and apply fixes
# (Follow output from step 2)

# 4. Verify resolution
python3 packages/governance_compliance.py --verify --enforce strict

# 5. Retry operation
git push origin main
```

---

#### Problem: "Can't bypass governance check"

**Symptom**: Enforcement level is STRICT, need to bypass

**Root Cause**: Your enforcement level is set to "STRICT" (most restrictive)

**Solution** (with authorization):

```bash
# 1. Check current enforcement
python3 packages/governance_compliance.py --enforcement-check

# 2. Check your role
# Current: operations (can bypass in STANDARD/PERMISSIVE)
# Required: STANDARD or PERMISSIVE mode

# 3. Change enforcement level (if authorized)
# Edit packages/.sdd/governance-core.json:
# "enforcement_level": "STANDARD"

# 4. Verify change
python3 packages/governance_compliance.py --enforcement-check

# 5. Retry operation
git commit --no-verify
```

**Note**: Only "architect" role can lower enforcement level.

---

### Agent/Handshake Issues

#### Problem: "Agent handshake failed"

**Symptom**: Agent won't start

```bash
python3 packages/agent_handshake.py
# ❌ Handshake failed: Health check incomplete
```

**Diagnosis**:
```bash
python3 packages/agent_handshake.py --verbose
# Shows which layer failed (Layer 1-4)
```

**Root Causes by Layer**:

| Layer | Issue | Fix |
|-------|-------|-----|
| Layer 1 | Intent unclear | Rephrase your request, use clear keywords |
| Layer 2 | Health check failed | `python3 packages/health_check.py --force-recheck` |
| Layer 3 | Governance violated | `python3 packages/governance_compliance.py --fix-steps` |
| Layer 4 | Enforcement blocks operation | Check enforcement mode and your role |

**Fix Steps**:
```bash
# 1. Run with verbose to see which layer failed
python3 packages/agent_handshake.py --verbose

# 2. Fix based on layer
# If Layer 2: python3 packages/health_check.py --force-recheck
# If Layer 3: python3 packages/governance_compliance.py --verify
# If Layer 4: python3 packages/governance_compliance.py --enforcement-check

# 3. Clear cache
rm -f packages/.sdd/agent_state.json

# 4. Retry
python3 packages/agent_handshake.py
```

---

#### Problem: "State cache stale"

**Symptom**: Changes not reflected, old values

**Root Cause**: 30-minute TTL cache still valid

**Solution**:
```bash
# Clear cache
rm -f packages/.sdd/agent_state.json

# Or force recheck
python3 packages/health_check.py --force-recheck
python3 packages/agent_handshake.py --force-recheck

# Or wait 30 minutes (TTL expires)
```

---

### Quiz Issues

#### Problem: "Quiz won't execute"

**Symptom**: Quiz fails to start

```bash
python3 packages/quiz_executor.py
# ❌ Quiz initialization failed
```

**Diagnosis**:
```bash
python3 packages/quiz_executor.py --verbose
```

**Root Causes** (with fixes):

| Issue | Fix |
|-------|-----|
| quiz_questions.json missing | Restore from GitHub: `git checkout origin/main -- packages/quiz_questions.json` |
| Invalid JSON format | `python3 -m json.tool packages/quiz_questions.json` |
| Health check failed | `python3 packages/health_check.py --force-recheck` |
| Wrong Python version | Ensure Python 3.8+ |

**Fix Steps**:
```bash
# 1. Check JSON validity
python3 -m json.tool packages/quiz_questions.json

# 2. Restore if needed
git checkout origin/main -- packages/quiz_questions.json

# 3. Run health check
python3 packages/health_check.py

# 4. Try again
python3 packages/quiz_executor.py
```

---

#### Problem: "Quiz scoring wrong"

**Symptom**: Passing score too high/low

```bash
python3 packages/quiz_executor.py --topic governance
# Score: 5/10 (50%) - FAIL (70% required)
# But I got these right...
```

**Root Cause**: Scoring system calculates per-topic or global

**Solution**:
```bash
# 1. Run in verbose mode to see answers
python3 packages/quiz_executor.py --verbose

# 2. Review your answers
# (Check which ones were marked wrong)

# 3. Run again with same topic
python3 packages/quiz_executor.py --topic governance

# Note: Quiz requires 70% globally (not per-topic)
```

---

### Performance Issues

#### Problem: "Health check too slow"

**Symptom**: Health check takes 10+ seconds

```bash
time python3 packages/health_check.py
# real 0m12.345s <- Too slow
```

**Root Causes**:
- Disk I/O slow (network drive?)
- Python startup overhead
- Large file system operations

**Quick Fixes**:
```bash
# 1. Clear cache and rerun (first run slower)
rm -f packages/.sdd/agent_state.json
time python3 packages/health_check.py

# 2. Use compact mode (faster)
python3 packages/health_check.py --mode compact

# 3. Check specific category (faster)
python3 packages/health_check.py --category git

# Expected: <500ms for quick check, <2s for full
```

#### Problem: "Agent startup slow"

**Symptom**: Handshake takes 5+ seconds

```bash
time python3 packages/agent_handshake.py
# real 0m8.234s <- Slower than expected
```

**Quick Fixes**:
```bash
# 1. Use silent mode (skip output)
python3 packages/agent_handshake.py --mode silent

# 2. Check what's slow
python3 packages/agent_handshake.py --verbose

# 3. Profile specific layer
# (See Phase 3 performance guide)

# Expected: <2s for handshake
```

---

## Recovery Decision Tree

```
Start: Issue Detected
│
├─ All checks failing (0/10)?
│  └─ Yes → Check Git repo exists
│     ├─ No → git init && git remote add origin <url>
│     └─ Yes → Run: git status && git log
│
├─ Some checks failing (6-9/10)?
│  ├─ Governance issue?
│  │  └─ Run: python3 packages/governance_compliance.py --verify
│  ├─ Config missing?
│  │  └─ Run: mkdir -p packages/.sdd
│  └─ Python version?
│     └─ Check: python3 --version
│
├─ Health check passes but agent fails?
│  ├─ Layer 2 (health)?
│  │  └─ Force recheck: --force-recheck
│  ├─ Layer 3 (governance)?
│  │  └─ Verify: python3 packages/governance_compliance.py --verify
│  └─ Layer 4 (enforcement)?
│     └─ Check: python3 packages/governance_compliance.py --enforcement-check
│
├─ Can't commit/push?
│  ├─ Governance violation?
│  │  └─ Fix: python3 packages/governance_compliance.py --fix-steps
│  └─ Git issue?
│     └─ Check: git status && git remote -v
│
└─ Still broken?
   └─ See Level 3-5 Recovery in HEALTH_CHECK_GUIDE.md
```

---

## Common Error Messages

### Error: "ModuleNotFoundError: No module named 'packages'"

**Cause**: Python path not set correctly

**Fix**:
```bash
# Run from project root
cd /home/sergio/dev/sdd-architecture
python3 packages/health_check.py

# Or add to PYTHONPATH
export PYTHONPATH=/home/sergio/dev/sdd-architecture:$PYTHONPATH
python3 packages/health_check.py
```

---

### Error: "FileNotFoundError: .git/config"

**Cause**: Not a Git repository

**Fix**:
```bash
git init
git remote add origin <repo-url>
python3 packages/health_check.py
```

---

### Error: "JSONDecodeError in governance-core.json"

**Cause**: Invalid JSON formatting

**Fix**:
```bash
# Validate JSON
python3 -m json.tool packages/.sdd/governance-core.json

# Find error line (output shows line number)
# Edit the file to fix syntax

# Verify fix
python3 -m json.tool packages/.sdd/governance-core.json
```

---

### Error: "PermissionError: permission denied"

**Cause**: File/directory permissions wrong

**Fix**:
```bash
# Check permissions
ls -la packages/health_check.py

# Make executable
chmod +x packages/health_check.py
chmod +x packages/agent_handshake.py
chmod +x packages/governance_compliance.py

# Verify
python3 packages/health_check.py
```

---

### Error: "subprocess.CalledProcessError: git command failed"

**Cause**: Git operation failed (bad state, auth issue, etc.)

**Fix**:
```bash
# Check Git status
git status

# If detached HEAD:
git checkout main

# If auth issue:
git remote set-url origin <correct-url>

# If needs credentials:
git config credential.helper store
git pull origin main

# Retry
python3 packages/health_check.py
```

---

## Preventive Measures

### 1. Regular Health Checks

```bash
# Add to cron (every 6 hours)
0 */6 * * * cd /path/to/project && python3 packages/health_check.py >> logs/health.log 2>&1
```

### 2. Pre-commit Validation

```bash
# Install git hooks (Step 4)
bash scripts/install-git-hooks.sh

# Hooks will auto-run:
# - Before commit: python3 packages/health_check.py
# - Before push: python3 packages/health_check.py --force-recheck
```

### 3. Governance Monitoring

```bash
# Weekly compliance check
0 0 * * 0 cd /path/to/project && python3 packages/governance_compliance.py --verify
```

### 4. Agent State Cleanup

```bash
# Clear stale cache weekly
0 1 * * 0 rm -f packages/.sdd/agent_state.json
```

---

## When to Contact Support

If none of the above fixes work:

1. **Gather diagnostics**:
   ```bash
   python3 packages/health_check.py --verbose > diagnostics.log
   python3 packages/governance_compliance.py --verify >> diagnostics.log
   git status >> diagnostics.log
   python3 --version >> diagnostics.log
   ```

2. **Check logs**:
   ```bash
   cat logs/health.log (if exists)
   cat packages/.sdd/debug.log (if exists)
   ```

3. **Create issue** with:
   - diagnostics.log output
   - Error message (full)
   - Steps to reproduce
   - Python version
   - Git status

---

## FAQ

### Q: Do I need to run health checks manually?
**A**: No, they run automatically before major operations. Run manually to debug or verify.

### Q: Can I ignore failed health checks?
**A**: Not in STRICT/STANDARD mode. In PERMISSIVE, you can bypass with warnings.

### Q: How long does recovery take?
**A**: Level 1-2: <5 minutes. Level 3-4: 10-15 minutes. Level 5: Full reset, 20+ minutes.

### Q: Will recovery delete my work?
**A**: No, unless you choose Level 5 reset. Backup first: `cp -r . ~/backup-$(date +%s)`

### Q: What if health check is wrong?
**A**: Open an issue with verbose output. Checks are adjustable in `packages/health_check.py`.

---

## Related Documentation

- [Health Check Guide](HEALTH_CHECK_GUIDE.md) - How to interpret checks
- [Governance Implementation](../packages/.sdd-wizard/templates/governance/base-seedling/GOVERNANCE_IMPLEMENTATION.md) - Set up governance
- [Performance Guide](../context/runtime-state/analysis/PERFORMANCE_TESTING_GUIDE.md) - Speed optimization
- [Agent Handshake](../context/README.md#agent-handshake-protocol) - Agent validation

---

**Last updated**: Phase 5, Step 2  
**Related**: health_check.py, governance_compliance.py, agent_handshake.py
