# 🔄 MIGRATION GUIDE: New docs/ia Structure (April 2026)

**Status:** ✅ Active  
**Effective Date:** 2026-04-19  
**Impact:** All developers  
**Duration:** 1 day to adapt

---

## 🎯 What Changed?

The `/docs/ia` structure has been refactored to:

1. **Standardize language to English** (was mixing Portuguese)
2. **Separate generic templates from project specializations** (was mixed together)
3. **Optimize for on-demand reading** (was unclear what to read when)

---

## 📊 Before vs. After

### BEFORE (Mixed)
```
CANONICAL/
├─ rules/
│  ├─ ia-rules.md (had "rpg-narrative-server" hardcoded) ❌
│  └─ constitution.md (had "campaign" everywhere) ❌
└─ specifications/
   ├─ security-model.md (referenced rpg-narrative-server)
   └─ ...

custom/rpg-narrative-server/
├─ development/
└─ reality/
    # No specializations - everything mixed in CANONICAL

guides/
├─ onboarding/
├─ implementation/
└─ reference/
    # Unclear what to read for which task
```

### AFTER (Clean)
```
CANONICAL/
├─ rules/
│  ├─ ia-rules.md (now generic, uses [PROJECT_NAME] template) ✅
│  ├─ constitution.md (now generic, uses "entity" not "campaign") ✅
│  └─ ...
└─ specifications/
   └─ (all generic, 100% reusable)

custom/rpg-narrative-server/
├─ SPECIALIZATIONS/ (NEW)
│  ├─ ia-rules-rpg-specific.md (project-specific values) ✅
│  ├─ constitution-rpg-specific.md (campaign-specific patterns) ✅
│  └─ README.md (how specializations work) ✅
├─ development/
└─ reality/

guides/
├─ _INDEX.md (NEW - on-demand navigation) ✅
├─ onboarding/
├─ implementation/
└─ reference/
```

---

## 🔑 Key Improvements

### 1. **Standardized to English**
- Removed Portuguese text from documents
- All documents now 100% English
- Easier for international teams

### 2. **CANONICAL is now truly generic**
- `ia-rules.md`: Uses `[PROJECT_NAME]` and `[PROJECT_PATH]` templates
- `constitution.md`: Uses "domain entity" instead of "campaign"
- Can be reused across multiple projects

### 3. **Project specializations separate**
- New `/custom/rpg-narrative-server/SPECIALIZATIONS/` directory
- Maps generic principles to project-specific implementations
- Example: "Concurrency target: 50+ entities" → "50+ campaigns in rpg-narrative-server"

### 4. **On-demand reading optimized**
- New `guides/_INDEX.md` tells you what to read based on:
  - Your task (bug fix, feature, learning)
  - Your time budget (5 min, 15 min, 1 hour)
  - Your role (backend, devops, PM, architect)

---

## 🛠️ How to Use New Structure

### **If you're learning the framework**
1. Read: `guides/_INDEX.md` → "I'm new to the project"
2. Follow PATH A, B, C, or D based on your task
3. Skip project-specific docs until you start implementing

### **If you're implementing a feature**
1. Check: `guides/_INDEX.md` → "I'm implementing X"
2. Read CANONICAL principles relevant to your task
3. Read project specializations for rpg-narrative-server specifics
4. Implement with confidence

### **If you're confused about something**
1. Check: `guides/_INDEX.md` → "I'm stuck with..."
2. It points you to the exact document
3. Read that document, problem solved

### **If you're adding a new project to SPEC**
1. Copy `/custom/_TEMPLATE/` to `/custom/your-project/`
2. Create `SPECIALIZATIONS/` directory
3. Create `*-your-project-specific.md` files
4. Map CANONICAL principles to your project
5. Share specializations with team

---

## 📍 Document Locations: Old vs. New

### Rules & Policies

| Topic | Before | After |
|-------|--------|-------|
| Execution rules | `CANONICAL/rules/ia-rules.md` (mixed) | `CANONICAL/rules/ia-rules.md` (generic) + `custom/.../ia-rules-rpg-specific.md` (concrete) |
| Principles | `CANONICAL/rules/constitution.md` (mixed) | `CANONICAL/rules/constitution.md` (generic) + `custom/.../constitution-rpg-specific.md` (concrete) |
| Backward compat | `CANONICAL/rules/backward-compatibility-policy.md` (mixed) | `CANONICAL/rules/backward-compatibility-policy.md` (generic only) |

### Specifications

| Topic | Before | After |
|-------|--------|-------|
| Architecture | `CANONICAL/specifications/architecture.md` | Same (generic) |
| Security | `CANONICAL/specifications/security-model.md` | Same (generic) |
| Observability | `CANONICAL/specifications/observability.md` | Same (generic) |
| Performance | `CANONICAL/specifications/performance.md` | Same (generic) |

### Guides

| Topic | Before | After |
|-------|--------|-------|
| Getting started | `guides/onboarding/FIRST_SESSION_SETUP.md` | Same |
| Quick start | `guides/onboarding/QUICK_START.md` | Same |
| Navigation | None | NEW: `guides/_INDEX.md` |

### Project-Specific (NEW)

| Topic | Before | After |
|-------|--------|-------|
| Project rules | Scattered in CANONICAL | NEW: `custom/.../SPECIALIZATIONS/ia-rules-rpg-specific.md` |
| Campaign patterns | Scattered in CANONICAL | NEW: `custom/.../SPECIALIZATIONS/constitution-rpg-specific.md` |
| Understanding specializations | N/A | NEW: `custom/.../SPECIALIZATIONS/README.md` |

---

## 📖 Reading Flow Changes

### BEFORE
You had to:
1. Read generic principle in CANONICAL
2. Infer project specifics (campaign, rpg-narrative-server values)
3. Hope you interpreted correctly
4. Find out in PR review you were wrong

### AFTER
You:
1. Read generic principle in CANONICAL
2. Read concrete specialization in custom/
3. Implement exactly as documented
4. PR review confirms you understood correctly

---

## ✅ Migration Checklist

### For Developers

- [ ] Read `guides/_INDEX.md` (bookmark it!)
- [ ] Know your role and time budget
- [ ] When learning: Use index to find what to read
- [ ] When implementing: Read CANONICAL + specializations
- [ ] When stuck: Check index for help

### For Architects

- [ ] Review new specializations for accuracy
- [ ] Add new specializations as project grows
- [ ] Keep CANONICAL purely generic
- [ ] Update CANONICAL only for cross-project changes

### For Leads

- [ ] Share `guides/_INDEX.md` with team
- [ ] Explain new structure in standup
- [ ] Point developers to index for questions
- [ ] Monitor for confusion, update index

---

## 🔗 Quick Links After Migration

### For Every Developer
- **Bookmark:** `guides/_INDEX.md` (your navigation guide)
- **Bookmark:** `guides/onboarding/QUICK_START.md` (refresh on PATH)

### For Backend Developers
- **Bookmark:** `/EXECUTION/spec/CANONICAL/rules/constitution.md` (15 principles)
- **Bookmark:** `custom/rpg-narrative-server/SPECIALIZATIONS/` (project specifics)

### For DevOps/SRE
- **Bookmark:** `/EXECUTION/spec/CANONICAL/specifications/observability.md` (logging/metrics)
- **Bookmark:** `/EXECUTION/spec/CANONICAL/rules/COMPLIANCE_AUTOMATION_SETUP.md` (CI/CD)

### For Architects
- **Bookmark:** `/EXECUTION/spec/CANONICAL/rules/constitution.md` (all principles)
- **Bookmark:** `/EXECUTION/spec/CANONICAL/decisions/` (all ADRs)

---

## ⚠️ What Didn't Change

✅ Still the same:
- Core principles (same 15 principles in constitution)
- Architecture decisions (same 6 ADRs)
- Technology stack (same FastAPI, async, ChromaDB)
- Development process (same git workflow)

❌ Don't expect to find:
- Old Portuguese docs (`/docs/en/`, `/docs/pt-br/`) — moved to ARCHIVE
- Mixed project-specific details in CANONICAL — now in SPECIALIZATIONS

---

## 🆘 Common Questions

### **Q: Where are the campaign details?**
A: In `custom/rpg-narrative-server/SPECIALIZATIONS/constitution-rpg-specific.md`

### **Q: Where are the rpg-narrative-server paths?**
A: In `custom/rpg-narrative-server/SPECIALIZATIONS/ia-rules-rpg-specific.md`

### **Q: What should I read first?**
A: Check `guides/_INDEX.md` based on your task

### **Q: Can I modify CANONICAL?**
A: Only for cross-project improvements. Keep it generic.

### **Q: How do I add a new project?**
A: See `/custom/_TEMPLATE/README.md` for setup, then create specializations.

### **Q: Is the structure stable?**
A: Yes. Won't change unless adding major new project.

---

## 📞 Support

**Questions about migration?**
- Email: architecture@example.com
- Slack: #architecture-discussions

**Bug in new structure?**
- Report to: Lead Architect
- Include: What you were trying to do, what you expected, what you found

**Feature request for guides?**
- Request in: GitHub issues (label: docs)
- Include: Who needs this, when would they read it

---

**Version:** 1.0 (Initial Migration)  
**Status:** ✅ Effective  
**Effective Date:** 2026-04-19  
**Owner:** Chief Architect  
**Follow-up Review:** 2026-06-19 (2 months post-migration)
