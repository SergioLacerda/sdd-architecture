# 🚀 START HERE — EXECUTION Workflow

**You're about to implement something. This guide gets you oriented in 5 minutes.**

---

## ❓ What Are You Doing?

Pick ONE:

### 1️⃣ **"This is my first time using SDD"**

You need to set up your development environment with SDD governance.

→ **Read:** [PHASE_0_SETUP.md](./docs/ia/guides/onboarding/PHASE-0-AGENT-ONBOARDING.md)

*Output: `.ai/` infrastructure created, you're ready to work*

**Time:** 20-30 minutes

---

### 2️⃣ **"I'm implementing a feature/bug right now"**

You have a task assigned. You want to implement it following SDD rules.

→ **Read:** [AGENT_HARNESS.md](./docs/ia/guides/onboarding/AGENT_HARNESS.md)

→ **Then:** Choose your PATH (A=bug, B=simple feature, C=complex, D=multithread)

*Output: Feature implemented, tests passing, checkpoint documented*

**Time:** Depends on complexity (30 min → 2 days)

---

### 3️⃣ **"Something broke, I need help now"**

Production emergency? Test failure? Governance violation?

→ **Read:** [Emergency Procedures](./docs/ia/guides/emergency/README.md)

Pick from:
- `PRE_COMMIT_HOOK_FAILURE.md` — Hook is blocking commits
- `TEST_FAILURE_GUIDE.md` — Tests failing unexpectedly
- `RULES_VIOLATION_DETECTED.md` — CI blocked for rule violation
- `IMPORTS_CORRUPTED.md` — Import system broken
- `METRICS_CORRUPTION.md` — Metrics don't make sense

*Output: Issue resolved, root cause documented*

**Time:** 10-30 minutes

---

### 4️⃣ **"I need to find specific documentation"**

You don't have a task—you just want to read about something.

→ **Read:** [NAVIGATION.md](./NAVIGATION.md)

*Use keyword search to find docs*

**Time:** 2-5 minutes

---

### 5️⃣ **"I have questions about how SDD works"**

Confused about architecture? Rules? Workflow?

→ **Read:** [FAQ.md](./docs/ia/guides/reference/FAQ.md) or [GLOSSARY.md](./docs/ia/guides/reference/GLOSSARY.md)

*Output: Clarification + links to detailed docs*

**Time:** 5-15 minutes

---

## 🎯 Seven Phases of AGENT_HARNESS (Quick Summary)

If you picked **#2 above**, here's what you'll do:

```
PHASE 1: Lock to Rules (15 min)
  → Read constitution + ia-rules
  → Pass VALIDATION_QUIZ (≥80%)

PHASE 2: Check Execution State (5 min)
  → Look at .ai/context-aware/
  → Make sure no one else is working on this

PHASE 3: Choose PATH (5 min)
  → A = Bug fix
  → B = Simple feature (1-2 days)
  → C = Complex feature (3+ days)
  → D = Multi-thread work (coordinated)

PHASE 4: Load Context (10-20 min)
  → Search .ai/runtime/search-keywords.md
  → Read only docs for your PATH

PHASE 5: Implement (1-8 hours)
  → Write code + tests (TDD)
  → Track progress in .ai/context-aware/task-progress/

PHASE 6: Validate (10-15 min)
  → All tests pass
  → Check definition_of_done (45+ items)

PHASE 7: Checkpoint (10 min)
  → Document decisions + risks
  → Create PR
```

**Total setup time:** 40-50 min (one time)  
**Implementation time:** Depends on complexity

---

## ✅ Quick Validation

Before continuing, confirm:

- ✅ You have `.spec.config` in project root
- ✅ It points to sdd-architecture (check: `cat .spec.config`)
- ✅ You have `.ai/runtime/` directory
- ✅ PHASE 0 has been run (creates `.ai/` infrastructure)

If something is missing → [PHASE_0_SETUP.md](./docs/ia/guides/onboarding/PHASE-0-AGENT-ONBOARDING.md)

---

## 🔗 Key Entry Points

| Scenario | Read This |
|----------|-----------|
| First time setup | [PHASE-0-AGENT-ONBOARDING.md](./docs/ia/guides/onboarding/PHASE-0-AGENT-ONBOARDING.md) |
| Implementing feature | [AGENT_HARNESS.md](./docs/ia/guides/onboarding/AGENT_HARNESS.md) |
| Emergency/blocked | [Emergency Procedures](./docs/ia/guides/emergency/README.md) |
| Need to find docs | [NAVIGATION.md](./NAVIGATION.md) |
| Questions | [FAQ.md](./docs/ia/guides/reference/FAQ.md) |

---

## 🚀 Next Action

Pick your scenario from the 5 above, then follow the link.

**Uncertain?** Start with [NAVIGATION.md](./NAVIGATION.md) — you'll find what you need.

---

**This page:** 5-minute orientation  
**Status:** Ready  
**Last updated:** April 19, 2026
