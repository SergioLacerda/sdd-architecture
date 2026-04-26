# 📈 SCALING CONSTRAINTS

**Para**: Entender limites de crescimento  
**Ler se**: Feature que precisa escalar, performance crítica, ou arquitetura multi-instância

---

## 5 Scaling Bottlenecks

### 1. Vector Index In-Memory Only (IVF)

**What**: ChromaDB IVF index exists only in application memory

**Characteristics**:
```
- Size: ~10MB per 10k events
- Shared across all campaigns
- Lost on process restart
- No distributed querying
```

**Current Scale**:
```
Safe: 10-50 campaigns (~1-5M vectors)
Warning: 50-100 campaigns
Breaking: >100 campaigns (memory exhaustion)
```

**When It Breaks**:
```
RAM Usage Example:
  10 campaigns, 100k events each
  = 1M vectors
  = ~100MB index
  = ~500MB with overhead
  
  100 campaigns, 100k events each
  = 10M vectors
  = ~1GB index
  = Out of memory on typical box!
```

**Impact**: OOM kills, process restart, data loss

---

### 2. Semantic Cache In-Memory Only

**What**: Response cache (KeyValueStore) entirely in RAM

**Characteristics**:
```
- Stores LLM responses (2-10KB each)
- Unbounded growth (no eviction)
- Lost on restart
- Shared globally
```

**When It Breaks**:
```
If averaging 1 response per action:
  1000 actions = 1000 responses × 5KB = 5MB
  10000 actions = 10000 responses × 5KB = 50MB
  100000 actions = 100000 responses × 5KB = 500MB!
```

**Impact**: Memory creep, eventual OOM

---

### 3. All Campaign Containers In-Memory

**What**: Each campaign gets loaded fully into memory (MemoryService, VectorReaderService, etc)

**Characteristics**:
```
- Per-campaign: ~10-50MB state
- All active campaigns loaded
- Unloading not automatic
```

**Current Scale**:
```
Safe: 50-100 active campaigns simultaneously
Warning: 100-500 campaigns (memory pressure)
Breaking: >500 campaigns
```

**When It Breaks**:
```
If 1000 campaigns average 20MB each:
  1000 × 20MB = 20GB RAM
  = Out of memory
```

**Impact**: Slow startup, sluggish performance, eventual crash

---

### 4. Hardcoded Concurrency = 5 (Embedding)

**What**: EmbeddingGateway semaphore set to 5

**Characteristics**:
```
- Max 5 concurrent embedding requests
- Others queue up
- No backpressure (queue grows)
```

**Throughput**:
```
Embedding latency: ~200ms per request
Concurrency: 5
Max throughput: 5 / 0.2 = ~25 requests/sec

If you get 100 requests/sec:
  Queue grows 75 requests per second
  → Queue: 75 items at t=1s, 150 at t=2s, ...
  → Eventually > 10k queued (memory spike)
```

**Impact**: Latency explosion, queue memory spike, timeouts

---

### 5. No Batch Pooling (Request Coalescing)

**What**: Each request calls embedding/LLM independently

**Characteristics**:
```
- No request batching
- No response caching for identical queries
```

**Inefficiency**:
```
Scenario: 100 users in same campaign all ask same question
  ❌ Current: 100 embedding calls, 100 LLM calls
  ✅ Optimal: 1 embedding call, 1 LLM call (cached)
  
  Savings: 99× reduction
```

**Impact**: Wasted compute, high latency

---

## Scaling Path

```
CURRENT (Single Instance, <100 campaigns)
├─ Acceptable: Vertical scaling (more RAM/CPU)
├─ When breaks: >100 campaigns or >50k events per campaign
│
NEXT TIER (Sharding by Campaign)
├─ Distribute campaigns across instances
├─ Shared LLM service (load balanced)
├─ Shared vector index (Milvus/Weaviate)
│
ENTERPRISE (Full Distributed)
├─ Distributed vector index (Milvus cluster)
├─ Distributed cache (Redis)
├─ Distributed storage (PostgreSQL)
├─ Multiple LLM replicas
└─ Load-balanced embedding service
```

---

## Bottleneck Priority

| Bottleneck | Current Limit | Fix Priority | Effort |
|------------|---------------|--------------|--------|
| **Vector index** | ~100 campaigns | 🔴 High | Medium (Milvus) |
| **Cache memory** | Unbounded growth | 🟡 Medium | Low (Redis) |
| **Campaign containers** | ~200-500 active | 🔴 High | High (multi-process) |
| **Embedding concurrency** | 5 max | 🟡 Medium | Low (increase semaphore) |
| **Batch pooling** | None | 🟢 Low | Medium (query dedup) |

---

## Migration Checkpoints

**Can handle 100 campaigns**:
```
✓ Vector index: ~10M vectors in memory
✓ Cache: ~500MB responses
✓ Campaigns: Loaded as needed
→ Acceptable (with monitoring)
```

**Can't handle 1000 campaigns**:
```
✗ Vector index: ~100M vectors (OOM)
✗ Cache: ~5GB responses (OOM)
✗ Campaigns: Can't fit in memory
→ MUST migrate architecture
```

---

## Quick Wins (No Architecture Change)

| Quick Win | Impact | Effort |
|-----------|--------|--------|
| Increase embedding semaphore to 10-20 | 2x embedding throughput | 5 minutes |
| Add cache eviction (LRU) | Bound cache memory | 30 minutes |
| Implement response caching | 50-90% cache hit rate | 1 hour |
| Add campaign unloading on idle | Reduce memory per campaign | 2 hours |

---

## Related Docs

- See: `/docs/ia/current-system-state/storage_limitations.md` (persistence bottleneck)
- See: `/docs/ia/current-system-state/threading_concurrency.md` (concurrency limits)
- See: `/docs/ia/specs/design-decisions.md` (why current architecture chosen)
