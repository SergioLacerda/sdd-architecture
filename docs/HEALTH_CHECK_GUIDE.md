# Health Check Guide

Complete reference for understanding, running, and troubleshooting health checks in the SDD Architecture framework.

## Quick Start

```bash
# Run all health checks
python3 _core/health_check.py

# Run specific category
python3 _core/health_check.py --category git

# Show detailed output
python3 _core/health_check.py --verbose
```

---

## Health Check Overview

The health check system validates your project against **10 critical requirements** organized into 4 categories:

### Categories

| Category | Checks | Purpose |
|----------|--------|---------|
| **git** | 2 checks | Git repository integrity |
| **structure** | 3 checks | Project directory structure |
| **config** | 2 checks | Configuration files |
| **governance** | 3 checks | Governance & compliance |

---

## Health Check States

### 🟢 **Healthy**
- **What it means**: All 10/10 checks passing
- **Exit code**: 0
- **Action**: None required - proceed normally
- **TTL**: 30 minutes (cached)

### 🟡 **Degraded**
- **What it means**: Some checks failing (6-9/10 passing)
- **Exit code**: 1
- **Action**: Review failures immediately
- **Common causes**:
  - Missing configuration files
  - Git repository not initialized
  - Dependencies not installed

### 🔴 **Failed**
- **What it means**: Critical checks failing (0-5/10 passing)
- **Exit code**: 1
- **Action**: Block operations, fix immediately
- **Common causes**:
  - Corrupted project structure
  - Missing core files
  - Governance violations

---

## Understanding Health Check Output

### Verbose Output Example

```
Health Check Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[GIT]
✓ Repository initialized        (git/.git exists)
✓ Remote configured             (origin detected)

[STRUCTURE]
✓ Core directories exist        (_core, docs, etc.)
✓ Python files present          (health_check.py, etc.)
✗ Config directory missing      (_core/.sdd/ missing)

[CONFIG]
✓ Python version 3.10+          (Current: 3.10.14)
✗ governance-core.json missing  (Required)

[GOVERNANCE]
✓ Seedling template exists      (.sdd-wizard/templates)
✓ Quiz system initialized       (quiz_questions.json)
✗ Compliance rules missing      (ENFORCEMENT_RULES.json)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SUMMARY: 7/10 checks passing
STATUS: 🟡 Degraded
EXIT CODE: 1
```

### Compact Output (Default)

```
Health Check: 7/10 passing (🟡 Degraded)
Issues: config directory, governance config
Run with --verbose for details
```

### Reading the Output

Each check shows:
- **Status indicator** (✓ = pass, ✗ = fail)
- **Check name**
- **Details** in parentheses (what's checked)

---

## When to Run Health Checks

### Automatic (Always)

Health checks run automatically in these scenarios:

```
Before:
├─ Agent Handshake (on agent startup)
├─ Governance validation (before commit)
├─ Compliance enforcement (pre-push)
└─ Quiz execution (knowledge validation)

Cache:
├─ 30-minute TTL (performance)
├─ Force recheck with --force-recheck
└─ Shared across processes
```

### Manual (On Demand)

Run manually when:

```
1. Setting up new project
   $ python3 _core/health_check.py

2. After structure changes
   $ python3 _core/health_check.py --verbose

3. Debugging failures
   $ python3 _core/health_check.py --category governance

4. CI/CD verification
   $ python3 _core/health_check.py || exit 1

5. After governance updates
   $ python3 _core/health_check.py --force-recheck --verbose
```

---

## Health Check Categories

### Git Checks (2 checks)

```python
# Check 1: Repository initialized
✓ Pass: .git/ directory exists
✗ Fail: Not a Git repository

# Fix: git init && git remote add origin <url>

---

# Check 2: Remote configured
✓ Pass: origin remote detected
✗ Fail: No remote configured

# Fix: git remote add origin <url>
```

### Structure Checks (3 checks)

```python
# Check 1: Core directories exist
Required: _core, docs, tests, EXECUTION, INTEGRATION
✓ Pass: All directories present
✗ Fail: Missing _core or docs

# Fix: mkdir -p _core docs tests

---

# Check 2: Core files present
Required: health_check.py, agent_handshake.py, etc.
✓ Pass: All core files exist
✗ Fail: Missing health_check.py

# Fix: See Phase 1 setup guide

---

# Check 3: Python modules importable
✓ Pass: All imports successful
✗ Fail: Module not found

# Fix: pip install -r requirements.txt
```

### Config Checks (2 checks)

```python
# Check 1: Config directory exists
Required: _core/.sdd/
✓ Pass: Directory exists
✗ Fail: Missing _core/.sdd/

# Fix: mkdir -p _core/.sdd/

---

# Check 2: Python version sufficient
Required: Python 3.8+
✓ Pass: Python 3.10.14
✗ Fail: Python 3.7.x

# Fix: upgrade to Python 3.8+
```

### Governance Checks (3 checks)

```python
# Check 1: Governance config exists
Required: governance-core.json
✓ Pass: File present and valid
✗ Fail: File missing or invalid JSON

# Fix: python3 _core/governance_compliance.py --fix-steps

---

# Check 2: Seedling templates present
Required: .sdd-wizard/templates/
✓ Pass: All seedlings present
✗ Fail: Missing seedling files

# Fix: Restore from GitHub or Phase 2 setup

---

# Check 3: Mandatory policies met
Required: ENFORCEMENT_RULES, authority roles, etc.
✓ Pass: All policies configured
✗ Fail: Missing policy definitions

# Fix: python3 _core/governance_compliance.py --verify
```

---

## Debugging Failed Checks

### Step-by-Step Process

**1. Run verbose output**
```bash
python3 _core/health_check.py --verbose
```
Identify which checks are failing.

**2. Run by category**
```bash
# Test specific category
python3 _core/health_check.py --category git
python3 _core/health_check.py --category structure
python3 _core/health_check.py --category config
python3 _core/health_check.py --category governance
```

**3. Check individual files**
```bash
# Git checks
ls -la .git/
git remote -v

# Structure checks
ls -la _core/ docs/ tests/

# Config checks
ls -la _core/.sdd/
python3 --version

# Governance checks
ls -la _core/.sdd/*.json
python3 _core/governance_compliance.py --verify
```

**4. Apply fixes**
See "Recovery Procedures" below.

### Common Failing Checks & Fixes

| Check | Failure Reason | Quick Fix |
|-------|---|---|
| Repository initialized | Not a Git repo | `git init && git remote add origin <url>` |
| Remote configured | Missing origin | `git remote add origin <url>` |
| Core directories | Missing dirs | `mkdir -p _core docs tests` |
| Core files | Missing Python files | Restore from GitHub (Phase 1) |
| Config directory | No _core/.sdd | `mkdir -p _core/.sdd` |
| Python version | Version < 3.8 | Upgrade Python |
| Governance config | Invalid JSON | `python3 _core/governance_compliance.py --fix-steps` |
| Seedling templates | Missing files | Restore from Phase 2 |
| Mandatory policies | Config incomplete | Run compliance validator |

---

## Recovery Procedures

### Recovery Level 1: Configuration Issues

**Scenario**: Missing config files or directories

```bash
# 1. Check what's missing
python3 _core/health_check.py --verbose

# 2. Create missing directories
mkdir -p _core/.sdd
mkdir -p .sdd-wizard/templates

# 3. Verify structure
python3 _core/health_check.py

# 4. Proceed if all green (🟢)
```

### Recovery Level 2: Governance Violations

**Scenario**: Governance config invalid or incomplete

```bash
# 1. Validate current state
python3 _core/governance_compliance.py --verify

# 2. Get auto-fix steps
python3 _core/governance_compliance.py --fix-steps

# 3. Apply recommended fixes
# (Follow the output from step 2)

# 4. Verify resolution
python3 _core/governance_compliance.py --verify

# 5. Run health check
python3 _core/health_check.py
```

### Recovery Level 3: Structural Issues

**Scenario**: Missing core files or directories

```bash
# 1. Check current structure
find _core -type f -name "*.py" | head -20

# 2. List missing from Phase 1/2
# Expected files:
#   _core/health_check.py
#   _core/agent_handshake.py
#   _core/quiz_executor.py
#   _core/governance_compliance.py

# 3. Restore from GitHub
git pull origin main

# 4. Or, reset to known good state
git reset --hard origin/main

# 5. Run full health check
python3 _core/health_check.py --verbose
```

### Recovery Level 4: Repository Issues

**Scenario**: Git repo corrupted or detached

```bash
# 1. Check Git status
git status
git log --oneline -5

# 2. If detached HEAD
git checkout main

# 3. If repo corrupted
# Option A: Re-clone
cd /tmp
git clone <repo-url> sdd-backup
cp -r sdd-backup/_core/* /path/to/project/_core/

# Option B: Recover from backup
git reflog
git reset --hard <commit-hash>

# 4. Verify
python3 _core/health_check.py
```

### Recovery Level 5: Complete Reset

**Last resort**: Complete reinstallation

```bash
# 1. Backup current work
cp -r /path/to/project /tmp/project-backup

# 2. Fresh clone
rm -rf /path/to/project
git clone <repo-url> /path/to/project
cd /path/to/project

# 3. Setup from scratch
python3 _core/health_check.py --verbose

# 4. If still failing, check Phase 1 setup guide
cat EXECUTION/_START_HERE.md
```

---

## Health Checks in CI/CD

### GitHub Actions Integration

```yaml
# .github/workflows/health-check.yml
name: Health Check

on: [push, pull_request]

jobs:
  health:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - uses: actions/setup-python@v4
        with:
          python-version: "3.10"
      
      - name: Run health check
        run: |
          python3 _core/health_check.py --verbose
          exit_code=$?
          echo "Health check exit code: $exit_code"
          exit $exit_code
      
      - name: Report on failure
        if: failure()
        run: |
          python3 _core/health_check.py --category governance
          python3 _core/governance_compliance.py --verify
```

### Pre-commit Hook Integration

```bash
# .git/hooks/pre-commit (executable)
#!/bin/bash
python3 _core/health_check.py
if [ $? -ne 0 ]; then
    echo "❌ Health check failed - commit blocked"
    exit 1
fi
```

### Pre-push Hook Integration

```bash
# .git/hooks/pre-push (executable)
#!/bin/bash
python3 _core/health_check.py --force-recheck
if [ $? -ne 0 ]; then
    echo "❌ Health check failed - push blocked"
    echo "Run: python3 _core/health_check.py --verbose"
    exit 1
fi
```

---

## Health Checks with Agent Handshake

### Implicit Validation (Automatic)

When agent starts, health check runs automatically:

```python
# In agent_handshake.py
layer_1 = _check_semantic_triggers()  # Is user intent clear?
layer_2 = _check_health_status()      # ← Health checks here
layer_3 = _check_governance()         # Are rules followed?
layer_4 = _check_enforcement()        # Can we proceed?

if health_status == "🟢 Healthy":
    allow_operation()
elif health_status == "🟡 Degraded":
    warn_and_continue()
else:  # 🔴 Failed
    block_operation()
```

### Expected Behavior

| Health State | Agent Behavior | User Action |
|---|---|---|
| 🟢 Healthy | Proceed normally | Continue |
| 🟡 Degraded | Warn, continue | Fix issues soon |
| 🔴 Failed | Block operations | Fix immediately |

---

## Monitoring Health Over Time

### Checking Health Trends

```bash
# Daily health check log
python3 _core/health_check.py >> logs/health.log
tail -f logs/health.log

# Count passing checks over time
grep "passing" logs/health.log
```

### Setting up Monitoring

```bash
# Cron job (every 6 hours)
0 */6 * * * cd /path/to/project && python3 _core/health_check.py --verbose >> logs/health-monitor.log

# Dashboard integration (Phase 7)
# Will show compliance trends, health history, anomalies
```

---

## FAQ

### Q: How often do I need to run health checks?
**A**: Automatically before every major operation. Manually after structure changes or when debugging. Cache expires every 30 minutes.

### Q: Can I bypass a failing health check?
**A**: In PERMISSIVE mode, yes (with warnings). In STANDARD/STRICT, no. See governance enforcement levels.

### Q: Why did the health check fail after I just fixed it?
**A**: The cache may be stale. Run with `--force-recheck` to bypass the 30-minute TTL.

### Q: What if I ignore health check warnings?
**A**: In STRICT mode, operations will be blocked. In STANDARD mode, you'll get warnings. Always fix issues before push/merge.

### Q: How do I run health checks in my CI/CD pipeline?
**A**: Use the GitHub Actions example above. Exit code 0 = pass, 1 = fail. Recommended: block merge on failure.

### Q: Can health checks be customized?
**A**: Yes, extend in `_core/health_check.py`. Add new checks, categories, or validation rules as needed.

---

## Next Steps

- **Quick issues?** See [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- **Performance tuning?** See [Performance Optimization Guide](../context/runtime-state/analysis/PERFORMANCE_TESTING_GUIDE.md)
- **Governance problems?** See [GOVERNANCE_IMPLEMENTATION.md](../_core/.sdd-wizard/templates/governance/base-seedling/GOVERNANCE_IMPLEMENTATION.md)
- **Agent integration?** See [Agent Handshake Protocol](../context/README.md#agent-handshake-protocol)

---

**Last updated**: Phase 5, Step 1  
**Related**: health_check.py, agent_handshake.py, governance_compliance.py
