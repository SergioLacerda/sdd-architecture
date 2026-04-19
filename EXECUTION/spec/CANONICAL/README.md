# CANONICAL Layer — Immutable Authority

**Layer:** CANONICAL  
**Authority Level:** ✅ YES — These define the ideal  
**Update Frequency:** Rare (only ADRs, breaching changes via formal process)  
**Owner:** Architect + ADR process  
**Last Reviewed:** April 2026 ✅  
**Next Review Required:** October 2026  

---

## Purpose

This layer contains the **immutable rules, specifications, and decisions** that govern the system. These files represent the source of truth for:
- System architecture and design constraints
- Coding standards and conventions
- Formal decisions made via Architecture Decision Records (ADRs)
- Contract specifications (what the system SHOULD do)

## Structure

### rules/
Foundational rules that CANNOT be bypassed:
- `ia-rules.md` — 16 mandatory execution protocols
- `constitution.md` — Immutable principles  
- `conventions.md` — Naming, style, and code organization

### specifications/
Technical specifications defining system behavior:
- `architecture.md` — 8-layer clean architecture blueprint
- `contracts.md` — 18 ports, their guarantees, and signatures
- `feature-checklist.md` — 8-layer feature development process
- `testing.md` — Test patterns and coverage expectations
- `definition_of_done.md` — Merge criteria and quality gates

### decisions/
Formal architectural decisions:
- `ADR-001-clean-architecture-8-layer.md` — Foundation
- `ADR-002-async-first-no-blocking.md` — No synchronous I/O
- `ADR-003-ports-adapters-pattern.md` — Hexagonal architecture
- `ADR-004-vector-index-strategy.md` — Vector DB abstraction
- `ADR-005-thread-isolation-mandatory.md` — Concurrency model
- `ADR-006-append-only-storage.md` — Event sourcing

## When to Reference

**Use CANONICAL for:**
- Understanding what the system SHOULD be
- Understanding WHY architecture decisions exist
- Validating code against immutable rules
- Adding new architecture constraints

**When updating:**
- Changes require ADR process (formal review)
- Updates must not conflict with existing ADRs
- Document the decision (add to decisions/)
- Notify team (this is authoritative)

## Authority Hierarchy

1. **Constitution** (principles) — highest authority
2. **Architecture** + **Contracts** — system design
3. **Feature Checklist** — development process
4. **Testing** + **Definition of Done** — quality gates
5. **ADRs** — technical decisions
6. **Rules** — execution protocols

---

**NOTE:** This layer is read-mostly. Changes happen ~1/quarter via ADR process.
