# 🚀 FASE 1: Runtime Infrastructure (SDD Remote Index)

**Status:** ✅ COMPLETE  
**Date:** 2026-04-19  
**Focus:** Agent discovery layer for on-demand context segmentation  

---

## 🎯 What Was Built

A new **runtime infrastructure** layer in PHASE 0 that creates `.ai/runtime/` directory with:

1. **README.md** — Master navigation for SDD remote index
2. **spec-canonical-index.md** — Index of CANONICAL/ (rules, decisions, specs)
3. **spec-guides-index.md** — Index of guides/ (onboarding, operational, emergency)
4. **search-keywords.md** — Keyword mapping for quick discovery

---

## 🏗️ New Directory Structure

After PHASE 0, agents get:

```
project-alvo/
├── .spec.config (seed)
├── .github/copilot-instructions.md (entry point)
│
├── .ai/ (NEW: Agent-created during PHASE 0)
│   │
│   ├── context-aware/ (dynamic discovery tracking)
│   │   ├── README.md
│   │   ├── task-progress/
│   │   │   ├── _current.md (current tasks)
│   │   │   └── completed/ (finished tasks)
│   │   ├── analysis/
│   │   │   └── _current-issues.md (discoveries)
│   │   └── runtime-state/
│   │       └── _current.md (metrics)
│   │
│   └── runtime/ (SDD REMOTE INDEX - NEW!)
│       ├── README.md (master navigation)
│       ├── spec-canonical-index.md (CANONICAL reference)
│       ├── spec-guides-index.md (guides reference)
│       └── search-keywords.md (keyword → document mapping)
│
├── .pre-commit-config.yaml (copied from templates)
├── scripts/
│   └── setup-precommit-hook.sh (copied from templates)
│
└── ... (project code)
```

---

## 🔍 Runtime Infrastructure Features

### 1. spec-canonical-index.md

**Purpose:** Navigate CANONICAL/ (immutable rules & architecture)

**What it does:**
- Lists all CANONICAL files (constitution, rules, decisions, specs)
- Shows what each file contains
- Provides reading paths (quick, implementation, debugging, design)
- Includes keyword search mapping

**Example search:**
```
Agent: "What are the rules?"
→ Search: "rules"
→ Found in: spec-canonical-index.md
→ Go to: CANONICAL/rules/ia-rules.md (16 mandatory protocols)
```

### 2. spec-guides-index.md

**Purpose:** Navigate guides/ (onboarding, operational, emergency)

**What it does:**
- Lists all guides (PHASE 0, AGENT_HARNESS, runtime, operational, emergency)
- Shows time to read, purpose, when to use
- Provides guide levels (essential, important, reference)
- Includes recommended reading schedule

**Example search:**
```
Agent: "How do I start working?"
→ Search: "workflow"
→ Found in: spec-guides-index.md
→ Go to: guides/onboarding/AGENT_HARNESS.md (7-phase protocol)
```

### 3. search-keywords.md

**Purpose:** Quick discovery via keyword mapping

**Structure:** Keyword → Document Location → Reason

**Example mappings:**
```
| architecture | CANONICAL/specifications/architecture.md | 8-layer structure |
| TDD | CANONICAL/specifications/testing.md | Test-driven development |
| incident | guides/emergency/incident-response.md | Production issues |
| checkpoint | guides/runtime/CONTEXT_AWARE_USAGE.md | Work documentation |
```

**Common scenarios:**
```
Scenario 1: "I don't know what rules apply"
  Search: "rules", "mandatory"
  → CANONICAL/rules/ia-rules.md

Scenario 2: "Something broke in production"
  Search: "incident", "emergency", "error"
  → guides/emergency/incident-response.md

Scenario 3: "How do I structure code?"
  Search: "architecture", "layers", "domain"
  → CANONICAL/specifications/architecture.md
```

### 4. README.md

**Purpose:** Master navigation & orientation

**What it includes:**
- Three states documentation (seed → initialization → ready)
- How to use the index
- Quick links table
- Agent usage pattern
- When to update

---

## 📊 Benefits

### For Agents

✅ **Quick Discovery** — Use search-keywords.md instead of guessing  
✅ **Segmented Context** — Load only what you need  
✅ **On-Demand Learning** — Reference specific docs without reading everything  
✅ **Under Control** — Know exactly where to look  

### For Projects

✅ **Single Source of Truth** — spec-architecture holds all knowledge  
✅ **Consistent** — All projects use same index structure  
✅ **Portable** — Runtime index is created locally, stays with project  
✅ **Discoverable** — No hidden knowledge, everything indexed  

---

## 🔄 How PHASE 0 Creates It

Updated script: `spec-architecture/docs/ia/SCRIPTS/phase-0-agent-onboarding.py`

**Step 3 now:**
1. Creates `.ai/runtime/` directory
2. Copies 4 runtime templates:
   - `templates/ai/runtime/README.md`
   - `templates/ai/runtime/spec-canonical-index.md`
   - `templates/ai/runtime/spec-guides-index.md`
   - `templates/ai/runtime/search-keywords.md`
3. Copies governance:
   - `templates/.pre-commit-config.yaml`
   - `templates/scripts/setup-precommit-hook.sh`
4. Makes scripts executable

**Result:** Complete infrastructure in ~15-20 minutes automated

---

## 📂 Moved to Templates

All these now live in `spec-architecture/templates/`:

```
templates/
├── .spec.config (seed config)
├── .github/copilot-instructions.md (entry point)
├── .vscode/ai-rules.md (generic rules)
├── .cursor/rules/spec.mdc (cursor rules)
├── .pre-commit-config.yaml (NEW - moved from projects)
├── scripts/
│   └── setup-precommit-hook.sh (NEW - moved from projects)
├── ai/
│   ├── context-aware/
│   │   ├── README.md
│   │   ├── task-progress/_current.md
│   │   ├── analysis/_current-issues.md
│   │   └── runtime-state/_current.md
│   └── runtime/ (NEW - on-demand index)
│       ├── README.md
│       ├── spec-canonical-index.md
│       ├── spec-guides-index.md
│       └── search-keywords.md
└── tests/
    └── specs-ia-units/ (mandate template)
```

---

## ✨ Agent Workflow (Updated)

```
Day 1: Agent joins project

T+0:00  Agent clones project
        Reads: .github/copilot-instructions.md

T+0:05  Discovers: .spec.config
        Extracts: spec_path = ../spec-architecture

T+0:15  Executes PHASE 0:
        $ python $SPEC_PATH/docs/ia/SCRIPTS/phase-0-agent-onboarding.py

T+0:30  Result:
        ✅ .ai/context-aware/ created (task tracking)
        ✅ .ai/runtime/ created (SDD index) ← NEW!
        ✅ .pre-commit-config.yaml created
        ✅ scripts/setup-precommit-hook.sh created
        ✅ Knowledge validated (quiz passed)

T+0:35  Agent reads:
        1. .ai/runtime/README.md (orientation)
        2. .ai/runtime/search-keywords.md (how to find things)

T+0:40  Agent proceeds:
        Reads: guides/onboarding/AGENT_HARNESS.md
        Ready for 7-phase workflow!
```

---

## 🎯 Use Cases

### Case 1: New Agent, First Day
```
Agent: "I'm overwhelmed, where do I start?"

Solution:
  1. Cat .ai/runtime/README.md
  2. Read "Agent Usage Pattern" section
  3. Understand the 3 states (seed → init → ready)
  4. Proceed with confidence
```

### Case 2: Searching for a Pattern
```
Agent: "How do I write a port?"

Solution:
  1. Cat .ai/runtime/search-keywords.md
  2. Find: "ports" → CANONICAL/decisions/ADR-003
  3. Read decision + examples
  4. Implement pattern
```

### Case 3: Production Issue
```
Agent: "Everything is broken, where's the runbook?"

Solution:
  1. Cat .ai/runtime/search-keywords.md
  2. Find: "incident", "emergency"
  3. Go to: guides/emergency/incident-response.md
  4. Follow 5-step recovery
```

### Case 4: Lost in Context
```
Agent: "I have 100 docs open, need to focus"

Solution:
  1. Use .ai/runtime/spec-guides-index.md
  2. Find "guide levels" (essential, important, reference)
  3. Focus on essential first
  4. Load others on-demand
```

---

## 📊 Quality Metrics

| Metric | Status |
|--------|--------|
| On-demand context segmentation | ✅ Implemented |
| Keyword search layer | ✅ Implemented |
| Reference caching organization | ✅ Implemented |
| PHASE 0 integration | ✅ Complete |
| Project templates | ✅ Updated |
| Agent workflow | ✅ Streamlined |
| Documentation | ✅ Comprehensive |

---

## ✅ Deliverables

**Templates Added:**
- ✅ templates/ai/runtime/README.md
- ✅ templates/ai/runtime/spec-canonical-index.md
- ✅ templates/ai/runtime/spec-guides-index.md
- ✅ templates/ai/runtime/search-keywords.md
- ✅ templates/.pre-commit-config.yaml
- ✅ templates/scripts/setup-precommit-hook.sh

**Scripts Updated:**
- ✅ phase-0-agent-onboarding.py (now copies runtime)

**Projects Updated:**
- ✅ rpg-narrative-server (cleaned up, minimal seed)

**Commits:**
```
ca86088  ✨ Add Runtime Infrastructure (SDD Remote Index)
6754367  🧹 Cleanup: Move pre-commit infrastructure to templates
```

---

## 🎓 How Agents Use Runtime Index

### Discovery Flow
```
Agent has question
    ↓
Search: .ai/runtime/search-keywords.md
    ↓
Find: matching keyword(s)
    ↓
Get: document location in SPEC_PATH
    ↓
Read: specific document
    ↓
Learn: under demand (efficient)
```

### Example: "What's thread isolation?"
```
Search: search-keywords.md for "thread"
Found: concurrent | CANONICAL/decisions/ADR-004
Read: spec-architecture/EXECUTION/spec/CANONICAL/decisions/ADR-004
Learn: "Each thread owns its code" (20 min read)
No wasted time on unrelated docs
```

---

## 🚀 Next Steps

### For Projects Using PHASE 0

1. **Run PHASE 0:**
   ```bash
   python $(grep spec_path .spec.config | cut -d' ' -f3)/docs/ia/SCRIPTS/phase-0-agent-onboarding.py
   ```

2. **Explore Runtime Index:**
   ```bash
   cat .ai/runtime/README.md
   cat .ai/runtime/search-keywords.md
   ```

3. **Proceed to AGENT_HARNESS:**
   ```bash
   cat $(grep spec_path .spec.config | cut -d' ' -f3)/docs/ia/guides/onboarding/AGENT_HARNESS.md
   ```

### For New Projects

1. **Copy seed:**
   ```bash
   cp spec-architecture/.spec.config .
   cp -r spec-architecture/.github .
   ```

2. **Agent runs PHASE 0** (rest is automatic)

3. **Infrastructure created** with runtime index included

---

## 📊 Impact

**Before (Manual Setup):**
- Agent needs to find docs manually
- No index, no search layer
- Context scattered across files
- Learning curve steep

**After (Runtime Index):**
- Agent uses search-keywords.md
- Find docs in seconds
- Context organized by topic
- Learning curve gentle
- On-demand segmentation ✅

---

**FASE 1 Status:** ✅ **COMPLETE**

Runtime infrastructure enables agents to:
- Discover what they need
- Find it quickly
- Learn under demand
- Stay focused
- Work efficiently

**Result:** Scalable, discoverable, agent-friendly SDD framework 🚀
