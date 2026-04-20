# 🔍 RPG-Narrative-Server → Framework Gap Analysis

**Date:** April 19, 2026  
**Analysis:** Audit of rpg-narrative-server to extract patterns for framework authority  
**Status:** Framework is COMPREHENSIVE, some patterns need explicit documentation

---

## 📊 What rpg-narrative-server Discovered

### ✅ ALREADY IN FRAMEWORK (Proper Authority)

1. **8-Layer Clean Architecture**
   - Domain, UseCases, Interfaces, Frameworks, Infrastructure, Bootstrap, Config, Shared
   - ✅ Documented in: `CANONICAL/specifications/architecture.md`
   - ✅ Enforced via ADR-002

2. **Ports & Adapters Pattern**
   - Infrastructure accessed ONLY through ports
   - ✅ Documented in: `CANONICAL/decisions/ADR-003`
   - ✅ Example: StoragePort, ConfigPort pattern

3. **Thread Isolation**
   - Each thread owns its code modifications
   - ✅ Documented in: `CANONICAL/decisions/ADR-004`
   - ✅ Enforced via execution-state tracking

4. **.spec.config Pattern**
   - INI configuration for framework discovery
   - ✅ Documented in: `CANONICAL/decisions/ADR-006`
   - ✅ Template exists in INTEGRATION/templates/

5. **Context-Aware Infrastructure (.ai/context-aware/)**
   - ✅ Documented in: `guides/runtime/CONTEXT_AWARE_USAGE.md`
   - ✅ Structure: task-progress, analysis, runtime-state
   - ✅ Just standardized with 3-tier structure

6. **PHASE 0 Onboarding**
   - Agent-driven initialization (30-40 min)
   - ✅ Documented in: `guides/onboarding/PHASE-0-AGENT-ONBOARDING.md`
   - ✅ Automation available: SCRIPTS/phase-0-agent-onboarding.py

7. **AGENT_HARNESS (7-phase workflow)**
   - ✅ Documented in: `guides/onboarding/AGENT_HARNESS.md`
   - ✅ Covers: Lock rules → Check state → Choose path → Load context → Implement → Validate → Checkpoint

---

## ⚠️ DISCOVERED BUT NEEDS EXPLICIT DOCUMENTATION

### 1. Runtime Indices (.ai/runtime/) — MISSING MANDATE

**What:** rpg-narrative-server uses:
- `spec-canonical-index.md` — Index to CANONICAL documents
- `spec-guides-index.md` — Index to guides
- `search-keywords.md` — Keyword mapping to documents

**Status:** Created BY PHASE 0, but NOT explicitly mandated in framework

**Issue:** Framework doesn't say "agents MUST create these"

**What Needs to be Added:**
- [ ] Document as **MANDATORY post-PHASE-0** files
- [ ] Add to PHASE-0 automation script
- [ ] Create templates in INTEGRATION/templates/

**Where to Document:**
- `guides/runtime/RUNTIME_INDICES_SPECIFICATION.md` (NEW)
- Update `PHASE-0-AGENT-ONBOARDING.md` Step 6 with runtime indices requirement

---

### 2. Architecture Compliance Tests — MISSING MANDATE

**What:** rpg-narrative-server enforces via:
- `tests/specs-ia-units/test_layer_isolation.py` — Domain ≠ Infrastructure
- `tests/specs-ia-units/test_port_contracts.py` — Use ports for abstraction
- `tests/specs-ia-units/test_thread_isolation.py` — Thread safety
- `tests/specs-ia-units/test_specialization_compliance.py` — Project rules
- `tests/architecture/test_spec_compliance.py` — Governance validation

**Status:** rpg-narrative-server DISCOVERED this need, but framework doesn't mandate it

**Issue:** Framework doesn't explicitly require projects to have architecture tests

**What Needs to be Added:**
- [ ] Document as **MANDATORY test suite requirement**
- [ ] Create templates in `INTEGRATION/templates/tests/specs-ia-units/`
- [ ] Add to INTEGRATION/README.md Step 2 "Copy architecture tests"
- [ ] Add to CI/CD requirements

**Where to Document:**
- `CANONICAL/rules/ENFORCEMENT_RULES.md` (NEW) — Governance enforcement mechanism
- `CANONICAL/specifications/testing.md` — Add "Architecture compliance tests" section
- `guides/operational/ARCHITECTURE_VALIDATION.md` (NEW) — How to write compliance tests

---

### 3. Specialization Folder Structure — NEEDS CLARIFICATION

**What:** rpg-narrative-server uses:
```
docs/ia/custom/rpg-narrative-server/
├── development/
│   ├── execution-state/
│   └── [project-specific decisions]
├── reality/
│   └── [observed system reality]
└── SPECIALIZATIONS/
    └── constitution-rpg-specific.md
```

**Status:** Partially documented, but structure not crystal clear

**Issue:** Framework mentions "custom/" but doesn't clearly explain subfolders

**What Needs to be Added:**
- [ ] Clear mandate for `development/` vs `reality/` distinction
- [ ] Explain `SPECIALIZATIONS/` folder purpose
- [ ] Document what goes in each

**Where to Document:**
- `CANONICAL/specifications/PROJECT_STRUCTURE.md` (NEW)
- Or update `CANONICAL/decisions/ADR-006.md` to clarify custom/ structure

---

### 4. ENFORCEMENT_RULES.md — MISSING

**What:** rpg-narrative-server expects:
- How rules are enforced?
- Pre-commit hooks?
- CI/CD gates?
- Manual review points?

**Status:** Not documented in framework authority

**Issue:** Framework has rules but doesn't document HOW they're enforced

**What Needs to be Added:**
- [ ] Create `CANONICAL/rules/ENFORCEMENT_RULES.md`
- [ ] Document pre-commit hook strategy
- [ ] Document CI/CD validation gates
- [ ] Document manual review checkpoints
- [ ] Document penalty for violations

**Where to Document:**
- `CANONICAL/rules/ENFORCEMENT_RULES.md` (NEW - **CRITICAL**)

---

### 5. CI/CD Integration Pattern — NEEDS DOCUMENTATION

**What:** rpg-narrative-server does:
```yaml
# In .github/workflows/ci.yml
- name: Validate SPEC Architecture
  run: pytest tests/specs-ia-units/ -v --tb=short
```

**Status:** Mentioned in rpg-narrative-server code, but NOT documented in framework

**Issue:** Projects don't know WHAT tests to run in CI/CD

**What Needs to be Added:**
- [ ] Document as **required CI/CD gates**
- [ ] Template GitHub Actions workflow
- [ ] Specify command line requirements

**Where to Document:**
- `guides/operational/CI_CD_INTEGRATION.md` (NEW)
- Add template in `INTEGRATION/templates/.github/workflows/`

---

### 6. Specialization Compliance Tests — NEEDS FORMAL SPEC

**What:** rpg-narrative-server does:
```python
def test_concurrent_campaign_limit(self):
    """rpg-narrative-server limits to 50 concurrent campaigns."""
    spec_file = Path("docs/ia/custom/rpg-narrative-server/SPECIALIZATIONS/...")
    # Verify specialization compliance
```

**Status:** Pattern used, but not formally specified in framework

**Issue:** Framework doesn't explain HOW to write specialization compliance tests

**What Needs to be Added:**
- [ ] Document specialization test pattern
- [ ] Create template for specialization compliance tests
- [ ] Explain when to use vs architecture tests

**Where to Document:**
- `guides/operational/SPECIALIZATION_TESTING.md` (NEW)

---

## ✅ REVERSE DEPENDENCY CHECK

**Question:** Does rpg-narrative-server reference sdd-architecture in ways that would make sdd-architecture dependent on rpg?

**Files Checked:**
- `.spec.config` — GOOD: Points to sdd-architecture, no reference back ✅
- `README.md` — GOOD: Mentions "SPEC framework", generic ✅
- `.vscode/ai-rules.md` — GOOD: Generic rules reference ✅
- `.github/copilot-instructions.md` — References SPEC via `.spec.config`, clean ✅
- Tests — GOOD: Reference generic patterns, not specific sdd files ✅

**Conclusion:** ✅ NO REVERSE DEPENDENCY FOUND

rpg-narrative-server correctly uses sdd-architecture as authority source, not the other way around.

---

## 📋 Complete Gap List with Priority

### CRITICAL (Framework Incomplete Without These)

| # | Issue | Impact | Effort | Add Where |
|---|-------|--------|--------|-----------|
| 1 | ENFORCEMENT_RULES.md missing | How rules enforced? | 1 day | CANONICAL/rules/ |
| 2 | Architecture tests not mandated | Projects don't validate | 1 day | guides/operational/ |
| 3 | Runtime indices not mandated | Agent context incomplete | 4 hours | guides/runtime/ |

### HIGH (Should Have for Completeness)

| # | Issue | Impact | Effort | Add Where |
|---|-------|--------|--------|-----------|
| 4 | Specialization folder structure unclear | Projects confused | 2 hours | CANONICAL/specifications/ |
| 5 | CI/CD integration pattern missing | Projects miss gates | 4 hours | guides/operational/ |
| 6 | Specialization test pattern missing | No compliance check | 4 hours | guides/operational/ |

### MEDIUM (Nice to Have)

| # | Issue | Impact | Effort | Add Where |
|---|-------|--------|--------|-----------|
| 7 | Runtime indices templates missing | Projects start from scratch | 2 hours | INTEGRATION/templates/ |
| 8 | Architecture tests templates missing | Projects start from scratch | 4 hours | INTEGRATION/templates/ |

---

## 🎯 Implementation Order

### Phase 1: CRITICAL (Do Today)

1. **Create ENFORCEMENT_RULES.md** (2 hours)
   - File: `EXECUTION/spec/CANONICAL/rules/ENFORCEMENT_RULES.md`
   - Content: Pre-commit, CI/CD, manual review, penalties
   - Reference in: ia-rules.md

2. **Create ARCHITECTURE_VALIDATION.md** (2 hours)
   - File: `EXECUTION/spec/guides/operational/ARCHITECTURE_VALIDATION.md`
   - Content: How to write compliance tests, templates, examples
   - Reference in: AGENT_HARNESS, testing.md

3. **Create RUNTIME_INDICES_SPECIFICATION.md** (1 hour)
   - File: `EXECUTION/spec/guides/runtime/RUNTIME_INDICES_SPECIFICATION.md`
   - Content: What are runtime indices, when created, purpose
   - Reference in: PHASE-0-AGENT-ONBOARDING.md

### Phase 2: HIGH (This Week)

4. Update PHASE-0-AGENT-ONBOARDING.md
   - Add Step 6: Runtime indices creation
   - Add Step 7: Architecture tests verification
   - Estimated: 1 hour

5. Create CI_CD_INTEGRATION.md (2 hours)
   - Include GitHub Actions template
   - Document required gates
   - Examples from rpg-narrative-server

6. Update architecture.md specialization section (1 hour)

### Phase 3: MEDIUM (Next Sprint)

7. Create templates in INTEGRATION/templates/tests/ (2 hours)
8. Create templates in INTEGRATION/templates/.github/ (1 hour)
9. Create templates in INTEGRATION/templates/.ai/runtime/ (1 hour)

---

## 📝 Summary: Framework Authority Status

**Good News:** ✅ Framework has 90% of what's needed

**Pattern:** rpg-narrative-server didn't invent new patterns, it DISCOVERED patterns the framework implied and is systematizing

**Task:** Document what's implicit explicitly

**Result:** Framework becomes MORE AUTHORITATIVE by formalizing enforcement mechanisms

---

## 🚀 Next Action

Suggest committing:
1. ENFORCEMENT_RULES.md (critical)
2. ARCHITECTURE_VALIDATION.md (critical)
3. RUNTIME_INDICES_SPECIFICATION.md (critical)

Then in follow-up PR:
4. Updates to PHASE-0 automation
5. New templates in INTEGRATION/

---

**Analysis Date:** April 19, 2026  
**Finding:** Framework is SOLID, enforcement mechanisms need documentation  
**Confidence:** 95% complete, 5% documentation gaps
