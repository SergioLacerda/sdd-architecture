# 🎼 SDD Wizard Orchestration

**The Motor That Drives the Entire Workflow**

---

## 📋 Wizard's Role

The Wizard is the **central orchestrator** that:
1. Reads user input (language, mandates, profile)
2. Loads SOURCE from `.sdd-core/` (validation)
3. Reads COMPILED from `.sdd-runtime/` (binary)
4. Applies SCAFFOLD from `.sdd-template/` (base files)
5. Generates final TEMPLATE (filters & customizes)
6. Outputs to CLIENT DELIVERY `.sdd/` (final product)

---

## 🎯 Orchestration Pipeline

```
┌─ USER INPUT ────────────────────────────────────────┐
│ • Language: Java / Python / JS                      │
│ • Mandates: Select M001, M002, ...                  │
│ • Profile: ULTRA-LITE / LITE / FULL                │
│ • Destination: /path/to/my-project/                │
└───────────────┬──────────────────────────────────────┘
                │
                ↓ PHASE 1: VALIDATE & LOAD
┌────────────────────────────────────────────────────┐
│ Check SOURCE Integrity                             │
│ • Read .sdd-core/mandate.spec (architect source)   │
│ • Read .sdd-core/guidelines.dsl (architect source) │
│ • Validate DSL syntax & semantics                  │
│ • Confirm all references are valid                 │
└───────────────┬──────────────────────────────────────┘
                │
                ↓ PHASE 2: LOAD COMPILED
┌────────────────────────────────────────────────────┐
│ Read Compiled Artifacts                            │
│ • Load .sdd-runtime/mandate.bin (msgpack)          │
│ • Load .sdd-runtime/guidelines.bin (msgpack)       │
│ • Load .sdd-runtime/metadata.json (audit trail)    │
│ • Decompress & deserialize binary format           │
└───────────────┬──────────────────────────────────────┘
                │
                ↓ PHASE 3: FILTER BY MANDATE SELECTION
┌────────────────────────────────────────────────────┐
│ User Selected Mandates                             │
│ • Extract M001 (user chose)                        │
│ • Extract M002 (user chose)                        │
│ • Skip M003, M004, ... (not selected)              │
│ • Build filtered mandate.spec                      │
└───────────────┬──────────────────────────────────────┘
                │
                ↓ PHASE 4: FILTER GUIDELINES BY LANGUAGE & PROFILE
┌────────────────────────────────────────────────────┐
│ Guidelines Filtering Pipeline                      │
│ • Filter by LANGUAGE (remove irrelevant guides)    │
│ • Filter by PROFILE (LITE=essential only)          │
│ • Organize by CATEGORY (git, testing, naming, ...) │
│ • Generate .md files per category                  │
└───────────────┬──────────────────────────────────────┘
                │
                ↓ PHASE 5: APPLY SCAFFOLD
┌────────────────────────────────────────────────────┐
│ Load Base Template                                 │
│ • Copy .sdd-template/base/ files                   │
│ • Substitute PLACEHOLDERS:                         │
│   - {{TIMESTAMP}} → current time                   │
│   - {{SOURCE_HASH}} → hash of sources              │
│   - {{MANDATES}} → selected mandate list           │
│   - {{LANGUAGE}} → java/python/js                  │
│   - {{PROFILE}} → ultra-lite/lite/full             │
│ • Load language-specific scaffold                  │
│ • Load profile-specific templates (v3.2+)         │
└───────────────┬──────────────────────────────────────┘
                │
                ↓ PHASE 6: GENERATE PROJECT STRUCTURE
┌────────────────────────────────────────────────────┐
│ Create Final Template                              │
│ • mkdir -p /path/to/my-project/.sdd/CANONICAL/    │
│ • mkdir -p /path/to/my-project/.sdd-guidelines/   │
│ • mkdir -p /path/to/my-project/src/               │
│ • mkdir -p /path/to/my-project/.github/workflows/ │
│ • Write filtered mandate.spec to .sdd/CANONICAL/  │
│ • Write filtered guidelines.dsl to .sdd/CANONICAL/│
│ • Generate .sdd-guidelines/*.md files              │
│ • Copy examples/ to .sdd/examples/                 │
│ • Write metadata.json with compile info           │
│ • Copy CI/CD workflows from .sdd-template/        │
│ • Add build files (pom.xml, requirements.txt, etc)│
│ • Copy README-SDD.md from .sdd-template/base/     │
└───────────────┬──────────────────────────────────────┘
                │
                ↓ PHASE 7: VALIDATE OUTPUT
┌────────────────────────────────────────────────────┐
│ Verify Deliverable                                 │
│ • Check all required files exist                   │
│ • Verify directory structure integrity             │
│ • Validate mandates can be parsed                  │
│ • Validate guidelines can be read                  │
│ • Run basic tests (project structure)              │
└───────────────┬──────────────────────────────────────┘
                │
                ↓ SUCCESS
┌────────────────────────────────────────────────────┐
│ Client Receives                                    │
│ /path/to/my-project/                              │
│ ├── .sdd/                    (compiled specs)      │
│ ├── .sdd-guidelines/         (organized guides)    │
│ ├── src/                     (code structure)      │
│ ├── .github/workflows/       (CI/CD)               │
│ ├── pom.xml/requirements.txt (build config)        │
│ ├── README.md                (project README)      │
│ └── README-SDD.md            (SDD setup guide)     │
└────────────────────────────────────────────────────┘
```

---

## 🔧 Implementation Phases

### Phase A: Orchestrator Core (Current - v3.0)
- [x] Reads SOURCE (.sdd-core/)
- [x] Reads COMPILED (.sdd-runtime/)
- [ ] User input collection (interactive prompts)
- [ ] Mandate selection & filtering
- [ ] Guideline filtering by language + profile
- [ ] Template generation

### Phase B: Advanced Filtering (v3.1)
- [ ] Category-based guideline organization
- [ ] Language-specific examples
- [ ] Profile-specific content selection

### Phase C: Customization (v3.2)
- [ ] .sdd-custom/ support (user overrides)
- [ ] Local mandate extensions
- [ ] Guideline remixing

### Phase D: CI/CD Integration (v3.3+)
- [ ] GitHub Actions trigger
- [ ] Automated template updates
- [ ] Version tracking

---

## 📌 Key Design Decisions

1. **Stateless Execution**
   - Each wizard run is independent
   - No state persisted between runs
   - Idempotent output

2. **Always Fresh**
   - Always reads latest .sdd-core/ (architect edits)
   - Always reads latest .sdd-runtime/ (compiled)
   - Always uses latest .sdd-template/ (scaffolds)

3. **Immutable Delivery**
   - Generated `.sdd/` is read-only for client
   - Client cannot edit `.sdd/` directly
   - Client customizations go to `.sdd-custom/` (v3.2+)

4. **Auditability**
   - metadata.json tracks source version
   - metadata.json tracks compile timestamp
   - metadata.json tracks user selections
   - Client can verify template lineage

---

## 💾 Implementation Structure

```
.sdd-wizard/
├── ORCHESTRATION.md              (This file - architecture & phases)
├── WORKFLOW_FLOW.md              (Detailed flow diagrams & interactions)
├── src/
│   ├── wizard.py                 (Main orchestrator entry point)
│   ├── loader.py                 (Load SOURCE + COMPILED artifacts)
│   ├── validator.py              (Validate inputs & artifacts)
│   ├── filter.py                 (Mandate & guideline filtering)
│   ├── generator.py              (Template generation & substitution)
│   ├── user_input.py             (Interactive prompts)
│   └── config.py                 (Configuration & constants)
├── orchestration/
│   ├── phase_1_validate.py        (Validate SOURCE)
│   ├── phase_2_load_compiled.py   (Load COMPILED)
│   ├── phase_3_filter_mandates.py (Filter by user selection)
│   ├── phase_4_filter_guidelines.py (Filter by lang + profile)
│   ├── phase_5_apply_scaffold.py  (Apply base template)
│   ├── phase_6_generate.py        (Generate final template)
│   └── phase_7_validate.py        (Validate output)
├── generators/
│   ├── manifest_generator.py      (Generate project manifest)
│   ├── metadata_generator.py      (Generate metadata.json)
│   └── guideline_markdown.py      (Generate .md from categories)
├── validators/
│   ├── source_validator.py        (Validate .sdd-core/)
│   ├── compiled_validator.py      (Validate .sdd-runtime/)
│   ├── output_validator.py        (Validate generated template)
│   └── dependency_validator.py    (Check all dependencies exist)
└── tests/
    ├── test_orchestration.py      (End-to-end workflow tests)
    ├── test_phases.py             (Individual phase tests)
    ├── test_filtering.py          (Filter logic tests)
    └── test_generators.py         (Generator output tests)
```

---

## 🚀 Usage

```bash
# Interactive mode (v3.0+)
python .sdd-wizard/src/wizard.py

# Non-interactive mode (v3.1+)
python .sdd-wizard/src/wizard.py \
  --language java \
  --mandates M001,M002 \
  --profile lite \
  --output ~/my-project/

# Verbose mode
python .sdd-wizard/src/wizard.py --verbose --dry-run
```
