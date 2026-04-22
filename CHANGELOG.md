# Changelog — SDD Framework v3.0

**Current version documentation**

For historical release notes (v2.x), see [CHANGELOG_ARCHIVE.md](CHANGELOG_ARCHIVE.md).

---

## [3.0] — April 22, 2026

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

**Status:** ✅ All 6 phases complete, 124/124 tests passing, fully operational

### 🎯 PHASE 6 Additions

**CLI Implementation (Typer Framework)**
- Modern Python CLI using Typer 0.12.1 (type-first)
- Commands: governance load, governance validate, governance generate, sdd version
- Rich formatted output (colors, tables, panels)
- PyInstaller binary: 20M standalone executable (no Python installation required)
- Tests: 24/24 passing (100% coverage)
- Ready for cross-platform distribution

**Documentation Consolidation**
- EXECUTION folder → .sdd-core/ (106 files, complete source + specs)
- INTEGRATION folder → .sdd-integration/ (50 files, integration templates)
- Root reference updates in 5+ files
- Namespace pattern: .sdd-* for all framework folders
- Fully organized for production deployment

### 📋 Reference

**Tags:**
- v3.0-pipeline-compiler-complete (PHASE 1-4): 0632a97
- v3.0-wizard-integration-complete (PHASE 1-5): bae26d4
- v3.0-cli-complete (PHASE 6): [wip/centralize-sdd-core]

### 📚 Resources

- **Release notes history:** [CHANGELOG_ARCHIVE.md](CHANGELOG_ARCHIVE.md)
- **Getting started:** [.sdd-core/_START_HERE.md](./.sdd-core/_START_HERE.md)
- **Integration:** [.sdd-integration/README.md](./.sdd-integration/README.md)
- **Documentation hub:** [INDEX.md](INDEX.md)
