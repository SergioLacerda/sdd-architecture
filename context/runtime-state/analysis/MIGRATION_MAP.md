# 📊 Structural Reorganization — Migration Map

**This document shows how existing files are reorganized into INTEGRATION/ and EXECUTION/ flows.**

---

## 📦 Existing Structure → New Structure

### Current State (Before Reorganization)

```
sdd-archtecture/
├── README.md                    ← OLD (monolithic)
├── INTEGRATION.md               ← OLD (standalone)
├── PHASE-7-DELIVERY-SUMMARY.md
├── docs/
│   ├── ia/
│   │   ├── _INDEX.md
│   │   ├── MASTER_INDEX.md
│   │   ├── CANONICAL/
│   │   ├── guides/
│   │   ├── custom/
│   │   ├── SCRIPTS/
│   │   └── runtime/
│   └── (other docs)
├── templates/                   ← Templates
├── tests/spec_validation/
├── .spec.config
└── (other files)
```

---

## 🗺️ Migration Plan

| Old Location | New Location | Why |
|--------------|--------------|-----|
| `README.md` | `README_NEW.md` (replace old) | Decision tree for INTEGRATION vs EXECUTION |
| `INTEGRATION.md` | Moved/archived | Old standalone doc, replaced by INTEGRATION/ |
| `templates/` | `INTEGRATION/templates/` | Belongs to integration flow |
| `docs/ia/` | `EXECUTION/spec/` | Used during execution workflow |
| `docs/ia/CANONICAL/` | `EXECUTION/spec/CANONICAL/` | Specs used during EXECUTION |
| `docs/ia/guides/` | `EXECUTION/spec/guides/` | Guides used during EXECUTION |
| `docs/ia/custom/` | `EXECUTION/spec/custom/` | Project-specific during EXECUTION |
| `docs/ia/SCRIPTS/` | `EXECUTION/spec/SCRIPTS/` | Tools used during EXECUTION |
| `docs/ia/runtime/` | `EXECUTION/spec/runtime/` | Search indices for EXECUTION |
| `tests/spec_validation/` | `EXECUTION/tests/` | Validation tests for framework |
| `PHASE-7-DELIVERY-SUMMARY.md` | `docs/audit/` | Audit document (not flow-critical) |
| `docs/ia/_INDEX.md` | Removed | Replaced by local EXECUTION/INDEX.md |
| `docs/ia/MASTER_INDEX.md` | Removed | Replaced by NAVIGATION.md |

---

## 🎯 Target Structure (After Reorganization)

```
sdd-archtecture/
│
├── README.md ✅ NEW                    ← Decision map (pick INTEGRATION or EXECUTION)
├── .spec.config
│
├── INTEGRATION/                        ← New folder
│   ├── README.md ✅ NEW                ← Integration overview
│   ├── INDEX.md ✅ NEW                 ← Local index
│   ├── CHECKLIST.md                    ← 5-step process
│   ├── STEP_1_SETUP.md                 ← Step guides
│   ├── STEP_2_TEMPLATES.md
│   ├── STEP_3_CONFIG.md
│   ├── STEP_4_VALIDATE.md
│   ├── STEP_5_COMMIT.md
│   └── templates/                      ← Moved from ./templates/
│       ├── .spec.config
│       ├── .github/
│       ├── .vscode/
│       ├── .cursor/
│       ├── scripts/
│       └── ai/
│
├── EXECUTION/                          ← New folder
│   ├── README.md ✅ NEW                ← Execution overview
│   ├── INDEX.md ✅ NEW                 ← Local index
│   ├── _START_HERE.md ✅ NEW           ← 5-scenario entry point
│   ├── NAVIGATION.md ✅ NEW            ← Task-based search
│   │
│   ├── docs/
│   │   └── ia/                         ← Moved from ./docs/ia/
│   │       ├── CANONICAL/
│   │       │   ├── rules/
│   │       │   ├── decisions/
│   │       │   └── specifications/
│   │       ├── guides/
│   │       │   ├── onboarding/
│   │       │   ├── operational/
│   │       │   ├── emergency/
│   │       │   ├── reference/
│   │       │   └── README.md
│   │       ├── custom/
│   │       ├── runtime/
│   │       ├── SCRIPTS/
│   │       └── README.md
│   │
│   └── tests/                          ← Moved from ./tests/
│       └── spec_validation/
│
├── docs/
│   ├── audit/                          ← New folder (cleanup)
│   │   ├── PHASE-7-DELIVERY-SUMMARY.md ← Moved from root
│   │   └── (other session/audit docs)
│   └── (other documentation)
│
├── LICENSE, .gitignore, etc.
└── (CI/CD config, etc.)
```

---

## ✅ File Checklist

### To Create (New Files)

- [ ] `README_NEW.md` → Rename to `README.md` after validation
- [ ] `INTEGRATION/README.md` ✅ Created
- [ ] `INTEGRATION/INDEX.md` ✅ Created
- [ ] `INTEGRATION/CHECKLIST.md` (pending)
- [ ] `INTEGRATION/STEP_1_SETUP.md` (pending)
- [ ] `INTEGRATION/STEP_2_TEMPLATES.md` (pending)
- [ ] `INTEGRATION/STEP_3_CONFIG.md` (pending)
- [ ] `INTEGRATION/STEP_4_VALIDATE.md` (pending)
- [ ] `INTEGRATION/STEP_5_COMMIT.md` (pending)
- [ ] `EXECUTION/README.md` ✅ Created
- [ ] `EXECUTION/INDEX.md` ✅ Created
- [ ] `EXECUTION/_START_HERE.md` ✅ Created
- [ ] `EXECUTION/NAVIGATION.md` ✅ Created

### To Move (Files)

- [ ] `templates/` → `INTEGRATION/templates/`
- [ ] `docs/ia/` → `EXECUTION/spec/`
- [ ] `tests/spec_validation/` → `EXECUTION/tests/`

### To Archive (Audit)

- [ ] `PHASE-7-DELIVERY-SUMMARY.md` → `docs/audit/`
- [ ] `docs/ia/_INDEX.md` → `docs/audit/` (old index)
- [ ] `docs/ia/MASTER_INDEX.md` → `docs/audit/` (old index)
- [ ] `INTEGRATION.md` → `docs/audit/` (old standalone doc)

### To Delete (Redundant)

- [ ] Old `README.md` (after `README_NEW.md` is renamed)

---

## 🚀 Implementation Phases

### Phase 1: Create New Entry Points ✅ DONE
- [x] Create `README_NEW.md` (decision map)
- [x] Create `INTEGRATION/README.md`
- [x] Create `INTEGRATION/INDEX.md`
- [x] Create `EXECUTION/README.md`
- [x] Create `EXECUTION/INDEX.md`
- [x] Create `EXECUTION/_START_HERE.md`
- [x] Create `EXECUTION/NAVIGATION.md`

### Phase 2: Create Step Guides (PENDING)
- [ ] Create `INTEGRATION/CHECKLIST.md`
- [ ] Create `INTEGRATION/STEP_1_SETUP.md`
- [ ] Create `INTEGRATION/STEP_2_TEMPLATES.md`
- [ ] Create `INTEGRATION/STEP_3_CONFIG.md`
- [ ] Create `INTEGRATION/STEP_4_VALIDATE.md`
- [ ] Create `INTEGRATION/STEP_5_COMMIT.md`

### Phase 3: Move Directories (PENDING)
- [ ] Create `EXECUTION/docs/` directory
- [ ] Move `docs/ia/` → `EXECUTION/spec/`
- [ ] Move `templates/` → `INTEGRATION/templates/`
- [ ] Move `tests/spec_validation/` → `EXECUTION/tests/spec_validation/`

### Phase 4: Archive & Cleanup (PENDING)
- [ ] Create `docs/audit/` directory
- [ ] Move audit files to `docs/audit/`
- [ ] Delete old `.README.md` (after validation)
- [ ] Update `.gitignore` if needed

### Phase 5: Validate Structure (PENDING)
- [ ] Check all symlinks/references still work
- [ ] Test INTEGRATION flow (can new project follow it?)
- [ ] Test EXECUTION flow (can agent use it?)
- [ ] Verify search indices point to right files
- [ ] Git status check (all files accounted for)

### Phase 6: Update & Commit (PENDING)
- [ ] Update root `.spec.config` if needed
- [ ] Create git commit
- [ ] Document changes in commit message

---

## 🎯 World-Class Engineering Validation

**After reorganization, verify:**

| Criteria | Check |
|----------|-------|
| **Separation** | No INTEGRATION docs reference EXECUTION details; vice versa |
| **Independence** | New project can use INTEGRATION/ without seeing EXECUTION/ |
| **Clarity** | Each doc has clear purpose; no ambiguous double-purposes |
| **Scalability** | New projects won't clutter existing structures |
| **Maintainability** | Updating one flow doesn't break other |
| **Testability** | Each flow has own success metrics |

---

## 📝 Reference: Existing File Locations

### In docs/ia/CANONICAL/

```
docs/ia/CANONICAL/
├── rules/
│   ├── constitution.md
│   ├── ia-rules.md
│   └── conventions.md
├── decisions/
│   ├── ADR-001-autonomous-agents.md
│   ├── ADR-002-three-layer-architecture.md
│   ├── ADR-003-ports-adapters-pattern.md
│   ├── ADR-004-isolated-testing.md
│   ├── ADR-005-thread-isolation-mandatory.md
│   └── ADR-006-governance-automation.md
└── specifications/
    ├── architecture.md
    ├── testing.md
    ├── feature-checklist.md
    ├── definition-of-done.md
    └── communication.md
```

### In docs/ia/guides/

```
docs/ia/guides/
├── onboarding/
│   ├── PHASE-0-AGENT-ONBOARDING.md
│   ├── AGENT_HARNESS.md
│   └── (others)
├── operational/
│   ├── DEVELOPMENT_WORKFLOW_VALIDATION.md
│   ├── METRICS_TRACKING.md
│   ├── PRE_COMMIT_HOOKS.md
│   └── (others)
├── emergency/
│   ├── README.md
│   ├── PRE_COMMIT_HOOK_FAILURE.md
│   ├── TEST_FAILURE_GUIDE.md
│   ├── RULES_VIOLATION_DETECTED.md
│   ├── IMPORTS_CORRUPTED.md
│   └── METRICS_CORRUPTION_RECOVERY.md
└── reference/
    ├── FAQ.md
    ├── GLOSSARY.md
    └── HOW_EACH_LAYER_WORKS.md
```

### In docs/ia/custom/

```
docs/ia/custom/
└── [project-name]/
    ├── SPECIALIZATIONS/
    └── development/
        └── execution-state/
            ├── _current.md
            └── (checkpoint history)
```

---

## 🔄 Validation Checklist

Before considering reorganization complete:

- [ ] All links still resolve
- [ ] No broken references
- [ ] Both INTEGRATION/ and EXECUTION/ are self-contained
- [ ] New project can follow INTEGRATION/ alone
- [ ] Developer can use EXECUTION/ alone
- [ ] Search indices point to correct locations
- [ ] Pre-commit hooks still work
- [ ] CI/CD validates correctly

---

**Status:** Migration plan defined, Phase 1 complete  
**Next:** Phase 2 (create step guides)  
**Updated:** April 19, 2026
