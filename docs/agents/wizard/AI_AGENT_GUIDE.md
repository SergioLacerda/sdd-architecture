# 🤖 AI Agent Navigation Guide

**Optimized for AI agents working with SDD v3.0 Wizard**

---

## 🚀 Start Here (30 seconds)

**What am I looking at?**
- System: SDD v3.0 Governance Wizard
- Purpose: Transforms architect specifications into client projects
- Status: ✅ Production Ready (124/124 tests passing)
- Your role: Agent helping users/developers with this system

**Key fact:** Everything is deterministic, stateless, and fully auditable.

---

## 🧠 Mental Model (For Agents)

### The System in 3 Pictures

#### 1. What It Does
```
User Input:
  ├─ Language (python/java/js)
  ├─ Mandates (M001, M002, ...)
  └─ Project path

         ↓↓↓ WIZARD MAGIC (7 phases) ↓↓↓

Output:
  ├─ .sdd/CANONICAL/  (filtered specs)
  ├─ .sdd-guidelines/ (organized rules)
  ├─ src/             (scaffolds)
  └─ metadata.json    (audit trail)
```

#### 2. The 7 Phases
```
Phase 1: VALIDATE   → Check files exist
Phase 2: LOAD       → Read binary artifacts
Phase 3: FILTER     → User mandates only
Phase 4: ORGANIZE   → By language
Phase 5: SCAFFOLD   → Add templates
Phase 6: GENERATE   → Create structure
Phase 7: VALIDATE   → Verify output
```

#### 3. The Governance Model
```
CORE (Immutable)
├─ M001: Architecture
├─ M002: Performance
└─ [2 more mandates]

CLIENT (User Chooses)
├─ G001-G150: Guidelines
└─ [151 total - pick which to use]

Result: No profiles needed!
```

---

## 📖 How to Use This System

### ✅ To Answer "How does X work?"

| Question | Check | Time |
|----------|-------|------|
| "What are the 7 phases?" | [ORCHESTRATION.md](./ORCHESTRATION.md#-orchestration-pipeline) | 2 min |
| "How is data transformed?" | [WORKFLOW_FLOW.md](./WORKFLOW_FLOW.md#-complete-data-flow) | 5 min |
| "Why no profiles?" | [ARCHITECTURE_ALIGNMENT.md](./ARCHITECTURE_ALIGNMENT.md#-what-doesnt-exist-why-profiles-are-gone) | 3 min |
| "What's implemented?" | [IMPLEMENTATION_STATUS_v3.0.md](./IMPLEMENTATION_STATUS_v3.0.md#-implementation-matrix) | 5 min |
| "Is it production ready?" | [FINAL_STATUS.md](./FINAL_STATUS.md#-production-readiness-checklist) | 2 min |

### ✅ To Implement a Feature

| Task | Check | Then |
|------|-------|------|
| Add phase | [ORCHESTRATION.md](./ORCHESTRATION.md#implementation-phases) | Copy `phase_X_template.py` |
| Add language | [IMPLEMENTATION_STATUS_v3.0.md](./IMPLEMENTATION_STATUS_v3.0.md#-how-to-use-the-wizard) | Edit Phase 4 filter logic |
| Add guideline | [ARCHITECTURE_ALIGNMENT.md](./ARCHITECTURE_ALIGNMENT.md#-governance-architecture) | Edit `.sdd-core/guidelines.dsl` |
| Fix bug | [IMPLEMENTATION_STATUS_v3.0.md](./IMPLEMENTATION_STATUS_v3.0.md#-test-results) | Check corresponding test first |

### ✅ To Debug an Issue

| Problem | First Check | Then Check |
|---------|-------------|------------|
| "Phase X failing" | `tests/test_phases.py` | `orchestration/phase_X.py` code |
| "Output missing files" | [WORKFLOW_FLOW.md](./WORKFLOW_FLOW.md#-complete-data-flow) | `generators/` code |
| "Language not supported" | [IMPLEMENTATION_STATUS_v3.0.md](./IMPLEMENTATION_STATUS_v3.0.md#-language-support) | `orchestration/phase_4_filter_guidelines.py` |
| "Performance issue" | Check input size | Profile with `--verbose` flag |

---

## 🎯 Document Navigation Map

### By Purpose

**Need architecture understanding?**
```
START: README.md (this file) → ORCHESTRATION.md (5 min) → WORKFLOW_FLOW.md (10 min)
```

**Need implementation details?**
```
START: README.md → IMPLEMENTATION_STATUS_v3.0.md → src/ code
```

**Need to debug a problem?**
```
START: Find which phase fails → Check tests/test_phases.py → Read phase code → Check ORCHESTRATION.md for context
```

**Need production readiness info?**
```
START: FINAL_STATUS.md → DEPLOYMENT.md → MONITORING.md
```

### By Document

| File | Purpose | AI Agent Use | Time |
|------|---------|--------------|------|
| **README.md** | Navigation guide | Start here for orientation | 5 min |
| **ORCHESTRATION.md** | Technical architecture | Understand system design | 5 min |
| **WORKFLOW_FLOW.md** | Complete data flow | See all transformations | 10 min |
| **ARCHITECTURE_ALIGNMENT.md** | Governance model | Understand CORE+CLIENT | 5 min |
| **IMPLEMENTATION_STATUS_v3.0.md** | Implementation details | Learn what's built | 10 min |
| **FINAL_STATUS.md** | Executive summary | Get complete overview | 10 min |

---

## 🔍 Code Navigation Cheatsheet

### Entry Point
```
.sdd-wizard/src/wizard.py
  └─ parse arguments
  └─ call WizardOrchestrator
     └─ run_full_pipeline()
```

### Phase Implementations
```
orchestration/phase_1_validate_source.py     ← Validation logic
orchestration/phase_2_load_compiled.py       ← Binary loading
orchestration/phase_3_filter_mandates.py     ← User selection
orchestration/phase_4_filter_guidelines.py   ← Language filtering
orchestration/phase_5_apply_template.py      ← Template substitution
orchestration/phase_6_generate_project.py    ← Directory creation
orchestration/phase_7_validate_output.py     ← Output verification
```

### Support Modules
```
src/compile_artifacts.py    ← SOURCE → COMPILED conversion
src/validator.py            ← Input validation
src/loader.py               ← Load governance
```

### Generators
```
generators/manifest_generator.py      ← Create manifest
generators/metadata_generator.py      ← Create metadata
generators/guideline_markdown.py      ← Convert to markdown
```

### Testing
```
tests/test_orchestration.py   ← Full pipeline tests
tests/test_phases.py          ← Individual phase tests
tests/test_generators.py      ← Generator tests
tests/test_validators.py      ← Validator tests
```

---

## 💡 Key Concepts (For AI Understanding)

### Concept: Stateless Execution
```
Every run is INDEPENDENT
├─ No caching
├─ No state files
├─ Always-fresh artifacts
└─ Fully reproducible

Why? Auditability. Every result is fresh from SOURCE.
```

### Concept: Immutable Core
```
.sdd-core/ is THE TRUTH
├─ Nobody can bypass mandates
├─ SALT fingerprint proves integrity
├─ Client can customize around it
└─ But core never bends

Why? Governance integrity.
```

### Concept: User-Driven Customization
```
Before (v2.1): Framework decides (LITE, FULL, ULTRA-LITE)
After (v3.0):  User decides (pick which guidelines matter)

Why? No artificial buckets. Just "what we need".
```

### Concept: Filtered Propagation
```
M001, M002, M003, M004 (ALL MANDATES)
    ↓ User selects M001, M002
M001, M002 (USER'S MANDATES)
    ↓ Both get CORE hash fingerprint
VERIFIED M001, M002 (SAFE FOR DELIVERY)

Why? You only deliver what the user asked for.
```

---

## 🚨 Common Agent Tasks & Solutions

### Task: "Understand what the wizard does"
```
1. Read: README.md (this file)
2. Read: ORCHESTRATION.md section "The Motor"
3. Look at: src/wizard.py WizardOrchestrator.run_full_pipeline()
4. Verify: Run `python wizard.py --test-phases 1-7 --verbose`
```

### Task: "Debug Phase X failing"
```
1. Check: tests/test_phases.py for phase X test case
2. Read: orchestration/phase_X_description.py implementation
3. Trace: What data enters phase? What should exit?
4. Compare: With test expectations
5. Check: Error message vs. code logic
```

### Task: "Add support for language Y"
```
1. Read: ARCHITECTURE_ALIGNMENT.md section "Language Filtering"
2. Check: orchestration/phase_4_filter_guidelines.py
3. Add: Language to SUPPORTED_LANGUAGES constant
4. Implement: Language-specific filter logic
5. Test: Add test case in tests/test_filtering.py
```

### Task: "Generate a new project"
```
1. Check: IMPLEMENTATION_STATUS_v3.0.md "How to Use"
2. Run: python .sdd-wizard/src/wizard.py
3. Answer: Language? (python/java/js)
4. Answer: Which mandates? (M001, M002, ...)
5. Answer: Where to generate? (/path/to/project)
6. Verify: python .sdd-wizard/src/wizard.py --test-phases 1-7
```

### Task: "Understand SALT fingerprinting"
```
1. Read: ARCHITECTURE_ALIGNMENT.md section "SALT Protection"
2. See: How CORE hash is computed
3. See: How it's embedded in client metadata
4. See: How it prevents tampering
5. Check: src/compile_artifacts.py for implementation
```

---

## 🎓 Mental Model for New Agents

### Layer 1: System Purpose
```
SDD Framework problem: How to keep governance specifications
                       up-to-date with client projects?

Wizard solution: Automated 7-phase orchestration that:
  1. Loads specifications
  2. Filters by user choice
  3. Generates projects
  4. Validates output
```

### Layer 2: Data Flow
```
INPUT (what user wants):
  - Language: python
  - Mandates: M001, M002
  - Path: ~/project/

PROCESSING (what wizard does):
  - Validate source specs exist
  - Load compiled artifacts
  - Filter to user's mandates
  - Filter to python guidelines
  - Apply templates
  - Generate directory structure
  - Validate output

OUTPUT (what user gets):
  - Complete project structure
  - .sdd/ canonical specs
  - .sdd-guidelines/ organized rules
  - metadata.json (audit trail)
```

### Layer 3: Governance Model
```
IMMUTABLE (can't change):
  - 4 CORE mandates
  - Architecture rules
  - Performance SLOs

CUSTOMIZABLE (user picks):
  - Which guidelines to implement
  - How to organize them
  - What to prioritize

FINGERPRINTED (can't tamper with):
  - CORE hash embedded
  - Prevents core bypass
  - Verifies integrity
```

---

## ✅ Quality Signals

### When System Is Working Well
```
✅ All phases complete in <10s
✅ Generated project structure complete
✅ All 7 phases show GREEN status
✅ metadata.json has valid fingerprint
✅ No warnings in output
```

### Red Flags
```
❌ Phase fails with exception
❌ Missing files in generated project
❌ Fingerprint validation fails
❌ Metadata.json invalid
❌ More than 2-3 seconds per phase
```

---

## 🔗 AI Agent Quick References

### I'm Building Something With This
```
1. Understand workflow: WORKFLOW_FLOW.md (10 min)
2. See implementation: src/wizard.py (5 min)
3. Check tests: tests/ (5 min)
4. Integrate: Call WizardOrchestrator directly
```

### I'm Debugging Something
```
1. Identify phase: Which of 7 failed?
2. Check test: tests/test_phases.py for phase
3. Read code: orchestration/phase_X.py
4. Trace data: What in? What out?
```

### I'm Helping a User
```
1. What do they want? (generate project? understand flow? deploy?)
2. Point them to: See "Documentation by Audience" above
3. Run test: `python wizard.py --test-phases 1-7 --verbose`
4. Show output: Generated project in `.sdd/`
```

### I'm Deploying This
```
1. Read: DEPLOYMENT.md (.sdd-core/)
2. Check: FINAL_STATUS.md "Production Readiness"
3. Verify: All 124 tests passing
4. Monitor: Use MONITORING.md alerts
```

---

## 📊 One-Pager Facts

| Fact | Value | Link |
|------|-------|------|
| **Purpose** | Transform specs → projects | [README.md](./README.md) |
| **Phases** | 7 (validate, load, filter, scaffold, generate, validate) | [ORCHESTRATION.md](./ORCHESTRATION.md) |
| **Tests** | 124/124 passing | [FINAL_STATUS.md](./FINAL_STATUS.md) |
| **Status** | ✅ Production Ready | [FINAL_STATUS.md](./FINAL_STATUS.md) |
| **Governance** | 4 CORE + 151 CLIENT | [ARCHITECTURE_ALIGNMENT.md](./ARCHITECTURE_ALIGNMENT.md) |
| **Language Support** | Python, Java, JavaScript | [IMPLEMENTATION_STATUS_v3.0.md](./IMPLEMENTATION_STATUS_v3.0.md) |
| **Speed** | <10s per project | [WORKFLOW_FLOW.md](./WORKFLOW_FLOW.md) |
| **Immutability** | CORE fingerprinted | [ARCHITECTURE_ALIGNMENT.md](./ARCHITECTURE_ALIGNMENT.md) |
| **Profiles** | None (user-driven) | [ARCHITECTURE_ALIGNMENT.md](./ARCHITECTURE_ALIGNMENT.md) |
| **Version** | v3.0 Final | [FINAL_STATUS.md](./FINAL_STATUS.md) |

---

## 🎯 Quick Decision Trees

### "I need to understand X"

**"...how the system works?"**
→ ORCHESTRATION.md (5 min)

**"...how data flows through it?"**
→ WORKFLOW_FLOW.md (10 min)

**"...why there are no profiles?"**
→ ARCHITECTURE_ALIGNMENT.md (3 min)

**"...what's implemented?"**
→ IMPLEMENTATION_STATUS_v3.0.md (10 min)

**"...if it's production ready?"**
→ FINAL_STATUS.md (10 min)

### "I need to do X"

**"...add a new phase?"**
→ ORCHESTRATION.md → copy template → implement

**"...support a new language?"**
→ IMPLEMENTATION_STATUS_v3.0.md → edit phase 4

**"...debug a failing test?"**
→ tests/ → find test → trace phase code

**"...deploy this system?"**
→ .sdd-core/DEPLOYMENT.md → follow checklist

**"...monitor it in production?"**
→ .sdd-core/MONITORING.md → set up alerts

---

## 🤝 Agent-Friendly API

### Reading Documentation
```
When you read a .md file, look for:
1. Purpose statement (what does this explain?)
2. Diagrams/flowcharts (how does it work visually?)
3. Code references (where in src/ is this?)
4. Test cases (how is this verified?)
5. Links to related docs (what else should I know?)
```

### Understanding Code
```
When you read Python, look for:
1. Docstring (what does this do?)
2. Function signature (what goes in/out?)
3. Error handling (what can go wrong?)
4. State management (is it stateless?)
5. Dependencies (what else does it call?)
```

### Verifying Correctness
```
When verifying something works:
1. Check: Does a test exist? (tests/)
2. Run: Does test pass? (pytest)
3. Trace: Does data flow make sense? (trace through phases)
4. Verify: Does output match spec? (check metadata)
5. Confirm: Is fingerprint valid? (SHA-256 matches)
```

---

## 🎬 Getting Started (For New Agents)

### Scenario: "I just loaded the workspace, help me start"

**Step 1 (2 min):** Read this file (you're reading it!)

**Step 2 (5 min):** Read [README.md](./README.md) "Quick Start"

**Step 3 (5 min):** Read [ORCHESTRATION.md](./ORCHESTRATION.md) "Wizard's Role"

**Step 4 (5 min):** Look at [src/wizard.py](./src/wizard.py) - find `run_full_pipeline()`

**Step 5 (2 min):** Run test: `python wizard.py --test-phases 1-7 --verbose`

**Now you know:**
- ✅ What the system does
- ✅ How it's architectured
- ✅ Where the code is
- ✅ How to verify it works

**Time invested:** 20 min | **Knowledge gained:** Complete system understanding

---

**Last Updated:** April 22, 2026  
**Version:** SDD v3.0 Final  
**Audience:** AI Agents working with SDD Wizard  
**Status:** ✅ Approved for use
