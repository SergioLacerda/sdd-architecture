# 🚀 NEXT IMMEDIATE ACTIONS - SDD v3.0 Wizard Implementation

**Date:** April 21, 2026  
**Current Status:** Phase 6A Complete | Phase 6C Ready to Start  
**Estimated Time for Phase 6C-D:** 3 weeks  
**Complexity:** Medium (well-defined, fully documented)

---

## 📋 Prioritized Action Items

### Priority 1: Decision (Before Starting Implementation)

**Question:** Which direction for wizard implementation?

**Option A: Start with Phase 1-2 (Foundation)**
- Create `wizard.py` entry point with CLI
- Implement Phase 1: Validate SOURCE
- Implement Phase 2: Load COMPILED
- Time: 3-4 days
- Benefit: Proven foundation, early testing
- **RECOMMENDED** ✅

**Option B: Generate Code from Blueprints**
- Use existing blueprints in `IMPLEMENTATION_PHASES_6.md`
- Generate all 7 phases at once
- Time: 5-7 days
- Benefit: Faster, but larger change set
- Risk: More to test at once

**Decision to Make:** Option A or B?

---

### Priority 2: Create Wizard Entry Point (Next 2 hours)

**File to Create:** `.sdd-wizard/src/wizard.py`

**Minimal Implementation:**
```python
#!/usr/bin/env python
"""
SDD v3.0 Wizard - Interactive CLI for project generation
Transforms architect specs into client-ready projects
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime


def create_argument_parser():
    """Create and configure CLI argument parser"""
    parser = argparse.ArgumentParser(
        description="Generate SDD project from compiled specifications",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Interactive mode:
    python wizard.py
  
  Non-interactive mode:
    python wizard.py --language java --mandates M001 --profile lite --output ~/my-project/
  
  Dry-run (preview without creating files):
    python wizard.py --language java --dry-run --verbose
        """
    )
    
    parser.add_argument(
        "--language",
        choices=["java", "python", "js"],
        help="Target programming language"
    )
    
    parser.add_argument(
        "--mandates",
        help="Comma-separated mandate IDs (e.g., M001,M002)"
    )
    
    parser.add_argument(
        "--profile",
        choices=["lite", "full"],
        default="lite",
        help="Guideline profile level (default: lite)"
    )
    
    parser.add_argument(
        "--output",
        type=Path,
        help="Output directory for generated project"
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview without creating files"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed output"
    )
    
    return parser


def main():
    """Main entry point"""
    parser = create_argument_parser()
    args = parser.parse_args()
    
    print("🔮 SDD v3.0 Wizard")
    print("=" * 50)
    print(f"Started: {datetime.now().isoformat()}")
    print()
    
    # TODO: Implement 7 phases here
    # Phase 1: Validate SOURCE
    # Phase 2: Load COMPILED
    # Phase 3: Filter mandates
    # Phase 4: Filter guidelines
    # Phase 5: Apply scaffold
    # Phase 6: Generate
    # Phase 7: Validate
    
    print("🚀 TODO: Implement wizard phases")
    print()
    print("=" * 50)
    print("✅ Ready to implement!")


if __name__ == "__main__":
    main()
```

**Testing:**
```bash
python .sdd-wizard/src/wizard.py --help
# Should show help with all options
```

**Status:** 30 minutes to create + test

---

### Priority 3: Implement Phase 1-2 (Next 2 days)

**Files to Create:**
1. `.sdd-wizard/src/loader.py` - Load artifacts
2. `.sdd-wizard/orchestration/phase_1_validate.py` - Validate SOURCE
3. `.sdd-wizard/orchestration/phase_2_load_compiled.py` - Load COMPILED
4. `.sdd-wizard/tests/test_phases_1_2.py` - Unit tests

**What Phase 1 Does:**
```
Input: .sdd-core/mandate.spec and .sdd-core/guidelines.dsl
- Check files exist
- Validate DSL syntax (balanced braces)
- Check for valid mandate IDs (M001, M002, etc.)
- Check for valid guideline IDs (G001, G002, etc.)
Output: Validation report (pass/fail)
```

**What Phase 2 Does:**
```
Input: .sdd-runtime/mandate.bin, guidelines.bin, metadata.json
- Deserialize binary files (msgpack or JSON)
- Load metadata audit trail
- Validate format version
Output: In-memory data structures ready for filtering
```

**Test Cases:**
```python
test_phase_1_validates_mandate_spec()
test_phase_1_validates_guidelines_dsl()
test_phase_1_fails_on_missing_files()
test_phase_1_fails_on_syntax_error()
test_phase_2_loads_mandates()
test_phase_2_loads_guidelines()
test_phase_2_validates_metadata()
test_phase_2_fails_on_corrupted_data()
```

**Status:** 2 days for phases 1-2 + tests

---

### Priority 4: Test Full Phase 1-2 Pipeline (Next 4 hours)

**Test Command:**
```bash
cd .sdd-wizard

# Unit tests
pytest tests/test_phases_1_2.py -v

# Integration test (end-to-end for phases 1-2)
python src/wizard.py --verbose --dry-run
# Should load and validate without errors
```

**Success Criteria:**
- ✅ All tests pass (8+ tests)
- ✅ CLI shows helpful output
- ✅ Both phases complete without errors
- ✅ Metadata loaded and displayed

**Status:** 4 hours for testing

---

### Priority 5: Implement Phase 3-4 (Week 2)

**Files to Create:**
1. `.sdd-wizard/orchestration/phase_3_filter_mandates.py`
2. `.sdd-wizard/orchestration/phase_4_filter_guidelines.py`
3. `.sdd-wizard/tests/test_phases_3_4.py`

**Phase 3: Filter Mandates**
```
Input: All mandates from .sdd-runtime/, user selections (M001, M002)
- User chooses which mandates to include
- Interactive: "Which mandates do you want? (M001, M002, etc.)"
Output: Filtered mandate list
```

**Phase 4: Filter Guidelines**
```
Input: All guidelines, language (java/python/js), profile (lite/full)
- Filter by language tags (remove non-relevant)
- Filter by priority level (lite=1-2, full=1-4)
Output: Filtered guideline list
```

**Status:** 2 days for phases 3-4 + tests

---

### Priority 6: Implement Phase 5-7 (Week 3)

**Files to Create:**
1. `.sdd-wizard/orchestration/phase_5_apply_scaffold.py`
2. `.sdd-wizard/orchestration/phase_6_generate.py`
3. `.sdd-wizard/orchestration/phase_7_validate.py`
4. `.sdd-wizard/generators/manifest_generator.py`
5. `.sdd-wizard/generators/metadata_generator.py`
6. `.sdd-wizard/tests/test_phases_5_7.py`
7. `.sdd-wizard/tests/test_end_to_end.py`

**Phase 5: Apply Scaffold**
```
Input: .sdd-wizard/templates/base/ files, metadata
- Load README-SDD.md, metadata-template.json, CI/CD workflow
- Substitute {{PLACEHOLDER}} with actual values
- {{LANGUAGE}}, {{PROFILE}}, {{MANDATES}}, {{TIMESTAMP}}
Output: Ready-to-use template content
```

**Phase 6: Generate**
```
Input: Filtered mandates, guidelines, scaffolds
- Create /output/.sdd/CANONICAL/
- Write mandate.spec, guidelines.dsl
- Copy scaffold files
- Create .md documentation
- Generate GitHub Actions workflow
Output: Complete project structure
```

**Phase 7: Validate**
```
Input: Generated project
- Check all required files exist
- Validate JSON syntax
- Check permissions
- Verify metadata integrity
Output: Validation report (pass/warnings/errors)
```

**Status:** 3 days for phases 5-7 + comprehensive testing

---

## 🎯 Weekly Timeline (Recommended)

### Week 1
| Day | Task | Effort | Status |
|-----|------|--------|--------|
| Mon | Setup + Phase 1-2 | 8h | Start |
| Tue | Phase 1-2 complete + tests | 8h | Execute |
| Wed | Phase 1-2 review + integration test | 8h | Verify |
| Thu | Phase 3-4 start | 8h | Plan |
| Fri | Phase 3-4 complete + tests | 8h | Execute |

**Goal:** Phases 1-4 complete and tested ✅

### Week 2
| Day | Task | Effort | Status |
|-----|------|--------|--------|
| Mon | Phase 5-7 start | 8h | Plan |
| Tue | Phase 6 generation + tests | 8h | Execute |
| Wed | Phase 7 validation + tests | 8h | Execute |
| Thu | E2E testing + fixes | 8h | Verify |
| Fri | Performance testing | 8h | Optimize |

**Goal:** All phases complete, E2E working ✅

### Week 3
| Day | Task | Effort | Status |
|-----|------|--------|--------|
| Mon | Documentation updates | 8h | Document |
| Tue | GitHub Actions CI/CD setup | 8h | Setup |
| Wed | Integration testing (full pipeline) | 8h | Verify |
| Thu | User acceptance testing | 8h | Test |
| Fri | Production hardening | 8h | Harden |

**Goal:** Production ready, v3.0.0 release ✅

---

## 📊 IMPLEMENTATION STATUS — Option A + Blueprints Hybrid ✅ CHOSEN

**Decision:** Use Option A (foundation-first) + Blueprints (copy code templates)

**Current State (April 22, 2026 16:56):**
- ✅ Phase 1: WORKING (validates mandate.spec + guidelines.dsl)
- ❌ Phase 2: Blocked (needs .sdd-runtime/ artifacts)
- ⏳ Phase 3-7: Ready to implement

**Next Immediate Actions:**

---

## 🚀 Starting Right Now

### Today (Next 2 Hours)
```bash
# 1. Make decision: Option A or B
# Recommendation: Start with Option A (Phase 1-2 foundation)

# 2. Create wizard entry point
touch .sdd-wizard/src/wizard.py
# Add the code from Priority 2 above

# 3. Test basic CLI
python .sdd-wizard/src/wizard.py --help
# Should show help with no errors
```

### This Week
```bash
# 4. Create loader.py and phase implementations
# Reference: .sdd-migration/IMPLEMENTATION_PHASES_6.md (has code blueprints)

# 5. Test phases 1-2
pytest .sdd-wizard/tests/test_phases_1_2.py -v

# 6. Commit progress
git add .sdd-wizard/
git commit -m "feat: implement wizard phases 1-2"
```

---

## 📞 Questions to Answer Now

1. **Format:** Should `.bin` files be true MessagePack or JSON is OK?
   - Current: JSON-named files (.bin extension but JSON content)
   - Upgrade path: Convert to true MessagePack later

2. **CLI Style:** Interactive prompt or argument-only?
   - Recommended: Both (auto-detect based on args)

3. **Validation Level:** Strict or lenient?
   - Recommended: Strict (fail fast on errors)

4. **Output Format:** Directory structure?
   - Reference: `.sdd-wizard/WORKFLOW_FLOW.md` (has examples)

---

## ✅ Success Criteria for Phase 6C-D

- [ ] `wizard.py` created and CLI works
- [ ] All 7 phases implemented
- [ ] 40+ unit tests passing
- [ ] E2E test: migration → compiler → wizard → delivery
- [ ] Performance: <2s for typical project generation
- [ ] Documentation complete
- [ ] Ready for production use

---

## 📁 File Structure (After Completion)

```
.sdd-wizard/
├── src/
│   ├── __init__.py
│   ├── wizard.py                 ✅ Main entry point
│   ├── loader.py                 ✅ Load artifacts
│   ├── validator.py              ✅ Validate integrity
│   ├── config.py                 ✅ Configuration
│   └── user_input.py             ✅ User interaction
│
├── orchestration/
│   ├── __init__.py
│   ├── phase_1_validate.py        ✅ Validate SOURCE
│   ├── phase_2_load.py            ✅ Load COMPILED
│   ├── phase_3_filter_mandates.py ✅ Filter mandates
│   ├── phase_4_filter_guidelines.py ✅ Filter guidelines
│   ├── phase_5_apply_scaffold.py  ✅ Apply templates
│   ├── phase_6_generate.py        ✅ Generate project
│   └── phase_7_validate.py        ✅ Validate output
│
├── generators/
│   ├── __init__.py
│   ├── manifest_generator.py      ✅ Create manifest
│   ├── metadata_generator.py      ✅ Create metadata
│   └── guideline_markdown.py      ✅ Generate .md files
│
├── validators/
│   ├── __init__.py
│   ├── source_validator.py        ✅ Validate source
│   ├── compiled_validator.py      ✅ Validate compiled
│   └── output_validator.py        ✅ Validate output
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py                ✅ Pytest config
│   ├── test_phases_1_2.py         ✅ Phases 1-2
│   ├── test_phases_3_4.py         ✅ Phases 3-4
│   ├── test_phases_5_7.py         ✅ Phases 5-7
│   └── test_end_to_end.py         ✅ E2E integration
│
├── ORCHESTRATION.md               ✅ Already complete
├── WORKFLOW_FLOW.md               ✅ Already complete
├── README.md                       ✅ Already complete
└── __init__.py
```

---

## 🎯 Decision Point

**Recommendation:** Start with Option A today

**Rationale:**
1. Well-defined phases (documented in IMPLEMENTATION_PHASES_6.md)
2. Clear success criteria
3. Each phase can be tested independently
4. Foundation-first approach reduces risk
5. 2-3 week timeline is achievable
6. CI/CD can be wired in parallel

**Next Meeting Agenda:**
1. Confirm wizard implementation approach (Option A/B)
2. Review Phase 1-2 implementation
3. Discuss MessagePack format decision
4. Confirm production timeline

---

**Ready to Start:** ✅ YES  
**Blocking Issues:** ❌ NONE  
**Confidence Level:** 🟢 HIGH  
**Recommended Action:** Begin Phase 1-2 implementation immediately
