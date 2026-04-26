# 🔄 SDD v2.1 → v3.0 Migration

**Status:** Staging (Parallel to v2.1 Legacy)  
**Timeline:** Phase 1-6 over 6 weeks (complete by mid-June 2026)  
**Goal:** Seamless transition with zero downtime

---

## 📋 Overview

This migration path allows **parallel operation** of v2.1 (legacy) and v3.0 (new) systems until cutover is ready.

```
┌─────────────────────────────────────┐
│  PHASE 1-5: Parallel (Safe)        │
│  ├─ v2.1 running (production)      │
│  ├─ v3.0 being prepared (staging)  │
│  └─ No impact on users             │
├─────────────────────────────────────┤
│  PHASE 6: Cutover (Quick)          │
│  ├─ Final validation               │
│  ├─ Switch to v3.0                 │
│  ├─ v2.1 archived (backup)         │
│  └─ Rollback ready if needed       │
└─────────────────────────────────────┘
```

---

## 🚀 Quick Start

### 1. Check Prerequisites
```bash
cd .sdd-migration
python -m pytest tests/ -v
```

### 2. Extract v2.1 → v3.0
```bash
python tooling/migrate.py --source ../EXECUTION/spec/CANONICAL/ --output output/
```

### 3. Validate Output
```bash
python tooling/migration_validator.py --check output/
```

### 4. Review Changes
```bash
# See detailed extraction report
cat reports/extraction_report.json

# See validation results
cat reports/validation_report.json
```

---

## 📚 What's Included

```
.sdd-migration/
├── README.md (this file)
│  └─ Start here, overview
│
├── PHASES.md
│  └─ 6-phase detailed plan with checklist
│
├── CUTOVER.md
│  └─ Final critical steps (passo-a-passo)
│
├── tooling/
│  ├── migrate.py (orchestrator - RUN THIS!)
│  ├── constitution_parser.py (parse v2.1)
│  ├── dsl_converter.py (convert to DSL)
│  ├── guidelines_extractor.py (extract soft rules)
│  ├── migration_validator.py (validate output)
│  ├── __init__.py
│  └── requirements.txt
│
├── tests/
│  ├── test_migration_v2_to_v3.py
│  ├── conftest.py
│  └── fixtures/
│     ├── v2_sample.md (test input)
│     └── v3_expected.spec (expected output)
│
├── input/
│  ├── SOURCES.md (file mapping)
│  └── sources.txt
│
├── output/
│  ├── mandate.spec (v3.0 compiled)
│  ├── guidelines.dsl (v3.0 compiled)
│  └─ .gitkeep
│
└── reports/
   ├── extraction_report.json (detail)
   ├── validation_report.json (validation)
   └─ .gitkeep
```

---

## 🎯 Key Concepts

### MANDATE (Tier 1: Hard Rules)
- Non-negotiable, immutable
- 2 mandates from v2.1 EXECUTION/spec/CANONICAL/
- Example: "Architecture must follow layering principle"

### GUIDELINES (Tier 2: Soft Patterns)
- Customizable, overridable
- 150 guidelines extracted from constitution.md
- Example: "Prefer composition over inheritance"

### OPERATIONS (Tier 3: Runtime State)
- Agent-managed, session-scoped
- Cache, progress tracking, project-specific utilities
- v3.0: skeleton ready; v3.1+: populated

---

## 🔍 Migration Extraction

**Source:** `EXECUTION/spec/CANONICAL/rules/constitution.md` (v2.1)

**Extraction Process:**

```
1. Parse constitution.md
   ├─ Identify mandates (M001-M002)
   ├─ Identify guidelines (G01-G150)
   └─ Identify patterns (telemetry, formatting, etc.)

2. Convert to DSL
   ├─ Mandates → mandate.spec
   ├─ Guidelines → guidelines.dsl
   └─ Patterns → RTK patterns

3. Compile to Binary
   ├─ mandate.spec → .msgpack (binary, optimized)
   ├─ Compute fingerprints (for audit)
   └─ Generate metadata.json (hash, versions)

4. Validate
   ├─ Check: all mandates present
   ├─ Check: all guidelines convertible
   ├─ Check: fingerprints match
   └─ Report: extraction_report.json
```

---

## 📊 Migration Statistics

| Metric | v2.1 | v3.0 | Change |
|--------|------|------|--------|
| Mandates | 2 | 2 | ✅ Same |
| Guidelines | 150 | 150 | ✅ Same (organized) |
| Storage | 500KB JSON | 25KB binary | 📉 95% smaller |
| Parse time | 5-10ms | 1-3ms | ⚡ 3-5x faster |
| RTK patterns | Manual | 50+ automated | ✨ Deduplication |
| Fingerprint validation | ❌ None | ✅ Full audit trail | 🔒 Security |

---

## 🎬 Six Phases

```
PHASE 1: Discovery (Week 1)
  └─ Map v2.1 → v3.0 concepts
     
PHASE 2: Extraction (Week 2)
  └─ Parse constitution.md, extract mandates/guidelines
     
PHASE 3: Conversion (Week 2-3)
  └─ Convert to DSL, compile to binary
     
PHASE 4: Validation (Week 3)
  └─ Comprehensive testing, reporting
     
PHASE 5: Documentation (Week 4)
  └─ User guides, migration docs, ADRs
     
PHASE 6: Cutover (Week 5-6)
  └─ Final preparation, switch, rollback ready
```

**See PHASES.md for detailed checklist.**

---

## 🔴 Cutover Checklist

When v3.0 is ready to go live:

```
FINAL VERIFICATION (Friday before cutover):
  [ ] All 111 tests passing
  [ ] All extraction validated (reports/)
  [ ] Fingerprints match expected values
  [ ] Migration tests passing
  [ ] v2.1 backup created
  [ ] Rollback procedure documented

CUTOVER DAY (Monday):
  [ ] Final extraction run
  [ ] Deploy .sdd-core/ to production
  [ ] Deploy .sdd-guidelines/ to production
  [ ] Deploy agents (updated loader)
  [ ] Monitor: no errors for 1 hour
  [ ] Verify: fingerprints match audit trail

POST-CUTOVER (Week 1):
  [ ] Archive v2.1 (EXECUTION/ → backup/)
  [ ] Update client .sdd/ templates
  [ ] Publish migration guide
  [ ] Celebrate! 🎉
```

**See CUTOVER.md for full procedure.**

---

## 📖 Documentation

- **PHASES.md** - 6-phase detailed plan with all tasks
- **CUTOVER.md** - Final critical steps (passo-a-passo)
- **input/SOURCES.md** - File mapping (v2.1 → v3.0)

---

## 🛠️ Tooling

All scripts in `tooling/`:

```bash
# Install dependencies
pip install -r tooling/requirements.txt

# Extract v2.1 → v3.0
python tooling/migrate.py --source ../EXECUTION/ --output output/

# Validate extraction
python tooling/migration_validator.py --check output/

# Run tests
pytest tests/ -v --cov=tooling
```

---

## ✅ Success Criteria

```
EXTRACTION COMPLETE when:
  ✅ mandate.spec contains all 2 mandates (M001, M002)
  ✅ guidelines.dsl contains all 150 guidelines (G01-G150)
  ✅ Binary compilation succeeds (mandate.compiled.msgpack)
  ✅ Fingerprints computed and stored
  ✅ All tests passing
  ✅ extraction_report.json shows 100% conversion
  ✅ validation_report.json shows 0 errors

MIGRATION COMPLETE when:
  ✅ v3.0 deployed to production
  ✅ All agents using new loader
  ✅ No rollback needed (stable 24h)
  ✅ Client templates updated
  ✅ Documentation published
```

---

## 🆘 Troubleshooting

### "Migration parser fails on constitution.md"
→ Check: input/SOURCES.md has correct file mapping
→ Run: `python tooling/constitution_parser.py --debug`

### "Fingerprints don't match"
→ Check: mandate.spec is byte-for-byte identical
→ Run: `python tooling/migration_validator.py --fingerprint-debug`

### "Guidelines extraction incomplete"
→ Check: guidelines_extractor.py covers all G01-G150
→ Run: `python tooling/guidelines_extractor.py --verbose`

### "Test fixtures outdated"
→ Run: `python tooling/migrate.py --update-fixtures`

---

## 📞 Contact

Migration lead: See PHASES.md (Phase Owner column)  
Escalation: See CUTOVER.md (Emergency Procedures)

---

## 📅 Timeline at a Glance

```
WEEK 1 (Apr 28-May 2):    PHASE 1-2 (Discovery + Extraction)
WEEK 2 (May 5-9):         PHASE 2-3 (Conversion + initial tests)
WEEK 3 (May 12-16):       PHASE 3-4 (Validation + reports)
WEEK 4 (May 19-23):       PHASE 5 (Documentation)
WEEK 5-6 (May 26-Jun 6):  PHASE 6 (Cutover + stabilization)

TARGET: v3.0 LIVE by mid-June 2026
```

---

**Status:** Ready for Phase 1  
**Next Action:** Review PHASES.md for detailed checklist
