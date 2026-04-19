# SPEC: Canonical vs Reality vs Development Separation

**Status:** 🎯 WORLD-CLASS ENGINEERING PATTERN | **Effective:** April 2026

---

## ⚠️ PROBLEM IDENTIFIED

### Current Coupling Issues

**Issue 1: "Runtime" is ambiguous**
```
Current state:
├─ GOVERNANCE_RULES.md (says "rules are immutable")
├─ RUNTIME_STATE.md (says "runtime is mutable" but what is runtime?)
└─ Question: Is "runtime" = execution_state.md? or current-system-state/? or both?

Result: ❌ Confusion about "what's the truth?"
```

**Issue 2: Three concepts mixed together**
```
RUNTIME_STATE.md conflates:
├─ Authority questions (what's the rule?)
├─ Reality questions (what actually exists?)
└─ Development questions (what are we doing?)

Result: ❌ Ambiguity when reading a file: "Is this a rule or observation?"
```

**Issue 3: Authority is unclear**
```
If code violates known_issues.md:
├─ Is known_issues.md authoritative? (what we know)
├─ Or is architecture.md authoritative? (what should be)
├─ Which one matters for code review?

Result: ❌ Conflicting review standards
```

**Issue 4: No clear separation of concerns**
```
Developer asks: "Should I follow architecture.md or respect known_issues.md?"

Answer varies:
├─ For NEW code: Follow architecture.md ✅
├─ For BUGFIX: Respect known_issues.md ✅
├─ But docs don't say which is which!

Result: ❌ Agents make inconsistent decisions
```

---

## 🎯 PROPOSED: Three-Layer Architecture

### Layer 1: CANONICAL (Immutable, Authority)
**What's RIGHT and WHY**

```
Purpose: Define the ideal, the rules, the decisions
Authority: YES — These are the source of truth
Updates: RARE (only ADRs, breaching changes)
Changed by: Architecture review board, high-bar decisions
```

**Files:**
```
/docs/ia/CANONICAL/
├─ rules/
│  ├─ ia-rules.md (16 protocols - NEVER violated)
│  ├─ constitution.md (principles)
│  └─ conventions.md (style)
│
├─ specifications/
│  ├─ architecture.md (design patterns - HOW to build right)
│  ├─ contracts.md (port specifications - WHAT to depend on)
│  ├─ feature-checklist.md (process - HOW to implement features)
│  ├─ testing.md (validation - HOW to validate)
│  └─ definition_of_done.md (quality - WHEN to merge)
│
├─ decisions/
│  ├─ ADR-001.md (WHY architecture)
│  ├─ ADR-002.md (WHY async)
│  └─ ... (6 total)
│
└─ README.md (authority guide)
```

**Authority Level: ✅ ABSOLUTE**
- Code must conform or have written exception
- If code violates canonical, code is WRONG
- Exception: Technical debt documented in REALITY layer

**Update Pattern:**
```
Rule change request:
  1. Document WHY in checkpoint
  2. Create ADR if architectural
  3. Flag as BREAKING
  4. All agents must re-read
  5. Update only after consensus
```

---

### Layer 2: REALITY (Mutable, Observed)
**What ACTUALLY EXISTS and WHAT WE'VE LEARNED**

```
Purpose: Document actual system behavior, gaps, limitations
Authority: NO — These are observations, not rules
Updates: FREQUENT (every bug discovery, performance finding)
Changed by: Developers when discovering reality
```

**Files:**
```
/docs/ia/REALITY/
├─ current-system-state/
│  ├─ rag_pipeline.md (how RAG actually works - real components, real flows)
│  ├─ services.md (actual service behavior - not ideal, real)
│  ├─ contracts.md (what ports actually guarantee NOW - may lag spec)
│  ├─ data_models.md (actual DTOs, schemas)
│  └─ performance_baseline.md (actual perf, metrics)
│
├─ limitations/
│  ├─ known_issues.md (11 bugs, workarounds, race conditions)
│  ├─ storage_limitations.md (actual constraints, hitting limits)
│  ├─ threading_concurrency.md (actual race conditions found)
│  ├─ scaling_constraints.md (actual bottlenecks)
│  └─ technical_debt.md (what's broken vs spec)
│
├─ observations/
│  ├─ architecture_gaps.md (where reality != spec, why it matters)
│  ├─ performance_findings.md (what's slow, why)
│  └─ usability_issues.md (what breaks in practice)
│
└─ README.md (reality guide)
```

**Authority Level: 🟡 CONTEXT (Not rules, but important context)**
- Code can temporarily violate canonical IF documented here
- But temp becomes permanent debt if not fixed
- Reality informs prioritization
- Known issues MUST be tested and documented

**Update Pattern:**
```
Bug discovery:
  1. Add to known_issues.md (immediately)
  2. Link to failing test
  3. Document workaround if exists
  4. Flag severity (P1/P2/P3)
  5. Note: Canonical still applies (bug is still a bug)
```

---

### Layer 3: DEVELOPMENT (Mutable, Execution & Planning)
**What We're DOING RIGHT NOW and WHAT'S NEXT**

```
Purpose: Track current work, decisions made, next steps
Authority: NO — These are working notes, ephemeral
Updates: REAL-TIME during active work
Changed by: Agents executing work, updating progress
```

**Files:**
```
/docs/ia/DEVELOPMENT/
├─ execution-state/
│  ├─ _current.md (what's being worked on NOW)
│  ├─ threads/ (parallel work streams)
│  │  ├─ thread-1-campaign-isolation.md
│  │  ├─ thread-2-memory-hierarchy.md
│  │  └─ ...
│  └─ next-steps.md (what's planned)
│
├─ checkpoints/
│  ├─ TEMPLATE.md (checkpoint format)
│  ├─ checkpoint-001-foundation.md (completed work)
│  ├─ checkpoint-002-bootstrap.md
│  └─ ...
│
├─ decisions-in-progress/
│  ├─ decision-proposal-1.md (being considered)
│  ├─ decision-rationale-2.md (reasoning)
│  └─ ...
│
├─ blockers-and-risks/
│  ├─ current-blockers.md (what's stopping us)
│  ├─ risks.md (what could go wrong)
│  └─ assumptions.md (what we're assuming)
│
└─ README.md (development guide)
```

**Authority Level: 🟢 NONE (Ephemeral, working state)**
- These are notes, not rules
- Updated frequently, often out of sync
- Don't rely on them for code decisions
- Use CANONICAL for code decisions
- Use DEVELOPMENT to understand what we're working on

**Update Pattern:**
```
Start work:
  1. Create thread or update _current.md
  2. Link to next step
  
During work:
  1. Update blockers-and-risks as discovered
  2. Update _current.md with progress
  
End of session:
  1. Update checkpoints/
  2. Update next-steps.md
  3. Mark completion/pending
```

---

### Layer 4: ARCHIVE (Historical, Reference)
**What we LEARNED and DISCARDED**

```
Purpose: Historical context, previous attempts, deprecated decisions
Authority: NO — These are deprecated, kept for learning
Updates: NEVER (append-only after archival)
Changed by: Archivists when cleaning up completed work
```

**Files:**
```
/docs/ia/ARCHIVE/
├─ deprecated-decisions/
│  ├─ ADR-old-001-rejected-reason.md
│  └─ ...
│
├─ working-sessions/
│  ├─ session-2026-04-15-analysis.md
│  ├─ session-2026-04-16-refactoring.md
│  └─ ...
│
├─ legacy-documentation/
│  ├─ old-architecture-2025.md
│  ├─ old-api-spec-2025.md
│  └─ ...
│
└─ README.md (archive guide)
```

**Authority Level: 🟣 HISTORICAL (Never referenced for code decisions)**
- Why it matters: Helps us understand why we changed
- Why it's kept: Sometimes we need to know "we tried this before"
- When to read: "What was tried before?" / "Why did we change?"
- Never as authority: "This doesn't apply anymore"

**Update Pattern:**
```
Completion of work:
  1. Move session notes to ARCHIVE/
  2. Keep for 1 year minimum
  3. Document lessons learned
  4. Then delete or deep-archive
```

---

## 📊 Decision Matrix: Which Layer?

| Question | Layer | File | Why |
|----------|-------|------|-----|
| "Should I do X?" | CANONICAL | architecture.md, ia-rules.md | Rule-based |
| "Can I break X rule?" | CANONICAL + REALITY | Check both | Rule + context |
| "Is this a workaround?" | REALITY | known_issues.md | Document gap |
| "Does X already exist?" | REALITY | current-system-state/ | Current state |
| "What's the bug?" | REALITY | known_issues.md | Bug reference |
| "What's happening now?" | DEVELOPMENT | execution-state/ | Progress |
| "What's next?" | DEVELOPMENT | next-steps.md | Planning |
| "Why did we change?" | ARCHIVE | deprecated-decisions/ | History |
| "What were we thinking?" | ARCHIVE | working-sessions/ | Session notes |

---

## 🚨 Anti-Patterns to Avoid

### ❌ Anti-Pattern 1: Mixed Authority
```
WRONG:
  "According to execution_state.md, we're doing X, so the code is right"

RIGHT:
  "Execution_state.md says we're doing X, but canonical says Y, so we follow Y"
```

### ❌ Anti-Pattern 2: Using Reality as Rule
```
WRONG:
  "known_issues.md says this happens, so let's accept it"

RIGHT:
  "known_issues.md documents this gap; canonical says it shouldn't happen"
  Action: Fix it OR document as technical debt
```

### ❌ Anti-Pattern 3: Letting Development Become Canonical
```
WRONG:
  "We did it this way in execution_state, so that's the pattern"

RIGHT:
  "We did it this way in development, now let's check if it should be canonical"
```

### ❌ Anti-Pattern 4: Canonical Becomes Outdated
```
WRONG:
  "architecture.md is old, ignore it and follow reality"

RIGHT:
  "architecture.md and reality differ; this is technical debt; create ADR for change"
```

---

## ✅ Best Practices

### 1. Canonical is Authority
```
Rule: If canonical says X and code does Y:
  → Code is wrong (unless technical debt is documented)
  → Don't change canonical to match code
```

### 2. Reality Informs Priority
```
Rule: If reality shows bug or limitation:
  → Document in known_issues.md
  → Prioritize fix based on impact
  → Don't change canonical to accept the bug
```

### 3. Development is Ephemeral
```
Rule: When work completes:
  → Move notes to ARCHIVE/
  → Don't keep development files as "reference"
  → Clean up execution-state/ frequently
```

### 4. Changes Flow Upward
```
Observation (REALITY) → Problem (DEVELOPMENT) → Fix (CODE) → Update (CANONICAL)

NOT downward:
  ❌ Canonical → Development → Reality (wrong direction)
```

---

## 🎯 World-Class Engineering Principles

### Principle 1: Separation of Concerns
- **Canonical** = "What's RIGHT" (not polluted by current state)
- **Reality** = "What EXISTS" (not prescriptive)
- **Development** = "What we're DOING" (not decisions)
- **Archive** = "What we LEARNED" (not authority)

### Principle 2: Clear Authority
```
Code decision:
  1. Read CANONICAL (is it allowed?)
  2. Read REALITY (what's the context?)
  3. Make decision based on both
  4. Code according to CANONICAL
  5. If can't match CANONICAL, document gap in REALITY
```

### Principle 3: Change Governance
```
Minor change (wording, examples):
  → Update CANONICAL directly
  
Bug/limitation discovered:
  → Add to REALITY/known_issues.md
  
Architectural change needed:
  → Create ADR
  → Update CANONICAL
  → Mark work in DEVELOPMENT
  → Review & approve
```

### Principle 4: No Ambiguity
```
Every file has:
  1. Clear layer (CANONICAL / REALITY / DEVELOPMENT / ARCHIVE)
  2. Authority level (✅ / 🟡 / 🟢 / 🟣)
  3. Update frequency (rare/occasional/frequent/never)
  4. Owner (architect/developer/team/historical)
```

---

## 🗂️ File Structure (Proposed)

```
/docs/ia/
├─ MASTER_INDEX.md (routing to all 4 layers)
│
├─ CANONICAL/                          ← Authority (Change = ADR required)
│  ├─ rules/
│  ├─ specifications/
│  ├─ decisions/
│  └─ README.md
│
├─ REALITY/                            ← Observations (Change = bug fix)
│  ├─ current-system-state/
│  ├─ limitations/
│  ├─ observations/
│  └─ README.md
│
├─ DEVELOPMENT/                        ← Ephemeral (Change = daily)
│  ├─ execution-state/
│  ├─ checkpoints/
│  ├─ decisions-in-progress/
│  ├─ blockers-and-risks/
│  └─ README.md
│
└─ ARCHIVE/                            ← Historical (Never change)
   ├─ deprecated-decisions/
   ├─ working-sessions/
   ├─ legacy-documentation/
   └─ README.md
```

---

## 🔄 Migration Path

**Current → Proposed** (What moves where):

```
Current File                    → Proposed Layer
─────────────────────────────────────────────────
ia-rules.md                     → CANONICAL/rules/
constitution.md                 → CANONICAL/rules/
conventions.md                  → CANONICAL/rules/
architecture.md                 → CANONICAL/specifications/
contracts.md (spec)             → CANONICAL/specifications/
feature-checklist.md            → CANONICAL/specifications/
testing.md                       → CANONICAL/specifications/
definition_of_done.md           → CANONICAL/specifications/
ADR-*.md                        → CANONICAL/decisions/
GOVERNANCE_RULES.md             → DELETE (absorbed by structure)
execution_state.md              → DEVELOPMENT/execution-state/_current.md
specs/runtime/threads/          → DEVELOPMENT/execution-state/threads/
specs/runtime/checkpoints/      → DEVELOPMENT/checkpoints/
known_issues.md                 → REALITY/limitations/known_issues.md
rag_pipeline.md                 → REALITY/current-system-state/rag_pipeline.md
services.md                     → REALITY/current-system-state/services.md
contracts.md (current)          → REALITY/current-system-state/contracts.md
data_models.md                  → REALITY/current-system-state/data_models.md
storage_limitations.md          → REALITY/limitations/storage_limitations.md
threading_concurrency.md        → REALITY/limitations/threading_concurrency.md
scaling_constraints.md          → REALITY/limitations/scaling_constraints.md
RUNTIME_STATE.md                → DELETE (absorbed by structure + new README.md)
```

---

## 💡 Why This is World-Class

### 1. No Ambiguity
Every file has one purpose, one authority level, one owner
- Developers never ask "which file is the truth?"
- Code reviewers have clear standards
- No mixed signals

### 2. Scalable
Each layer grows independently without contamination
- Add new CANONICAL rules → doesn't affect REALITY
- Add new bugs to REALITY → doesn't change CANONICAL
- Clean work in DEVELOPMENT → doesn't pollute anything
- Archive old work → doesn't clutter active development

### 3. Decision-Making is Clear
```
Code change decision:
  1. CANONICAL says X? → Must do X
  2. REALITY documents exception Y? → Acceptable for now
  3. DEVELOPMENT says working on Z? → Context only
  4. Decision: Do X per CANONICAL, document as technical debt in REALITY
```

### 4. Authority is Earned
- CANONICAL files = must pass architectural review
- REALITY files = must have evidence (bug reproduction, perf data)
- DEVELOPMENT files = working notes, no approval needed
- ARCHIVE files = historical, read-only

### 5. No Coupled Updates
```
Bug found:
  ✅ Update REALITY/known_issues.md (immediate)
  ✅ Update DEVELOPMENT (link to work)
  🟢 Update CANONICAL? Only if rule is wrong (ADR)

Canonical changes:
  🟢 DEVELOPMENT updates (replan)
  🟢 REALITY updates if conflicts (document gap)
```

---

## ✅ Implementation Checklist

- [ ] Create CANONICAL/ directory structure
- [ ] Create REALITY/ directory structure  
- [ ] Create DEVELOPMENT/ directory structure
- [ ] Create ARCHIVE/ directory structure
- [ ] Move files per migration table
- [ ] Create README.md for each layer
- [ ] Update MASTER_INDEX.md
- [ ] Delete GOVERNANCE_RULES.md (structure absorbs it)
- [ ] Delete RUNTIME_STATE.md (structure absorbs it)
- [ ] Create "Decision Matrix" document in MASTER_INDEX
- [ ] Document anti-patterns for agents
- [ ] Add layer reference to every file header

---

## 🎯 Governance

**This is a SPEC mandate:**
- All new documentation follows 4-layer model
- File headers include layer + authority + update frequency
- Changes respect layer boundaries
- Anti-patterns are flagged in review

---

**Principle:**
> Authority is immutable.  
> Reality is observed.  
> Development is ephemeral.  
> Archive is history.  
>
> Each layer has clear purpose.  
> No file is ambiguous.  
> World-class engineering.
