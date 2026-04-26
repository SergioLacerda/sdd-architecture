# 🚨 Emergency Procedures Index

**When production governance breaks, start here.**

---

## 📋 All Emergency Procedures

| Emergency | Symptom | Recovery Time | Severity |
|-----------|---------|----------------|----------|
| [Pre-Commit Hook Failure](PRE_COMMIT_HOOK_FAILURE.md) | Can't commit anything | 2-15 min | 🔴 CRITICAL |
| [Auto-Fix Corruption](AUTO_FIX_CORRUPTION_RECOVERY.md) | `--fix` mode broke files | 5-15 min | 🔴 CRITICAL |
| [CANONICAL Corruption](CANONICAL_CORRUPTION_RECOVERY.md) | Merge conflicts in ia-rules.md | 5-30 min | 🔴 CRITICAL |
| [CI/CD Gate Failure](CI_CD_GATE_FAILURE.md) | All PRs blocked by spec-enforcement | 2-30 min | 🔴 CRITICAL |
| [Metrics Corruption](METRICS_CORRUPTION_RECOVERY.md) | METRICS.md has impossible values | 5-30 min | 🟠 HIGH |

---

## 🎯 Decision Tree

**Something is broken. Which procedure do I use?**

```
❌ SOMETHING IS BROKEN
│
├─ Can't run git commit?
│  └─ → Pre-Commit Hook Failure
│
├─ Files got corrupted after auto-fix?
│  └─ → Auto-Fix Corruption Recovery
│
├─ Merge conflicts in /EXECUTION/spec/CANONICAL/?
│  └─ → CANONICAL Corruption Recovery
│
├─ All PRs failing in CI/CD?
│  └─ → CI/CD Gate Failure
│
├─ METRICS.md shows impossible values?
│  └─ → Metrics Corruption Recovery
│
└─ Other issue?
   └─ Check: docs/ia/guides/troubleshooting/
      (For non-emergency issues)
```

---

## 🚀 Quick Links

- [All Emergency Procedures](./index.md) ← You are here
- [Troubleshooting Guides](../troubleshooting/) ← For non-emergencies
- [Operational Guides](../operational/) ← For normal workflows
- [AGENT_HARNESS](../onboarding/AGENT_HARNESS.md) ← Start here normally

---

## 📞 Getting Help

**If no procedure covers your issue:**

1. **Check troubleshooting guides** first (non-emergencies)
2. **File issue** with details: symptoms, what you tried, error output
3. **Contact repo maintainer** if blocking entire team

---

**Status:** ✅ Complete (5/5 procedures documented)  
**Last Updated:** April 19, 2026  
**Maintenance:** Review quarterly, add procedures as needed
