# 🎯 8 DECISÕES REFATORADAS — Funcionalidades + SPEC Mandates (April 2026)

**Contexto:** Refactor desconsiderando código truncado, priorizando FUNCIONALIDADES > SPEC > implementação

**Mandates SPEC (6 ADRs Invioláveis):**
- ADR-001: Clean Architecture 8-layer
- ADR-002: Async-first, no blocking I/O
- ADR-003: Ports & Adapters (18 ports)
- ADR-004: Vector index black-box factory pattern
- ADR-005: Thread isolation (2 levels)
- ADR-006: Event sourcing append-only

**Setups de Deployment (todos devem funcionar):**
- Local: LLM local + Embedding local
- Hybrid: LLM local + Embedding remoto (cloud)
- Remote: LLM remoto + Embedding remoto

---

# 🎯 DECISÃO #1: Campaign Isolation Strategy

## 🎯 FUNCIONALIDADE HABILITADA

```
Requisito: Duas campanhas rodando em paralelo (Thread A + Thread B)
NÃO devem contaminar contexto uma da outra

Exemplo:
├─ Campaign A (Medieval): "Player está na taverna de Winterhold"
├─ Campaign B (Cyberpunk): "Player está no nightclub Neon Tokyo"
└─ Requisito: Cada campaign vê seu próprio contexto (ISOLADO)

Quebra-requisito se:
├─ Campaign A acessa memoria de Campaign B
├─ Campaign B acessa services de Campaign A
├─ Cleanup de A deixa lixo em B
└─ Exception em A afeta B
```

## 🏛️ SPEC VALIDATION

**ADR-005:** "Thread isolation mandatory at 2 LEVELS"
- ✅ Level 1: AI agent threads (governance)
- ✅ Level 2: Campaign runtime threads (concurrent execution)

**ADR-001:** Clean Architecture Layer 5 (Application Composition)
- ✅ DI Container per campaign in thread-local storage

**ADR-002:** Async-first
- ✅ Context manager (async-compatible)
- ✅ No blocking on thread lock

**ADR-003:** Ports & Adapters
- ✅ Container resolves ports (not adapters)
- ✅ Each campaign gets isolated port implementations

## 💡 WORLD CLASS PATTERNS

**Pattern: Thread-Local Storage + Context Manager**
```
Standard Pattern Used By:
- asyncio (context vars)
- Django (thread-local request context)
- FastAPI (dependency injection per request)
- Twisted (deferred context)

Advantages:
✅ No explicit passing of campaign_id through call stack
✅ Implicit context available anywhere
✅ Python idiomatic
✅ Works with async/await
```

## 📊 SETUP COMPATIBILITY

| Setup | Requirement | Impact |
|-------|-------------|--------|
| **Local** | Thread-local dict | ✅ No issue |
| **Hybrid** | Thread-local dict + RemoteVectorPort | ✅ No issue |
| **Remote** | Thread-local dict + RemoteLLMPort + RemoteVectorPort | ✅ No issue |

*No setup-specific concerns. Thread-local is universal.*

## 🎯 DECISION

**Choose Option:** Simple Lock (threading.Lock) + Context Manager + Thread-Local

```python
# PSEUDO-CODE (functional spec only)
class CampaignScopedContainer:
    _lock = threading.Lock()          # 1 lock for all campaigns
    _containers = {}                  # {campaign_id: container}
    _local = threading.local()        # Thread-local context
    
    @contextmanager
    def campaign_scope(self, campaign_id: str):
        """Isolate campaign context in thread-local storage"""
        # Ensure thread-safety for container creation
        with self._lock:
            if campaign_id not in self._containers:
                self._containers[campaign_id] = self._create_container()
            container = self._containers[campaign_id]
        
        # Thread-local assignment (no lock needed)
        prev_campaign_id = getattr(self._local, 'campaign_id', None)
        self._local.campaign_id = campaign_id
        
        try:
            yield container
        finally:
            # Restore previous campaign context
            if prev_campaign_id:
                self._local.campaign_id = prev_campaign_id
            else:
                del self._local.campaign_id
            
            # Cleanup happens here (see Decision #2)
```

**World Class Reasoning:**
- ✅ Respects all 6 ADRs
- ✅ Idiomatic Python
- ✅ Works across all 3 setups
- ✅ Clear semantics (one campaign per thread at a time)
- ✅ No deadlock risk (single lock)

---

# 🎯 DECISÃO #2: Resource Lifecycle Management

## 🎯 FUNCIONALIDADE HABILITADA

```
Requisito: Clean shutdown of campaign resources

Scenarios:
1. Normal: Session ends gracefully
   ├─ Close vector connections
   ├─ Flush response cache
   ├─ Persist game state
   └─ Free memory
   
2. Abnormal: Exception during gameplay
   ├─ Still close connections
   ├─ Still persist state
   └─ Still free memory
   
3. Emergency: Thread crash / process exit
   ├─ Best-effort cleanup
   └─ Minimize resource leaks

Quebra-requisito se:
├─ Resources not cleaned (memory leak)
├─ Connections left open (database lock)
├─ Cache not flushed (data loss)
└─ Cleanup doesn't happen on exception
```

## 🏛️ SPEC VALIDATION

**ADR-002:** Async-first
- ✅ Cleanup must be async (connections, disk I/O)
- ✅ No blocking during cleanup

**ADR-006:** Event sourcing
- ✅ Cleanup must persist events before closing
- ✅ Append-only: no mutations

**ADR-003:** Ports & Adapters
- ✅ Call port.shutdown() (not adapter implementation)
- ✅ Each port responsible for own cleanup

## 💡 WORLD CLASS PATTERNS

**Pattern: RAII + Finalizer (Resource Acquisition Is Initialization)**
```
Standard Pattern Used By:
- C++: Destructors
- Rust: Drop trait
- Python: context managers + __del__
- Python async: AsyncExitStack

Advantages:
✅ Automatic resource cleanup
✅ Exception-safe (finally block)
✅ Deterministic cleanup timing
✅ Fail-safe (finalizer backup)
```

## 📊 SETUP COMPATIBILITY

| Setup | Concern | Solution |
|-------|---------|----------|
| **Local** | Close local connections | ✅ Immediate shutdown |
| **Hybrid** | Close local LLM, remote vector | ✅ Async cleanup on both |
| **Remote** | Close remote connections | ✅ Graceful disconnect |

## 🎯 DECISION

**Choose Option:** Automatic on Context Exit (finally block) + Async Cleanup + Finalizer Backup

```python
# PSEUDO-CODE (functional spec)
@contextmanager
async def campaign_scope(self, campaign_id: str):
    """Manage campaign lifecycle (init + cleanup)"""
    container = self._get_or_create_container(campaign_id)
    
    # Register finalizer as backup cleanup
    def finalizer():
        asyncio.create_task(self._cleanup_campaign_async(campaign_id))
    
    weakref.finalize(container, finalizer)
    
    # Set thread-local context
    self._local.campaign_id = campaign_id
    
    try:
        yield container
    finally:
        # Graceful shutdown
        await self._cleanup_campaign_async(campaign_id)
        
        # Cleanup helpers:
        # 1. Call all port.shutdown() methods
        # 2. Wait for pending operations
        # 3. Persist final state
        # 4. Release container reference
```

**Async Cleanup Sequence (Order Matters - ADR-006):**
```
1. Stop accepting new events (pause event bus)
2. Wait for in-flight operations (executor.wait_all())
3. Persist accumulated events (append-only commit)
4. Close vector connections (remote or local)
5. Close LLM connections (if exists)
6. Flush caches
7. Update campaign state (END_CAMPAIGN event)
8. Release container from _containers dict
```

**World Class Reasoning:**
- ✅ Exception-safe (finally always runs)
- ✅ Fail-safe (finalizer backup)
- ✅ Async throughout (no blocking)
- ✅ Event sourcing compatible (append-only persist)
- ✅ Works across all 3 setups

---

# 🎯 DECISÃO #3: Concurrency Safety Strategy

## 🎯 FUNCIONALIDADE HABILITADA

```
Requisito: Multiple campaigns + Multiple threads = No data corruption

Scenarios:
1. Normal case:
   ├─ Campaign A in Thread 1
   ├─ Campaign B in Thread 2
   └─ Both use container concurrently
   
2. Fast switching:
   ├─ Thread 1: Campaign A for 100ms
   ├─ Thread 1: Campaign B for 100ms
   ├─ Thread 1: Campaign A again
   └─ No context bleeding
   
3. Exception case:
   ├─ Campaign A exception in Thread 1
   ├─ Container state still valid
   └─ Campaign B can continue

Quebra-requisito se:
├─ Race condition on _containers dict
├─ Context bleeding between campaigns
├─ Exception leaves lock held
└─ Deadlock between campaigns
```

## 🏛️ SPEC VALIDATION

**ADR-005:** Thread isolation mandatory
- ✅ Two levels: governance level + runtime level
- ✅ No cross-campaign state

**ADR-002:** Async-first (no blocking)
- ✅ Lock contention should be minimal
- ✅ Lock held only during container creation (fast)

**ADR-001:** Clean Architecture
- ✅ Lock is infrastructure concern (Layer 7)
- ✅ Not visible to domain logic

## 💡 WORLD CLASS PATTERNS

**Pattern: Reader-Writer Lock vs Simple Lock**
```
Context:
- Most campaigns are READ-HEAVY (resolving ports)
- Few campaigns are WRITE-HEAVY (creating container)
- Lock needed only during creation (10ms)

World Class Choice:
✅ Simple Lock (threading.Lock)
- Sufficient for typical RPG workload (5-10 concurrent campaigns)
- Simpler to understand and maintain
- Lower overhead
- Can upgrade to RWLock if benchmarks show bottleneck

Alternative (if 100+ concurrent campaigns):
⚠️  Reader-Writer Lock (threading.RWLock) - Python 3.13+
- Allows multiple readers (port resolution)
- Exclusive write (container creation)
- More complex, more overhead
```

## 📊 SETUP COMPATIBILITY

| Setup | Concern | Pattern |
|-------|---------|---------|
| **Local** | Low contention | Simple Lock sufficient |
| **Hybrid** | Low contention | Simple Lock sufficient |
| **Remote** | Low contention (async I/O) | Simple Lock sufficient |

*No setup needs fine-grained locking.*

## 🎯 DECISION

**Choose Option:** Simple threading.Lock + Exception-safe acquisition

```python
# PSEUDO-CODE (functional spec)
class CampaignScopedContainer:
    _lock = threading.Lock()  # Single lock, fast
    _containers = {}
    
    def _get_or_create_container(self, campaign_id):
        """Thread-safe container creation"""
        # Fast path: already exists (no lock)
        if campaign_id in self._containers:
            return self._containers[campaign_id]
        
        # Slow path: create new container (with lock)
        with self._lock:
            # Double-check (another thread might have created it)
            if campaign_id in self._containers:
                return self._containers[campaign_id]
            
            # Create and store
            container = self._create_new_container()
            self._containers[campaign_id] = container
            return container
```

**World Class Reasoning:**
- ✅ Double-checked locking (efficient)
- ✅ Lock held minimal time
- ✅ No deadlock risk (single lock)
- ✅ Works across all 3 setups
- ✅ Can upgrade to RWLock non-breaking if needed

---

# 🎯 DECISÃO #4: Memory Hierarchy & Scoping

## 🎯 FUNCIONALIDADE HABILITADA

```
Requisito: Echo system - New campaigns can access previous narratives

Business Rule: "Multi-level memory hierarchy"
├─ World (Canonical) - Immutable baseline shared by ALL campaigns
├─ Genre (Shared Cache) - Reusable between campaigns with same theme
├─ Campaign (Dynamic) - Isolated to specific campaign
└─ Global (Semantic) - Reusable templates

Example:
├─ Campaign 1 (Medieval Tavern): Discovers "Necromancer is real threat"
├─ Campaign 2 (Medieval Forest): Wants to know "What's the threat in this world?"
└─ Campaign 2 should be able to ACCESS Campaign 1's discovery (via echo system)

Quebra-requisito se:
├─ Campaign 2 can't find Campaign 1 data
├─ Can't distinguish between world baseline + campaign mutations
├─ No way to share templates between similar campaigns
└─ Can't retrieve memory "as it was" at specific timestamp
```

## 🏛️ SPEC VALIDATION

**ADR-006:** Event sourcing append-only
- ✅ Every memory change is an immutable event
- ✅ Can reconstruct state at any timestamp (for echo system)
- ✅ Full audit trail

**ADR-003:** Ports & Adapters
- ✅ NarrativeGraphPort: Multi-level retrieval
- ✅ VectorReaderPort: Cascading search (campaign → genre → world → global)

**ADR-001:** Clean Architecture (layers)
- ✅ Domain knows hierarchy (Layer 2: Domain Models)
- ✅ Application implements retrieval logic (Layer 4: Application)
- ✅ Infrastructure stores in hierarchy (Layer 7: Storage)

## 💡 WORLD CLASS PATTERNS

**Pattern: Hierarchical Storage + Cascading Retrieval**
```
Standard Pattern Used By:
- Linux: inode hierarchy with shadowing
- Browser: CSS cascade (element -> class -> tag -> global)
- Package managers: Local cache -> repository cache -> package index
- Database: Page cache -> buffer pool -> disk

Advantages:
✅ Clear priority (campaign > genre > world > global)
✅ Efficient (check local before remote)
✅ Reuse (genre cache shared)
✅ Safety (world baseline immutable)
```

## 📊 SETUP COMPATIBILITY

| Setup | Hierarchy Locations | Impact |
|-------|-------------------|--------|
| **Local** | `data/world/*/genre/*/campaign/*/` (local FS) | ✅ All in RAM/disk |
| **Hybrid** | Campaign local, Genre/World remote | ✅ Minimal remote traffic |
| **Remote** | All remote (cloud storage) | ✅ Single source of truth |

## 🎯 DECISION

**Choose Option:** Hierarchical 4-level (World/Genre/Campaign/Global) with Event Sourcing

```python
# PSEUDO-CODE (functional spec)
class MemoryHierarchy:
    """
    Four levels with clear semantics:
    
    1. WORLD (Canonical)
       - Immutable after creation
       - Shared across ALL campaigns
       - Source of truth for world baseline
    
    2. GENRE (Shared Cache)
       - Mutable, but event-sourced
       - Shared across campaigns with same genre
       - 90-day TTL + event invalidation
    
    3. CAMPAIGN (Dynamic)
       - Mutable with full history
       - Isolated to specific campaign
       - High-frequency changes
    
    4. GLOBAL (Semantic)
       - Reusable templates
       - Shared across all worlds/genres
       - Archetypal patterns
    """
    
    async def retrieve_with_cascade(self, query: str, campaign_id: str, genre: str):
        """
        Retrieval order (falling back through hierarchy):
        
        1. Check campaign-specific memory
        2. Check genre shared cache
        3. Check world canonical facts
        4. Check global templates
        
        Return with source information:
        {
            "content": "...",
            "source": "campaign" | "genre" | "world" | "global",
            "timestamp": "...",
            "version": "..."  # For echo system
        }
        """
```

**Storage Structure:**
```
data/
└── world_cyberpunk_2087/
    ├── canonical/
    │   ├── lore_001.json  (immutable)
    │   └── lore_002.json
    ├── genre_cyberpunk/
    │   ├── shared_cache/
    │   │   └── (90-day TTL, event-invalidatable)
    │   ├── campaign_001/
    │   │   └── (mutable, session-scoped)
    │   ├── campaign_002/
    │   └── campaign_003/
    └── global/
        ├── templates/
        └── archetypes/
```

**World Class Reasoning:**
- ✅ Clear priority prevents conflicts
- ✅ Event sourcing enables time-travel (echo system)
- ✅ Immutable canonical preserves baseline
- ✅ Shared cache enables resource reuse
- ✅ Works across all 3 setups

---

# 🎯 DECISÃO #5: Event-Driven Invalidation

## 🎯 FUNCIONALIDADE HABILITADA

```
Requisito: Genre cache stays correct when world changes

Scenario:
├─ February 1: Campaign 1 creates genre cache "cyberpunk"
│  └─ "Zaibatsus control mega-cities"
├─ March 1: World lore updated (admin changes canon)
│  └─ "Zaibatsus actually fractured"
├─ March 20: Campaign 2 starts
│  └─ Should see UPDATED cache, not 7-week-old data

Problem with TTL-based:
├─ 90-day TTL is arbitrary
├─ Stale cache if world changed after 1 day
├─ Valid cache invalidated even if nothing changed

Solution: Event-driven
├─ When world changes → emit WorldChangedEvent
├─ Genre cache listens and invalidates
├─ Next Campaign 2 rebuilds from fresh data
```

## 🏛️ SPEC VALIDATION

**ADR-006:** Event sourcing
- ✅ Changes are events
- ✅ Can subscribe to events
- ✅ Full audit trail

**ADR-002:** Async-first
- ✅ Event listeners are async
- ✅ Invalidation doesn't block

**ADR-003:** Ports & Adapters
- ✅ EventBusPort: publish/subscribe
- ✅ Event handlers are decoupled

## 💡 WORLD CLASS PATTERNS

**Pattern: Event-Driven Cache Invalidation**
```
Standard Pattern Used By:
- Redis: Pub/Sub invalidation
- GraphQL: Apollo cache invalidation events
- HTTP: ETag + Cache-Control headers
- Kafka: Event-driven data pipelines

Advantages:
✅ Reactive (cache invalidates when it SHOULD)
✅ No arbitrary timing
✅ Precise (only affected caches invalidate)
✅ Scalable (decoupled components)
```

## 📊 SETUP COMPATIBILITY

| Setup | Event Source | Propagation |
|-------|---|---|
| **Local** | Local app events | In-process |
| **Hybrid** | Local world changes | Broadcast to all campaigns |
| **Remote** | Remote world changes | Webhook/long-poll/websocket |

## 🎯 DECISION

**Choose Option:** Event-based invalidation (not TTL)

```python
# PSEUDO-CODE (functional spec)
class GenreCacheManager:
    """Cache that stays correct via events"""
    
    def __init__(self, event_bus: EventBusPort, genre_id: str):
        self.event_bus = event_bus
        self.genre_id = genre_id
        self._cache = None
        
        # Subscribe to world changes
        event_bus.subscribe(WorldChangedEvent, self.on_world_changed)
    
    async def on_world_changed(self, event: WorldChangedEvent):
        """React to world changes"""
        if event.genre_id == self.genre_id or event.is_global():
            # Invalidate cache
            self._cache = None
            # Will rebuild on next access
    
    async def get_cache(self, campaign_id: str):
        """Get cache, rebuilding if invalidated"""
        if self._cache is None:
            self._cache = await self._build_genre_cache()
        return self._cache

# Events that trigger invalidation:
class WorldChangedEvent:
    world_id: str
    genre_id: Optional[str]  # None = affects all genres
    change_type: str  # "canonical_updated", "genre_config_changed", etc.
    timestamp: datetime
```

**World Class Reasoning:**
- ✅ Reactive (not time-based)
- ✅ Precise (only affected caches invalidate)
- ✅ Respects Event Sourcing (ADR-006)
- ✅ Async-compatible (ADR-002)
- ✅ Works across all 3 setups

---

# 🎯 DECISÃO #6: Memory Versioning Strategy

## 🎯 FUNCIONALIDADE HABILITADA

```
Requisito: Echo system needs temporal queries

Scenario:
├─ Campaign 1 (Week 1): "Hero discovers ancient prophecy"
├─ Campaign 1 (Week 2): "Prophecy is MISINTERPRETED - actually says opposite"
└─ Campaign 2 (Week 3): "What was the prophecy about?"
   └─ Should see: Original prophecy (Week 1) to understand the confusion
   └─ AND: Corrected interpretation (Week 2) to know the truth
   └─ BUT: Needs full history for context reconstruction

Temporal Query Example:
├─ Give me narrative state as it was on Week 1 (prophecy correct)
├─ Give me all updates to prophecy since Week 1
├─ Give me who made changes and why
└─ Reconstruct session exactly as happened (audit trail)
```

## 🏛️ SPEC VALIDATION

**ADR-006:** Event sourcing append-only
- ✅ Every change is an immutable event
- ✅ Full history preserved
- ✅ Can replay to any point in time

**ADR-003:** Ports & Adapters
- ✅ NarrativeGraphPort: Versioned queries
- ✅ EventBusPort: Version change events

## 💡 WORLD CLASS PATTERNS

**Pattern: Event Sourcing (Complete History)**
```
Standard Pattern Used By:
- Git: Complete commit history
- Postgres: WAL (Write Ahead Log)
- Event stores: Event Store DB, DynamoDB Streams
- Auditing: Complete change log

Advantages:
✅ Complete history
✅ Temporal queries (state at time T)
✅ Full audit trail
✅ Can replay events
✅ Time-travel debugging
```

## 📊 SETUP COMPATIBILITY

| Setup | Storage | Query |
|-------|---------|-------|
| **Local** | JSON files (append-only) | In-memory version map |
| **Hybrid** | Remote event store | Remote temporal queries |
| **Remote** | Cloud event store (S3/DynamoDB) | Cloud SDK |

## 🎯 DECISION

**Choose Option:** Event Sourcing (Full History)

```python
# PSEUDO-CODE (functional spec)
class VersionedMemory:
    """
    Every memory has full version history:
    
    versions: {
        1: {
            timestamp: "2026-03-15T10:00:00Z",
            type: "CREATED",
            actor: "game_engine",
            content: "Ancient prophecy discovered",
            metadata: {}
        },
        2: {
            timestamp: "2026-03-22T15:30:00Z",
            type: "UPDATED",
            actor: "player_decision",
            changes: {
                "interpretation": "Prophecy means opposite"
            },
            content: "Ancient prophecy (REINTERPRETED)",
            previous_version: 1,
            metadata: {
                "reason": "Found hidden scroll in archive",
                "player_reaction": "Mind blown!"
            }
        }
    },
    current_version: 2
    """
    
    async def get_state_at_timestamp(self, timestamp: datetime) -> Memory:
        """Retrieve memory as it was at specific time"""
        # Find latest version before timestamp
        version = max(
            v for v in self.versions.values()
            if v.timestamp <= timestamp
        )
        return version.content
    
    async def get_history_since(self, since: datetime) -> List[VersionEvent]:
        """Get all changes since timestamp (for echo system)"""
        return [
            v for v in self.versions.values()
            if v.timestamp >= since
        ]
```

**World Class Reasoning:**
- ✅ Complete audit trail
- ✅ Enables echo system
- ✅ Temporal queries work
- ✅ ADR-006 compliance
- ✅ Works across all 3 setups

---

# 🎯 DECISÃO #7: Canonical Immutability Enforcement

## 🎯 FUNCIONALIDADE HABILITADA

```
Requisito: World baseline NEVER changes after creation

Business Rule: "Canon é imutável"
├─ After created, world facts are fixed
├─ Provides stable baseline for all campaigns
├─ Ensures echo system consistency

Scenario:
├─ World created with fact: "Princess is King's sister"
├─ Campaign 1 (10 sessions): Uses this fact
├─ Campaign 2 starts: References Campaign 1 echoes
├─ Admin tries to update: "Actually, she's a cousin"
│  └─ ❌ ERROR: Cannot modify canonical
│  └─ ✅ Solution: Create new fact, deprecate old

Problem to solve:
├─ How to enforce immutability?
├─ What if admin NEEDS to fix error?
├─ How to guide correction without breaking echoes?
```

## 🏛️ SPEC VALIDATION

**ADR-006:** Event sourcing
- ✅ Immutable events (once created, never change)
- ✅ Corrections are new events (not updates)

**ADR-001:** Clean Architecture
- ✅ Domain rule (Layer 2): Canonical facts are immutable
- ✅ Application validates (Layer 4): Update attempts rejected
- ✅ Adapter reports (Layer 7): Clear error message

## 💡 WORLD CLASS PATTERNS

**Pattern: Write-Once / Immutable Storage**
```
Standard Pattern Used By:
- Git objects: Immutable once created
- S3: Write-once, read-many
- IPFS: Content-addressed (immutable by hash)
- Firestore: Document versioning
- Append-only logs: Never modify records

Advantages:
✅ Thread-safe (no race conditions on canonical)
✅ Cache-friendly (never changes, always valid)
✅ Audit-safe (changes are new facts, not mutations)
✅ Distributed-friendly (no sync conflicts)
```

## 📊 SETUP COMPATIBILITY

| Setup | Enforcement | Storage |
|-------|---|---|
| **Local** | Python validation | File immutable flag (chmod -w) |
| **Hybrid** | Python + remote validation | Cloud storage write-once |
| **Remote** | Remote service enforces | Cloud audit (immutable storage) |

## 🎯 DECISION

**Choose Option:** Strict Immutable (error on modify attempt)

```python
# PSEUDO-CODE (functional spec)
class MemoryStore:
    """Enforce canonical immutability"""
    
    async def update_memory(self, memory_id: str, new_content: str):
        """Update fails for canonical, succeeds for mutable levels"""
        existing = await self.retrieve(memory_id)
        
        if existing.level == MemoryLevel.CANONICAL:
            # Enforce immutability
            raise ImmutableCanonicalError(
                f"Cannot modify canonical memory {memory_id}.\n"
                f"Canonical facts form the world baseline and are shared by all campaigns.\n"
                f"\n"
                f"If correction needed:\n"
                f"1. Create new canonical fact (describing corrected version)\n"
                f"2. Deprecate old fact (mark as DEPRECATED)\n"
                f"3. Update genre cache (invalidate affected caches)\n"
                f"4. Future campaigns will see corrected version"
            )
        
        # Allow updates for mutable levels (genre, campaign)
        if existing.level in [MemoryLevel.GENRE, MemoryLevel.CAMPAIGN]:
            # Event sourcing: new version event, not mutation
            await self.append_version_event(
                memory_id=memory_id,
                type="UPDATED",
                old_content=existing.content,
                new_content=new_content,
                actor=current_actor()
            )
```

**World Class Reasoning:**
- ✅ Strict enforcement (prevents accidents)
- ✅ Clear error message (guides user)
- ✅ ADR-006 compatible (event sourcing)
- ✅ Echo system safe
- ✅ Distributed-safe (immutable = no sync issues)

---

# 🎯 DECISÃO #8: Port Isolation & Dependency Boundaries

## 🎯 FUNCIONALIDADE HABILITADA

```
Requisito: Swap implementations without affecting other systems

Examples:
├─ Swap LLMServicePort
│  ├─ from: OpenAI (remote)
│  ├─ to: LMStudio (local)
│  └─ Rest of system: no changes
├─ Swap VectorReaderPort
│  ├─ from: ChromaDB (remote)
│  ├─ to: Faiss (local)
│  └─ Rest of system: no changes
├─ Swap EventBusPort
│  ├─ from: Blinker (in-process)
│  ├─ to: RabbitMQ (distributed)
│  └─ Rest of system: no changes

Problem to solve:
├─ Should ExecutorPort + EventBusPort be ONE port?
├─ Or SEPARATE ports (each with own interface)?
└─ Different setups need different combinations
```

## 🏛️ SPEC VALIDATION

**ADR-003:** Ports & Adapters
- ✅ "Each port has single responsibility"
- ✅ "Mix and match ports for different deployments"

**ADR-001:** Clean Architecture
- ✅ Layer 6 (Ports): Define contracts
- ✅ Layer 7 (Adapters): Implement contracts
- ✅ Domain doesn't know about adapter details

## 💡 WORLD CLASS PATTERNS

**Pattern: Interface Segregation Principle (ISP)**
```
Standard Practice:
- One port = One responsibility
- Client depends only on what it needs
- Adapters implement one port (or minimal set)

Examples:
- Java: Comparable vs Serializable vs Comparable+Serializable
- Go: Reader interface (separate from Writer)
- Python: Iterator (separate from Iterable)

Advantages:
✅ Easy to mock/test (mock single port)
✅ Easy to upgrade (swap one port, not many)
✅ Clear contracts
✅ Enables independent evolution
```

## 📊 SETUP COMPATIBILITY

**Local Setup:**
```
LLMServicePort → LMStudio local adapter
VectorReaderPort → Faiss local adapter
VectorWriterPort → Faiss local adapter
EventBusPort → Blinker in-process adapter
```

**Hybrid Setup:**
```
LLMServicePort → LMStudio local adapter
VectorReaderPort → RemoteChroma adapter (cloud)
VectorWriterPort → RemoteChroma adapter (cloud)
EventBusPort → BlinkerWithWebhook adapter (hybrid)
```

**Remote Setup:**
```
LLMServicePort → OpenAI adapter (cloud)
VectorReaderPort → RemoteChroma adapter (cloud)
VectorWriterPort → RemoteChroma adapter (cloud)
EventBusPort → RabbitMQ adapter (distributed)
```

## 🎯 DECISION

**Choose Option:** Keep Ports SEPARATE (ExecutorPort ≠ EventBusPort)

```python
# PSEUDO-CODE (functional spec)
class ExecutorPort(Protocol):
    """Task execution (CPU-bound work)"""
    async def run_sync(self, func: Callable) -> Any: ...
    async def run_async(self, coro: Coroutine) -> Any: ...
    async def start(self) -> None: ...
    async def shutdown(self) -> None: ...

class EventBusPort(Protocol):
    """Event dispatch (messaging)"""
    async def publish(self, event: object) -> None: ...
    async def subscribe(self, event_type: type, handler) -> None: ...
    async def start(self) -> None: ...
    async def shutdown(self) -> None: ...

# Container registration (mix and match for setups):

# LOCAL SETUP:
container.register(ExecutorPort, LocalThreadPoolExecutor())
container.register(EventBusPort, BlinkerEventBus())

# HYBRID SETUP:
container.register(ExecutorPort, LocalThreadPoolExecutor())
container.register(EventBusPort, BlinkerWithWebhookBridge())

# REMOTE SETUP:
container.register(ExecutorPort, RemoteExecutor(rabbitmq_url))
container.register(EventBusPort, RabbitMQEventBus())
```

**Why Separate is World Class:**
- ✅ Each port has single concern
- ✅ Different setups need different combinations
- ✅ Can evolve independently
- ✅ Easier to test (mock individually)
- ✅ Respects SOLID principles (Interface Segregation)

---

# 📋 RESUMO: 8 DECISÕES FUNCIONAIS

| # | FUNCIONALIDADE | MUNDO CLASS PATTERN | MUNDO CLASS | Setup |
|---|---|---|---|---|
| 1 | Campaign isolation | Thread-local storage | ✅ idiomatic | All 3 |
| 2 | Resource lifecycle | RAII + Finalizer | ✅ exception-safe | All 3 |
| 3 | Concurrency safety | Simple lock | ✅ scalable | All 3 |
| 4 | Memory hierarchy | Hierarchical cascade | ✅ clear priority | All 3 |
| 5 | Cache correctness | Event-driven invalidation | ✅ reactive | All 3 |
| 6 | Temporal queries | Event sourcing | ✅ full audit trail | All 3 |
| 7 | Baseline integrity | Write-once immutable | ✅ distributed-safe | All 3 |
| 8 | Port isolation | Interface segregation | ✅ SOLID | All 3 |

---

# ✅ SPEC MANDATE COVERAGE

**ADR-001: Clean Architecture 8-layer**
- ✅ #1: Layer 5 (Application Composition) - DI container
- ✅ #4: Layer 2 (Domain) + Layer 7 (Storage) - Hierarchy
- ✅ #7: Layer 2 (Domain rule) + Layer 4 (Validation)

**ADR-002: Async-first, no blocking**
- ✅ #2: Async cleanup
- ✅ #5: Async event listeners
- ✅ All: Context managers (no blocking)

**ADR-003: Ports & Adapters (18 ports)**
- ✅ #4: NarrativeGraphPort (hierarchy)
- ✅ #5: EventBusPort (invalidation)
- ✅ #6: VectorReaderPort (versioned queries)
- ✅ #8: Port separation (18 independent contracts)

**ADR-004: Vector black-box factory**
- ✅ #4: VectorReaderPort via factory (not direct import)

**ADR-005: Thread isolation (2 levels)**
- ✅ #1: Level 2 - Campaign runtime thread isolation

**ADR-006: Event sourcing append-only**
- ✅ #2: Persist events before cleanup
- ✅ #5: Changes are events
- ✅ #6: Full version history
- ✅ #7: Immutability (updates are new events)

---

# ✅ LEARNING FROM LEGACY (sem acumular débito)

When implementing, consult legacy for:
1. **What works:** Ports that are solid (LLMServicePort, VectorIndex abstractions)
2. **What doesn't:** Truncated code (ignore implementation details)
3. **What changed:** Business rules (learn from why changes happened)

**Example:**
- ❌ Don't copy-paste old container code (truncated)
- ✅ Do understand what services need to be resolved
- ✅ Do keep working Ports as-is (adapt not rewrite)
- ✅ Do learn why certain decisions were made

---

# 🎯 PRÓXIMO PASSO

Confirmar essas 8 decisões **FUNCIONAIS** (não código)?

```
✅ Decision #1: Campaign isolation via thread-local + simple lock
✅ Decision #2: Resource lifecycle via RAII + finalizer + async cleanup
✅ Decision #3: Concurrency safety via double-checked locking
✅ Decision #4: Memory hierarchy (World/Genre/Campaign/Global)
✅ Decision #5: Cache invalidation via events (not TTL)
✅ Decision #6: Versioning via event sourcing (full history)
✅ Decision #7: Canonical immutability (strict, with clear error)
✅ Decision #8: Port separation (ExecutorPort ≠ EventBusPort)
```

Se tudo alinhado, próximo passo: **Phase 1 Implementation** com foco em:
- SPEC-first (not code-first)
- World class patterns
- All 3 setups supported
- Learning from legacy (não pagando débito)

Quer prosseguir? 🚀
