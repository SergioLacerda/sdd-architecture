# 🔍 Search Keywords Index

**Fast lookup table: Search term → File location**

Use this when you know WHAT you're looking for, but not WHERE it is.

---

## Framework Concepts

| Concept | Find In | File |
|---------|----------|------|
| **How AGENT_HARNESS works** | Guides/Onboarding | `guides/onboarding/AGENT_HARNESS.md` |
| **The 7 phases explained** | Guides/Onboarding | `guides/onboarding/AGENT_HARNESS.md` |
| **Entry points by tool** | Guides/Onboarding | `guides/onboarding/ENTRY_POINTS_BY_TOOL.md` |
| **Validation process** | Guides/Onboarding | `guides/onboarding/PHASE-7-VALIDATION.md` |
| **Quick reference** | Guides/Onboarding | `guides/onboarding/SESSION_QUICK_REFERENCE.md` |
| **Consolidation guide** | Guides/Onboarding | `guides/onboarding/ONBOARDING_CONSOLIDATION.md` |
| **Validation quiz** | Guides/Onboarding | `guides/onboarding/VALIDATION_QUIZ.md` |

---

## Constitutional Foundation

| Concept | Find In | File |
|---------|----------|------|
| **Core principles** | Rules/Constitution | `CANONICAL/rules/constitution.md` |
| **15 immutable principles** | Rules/Constitution | `CANONICAL/rules/constitution.md` |
| **Mandatory rules** | Rules | `CANONICAL/rules/ia-rules.md` |
| **16 SDD rules** | Rules | `CANONICAL/rules/ia-rules.md` |
| **Code conventions** | Rules | `CANONICAL/rules/conventions.md` |
| **Style guide** | Rules | `CANONICAL/rules/conventions.md` |

---

## Architecture Decisions

| Concept | Find In | File |
|---------|----------|------|
| **Why clean architecture?** | Decisions | `CANONICAL/decisions/ADR-001-clean-architecture-8-layer.md` |
| **8-layer architecture** | Decisions | `CANONICAL/decisions/ADR-001-clean-architecture-8-layer.md` |
| **Async-first design** | Decisions | `CANONICAL/decisions/ADR-002-async-first-no-blocking.md` |
| **Why ports & adapters?** | Decisions | `CANONICAL/decisions/ADR-003-ports-adapters-pattern.md` |
| **Infrastructure independence** | Decisions | `CANONICAL/decisions/ADR-003-ports-adapters-pattern.md` |
| **Vector index strategy** | Decisions | `CANONICAL/decisions/ADR-004-vector-index-strategy.md` |
| **Why thread isolation?** | Decisions | `CANONICAL/decisions/ADR-005-thread-isolation-mandatory.md` |
| **Thread isolation mandatory** | Decisions | `CANONICAL/decisions/ADR-005-thread-isolation-mandatory.md` |
| **Append-only storage** | Decisions | `CANONICAL/decisions/ADR-006-append-only-storage.md` |

---

## Context-Aware Agent Patterns

| Concept | Find In | File |
|---------|----------|------|
| **How to use context-aware** | Specifications | `CANONICAL/specifications/context-aware-agent-pattern.md` |
| **Agent patterns** | Specifications | `CANONICAL/specifications/context-aware-agent-pattern.md` |
| **SPECIALIZATIONS vs context** | Specifications | `CANONICAL/specifications/context-aware-agent-pattern.md` |
| **Task progress tracking** | Specifications | `CANONICAL/specifications/context-aware-agent-pattern.md` |
| **Analysis documentation** | Specifications | `CANONICAL/specifications/context-aware-agent-pattern.md` |
| **Execution-state management** | Specifications | `CANONICAL/specifications/context-aware-agent-pattern.md` |

---

## Implementation Standards

| Concept | Find In | File |
|---------|----------|------|
| **Definition of done** | Specifications | `CANONICAL/specifications/definition_of_done.md` |
| **45+ completion criteria** | Specifications | `CANONICAL/specifications/definition_of_done.md` |
| **How to communicate** | Specifications | `CANONICAL/specifications/communication.md` |
| **Documentation style** | Specifications | `CANONICAL/specifications/communication.md` |
| **Testing patterns** | Specifications | (In definition_of_done testing section) |
| **Hexagonal architecture** | Specifications | (In definition_of_done architecture section) |

---

## Development Workflow

| Concept | Find In | File |
|---------|----------|------|
| **Adding new project** | Operational | `guides/operational/ADDING_NEW_PROJECT.md` |
| **Integration process** | Operational | `guides/operational/ADDING_NEW_PROJECT.md` |
| **PHASE 0 detailed** | Operational | `guides/operational/` |
| **Merging doc conflicts** | Operational | `guides/operational/HANDLING_MERGE_CONFLICTS_IN_DOCS.md` |
| **Moving docs between projects** | Operational | `guides/operational/MIGRATING_DOCS_BETWEEN_PROJECTS.md` |
| **Revoking deprecated rules** | Operational | `guides/operational/REVOKING_DEPRECATED_RULES.md` |
| **Troubleshooting violations** | Operational | `guides/operational/TROUBLESHOOTING_SPEC_VIOLATIONS.md` |
| **Workflow validation** | Operational | `guides/operational/` (see DEVELOPMENT_WORKFLOW_VALIDATION.md) |
| **Metrics tracking** | Operational | `guides/operational/` (see METRICS_TRACKING.md if exists) |

---

## Emergency Procedures

| Concept | Find In | File |
|---------|----------|------|
| **What to do when stuck** | Emergency | `guides/emergency/README.md` |
| **Auto-fix corruption** | Emergency | `guides/emergency/AUTO_FIX_CORRUPTION_RECOVERY.md` |
| **Fix broken rules** | Emergency | `guides/emergency/CANONICAL_CORRUPTION_RECOVERY.md` |
| **CI/CD gates failing** | Emergency | `guides/emergency/CI_CD_GATE_FAILURE.md` |
| **Metrics corrupted** | Emergency | `guides/emergency/METRICS_CORRUPTION_RECOVERY.md` |
| **Pre-commit hook failed** | Emergency | `guides/emergency/PRE_COMMIT_HOOK_FAILURE.md` |

---

## Reference & Glossary

| Concept | Find In | File |
|---------|----------|------|
| **Common questions** | Reference | `guides/reference/FAQ.md` |
| **FAQ** | Reference | `guides/reference/FAQ.md` |
| **Terminology** | Reference | `guides/reference/GLOSSARY.md` |
| **SDD words defined** | Reference | `guides/reference/GLOSSARY.md` |
| **How 6 layers work** | Reference | `guides/reference/HOW_EACH_LAYER_WORKS.md` |
| **Layer hierarchy** | Reference | `guides/reference/HOW_EACH_LAYER_WORKS.md` |
| **Authority order** | Reference | `guides/reference/HOW_EACH_LAYER_WORKS.md` |

---

## Quick Navigation

**Need help?** Use this priority:
1. **FAQ** — Common questions
2. **GLOSSARY** — Term definitions
3. **NAVIGATION** (EXECUTION/NAVIGATION.md) — Full doc index
4. **Emergency** — When broken

---

## By Task Type

### "I'm implementing a feature"
1. Start: `CANONICAL/rules/ia-rules.md` (PHASE 1)
2. Check: `custom/[PROJECT]/development/execution-state/` (PHASE 2)
3. Choose: `guides/onboarding/AGENT_HARNESS.md` PATH (PHASE 3)
4. Search: This file (PHASE 4)
5. Build: `CANONICAL/specifications/definition_of_done.md` (PHASE 5-6)
6. Document: `custom/[PROJECT]/development/execution-state/` (PHASE 7)

### "I need help with a specific phase"
→ `guides/onboarding/AGENT_HARNESS.md` (all 7 phases with links)

### "Something is broken"
→ `guides/emergency/README.md` (troubleshooting guide)

### "I need to add a new project"
→ `guides/operational/ADDING_NEW_PROJECT.md`

### "I want to learn SDD"
→ Start: `guides/reference/HOW_EACH_LAYER_WORKS.md`

### "I need to organize my context"
→ `CANONICAL/specifications/context-aware-agent-pattern.md` (canonical pattern)

---

**Still can't find it?** → Check [NAVIGATION.md](../../../NAVIGATION.md) for complete index

---

**Last Updated:** April 19, 2026  
**Authority:** SPEC v2.1  
**Location:** `EXECUTION/spec/indices/`
