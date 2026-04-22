# 📚 SPEC Framework — Governance & Documentation  

**Version:** 2.0 (April 2026 Restructuring)  
**Status:** ✅ Multi-Project Ready  
**Last Updated:** April 19, 2026

---

## 🎯 Quick Navigation

→ **New to SPEC?** Start at [_INDEX.md](./_INDEX.md) (5 min)  
→ **Need rules?** See [CANONICAL/rules/ia-rules.md](./CANONICAL/rules/ia-rules.md) (10 min)  
→ **Need architecture?** See [CANONICAL/specifications/architecture.md](./CANONICAL/specifications/architecture.md) (15 min)  
→ **Project-specific?** See [custom/rpg-narrative-server/](./custom/rpg-narrative-server/) ⭐ **START HERE**

---

## 🏗️ 4-Layer Architecture (AI-FIRST Designed)

> **IA-FIRST PRINCIPLE:** All documentation is structured for both human reading and machine analysis. Consistent hierarchies, explicit markers, structured metadata.

### Layer 1: CANONICAL/ ✅ **Immutable Global Authority**

**What:** Generic rules, principles, and specifications shared by ALL projects.  
**How to identify:** No project-specific terms (no "campaign", "rpg-narrative-server", etc.)  
**Update frequency:** Quarterly  
**Inheritance:** 100% automatic by all new projects

```
CANONICAL/
├── rules/                (16 mandatory protocols)
│   ├── ia-rules.md       (execution rules for AI agents)
│   ├── constitution.md   (15 immutable principles)
│   ├── conventions.md    (coding standards)
│   ├── ENFORCEMENT_RULES.md
│   └── backward-compatibility-policy.md
├── specifications/       (design blueprints)
│   ├── architecture.md   (8-layer clean + ports & adapters)
│   ├── definition_of_done.md
│   ├── feature-checklist.md
│   ├── testing.md
│   ├── observability.md
│   ├── security-model.md
│   ├── performance.md
│   └── compliance.md
└── decisions/            (6 Architecture Decision Records)
    ├── ADR-001.md through ADR-006.md (6 Architecture Decision Records)
```

**Key metrics:**  
- 24 files (288 KB)
- 100% generic (reusable by any project)
- Read-only during active development

---

### Layer 2: custom/ 🎨 **Project-Specific Specializations**

**What:** Project-specific mappings and implementations (one folder per project).  
**Structure:** Each project has identical subdirectories (DRY template).  
**Inheritance:** Each project extends CANONICAL + customizes via SPECIALIZATIONS.

#### **_TEMPLATE/** — Starter for New Projects
```
_TEMPLATE/
├── README.md                      (how to use)
├── INTEGRATION_CHECKLIST.md       (4-phase setup)
├── SPECIALIZATIONS/               (mappings from CANONICAL)
├── development/                   (active work)
└── reality/                       (system state)
```

#### **rpg-narrative-server/** — Demonstration Project ⭐
```
custom/rpg-narrative-server/
├── README.md                      (project description)
├── INTEGRATION_RESULTS.md         (integration details)
├── SPECIALIZATIONS/               (generic → project-specific)
│   ├── README.md
│   ├── ia-rules-rpg-specific.md   (project paths, services)
│   └── constitution-rpg-specific.md (campaign patterns)
├── development/                   (active threads, ephemeral)
│   └── execution-state/
│       ├── _current.md            (current status + next actions)
│       └── threads/               (active work threads)
├── reality/                       (observed system state, evolving)
│   ├── current-system-state/
│   │   ├── services.md
│   │   └── contracts.md
│   ├── limitations/
│   │   ├── known_issues.md
│   │   ├── storage_limitations.md
│   │   └── threading_concurrency.md
│   └── observations/
│       └── future_improvements.md
└── archive/                       (completed work, historical)
    ├── deprecated-decisions/
    ├── legacy-documentation/
    └── working-sessions/
```

---

### Layer 3: guides/ 📖 **Navigation & Learning**

**What:** How-to guides, navigation aids, and learning resources (shared by all projects).  
**Purpose:** Help developers find what they need quickly.

```
guides/
├── _INDEX.md                      (START HERE - task-based navigation)
├── MIGRATION_APRIL_2026.md        (structure changes + transition guide)
├── onboarding/                    (getting started)
│   ├── QUICK_START.md
│   ├── FIRST_SESSION_SETUP.md
│   └── VALIDATION_QUIZ.md
├── implementation/                (step-by-step guides)
│   ├── IMPLEMENTATION_ROADMAP.md
│   └── ADAPTIVE_CONTEXT_LOADING.md
├── navigation/                    (finding information)
│   └── REUSABILITY_GUIDE.md
└── reference/                     (quick lookup)
    ├── FAQ.md
    ├── GLOSSARY.md
    └── SESSION_QUICK_REFERENCE.md
```

---

### Layer 4: development/_SHARED/ 🔄 **Cross-Project Coordination**

**What:** Shared state between multiple projects (if integrated).  
**Purpose:** Synchronize work across projects.

```
development/_SHARED/
├── execution-state-matrix.md      (all active threads across projects)
├── threading-status.md            (concurrency coordination)
└── active-threads.md              (global state)
```

---

## 🎯 IA-FIRST Design Principles

1. **Explicit Structure** — All docs use consistent heading hierarchies (H1→H2→H3)
2. **Clear Markers** — Section types marked: `### 🏗️ [Name]`, `### 🎯 [Name]`, etc.
3. **Machine-Readable** — Code blocks, tables, lists (not prose paragraphs)
4. **Metadata in Headers** — Context clues in titles (✅, ❌, 📍, 🚀, etc.)
5. **No Language Mixing** — 100% English (no Portuguese remnants)
6. **One Idea Per Section** — Easy for AI to parse and reuse

---

## 📖 Reading Paths by Role

### **Backend Developer**
1. Read: [CANONICAL/rules/ia-rules.md](./CANONICAL/rules/ia-rules.md) (mandatory)
2. Read: [CANONICAL/specifications/architecture.md](./CANONICAL/specifications/architecture.md) (design)
3. Read: [custom/rpg-narrative-server/SPECIALIZATIONS/](./custom/rpg-narrative-server/SPECIALIZATIONS/) (project specifics)
4. Reference: [custom/rpg-narrative-server/reality/](./custom/rpg-narrative-server/reality/) (current state)

### **DevOps / Infrastructure**
1. Read: [CANONICAL/specifications/performance.md](./CANONICAL/specifications/performance.md) (SLOs)
2. Read: [CANONICAL/specifications/observability.md](./CANONICAL/specifications/observability.md) (logging/tracing)
3. Reference: [custom/rpg-narrative-server/reality/limitations/](./custom/rpg-narrative-server/reality/limitations/) (constraints)

### **Product Manager / Architect**
1. Read: [CANONICAL/rules/constitution.md](./CANONICAL/rules/constitution.md) (principles)
2. Read: [CANONICAL/decisions/](./CANONICAL/decisions/) (why decisions were made)
3. Reference: [custom/rpg-narrative-server/development/execution-state/](./custom/rpg-narrative-server/development/execution-state/) (progress)

---

## 🎯 Common Tasks

| Task | Start Here | Time |
|------|-----------|------|
| **Learn the framework** | [guides/_INDEX.md](./guides/_INDEX.md) | 5 min |
| **Fix a bug** | [custom/rpg-narrative-server/reality/limitations/known_issues.md](./custom/rpg-narrative-server/reality/limitations/known_issues.md) | 15 min |
| **Implement feature** | [CANONICAL/specifications/feature-checklist.md](./CANONICAL/specifications/feature-checklist.md) | 20 min |
| **Understand decision** | [CANONICAL/decisions/ADR-001.md](./CANONICAL/decisions/ADR-001.md) | 10 min |
| **Start new project** | [custom/_TEMPLATE/README.md](./custom/_TEMPLATE/README.md) | 2h |
| **Understand performance** | [CANONICAL/specifications/performance.md](./CANONICAL/specifications/performance.md) | 15 min |

---

## 📊 Structure Statistics

| Layer | Files | Size | Purpose |
|-------|-------|------|---------|
| **CANONICAL/** | 24 | 288 KB | Generic (all projects inherit) |
| **custom/rpg-narrative-server/** | 30 | 156 KB | Project-specific (rpg-narrative-server) |
| **custom/_TEMPLATE/** | 8 | 48 KB | Starter for new projects |
| **guides/** | 24 | 288 KB | Navigation & learning |
| **Total active** | 86 | ~780 KB | Loaded during development |

---

## ✅ Architecture Guarantees

1. **CANONICAL is 100% Generic** — No project names, no project-specific terminology
2. **No Duplication** — Each principle written once in CANONICAL
3. **Automatic Inheritance** — New projects automatically inherit all CANONICAL rules
4. **Clear Override Mechanism** — SPECIALIZATIONS map generic → specific
5. **AI-First Design** — All docs structured for both humans and machines
6. **100% English** — No language mixing (Portuguese remnants cleaned)

---

## 🚀 Getting Started (3 paths)

### **Path A: I want to understand the rules** (10 min)
```bash
1. Read: _INDEX.md
2. Read: CANONICAL/rules/ia-rules.md
3. Read: CANONICAL/rules/constitution.md
```

### **Path B: I want to implement something** (30 min)
```bash
1. Read: guides/_INDEX.md
2. Read: CANONICAL/specifications/architecture.md
3. Read: CANONICAL/specifications/feature-checklist.md
4. Read: custom/rpg-narrative-server/SPECIALIZATIONS/
```

### **Path C: I want to start a new project** (2 hours)
```bash
1. Copy: custom/_TEMPLATE/ → custom/my-project/
2. Follow: INTEGRATION_CHECKLIST.md
3. Create SPECIALIZATIONS/ mappings
4. Document in reality/ directory
```

---

## 📍 Key Files by Purpose

**When you need to...**

| Need | File | Why |
|------|------|-----|
| Understand mandatory rules | `CANONICAL/rules/ia-rules.md` | 16 non-negotiable protocols |
| Understand principles | `CANONICAL/rules/constitution.md` | 15 architectural principles |
| Design architecture | `CANONICAL/specifications/architecture.md` | 8-layer pattern + ports |
| Check definition of done | `CANONICAL/specifications/definition_of_done.md` | 45+ item completion checklist |
| Understand a design decision | `CANONICAL/decisions/ADR-*.md` | Rationale + context |
| Project-specific details | `custom/rpg-narrative-server/SPECIALIZATIONS/*` | Campaign-specific implementations |
| Current system state | `custom/rpg-narrative-server/reality/current-system-state/` | What exists now |
| Active work | `custom/rpg-narrative-server/development/execution-state/_current.md` | What's being worked on |
| Known issues | `custom/rpg-narrative-server/reality/limitations/known_issues.md` | What's broken |
| Navigate docs | `guides/_INDEX.md` | Start here (task-based nav) |

---

## 🔄 Moving Between Projects

**When adding a new project to SPEC:**

1. Copy `custom/_TEMPLATE/` → `custom/new-project/`
2. Automatically inherits 100% of CANONICAL/
3. Create `SPECIALIZATIONS/` directory with project-specific docs
4. Document project state in `reality/`
5. Track active work in `development/execution-state/`

**All projects get:**
- Same architecture rules
- Same testing standards
- Same observability requirements
- Same security model
- (But each project specializes as needed)

1. Read: [CANONICAL/decisions/](./CANONICAL/decisions/) - Review relevant ADRs (15 minutes)
2. Start: Phase 1 implementation using 8 decisions as blueprint
3. Reference: [CANONICAL/specifications/architecture.md](./CANONICAL/specifications/architecture.md) during coding
4. Check: [CANONICAL/specifications/definition_of_done.md](./CANONICAL/specifications/definition_of_done.md) before PR

---

**Status:** ✅ ANALYSIS COMPLETE | SPEC CONSOLIDATED | READY FOR CODING

**Questions?** Check [MASTER_INDEX.md](./MASTER_INDEX.md) for navigation help.
