# ARCHIVE Layer — Historical Record

**Layer:** ARCHIVE  
**Authority Level:** 🟣 NONE — Read-only history  
**Update Frequency:** Low (when threads complete, decisions are deprecated)  
**Owner:** Team lead (moves content here, never modifies)  
**Last Reviewed:** April 2026 ✅  
**Next Review Required:** Quarterly (cleanup old threads)  

---

## Purpose

This layer preserves **historical record**. It captures:
- Completed threads (what did we build?)
- Deprecated decisions (why did we change approach?)
- Working sessions (what was the thinking process?)
- Legacy documentation (old approaches, for context)

**This layer is READ-ONLY.** Never modify files here; only move into or move out.

## Structure

### working-sessions/
Historical analysis and thinking:
- Session summaries from architecture reviews
- Analysis of design problems
- Exploration of solution approaches
- Rationale for decisions made

### deprecated-decisions/
Old ADRs or decisions that changed:
- `ADR-NNN-DEPRECATED-title.md` — Move here with rationale
- Always include: "Deprecated in favor of ADR-XXX (reason)"
- Never delete, always keep full history

### legacy-documentation/
Old docs that are no longer authoritative:
- Previous architecture attempts
- Old onboarding guides (superseded)
- Previous decision analysis (replaced by consolidated versions)

## Common Patterns

### Moving a thread to ARCHIVE
```
1. Thread completes (goal reached, or deprioritized)
2. Capture final state: THREAD-NAME-FINAL.md
3. Move THREAD-NAME-*.md to ARCHIVE/working-sessions/
4. Delete from DEVELOPMENT/execution-state/threads/
5. Remove from DEVELOPMENT/execution-state/_current.md
```

### Deprecating a decision
```
1. New ADR created (e.g., ADR-007)
2. Old ADR gets "-DEPRECATED" suffix
3. Move to ARCHIVE/deprecated-decisions/
4. Update CANONICAL/decisions/ to reference the deprecation
5. Note: Don't delete, keep for audit trail
```

## When to Reference

**Use ARCHIVE for:**
- "Why did we stop doing X?"
- "What was the thinking behind approach Y?"
- Understanding decision history
- Learning from past attempts

**When adding:**
- Always move from DEVELOPMENT (completed threads)
- Always move from CANONICAL (deprecated decisions)
- Always include context/rationale
- Never delete; append only

## Cleanup Rules

- Keep working-sessions for 6 months, then review
- Keep deprecated decisions FOREVER (audit trail)
- Keep legacy docs for 1 year, then review
- When in doubt, keep it (cost of storage is low)

---

**NOTE:** This layer is append-only, read-mostly, and provides historical context for future decision-making.

## 🔍 Why Archive These?

**Removed from Active Development Because:**
- ✅ Insights have been consolidated into DECISIONS_APRIL_2026.md
- ✅ All decisions are final (no pending choices)
- ✅ All SPEC gaps have been fixed
- ✅ Analysis paralysis risk (multiple docs say same thing)

**Kept as Reference Because:**
- 📖 Detailed problem scenarios (useful for onboarding)
- 📖 Validation logic (why each decision is right)
- 📖 Historical record (how we got here)

---

## 📍 How to Find Information

**If you need:**

| Need | Look In |
|------|---------|
| Current 8 decisions | `/docs/ia/decisions/DECISIONS_APRIL_2026.md` |
| Problem scenarios | `DECISIONS_EXPLAINED_PRACTICAL.md` (archived) |
| Validation logic | `CONSOLIDATION_QUALITY_AUDIT.md` (archived) |
| Business rules context | `/docs/ia/specs/_shared/business-rules.md` |
| Memory hierarchy details | `SEMANTIC_MEMORY_VISION.md` (archived) |
| Architecture specs | `/docs/ia/specs/_shared/architecture.md` |

---

**Last Updated:** April 18, 2026
**Status:** Complete (no pending items)
