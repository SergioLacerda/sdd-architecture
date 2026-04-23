# 📇 SPEC-CANONICAL Index

**Remote Location:** SPEC_PATH/docs/ia/CANONICAL/  
**Purpose:** Quick reference to all immutable rules and architecture  
**Updated:** [auto-filled by agent]  

---

## 🔴 Core Documents (Read in This Order)

### 1. Constitution
**File:** constitution.md  
**Lines:** ~150  
**What:** 15 immutable principles that guide all SDD work  
**When:** Understand what SPEC is about  
**Key Sections:**
- Principle 1-5: Framework authority
- Principle 6-10: Project autonomy
- Principle 11-15: Agent responsibility

---

### 2. Rules (IA-RULES)
**File:** rules/ia-rules.md  
**Lines:** ~400  
**What:** 16 mandatory execution protocols  
**When:** Before every implementation  
**Key Rules:**
- Rule 1-4: Architecture layer isolation
- Rule 5-8: Testing & validation
- Rule 9-12: Context & state management
- Rule 13-16: Governance & checkpointing

---

### 3. Decisions (ADRs)
**Directory:** decisions/  
**Count:** 6+ Architecture Decision Records  

#### ADR-001: Spec-Driven Development Pattern
- **Topic:** Overall SDD approach
- **Decision:** Framework-first, project-second
- **Status:** Active

#### ADR-002: 8-Layer Clean Architecture
- **Topic:** Architecture layering
- **Layers:** Domain, usecases, interfaces, frameworks, infrastructure, bootstrap, config, shared
- **Status:** Active

#### ADR-003: Ports & Adapters Pattern
- **Topic:** Dependency inversion
- **Decision:** Never import infrastructure directly
- **Status:** Active

#### ADR-004: Thread Isolation
- **Topic:** Concurrent development
- **Decision:** Each thread owns its code
- **Status:** Active

#### ADR-005: Context-Aware Infrastructure
- **Topic:** Dynamic agent context
- **Decision:** .ai/context-aware/ for discoveries
- **Status:** Active

#### ADR-006: .spec.config Pattern
- **Topic:** Project discovery
- **Decision:** INI config for SPEC framework location
- **Status:** Active

---

### 4. Specifications
**Directory:** specifications/  
**Count:** 5+ Comprehensive Specs

#### architecture.md
- **Topic:** 8-layer clean architecture
- **Includes:** Layer responsibilities, communication patterns
- **Reference for:** Understanding project structure

#### testing.md
- **Topic:** Testing patterns (unit, integration, contract, golden)
- **Includes:** Test structure, TDD approach, coverage expectations
- **Reference for:** Writing tests during implementation

#### patterns.md
- **Topic:** Reusable patterns (ports, adapters, factories)
- **Includes:** Code examples, when to use each
- **Reference for:** Implementing features

#### requirements.md
- **Topic:** Non-functional requirements
- **Includes:** Performance, security, scalability, maintainability
- **Reference for:** Design decisions

#### conventions.md
- **Topic:** Code conventions (naming, structure, organization)
- **Includes:** Python/Go/TypeScript specific patterns
- **Reference for:** Code style consistency

---

## 🔍 How to Search This Index

**Use this mapping to find what you need:**

| You Need | Find In | Search For |
|----------|---------|-----------|
| "What are the rules?" | rules/ia-rules.md | "Rule 1-16" |
| "How do I structure code?" | specifications/architecture.md | "8-layer", "domain", "usecases" |
| "How do I write tests?" | specifications/testing.md | "unit test", "TDD", "contract" |
| "Why no direct imports?" | decisions/ADR-003 | "ports", "adapters", "infrastructure" |
| "How do agents find SPEC?" | decisions/ADR-006 | ".spec.config", "discovery" |
| "What are the principles?" | constitution.md | "Principle 1-15" |

---

## 📊 Quick Reference

### By Topic

**Architecture:**
- decisions/ADR-002 (8-layer)
- specifications/architecture.md
- specifications/patterns.md

**Testing:**
- specifications/testing.md
- rules/ia-rules.md (Rule 4: TDD)

**Development:**
- rules/ia-rules.md (Rule 1-16)
- specifications/conventions.md

**Collaboration:**
- decisions/ADR-004 (thread isolation)
- rules/ia-rules.md (Rule 2: isolation)

**Discovery & Onboarding:**
- decisions/ADR-006 (.spec.config)
- constitution.md (principles)

---

## 📖 Reading Paths

### Path 1: New Agent (Full Understanding - 1 hour)
```
1. constitution.md (15 min) — Understand principles
2. rules/ia-rules.md (20 min) — Learn mandatory rules
3. decisions/ADR-001 (5 min) — Why SDD?
4. specifications/architecture.md (15 min) — Project structure
5. specifications/testing.md (5 min) — Testing approach
```

### Path 2: Implementing Feature (30 min)
```
1. specifications/architecture.md (10 min) — Find layer
2. specifications/patterns.md (10 min) — Find pattern
3. rules/ia-rules.md (5 min) — Refresh rules
4. specifications/testing.md (5 min) — Write tests
```

### Path 3: Debugging Issue (15 min)
```
1. specifications/architecture.md (5 min) — Understand layer
2. rules/ia-rules.md (5 min) — Check for violations
3. specifications/patterns.md (5 min) — Verify pattern usage
```

### Path 4: Design Decision (20 min)
```
1. decisions/ (10 min) — Find related ADR
2. specifications/ (10 min) — Find specification
3. Verify: Does your design align?
```

---

## ⏰ Update Frequency

This index is:
- **Static** (rarely changes) — CANONICAL is immutable
- **Auto-synced** during PHASE 0 (reads from remote)
- **Reference only** — Don't modify this file

To update: See SPEC_PATH/docs/ia/CANONICAL/README.md for governance

---

**Location:** .ai/runtime/spec-canonical-index.md  
**SPEC Version:** 2.1  
**Authority:** spec-architecture (remote, source of truth)
