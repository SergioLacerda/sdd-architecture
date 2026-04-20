# 🏛️ SYSTEM CONSTITUTION v2.0

**Effective Date:** 2026-04-19  
**Status:** ✅ Production-Grade  
**Scope:** All [PROJECT_NAME] implementations (mandatory inheritance)  
**Classification:** Non-negotiable principles

---

## 📋 IA-FIRST DESIGN NOTICE

> **This document is structured for AI analysis and human comprehension.**
>
> **Parsing guarantees:**
> - Fixed heading hierarchy (H1 title → H2 sections → H3 subsections → lists)
> - Clear principle statements (starts with "**THE PRINCIPLE**")
> - Structured validation sections (lists + code blocks, no prose)
> - Explicit status markers (✅ Active, ⚠️ Planned, ❌ Deprecated)
> - Consistent cross-reference format: `[ADR-001](../../decisions/ADR-001.md)`
> - Machine-readable constraints: ❌ NEVER, ✅ ALWAYS, ⚠️ WHEN

**For maintainers:** Preserve structure when updating. Add emoji markers (🎯, 🔴, 🟢) for quick scanning.

---

## ⚠️ IMPORTANT: Python/FastAPI Implementation

**This Constitution v2.1 is built specifically for Python + FastAPI.**

While the core principles are language-agnostic, the examples, validation commands, and specific requirements throughout this document are Python-focused. This is honest, not a limitation.

**If you're adopting for a different language (Node.js, Go, Rust):**
- ✅ LITE or ULTRA-LITE paths abstract most language specifics
- ⚠️ FULL Constitution requires translation to your language
- 📖 See [CONSTITUTION-CUSTOMIZATION.md](../guides/CONSTITUTION-CUSTOMIZATION.md) for guidance
- 📋 See [HONEST-CRITIQUE-CONSTITUTION.md](../../HONEST-CRITIQUE-CONSTITUTION.md) for full transparency

**For multi-language support:**
- ⏳ v2.2 (Q2 2026): Universal principles + Python specialization
- ⏳ v3.0 (Q4 2026): Node.js, Go, Rust specializations

**Bottom line:** This Constitution works perfectly for Python. Other languages need translation (we're planning this for v3.0).

---

**PREAMBLE**

This Constitution codifies the immutable architectural principles that govern all systems built on the SPEC framework. These principles are not guidelines, recommendations, or suggestions. They are binding requirements that apply to every implementation, every feature, and every architectural decision.

The Constitution derives from lessons learned across multiple production systems, extensive load testing, security audits, and operational experience. Violating these principles leads to predictable failure modes. Adherence ensures systems that are maintainable, scalable, secure, and resilient.

---

## 🎯 CORE PRINCIPLE: Clean Architecture as Foundation

**THE PRINCIPLE**

All systems must implement 8-layer Clean Architecture as defined in ADR-001. The layers are:

```
Layer 8: Interfaces (Controllers, API handlers)
Layer 7: DTOs (Data serialization, Pydantic models)
Layer 6: Adapters (Infrastructure implementations)
Layer 5: Error Mapping (Domain → HTTP status codes)
Layer 4: Use Cases (Application logic, orchestration)
Layer 3: Ports (Abstract interfaces, contracts)
Layer 2: Domain (Business logic, entities)
Layer 1: Value Objects (Domain primitives)
```

**WHY THIS MATTERS**

Clean Architecture is the foundation upon which all other principles depend. It enables:
- **Testability** — Business logic tested without frameworks
- **Replaceability** — Infrastructure swapped without code changes
- **Clarity** — New engineers understand code structure immediately
- **Resilience** — Failures contained by layers
- **Evolution** — New frameworks supported without rewrite

**ENFORCEMENT**

- Every feature MUST follow all 8 layers
- Infrastructure MUST NEVER leak into domain layers
- Frameworks MUST NEVER appear in layers 1-5
- Error mapping MUST occur explicitly in Layer 5
- All adapters MUST implement ports (Layer 3 interfaces)

**VALIDATION**

```bash
# Automated layer validation
pytest tests/architecture/test_layers.py -v
pytest tests/architecture/test_no_cycles.py -v

# No framework imports in domain
grep -r "import fastapi\|import django" src/domain/ && exit 1
```

---

## ⚡ CORE PRINCIPLE: Async-First, No Blocking

**THE PRINCIPLE**

All I/O operations MUST be asynchronous. No blocking calls allowed on the event loop. CPU-bound work must be delegated to thread pool via ExecutorPort.

**REQUIRED BEHAVIOR**

✅ **Must be async:**
- External service calls (databases, APIs, search indexes)
- File I/O operations
- HTTP requests
- Cache operations
- Message queue operations
- Any I/O bound work

❌ **Must NOT be done:**
- `time.sleep()` (use `asyncio.sleep()`)
- Blocking file operations (use async equivalents)
- CPU-heavy computations in event loop
- Blocking library calls

**WHY THIS MATTERS**

The system must handle 50+ concurrent domain entities on a single machine. Blocking calls would reduce concurrency by orders of magnitude. Async-first enables:
- 50+ concurrent entities on single CPU
- Sub-second response times
- Linear memory growth (not exponential with threads)
- Natural event-driven architecture

**ENFORCEMENT**

- Code review: Check all I/O is async
- Linting: Detect blocking calls
- Runtime: Use async dev mode for blocking detection
- Testing: Load test with 50+ concurrent entities

> **Project example:** In rpg-narrative-server, this means 50+ concurrent campaigns. See [Campaign Load Testing](../../custom/rpg-narrative-server/SPECIALIZATIONS/constitution-rpg-specific.md#campaign-concurrency)

**VALIDATION**

```bash
# Find blocking calls
grep -r "time.sleep\|blocking_call" src/ && exit 1

# Check async consistency
pytest tests/quality/test_async_compliance.py -v

# Load test (50+ concurrent entities)
pytest tests/integration/test_concurrent_load.py --concurrent=50
```

---

## 🔌 CORE PRINCIPLE: Ports & Adapters (Hexagonal Architecture)

**THE PRINCIPLE**

All external systems MUST be accessed through Ports (abstract interfaces). Business logic MUST NOT know which adapter is being used. Multiple implementations of each port must be possible.

**TEN MANDATORY PORTS**

| Port | Purpose | Example Adapters |
|------|---------|------------------|
| KeyValueStorePort | Campaign KV storage | JSONFile, PostgreSQL, Redis |
| VectorStorePort | Vector indexing | ChromaDB, Qdrant, Pinecone |
| DocumentStorePort | Long-form documents | JSONAppendOnly, PostgreSQL |
| VectorReaderPort | Semantic search | ChromaDB, Qdrant |
| VectorWriterPort | Index updates | ChromaDB, Qdrant |
| LLMServicePort | LLM access | OpenAI, LocalLLM, Anthropic |
| EmbeddingGateway | Text → vectors | OpenAI embeddings, local |
| CampaignRepositoryPort | Campaign CRUD | JSONFile, PostgreSQL |
| ExecutorPort | CPU work | ThreadPool, Ray, Dask |
| EventBusPort | Events + lifecycle | Blinker, AsyncIO |

**WHY THIS MATTERS**

Ports ensure:
- **Zero lock-in** — Swap LLM providers without code change
- **Easy testing** — Mock ports in tests
- **Independence** — Business logic independent of infrastructure
- **Future-proof** — New adapters added without touching domain

**ENFORCEMENT**

- EVERY infrastructure access MUST go through a port
- NO direct imports of adapters in usecases
- EVERY adapter MUST implement a port's full contract
- Port methods MUST be async-first

**VALIDATION**

```bash
# Check no direct adapter access
grep -r "from.*adapters.*import" src/usecases/ && exit 1

# Run port compliance tests
pytest tests/contracts/ -v

# Verify adapters implement ports
pytest tests/architecture/test_adapter_implementation.py -v
```

---

## 🔒 CORE PRINCIPLE: Security by Default

**THE PRINCIPLE**

Security is not optional. Every system MUST implement the complete security model from `/EXECUTION/spec/CANONICAL/specifications/security-model.md`.

**MANDATORY SECURITY REQUIREMENTS**

**Authentication:**
- JWT tokens with HS256+ algorithm
- Token expiration: 1 hour (access), 30 days (refresh)
- Session timeout: 30 minutes idle
- Never store plaintext passwords

**Authorization:**
- RBAC: admin, game_master, player, viewer
- Deny-by-default (explicit allow only)
- Campaign isolation (each user sees only their campaigns)
- Audit log all permission checks

**Data Protection:**
- TLS 1.2+ for all traffic
- AES-256-GCM for sensitive data at rest
- Never log PII or secrets
- Encrypt API keys in environment

**Input Validation:**
- All inputs validated (Pydantic)
- No injection attacks possible
- Rate limiting: 50 req/min default
- Input constraints enforced

**WHY THIS MATTERS**

Security breaches destroy trust and cost millions. The security model provides:
- **OWASP Top 10 coverage** — Proven protection patterns
- **Compliance ready** — GDPR, CCPA requirements met
- **Operational confidence** — Know system is secure
- **User protection** — Privacy and safety guaranteed

**ENFORCEMENT**

- Code review: Check authentication on every endpoint
- Testing: Security integration tests in CI/CD
- Linting: Detect hardcoded secrets
- Audit: Monthly security review

**VALIDATION**

```bash
# Check no hardcoded secrets
git log -p | grep -i "password\|api_key\|secret" && exit 1

# Run security tests
pytest tests/contracts/security/ -v

# Verify HTTPS
curl -i http://api.example.com  # Must 301 to https://
```

---

## 📊 CORE PRINCIPLE: Observability is Production Requirement

**THE PRINCIPLE**

Every production system MUST implement complete observability. Logging, tracing, metrics, and on-call procedures are NOT optional.

**FOUR OBSERVABILITY PILLARS**

**1. Logging**
- Structured JSON logs
- Request ID on every log
- No sensitive data logged
- Per-layer appropriate logging

**2. Tracing**
- OpenTelemetry instrumentation
- Trace context propagation
- 10% sampling in production
- 100% sampling in staging

**3. Metrics**
- Golden Signals (latency, traffic, errors, saturation)
- Per-endpoint metrics
- Alerts on threshold violations
- Prometheus scraping

**4. On-Call**
- Incident runbooks for each alert
- 5-minute response time
- Blameless post-mortems within 24h
- Continuous improvement cycle

**WHY THIS MATTERS**

You cannot manage what you cannot observe. Observability enables:
- **Fast incident response** — See problem immediately
- **Continuous improvement** — Data-driven optimization
- **Operational confidence** — Know system is healthy
- **User satisfaction** — Quick fixes before complaints

**ENFORCEMENT**

- Every endpoint must have tracing
- Every error must appear in logs
- Metrics scraped every 30 seconds
- Alerts tested monthly

**VALIDATION**

```bash
# Check logging coverage
grep -c "logger\." tests/integration/test_*.py  # Should be > 0

# Verify tracing instrumentation
pytest tests/integration/test_tracing.py -v

# Check metrics collection
curl http://localhost:9090/metrics | grep "http_requests_total"
```

---

## 🎯 CORE PRINCIPLE: Performance SLOs Mandatory

**THE PRINCIPLE**

Every system MUST meet performance Service Level Objectives. Performance is not afterthought; it is architectural requirement.

**SLO COMMITMENTS**

**Response Time (P99 Latency)**

| Layer | Budget |
|-------|--------|
| Adapter | 10ms |
| Interface | 20ms |
| Application | 100ms |
| Domain | 200ms |
| Infrastructure | 500ms |

**Throughput Minimums**

| Endpoint | Minimum |
|----------|---------|
| GET endpoints | 100 RPS |
| POST endpoints | 50 RPS |
| AI generation | 5 RPS |
| Vector search | 50 RPS |

**Availability**

- 99.9% uptime target (4.3 hours downtime/month)
- Mean Time To Recovery (MTTR) < 5 minutes
- Mean Time Between Failures (MTBF) > 30 days

**WHY THIS MATTERS**

Users abandon slow systems. Performance SLOs ensure:
- **User satisfaction** — Experiences stay fast
- **Scalability plan** — Know when to scale
- **Cost control** — Only pay for needed resources
- **Competitive advantage** — Faster than competitors

**ENFORCEMENT**

- Benchmark every feature before merge
- Load tests in CI/CD
- Performance regression alerts
- Monthly performance review

**VALIDATION**

```bash
# Run performance benchmarks
pytest tests/quality/test_performance_slos.py -v

# Check P99 latency
pytest tests/quality/test_performance_slos.py::test_application_layer_latency -v

# Load test (50 RPS minimum)
pytest tests/quality/test_performance_slos.py::test_throughput_slo -v
```

---

## 🧵 CORE PRINCIPLE: Thread Isolation Mandatory

**THE PRINCIPLE**

All parallel work (whether AI agents or campaign runtimes) must be completely isolated. No shared mutable state between threads.

**TWO LEVELS OF ISOLATION**

**Level 1: Development Thread Isolation (Concurrent Development)**
- Each development thread has isolated scope
- Each thread has own work documented
- No modifications to other threads' work
- Global architecture changes coordinated

**Level 2: Runtime Thread Isolation (Concurrent Execution)**
- Each domain entity gets thread-local container
- Entity state never shared across threads
- Cleanup happens automatically
- System supports N+ concurrent entities

> **rpg-narrative-server specialization:** See [Campaign Thread Isolation](../../custom/rpg-narrative-server/SPECIALIZATIONS/constitution-rpg-specific.md#campaign-threads)

**WHY THIS MATTERS**

Thread safety is hard and bugs are subtle. Mandatory isolation ensures:
- **No race conditions** — Shared state eliminated
- **Parallel safety** — Multiple developers work safely
- **Scalability** — 50+ concurrent campaigns
- **Debugging** — Issues isolated to one thread

**ENFORCEMENT**

- Code review: Check thread boundaries
- Linting: Detect global state modifications
- Testing: Concurrent load tests
- Documentation: Thread state documented

**VALIDATION**

```bash
# Check thread isolation
pytest tests/integration/test_campaign_isolation.py -v

# Concurrent load test (50 campaigns)
pytest tests/integration/test_concurrent_campaigns.py --concurrent=50

# Memory leak detection
pytest tests/integration/test_campaign_cleanup.py --memray
```

---

## 🌍 CORE PRINCIPLE: Multitenancy by Design

**THE PRINCIPLE**

Systems MUST support multiple independent projects/clients in a single deployment. Tenants must be completely isolated.

**TENANT ISOLATION REQUIREMENTS**

- **Data isolation** — Campaign data isolated per tenant
- **Configuration isolation** — Each tenant different config
- **Resource isolation** — Quotas per tenant
- **Failure isolation** — One tenant's failure doesn't affect others

**IMPLEMENTATION PATTERN**

```python
# Every request includes tenant context
async def middleware(request, call_next):
    tenant_id = extract_tenant_from_request(request)
    request.state.tenant_id = tenant_id
    
    # Use tenant-scoped container
    with container.tenant_scope(tenant_id):
        response = await call_next(request)
    
    return response
```

**WHY THIS MATTERS**

Multitenancy enables:
- **SaaS model** — Multiple customers in one system
- **Cost efficiency** — Shared infrastructure
- **Faster iteration** — Deploy once, all customers updated
- **Simpler operations** — One system to manage

**ENFORCEMENT**

- Every endpoint extracts tenant/project ID
- Data queries filtered by tenant
- No cross-tenant data visible
- Tenant quotas enforced
- Storage isolated per tenant

**VALIDATION**

```bash
# Test tenant isolation
pytest tests/integration/test_tenant_isolation.py -v

# Verify no cross-tenant data leakage
pytest tests/quality/test_data_isolation.py -v
```

> **rpg-narrative-server specialization:** See [Campaign Multitenancy](../../custom/rpg-narrative-server/SPECIALIZATIONS/constitution-rpg-specific.md#campaign-isolation)

---

## 🔄 CORE PRINCIPLE: Consistency Model Defined

**THE PRINCIPLE**

The consistency model MUST be explicitly defined and documented. Choose from:

1. **Strong Consistency** — All reads see latest writes (slow)
2. **Eventual Consistency** — Reads eventually consistent (fast, complex)
3. **Causal Consistency** — Related operations ordered (balanced)
4. **Session Consistency** — Consistent within session (practical)

**OUR CHOICE: Causal Consistency**

- Campaign events are causally consistent
- Related events ordered correctly
- Read-your-own-writes guaranteed
- Eventually consistent across replicas

**WHY THIS MATTERS**

Consistency decisions affect:
- **Performance** — Strong = slow, eventual = fast
- **Correctness** — Eventual = complexity in application
- **User experience** — Session consistency feels instant

**ENFORCEMENT**

- Document consistency model per operation
- Tests verify consistency guarantees
- Failures don't violate consistency

**VALIDATION**

```bash
# Test consistency guarantees
pytest tests/integration/test_consistency.py -v

# Verify event ordering
pytest tests/quality/test_event_causality.py -v
```

---

## 🔌 CORE PRINCIPLE: Technology Stack Immutable

**THE PRINCIPLE**

Core technology decisions are locked in. Use only:

**MANDATORY:**
- FastAPI (HTTP framework)
- Pydantic (validation)
- Blinker (event bus)
- Python 3.11+ (language)
- asyncio (async runtime)

**STORAGE (Pick one per category):**
- Key-Value: PostgreSQL, Redis, or JSON files
- Vector: ChromaDB, Qdrant, or Pinecone
- Documents: PostgreSQL or JSON files

**EXTERNAL:**
- LLM: OpenAI, Local Ollama, or Anthropic
- Monitoring: Prometheus, Jaeger, DataDog

**YOU CANNOT USE:**
- ❌ Django (too heavy for microservices)
- ❌ SQL Alchemy ORM (use raw queries or SQLAlchemy Core)
- ❌ Celery (use asyncio + ExecutorPort)
- ❌ Synchronous frameworks
- ❌ Blocking I/O libraries

**WHY THIS MATTERS**

Technology choices have long-term consequences. Locked-in decisions ensure:
- **Team expertise** — Everyone knows stack
- **Hiring** — Know what to hire for
- **Consistency** — All services same tech
- **Interoperability** — Services work together

**ENFORCEMENT**

- Code review: Check technology stack
- Dependency scanning: No unapproved packages
- Architecture tests: Check imports

---

## 📜 CORE PRINCIPLE: Data Governance

**THE PRINCIPLE**

Data has rules. Define what data is collected, how long kept, who can access.

**DATA CLASSIFICATION**

| Classification | Examples | Encryption | Retention | Access |
|---|---|---|---|---|
| Public | Campaign names, stats | No | Indefinite | Everyone |
| Internal | System metrics | No | 90 days | Staff only |
| Confidential | User data, auth tokens | Yes | Until deleted | Authorized users |
| Secret | API keys | Yes | Until rotated | Service accounts |

**MANDATORY PRACTICES**

- Collect minimum necessary only
- Encrypt sensitive data at rest
- Never log PII or secrets
- Delete data after retention period
- Audit who accessed what

**WHY THIS MATTERS**

Data is liability. Proper governance:
- **Legal compliance** — GDPR, CCPA requirements
- **Trust** — Users trust us with data
- **Breach preparedness** — Know what to disclose
- **Cost control** — Don't store unnecessary data

**ENFORCEMENT**

- Data governance review in PRs
- PII audits monthly
- Retention policy enforced
- Access logs reviewed

---

## 🚨 CORE PRINCIPLE: Error Handling Strict

**THE PRINCIPLE**

Errors MUST be handled explicitly. No silent failures, no unhandled exceptions.

**ERROR HANDLING REQUIREMENTS**

1. **Catch specifically** — Not bare `except:`
2. **Log with context** — Include what failed and why
3. **Map to domain** — Convert to domain exceptions
4. **Handle at layer boundary** — Layer 5 maps to HTTP
5. **Return user-friendly message** — Never expose internals

**ERROR MAPPING EXAMPLE**

```python
# Domain layer raises domain exception
raise InvalidNarrativeError("Quality score below threshold")

# Application catches and handles
except InvalidNarrativeError as e:
    logger.warning(f"Narrative rejected: {e}")
    raise

# Layer 5 maps to HTTP
except InvalidNarrativeError:
    return HTTPException(
        status_code=400,
        detail="Narrative quality insufficient"
    )
```

**WHY THIS MATTERS**

Error handling affects:
- **Reliability** — Graceful degradation
- **Debugging** — Know what went wrong
- **Security** — Don't expose internals
- **User experience** — Clear error messages

**ENFORCEMENT**

- Code review: Check error handling
- Linting: No bare `except:`
- Testing: Error cases tested

---

## ♻️ CORE PRINCIPLE: Backward Compatibility Required

**THE PRINCIPLE**

Breaking changes are expensive. Maintain backward compatibility unless absolutely necessary.

**COMPATIBILITY RULES**

1. **API versions** — `/api/v1/` and `/api/v2/` both work
2. **Graceful degradation** — Old clients still work
3. **Deprecation warnings** — Tell users before breaking
4. **Migration path** — Help users upgrade
5. **Sunset timeline** — At least 6 months notice

**VERSIONING STRATEGY**

| Change | Version | Breaking? |
|--------|---------|-----------|
| Bug fix | 1.0.1 | No |
| New feature | 1.1.0 | No |
| Change behavior | 2.0.0 | Yes |
| Remove feature | 2.0.0 | Yes |

**WHY THIS MATTERS**

Breaking changes:
- **Cost users money** — Force them to upgrade
- **Damage trust** — We care about stability
- **Reduce adoption** — Users afraid to upgrade
- **Increase support** — Answer upgrade questions

**ENFORCEMENT**

- Breaking changes need architecture review
- Deprecation warnings added first
- Old version supported 6 months minimum
- Migration guide provided

---

## 🎓 CORE PRINCIPLE: Testability Non-Negotiable

**THE PRINCIPLE**

Code must be testable. If something can't be tested, it shouldn't be in production.

**TEST REQUIREMENTS**

| Layer | Coverage | Type |
|-------|----------|------|
| Domain | 95%+ | Unit |
| Application | 85%+ | Unit + Integration |
| Adapter | 80%+ | Unit + Integration |
| Interface | 70%+ | Integration + E2E |

**TEST TYPES**

- **Unit:** Test layer in isolation (mock dependencies)
- **Integration:** Test layer interaction (real dependencies)
- **E2E:** Test full request flow
- **Performance:** Benchmark against SLOs
- **Security:** Check vulnerability patterns

**WHY THIS MATTERS**

Testing ensures:
- **Confidence** — Know changes don't break things
- **Regression prevention** — Catch bugs early
- **Refactoring safety** — Change code without fear
- **Documentation** — Tests show how to use code

**ENFORCEMENT**

- Coverage gates in CI/CD (fail if below targets)
- Code review: Check tests before approving
- Performance regression tests
- Security scanning

---

## 🔗 CORE PRINCIPLE: Documentation Living

**THE PRINCIPLE**

Documentation must be kept up-to-date. Outdated docs are worse than no docs.

**DOCUMENTATION REQUIREMENTS**

| Type | Update | Owner |
|------|--------|-------|
| ADRs | Per decision | Architect |
| API Docs | Per API change | Developer |
| Runbooks | Per incident | SRE |
| Onboarding | Per release | Tech lead |

**DOCUMENTATION PROCESS**

1. Feature implemented
2. Documentation updated SAME PR
3. CI/CD verifies docs not stale
4. Deploy only if docs updated

**WHY THIS MATTERS**

Good documentation:
- **Onboarding faster** — New team members productive quickly
- **Fewer bugs** — Devs understand what to do
- **Continuity** — Knowledge doesn't leave with person
- **Quality** — Shared understanding of decisions

**ENFORCEMENT**

- Documentation in same PR as code
- CI/CD fails if docs outdated
- Annual documentation audit

---

## 🏆 SUMMARY: The Non-Negotiables

These principles are the foundation of every system built on SPEC:

1. **Clean Architecture** — 8 layers, always
2. **Async-First** — No blocking I/O
3. **Ports & Adapters** — Infrastructure abstraction
4. **Security by Default** — Complete security model
5. **Observability Required** — Logging, tracing, metrics, on-call
6. **Performance SLOs** — Meeting targets mandatory
7. **Thread Isolation** — Parallel safety
8. **Multitenancy** — Multiple projects supported
9. **Consistency Model** — Defined and tested
10. **Technology Stack** — Locked in, approved only
11. **Data Governance** — Rules for data lifecycle
12. **Error Handling** — Explicit, never silent
13. **Backward Compatibility** — Breaking changes costly
14. **Testability** — Everything testable
15. **Documentation** — Kept current

---

## 📞 Constitution Governance

**Questions about Constitution?**
- Ask Architecture Lead
- Check ADRs for rationale
- Request Constitution review if needed

**Violating Constitution?**
- Code review blocks merge
- CI/CD gates fail
- Architecture review required
- Document rationale or change approach

**Updating Constitution?**
- Propose via RFC (Request for Comments)
- Needs architect approval
- Needs engineering lead approval
- Update all related documentation

---

**Version:** 2.0 (Complete & Production-Grade)  
**Status:** ✅ Approved  
**Effective:** 2026-04-19  
**Next Review:** 2026-10-19 (6 months)  
**Owner:** Chief Architect  
**Enforcement:** Mandatory, non-negotiable
