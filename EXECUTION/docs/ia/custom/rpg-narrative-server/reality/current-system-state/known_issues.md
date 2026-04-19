# 🐛 PROBLEMAS CONHECIDOS (Bugs & Edge Cases)

**Para**: Entender bugs já conhecidos para não repetir  
**Ler se**: Qualquer feature (sempre revisar para não repetir erros)

---

## Severidade Levels

```
🔴 CRITICAL: Data loss or crash
🟡 MEDIUM: Workaround exists, acceptable for now
🟢 LOW: Known limitation, not urgent
```

---

## 11 Problemas Documentados

### 🔴 CRITICAL: ANN Lazy-Init Race Condition

**Location**: `vector_index/rag_context_builder.py` + `health_service.py`  
**Severity**: High impact, low probability  

**Bug**:
```
is_ready property checks _background_tasks but doesn't validate IVF actually built
```

**Trigger**: Call `search()` during startup, before `_background_tasks` complete

**Observed Behavior**:
```
1. Request comes in
2. is_ready() returns True (tasks exist)
3. search() calls ANN
4. ANN not ready → fallback to slow vector_store.search()
5. 10-100x slower response (~1500ms vs ~100ms)
```

**Impact**: Sporadic latency spikes on startup  
**Workaround**: Add delay after server startup, or manually check ANN readiness  
**Proper Fix**: Synchronous ANN initialization or explicit completion signal

---

### 🔴 CRITICAL: Memory Context Silently Fails

**Location**: `narrative/narrative_event_usecase.py:129`  
**Severity**: Medium impact (quality loss)

**Bug**:
```python
try:
    memory = await memory_service.load_memory()
except Exception:  # ❌ Catches ALL
    memory = empty_memory()  # ❌ Silent fail
```

**Trigger**: MemoryService throws (storage error, LLM error, network error)

**Observed Behavior**:
```
1. Memory load fails (e.g., file corrupted)
2. Exception caught silently
3. Context builder gets empty memory
4. RAG retrieval weak (no semantic context)
5. LLM generates poor response
6. User doesn't know why (silent degradation)
```

**Impact**: Silent quality degradation  
**Current Workaround**: Monitor logs, check memory service  
**Proper Fix**: Propagate error, add retry logic, or fallback with warning

---

### 🔴 CRITICAL: Vector Writer Queue Loss

**Location**: `vector_index/vector_writer_service.py`  
**Severity**: Data loss risk

**Bug**:
```python
queue: list[str] = []  # In-memory only!

async def store_event(texts: list[str]):
    queue.append(*texts)  # Queued
    # Async flush scheduled but NOT guaranteed
    
# If process crashes before flush → queue.append() lost!
```

**Trigger**: Process crash or kill before async flush completes

**Observed Behavior**:
```
1. Event appended to memory queue
2. Async flush scheduled for 5 seconds
3. Process killed after 2 seconds
4. Flush never happens
5. 3 events in queue lost forever
6. Future searches miss these events
```

**Impact**: Data loss (recent events not indexed)  
**Current Workaround**: Accept data loss or restart cleanly  
**Proper Fix**: Persist queue to disk, implement write-ahead logging

---

### 🔴 CRITICAL: Summarization Unbounded Growth

**Location**: `memory/memory_service.py`  
**Severity**: Bug if summary > max_tokens

**Bug**:
```python
try:
    summary = await llm_service.summarize(recent_events)
except Exception:
    # ❌ Fallback: concatenate all events!
    summary = "\n".join(recent_events)  # Unbounded!
```

**Trigger**: LLM timeout, embedding service down, or network error

**Observed Behavior**:
```
1. Summarize 50 recent events (each 100 chars)
   → Expected: 500 chars
2. LLM fails (timeout)
3. Fallback: concatenate all events
   → Result: 5000 chars
4. Summary grows 10x
5. Next LLM call: token overflow
   → Truncation or error
```

**Impact**: Token overflow, poor narrative quality  
**Current Workaround**: Cap summary size, manual truncation  
**Proper Fix**: Implement chunked summarization with size limit

---

### 🟡 MEDIUM: Intent Classifier Incomplete

**Location**: `narrative/intent_classifier.py` + test skipped at `tests/...test_intent_classifier.py:151`

**Status**: Incomplete implementation  
**Test Skip**: "Not enough triggers"

**Bug**:
```python
TRIGGER_PATTERNS = {
    "combat": ["attack", "fight", ...],  # Minimal patterns
    "diplomacy": ["convince", ...],
    # ... very incomplete
}
```

**Trigger**: User action with novel intent pattern

**Observed Behavior**:
```
1. Agent tries to persuade using unusual phrasing
2. Doesn't match any TRIGGER_PATTERNS
3. Falls back to generic intent ("other")
4. Response uses generic template
5. Less coherent narrative
```

**Impact**: Novel intents not classified (fallback to generic)  
**Workaround**: Manually expand trigger patterns or implement ML classifier  
**Status**: Known limitation, not urgent

---

### 🟡 MEDIUM: LLM Service No Circuit Breaker

**Location**: `llm/llm_service.py`  
**Severity**: Cascade failure risk

**Bug**:
```python
# No circuit breaker!
for request in queue:
    response = await llm_provider.generate(request)  # Can fail repeatedly
    # If provider is down: ALL requests timeout
```

**Trigger**: LLM provider down or very slow

**Observed Behavior**:
```
1. LLM provider returns 503 errors
2. All requests timeout (60sec each)
3. Requests queue up (100/sec × 60s = 6000 queued)
4. Memory spike, system slow
5. Even after provider recovers, queue still draining
```

**Impact**: Cascade failures, slow recovery  
**Workaround**: External monitoring, manual restart  
**Proper Fix**: Implement circuit breaker (Fail Fast pattern)

---

### 🟡 MEDIUM: No Distributed Locking

**Location**: `storage/adapters/`, `campaign_repository.py`  
**Severity**: Multi-instance race conditions

**Bug**:
```python
# No locking!
events = load_campaign_events(campaign_id)
events.append(new_event)
save_campaign_events(campaign_id, events)  # Can overwrite if concurrent
```

**Trigger**: Multi-instance deployment with same campaign accessed simultaneously

**Observed Behavior**:
```
Instance A: Load campaigns/c1/events.json (100 events)
Instance B: Load campaigns/c1/events.json (100 events)
Instance A: Append event A → Save (101 events)
Instance B: Append event B → Save (101 events, loses A!)

Result: Event A lost, data inconsistency
```

**Impact**: Data loss in multi-instance (undetectable)  
**Current**: Assume single-instance only  
**Workaround**: Single writer per campaign  
**Proper Fix**: Add distributed locking (Redis, etcd)

---

### 🟡 MEDIUM: Storage Adapter Isolation Not Validated

**Location**: `infrastructure/storage/adapters/`  
**Severity**: Architectural debt

**Potential Issue**:
```python
# Could accidentally access global state (violates ports & adapters)
global_cache = {}  # ❌ If exists, breaks isolation
```

**Trigger**: Adapter implementation adds global mutable state

**Impact**: Hidden dependencies, hard-to-debug bugs  
**Workaround**: Code review focus on isolation  
**Proper Fix**: Design review, add architectural tests

---

### 🟢 LOW: Vector Index Cleanup Exceptions Swallowed

**Location**: `vector_index/cleanup.py`  
**Severity**: Resource leak risk

**Bug**:
```python
try:
    await cleanup_vector_index()
except Exception as e:
    logger.error(f"Cleanup failed: {e}")  # Just logs, not propagated
```

**Impact**: Resources may leak (file handles, memory), but cleanup logged  
**Workaround**: Monitor cleanup logs manually  
**Proper Fix**: Propagate cleanup errors to startup failure

---

### 🟢 LOW: Signal Handler Tests Hang on xdist

**Location**: `tests/runtime/test_signal_handler.py`  
**Marker**: `@pytest.mark.skipif(IS_XDIST)`

**Issue**: xdist worker hangs when running signal handler tests

**Workaround**: Run without xdist (`pytest -n0`) or skip  
**Status**: Test infrastructure issue, not production bug

---

### 🟢 LOW: Hardcoded Embedding Concurrency = 5

**Location**: `embedding/embedding_gateway.py`  
**Severity**: Throughput limitation

**Limitation**:
```python
semaphore = asyncio.Semaphore(5)  # Hardcoded!
```

**Impact**:
```
Max embedding throughput: ~25 req/sec
If traffic > 25 req/sec: Queue grows, latency increases
```

**Workaround**: Increase if GPU available, or use external embedding service  
**Proper Fix**: Make configurable via environment

---

## Bug Patterns to Avoid

**Pattern 1: Silent Exception Swallowing**
```python
❌ try:
     result = await risky_operation()
   except Exception:
     return default_value  # Silent!

✅ try:
     result = await risky_operation()
   except ExpectedError:
     return default_value  # Explicit
   except UnexpectedError:
     raise  # Propagate
```

**Pattern 2: Unbounded Resource Accumulation**
```python
❌ results_cache = {}  # Grows forever
   while requests:
     results_cache[request.id] = await process(request)

✅ results_cache = {}  # Bounded
   while requests:
     if len(results_cache) > MAX_SIZE:
       results_cache.popitem()  # Evict
     results_cache[request.id] = await process(request)
```

**Pattern 3: Race Conditions from Lack of Locking**
```python
❌ state = load()
   state.append(new_value)
   save(state)  # Can lose concurrent writes

✅ async with lock:
     state = load()
     state.append(new_value)
     save(state)
```

---

## Checklist When Implementing

- [ ] Read this file (current bugs)
- [ ] Explicitly handle errors (don't silently swallow)
- [ ] Test with concurrent requests
- [ ] Validate resource limits (memory, connections)
- [ ] Add distributed locking if multi-instance
- [ ] Implement circuit breakers for external services
- [ ] Test startup race conditions
- [ ] Verify cleanup on shutdown

---

## Related Docs

- See: `/docs/ia/current-system-state/threading_concurrency.md` (race conditions)
- See: `/docs/ia/current-system-state/storage_limitations.md` (data loss scenarios)
- See: `/docs/ia/current-system-state/scaling_constraints.md` (resource limits)
