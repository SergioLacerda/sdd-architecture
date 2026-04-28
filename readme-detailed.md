# 🏗️ Technical Deep-Dive: 7-Phase Workflow

*Complete technical explanation of the SDD Wizard orchestration*

---

## 📋 Overview

The SDD Wizard executes a **7-phase pipeline** to transform governance specifications into executable projects. This document explains the technical flow, data structures, and error handling.

---

## 🔄 Phase-by-Phase Breakdown

### Phase 1: Validate SOURCE (.sdd-core/)

**What it does:**
- Reads `.sdd-core/mandate.spec` (text DSL)
- Reads `.sdd-core/guidelines.dsl` (text DSL)
- Validates syntax (balanced braces, valid IDs)
- Counts mandates (M001, M002, etc) and guidelines (G01-G150)

**Input Files:**
```
packages/.sdd-core/
├── mandate.spec          ← Architect's mandate definitions
└── guidelines.dsl        ← Architect's guideline definitions
```

**Output:**
```json
{
  "success": true,
  "mandate": {
    "valid": true,
    "count": 4,
    "ids": ["M001", "M002", "M003", "M004"]
  },
  "guidelines": {
    "valid": true,
    "count": 151,
    "ids": ["G01", "G02", ..., "G150"]
  }
}
```

**Error Cases:**
- ❌ File not found → "mandate.spec not found"
- ❌ Syntax error → "Unbalanced braces"
- ❌ Empty file → "File is empty"

**Code Location:** `packages/.sdd-wizard/src/validator.py`

---

### Phase 2: Load COMPILED (.sdd-runtime/)

**What it does:**
- Deserializes `.sdd-runtime/mandate.bin` (binary or JSON)
- Deserializes `.sdd-runtime/guidelines.bin` (binary or JSON)
- Loads metadata from `.sdd-runtime/metadata.json`
- Verifies integrity with SHA-256 fingerprints

**Input Files:**
```
.sdd-runtime/
├── mandate.bin           ← Compiled mandates (binary/JSON)
├── guidelines.bin        ← Compiled guidelines (binary/JSON)
├── mandate.json          ← JSON fallback
├── guidelines.json       ← JSON fallback
└── metadata.json         ← Audit trail + fingerprints
```

**Output:**
```json
{
  "mandates": {
    "M001": {
      "title": "Clean Architecture",
      "description": "Separate concerns into layers",
      "type": "hard",
      ...
    }
  },
  "guidelines": {
    "G01": {
      "category": "code-style",
      "language": "python",
      "status": "required",
      ...
    }
  },
  "metadata": {
    "version": "3.0",
    "generated_at": "2026-04-21T15:35:22Z",
    "source_commit_hash": "ae66c6d",
    "mandates_compiled": ["M001", "M002", "M003", "M004"],
    "guidelines_count": 151
  }
}
```

**Error Cases:**
- ❌ File not found → "mandate.bin not found"
- ❌ Invalid JSON → "JSON decode error"
- ❌ Fingerprint mismatch → "Integrity check failed"

**Code Location:** `packages/.sdd-wizard/src/loader.py`

---

### Phase 3: Filter Mandates

**What it does:**
- Takes all mandates from Phase 2
- User selects which mandates apply
- Filters to only selected mandates
- All mandates retained (immutable core always included)

**Input:**
```
From Phase 2:
├── M001: Clean Architecture
├── M002: Test-Driven Development
├── M003: Secure by Default
└── M004: Performance First

User Selection:
├── ✓ M001
├── ✓ M002
├── ✗ M003
└── ✓ M004
```

**Output:**
```json
{
  "selected_mandates": ["M001", "M002", "M004"],
  "filtered_mandate": {
    "M001": { ... },
    "M002": { ... },
    "M004": { ... }
  }
}
```

**Logic:**
```python
all_mandates = phase_2_output["mandates"]  # All mandates
selected = ["M001", "M002", "M004"]        # User choice
filtered = {m: all_mandates[m] for m in selected}
```

**Error Cases:**
- ❌ Invalid mandate ID → "M999 not found"
- ❌ No mandates selected → "Must select at least M001"

**Code Location:** `packages/.sdd-wizard/orchestration/phase_3_filter_mandates.py`

---

### Phase 4: Filter Guidelines

**What it does:**
- Takes all guidelines from Phase 2
- Filters by user-selected language (Python, Java, TypeScript)
- Filters by user preferences (required, custom, optional)
- Removes optional guidelines

**Input:**
```
From Phase 2:
├── G01: Code Style (language: python)
├── G02: Code Style (language: java)
├── G03: Testing (language: all)
└── ...150 more guidelines

User Selection:
├── Language: Python
├── Preferences: required + custom (skip optional)
```

**Output:**
```json
{
  "filtered_guidelines": {
    "G01": { "language": "python", "status": "required" },
    "G03": { "language": "all", "status": "required" },
    ...
  },
  "count": 45,
  "language": "python"
}
```

**Logic:**
```python
all_guidelines = phase_2_output["guidelines"]
language = "python"
status_filter = ["required", "custom"]

filtered = {
    g: all_guidelines[g] 
    for g in all_guidelines
    if all_guidelines[g]["language"] in [language, "all"]
    and all_guidelines[g]["status"] in status_filter
}
```

**Error Cases:**
- ⚠️ No guidelines for language → Returns empty (not fatal)
- ⚠️ All guidelines filtered out → Warns but continues

**Code Location:** `packages/.sdd-wizard/orchestration/phase_4_filter_guidelines.py`

---

### Phase 5: Apply Template

**What it does:**
- Copies project template from `.sdd-wizard/templates/{language}/`
- Substitutes placeholders with user selections
- Prepares scaffold directory with customized templates

**Input:**
```
Template:
.sdd-wizard/templates/python/
├── src/
│   └── {package_name}/
│       └── __init__.py
├── tests/
│   └── test_{package_name}.py
├── setup.py.template
├── README.md.template
└── .sdd/
    └── CANONICAL/
        └── mandates.spec.template

Substitutions:
├── {package_name} → "my_project"
├── {language} → "python"
├── {mandates} → "M001, M002"
└── {author} → "user@example.com"
```

**Output:**
```
sdd-generated/scaffold/
├── src/
│   └── my_project/
│       └── __init__.py
├── tests/
│   └── test_my_project.py
├── setup.py
├── README.md
└── .sdd/
    └── CANONICAL/
        └── mandates.spec
```

**Logic:**
```python
template_dir = f"templates/{language}/"
for file in walk(template_dir):
    content = read(file)
    # Replace placeholders
    content = content.replace("{package_name}", "my_project")
    content = content.replace("{language}", "python")
    write(output_dir / file, content)
```

**Error Cases:**
- ❌ Template not found → "templates/unknown_lang/ not found"
- ❌ Permission denied → "Cannot write to output directory"

**Code Location:** `packages/.sdd-wizard/orchestration/phase_5_apply_template.py`

---

### Phase 6: Generate Project

**What it does:**
- Creates output directory structure
- Writes all project files (templates + specifications)
- Generates metadata.json with audit trail
- Sets proper file permissions

**Input:**
```
From Phase 5: Customized templates
From Phase 3-4: Filtered mandates + guidelines
User Input: Output directory path

Configuration:
├── Language: python
├── Mandates: M001, M002
├── Guidelines: 45 (filtered for Python)
└── Output: ~/my-project/
```

**Output:**
```
~/my-project/
├── .sdd/
│   ├── CANONICAL/
│   │   ├── mandate.spec (filtered)
│   │   ├── guidelines.dsl (filtered)
│   │   └── metadata.json
│   └── -guidelines/
│       ├── architecture.md
│       ├── testing.md
│       └── ...
├── src/
│   └── main.py
├── tests/
│   └── test_main.py
├── README.md
└── setup.py
```

**Metadata Generated:**
```json
{
  "version": "3.0",
  "generated_at": "2026-04-26T10:30:00Z",
  "source_commit_hash": "abc123def",
  "language": "python",
  "mandates_chosen": ["M001", "M002"],
  "guidelines_count": 45,
  "user_email": "developer@example.com",
  "framework_path": "/path/to/sdd-architecture",
  "salt_hash": "sha256(mandate.spec + guidelines.dsl)"
}
```

**Error Cases:**
- ❌ Directory exists → Ask overwrite/backup/cancel
- ❌ Permission denied → "Cannot create directory"
- ❌ Disk full → "Not enough space"

**Code Location:** `packages/.sdd-wizard/orchestration/phase_6_generate_project.py`

---

### Phase 7: Validate Output

**What it does:**
- Verifies all expected files exist
- Checks metadata integrity
- Validates specification format
- Runs basic sanity checks

**Input:**
```
Generated Project Directory: ~/my-project/
Expected Structure: From template + manifest
```

**Validation Checks:**
```
1. Directory exists                          ✓
2. .sdd/ directory present                   ✓
3. CANONICAL/ subdirectory present           ✓
4. mandate.spec file exists                  ✓
5. guidelines.dsl file exists                ✓
6. metadata.json exists                      ✓
7. metadata.json valid JSON                  ✓
8. All template files present                ✓
9. No empty directories                      ✓
10. File permissions correct                 ✓
```

**Output:**
```json
{
  "success": true,
  "validation_results": {
    "directory_structure": "✅ Valid",
    "specification_files": "✅ Valid",
    "metadata_integrity": "✅ Valid",
    "file_count": 12,
    "total_size": "2.3 MB"
  },
  "warnings": [],
  "ready_for_use": true
}
```

**Error Cases:**
- ⚠️ Missing files → List which files are missing
- ⚠️ Invalid JSON → "metadata.json not valid JSON"
- ⚠️ Corrupted → Rollback and remove generated files

**Code Location:** `packages/.sdd-wizard/orchestration/phase_7_validate_output.py`

---

## 🔀 Data Flow Between Phases

```
Phase 1 Output
    ↓
    └─→ SOURCE metadata (count, IDs, syntax OK)

Phase 2 Output
    ↓
    ├─→ mandate dict: {M001: {...}, M002: {...}, ...}
    ├─→ guidelines dict: {G01: {...}, G02: {...}, ...}
    └─→ metadata: version, timestamp, hashes

Phase 3 Output
    ↓
    └─→ filtered_mandate: {M001: {...}, M002: {...}}
        (Only user-selected mandates)

Phase 4 Output
    ↓
    └─→ filtered_guidelines: {G01: {...}, G03: {...}}
        (Only language-matching + non-optional)

Phase 5 Output
    ↓
    └─→ scaffold/: Template files with placeholders replaced

Phase 6 Output
    ↓
    ├─→ ~/my-project/: Complete project structure
    └─→ ~/my-project/.sdd/metadata.json: Audit trail

Phase 7 Output
    ↓
    └─→ validation_report: Success ✅ or rollback ❌
```

---

## ⚠️ Error Handling Strategy

### Error Categories

| Phase | Error Type | Action |
|-------|-----------|--------|
| 1 | Validation | STOP + Show error |
| 2 | Missing files | STOP + Suggest recompile |
| 3 | Invalid selection | RETRY + Show valid options |
| 4 | No guidelines match | WARN + Continue with empty |
| 5 | Template missing | STOP + Check language |
| 6 | Dir exists | ASK + Overwrite/Backup/Cancel |
| 7 | Validation failed | ROLLBACK + Delete generated |

### Rollback Strategy

If Phase 6 or 7 fails:
```bash
# 1. Delete partially generated directory
rm -rf ~/my-project/

# 2. Inform user of error
echo "❌ Project generation failed at Phase 7"

# 3. Show troubleshooting
echo "Try: ./wizard.sh --verbose"
echo "Or: ./wizard.sh --dry-run"
```

---

## 🔌 Integration with Governance Systems

### Integration Point 1: Health Check

**When:** Before running wizard  
**What:** Validates SDD structure exists

```bash
python3 packages/health_check.py
# Output: 🟢 HEALTHY | All 10 checks pass
```

**If fails:** Suggest setup.sh

### Integration Point 2: Agent Handshake

**When:** Before providing response  
**What:** 4-layer validation (Discovery → Link → Runtime → Health)

```bash
python3 packages/agent_handshake.py --mode=silent
# Output: HEALTHY | Confidence: 92%
```

### Integration Point 3: Governance Compliance

**When:** Phase 1 + Phase 2  
**What:** Ensures mandates are immutable + valid

```bash
python3 packages/tools/governance_compliance.py --verify
# Output: ✅ All 4 mandates verified
```

---

## 📊 Performance Metrics

| Phase | Time | Bottleneck |
|-------|------|-----------|
| Phase 1 | <1s | File I/O |
| Phase 2 | <2s | JSON parsing |
| Phase 3 | <100ms | Filter logic |
| Phase 4 | <500ms | Pattern matching |
| Phase 5 | <3s | Template substitution |
| Phase 6 | <5s | File writing |
| Phase 7 | <1s | Validation |
| **Total** | **~15s** | Phase 6 (file I/O) |

**Optimization targets:**
- Phase 6: Use parallel file writing
- Phase 2: Cache JSON parsing
- Phase 5: Pre-compile templates

---

## 🚀 CI/CD Integration (GitHub Actions)

### How the Wizard Interacts with CI/CD

The 7-phase wizard runs within the context of **10 GitHub Actions workflows** that validate and enforce quality:

```
Wizard Execution (Local)
    ↓
    └─→ Pre-push Hook validates
        ├─→ Health Check (10 points)
        ├─→ Governance Compliance (4 mandates)
        └─→ Allow or block push
    ↓
Git Push to GitHub
    ↓
GitHub Actions Workflows Trigger
    ├─→ Validate Workflows (YAML syntax)
    ├─→ Health Check (same 10 checks)
    ├─→ Tests (124 tests, Python 3.8-3.12)
    ├─→ Lint (code quality, type hints)
    ├─→ Governance Enforce (compliance)
    ├─→ Integration (wizard e2e test)
    ├─→ Compliance Report (dashboard)
    ├─→ Dependencies (security scan)
    └─→ Merge Allowed? (all must pass)
    ↓
Success: Merge to main
    ├─→ Docs auto-generated
    ├─→ Compliance metrics updated
    └─→ Release pipeline ready
```

### The 10 Workflows Explained for Developers

| Workflow | Runs | Checks | Blocks Merge? |
|----------|------|--------|---------------|
| Health Check | Push, PR, Daily | 10 system checks | ✅ Yes |
| Tests | Push, PR | 124 tests, 100% coverage | ✅ Yes |
| Lint | Push, PR | Code quality, types, format | ✅ Yes |
| Governance Enforce | Push, PR | 4 mandates, 151 guidelines | ✅ Yes |
| Validate Workflows | Push, PR | YAML syntax, structure | ✅ Yes |
| Compliance Report | Daily | Governance dashboard | ⚠️ Info only |
| Integration | Push, PR | Wizard, compiler, CLI | ⚠️ Warning |
| Dependencies | Weekly | Security vulnerabilities | ⚠️ Warning |
| Docs | Main push | Auto-generate docs | 🔄 Post-merge |
| Release | Tag push | Build, publish, changelog | 🔄 Post-merge |

### Relationship Between Wizard Phases and Workflows

```
Phase 1-2 (Validate & Load)
    ↓
    └─→ Tests must cover validation logic
    └─→ Lint must approve code quality
    └─→ Governance must allow specs
    
Phase 3-4 (Filter)
    ↓
    └─→ Integration test filters correctly
    └─→ No hardcoded selections
    
Phase 5 (Template Application)
    ↓
    └─→ Generated templates pass lint
    └─→ Generated code has tests
    
Phase 6-7 (Generate & Validate)
    ↓
    └─→ Output project runs through same CI/CD
    └─→ Metadata correctly formatted
```

### Pre-Push Hook Strategy

**SDD Architecture framework** uses `.git/hooks/pre-push` that runs locally:

```bash
#!/bin/bash
# Pre-push Hook - SDD Architecture Framework (Not for Client Projects)
#
# ⚠️ This hook is for the framework only, not client projects.
# Validates framework health + governance compliance.

[PRE-PUSH] Starting final validation...
→ Running full health check (fresh, no cache)...
  ✓ Health check passed (10/10)
→ Verifying governance enforcement level...
  ✓ Enforcement mode: STRICT
→ Checking compliance percentage...
  ✓ Fully compliant (100%)
[PRE-PUSH] All checks passed. Push allowed.
```

**If pre-push fails:**
```bash
# Run individually to debug
python3 packages/health_check.py --verbose
cd packages && python3 run-all-tests.py
python3 packages/tools/governance_compliance.py --verify

# Force push if absolutely necessary (not recommended)
git push --no-verify
```

**⚠️ Important distinction:**
- **Framework hook**: Validates governance + health (blocks if compliance fails)
- **Client project hook** (future): Validates project quality only (no framework governance validation)

### Continuous Monitoring Post-Merge

After merging to main:
- 📚 **Docs** auto-generated and committed
- 📊 **Compliance Report** updates governance dashboard
- 🔗 **Integration** runs full wizard test
- 📦 **Dependencies** checked for security issues

---

## 🧪 Testing Strategy

### Unit Tests (per phase)
```bash
pytest packages/tests/test_phase_1.py  # Validate
pytest packages/tests/test_phase_2.py  # Load
# ... etc
```

### Integration Tests (full pipeline)
```bash
pytest packages/tests/test_wizard_integration.py
# Runs all 7 phases together
```

### End-to-End Tests
```bash
./wizard.sh --test-phases 1-7 --dry-run
# Preview without creating files
```

---

## 🔗 Related Files

| File | Purpose |
|------|---------|
| `wizard.py` | Main orchestrator |
| `interactive_mode.py` | User questionnaire |
| `validator.py` | Phase 1 logic |
| `loader.py` | Phase 2 logic |
| `orchestration/phase_*.py` | Phases 3-7 |
| `.sdd-runtime/` | Compiled artifacts |
| `.sdd-wizard/templates/` | Project scaffolds |

---

## 📚 Related Documentation

- [README.md](README.md) — Quick start
- [readme-ia.md](readme-ia.md) — AI integration
- [packages/.sdd-wizard/WORKFLOW_FLOW.md](packages/.sdd-wizard/WORKFLOW_FLOW.md) — Complete orchestration
- [packages/.sdd-wizard/AI_AGENT_GUIDE.md](packages/.sdd-wizard/AI_AGENT_GUIDE.md) — AI-focused guide

---

**For Technical Understanding:** Use this guide when:
- Debugging wizard failures
- Optimizing performance  
- Extending wizard functionality
- Understanding data transformations

*Last Updated: April 26, 2026*
