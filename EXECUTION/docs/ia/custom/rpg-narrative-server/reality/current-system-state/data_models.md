# 📦 MODELOS DE DADOS

**Para**: Entender DTOs, serialização, formatos de API  
**Ler se**: Feature que toca em DTOs, serialização, ou API

---

## 4 Categorias de Modelos

```
LLM DTOs (Request/Response)
Domain Models (Business Logic)
API Models (REST/WebSocket)
Storage Models (Serialization)
```

---

## LLM DTOs

### LLMRequest (Frozen Input)
```python
@dataclass(frozen=True)
class LLMRequest:
    prompt: str                          # Required, non-empty
    campaign_id: str                     # Required, max 100 chars
    system_prompt: str | None = None     # Optional
    temperature: float = 0.7             # MUST be 0-2, else error
    max_tokens: int = 1000               # Recommend 500-2000
    timeout: float | None = None         # Seconds, None = no timeout
    metadata: dict[str, Any] = {}        # Provider-specific
    intent: str | None = None            # For intent-aware responses
```

**Constraints**:
- `temperature` MUST be in [0, 2] or LLM rejects
- `max_tokens` should be 500-2000 (balance quality/cost)
- `prompt` max ~8000 tokens (GPT-3.5) or ~100k (GPT-4)

**Example**:
```python
request = LLMRequest(
    prompt="You are an RPG narrator...\n\nScene: ...",
    campaign_id="campaign_123",
    temperature=0.8,
    max_tokens=1500,
    intent="narrative"
)
```

---

### LLMResponse (Output)
```python
@dataclass
class LLMResponse:
    content: str                         # Required, non-empty
    provider: str                        # e.g., "openai", "local", "claude"
    model: str | None = None             # e.g., "gpt-4", may be None
    latency_ms: float | None = None      # Response time, may be None
    tokens_input: int | None = None      # Consumed, provider-dependent
    tokens_output: int | None = None     # Generated, provider-dependent
```

**Guarantees**:
- `content` always non-empty
- Metadata fields may be None (provider-dependent)

**Example**:
```python
response = LLMResponse(
    content="The guard's eyes narrow...",
    provider="openai",
    model="gpt-4",
    latency_ms=1234,
    tokens_input=342,
    tokens_output=85
)
```

---

## Domain Models

### NarrativeMemory (Core State)
```python
class NarrativeMemory:
    world_facts: list[str]               # Max 100, world-level facts
    scene_state: list[str]               # Max 20, scene context
    recent_events: list[str]             # Max 50, FIFO chronological
    summary: str                         # Auto-generated via LLM
```

**Storage**: `campaigns/{id}/memory/narrative.json` (serialized)

**Constraints**:
- `world_facts`: Max 100 items (oldest auto-deleted)
- `scene_state`: Max 20 items (context for current scene)
- `recent_events`: Max 50 items (FIFO, oldest deleted)
- `summary`: Auto-updated when `recent_events > threshold`

**Example**:
```python
memory = NarrativeMemory(
    world_facts=[
        "The kingdom is under attack",
        "The prince disappeared 3 days ago",
        ...
    ],
    scene_state=[
        "Party in the castle throne room",
        "Guards are alert",
        ...
    ],
    recent_events=[
        "Player tries to convince guard",
        "Guard asks for ID",
        "Player fails deception roll",
        ...
    ],
    summary="The party has infiltrated the castle to..."
)
```

---

### PlayerActionEvent (Domain Event)
```python
@dataclass
class PlayerActionEvent:
    campaign_id: str                     # Max 100 chars
    action: str                          # Max 500 chars, non-empty
    user_id: str                         # Max 100 chars
    timestamp: float                     # Unix timestamp
    metadata: dict                       # Custom per event
```

**Storage**: Appended to `campaigns/{id}/events.json`

**Constraints**:
- `action` max 500 chars (prevent spam/DOS)
- Non-empty (meaningful action)

**Example**:
```python
event = PlayerActionEvent(
    campaign_id="campaign_123",
    action="I try to convince the guard that I'm a royal diplomat",
    user_id="player_456",
    timestamp=1713445200.0,
    metadata={
        "source": "api",
        "language": "en"
    }
)
```

---

### DiceExpression (Domain Model)
```python
@dataclass
class DiceExpression:
    expression: str                      # e.g., "2d6+3"
    result: int                          # Total rolled
    rolls: list[int]                     # Individual roll results
    modifiers: dict                      # e.g., {"bonus": 3}
```

**Parsing**:
```
"2d6" → 2 dice with 6 sides each
"2d6+3" → 2d6 plus 3 modifier
"1d20-2+5" → 1d20 minus 2, plus 5
```

---

## API Models

### Request: NarrativeEventRequest (Pydantic)
```python
class NarrativeEventRequest(BaseModel):
    action: str                          # Max 500 chars, required
    user_id: str                         # Max 100 chars, required
```

**Validation**:
- Non-empty strings
- Type checks (must be string)
- Length constraints (via max_length)

**HTTP**:
```
POST /campaign/{campaign_id}/event
Content-Type: application/json

{
  "action": "I try to convince the guard.",
  "user_id": "player_123"
}
```

---

### Response: Response (Success)
```python
class Response:
    text: str                            # Generated narrative
    type: str                            # "text", "narrative", "dice", "error"
    metadata: dict | None                # {duration, tokens, intent, ...}
```

**HTTP Success (200)**:
```json
{
  "status": "ok",
  "response": {
    "text": "The guard eyes you suspiciously, hand on sword hilt...",
    "type": "narrative",
    "metadata": {
      "latency_ms": 1234,
      "context_size": 5000,
      "tokens_used": 342,
      "intent": "diplomacy"
    }
  }
}
```

**HTTP Error (400)**:
```json
{
  "status": "error",
  "error": "action is required",
  "detail": "Request body missing 'action' field"
}
```

**HTTP Error (500)**:
```json
{
  "status": "error",
  "error": "Internal error",
  "detail": "LLM service timeout after 60s"
}
```

---

## API Endpoints

### POST /campaign/{campaign_id}/event
```
Creates narrative event and generates response

Request:
  campaign_id: string (path param)
  body: NarrativeEventRequest

Response (200):
  { status: "ok", response: Response }

Response (400):
  { status: "error", error: "..." }

Response (404):
  { status: "error", error: "campaign not found" }

Response (500):
  { status: "error", error: "Internal error", detail: "..." }
```

---

### POST /campaigns
```
Create new campaign

Request:
  { campaign_id: string }

Response (200):
  { status: "ok", campaign_id: "..." }

Response (400):
  { status: "error", error: "campaign_id already exists" }
```

---

### POST /campaigns/{id}/delete
```
Delete campaign and all data

Request:
  (no body)

Response (200):
  { status: "ok", campaign_id: "..." }

Response (404):
  { status: "error", error: "campaign not found" }
```

---

### GET /campaigns
```
List all campaigns

Response (200):
  { campaigns: ["c1", "c2", ...] }
```

---

### GET /health
```
Health check

Response (200):
  { ready: true, components: {...} }

Response (503):
  { ready: false, components: {...} }
```

---

## Storage Format

### Campaign Structure
```
data/campaigns/{campaign_id}/
  ├── events.json                   # Array of PlayerActionEvent
  │   [
  │     {campaign_id, action, user_id, timestamp, metadata},
  │     ...
  │   ]
  │
  ├── sessions.json                 # Array of sessions
  │   [
  │     {session_id, start_time, end_time, player_count},
  │     ...
  │   ]
  │
  ├── memory/
  │   └── narrative.json            # NarrativeMemory (serialized)
  │       {
  │         "world_facts": [...],
  │         "scene_state": [...],
  │         "recent_events": [...],
  │         "summary": "..."
  │       }
  │
  └── kv/
      ├── cache_key1.json           # Semantic cache entries
      ├── cache_key2.json
      └── ...
```

---

## Serialization

### JSON Serialization (Python → JSON)
```python
import json

event = PlayerActionEvent(...)
json_str = json.dumps(asdict(event))  # Python dataclass → JSON

# Restore
restored = PlayerActionEvent(**json.loads(json_str))
```

### Memory Serialization
```python
memory = NarrativeMemory(...)
json_str = json.dumps({
    "world_facts": memory.world_facts,
    "scene_state": memory.scene_state,
    "recent_events": memory.recent_events,
    "summary": memory.summary
})
```

---

## Type Constraints Reference

| Field | Type | Max Length | Constraints |
|-------|------|-----------|-----------|
| campaign_id | str | 100 | Alphanumeric, hyphen, underscore |
| action | str | 500 | Non-empty, not just whitespace |
| user_id | str | 100 | Alphanumeric, hyphen, underscore |
| world_facts | list[str] | 100 items | Auto-delete oldest |
| scene_state | list[str] | 20 items | Auto-delete oldest |
| recent_events | list[str] | 50 items | Auto-delete oldest (FIFO) |
| prompt | str | 8000 tokens | Per LLM model limit |
| temperature | float | N/A | Must be 0.0-2.0 |
| max_tokens | int | N/A | Recommend 500-2000 |

---

## Related Docs

- See: `/docs/ia/current-system-state/services.md` (who creates/uses models)
- See: `/docs/ia/specs/_shared/feature-checklist.md` (Layer 3: DTOs)
