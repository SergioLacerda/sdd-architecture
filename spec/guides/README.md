# 📚 GUIDES ORGANIZATION

New structure for guides by purpose:

```
guides/
  ├─ README.md (this file - overview)
  │
  ├─ 🟢 onboarding/
  │   ├─ FIRST_SESSION_SETUP.md (15-min orientation)
  │   ├─ QUICK_START.md (3-min PATH decision)
  │   └─ SESSION_QUICK_REFERENCE.md (printable card)
  │
  ├─ 🔵 implementation/
  │   ├─ IMPLEMENTATION_ROADMAP.md (step-by-step process)
  │   ├─ DESIGN_DECISIONS.md (how to decide architecture)
  │   └─ TROUBLESHOOTING.md (debugging guide)
  │
  ├─ 🟣 navigation/
  │   ├─ INDEX.md (master reference index)
  │   └─ CONTEXT_INDEX.md (search guide)
  │
  ├─ 🟡 context/
  │   ├─ DELIVERY_SUMMARY.md (what was delivered)
  │   ├─ FINAL_STATUS.md (completion status)
  │   ├─ YOUR_VISION_IMPLEMENTED.md (how consulta works)
  │   └─ GOVERNANCE_BY_DOMAIN.md (reference copy)
  │
  └─ 📋 reference/
      ├─ FAQ.md (common questions)
      └─ GLOSSARY.md (terminology)
```

---

## 🟢 ONBOARDING

When starting a new agent session:

1. **FIRST_SESSION_SETUP.md** — 15-minute orientation
   - Understand documentation structure
   - Lock to ia-rules.md
   - Choose your PATH
   - Check execution state
   - Load adaptive context

2. **QUICK_START.md** — 3-minute decision tree
   - Decide your work type (A/B/C/D)
   - Know your context size
   - See common scenarios

3. **SESSION_QUICK_REFERENCE.md** — Printable reference card
   - All 16 rules
   - Checklists
   - Quick lookup tables
   - Keep handy while working

---

## 🔵 IMPLEMENTATION

When building features:

1. **IMPLEMENTATION_ROADMAP.md** — Step-by-step process
   - Full workflow from idea to merge
   - Checkpoints along the way
   - Integration points

2. **DESIGN_DECISIONS.md** — Making architectural choices
   - How to evaluate options
   - When to follow patterns vs deviate
   - How to document your decision

3. **TROUBLESHOOTING.md** — When things break
   - Common errors and fixes
   - Debugging strategies
   - Getting help

---

## 🟣 NAVIGATION

Finding what you need:

1. **INDEX.md** — "I need X, where do I go?"
   - Master reference
   - 30+ questions mapped to docs
   - Document matrix

2. **CONTEXT_INDEX.md** — Semantic search guide
   - How to search across docs
   - Keyword mapping
   - Browse by topic

---

## 🟡 CONTEXT

Background and historical information:

1. **DELIVERY_SUMMARY.md** — What was delivered
   - New files created
   - Files changed
   - Impact metrics

2. **FINAL_STATUS.md** — Completion checklist
   - Before/after comparison
   - Validation results
   - Metrics and impact

3. **YOUR_VISION_IMPLEMENTED.md** — How it works
   - Consulta sob medida explained
   - Practical examples
   - Execution awareness

4. **GOVERNANCE_BY_DOMAIN.md** — Copy of specs index
   - Reference convenience
   - Same info as specs/_INDEX_BY_DOMAIN.md

---

## 📋 REFERENCE

Lookup tables and definitions:

1. **FAQ.md** — Common questions and answers
   - "Why X?" type questions
   - "How do I Y?" type questions
   - Links to detailed docs

2. **GLOSSARY.md** — Terminology
   - Terms used in governance docs
   - Port names and meanings
   - Acronyms

---

## QUICK NAVIGATION

**"I'm new and starting now"** → `onboarding/FIRST_SESSION_SETUP.md`

**"I'm ready to code"** → `onboarding/QUICK_START.md` + `implementation/IMPLEMENTATION_ROADMAP.md`

**"I need to find something"** → `navigation/INDEX.md`

**"I need a reference card"** → `onboarding/SESSION_QUICK_REFERENCE.md`

**"I need to understand a decision"** → `specs/decisions/ADR-XXX.md`

**"What was delivered?"** → `context/DELIVERY_SUMMARY.md`

**"I'm stuck"** → `implementation/TROUBLESHOOTING.md`

---

## MIGRATION NOTE

Old structure (flat):
```
guides/
  ├─ QUICK_START.md
  ├─ FIRST_SESSION_SETUP.md
  ├─ INDEX.md
  ├─ IMPLEMENTATION_ROADMAP.md
  └─ ... (9 files)
```

New structure (organized):
```
guides/
  ├─ onboarding/
  │   ├─ QUICK_START.md ✓ moved
  │   ├─ FIRST_SESSION_SETUP.md ✓ moved
  │   └─ SESSION_QUICK_REFERENCE.md ✓ moved
  ├─ navigation/
  │   └─ INDEX.md ✓ moved
  ├─ implementation/
  │   └─ IMPLEMENTATION_ROADMAP.md ✓ moved
  ├─ context/
  │   ├─ DELIVERY_SUMMARY.md ✓ moved
  │   ├─ FINAL_STATUS.md ✓ moved
  │   └─ YOUR_VISION_IMPLEMENTED.md ✓ moved
  └─ reference/ (NEW)
      └─ (future FAQ, GLOSSARY)
```

Old files still exist at root level for compatibility during transition.
