# Changelog — SDD Framework v3.0

**Complete version history and release notes**

---

## [3.0] — April 22, 2026 (FINAL)

### ✨ Major Features

#### 🏗️ Governance Pipeline Architecture (COMPLETE)

**PHASE 1: Pipeline Builder** ✅
- Consolidated governance source files into 2 JSON structures
- **Core (immutable):** 4 governance items with `customizable=false`
- **Client (customizable):** 151 governance items with `customizable=true`
- SHA-256 fingerprinting with canonical JSON serialization
- Parsing support for: mandate.spec, guidelines.dsl, decisions/, rules/, guardrails/
- **Result:** governance-core.json + governance-client.json
- **Tests:** 13/13 passing

**PHASE 2: Governance Compiler** ✅
- Binary serialization of JSON structures to msgpack format
- Fingerprint preservation (not recalculation) for integrity validation
- Metadata generation with statistics (item counts, type distribution, criticality breakdown)
- Salt-based strategy: Core fingerprint embedded in client metadata
- **Outputs:** 2 msgpack files + 2 metadata JSONs
- **Result:** 4 compiled artifacts ready for runtime
- **Tests:** 15/15 passing

**PHASE 3: End-to-End Integration** ✅
- Orchestrated PHASE 1 + PHASE 2 execution with validation
- 8-point validation (file integrity, fingerprint preservation, salt strategy, separation, counts)
- Idempotence verification (same input → identical output)
- Roundtrip serialization testing (JSON ↔ msgpack)
- Data completeness validation (all 155 items preserved)
- **Tests:** 15/15 passing

**PHASE 4: Deployment** ✅
- Deployed compiled artifacts to `.sdd-wizard/compiled/`
- Backup management for existing files
- Deployment verification and checklist
- Manifest generation with deployment metadata
- **Outputs:** Copied to .sdd-wizard/compiled/ with backups
- **Tests:** 16/16 passing
- **Status:** ✅ Ready for wizard and agent runtime integration

#### 🔐 Security & Integrity

**Fingerprinting Strategy**
- Core fingerprint: `35efc54d3e353daaf633fad531562f1da97ec17814193b7ac44b2e9ef12daddd`
- Client fingerprint: `2247922049fc14d93c174fb22a584e5640f3d456980ef57107a4083187591e38`
- Salt strategy: Core fingerprint embedded in client metadata enables tampering detection
- Immutable core prevents unauthorized governance changes
- Customizable client allows organizational adaptation

**PHASE 5: Wizard Integration** ✅
- **Runtime Loader:** Load compiled msgpack artifacts from .sdd-wizard/
  * Deserialize and validate governance data
  * Provide governance data API for agents and wizards
  * Fingerprint validation and salt strategy verification
  * Item filtering by type, criticality, and customizability
  
- **Wizard Integrator:** Connect governance with setup wizard workflow
  * Integration hooks for custom wizard behavior
  * Governance-aware configuration generation
  * Customization template creation and validation
  * Agent-aware constitution configuration
  
- **Customization Templates:** Generate templates for governance customization
  * Basic, full, category-based, criticality-based, adoption-based templates
  * Support multiple customization workflows and adoption levels
  * 17 templates generated automatically
  * Template validation against immutable core
  
- **Wizard Orchestrator:** Coordinate complete wizard initialization
  * Load governance → Integrate with wizard → Generate templates
  * 7-step workflow validation
  * Deployment summary for wizard readiness
  * Ready for agent runtime integration

- **Result:** Governance data ready for wizard and agent use
- **Tests:** 41/41 passing (11 orchestrator + 30 integration tests)

#### 📊 Quality Metrics
- **Total Tests:** 100 passing (100% pass rate)
  - PHASE 1: 13 tests
  - PHASE 2: 15 tests
  - PHASE 3: 15 tests
  - PHASE 4: 16 tests
  - PHASE 5: 41 tests
- **Code Coverage:** All critical paths tested
- **Validation Points:** 7-point workflow validation + idempotence checks

#### 🎯 Architecture Pattern: 2-File Governance Model

```
Source Files (.sdd-core/) 
  ↓ [PHASE 1: Pipeline]
governance-core.json (4 items, immutable)
governance-client.json (151 items, customizable)
  ↓ [PHASE 2: Compiler]
msgpack binaries + metadata
  ↓ [PHASE 3: Integration]
Full pipeline validation (8 checks)
  ↓ [PHASE 4: Deployment]
.sdd-wizard/compiled/ (artifacts deployed)
  ↓ [PHASE 5: Wizard Integration]
Runtime loaders, integrators, templates
Ready for wizard and agent use
```

### 🐛 Bug Fixes & Critical Improvements

- ✅ **Fingerprint Calculation Order:** Fingerprints now calculated BEFORE embedding in structure
  - Prevents circular reference issues
  - Ensures idempotent hashing
  - Critical for salt strategy validation

- ✅ **Import Path Resolution:** Fixed GovernanceOrchestrator module imports
  - sys.path.insert(0, ...) for cross-directory imports
  - All 4 phases can coordinate seamlessly

### 📦 Artifacts Generated

**Compiled Directory: `.sdd-compiled/`**
- `governance-core.compiled.msgpack` (2.3 KB) — Core governance (4 items)
- `governance-client-template.compiled.msgpack` (34 KB) — Client governance (151 items)
- `metadata-core.json` — Core metadata with readonly flag
- `metadata-client-template.json` — Client metadata with customizable flag

**Deployed Directory: `.sdd-wizard/compiled/`**
- All 4 artifacts copied from .sdd-compiled/
- Backup directory for previous versions
- DEPLOYMENT_MANIFEST.json with versioning info

### 🔗 Next Phases

**PHASE 6: Agent Integration** (Planned)
- Integrate GovernanceRuntimeLoader into agent initialization
- Agent-aware governance enforcement
- Dynamic governance adaptation based on agent capabilities
- Governance telemetry and compliance tracking

**PHASE 7: Production Deployment** (Planned)
- Production deployment checklist and validation
- Performance optimization for runtime loading
- Governance versioning and upgrade strategy
- Multi-environment configuration support

### 📋 Reference

**Tags:**
- v3.0-pipeline-compiler-complete (PHASE 1-4): 0632a97
- v3.0-wizard-integration-complete (PHASE 1-5): bae26d4

**Status:** ✅ All 6 phases complete, 124/124 tests passing, production-ready

### 🎯 PHASE 6: CLI & Documentation Finalization

#### A. CLI Implementation (Typer Framework)
- **Framework:** Typer 0.12.1 (type-first Python CLI)
- **Commands:**
  * `sdd governance load` — Load and display governance configuration
  * `sdd governance validate` — Validate integrity and fingerprints
  * `sdd governance generate` — Generate agent seed templates (Cursor, Copilot, Generic)
  * `sdd version` — Show framework version
- **Output:** PyInstaller binary (20M standalone executable, no Python required)
- **Tests:** 24/24 passing (100% coverage)
- **Dependencies:** typer==0.12.1, click==8.1.7, rich==13.7.0, msgpack==1.0.8, PyYAML==6.0.1
- **Distribution:** Cross-platform ready (Linux, macOS, Windows)

#### B. Documentation Consolidation
- **EXECUTION folder → .sdd-core/:** 106 files migrated
  * Source code (pipeline, compiler, deployment)
  * Specification layer (CANONICAL, decisions, rules)
  * Guide layer (adoption, operational, reference, emergency)
  * Integration components
  * Test suite (execution_tests/)
  * Tooling (generators, optimizers)

- **INTEGRATION folder → .sdd-integration/:** 50 files migrated
  * Integration workflow (STEP_1 through STEP_5)
  * Checklist and guides
  * Templates for project setup
  * Concepts and comparison documents

- **Namespace pattern:** All framework folders now follow `.sdd-*` pattern:
  * `.sdd-core/` — Governance + framework source
  * `.sdd-integration/` — Project integration workflow
  * `.sdd-migration/` — Historical migration documentation
  * `.sdd-wizard/` — Runtime compiled artifacts
  * `.sdd-compiler/` — Compiler source code
  * `.sdd-compiled/` — Compiled outputs

- **Reference updates:** 7+ root files updated with new paths

#### C. Root Documentation Cleanup
- **Removed:** All v2.1 references and documentation
  * RELEASE_v2.1.md archived
  * v2.1 content removed from CHANGELOG.md
  * v2.0 historical content consolidated
  
- **Updated:** Core documentation to v3.0 focus
  * README.md: Removed adoption profiles (ULTRA-LITE, LITE, FULL)
  * README.md: Added comprehensive CLI usage section
  * INDEX.md: Simplified navigation
  * .ai-index.md: Updated version and terminology
  * CHANGELOG.md: Kept only v3.0 current (v2.x in archive)

- **New:** CLI instructions in README
  * Installation options (binary vs source)
  * Available commands with examples
  * Troubleshooting guide

#### D. Documentation Simplification
- **Removed:** Adoption path complexity
  * No more ULTRA-LITE/LITE/FULL decision trees in README
  * Removed adoption/INDEX.md references from main flow
  * Simplified role-based navigation

- **Added:** DevOps/Operator role guidance
  * `sdd governance load` command in quick start
  * CLI troubleshooting section
  * Operator entry point in role-based navigation

### 📊 Complete Testing Summary
- **Total Tests:** 124/124 passing (100% coverage)
  - PHASE 1 (Pipeline): 13 tests ✅
  - PHASE 2 (Compiler): 15 tests ✅
  - PHASE 3 (Orchestration): 15 tests ✅
  - PHASE 4 (Deployment): 16 tests ✅
  - PHASE 5 (Wizard): 41 tests ✅
  - PHASE 6 (CLI): 24 tests ✅

### 🎯 Git Commits (Session Summary)
1. `b54d796` — Consolidate EXECUTION → .sdd-core (106 files)
2. `10cc26b` — Consolidate INTEGRATION → .sdd-integration (50 files)
3. `3706ede` — Remove v2.1 documentation, update to v3.0 focus
4. `8eb0cc4` — Simplify README.md (remove adoption profiles, add CLI)
5. Final commit → Update CHANGELOG with all session changes

### 📋 Final Metrics
- **Total Files Consolidated:** 156 files (106 + 50)
- **Root Documentation Updated:** 7+ files
- **CLI Tests:** 24/24 passing
- **Binary Size:** 20M (no external dependencies)
- **Namespace Consolidation:** 100% complete
- **Documentation Cleanup:** 100% complete

### 🎯 PHASE 7: Wizard Architecture Alignment & Profile Removal

#### A. Profile Model Elimination
- **Removed:** `--profile` CLI parameter (was LITE/FULL/ULTRA-LITE)
  * Analysis: Profiles don't exist in v3.0 architecture (by design)
  * CORE+CLIENT separation with SALT fingerprinting eliminates need for predefined buckets
  * Users autonomously choose which guidelines to implement (no fixed profiles)
  
- **Removed:** Profile-specific code
  * Deleted `_customize_file_for_profile()` function from Phase 5
  * Removed profile filtering logic (Phase 4)
  * Removed profile template directories
  * Removed profile parameter from all phase function signatures
  
- **Result:** Guidelines filtered by language only (Python/Java/JavaScript)
  * Phase 4: Language-based filtering (not profile-based)
  * All 151 guidelines available for customization selection
  * No priority metadata (profiles eliminated the need for it)

#### B. Version Field Removal
- **Removed:** `version: '3.0'` metadata field
  * No retrocompat strategy needed (v3.0 is production-ready)
  * Single-version deployment model eliminates version noise
  * Metadata now contains only: `generated_at`
  
- **Updated:** Phase 7 validation checks
  * Removed version field requirement from output validation
  * Simplified metadata validation (only required field: `generated_at`)

#### C. Architecture Alignment Documentation
- **Created:** [.sdd-wizard/ARCHITECTURE_ALIGNMENT.md](./.sdd-wizard/ARCHITECTURE_ALIGNMENT.md)
  * Explains why profiles don't exist in v3.0
  * Details CORE+CLIENT governance model
  * Documents SALT fingerprinting strategy
  * Design rationale for profile removal
  * FAQ addressing common questions
  * Migration notes from v2.1 to v3.0

- **Updated:** Wizard documentation
  * [.sdd-wizard/WORKFLOW_FLOW.md](./.sdd-wizard/WORKFLOW_FLOW.md) — Removed profile references
  * [.sdd-wizard/ORCHESTRATION.md](./.sdd-wizard/ORCHESTRATION.md) — Updated diagrams
  * [.sdd-wizard/IMPLEMENTATION_STATUS_v3.0.md](./.sdd-wizard/IMPLEMENTATION_STATUS_v3.0.md) — Updated status

#### D. Validation & Testing
- **Wizard Testing:** Full 7-phase pipeline validation
  * ✅ Phase 1: VALIDATE_SOURCE (2 mandates, 150 guidelines)
  * ✅ Phase 2: LOAD_COMPILED (artifact deserialization)
  * ✅ Phase 3: FILTER_MANDATES (user selection)
  * ✅ Phase 4: FILTER_GUIDELINES (language filtering only)
  * ✅ Phase 5: APPLY_TEMPLATE (scaffold customization)
  * ✅ Phase 6: GENERATE_PROJECT (output generation)
  * ✅ Phase 7: VALIDATE_OUTPUT (integrity checks, no version field check)
  
- **Result:** 7/7 phases passing, wizard fully operational
- **Tests:** 100% successful execution with cleanup complete

### 🚀 Production Ready Status
✅ All 7 PHASES complete  
✅ 124/124 tests passing  
✅ CLI operational  
✅ Documentation consolidated  
✅ Wizard architecture aligned with v3.0  
✅ Profiles and version field removed  
✅ Root cleanup complete  
✅ Namespace patterns established  
✅ DevOps tooling available  
✅ Ready for deployment

### 🔗 Entry Points (Updated)
- **Main:** [README.md](README.md)
- **Developers:** [.sdd-core/_START_HERE.md](./.sdd-core/_START_HERE.md)
- **Integration:** [.sdd-integration/README.md](./.sdd-integration/README.md)
- **AI Agents:** [.ai-index.md](./.ai-index.md)
- **CLI:** `sdd --help` or see README CLI Usage section
- **Architecture:** [.sdd-core/NAVIGATION.md](./.sdd-core/NAVIGATION.md)

### 📚 Historical References
- **v2.x Archive:** See [CHANGELOG_ARCHIVE.md](CHANGELOG_ARCHIVE.md) for v2.1 and v2.0 release notes
- **Migration:** [.sdd-migration/](./sdd-migration/) contains v3.0 migration documentation
