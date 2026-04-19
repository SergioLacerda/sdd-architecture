# 🤖 AI Governance Rules — VS Code

**Rules for AI agents working in VS Code on this project**

---

## 📋 Entry Point

1. Check `.spec.config` for framework location
2. Go to: `.../EXECUTION/_START_HERE.md`
3. Read rules: `.../EXECUTION/spec/CANONICAL/rules/ia-rules.md`

---

## ⚡ Quick Rules

### Rule 1: Ports Mandatory
- Never: `from src.infrastructure.storage import Database`
- Always: `from src.domain.ports import StoragePort`
- Use abstract ports, never concrete implementations

### Rule 2: Thread Isolation
- Only modify code for YOUR assigned task
- Check `.ai/context-aware/execution-state/` before starting
- If someone else works on it, wait or coordinate

### Rule 3: Tests During Implementation
- Always TDD: write test first, then code
- Never "implement first, test later"

### Rule 4: Documentation Mandatory
- Document decisions in checkpoint
- File: `.ai/context-aware/execution-state/`

### Rule 5: 45+ Definition of Done Criteria
- Before PR: Check `.../EXECUTION/spec/CANONICAL/specifications/definition_of_done.md`
- Verify all criteria met

---

## 🔗 Full Rules

All 16 mandatory rules: `.../EXECUTION/spec/CANONICAL/rules/ia-rules.md`

---

## 🚀 Workflow: AGENT_HARNESS (7 Phases)

1. **PHASE 1:** Read rules + pass quiz
2. **PHASE 2:** Check execution state (conflicts?)
3. **PHASE 3:** Choose PATH (bug/simple/complex/multi)
4. **PHASE 4:** Load context (search framework docs)
5. **PHASE 5:** Implement (with TDD)
6. **PHASE 6:** Validate (tests + definition of done)
7. **PHASE 7:** Checkpoint (document + PR)

See: `.../EXECUTION/spec/guides/onboarding/AGENT_HARNESS.md`

---

## 🆘 Emergency Help

- Framework broken? → `.../EXECUTION/spec/guides/emergency/`
- Questions? → `.../EXECUTION/spec/guides/reference/FAQ.md`
- Need help? → Read `.../README.md` for support

---

**Questions?** See `.spec.config` → framework path → docs
