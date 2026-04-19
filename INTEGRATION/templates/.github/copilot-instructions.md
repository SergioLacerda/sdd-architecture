# 🎯 AI GOVERNANCE — Agent Initialization Protocol

**FOR ALL AGENTS: Read this file, then follow AGENT_HARNESS workflow**

This file tells you:
1. Where the SDD framework lives (check `.spec.config`)
2. What rules you must follow (read `.spec.config` → framework → rules)
3. How to work (follow 7-phase AGENT_HARNESS workflow)

---

## 🚀 Quick Start

### 1. Find the framework
```bash
cat .spec.config | grep spec_path
# Returns: spec_path = ../sdd-archtecture (or your path)
```

### 2. Read entry point
Framework is at: `{spec_path}/EXECUTION/_START_HERE.md`

Use that to understand:
- What you need to learn
- 7-phase workflow
- Where to find rules

### 3. Begin PHASE 1
Read rules: `{spec_path}/EXECUTION/spec/CANONICAL/rules/`
- constitution.md
- ia-rules.md

### 4. Follow AGENT_HARNESS
7 phases of development workflow (see `.spec.config` framework for full guide)

---

## 📍 Key Files for This Project

**Framework location:** (from .spec.config)
**Framework entry:** `.../EXECUTION/_START_HERE.md`
**Rules:** `.../EXECUTION/spec/CANONICAL/rules/`
**Guides:** `.../EXECUTION/spec/guides/`

---

## 🔗 Integration Process

This file was copied during project integration:
```bash
cp {framework}/INTEGRATION/templates/.github/copilot-instructions.md .github/
```

**For integration help:** See `{spec_path}/INTEGRATION/README.md`

---

## ✅ First-Time Setup

1. ✅ This file copied (you're reading it)
2. Find `.spec.config` — read `spec_path` value
3. Go to that path: `{spec_path}/EXECUTION/`
4. Read `_START_HERE.md`
5. Start Phase 1 of AGENT_HARNESS

---

**Questions?** See the framework's FAQ at: `{spec_path}/EXECUTION/spec/guides/reference/FAQ.md`
