# REALITY Layer — Observed State

**Layer:** REALITY  
**Authority Level:** 🟡 CONTEXT — Documents what we've discovered  
**Update Frequency:** Moderate (when new gaps/constraints discovered)  
**Owner:** Architecture + DevOps + QA  
**Last Reviewed:** April 2026 ✅  
**Next Review Required:** July 2026  

---

## Purpose

This layer documents the **current reality of what exists vs. what CANONICAL specifies**. It answers:
- What system limitations exist RIGHT NOW?
- What gaps exist between ideal (CANONICAL) and reality?
- What constraints must we work around?
- What observations should inform future decisions?

## Structure

### current-system-state/
Live facts about the running system:
- `_INDEX.md` — Query router ("I need X, where is Y?")
- `rag_pipeline.md` — Real 8-component pipeline architecture
- `services.md` — 8 services, execution flows, dependencies
- `contracts.md` — Real 9 ports (vs. CANONICAL's 18 planned)
- `data_models.md` — DTOs, API schemas, storage structure
- `_quiz_tracking.json` — Session state for validation quiz

### limitations/
Hard constraints discovered through operation:
- `known_issues.md` — 11 documented bugs with workarounds
- `storage_limitations.md` — JSON storage bottlenecks, migration plan
- `threading_concurrency.md` — Concurrency limits (2-level isolation only)
- `scaling_constraints.md` — Vector index scaling ceiling, memory limits

### observations/
Notes on system behavior (currently empty, for future use):
- Gap analysis reports
- Performance observations
- Deployment notes
- Lessons learned during operation

## When to Reference

**Use REALITY for:**
- Understanding what ACTUALLY exists today
- Finding workarounds for known limitations
- Planning features (what constraints must we respect?)
- Understanding gap between CANONICAL and reality

**When updating:**
- Document newly discovered constraints
- Record workarounds (don't lose tribal knowledge)
- Update when limitations are fixed (move to ARCHIVE)
- Always link to related CANONICAL files

## Priority Issues to Address

1. **Concurrency:** Limited to 2 levels, CANONICAL allows 4
2. **Storage:** JSON storage at scaling limit, needs PostgreSQL
3. **Vector Index:** HNSW hitting memory ceiling at 100K vectors
4. **Ports:** Only 9 implemented, CANONICAL specifies 18

---

**NOTE:** This layer is read-mostly during development, updated ~1-2/month when new constraints discovered.
