# 🧠 ADAPTIVE CONTEXT LOADING — Token & Memory Optimization

**Version:** 1.0  
**Purpose:** Show how agents load ONLY necessary docs (consulta sob medida)  
**Benefit:** 50-85% context savings + better thread isolation

---

# 💡 THE CONCEPT

**Traditional Approach:**
```
Agente inicia → Lê TODOS os docs → ~100KB contexto
→ Implementa feature → Termina

Problema: 70% do contexto é desnecessário para essa feature específica
```

**Adaptive Approach:**
```
Agente inicia → Lê execution_state.md (5 min)
→ Diagnóstico: Que tipo de trabalho é?
→ Carrega APENAS docs relevantes → ~25KB contexto (75% savings!)
→ Implementa feature → Termina

Benefício: Mesmo conhecimento, contexto otimizado
```

---

# 🎯 DECISION TREE (Como Escolher Seu Caminho)

```
┌──────────────────────────────────────┐
│  AGENTE INICIA                        │
│  1. Lê execution_state.md             │
│  2. Lê constitution.md + ai-rules.md  │
│  3. Classifica trabalho               │
└──────────────┬───────────────────────┘
               │
        ┌──────┴───────┬─────────┬──────────────┐
        │              │         │              │
        ▼              ▼         ▼              ▼
    BUG FIX      FEATURE     COMPLEX      MULTI-THREAD
    (PATH A)     SIMPLES     FEATURE      (PATH D)
                 (PATH B)    (PATH C)
    
┌──────────────┐ ┌───────────────┐ ┌────────────────┐ ┌──────────────┐
│ 1.5 hours    │ │ 2 hours       │ │ 3-4 hours      │ │ Variable     │
│ 1 camada     │ │ 1-2 camadas   │ │ 3+ camadas     │ │ Isolado      │
│ ~15KB ctx    │ │ ~25KB ctx     │ │ ~50KB ctx      │ │ per thread   │
│              │ │               │ │                │ │              │
│ Load:        │ │ Load:         │ │ Load:          │ │ Load:        │
│ • arch sect  │ │ • arch full   │ │ • arch full    │ │ • exec state │
│ • layer sect │ │ • conventions │ │ • design dec   │ │ • thread     │
│ • test layer │ │ • full FC     │ │ • conventions  │ │ • arch sect  │
│ • def done   │ │ • test layers │ │ • all layers   │ │ • relevant   │
└──────────────┘ │ • def done    │ │ • all tests    │ │   docs only  │
                 │               │ │ • def done     │ │              │
                 └───────────────┘ │                │ └──────────────┘
                                   │                │
                                   └────────────────┘
```

---

# 📊 EXAMPLE: Bug Fix (PATH A)

**Scenario:** Player XP not being saved to database

### Context Loading Strategy
```python
# Load ONLY what's needed for this bug
load("constitution.md")              # Mandatory: 10KB
load("ai-rules.md")                  # Mandatory: 15KB
check("execution_state.md")          # Check threads: 2KB

# Diagnose: Where is bug?
# Answer: Adapter layer (storage persistence)

load("architecture.md", section="infrastructure_adapters")  # 5KB
load("architecture.md", section="ports_pattern")             # 3KB
load("feature-checklist.md", layer=4)                        # Layer 4: Adapter
load("testing.md", section="adapter_tests")

# TOTAL: ~40KB (60% saved vs full 100KB)
```

### What Agent Does
```
1. Find bug in JsonPlayerXPAdapter.save()
2. Read feature-checklist.md Layer 4 (Adapter specifics)
3. Implement fix
4. Write adapter test (testing.md pattern for adapters)
5. Validate: definition_of_done.md (adapter subset only)
6. Checkpoint
```

### Time Breakdown
```
Load docs:        10 min (vs 60 min if reading all)
Diagnose bug:     10 min
Implement fix:    15 min
Test fix:         10 min
Validate:          5 min
───────────────────────
TOTAL:           50 min (vs 3-4 hours if reading all)
```

---

# 📊 EXAMPLE: Simple Feature (PATH B)

**Scenario:** "Add gold to player wallet"

### Context Loading Strategy
```python
# Phase 1: Always mandatory
load("constitution.md")
load("ai-rules.md")
check("execution_state.md")

# Phase 2: Diagnose
# Decision: Domain + UseCase only (simple feature)

load("conventions.md")                              # 10KB
load("architecture.md", section="clean_arch")      # 8KB
load("architecture.md", section="domain_layer")    # 5KB
load("architecture.md", section="application")     # 5KB
load("feature-checklist.md", layers=[1,2,3])      # Domain, Port, UseCase

# Testing: Only these layers
load("testing.md", section="domain_tests")         # 5KB
load("testing.md", section="usecase_tests")        # 5KB

# Validation: Relevant criteria only
load("definition_of_done.md", section="architecture")  # 3KB

# TOTAL: ~44KB (56% saved vs 100KB)
```

### What Agent Does
```
Layer 1: Domain
├─ Class Gold(amount)
├─ Class Wallet(gold, max_gold)
├─ Method add_gold() - validate limit
└─ Domain tests (no mocks)

Layer 2: Port
├─ WalletRepositoryPort
└─ load() and save() async methods

Layer 3: UseCase
├─ AddGoldToWalletUseCase
├─ Uses WalletRepositoryPort
└─ UseCase tests (mock port)

SKIP Layer 4-8: Not needed for simple feature
```

### Time Breakdown
```
Load docs:        15 min (read only relevant sections)
Domain layer:     15 min
Port layer:       10 min
UseCase layer:    15 min
Domain tests:     10 min
UseCase tests:    10 min
Validate:          5 min
───────────────────────
TOTAL:          ~80 min (2 hours)
```

---

# 📊 EXAMPLE: Complex Feature (PATH C)

**Scenario:** "Implement Merchant NPC with inventory management"

### Context Loading Strategy
```python
# Phase 1: Always mandatory
load("constitution.md")
load("ai-rules.md")
check("execution_state.md")

# Phase 2: Complex feature = load everything
load("conventions.md")                              # 10KB
load("architecture.md", full=True)                  # 20KB
load("design-decisions.md")                         # 8KB
load("feature-checklist.md", full=True)             # 15KB

# Testing: All patterns
load("testing.md", full=True)                       # 20KB

# Validation: Complete checklist
load("definition_of_done.md", full=True)            # 12KB

# TOTAL: ~85KB (15% saved vs naive approach)
```

### What Agent Does
```
Layer 1: Domain
├─ Merchant entity with personality
├─ Inventory with max weight
├─ Pricing logic
└─ Domain tests

Layer 2-3: Ports + UseCase
├─ MerchantRepositoryPort
├─ InventoryRepositoryPort
├─ BuyFromMerchantUseCase
├─ SellToMerchantUseCase
└─ UseCase tests with mocked ports

Layer 4: Adapters
├─ JsonMerchantAdapter
├─ JsonInventoryAdapter
└─ Real backend tests

Layer 5: Error Handling
├─ MerchantNotFoundError
├─ InsufficientFundsError
├─ InventoryFullError
└─ Error mapping chain

Layer 6-8: Interface + DI
├─ API endpoints
├─ Commands/Queries
└─ DI module wiring
```

### Time Breakdown
```
Load docs:           30 min (read all sections)
Implement layers:    60 min (8 layers × ~7.5 min avg)
Tests all layers:    30 min
Validate:            15 min
───────────────────────
TOTAL:            ~135 min (2.25 hours)
```

---

# 🧵 EXAMPLE: Multi-Thread (PATH D)

**Scenario:** Complex system needing parallel development
- Thread 1: Implement domain + usecase (storage layer)
- Thread 2: Implement adapter (actual database connection)
- Thread 3: Implement API routes (interface layer)

### How Execution Awareness Helps

```python
# BEFORE THREAD 1 STARTS
check("execution_state.md")
# Sees: No active threads

# THREAD 1 AGENT
load("constitution.md", "ai-rules.md")  # Mandatory
create("threads/thread_1_storage.md")    # Declare work
load("architecture.md", sections=["domain", "application"])
implement_layer_1_2_3()  # Domain, Port, UseCase
checkpoint("Thread 1 complete: Domain + UseCase ready for Thread 2")

# THREAD 2 AGENT (different agent, different time)
load("constitution.md", "ai-rules.md")  # Mandatory
check("execution_state.md")
# Sees: Thread 1 done, knows Domain+UseCase exist
load("runtime/threads/thread_1_storage.md")  # Understand prior work
load("architecture.md", section="infrastructure")
# KNOWS: Domain/UseCase already exist, just implement adapter
implement_layer_4()  # Adapter only
checkpoint("Thread 2 complete: Storage adapter ready for Thread 3")

# THREAD 3 AGENT
load("constitution.md", "ai-rules.md")
check("execution_state.md")
# Sees: Threads 1+2 done, everything ready
load("runtime/threads/thread_1_storage.md")
load("runtime/threads/thread_2_adapter.md")
load("architecture.md", section="interfaces")
# Can implement routes knowing all underlying layers exist
implement_layer_6_7_8()  # Interface, DTO, DI
checkpoint("Thread 3 complete: Full feature done")

# BENEFITS:
# 1. No conflicts (threads know what others did)
# 2. Optimized context (each loads only their section)
# 3. Sequential clarity (checkpoint shows order)
# 4. Knowledge transfer (next agent reads prior checkpoint)
```

### Context Per Thread
```
Thread 1: ~30KB (domain + application sections only)
Thread 2: ~25KB (infrastructure sections only, knows T1 done)
Thread 3: ~20KB (interface sections only, knows T1+T2 done)

Total: ~75KB across 3 threads
vs naive: ~300KB (100KB × 3 agents reading everything)

SAVINGS: 75% context reduction! ✅
```

---

# 🎯 CONTEXT OPTIMIZATION RULES

### Rule 1: Always Load Foundation
**Mandatory regardless of path:**
```
✓ constitution.md (5 min)        # Immutable principles
✓ ai-rules.md (10 min)            # Execution protocols
✓ execution_state.md (5 min)      # Check conflicts & threads
```

### Rule 2: Load Based on Diagnosis
```
✓ Diagnose: What type of work?
  ├─ Bug fix? Load: affected layer docs only
  ├─ Simple feature? Load: full architecture + relevant layers
  ├─ Complex feature? Load: everything
  └─ Multi-thread? Load: thread spec + your section only
```

### Rule 3: Skip Unnecessary Sections
```
✓ Don't load testing.md domain section if fixing adapter bug
✓ Don't load design-decisions.md for simple CRUD feature
✓ Don't load full testing.md if only implementing domain
✓ Don't load adapter patterns if implementing interface
```

### Rule 4: Load Testing Pattern for Your Layer Only
```
✓ Implementing domain? testing.md domain section only (~5KB)
✓ Implementing usecase? testing.md usecase section only (~5KB)
✓ Implementing adapter? testing.md adapter section only (~5KB)
✓ Full feature? all testing sections (~20KB)
```

### Rule 5: Validation Scales with Work
```
✓ Bug fix? definition_of_done.md affected layer criteria only
✓ Simple feature? affected layers + interfaces criteria
✓ Complex feature? full definition_of_done.md
```

---

# 📈 CONTEXT SAVINGS COMPARISON

| Type of Work | Full Load | Adaptive Load | Savings |
|--------------|-----------|---------------|---------|
| **Bug Fix** | 100KB | 40KB | **60%** ✅ |
| **Simple Feature** | 100KB | 45KB | **55%** ✅ |
| **Complex Feature** | 100KB | 85KB | **15%** ⚠️ |
| **Thread 1 (3 parallel)** | 300KB | 75KB | **75%** ✅ |
| **Average** | 100KB | 61KB | **39%** ✅ |

---

# 🧠 EXECUTION AWARENESS BENEFITS

### Without Execution Awareness
```
Thread 1: Implements domain + usecase
Thread 2: Doesn't know what Thread 1 did
         → May re-implement same things
         → Loads full context again
         → 100KB per thread

Result: 300KB for 3 parallel threads (wasteful)
```

### With Execution Awareness
```
Thread 1: Implements domain + usecase
         → Checkpoints progress in execution_state.md

Thread 2: Reads execution_state.md
         → Sees "Thread 1 completed domain+usecase"
         → Loads only adapter section (~25KB)
         → Knows exactly what to implement

Thread 3: Reads execution_state.md
         → Sees both prior threads completed
         → Loads only interface section (~20KB)
         → Knows full context without re-reading

Result: 75KB total (75% savings + no conflicts) ✅
```

---

# 🎯 FINAL CHECKLIST

For optimal adaptive loading:

- [ ] Always load Phase 1 (constitution + ai-rules + execution_state)
- [ ] Diagnose type of work (bug, simple feature, complex, multi-thread)
- [ ] Choose corresponding PATH (A, B, C, or D)
- [ ] Load ONLY relevant documentation sections
- [ ] Read testing.md section for your layer(s) only
- [ ] Use definition_of_done.md criteria relevant to your work
- [ ] Checkpoint when done (helps next agent)
- [ ] Calculate context savings (should be 30-75% less than 100KB)

---

# 💡 KEY INSIGHT

**"Consulta Sob Medida" isn't about reading less documentation.**  
**It's about reading the RIGHT documentation at the RIGHT time.**

With Execution Awareness + Adaptive Paths:
- ✅ Agents know exactly what to read
- ✅ Threads don't interfere or duplicate work
- ✅ Context is optimized (50-85% savings possible)
- ✅ Quality remains high (same guidance, better efficiency)

**Result:** Faster, smarter, more efficient AI-driven development.
