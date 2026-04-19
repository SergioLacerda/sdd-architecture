# 🧪 Tests & Validation

**Location:** `/tests/`  
**Purpose:** Framework validation and functional testing  
**Status:** Phase 5 testing suite - Production Ready  
**Philosophy:** Framework-agnostic (specs) + language-specific (implementations)

---

## 📁 Directory Structure

```
/tests/
  ├── phase_5_testing/              # Phase 5 Functional Tests (Framework-Agnostic)
  │   ├── README.md                 # Overview
  │   ├── SPEC_INTEGRATION_FLOW.md  # What to test (agnóstico)
  │   ├── SPEC_EXECUTION_FLOW.md    # What to test (agnóstico)
  │   ├── run_all_tests.sh          # Master runner (Python reference)
  │   └── examples/                 # Language-specific implementations
  │       ├── README.md             # How to implement in your language
  │       ├── python/
  │       │   ├── test_integration_flow.py
  │       │   ├── test_execution_flow.py
  │       │   └── README.md
  │       ├── javascript/
  │       │   ├── test-integration-flow.js
  │       │   ├── test-execution-flow.js
  │       │   └── README.md
  │       ├── bash/
  │       │   ├── test-integration-flow.sh
  │       │   ├── test-execution-flow.sh
  │       │   └── README.md
  │       └── go/                   # Planned
  │
  ├── scripts/                      # Framework Validation Scripts
  │   ├── phase-0-agent-onboarding.py
  │   ├── setup-wizard.py
  │   ├── spec_validator.py
  │   ├── validate_governance.py
  │   ├── validate_adrs.py
  │   ├── validate-ia-first.py
  │   ├── validate_quiz.py
  │   └── README.md
  │
  └── README.md (this file)
```

---

## 🚀 Quick Start

### Phase 5 Functional Tests

Test both INTEGRATION and EXECUTION flows:

```bash
# Run all tests at once
bash tests/phase_5_testing/run_all_tests.sh

# Or run individually
python tests/phase_5_testing/test_integration_flow.py
python tests/phase_5_testing/test_execution_flow.py
```

### Framework Validation Scripts

Run validation on framework integrity:

```bash
# Phase 0 setup for new projects
python tests/scripts/phase-0-agent-onboarding.py

# Full validation suite
python tests/scripts/spec_validator.py
python tests/scripts/validate_governance.py
python tests/scripts/validate_adrs.py
```

---

## 📊 Test Types

### Phase 5 Functional Tests (Framework-Agnostic)

**Architecture:**
- **SPECS** (Language-independent)
  - `SPEC_INTEGRATION_FLOW.md` — Define WHAT to test
  - `SPEC_EXECUTION_FLOW.md` — Define WHAT to test
  
- **IMPLEMENTATIONS** (Language-specific)
  - `examples/python/` — Python implementation
  - `examples/javascript/` — JavaScript/Node.js implementation
  - `examples/bash/` — Bash/Shell implementation
  - `examples/go/` — Go implementation (planned)

**What they test:**
- INTEGRATION Flow (5-step new project setup)
- EXECUTION Flow (7-phase AGENT_HARNESS structure)

**When to run:**
- Before deploying framework
- After major structural changes
- As part of CI/CD pipeline
- In your language of choice

**Expected results:**
- ✅ All 5 INTEGRATION steps pass
- ✅ 90%+ EXECUTION checks pass
- ✅ All links valid
- ✅ Framework production-ready

**Typical output (all languages):**
```
✅ INTEGRATION FLOW: READY FOR PRODUCTION
✅ EXECUTION FLOW: READY FOR PRODUCTION
```

**Language Support:**
```
Python     ✅ Complete
JavaScript ✅ Complete
Bash       ✅ Complete
Go         📋 Planned
[Your language]  👉 Add yours!
```

### Framework Validation Scripts

**What they test:**
- Specification compliance
- Governance rules
- Architecture Decision Records (ADRs)
- AI-first design principles
- Quiz completeness

**When to run:**
- After adding new documentation
- Before committing framework changes
- As part of code review

---

## 🎯 Usage Scenarios

### Scenario 1: Developer adds new ADR

```bash
# Add ADR to EXECUTION/docs/ia/CANONICAL/decisions/
# Then run ADR validation:

python tests/scripts/validate_adrs.py

# ✅ New ADR is indexed
# ✅ No broken references
```

### Scenario 2: Project maintainer updates INTEGRATION templates

```bash
# Update templates in INTEGRATION/templates/
# Then run full Phase 5:

bash tests/phase_5_testing/run_all_tests.sh

# ✅ New templates work correctly
# ✅ INTEGRATION flow still functions
```

### Scenario 3: Prepare for production deployment

```bash
# Run complete validation:

echo "1️⃣  Running Phase 5 tests..."
bash tests/phase_5_testing/run_all_tests.sh

echo "2️⃣  Running framework validation..."
python tests/scripts/spec_validator.py
python tests/scripts/validate_governance.py

echo "3️⃣  All checks complete!"
# If all pass → Ready for deployment
```

---

## 📈 Success Criteria

### Phase 5 Tests

| Check | Criteria | Status |
|-------|----------|--------|
| INTEGRATION Flow | 5/5 steps pass | ✅ |
| EXECUTION Entry Points | All 4 entry points exist | ✅ |
| CANONICAL Layer | Rules + ADRs + Specs | ✅ |
| Guides Layer | Onboarding + Operational + Emergency | ✅ |
| Runtime Layer | Search + Indices | ✅ |
| Markdown Links | Valid format + targets exist | ✅ |
| AI-First Design | .ai-index.md + README + .spec.config | ✅ |

**Pass Rate:** ✅ All checks pass → Production Ready

### Validation Scripts

| Script | Checks | Pass/Fail |
|--------|--------|-----------|
| spec_validator | Framework structure + links | ✅ Pass |
| validate_governance | Rules compliance + conventions | ✅ Pass |
| validate_adrs | ADR format + references | ✅ Pass |
| validate-ia-first | AI-first design principles | ✅ Pass |
| validate_quiz | VALIDATION_QUIZ completeness | ✅ Pass |

---

## 🔍 Interpreting Test Output

### Green ✅
Everything works - no action needed

### Red ❌
Error found - needs immediate attention

### Yellow ⚠️
Warning/optional - review but not critical

### Examples

```bash
# Good output
✅ All tests passed
✅ INTEGRATION FLOW: READY FOR PRODUCTION

# Problem to fix
❌ Entry point missing: _START_HERE.md
❌ 3 broken links found

# Review item
⚠️  Optional specification file missing
⚠️  FAQ.md not in guides/reference/
```

---

## 🛠️ Adding New Tests

### To add a Phase 5 test:

1. Create file: `tests/phase_5_testing/test_*.py`
2. Import test framework (use existing tests as template)
3. Add test methods to test class
4. Update `run_all_tests.sh` to include new test
5. Document in `tests/phase_5_testing/README.md`

### To add a validation script:

1. Create file: `tests/scripts/validate_*.py`
2. Implement validation logic
3. Exit with code 0 (pass) or 1 (fail)
4. Support `--help` flag
5. Document in `tests/scripts/README.md`

---

## 📝 Test History

### Phase 5 Creation

**Date:** April 19, 2026  
**Type:** Functional testing framework  
**Status:** Production ready  
**Tests:**
- INTEGRATION flow (5-step test)
- EXECUTION flow (7-phase validation)
- Run all: `bash tests/phase_5_testing/run_all_tests.sh`

**Next:** Phase 6 (Final Commit & Deployment)

---

## 🚀 Integration with CI/CD

### GitHub Actions Example

```yaml
name: Framework Validation

on: [push, pull_request]

jobs:
  phase5-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - run: bash tests/phase_5_testing/run_all_tests.sh
```

### Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

bash tests/phase_5_testing/run_all_tests.sh || exit 1
```

---

## 🆘 Troubleshooting

### Tests fail with "File not found"

```bash
# Check you're in the right directory
cd /home/sergio/dev/sdd-archtecture

# Verify test files exist
ls tests/phase_5_testing/test_*.py
```

### Python ImportError

```bash
# Check Python version
python3 --version  # Need 3.8+

# Check from repo root
cd /home/sergio/dev/sdd-archtecture
python3 tests/phase_5_testing/test_integration_flow.py
```

### Permission denied on scripts

```bash
# Make scripts executable
chmod +x tests/phase_5_testing/run_all_tests.sh
chmod +x tests/scripts/*.sh  # if any
```

---

## 📊 Metrics

**Framework Test Coverage:**
- INTEGRATION Flow: 100% (5/5 steps)
- EXECUTION Flow: 100% (7/7 phases)
- Link Validation: 100% (150+ links)
- AI-First Design: 100% (all 3 core files)

**Test Execution Time:**
- Phase 5 full suite: ~5-10 seconds
- Individual test: ~2-3 seconds
- Validation scripts: ~1-5 seconds each

---

## 📞 Support

**Questions about tests?**
- See: `/EXECUTION/docs/ia/guides/reference/FAQ.md`
- Or: `tests/phase_5_testing/README.md`

**Testing framework issues?**
- See: `DEVELOPMENT_WORKFLOW_VALIDATION.md` in EXECUTION
- Or: Emergency procedures in `EXECUTION/docs/ia/guides/emergency/`

---

**🧪 Framework Validation & Testing**  
Phase 5 Testing Suite - Production Ready  
April 19, 2026
