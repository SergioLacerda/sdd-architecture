# 📋 CONTRATOS (PORTS)

**Para**: Entender interfaces, garantias, implementações atuais  
**Ler se**: Tocando em ports, novo adapter, ou quebra de contrato

---

## 9 PORTS (Interfaces)

### 1. KeyValueStorePort
```python
class KeyValueStorePort(Protocol):
    async def get(self, key: str) → T | None
    async def set(self, key: str, value: T) → None
    async def delete(self, key: str) → None
```

**Current Implementation**: JSONFileStore (`data/{namespace}/kv/`)  
**Guarantees**:
- Atomic get/set (no partial reads)
- Key isolation per namespace
- No TTL/expiration

**Usage**:
- Campaign KV store
- Semantic response cache
- Session data

**What You Can Change**: Implementation (add Redis, DynamoDB)  
**What You CAN'T Change**: Interface signature, guarantees

---

### 2. VectorStorePort
```python
class VectorStorePort(Protocol):
    async def add(
        self,
        doc_id: str,
        vector: list[float],
        metadata: dict
    ) → None

    async def search(
        self,
        vector: list[float],
        limit: int
    ) → list[str]  # doc_ids
```

**Current Implementation**: ChromaDB (IVF index with fallback)  
**Guarantees**:
- Returns `limit` doc_ids or fewer if not enough
- Scores normalized (0-1, higher = more relevant)
- No guarantee of score threshold

**Usage**: Event vector storage, semantic search

**What You Can Change**: Backend (Milvus, Pinecone, FAISS)  
**What You CAN'T Change**: Return format (still list of doc_ids)

---

### 3. DocumentStorePort
```python
class DocumentStorePort(Protocol):
    async def set(self, key: str, value: Mapping[str, Any]) → None
    async def get(self, key: str) → dict | None
```

**Current Implementation**: JSONFileStore (`campaigns/{id}/events.json`)  
**Guarantees**:
- Append-only semantics (no update, only set)
- Stores any JSON-serializable dict

**Usage**: Campaign events, sessions, narrative state

**What You Can Change**: Backend (MongoDB, PostgreSQL)  
**What You CAN'T Change**: Append-only guarantee

---

### 4. VectorReaderPort
```python
class VectorReaderPort(Protocol):
    async def search(
        self,
        campaign_id: str,
        query: str,
        k: int = 10
    ) → list[dict]
```

**Current Implementation**: RAG pipeline orchestrator (8 stages, 5 ranking stages)  
**Guarantees**:
- Returns `k` documents or fewer
- Each dict has `id`, `text`, `metadata`, `score`
- Higher score = more relevant
- Stable results (same query twice = same top-10)

**Usage**: RAG retrieval in ContextBuilder

**What You Can Change**: Ranking algorithm, expansion stages  
**What You CAN'T Change**: Return format

---

### 5. VectorWriterPort
```python
class VectorWriterPort(Protocol):
    async def store_event(
        self,
        campaign_id: str,
        texts: list[str],
        metadata: dict
    ) → None
```

**Current Implementation**: Batch queue in memory with async flush  
**Guarantees**:
- Batches internally (no guarantee of immediate persistence)
- **No transactional guarantee** (may lose on crash)
- Errors logged but not propagated

**Usage**: After appending events to memory

**What You Can Change**: Batching strategy, persistence backend  
**What You CAN'T Change**: Async interface

**⚠️ Known Issue**: Queue loss on process crash

---

### 6. LLMServicePort
```python
class LLMServicePort(Protocol):
    async def generate(request: LLMRequest) → LLMResponse
```

**Request**:
```python
@dataclass(frozen=True)
class LLMRequest:
    prompt: str                          # Required
    campaign_id: str                     # Required
    system_prompt: str | None = None
    temperature: float = 0.7             # MUST be 0-2
    max_tokens: int = 1000               # Recommend 500-2000
    timeout: float | None = None
    metadata: dict[str, Any] = {}
    intent: str | None = None
```

**Response**:
```python
@dataclass
class LLMResponse:
    content: str                         # Required, non-empty
    provider: str                        # e.g., "openai", "local"
    model: str | None = None
    latency_ms: float | None = None
    tokens_input: int | None = None
    tokens_output: int | None = None
```

**Guarantees**:
- Returns within `timeout` or raises `TimeoutError`
- Content is non-empty or raises `LLMError`
- Metadata fields may be None (provider-dependent)

**Usage**: Generate narrative responses, adaptive ranking

**What You Can Change**: Provider (OpenAI, Claude, local)  
**What You CAN'T Change**: Request/response schema, timeout behavior

---

### 7. EmbeddingGateway
```python
class EmbeddingGateway(Protocol):
    async def embed(text: str) → list[float]
    
    async def embed_batch(
        texts: Iterable[str],
        concurrency: int = 5
    ) → list[list[float]]
```

**Current Implementation**: Hardcoded concurrency=5 semaphore  
**Guarantees**:
- Returns vectors with consistent dimension
- Concurrency limited (semaphore)
- Error handling: logs exception, returns empty list (NOT propagated)

**Usage**: Query embedding, event embedding

**What You Can Change**: Backend (OpenAI, SentenceTransformers)  
**What You CAN'T Change**: Error handling (swallows exceptions)

**⚠️ Known Issue**: Concurrency hardcoded to 5

---

### 8. CampaignRepositoryPort
```python
class CampaignRepositoryPort(Protocol):
    async def get_events(campaign_id: str) → list[Event]
    async def save_events(campaign_id: str, events: list[Event]) → None
    async def create(campaign_id: str) → None
    async def exists(campaign_id: str) → bool
```

**Current Implementation**: JSONFileStore (`data/campaigns/{id}/events.json`)  
**Guarantees**:
- Append-only (no update, only save)
- Per-campaign isolation
- **No distributed locking** (race conditions in multi-instance)

**Usage**: Store/retrieve campaign events

**What You Can Change**: Backend (DB)  
**What You CAN'T Change**: Append-only semantics

---

### 9. ExecutorPort
```python
class ExecutorPort(Protocol):
    async def run(
        func: Callable[..., T],
        *args,
        **kwargs
    ) → T
```

**Current Implementation**: ThreadPoolExecutor (delegated from async loop)  
**Guarantees**:
- Runs CPU-bound func on executor thread (doesn't block event loop)
- Returns result or raises exception

**Usage**: CPU-bound ops (embedding, summarization, dice parsing)

**What You Can Change**: Backend (ProcessPoolExecutor, Ray)  
**What You CAN'T Change**: Async interface

**⚠️ Known Issue**: No timeout, no task cancellation

---

## WHICH PORTS YOU CAN CHANGE

```
For new feature:
  ├─ You WILL use: LLMServicePort, ExecutorPort (always)
  ├─ You PROBABLY use: VectorReaderPort, KeyValueStorePort
  ├─ You MAYBE use: DocumentStorePort, CampaignRepositoryPort
  └─ You SHOULDN'T use directly: VectorWriterPort, VectorStorePort (use VectorWriterService)

For multi-instance:
  ├─ MUST change: CampaignRepositoryPort (add distributed locking)
  ├─ MUST change: VectorWriterPort (persist queue)
  └─ SHOULD change: VectorStorePort (distributed index)

For scaling:
  ├─ MUST change: VectorStorePort (distributed)
  ├─ SHOULD change: KeyValueStorePort (Redis instead of JSON)
  ├─ SHOULD change: DocumentStorePort (DB instead of JSON)
  └─ SHOULD change: EmbeddingGateway (increase concurrency)
```

---

## GUARANTEES YOU CAN'T BREAK

```
❌ FORBIDDEN CHANGES:
  • Changing port signatures (add params, change return type)
  • Breaking append-only guarantee (DocumentStorePort)
  • Removing error handling contracts
  • Changing vector dimensions (would break search)
  • Removing timeout behavior (LLMServicePort)
```

---

## Related Docs

- See: `/docs/ia/current-system-state/services.md` (who uses which ports)
- See: `/docs/ia/specs/_shared/architecture.md` (design patterns for ports)
