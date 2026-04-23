# 🔗 THREADING & CONCURRENCY

**Para**: Entender constraints de concorrência  
**Ler se**: Feature paralela, async, background tasks, ou multi-instance

---

## Concurrency Model

```
ASYNCIO EVENT LOOP (Single-Threaded)
├─ All async operations run here
├─ No true parallelism (cooperative multitasking)
├─ CPU-bound ops delegated to ThreadPoolExecutor
└─ I/O-bound ops (network, disk) async-native
```

---

## 5 Limitações Críticas

### 1. Single-Threaded Event Loop

**What**: All async code runs on one OS thread

**Characteristics**:
```
- No true parallelism (only one instruction at a time)
- Cooperative multitasking (must await to yield)
- CPU-bound code blocks the entire loop
```

**Why This Matters**:
```
If you run CPU-bound code in async function:
  ❌ Blocks ALL other async operations
  ✅ Use ExecutorPort.run(func) to delegate to thread pool
```

**Examples**:
```
❌ BAD (blocks loop):
  async def bad_generate_prompt():
      prompt = summarize_full_campaign_history()  # CPU-bound!
      return prompt

✅ GOOD (doesn't block):
  async def good_generate_prompt(executor):
      prompt = await executor.run(summarize_full_campaign_history)
      return prompt
```

---

### 2. No Distributed Locking

**What**: Multiple instances can write same campaign simultaneously

**Race Condition**:
```
Instance A: Read campaigns/{id}/events.json
Instance B: Read campaigns/{id}/events.json
Instance A: Append event A → Write
Instance B: Append event B → Write (overwrites A!)

Result: Event A lost
```

**Current**: Assume single-instance only (or single writer per campaign)

**When It Breaks**: Multi-instance deployments (load-balanced)

---

### 3. Vector Index Lazy-Init Race

**What**: `is_ready` property doesn't guarantee ANN built

**Scenario**:
```
1. Startup: Begin building IVF index in background
2. Early request: Check is_ready → _background_tasks exist
3. But ANN not actually built yet!
4. Search falls back to slow vector_store.search()
```

**Impact**: Sporadic 10x latency slowdown on startup

**When It Breaks**: Immediately after startup under load

---

### 4. No Task Queue Persistence

**What**: VectorWriterService batches in memory, no persistence

**Scenario**:
```
1. Events queued in memory: [event1, event2, event3]
2. Async flush scheduled for 5 seconds
3. Process crashes after 2 seconds
4. Flushed 0 events, 3 lost forever
```

**Impact**: Recent events not indexed, won't be retrieved

**When It Breaks**: Any process crash before flush

---

### 5. CPU-Bound Blocking If Not Delegated

**What**: LLM calls, embedding service, dice parsing are CPU-intensive

**If Not Delegated to Executor**:
```
Event Loop Timeline:
  t=0ms:   Request 1 comes in
  t=100ms: Embedding service called (CPU-bound)
  t=600ms: Request 1 still processing (blocks!)
  t=100ms: Request 2 arrives (queued, waiting)
  t=600ms: Request 2 finally starts
  
Effective: Sequential (no concurrency)
```

**If Delegated (Current)**:
```
Event Loop Timeline:
  t=0ms:   Request 1 → delegate embedding to thread pool
  t=10ms:  Request 2 → delegate embedding to thread pool
  t=500ms: Request 1 response ready
  t=610ms: Request 2 response ready
  
Effective: Parallel (2 threads working)
```

**Current**: Properly delegated (good!)

---

## Async/Await Patterns

### ✅ Correct Pattern
```python
async def process_event(action: str, executor: ExecutorPort):
    # I/O-bound: OK to do in async
    memory = await memory_service.load_memory()
    
    # CPU-bound: delegate to executor
    embedding = await executor.run(embed_text, action)
    
    # I/O-bound: OK to do in async
    await vector_store.add(embedding)
    
    return response
```

### ❌ Wrong Pattern
```python
async def bad_process_event(action: str):
    # ❌ CPU-bound in async function!
    embedding = embed_text(action)  # BLOCKS event loop
    
    # This won't run until embed_text finishes
    memory = await memory_service.load_memory()
    
    return response
```

---

## Concurrency Limits

| Resource | Limit | Reason | Impact |
|----------|-------|--------|--------|
| **Embedding requests** | 5 concurrent | Hardcoded semaphore | Bursts queue up |
| **LLM requests** | Unbounded | No semaphore | Can overload |
| **Campaign containers** | N (in-memory) | Memory | All loaded in RAM |
| **Vector index** | 1 (per campaign) | Single IVF | No sharding |
| **Concurrent narrative requests** | 1 per campaign | Sequential | Sequential per campaign |

---

## Multi-Thread Safety

### ✅ Safe (Thread-Safe)
```
- asyncio primitives (Lock, Event, Queue)
- Immutable data structures
- Per-thread state (campaign containers)
```

### ❌ Unsafe (Not Thread-Safe)
```
- Shared mutable state (global dicts)
- Direct file I/O (not coordinated)
- VectorWriterService queue (memory only)
```

---

## When To Add Distributed Locking

**Migrate to distributed locking when**:
- [ ] Multi-instance deployment (load-balanced)
- [ ] Shared campaign storage
- [ ] Need consistency across instances

**Implement with**:
- Redis (SETNX, Lua scripts)
- etcd (distributed locks)
- Zookeeper
- Database row locks

---

## Mitigation Strategies

| Limitation | Current Workaround | Proper Solution |
|------------|-------------------|-----------------|
| Single-threaded loop | Delegate CPU ops to executor | ✅ Done |
| No distributed lock | Single instance only | Add Redis/etcd locking |
| Vector init race | Cold start adds latency | Add safety check after init |
| Queue loss | Accept data loss | Persist queue to DB |
| Hardcoded concurrency=5 | Limit on embedding throughput | Make semaphore configurable |

---

## Related Docs

- See: `/docs/ia/current-system-state/contracts.md` (ExecutorPort)
- See: `/docs/ia/current-system-state/scaling_constraints.md` (distributed implications)
- See: `/docs/ia/current-system-state/known_issues.md` (concurrency bugs)
