# docs/ - Implementation Context & Project Documentation

This directory contains all project implementation context, workflow documentation, and execution history for the SDD framework. This is distinct from `/spec` which contains the formal specifications and architecture definitions.

## Structure

```
docs/
├── INDEX.md                              # Master index of all documentation
├── CHANGELOG.md                          # Version history & releases
├── TEST_RUNNER_GUIDE.md                  # Guide for running tests
│
├── Workflow Documentation               # Project execution history
│   ├── PHASE_2_OUTPUT_ANALYSIS.md       # Analysis of Phase 2 outputs
│   ├── PHASE_2_VALIDATION_CHECKLIST.md  # Validation checklist for Phase 2
│   ├── PHASE_3_WIZARD_INTEGRATION.md    # Wizard integration work
│   ├── PHASE_4_AUDIT_REPORT.md          # Phase 4 audit results
│   ├── PHASE_4_CODE_DOCS_SEPARATION.md  # Code/docs separation work
│   ├── PHASE_4_COMPLETION_SUMMARY.md    # Phase 4 summary
│   ├── V3_LAUNCH_READINESS.md           # V3 launch status
│   └── V3.1_BETA1_IMPLEMENTATION_PLAN.md # V3.1 Beta implementation
│
├── Wizard Documentation                 # Wizard implementation guides
│   ├── WIZARD_DOCUMENTATION_INDEX.md    # Wizard docs index
│   ├── WIZARD_QUICK_START.md            # Quick start guide
│   ├── WIZARD_INTERACTIVE_GUIDE.md      # Interactive walkthrough
│   ├── WIZARD_EXAMPLE_SESSION.md        # Example session transcript
│   └── WIZARD_MAPPING.md                # Wizard functionality mapping
│
├── Checkpoints & Status                 # Project checkpoints
│   └── CHECKPOINT_DOCUMENTATION_RESTRUCTURING.md  # Docs restructuring checkpoint
```

## Key Documents

| Document | Purpose | Audience |
|----------|---------|----------|
| [INDEX.md](INDEX.md) | Master documentation index | Everyone |
| [CHANGELOG.md](CHANGELOG.md) | Version history & releases | Everyone |
| [PHASE_3_WIZARD_INTEGRATION.md](PHASE_3_WIZARD_INTEGRATION.md) | Wizard integration work | Developers |
| [WIZARD_QUICK_START.md](WIZARD_QUICK_START.md) | Quick start guide | New users |
| [TEST_RUNNER_GUIDE.md](TEST_RUNNER_GUIDE.md) | Testing guide | Developers |

## Quick Start

```bash
# View master documentation index
cat docs/INDEX.md

# View project history
cat docs/CHANGELOG.md

# View wizard documentation
cat docs/WIZARD_QUICK_START.md

# View testing guide
cat docs/TEST_RUNNER_GUIDE.md
```

## Sections

### 📊 Workflow Documentation
Documentation of each project phase execution, outputs analysis, and validation results.

### 🧙 Wizard Documentation
Complete documentation of the SDD Wizard v3 interactive setup tool, including quick start guides, example sessions, and functionality mapping.

### ✅ Checkpoints & Status
Project status checkpoints documenting major work completion and validation.

### 📚 Supporting Docs
- CHANGELOG.md - Version history and release notes
- TEST_RUNNER_GUIDE.md - Guide for running the test suite
- INDEX.md - Master index of all documentation

## Relationship to `/spec`

- **`/docs`** - Implementation context, project history, workflow documentation
- **`/_spec`** - Formal specifications, architecture decisions, guides, governance rules

Files in `/docs` document *how we got here* and *what we're working on*.
Files in `/_spec` define *what we should do* and *how things should work*.
