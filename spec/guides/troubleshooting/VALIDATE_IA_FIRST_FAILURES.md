# 🔍 VALIDATE IA-FIRST Failures — Troubleshooting Guide

**For:** Developers seeing IA-FIRST format validation errors  
**Time to Resolution:** 5-15 minutes (most cases)  
**Status:** Documentation is migrating to IA-FIRST format (in progress)

---

## 🎯 Quick Navigation

| Issue | Symptom | Resolution | Time |
|-------|---------|-----------|------|
| **Missing IA-FIRST DESIGN NOTICE** | `Warning: Missing IA-FIRST DESIGN NOTICE` | Add header section | 2 min |
| **Invalid Status field** | `Error: Invalid status 'X'` | Use Complete/WIP/Deprecated | 1 min |
| **Heading hierarchy broken** | `Warning: Inconsistent heading` | Fix H1→H2→H3 structure | 3 min |
| **Backtick links** | `Warning: Found backtick links` | Change \`[text]\` to [text](path) | 2 min |
| **Missing metadata** | `Error: Missing Status field` | Add Status: Complete/WIP/Deprecated | 1 min |
| **No emoji markers** | `Warning: No emoji markers` | Add ✅ ❌ 🎯 ⚠️ to decision points | 3 min |

---

## 📋 Common Errors & Fixes

### Error 1: Missing IA-FIRST DESIGN NOTICE

**Symptom:**
```
⚠️ docs/ia/my-doc.md: Missing IA-FIRST DESIGN NOTICE
```

**Cause:**
The document exists but doesn't have the required header section that explains the format.

**Fix (1 minute):**
```markdown
# My Document Title

## ⚡ IA-FIRST DESIGN NOTICE

**This document is optimized for AI parsing:**
- Structure: H1 → H2 (sections) → H3 (subsections)
- Lists use `-` (not numbers)
- Links use [text](path.md) format (no backticks)
- Constraints marked with emoji: ✅ ❌ 🎯 ⚠️

**Status:** Complete
**Last Updated:** 2026-04-19

---

## Your Content Here
```

**Why it matters:**
AI agents need to know the document format is machine-parseable. This notice guarantees consistency.

---

### Error 2: Invalid Status Field

**Symptom:**
```
❌ docs/ia/my-doc.md: Invalid status '🚀'. Must be: ['Complete', 'WIP', 'Deprecated']
```

**Cause:**
Status field has emoji or invalid value instead of exactly: `Complete`, `WIP`, or `Deprecated`.

**Fix (1 minute):**
```markdown
# Valid Statuses

**WRONG:**
  Status: 🚀 Complete     ← Emoji not allowed
  Status: Ready           ← Not in allowed list
  Status: COMPLETE        ← Wrong case

**RIGHT:**
  Status: Complete        ← Exactly this
  Status: WIP             ← Or this
  Status: Deprecated      ← Or this
```

**Where to add it:**
```markdown
## ⚡ IA-FIRST DESIGN NOTICE

**This document is...**
- ...
- ...

**Status:** Complete  ← Add here in the notice section
```

---

### Error 3: Inconsistent Heading Hierarchy

**Symptom:**
```
⚠️ docs/ia/my-doc.md: Inconsistent heading hierarchy (should be H1 → H2 → H3)
```

**Cause:**
Heading levels jump (e.g., H1 → H3, skipping H2), or other structure issues.

**Fix (3 minutes):**

**WRONG:**
```markdown
# Title

### Section A    ← Skipped H2!

## Section B
```

**RIGHT:**
```markdown
# Title (H1)

## Section A (H2)

### Subsection A1 (H3)

## Section B (H2)

### Subsection B1 (H3)
```

**Key rule:**
- Each level can only increase by 1: `#` → `##` → `###` (not `##` → `####`)
- Valid sequences: `#` alone OR `# → ## → ###` only

---

### Error 4: Backtick Links

**Symptom:**
```
⚠️ docs/ia/my-doc.md: Found backtick links (use [text](path) instead of `[text]`)
```

**Cause:**
Link text is wrapped in backticks: `` `[text]` ``

**Fix (2 minutes):**

**WRONG:**
```markdown
Read the `[rules](docs/ia/ia-rules.md)` doc.
Or: ` `[my reference]` `
```

**RIGHT:**
```markdown
Read the [rules](docs/ia/ia-rules.md) doc.
Or: [my reference](docs/ia/...)
```

**Common mistake:**
Developers accidentally wrap links in backticks thinking they need code formatting. Don't - links are naturally formatted.

---

### Error 5: Missing Status Field

**Symptom:**
```
❌ docs/ia/my-doc.md: Missing Status field
```

**Cause:**
The document doesn't have a Status metadata field.

**Fix (1 minute):**
Add to your IA-FIRST DESIGN NOTICE section:

```markdown
## ⚡ IA-FIRST DESIGN NOTICE

**This document is optimized for AI parsing:**
- Structure: H1 → H2 → H3
- [other guidelines...]

**Status:** Complete  ← Add this line
**Last Updated:** 2026-04-19
```

---

### Error 6: No Emoji Markers

**Symptom:**
```
⚠️ docs/ia/my-doc.md: No emoji markers found (use ✅, ❌, 🎯, ⚠️)
```

**Cause:**
Document uses prose but no emoji to highlight decisions.

**Fix (3 minutes):**
Add emoji at decision points:

**BEFORE:**
```markdown
### Design Decision

We chose database X instead of Y because...
```

**AFTER:**
```markdown
### Design Decision

✅ **Choice:** Database X  
❌ **Rejected:** Database Y (too slow for 1000+ concurrent)  
🎯 **Constraint:** Must handle 10k entities, <100ms latency  
⚠️ **Risk:** Migration complex, needs manual testing
```

**When to use each emoji:**
- ✅ Chosen approach, enabled, working
- ❌ Rejected approach, disabled, error
- 🎯 Goal, target, constraint
- ⚠️ Risk, warning, caution

---

## 🚀 Automated Fix Mode (Use Carefully!)

**Warning:** Auto-fix may corrupt your docs. Use only if you understand the risks.

```bash
# Run validation with auto-fix
python packages/.sdd-wizard/SCRIPTS/validate-ia-first.py --fix

# This will:
# ✅ Add IA-FIRST DESIGN NOTICE to docs that are missing it
# ✅ Fix obvious heading hierarchy issues
# ❌ NOT fix Status fields (manual required - too risky to auto-guess)
# ❌ NOT fix backtick links (need human context)
```

**After running --fix:**
```bash
# Always verify changes
git diff docs/ia/

# If corrupted:
git checkout docs/ia/
```

---

## 📊 Status: PHASE 3 Migration

**Current State:**
- ✅ New docs (created in v2.1+) follow IA-FIRST format
- ⚠️ Existing docs (~116 docs) not yet migrated
- 🚀 Migration scheduled for PHASE 3 (Operational Clarity)

**What to do NOW:**
- When creating new docs: Always include IA-FIRST DESIGN NOTICE
- When updating old docs: Fix IA-FIRST issues while you're editing
- **Don't worry about:** Passing --audit check (it's a warning, not blocking)

**What happens PHASE 3:**
- Mass migration of all 116 docs to IA-FIRST format
- Automated where possible, manual where needed
- Will include tooling to prevent drift

---

## 🔗 Related Docs

- [IA-FIRST Specification](../../../CANONICAL/specifications/IA_FIRST_SPECIFICATION.md) — Format definition
- [validate-ia-first.py Script](packages/.sdd-wizard/SCRIPTS/validate-ia-first.py) — Source code
- [Emergency Procedures](../emergency/) — If validation completely breaks

---

## 📝 Quick Checklist (for new docs)

When creating a new document, ensure:

- [ ] H1 title at top
- [ ] ## ⚡ IA-FIRST DESIGN NOTICE section after H1
- [ ] Status field (Complete/WIP/Deprecated)
- [ ] Heading hierarchy: H1 → H2 → H3 (no skips)
- [ ] Links use [text](path.md) format, not backticks
- [ ] Decision points marked with emoji (✅ ❌ 🎯 ⚠️)

**Time to check:** < 2 minutes  
**Prevents:** Validation warnings + keeps docs machine-parseable

---

**Last Updated:** 2026-04-19  
**Status:** Complete (v1.0)
