# 📐 CONVENTIONS

## Architecture

- Follow Clean Architecture
- Use Ports & Adapters (Hexagonal)
- No infrastructure leakage across layers

---

## Naming Conventions

- UseCase: `<Action><Entity>UseCase`
- Port: `<Entity>RepositoryPort`
- Adapter: `<Technology><Entity>Adapter`

Examples:
- `RetrieveContextUseCase`
- `CampaignRepositoryPort`
- `ChromaCampaignAdapter`

---

## Async Rules

- All I/O must be async
- Never block the event loop
- Use `async/await` consistently
- Use executors for sync-bound work

---

## Storage Rules

- KV storage = source of truth
- Vector index = retrieval only (non-authoritative)
- Never mix responsibilities

---

## Error Handling

- Domain errors must be explicit
- Do not leak infrastructure exceptions
- Map infra errors to domain-level errors

---

## Dependency Rules

- Domain → no dependencies
- Application → depends only on domain
- Infrastructure → implements ports
- Interface → depends on application

---

## Code Style

- Prefer explicit over implicit
- Keep functions small and focused
- Avoid unnecessary abstractions

---

## Testing Rules

**MANDATORY:**
- Never modify production code to satisfy tests
- Mock only Ports (abstract interfaces), never concrete adapters
- Domain tests must have zero mocks
- UseCase tests must mock ports only
- No test-specific flags in production code (e.g., `if TEST_MODE`)

### Detailed Rules on Test-Specific Code

**❌ PROHIBITED Patterns:**
```python
# ❌ if TEST_MODE:
if os.getenv("TEST_MODE"):
    use_fake_backend()

# ❌ if is_test:
if __name__ == "__test__":
    setup_test_config()

# ❌ if test_flag in config:
if getattr(self, "test_flag", False):
    return default_value
    
# ❌ Backdoor test methods:
class Service:
    def _set_test_mode(self):  # Hidden test interface
        pass
```

**✅ ALLOWED Patterns:**
```python
# ✅ ENVIRONMENT config (generic, not test-specific)
if os.getenv("ENVIRONMENT") in ["test", "dev"]:
    config.backend = "memory"

# ✅ Dependency injection (tests provide different impl)
class MyService:
    def __init__(self, backend: StoragePort):
        # Code doesn't know it's mocked!
        self.backend = backend

# ✅ Factory pattern (tests call with different factory)
def create_service(*, backend_factory=default_factory):
    return MyService(backend=backend_factory())

# ✅ Monkeypatch (in conftest.py, not in production code)
@pytest.fixture
def forbid_real_llm(monkeypatch):
    monkeypatch.setattr("module.create_llm", lambda: raise_error())

# ✅ Debug flag (universal, not test-specific)
if DEBUG or logger.level == logging.DEBUG:
    log_extra_info()
```

### The Rule in Plain English

**Production code MUST NOT know it's being tested.**

Tests must configure code via:
1. Constructor injection (Ports, which can be mocked)
2. Environment variables (ENVIRONMENT, DEBUG, LOG_LEVEL — generic configs)
3. Monkeypatch (in fixtures only, not in production)

NOT via:
- if TEST_MODE
- if is_test
- if hasattr(self, "test_flag")
- Hidden test interfaces (_set_test_mode())

**Why?** Because test-specific code paths don't get exercised in production, so regressions hide.

For detailed testing patterns and strategies:
→ See [testing.md](./testing.md)

