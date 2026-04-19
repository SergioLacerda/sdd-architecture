# 🚨 SPEC v2.1 QUALITY REGRESSION — ACTION PLAN

**Date:** April 19, 2026  
**Current Score:** 5.0/10 ⚠️ (regressed from 6.8/10)  
**Root Cause:** 4 features delivered with 0 tests, 0 runbooks, 0 integration  
**Recovery Effort:** 20-25 hours to reach 8.0/10  
**Timeline:** This week (5 days)

---

## 📊 REGRESSION ANALYSIS

```
v2.0 (After critical fixes):    6.8/10 ✅ Working
v2.1 (After improvements):      5.0/10 ⚠️ Regressed

Why? Added features without integration:
  ✅ 4 new features delivered
  ❌ 0 tests written
  ❌ 0 CI/CD integration
  ❌ 0 operational runbooks
  ❌ 0 emergency procedures
  ❌ 0 measurement infrastructure

This is ANTI-PATTERN for world-class engineering.
```

---

## 🎯 PHASE 1: EMERGENCY STABILIZATION (6 hours)

### Task 1.1: Emergency Procedures Documentation (2 hours)

**Deliverable:** `/docs/ia/guides/operational/EMERGENCY_PROCEDURES.md`

```markdown
# Emergency Procedures for SPEC Governance

## Emergency #1: Pre-commit Validation Fails for All Commits
### Cause
  - validate-ia-first.py crashed
  - setup-wizard.py incompatibility
  - Path validation broken

### Immediate Mitigation (Temporary)
  git commit --no-verify -m "Emergency: bypass governance validation

  [EMERGENCY] pre-commit broken
  Reason: $REASON
  Temporary measure: revert in next commit
  "

### Recovery (30 minutes)
  1. Identify broken validator
  2. Disable in .pre-commit-config.yaml
  3. Fix the validator
  4. Re-enable and test
  5. Document root cause

### Prevention
  Add to test suite: "Verify all hooks are runnable"

---

## Emergency #2: generate-specializations.py Corrupted Files
### Cause
  Script auto-fixed docs incorrectly
  --fix flag applied unsafe transformations

### Immediate Mitigation
  git checkout docs/ia/custom/
  git commit -m "Revert corrupted specializations"

### Recovery (15 minutes)
  1. git log --oneline | grep generate
  2. git show COMMIT_HASH
  3. Analyze what went wrong
  4. Fix generate-specializations.py
  5. Re-run with --dry-run first
  6. Commit with detailed message

### Prevention
  Always use --dry-run before --fix
  Add tests for idempotency

---

## Emergency #3: CANONICAL Merge Conflict
### Cause
  Two teams modified ia-rules.md simultaneously
  Merge conflict markers present

### Immediate Mitigation
  git status | grep "both modified"
  For each file:
    git checkout --ours docs/ia/CANONICAL/rules/ia-rules.md
    # Then manually fix + test

### Recovery (1 hour)
  1. Identify which changes were needed
  2. Manually reapply non-conflicting changes
  3. Add test case for this specific conflict
  4. Document resolution in DECISIONS.md

### Prevention
  Create CANONICAL coordination process
  Document in .github/CONTRIBUTING.md

---

## Emergency #4: CI/CD spec-enforcement Gate Blocking Valid PRs
### Cause
  validation job too strict
  false positive in rule checking

### Immediate Mitigation
  Temporarily disable job:
    .github/workflows/spec-enforcement.yml
    # Comment out: validate-ia-first job

### Recovery (30 minutes)
  1. Identify which validation is too strict
  2. Review test case
  3. Adjust threshold or rule
  4. Re-enable job + test
  5. Document decision

### Prevention
  All enforcement rules must have exceptions documented
  Document in compliance.md what bypassing requires

---

## Emergency #5: METRICS Data Corrupted
### Cause
  Manual data entry error
  Collection script bug

### Immediate Mitigation
  git checkout docs/ia/METRICS.md
  # Reset to last known good

### Recovery (20 minutes)
  1. Identify when corruption happened
  2. Restore from git history
  3. Audit collection process
  4. Fix collection script
  5. Re-baseline if needed

### Prevention
  Use automated collection (no manual entry)
  Add data validation to collection script
  Set up alerts for anomalies

---

## Emergency #6: setup-wizard.py Breaks for All New Developers
### Cause
  Missing dependency
  Python version incompatibility
  Configuration error

### Immediate Mitigation
  Revert to FIRST_SESSION_SETUP.md:
    1. Update .github/copilot-instructions.md
    2. Direct new devs to old path
    3. Document known issue

### Recovery (1 hour)
  1. Diagnose root cause
  2. Fix setup-wizard.py
  3. Add test case
  4. Verify with new developer
  5. Re-enable as primary path

### Prevention
  Test setup-wizard.py with Python 3.10, 3.11, 3.12
  Document dependency requirements
  Add CI/CD test of setup-wizard.py itself

---

## Emergency #7: validate-ia-first.py False Positives
### Cause
  Rule too strict
  Auto-fix corrupting valid docs

### Immediate Mitigation
  Disable auto-fix:
    git checkout docs/ia/SCRIPTS/validate-ia-first.py
    # Remove or comment out auto-fix logic

### Recovery (1 hour)
  1. Review false positive cases
  2. Adjust rules in IA_FIRST_SPECIFICATION.md
  3. Update validator logic
  4. Re-test on all 50+ docs
  5. Re-enable

### Prevention
  Create test cases for edge cases
  Test on ALL existing docs before deployment
```

**Status:** ⏳ TODO (2 hours)

---

### Task 1.2: Integrate New Scripts to CI/CD (2 hours)

**File:** `.github/workflows/spec-enforcement.yml`

**Changes needed:**

```yaml
# ADD NEW JOBS:

  validate-ia-first:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install questionary  # for setup-wizard
      - name: Validate IA-FIRST format
        run: |
          cd docs/ia
          python SCRIPTS/validate-ia-first.py --audit . --verbose
        continue-on-error: false  # BLOCKING
      - name: Report violations
        if: failure()
        run: |
          echo "IA-FIRST validation failed"
          echo "Run locally: python docs/ia/SCRIPTS/validate-ia-first.py --audit docs/ia/"
          exit 1

  test-setup-wizard:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
      - run: pip install questionary
      - name: Test setup wizard (dry-run)
        run: |
          cd docs/ia
          python SCRIPTS/setup-wizard.py --test-mode
        continue-on-error: false

  test-specializations-generation:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
      - name: Validate specializations script
        run: |
          cd docs/ia
          python -m py_compile SCRIPTS/generate-specializations.py
          # Check for syntax errors
        continue-on-error: false
```

**Status:** ⏳ TODO (2 hours)

---

### Task 1.3: Resolve Onboarding Path Confusion (1 hour)

**Decisions to make:**

```
Decision 1: Which is canonical onboarding path?
  Option A: Keep OLD path (FIRST_SESSION_SETUP.md) — safe, tested
  Option B: Use NEW path (ULTRA_QUICK_ONBOARDING + setup-wizard.py) — experimental
  Recommendation: NEW path, but old path as fallback
  
  Action: Explicitly mark one as PRIMARY, one as LEGACY

Decision 2: Is VALIDATION_QUIZ still mandatory?
  Current: Yes (takes 10 minutes)
  Problem: Adds to onboarding time
  Recommendation: Move to optional, but document it's important
  
  Action: Update documentation clearly

Decision 3: Update .github/copilot-instructions.md?
  Current: Still references old path
  Action: Update to reference NEW setup-wizard.py path

Decision 4: Create deprecation timeline
  Old path deprecated: May 31, 2026
  Old path removed: June 30, 2026
  Action: Add timeline to both docs
```

**Files to update:**
- `docs/ia/guides/onboarding/ULTRA_QUICK_ONBOARDING.md` — Add "PRIMARY" label
- `docs/ia/guides/onboarding/FIRST_SESSION_SETUP.md` — Add "LEGACY - see ULTRA_QUICK for new path"
- `.github/copilot-instructions.md` — Reference setup-wizard.py
- `docs/ia/guides/onboarding/README.md` — New file with decision

**Status:** ⏳ TODO (1 hour)

---

### Task 1.4: Add Metrics Collection Infrastructure (1 hour)

**Deliverable:** `/docs/ia/SCRIPTS/collect-metrics.py`

```python
#!/usr/bin/env python3
"""Collect SPEC governance metrics.

Usage:
  python collect-metrics.py --collect    # Collect and append
  python collect-metrics.py --summarize  # Generate weekly report
"""

import json
import datetime
from pathlib import Path

def collect_readership_metrics():
    """Measure which docs are most read."""
    # TODO: Hook into CI/CD logs? Git access counts?
    # For now: manual estimates from team feedback
    return {
        "ia-rules.md": 12,  # reads per week
        "QUICK_START.md": 8,
        "architecture.md": 5,
        "ADR-001.md": 2,
    }

def collect_validation_metrics():
    """Measure enforcement effectiveness."""
    # Check CI/CD logs for validation job results
    return {
        "violations_caught_this_week": 3,
        "false_positives": 0,
        "false_negatives": 0,
        "validation_time_seconds": 45,
    }

def collect_onboarding_metrics():
    """Measure setup-wizard.py performance."""
    # TODO: Instrument setup-wizard.py to measure actual time
    return {
        "setup_wizard_success_rate": 0.85,  # 85% succeeded
        "setup_wizard_avg_time_seconds": 340,  # 5.67 minutes
        "new_dev_first_pr_time_hours": 2.5,
    }

def append_to_metrics():
    """Append weekly metrics to METRICS.md."""
    metrics = {
        "week": datetime.date.today().isocalendar()[1],
        "date": str(datetime.date.today()),
        "readership": collect_readership_metrics(),
        "validation": collect_validation_metrics(),
        "onboarding": collect_onboarding_metrics(),
    }
    
    metrics_file = Path("../METRICS.md")
    # Append to historical data section
    # TODO: Implement

def generate_weekly_report():
    """Generate summary for team."""
    print("=== SPEC Metrics Weekly Report ===")
    # TODO: Calculate trends
    # TODO: Alert if any metric regressed
    # TODO: Show progress toward Q2 2026 targets

if __name__ == "__main__":
    import sys
    if "--collect" in sys.argv:
        append_to_metrics()
        print("✅ Metrics collected")
    elif "--summarize" in sys.argv:
        generate_weekly_report()
```

**Status:** ⏳ TODO (1 hour)

---

## 🎯 PHASE 2: VALIDATION & TESTING (4 hours)

### Task 2.1: Comprehensive Test Suite (2 hours)

**Deliverable:** `tests/spec_validation/test_new_features.py`

```python
"""Test the 4 new SPEC improvements."""

import pytest
import subprocess
from pathlib import Path

class TestSetupWizard:
    def test_setup_wizard_exists(self):
        """Verify script exists."""
        assert Path("docs/ia/SCRIPTS/setup-wizard.py").exists()
    
    def test_setup_wizard_runs_without_error(self):
        """Test --test-mode doesn't crash."""
        # Mock interactive responses
        result = subprocess.run(
            ["python", "docs/ia/SCRIPTS/setup-wizard.py", "--test-mode"],
            cwd="docs/ia",
            capture_output=True,
        )
        assert result.returncode == 0, f"Stderr: {result.stderr}"
    
    def test_setup_wizard_loads_correct_docs_for_bug_fix(self):
        """Bug fix should recommend ia-rules.md + known_issues.md."""
        # Test logic in setup-wizard.py
        pass
    
    def test_setup_wizard_error_handling(self):
        """Test graceful error handling."""
        pass

class TestValidateIAFirst:
    def test_validate_ia_first_exists(self):
        """Verify script exists."""
        assert Path("docs/ia/SCRIPTS/validate-ia-first.py").exists()
    
    def test_validate_ia_first_checks_h1_header(self):
        """Verify H1 header check works."""
        pass
    
    def test_validate_ia_first_auto_fix_idempotent(self):
        """Run --fix twice, should be identical."""
        pass
    
    def test_validate_ia_first_on_all_canonical_docs(self):
        """Test on all 25 CANONICAL docs."""
        # Run on actual docs
        result = subprocess.run(
            ["python", "SCRIPTS/validate-ia-first.py", "--audit", "CANONICAL/"],
            cwd="docs/ia",
            capture_output=True,
        )
        # Should pass or show specific violations
        pass

class TestGenerateSpecializations:
    def test_generate_specializations_exists(self):
        """Verify script exists."""
        assert Path("docs/ia/SCRIPTS/generate-specializations.py").exists()
    
    def test_generate_specializations_syntax(self):
        """Script should be valid Python."""
        result = subprocess.run(
            ["python", "-m", "py_compile", "SCRIPTS/generate-specializations.py"],
            cwd="docs/ia",
        )
        assert result.returncode == 0
    
    def test_generate_specializations_template_exists(self):
        """Template should exist."""
        assert Path("docs/ia/SPECIALIZATIONS.template.md").exists()

class TestMetricsFramework:
    def test_metrics_md_exists(self):
        """Metrics framework should exist."""
        assert Path("docs/ia/METRICS.md").exists()
    
    def test_metrics_md_has_baseline_data(self):
        """Should have April 2026 baseline."""
        content = Path("docs/ia/METRICS.md").read_text()
        assert "April 2026" in content or "2026" in content
    
    def test_metrics_collection_script_can_run(self):
        """collect-metrics.py should be runnable."""
        # Once implemented
        pass
```

**Status:** ⏳ TODO (2 hours)

---

### Task 2.2: User Acceptance Testing (1 hour)

**Procedure:** Have a real new developer follow onboarding path

```
1. Select team member who hasn't used SPEC before
2. Measure time: python -c "import time; print(time.time())" before + after
3. Steps:
   a. Have them run: python docs/ia/SCRIPTS/setup-wizard.py
   b. Measure time taken
   c. Ask: "Did this help? Was it clear?"
   d. Did they get stuck? Where?
   e. Do they feel ready to code?
4. Record results
5. If time > 10 minutes: Investigate why
6. If confused at any step: Improve guidance
```

**Success criteria:**
- Time < 10 minutes
- Confidence level > 7/10
- Zero blockers

**Status:** ⏳ TODO (1 hour, requires team member)

---

### Task 2.3: Second Project Validation (1 hour)

**Procedure:** Use generate-specializations.py for hypothetical project

```
1. Create test config: docs/ia/SPECIALIZATIONS_CONFIG_GAMEMASTER.md
   project:
     name: game-master-api
     domain: Game Master API (different from campaigns)
     concurrent_entities: 1000+ (very different scale)
     
2. Run: python docs/ia/SCRIPTS/generate-specializations.py --project game-master-api --dry-run

3. Validate:
   - Generated files are reasonable
   - No domain assumptions from rpg-narrative-server leak through
   - Specializations are correctly adapted

4. If fails: Document what template doesn't handle, improve template

5. If succeeds: Confirms pattern is generalizable
```

**Success criteria:**
- Script completes without error
- Generated files are sensible
- No rpg-specific assumptions in output

**Status:** ⏳ TODO (1 hour)

---

## 🎯 PHASE 3: DOCUMENTATION & CLARITY (5 hours)

### Task 3.1: Operational Runbooks (3 hours)

**Deliverable:** 5 new guides in `/docs/ia/guides/operational/`

1. **ADDING_NEW_PROJECT.md** (1 hour)
   ```
   Step-by-step: Add project 2, 3, 4, etc.
   - Run generate-specializations.py
   - Validate output
   - Add to CI/CD
   - Test enforcement for new project
   - Add to documentation index
   ```

2. **TROUBLESHOOTING_SPEC_VIOLATIONS.md** (30 min)
   ```
   My PR got rejected:
   "ERROR: Path 'docs/ia/REALITY/...' not allowed in CANONICAL"
   
   Solution A: Moving to right location
   Solution B: If legitimate exception, document
   ```

3. **HANDLING_MERGE_CONFLICTS.md** (30 min)
   ```
   Merge conflict in ia-rules.md
   - Don't just auto-resolve
   - Understand which side is "newer"
   - Validate both changes are needed
   - Test enforcement after merge
   ```

4. **ONBOARDING_PATH_SELECTION.md** (30 min)
   ```
   Which path for new developers?
   - New approach: setup-wizard.py (primary, 10 min)
   - Legacy approach: FIRST_SESSION_SETUP.md (fallback)
   - When to use each
   - Deprecation timeline
   ```

5. **INTEGRITY_RECOVERY.md** (30 min)
   ```
   If SPEC got corrupted:
   - Restore from git
   - Verify enforcement still works
   - Run tests
   - Document what went wrong
   ```

**Status:** ⏳ TODO (3 hours)

---

### Task 3.2: Clarify Compliance Gates (2 hours)

**File:** Update `/docs/ia/CANONICAL/specifications/compliance.md`

**Changes:**
1. Add operational verification steps for EACH gate
2. Link to CI/CD job that enforces
3. Add troubleshooting for failures
4. Add SLOs (service level objectives)

**Example:**

```markdown
### Code Quality Gate #1: Coverage Threshold

#### Specification
Domain layer: 95% minimum
Application layer: 85% minimum
Infrastructure layer: 80% minimum

#### Verification (What to run)
```bash
pytest --cov=src/rpg_narrative_server \
       --cov-report=term-missing \
       --cov-fail-under=95
```

#### Automated Enforcement
CI/CD Job: .github/workflows/test-coverage.yml
Trigger: Every push
Blocking: Yes (PR cannot merge if fails)
SLO: Must complete in < 2 minutes

#### If Gate Fails
See: docs/ia/guides/troubleshooting/COVERAGE_GATE_FAILED.md

#### Exceptions
To request exception:
1. File issue: "Coverage exception request"
2. Provide justification
3. Requires tech lead approval
4. Must document in DECISIONS.md
```

**Status:** ⏳ TODO (2 hours)

---

## 📋 SUMMARY OF ALL TASKS

| # | Task | Hours | Owner | Blocking? |
|---|------|-------|-------|-----------|
| 1.1 | Emergency Procedures | 2h | Sergio | 🔴 YES |
| 1.2 | CI/CD Integration | 2h | Sergio | 🔴 YES |
| 1.3 | Onboarding Path | 1h | Sergio | 🔴 YES |
| 1.4 | Metrics Infrastructure | 1h | Sergio | 🟡 MEDIUM |
| 2.1 | Test Suite | 2h | Sergio | 🔴 YES |
| 2.2 | User Testing | 1h | Team member | 🟡 MEDIUM |
| 2.3 | Second Project | 1h | Sergio | 🟡 MEDIUM |
| 3.1 | Operational Runbooks | 3h | Sergio | 🔴 YES |
| 3.2 | Compliance Clarity | 2h | Sergio | 🟡 MEDIUM |

**Total Effort:** 15 hours (mandatory) + 5 hours (validation) = **20 hours**

---

## 📅 RECOMMENDED SCHEDULE

### Monday (6 hours)
- Task 1.1: Emergency Procedures (2h)
- Task 1.2: CI/CD Integration (2h)
- Task 1.3: Onboarding Path (1h)
- Task 1.4: Metrics Infrastructure (1h)

### Tuesday (5 hours)
- Task 2.1: Test Suite (2h)
- Task 3.1: Operational Runbooks (3h) — Start in parallel

### Wednesday (5 hours)
- Task 3.1: Continue (1h)
- Task 2.2: User Testing (1h)
- Task 2.3: Second Project (1h)
- Task 3.2: Compliance Clarity (2h)

### Thursday (3 hours)
- Integration testing + QA (3h)

### Friday (1 hour)
- Team communication + deployment (1h)

**Total:** 20 hours over 5 days = ~4 hours per day

---

## 🎯 SUCCESS CRITERIA (v2.2 Readiness)

Before marking v2.2 complete, MUST verify:

- [ ] All 4 scripts integrated to CI/CD (blocking jobs)
- [ ] All 4 scripts have 90%+ test coverage
- [ ] Emergency procedures documented (all 7 scenarios)
- [ ] Onboarding path unambiguous (one PRIMARY, one LEGACY)
- [ ] Metrics collection working (automated or at least runnable)
- [ ] Second project created (validates SPECIALIZATIONS)
- [ ] Real developer tested (actual time measured)
- [ ] All runbooks written (5 operational guides)
- [ ] Compliance gates linked to enforcement (executable procedures)
- [ ] .github/copilot-instructions.md updated (new onboarding path)

**Quality target for v2.2:** 8.0/10 (up from 5.0/10)

---

## 🚨 BEFORE STARTING

**Pre-conditions that must be satisfied:**

1. ✅ WORLD_CLASS_REVIEW_V2.md (this document's findings) committed
2. ✅ Team agrees this is critical path (not optional)
3. ✅ Sergio owns tasks 1.1-3.2
4. ✅ Team member available Tuesday-Wednesday for UAT (Task 2.2)
5. ✅ No production incidents competing for attention

**If any pre-condition not met: Delay until satisfied.**

---

## 📌 KEY INSIGHT

**Quality didn't improve from v2.0 → v2.1 because:**

```
Shipped features without:
  ❌ Tests proving they work
  ❌ Integration into production systems
  ❌ Operational procedures for failures
  ❌ Measurement proving improvements real
  ❌ Runbooks for common problems

This is the opposite of world-class engineering.
```

**This recovery plan restores that discipline.**

---

## ✅ Next Step

1. Read this plan carefully
2. Commit WORLD_CLASS_REVIEW_V2.md + this file
3. Start Phase 1 Monday morning
4. Update this file as tasks complete
5. Document any blockers immediately

**Estimated completion:** End of week (Friday 5pm)
