# 🎬 Runtime Guides — Context-Aware for AI Agents

**Purpose:** Show how SPEC enables agents to create and use project-specific dynamic context  
**Audience:** AI agents, developers  
**Key Concept:** Context-aware ≠ SPECIALIZATIONS (dynamic ≠ static)

---

## 📚 What's in This Folder

```
runtime/
├── README.md (you are here)
├── CONTEXT_AWARE_USAGE.md        ← Main guide for agents
├── example-task-progress.md      ← How to track tasks
├── example-analysis.md           ← How to document discoveries
├── example-runtime-state.md      ← How to track live state
└── agent-workflow.md             ← Step-by-step for agents
```

---

## 🎯 Three Core Concepts

### 1️⃣ **SPECIALIZATIONS** (Static, Immutable)

**"How we always build on this project"**

```
Location: /docs/ia/CUSTOM/[PROJECT]/SPECIALIZATIONS/
Format: Markdown or YAML
Examples:
  - "Always use ThreadLocal for state"
  - "Use asyncio for concurrent work"
  - "API responses must include X-Request-ID header"
  
Change Frequency: Rarely (major architectural decisions)
Owner: Team (consensus)
```

### 2️⃣ **CONTEXT-AWARE** (Dynamic, Living)

**"What we discovered today"**

```
Location: .ai/context-aware/
Format: Markdown (organized by type)
Examples:
  - "Vector search is slow (500ms)"
  - "Campaign #5 has memory leak"
  - "Thread 1 is waiting for Thread 2"
  
Change Frequency: During work (agents create/update)
Owner: Agents + Team
```

### 3️⃣ **EXECUTION-STATE** (Thread State)

**"Who's working on what right now"**

```
Location: /docs/ia/CUSTOM/[PROJECT]/development/execution-state/
Format: Markdown + structured
Examples:
  - Thread isolation tracking
  - Current task assignment
  - Blockers and dependencies
  
Change Frequency: Per task (when work changes)
Owner: Agents
```

---

## 🤖 For Agents: Complete Workflow

### Scenario: You Discover a Performance Problem

```
1. SESSION START
   ✓ Read context-aware/task-progress/_current.md
   ✓ Read context-aware/analysis/_current-issues.md
   ✓ Read execution-state/_current.md

2. YOU WORK
   ✓ Profile code
   ✓ Find: Vector search takes 500ms (goal: 200ms)
   ✓ Root cause: N+1 queries in embedding loop
   ✓ Suggested fix: Batch embeddings

3. YOU DOCUMENT
   ✓ Create: context-aware/analysis/vector-search-bottleneck.md
     - What: Slow vector search
     - Why: N+1 queries
     - Fix: Batch embeddings
     - Severity: HIGH
   ✓ Update: context-aware/analysis/_current-issues.md
     - Add new issue

4. YOU COMMIT
   ✓ git add .ai/context-aware/
   ✓ git commit -m "📝 Document vector search bottleneck (500ms)"

5. NEXT SESSION (Another agent)
   ✓ Reads: context-aware/analysis/vector-search-bottleneck.md
   ✓ Knows: Issue exists, root cause, suggested fix
   ✓ Result: No duplicate investigation! 🎯
```

---

## 📊 Context-Aware Structure

### Folder: `task-progress/`

**What:** Current and completed tasks

```
task-progress/
├── _current.md              ← ALWAYS update before finishing
├── 2026-04-19.md           ← Tasks worked on today
├── completed/
│   ├── 2026-04-18.md       ← Yesterday's finished tasks
│   └── 2026-04-17.md
```

**When to update:** Before/after each task

**Who reads it:** Next agent (to avoid duplicate work)

### Folder: `analysis/`

**What:** Project discoveries and insights

```
analysis/
├── _current-issues.md           ← All known issues (living list)
├── _architecture-map.md         ← Module dependencies
├── vector-search-bottleneck.md  ← Specific findings
├── memory-leak-investigation.md ← Detailed analysis
```

**When to update:** When you discover something about the system

**Who reads it:** Next agent (to build on your findings)

### Folder: `runtime-state/`

**What:** Live execution context

```
runtime-state/
├── _current.md              ← Overall health score
├── active-threads.md        ← What threads are running
├── performance-metrics.md   ← Latency, throughput
├── deployment-status.md     ← Where is code running
└── known-issues.md          ← Active problems
```

**When to update:** During development, especially before commits

**Who reads it:** Next agent (to understand current state)

---

## ✅ Agent Pre-Flight Checklist

**When starting work on a project:**

```markdown
## Agent Pre-Flight Checklist

- [ ] .spec.config exists and is readable
- [ ] spec_path points to valid SPEC framework
- [ ] .ai/context-aware/ folder exists
- [ ] task-progress/_current.md is readable
- [ ] analysis/ has at least one file
- [ ] runtime-state/_current.md exists
- [ ] execution-state/_current.md has no conflicts
- [ ] I'm ready to work (context loaded)
```

**If ANY fail:** Report to team, don't proceed alone.

---

## 🔄 Agent Handoff Protocol

### Agent A finishes work

```bash
1. Update task-progress/_current.md
   - Mark task as COMPLETE
   - Document what was done
   - Note any blockers for next agent

2. Update analysis/ if needed
   - Add any findings
   - Update architecture map if code changed
   - Add any issues discovered

3. Update runtime-state/_current.md
   - Update performance metrics if changed
   - Note any threads that need pickup
   - Mark status as READY or BLOCKED

4. Commit with clear message
   git commit -m "✅ Task complete: [name] (ready for review)"

5. Tag for review
   git tag -a "task/[name]-complete" -m "Ready for review"
```

### Agent B starts work

```bash
1. Clone/pull latest
   git pull

2. Check context-aware
   cat .ai/context-aware/task-progress/_current.md
   cat .ai/context-aware/analysis/_current-issues.md

3. Read findings
   Understand what Agent A discovered

4. Review runtime-state
   Check performance metrics, active threads

5. Begin work (you're caught up!)
```

**Result:** No context switching, no information loss! 🎯

---

## 🚨 Error Recovery: Using Context-Aware

### Scenario: Your Code Breaks Tests

```bash
1. You see test failure: AssertionError in test_vector_search

2. Before investigating, check:
   cat .ai/context-aware/analysis/_current-issues.md
   # Find: "Vector search is slow (500ms)" ← Known issue!

3. Action:
   - If issue is known, don't re-investigate
   - Check suggested fix from context-aware
   - Apply that fix instead

4. Result:
   - Avoid duplicate debugging
   - Use previous agent's findings
   - Faster resolution
```

---

## 📈 Quality Metrics from Context-Aware

**What can you measure?**

```bash
# Issue density
wc -l .ai/context-aware/analysis/_current-issues.md
# Healthy: 50-100 lines (moderate complexity)

# Task velocity
wc -l .ai/context-aware/task-progress/*.md | tail -1
# Healthy: Growing (more tasks tracked)

# Architecture stability
diff -u <(cat .ai/context-aware/analysis/_architecture-map.md | grep "^|") \
        <(cat .ai/context-aware/analysis/_architecture-map-2026-04-18.md | grep "^|")
# Healthy: Few diffs (stable structure)

# Thread activity
cat .ai/context-aware/runtime-state/active-threads.md | grep "In Progress" | wc -l
# Healthy: 1-3 active threads (not overloaded)
```

---

## 🔗 Relationship to SPEC Framework

```
SPEC Framework Architecture:

CANONICAL/
  ├── rules/ ← Immutable principles (constitution, ia-rules)
  ├── decisions/ ← Architecture decisions (ADRs)
  └── specifications/ ← How to implement things
       ↓
SPECIALIZATIONS/ ← Project personality (how WE build)
       ↓
CONTEXT-AWARE/ ← Runtime discoveries (what WE learned today) ← YOU ARE HERE
       ↓
execution-state/ ← Thread state + task assignment
```

**Key insight:**
- CANONICAL = Framework rules (never changes)
- SPECIALIZATIONS = Project rules (rarely changes)
- context-aware = Project state (changes daily)
- execution-state = Who's doing what (changes per task)

---

## ✨ Benefits of Context-Aware

| Benefit | How It Works |
|---------|-------------|
| **No Duplicate Investigation** | Next agent reads analysis, doesn't re-investigate |
| **Faster Onboarding** | New agent reads task-progress, knows what was done |
| **Shared Knowledge** | All agents see runtime discoveries |
| **Context Persistence** | Work carries over between sessions |
| **Issue Tracking** | Known problems are documented, not forgotten |
| **Performance Insights** | Metrics tracked over time |
| **Async Collaboration** | Agents don't need to be online simultaneously |

---

## 🎓 Next Steps

**For a new project (like game-master-api):**

1. Copy structure from rpg-narrative-server:
   ```bash
   cp -r rpg-narrative-server/.ai game-master-api/.ai
   ```

2. Initialize files:
   ```bash
   cat game-master-api/.ai/context-aware/README.md  # Verify structure
   ```

3. Start using it:
   ```bash
   # Agent starts work
   cat .ai/context-aware/task-progress/_current.md
   # ... does work ...
   # Agent updates files and commits
   git add .ai/context-aware/ && git commit -m "📝 Update context"
   ```

4. You're done! Context-aware is live.

---

## 📚 Files in This Guide

- **CONTEXT_AWARE_USAGE.md** — Detailed usage for agents
- **example-task-progress.md** — What good task tracking looks like
- **example-analysis.md** — What good analysis looks like
- **example-runtime-state.md** — What good state tracking looks like
- **agent-workflow.md** — Step-by-step workflow

---

## 🚀 Ready to Use?

Context-aware is:
- ✅ Lightweight (just Markdown files)
- ✅ Portable (no database required)
- ✅ Agent-friendly (structures agents understand)
- ✅ Git-friendly (versioned with code)
- ✅ Async-friendly (doesn't need realtime updates)

**You're ready to start using context-aware today!**
