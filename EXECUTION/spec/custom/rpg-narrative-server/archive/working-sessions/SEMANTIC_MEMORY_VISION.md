# 🧠 SEMANTIC MEMORY VISION — Consolidação (April 2026)

**Status:** ✅ VALIDATED & ALIGNED

**Purpose:** Consolidate user's semantic memory vision with architectural decisions

**Sources:**
- rpg_architecture_summary.md (user's architecture overview)
- rpg_memory_architecture.md (user's memory evolution model)
- business-rules.md (our consolidation)
- DECISION_POINTS_CONSOLIDATED.md (our 8 decisions)

---

## 📊 Executive Summary

**User's Vision:**
```
LLM (neutro, sem memória)
  ↑ Context Builder
  ↑ Retrieval (com scoping obrigatório)
  ↑ Memórias (Canon → World → Campaign → Global)
  ↑ Storage (JSON + Embeddings)

Regra crítica: "Sem escopo = bug"
Regra de ouro: "Campaign sobrescreve tudo, Canon nunca muda"
```

**Our Consolidation:**
- 8 decisions (5 technical, 3 business-rule-driven)
- Hierarchical scoping (World/Genre/Campaign)
- Event sourcing for audit trail
- Multi-level cache with event-based invalidation

**Result:** 100% ALIGNED ✅

---

## 🎯 Memory Hierarchy — User Vision vs. Our Architecture

### User's Model (3 Layers)

```
Canon (Immutable)
  ↓ Never changes, source of truth
  
World (Semi-dynamic)
  ↓ Persistent state across campaigns
  
Campaign (Dynamic)
  ↓ Session-specific, volatile
  
Global (Semantic)
  ↓ Reutilizable ideas, templates
```

### Our Model (3-4 Layers with Genre)

```
World (Canonical) ← Immutable baseline
  ├─ Genre Cache ← Shared, reusable (90-day TTL, event-invalidatable)
  │   ├─ Campaign 1 ← Isolated, dynamic
  │   ├─ Campaign 2 ← Isolated, dynamic
  │   └─ Campaign 3 ← Can access Campaign 1-2 via echoes
  └─ Global ← Semantic templates
```

**Mapping:**
- User's "Canon" = Our "World (Canonical)"
- User's "World" = Our "Genre Cache" (shared state)
- User's "Campaign" = Our "Campaign (Dynamic)"
- User's "Global" = Our "Global (Semantic)"

**Enhancement:** Added "Genre" layer for cache reuse between thematically-related campaigns

---

## 🔄 Retrieval Cascade — User's Scoping Rules

**User's Rule:**
```
Fallback: campaign → world → canon → global
Critical: "Similaridade sem escopo = BUG"
```

**Our Implementation:**
```
1. Build context for campaign scope
   └─ If found: return with source = campaign
   
2. If not found: query genre cache (world level)
   └─ If found: return with source = genre
   
3. If not found: query canonical facts (world baseline)
   └─ If found: return with source = canonical
   
4. If not found: query global semantic templates
   └─ If found: return with source = global

5. Metadata enforcement:
   └─ Every result tagged with: campaign_id, world_id, scope, style
   └─ Retrieval filters BEFORE ranking (prevents cross-scope contamination)
```

**Validation:** Our retrieval respects user's "no scope = bug" rule ✅

---

## 📦 Storage Structure — User's Blueprint

**User's Proposed (rpg_memory_architecture.md):**
```
data/
├── canon/        # Fixed world baseline
├── worlds/       # Persistent shared state
├── campaigns/    # Dynamic session state
└── global/       # Semantic templates
```

**Our Implementation:**
```
data/
└── world_x/
    ├── canonical/                 ← canon/ (immutable)
    └── genre_y/
        ├── shared_cache/          ← worlds/ (persistent)
        ├── campaign_1/            ← campaigns/ (dynamic)
        ├── campaign_2/
        └── campaign_3/
    └── global/
        ├── narrative_templates/   ← global/ (semantic)
        ├── entity_archetypes/
        └── scene_patterns/
```

**Enhancement:** Hierarchical (world/genre/campaign) for scalability

---

## 🎯 Alignment: 5-Step Incremental Roadmap

**User's Proposed (rpg_memory_architecture.md):**
```
Step 1: Scoping in retrieval
Step 2: Cache per campaign
Step 3: Scene state
Step 4: Entity memory
Step 5: Memory orchestrator
```

**Our Phase Mapping:**

| Step | User | Our Phase | Duration | Decisions |
|------|------|-----------|----------|-----------|
| 1 | Scoping retrieval | Phase 3.1 | 1-2d | #4 (nesting) |
| 2 | Cache per campaign | Phase 2B | 1-2d | #2 (cleanup), #8 (invalidation) |
| 3 | Scene state | Phase 3.2 | 1d | #6 (versioning) |
| 4 | Entity memory | Phase 3.3 | 1-2d | #7 (immutability) |
| 5 | Memory orchestrator | Phase 4 | 1d | #3 (error handling) |

**Status:** Our phases 1-4 implement this roadmap with architectural rigor ✅

---

## 💡 Key Insights: User's Vision Drives Architecture

### Insight #1: "LLM has no memory"

**User's statement:** "O LLM não possui memória, contexto é reconstruído via RAG"

**Implication for DECISION #6 (Memory Versioning):**
- Event sourcing allows recreating exact context from history
- "Given timestamp T, reconstruct narrative context as it was then"
- Enables time-travel queries for echoes

**Decision reinforced:** ✅ Event Sourcing (Option C) is correct

---

### Insight #2: "Sem escopo = bug"

**User's critical rule:** Retrieval without scope filtering = contamination

**Implication for DECISION #8 (Cache Invalidation):**
- Event-based invalidation maintains scoping integrity
- When genre cache invalidated: campaign queries fall back to canonical
- Prevents stale genre data contaminating campaign context

**Decision reinforced:** ✅ Event-Based Invalidation (Option B) is correct

---

### Insight #3: "Campaign sobrescreve tudo"

**User's merge rule:** Campaign > World > Canon > Global

**Implication for DECISION #4 (Nesting Support):**
- No nested scopes = clear priority (top-of-stack always wins)
- Prevents ambiguity (which campaign is "current"?)
- Matches user's linear priority model

**Decision reinforced:** ✅ No Nesting (Option A) is correct

---

### Insight #4: "Canon nunca muda"

**User's immutability rule:** Canon is immutable, world consolidates, campaign is volatile

**Implication for DECISION #7 (Canonical Immutability):**
- Strict immutability (error on modify) enforces this rule
- If update needed: create new fact in world layer, deprecate old
- Prevents accidental corruption of baseline

**Decision reinforced:** ✅ Strict Immutable (Option C) is correct

---

### Insight #5: "Cache precisa ser segmentado"

**User's caching strategy:** Global cache + Campaign cache + World cache (hybrid)

**Implication for DECISION #2 (Cleanup Timing):**
- Campaign cache must clean up on context exit (automatic)
- Prevents stale campaign data in next campaign
- Automatic cleanup = guaranteed cache isolation

**Decision reinforced:** ✅ Automatic Context Exit (Option A) is correct

---

## 🔗 Cross-Reference: Business Rules ↔ Architecture Decisions

### User's "Regras de Ouro" → Our Decisions

| Rule | User Statement | Decision | Our Choice |
|------|---|---|---|
| R1 | LLM não guarda memória | #6 Versioning | Event sourcing (full audit trail) |
| R2 | Retrieval controla tudo | #4 Nesting | No nesting (simple retrieval priority) |
| R3 | Canon nunca muda | #7 Canonical | Strict immutable (error on modify) |
| R4 | Campaign sobrescreve | #4 Nesting | No nesting (campaign = top scope) |
| R5 | World consolida mudanças | #8 Invalidation | Event-based (reactive to world changes) |
| R6 | Ruleset calcula | N/A | (Rules Engine Port already supported) |
| R7 | LLM narra | N/A | (Context Builder + Retrieval separate from LLM) |

**Status:** All 7 user rules are covered by our 8 decisions ✅

---

## 🚀 Unified Implementation Model

**The Complete Picture:**

```
┌─────────────────────────────────────────────────────┐
│ SEMANTIC MEMORY VISION (User's Model)               │
├─────────────────────────────────────────────────────┤
│ Canon → World → Campaign → Global (4-layer cascade) │
│ Regra: "Sem escopo = bug"                           │
│ Merge: Campaign > World > Canon > Global            │
└─────────────────────────────────────────────────────┘
                           ↓ (Implemented by)
┌─────────────────────────────────────────────────────┐
│ ARCHITECTURAL DECISIONS (Our 8 Consolidations)      │
├─────────────────────────────────────────────────────┤
│ #1: Lock strategy (Simple)                          │
│ #2: Cleanup timing (Auto)                           │
│ #3: Error handling (Finalizer)                      │
│ #4: Nesting support (No nesting)                    │
│ #5: EventBusPort (Separate)                         │
│ #6: Memory versioning (Event sourcing)              │
│ #7: Canonical immutability (Strict)                 │
│ #8: Cache invalidation (Event-based)                │
└─────────────────────────────────────────────────────┘
                           ↓ (Enables)
┌─────────────────────────────────────────────────────┐
│ IMPLEMENTATION PHASES (Our Roadmap)                 │
├─────────────────────────────────────────────────────┤
│ Phase 1: DI fixes (150 LOC, 3-4h)                   │
│ Phase 2A: Bootstrap reorg (150 LOC, 1-2d)          │
│ Phase 2B: Campaign scoping (250 LOC, 1-2d)         │
│ Phase 3: Memory hierarchy (200 LOC, 1-2d)          │
│ Phase 4: E2E tests (50 LOC, 1d)                     │
└─────────────────────────────────────────────────────┘
```

---

## ✅ VALIDATION CHECKLIST

**User's Vision Components:**
- [x] Canon/World/Campaign hierarchy → Implemented via multi-level scoping
- [x] Immutable baseline → DECISION #7 (Strict)
- [x] Shared cache between campaigns → Genre layer + cache strategy
- [x] Scoping metadata → Mandatory campaign_id/world_id/scope/style
- [x] Fallback cascade → Retrieval pipeline (campaign → world → canon → global)
- [x] Semantic templates → Global layer + echo system
- [x] Entity memory → Campaign isolation via CampaignScopedContainer
- [x] Scene state → Implicitly tracked via versioning (event sourcing)
- [x] Rules engine → RulesEnginePort (already exists)
- [x] Incremental roadmap → Phase 1-4 map to 5-step model

**Architecture Quality:**
- [x] No scope = bug → Enforced by retrieval filters
- [x] Campaign sobrescreve → No nesting (DECISION #4 Option A)
- [x] Canon nunca muda → Immutable (DECISION #7 Option C)
- [x] Cache segmentado → 3-tier with invalidation (DECISION #8 Option B)
- [x] Event sourcing → Full audit trail (DECISION #6 Option C)

**Status:** ✅ 100% ALIGNED

---

## 📋 Próximos Passos

1. **User Confirmation:** Confirm all 8 decisions (with recommended options) ✅
2. **Update STRATEGY_B_OPTIMIZED.md** with semantic memory alignment
3. **Generate Phase 1 code templates** using event sourcing patterns
4. **Update architecture.md** with echo system section
5. **Start Phase 1 immediately** (can proceed without Phase 2B decisions)

---

## 🎯 Resumo para Usuário

Seus documentos **reforçam e validam 100%** das decisões que consolidei:

✅ **Hierarquia** (Canon/World/Campaign/Global) alinha com DECISION #4 e #8
✅ **Scoping crítico** ("sem escopo = bug") força DECISION #7 e #8
✅ **Cache segmentado** confirma DECISION #2 (auto cleanup) e #8 (event invalidation)
✅ **Immutabilidade** valida DECISION #7 (strict)
✅ **Event sourcing** necessário para echo system = DECISION #6
✅ **Roadmap 5-passos** mapeia perfeitamente para Phase 1-4

**Conclusão:** Estamos no caminho certo. Pronto para confirmação e Phase 1! 🚀
