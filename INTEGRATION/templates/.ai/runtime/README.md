# 🔗 Runtime References — SDD Remote Index

**Purpose:** Index and search layer for spec-architecture (remote SDD)  
**Updated:** [timestamp will be filled by agent]  
**Project:** [project-name from .spec.config]  

---

## 🎯 What is this?

This directory provides **on-demand context segmentation** for agents:
- ✅ Index of remote SPEC framework (spec-architecture)
- ✅ Quick navigation to rules, patterns, specifications
- ✅ Search keywords for fast discovery
- ✅ Context caching (load only what you need)

---

## 📍 Quick Links to Remote SDD

### Core Rules & Architecture

| What | Link | When | Search |
|------|------|------|--------|
| **Rules** | SPEC_PATH/docs/ia/CANONICAL/rules/ia-rules.md | Starting work | "rules", "mandatory protocols" |
| **Constitution** | SPEC_PATH/docs/ia/CANONICAL/constitution.md | Understanding principles | "principles", "immutable" |
| **Decisions** | SPEC_PATH/docs/ia/CANONICAL/decisions/ | Understanding patterns | "ADR", "decision", "pattern" |
| **Specs** | SPEC_PATH/docs/ia/CANONICAL/specifications/ | Implementing features | "architecture", "testing", "requirements" |

### Onboarding & Workflow

| What | Link | When | Search |
|------|------|------|--------|
| **PHASE 0** | SPEC_PATH/docs/ia/guides/onboarding/PHASE-0-AGENT-ONBOARDING.md | First time | "onboarding", "PHASE 0", "initialization" |
| **AGENT_HARNESS** | SPEC_PATH/docs/ia/guides/onboarding/AGENT_HARNESS.md | Starting work | "HARNESS", "7 phases", "workflow" |
| **VALIDATION_QUIZ** | SPEC_PATH/docs/ia/guides/onboarding/VALIDATION_QUIZ.md | Knowledge check | "quiz", "knowledge", "validation" |

### Runtime & Context-Aware

| What | Link | When | Search |
|------|------|------|--------|
| **Context Usage** | SPEC_PATH/docs/ia/guides/runtime/CONTEXT_AWARE_USAGE.md | Managing context | "context-aware", "task-progress", "discovery" |
| **Task Example** | SPEC_PATH/docs/ia/guides/runtime/example-task-progress.md | Real workflow | "example", "workflow", "task-progress" |
| **Runtime Index** | SPEC_PATH/docs/ia/guides/runtime/_INDEX.md | Navigation | "index", "navigation", "guides" |

### Operational Guides

| What | Link | When | Search |
|------|------|------|--------|
| **Emergency** | SPEC_PATH/docs/ia/guides/emergency/ | Things break | "emergency", "broken", "error", "recovery" |
| **Operations** | SPEC_PATH/docs/ia/guides/operational/ | Daily work | "operational", "process", "workflow" |

---

## 🔍 How to Use This Index

### Scenario 1: "I'm starting a task"
```
1. Go to AGENT_HARNESS
2. Read: "Choose PATH A/B/C/D"
3. Load only context for your PATH
4. Don't load unnecessary docs
```

### Scenario 2: "I hit an error"
```
1. Search: see search-keywords.md
2. Find: matching error type
3. Go to: emergency/
4. Execute: recovery procedure
```

### Scenario 3: "I need to understand a pattern"
```
1. Search: see spec-canonical-index.md
2. Find: matching ADR or spec
3. Read: decision rationale
4. Apply: pattern to your code
```

---

## 📊 Index Structure

See detailed indexes:
- [spec-canonical-index.md](./spec-canonical-index.md) — All CANONICAL files
- [spec-guides-index.md](./spec-guides-index.md) — All guides
- [search-keywords.md](./search-keywords.md) — Keyword search mapping

---

## 🎯 Agent Usage Pattern

```
Agent workflow:
  1. Read: .spec.config (discover SPEC_PATH)
  2. Go to: SPEC_PATH/docs/ia/
  3. Use: .ai/runtime/ as index
  4. Search: using search-keywords.md
  5. Load: only needed context
  6. Work: with confidence!
```

---

## ⏱️ When to Update This

This index is **auto-updated when:**
- Agent runs PHASE 0 (copies latest from remote)
- New context is discovered (add to analysis/)
- Search queries fail (add to search-keywords.md)

---

## 🔗 Back to Context-Aware

- Task tracking: `../.ai/context-aware/task-progress/`
- Discoveries: `../.ai/context-aware/analysis/`
- Runtime state: `../.ai/context-aware/runtime-state/`
- **This index**: `../.ai/runtime/` (you are here)

---

**Last Updated:** [auto-filled by agent]  
**SPEC Version:** 2.1  
**Project:** [from .spec.config]
