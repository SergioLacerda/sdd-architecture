# Changelog Archive — SDD Framework v2.x

**Historical release notes for versions prior to v3.0 (April 22, 2026)**

For current information, see [CHANGELOG.md](CHANGELOG.md) for v3.0 details.

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

## Philosophy (v2.x)

### Semantic Versioning

We follow [Semantic Versioning](https://semver.org/):

- **MAJOR** — Breaking changes to core principles (unlikely, very rare)
- **MINOR** — New features, new adoption paths, documentation improvements (normal)
- **PATCH** — Bug fixes, small clarifications (frequent)

### Stability Promise

- **v2.x** is stable and production-ready
- All breaking changes were planned in v3.0 (not before Q4 2026)
- Early adopters upgraded with confidence

### Release Frequency (v2.x Planning)

- **v2.1 → v2.2:** Q2 2026 (metrics + multi-language planning)
- **v2.2 → v2.3:** Q3 2026 (refinements based on real data)
- **v3.0:** Q4 2026 (multi-language support launches)

---

## Contributors

SDD v2.1 was shaped by feedback from:

- 5+ pilot teams (internal + partners)
- 3+ organizations (early adopters)
- 100+ developer-hours (real-world validation)
- World-class engineering principles (external critique review)

---

## Releases

- [v2.1](https://github.com/SergioLacerda/sdd-architecture/releases/tag/v2.1) — April 20, 2026
- [v2.0](https://github.com/SergioLacerda/sdd-architecture/releases/tag/v2.0) — March 20, 2026

---

**See [CHANGELOG.md](CHANGELOG.md) for current v3.0 release notes.**
