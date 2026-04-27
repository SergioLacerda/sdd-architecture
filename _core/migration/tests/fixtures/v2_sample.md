# Sample v2.1 Constitution (for testing)

## 🎯 CORE PRINCIPLE: Clean Architecture

**THE PRINCIPLE**

All systems must implement 8-layer Clean Architecture.

**ENFORCEMENT**

- Every feature MUST follow all 8 layers
- Infrastructure MUST NEVER leak into domain
- Presentation layer must be UI-agnostic

**VALIDATION**

```bash
pytest tests/architecture/test_layers.py -v
```

---

## 🎯 CORE PRINCIPLE: Test-Driven Development

**THE PRINCIPLE**

All code must be written using TDD (tests first).

**ENFORCEMENT**

- Red-Green-Refactor cycle is mandatory
- Coverage must be >= 80%
- No code without corresponding tests

**RATIONALE**

TDD ensures design clarity and prevents regressions.

**VALIDATION**

```bash
pytest --cov
pytest --cov-report=term-missing
```
