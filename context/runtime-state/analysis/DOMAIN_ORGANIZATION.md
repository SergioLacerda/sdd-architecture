# `/docs/ia/` — Domain-Segregated Organization

**SPEC Mandate:** Reactive, query-driven documentation segregation

---

## 📍 Directory Map by Domain

### **Domain 1: GOVERNANCE** — Rules, Principles, Immutable Decisions
For: "Why do we do it this way?"

```
/docs/ia/
├─ MASTER_INDEX.md              ← Entry point (query router)
├─ ia-rules.md                  ← 16 execution protocols (MANDATORY)
├─ GOVERNANCE_RULES.md          ← Governance layer
├─ RUNTIME_STATE.md             ← Mutable runtime + classification matrix
│
├─ decisions/
│  ├─ ADR-001.md                ← Why clean architecture 8-layer
│  ├─ ADR-002.md                ← Why async-first
│  ├─ ADR-003.md                ← Why ports & adapters
│  ├─ ADR-004.md                ← Why black-box factory pattern
│  ├─ ADR-005.md                ← Why thread isolation (2 levels)
│  └─ ADR-006.md                ← Why event sourcing append-only
```

**Query Examples:**
- "Why this architecture?" → ADR-001 to ADR-006
- "What are the rules?" → ia-rules.md (16 protocols)
- "What's the current state?" → RUNTIME_STATE.md

**Typical Load:** 15-40 KB per query

---

### **Domain 2: SPECS** — How It SHOULD Be Built
For: "Implement this correctly"

```
/docs/ia/specs/
│
├─ constitution.md              ← Immutable principles
│
├─ _shared/                      ← Shared architectural rules
│  ├─ architecture.md            ← 8-layer design + multi-level scoping
│  ├─ business-rules.md          ← Memory hierarchy, echoes, cache strategy
│  ├─ contracts.md               ← 18 port definitions & guarantees
│  ├─ conventions.md             ← Naming, style, patterns
│  ├─ reactive_documentation.md  ← ✨ This segregation strategy
│  │
│  ├─ feature-checklist.md       ← 8-layer process for new features
│  ├─ feature-template.md        ← Template for new features
│  ├─ design-decisions.md        ← How to document decisions
│  ├─ testing.md                 ← Test patterns (port mocking, etc)
│  ├─ definition_of_done.md      ← Merge criteria checklist
│  │
│  ├─ glossary.md                ← Terminology
│  ├─ project-structure.md       ← Codebase layout
│  └─ [other].md                 ← Topic-specific rules
│
├─ runtime/
│  ├─ execution_state.md         ← Current work + checkpoints
│  ├─ checkpoints/
│  │  └─ TEMPLATE.md             ← Template for checkpoints
│  └─ threads/
│     └─ TEMPLATE.md             ← Template for thread work
│
├─ _INDEX_BY_DOMAIN.md           ← This file: organize by query type
└─ DEPENDENCIES.md               ← Which specs depend on which
```

**Query Examples:**
- "How do I implement X?" → feature-checklist.md (process)
- "What's the architecture?" → architecture.md (full design)
- "How do I test?" → testing.md (patterns & examples)
- "What's the port I need?" → contracts.md (18 port definitions)
- "Am I done with PR?" → definition_of_done.md (checklist)

**Typical Load:** 25-80 KB per query

---

### **Domain 3: CURRENT REALITY** — What Actually Exists
For: "How does it work NOW?"

```
/docs/ia/current-system-state/
│
├─ _INDEX.md                    ← Adaptive query router
├─ rag_pipeline.md              ← 8 components, flows, data models
├─ services.md                  ← 8 services, interactions
├─ contracts.md                 ← 9 ports currently implemented
├─ storage_limitations.md       ← Constraints & workarounds
├─ threading_concurrency.md     ← Current threading model
├─ scaling_constraints.md       ← Bottlenecks, limits
├─ known_issues.md              ← 11 bugs, workarounds
└─ data_models.md               ← DTOs, API schemas, storage schemas
```

**Query Examples:**
- "How does RAG work now?" → rag_pipeline.md
- "What services exist?" → services.md
- "What's the bug?" → known_issues.md
- "Can I scale this?" → scaling_constraints.md
- "What's the limit?" → storage_limitations.md

**Typical Load:** 30-60 KB per query

---

### **Domain 4: GUIDES** — How To USE These Specs
For: "Teach me the process"

```
/docs/ia/guides/
│
├─ onboarding/
│  ├─ README.md                 ← What guides exist
│  ├─ FIRST_SESSION_SETUP.md    ← 15-min orientation
│  ├─ QUICK_START.md            ← 3-min PATH choice (A/B/C/D)
│  ├─ VALIDATION_QUIZ.md        ← 5 questions (80% pass required)
│  ├─ SESSION_QUICK_REFERENCE.md ← Printable card
│  └─ IMPLEMENTATION_NOTES.md   ← Important notes
│
├─ implementation/
│  ├─ IMPLEMENTATION_ROADMAP.md ← Step-by-step phases
│  ├─ IMPLEMENTATION_FLOW_ANALYSIS.md ← Data flow diagrams
│  ├─ IMPLEMENTATION_PROCESS_MAP.md ← Process visualization
│  ├─ ADAPTIVE_CONTEXT_LOADING.md ← How to load context efficiently
│  └─ TROUBLESHOOTING.md        ← Common issues + solutions
│
├─ navigation/
│  ├─ INDEX.md                  ← "I need X, where do I go?"
│  └─ [topic guides]
│
├─ context/
│  ├─ DELIVERY_SUMMARY.md       ← What was delivered
│  ├─ YOUR_VISION_IMPLEMENTED.md ← How user vision maps to architecture
│  ├─ FINAL_STATUS.md           ← Completion status
│  ├─ FILES_DELIVERED.md        ← All files created/updated
│  └─ SYSTEM_ARCHITECTURE_VISUAL.md ← Diagrams & visuals
│
└─ reference/
   ├─ README.md                 ← Reference docs overview
   ├─ FAQ.md                    ← Common questions
   ├─ TESTING_EVALUATION_SUMMARY.md ← Testing analysis
   └─ TESTING_STRATEGY_CLARIFICATION.md ← Strategy details
```

**Query Examples:**
- "New to this project?" → onboarding/QUICK_START.md (3 min)
- "How do I implement?" → implementation/IMPLEMENTATION_ROADMAP.md
- "Where's feature X?" → navigation/INDEX.md
- "Common issues?" → implementation/TROUBLESHOOTING.md

**Typical Load:** 10-30 KB per query (focused guides)

---

### **Domain 5: REFERENCE** — Historical & Archive
For: "This is for reference, rarely needed"

```
/docs/ia/
├─ ARCHIVE/
│  └─ working-sessions/         ← Previous analysis (4+ files archived)
│
└─ LEGACY/                       ← See /docs/LEGACY/
```

**Query Examples:**
- "How was this decided?" → ARCHIVE/working-sessions/
- "What's the history?" → LEGACY/ (old docs)

**Typical Load:** 0 KB for most queries (reference only)

---

## 🎯 Query Router Examples

**Query: "I need to implement EventBusPort"**
```
Domain: SPECS (how to build)
Load:
  1. contracts.md           ← EventBusPort definition (8 KB)
  2. architecture.md        ← Where it integrates (6 KB)
  3. testing.md             ← EventBus test patterns (5 KB)
  4. definition_of_done.md  ← Validation checklist (3 KB)
Total: ~22 KB (focused implementation)
```

**Query: "Why did we choose this architecture?"**
```
Domain: GOVERNANCE (why)
Load:
  1. ADR-001 to ADR-006     ← 6 decisions (15 KB)
  2. constitution.md        ← Principles (5 KB)
Total: ~20 KB (decision context)
```

**Query: "What's broken in the system?"**
```
Domain: CURRENT REALITY (what is)
Load:
  1. known_issues.md        ← 11 bugs (10 KB)
  2. current-system-state/  ← Specific issue details (15 KB)
Total: ~25 KB (issue diagnosis)
```

**Query: "How do I build something new?"**
```
Domain: SPECS + GUIDES (how + process)
Load:
  1. feature-checklist.md   ← 8-layer process (8 KB)
  2. architecture.md        ← Reference design (6 KB)
  3. testing.md             ← Test each layer (5 KB)
  4. definition_of_done.md  ← Done criteria (3 KB)
Total: ~22 KB (development context)
```

---

## 📊 Load Recommendations

| Use Case | Primary Domain | Size | Time |
|----------|----------------|------|------|
| Fix bug | CURRENT REALITY | 25-40 KB | 10 min |
| Implement feature | SPECS + GUIDES | 40-70 KB | 20 min |
| Understand why | GOVERNANCE | 15-30 KB | 10 min |
| New to project | GUIDES | 30-50 KB | 30 min |
| All context (rare) | All domains | 500+ KB | full session |

---

## ✅ Maintenance Rules

**Domain Owners (SPEC Mandates):**

- **GOVERNANCE:** Never changes after decision (locked)
- **SPECS:** Updates only when architecture changes (rare)
- **CURRENT REALITY:** Updates after each code change (automated where possible)
- **GUIDES:** Updated when processes change (quarterly+)
- **REFERENCE:** Archive only (never loaded for coding)

---

## 🔄 Navigation Hierarchy

```
Start at: MASTER_INDEX.md
   ↓
Choose domain based on query:
   ├─ "Why?" → GOVERNANCE/
   ├─ "How to build?" → SPECS/
   ├─ "How does it work now?" → CURRENT_REALITY/
   ├─ "How do I use it?" → GUIDES/
   └─ "Reference?" → REFERENCE/ARCHIVE/
   ↓
Load specific files for query
   ↓
Stay focused! (no noise)
```

---

## ✨ Benefits of This Organization

| Benefit | Mechanism |
|---------|-----------|
| **Fast loading** | Query router → domain → file (vs 500+ KB everywhere) |
| **Clear ownership** | Each domain has clear maintainer |
| **No confusion** | "Where is X?" answered clearly |
| **Scaling** | Add topics within domain (modular) |
| **Reuse** | Same file serves multiple queries |
| **AI-friendly** | Structured for code generation tools |

---

See: `/docs/ia/specs/_shared/reactive_documentation.md` for full SPEC
