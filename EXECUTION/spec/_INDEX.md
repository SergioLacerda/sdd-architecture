# 📚 SPEC Master Index — Navigation & Documentation

**Navigation guide for SPEC framework (Principles & Specifications system) shared across multiple projects.**

> **AI-FIRST DESIGN:** All documentation structured for both human reading and AI analysis. Use clear hierarchies, explicit section markers, and consistent formatting.

## 🏗️ 4-Layer Architecture

### 1️⃣ CANONICAL/ ✅ **Immutable Authority**
Decisions, rules, specifications **global** (all projects inherit 100%).

- **rules/** — Mandatory rules and constitution
  - `ia-rules.md` — 16 mandatory protocols
  - `constitution.md` — Immutable principles (15 core)
  - `conventions.md` — Code patterns and style
  - `ENFORCEMENT_RULES.md` — Validation mechanism
  - `backward-compatibility-policy.md` — Deprecation process

- **specifications/** — Design blueprints
  - `architecture.md` — 8-layer clean architecture
  - `definition_of_done.md` — 45+ item checklist
  - `feature-checklist.md` — 8-layer process
  - `testing.md` — Testing strategy
  - `observability.md` — Logging, tracing, metrics, on-call
  - `security-model.md` — Threat model, auth, encryption
  - `performance.md` — SLO budgets and targets
  - `compliance.md` — Regulatory requirements

- **decisions/** — Architecture Decision Records
  - `ADR-001.md` — Clean Architecture (8-layer mandatory)
  - `ADR-002.md` — Async-first, no blocking
  - `ADR-003.md` — Ports & Adapters pattern
  - `ADR-004.md` — Vector index strategy
  - `ADR-005.md` — Thread isolation (2-level)
  - `ADR-006.md` — Event sourcing append-only

### 2️⃣ custom/ 🎨 **Project-Specific Specialization**
Project-specific customization (DRY principle, reusable templates).

- **_TEMPLATE/** — Starter template for new projects
  - `README.md` — How to use
  - `INTEGRATION_CHECKLIST.md` — Setup checklist
  - `development/` — Execution structure
  - `reality/` — Observed system state structure

- **[PROJECT_NAME]/** — Per-project implementation (e.g., rpg-narrative-server)
  - `README.md` — Project description
  - `INTEGRATION_RESULTS.md` — Integration details
  - `SPECIALIZATIONS/` — Mappings (generic → project-specific)
  - `development/` — Active work (ephemeral)
  - `reality/` — Current state (evolving)
  - `archive/` — Completed work (historical)

### 3️⃣ guides/ 📖 **Navigation & Learning**
How to use the framework effectively (for all projects).

- **onboarding/** — Getting started (3-15 min sessions)
- **implementation/** — Step-by-step how-to guides
- **navigation/** — Finding information quickly
- **reference/** — FAQ, glossary, quick reference
- **_INDEX.md** — This file (task-based navigation)
- **MIGRATION_*.md** — Transition guides for structure changes

### 4️⃣ development/_SHARED/ 🔄 **Cross-Project Coordination**
Shared state between projects (synchronization).

- `execution-state-matrix.md` — Status of all active threads
- `threading-status.md` — Concurrency status
- `active-threads.md` — Global threads (non-isolated)

---

## 📍 Quick Navigation by Task

### "I'm new to SPEC"
→ Read: `/docs/ia/guides/onboarding/QUICK_START.md` (3 min)  
→ Then: Choose PATH A, B, C, or D based on your task

### "I want to understand mandatory rules"
→ Read: `/docs/ia/CANONICAL/rules/ia-rules.md` (16 protocols)  
→ Time: 10 minutes

### "I want to understand architecture"
→ Read: `/docs/ia/CANONICAL/specifications/architecture.md` (8-layer blueprint)  
→ Time: 15 minutes

### "What's the current state of [PROJECT]?"
→ Go to: `/docs/ia/custom/[PROJECT_NAME]/reality/current-system-state/`  
→ Time: 5-10 minutes

### "What's the active work on [PROJECT]?"
→ Go to: `/docs/ia/custom/[PROJECT_NAME]/development/execution-state/_current.md`  
→ Time: 5-10 minutes

### "How do I start a new project?"
→ Copy: `/docs/ia/custom/_TEMPLATE/` to `/docs/ia/custom/[your-project]/`  
→ Follow: `INTEGRATION_CHECKLIST.md`  
→ Time: 2 hours

### "I want to understand a decision"
→ Read: `/docs/ia/CANONICAL/decisions/ADR-*.md`  
→ Then: Project specialization if needed  
→ Time: 10-15 minutes

### "How do I integrate SPEC into another project?"
→ Read: `/docs/ia/guides/navigation/REUSABILITY_GUIDE.md`  
→ Time: 20 minutes

### "What improvements are planned?"
→ Check: `/docs/ia/CANONICAL/specifications/` (new files marked ✨ WIP)  
→ Time: 10 minutes

---

## 🎯 Quick Summary

| Layer | Ownership | Update Frequency | Authority |
|-------|-----------|------------------|-----------|
| CANONICAL/ | Shared (all projects) | Quarterly (3 months) | Architect |
| custom/ | Per-project | Weekly | Tech Lead |
| guides/ | Shared (all projects) | Monthly | Documentation Owner |
| development/_SHARED/ | Cross-project | Real-time | Engineering Leads |

---

## 🚀 5-Minute Quick Start

1. **First time?** → Read `/docs/ia/guides/onboarding/QUICK_START.md` (3 min)
2. **Starting new project?** → Copy `/docs/ia/custom/_TEMPLATE/` to your project (2 min)
3. **Need to understand rules?** → `/docs/ia/CANONICAL/rules/ia-rules.md` (10 min)
4. **Filling in project details?** → Edit `custom/[your-project]/reality/` (2 hours)

---

**Last Updated:** 2026-04-19  
**Maintained by:** SPEC Governance Framework  
**Status:** ✅ Production-ready
