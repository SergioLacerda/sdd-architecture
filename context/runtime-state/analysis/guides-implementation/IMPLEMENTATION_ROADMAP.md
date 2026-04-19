# 🧭 IMPLEMENTATION ROADMAP — Start Here!

**Version:** 1.0  
**Status:** MANDATORY READING FOR ALL IMPLEMENTATIONS  
**Purpose:** Clear entry point and sequence for implementing features

---

# 🎯 WHY THIS EXISTS

The governance system has many specs. This document tells you:
- **WHEN** to read each spec
- **IN WHAT ORDER** to read them
- **WHY** you need each one
- **WHAT THEY PREPARE YOU FOR**

---

# ⏯️ START HERE: YOUR JOURNEY

You want to implement a feature or fix a bug.  
Follow this sequence. Don't skip steps.

---

# 🚀 STEP 0: UNDERSTAND YOUR TASK (5 minutes)

**Do this FIRST:**

1. Read your task description carefully
2. Ask: "Is this a new feature or a bug fix?"
3. Ask: "Will this touch domain logic, application, or just interfaces?"

**Then proceed to Step 1.**

---

# 📖 STEP 1: LEARN THE IMMUTABLE PRINCIPLES (10 minutes)

**Read:** `/EXECUTION/spec/CANONICAL/rules/constitution.md`

**Why:** 
- Defines what CAN'T change
- Establishes Clean Architecture as mandatory
- Sets expectations about layers and dependencies

**You'll learn:**
- ✅ What architecture pattern is non-negotiable
- ✅ What Ports & Adapters means
- ✅ What each layer can/cannot do
- ✅ What Storage and Vector Index mean

**Exit criteria:** You understand why architecture matters

---

# 🛠️ STEP 2: LEARN EXECUTION PROTOCOLS (15 minutes)

**Read:** `/docs/ia/ai-rules.md`

**Why:**
- Defines HOW to implement (not just WHAT)
- 16 rules that govern every decision
- Execution Awareness protocol

**You'll learn:**
- ✅ Check execution_state.md before starting
- ✅ Respect thread isolation
- ✅ Follow "Next Actions" strictly
- ✅ Never modify production code for tests
- ✅ Checkpoint after changes

**Exit criteria:** You know the rules of execution

---

# 🏛️ STEP 3: UNDERSTAND ARCHITECTURE PATTERNS (20 minutes)

**Read:** `/EXECUTION/spec/CANONICAL/specifications/architecture.md`

**Why:**
- Shows ACTUAL implementation patterns
- Explains specific decisions already made
- Defines constraints for your code

**You'll learn:**
- ✅ Clean Architecture layers
- ✅ Ports & Adapters pattern
- ✅ Data flow and isolation rules
- ✅ Async model requirements
- ✅ Vector Index as black box
- ✅ 6 key implementation decisions

**Exit criteria:** You know what the system looks like

---

# 📋 STEP 4: GET NAMING & STYLE CONVENTIONS (10 minutes)

**Read:** `/EXECUTION/spec/CANONICAL/rules/conventions.md`

**Why:**
- Ensures consistency across codebase
- Prevents naming ambiguities
- Defines testing rules

**You'll learn:**
- ✅ UseCase naming: `<Action><Entity>UseCase`
- ✅ Port naming: `<Entity>RepositoryPort`
- ✅ Adapter naming: `<Technology><Entity>Adapter`
- ✅ Async requirements
- ✅ Storage source of truth rules
- ✅ Error handling rules
- ✅ Testing rules

**Exit criteria:** You know how to name things

---

# 🎬 STEP 5: FOLLOW STEP-BY-STEP IMPLEMENTATION (60 minutes)

**Read:** `/EXECUTION/spec/CANONICAL/specifications/feature-checklist.md`

**Why:**
- Gives you the exact sequence of layers to implement
- Provides checklist for each layer
- Shows patterns and examples

**You'll follow:**
1. Layer 1: Define Domain Rules
2. Layer 2: Define Port/Contract
3. Layer 3: Create UseCase
4. Layer 4: Create Adapter
5. Layer 5: Create Interface Endpoint
6. Layer 6: Create Command/Query DTO
7. Layer 7: Create DI Module

**For each layer:**
- [ ] Read the layer description
- [ ] Check the checklist
- [ ] Look at the code example
- [ ] Implement the layer
- [ ] Note any anti-patterns to avoid

**Exit criteria:** You have a working implementation

---

# 🧪 STEP 6: UNDERSTAND TESTING STRATEGY (30 minutes)

**Read:** `/EXECUTION/spec/CANONICAL/specifications/testing.md`

**Why:**
- Testing is 30% of implementation
- Each layer has specific testing requirements
- Knowing this BEFORE you code saves time

**You'll learn:**
- ✅ Domain tests: Unit (no mocks)
- ✅ UseCase tests: Integration with mocked ports
- ✅ Adapter tests: Real backends or containers
- ✅ Interface tests: UseCase mocks only
- ✅ Mocking discipline (Ports only, not adapters)
- ✅ Fake adapters vs mocks (when to use each)
- ✅ Anti-patterns to avoid

**Exit criteria:** You know how to test each layer

---

# 🧪 STEP 7: IMPLEMENT TESTS (45 minutes)

**Follow:** `/EXECUTION/spec/CANONICAL/specifications/testing.md` patterns

**For each layer:**
- [ ] Create test file
- [ ] Follow layer-specific testing pattern
- [ ] Mock only Ports (never adapters)
- [ ] Test behavior, not implementation
- [ ] Ensure async/await usage
- [ ] Validate error handling

**Exit criteria:** All tests pass

---

# ✅ STEP 8: VALIDATE BEFORE MERGE (15 minutes)

**Check:** `/EXECUTION/spec/CANONICAL/specifications/definition_of_done.md`

**You'll verify:**
- [ ] Architecture checklist (layers, patterns)
- [ ] Testing checklist (coverage, isolation)
- [ ] Code quality checklist (naming, async, errors)
- [ ] Documentation checklist (docstrings, comments)

**Exit criteria:** You meet definition of done

---

# 📍 STEP 9: CHECKPOINT & HANDOFF (10 minutes)

**Do this LAST:**

1. Update `/docs/ia/DEVELOPMENT/execution-state/_current.md`:
   - Record what was done
   - Flag any risks or questions
   - Update "Next Actions"

2. If complex work:
   - Create checkpoint in `/docs/ia/specs/runtime/checkpoints/`
   - Document decisions made

**Exit criteria:** Next agent can continue smoothly

---

# ⏱️ TIME ESTIMATES (Adaptive by Work Type)

## For Small Bug Fix / Single Layer Change
| Step | Time |
|------|------|
| Phase 1: Always (principles + rules + awareness check) | 30 min |
| Phase 2: Read only affected layer docs | 10 min |
| Implement single layer | 20 min |
| Test single layer | 15 min |
| Validate subset of criteria | 10 min |
| **TOTAL:** | **~1.5 hours** |

## For Simple Feature (1-2 layers)
| Step | Time |
|------|------|
| Phase 1: Always (principles + rules + awareness check) | 30 min |
| Phase 2: Read relevant sections of architecture | 15 min |
| Read conventions | 10 min |
| Implement 1-2 layers | 30 min |
| Test relevant layers | 20 min |
| Validate | 10 min |
| **TOTAL:** | **~2 hours** |

## For Complex Feature (3+ layers, error handling)
| Step | Time |
|------|------|
| Phase 1: Always (principles + rules + awareness check) | 30 min |
| Phase 2: Read architecture + design-decisions | 30 min |
| Read conventions | 10 min |
| Per-layer: Read specific docs + implement + test | 15 min × N layers |
| Test all layers | 30 min |
| Validate complete checklist | 15 min |
| **TOTAL:** | **~3-4 hours** (N = 3-4 layers) |

## For Multi-Thread Complex Work
| Step | Time |
|------|------|
| Phase 1: Always (principles + rules) | 30 min |
| Read execution_state.md (understand other threads) | 10 min |
| Create isolated thread spec | 10 min |
| Read relevant architecture for this thread only | 15 min |
| Implement thread-isolated components | Variable |
| Checkpoint + handoff | 10 min |
| **TOTAL:** | **Depends on scope, but optimized for isolation** |

---

## 🎯 Context Optimization

Each path loads **ONLY** what's needed:

- **Bug Fix:** ~15KB context (vs 100KB if reading everything)
- **Simple Feature:** ~25KB context (75% savings)
- **Complex Feature:** ~50KB context (50% savings)
- **Multi-Thread:** Isolated contexts, no interference

**Key benefit:** Execution Awareness prevents threads from conflicting, maintaining clean separation

---

# 🎯 ADAPTIVE PATHS (Consulta Sob Medida)

**Key Concept:** Not all work requires all steps. Choose your path:

## PATH A: Bug Fix / Small Change (1.5 hours)
```
✓ Phase 1: Always (constitution + ai-rules + execution_state check)
✓ Read: architecture.md (affected section only)
✓ Read: feature-checklist.md (affected layer only)
✓ Implement: Single layer change
✓ Test: testing.md (layer-specific pattern)
✓ Validate: definition_of_done.md (subset relevant to change)
✓ Context saved: 85% less than full roadmap
```

## PATH B: Simple Feature (2 hours)
```
✓ Phase 1: Always (constitution + ai-rules + execution_state check)
✓ Read: conventions.md (naming for your components)
✓ Read: architecture.md (full patterns)
✓ Read: feature-checklist.md (Layer 1-3: Domain, Port, UseCase)
✓ Implement: 1-2 layers
✓ Test: testing.md (patterns for your layers)
✓ Validate: definition_of_done.md (relevant criteria)
✓ Context saved: 75% less than full roadmap
```

## PATH C: Complex Feature (3-4 hours)
```
✓ Phase 1: Always (constitution + ai-rules + execution_state check)
✓ Read: architecture.md (full)
✓ Read: design-decisions.md (understand decisions)
✓ Read: conventions.md (naming)
✓ Read: feature-checklist.md (all 8 layers)
✓ For each layer: Read relevant section + implement + test
✓ Read: testing.md (all layer patterns)
✓ Validate: definition_of_done.md (complete checklist)
✓ Context saved: 50% less than naive approach
```

## PATH D: Multi-Thread Complex (Variable)
```
✓ Phase 1: Always (constitution + ai-rules)
✓ Read: execution_state.md (understand active threads)
✓ Read: runtime/threads/TEMPLATE.md (create isolated thread)
✓ Read: Only relevant sections of architecture for THIS thread
✓ Implement: Isolated components for this thread
✓ Checkpoint: Update execution_state.md
✓ Benefit: Execution Awareness prevents conflicts
✓ Context: Isolated per thread, no cross-contamination
```

---

# 🚨 DO NOT SKIP (Universal)

These are **mandatory for ALL paths**:

- ❌ Do NOT skip Phase 1 (constitution.md + ai-rules.md + execution_state.md check)
  - These are universal context for ANY work
  - Prevents conflicts and architectural violations

- ❌ Do NOT skip testing your layer
  - Whatever path you take, test it properly
  - Use testing.md pattern for your layer

- ❌ Do NOT skip validation
  - At minimum, check definition_of_done.md criteria relevant to your work
  - Better: use full checklist for complex features

- ❌ Do NOT skip checkpoint
  - Always update execution_state.md
  - Helps next agent understand what was done

---

# ⚡ QUICK REFERENCE

If you forget, remember this:

```
Principles (constitution)
    ↓
Rules (ai-rules)
    ↓
Patterns (architecture)
    ↓
Conventions (conventions)
    ↓
Step-by-step (feature-checklist)
    ↓
Implement
    ↓
Testing patterns (testing)
    ↓
Test
    ↓
Validate (definition_of_done)
    ↓
Checkpoint
```

---

# 🎓 EXAMPLE: Implementing "Player Inventory"

### Using This Roadmap:

1. **Read constitution** → "Must be clean architecture"
2. **Read ai-rules** → "Must checkpoint after"
3. **Read architecture** → "Ports & Adapters pattern"
4. **Read conventions** → "Name it InventoryRepositoryPort"
5. **Follow feature-checklist** → 7 layers, step-by-step
6. **Read testing** → "Mock port, test behavior"
7. **Implement tests** → Following layer patterns
8. **Check definition_of_done** → All criteria met?
9. **Checkpoint** → Done!

**Time:** 3-4 hours  
**Result:** High-quality, well-tested feature

---

# 🤖 FOR AI AGENTS

**PRIORITY ORDER FOR YOUR DECISION MAKING:**

1. constitution.md (Non-negotiable)
2. ai-rules.md (Execution protocol)
3. architecture.md (Current patterns)
4. feature-checklist.md (Step-by-step)
5. testing.md (Quality assurance)
6. conventions.md (Consistency)
7. Other specs (Reference as needed)

**WHEN IN DOUBT:**
- Refer to constitution.md (source of truth)
- Check execution_state.md (current state)
- Follow feature-checklist.md (methodology)

---

# 📞 QUESTIONS?

Each spec has detailed explanations. If you're confused about something:

1. Constitution.md? → Why is this non-negotiable?
2. Ai-rules.md? → What am I not allowed to do?
3. Architecture.md? → How does this pattern work?
4. Feature-checklist.md? → What's the step-by-step process?
5. Testing.md? → How do I test this layer?
6. Conventions.md? → What should I name this?

Each document has examples and detailed explanations.

---

# ✅ YOU'RE READY

You now have a clear path from "I need to implement something" to "My code is merged and high-quality."

**Next:** Start with Step 1. Read constitution.md. Then proceed in order.

Good luck! 🚀
