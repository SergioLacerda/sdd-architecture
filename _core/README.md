# _core/ - Implementation & Code

This directory contains all implementation code, tests, configuration, and generated artifacts for the SDD framework.

## Structure

```
_core/
├── .sdd-core/              # Governance compiler and source items
│   ├── source/             # 155 markdown governance items
│   ├── compile_governance.py   # Main compiler
│   ├── extract_governance_items.py
│   ├── regenerate_from_catalog.py
│   └── ...
│
├── .sdd-wizard/            # Wizard orchestration engine
│   ├── src/                # Main wizard code
│   ├── orchestration/      # 7-phase pipeline
│   └── tests/              # Wizard tests
│
├── .sdd-compiler/          # Compiler utilities
├── .sdd-migration/         # Migration scripts
├── .sdd-integration/       # Integration tools
├── .sdd-runtime/           # Runtime compiled governance
│
├── .sdd-cli/               # CLI interface
├── tests/                  # All test files (82+ tests)
│
├── Configuration
│   ├── Makefile.tests      # Test runner
│   ├── requirements-cli.txt # Dependencies
│   ├── .spec.config        # Config file
│   └── .pytest_cache/      # Pytest cache
│
├── sdd-generated/          # Generated project artifacts
├── governance_items_catalog.json
├── user_selections_sample.json
│
├── Artifacts
│   ├── build/              # Build artifacts
│   ├── dist/               # Distribution
│   └── .pytest_cache/
│
└── Scripts
    ├── run-all-tests.py    # Test runner
    └── run-all-tests.sh    # Test runner (shell)
```

## Quick Start (Developer)

```bash
# Navigate to implementation
cd _core

# Run tests
python run-all-tests.py

# Run specific tests
cd tests && pytest test_phase_3_integration.py -v

# Compile governance
cd .sdd-core && python compile_governance.py

# Run wizard
python .sdd-wizard/src/wizard.py --help
```

## Key Modules

| Module | Purpose | Location |
|--------|---------|----------|
| **Compiler** | Extract & compile governance items | `.sdd-core/compile_governance.py` |
| **Wizard** | 7-phase orchestration pipeline | `.sdd-wizard/src/wizard.py` |
| **CLI** | Command-line interface | `.sdd-cli/` |
| **Tests** | 82+ integration tests | `tests/` |
| **Runtime** | Compiled governance artifacts | `.sdd-runtime/` |

## Import Paths

Old paths (with symlinks) still work:
```python
# These work (via symlinks)
from .sdd-core import compile_governance
from .sdd-wizard.src import wizard
```

New paths (recommended):
```python
# These also work
from _core.sdd-core import compile_governance
from _core.sdd-wizard.src import wizard
```

## Testing

```bash
# Run all tests
python run-all-tests.py

# Run with details
python run-all-tests.py --verbose

# Run specific layer
python run-all-tests.py --layer "Wizard"

# Quick check (stop on first failure)
python run-all-tests.py --fail-fast
```

## Configuration

- `.spec.config` - Specification configuration
- `requirements-cli.txt` - Python dependencies
- `Makefile.tests` - Test configuration

## Generated Artifacts

- `governance_items_catalog.json` - 155 extracted items
- `user_selections_sample.json` - Example user selections
- `sdd-generated/` - Generated projects from wizard

## Architecture

### 5-Phase Pipeline (Compiler)
1. **Extract** - Parse 155 markdown items
2. **Separate** - Split into CORE (34) + CLIENT (121)
3. **Compile** - Generate JSON governance files
4. **Fingerprint** - Add SHA256 + SALT validation
5. **Deploy** - Output to `.sdd-runtime/` and `.sdd-compiled/`

### 7-Phase Wizard Pipeline
1. Validate SOURCE
2. Load COMPILED (JSON governance)
3. Filter MANDATES
4. Filter GUIDELINES
5. Apply TEMPLATE
6. Generate PROJECT
7. Validate OUTPUT

## Files Not to Edit

- `.sdd-runtime/compiled/` - Automated deployment
- `build/`, `dist/` - Build artifacts
- `.pytest_cache/` - Pytest cache

## See Also

- [Root README.md](../README.md) - Main documentation
- [_spec/ README.md](_spec/README.md) - Specification documentation
- [Phase 3 Integration](../docs/PHASE_3_WIZARD_INTEGRATION.md) - Wizard integration details
