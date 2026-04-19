# 🛑 PROJECT BOUNDARY — SDD Framework Work Scope

**Effective Date:** April 19, 2026  
**Decision:** Focus exclusively on SDD framework development  
**Status:** ACTIVE

---

## 📌 Decision

**SDD-ARCHTECTURE is a STANDALONE FRAMEWORK project.**

Starting April 19, 2026:
- ❌ DO NOT reference rpg-narrative-server for patterns
- ❌ DO NOT audit other target projects for ideas
- ❌ DO NOT use target projects as examples

Why? The gap analysis (Commit 037d04f) extracted ALL useful patterns. Framework now contains complete authority.

---

## ✅ What We Already Extracted

From rpg-narrative-server audit:
- ✅ 8-layer architecture pattern (now in ADR-002)
- ✅ Ports & adapters pattern (now in ADR-003)
- ✅ Thread isolation pattern (now in ADR-004)
- ✅ Context-aware infrastructure (now in guides/runtime/)
- ✅ Runtime indices necessity (now in RUNTIME_INDICES_SPECIFICATION.md)
- ✅ Architecture compliance tests (now in ARCHITECTURE_VALIDATION.md)
- ✅ Enforcement mechanisms (now in ENFORCEMENT_RULES.md)

**Result:** Everything useful is NOW IN THE FRAMEWORK.

---

## 🎯 Work Scope Going Forward

**ONLY WORK ON SDD FRAMEWORK:**

1. **Complete pending HIGH priority items:**
   - [ ] Update PHASE-0-AGENT-ONBOARDING.md (add steps 6-7)
   - [ ] Create CI_CD_INTEGRATION.md
   - [ ] Expand INTEGRATION/templates for more scenarios

2. **Add MEDIUM priority documentation:**
   - [ ] Architecture test templates (full suite)
   - [ ] GitHub Actions workflow templates
   - [ ] Runtime indices templates (.ai/runtime/)

3. **Improve existing docs:**
   - [ ] Add more examples to ADRs
   - [ ] Expand CANONICAL/specifications/
   - [ ] Create more INTEGRATION examples

4. **Build ecosystem around framework:**
   - [ ] CLI tool for PHASE 0 automation
   - [ ] Compliance checker (pre-commit hook)
   - [ ] Documentation validator

---

## ❌ DO NOT

- ❌ Look at rpg-narrative-server for ideas (it's a CLIENT, not an EXAMPLE)
- ❌ Ask "what does rpg-narrative-server do?" (ask "what does framework say?")
- ❌ Use rpg-narrative-server as reference implementation
- ❌ Import/reference rpg-narrative-server code in any framework docs
- ❌ Make decisions based on "rpg-narrative-server needs this"

---

## ✅ DO

- ✅ Build framework features based on SPEC principles
- ✅ Reference framework's own ADRs and specifications
- ✅ Ask "does framework have this documented?"
- ✅ Improve CANONICAL documentation
- ✅ Expand INTEGRATION templates
- ✅ Make framework more complete/authoritative

---

## 🔗 Authority Flow

```
SDD Framework (AUTHORITY)
    ↓
rpg-narrative-server (CLIENT - implements framework)
    ↓
Other projects (CLIENTS - will implement framework)

Flow is ONE-DIRECTIONAL:
Framework → Projects (not the other way around!)
```

---

## 📝 When to Reference rpg-narrative-server

**NEVER.** 

If you think you need to reference it:
- **Situation:** "I wonder how rpg-narrative-server handles X"
- **Do This Instead:** "What does framework say about X?"
- **If Framework is Silent:** Propose new pattern in framework (via ADR)
- **Then:** Document in framework
- **Never:** Look at rpg-narrative-server implementation

---

## ✨ Key Principle

**"Framework is the source of truth, not the projects that use it."**

- Framework defines HOW projects should be built
- Projects prove framework works (they're evidence)
- Framework doesn't copy from projects (projects copy from framework)
- If project discovers pattern framework missed → document in framework, NOT in project

---

## 🚀 Next Steps (SDD Framework Only)

1. Review pending HIGH priority items
2. Complete PHASE-0 automation
3. Expand CI/CD integration docs
4. Build INTEGRATION examples for common scenarios
5. Create better templates for quick starts

---

**Authority:** User decision, Commit 037d04f  
**Status:** ACTIVE boundary  
**Review Date:** Monthly (ensure scope respected)
