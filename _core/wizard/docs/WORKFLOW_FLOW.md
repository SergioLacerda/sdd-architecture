# 🔄 SDD v3.0 Complete Workflow Flow

**End-to-End orchestration from architect edits to client delivery**

---

## 📊 Complete System Architecture

```
┌────────────────────────────────────────────────────────────────────┐
│                         ARCHITECT WORKSPACE                        │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  .sdd-core/                    (SOURCE)                            │
│  ├── mandate.spec              (2 mandates, edited by architect)  │
│  └── guidelines.dsl            (150 guidelines, edited)           │
│                                                                    │
│  Git Workflow (ADR-008):                                          │
│  • Edit on WIP branch          (wip/update-*)                    │
│  • Push to origin               (origin/wip/*)                   │
│  • Create PR on GitHub          (needs architect approval)        │
│  • Architect merges to main     (only way to main)               │
│                                                                    │
└──────────────────────────┬───────────────────────────────────────┘
                           │
                           ↓ ON COMMIT TO MAIN
┌────────────────────────────────────────────────────────────────────┐
│                        CI/CD PIPELINE                              │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  1. GitHub Actions Trigger                                        │
│     → on: push to main                                           │
│                                                                    │
│  2. Run Compiler (.sdd-compiler/)                                │
│     → Read .sdd-core/mandate.spec                               │
│     → Read .sdd-core/guidelines.dsl                             │
│     → Validate DSL syntax                                        │
│     → Compile to MessagePack binary                              │
│     → Output to .sdd-runtime/mandate.bin                         │
│     → Output to .sdd-runtime/guidelines.bin                      │
│     → Generate .sdd-runtime/metadata.json                        │
│                                                                    │
│  3. Run Tests                                                     │
│     → Test migration (test_migration_v2_to_v3.py)               │
│     → Test compiler (test_compiler.py)                           │
│     → Test core (111+ core tests)                               │
│     → All must PASS before commit                               │
│                                                                    │
│  4. Commit Compiled Artifacts (auto-commit by CI/CD)            │
│     → .sdd-runtime/mandate.bin                                   │
│     → .sdd-runtime/guidelines.bin                                │
│     → .sdd-runtime/metadata.json                                 │
│     → Commit message: "chore: recompile artifacts"              │
│                                                                    │
└──────────────────────────┬───────────────────────────────────────┘
                           │
                           ↓ NOW READY FOR WIZARD
┌────────────────────────────────────────────────────────────────────┐
│                    .SDD-WIZARD ORCHESTRATION                       │
│                    "The Motor That Drives It All"                  │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  INPUTS (from wizard user):                                       │
│  • Language: java | python | js                                  │
│  • Mandates: M001, M002, ... (user selects or all)              │
│  • Destination: /path/to/my-project/                             │
│                                                                    │
│  ┌─ PHASE 1: VALIDATE SOURCE ──────────────────────────┐         │
│  │ Reads: .sdd-core/mandate.spec                        │         │
│  │ Reads: .sdd-core/guidelines.dsl                      │         │
│  │ Checks: DSL syntax valid                             │         │
│  │ Checks: All references resolvable                    │         │
│  │ Output: ✅ SOURCE integrity confirmed                │         │
│  └──────────────────────┬───────────────────────────────┘         │
│                         │                                         │
│  ┌─ PHASE 2: LOAD COMPILED ────────────────────────────┐         │
│  │ Reads: .sdd-runtime/mandate.bin (msgpack)            │         │
│  │ Reads: .sdd-runtime/guidelines.bin (msgpack)         │         │
│  │ Reads: .sdd-runtime/metadata.json                    │         │
│  │ Deserializes: Binary → Python objects                │         │
│  │ Output: mandate_dict, guidelines_dict, metadata      │         │
│  └──────────────────────┬───────────────────────────────┘         │
│                         │                                         │
│  ┌─ PHASE 3: FILTER MANDATES ──────────────────────────┐         │
│  │ User Selected: [M001, M002]                           │         │
│  │ Action: Extract only M001 & M002 from mandate_dict   │         │
│  │ Action: Drop M003, M004, etc.                         │         │
│  │ Output: filtered_mandate_spec (DSL format)            │         │
│  └──────────────────────┬───────────────────────────────┘         │
│                         │                                         │
│  ┌─ PHASE 4: FILTER GUIDELINES ────────────────────────┐         │
│  │ Language Filter: java                                 │         │
│  │ → Remove Python-specific guidelines (G045, G089)     │         │
│  │ → Remove JS-specific guidelines (G101, G110)         │         │
│  │ → Keep Java-relevant (G001, G002, ...)               │         │
│  │                                                       │         │
│  │ Adoption Level: LITE                                   │         │
│  │ → Keep only "essential" guidelines                    │         │
│  │ → Drop "nice-to-have" guidelines                      │         │
│  │                                                       │         │
│  │ Category Organization:                               │         │
│  │ → Group by: git, testing, naming, docs, style, perf  │         │
│  │ → Generate: .md files per category                    │         │
│  │ Output: guidelines_dict[category][]: [G001, G002]    │         │
│  └──────────────────────┬───────────────────────────────┘         │
│                         │                                         │
│  ┌─ PHASE 5: APPLY SCAFFOLD ───────────────────────────┐         │
│  │ Load: .sdd-wizard/templates/base/README-SDD.md               │         │
│  │ Load: .sdd-wizard/templates/base/metadata-template.json      │         │
│  │ Load: .sdd-template/base/.github/workflows/*.yml     │         │
│  │ Load: .sdd-wizard/templates/languages/java/* (if java)       │         │
│  │ Load: .sdd-wizard/templates/base/* (language-neutral)         │         │
│  │                                                       │         │
│  │ Substitute Placeholders:                             │         │
│  │ • {{TIMESTAMP}} → 2026-04-21T15:35:22Z              │         │
│  │ • {{SOURCE_HASH}} → a1b2c3d4e5f6...                 │         │
│  │ • {{MANDATES}} → M001, M002                          │         │
│  │ • {{LANGUAGE}} → java                                │         │
│  │ • {{PROJECT_NAME}} → my-project                      │         │
│  │ • {{JAVA_VERSION}} → 11 (if java)                    │         │
│  │ • {{BUILD_TOOL}} → maven (if java)                   │         │
│  │                                                       │         │
│  │ Output: scaffold_templates_dict[]                    │         │
│  └──────────────────────┬───────────────────────────────┘         │
│                         │                                         │
│  ┌─ PHASE 6: GENERATE PROJECT ─────────────────────────┐         │
│  │ Create Directory Structure:                           │         │
│  │ • mkdir -p /path/to/my-project/.sdd/CANONICAL/      │         │
│  │ • mkdir -p /path/to/my-project/.sdd-guidelines/     │         │
│  │ • mkdir -p /path/to/my-project/src/main/{java,..}   │         │
│  │ • mkdir -p /path/to/my-project/.github/workflows/   │         │
│  │ • mkdir -p /path/to/my-project/target/ (java)       │         │
│  │                                                       │         │
│  │ Write Files:                                          │         │
│  │ • .sdd/CANONICAL/mandate.spec (filtered)             │         │
│  │ • .sdd/CANONICAL/guidelines.dsl (filtered)           │         │
│  │ • .sdd-guidelines/git.md (from categories)           │         │
│  │ • .sdd-guidelines/testing.md                         │         │
│  │ • .sdd-guidelines/naming.md                          │         │
│  │ • .sdd-guidelines/README.md (index)                  │         │
│  │ • .sdd/metadata.json (with placeholders filled)      │         │
│  │ • .sdd/examples/*.java (example implementations)     │         │
│  │ • .github/workflows/sdd-validation.yml               │         │
│  │ • pom.xml (maven config)                             │         │
│  │ • README.md (project README)                         │         │
│  │ • README-SDD.md (SDD setup guide)                    │         │
│  │                                                       │         │
│  │ Output: Complete project structure in destination    │         │
│  └──────────────────────┬───────────────────────────────┘         │
│                         │                                         │
│  ┌─ PHASE 7: VALIDATE OUTPUT ──────────────────────────┐         │
│  │ Checks:                                               │         │
│  │ • All required directories exist                      │         │
│  │ • All required files exist                            │         │
│  │ • .sdd/CANONICAL/ is readable                         │         │
│  │ • .sdd-guidelines/ has all category files             │         │
│  │ • metadata.json is valid JSON                         │         │
│  │ • pom.xml parses correctly (for java)                │         │
│  │ • No files are world-writable (security)             │         │
│  │                                                       │         │
│  │ Tests:                                                │         │
│  │ • Basic syntax validation                             │         │
│  │ • Structure integrity checks                          │         │
│  │ • Manifest generation                                 │         │
│  │                                                       │         │
│  │ Output: ✅ DELIVERABLE VALIDATED                      │         │
│  └──────────────────────┬───────────────────────────────┘         │
│                         │                                         │
│                    ✅ SUCCESS                                     │
└────────────────────────┬───────────────────────────────────────────┘
                         │
                         ↓
┌────────────────────────────────────────────────────────────────────┐
│                    CLIENT DELIVERS TO DEVELOPER                    │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  Project Structure:                                               │
│  my-project/                                                      │
│  ├── .sdd/                                                        │
│  │   ├── CANONICAL/                                              │
│  │   │   ├── mandate.spec              (read-only specs)         │
│  │   │   └── guidelines.dsl            (read-only specs)         │
│  │   ├── examples/                     (code examples)           │
│  │   ├── metadata.json                 (audit trail)             │
│  │   └── README-SDD.md                 (setup guide)             │
│  │                                                                │
│  ├── .sdd-guidelines/                  (REQUIRED PATH)            │
│  │   ├── README.md                                               │
│  │   ├── git.md                                                  │
│  │   ├── testing.md                                              │
│  │   ├── naming.md                                               │
│  │   ├── docs.md                                                 │
│  │   ├── style.md                                                │
│  │   └── performance.md                                          │
│  │                                                                │
│  ├── .github/workflows/                                           │
│  │   └── sdd-validation.yml            (CI/CD validation)        │
│  │                                                                │
│  ├── src/main/java/                    (code structure)          │
│  ├── pom.xml                           (maven config)            │
│  ├── README.md                         (project README)          │
│  └── README-SDD.md                     (SDD setup)              │
│                                                                    │
│  Developer Actions:                                              │
│  1. cd my-project                                                │
│  2. cat .sdd-guidelines/git.md         (review guidelines)       │
│  3. cat .sdd/CANONICAL/mandate.spec    (review mandates)         │
│  4. mvn clean test                     (run with SDD validation) │
│  5. git config core.hooksDir .sdd/.git/hooks (use SDD hooks)    │
│  6. Start coding following SDD rules                             │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Layer Interactions

```
ARCHITECT                          CI/CD PIPELINE              WIZARD ORCHESTRATOR
(makes edits)                     (auto-compiles)             (generates projects)

.sdd-core/                        .sdd-compiler/              .sdd-wizard/
mandate.spec ────┐                                            (uses compiled artifacts)
guidelines.dsl ──┼──→ On commit ──→ Compiler ────→ .sdd-runtime/
                 │                                mandate.bin      ↓
              [PR]                              guidelines.bin      │
            [Merge]                               metadata.json     │
                 │                                    ↑          PHASE 1-2
                 │                                    │       (Load & Validate)
                 └────────────────────────────────────┘          │
                                                                  ↓
                                                            Mandate Filter
                                                            Guideline Filter
                                                            .sdd-wizard/templates/
.sdd-wizard/templates/                                                    ↓
(base files)  ─────────────────────────────────────────→ PHASE 3-5
                                                        (Filter & Scaffold)
                                                                  ↓
                                                            PHASE 6
                                                        (Generate Project)
                                                                  ↓
                                                            PHASE 7
                                                        (Validate Output)
                                                                  ↓
                                                    /path/to/my-project/
                                                    (client receives)
```

---

## 🎯 Decision Points & Filtering Logic

### Mandate Selection
```
User Input: "Select mandates for this project"
Options: [M001: Clean Architecture, M002: Test-Driven Development]

User Selects: M001 only

Phase 3 Filtering:
  Input:  mandate_dict = {M001: {...}, M002: {...}}
  Filter: Keep only keys in user_selection [M001]
  Output: filtered_mandate = {M001: {...}}
  
Result:
  .sdd/CANONICAL/mandate.spec written with ONLY M001
```

### Guideline Filtering - Language
```
User Input: Language = "java"

Available Guidelines:
  - G001: Use Java streams (language: java)
  - G002: Follow Maven conventions (language: java)
  - G045: Use Python type hints (language: python) ← REMOVE
  - G089: Python packaging (language: python) ← REMOVE
  - G101: ES6 modules (language: js) ← REMOVE
  - G110: NPM scripts (language: js) ← REMOVE

Phase 4 Filtering (by language):
  Keep: G001, G002
  Drop: G045, G089, G101, G110

Result: Only Java-relevant guidelines in .sdd-guidelines/
```

### Guideline Filtering - By Adoption Level
```
User Input: Language = "java", Adoption Level = "LITE"

All Java Guidelines (filtered by adoption level):
  - G001: essential (priority: 1) ← KEEP
  - G002: essential (priority: 1) ← KEEP
  - G020: advanced (priority: 3) ← DROP (LITE only = essential level)
  - G055: expert (priority: 4) ← DROP

Phase 4 Filtering (by adoption_level):
  Language-specific:   Filter by language tags
  Adoption-level:      Filter by adoption level (LITE/FULL)
  User-customizable:    Choose which guidelines to implement
  
Result:
  .sdd/source/guidelines/ organized by category with LITE-level content
```

---

## 📈 Data Flow Example: M001 Mandate Propagation

**Step 1: Architect Edits Source**
```
.sdd-core/mandate.spec:
  mandate M001 {
    type: "hard"
    title: "Clean Architecture"
    description: "Separate concerns into distinct layers"
  }
```

**Step 2: Commit to Main**
```
git commit -m "docs: Clarify M001 Clean Architecture"
git push origin main
```

**Step 3: CI/CD Compiles**
```
.sdd-compiler/src/dsl_compiler.py:
  Input:  .sdd-core/mandate.spec
  Parse:  Extract M001 mandate
  Encode: MessagePack binary format
  Output: .sdd-runtime/mandate.bin
```

**Step 4: Wizard Loads**
```
.sdd-wizard/src/loader.py:
  Load:   .sdd-runtime/mandate.bin
  Decode: MessagePack → Python dict
  Result: mandate_dict = {
            M001: {title: "Clean Architecture", ...}
          }
```

**Step 5: User Runs Wizard**
```
$ python .sdd-wizard/src/wizard.py
? Choose mandates:
  [✓] M001: Clean Architecture
  [ ] M002: Test-Driven Development
> Confirmed
```

**Step 6: Wizard Filters**
```
.sdd-wizard/orchestration/phase_3_filter_mandates.py:
  Input:        mandate_dict
  User Choice:  [M001]
  Filter:       Keep only M001
  Output:       filtered_mandate = {M001: {...}}
```

**Step 7: Wizard Generates**
```
.sdd-wizard/orchestration/phase_6_generate.py:
  Create: /path/to/my-project/.sdd/CANONICAL/
  Write:  mandate.spec with only M001
  
  Result:
  my-project/.sdd/CANONICAL/mandate.spec:
    mandate M001 {
      type: "hard"
      title: "Clean Architecture"
      description: "Separate concerns into distinct layers"
    }
```

**Step 8: Client Reads**
```
$ cd /path/to/my-project
$ cat .sdd/CANONICAL/mandate.spec

You see your architect's LATEST version of M001!
```

---

## 🔐 Immutability & Safety Guarantees

```
SOURCE (Mutable)
├─ Editable:       .sdd-core/mandate.spec
├─ Editable:       .sdd-core/guidelines.dsl
├─ Via:            PR (WIP branch → Architect review → Merge)
└─ Authority:      Architect only

COMPILED (Regenerated)
├─ Auto-generated: .sdd-runtime/mandate.bin
├─ Auto-generated: .sdd-runtime/guidelines.bin
├─ Trigger:        CI/CD on main commit
├─ Never commit:   These are build artifacts
└─ Cache-like:     Can always be regenerated

TEMPLATE (Immutable)
├─ Read-only:      .sdd/CANONICAL/mandate.spec (in generated project)
├─ Read-only:      .sdd/CANONICAL/guidelines.dsl
├─ Read-only:      .sdd-guidelines/*.md
├─ Reason:         Client must not edit specs
└─ Customization:  Via .sdd-custom/ (v3.2+)
```

---

## 🚨 Error Handling Flow

```
Phase 1: Validate Source
  ✗ ERROR: mandate.spec has syntax error
    → Wizard stops with error message
    → Architect must fix .sdd-core/mandate.spec
    → Commit fix via PR
    → Retry wizard

Phase 2: Load Compiled
  ✗ ERROR: .sdd-runtime/mandate.bin not found
    → Suggest: Run compiler first
    → Suggest: Check CI/CD pipeline status
    → Wizard stops

Phase 3: Filter Mandates
  ✗ ERROR: User selected M999 (doesn't exist)
    → Wizard stops
    → Show available mandates
    → Retry with valid selection

Phase 4: Filter Guidelines
  ✓ Gracefully handles missing language
  ✓ Filters guidelines by language (practical)
  ✓ Falls back to defaults

Phase 6: Generate Project
  ✗ ERROR: Destination already exists
    → Ask user: Overwrite? Backup? Cancel?
    → Proceed based on user choice

Phase 7: Validate Output
  ✗ ERROR: Missing required files
    → List missing files
    → Suggest debugging steps
    → Rollback generated project
```

---

## 📊 Versioning & Audit Trail

**What Gets Tracked in metadata.json:**

```json
{
  "version": "3.0",
  "tier": "lite",
  "format": "spec-v1",
  "generated_at": "2026-04-21T15:35:22Z",
  "source_commit_hash": "ae66c6d",
  "source_commit_message": "refactor: simplify paths",
  "mandates_compiled": ["M001", "M002"],
  "guidelines_count": 45,
  "user_selections": {
    "language": "java",
    "mandates_chosen": ["M001"],
    "language": "java"
  },
  "wizard_version": "3.0.0",
  "java_version": "11",
  "build_tool": "maven"
}
```

**Client Can Verify:**
```
$ cat .sdd/metadata.json | jq .

"When was this generated?" → generated_at
"Which mandates does this follow?" → mandates_chosen
"What guidelines are included?" → guidelines_count
"Can I upgrade to a newer version?" → source_commit_hash (check for updates)
```

---

## 🎼 Orchestration State Machine

```
[START] 
  ↓
[AWAITING INPUT] ← User runs wizard.py
  │
  ├─→ Language? java/python/js → Validate ✓
  ├─→ Mandates? M001,M002 → Validate ✓
  ├─→ Language? java/python/js → Validate ✓
  ├─→ Output? /path → Validate ✓
  │
  ↓
[PHASE 1-2: LOAD]
  ├─→ Load .sdd-core/ (SOURCE)
  ├─→ Load .sdd-runtime/ (COMPILED)
  ├─→ Validate integrity
  ├─→ Error? → [ERROR STATE] → STOP
  │
  ↓
[PHASE 3-5: FILTER & SCAFFOLD]
  ├─→ Filter mandates by user choice
  ├─→ Filter guidelines by language
  ├─→ Load .sdd-wizard/templates/ scaffolds
  ├─→ Substitute placeholders
  ├─→ Error? → [ERROR STATE] → STOP
  │
  ↓
[PHASE 6: GENERATE]
  ├─→ Create directory structure
  ├─→ Write all files
  ├─→ Set permissions
  ├─→ Error? → [ROLLBACK] → STOP
  │
  ↓
[PHASE 7: VALIDATE]
  ├─→ Verify all files created
  ├─→ Run integrity checks
  ├─→ Error? → [ROLLBACK] → STOP
  │
  ↓
[SUCCESS]
  └─→ Print success message
  └─→ Print next steps for user
  └─→ [END]
```

---

## 🚀 Complete User Journey

**Day 1: Architect defines mandates**
```
1. Architect edits .sdd-core/mandate.spec
2. Architect creates PR: wip/define-mandates
3. Architect reviews own PR
4. Architect merges to main
5. CI/CD auto-compiles → .sdd-runtime/mandate.bin
```

**Day 2: Architect adds guidelines**
```
1. Architect edits .sdd-core/guidelines.dsl
2. Architect creates PR: wip/add-guidelines
3. Architect reviews
4. Architect merges to main
5. CI/CD auto-compiles → .sdd-runtime/guidelines.bin
```

**Day 3: Developer generates project from template**
```
1. Developer runs wizard:
   $ python sdd-architecture/.sdd-wizard/src/wizard.py

2. Wizard asks questions:
   Language? → java
   Mandates? → M001, M002
   Language? → java
   Output? → ~/my-java-project/

3. Wizard orchestrates:
   PHASE 1-2: Validates + loads sources
   PHASE 3-4: Filters by language + user selection
   PHASE 5-6: Applies template + generates project
   PHASE 7: Validates output

4. Developer receives fully configured project:
   ~/my-java-project/
   ├── .sdd/CANONICAL/ (read-only specs)
   ├── .sdd-guidelines/ (categorized guidelines)
   ├── src/main/java/ (project structure)
   └── pom.xml (maven ready)

5. Developer starts coding:
   $ cd ~/my-java-project
   $ cat .sdd-guidelines/git.md
   $ mvn clean test
   $ git init
   $ git add .
   $ git commit -m "initial: SDD v3.0 project"
```

---

## 📋 Next Implementation Steps

1. **Phase A (Current):** Orchestrator core + phase implementations
2. **Phase B:** Advanced filtering (v3.1)
3. **Phase C:** Customization support (v3.2)
4. **Phase D:** CI/CD integration (v3.3+)
