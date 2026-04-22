# 🎯 Context-Aware Agent Pattern — CANONICAL SPECIFICATION

**Authority:** SPEC v2.1 (Immutable)  
**Status:** Mandatory for all agents  
**Version:** 1.0  
**Updated:** April 19, 2026

---

## 📍 Overview

**Purpose:** Define how AI agents create and use project-specific dynamic context  
**Scope:** All agent work on SPEC-governed projects  
**Key Principle:** Context-aware ≠ SPECIALIZATIONS (dynamic ≠ static)

**This specification answers:**
- ✅ When do I create context vs. specialization?
- ✅ What folder structure should I use?
- ✅ How do I document my discoveries?
- ✅ How do I track tasks and state?

---

## 🎯 Three Core Concepts

### 1️⃣ **SPECIALIZATIONS** (Static, Immutable)

**Definition:** "How we ALWAYS build on this project"

**Characteristics:**
- 📍 Location: `EXECUTION/spec/custom/[PROJECT]/SPECIALIZATIONS/`
- 📄 Format: Markdown or YAML
- 🔄 Change Frequency: Rarely (major architectural decisions)
- 👥 Owner: Team (consensus)
- ⏱️ Lifetime: Project lifecycle

**Examples:**
```
- "Always use ThreadLocal for state"
- "Use asyncio for concurrent work"
- "API responses must include X-Request-ID header"
- "Database: PostgreSQL with connection pooling"
- "Message format: Always include version number"
```

**When to create:**
- Major architectural decisions
- Team consensus reached
- Decision affects multiple tasks
- Change impacts future work

**Validation:**
- ✅ Reviewed by team lead
- ✅ Documented with rationale
- ✅ Affects 2+ tasks/modules

---

### 2️⃣ **CONTEXT-AWARE** (Dynamic, Living)

**Definition:** "What we discovered TODAY"

**Characteristics:**
- 📍 Location: `.ai/context-aware/` (project-local, not in framework)
- 📄 Format: Markdown (organized by type)
- 🔄 Change Frequency: During work (agents create/update)
- 👥 Owner: Agents + Team
- ⏱️ Lifetime: Session to task duration (then archive)

**Examples:**
```
- "Vector search is slow (500ms)"
- "Campaign #5 has memory leak"
- "Thread 1 is waiting for Thread 2"
- "ChromaDB API v0.3 has batch_search method"
- "Database connection pool exhausted under load"
```

**Types of Context-Aware Documents:**

#### Type 1: Task Progress
**File:** `.ai/context-aware/task-progress/_current.md`  
**Owner:** Agent executing the task  
**Audience:** Next agent (handoff)

```markdown
### Task 5: Optimize Vector Search
- **Status:** In Progress
- **Agent:** Agent Name
- **Started:** 2026-04-19
- **Expected Completion:** 2026-04-20
- **Subtasks:**
  - [ ] Profile current implementation
  - [ ] Identify N+1 queries
  - [ ] Implement batching
  - [ ] Verify performance improvement
- **Blockers:** None
- **Notes:** See analysis/_current-issues.md #Issue1
```

#### Type 2: Issue Documentation
**File:** `.ai/context-aware/analysis/[issue-name].md`  
**Owner:** Agent who discovered it  
**Audience:** Any agent (reference)

```markdown
# Vector Search Bottleneck

**Severity:** 🔴 HIGH  
**Impact:** Campaign search takes 500ms (goal: 100ms)  
**Root Cause:** N+1 queries in embedding loop

## Investigation
1. Profiled with cProfile
2. Found: ChromaDB.search() called 50x per campaign
3. Root cause: Loop over campaigns, search each one

## Suggested Fix
- Implement batch_search() method
- Call once instead of 50x
- Expected: 500ms → 50ms (10x improvement)
```

#### Type 3: Architecture Analysis
**File:** `.ai/context-aware/analysis/_architecture-map.md`  
**Owner:** Agent who reviewed structure  
**Audience:** Next agent (understanding dependencies)

```markdown
# Architecture Map

## Dependency Graph
Application Layer → Domain Layer → Infrastructure Layer

## Red Flags ✅
- [x] No circular imports
- [x] Domain doesn't import infrastructure
- [x] All infrastructure behind ports
- [x] Thread safety verified

## Current Bottlenecks
- Vector search (500ms) — see vector-search-bottleneck.md
```

#### Type 4: Runtime State
**File:** `.ai/context-aware/runtime-state/_current.md`  
**Owner:** Agent executing the task  
**Audience:** Next agent (immediate context)

```markdown
# Runtime State — 2026-04-19

## Active Threads
| Thread | Work | Status | Blocker |
|--------|------|--------|---------|
| Thread 1 | Vector optimization | In Progress | None |
| Thread 2 | Cache refactor | Waiting | Thread 1 complete |

## Environment State
- Database: Connected ✅
- Cache: 450MB/500MB used (90%) ⚠️
- Vector DB: Responsive ✅

## Known Issues
- Cache memory pressure (mitigation: see analysis/cache-pressure.md)
```

**When to create:**
- Discover a performance issue
- Learn something about the system
- Find a dependency or blocker
- Start or update a task

**Validation:**
- ✅ Dated and authored
- ✅ Clear and actionable
- ✅ Linked to related tasks

---

### 3️⃣ **EXECUTION-STATE** (Thread State)

**Definition:** "Who's working on WHAT right now"

**Characteristics:**
- 📍 Location: `EXECUTION/spec/custom/[PROJECT]/development/execution-state/`
- 📄 Format: Markdown + structured  
- 🔄 Change Frequency: Per task (when work changes)
- 👥 Owner: Agents
- ⏱️ Lifetime: Task duration (updated per checkpoint)

**Examples:**
```
- Thread 1 assigned to: Vector search optimization
- Thread 2 assigned to: Cache invalidation
- Thread 1 blocker: Waiting for Thread 2 commit
- Thread 3 checkpoint: ✅ Feature A complete
```

**File Structure:**

```markdown
# Execution State — April 19, 2026

## Thread Assignments

| Thread | Assigned To | Task | Status | Risk |
|--------|-------------|------|--------|------|
| Thread 1 | Copilot | Vector optimization | In Progress | Module X conflict |
| Thread 2 | Copilot | Cache refactor | Blocked | Waiting Thread 1 |

## Checkpoints (Thread 1)
- ✅ 09:00 - Profiling complete
- ✅ 11:30 - Root cause identified
- 🔄 14:00 - Implementation in progress

## Blockers & Dependencies
- Thread 1 → Thread 2: (Thread 2 waiting for Thread 1 commit)
- Thread 2 → Database: (waiting for connection pool fix)

## Risk Assessment
- HIGH: Cache memory pressure (active monitoring)
- MEDIUM: Module X compatibility (testing ongoing)
```

**When to update:**
- Checkpoint (at least daily)
- Status change (in-progress → blocked)
- Discovery of blocker
- Completion of task

---

## 🤖 Agent Workflow: Complete Example

### Scenario: You Discover a Performance Problem

**Step 1: SESSION START (2 minutes)**

```bash
# Read current state
cat .ai/context-aware/task-progress/_current.md

# Check existing issues  
cat .ai/context-aware/analysis/_current-issues.md

# Understand thread state
cat EXECUTION/spec/custom/[PROJECT]/development/execution-state/_current.md
```

**Step 2: YOU WORK (variable time)**

```
1. Profile code
2. Find: Vector search takes 500ms (goal: 200ms)
3. Root cause: N+1 queries in embedding loop
4. Suggested fix: Batch embeddings
```

**Step 3: YOU DOCUMENT (15 minutes)**

```bash
# Create analysis file
cat > .ai/context-aware/analysis/vector-search-bottleneck.md << 'EOF'
# Vector Search Bottleneck

**Severity:** 🔴 HIGH  
**Impact:** Campaign search takes 500ms (goal: 200ms)  
**Root Cause:** N+1 queries in embedding loop

## Investigation
[details...]

## Suggested Fix
- Implement batch_search() method
- Expected improvement: 500ms → 50ms (10x)
EOF

# Update task progress
cat > .ai/context-aware/task-progress/_current.md << 'EOF'
### Task 5: Optimize Vector Search
- **Status:** In Progress
- **Agent:** You
- **Findings:**
  - [x] Profile: N+1 queries identified
  - [x] Root cause: Loop over campaigns
  - [ ] Implement: Batch loading
  - [ ] Verify: Performance test
- **Related:** See analysis/vector-search-bottleneck.md
EOF

# Update runtime state
cat >> .ai/context-aware/runtime-state/_current.md << 'EOF'
## Task Update — 14:30
- Task 5: Profiling complete, root cause identified
- Next: Implement batch_search() method
- Risk: Database connection pool under load (see analysis)
EOF
```

**Step 4: YOU COMMIT (5 minutes)**

```bash
# Add all context updates
git add .ai/context-aware/

# Commit with clear message
git commit -m "📝 Discover: Vector search N+1 bottleneck (500ms)

- Profiled with cProfile
- Found: ChromaDB.search() called 50x per campaign
- Root cause: Loop over campaigns
- Suggested fix: Batch embeddings
- Expected improvement: 10x (500ms → 50ms)

See .ai/context-aware/analysis/vector-search-bottleneck.md"
```

**Step 5: HANDOFF**

Next agent reads:
- ✅ Task progress (what's done, what's next)
- ✅ Analysis (root cause, suggested fix)
- ✅ Runtime state (immediate blockers, dependencies)

---

## 📂 Folder Structure (Project Template)

```
[PROJECT]/.ai/context-aware/
├── task-progress/
│   ├── _current.md           ← Active tasks (updated per session)
│   ├── completed/
│   │   ├── 2026-04-18.md
│   │   └── 2026-04-17.md
│   └── _INDEX.md             ← Navigation
│
├── analysis/
│   ├── _current-issues.md    ← High-priority issues (auto-generated)
│   ├── vector-search-bottleneck.md
│   ├── cache-pressure-analysis.md
│   ├── _architecture-map.md
│   └── thread-dependency-graph.md
│
├── runtime-state/
│   ├── _current.md           ← Live state (updated per checkpoint)
│   ├── 2026-04-19.md         ← Historical snapshots
│   └── observations.md       ← Long-term patterns
│
└── _INDEX.md                 ← Master navigation
```

---

## ✅ Validation Checklist

**When creating context-aware:**

- [ ] Location correct (`.ai/context-aware/[type]/`)
- [ ] Filename clear and descriptive
- [ ] Dated (include date in filename or header)
- [ ] Authored (who created this? agent name)
- [ ] Linked (references to related docs or tasks)
- [ ] Actionable (next steps are clear)
- [ ] Not opinion (factual, evidence-based)

**Before committing:**

- [ ] No SPECIALIZATIONS here (use EXECUTION/spec/custom/ instead)
- [ ] No framework docs (stay project-local)
- [ ] No secrets (API keys, passwords)
- [ ] Related task is updated
- [ ] Runtime state reflects changes

---

## 🔄 Lifecycle: From Context-Aware to Specialization

**Stage 1: Discovery (Context-Aware)**
```
Agent finds: "Vector search N+1 bottleneck"
Location: .ai/context-aware/analysis/
Duration: 1 task
Audience: Next agent
```

**Stage 2: Validation (Team Discussion)**
```
Team confirms: "Yes, this is a real pattern"
Decision: "Should be applied project-wide"
Owner: Team lead reviews
```

**Stage 3: Specialization (Framework)**
```
Promoted to: EXECUTION/spec/custom/[PROJECT]/SPECIALIZATIONS/
Content: "Always use batch_search() for vector queries"
Duration: Project lifetime
Audience: All future agents
```

---

## 🚫 Anti-Patterns: What NOT To Do

### ❌ Anti-Pattern 1: Context-Aware as Specialization

```markdown
# ❌ WRONG

File: .ai/context-aware/analysis/batch-search-strategy.md

Content: "We should always use batch_search() because..."
```

**Why wrong:**
- Duration: Permanent (belongs in SPECIALIZATIONS)
- Scope: Affects all future work (belongs in SPECIALIZATIONS)
- Owner: Decided by team (not just agent)

**✅ Correct approach:**
```
1. Create: .ai/context-aware/analysis/vector-search-bottleneck.md (discovery)
2. Discuss: Team meeting (validation)
3. Move: EXECUTION/spec/custom/[PROJECT]/SPECIALIZATIONS/ (decision)
```

---

### ❌ Anti-Pattern 2: Framework Docs in Context

```markdown
# ❌ WRONG

File: .ai/context-aware/analysis/how-to-use-ports-pattern.md

Content: "All infrastructure must use ports because..."
```

**Why wrong:**
- This is framework knowledge (belongs in CANONICAL)
- Shouldn't vary by project
- Belongs in CANONICAL/specifications/architecture.md

**✅ Correct approach:**
```
Read: EXECUTION/spec/CANONICAL/decisions/ADR-003-ports-adapters-pattern.md
(Don't recreate framework knowledge in project context)
```

---

### ❌ Anti-Pattern 3: Private Speculation

```markdown
# ❌ WRONG

File: .ai/context-aware/analysis/maybe-api-problem.md

Content: "I think the API might be slow... not sure though"
```

**Why wrong:**
- Not factual (opinion)
- Not actionable (vague)
- Wastes next agent's time (ambiguous)

**✅ Correct approach:**
```markdown
# ✅ API Latency Analysis

**Finding:** API responses average 250ms, goal 50ms
**Evidence:** Profiled with APM tool
**Root cause:** N+1 database queries in endpoint
**Suggested fix:** Implement query batching

(Clear, factual, actionable)
```

---

## 📊 Reference: Decision Matrix

**When do I use each tier?**

| Tier | Question | Example | Location |
|------|----------|---------|----------|
| **CANONICAL** | "Do rules/ALL projects apply?" | "Always use ports for infrastructure" | EXECUTION/spec/CANONICAL/ |
| **SPECIALIZATION** | "Does this project ALWAYS apply?" | "Always use ThreadLocal for state" | EXECUTION/spec/custom/[PROJECT]/SPECIALIZATIONS/ |
| **CONTEXT-AWARE** | "Did I discover this TODAY?" | "Vector search has N+1 bottleneck" | .ai/context-aware/ |
| **EXECUTION-STATE** | "WHO is doing WHAT right NOW?" | "Thread 1: Vector optimization" | EXECUTION/spec/custom/[PROJECT]/development/execution-state/ |

---

## 🎓 Quick Reference: When to Document

| Event | What to Create | Where | Who |
|-------|---|---|----|
| Discover issue | Issue doc | `.ai/context-aware/analysis/` | Agent |
| Start task | Task entry | `.ai/context-aware/task-progress/` | Agent |
| Finish task | Checkpoint | `.ai/context-aware/task-progress/` | Agent |
| Review architecture | Architecture map | `.ai/context-aware/analysis/` | Agent |
| Find blocker | Blocker entry | `.ai/context-aware/runtime-state/` | Agent |
| Decide pattern | Specialization | `EXECUTION/spec/custom/[PROJECT]/SPECIALIZATIONS/` | Team |

---

## ✨ Success Criteria

**A well-implemented context-aware system has:**

- ✅ Clear task tracking (who did what, what's next)
- ✅ Documented discoveries (issues, root causes, fixes)
- ✅ Live state visible (blockers, dependencies, risks)
- ✅ Handoff ready (next agent knows full context)
- ✅ No surprises (findings are specific, dated, authored)
- ✅ Separation maintained (context ≠ specializations ≠ framework)

---

## 📚 Related Documents

- **CANONICAL/specifications/architecture.md** — Framework structure
- **guides/onboarding/AGENT_HARNESS.md** — Agent workflow
- **custom/[PROJECT]/SPECIALIZATIONS/** — Project-specific rules
- **custom/[PROJECT]/development/execution-state/** — Thread state
- **context/runtime-state/analysis/** — Session analysis (framework reference)

---

**Authority:** SPEC v2.1 Canonical  
**Enforcement:** Required for all agents  
**Review:** Quarterly  
**Status:** Production-Ready  
