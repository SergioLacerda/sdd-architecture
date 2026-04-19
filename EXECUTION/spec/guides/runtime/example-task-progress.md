# Example: Task Progress Workflow

**Purpose:** Show what good task tracking looks like  
**This is an example.** Use this as a template for your projects.

---

## Example: From Start to Finish

### Day 1: Morning — Agent A Starts

```markdown
# Task Progress — 2026-04-22

## Active Tasks

### Task 1: Optimize Vector Search Performance
- **Status:** In Progress 🔵
- **Agent:** Copilot Agent (assigned 2026-04-22)
- **Started:** 2026-04-22 09:00
- **Expected Completion:** 2026-04-22 18:00
- **Story Points:** 5

#### Subtasks
- [ ] Profile current implementation (find bottleneck)
- [ ] Identify root cause (N+1 queries?)
- [ ] Design fix (batch queries?)
- [ ] Implement fix
- [ ] Write tests
- [ ] Performance validation (target: 100ms)

#### Blockers
- None currently

#### Notes
- Related issue: See `analysis/_current-issues.md` #Issue1
- Prerequisite: Must understand ChromaDB API
```

---

### Day 1: Afternoon — Agent A Makes Progress

Agent updates the file as they work:

```markdown
## Active Tasks

### Task 1: Optimize Vector Search Performance
- **Status:** In Progress 🔵
- **Agent:** Copilot Agent
- **Started:** 2026-04-22 09:00
- **Expected Completion:** 2026-04-22 18:00

#### Subtasks
- [x] Profile current implementation ← DONE (found N+1 at 14:30)
- [x] Identify root cause ← DONE (loop + search calls)
- [ ] Design fix (batch queries?)
- [ ] Implement fix
- [ ] Write tests
- [ ] Performance validation

#### Findings
- **Current performance:** 500ms per search (50 campaigns)
- **Root cause:** Loop: for campaign in campaigns: search(campaign)
- **Fix candidate:** Implement batch_search(campaigns, query)
- **Expected improvement:** 500ms → 50ms (10x)

#### Blockers
- None (proceeding with implementation)

#### Progress Log
- 09:00: Started profiling
- 11:00: Identified N+1 query pattern
- 14:30: Confirmed with cProfile
- 15:00: Designing fix
```

Then Agent A creates a detailed analysis file:

```bash
# Create: analysis/vector-search-optimization.md
cat > .ai/context-aware/analysis/vector-search-optimization.md << 'EOF'
# Vector Search Optimization

**Task:** Task 1 in task-progress/_current.md  
**Status:** In Progress

## Problem
Vector search takes 500ms per query with 50 campaigns.

## Root Cause Analysis
```python
# CURRENT IMPLEMENTATION (SLOW)
def search_campaigns(campaigns, query):
    results = []
    for campaign_id in campaigns:  # 50 iterations
        result = chroma.search(campaign_id, query)  # 50 DB calls!
        results.append(result)
    return results
```

## Proposed Solution
```python
# BETTER IMPLEMENTATION (FAST)
def search_campaigns(campaigns, query):
    # Single database call for all campaigns
    return chroma.batch_search(campaign_ids, query)
```

## Expected Outcome
- Current: 500ms
- Target: 50ms (10x improvement)
- Status: Implementing...
EOF

git add .ai/context-aware/
git commit -m "📝 Document vector search optimization (N+1 query pattern identified)"
```

---

### Day 1: Evening — Agent A Completes

Agent A finishes the task:

```markdown
## Active Tasks

### Task 1: Optimize Vector Search Performance
- **Status:** ✅ COMPLETE
- **Agent:** Copilot Agent
- **Started:** 2026-04-22 09:00
- **Completed:** 2026-04-22 17:00

#### Subtasks
- [x] Profile current implementation
- [x] Identify root cause
- [x] Design fix
- [x] Implement fix
- [x] Write tests (95% coverage)
- [x] Performance validation ✅ PASSED

#### Deliverables
1. **Implementation**
   - Added `batch_search()` method to ChromaDB adapter
   - Updated `search_campaigns()` to use batch
   - All tests passing

2. **Performance**
   - Before: 500ms per search
   - After: 120ms per search
   - Improvement: 76% faster ✅

3. **Tests**
   - 12 new tests added
   - Coverage: 95%
   - All passing ✅

4. **Documentation**
   - Updated ChromaDB port with batch method
   - Added docstring explaining batch behavior
   - Related issue closed

#### Related Files
- **Implementation:** src/infrastructure/storage/chroma_adapter.py
- **Tests:** tests/unit/storage/test_chroma_adapter.py
- **Analysis:** See analysis/vector-search-optimization.md
- **Issue:** Closes analysis/_current-issues.md #Issue1

#### Commit
```
✅ Task complete: Vector search optimization (500ms→120ms, 76% improvement)

- Implemented batch_search() for ChromaDB adapter
- 12 new tests, 95% coverage
- Performance: 500ms → 120ms per search
- Related: Closes #Issue1 in known issues
```

---

### Next Day: Agent B Picks It Up

Agent B reads the task progress:

```markdown
## Recently Completed Tasks

### Task 1: Optimize Vector Search ← SEE THIS
- **Status:** ✅ COMPLETE (2026-04-22)
- **Performance gain:** 500ms → 120ms (76% improvement)
- **Review status:** Ready for review
- **Implementation:** src/infrastructure/storage/chroma_adapter.py
```

Agent B checks what was done:

```bash
# Agent B reads the analysis
cat .ai/context-aware/analysis/vector-search-optimization.md
# Understands: The fix, why it works, the improvement

# Agent B checks if it's ready
git log --oneline | head -5
# Sees: "✅ Task complete: Vector search optimization"

# Agent B reviews the code
git show HEAD:src/infrastructure/storage/chroma_adapter.py | head -50

# Agent B is ready to review or move to next task
# NO DUPLICATE WORK! ✅
```

---

## Key Takeaways

### What Made This Work

1. ✅ **Clear Status Updates** — Agent A updated task progress as they worked
2. ✅ **Detailed Analysis** — Agent A created analysis file with findings
3. ✅ **Specific Numbers** — Not "slow", but "500ms → 120ms"
4. ✅ **Clear Deliverables** — Tests, implementation, performance numbers
5. ✅ **Related Files** — Links to code, analysis, issues
6. ✅ **Commit Messages** — Clear message indicating completion

### How Agent B Benefited

1. ✅ **Knows what was done** — Read task-progress
2. ✅ **Understands why** — Read analysis file
3. ✅ **Sees the impact** — Performance numbers in task
4. ✅ **Can review quickly** — Implementation is referenced
5. ✅ **No duplicat investigation** — All findings already documented
6. ✅ **Can move to next task** — Smooth handoff

---

## Template: Copy This Structure

When starting a task, create this structure:

```markdown
### Task N: [Name]
- **Status:** In Progress 🔵
- **Agent:** [Your Name]
- **Started:** [Date/Time]
- **Expected Completion:** [Date/Time]

#### Subtasks
- [ ] Subtask 1
- [ ] Subtask 2
- [ ] Subtask 3

#### Blockers
- [None / Description]

#### Progress
- [What you've done so far]

#### Related
- **Analysis:** [Link to analysis file]
- **Issues:** [Link to related issues]
```

When completing, update to:

```markdown
### Task N: [Name]
- **Status:** ✅ COMPLETE
- **Completed:** [Date/Time]

#### Deliverables
1. [What you delivered]
2. [Tests added]
3. [Performance/quality metrics]

#### Commit
[Your commit message]
```

---

## Next Steps

1. **In your project:** Copy `.ai/context-aware/task-progress/_current.md`
2. **Create your tasks** using this template
3. **Update as you work** (5 min per task)
4. **Commit when done** with clear message
5. **Next agent reads** and continues efficiently

**Result:** Smooth handoffs, no duplicate work! 🎯
