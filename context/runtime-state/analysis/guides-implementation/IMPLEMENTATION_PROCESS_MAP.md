# 🗺️ IMPLEMENTATION PROCESS MAP — Visual Guide

**Version:** 1.0  
**Purpose:** Visual overview of complete implementation flow  

---

# 📋 THE COMPLETE JOURNEY

```
┌─────────────────────────────────────────────────────────────┐
│                   🎯 FEATURE REQUEST                        │
│          "Add player inventory system"                      │
└────────────────────────┬────────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────────┐
│         📖 STEP 0: UNDERSTAND YOUR TASK (5 min)             │
│  Is this new feature? Will it touch domain logic?           │
└────────────────────────┬────────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────────┐
│    ⚠️ STEP 1: EXECUTION AWARENESS CHECK (5 min)             │
│  Read: execution_state.md                                   │
│  Check: Any active threads? Any conflicts?                  │
└────────────────────────┬────────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────────┐
│   📖 STEP 2: LEARN IMMUTABLE PRINCIPLES (10 min)            │
│  Read: constitution.md                                      │
│  Learn: Why Clean Architecture is mandatory                 │
└────────────────────────┬────────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────────┐
│     🛠️ STEP 3: LEARN EXECUTION RULES (15 min)              │
│  Read: ai-rules.md                                          │
│  Learn: HOW to implement (16 execution protocols)           │
└────────────────────────┬────────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────────┐
│    🏛️ STEP 4: UNDERSTAND PATTERNS (20 min)                │
│  Read: architecture.md                                      │
│  Learn: Current implementation patterns                      │
└────────────────────────┬────────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────────┐
│    🎨 STEP 5: LEARN STYLE GUIDE (10 min)                   │
│  Read: conventions.md                                       │
│  Learn: Naming, formatting, consistency rules               │
└────────────────────────┬────────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                🔧 IMPLEMENTATION (60 min)                   │
│                                                              │
│  ╔════════════════════════════════════════╗                 │
│  ║ Layer 1: DOMAIN RULES                  ║                 │
│  ║ ├─ inventory.py                        ║                 │
│  ║ └─ item.py                             ║                 │
│  ╚════════════════════════════════════════╝                 │
│                      ▼                                       │
│  ╔════════════════════════════════════════╗                 │
│  ║ Layer 2: PORTS                         ║                 │
│  ║ └─ inventory_repository_port.py        ║                 │
│  ╚════════════════════════════════════════╝                 │
│                      ▼                                       │
│  ╔════════════════════════════════════════╗                 │
│  ║ Layer 3: USECASES                      ║                 │
│  ║ ├─ add_to_inventory_usecase.py         ║                 │
│  ║ └─ remove_from_inventory_usecase.py    ║                 │
│  ╚════════════════════════════════════════╝                 │
│                      ▼                                       │
│  ╔════════════════════════════════════════╗                 │
│  ║ Layer 4: ADAPTERS                      ║                 │
│  ║ └─ json_inventory_adapter.py           ║                 │
│  ╚════════════════════════════════════════╝                 │
│                      ▼                                       │
│  ╔════════════════════════════════════════╗                 │
│  ║ Layer 5: ERROR HANDLING                ║                 │
│  ║ ├─ Map infra errors to domain          ║                 │
│  ║ ├─ Document failure modes              ║                 │
│  ║ └─ Test error paths                    ║                 │
│  ╚════════════════════════════════════════╝                 │
│                      ▼                                       │
│  ╔════════════════════════════════════════╗                 │
│  ║ Layer 6: INTERFACE ENDPOINTS           ║                 │
│  ║ └─ inventory_routes.py                 ║                 │
│  ╚════════════════════════════════════════╝                 │
│                      ▼                                       │
│  ╔════════════════════════════════════════╗                 │
│  ║ Layer 7: COMMAND/QUERY DTOs            ║                 │
│  ║ └─ inventory_commands.py               ║                 │
│  ╚════════════════════════════════════════╝                 │
│                      ▼                                       │
│  ╔════════════════════════════════════════╗                 │
│  ║ Layer 8: DI MODULES                    ║                 │
│  ║ └─ inventory_module.py                 ║                 │
│  ╚════════════════════════════════════════╝                 │
└────────────────────────┬────────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────────┐
│    🧪 STEP 6: LEARN TESTING PATTERNS (30 min)              │
│  Read: testing.md                                           │
│  Read: TESTING_STRATEGY_CLARIFICATION.md (if confused)      │
│  Understand: Test patterns for each layer                   │
└────────────────────────┬────────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              🧪 TESTING (45 min)                            │
│                                                              │
│  ╔════════════════════════════════════════╗                 │
│  ║ Domain Tests (UNIT - no mocks)         ║                 │
│  ║ test_inventory.py                      ║                 │
│  ║ • Pure function testing                ║                 │
│  ║ • No external deps                     ║                 │
│  ╚════════════════════════════════════════╝                 │
│                      ▼                                       │
│  ╔════════════════════════════════════════╗                 │
│  ║ UseCase Tests (INTEGRATION - mock port)║                 │
│  ║ test_add_to_inventory_usecase.py       ║                 │
│  ║ • Mock repository port                 ║                 │
│  ║ • Test behavior, not implementation    ║                 │
│  ╚════════════════════════════════════════╝                 │
│                      ▼                                       │
│  ╔════════════════════════════════════════╗                 │
│  ║ Adapter Tests (INTEGRATION - real I/O) ║                 │
│  ║ test_json_inventory_adapter.py         ║                 │
│  ║ • Use real or container backend        ║                 │
│  ║ • No mocking ports                     ║                 │
│  ╚════════════════════════════════════════╝                 │
│                      ▼                                       │
│  ╔════════════════════════════════════════╗                 │
│  ║ Route Tests (E2E - mock usecase)       ║                 │
│  ║ test_inventory_routes.py               ║                 │
│  ║ • Mock application layer                ║                 │
│  ║ • Test HTTP behavior                   ║                 │
│  ╚════════════════════════════════════════╝                 │
│                      ▼                                       │
│  [ pytest tests/unit/ ] ✅ PASS                             │
│  [ pytest tests/integration/ ] ✅ PASS                      │
│  [ pytest tests/architecture/ ] ✅ PASS                     │
│                                                              │
└────────────────────────┬────────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────────┐
│    ✅ STEP 8: VALIDATE WITH DEFINITION OF DONE (15 min)    │
│  Check: definition_of_done.md                               │
│                                                              │
│  Architecture Compliance                                     │
│  ├─ [ ] Layer boundaries correct                            │
│  ├─ [ ] Ports & Adapters pattern followed                   │
│  ├─ [ ] All I/O is async                                    │
│  └─ [ ] Error handling correct                              │
│                                                              │
│  Testing Compliance                                         │
│  ├─ [ ] All tests pass                                      │
│  ├─ [ ] Layer-specific testing patterns                     │
│  ├─ [ ] No direct adapter mocking                           │
│  └─ [ ] Deterministic & isolated                            │
│                                                              │
│  Code Quality                                               │
│  ├─ [ ] Naming conventions followed                         │
│  ├─ [ ] Docstrings present                                  │
│  ├─ [ ] Type hints complete                                 │
│  ├─ [ ] No test-specific code                               │
│  ├─ [ ] import-linter passes                                │
│  ├─ [ ] mypy passes                                         │
│  └─ [ ] ruff passes                                         │
│                                                              │
│  Functionality                                              │
│  ├─ [ ] All acceptance criteria met                         │
│  ├─ [ ] All error paths tested                              │
│  └─ [ ] Edge cases handled                                  │
│                                                              │
│  Documentation                                              │
│  └─ [ ] execution_state.md updated                          │
│                                                              │
└────────────────────────┬────────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────────┐
│     📍 STEP 9: CHECKPOINT & HANDOFF (10 min)               │
│  Update: execution_state.md                                 │
│  Record: What was done                                      │
│  Flag: Risks or open questions                              │
│  Update: Next Actions for next agent                        │
└────────────────────────┬────────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   ✅ READY TO MERGE!                        │
│                                                              │
│  ✅ Code is clean and well-tested                           │
│  ✅ Architecture is clean                                    │
│  ✅ All validation passed                                    │
│  ✅ Documentation updated                                    │
│  ✅ Ready for production                                     │
└─────────────────────────────────────────────────────────────┘
```

---

# ⏱️ TIME BREAKDOWN

```
Setup & Learning:           50 minutes
  ├─ Steps 0-5: Foundation   60 min
  └─ Total foundation:       60 min

Implementation:             45 minutes
  ├─ 8 layers:             ~7 min each (60 min)
  └─ Total:                60 min

Testing:                    45 minutes
  ├─ 4 test types:         ~11 min each (45 min)
  └─ Total:                45 min

Validation:                 25 minutes
  ├─ Step 8: Definition of done    15 min
  └─ Step 9: Checkpoint            10 min

────────────────────────────────────
TOTAL:                      3-4 hours

For experienced developers: 2-3 hours (skip some reading)
For new developers: 4-5 hours (deeper study)
```

---

# 🏗️ ARCHITECTURE LAYERS VISUALIZATION

```
┌─────────────────────────────────────────┐
│      🔌 INTERFACES (Entry Points)       │
│   ├─ /api/routes/inventory.py          │
│   ├─ /discord/handlers/inventory.py    │
│   └─ /cli/commands/inventory.py        │
└────────────────┬────────────────────────┘
                 │ calls UseCases ↓
┌────────────────┴────────────────────────┐
│     🎯 APPLICATION (Orchestration)      │
│   ├─ /usecases/add_to_inventory.py     │
│   ├─ /commands/inventory_command.py    │
│   └─ /queries/inventory_query.py       │
└────────────────┬────────────────────────┘
                 │ uses Ports ↓
┌────────────────┴────────────────────────┐
│      🔌 PORTS (Abstraction)             │
│   └─ /ports/inventory_repository_port.py│
└────────────────┬────────────────────────┘
                 │ implemented by ↓
┌────────────────┴────────────────────────┐
│   🔧 INFRASTRUCTURE (Implementation)    │
│   ├─ /adapters/json_inventory_adapter.py│
│   ├─ /adapters/postgres_adapter.py     │
│   └─ /events/event_bus.py              │
└────────────────┬────────────────────────┘
                 │ stores ↓
┌────────────────┴────────────────────────┐
│      💾 STORAGE (Persistence)           │
│   ├─ JSON files                         │
│   ├─ PostgreSQL                         │
│   └─ ChromaDB (vector index)            │
└─────────────────────────────────────────┘

                 AND

┌─────────────────────────────────────────┐
│      🏛️ DOMAIN (Pure Business Logic)    │
│   ├─ inventory.py                       │
│   ├─ item.py                            │
│   └─ inventory_error.py                 │
│                                         │
│  NO external dependencies               │
│  NO I/O operations                      │
│  Pure functions & business rules        │
└─────────────────────────────────────────┘
```

**Key Rule:** Domain never imports from anything else. Everything else imports domain.

---

# 🧪 TESTING LAYERS

```
┌──────────────────────────────────────┐
│   Interface Tests (Routes)            │
│   ├─ Mock UseCases                    │
│   ├─ Test HTTP behavior               │
│   └─ Test error responses             │
│   Pattern: test_<action>_route_<case> │
└──────────────────────────────────────┘
           ↓
┌──────────────────────────────────────┐
│   UseCase Tests (Orchestration)       │
│   ├─ Mock Ports ONLY                  │
│   ├─ Test orchestration logic         │
│   └─ Test error handling              │
│   Pattern: test_<usecase>_<case>      │
└──────────────────────────────────────┘
           ↓
┌──────────────────────────────────────┐
│   Adapter Tests (Implementation)      │
│   ├─ Use REAL backends (or stubs)     │
│   ├─ Test persistence                 │
│   └─ Test error conditions            │
│   Pattern: test_<adapter>_<case>      │
└──────────────────────────────────────┘
           ↓
┌──────────────────────────────────────┐
│   Domain Tests (Business Logic)       │
│   ├─ ZERO mocks                       │
│   ├─ Test business rules              │
│   └─ Pure function testing            │
│   Pattern: test_<entity>_<case>       │
└──────────────────────────────────────┘

🎯 Golden Rule:
   Domain = no mocks
   UseCase = mock ports
   Adapter = use real backends
   Interface = mock usecases
```

---

# 🎯 ERROR HANDLING FLOW

```
Infrastructure (Low Level)
│
├─ FileNotFoundError
├─ DatabaseConnectionError
├─ NetworkTimeoutError
│
└─ [CAUGHT BY ADAPTER]
   [LOGGED FOR OBSERVABILITY]
         ↓
Application (Orchestration)
│
├─ [USECASE CATCHES ADAPTER ERROR]
│  [MAPS TO DOMAIN ERROR]
│
├─ NarrativeNotFoundError ──┐
├─ InvalidNarrativeError ──┐│
├─ InventoryFullError ─────┐│
└─ ConflictError ─────────┐││
         ↓                ││
         └────────────────┘│
                           ├─ [INTERFACE CATCHES DOMAIN ERROR]
                           │  [CONVERTS TO HTTP/DISCORD RESPONSE]
                           │
                           ├─ 404 Not Found
                           ├─ 400 Bad Request
                           ├─ 409 Conflict
                           └─ Discord error message

🎯 Golden Rule:
   Always map DOWN the stack (infra → application → domain)
   Never let technical errors escape the application layer
```

---

# 📚 DOCUMENT NAVIGATION

```
START HERE: IMPLEMENTATION_ROADMAP.md
         │
         ├─ For principles → constitution.md
         ├─ For rules → ai-rules.md
         ├─ For patterns → architecture.md
         ├─ For conventions → conventions.md
         ├─ For step-by-step → feature-checklist.md
         ├─ For testing → testing.md + TESTING_STRATEGY_CLARIFICATION.md
         ├─ For validation → definition_of_done.md
         ├─ For runtime state → execution_state.md
         └─ For error handling → Layer 5 in feature-checklist.md

All documents are cross-referenced. You can start anywhere,
but IMPLEMENTATION_ROADMAP.md is the recommended entry point.
```

---

# ✅ QUICK CHECKLIST

### Before You Start:
- [ ] Read IMPLEMENTATION_ROADMAP.md
- [ ] Follow the 9 steps in order
- [ ] Don't skip steps

### During Development:
- [ ] Reference feature-checklist.md for each layer
- [ ] Write tests as you implement each layer
- [ ] Check error handling (Layer 5)

### Before Merge:
- [ ] Run all tests: `pytest tests/`
- [ ] Check linting: `ruff check src/`
- [ ] Check types: `mypy src/`
- [ ] Check imports: `python -m importlinter lint`
- [ ] Use definition_of_done.md checklist
- [ ] Update execution_state.md

### After Merge:
- [ ] Celebrate! 🎉

---

# 🚀 YOU'RE READY!

This map shows the complete journey from feature request to merge.

**Next step:** Open [IMPLEMENTATION_ROADMAP.md](../IMPLEMENTATION_ROADMAP.md) and start Step 1.

Good luck! 🚀
