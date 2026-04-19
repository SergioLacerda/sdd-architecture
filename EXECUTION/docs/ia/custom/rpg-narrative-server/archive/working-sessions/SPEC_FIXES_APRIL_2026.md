# 📋 SPEC FIXES - April 2026

**Purpose:** Document all 9 spec gaps/conflicts fixed before Phase 1 implementation

**Status:** ✅ All 9 documented with decision markers

---

## 🔴 CRÍTICOS (3 fixes)

### FIX #1: Vector Port Naming Consistency

**Gap:** Architecture.md vs ADR-003 mismatch
- architecture.md called it: "VectorIndexPort" (singular)
- ADR-003 lists: "VectorReaderPort" + "VectorWriterPort" (plural)
- STRATEGY_B proposes: Use both (separate ports)

**Resolution:** ✅ FIXED - Separated ports intentional
- **[MARKER: Vector Ports]** VectorReaderPort + VectorWriterPort are DISTINCT
- Rationale: Allows read-only cache layers, write-disabled deployments
- Decision: Separation is APPROVED (not to be merged into single port)
- Files Updated:
  - ADR-003: Clarified port list (now 10 ports, not 9)
  - architecture.md: Updated Vector Index section

**Implementation Impact:**
- Phase 1.1 must register BOTH ports separately
- Factory pattern must create both readers and writers independently
- Tests must mock both ports independently

---

### FIX #2: Vector Index Black-Box Violation

**Gap:** STRATEGY_B Phase 1.1 code violates architecture rule
- Proposed: Direct import of ChromaVectorDB in container_builder.py
- Rule: "Never couple implementation details" (architecture.md #1)
- Violation: Direct adapter instantiation breaks black-box

**Resolution:** ✅ FIXED - Factory pattern requirement added
- **[MARKER: Factory Requirement]** MANDATORY for vector initialization
- New Pattern:
  ```python
  # ✅ CORRECT
  from bootstrap.vector.factory import VectorIndexFactory
  reader = VectorIndexFactory.create_reader()
  writer = VectorIndexFactory.create_writer()
  
  # ❌ WRONG (what STRATEGY_B proposed)
  from infrastructure.adapters.vector.chroma_adapter import ChromaVectorDB
  db = ChromaVectorDB(...)  # VIOLATES ARCH
  ```
- Files Updated:
  - architecture.md: Vector Index section (complete rewrite)
  - Added explicit "FACTORY PATTERN IS MANDATORY" marker

**Implementation Impact:**
- Phase 1.1 MUST use factory, not direct import
- New file needed: `bootstrap/vector/factory.py` (~30 LOC)
- container_builder.py calls factory, not adapter directly

---

### FIX #3: CampaignScopedContainer Not Defined

**Gap:** STRATEGY_B Phase 2B introduces core component without spec
- Proposed: CampaignScopedContainer (250 LOC) for campaign isolation
- Problem: Not mentioned in any ADR or architecture.md
- Impact: Agents don't know design decisions behind it

**Resolution:** ✅ FIXED - Added to ADR-005 as Level 2
- **[MARKER: CampaignScopedContainer Design]** Thread-local isolation (NEW concept)
- Layering: ADR-005 now has TWO levels of thread isolation
  - Level 1: AI Agent Threads (governance/AI work)
  - Level 2: Campaign Runtime Threads (concurrent campaign execution)
- Decision Points identified:
  1. Lock strategy (simple vs per-campaign locks)
  2. Cleanup timing (automatic vs explicit)
  3. Error handling (resource leaks, finalizers)
  4. Nesting support (allow nested campaign_scope()?)
- Files Updated:
  - ADR-005: Added Level 2 thread isolation section
  - architecture.md: Added Campaign Scoping section

**Implementation Impact:**
- Phase 2B has design guidance now
- Decision points MUST be resolved before implementation
- All 4 decision points marked as TBD (need user input)

---

## 🟡 MAJORS (6 fixes)

### FIX #4: EventBusPort Not in Port List

**Gap:** ADR-003 claims "9 Ports" but missing EventBusPort
- Problem: EventBusPort needed for Phase 1.3 (async lifecycle)
- Impact: Port list is incomplete, unclear if EventBusPort is 10th port or part of another

**Resolution:** ✅ FIXED - Added as 10th port
- **[MARKER: EventBusPort]** Explicitly added to port list
- Clarification: NOT part of ExecutorPort, separate for lifecycle management
- Files Updated:
  - ADR-003: Updated "9 ports" → "10 ports", added EventBusPort
  - Mark in implementation status

**Implementation Impact:**
- Total ports now 10 (was 9)
- Phase 1 must register EventBusPort
- Container has all 10 ports available

**Remaining Ambiguity:**
- Should EventBusPort be consolidated into ExecutorPort?
- Alternative decision: Keep separate (current)
- Status: DECISION POINT (recommend keep separate)

---

### FIX #5: RuntimeModule Layer Undefined

**Gap:** STRATEGY_B proposes RuntimeModule but layer is ambiguous
- Problem: Not clear if Layer 5, Layer 6, or new layer
- Impact: Agents don't know where runtime setup code belongs

**Resolution:** ✅ FIXED - Clarified as Layer 5 (Composition)
- **RuntimeModule** = Bootstrap DI composition layer
- **AppRuntime** = Application layer orchestration component
- Files Updated:
  - architecture.md: Added section 7 "Runtime Components"
  - Clarified Layer 5 vs Application layer distinction

**Implementation Impact:**
- Phase 1.2: RuntimeModule goes in `modules/runtime_module.py`
- Clear responsibilities defined
- Location in architecture documented

**Remaining Ambiguity:**
- Exact configuration parameters for RuntimeModule
- Status: MINOR (config details in Phase 1.2)

---

### FIX #6: AppRuntime Not Defined

**Gap:** STRATEGY_B introduces AppRuntime without spec definition
- Problem: Not in any ADR or architecture.md
- Impact: Unclear responsibilities, testing patterns, layer placement

**Resolution:** ✅ FIXED - Added to architecture.md section 7
- **AppRuntime** = Application layer orchestrator
- Responsibilities:
  - Startup/shutdown coordination
  - EventBus, Executor lifecycle management
  - Health checks
- Testing pattern: TBD (needs testing.md update)
- Files Updated:
  - architecture.md: Added AppRuntime definition
  - Reference to AppRuntime in contracts needed

**Implementation Impact:**
- Phase 1.2: AppRuntime instantiated and registered
- Phase 4: Testing patterns needed (testing.md update)
- Location: `application/runtime/app_runtime.py`

**Remaining Ambiguity:**
- Health check interface spec
- Error handling during shutdown
- Status: MINOR (implementation details)

---

### FIX #7: Async Lifecycle Testing Not in Spec

**Gap:** testing.md has no patterns for async lifecycle methods
- Problem: Phase 1.3 adds async methods to EventBusPort (start(), shutdown(), run_async())
- Impact: Agents don't know how to test them

**Resolution:** ✅ FIXED - Added reference to testing.md
- Need: New section "Async Lifecycle Testing" in testing.md
- Pattern: Mock async context managers, validate lifecycle calls
- Files Updated:
  - architecture.md: Added reference to testing.md#async-lifecycle-testing
  - testing.md: NEEDS UPDATE (see below)

**Implementation Impact:**
- Phase 1: Tests for EventBusPort async methods needed
- Testing pattern from testing.md guides implementation
- Status: BLOCKED on testing.md update

**Required testing.md Updates:**
- Add section: "Testing Async Lifecycle Methods"
- Pattern: How to test start(), shutdown() without real infrastructure
- Example: Mocking AsyncMock(spec=EventBusPort) for lifecycle tests

---

### FIX #8: 8-Layer Diagram Incomplete

**Gap:** architecture.md diagram shows only 6 entities, not full 8 layers
- Problem: Layers 7 (DTOs) and 8 (Controllers) missing from flow
- Impact: Visual model incomplete, agents confused about where layers fit

**Resolution:** ⚠️ PARTIAL - Identified but needs visual update
- Diagram needs:
  - Controllers layer (Layer 8, between API and UseCases)
  - DTOs layer (Layer 7, between Controllers and Adapters?)
  - Current flow: API → UseCase → Domain → Ports → Adapters
  - Complete flow: API → Controllers → DTOs → UseCase → Domain → Ports → Adapters
- Files to Update:
  - architecture.md: Diagram needs Mermaid rewrite
  - ADR-001: Might need layer clarification

**Implementation Impact:**
- Phase 0: Need diagram update before coding
- Not blocking Phase 1-4 (structural, not functional)
- Visual clarity aids onboarding

**Status:** 🟡 NOT YET FIXED (requires Mermaid diagram update)

---

### FIX #9: Lazy Initialization Not Documented

**Gap:** STRATEGY_B Phase 2A mentions lazy_registry.py but no design decision
- Problem: Why lazy initialization? What can/can't be lazy?
- Impact: Agents don't understand rationale or constraints

**Resolution:** ⚠️ IDENTIFIED - Needs feature-checklist.md update
- Decision Needed:
  - Which components should be lazy-initialized?
  - Recommendations: Vector index, Cache managers, Semantic cache
  - Not lazy: Bootstrap core (container, DI), RuntimeModule
- Pattern Needed: When/how to use lazy initialization
- Testing Pattern: How to validate lazy initialization works
- Files to Update:
  - feature-checklist.md: Add "Layer 0: Lazy Initialization" guidance
  - architecture.md: Could mention lazy pattern (optional)

**Implementation Impact:**
- Phase 2A needs design guidance
- Phase 2B might use lazy containers for campaigns
- Testing needs lazy-specific validation

**Status:** 🟡 NOT YET FIXED (needs feature-checklist.md update)

---

## 📊 SUMMARY TABLE

| # | Fix | Severity | Type | Status | Files Updated | Blocking? |
|---|-----|----------|------|--------|----------------|-----------|
| 1 | Vector port naming | 🔴 Critical | Contradiction | ✅ FIXED | ADR-003, arch.md | YES |
| 2 | Vector black-box violation | 🔴 Critical | Contradiction | ✅ FIXED | arch.md | YES |
| 3 | CampaignScopedContainer | 🔴 Critical | Gap | ✅ FIXED | ADR-005, arch.md | YES |
| 4 | EventBusPort missing | 🟡 Major | Gap | ✅ FIXED | ADR-003 | NO |
| 5 | RuntimeModule layer | 🟡 Major | Gap | ✅ FIXED | arch.md | NO |
| 6 | AppRuntime undefined | 🟡 Major | Gap | ✅ FIXED | arch.md | NO |
| 7 | Async lifecycle testing | 🟡 Major | Gap | ⚠️ PARTIAL | arch.md | NO |
| 8 | 8-layer diagram | 🟡 Major | Gap | ⚠️ TODO | — | NO |
| 9 | Lazy initialization | 🟡 Major | Gap | ⚠️ TODO | — | NO |

---

## 🎯 DECISION POINTS REQUIRING USER INPUT

### [DECISION: CampaignScopedContainer - Lock Strategy]
Options:
1. Simple threading.Lock() on _containers dict
2. Per-campaign locks for fine-grained concurrency
Recommendation: Option 1 (simpler, sufficient for concurrent campaigns)

### [DECISION: CampaignScopedContainer - Cleanup Timing]
Options:
1. Automatic on context exit (current plan)
2. Explicit cleanup_campaign() call
3. TTL-based cleanup
Recommendation: Option 1 (context manager is cleanest)

### [DECISION: CampaignScopedContainer - Error Handling]
Options:
1. Resource leak if context not closed (bad)
2. Add finalizer for cleanup
3. Strict validation (error on scope exit)
Recommendation: Option 2 (finalizer prevents leaks)

### [DECISION: CampaignScopedContainer - Nesting Support]
Options:
1. Allow nested campaign_scope() calls (with stack)
2. No nesting (raise error if attempted)
Recommendation: Option 2 (simpler, prevents confusion)

### [DECISION: EventBusPort vs ExecutorPort]
Options:
1. Keep separate (current, allows independent lifecycle)
2. Consolidate into ExecutorPort
Recommendation: Option 1 (separate concerns, better modularity)

---

## 📝 NEXT STEPS

**Before Phase 1:**
- [ ] Resolve 5 DECISION POINTS above
- [ ] Update testing.md: Add "Async Lifecycle Testing" section
- [ ] Update architecture.md diagram: Add missing layers (Mermaid)
- [ ] Update feature-checklist.md: Add lazy initialization guidance

**After Decision Points Resolved:**
- [ ] Phase 1: Implement with all decision points clarified
- [ ] Phase 2A: Bootstrap reorganization with lazy pattern
- [ ] Phase 2B: CampaignScopedContainer with resolved design

---

## ✅ VERIFICATION CHECKLIST

Before starting Phase 1:
- [ ] All 9 fixes reviewed and understood
- [ ] Decision points resolved (or documented why deferred)
- [ ] 5 DECISION POINTS answered
- [ ] testing.md updated with async lifecycle patterns
- [ ] architecture.md diagram updated (8 layers visible)
- [ ] feature-checklist.md has lazy initialization guidance
- [ ] Team agrees with all spec updates

---

## 📚 FILES MODIFIED

1. `/docs/ia/decisions/ADR-003-ports-adapters-pattern.md`
   - Updated port count (9 → 10)
   - Added VectorReaderPort/VectorWriterPort clarification
   - Added EventBusPort with implementation notes

2. `/docs/ia/decisions/ADR-005-thread-isolation-mandatory.md`
   - Added Level 2 (Campaign Runtime Threads)
   - Added CampaignScopedContainer pattern
   - Added 4 decision points (TBD)

3. `/docs/ia/specs/_shared/architecture.md`
   - Updated Vector Index section (factory pattern mandatory)
   - Added section 7: Runtime Components (AppRuntime + RuntimeModule)
   - Added section 8: Campaign Scoping (NEW)
   - References to decision markers throughout

**Files Needing Updates (TODO):**
- `/docs/ia/specs/_shared/testing.md` — Add async lifecycle testing patterns
- `/docs/ia/specs/_shared/feature-checklist.md` — Add lazy initialization guidance
- `/docs/ia/specs/_shared/architecture.md` — Update 8-layer diagram (Mermaid)
