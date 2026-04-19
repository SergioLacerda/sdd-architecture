# 📋 DOC CONSOLIDATION PLAN (April 18, 2026)

## 📊 Inventory

**Total docs:** 94 files

**Current structure:**
- `/docs/ia/` = Governance + Specs (GOOD)
- `/docs/ia/todo/` = Legacy/Working docs (NEEDS CLEANUP)
- `/docs/en/`, `/docs/pt-br/` = Old duplicates (ARCHIVE)
- `/docs/` root = Old docs (ARCHIVE)

---

## 🎯 CONSOLIDATION STRATEGY

### PHASE 1: Segregate

**Keep (Current State - Needed for Development):**
```
/docs/ia/
├── MASTER_INDEX.md (entry point)
├── ia-rules.md (mandatory execution rules - 16 protocols)
├── GOVERNANCE_RULES.md (immutable layer)
├── RUNTIME_STATE.md (current state)
│
├── specs/ (HOW IT SHOULD BE)
│   ├── constitution.md (immutable principles)
│   ├── _shared/
│   │   ├── architecture.md (8-layer design) ✅ UPDATED
│   │   ├── business-rules.md (memory hierarchy) ✅ NEW
│   │   ├── contracts.md (18 ports)
│   │   ├── conventions.md (naming, style)
│   │   ├── glossary.md (terminology)
│   │   ├── feature-checklist.md (8-layer process)
│   │   ├── testing.md (test patterns)
│   │   └── definition_of_done.md (merge criteria)
│   ├── runtime/
│   │   ├── execution_state.md (current state)
│   │   └── threads/TEMPLATE.md (thread format)
│   └── _INDEX_BY_DOMAIN.md (navigate by feature)
│
├── decisions/ (ADRs 1-6 - WHY)
│   ├── ADR-001.md (Clean Architecture 8-layer)
│   ├── ADR-002.md (Async-first, no blocking)
│   ├── ADR-003.md (Ports & Adapters - 18 ports)
│   ├── ADR-004.md (Vector black-box factory)
│   ├── ADR-005.md (Thread isolation 2 levels)
│   └── ADR-006.md (Event sourcing append-only)
│
├── guides/ (HOW TO USE)
│   ├── onboarding/ (FIRST SESSION)
│   ├── implementation/ (BUILD)
│   ├── navigation/ (FIND)
│   └── reference/ (FAQ, GLOSSARY)
│
└── current-system-state/ (WHAT EXISTS NOW)
    ├── _INDEX.md (adaptive query router)
    ├── rag_pipeline.md (real RAG - 8 components)
    ├── services.md (8 services + flows)
    ├── contracts.md (9 Ports, guarantees)
    ├── storage_limitations.md (constraints)
    ├── threading_concurrency.md (limits)
    ├── scaling_constraints.md (bottlenecks)
    ├── known_issues.md (11 bugs)
    └── data_models.md (DTOs, API, storage)
```

**Move to Archive (Not needed during development):**
```
/docs/LEGACY/  (keep for reference only)
├── en/ (old English docs)
├── pt-br/ (old Portuguese docs)
├── old_architecture/ (pre-consolidation)
├── superseded/ (old analysis)
└── reference_only/ (historical)
```

**Move to Archive - Working Docs (Completed but keep for reference):**
```
/docs/ia/ARCHIVE/working-sessions/
├── CONSOLIDATION_QUALITY_AUDIT.md (analysis - use insights, remove file)
├── SPEC_FIXES_APRIL_2026.md (fixed - insights moved to specs)
├── DECISIONS_EXPLAINED_PRACTICAL.md (use for context, consolidate)
├── DECISIONS_REFACTORED_FUNCTIONAL.md (final, consolidate)
├── DECISION_POINTS_CONSOLIDATED.md (use for context, consolidate)
├── SEMANTIC_MEMORY_VISION.md (insights merged to business-rules.md)
└── todo/ (remove all - consolidate into execution_state.md)
```

---

## 🔄 CONSOLIDATION ACTIONS

### Action 1: Create Archive Structure

**Create:**
- `/docs/ia/ARCHIVE/` - For completed analysis (read-only reference)
- `/docs/LEGACY/` - For old docs (not loaded during development)

### Action 2: Consolidate Decision Analysis

**Current (4 files, 2000+ lines):**
- DECISIONS_EXPLAINED_PRACTICAL.md
- DECISIONS_REFACTORED_FUNCTIONAL.md
- DECISION_POINTS_CONSOLIDATED.md
- CONSOLIDATION_QUALITY_AUDIT.md

**Consolidate into:**
- `/docs/ia/decisions/DECISIONS_APRIL_2026.md` (500 lines)
  - 8 functional decisions
  - Mapping to ADRs
  - Setup-agnnostic rationale
  - World class patterns

### Action 3: Update MASTER_INDEX.md

**Add:**
- Clear "CURRENT STATE" vs "ARCHIVE" distinction
- Direct paths to 8 decisions
- Optimized context loading

### Action 4: Consolidate execution_state.md

**Move into execution_state.md:**
- All "Next Actions" from todo files
- Active decisions (8 points)
- Phase 1-4 status
- Checkpoint data

### Action 5: Remove /docs/ia/todo/ entirely

**Move to execution_state.md:**
- DAILY_CHECKLIST → execution_state.md checkpoint
- STRATEGY_B_OPTIMIZED.md → Phase summary in execution_state.md
- base/ analysis → insights kept, files removed

---

## 📐 NEW OPTIMIZED STRUCTURE (Post-Consolidation)

```
/docs/ia/                              ← CURRENT STATE (Loaded)
├── README.md                          ← Quick entry point
├── MASTER_INDEX.md                    ← Complete map
├── ia-rules.md                        ← 16 mandatory protocols
├── GOVERNANCE_RULES.md                ← Immutable layer
├── RUNTIME_STATE.md                   ← Updated with all decisions
│
├── specs/                             ← SPEC LAYER
│   ├── constitution.md
│   ├── _shared/
│   │   ├── architecture.md (UPDATED)
│   │   ├── business-rules.md
│   │   ├── contracts.md
│   │   ├── conventions.md
│   │   ├── glossary.md
│   │   ├── feature-checklist.md
│   │   ├── testing.md
│   │   └── definition_of_done.md
│   ├── runtime/
│   │   ├── execution_state.md (EXPANDED)
│   │   └── threads/TEMPLATE.md
│   └── _INDEX_BY_DOMAIN.md
│
├── decisions/                         ← ADRs (WHY)
│   ├── ADR-001.md
│   ├── ADR-002.md
│   ├── ADR-003.md
│   ├── ADR-004.md
│   ├── ADR-005.md
│   ├── ADR-006.md
│   └── DECISIONS_APRIL_2026.md        ← CONSOLIDATED (NEW)
│
├── guides/                            ← HOW TO USE
│   ├── onboarding/
│   ├── implementation/
│   ├── navigation/
│   └── reference/
│
├── current-system-state/              ← WHAT EXISTS
│   └── (all 9 files)
│
└── ARCHIVE/                           ← REFERENCE ONLY (Not loaded)
    └── working-sessions/
        ├── analysis-april-2026.md
        ├── consolidation-insights.md
        └── [old files]

/docs/LEGACY/                          ← OLD DOCS (Not loaded)
├── en/
├── pt-br/
└── old-analysis/
```

---

## ⏱️ TOKEN EFFICIENCY GAINS

**Before consolidation:**
- 94 files scattered
- User loads wrong docs (bloat)
- Redundant analysis repeated
- Legacy confuses development

**After consolidation:**
```
Core Development (loaded):
  ├── ia-rules.md (8 KB) - Rules only, not discussion
  ├── MASTER_INDEX.md (5 KB) - Entry point only
  ├── specs/ (150 KB) - Pure SPEC, no repetition
  ├── decisions/ (80 KB) - Pure ADR decisions
  ├── guides/ (100 KB) - Implementation guides
  ├── current-system-state/ (60 KB) - System reality
  └── RUNTIME_STATE.md (30 KB) - Current state
     ─────────────────
     TOTAL: ~433 KB (lean, focused)

NOT loaded (reference only):
  ├── ARCHIVE/ (200 KB)
  └── LEGACY/ (300+ KB)
     ─────────────────
     REFERENCE: ~500+ KB (not in development context)

Savings: 60% reduction in active context during development
```

---

## 📋 CHECKLIST

### Files to Remove (move to ARCHIVE or LEGACY)

Current `/docs/ia/` root files to archive:
- ❌ DECISIONS_EXPLAINED_PRACTICAL.md → ARCHIVE/analysis/
- ❌ DECISIONS_REFACTORED_FUNCTIONAL.md → ARCHIVE/analysis/
- ❌ DECISION_POINTS_CONSOLIDATED.md → ARCHIVE/analysis/
- ❌ CONSOLIDATION_QUALITY_AUDIT.md → ARCHIVE/analysis/
- ❌ SEMANTIC_MEMORY_VISION.md → Merged into business-rules.md, archive summary
- ❌ SPEC_FIXES_APRIL_2026.md → ARCHIVE/analysis/

Current `/docs/ia/todo/` directory:
- ❌ Remove entire tree → Move to ARCHIVE/todo-sessions/

Old `/docs/` (en/, pt-br/, c4_architecture.md, etc.):
- ❌ Move all to LEGACY/

### Files to Update

- ✅ RUNTIME_STATE.md → Add 8 decisions + Phase status
- ✅ MASTER_INDEX.md → Add new decision location
- ✅ architecture.md (specs/) → Already updated ✓
- ✅ business-rules.md (specs/) → Already created ✓
- ✅ execution_state.md → Consolidate decisions + checkpoints

### Files to Create

- ✅ /docs/ia/decisions/DECISIONS_APRIL_2026.md (consolidate 4 files)
- ✅ /docs/ia/README.md (quick start)
- ✅ /docs/ia/ARCHIVE/README.md (what went here + why)
- ✅ /docs/LEGACY/README.md (historical reference)

---

## 🚀 EXECUTION ORDER

1. **Create archive directories** (5 min)
2. **Create DECISIONS_APRIL_2026.md** (consolidate 4 files, 10 min)
3. **Update execution_state.md** (add decisions + checkpoints, 10 min)
4. **Update MASTER_INDEX.md** (new paths, 5 min)
5. **Move files to ARCHIVE/** (20 min)
6. **Move /docs/ to LEGACY/** (10 min)
7. **Create README files** (5 min)
8. **Remove /docs/ia/todo/** (5 min)
9. **Verify structure** (5 min)

**Total: ~75 minutes**

---

## ✅ RESULT

**Optimized for Phase 1 Implementation:**
- ✅ Specs are pure (no noise)
- ✅ Decisions are consolidated (easy to reference)
- ✅ Current state is clear (execution_state.md)
- ✅ Legacy is segregated (not confusing)
- ✅ Token efficiency (60% reduction)
- ✅ Ready for code generation

---

**Ready to execute consolidation? 🚀**
