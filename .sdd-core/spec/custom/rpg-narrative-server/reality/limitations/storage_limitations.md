# 💾 STORAGE LIMITAÇÕES

**Para**: Entender constraints de storage  
**Ler se**: Feature com persistence, multi-instance, ou performance crítica

---

## Storage Stack

```
API Request
    ↓
[Application Layer]
    ↓
[DocumentStorePort / KeyValueStorePort / VectorStorePort]
    ↓
[JSONFileStore / ChromaDB]
    ↓
[Filesystem / Index Files]
```

---

## 5 Limitações Críticas

### 1. Single-File JSON (No Database)

**What**: All campaign events stored in `campaigns/{campaign_id}/events.json`

**Characteristics**:
```
- Append-only (no update, no delete)
- Full file read/write on each operation
- No indexing (O(n) to find event)
- No query capability (can't select by criteria)
- Not queryable (manual iteration needed)
```

**Impact**:
- Large campaigns (10k+ events) = slow reads
- Can't efficiently find "all events by type X"
- Can't efficiently find "events between timestamp Y and Z"

**When It Breaks**:
- Campaign grows > 50k events (multi-hour read times)
- Need to query events by pattern (not possible)

---

### 2. No Transaction Support

**What**: Append-only JSON, ACID not enforced

**Characteristics**:
```
- No atomic writes (partial writes possible on crash)
- No rollback (can't undo append)
- No locks (concurrent appends = corruption)
```

**Race Condition Scenario**:
```
Process A: Append event {id: 1, text: "A"} → writes partial JSON
Process B: Append event {id: 2, text: "B"} → reads corrupted JSON, writes worse

Result: Corrupted events.json, data loss
```

**When It Breaks**: Multi-instance deployments (multiple processes writing same campaign)

---

### 3. No Encryption At Rest

**What**: All data stored in plaintext JSON files

**Impact**:
- Sensitive narrative data (campaign secrets) readable by anyone with file access
- No protection for PII (player names, emails)
- Violates privacy best practices

**Current**: Design choice (assume trusted environment)

---

### 4. In-Memory by Default (Data Loss on Restart)

**What**: Data optionally persisted to JSON, but can be in-memory only

**Characteristics**:
```
- Restart = data loss
- No crash recovery
- No audit trail
```

**When It Breaks**: Process crashes (any reason)

---

### 5. Campaign Isolation (No Cross-Campaign Queries)

**What**: Each campaign is isolated in its own directory

**Characteristics**:
```
- Can't query "all campaigns with player X"
- Can't find "all campaigns created after date Y"
- Can't aggregate stats across campaigns
```

**When It Breaks**: Need multi-campaign analytics, admin dashboards

---

## Storage Layout

```
data/
  campaigns/
    {campaign_id}/
      events.json              # Array of all events
      sessions.json            # Session metadata
      memory/
        narrative.json         # NarrativeMemory (serialized)
      kv/                      # Campaign-scoped KV
        *.json                 # Individual KV pairs

  memory/
    narrative_graph.json       # Optional graph topology
    response_cache.json        # LLM response cache
    vectors.json               # Vector index metadata
```

**File Size Expectations**:
```
Small campaign (1 week):    ~500KB
Medium campaign (1 month):  ~5MB
Large campaign (6 months):  ~50MB+
```

---

## Mitigation Strategies

| Limitation | Current Workaround | Proper Solution |
|------------|-------------------|-----------------|
| Single-file JSON | Manual pagination in code | Use PostgreSQL/MongoDB |
| No transactions | Assume single-writer per campaign | Add distributed locking |
| No encryption | Trust filesystem permissions | Encrypt at rest (AES-256) |
| Data loss | Manual backup | Enable WAL (write-ahead logging) |
| No cross-campaign queries | Build custom aggregations | Use DB with indexing |

---

## Performance Characteristics

**Read Event by ID**:
```
Current: O(n) - must read entire file
Optimized: O(log n) - with indexing
```

**Append Event**:
```
Current: O(n) - must write entire file
Optimized: O(1) - append-only log
```

**Search Events by Pattern**:
```
Current: ❌ Not possible (must read all + parse)
Optimized: ✅ O(log n) with DB index
```

---

## When To Migrate Storage

**Migrate to Database when**:
- [ ] Campaign reaches 50k+ events
- [ ] Need multi-instance consistency
- [ ] Need cross-campaign queries
- [ ] Need encryption at rest
- [ ] Need transaction safety

**Don't migrate if**:
- [ ] Single instance, <10k events per campaign
- [ ] Local dev only
- [ ] No sensitive data concerns

---

## Related Docs

- See: `/docs/ia/current-system-state/contracts.md` (DocumentStorePort)
- See: `/docs/ia/current-system-state/known_issues.md` (data loss bugs)
- See: `/docs/ia/current-system-state/threading_concurrency.md` (race conditions)
