# Template: SPECIALIZATIONS Configuration

**Purpose:** Map generic CANONICAL principles to project-specific values  
**Usage:** Copy this template to `custom/<project-name>/SPECIALIZATIONS_CONFIG.json` and fill in values  
**Generated:** Auto-generated from /CANONICAL/rules/constitution.md and ia-rules.md  
**Last Updated:** 2026-04-19

---

## 📝 How to Use This Template

1. **Copy template:**
   ```bash
   cp SPECIALIZATIONS.template.md custom/my-project/SPECIALIZATIONS_CONFIG.md
   ```

2. **Fill in project-specific values** in the CONFIG sections below

3. **Run automation:**
   ```bash
   python SCRIPTS/generate-specializations.py custom/my-project
   ```

4. **Output files generated:**
   - `custom/my-project/SPECIALIZATIONS/README.md`
   - `custom/my-project/SPECIALIZATIONS/constitution-my-project-specific.md`
   - `custom/my-project/SPECIALIZATIONS/ia-rules-my-project-specific.md`

---

## 🔧 PROJECT CONFIGURATION

### Project Identity

```
PROJECT_NAME = "my-project"              # e.g., "rpg-narrative-server"
PROJECT_SLUG = "my_project"              # e.g., "rpg_narrative_server" (no hyphens)
GITHUB_REPO = "org/my-project"           # GitHub repository path
TEAM_LEAD = "Name <email>"               # Primary maintainer
DOCUMENTATION_OWNER = "Name <email>"     # Docs maintainer
```

### Scale & Constraints

```
MAX_CONCURRENT_ENTITIES = 50             # Max concurrent domain objects
MAX_CONCURRENT_USERS = 100               # Max concurrent users
MAX_REQUEST_LATENCY_MS = 100             # P99 response time target
MAX_STORAGE_GB = 500                     # Total storage limit
```

### Technology Stack

```
LANGUAGE = "python"                      # Primary language
ASYNC_FRAMEWORK = "FastAPI + discord.py" # Async runtime
DATABASE = "PostgreSQL"                  # Primary database
CACHE = "ChromaDB"                       # Cache layer
MESSAGE_BUS = "Blinker"                  # Event bus
LLM_PROVIDER = "OpenAI"                  # LLM service
```

### Team Constraints

```
TEAM_SIZE = 3                            # Number of developers
SPRINT_LENGTH_DAYS = 14                  # Sprint duration
DEPLOYMENT_FREQUENCY = "weekly"          # Deployment cadence
ONCALL_ROTATION = "weekly"               # On-call schedule
TIMEZONE = "UTC"                         # Primary timezone
```

---

## 🎯 CANONICAL PRINCIPLE MAPPINGS

Below are the 15 constitutional principles from CANONICAL/rules/constitution.md mapped to your project:

### Principle 1: Single Responsibility Per Layer

**Generic:** "Each layer (Domain, Application, Infrastructure) must have exactly one reason to change"

**Project-specific configuration:**
```
PRIMARY_DOMAIN_OBJECTS = [
  "Campaign",                   # The root aggregate
  "Encounter",                  # Battle/encounter
  "Character",                  # NPC/Player character
  "Narrative"                   # Story state
]

LAYER_RESPONSIBILITIES = {
  "Domain": "Business logic for campaigns, encounters, characters",
  "Application": "Use case orchestration (create campaign, update character)",
  "Infrastructure": "Database persistence, LLM API calls"
}
```

### Principle 2: All Code is Async-First

**Generic:** "No blocking operations in runtime code (except initialization)"

**Project-specific configuration:**
```
BLOCKING_EXCEPTIONS = [
  "initialization/bootstrap.py",    # Allowed to block during startup
  "tests/**/*.py"                    # Allowed to block in tests
]

ASYNC_PATTERNS = [
  "Use: await asyncio.create_task() for parallel work",
  "Use: async with for resource management",
  "Use: async for for stream processing"
]
```

### Principle 3: Ports & Adapters Mandatory

**Generic:** "Infrastructure never accessed directly; always through ports"

**Project-specific configuration:**
```
PRIMARY_PORTS = [
  "LLMPort",                    # Generate narrative
  "StoragePort",                # Persist campaign state
  "VectorIndexPort",            # Similarity search
  "MessageBusPort"              # Event distribution
]

FORBIDDEN_DIRECT_IMPORTS = [
  "import chromadb",            # Use VectorIndexPort instead
  "import openai",              # Use LLMPort instead
  "import psycopg2"             # Use StoragePort instead
]
```

### Principle 4: Data Model Authority

**Generic:** "Domain entities are source of truth, not external systems"

**Project-specific configuration:**
```
SOURCE_OF_TRUTH = {
  "Campaign state": "Domain Campaign entity",
  "Character stats": "Domain Character entity",
  "Narrative embeddings": "Computed from narrative (ChromaDB is cache only)"
}

SYNC_STRATEGY = [
  "On every campaign state change: publish event",
  "Event listeners update projections (read models)",
  "ChromaDB may lag behind domain (acceptable)"
]
```

### Principle 5: Thread Isolation Mandatory

**Generic:** "Each background thread operates independently; no shared mutable state"

**Project-specific configuration:**
```
CONCURRENT_THREADS = [
  "UpdateThread",                # Poll campaigns for updates
  "GenerationThread",            # Generate narrative content
  "IndexThread",                 # Update vector index
  "EventThread"                  # Distribute events
]

ISOLATION_RULES = {
  "UpdateThread": "Can read/write Campaign entity only",
  "GenerationThread": "Can read Campaign, write Narrative, call LLM",
  "IndexThread": "Can read Narrative, write to ChromaDB"
}
```

### Principle 6: Explicit Error Handling

**Generic:** "Never silent failures; all errors logged and handled"

**Project-specific configuration:**
```
CRITICAL_ERRORS = [
  "LLM API timeout",
  "Database connection lost",
  "Vector index unavailable",
  "Campaign corruption detected"
]

ERROR_HANDLERS = {
  "LLMError": "Log + fallback to cached response",
  "DatabaseError": "Log + rollback + retry (with backoff)",
  "IndexError": "Log + use search via database",
  "CorruptionError": "Log + alert team + pause updates"
}
```

### Principle 7: Immutable Configuration

**Generic:** "Configuration changes require code review and deployment"

**Project-specific configuration:**
```
IMMUTABLE_CONFIG = [
  "MAX_CONCURRENT_CAMPAIGNS",
  "LLM_TIMEOUT_SECONDS",
  "VECTOR_INDEX_DIMENSION",
  "ARCHIVE_RETENTION_DAYS"
]

HOW_TO_CHANGE = "Edit pyproject.toml, create PR, merge to main, redeploy"
```

### Principle 8: Observability is Non-Negotiable

**Generic:** "Every request must be traceable; every error loggable"

**Project-specific configuration:**
```
TRACING_REQUIREMENT = {
  "Campaign creation": "Trace all steps (validate → persist → index → publish)",
  "Narrative generation": "Trace LLM call (input → tokens → latency → output)",
  "Vector search": "Trace query (text → embedding → search → latency)"
}

METRICS_REQUIRED = [
  "campaign_generation_latency_ms",
  "llm_api_calls_total",
  "index_update_lag_ms",
  "error_rate_percent"
]
```

---

## 🔄 SPECIALIZATIONS AUTO-GENERATION

Run this command to generate project-specific documentation from this config:

```bash
python docs/ia/SCRIPTS/generate-specializations.py \
  --project my-project \
  --config docs/ia/custom/my-project/SPECIALIZATIONS_CONFIG.md \
  --output docs/ia/custom/my-project/SPECIALIZATIONS/
```

**Generated files:**
1. `README.md` — Project-specific overview
2. `constitution-my-project-specific.md` — Mapped principles
3. `ia-rules-my-project-specific.md` — Mapped execution rules
4. `specializations-index.md` — Cross-reference index

**Automatic updates:**
- Whenever CANONICAL/rules/constitution.md changes → regenerate (with prompts for new principles)
- Whenever CANONICAL/rules/ia-rules.md changes → regenerate (with prompts for new rules)
- Ci/CD validates specializations match latest CANONICAL ✅

---

## 📋 MAPPING EXAMPLES

### Example 1: rpg-narrative-server Specialization

**Generic principle (from CANONICAL/rules/constitution.md):**
```
"50+ concurrent domain entities with independent lifecycles"
```

**rpg-narrative-server mapping:**
```
"50-200 concurrent campaigns (default 50, scaling to 200)
 Each campaign: independent state, independent threads
 Entities: Campaign, Encounter, Character, Narrative"
```

### Example 2: game-master-api Specialization (hypothetical future project)

**Generic principle:**
```
"50+ concurrent domain entities with independent lifecycles"
```

**game-master-api mapping:**
```
"100-500 concurrent game sessions
 Each session: independent state, independent AI moderators
 Entities: Session, Turn, Player, Action"
```

---

## ✅ Validation Checklist

Before committing this config file:

- [ ] PROJECT_NAME filled in
- [ ] GITHUB_REPO filled in
- [ ] MAX_CONCURRENT_ENTITIES specified
- [ ] All PRIMARY_PORTS listed
- [ ] All CONCURRENT_THREADS listed
- [ ] ERROR_HANDLERS defined
- [ ] TRACING_REQUIREMENT defined
- [ ] Team lead assigned
- [ ] Timezone set

---

## 🔗 References

- [CANONICAL/rules/constitution.md](../CANONICAL/rules/constitution.md) — Source of truth
- [CANONICAL/rules/ia-rules.md](../CANONICAL/rules/ia-rules.md) — Execution protocols
- [SCRIPTS/generate-specializations.py](../SCRIPTS/generate-specializations.py) — Automation script
- [rpg-narrative-server example](./rpg-narrative-server/SPECIALIZATIONS/) — Real example
