# 🤖 AI RULES — RPG NARRATIVE SERVER SPECIALIZATION

**Extends:** `/docs/ia/CANONICAL/rules/ia-rules.md`  
**Scope:** Project-specific paths and values for rpg-narrative-server  
**Last Updated:** 2026-04-19

---

## Source of Truth Paths

**For rpg-narrative-server, the actual paths are:**

```
1. CANONICAL/rules/ia-rules.md
   └─ /docs/ia/CANONICAL/rules/ia-rules.md

2. PROJECT STATE
   └─ /docs/ia/custom/rpg-narrative-server/development/execution-state/_current.md

3. ACTIVE THREADS
   └─ /docs/ia/custom/rpg-narrative-server/development/execution-state/threads/
      ├─ thread-*.md (each active thread)
      └─ Example: threads/feature-security-implementation.md

4. CANONICAL SPECIFICATIONS
   └─ /docs/ia/CANONICAL/specifications/
      ├─ architecture.md (8-layer, ports/adapters)
      ├─ performance.md (SLO budgets)
      ├─ security-model.md (auth/authz/encryption)
      └─ observability.md (logging/tracing/metrics)

5. PROJECT REALITY
   └─ /docs/ia/custom/rpg-narrative-server/reality/
      ├─ current-system-state/ (what exists now)
      ├─ limitations/ (known issues, constraints)
      └─ observations/ (gaps, future state)
```

---

## Hard Constraints for rpg-narrative-server

**NEVER in rpg-narrative-server:**

- ❌ Use blocking I/O (no `time.sleep()`, no `open()`)
- ❌ Access ChromaDB directly (use VectorReaderPort/VectorWriterPort)
- ❌ Mix campaign state across threads
- ❌ Store secrets in code (use environment variables)
- ❌ Log PII (user names, API keys, sensitive data)
- ❌ Bypass Ports layer for infrastructure
- ❌ Create direct imports: `from src.infrastructure.adapters import ChromaDBAdapter`

**ALWAYS in rpg-narrative-server:**

- ✅ Use ports: `from src.infrastructure.ports import VectorReaderPort`
- ✅ Async/await for all I/O
- ✅ Document campaign isolation
- ✅ Use thread-local containers
- ✅ Validate inputs with Pydantic
- ✅ Map errors to domain exceptions (Layer 5)
- ✅ Log with request context

---

## External Services (Black Box)

### Vector Search (ChromaDB)

**Port:** `VectorReaderPort`, `VectorWriterPort`  
**Location:** `src/infrastructure/ports/vector_*_port.py`  
**Adapters:**
- `src/infrastructure/adapters/chromadb_vector_adapter.py`
- Future: `src/infrastructure/adapters/qdrant_vector_adapter.py`

**Rules:**
- Vector index NOT source of truth
- Always have fallback search (BM25)
- Never rely on exact match behavior
- Mock in tests

**Example:**
```python
# ✅ CORRECT: Via port
@inject
async def search_narrative(
    query: str,
    vector_port: VectorReaderPort
) -> list[Narrative]:
    try:
        vectors = await vector_port.search(query, top_k=5)
    except VectorServiceError:
        # Fallback to BM25 search
        vectors = await bm25_search(query)

# ❌ WRONG: Direct access
from src.infrastructure.adapters.chromadb import ChromaDB
index = ChromaDB()  # NO! Use port instead
```

---

### LLM Service (OpenAI)

**Port:** `LLMServicePort`  
**Location:** `src/infrastructure/ports/llm_service_port.py`  
**Adapters:**
- `src/infrastructure/adapters/openai_adapter.py`
- Future: `src/infrastructure/adapters/ollama_local_adapter.py`

**Rules:**
- Never hardcode prompts (use templates)
- Always set timeout (30s default)
- Rate limit: max 5 RPS per campaign
- Cost tracking per campaign

**Example:**
```python
# ✅ CORRECT
async def generate_narrative(
    campaign_id: str,
    llm_port: LLMServicePort
):
    prompt = NARRATIVE_PROMPT_TEMPLATE.format(
        context=context,
        style=campaign.style
    )
    response = await asyncio.wait_for(
        llm_port.complete(prompt),
        timeout=30
    )

# ❌ WRONG
async def generate_narrative(campaign_id: str):
    import openai  # NO! Use port
    response = openai.ChatCompletion.create(...)
```

---

### Campaign Storage (JSON / PostgreSQL)

**Port:** `KeyValueStorePort`, `DocumentStorePort`  
**Location:** `src/infrastructure/ports/store_*_port.py`  
**Adapters:**
- `src/infrastructure/adapters/json_kv_adapter.py` (current)
- Future: `src/infrastructure/adapters/postgres_adapter.py`

**Rules:**
- One container per campaign (thread-local)
- Cleanup on campaign deletion
- No cross-campaign access
- Events append-only

**Example:**
```python
# ✅ CORRECT
@inject
async def get_campaign(
    campaign_id: str,
    store: KeyValueStorePort
):
    campaign = await store.get(f"campaign:{campaign_id}")
    if not campaign:
        raise CampaignNotFoundError(campaign_id)
    return campaign

# ❌ WRONG
async def get_campaign(campaign_id: str):
    import json
    with open(f"data/campaigns/{campaign_id}.json") as f:  # NO!
        return json.load(f)
```

---

## Campaign Isolation (Runtime Threads)

### Thread-Local Container Setup

```python
# In src/interfaces/http/middleware.py

async def campaign_scope_middleware(request, call_next):
    # Extract campaign_id from URL
    campaign_id = request.path_params.get('campaign_id')
    
    if campaign_id:
        # Create campaign-scoped container
        with container.campaign_scope(campaign_id):
            # All services in this request use campaign-specific instances
            response = await call_next(request)
    else:
        response = await call_next(request)
    
    return response
```

### No Cross-Campaign Access

```python
# ✅ CORRECT: Campaign isolated
async def get_campaign_state(campaign_id: str, store: KeyValueStorePort):
    state = await store.get(f"campaign:{campaign_id}")
    return state

# ❌ WRONG: Could leak other campaigns
async def get_all_narratives(store: KeyValueStorePort):
    all_keys = await store.list_keys()  # Might get other campaigns!
    return [await store.get(k) for k in all_keys]
```

---

## Development Threads (AI Agent Work)

### Thread Documentation Pattern

Create `/docs/ia/custom/rpg-narrative-server/development/execution-state/threads/{THREAD_NAME}.md`:

```markdown
# THREAD: Feature Security Model Implementation

**Status:** IN_PROGRESS  
**Assigned to:** [Your Name]  
**Duration:** 3 hours (started 2026-04-19)

## Scope
Implementing security model (ADR-XXX):
- JWT token validation
- RBAC matrix
- Campaign access control

## Modified Files
- src/infrastructure/security/token_validator.py (new)
- src/domain/models/permission.py (new)
- src/infrastructure/ports/auth_port.py (modified)
- docs/ia/CANONICAL/specifications/security-model.md (no modifications)

## Current Status
[Details of what's done, what's in progress]

## Blockers
[Any blockers preventing progress]

## Next Steps
1. Implement JWT validation in adapter
2. Add tests for RBAC matrix
3. Create integration tests
```

### Thread Isolation Rules

- ❌ **DON'T modify:** CANONICAL/ (immutable by all)
- ✅ **DO modify:** custom/rpg-narrative-server/development/
- ✅ **DO modify:** Files you listed in thread scope
- ❌ **DON'T modify:** Other threads' files
- ✅ **DO coordinate:** Changes that affect global architecture

---

## Checkpoint Protocol

After making changes:

```
1. Update thread file:
   /docs/ia/custom/rpg-narrative-server/development/execution-state/threads/{THREAD}.md

2. Run compliance checks:
   pytest tests/architecture/test_spec_compliance.py -v

3. Commit with checkpoint message:
   git commit -m "CHECKPOINT: [thread-name] - [what was done]"

4. When done, update status:
   /docs/ia/custom/rpg-narrative-server/development/execution-state/_current.md
   Mark thread as COMPLETE
```

---

## Quick Reference: Actual Values for rpg-narrative-server

```
[PROJECT_NAME] = rpg-narrative-server
[PROJECT_PATH] = /docs/ia/custom/rpg-narrative-server

Key Paths:
├─ Execution state: /docs/ia/custom/rpg-narrative-server/development/execution-state/
├─ Active threads: /docs/ia/custom/rpg-narrative-server/development/execution-state/threads/
├─ Current state: /docs/ia/custom/rpg-narrative-server/development/execution-state/_current.md
├─ Project reality: /docs/ia/custom/rpg-narrative-server/reality/
├─ System state: /docs/ia/custom/rpg-narrative-server/reality/current-system-state/
├─ Limitations: /docs/ia/custom/rpg-narrative-server/reality/limitations/
└─ Observations: /docs/ia/custom/rpg-narrative-server/reality/observations/

Key Services:
├─ Vector index: ChromaDB (src/infrastructure/adapters/chromadb_vector_adapter.py)
├─ LLM: OpenAI (src/infrastructure/adapters/openai_adapter.py)
├─ Storage: JSON (src/infrastructure/adapters/json_kv_adapter.py)
├─ Event bus: Blinker (src/infrastructure/adapters/blinker_event_adapter.py)
└─ Embedding: OpenAI embeddings (src/infrastructure/adapters/openai_embedding_adapter.py)

Key Concepts:
├─ Entity: Campaign
├─ Concurrency: 50-200 concurrent campaigns
├─ Isolation: Thread-local container per campaign
└─ Storage: JSON files in data/ (migration to PostgreSQL planned)
```

---

**Version:** 1.0 (Initial)  
**Status:** ✅ Active  
**Owner:** RPG Narrative Server Project
