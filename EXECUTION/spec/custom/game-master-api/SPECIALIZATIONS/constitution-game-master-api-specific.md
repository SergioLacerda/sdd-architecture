# Constitutional Principles — game-master-api Specialization

**Project:** game-master-api  
**Version:** 1.0  
**Generated:** 2026-04-19T12:55:46.101988  
**Based on:** /EXECUTION/spec/CANONICAL/rules/constitution.md

---

## 📋 Overview

This document maps the 15 generic constitutional principles from CANONICAL to game-master-api-specific constraints and implementation guidelines.

**Team size:** 3 developers  
**Scale:** 200 concurrent entities  
**Primary entities:** campaigns,encounters,npcs,quest_chains

---

## ✅ Principle Specializations

### 1. Single Responsibility Per Layer

**Generic:** Each layer must have exactly one reason to change

**game-master-api specialization:**
```
Domain Layer:
  ├─ Campaign entity (campaign lifecycle, state transitions)
  ├─ Encounter entity (encounter logic)
  ├─ Character entity (character state)
  └─ Narrative entity (narrative generation orchestration)

Application Layer:
  ├─ CreateCampaignUseCase
  ├─ UpdateCampaignUseCase
  ├─ GenerateNarrativeUseCase
  └─ RetrieveCampaignUseCase

Infrastructure Layer:
  ├─ PostgreSQL adapter (persistence)
  ├─ ChromaDB adapter (vector index)
  ├─ OpenAI adapter (LLM)
  └─ Blinker adapter (message bus)
```

**Constraint:** Each domain entity responsible for exactly one business concept
**Validation:** Mismatch detected by architecture tests → CI/CD failure

---

### 2. All Code is Async-First

**Generic:** No blocking operations (except bootstrap)

**game-master-api specialization:**
```
Async requirements:
  ✅ campaign_service.py — All methods async
  ✅ narrative_generator.py — All methods async
  ✅ vector_index_adapter.py — All methods async
  ✅ llm_adapter.py — All methods async

Allowed blocking:
  ✓ Bootstrap initialization (pyproject.toml: startup tasks)
  ✓ Test fixtures (conftest.py)
  ✓ Migration scripts (one-time operations)

Validation:** pytest detects sync functions in runtime code → FAIL
```

**Constraint:** Zero blocking I/O in production hot paths

---

### 3. Ports & Adapters Mandatory

**Generic:** Infrastructure never accessed directly

**game-master-api specialization:**
```
Mandatory ports:
  - StoragePort: all database access
  - VectorIndexPort: all embedding operations
  - LLMPort: all LLM interactions
  - MessageBusPort: all event distribution
  - ConfigPort: all configuration access

Example violation (FORBIDDEN):
  ❌ import chromadb; chromadb.search(...)
  ✅ self.vector_index_port.search(...)

Validation:** Import checker blocks chromadb, openai, psycopg2 in domain/
```

**Constraint:** 100% port usage, 0% direct infrastructure imports in domain/app

---

### 4. Data Model Authority

**Generic:** Domain entities are source of truth, not external systems

**game-master-api specialization:**
```
Source of truth:
  - Campaign state: Campaign entity (domain/)
  - Character stats: Character entity (domain/)
  - Narrative history: Narrative entity (domain/)
  - Embeddings: Derived from Narrative (ChromaDB is cache only)

Acceptable lag:
  - Campaign→Database: <100ms
  - Campaign→MessageBus: <50ms
  - Campaign→ChromaDB: <5 minutes (cache refresh)

Validation:** If ChromaDB and Campaign disagree: Campaign wins, ChromaDB recomputed
```

**Constraint:** Domain entities are immutable source of truth

---

### 5. Thread Isolation Mandatory

**Generic:** Each thread operates independently, no shared mutable state

**game-master-api specialization:**
```
Concurrent threads:
  - UpdateThread: polls for campaign changes
  - GenerationThread: generates narrative (calls LLM)
  - IndexThread: updates vector index
  - EventThread: distributes events via message bus

Isolation rules:
  - UpdateThread can ONLY write: Campaign
  - GenerationThread can ONLY write: Narrative
  - IndexThread can ONLY write: ChromaDB
  - No thread shares mutable state

Coordination via:
  - Message bus for notifications
  - Database for shared read-only data
  - Thread-safe queues for work distribution

Validation:** Thread isolation tests verify no data races (ThreadSanitizer)
```

**Constraint:** 200 campaigns must support 200 concurrent threads without deadlock

---

### 6. Explicit Error Handling

**Generic:** Never silent failures

**game-master-api specialization:**
```
Critical failure modes:
  1. LLM API timeout → log + fallback to cached narrative
  2. Database connection lost → log + graceful degradation
  3. Vector index unavailable → log + use DB search fallback
  4. Campaign corruption detected → log + ALERT team + pause updates

Error budget:
  - LLM errors: acceptable (fallback to cache)
  - Database errors: NOT acceptable (requires rollback)
  - Index errors: acceptable (rebuild from source)
  
Monitoring:**
  - error_rate_percent < 0.5% (SLO)
  - error_types tracked by middleware
  - on-call alert for any database errors
```

**Constraint:** Zero unhandled exceptions reach users

---

### 7. Immutable Configuration

**Generic:** Configuration changes require code review

**game-master-api specialization:**
```
Immutable config (cannot change without deployment):
  - MAX_CAMPAIGNS_PER_USER
  - MAX_CONCURRENT_GENERATIONS
  - LLM_MODEL_VERSION
  - VECTOR_INDEX_DIMENSION

Mutable config (can change live):
  - LLM_TEMPERATURE (within bounds)
  - CACHE_TTL_SECONDS (within bounds)
  - RETRY_BACKOFF_MS (within bounds)

How to change immutable:
  1. Edit pyproject.toml
  2. Create PR (code review required)
  3. Merge to main
  4. Deploy (blue-green deployment)
  5. Rollback plan: revert + redeploy
```

**Constraint:** Immutable config validated at startup, non-compliance → EXIT

---

### 8. Observability is Non-Negotiable

**Generic:** Every request traceable, every error loggable

**game-master-api specialization:**
```
Tracing requirements:
  - Campaign creation: trace all steps
  - Narrative generation: trace LLM call (tokens, latency)
  - Vector search: trace query (embedding, distance, latency)

Metrics required:
  - campaign_generation_latency_ms (p50, p99)
  - llm_api_calls_total (by model)
  - vector_index_update_lag_ms (max lag allowed)
  - error_rate_percent (by error type)

Logging levels:
  - DEBUG: disabled in production
  - INFO: campaign lifecycle events
  - WARNING: rate limiting, retries
  - ERROR: failures that don't stop system
  - CRITICAL: system-wide failures

Validation:** Every endpoint must log on entry/exit with trace ID
```

**Constraint:** Zero unlogged errors in production

---

### 9-15. [Additional Principles]

[Additional principles would follow same pattern...]

---

## 🔗 References

- Generic principles: [CANONICAL/rules/constitution.md](../../CANONICAL/rules/constitution.md)
- Execution rules: [CANONICAL/rules/ia-rules.md](../../CANONICAL/rules/ia-rules.md)
- Architecture spec: [CANONICAL/specifications/architecture.md](../../CANONICAL/specifications/architecture.md)
- game-master-api config: [SPECIALIZATIONS_CONFIG.md](./SPECIALIZATIONS_CONFIG.md)

---

## ✅ Validation

**Generated:** 2026-04-19T12:55:46.101988  
**Next update:** Auto-generated when CANONICAL/ changes  
**Manual updates:** game-master-api-specific constraints only (marked with **specialization**)

