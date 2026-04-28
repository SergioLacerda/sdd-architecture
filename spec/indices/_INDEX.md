# 📑 Indices Layer — Quick Lookup

**Fast reference templates and indices for all projects**

---

## 🎯 Purpose

The indices layer provides template indices that projects copy and customize during PHASE 0 setup. Projects maintain their own copies in `.ai/runtime/` for fast, project-specific lookups.

---

## 📂 Available Indices

### 1. Search Keywords Index
**File:** `search-keywords.md`  
**Purpose:** Keyword-to-document mapping for on-demand discovery  
**Use When:** You know WHAT you're looking for, but not WHERE  
**Copy To:** `.ai/runtime/search-keywords.md` (project-local)

**Contents:**
- Framework concepts
- Constitutional foundation
- Architecture decisions
- Context-aware patterns
- Implementation standards
- Development workflow
- Emergency procedures
- Reference & glossary

---

### 2. CANONICAL Layer Index
**File:** `spec-canonical-index.md`  
**Purpose:** Complete reference to immutable authority layer  
**Use When:** Need to understand rules, decisions, and specifications  
**Copy To:** `.ai/runtime/spec-canonical-index.md` (project-local)

**Contents:**
- Authority hierarchy
- Rules (constitution, mandatory, conventions)
- Architecture decisions (6 ADRs)
- Specifications (how-to guides)
- Quick navigation by need
- Layers below CANONICAL
- Emergency quick links

---

### 3. Guides Layer Index
**File:** `spec-guides-index.md`  
**Purpose:** Complete reference to operational guides  
**Use When:** Need step-by-step help for specific scenarios  
**Copy To:** `.ai/runtime/spec-guides-index.md` (project-local)

**Contents:**
- Onboarding guides (9 files)
- Operational guides (5 files)
- Emergency guides (6 files)
- Quick navigation by scenario
- Duration estimates
- Guide relationships
- Quick links by problem

---

## 🔄 Two-Tier Index System

**Framework Tier (here, EXECUTION/spec/indices/):**
- ✅ Templates for all projects
- ✅ Updated quarterly (when framework changes)
- ✅ Canonical reference

**Project Tier (.ai/runtime/ in each project):**
- ✅ Project-specific copies
- ✅ Can diverge from framework
- ✅ Updated as needed by projects
- ✅ Fast local reference

**Workflow:**
```
1. Framework provides templates → EXECUTION/spec/indices/
2. During PHASE 0, templates copied → .ai/runtime/
3. Projects customize as needed
4. Each project maintains own indices
```

---

## 🚀 Getting Started

### For New Projects (PHASE 0)

```bash
# Copy indices templates to project-local
cp EXECUTION/spec/indices/search-keywords.md .ai/runtime/
cp EXECUTION/spec/indices/spec-canonical-index.md .ai/runtime/
cp EXECUTION/spec/indices/spec-guides-index.md .ai/runtime/

# Customize for your project (optional)
vi .ai/runtime/search-keywords.md
```

### For Existing Projects

```bash
# Verify you have project copies
ls -la .ai/runtime/search-keywords.md
ls -la .ai/runtime/spec-canonical-index.md
ls -la .ai/runtime/spec-guides-index.md

# If missing, copy from framework
cp EXECUTION/spec/indices/* .ai/runtime/
```

---

## 📊 Index Contents at a Glance

| Index | Primary Use | Size | Update Freq |
|-------|-------------|------|-------------|
| search-keywords.md | Fast keyword lookup | ~100 lines | Quarterly |
| spec-canonical-index.md | Understanding authority | ~150 lines | Quarterly |
| spec-guides-index.md | Finding how-to guides | ~180 lines | Monthly |

---

## ✅ How Indices Work

### Scenario 1: "Where's the rule about testing?"

```
1. Search keywords.md → "testing"
2. Find: CANONICAL/specifications/definition_of_done.md
3. Read: Testing section
```

### Scenario 2: "How do I add a new project?"

```
1. Search spec-guides-index.md → "Adding new project"
2. Find: guides/operational/ADDING_NEW_PROJECT.md
3. Follow: Step-by-step guide
```

### Scenario 3: "Why is thread isolation mandatory?"

```
1. Search spec-canonical-index.md → "thread isolation"
2. Find: CANONICAL/decisions/ADR-005
3. Read: Architecture decision
```

---

## 🔗 Related Documents

- **CANONICAL/specifications/context-aware-agent-pattern.md** — Canonical pattern for agent context organization
- **guides/** — Operational guides and onboarding
- **custom/[PROJECT]/** — Project-specific customizations
- **.ai/runtime/** — Project-local copies of these indices

---

## 📝 Notes

- These indices are TEMPLATES, not project-local instances
- Each project customizes its own `.ai/runtime/` copies
- Framework tier updated quarterly; projects can diverge
- For framework-level questions: use these files
- For project-specific questions: use `.ai/runtime/` copies

---

**Authority:** SPEC v2.1  
**Purpose:** Quick reference templates  
**Last Updated:** April 19, 2026  
**Status:** Production-Ready
