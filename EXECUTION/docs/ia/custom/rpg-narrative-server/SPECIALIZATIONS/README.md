# 🎮 RPG Narrative Server — SPECIALIZATIONS

**Purpose:** Project-specific instantiations of CANONICAL templates

---

## 📚 What is a Specialization?

Specializations map generic CANONICAL principles to rpg-narrative-server-specific details:

- **CANONICAL:** Generic template (all projects share)
- **SPECIALIZATIONS:** Concrete instances (this project only)

Example:
```
CANONICAL/rules/constitution.md (line 87):
  "50+ concurrent domain entities"

SPECIALIZATIONS/constitution-rpg-specific.md:
  "50+ concurrent campaigns" 
  (implementation details for rpg-narrative-server)
```

---

## 📂 Specialization Files

### 1. [ia-rules-rpg-specific.md](ia-rules-rpg-specific.md)
Extends: `/docs/ia/CANONICAL/rules/ia-rules.md`

**What's here:**
- Actual paths for rpg-narrative-server
- Project state locations
- Thread isolation specifics
- External service mappings (ChromaDB, OpenAI, etc.)

**When to read:**
- You're implementing a feature in rpg-narrative-server
- You need to understand execution flow for this project
- You're setting up development threads

### 2. [constitution-rpg-specific.md](constitution-rpg-specific.md)
Extends: `/docs/ia/CANONICAL/rules/constitution.md`

**What's here:**
- Campaign concurrency model (50-200 campaigns)
- Campaign isolation guarantees
- Campaign cleanup patterns
- Thread-local container setup

**When to read:**
- You're designing campaign infrastructure
- You need to understand multitenancy in this project
- You're optimizing performance

### 3. [enforcement-rpg-specific.md](enforcement-rpg-specific.md)
Extends: `/docs/ia/CANONICAL/rules/ENFORCEMENT_RULES.md`

**What's here:**
- Pre-commit hooks configuration
- Pytest validators for rpg-narrative-server
- CI/CD checks specific to this project
- What violations are checked

**When to read:**
- You're setting up development environment
- A commit hook failed
- You want to understand what's being validated

---

## 🔄 How Specializations Work

**Step 1: Read Generic Rule** (if new to topic)
```
→ /docs/ia/CANONICAL/rules/constitution.md
  (understand the principle)
```

**Step 2: Read Project Specialization** (to implement)
```
→ /docs/ia/custom/rpg-narrative-server/SPECIALIZATIONS/constitution-rpg-specific.md
  (implement for rpg-narrative-server)
```

**Step 3: Read Project Reality** (to debug)
```
→ /docs/ia/custom/rpg-narrative-server/reality/
  (understand current state)
```

---

## 🎯 When to Create New Specializations

Create a new specialization when:

✅ **DO create specialization for:**
- Project-specific tools or services
- Domain-specific terminology (campaign, narrative, etc.)
- Project-specific paths or configuration
- Project-specific examples

❌ **DON'T create specialization for:**
- Generic principles (those stay in CANONICAL)
- Rules that apply to all projects (those stay in CANONICAL)
- General examples (try generic ones first)

---

## 🔗 Integration with Other Projects

If multiple projects use SPEC:

```
CANONICAL/rules/constitution.md (shared by all)
├── custom/rpg-narrative-server/SPECIALIZATIONS/
├── custom/other-project/SPECIALIZATIONS/
└── custom/yet-another/SPECIALIZATIONS/
```

Each project specializes independently. No cross-project specializations.

---

## ✅ Specialization Checklist

When creating a new specialization:

- [ ] File name follows pattern: `{template-name}-rpg-specific.md`
- [ ] First line: "Extends: `/docs/ia/CANONICAL/{path}`"
- [ ] Sections map to CANONICAL sections (same headers)
- [ ] Concrete examples with project-specific values
- [ ] Links back to CANONICAL for principle details
- [ ] Added to this README

---

**Version:** 1.0 (Initial)  
**Status:** ✅ Active  
**Owner:** RPG Narrative Server Project  
**Last Updated:** 2026-04-19
