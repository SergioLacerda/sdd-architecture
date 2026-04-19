# 🔄 RAG PIPELINE — Fluxo Real

**Para**: Entender como retrieval realmente funciona  
**Ler se**: Bug em retrieval, ranking, memória, expansão

---

## Component Diagram

```
API Request (action, user_id)
    ↓
[NarrativeUseCase.execute()] ← ENTRY POINT
    ↓
[ContextBuilder.build()] ← RAG ORCHESTRATOR
    ├─→ [QueryExpansion] (expands with memory context)
    ├─→ [EmbedStage] (creates query embedding)
    ├─→ [ANNPrefilter] (IVF search OR fallback to slow vector_store.search)
    ├─→ [CandidateRetriever] (batch gets documents)
    ├─→ [Narrative Expansion Layer] (adds causal/temporal context)
    ├─→ [Candidate Control Layer] (manages pool size)
    ├─→ [Context Prioritization Layer] (dedup, recentness)
    ├─→ [5-Stage Ranking Pipeline]
    │   ├─ RankingStage1 (fast recall)
    │   ├─ RankingStage2 (temporal + cluster)
    │   ├─ HybridFusionStage (RRF fusion)
    │   ├─ AdaptiveRankingStage (context-aware)
    │   └─ NarrativeImportanceStage (story coherence)
    └─→ [RankingFinalStage] (select top_k)
    ↓
[Selected Context: list[dict]]
    ↓
[LLMRequest Builder] (prompt + context)
    ↓
[LLMService.generate()] ← SECOND ORCHESTRATOR
    ↓
[Response] (text, type, metadata)
```

---

## 8 Componentes do Pipeline

### 1. QueryExpansion
- **Input**: User action + current memory
- **Output**: Expanded query with context
- **Failure Mode**: If memory load fails, uses original action
- **Latency**: ~50ms (memory read only)

### 2. EmbedStage  
- **Input**: Expanded query string
- **Output**: Vector embedding (384-1024 dim depending on model)
- **Failure Mode**: If embedding fails, no retrieval happens
- **Latency**: ~200-500ms (network to embedding service)
- **Constraint**: Concurrency limited to 5 (hardcoded semaphore)

### 3. ANNPrefilter (Approximate Nearest Neighbors)
- **Input**: Query vector
- **Output**: Candidate doc IDs (fast, approximate)
- **Fallback**: If IVF not initialized, uses slow `vector_store.search()`
- **Latency**: ~10ms (ANN) or ~500ms (fallback)
- **Issue**: Race condition on startup (sees `is_ready` but IVF not built yet)

### 4. CandidateRetriever
- **Input**: Candidate doc IDs
- **Output**: Full documents (text + metadata)
- **Batch Size**: All candidates at once (N+1 calls for N candidates)
- **Latency**: ~50ms per batch
- **Failure Mode**: If storage fails, returns empty

### 5. Narrative Expansion Layer
```
CausalExpansion   → finds related events (cause-effect)
TemporalExpansion → time-aware context (before/after)
TimelineExpansion → chronological ordering
```
- **Purpose**: Add context beyond semantic similarity
- **Cost**: +30% latency, +20% tokens
- **Opt-in**: Configuration-based

### 6. Candidate Control Layer
```
CandidateSetReservoir  → manage pool (dedup, limits)
AdaptiveCandidateLimiter → dynamic limiting (memory aware)
```
- **Purpose**: Keep candidate set bounded
- **Strategy**: Keep top-N by score, then apply filters

### 7. Context Prioritization Layer
```
TemporalPriorityStage → recent events first
ClusterDedupStage     → dedup within clusters
DeduplicateStage      → exact dedup
```
- **Purpose**: Final context quality before ranking
- **Order**: Chronological → dedup → final selection

### 8. 5-Stage Ranking Pipeline

```
Stage 1: Fast Recall Ranking
  ├─ BM25 score + vector similarity
  ├─ Fast heuristics, no ML
  └─ Output: Top-50 candidates

Stage 2: Temporal + Cluster Refinement
  ├─ Temporal decay (recent > old)
  ├─ Cluster cohesion (keep related events)
  └─ Output: Top-30 candidates

Stage 3: Hybrid Fusion (RRF - Reciprocal Rank Fusion)
  ├─ Combine BM25, vector, temporal signals
  ├─ Weighted fusion (tunable)
  └─ Output: Top-20 candidates

Stage 4: Adaptive Ranking (Context-Aware)
  ├─ LLM-light scoring (not full generation, just scoring)
  ├─ Story coherence heuristics
  └─ Output: Top-15 candidates

Stage 5: Narrative Importance
  ├─ Final pass: which are most important to story?
  ├─ Canonical events prioritized
  └─ Output: Top-10 final context
```

---

## Limitações Conhecidas

| Limitação | Causa | Impacto | Severity |
|-----------|-------|--------|----------|
| **ANN Lazy Init** | Background task may not finish during startup | Falls back to slow `vector_store.search()` (10x slower) | ⚠️ Known |
| **Memory Context Silently Fails** | Exception in memory service | Continues with empty context (poor quality) | 🔴 Bug |
| **Summarization Unbounded Growth** | Summarizer fails → text concat fallback | Summary can grow 2x-3x, cause token overflow | 🔴 Bug |
| **Vector Writer Queue Loss** | Batched in memory, not persisted | Lost on process crash (missing future events) | 🔴 Bug |
| **ANN Not Distributed** | In-memory IVF only | Single instance, no sharding across nodes | ⚠️ Scaling blocker |
| **No Transaction Support** | Append-only JSON, no ACID | Race conditions in multi-instance | 🔴 Consistency issue |

---

## Pipeline Characteristics

**Latency Profile**:
```
Best case (ANN + fast stages):    ~400ms
Typical (all 5 stages):            ~800ms
Worst case (fallback search):      ~1500ms
```

**Context Output**:
```
Typical: 10-15 events retrieved
Max: 25 events (limited by token budget)
Min: 1 event (if only one matches)
```

**Concurrency**:
```
Per campaign: Sequential (one narrative at a time)
Across campaigns: Parallel (independent RAG per campaign)
Embedding service: Max 5 concurrent (hardcoded)
```

---

## Next Actions When Implementing

1. **Don't bypass ranking stages**: Each stage has purpose
2. **Handle ANN init race**: Check `vector_index.is_ready()` or add safety delay
3. **Propagate failures**: Don't silently fail in retrieval
4. **Test all 5 stages**: Rank changes affect final quality
5. **Monitor expansion layer**: Adds latency significantly

---

## Related Docs

- See: `/docs/ia/current-system-state/services.md` (who orchestrates this)
- See: `/docs/ia/current-system-state/contracts.md` (VectorReaderPort, VectorWriterPort)
- See: `/docs/ia/current-system-state/known_issues.md` (bugs in each stage)
