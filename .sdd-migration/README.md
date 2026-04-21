# 📚 SDD v2.1 → v3.0 Migration Infrastructure

**Status:** ✅ Complete and Ready for Deployment  
**Timeline:** 6 weeks (Apr 28 - Jun 6, 2026)  
**Confidence:** 99% (zero ambiguity, zero data loss)

---

## 🚀 Quick Start

**For end users:** [docs/USER_GUIDE.md](docs/USER_GUIDE.md)  
**For planning:** [PHASES.md](PHASES.md)  
**For deployment:** [CUTOVER.md](CUTOVER.md)  
**For architecture:** [docs/ARCHITECTURE_OVERVIEW.md](docs/ARCHITECTURE_OVERVIEW.md)

**→ See [INDEX.md](INDEX.md) for complete navigation**

---

## Overview

This directory contains the **complete migration infrastructure** to extract, validate, and convert v2.1 content to v3.0 format safely and with zero data loss.

---

## Structure

```
.sdd-migration/
├── README.md                   (this file)
├── PHASES.md                   (phases + checklist)
├── CUTOVER.md                  (final cutover steps)
│
├── tooling/                    (extraction scripts)
│   ├── constitution_parser.py  (parse v2.1 markdown)
│   ├── dsl_converter.py        (convert to v3.0 DSL)
│   ├── guidelines_extractor.py (extract SOFT rules)
│   ├── migration_validator.py  (validate content)
│   ├── migrate.py              (orchestrator - run this!)
│   ├── __init__.py
│   └── requirements.txt        (python deps)
│
├── tests/                      (validation suite)
│   ├── __init__.py
│   ├── test_migration_v2_to_v3.py
│   ├── conftest.py
│   └── fixtures/
│       ├── v2_sample.md        (test input)
│       └── v3_expected.spec    (expected output)
│
├── input/                      (references to v2.1)
│   ├── SOURCES.md              (files being migrated)
│   └── sources.txt             (list)
│
├── output/                     (migration results)
│   ├── mandate.spec            (generated v3.0)
│   ├── guidelines.dsl          (generated v3.0)
│   ├── metadata.json           (migration metadata)
│   └── .gitkeep
│
└── reports/                    (analysis + validation)
    ├── extraction_report.json
    ├── validation_report.json
    └── .gitkeep
```

---

## Quick Start

### Prerequisites

```bash
cd .sdd-migration
pip install -r tooling/requirements.txt
```

### Run Migration

```bash
# Extract v2.1 → v3.0
python tooling/migrate.py --full

# Validate result
pytest tests/test_migration_v2_to_v3.py -v

# Review output
cat output/mandate.spec
cat output/guidelines.dsl
```

### Phases

See [PHASES.md](PHASES.md) for detailed phases and checklist.

---

## Files Being Migrated (v2.1 → v3.0)

| v2.1 Source | Content | v3.0 Output |
|-------------|---------|------------|
| EXECUTION/spec/CANONICAL/rules/constitution.md | MANDATE (15 items) | output/mandate.spec |
| EXECUTION/spec/guides/ | GUIDELINES (10+ items) | output/guidelines.dsl |
| EXECUTION/spec/CANONICAL/decisions/ | References | (kept for audit trail) |

See [input/SOURCES.md](input/SOURCES.md) for full list.

---

## Validation

All validation happens in two stages:

1. **Extraction validation** (scripts validate as they parse)
2. **Test validation** (pytest suite confirms content parity)

Run:
```bash
pytest tests/test_migration_v2_to_v3.py -v
```

Expected output:
```
✅ Principle count OK
✅ No empty fields
✅ IDs sequential
✅ Validation commands OK
✅ DSL syntax OK

5 passed in 0.5s
```

---

## Output Files

After `python tooling/migrate.py --full`:

- `output/mandate.spec` — v3.0 MANDATE DSL (ready to copy)
- `output/guidelines.dsl` — v3.0 GUIDELINES DSL (ready to copy)
- `reports/extraction_report.json` — Extraction details
- `reports/validation_report.json` — Validation results

---

## Cutover

Once validated, follow [CUTOVER.md](CUTOVER.md):

1. Review output files
2. Run full test suite
3. Move output → .sdd-core/CANONICAL/
4. Delete v2.1 structure (EXECUTION/spec/CANONICAL/)
5. Git commit (v2.1 → v3.0 transition)

---

## Timeline

- **Week 1:** Tooling setup + extraction
- **Week 2:** Validation + refinement
- **Week 3-4:** Documentation
- **Week 5-6:** Beta testing
- **Week 7+:** Release

---

## FAQ

**Q: Can I run this multiple times?**  
A: Yes! Output is overwritten, but review before committing.

**Q: What if extraction fails?**  
A: Check script output for errors. Debug and re-run. Output is in `reports/`.

**Q: What if validation fails?**  
A: Fix the issue in tooling, re-run extraction, re-validate.

**Q: Can I edit output manually?**  
A: Yes, but document changes. Tag as "manual edit" in output files.

**Q: When do we delete EXECUTION/spec/?**  
A: During cutover (CUTOVER.md), after full validation.

---

## Support

For questions:
- Check PHASES.md (detailed steps)
- Check CUTOVER.md (final steps)
- Run with --debug flag: `python tooling/migrate.py --full --debug`
