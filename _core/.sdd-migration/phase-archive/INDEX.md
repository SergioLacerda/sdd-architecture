# 📦 Phase Archive - Architectural Decisions

This directory contains the **essential architectural decisions** for v3.0 migration.

**This is NOT a pile of historical files.** It's a curated set of decision records.

---

## 📋 What's Here

```
phase-archive/
├── DECISIONS.md ✨ NEW - Complete decision matrix
├── PHASE_8_AMBIGUITIES_RESOLVED.md - Full architectural justification  
├── PHASE_8_PLANNING.md - Historical context (if needed)
└── INDEX.md (this file)
```

---

## 🎯 Single Source of Truth Structure

| Need | Location | Use Case |
|------|----------|----------|
| **Execute migration** | [../PHASES.md](../PHASES.md) | "How do I run Phase 1?" |
| **Understand decisions** | **DECISIONS.md** | "Why did we choose 3-tier?" |
| **See full justification** | PHASE_8_AMBIGUITIES_RESOLVED.md | "Show me problem + solution + rationale" |
| **Historical context** | PHASE_8_PLANNING.md | "How did we get here?" |

---

## 📌 Key Decisions (Summary)

See **DECISIONS.md** for complete decision matrix, or below for quick reference:

### 1. 3-Tier Model (MANDATE/GUIDELINES/OPERATIONS)
- **Decision:** Three distinct tiers with clear ownership
- **Impact:** Core v3.0 architecture
- **Status:** ✅ v3.0

### 2. 2-Stage Compilation (Override System)
- **Decision:** Core + customizations compiled separately, merged immutably
- **Impact:** Prevents runtime corruption
- **Status:** ✅ v3.0

### 3. Wizard Dynamic Selection
- **Decision:** Three adoption paths (5min/15min/40min)
- **Impact:** Lower entry barrier
- **Status:** ⏳ v3.2 (deferred)

### 4. IDE + Atomic Profiles
- **Decision:** Profiles system with atomic transactions
- **Impact:** Multi-user workflows
- **Status:** ⏳ v3.1

### 5. Feature Flags
- **Decision:** `.sdd-core/features.json` for runtime toggles
- **Impact:** Gradual feature rollout
- **Status:** ✅ v3.0 ready

### 6. Centralized `.sdd/` Root
- **Decision:** Single `.sdd/` directory for all rules
- **Impact:** Single source of truth
- **Status:** ✅ v3.0

---

## 🚀 Quick Navigation

**I want to...**

- **Execute the migration** → Go to [../PHASES.md](../PHASES.md)
- **Understand why we chose X** → Read DECISIONS.md (summary) then PHASE_8_AMBIGUITIES_RESOLVED.md (full)
- **See historical planning** → Read PHASE_8_PLANNING.md
- **Find examples/diagrams** → See PHASE_8_AMBIGUITIES_RESOLVED.md

---

## ✅ What's NOT Here Anymore

**Deleted (redundant/obsolete):**
- ❌ PHASE_3/6/7 (obsolete phases)
- ❌ PHASE_8_IMPLEMENTATION_CHECKLIST* (v3.1-beta.1, not migration)
- ❌ PHASE_8_REAL_WORLD_VALIDATION_STRATEGY (deferred to v3.2)
- ❌ PHASE_8_SDD_WIZARD_SPECIFICATION (deferred to v3.2)
- ❌ Weekly summaries (status artifacts, not decisions)
- ❌ Release announcements/checklists (procedural templates)
- ❌ Planning reviews (decision process, not decisions)

**Result:** Clean archive with only essential decision records

---

## 📖 Files in This Archive

### DECISIONS.md (NEW - Start Here!)
- **Purpose:** Complete decision matrix consolidated from all sources
- **Content:** 6 decisions, rationale, impact, timeline
- **Use:** "I need to understand all the architectural decisions"

### PHASE_8_AMBIGUITIES_RESOLVED.md  
- **Purpose:** Full problem/solution/justification for each ambiguity
- **Content:** OPERATIONS, Override, Wizard, Profiles, Features, Root
- **Use:** "I need deep justification with diagrams and examples"

### PHASE_8_PLANNING.md
- **Purpose:** Historical context - how we got here
- **Content:** Original planning, scope, tradeoffs
- **Use:** "I want to understand the decision-making process"

### INDEX.md (this file)
- **Purpose:** Navigation guide
- **Use:** "I'm lost, where should I go?"

---

## 🎯 Usage Rules

✅ **DO:**
- Reference DECISIONS.md when explaining "why v3.0 looks like this"
- Link to PHASE_8_AMBIGUITIES_RESOLVED.md for full justification
- Use PHASES.md for execution
- Archive this when decisions change (v3.1, v3.2, etc.)

❌ **DON'T:**
- Add new files here without removing old ones (keep it curated!)
- Reference old PHASE_*.md files for decisions (use DECISIONS.md instead)
- Add tactical planning docs (those go to `.sdd-migration/` root)

---

## 🔄 Evolution Path

```
Phase Archive v3.0 (Current):
├── DECISIONS.md (6 decisions for v3.0)
├── PHASE_8_AMBIGUITIES_RESOLVED.md (full justification)
└── PHASE_8_PLANNING.md (historical context)

Phase Archive v3.1 (Future):
├── DECISIONS.md (9 decisions for v3.1)
├── PHASE_8_AMBIGUITIES_RESOLVED.md (v3.0 archived)
├── PHASE_9_DECISIONS_v3.1.md (new decisions)
└── PHASE_8_PLANNING.md (keep for history)

Phase Archive v3.2+ (Future):
├── DECISIONS.md (12+ decisions for v3.2)
├── ARCHIVES/v3.0/ (old decisions archived)
└── ARCHIVES/v3.1/ (old decisions archived)
```

---

## 📊 Archive Statistics

| Metric | Before | After | Benefit |
|--------|--------|-------|---------|
| **Files** | 24 | 4 | -83% clutter |
| **Noise** | High | None | Clear signal |
| **Decision docs** | Scattered | Consolidated | Easy to find |
| **Source of truth** | Multiple | Single | No confusion |

---

## ✅ Validation

This archive is:
- ✅ Minimal (only 4 files)
- ✅ Curated (no redundant files)
- ✅ Linked (points to PHASES.md for execution)
- ✅ Complete (all 6 decisions documented)
- ✅ Single source of truth (reference point for "why")

---

## 📞 Questions?

- **"How do I run the migration?"** → [../PHASES.md](../PHASES.md)
- **"Why did we choose this approach?"** → DECISIONS.md + PHASE_8_AMBIGUITIES_RESOLVED.md  
- **"What's the full justification?"** → PHASE_8_AMBIGUITIES_RESOLVED.md
- **"How did we get here?"** → PHASE_8_PLANNING.md

---

**Archive Status:** ✅ Clean, curated, ready for v3.0  
**Last Updated:** April 21, 2026  
**Next Review:** Before v3.1 decisions (June 2026)
