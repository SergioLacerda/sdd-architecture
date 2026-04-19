# 📚 MASTER INDEX — Start Here

**🎯 Entry Point for All Governance Documentation**

This is your starting point for everything related to:
- Architecture & design patterns
- Implementation process & guidelines
- Testing strategies & validation
- **Reactive, query-driven documentation** (segregated by domain)
- Token/context optimization

---
# 🚨 CRITICAL ISSUE IDENTIFIED & FIXED

## Problem: Canonical ↔ Runtime Coupling

We identified acoplamento between:
- GOVERNANCE_RULES.md + RUNTIME_STATE.md (mixed concepts)
- execution_state.md + current-system-state/ (ambiguous purpose)
- No clear separation of authority vs observation

**Result:** ❌ Ambiguity about "which file is the truth?"

## Solution: 4-Layer Architecture (World-Class Engineering)

→ **[SPEC_CANONICAL_REALITY_DEVELOPMENT.md](./SPEC_CANONICAL_REALITY_DEVELOPMENT.md)** (30 minutes)
- **The Pattern:** CANONICAL / REALITY / DEVELOPMENT / ARCHIVE
- **The Problem:** Current coupling explained clearly
- **The Solution:** No ambiguity, clear authority per layer
- **Status:** ✅ Ready to implement

→ **[CRITIQUE_WORLDCLASS_ENGINEERING.md](./CRITIQUE_WORLDCLASS_ENGINEERING.md)** (20 minutes)
- **Analysis:** 8 critical problems with current structure
- **Improvements:** 8 world-class engineering additions
- **Priority Matrix:** P1/P2/P3 implementation path
- **Impact:** 90% ambiguity reduction

→ **[IMPLEMENTATION_4LAYER_SEPARATION.md](./IMPLEMENTATION_4LAYER_SEPARATION.md)** (Reference)
- **8 Phases:** Exactly how to migrate
- **Timeline:** 4 hours, backward compatible
- **Checklist:** What to move where
- **Verification:** How to validate success

**Recommendation:** Read SPEC first, then implement

---
## 🌍 DOCUMENTATION DOMAINS

Our documentation is **segregated by domain and query-driven**:

| Domain | Location | Audience | Purpose |
|--------|----------|----------|---------|
| **IA** | `/docs/ia/` | AI agents, code gen | SPEC-driven, focused |
| **System (EN)** | `/docs/en/` | End-users, developers | Tutorials, reference |
| **System (PT)** | `/docs/pt-br/` | Portuguese speakers | Localized content |

→ **[DOMAIN_ORGANIZATION.md](./DOMAIN_ORGANIZATION.md)** — How `/docs/ia/` is organized  
→ **[specs/_shared/reactive_documentation.md](./specs/_shared/reactive_documentation.md)** — Full SPEC

---

# 🔴 MANDATORY STARTUP (Read this first!)

## ⚠️ NEW AGENT SESSION?

**Before ANYTHING else:**

1. **Read (MANDATORY)**: [CANONICAL/rules/ia-rules.md](./CANONICAL/rules/ia-rules.md) — 16 execution protocols you MUST follow
2. **Then read**: [guides/onboarding/FIRST_SESSION_SETUP.md](./guides/onboarding/FIRST_SESSION_SETUP.md) — 20-minute orientation + validation quiz
3. **Take the QUIZ**: [guides/onboarding/VALIDATION_QUIZ.md](./guides/onboarding/VALIDATION_QUIZ.md) — 5-10 min (mandatory)
   - Need ≥80% to pass
   - Run: `python docs/ia/scripts/validate_quiz.py` (for AI agents)
   - Results logged to `_quiz_tracking.json`

After these 3 steps, you'll know:
- ✅ Where you are in the documentation structure
- ✅ What rules you must follow (non-negotiable)
- ✅ **VALIDATED** your understanding of core protocols ✨
- ✅ How to choose your work PATH
- ✅ What context to load (optimized for your task)
- ✅ How to avoid common mistakes

**Time**: 20 minutes total (15 min setup + 5-10 min validation)  
**Important**: Don't skip this, don't guess
**Validation**: Must pass quiz (≥80%) before proceeding

---

# 🏗️ Understand the Structure

## 4-Layer Architecture (Immutable Structure)

**→ [CANONICAL/](./CANONICAL/)** (Authority ✅)
- Immutable rules, specifications, and decisions
- **What's in here:** ia-rules.md, constitution.md, contracts.md, architecture.md, ADRs 1-6
- **Update frequency:** Rare (ADR process)
- **Authority:** YES — these define the ideal

**→ [REALITY/](./REALITY/)** (Observation 🟡)
- Current gaps, constraints, and observed limitations
- **What's in here:** current-system-state/, known_issues.md, storage_limitations.md
- **Update frequency:** Moderate (when new constraints discovered)
- **Authority:** CONTEXT — documents what we've found

**→ [DEVELOPMENT/](./DEVELOPMENT/)** (Active Work 🟢)
- Real-time work in progress (ephemeral, high-churn)
- **What's in here:** execution-state/, threads/, decisions-in-progress/, blockers-and-risks/
- **Update frequency:** Real-time during active work
- **Authority:** NONE — for coordination only

**→ [ARCHIVE/](./ARCHIVE/)** (History 🟣)
- Historical record, completed threads, deprecated decisions
- **What's in here:** working-sessions/, deprecated-decisions/, legacy-documentation/
- **Update frequency:** Low (only when threads complete)
- **Authority:** NONE — read-only history

**Key insight**: Governance answers "What's RIGHT?" | Runtime answers "What's NOW?" | Decisions answer "Why?"

---

# ⚡ Quick Navigation

## 📍 NEW: Understand Documentation Structure
→ **[DOMAIN_ORGANIZATION.md](./DOMAIN_ORGANIZATION.md)** (10 minutes)
- How `/docs/ia/` is organized by topic
- 5 domains: Governance, Specs, Current Reality, Guides, Reference
- Query router: "I need X, go to Y"
- Reactive loading examples
- **New to project?** → Start here

## ♻️ NEW: Reactive Documentation Strategy
→ **[specs/_shared/reactive_documentation.md](./specs/_shared/reactive_documentation.md)** (SPEC, 15 minutes)
- Why we segregate documentation by domain
- Query-driven loading examples
- Load 50-80% less context per query
- Focus on signal, eliminate noise

## 🎯 APRIL 2026: 8 Decisions Ready for Implementation
→ **[decisions/DECISIONS_APRIL_2026.md](./decisions/DECISIONS_APRIL_2026.md)** (15 minutes)
- ✅ 8 consolidated functional decisions
- ✅ All ADRs mapped and validated
- ✅ World-class patterns explained
- ✅ Ready for Phase 1 coding
- **Start here if implementing Phase 1** → All decisions in one file

## 🚀 Ready to Implement?
→ **[guides/onboarding/QUICK_START.md](./guides/onboarding/QUICK_START.md)** (3 minutes)
- Decide your PATH (bug fix, simple feature, complex, multi-thread)
- Load only the docs you need (reactive loading)
- Start implementing immediately

---

# ⚡ Quick Navigation (Continued)

## 🎯 Want to Understand the Vision?
→ **[guides/context/YOUR_VISION_IMPLEMENTED.md](./guides/context/YOUR_VISION_IMPLEMENTED.md)** (15 minutes)
- See how "consulta sob medida" was implemented
- Examples: 60% context savings (bug fix) to 75% (multi-thread)
- Practical scenarios fully explained

## 📖 Need Something Specific?
→ **[guides/navigation/INDEX.md](./guides/navigation/INDEX.md)** (Master Reference)
- "I need X, where do I go?" quick lookup
- 30+ questions mapped to docs
- Document matrix with categories

## 📚 See Guides Structure
→ **[guides/README.md](./guides/README.md)** (Organization Guide)
- How guides are organized
- What each category contains
- How to navigate

## 🎓 Understanding the Architecture
→ **[specs/_INDEX_BY_DOMAIN.md](./specs/_INDEX_BY_DOMAIN.md)** (Specs by Domain)
- Governance by conceptual domain
- Pattern specifications
- Quality standards
- Where to find each thing

## 📈 Spec Dependencies
→ **[specs/DEPENDENCIES.md](./specs/DEPENDENCIES.md)** (How Specs Work Together)
- Feature implementation flow
- Cross-reference matrix
- Testing dependencies
- Update sequence

---

# 📁 Directory Structure

```
/
├── ai-rules.md ⭐ (MOVED TO ROOT)
│   └── 16 execution protocols for agents
│
├── YOUR_VISION_IMPLEMENTED.md ⭐ (KEY DOCUMENT)
│   └── How your vision was fully realized
│
└── docs/ia/
    ├── guides/ 📚 (ALL NAVIGATION & GUIDES HERE)
    │   ├── QUICK_START.md ⚡ (3-minute start)
    │   ├── INDEX.md (master reference)
    │   ├── IMPLEMENTATION_ROADMAP.md (9-step process)
    │   ├── ADAPTIVE_CONTEXT_LOADING.md (how it works)
    │   ├── DELIVERY_SUMMARY.md (what was built)
    │   ├── FILES_DELIVERED.md (complete list)
    │   ├── FINAL_STATUS.md (completion checklist)
    │   ├── SYSTEM_ARCHITECTURE_VISUAL.md (flowcharts)
    │   ├── IMPLEMENTATION_FLOW_ANALYSIS.md (audit)
    │   ├── IMPLEMENTATION_PROCESS_MAP.md (visual map)
    │   ├── TESTING_EVALUATION_SUMMARY.md (test eval)
    │   └── TESTING_STRATEGY_CLARIFICATION.md (testing docs)
    │
    └── specs/ 📋 (CORE GOVERNANCE - UNCHANGED)
        ├── constitution.md (immutable principles)
        ├── design-decisions.md (architecture decisions)
        ├── ai-rules.md (was here, moved to root)
        ├── _shared/
        │   ├── architecture.md (clean architecture)
        │   ├── feature-checklist.md (8-layer guide)
        │   ├── testing.md (test patterns)
        │   ├── testing_strategy_spec.md (test rules)
        │   ├── conventions.md (naming)
        │   └── definition_of_done.md (merge criteria)
        └── runtime/
            ├── execution_state.md (current work)
            └── threads/TEMPLATE.md (thread format)

    └── current-system-state/ 🔍 (IS/AS-IS - Real Behavior)
        ├── _INDEX.md (navigation for specialized queries)
        ├── rag_pipeline.md (real RAG flow, 8 components)
        ├── services.md (8 core services, orchestration)
        ├── contracts.md (9 Ports, guarantees)
        ├── storage_limitations.md (5 storage constraints)
        ├── threading_concurrency.md (5 async/concurrency limits)
        ├── scaling_constraints.md (5 scaling bottlenecks)
        ├── known_issues.md (11 bugs + edge cases)
        └── data_models.md (DTOs, API schemas, storage format)
```

---

# 🎯 By Role/Need

### I'm an AI Agent Implementing a Feature
1. Read: [QUICK_START.md](./docs/ia/guides/QUICK_START.md) (3 min)
2. Choose: Your work type (bug/simple/complex/multi)
3. Load: Phase 1 + PATH-specific docs
4. Follow: Implementation guides
5. Done: Ready for merge ✅

### I'm a Code Reviewer
1. Read: [/docs/ia/CANONICAL/specifications/definition_of_done.md](./docs/ia/CANONICAL/specifications/definition_of_done.md)
2. Check: All applicable criteria
3. Validate: Architecture compliance
4. Approve: When all ✅

### I'm a New Team Member
1. Read: [YOUR_VISION_IMPLEMENTED.md](./YOUR_VISION_IMPLEMENTED.md)
2. Read: [/docs/ia/guides/IMPLEMENTATION_ROADMAP.md](./docs/ia/guides/IMPLEMENTATION_ROADMAP.md)
3. Do: First feature using QUICK_START.md

### I'm an Architect
1. Read: [/docs/ia/CANONICAL/rules/constitution.md](./docs/ia/CANONICAL/rules/constitution.md)
2. Read: [/docs/ia/CANONICAL/specifications/architecture.md](./docs/ia/CANONICAL/specifications/architecture.md)
3. Review: [/docs/ia/guides/DELIVERY_SUMMARY.md](./docs/ia/guides/DELIVERY_SUMMARY.md)
4. Oversee: Via `/docs/ia/DEVELOPMENT/execution-state/_current.md`

---

# 🚀 The 4 Adaptive Paths

Your work determines which docs you load:

```
PATH A: Bug Fix (1.5h)
├─ Load: ~40KB context (60% savings!)
├─ For: Fixing single-layer bugs
└─ Docs: Phase 1 + affected layer

PATH B: Simple Feature (2h)
├─ Load: ~45KB context (55% savings!)
├─ For: Features using 1-2 layers
└─ Docs: Phase 1 + layers 1-3

PATH C: Complex Feature (3-4h)
├─ Load: ~85KB context (15% savings)
├─ For: Features using 3+ layers
└─ Docs: Phase 1 + all docs needed

PATH D: Multi-Thread (variable)
├─ Load: Isolated per thread (~75% total savings!)
├─ For: Parallel development
└─ Docs: Only your thread's section + phase 1
```

---

# 📊 Key Files Map

| File | Purpose | Read Time | Location |
|------|---------|-----------|----------|
| **DECISIONS_APRIL_2026.md** | 8 final decisions for Phase 1 | 15 min | `/docs/ia/CANONICAL/decisions/` |
| **QUICK_START.md** | Choose your path | 3 min | `/docs/ia/guides/` |
| **YOUR_VISION_IMPLEMENTED.md** | See vision realized | 15 min | Root (this repo) |
| **INDEX.md** | Find anything | Varies | `/docs/ia/guides/` |
| **constitution.md** | Immutable rules | 20 min | `/docs/ia/CANONICAL/rules/` |
| **ia-rules.md** | Execution protocols | 15 min | `/docs/ia/CANONICAL/rules/` |
| **architecture.md** | Design patterns | 30 min | `/docs/ia/CANONICAL/specifications/` |
| **feature-checklist.md** | Implementation | 25 min | `/docs/ia/CANONICAL/specifications/` |
| **testing.md** | Test patterns | 20 min | `/docs/ia/CANONICAL/specifications/` |
| **definition_of_done.md** | Merge criteria | 20 min | `/docs/ia/CANONICAL/specifications/` |
| **execution_state.md** | Current work | 5 min | `/docs/ia/DEVELOPMENT/execution-state/` |

---

# ✅ What's New

**3 New Architecture Documents** (April 2026 - Reactive Segregation):
1. ✅ **DOMAIN_ORGANIZATION.md** — How `/docs/ia/` is organized by domain + query router
2. ✅ **reactive_documentation.md** — SPEC mandate on segregated, reactive documentation
3. ✅ **CONSOLIDATION_SUMMARY.md** — Consolidation results & token efficiency gains

**Documentation Domains Clarified:**
- ✅ `/docs/ia/` = **IA First** (SPEC-driven, query-reactive)
- ✅ `/docs/en/` = **System Documentation** (end-user/developer focused)
- ✅ `/docs/pt-br/` = **System Documentation** (Portuguese localized)

**7 Guidance Documents** (in `/docs/ia/guides/`):
1. ✅ QUICK_START.md — 3-minute decision tree
2. ✅ ADAPTIVE_CONTEXT_LOADING.md — Complete explanation
3. ✅ DELIVERY_SUMMARY.md — What was built
4. ✅ SYSTEM_ARCHITECTURE_VISUAL.md — Flowcharts
5. ✅ FILES_DELIVERED.md — Complete list
6. ✅ FINAL_STATUS.md — Completion status
7. ✅ TESTING_STRATEGY_CLARIFICATION.md — Testing guidance

**2 Enhanced Existing Documents**:
1. ✅ INDEX.md — Updated with 5 new entry points
2. ✅ IMPLEMENTATION_ROADMAP.md — Added 4 adaptive paths

---

# 💡 Your "Consulta Sob Medida"

**What it means:**
"Adaptive consultation where agents load ONLY necessary docs based on work type"

**How it works:**
```
Agent starts → Identifies work type → Chooses PATH
    ↓
Loads Phase 1 (mandatory)
    ↓
Loads PATH-specific docs (only relevant)
    ↓
Implements with clear guidance
    ↓
Result: 50-85% context savings!
```

---

# 🎉 Ready?

**Pick your starting point:**

- ⚡ **In a hurry?** → [QUICK_START.md](./docs/ia/guides/QUICK_START.md) (3 min)
- 🎯 **Want the full picture?** → [YOUR_VISION_IMPLEMENTED.md](./YOUR_VISION_IMPLEMENTED.md) (15 min)
- 📖 **Need to find something?** → [/docs/ia/guides/INDEX.md](./docs/ia/guides/INDEX.md) (lookup)
- 📊 **Want overview?** → [/docs/ia/guides/DELIVERY_SUMMARY.md](./docs/ia/guides/DELIVERY_SUMMARY.md) (15 min)

---

**Everything you need is here. Pick a document and go! 🚀**
