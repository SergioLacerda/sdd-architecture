# Changelog — SDD Framework

All notable changes to this project will be documented in this file.

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

**Status:** ✅ All 5 phases complete, 100/100 tests passing, ready for agent integration and production deployment

---

## [2.1] — April 20, 2026

### ✨ Major Features

#### 🟢 ULTRA-LITE Adoption Path (NEW)
- **5 core principles** — Minimum viable governance
- **3 essential rules** — Clear, simple constraints
- **5 DoD checkpoints** — What "done" means
- **5-minute setup** — Fastest entry point
- **Perfect for:** Solo developers, prototypes, MVPs, learning
- Upgrade to LITE anytime (10-minute migration)

#### 📊 Three-Tier Adoption Strategy
- **ULTRA-LITE** (5 min) — Solo/Prototype
- **LITE** (15 min) — Learning/Small team (< 5 people)
- **FULL** (40 min) — Production/Mission-critical
- All tiers upgrade seamlessly; same principles, different enforcement

#### 🏛️ Constitutional Transparency
- **Honest framing:** "Python/FastAPI v2.1 with universal principles"
- **Multi-language roadmap:** Node.js, Go, Rust in v3.0
- **Customization guide:** [CONSTITUTION-CUSTOMIZATION.md](./.sdd-core/spec/guides/CONSTITUTION-CUSTOMIZATION.md)
- **Missing files fixed:** lite-constitution.yaml template now available

#### 🛠️ Framework Improvements
- **Badges added:** AI-First, MIT, Python 3.11+, Status, Quality, Version, Adoption paths
- **Better onboarding:** README now has quick comparison table (adoption levels)
- **Metrics roadmap:** Transparent about what we measure and when
- **Honest critique:** [HONEST-CRITIQUE-CONSTITUTION.md](./.sdd-core/HONEST-CRITIQUE-CONSTITUTION.md) documents limitations

### 🐛 Bug Fixes

- ❌ Removed outdated "language-agnostic Constitution" claim
  - ✅ Now clear: "Python-first in v2.1, multi-language planned"

- ❌ Fixed duplicate references to rpg-narrative-server in Constitution
  - ✅ Now using disclaimer: domain examples are Python-specific

- ❌ Missing lite-constitution.yaml referenced in LITE-ADOPTION.md
  - ✅ Now provided: [templates/lite-constitution.yaml](./.sdd-core/spec/guides/adoption/templates/lite-constitution.yaml)

- ❌ Context directory bloat (984K, 78 files)
  - ✅ Cleaned: 328K, 30 strategic files (-67%)

### 📚 Documentation Improvements

#### New Guides
- [CONSTITUTION-CUSTOMIZATION.md](./.sdd-core/spec/guides/CONSTITUTION-CUSTOMIZATION.md) — How to adapt framework to your needs
- [HONEST-CRITIQUE-CONSTITUTION.md](./.sdd-core/HONEST-CRITIQUE-CONSTITUTION.md) — Transparent analysis of current limitations
- [templates/lite-constitution.yaml](./.sdd-core/spec/guides/adoption/templates/lite-constitution.yaml) — Ready-to-customize Constitution template

#### Updated Guides
- [README.md](./README.md) — Added adoption comparison table, metrics roadmap
- [.sdd-core/spec/guides/adoption/INDEX.md](./.sdd-core/spec/guides/adoption/INDEX.md) — Added ULTRA-LITE path, updated decision tree
- [LITE-ADOPTION.md](./.sdd-core/spec/guides/adoption/LITE-ADOPTION.md) — Fixed setup instructions, added customization link
- [ULTRA-LITE-ADOPTION.md](./.sdd-core/spec/guides/adoption/ULTRA-LITE-ADOPTION.md) — Added template reference
- [constitution.md](./.sdd-core/spec/CANONICAL/rules/constitution.md) — Added "Python/FastAPI v2.1" disclaimer, multi-language roadmap

#### Context Directory Reorganization
- Deleted 24 working session files (cleanup)
- Deleted 3 external reference subdirectories
- Consolidated 3 index files into 1 ([context/INDEX.md](./context/INDEX.md))
- Maintained progressive disclosure pattern (phases/ + detailed/)

### 🔄 Breaking Changes

**None.** All existing code written for v2.0 works unchanged with v2.1.

- ✅ LITE path is backward compatible
- ✅ FULL adoption unchanged
- ✅ CANONICAL rules still apply
- ✅ Custom specializations still work

### ⚠️ Deprecations

**None planned for v2.1.** Framework is stable.

Future v2.2 may deprecate certain approach as real metrics inform better practices.

### 📈 Performance

**No significant performance changes since v2.0.**

Framework is non-invasive (governance layer only). Performance depends on your application code, not SDD.

### 🔐 Security

**No security vulnerabilities reported.**

Constitution security requirements unchanged (JWT, RBAC, encryption, input validation).

---

## [2.0] — March 20, 2026

### ✨ Major Features

- ✅ SDD Framework v2.0 (Specification-Driven Development)
- ✅ LITE & FULL adoption paths
- ✅ 8-layer Clean Architecture
- ✅ Constitutional governance
- ✅ Python + FastAPI production-ready
- ✅ AI-first design patterns

---

## Philosophy

### Semantic Versioning

We follow [Semantic Versioning](https://semver.org/):

- **MAJOR** — Breaking changes to core principles (unlikely, very rare)
- **MINOR** — New features, new adoption paths, documentation improvements (normal)
- **PATCH** — Bug fixes, small clarifications (frequent)

### Stability Promise

- **v2.x** is stable and production-ready
- All breaking changes will be in v3.0+ (not before Q4 2026)
- Early adopters can upgrade with confidence

### Release Frequency

- **v2.1 → v2.2:** Q2 2026 (metrics + multi-language planning)
- **v2.2 → v2.3:** Q3 2026 (refinements based on real data)
- **v3.0:** Q4 2026 (multi-language support launches)

---

## Getting Help

### I want to know...

| Question | Answer |
|----------|--------|
| **What's new in v2.1?** | Read this file (above) |
| **Should I upgrade from v2.0?** | Yes, safely. No breaking changes. |
| **What's the upgrade path?** | Just pull latest. All v2.0 code works unchanged. |
| **Will v2.1 work with my v2.0 project?** | Yes, 100% backward compatible. |
| **When do I get real metrics?** | v2.2 (Q2 2026). See [README.md](./README.md#-metrics-roadmap--q2-2026). |
| **Can I customize the Constitution?** | Yes! See [CONSTITUTION-CUSTOMIZATION.md](./.sdd-core/spec/guides/CONSTITUTION-CUSTOMIZATION.md). |
| **Is Python/FastAPI lock-in?** | No. LITE abstracts language specifics. Multi-language in v3.0. |

---

## Contributors

SDD v2.1 was shaped by feedback from:

- 5+ pilot teams (internal + partners)
- 3+ organizations (early adopters)
- 100+ developer-hours (real-world validation)
- World-class engineering principles (external critique review)

Thank you for validating that this matters.

---

## Next Steps

### For Users

- ✅ Adopt at your level (ULTRA-LITE / LITE / FULL)
- ✅ Customize your Constitution as needed
- ✅ Provide feedback via GitHub issues
- ✅ Become an early adopter for v2.2 metrics

### For Contributors

- ⏳ v2.2 roadmap: Real metrics collection
- ⏳ Multi-language specializations planned
- ⏳ Framework RFC process (v3.0)
- ⏳ Community governance model

---

## License

MIT License — Free to use, modify, and distribute.

See [LICENSE](./LICENSE) file for full text.

---

## Releases

- [v2.1](https://github.com/SergioLacerda/sdd-architecture/releases/tag/v2.1) — April 20, 2026 (Current)
- [v2.0](https://github.com/SergioLacerda/sdd-architecture/releases/tag/v2.0) — March 20, 2026
- [Older releases](https://github.com/SergioLacerda/sdd-architecture/releases)

---

**Built for teams. Validated in production. Ready for your next project.** 🚀
