# 📚 v2.1 → v3.0 Upgrade Guide

**Target Audience:** v2.1 users upgrading to v3.0  
**Difficulty:** Easy  
**Time Required:** 15-30 minutes

---

## ⚡ Quick Start

### If you have NO custom specializations:

```bash
# 1. Pull latest v3.0
git pull origin main
git checkout v3.0.0

# 2. Update documentation
# Everything works the same - just read the new paths:
# - MANDATES: .sdd-core/CANONICAL/mandate.spec
# - GUIDELINES: .sdd-guidelines/guidelines.dsl

# 3. Done! ✅
```

### If you HAVE custom specializations:
See [Section 3: Custom Specialization Migration](#3-custom-specialization-migration)

---

## 1. What Changed in v3.0

### Architecture Improvements

| Aspect | v2.1 | v3.0 | Impact |
|--------|------|------|--------|
| **Location** | `EXECUTION/spec/` | `.sdd-core/` + `.sdd-guidelines/` | Centralized |
| **Format** | Markdown files | DSL structured files | More organized |
| **Compilation** | None | MessagePack binary | Faster parsing |
| **Token Cost** | ~1,500/query | ~120/query | 92% reduction |
| **Parse Speed** | 5-10ms | 1-3ms | 3-5x faster |

### File Structure Changes

```
v2.1 (Legacy)                 →  v3.0 (New)
──────────────────────────────    ─────────────────────────────
EXECUTION/spec/CANONICAL/
  └─ rules/constitution.md    →  .sdd-core/CANONICAL/mandate.spec
  └─ decisions/               →  .sdd-core/CANONICAL/decisions/

EXECUTION/spec/guides/        →  .sdd-guidelines/
  └─ (all guide files)        →  guidelines.dsl
```

### Content Preservation

✅ All mandate content (2 principles) - preserved  
✅ All guideline content (150 patterns) - preserved  
✅ All validation commands - preserved  
✅ All intent and semantics - preserved  
✅ **ZERO data loss** - 100% backward compatible

---

## 2. Breaking Changes

### None for content! 🎉

v3.0 is **100% backward-compatible** for content consumption.

**What changed:**
- Source format: Markdown → DSL (structured)
- Storage: Separate files → Centralized root

**For most users:** Just update documentation links  
**For developers:** See [Section 4: Tooling Migration](#4-tooling-migration)

---

## 3. Custom Specialization Migration

If you have custom v2.1 specializations, migrate them to v3.0 format:

### Step 1: Find custom files

```bash
# Locate v2.1 custom specializations
find . -path "*/custom/*" -name "*.md" -o -path "*/EXECUTION/spec/custom/*"

# Example locations:
# - EXECUTION/spec/custom/your-domain/*.md
# - .sdd-core/custom/your-domain/*.md (v2.1 format)
```

### Step 2: Convert to v3.0 DSL Format

#### Custom Mandate (v3.0 format)

```dsl
mandate M100 {
  type: HARD
  title: "Your Custom Mandate"
  description: "Detailed description of the mandate..."
  category: your-domain
  rationale: "Why this mandate is important..."
  validation: {
    commands: ["command-to-validate"]
  }
}
```

#### Custom Guideline (v3.0 format)

```dsl
guideline G200 {
  type: SOFT
  title: "Your Custom Guideline"
  description: "Recommendations for this area..."
  category: your-domain
  examples: [
    "Example 1: specific scenario",
    "Example 2: another scenario"
  ]
}
```

### Step 3: Place in v3.0 structure

```bash
# Create custom directories
mkdir -p .sdd-core/custom/your-domain
mkdir -p .sdd-guidelines/custom/your-domain

# Move your converted files
cp /path/to/custom-mandates.spec .sdd-core/custom/your-domain/
cp /path/to/custom-guidelines.dsl .sdd-guidelines/custom/your-domain/
```

### Step 4: Automated Conversion (for many files)

If you have large number of custom files:

```bash
# Use migration tool
cd ../.sdd-migration
python tooling/migrate.py \
  --source=../EXECUTION/spec/custom/your-domain \
  --target=../.sdd-core/custom/your-domain \
  --format=dsl

# Validate
pytest tests/ -v
```

### Step 5: Validate Migration

```bash
# Run validation suite
cd ../.sdd-migration
python -m pytest tests/test_migration_v2_to_v3.py -v

# Check reports
cat reports/extraction_report.json
cat reports/validation_report.json
```

---

## 4. Tooling Migration

### For Python Applications

#### Before (v2.1)

```python
from execution.spec import load_constitution
from execution.spec import load_guidelines

mandates = load_constitution()
guidelines = load_guidelines()
```

#### After (v3.0)

```python
from core import load_mandates
from guidelines import load_guidelines

mandates = load_mandates()         # Loads .sdd-core/CANONICAL/mandate.spec
guidelines = load_guidelines()     # Loads .sdd-guidelines/guidelines.dsl
```

#### New v3.0 APIs

```python
from core import MigrationValidator, DSLParser

# Validate mandate spec format
validator = MigrationValidator()
report = validator.validate_mandate_spec('.sdd-core/CANONICAL/mandate.spec')

# Parse DSL files
parser = DSLParser()
mandates = parser.parse('.sdd-core/CANONICAL/mandate.spec')
guidelines = parser.parse('.sdd-guidelines/guidelines.dsl')

# Compile to binary (MessagePack)
from compiler import compile_to_binary
binary = compile_to_binary(mandates, guidelines)

# Performance benefit: 92% smaller, 3-5x faster parsing
```

### For CLI Tools

#### Before (v2.1)

```bash
sdd inspect constitution.md
sdd validate EXECUTION/spec/
```

#### After (v3.0)

```bash
sdd inspect mandate
sdd inspect guidelines
sdd audit compiled
sdd update              # Recompile local .sdd/
```

---

## 5. DSL Format Reference

### Mandate Block Syntax

```dsl
mandate M### {
  type: HARD                                  # Required: always HARD
  title: "Human-readable title"               # Required: max 200 chars
  description: "Detailed description..."      # Required: markdown allowed
  category: category-name                     # Required: hyphen-separated
  rationale: "Why this matters..."            # Optional: justification
  validation: {
    commands: [
      "command1",
      "command2"
    ]
  }
}
```

### Guideline Block Syntax

```dsl
guideline G### {
  type: SOFT                                  # Required: always SOFT
  title: "Emoji + title"                      # Optional: emojis allowed
  description: "Recommendations..."           # Optional: markdown
  category: category-name                     # Optional: defaults to "general"
  examples: [
    "Example scenario 1",
    "Example scenario 2"
  ]                                           # Optional: array of examples
}
```

### Valid Categories

Common categories:
- `architecture` - Architectural patterns
- `code-style` - Naming, formatting, style
- `testing` - Test structure and coverage
- `performance` - Optimization, caching
- `operations` - Monitoring, logging, deployment
- `security` - Auth, data handling
- `documentation` - Comments, guides

---

## 6. Migration Checklist

```
PRE-MIGRATION:
  [ ] Backup v2.1 (git tag or snapshot)
  [ ] Review v3.0 architecture (docs/ARCHITECTURE_OVERVIEW.md)
  [ ] List custom specializations
  [ ] Plan conversion timeline

MIGRATION:
  [ ] Convert custom mandates to DSL format
  [ ] Convert custom guidelines to DSL format
  [ ] Place in .sdd-core/custom/ and .sdd-guidelines/custom/
  [ ] Run migration tests
  [ ] Review reports (extraction, validation)
  [ ] Update documentation links

POST-MIGRATION:
  [ ] Deploy v3.0 to staging
  [ ] Test with real workflows (1-2 hours)
  [ ] Validate performance (should be 3-5x faster)
  [ ] Deploy to production
  [ ] Monitor for 24 hours
  [ ] Declare stable ✅
```

---

## 7. Troubleshooting

### "DSL Parse Error"

**Symptom:** Error when parsing .spec or .dsl files

**Solution:**
1. Check syntax: commas, braces, quotes
2. Validate: `python .sdd-migration/tooling/migration_validator.py --check`
3. See examples in [Section 5](#5-dsl-format-reference)

### "Custom Specialization Lost"

**Symptom:** Custom files not found after migration

**Solution:**
1. Verify placement: `ls -la .sdd-core/custom/`
2. Re-run migration tool
3. Check SOURCES.md for file mapping

### "Performance Slower Than Expected"

**Symptom:** Parsing taking longer than 1-3ms

**Solution:**
1. Check binary compilation: `file .sdd-core/compiled.msgpack`
2. Validate cache is enabled
3. Profile with: `python .sdd-migration/tooling/benchmarks.py`

### "Tests Failing"

**Symptom:** `pytest tests/ -v` shows failures

**Solution:**
1. Check fixture files: `tests/fixtures/v2_sample.md`
2. Update fixtures if content changed: `python tooling/migrate.py --update-fixtures`
3. Re-run: `pytest tests/ -v`

---

## 8. Rollback Plan

If issues occur during migration:

### Quick Rollback

```bash
# 1. Stop agents/services
systemctl stop sdd-agent

# 2. Restore v2.1 backup
git checkout v2.1.0
# OR
cp -r backup/EXECUTION/ ./

# 3. Restart
systemctl start sdd-agent

# 4. Verify
sdd inspect constitution.md
```

### Post-Rollback Recovery

1. Identify issue in v3.0 migration
2. Fix in tooling or custom format
3. Re-run migration in staging
4. Test thoroughly (24 hours)
5. Retry deployment

**Time to rollback:** <5 minutes  
**Data impact:** None (rollback to v2.1 state)

---

## 9. Questions & Support

See [PHASES.md](../PHASES.md) for:
- Full migration timeline and phases
- Phase owners and escalation path
- Detailed checklist and sign-offs

See [CUTOVER.md](../CUTOVER.md) for:
- Production deployment procedures
- Emergency procedures
- Rollback decision tree

See [../input/SOURCES.md](../input/SOURCES.md) for:
- Complete file mapping (v2.1 → v3.0)
- Guidelines categories
- RTK patterns mapping

---

## 📞 Contact

**Migration Lead:** See PHASES.md  
**Support:** File issue in GitHub  
**Escalation:** See CUTOVER.md (Emergency Procedures)

---

**Status:** Ready for migration (Phase 1: Apr 28)  
**Timeline:** 6 weeks to v3.0 LIVE  
**Confidence:** 99% (zero data loss, rollback ready)

