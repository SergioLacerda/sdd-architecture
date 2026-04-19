# IMPLEMENTATION GUIDE: 4-Layer Separation

**Status:** 🎯 READY TO IMPLEMENT | **Backward Compatible:** YES | **Breaking Changes:** NO

---

## 🎯 What We're Doing

Moving from confusing coupling:
```
GOVERNANCE_RULES.md ─┐
RUNTIME_STATE.md ────┤ (mixed, ambiguous)
execution_state.md ──┘
```

To clear separation:
```
CANONICAL/ (immutable rules)
REALITY/ (observed gaps)
DEVELOPMENT/ (current work)
ARCHIVE/ (history)
```

**Result:** No ambiguity, clear authority per layer.

---

## 📋 Step-by-Step Implementation

### Phase 1: Create Directory Structure (30 min)

```bash
# Create the 4 layers
mkdir -p docs/ia/CANONICAL/{rules,specifications,decisions}
mkdir -p docs/ia/REALITY/{current-system-state,limitations,observations}
mkdir -p docs/ia/DEVELOPMENT/{execution-state,checkpoints,decisions-in-progress,blockers-and-risks}
mkdir -p docs/ia/ARCHIVE/{deprecated-decisions,working-sessions,legacy-documentation}

# Create README for each layer
touch docs/ia/CANONICAL/README.md
touch docs/ia/REALITY/README.md
touch docs/ia/DEVELOPMENT/README.md
touch docs/ia/ARCHIVE/README.md
```

### Phase 2: Move CANONICAL Files (30 min)

**Move these files with updated headers:**

```bash
# Rules
mv docs/ia/ia-rules.md → docs/ia/CANONICAL/rules/ia-rules.md
mv docs/ia/specs/constitution.md → docs/ia/CANONICAL/rules/constitution.md
mv docs/ia/specs/_shared/conventions.md → docs/ia/CANONICAL/rules/conventions.md

# Specifications
mv docs/ia/specs/_shared/architecture.md → docs/ia/CANONICAL/specifications/architecture.md
mv docs/ia/specs/_shared/contracts.md → docs/ia/CANONICAL/specifications/contracts.md
mv docs/ia/specs/_shared/feature-checklist.md → docs/ia/CANONICAL/specifications/feature-checklist.md
mv docs/ia/specs/_shared/testing.md → docs/ia/CANONICAL/specifications/testing.md
mv docs/ia/specs/_shared/definition_of_done.md → docs/ia/CANONICAL/specifications/definition_of_done.md

# Decisions
mv docs/ia/decisions/ADR-*.md → docs/ia/CANONICAL/decisions/
```

**Add header to each file:**

```markdown
# [Filename]

**Layer:** CANONICAL (Immutable, Authority)
**Authority Level:** ✅ YES — These define the ideal
**Update Frequency:** Rare (only ADRs, breaching changes)
**Owner:** Architect + ADR process
**Last Reviewed:** [DATE] ✅
**Next Review Required:** [DATE + 6 months]

---

[Rest of file content]
```

---

### Phase 3: Move REALITY Files (30 min)

**Move these files:**

```bash
# Current system state
mkdir -p docs/ia/REALITY/current-system-state
cp docs/ia/current-system-state/* docs/ia/REALITY/current-system-state/

# Limitations (reorganize)
mkdir -p docs/ia/REALITY/limitations
mv docs/ia/current-system-state/known_issues.md → docs/ia/REALITY/limitations/known_issues.md
mv docs/ia/current-system-state/storage_limitations.md → docs/ia/REALITY/limitations/storage_limitations.md
mv docs/ia/current-system-state/threading_concurrency.md → docs/ia/REALITY/limitations/threading_concurrency.md
mv docs/ia/current-system-state/scaling_constraints.md → docs/ia/REALITY/limitations/scaling_constraints.md

# Observations (new)
touch docs/ia/REALITY/observations/architecture_gaps.md
touch docs/ia/REALITY/observations/performance_findings.md
touch docs/ia/REALITY/observations/usability_issues.md
```

**Add header to each file:**

```markdown
# [Filename]

**Layer:** REALITY (Mutable, Observed)
**Authority Level:** 🟡 NO — These are observations, not rules
**Update Frequency:** Frequent (every bug discovery)
**Owner:** Developers (when discovering reality)
**Last Updated:** [DATE]
**Linked to Canonical:** [List sections that should match but don't]

---

[Rest of file content]
```

---

### Phase 4: Move DEVELOPMENT Files (20 min)

**Move these files:**

```bash
# Execution state
mkdir -p docs/ia/DEVELOPMENT/execution-state
mv docs/ia/specs/runtime/execution_state.md → docs/ia/DEVELOPMENT/execution-state/_current.md

# Threads
mkdir -p docs/ia/DEVELOPMENT/execution-state/threads
mv docs/ia/specs/runtime/threads/* → docs/ia/DEVELOPMENT/execution-state/threads/

# Checkpoints
mkdir -p docs/ia/DEVELOPMENT/checkpoints
mv docs/ia/specs/runtime/checkpoints/* → docs/ia/DEVELOPMENT/checkpoints/

# Create new files for decisions in progress
touch docs/ia/DEVELOPMENT/decisions-in-progress/TEMPLATE.md
touch docs/ia/DEVELOPMENT/blockers-and-risks/current-blockers.md
touch docs/ia/DEVELOPMENT/blockers-and-risks/risks.md
touch docs/ia/DEVELOPMENT/blockers-and-risks/assumptions.md
```

**Add header to each file:**

```markdown
# [Filename]

**Layer:** DEVELOPMENT (Mutable, Execution)
**Authority Level:** 🟢 NONE — These are working notes
**Update Frequency:** Real-time during work
**Owner:** Current agent(s)
**Refresh:** Weekly (delete/archive completed work)
**Ephemeral:** Yes — delete when work completes

---

[Rest of file content]
```

---

### Phase 5: Move ARCHIVE Files (20 min)

```bash
# Archive working sessions
mkdir -p docs/ia/ARCHIVE/working-sessions
mv docs/ia/ARCHIVE/working-sessions/* → docs/ia/ARCHIVE/working-sessions/

# Archive legacy docs
mkdir -p docs/ia/ARCHIVE/legacy-documentation
# Copy (don't move) old docs/en/, docs/pt-br/ versions if needed

# Create deprecated decisions folder
mkdir -p docs/ia/ARCHIVE/deprecated-decisions
# (Empty for now, populate as decisions are deprecated)
```

**Add header to archived files:**

```markdown
# [Filename] — ARCHIVED

**Layer:** ARCHIVE (Historical, Reference Only)
**Authority Level:** 🟣 NONE — Historical only, never reference for decisions
**Update Frequency:** Never (append-only)
**When Archived:** [DATE]
**Why:** [Reason: completed, deprecated, superseded]
**Read for:** Understanding history, lessons learned
**Never use for:** Code decisions, authority

---

[Rest of file content]
```

---

### Phase 6: Create Layer READMEs (20 min)

**`/docs/ia/CANONICAL/README.md`:**

```markdown
# CANONICAL Layer — Authority

This layer defines **what's RIGHT**. These are the rules, specifications, and decisions.

## Authority Level: ✅ YES
Code must conform or have written exception.

## Files Here
- `rules/` — Mandatory execution protocols
- `specifications/` — Design patterns & contracts
- `decisions/` — Architecture decision records (ADRs)

## Update Process
1. Changes require ADR or governance review
2. Mark as BREAKING if affects code standards
3. All agents must re-read
4. Update only after consensus

## Do NOT
- Change based on current state (use REALITY for that)
- Use development expediency as reason (use DEVELOPMENT for that)
- Bypass governance process

See: SPEC_CANONICAL_REALITY_DEVELOPMENT.md for full details.
```

**`/docs/ia/REALITY/README.md`:**

```markdown
# REALITY Layer — Observations

This layer describes **what ACTUALLY EXISTS**. Bugs, gaps, limitations, performance data.

## Authority Level: 🟡 CONTEXT
These are observations, not rules. Use for context and prioritization.

## Files Here
- `current-system-state/` — How the system actually works
- `limitations/` — Gaps, bugs, constraints, race conditions
- `observations/` — Interesting findings that don't fit elsewhere

## Update Process
1. Add immediately when discovering gap/bug
2. Link to canonical rule that should apply
3. Document workaround if exists
4. Flag severity (P1/P2/P3)

## Do NOT
- Use as excuse to violate canonical
- Leave gaps undocumented
- Assume they're permanent (they're technical debt)

See: SPEC_CANONICAL_REALITY_DEVELOPMENT.md for full details.
```

**`/docs/ia/DEVELOPMENT/README.md`:**

```markdown
# DEVELOPMENT Layer — Ephemeral Work

This layer tracks **what we're DOING RIGHT NOW**. Current work, decisions in progress, blockers.

## Authority Level: 🟢 NONE
These are working notes, not authority. Clean up frequently.

## Files Here
- `execution-state/` — Current work, threads, next steps
- `checkpoints/` — Completed milestones (move to ARCHIVE when done)
- `decisions-in-progress/` — Being considered, not yet decided
- `blockers-and-risks/` — What's stopping us, what could go wrong

## Update Process
1. Start work: Create entry or update _current.md
2. During work: Update blockers/risks as discovered
3. End of session: Update checkpoints
4. Work complete: Move to ARCHIVE

## Do NOT
- Make code decisions based only on here (check CANONICAL first)
- Keep outdated entries (archive or delete)
- Treat as authority (it's not)

See: SPEC_CANONICAL_REALITY_DEVELOPMENT.md for full details.
```

**`/docs/ia/ARCHIVE/README.md`:**

```markdown
# ARCHIVE Layer — History

This layer contains **what we LEARNED**. Previous attempts, deprecated decisions, historical context.

## Authority Level: 🟣 NONE
Historical only. Never reference for code decisions.

## Files Here
- `deprecated-decisions/` — Old ADRs, rejected alternatives
- `working-sessions/` — Old analysis, session notes
- `legacy-documentation/` — Previous versions of docs

## What Belongs Here
- Completed analysis (after decision made)
- Old documentation (after replaced)
- Deprecated decisions (after superseded)
- Session notes (after checkpoint complete)

## Do NOT
- Reference for code authority (it's deprecated)
- Keep current work here (use DEVELOPMENT)
- Modify after archival

Read for: Understanding "why did we change?" and "what was tried before?"

See: SPEC_CANONICAL_REALITY_DEVELOPMENT.md for full details.
```

---

### Phase 7: Update All Links (1 hour)

Update all references throughout the codebase:

```bash
# Update MASTER_INDEX.md
grep -r "docs/ia/ia-rules" . → Update to "docs/ia/CANONICAL/rules/ia-rules"
grep -r "specs/constitution" . → Update to "docs/ia/CANONICAL/rules/constitution"
grep -r "specs/architecture" . → Update to "docs/ia/CANONICAL/specifications/architecture"
# ... (continue for all files)

# Update copilot-instructions.md
# Update FIRST_SESSION_SETUP.md
# Update all guides
# Update code comments pointing to docs
```

### Phase 8: Create Migration Checklist (10 min)

Create `/docs/ia/LAYER_MIGRATION_CHECKLIST.md`:

```markdown
# 4-Layer Migration Checklist

**Status:** In Progress
**Date Started:** 2026-04-18
**Expected Completion:** 2026-04-19

## Structural Changes
- [x] Create CANONICAL directory structure
- [x] Create REALITY directory structure
- [x] Create DEVELOPMENT directory structure
- [x] Create ARCHIVE directory structure
- [ ] Move CANONICAL files (rules)
- [ ] Move CANONICAL files (specifications)
- [ ] Move CANONICAL files (decisions)
- [ ] Move REALITY files (current-system-state)
- [ ] Move REALITY files (limitations)
- [ ] Create REALITY/observations files
- [ ] Move DEVELOPMENT files
- [ ] Create DEVELOPMENT/decisions-in-progress
- [ ] Create DEVELOPMENT/blockers-and-risks
- [ ] Move ARCHIVE files

## Documentation Updates
- [ ] Create CANONICAL/README.md
- [ ] Create REALITY/README.md
- [ ] Create DEVELOPMENT/README.md
- [ ] Create ARCHIVE/README.md
- [ ] Add layer headers to all CANONICAL files
- [ ] Add layer headers to all REALITY files
- [ ] Add layer headers to all DEVELOPMENT files
- [ ] Add layer headers to all ARCHIVE files

## Link Updates
- [ ] Update MASTER_INDEX.md references
- [ ] Update FIRST_SESSION_SETUP.md
- [ ] Update all guides
- [ ] Update all README.md files
- [ ] Update code comments (if any) pointing to docs

## Cleanup
- [ ] Delete GOVERNANCE_RULES.md (absorbed by structure)
- [ ] Delete RUNTIME_STATE.md (absorbed by structure)
- [ ] Remove old specs/runtime/ (moved to DEVELOPMENT)
- [ ] Remove old current-system-state/ directory (moved to REALITY)
- [ ] Verify no broken links

## Verification
- [ ] CANONICAL layer is authoritative
- [ ] REALITY layer documents gaps
- [ ] DEVELOPMENT layer tracks progress
- [ ] ARCHIVE layer is read-only
- [ ] All agents can navigate clearly
- [ ] Decision-making is unambiguous

## Post-Implementation
- [ ] First development session validates structure
- [ ] Document any issues found
- [ ] Update this checklist with lessons learned
```

---

## 📊 Migration Timeline

| Phase | Duration | Status | Owner |
|-------|----------|--------|-------|
| 1. Create directories | 30 min | 🎯 Ready | You |
| 2. Move CANONICAL | 30 min | 🎯 Ready | You |
| 3. Move REALITY | 30 min | 🎯 Ready | You |
| 4. Move DEVELOPMENT | 20 min | 🎯 Ready | You |
| 5. Move ARCHIVE | 20 min | 🎯 Ready | You |
| 6. Create READMEs | 20 min | 🎯 Ready | You |
| 7. Update links | 1 hour | 🎯 Ready | You or automated |
| 8. Verify | 30 min | 🎯 Ready | You |
| **Total** | **~4 hours** | **READY** | **Today** |

---

## ✅ Verification Checklist

After implementation, verify:

```
CANONICAL Layer:
  ✅ Can find "is X allowed?"
  ✅ Can find "what's the rule for Y?"
  ✅ Single source of truth for code standards
  ✅ No mixing with current state

REALITY Layer:
  ✅ Can find "what's the bug?"
  ✅ Can find "what's the gap?"
  ✅ Can find "what actually works?"
  ✅ No rule-changing here

DEVELOPMENT Layer:
  ✅ Can find "what are we doing?"
  ✅ Can find "what's next?"
  ✅ Can find "what's blocking us?"
  ✅ Ephemeral, gets cleaned up

ARCHIVE Layer:
  ✅ Can find historical context
  ✅ Can find "why did we change?"
  ✅ Read-only, not referenced for decisions
  ✅ Clearly marked as historical

Overall:
  ✅ No ambiguity about which file is authority
  ✅ No accidental coupling
  ✅ Clear navigation
  ✅ World-class structure
```

---

## 🚨 Potential Issues & Mitigations

### Issue 1: Too Much Reorganization
**Risk:** Links break, confusion during migration  
**Mitigation:** Keep old files until all links updated, do in one session

### Issue 2: Existing Agents Confused
**Risk:** Documentation moves, agents don't know where to look  
**Mitigation:** Update FIRST_SESSION_SETUP.md immediately, explain in checkpoints

### Issue 3: Link Rot
**Risk:** Some links not updated, broken references  
**Mitigation:** Automated grep search + manual verification

### Issue 4: Ambiguity During Transition
**Risk:** Some docs in old place, some in new place  
**Mitigation:** Do complete migration same day, don't leave half-done

---

## 🎯 Success Metrics

- [ ] Zero ambiguity about "which file is authority"
- [ ] Clear separation of concerns (no leakage)
- [ ] Developers can navigate effortlessly
- [ ] Code reviewers have clear standards
- [ ] Zero broken links
- [ ] New team members understand structure immediately

---

## 🎉 Expected Benefits

After implementation:
- ✅ 90% reduction in "which file should I read?" confusion
- ✅ Clear governance process (no ad-hoc changes)
- ✅ Better prioritization (gaps are visible, documented)
- ✅ Scalable documentation (each layer grows independently)
- ✅ World-class engineering standards
- ✅ Historical narrative preserved (ARCHIVE layer)

---

## 📞 Support

If confused during migration:
1. Reference: SPEC_CANONICAL_REALITY_DEVELOPMENT.md
2. Check: Decision Matrix in that document
3. Ask: "Is this a rule, observation, work, or history?"
4. File goes to that layer

---

**Status:** Ready to implement. Estimated time: 4 hours, high confidence.

**Recommendation:** Do in one session to avoid transition confusion.
