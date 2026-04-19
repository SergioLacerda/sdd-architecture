# 🤖 AI Rules for VS Code

**VS Code has detected this workspace uses SDD Framework governance.**

---

## 🚀 Quick Start

**Read this first:** [.ai-index.md](./.ai-index.md)

This is your AI learning seed. It contains:
- What this project is (SDD Framework)
- Your entry points (INTEGRATION vs EXECUTION flows)
- Project boundary (framework only, no external projects)
- Rule enforcement mechanisms (4-layer validation)
- Framework status & priorities (what to work on)
- Full AGENT_HARNESS workflow (7-phase process)

---

## 🎯 Key Sections in `.ai-index.md`

1. **Project Boundary** → Understand what you should/shouldn't do
2. **Rule Enforcement Mechanisms** → 4 layers that validate your work
3. **Framework Status & Priorities** → What's HIGH priority now
4. **AGENT_HARNESS Workflow** → Your 7-phase development process

---

## ⚡ TL;DR (30 seconds)

1. You are working on the **SDD Framework** (not a client project)
2. Read `.ai-index.md` sections above
3. Follow `AGENT_HARNESS` in `.ai-index.md`
4. Your work will be validated by:
   - Pre-commit hooks (local)
   - CI/CD tests (GitHub)
   - Code review (human)
   - Metrics audits (continuous)

---

## 📍 Entry Points by Scenario

**First time here?**
→ Read [EXECUTION/_START_HERE.md](./EXECUTION/_START_HERE.md)

**Have a bug to fix?**
→ Read [EXECUTION/docs/ia/guides/onboarding/AGENT_HARNESS.md](./EXECUTION/docs/ia/guides/onboarding/AGENT_HARNESS.md)

**Stuck or confused?**
→ Read [EXECUTION/docs/ia/guides/emergency/README.md](./EXECUTION/docs/ia/guides/emergency/README.md)

**Need to find something?**
→ Read [EXECUTION/NAVIGATION.md](./EXECUTION/NAVIGATION.md)

---

## 📝 Mandatory Rules (16 Total)

Full list: [EXECUTION/docs/ia/CANONICAL/rules/ia-rules.md](./EXECUTION/docs/ia/CANONICAL/rules/ia-rules.md)

**Most critical 5:**

1. **Ports Mandatory** — Never import infrastructure directly
2. **Thread Isolation** — Only modify YOUR thread (check execution-state/)
3. **Tests During Implementation** — TDD always, never "test later"
4. **No Implicit State** — Always verify before acting
5. **Checkpoint After Work** — Document what you did

---

## ✅ Before You Commit

- [ ] Pre-commit hooks passed (`git commit` succeeded)
- [ ] All tests passing locally
- [ ] Checkpoint updated in execution-state/
- [ ] No rule violations (check ia-rules.md)
- [ ] Ready to push PR

---

## 🆘 Emergency Resources

- **Tests failing?** → `EXECUTION/docs/ia/guides/emergency/`
- **Rules violated?** → `EXECUTION/docs/ia/CANONICAL/rules/ia-rules.md`
- **Stuck on architecture?** → `EXECUTION/docs/ia/CANONICAL/decisions/`

---

**Version:** SDD Framework 2.1  
**Updated:** April 19, 2026  
**Authority:** SPEC v2.1 Framework
