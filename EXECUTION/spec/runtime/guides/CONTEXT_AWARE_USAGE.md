# 🎯 CONTEXT_AWARE_USAGE — Complete Agent Guide

**For:** AI Agents working on SPEC projects  
**Time:** 5 minutes to read, applies to all your work  
**Goal:** Understand how to create and use dynamic context  

---

## 🚀 Quick Start (2 minutes)

### When You Start Work

```bash
# Step 1: Navigate to project
cd your-project/

# Step 2: Check context-aware folder
ls -la .ai/context-aware/

# Step 3: Read task progress
cat .ai/context-aware/task-progress/_current.md

# Step 4: Read issues
cat .ai/context-aware/analysis/_current-issues.md

# Step 5: Check runtime state
cat .ai/context-aware/runtime-state/_current.md

# Step 6: You're caught up! Begin work
```

### When You Finish Work

```bash
# Step 1: Update what you did
vi .ai/context-aware/task-progress/_current.md

# Step 2: Document any issues you found
vi .ai/context-aware/analysis/_current-issues.md

# Step 3: Update runtime state
vi .ai/context-aware/runtime-state/_current.md

# Step 4: Commit your context
git add .ai/context-aware/
git commit -m "📝 Update context: [what changed]"

# Step 5: Next agent will read this!
```

---

## 📋 Detailed Guide: Task Progress

### File: `.ai/context-aware/task-progress/_current.md`

**What:** Track what tasks are active/completed  
**When to edit:** At start and end of each task  
**Format:** Markdown with structured sections  

### Example: Starting a New Task

```markdown
### Task 5: Optimize Vector Search
- **Status:** In Progress
- **Agent:** You (Your Name)
- **Started:** 2026-04-19
- **Expected Completion:** 2026-04-20
- **Subtasks:**
  - [ ] Profile current implementation
  - [ ] Identify N+1 queries
  - [ ] Implement batching
  - [ ] Verify performance improvement
- **Blockers:** None
- **Notes:** See analysis/_current-issues.md #Issue1 for context
```

### Example: Completing a Task

When you're done:

```markdown
### Task 5: Optimize Vector Search
- **Status:** ✅ COMPLETE
- **Agent:** You
- **Started:** 2026-04-19
- **Completed:** 2026-04-20
- **Deliverables:**
  - ✅ Profiled: N+1 queries identified
  - ✅ Implemented: Batch embedding loading
  - ✅ Verified: 500ms → 120ms (76% improvement)
  - ✅ Tests: All passing (98% coverage)
- **Notes:** Fixed issue #Issue1
- **Related:** See analysis/vector-search-optimization.md for details
```

Then move it to `completed/2026-04-20.md`:

```bash
# Archive completed task
mv .ai/context-aware/task-progress/_current.md \
   .ai/context-aware/task-progress/completed/2026-04-20.md

# Create new _current.md with updated task list
vi .ai/context-aware/task-progress/_current.md
```

---

## 📊 Detailed Guide: Analysis

### Folder: `.ai/context-aware/analysis/`

**What:** Document discoveries, issues, insights  
**When to create:** Whenever you learn something important  
**Format:** Markdown with structure  

### Types of Analysis Files

#### 1. Issue Documentation

**File:** `vector-search-bottleneck.md`  
**When:** You discover a performance problem  
**Who reads:** Next agent (to prioritize fixes)

```markdown
# Vector Search Bottleneck

**Severity:** 🔴 HIGH  
**Impact:** Campaign search takes 500ms (goal: 100ms)  
**Root Cause:** N+1 queries in embedding loop

## Investigation

### What I did
1. Profiled with cProfile
2. Found: ChromaDB.search() called 50x per campaign
3. Root cause: Loop over campaigns, search each one

### What I found
```python
# CURRENT (SLOW)
for campaign_id in campaign_ids:
    results += chroma.search(campaign_id, query)  # Called 50x!

# BETTER
results = chroma.batch_search(campaign_ids, query)  # Called 1x
```

## Suggested Fix
- Implement batch_search() method
- Call once instead of 50x
- Expected: 500ms → 50ms (10x improvement)

## Next Steps
- [ ] Implement batch_search()
- [ ] Add tests for batch operation
- [ ] Performance test improvement
- [ ] Update ChromaDB abstraction
```

#### 2. Architecture Analysis

**File:** `_architecture-map.md`  
**When:** You review or modify structure  
**Who reads:** Next agent (to understand dependencies)

```markdown
# Architecture Map

[Show module dependencies, layer isolation, thread safety]

## Dependency Graph

```
Application Layer
  ↓ (depends on)
Domain Layer (entities + ports)
  ↓ (depends on)
Infrastructure Layer
```

## Red Flags ✅
- [ ] No circular imports
- [ ] Domain doesn't import infrastructure
- [ ] All infrastructure behind ports
- [ ] Thread safety verified

## Notes
- Thread isolation: Using ThreadLocal for state ✅
- Current bottleneck: Vector search (see vector-search-bottleneck.md)
```

#### 3. Thread Dependency Graph

**File:** `thread-dependency-graph.md`  
**When:** Threads interact or have complex dependencies  
**Who reads:** Next agent (to plan concurrent work)

```markdown
# Thread Dependency Analysis

## Active Threads

| Thread | Task | Depends On | Blocks |
|--------|------|-----------|--------|
| Thread-A | Cache Invalidation | None | Thread-B |
| Thread-B | Memory Optimization | Thread-A | None |
| Thread-C | API Rate Limiting | None | None |

## Critical Path
```
Thread-A (20 min) → Thread-B (15 min)
Total critical path: 35 min

Parallel work:
Thread-C can run anytime (independent)
```

## Implications for Agents
- Don't start Thread-B until Thread-A completes
- Thread-C can be worked on by different agent
- Recommended: Assign Thread-C to another agent
```

---

## 📈 Detailed Guide: Runtime State

### File: `.ai/context-aware/runtime-state/_current.md`

**What:** Track live system state, performance, health  
**When to update:** Daily during development  
**Who reads:** Next agent (to understand current system state)

### What to Track

```markdown
# Current System Health

## Performance Baselines
| Component | Metric | Value | Target | Status |
|-----------|--------|-------|--------|--------|
| Vector Search | Latency | 500ms | <200ms | 🟡 SLOW |
| Campaign Load | Latency | 45ms | <100ms | ✅ OK |
| Memory | Usage | 120MB | <200MB | ✅ OK |
| Thread Pool | Active | 3/10 | 5/10 | ✅ OK |

## Issues Preventing Launch
- [ ] Vector search bottleneck (blocking)
- [ ] Pre-commit hook configuration (blocking)
- [ ] Import test coverage (low priority)

## External Service Status
| Service | Status | Last Check |
|---------|--------|-----------|
| OpenAI API | ✅ UP | 2026-04-19 |
| ChromaDB | ✅ UP | 2026-04-19 |
| Discord | ✅ UP | 2026-04-19 |

## Recommended Next Focus
1. Fix vector search (HIGH priority)
2. Fix pre-commit hook (blocking)
3. Improve import coverage (LOW priority)
```

---

## 🔄 Complete Workflow Example

### Session 1: Agent A discovers and documents

```bash
# 1. Start work
cat .ai/context-aware/task-progress/_current.md  # Understand what's active

# 2. Work on vector search optimization
# ... profiling, testing ...

# 3. Discover: N+1 queries in ChromaDB search loop
# ... analysis ...

# 4. Create analysis document
cat > .ai/context-aware/analysis/vector-search-bottleneck.md << 'EOF'
# Vector Search Bottleneck
**Severity:** 🔴 HIGH  
**Impact:** 500ms per search (goal: 100ms)
...
[detailed findings]
EOF

# 5. Update current issues
vi .ai/context-aware/analysis/_current-issues.md  # Add this issue

# 6. Update task progress
vi .ai/context-aware/task-progress/_current.md  # Mark as "Blocked - waiting for fix"

# 7. Update runtime state
vi .ai/context-aware/runtime-state/_current.md  # Note: Vector search is slow

# 8. Commit
git add .ai/context-aware/
git commit -m "📝 Document vector search bottleneck (500ms, N+1 queries)"
```

### Session 2: Agent B applies the fix

```bash
# 1. Start work
cat .ai/context-aware/task-progress/_current.md
# Sees: "Task: Optimize Vector Search - Blocked - waiting for fix"

# 2. Read the analysis
cat .ai/context-aware/analysis/vector-search-bottleneck.md
# Learns: N+1 queries, suggested fix is batch_search()

# 3. No duplicate investigation!
# Goes directly to implementing batch_search()

# 4. Apply fix
# ... implement batch_search() ...

# 5. Test improvement
# Result: 500ms → 120ms (76% improvement!)

# 6. Update task progress
vi .ai/context-aware/task-progress/_current.md
# Mark as: "✅ COMPLETE - Vector search optimized to 120ms"

# 7. Update issues
vi .ai/context-aware/analysis/_current-issues.md
# Mark issue as RESOLVED

# 8. Update runtime state
vi .ai/context-aware/runtime-state/_current.md
# Update performance baseline: "Vector Search: 120ms ✅ OK"

# 9. Commit
git add .ai/context-aware/
git commit -m "✅ Fix vector search: implemented batch_search (500ms→120ms)"
```

### Session 3: Agent C starts next task

```bash
# 1. Start work
cat .ai/context-aware/task-progress/_current.md
# Sees: "Vector search task is complete, next: memory optimization"

# 2. Check what was learned
cat .ai/context-aware/analysis/_current-issues.md
# No mention of vector search anymore (it's fixed!)
# Sees: "Memory Leak - Investigation needed"

# 3. Check runtime state
cat .ai/context-aware/runtime-state/_current.md
# "Memory usage: stable at 120MB (was growing, now fixed?)"

# 4. No context switching, clean handoff!
# Proceeds with memory optimization task
```

**Result:** 3 agents, 0 duplicate work, complete context continuity! 🎯

---

## ✅ Checklist: Before You Commit

**Use this before every commit:**

```markdown
## Pre-Commit Checklist for Context-Aware

- [ ] Task progress updated
  - [ ] Active tasks marked with status
  - [ ] Completed tasks moved to completed/
  - [ ] Next task is clear

- [ ] Analysis updated (if applicable)
  - [ ] Any issues documented
  - [ ] Any discoveries recorded
  - [ ] Architecture changes noted

- [ ] Runtime state updated
  - [ ] Performance metrics current
  - [ ] Known issues list updated
  - [ ] Blockers/dependencies noted

- [ ] Commit message is clear
  - [ ] Format: "📝 Update context: [what changed]"
  - [ ] Or: "✅ Task complete: [task name]"
  - [ ] Or: "🐛 Document issue: [issue name]"

- [ ] All files are git-staged
  - [ ] git add .ai/context-aware/
```

---

## 🚨 Common Mistakes (and How to Avoid)

### ❌ Mistake 1: Not Updating Task Progress

```
# Bad: Never update _current.md
git commit -m "Fixed vector search"
# Next agent has no idea what was done

# Good: Update before committing
cat > .ai/context-aware/task-progress/_current.md << 'EOF'
### Task: Optimize Vector Search
- **Status:** ✅ COMPLETE
- Improved from 500ms to 120ms
EOF
git add .ai/context-aware/ && git commit -m "✅ Task complete: Vector search optimization"
```

### ❌ Mistake 2: Not Documenting Issues

```
# Bad: Find a problem, don't record it
# Next agent has to re-investigate

# Good: Document immediately
cat > .ai/context-aware/analysis/new-issue.md << 'EOF'
# Memory Leak in Session Handler
- Growing 50MB/hour under load
- Suspect: Not clearing old sessions
EOF
git add .ai/context-aware/analysis/ && git commit -m "🐛 Document issue: Memory leak in session handler"
```

### ❌ Mistake 3: Stale Runtime State

```
# Bad: Performance metrics haven't been updated in days
# Next agent doesn't know current state

# Good: Update regularly
vi .ai/context-aware/runtime-state/_current.md
# Change: "Vector Search: 500ms" → "Vector Search: 120ms ✅"
git add .ai/context-aware/ && git commit -m "📈 Update runtime metrics"
```

---

## 🎓 Key Principles

### Principle 1: Context-Aware is for Agents

These files are **for AI agents first, humans second**.

- Use clear structure (Markdown headings, lists)
- Use emoji markers for quick scanning (✅, 🔴, 🟡, 🟢)
- Avoid prose, use structured data
- Link to other files explicitly

### Principle 2: Write for the Next Agent

Ask yourself: "If a different agent reads this tomorrow, will they understand?"

- Be specific (not "bug exists", but "vector search returns 500ms")
- Provide root cause (not just symptoms)
- Suggest fixes (not just problems)
- Link related findings

### Principle 3: Keep It Fresh

Stale context is worse than no context.

- Delete resolved issues from `_current-issues.md`
- Archive old tasks to `completed/`
- Update runtime metrics weekly
- Review monthly for accuracy

---

## 📚 Related Files

- `README.md` (this folder) — Overview of context-aware
- `example-task-progress.md` — Good task tracking
- `example-analysis.md` — Good analysis documentation
- `example-runtime-state.md` — Good state tracking
- `.ai/context-aware/README.md` (in projects) — Project-specific usage

---

## 🚀 Ready to Use Context-Aware?

You now know:
- ✅ When to create/update context-aware files
- ✅ What to document and why
- ✅ How to handoff work between agents
- ✅ How to avoid duplicate investigation
- ✅ How to keep projects "alive" with dynamic context

**Start using context-aware in your next work session!**

Questions? Check the project's `.ai/context-aware/README.md` for project-specific guidance.
