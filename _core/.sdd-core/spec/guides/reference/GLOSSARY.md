# 📖 GLOSSARY — SDD Terminology

**Common terms and definitions used throughout the framework**

---

## A

### ADR (Architecture Decision Record)
A document that records important architectural decisions and their rationale. Format: `ADR-###-topic-name.md`. Examples: ADR-001, ADR-003, etc.

### AGENT_HARNESS
The 7-phase workflow used by developers and AI agents to implement work: PHASE 1-7, covering rules, execution state, context loading, implementation, validation, and checkpointing.

### Autonomous Agent
An AI system (Copilot, Claude, etc.) that can work independently on tasks while following SDD rules and checkpointing progress.

---

## C

### CANONICAL Layer
The immutable, authoritative source of truth for the framework. Contains constitution, rules, decisions, and specifications. Never changes once defined.

### Checkpoint
A documented record of work completed, decisions made, risks identified, and current status. Updated after each feature in PHASE 7.

### Constitution
15 immutable principles that define SDD's core philosophy. The highest authority - never changes.

### Custom Layer
Project-specific documentation and specializations. Located in `EXECUTION/spec/custom/[PROJECT]/`.

---

## D

### Definition of Done
45+ detailed criteria for completing a feature. Used in PHASE 6 (Validation) to ensure quality.

### Decision Map
Overview document showing which flow (INTEGRATION vs EXECUTION) to use based on your task.

---

## E

### EXECUTION Flow
The 7-phase workflow for developers and AI agents implementing features. Also called AGENT_HARNESS.

### Execution State
Record of who is currently working on what, tracked in `.ai/context-aware/execution-state/`. Prevents conflicts between developers.

---

## G

### Governance
Rules + automation that enforces quality standards. Includes pre-commit hooks, tests, and checkpoints.

### Guides Layer
Step-by-step instructions for specific tasks. Located in `EXECUTION/spec/guides/`.

---

## I

### INTEGRATION Flow
The 5-step process for adding new projects to SDD framework. Takes 30 minutes.

---

## L

### Layers (6-layer hierarchy)
1. Constitutional (immutable)
2. Rules (mandatory)
3. Architecture (decisions)
4. Specifications (how-to)
5. Guides (operational)
6. Custom (project-specific)

---

## P

### Ports
Abstract interfaces for dependencies. Part of Ports & Adapters pattern (ADR-003).

### PHASE 0-7
The phases of AGENT_HARNESS workflow. Each phase has specific entry point and requirements.

---

## R

### Rules (16 Mandatory)
Set of non-negotiable requirements all developers/agents must follow. Located in `ia-rules.md`.

### Runtime Layer
Directory containing search indices and quick reference docs (`.ai/runtime/`).

---

## S

### SDD
Specification-Driven Development with Autonomous Governance. The framework itself.

### Specifications Layer
Practical patterns and standards for implementation. Located in `CANONICAL/specifications/`.

---

## T

### Thread
A single task or feature that one developer/agent works on. Each thread is isolated (thread isolation mandatory).

### Thread Isolation
Rule that each developer/agent modifies only their own task files. Prevents conflicts.

---

## V

### VALIDATION_QUIZ
8-10 question quiz about SDD principles. Must pass (≥80%) to proceed with development.

---

**More questions?** → See [FAQ.md](./FAQ.md)
