# 🎯 DECISION POINTS — Architecture & Engineering (April 2026)

**Purpose:** Consolidate 8 critical design decisions for Phase 1+ implementation

**Status:** PENDING USER INPUT (Recommendations provided)

**Impact:** All Phase 2B+ architecture and code generation depends on these decisions

---

## 📊 DECISION MATRIX

| # | Decision | Impact | Blocking | Recommendation | Your Choice |
|---|----------|--------|----------|-----------------|-------------|
| 1 | Lock strategy | CampaignScopedContainer | Phase 2B | Simple | ☐ A ☐ B |
| 2 | Cleanup timing | Lifecycle management | Phase 2B | Auto/Context | ☐ A ☐ B ☐ C |
| 3 | Error handling | Resource safety | Phase 2B | Finalizer | ☐ A ☐ B ☐ C |
| 4 | Nesting support | API design | Phase 2B | No nesting | ☐ A ☐ B |
| 5 | EventBusPort | Port independence | Phase 1 | Keep separate | ☐ A ☐ B |
| 6 | Memory versioning | Echo system | Phase 2B | Event sourcing | ☐ A ☐ B ☐ C |
| 7 | Canonical immutability | Memory semantics | Phase 2B | Strict immutable | ☐ A ☐ B ☐ C |
| 8 | Cache invalidation | Performance | Phase 3 | Event-based | ☐ A ☐ B ☐ C |

---

## 🔴 ORIGINAL 5: CampaignScopedContainer Design

These decisions affect **Phase 2B: Campaign Scoping** (1-2 days, 250 LOC)

---

### DECISION #1: Lock Strategy for Concurrent Campaigns

**Question:** How should concurrent `campaign_scope()` calls be protected?

**Context:**
```
Scenario: Two campaigns running in parallel
├─ Thread 1: campaign_scope("campaign_001")
└─ Thread 2: campaign_scope("campaign_002")

Problem: Both access shared _containers dict
Solution: Need synchronization strategy
```

**Options:**

**Option A: Simple threading.Lock() (RECOMMENDED)**
```python
class CampaignScopedContainer:
    _lock = threading.Lock()
    _containers = {}
    
    def campaign_scope(self, campaign_id):
        with self._lock:
            if campaign_id not in self._containers:
                self._containers[campaign_id] = self._create()
        # Thread-local assignment (no lock needed)
        self._local.campaign_id = campaign_id
        yield self._containers[campaign_id]
```

**Pros:**
- Simple, easy to understand
- Sufficient for typical concurrent load (5-10 campaigns)
- Fast (lock only during creation)

**Cons:**
- All campaigns compete for single lock
- Potential bottleneck if 100+ campaigns concurrent
- Not fine-grained

---

**Option B: Per-Campaign Locks (Alternative)**
```python
class CampaignScopedContainer:
    _locks = {}  # Per-campaign locks
    _containers = {}
    
    def campaign_scope(self, campaign_id):
        # Create lock if needed
        if campaign_id not in self._locks:
            self._locks[campaign_id] = threading.Lock()
        
        with self._locks[campaign_id]:
            if campaign_id not in self._containers:
                self._containers[campaign_id] = self._create()
        # ...
```

**Pros:**
- Fine-grained concurrency
- Scales better (100+ concurrent campaigns)

**Cons:**
- More complex code
- Lock dictionary itself needs protection
- Overkill for typical use case

---

**Recommendation:** **Option A (Simple Lock)**
- Rationale: Typical deployment has 5-10 concurrent campaigns
- Can upgrade to Option B if benchmarks show bottleneck
- Start simple, optimize if needed

**Engineering Impact:** 5 LOC in CampaignScopedContainer.__init__()

---

### DECISION #2: Cleanup Timing

**Question:** When/how should campaign containers be cleaned up?

**Context:**
```
Lifecycle:
Campaign starts → campaign_scope() context entered
Campaign progresses → container used
Campaign ends → context exited → container not needed

Problem: When to free resources? How to prevent leaks?
```

**Options:**

**Option A: Automatic on Context Exit (RECOMMENDED)**
```python
@contextmanager
def campaign_scope(self, campaign_id: str):
    try:
        self._local.campaign_id = campaign_id
        yield self._containers[campaign_id]
    finally:
        # Automatic cleanup on context exit
        self.cleanup_campaign(campaign_id)

# Usage
with container_singleton.campaign_scope("c_123"):
    service = resolve(NarrativeServicePort)
    await service.run()
# Cleanup happens automatically here ✅
```

**Pros:**
- Automatic (no manual calls)
- Exception-safe (finally block)
- Clean API (context manager pattern)
- Prevents resource leaks

**Cons:**
- Strict timing (cleanup on scope exit, not later)

---

**Option B: Explicit Cleanup (Alternative)**
```python
# Usage
container_singleton.campaign_scope("c_123")
service = resolve(NarrativeServicePort)
await service.run()
container_singleton.cleanup_campaign("c_123")  # Manual cleanup
```

**Pros:**
- Manual control

**Cons:**
- Error-prone (easy to forget cleanup)
- Requires discipline
- Can leak if exception before cleanup call

---

**Option C: TTL-Based Cleanup (Alternative)**
```python
class CampaignScopedContainer:
    _container_ttl = 3600  # 1 hour
    
    async def cleanup_expired(self):
        now = time.time()
        expired = [
            cid for cid, (container, created) in self._containers.items()
            if (now - created) > self._container_ttl
        ]
        for cid in expired:
            del self._containers[cid]

# Background task
@periodic_task(interval=300)  # Every 5 min
async def gc_expired_containers():
    await container_singleton.cleanup_expired()
```

**Pros:**
- Automatic background cleanup
- Doesn't require manual calls
- Forgiving (container lives even after campaign ends)

**Cons:**
- Memory can accumulate before TTL expires
- Harder to debug (cleanup timing unpredictable)
- Need background task

---

**Recommendation:** **Option A (Automatic Context Exit)**
- Rationale: Clean API, exception-safe, no resource leaks
- Standard Python pattern (with statement)
- Easy to understand and verify

**Engineering Impact:** 10 LOC in campaign_scope() implementation

---

### DECISION #3: Error Handling - Resource Cleanup on Improper Exit

**Question:** What if context manager exits without proper closure (e.g., exception, thread crash)?

**Context:**
```
Scenario: Exception during campaign execution
try:
    with campaign_scope("c_123"):
        await service.execute()  # ← Crashes here
finally:  # Does cleanup happen?
    ...

Risk: If exception, container resources (memory, connections) leak
```

**Options:**

**Option A: Accept Resource Leak (Not Recommended)**
```python
@contextmanager
def campaign_scope(self, campaign_id):
    self._local.campaign_id = campaign_id
    try:
        yield self._containers[campaign_id]
    finally:
        pass  # No cleanup
    # Container stays in memory forever if exception
```

**Cons:**
- Memory leaks accumulate
- Bad for long-running servers
- Unacceptable

---

**Option B: Finalizer-Based Cleanup (RECOMMENDED)**
```python
import weakref

class CampaignScopedContainer:
    def campaign_scope(self, campaign_id: str):
        container = self._containers.get(campaign_id)
        
        # Register finalizer to cleanup if container GC'd
        def cleanup_on_gc():
            self.cleanup_campaign(campaign_id)
        
        weakref.finalize(container, cleanup_on_gc)
        
        # Context manager
        @contextmanager
        def scope_manager():
            try:
                self._local.campaign_id = campaign_id
                yield container
            finally:
                self.cleanup_campaign(campaign_id)
        
        return scope_manager()
```

**Pros:**
- Automatic cleanup on context exit
- Also cleans up if exception occurs
- Python garbage collects finalizer
- Fail-safe

**Cons:**
- Slightly more complex
- Finalizers can be unpredictable timing

---

**Option C: Strict Validation (Alternative)**
```python
@contextmanager
def campaign_scope(self, campaign_id: str):
    if campaign_id in self._local.campaign_stack:
        raise RuntimeError("Nested scope not allowed")
    
    self._local.campaign_stack.append(campaign_id)
    try:
        yield self._containers[campaign_id]
    finally:
        self._local.campaign_stack.pop()
        # Explicit cleanup only on proper exit
        self.cleanup_campaign(campaign_id)
```

**Pros:**
- Clear error on misuse
- Enforces correct usage

**Cons:**
- Still doesn't handle all error cases
- Requires discipline

---

**Recommendation:** **Option B (Finalizer)**
- Rationale: Automatic cleanup guaranteed, handles exceptions, Python idiomatic
- Trade-off: Slightly more complex but worth it for safety
- Combines Options A + C best practices

**Engineering Impact:** 15 LOC (finalizer registration + context manager)

---

### DECISION #4: Nesting Support

**Question:** Should nested `campaign_scope()` calls be allowed?

**Context:**
```
Scenario 1: Sequential scopes (OK)
with campaign_scope("c_001"):
    # ...
with campaign_scope("c_002"):  # Different campaign, sequential
    # ...

Scenario 2: Nested scopes (Should this work?)
with campaign_scope("c_001"):
    with campaign_scope("c_002"):  # Nested campaign scope
        # Which campaign is "current"? c_001 or c_002?
        service = resolve(NarrativeServicePort)
```

**Options:**

**Option A: No Nesting - Raise Error (RECOMMENDED)**
```python
@contextmanager
def campaign_scope(self, campaign_id: str):
    if hasattr(self._local, 'campaign_id') and self._local.campaign_id:
        raise RuntimeError(
            f"Cannot nest campaign_scope. Already in {self._local.campaign_id}, "
            f"tried to enter {campaign_id}. Use sequential scopes instead."
        )
    # ...
```

**Pros:**
- Simple semantics (at most one campaign at a time per thread)
- Error on misuse (clearer)
- Prevents confusion

**Cons:**
- Not flexible for advanced use cases

---

**Option B: Allow Nesting with Stack (Alternative)**
```python
@contextmanager
def campaign_scope(self, campaign_id: str):
    # Maintain stack of campaigns
    if not hasattr(self._local, 'campaign_stack'):
        self._local.campaign_stack = []
    
    self._local.campaign_stack.append(campaign_id)
    try:
        yield self._containers[campaign_id]
    finally:
        self._local.campaign_stack.pop()

# Usage
with campaign_scope("c_001"):
    # Current: c_001
    with campaign_scope("c_002"):
        # Current: c_002 (top of stack)
        service = resolve(NarrativeServicePort)  # Uses c_002
    # Current: c_001 again (after inner context exits)
```

**Pros:**
- Allows advanced use cases
- Stack provides clear priority

**Cons:**
- More complex to reason about
- Easy to make mistakes
- Harder to debug

---

**Recommendation:** **Option A (No Nesting)**
- Rationale: RPG campaigns are sequential, not nested
- If need multiple campaigns: use sequential scopes
- Simpler semantics, easier to debug
- Can add Option B later if needed

**Engineering Impact:** 3 LOC (guard clause in campaign_scope)

---

### DECISION #5: EventBusPort Independence

**Question:** Should EventBusPort be a separate port or part of ExecutorPort?

**Context:**
```
Current state: EventBusPort proposed as 10th port (separate from ExecutorPort)

Question: Are they related enough to merge?
- ExecutorPort: CPU-bound task execution
- EventBusPort: Async event dispatch + lifecycle

Similarities:
- Both async
- Both component lifecycle management

Differences:
- ExecutorPort: Task execution (CPU focus)
- EventBusPort: Event dispatch (IO/coordination focus)
```

**Options:**

**Option A: Keep Separate (RECOMMENDED)**
```python
# ExecutorPort: CPU-bound execution
class ExecutorPort(Protocol):
    async def run_sync(self, func: Callable, *args) -> Any: ...
    async def run_async(self, coro: Coroutine) -> Any: ...

# EventBusPort: Event dispatch + lifecycle
class EventBusPort(Protocol):
    async def start(self) -> None: ...
    async def shutdown(self) -> None: ...
    async def publish(self, event: object) -> None: ...
    async def subscribe(self, event_type: type, handler: Callable) -> None: ...
```

**Pros:**
- Clear separation of concerns
- Can implement independently
- EventBus can be mocked separately
- Easier to test each port in isolation

**Cons:**
- Two ports instead of one
- Might feel redundant

---

**Option B: Consolidate into ExecutorPort (Alternative)**
```python
class ExecutorPort(Protocol):
    # CPU execution
    async def run_sync(self, func: Callable, *args) -> Any: ...
    async def run_async(self, coro: Coroutine) -> Any: ...
    
    # Event dispatch
    async def publish(self, event: object) -> None: ...
    async def subscribe(self, event_type: type, handler: Callable) -> None: ...
    
    # Lifecycle
    async def start(self) -> None: ...
    async def shutdown(self) -> None: ...
```

**Pros:**
- Single port for all async operations
- Simpler DI container

**Cons:**
- Violates single responsibility (execution + events)
- Harder to mock just one concern
- Harder to implement (adapter handles too much)
- Harder to test

---

**Recommendation:** **Option A (Keep Separate)**
- Rationale: Single responsibility principle (execution ≠ events)
- Easier to test, mock, implement
- More modular
- Aligns with Ports & Adapters pattern (ADR-003)

**Engineering Impact:** Already designed separately in ADR-003

---

## 🆕 NEW 3: Memory Hierarchy & Echo System

These decisions affect **Phase 2B/3+: Multi-Level Memory** implementation

---

### DECISION #6: Memory Versioning Strategy

**Question:** How should we track memory changes to support echo system?

**Context:**
```
Requirement: Support "echoes" (previous campaign memories in new campaigns)

Problem: How to know:
- What was the state of memory at time T?
- What changed between versions?
- Which version to expose as "echo"?

Solution needed: Full history tracking
```

**Options:**

**Option A: Simple Mutation (Not Recommended)**
```json
{
  "id": "event_001",
  "content": "Hero defeated dragon",
  "updated_at": "2026-03-20T20:15:00Z"
  // No history, just current state
}
```

**Cons:**
- Can't know what was true on day X
- Can't audit changes
- Can't properly support echoes

---

**Option B: Snapshot-Based Versioning (Alternative)**
```json
{
  "id": "event_001",
  "snapshots": [
    {
      "version": 1,
      "content": "Hero started quest",
      "timestamp": "2026-03-15T14:30:00Z"
    },
    {
      "version": 2,
      "content": "Hero defeated dragon",
      "timestamp": "2026-03-20T20:15:00Z"
    }
  ]
}
```

**Pros:**
- Simple versioning
- Easy to understand

**Cons:**
- Coarse-grained (only full snapshots)
- Hard to track granular changes
- Loses metadata about what changed

---

**Option C: Event Sourcing (RECOMMENDED)**
```json
{
  "id": "event_001",
  "versions": {
    "1": {
      "timestamp": "2026-03-15T14:30:00Z",
      "content": "Hero started quest",
      "actor": "game_engine",
      "action": "CREATE"
    },
    "2": {
      "timestamp": "2026-03-16T10:00:00Z",
      "content": "Hero reached first milestone",
      "actor": "game_engine",
      "action": "UPDATE",
      "previous_version": "1",
      "changes": {"milestone": "reached"}
    },
    "3": {
      "timestamp": "2026-03-20T20:15:00Z",
      "content": "Hero defeated dragon",
      "actor": "game_engine",
      "action": "UPDATE",
      "previous_version": "2",
      "changes": {"quest_status": "completed"}
    }
  },
  "current_version": 3
}
```

**Pros:**
- Full history with metadata
- Can reconstruct state at any time
- Enables audit trail
- Supports temporal queries
- Perfect for echo system

**Cons:**
- More storage
- More complex queries

---

**Recommendation:** **Option C (Event Sourcing)**
- Rationale: Echo system needs to know "what was true when"
- Enables temporal queries
- Supports audit trail (important for AI decisions)
- Can replay history
- Industry best practice for audit

**Engineering Impact:** 50-80 LOC for versioning logic

---

### DECISION #7: Canonical Memory Immutability

**Question:** How strictly should canonical memory be protected?

**Context:**
```
Business Rule: Canonical memory is world baseline (immutable)

Implementation options:
- Soft: Can modify, but discouraged
- Medium: Modification tracked but allowed
- Strict: Error on modification attempt
```

**Options:**

**Option A: Soft - Warnings Only (Not Recommended)**
```python
async def update_canonical(memory_id: str, new_content: str):
    logger.warning("Modifying canonical memory - usually not recommended")
    # Allow modification silently
    await storage_port.save(memory_id, new_content)
```

**Cons:**
- Defeats immutability
- Easy to accidentally modify canonical facts
- Breaks echo system (echoes would point to wrong data)

---

**Option B: Medium - Audit Trail (Alternative)**
```python
async def update_canonical(memory_id: str, new_content: str):
    # Track modification
    audit_log = {
        "original": await storage_port.get(memory_id),
        "new": new_content,
        "modified_at": now(),
        "modifier": current_user()
    }
    await audit_port.log(audit_log)
    # Allow modification
    await storage_port.save(memory_id, new_content)
```

**Pros:**
- Audit trail of modifications
- Allows emergency updates

**Cons:**
- Still breaks echo system
- Audit trail doesn't prevent mistakes

---

**Option C: Strict - Immutable (RECOMMENDED)**
```python
async def update_canonical(memory_id: str, new_content: str):
    existing = await storage_port.get(memory_id)
    if existing.type == "CANONICAL":
        raise ImmutableMemoryError(
            f"Cannot modify canonical memory {memory_id}. "
            f"Create new fact instead if needed."
        )
    await storage_port.save(memory_id, new_content)
```

**Pros:**
- True immutability
- Protects echo system
- Clear enforcement
- Prevents accidents

**Cons:**
- Strict (can't fix mistakes directly)
- Requires creating new facts for corrections

---

**Recommendation:** **Option C (Strict Immutable)**
- Rationale: Echo system depends on canonical facts never changing
- If mistake: create new fact, deprecate old one
- Clear enforcement prevents accidents
- Aligns with business rules

**Engineering Impact:** 10 LOC for immutability check

---

### DECISION #8: Cache Invalidation Strategy

**Question:** How should genre-level cache be invalidated when stale?

**Context:**
```
Scenario: Genre cache has data from campaign_001 (30 days ago)
├─ New campaign_003 starts
├─ Should it access 30-day-old cache?
├─ What if world changed? (Unlikely but possible)
└─ When to refresh cache?

Options: Time-based, Event-based, or Manual?
```

**Options:**

**Option A: TTL-Based (Time-To-Live)**
```python
genre_cache = {
    "id": "cache_001",
    "content": "Zaibatsu megacorp...",
    "created_at": "2026-02-01",
    "ttl": 7776000,  # 90 days
    "expires_at": "2026-05-01"
}

# On new campaign:
if cache["expires_at"] < now():
    cache_is_stale = True  # Refresh
else:
    cache_is_current = True  # Reuse
```

**Pros:**
- Simple, predictable
- No external dependencies

**Cons:**
- Arbitrary TTL (why 90 days?)
- Might use stale cache if world changed
- Cache expires even if still valid

---

**Option B: Event-Based (Reactive) (RECOMMENDED)**
```python
# When world/genre changes: emit event
class WorldChangedEvent:
    world_id: str
    genre_id: str  # optional, if genre-specific change
    change_type: str  # "canonical_updated", "genre_template_changed"

# Cache subscribes to events
def on_world_changed(event: WorldChangedEvent):
    if event.genre_id:
        self.invalidate_genre_cache(event.genre_id)
    else:
        self.invalidate_world_cache()
    
    # Cache will be refreshed on next access
```

**Pros:**
- Reactive (responds to actual changes)
- No stale cache unless world actually changed
- Precise invalidation

**Cons:**
- Requires event system
- More complex

---

**Option C: Manual Invalidation (Alternative)**
```python
# Admin manually triggers refresh
async def invalidate_genre_cache(world_id: str, genre_id: str):
    cache_key = f"{world_id}_{genre_id}"
    del self._genre_caches[cache_key]
    # Cache will rebuild on next access

# Usage: admin calls when needed
await admin_service.invalidate_cache("cyberpunk_2087", "cyberpunk")
```

**Pros:**
- Full manual control
- No surprises

**Cons:**
- Requires human intervention
- Easy to forget
- Not automated

---

**Recommendation:** **Option B (Event-Based)**
- Rationale: React to actual changes, not arbitrary time
- Combines correctness + automation
- Works with existing EventBusPort
- No surprise staleness

**Engineering Impact:** 30-50 LOC for event listeners

---

## ✅ SUMMARY & NEXT STEPS

### Current Status

| Decision | Option | Impact | Ready? |
|----------|--------|--------|---------|
| 1 | Lock strategy | CampaignScopedContainer | Pending |
| 2 | Cleanup timing | Context manager | Pending |
| 3 | Error handling | Finalizer + context | Pending |
| 4 | Nesting support | Sequential only | Pending |
| 5 | EventBusPort | Keep separate | Pending |
| 6 | Memory versioning | Event sourcing | Pending |
| 7 | Canonical immutable | Strict (error on modify) | Pending |
| 8 | Cache invalidation | Event-based | Pending |

### Action Items

1. **Answer all 8 decisions** (provide your choice for each)
2. **Update architecture specs** with chosen approaches
3. **Generate code templates** for Phase 1-3 implementation
4. **Update STRATEGY_B_OPTIMIZED.md** with decision impacts

### Timeline Impact

- **Phase 0 (TODAY):** Make 8 decisions ← YOU ARE HERE
- **Phase 1 (3-4h):** DI fixes (decisions 1-5 not needed yet)
- **Phase 2A (1-2d):** Bootstrap reorganization
- **Phase 2B (1-2d):** Campaign scoping (decisions 1-5 needed)
- **Phase 3 (1-2d):** Memory hierarchy (decisions 6-8 needed)

**Blocking?** Decisions 1-5 block Phase 2B start, but Phase 1 can start immediately.

---

## 📋 YOUR DECISION FORM

Please answer each decision:

```
DECISION #1: Lock Strategy
[ ] Option A (Simple threading.Lock) - RECOMMENDED
[ ] Option B (Per-campaign locks)

DECISION #2: Cleanup Timing
[ ] Option A (Automatic context exit) - RECOMMENDED
[ ] Option B (Explicit cleanup)
[ ] Option C (TTL-based)

DECISION #3: Error Handling
[ ] Option A (Accept leak)
[ ] Option B (Finalizer) - RECOMMENDED
[ ] Option C (Strict validation)

DECISION #4: Nesting Support
[ ] Option A (No nesting) - RECOMMENDED
[ ] Option B (Allow with stack)

DECISION #5: EventBusPort
[ ] Option A (Keep separate) - RECOMMENDED
[ ] Option B (Consolidate into ExecutorPort)

DECISION #6: Memory Versioning
[ ] Option A (Simple mutation)
[ ] Option B (Snapshots)
[ ] Option C (Event sourcing) - RECOMMENDED

DECISION #7: Canonical Immutability
[ ] Option A (Soft - warnings)
[ ] Option B (Medium - audit trail)
[ ] Option C (Strict - error) - RECOMMENDED

DECISION #8: Cache Invalidation
[ ] Option A (TTL-based)
[ ] Option B (Event-based) - RECOMMENDED
[ ] Option C (Manual)
```

---

**Ready to proceed?** Provide your answers above! 🚀
