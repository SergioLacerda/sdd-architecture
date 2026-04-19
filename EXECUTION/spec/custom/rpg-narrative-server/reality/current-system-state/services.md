# 🎭 SERVIÇOS PRINCIPAIS

**Para**: Entender orquestração e quem chama o quê  
**Ler se**: Bug em usecase, integração entre services, error handling

---

## 8 Core Services

### 🎭 NarrativeUseCase
```python
async def execute(
    campaign_id: str,
    action: str,
    user_id: str
) → NarrativeResponse
```
**Role**: Main orchestrator  
**Flow**:
```
1. Validate input (action, user_id)
2. Append action to memory
3. Build RAG context (ContextBuilder.build())
4. Generate response (LLMService.generate())
5. Cache response
6. Return to API
```
**Error Handling**: 
- Catches memory append failures → continues (⚠️ silent)
- Catches context build failures → continues with empty context (⚠️ silent)
- Catches LLM failures → returns error response

**Limitation**: Memory context failures silently swallowed, poor narrative quality

**Entry Point**: API → `POST /campaign/{id}/event` → this usecase

---

### 💾 MemoryService
```python
async def append(event_text: str) → None
async def get_context(query: str) → NarrativeMemory
async def load_memory() → NarrativeMemory
async def summarize() → str
```

**Role**: Event memory management + auto-summarization  
**Storage**: `campaigns/{id}/memory/narrative.json`  
**Data Model**:
```
world_facts: list[str]      # Max 100, world-level
scene_state: list[str]      # Max 20, scene context  
recent_events: list[str]    # Max 50, FIFO chronological
summary: str                # Auto-generated
```

**Auto-Summarize Trigger**: When `recent_events > threshold`  
**Summarize Method**: LLMService call (can fail → fallback to text concat)  
**Limitation**: No transaction support, can lose recent events

**Called By**: NarrativeUseCase, ContextBuilder

---

### 🔍 VectorReaderService
```python
async def search(
    campaign_id: str,
    query: str,
    k: int = 10
) → list[dict]
```

**Role**: Semantic retrieval wrapper  
**Internal Flow**: Calls all RAG pipeline stages (see rag_pipeline.md)  
**Output Format**:
```python
[
  {
    "id": "event_uuid",
    "text": "event description",
    "metadata": {...},
    "score": 0.95
  },
  ...
]
```
**Error Handling**: Falls back to slow search if ANN not ready  
**Limitation**: No distributed querying, single-instance only

**Called By**: ContextBuilder

---

### 📝 VectorWriterService
```python
async def store_event(
    campaign_id: str,
    texts: list[str],
    metadata: dict
) → None
```

**Role**: Batch vector indexing  
**Batching Strategy**: 
```
1. Queue events in memory
2. Periodic async flush (every N events or T seconds)
3. Errors logged but not propagated
```
**Limitation**: **Queue loss on process crash** (no persistence)

**Called By**: MemoryService (when appending events)

---

### 🎲 RollDiceUseCase
```python
async def execute(expression: str | DiceExpression) → DiceResult
```

**Role**: Dice rolling with probability analysis  
**Features**: Expression parsing, result calculation, probability distribution  
**Fallback**: Generic `DiceExpression` if parsing fails  
**Limitation**: No validation on expression type

**Entry Point**: API → `POST /dice`

---

### 🧠 ContextBuilder
```python
async def build(
    campaign_id: str,
    action: str,
    intent: str
) → str  # RAG context as text
```

**Role**: Orchestrates RAG context building  
**Internal Flow**:
```
1. Load memory (MemoryService.load_memory())
2. Extract entities from action
3. Vector search for similar events (VectorReaderService.search())
4. Rank results (5-stage ranking pipeline)
5. Format context for LLM prompt
```
**Integration Points**: Calls MemoryService, VectorReaderService, LLMService  
**Limitation**: Intent classification is template-based, not robust to novel patterns

**Called By**: NarrativeUseCase

---

### 🤖 LLMService
```python
async def generate(request: LLMRequest) → LLMResponse
```

**Role**: LLM request/response orchestration  
**Features**: 
- Caching (response cache in-memory)
- Timeout handling
- Metadata tracking (tokens, latency)
- Provider abstraction

**Request Format**:
```python
@dataclass(frozen=True)
class LLMRequest:
    prompt: str
    campaign_id: str
    system_prompt: str | None = None
    temperature: float = 0.7  # MUST be 0-2
    max_tokens: int = 1000
    timeout: float | None = None
    metadata: dict[str, Any] = {}
    intent: str | None = None
```

**Error Handling**: 
- No circuit breaker (sequential failures don't backoff)
- Timeout returns TimeoutError
- Provider errors return LLMError

**Limitation**: No circuit breaker pattern, can cascade failures

**Called By**: NarrativeUseCase, ContextBuilder (for scoring)

---

### 🏥 HealthService
```python
async def is_ready() → bool
```

**Health Checks**:
```
✓ Vector index initialized (_background_tasks complete)
✓ Storage accessible (can read/write)
✓ LLM service responsive (can ping)
```

**Limitation**: Only checks `_background_tasks` state, doesn't validate ANN actually built

**Entry Point**: API → `GET /health`

---

## Data Flow (E2E Request)

```
1. CLIENT REQUEST
   POST /campaign/{campaign_id}/event
   Body: { "action": "I try to convince the guard", "user_id": "player_123" }
   
2. CONTROLLER
   → Validate input (action max 500 chars, user_id max 100 chars)
   
3. NARRATIVE USECASE
   → Append action to memory (MemoryService.append())
   
4. CONTEXT BUILDER
   → Load memory (MemoryService.load_memory())
   → Vector search (VectorReaderService.search())
   → Format context
   
5. LLM SERVICE
   → Create LLMRequest with prompt + context
   → Call LLM provider
   → Cache response
   
6. RESPONSE
   {
     "status": "ok",
     "response": {
       "text": "The guard eyes you suspiciously...",
       "type": "narrative",
       "metadata": {
         "latency_ms": 1234,
         "context_size": 5000,
         "tokens_used": 342
       }
     }
   }
```

---

## Service Interactions Diagram

```
API Controller
    ↓
NarrativeUseCase
    ├─→ MemoryService
    │       ├─→ VectorWriterService (store events)
    │       └─→ LLMService (summarization)
    ├─→ ContextBuilder
    │       ├─→ MemoryService (load context)
    │       ├─→ VectorReaderService (RAG retrieval)
    │       └─→ LLMService (adaptive ranking stage)
    └─→ LLMService (generate response)
```

---

## Dependency Injection

All services injected via DI container (in bootstrap/):
```
Each campaign gets its own:
  ✓ MemoryService instance (isolated store)
  ✓ VectorReaderService (same vector index, different campaign)
  ✓ ContextBuilder (campaign-specific)

Shared (global):
  ✓ LLMService (connection pooled)
  ✓ VectorWriterService (batch queue shared, but campaign isolated)
  ✓ HealthService (aggregates all)
```

---

## Related Docs

- See: `/docs/ia/current-system-state/contracts.md` (ports each uses)
- See: `/docs/ia/current-system-state/rag_pipeline.md` (what ContextBuilder does internally)
- See: `/docs/ia/current-system-state/known_issues.md` (bugs per service)
