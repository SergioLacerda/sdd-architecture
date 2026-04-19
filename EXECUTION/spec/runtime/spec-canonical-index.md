# 📑 CANONICAL Layer Index

**Complete reference to the immutable authority layer**

---

## 🔴 Authority Hierarchy

This layer is second only to the Constitution. Contains rules, decisions, and specifications.

```
Constitution (never changes)
    ↓
Rules (16 mandatory)
    ↓
Decisions (ADRs - why rules exist)
    ↓
Specifications (how to follow rules)
```

---

## 📋 Rules

### Constitution
**File:** `CANONICAL/rules/constitution.md`  
**What:** 15 immutable principles defining SDD philosophy  
**Authority:** Highest (never changes)  
**When:** Read PHASE 1, reference throughout  
**Key Topics:**
- AI agents are first-class citizens
- Governance is automated
- Every decision is documented
- Developers are autonomous

### Mandatory Rules (16 total)
**File:** `CANONICAL/rules/ia-rules.md`  
**What:** Non-negotiable requirements for all developers/agents  
**Authority:** Mandatory (must follow or PR rejected)  
**When:** Read PHASE 1, verify in PHASE 6  
**Key Topics:**
- Rule 1: Ports mandatory (no direct infrastructure imports)
- Rule 3: Tests during implementation (TDD)
- Rule 5: Thread isolation (only modify YOUR work)
- Rule 16: (See file for complete list)

### Conventions
**File:** `CANONICAL/rules/conventions.md`  
**What:** Code style, naming, and format standards  
**Authority:** Standards (followed during implementation)  
**When:** Reference during PHASE 5  
**Key Topics:**
- File naming conventions
- Code structure
- Documentation format
- Comment style

---

## 🟡 Architecture Decisions (ADRs)

Why each architectural choice was made. Read when you need to understand WHY a rule exists.

### ADR-001: Clean Architecture (8-Layer)
**File:** `CANONICAL/decisions/ADR-001-clean-architecture-8-layer.md`  
**Topic:** Why we use 8-layer hexagonal architecture  
**Related Rules:** Rule 1 (ports mandatory)  
**When:** If you ask "why this structure?"

### ADR-002: Async-First Design
**File:** `CANONICAL/decisions/ADR-002-async-first-no-blocking.md`  
**Topic:** Why all operations are async, never blocking  
**Related Rules:** Multiple performance rules  
**When:** If you ask "why async everywhere?"

### ADR-003: Ports & Adapters Pattern
**File:** `CANONICAL/decisions/ADR-003-ports-adapters-pattern.md`  
**Topic:** Why infrastructure must be pluggable via ports  
**Related Rules:** Rule 1 (no direct imports)  
**When:** If you ask "why ports?" or "what's a port?"

### ADR-004: Vector Index Strategy
**File:** `CANONICAL/decisions/ADR-004-vector-index-strategy.md`  
**Topic:** Why we index vectors for semantic search  
**Related Rules:** Search-related rules  
**When:** If implementing search functionality

### ADR-005: Thread Isolation Mandatory
**File:** `CANONICAL/decisions/ADR-005-thread-isolation-mandatory.md`  
**Topic:** Why each developer/agent must work in isolation  
**Related Rules:** Rule 5 (thread isolation)  
**When:** If you ask "why can't I modify their work?"

### ADR-006: Append-Only Storage
**File:** `CANONICAL/decisions/ADR-006-append-only-storage.md`  
**Topic:** Why data is append-only (immutable)  
**Related Rules:** Data integrity rules  
**When:** If working with storage

---

## 🟢 Specifications (How-To)

Practical patterns and standards for implementation.

### Definition of Done
**File:** `CANONICAL/specifications/definition_of_done.md`  
**What:** 45+ detailed criteria for feature completion  
**Authority:** Standard (use during PHASE 6 validation)  
**Sections:**
- Code quality criteria
- Testing requirements
- Documentation standards
- Performance benchmarks
- Security checks

**When:** During PHASE 6 (Validation) - use as checklist

### Communication Standards
**File:** `CANONICAL/specifications/communication.md`  
**What:** How to document decisions, risks, and discoveries  
**Authority:** Standard (follow during PHASE 7 checkpointing)  
**Sections:**
- How to write a checkpoint
- Decision documentation template
- Risk assessment format
- Comment guidelines

**When:** During PHASE 7 (Checkpoint) when documenting work

---

## 🗺️ Quick Navigation by Need

### "I need to understand core principles"
→ `CANONICAL/rules/constitution.md` (15 immutable principles)

### "I need to know what I MUST do"
→ `CANONICAL/rules/ia-rules.md` (16 rules)

### "I need to know WHY a decision was made"
→ `CANONICAL/decisions/ADR-*.md` (architecture decisions)

### "I need to know HOW to follow a rule"
→ `CANONICAL/specifications/definition_of_done.md` (practical patterns)

### "I need to know HOW to document my work"
→ `CANONICAL/specifications/communication.md` (templates and formats)

### "I need to know code style"
→ `CANONICAL/rules/conventions.md` (naming and format)

---

## 📊 Layers Below CANONICAL

After mastering CANONICAL, explore:

| Layer | Purpose | Where |
|-------|---------|-------|
| **Guides** | Step-by-step help | `guides/onboarding/` and `guides/operational/` |
| **Emergency** | When things break | `guides/emergency/` |
| **Reference** | Definitions & examples | `guides/reference/` |
| **Custom** | Project-specific | `custom/[PROJECT]/` |
| **Runtime** | Quick lookup | `runtime/` |

---

## ⚡ Emergency Quick Links

**Need help immediately?**

- Can't decide what to do? → `CANONICAL/specifications/definition_of_done.md`
- Need to document? → `CANONICAL/specifications/communication.md`
- Don't understand a rule? → Find matching ADR in `CANONICAL/decisions/`
- Style questions? → `CANONICAL/rules/conventions.md`

---

**For complete SDD docs:** [NAVIGATION.md](../../../NAVIGATION.md)  
**For quick search:** [search-keywords.md](../runtime/search-keywords.md)
