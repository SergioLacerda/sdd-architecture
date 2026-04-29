# 🏛️ SDD Framework v3.0

**Specification-Driven Development with Autonomous Governance**

[![Version](https://img.shields.io/badge/v3.0-✅%20Production-brightgreen?style=flat-square&logo=github)](.) [![Tests](https://img.shields.io/badge/Tests-124%2F124%20✅-brightgreen?style=flat-square&logo=pytest)](docs/TEST_RUNNER_GUIDE.md) [![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python)](.) [![GitHub Actions](https://img.shields.io/badge/CI%2FCD-10%20Workflows-blue?style=flat-square&logo=github-actions)](https://github.com/SergioLacerda/sdd-architecture/actions) [![Code Coverage](https://img.shields.io/badge/Coverage-100%25-brightgreen?style=flat-square&logo=codecov)](.) [![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](.) [![Governance](https://img.shields.io/badge/Governance-16%20Rules-orange?style=flat-square)](.) [![Status](https://img.shields.io/badge/Status-Production%20Ready-success?style=flat-square&logo=checkmarx)](.) [![Code Quality](https://img.shields.io/badge/Code%20Quality-Enterprise-blue?style=flat-square)](.) [![Architecture](https://img.shields.io/badge/Architecture-4%2BLayer%20Validation-purple?style=flat-square)](.)

---

## 🎯 Quick Start — Choose Your Path

| 👨‍💻 Developer | 🤖 AI Agent | 🔬 Technical |
|---|---|---|
| **3 Steps:** | **AI-Ready:** | **7-Phase Workflow:** |
| 1. `make setup` | Wizard integration | Phase 1: Validate |
| 2. `./wizard.sh` | Phase execution | Phase 2: Load |
| 3. `cat .sdd/` | Seedling configs | Phase 3-4: Filter |
| ⏱️ **5 min** | ⏱️ **10 min** | Phase 5-7: Generate |
| [→ Developer](README.md) | [→ AI Guide](readme-ia.md) | ⏱️ **20 min** |
| | | [→ Technical](readme-detailed.md) |

---

## 📂 Structure (PHASE 4: Code/Docs Separation)

```
repository/
├── packages/              # 💻 Implementation & Code (82+ tests)
│   ├── .sdd-core/      # Governance compiler
│   ├── .sdd-wizard/    # Wizard orchestration
│   ├── cli/        # CLI interface
│   ├── tests/          # All tests
│   └── run-all-tests.py
│
├── _spec/              # 📚 Specification & Documentation
│   ├── docs/           # Main documentation
│   ├── .ai/            # AI agent config
│   ├── .ai-index.md    # AI entry point
│   ├── PHASE_*.md      # Phase documentation
│   ├── guides/         # How-to guides
│   └── CHANGELOG.md    # Version history
│
├── README.md (this file)
└── Backward compatibility symlinks (.sdd-core → packages/.sdd-core, etc.)
```

**Note:** Old import paths still work via symlinks. See [packages/README.md](packages/README.md) and [_spec/README.md](_spec/README.md) for details.

---

## 📖 Documentation Paths

### 👨‍💻 For Developers
- [README.md](README.md) — Overview (3 min)
- [packages/README.md](packages/README.md) — Code structure (5 min)  
- [docs/TEST_RUNNER_GUIDE.md](docs/TEST_RUNNER_GUIDE.md) — Testing (10 min)

### 🤖 For AI Agents
- [readme-ia.md](readme-ia.md) — Wizard integration guide
- [.ai-index.md](.ai-index.md) — AI entry point

### 🔬 For Technical Details
- [readme-detailed.md](readme-detailed.md) — 7-phase workflow
- [packages/.sdd-wizard/WORKFLOW_FLOW.md](packages/.sdd-wizard/WORKFLOW_FLOW.md) — Complete orchestration

---

## 🔧 First Time Setup (Required)

**Before using the CLI or wizard**, install dependencies (one-time setup):

```bash
# Automatic setup (recommended)
./setup.sh

# OR manually:
pip3 install -r packages/requirements-cli.txt
```

**What gets installed:**
- `typer` - CLI framework
- `click` - Command-line interface library
- `rich` - Terminal formatting
- `msgpack` - Data serialization
- `PyYAML` - Configuration files

---

## 🚀 Installation & Setup

### Step 1: Clone & Install

```bash
git clone github.com:SergioLacerda/sdd-architecture.git
cd sdd-architecture && make setup

# Run setup script (one-time)
./setup.sh
```

### Step 2: Create Your First Project

```bash
# Interactive mode (RECOMMENDED)
./wizard.sh

# Non-interactive
./wizard.sh --language python --mandates M001 --output ~/my-project/
```

### Step 3: Explore Generated Project

```bash
cd ~/my-project/
cat .sdd/CANONICAL/mandate.spec
make test
```

---

## 📚 Documentation (Choose Your Path)

**Quick navigation:**
- 🔤 **Code & Implementation:** See [packages/README.md](packages/README.md)
- 📖 **Specs & Documentation:** See [_spec/README.md](_spec/README.md)
- 📋 **Full Index:** See [docs/INDEX.md](docs/INDEX.md)
- 🧙 **Wizard Guide:** See [WIZARD_DOCUMENTATION_INDEX.md](WIZARD_DOCUMENTATION_INDEX.md)

### 🧙 Wizard Documentation (New!)
Start here if you want to create a new project with the SDD Wizard:

| Document | Duration | Best For |
|----------|----------|----------|
| [docs/WIZARD_QUICK_START.md](docs/WIZARD_QUICK_START.md) | 2 min | Get started immediately |
| [docs/WIZARD_MAPPING.md](docs/WIZARD_MAPPING.md) | 10 min | Understand the complete flow |
| [docs/WIZARD_INTERACTIVE_GUIDE.md](docs/WIZARD_INTERACTIVE_GUIDE.md) | 15 min | Learn every detail |
| [docs/WIZARD_EXAMPLE_SESSION.md](docs/WIZARD_EXAMPLE_SESSION.md) | 10 min | See a real example |
| [docs/WIZARD_DOCUMENTATION_INDEX.md](docs/WIZARD_DOCUMENTATION_INDEX.md) | Navigation | Find what you need |

---

## 🎯 Your Scenarios

### Testing

**Run all tests from packages (82+ tests):**
```bash
make test          # Executa todos os testes das 7 camadas
```

**Full Quality Audit:**
```bash
make check         # Linting + Type Check + Governance + Tests
```

**See:** [docs/TEST_RUNNER_GUIDE.md](docs/TEST_RUNNER_GUIDE.md) for complete guide

### CLI Commands

**Navigate to packages first, then use CLI:**
```bash
cd packages

# Load governance
python3 -m cli governance load

# Validate integrity
python3 -m cli governance validate

# Generate templates
python3 -m cli governance generate
```

### Development Workflow

**You have a task → Follow 7 phases:**

```
PHASE 0: Setup (.ai infrastructure) — 20-30 min, one time
PHASE 1: Lock to rules — 15 min
PHASE 2: Check execution state — 5 min
PHASE 3: Choose PATH (bug/feature/complex/multi) — 5 min
PHASE 4: Load context — 10-20 min
PHASE 5: Implement (TDD) — 1-8 hours
PHASE 6: Validate (tests + done criteria) — 15 min
PHASE 7: Checkpoint (document + PR) — 10 min
```

**Details:** [.sdd-core/spec/guides/onboarding/AGENT_HARNESS.md](.sdd-core/spec/guides/onboarding/AGENT_HARNESS.md)

---

## 🏗️ What's Inside

### Core Framework
- ✅ **4 immutable mandates** (CORE governance)
- ✅ **151 customizable guidelines** (CLIENT governance)
- ✅ **SHA-256 fingerprinting** (integrity validation)
- ✅ **7-phase wizard** (fully operational)

### Status
- ✅ **124/124 tests passing** (100% coverage)
- ✅ **CLI ready** (Typer framework)
- ✅ **Documentation complete** (150+ files)
- ✅ **Production-ready**

### Entry Points
- [.sdd-core/](.sdd-core/) — Development workflow
- [.sdd-integration/](.sdd-integration/) — Add projects
- [.sdd-wizard/](.sdd-wizard/) — Runtime artifacts
- [.sdd-compiler/](.sdd-compiler/) — Compiler source

---

## � CI/CD Automation (10 Workflows)

The SDD Architecture uses **GitHub Actions** for continuous integration, testing, and deployment.

### Framework Workflows (SDD Development)

| Workflow | Trigger | Purpose | Status |
|----------|---------|---------|--------|
| **🏥 Health Check** | Push, PR, Daily | Validates 10 health checks (Git, structure, governance, Python, dependencies) | ✅ Active |
| **🧪 Tests** | Push, PR | Runs 124 test suite across Python 3.8-3.12 | ✅ Active |
| **🔍 Lint** | Push, PR | Code quality checks (pylint, type hints, formatting) | ✅ Active |
| **📊 Compliance Report** | Daily | Governance compliance dashboard + enforcement checks | ✅ Active |
| **⚖️ Governance Enforce** | Push, PR | Validates mandatory policies before merge | ✅ Active |
| **📚 Docs** | Push to main | Auto-generates documentation and API references | ✅ Active |
| **🔗 Integration** | Push, PR | Tests wizard, compiler, and CLI integration | ✅ Active |
| **📦 Dependencies** | Weekly | Checks dependency security and updates | ✅ Active |
| **🏷️ Release** | Tag push | Builds releases, publishes to PyPI, creates changelogs | ✅ Active |
| **✅ Validate Workflows** | Push, PR | Validates all workflow YAML syntax and structure | ✅ Active |

### How Workflows Work Together

```
Developer Push
    ↓
├─→ [Validate Workflows] (syntax check)
│   ↓
├─→ [Health Check] (10-point validation)
│   ├─→ Git status, core structure, docs, seedlings
│   ├─→ Python version, modules, governance files
│   └─→ Wizard state
│   ↓
├─→ [Tests] (124 tests across Python 3.8-3.12)
│   ├─→ Unit tests (governance, compiler, wizard)
│   ├─→ Integration tests (e2e workflows)
│   └─→ Coverage report (100% target)
│   ↓
├─→ [Lint] (code quality)
│   ├─→ pylint, mypy, black
│   ├─→ Type hints validation
│   └─→ Security checks
│   ↓
├─→ [Governance Enforce] (mandatory policies)
│   ├─→ Check 4 immutable mandates
│   ├─→ Verify 151 guidelines
│   └─→ Compliance score
│   ↓
├─→ [Compliance Report] (dashboard)
│   └─→ Generates compliance metrics
│   ↓
├─→ [Integration] (wizard + compiler test)
│   ├─→ Phase 1-7 validation
│   ├─→ Template generation
│   └─→ Project creation
│   ↓
└─→ [Dependencies] (weekly security check)
    └─→ Updates and vulnerability scan
```

### Pushing to Main

**Before merge is allowed:**
- ✅ All 10 workflows must pass
- ✅ No security vulnerabilities
- ✅ 100% test coverage maintained
- ✅ Governance compliance verified

**Post-merge to main:**
- 📚 Documentation auto-updated
- 📊 Compliance report generated
- 🔗 Integration tests run
- 📦 Dependencies checked

### Running Workflows Locally

**Pre-commit validation (local):**
```bash
# Health check (same as CI/CD)
python3 packages/tools/health_check.py --verbose

# Tests (same as CI/CD)
cd packages && python3 tools/run-all-tests.py

# Lint (local pylint)
python3 -m pylint packages/**/*.py

# Governance (same as CI/CD)
python3 packages/governance_compliance.py --verify
```

**Pre-push hook behavior:**
```bash
# Install hooks (cross-platform)
python scripts/git_hooks.py install

git push origin main
# Runs .git/hooks/pre-push
# Validates: Health (10 checks) + Governance (4 mandates)
# If fails: Push is blocked
# Skip: git push --no-verify (not recommended)

# Uninstall hooks
python scripts/git_hooks.py uninstall
```

**View workflow logs:**
- GitHub → Actions tab → Click workflow
- Recent runs show status, timing, logs

### ⚠️ Important: Git Hooks in Framework vs Client Projects

**SDD Architecture framework** (this repo):
- ✅ `.git/hooks/pre-push` validates governance + health
- ✅ Blocks push if governance compliance fails
- ✅ This is correct - protects framework integrity

**Client projects** (generated by wizard - future):
- ⚠️ Should have `.git/hooks/pre-push` that validates **project quality only**
- ⚠️ Should NOT enforce SDD Architecture governance
- ⚠️ Should NOT block for framework compliance
- ✅ Can validate: tests pass, lint OK, local project health
- Note: Client hooks TBD - not yet implemented in seedlings

### Continuous Monitoring

| Check | Frequency | Dashboard |
|-------|-----------|-----------|
| Health | On push + daily | GitHub Actions → Health Check |
| Tests | On push | GitHub Actions → Tests |
| Compliance | Daily | GitHub Actions → Compliance Report |
| Dependencies | Weekly | GitHub Actions → Dependencies |
| Workflows | On push | GitHub Actions → Validate Workflows |

---

## �� Key Files

| File | Use When |
|------|----------|
| [.sdd-core/HONEST-CRITIQUE-CONSTITUTION.md](.sdd-core/HONEST-CRITIQUE-CONSTITUTION.md) | Need governance rules |
| [.sdd-core/spec/guides/onboarding/AGENT_HARNESS.md](.sdd-core/spec/guides/onboarding/AGENT_HARNESS.md) | Implementing a feature |
| [.sdd-core/spec/CANONICAL/decisions/](.sdd-core/spec/CANONICAL/decisions/) | Understand architecture |
| [.sdd-core/NAVIGATION.md](.sdd-core/NAVIGATION.md) | Find documentation |
| [docs/TEST_RUNNER_GUIDE.md](./docs/TEST_RUNNER_GUIDE.md) | Run tests |

---

## 📞 Help

- **Developer:** [.sdd-core/_START_HERE.md](.sdd-core/_START_HERE.md)
- **AI Agent:** [.ai-index.md](.ai-index.md)
- **Adding Project:** [.sdd-integration/README.md](.sdd-integration/README.md)
- **Tests:** [docs/TEST_RUNNER_GUIDE.md](./docs/TEST_RUNNER_GUIDE.md)
- **Emergency:** [.sdd-core/spec/guides/emergency/](.sdd-core/spec/guides/emergency/)

---

## ✅ Status

| Component | Status | Tests |
|-----------|--------|-------|
| Governance Pipeline | ✅ Complete | 13/13 |
| Compiler | ✅ Complete | 15/15 |
| Integration | ✅ Complete | 15/15 |
| Deployment | ✅ Complete | 16/16 |
| Wizard | ✅ Complete | 41/41 |
| CLI | ✅ Complete | 24/24 |
| **Total** | **✅ Ready** | **124/124** |

---

**SDD Framework v3.0** — Production Ready  
**Last Updated:** April 22, 2026  
**License:** MIT


## SDD CLi

```
sdd
sdd version
sdd setup run
sdd test run
sdd lint run
sdd wizard run
sdd governance load
sdd governance validate
sdd governance generate
sdd doctor run
sdd bootstrap run
```
