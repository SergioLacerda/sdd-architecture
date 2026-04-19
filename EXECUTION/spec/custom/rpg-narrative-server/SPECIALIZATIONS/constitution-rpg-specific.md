# 🏛️ CONSTITUTION — RPG NARRATIVE SERVER SPECIALIZATION

**Extends:** `/EXECUTION/spec/CANONICAL/rules/constitution.md`  
**Scope:** Project-specific implementations for rpg-narrative-server  
**Last Updated:** 2026-04-19

---

## Campaign Concurrency Model

### What is a Campaign?

In rpg-narrative-server, a **campaign** is the primary domain entity:

```
Campaign = Set of related narratives, events, and story state
         for a single game/story/project
```

Each campaign:
- Has its own narrative history (append-only events)
- Has its own vector index (ChromaDB collection)
- Has its own state container (thread-local)
- Is independent from other campaigns
- Can have multiple users (DM + players)

### Concurrency: 50-200 Campaigns

**Target:** System handles 50-200 concurrent campaigns on single machine

```
Scenario: 100 campaigns active
├─ 10 campaigns generating narratives (LLM active)
├─ 30 campaigns doing vector search (concurrent)
├─ 60 campaigns idle (waiting for user input)
└─ All without blocking each other
```

**Why possible:** Async-first + thread-local containers

```python
# Each campaign gets own container
@inject(container_key="campaign")
async def process_campaign(
    campaign_id: str,
    narrative_service: NarrativeService  # Campaign-scoped!
):
    # This service instance is specific to campaign_id
    # Other campaigns don't share this instance
    return await narrative_service.generate()
```

---

## Campaign Isolation Guarantees

### Thread-Local Container (Runtime)

```python
# In src/bootstrap/container.py

class CampaignContainer:
    """Per-campaign dependency container"""
    
    def __init__(self, campaign_id: str):
        self.campaign_id = campaign_id
        self.store = JSONKeyValueAdapter(campaign_id)
        self.vector_reader = ChromaDBVectorReader(campaign_id)
        self.vector_writer = ChromaDBVectorWriter(campaign_id)
        # etc.
    
    async def cleanup(self):
        """Called when campaign ends"""
        await self.store.cleanup()
        await self.vector_reader.cleanup()
        # Ensure no dangling resources

# Usage:
container = CampaignContainer(campaign_id="c1")
with container.scope():
    # All services in this scope use campaign-specific instances
    narrative = await narrative_service.generate()
# cleanup() called automatically
```

### Isolation Verification

```bash
# Test: One campaign doesn't see another's data
pytest tests/integration/test_campaign_isolation.py -v

# Test: 100 concurrent campaigns don't interfere
pytest tests/integration/test_concurrent_campaigns.py --concurrent=100

# Test: Cleanup removes all campaign state
pytest tests/integration/test_campaign_cleanup.py --memray
```

---

## Campaign Cleanup Patterns

### Automatic Cleanup (Recommended)

```python
async def process_user_request(campaign_id: str):
    """Automatic cleanup with context manager"""
    
    # Create campaign-scoped container
    container = CampaignContainer(campaign_id)
    
    try:
        async with container.scope():
            # Do work
            narrative = await generate_narrative()
            return narrative
    finally:
        # Always called, even on exception
        await container.cleanup()
```

### Manual Cleanup (If Needed)

```python
# In campaign deletion endpoint
async def delete_campaign(campaign_id: str, store: KeyValueStorePort):
    # Remove from database
    await store.delete(f"campaign:{campaign_id}")
    
    # Clean up vector index
    await vector_writer.delete_collection(campaign_id)
    
    # Clean up events file
    await os.aremove(f"data/{campaign_id}/events.json")
    
    # Log deletion
    logger.info(f"Campaign deleted: {campaign_id}")
```

### Cleanup Verification

```python
# Test: Memory returns to baseline after cleanup
def test_campaign_cleanup_no_memory_leak():
    import tracemalloc
    
    tracemalloc.start()
    
    # Create and cleanup 100 campaigns
    for i in range(100):
        container = CampaignContainer(f"test-campaign-{i}")
        async with container.scope():
            await do_work()
        await container.cleanup()  # Should free memory
    
    current, peak = tracemalloc.get_traced_memory()
    
    # Memory shouldn't grow much after cleanup
    assert current < 100_000_000  # 100MB
```

---

## Campaign-Level Security

### Campaign Access Control (RBAC)

```python
# Domain model: Permission model for campaigns

class CampaignRole(Enum):
    OWNER = "owner"
    DM = "dm"  # Game Master
    PLAYER = "player"
    VIEWER = "viewer"

class CampaignPermission:
    """What each role can do"""
    
    OWNER: {
        'read_campaign': True,
        'modify_campaign': True,
        'invite_users': True,
        'delete_campaign': True,
        'view_logs': True,
    }
    DM: {
        'read_campaign': True,
        'modify_campaign': True,
        'invite_users': True,
        'delete_campaign': False,
        'view_logs': False,
    }
    PLAYER: {
        'read_campaign': True,
        'modify_campaign': False,
        'invite_users': False,
        'delete_campaign': False,
        'view_logs': False,
    }
    VIEWER: {
        'read_campaign': True,
        'modify_campaign': False,
        'invite_users': False,
        'delete_campaign': False,
        'view_logs': False,
    }
```

### Campaign Isolation in Queries

```python
# ✅ CORRECT: Filter by campaign
async def get_narratives(campaign_id: str, store: KeyValueStorePort):
    narratives = await store.get(f"campaign:{campaign_id}:narratives")
    return narratives

# ✅ CORRECT: Use campaign-scoped service
@inject(container_key="campaign")
async def generate_narrative(narrative_service: NarrativeService):
    return await narrative_service.generate()

# ❌ WRONG: Could leak other campaigns
async def get_all_narratives(store: KeyValueStorePort):
    keys = await store.list_keys()  # Gets ALL campaigns!
    return [await store.get(k) for k in keys]
```

---

## Campaign Thread Isolation (AI Agent Threads)

### Development Threads

When developing campaign features, each thread has isolated scope:

```
Thread 1: "Implement campaign search"
├─ Scope: src/usecases/campaign/search_usecase.py
├─ Scope: tests/integration/test_campaign_search.py
└─ NO modifications to: Thread 2's files

Thread 2: "Implement narrative generation"
├─ Scope: src/usecases/campaign/narrative_usecase.py
├─ Scope: tests/integration/test_narrative_generation.py
└─ NO modifications to: Thread 1's files

Shared (coordinated changes):
├─ CANONICAL/ (immutable - no modifications)
├─ src/domain/ (only with coordination)
└─ src/infrastructure/ports/ (only with coordination)
```

### Thread Isolation Rules for Campaigns

- ✅ **DO:** Modify campaign-specific usecases
- ✅ **DO:** Modify campaign-specific tests
- ✅ **DO:** Add new campaign ports
- ❌ **DON'T:** Modify other thread's campaign services
- ❌ **DON'T:** Change campaign domain model without coordination
- ✅ **DO:** Coordinate if adding new campaign property

---

## Campaign Data Consistency

### Append-Only Events

Campaigns store events in append-only format:

```python
# data/campaigns/c1/events.json
[
  { "timestamp": "2026-04-19T10:00:00", "type": "CampaignCreated", "data": { "name": "Dragon Quest" } },
  { "timestamp": "2026-04-19T10:05:00", "type": "NarrativeGenerated", "data": { ... } },
  { "timestamp": "2026-04-19T10:10:00", "type": "PlayerJoined", "data": { "player": "Alice" } },
  # Never delete, never modify - only append
]
```

### Current State Reconstruction

```python
async def get_campaign_state(campaign_id: str, store: KeyValueStorePort):
    """Rebuild state by replaying events"""
    
    events = await store.get_events(campaign_id)
    state = CampaignState()
    
    for event in events:
        if event.type == "CampaignCreated":
            state.name = event.data['name']
        elif event.type == "NarrativeGenerated":
            state.narratives.append(event.data)
        elif event.type == "PlayerJoined":
            state.players.add(event.data['player'])
    
    return state
```

### Recovery from Backup

```python
async def restore_campaign_from_backup(campaign_id: str, backup_file: Path):
    """Restore campaign from backup"""
    
    # Load backup
    backup_events = json.load(backup_file)
    
    # Replay events to restore state
    store = JSONKeyValueAdapter(campaign_id)
    for event in backup_events:
        await store.append_event(campaign_id, event)
    
    # Rebuild vector index
    narratives = [e for e in backup_events if e['type'] == 'NarrativeGenerated']
    for narrative in narratives:
        await vector_writer.index(narrative)
    
    return "Campaign restored successfully"
```

---

## Campaign Performance Optimization

### Cache Strategy

```python
# Campaign state cached in memory during request
async def handle_campaign_request(campaign_id: str):
    # First request: load from disk
    campaign = await store.get(f"campaign:{campaign_id}")  # Disk hit
    
    # Within same async scope, reuse
    for _ in range(10):
        same_campaign = await store.get(f"campaign:{campaign_id}")  # Cached
    
    # Different scope: load again (but kernel filesystem cache helps)
```

### Lazy Loading

```python
# Don't load everything upfront
class Campaign:
    def __init__(self, campaign_id: str):
        self.id = campaign_id
        self._narratives = None  # Lazy
    
    async def get_narratives(self):
        if self._narratives is None:
            # Load only when needed
            self._narratives = await store.get(f"campaign:{self.id}:narratives")
        return self._narratives
```

---

## Campaign Migration Path (Future)

### From JSON to PostgreSQL

Current (50-200 concurrent campaigns):
```
data/
├─ campaigns/
│  ├─ c1/
│  │  ├─ events.json (append-only)
│  │  └─ state.json
│  └─ c2/
│     ├─ events.json
│     └─ state.json
```

Future (~1000+ campaigns):
```
PostgreSQL (same storage interface via adapter)
├─ campaigns (table)
├─ campaign_events (append-only table)
├─ campaign_state (materialized view)
└─ ChromaDB still handles vectors
```

Migration doesn't require code changes because of Ports & Adapters!

---

## Quick Reference: Campaign Concepts

| Concept | Value | Details |
|---------|-------|---------|
| Domain Entity | Campaign | A game/story project |
| Concurrency | 50-200 | Concurrent campaigns supported |
| Isolation Level | Complete | No shared state |
| Storage | JSON (→ PostgreSQL) | Append-only events |
| Vector Index | ChromaDB | Per-campaign collection |
| Container Type | Thread-local | Per-request container |
| Cleanup | Automatic | Via context manager |
| Access Control | RBAC | Owner/DM/Player/Viewer |
| Consistency | Causal | Event-ordered |

---

**Version:** 1.0 (Initial)  
**Status:** ✅ Active  
**Owner:** RPG Narrative Server Project
