# Quick Troubleshoot Reference

**One-page reference** for fastest problem resolution.

---

## Symptoms → Solutions (Speed-optimized)

| Symptom | Diagnosis | Fix | Time |
|---------|-----------|-----|------|
| **Commit blocked** | Governance failure | `python3 _core/governance_compliance.py --fix-steps` | 2min |
| **Push blocked** | Health check <10/10 | `python3 _core/health_check.py --force-recheck` | 2min |
| **Agent won't start** | Handshake failed | `python3 _core/agent_handshake.py --verbose` | 3min |
| **Quiz won't run** | Missing questions | `git checkout origin/main -- _core/quiz_questions.json` | 1min |
| **Everything fails** | 0/10 checks | `git pull origin main` or reset hard | 5min |
| **Slow operations** | Performance issue | `python3 tests/performance/benchmark.py` | 5min |
| **Cache stale** | Old state | `rm -f _core/.sdd/agent_state.json` | <1min |

---

## Health Check States & Meanings

| State | Checks | Meaning | Action |
|-------|--------|---------|--------|
| 🟢 **Healthy** | 10/10 | All good | Proceed normally |
| 🟡 **Degraded** | 6-9/10 | Partial failure | Fix soon |
| 🔴 **Failed** | 0-5/10 | Critical failure | Fix immediately |

---

## Most Common Fixes (Fastest)

### Fix 1: Clear Cache (< 1 second)
```bash
rm -f _core/.sdd/agent_state.json
```
**When**: Stale state, changes not reflected

### Fix 2: Force Fresh Health Check (< 2 seconds)
```bash
python3 _core/health_check.py --force-recheck
```
**When**: Cache invalid, need latest status

### Fix 3: Governance Compliance (< 3 seconds)
```bash
python3 _core/governance_compliance.py --fix-steps
```
**When**: Policy violations, auto-fix available

### Fix 4: Pull Latest (< 5 seconds)
```bash
git pull origin main
```
**When**: Missing files after merge, structure broken

### Fix 5: Hard Reset (< 10 seconds, DESTRUCTIVE)
```bash
git reset --hard origin/main
```
**When**: Everything broken, willing to lose local changes

---

## Command Quick-Ref

```bash
# Status checks
python3 _core/health_check.py                      # Quick (default)
python3 _core/health_check.py --verbose            # Detailed
python3 _core/health_check.py --force-recheck      # Fresh
python3 _core/health_check.py --category git       # Git only

# Governance
python3 _core/governance_compliance.py --verify    # Check
python3 _core/governance_compliance.py --fix-steps # Auto-fix
python3 _core/governance_compliance.py --enforcement-check

# Agent
python3 _core/agent_handshake.py                   # Check
python3 _core/agent_handshake.py --verbose         # Detailed
python3 _core/agent_handshake.py --force-recheck   # Fresh

# Quiz
python3 _core/quiz_executor.py                     # Interactive
python3 _core/quiz_executor.py --mode silent       # Auto-score
python3 _core/quiz_executor.py --topic governance  # Filter

# Performance
python3 tests/performance/benchmark.py             # Measure
python3 tests/performance/benchmark.py --save      # Save results

# Git
git status                                          # Status
git log --oneline -5                               # Recent commits
git remote -v                                       # Remotes
```

---

## Error Messages (Fastest Diagnosis)

```
❌ "Health check failed"
   → python3 _core/health_check.py --verbose

❌ "Governance violation"
   → python3 _core/governance_compliance.py --verify

❌ "ModuleNotFoundError"
   → export PYTHONPATH=/home/sergio/dev/sdd-architecture:$PYTHONPATH

❌ "Not a git repo"
   → git init && git remote add origin <url>

❌ "JSONDecodeError"
   → python3 -m json.tool <file>.json

❌ "Permission denied"
   → chmod +x .git/hooks/pre-commit (etc)
```

---

## Performance Targets

```
Health Check (quick):         < 200ms  ✓
Health Check (full):          < 1s     ✓
Governance Validation:        < 500ms  ✓
Agent Handshake:              < 2s     ✓
Quiz per Question:            < 3s     ✓
```

---

## When Everything is Broken

**Start here** if nothing works:

```bash
# 1. Check Git status
git status
git log --oneline -3

# 2. Check health
python3 _core/health_check.py --verbose

# 3. If <5/10, restore from origin
git fetch origin main
git reset --hard origin/main

# 4. Verify
python3 _core/health_check.py
```

---

## Help Resources

- **Full Health Check**: [HEALTH_CHECK_GUIDE.md](HEALTH_CHECK_GUIDE.md)
- **Detailed Troubleshooting**: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- **Performance Guide**: [PERFORMANCE_OPTIMIZATION.md](PERFORMANCE_OPTIMIZATION.md)
- **Git Hooks**: [GIT_HOOKS_GUIDE.md](GIT_HOOKS_GUIDE.md)

---

**Last updated**: Phase 5, Step 5  
**Type**: Quick reference  
**Use**: Save and print for fastest problem resolution
