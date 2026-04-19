# DEVELOPMENT Layer — Active Work

**Layer:** DEVELOPMENT  
**Authority Level:** 🟢 NONE — These are ephemeral, for coordination  
**Update Frequency:** Real-time (during active work)  
**Owner:** Active developer(s) + Team lead  
**Last Reviewed:** April 2026 ✅  
**Next Review Required:** N/A (cleanup after work completes)  

---

## Purpose

This layer tracks **real-time work in progress**. It's high-churn, temporary, and primarily for:
- What are we currently building?
- What are the active threads of work?
- What blockers exist RIGHT NOW?
- What assumptions are we making?
- What were the recent checkpoints?

## Structure

### execution-state/
Current progress snapshot:
- `_current.md` — Last known execution state (updated regularly)
- `threads/` — One file per active thread (e.g., THREAD-MEMORY-01.md)
  - Each thread has: Goal, Status, Next Steps, Risks, Assumptions

### checkpoints/
Saved progress markers:
- Checkpoint-TIMESTAMP.md files
- Created after significant progress (new layer working, test suite green, etc.)
- Can be used to rollback if direction changes

### decisions-in-progress/
Work-in-progress decisions:
- Not yet ready for CANONICAL ADR process
- Exploring options, gathering data
- Will move to CANONICAL once approved via ADR

### blockers-and-risks/
Real-time risk tracking:
- `blockers.md` — What's stopping us RIGHT NOW
- `risks.md` — Future risks we've identified
- `assumptions.md` — What we're assuming that could break

## When to Reference

**Use DEVELOPMENT for:**
- "What are we working on right now?"
- "What's the current status?"
- "What's blocking us?"
- "What were the last checkpoints?"

**When updating:**
- Create/update `_current.md` at END of each work session (5 min)
- Create checkpoint after major progress (0 min, copy _current.md)
- Update threads/ as active work progresses (real-time)
- Update blockers/risks daily if active (2 min)

## Cleanup Policy

**CRITICAL:** This layer is TEMPORARY. Files should be cleaned up:
- ✅ Move to CANONICAL when decision is finalized (ADR process)
- ✅ Move to ARCHIVE when thread completes (for history)
- ✅ Delete blockers once resolved
- ✅ Delete old checkpoints after 1 month (keep last 3)

**Never leave stale files here.** This layer is FOR ACTIVE WORK ONLY.

---

**NOTE:** This layer is high-churn, expected to change hourly during active development.
