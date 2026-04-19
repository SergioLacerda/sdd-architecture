# 🔄 RUNTIME STATE — Mutável

**These files describe the CURRENT STATE of the system.**

Change them as the system evolves. Update frequently when working.

---

## 📊 Mutable Runtime State Layer

| File | Purpose | Change Frequency |
|------|---------|------------------|
| [specs/runtime/execution_state.md](./specs/runtime/execution_state.md) | What's happening NOW (checkpoints, active threads, next steps) | Every checkpoint (hourly/daily) |
| [specs/runtime/threads/](./specs/runtime/threads/) | Active work threads, progress tracking | Real-time during work |
| [specs/runtime/checkpoints/](./specs/runtime/checkpoints/) | Completed work history, decisions made | After each checkpoint |
| [current-system-state/known_issues.md](./current-system-state/known_issues.md) | Bugs found, edge cases discovered | Every bug discovery |
| [current-system-state/rag_pipeline.md](./current-system-state/rag_pipeline.md) | Real RAG behavior, limitations found | As limitations discovered |
| [current-system-state/services.md](./current-system-state/services.md) | Actual service flow, performance issues | As system behavior changes |
| [current-system-state/contracts.md](./current-system-state/contracts.md) | Port guarantees, what actually works | When port behavior changes |
| [current-system-state/data_models.md](./current-system-state/data_models.md) | DTO definitions, storage format | When models evolve |
| [current-system-state/storage_limitations.md](./current-system-state/storage_limitations.md) | Real constraints, capacity limits | When hitting new limits |
| [current-system-state/threading_concurrency.md](./current-system-state/threading_concurrency.md) | Actual concurrency behavior, race conditions | When new races found |
| [current-system-state/scaling_constraints.md](./current-system-state/scaling_constraints.md) | Bottlenecks discovered, performance issues | When scaling bottleneck found |

---

## � DOCUMENT CLASSIFICATION MATRIX

**How to tell what type of document you're reading:**

| File | Type | Is Authority? | Updates | When to Use |
|------|------|---------------|---------|-------------|
| **ia-rules.md** | Governance | ✅ YES - Mandatory | Rarely | Before ANY work |
| **constitution.md** | Governance | ✅ YES - Principles | Rarely | When designing |
| **architecture.md** | Governance | ✅ YES - Design | Rarely | For patterns |
| **conventions.md** | Governance | ✅ YES - Standards | Rarely | For code style |
| **definition_of_done.md** | Governance | ✅ YES - Quality | Rarely | Before merge |
| **feature-checklist.md** | Governance | ✅ YES - Process | Rarely | Implementing feature |
| **testing.md** | Governance | ✅ YES - Validation | Rarely | Writing tests |
| **contracts.md** | Governance | ✅ YES - Port Spec | Rarely | Using ports |
| **execution_state.md** | State | 🟡 TRACKING | Every checkpoint | Planning work |
| **known_issues.md** | AS-IS Reality | 🟡 CURRENT | Every bug found | Bug fixes |
| **rag_pipeline.md** | AS-IS Reality | 🟡 CURRENT | Limitations found | RAG work |
| **services.md** | AS-IS Reality | 🟡 CURRENT | Behavior changes | Service work |
| **data_models.md** | AS-IS Reality | 🟡 CURRENT | Model changes | DTO work |
| **storage_limitations.md** | AS-IS Reality | 🟡 CURRENT | Scale changes | Performance work |
| **threading_concurrency.md** | AS-IS Reality | 🟡 CURRENT | Race found | Threading work |
| **scaling_constraints.md** | AS-IS Reality | 🟡 CURRENT | Bottleneck found | Scaling work |

**Legend**:
- **✅ YES** = Authority document. These define the ideal. Don't change them.
- **🟡 TRACKING** = Current state tracker. Documents what's happening.
- **🟡 CURRENT** = Reality documents. Describe actual system behavior.

---

## ⚠️ UNDERSTANDING GAPS (IMPORTANT!)

**Gaps between Governance and AS-IS are NORMAL and EXPECTED:**

```
GOVERNANCE documents say:           AS-IS Reality documents show:
"All I/O must be async"             "Service X has 2 sync calls"
  ↓                                   ↓
This is NOT a governance bug!       This IS a limitation to fix!
  
Gap = Technical debt, not an error in the rules.

What to do:
  1. Document the gap in AS-IS docs (known_issues.md)
  2. Don't change the governance rule
  3. Future work: Fix to match governance
  4. If governance is truly wrong, create ADR
```

**DO NOT assume governance is wrong just because reality differs.**

Governance documents (ia-rules.md, architecture.md, etc.) represent:
- What's RIGHT
- What works best
- What we aspire to
- What prevents problems

AS-IS documents (known_issues.md, rag_pipeline.md, etc.) represent:
- What exists NOW
- Gaps from ideal
- Technical debt
- What needs fixing

---

## �🔄 When to Update Runtime State

### execution_state.md (Checkpoint)
**Update after every significant checkpoint:**
```
After you finish important work:
  1. What did you implement?
  2. What's still pending?
  3. Any open questions?
  4. Any risks discovered?
  5. Next actions for next agent?
```

### known_issues.md (Bug Discovery)
**Update when you find a bug:**
```
When you discover a bug:
  1. Title: What's broken?
  2. Severity: 🔴 CRITICAL / 🟡 MEDIUM / 🟢 LOW
  3. Description: How to reproduce?
  4. Workaround: What's the current mitigation?
  5. Fix: What would solve it?
```

### current-system-state/*.md (Behavior Discovery)
**Update when discovering system behavior:**
```
When learning about the system:
  1. What did you discover?
  2. How is it different from spec?
  3. Why does it work this way?
  4. What are the implications?
```

### specs/runtime/threads/
**Update during multi-thread work:**
```
If doing PATH D (multi-thread work):
  1. Create: /docs/ia/specs/runtime/threads/THREAD_NAME.md
  2. Update: Your thread's progress
  3. Update: Next actions for your thread
  4. Mark: BLOCKED / IN_PROGRESS / COMPLETE
```

---

## 📈 Example: From Discovery to Documentation

### Day 1: Discovery
```
Working on cache feature...
Found: ChromaDB IVF sometimes returns wrong results
Workaround: Added manual re-ranking
→ Update known_issues.md (🟡 MEDIUM severity)
```

### Day 2: More Context
```
Debugging revealed: IVF not initialized on first call
Found: 10-50ms latency spike on first search
→ Update current-system-state/rag_pipeline.md (limitation)
→ Update scaling_constraints.md (new bottleneck)
```

### Day 3: Checkpoint
```
Completed: Cache layer + workaround
Ready: Next agent can remove workaround after IVF fix
→ Update execution_state.md (checkpoint)
```

---

## 🚨 CRITICAL: Gaps Between Governance & Reality

**The gap is normal.**

- **Governance** says: "System should use ports consistently"
- **Reality** says: "Service X bypasses port in 3 places"

**What to do:**
1. ✅ Document in [current-system-state/](./current-system-state/) (not a governance violation)
2. ✅ Create issue/checkpoint (flag for future fix)
3. ❌ DO NOT change governance.md (the ideal is still valid)
4. ✅ Work with what IS, not what SHOULD BE

**Why?**
- Governance stays clean (ideals don't change just because reality is messy)
- Reality layer documents actual constraints
- Future work can fix reality to match governance

---

## 📊 Reality Check: What "Mutable" Means

```
✅ CAN CHANGE:
  - "System has 11 known bugs"
  - "Cache hit ratio is 65%"
  - "Port X sometimes violates contract"
  - "Feature Y discovered limitation"
  - "Thread Z is blocked on issue #42"
  - "Current bottleneck is storage layer"

❌ SHOULD NOT CHANGE (see GOVERNANCE_RULES.md):
  - "Ports must be used for all I/O"
  - "All implementations must use 8-layer"
  - "No blocking operations allowed"
  - "Errors must propagate, not swallow"
  - "Thread isolation is mandatory"
```

---

## 🔗 Related Files

**For Governance** (immutable, stable):
→ See [GOVERNANCE_RULES.md](./GOVERNANCE_RULES.md)

**For New Agents** (starting session):
→ Read [guides/FIRST_SESSION_SETUP.md](./guides/FIRST_SESSION_SETUP.md)

**For Implementation** (doing work):
→ Check execution_state.md first, then load relevant current-system-state/ files

---

## 🎓 For New Agents

When starting a session:
1. ✅ Read [GOVERNANCE_RULES.md](./GOVERNANCE_RULES.md) (what's stable)
2. ✅ Read [specs/runtime/execution_state.md](./specs/runtime/execution_state.md) (what's active)
3. ✅ Check [current-system-state/_INDEX.md](./current-system-state/_INDEX.md) (system reality)

**Key insight**: If governance says "X" but reality shows "Y", you're seeing a gap.
- Document the gap in current-system-state/
- Don't assume governance is wrong
- Future work can close the gap

---

## 📝 Quick Update Checklist

Before finishing a session, consider:

```
[ ] Did I discover bugs? → Update known_issues.md
[ ] Did I hit a limitation? → Update current-system-state/relevant-file.md
[ ] Did I complete work? → Update execution_state.md
[ ] Am I multi-thread? → Update /docs/ia/specs/runtime/threads/MY_THREAD.md
[ ] Did reality differ from spec? → Document gap in current-system-state/
[ ] Will next agent need context? → Flag in execution_state.md "Next Actions"
```

Done? 🎯 You've kept the system self-aware and learning.
