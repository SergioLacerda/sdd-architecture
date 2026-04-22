# 🏛️ SDD Architecture Framework - v3.0 Complete & Ready

**Specification-Driven Development with Autonomous Governance**

![Status](https://img.shields.io/badge/v3.0-✅%20Production-brightgreen?style=flat-square)
![Tests](https://img.shields.io/badge/Tests-124%2F124%20✅-brightgreen?style=flat-square)
![Docs](https://img.shields.io/badge/Docs-Consolidated-blue?style=flat-square)

---

## 📚 Documentation Hub

**Start here:** [.sdd-core/_START_HERE.md](.sdd-core/_START_HERE.md) - Get started with v3.0  
**Integration workflow:** [.sdd-integration/README.md](.sdd-integration/README.md) - Add projects (30 min)  
**Architecture overview:** [.sdd-core/NAVIGATION.md](.sdd-core/NAVIGATION.md) - Complete structure  
**AI agents:** [.ai-index.md](.ai-index.md) - Agent entry point

---

## 🎯 Quick Navigation

### Current Status (v3.0)
✅ **Production Ready** - In active use  
✅ **All Code Ready** - 124/124 tests passing (100%)  
✅ **Fully Consolidated** - Documentation organized  
✅ **CLI Ready** - Standalone binary for governance management  
→ Next: Deploy to your projects via [.sdd-integration/](.sdd-integration/)

---

## ✨ What's Ready in v3.0?

🏗️ **Complete Governance Pipeline** — 7-phase architecture, all phases complete (PHASES 1-7)

🔐 **Immutable Core + Flexible Client** — 2-file governance model with fingerprinting for integrity validation

🧠 **AI-First Design** — Autonomous governance for agent-driven development with 124/124 tests passing

📦 **CLI Binary Ready** — Standalone executable (`sdd` command) for governance management

🚀 **Production Ready** — All artifacts compiled, templates ready, integration workflow + operational guides

📖 **Operational Documentation** — Complete guides for deployment, monitoring, maintenance

→ **Full details:** [CHANGELOG.md](./CHANGELOG.md) | [.sdd-core/README.md](./.sdd-core/README.md)

---

## 🤖 CLI Usage

The SDD framework includes a powerful CLI for governance management built with Typer and PyInstaller.

### Installation & Setup

**Option 1: Use the Pre-built Binary (Recommended)**
```bash
# The binary is at: ./dist/sdd (20MB standalone executable)
# It requires NO Python installation

# Make it executable (Linux/macOS)
chmod +x ./dist/sdd

# Add to PATH (optional)
export PATH=$PATH:$(pwd)/dist
```

**Option 2: Install from Source**
```bash
# Requires Python 3.11+
pip install -r requirements-cli.txt

# Run via Python module
python -m sdd_cli --help
```

### Available Commands

#### 1. **Load Governance Configuration**
```bash
sdd governance load

# Output: Displays current governance configuration
# Shows: Core items (immutable) + Client items (customizable)
```

#### 2. **Validate Governance**
```bash
sdd governance validate

# Output: Validates governance integrity
# Checks: Fingerprints, file structure, compliance
```

#### 3. **Generate Agent Seeds**
```bash
sdd governance generate

# Output: Generates agent seed knowledge files
# Supports: Cursor IDE, GitHub Copilot, Generic AI agents
```

#### 4. **Check Version**
```bash
sdd version

# Output: Current framework version
```

### Examples

```bash
# Get help on any command
sdd --help
sdd governance --help

# Run full governance workflow
sdd governance load
sdd governance validate
sdd governance generate

# Check what version is running
sdd version
```

### What Each Command Does

| Command | Purpose | Output |
|---------|---------|--------|
| `sdd governance load` | Load + display governance config | 155 total items (4 core + 151 customizable) |
| `sdd governance validate` | Validate integrity + checksums | Fingerprint verification results |
| `sdd governance generate` | Create agent seed templates | 3 templates (Cursor, Copilot, Generic) |
| `sdd version` | Show framework version | Current version number |

### Troubleshooting

**"Command not found: sdd"**
- Make sure binary is in PATH: `export PATH=$PATH:$(pwd)/dist`
- Or use full path: `./dist/sdd --help`

**"Permission denied"**
- Binary needs execute permission: `chmod +x ./dist/sdd`

**Python version too old**
- Ensure Python 3.11+: `python --version`
- Or use pre-built binary (no Python needed)

---

## 🎯 What is SDD?

**SDD = Specification-Driven Development with Autonomous Governance**

A complete framework for building software where:
- ✅ **AI agents are first-class citizens** — Not afterthoughts, integral to workflow
- ✅ **Governance is automated** — Rules enforced via code, not meetings
- ✅ **Every decision is documented** — Architecture Decision Records (ADRs)
- ✅ **Developers are autonomous** — Clear rules, then get out of the way
- ✅ **Quality is measurable** — 45+ definition-of-done criteria
- ✅ **Scaling is seamless** — From 1 project to 100+ projects

---

## 🗺️ Project Organization

**Everything in this framework is organized into clear namespaces:**

- **.sdd-core/:** Governance specification + framework source
- **.sdd-integration/:** Adding projects to the framework (30 min)
- **.sdd-migration/:** v3.0 migration and historical documentation
- **.sdd-wizard/:** Runtime compiled artifacts
- **context/:** Historical analysis & decisions (reference)

---

## 🚀 Quick Start

**Decision Tree:**

### 🔷 **Are you adding a NEW project to SDD?**
Yes → **[.sdd-integration/](./.sdd-integration/)** (30 minutes, 5 steps)

### 🔷 **Are you developing code with SDD?**
Yes → **[.sdd-core/_START_HERE.md](./.sdd-core/_START_HERE.md)** (7-phase development workflow)

### 🔷 **Are you an AI agent?**
Yes → **[.ai-index.md](./.ai-index.md)** (governance rules + workflow)

### 🔷 **Need to use the CLI?**
Yes → **See CLI Usage section above** ↑

---

## 🎯 Find Your Task (Quick Navigation)

### I want to...

| Task | Time | Go To |
|------|------|-------|
| **Learn about SDD** | 5-10 min | [README.md](./README.md) (you are here) |
| **Add my project** | 30 min | [.sdd-integration/README.md](./.sdd-integration/README.md) → [.sdd-integration/CHECKLIST.md](./.sdd-integration/CHECKLIST.md) |
| **Start developing** | 5 min | [.sdd-core/_START_HERE.md](./.sdd-core/_START_HERE.md) |
| **Use the CLI** | 2 min | See **CLI Usage** section above |
| **See our design** | 1 page | [context/analysis/CRITIQUE-RESPONSE-EXEC-SUMMARY.md](./context/analysis/CRITIQUE-RESPONSE-EXEC-SUMMARY.md) |
| **Setup AI agent** | 5 min | [.ai-index.md](./.ai-index.md) |

### By Role

- **👨‍💼 Engineering Manager:** [.sdd-integration/README.md](./.sdd-integration/README.md) → Setup integration → Ready
- **👨‍💻 Developer:** [.sdd-core/_START_HERE.md](./.sdd-core/_START_HERE.md) → Read governance → Start coding
- **🤖 AI Agent:** [.ai-index.md](./.ai-index.md) → Understand rules → Execute workflow
- **🛠️ Operator/DevOps:** Run `sdd governance load` → See CLI Usage section

---

## 📁 Project Structure

### Root (Entry Points Only)
```
/
├── README.md                ← You are here (main entry point)
├── .ai-index.md            ← AI agents entry point
├── INDEX.md                ← Documentation index
├── CHANGELOG.md            ← Version history (v3.0 only)
├── LICENSE                 ← MIT license
├── .spec.config            ← Framework config
└── [configuration files]
```

### Integration Flow (Add Projects - 30 min)
```
.sdd-integration/
├── README.md               ← Integration overview
├── CHECKLIST.md            ← 5-step checklist
├── STEP_1.md through STEP_5.md
├── guides/                 ← Concepts & examples
└── templates/              ← Setup files to copy
```

### Development Flow (Ongoing)
```
.sdd-core/
├── _START_HERE.md          ← Developer entry point
├── NAVIGATION.md           ← Find anything
├── spec/
│   ├── CANONICAL/          ← Source of truth
│   │   ├── rules/
│   │   ├── decisions/      ← Architecture decisions (ADRs)
│   │   └── specifications/
│   └── guides/             ← How-to guides
├── execution_tests/        ← Test suite
└── tools/                  ← Framework tooling
```

### Runtime & Compilation
```
.sdd-wizard/               ← Runtime artifacts
.sdd-compiler/             ← Compiler source
.sdd-compiled/             ← Build outputs
```

### Historical Context
```
context/                   ← Analysis, critique, historical decisions
.sdd-migration/           ← v3.0 migration documentation
```

---

## ✨ Core Principles

### Two-File Governance Model
- **governance-core.json** (4 immutable items) — Never changes
- **governance-client.json** (151 customizable items) — Adapt to your needs
- SHA-256 fingerprinting ensures integrity
- Salt strategy prevents tampering

### 45+ Definition of Done Criteria
- Code quality checkpoints
- Architecture compliance rules
- Testing requirements
- Documentation standards
- Security validation

### 8 Architecture Layers
1. Interface (HTTP/gRPC)
2. Controllers (Request handling)
3. Services (Business logic)
4. Repository (Data access)
5. Models (Domain objects)
6. Adapters (External integrations)
7. Config (Settings management)
8. Infrastructure (Deployment)

---

## 👥 For Different Roles

### 👨‍💼 Engineering Managers
- Predictable delivery timelines
- Autonomous teams (less micromanagement)
- Scalable governance (works at 5 people → 500)
- Measurable quality metrics

→ **Start:** [.sdd-integration/README.md](./.sdd-integration/README.md)

### 👨‍💻 Individual Developers
- Clear rules to follow
- No ambiguity about quality
- Fast onboarding to new projects
- Structured code reviews

→ **Start:** [.sdd-core/_START_HERE.md](./.sdd-core/_START_HERE.md)

### 🤖 AI Agents
- Complete framework specification
- Autonomous decision-making rules
- Checkpoint documentation
- Full context available

→ **Start:** [.ai-index.md](./.ai-index.md)

### 🛠️ DevOps / Operators
- CLI tools for governance management
- Automated compliance checking
- Configuration templates
- Deployment automation

→ **Start:** `sdd governance load` (see CLI Usage section above)

---

## 🏆 Active Usage

**Currently running at:**
- 5+ projects (internal + partner teams)
- 3+ organizations (being tested)
- 100+ developer-hours (in production)

**Status:** Framework fully operational. Ready for production deployment.

---

## 🔗 Quick Links

| Need | Link |
|------|------|
| **AI governance rules** | [.github/copilot-instructions.md](./.github/copilot-instructions.md) |
| **New project integration** | [.sdd-integration/README.md](./.sdd-integration/README.md) |
| **Start developing** | [.sdd-core/_START_HERE.md](./.sdd-core/_START_HERE.md) |
| **Rules to follow** | [.sdd-core/spec/CANONICAL/rules/](./.sdd-core/spec/CANONICAL/rules/) |
| **Architecture patterns** | [.sdd-core/spec/CANONICAL/decisions/](./.sdd-core/spec/CANONICAL/decisions/) |
| **How-to guides** | [.sdd-core/spec/guides/](./.sdd-core/spec/guides/) |
| **Search documentation** | [.sdd-core/NAVIGATION.md](./.sdd-core/NAVIGATION.md) |
| **Troubleshooting** | [.sdd-core/spec/guides/emergency/](./.sdd-core/spec/guides/emergency/) |

---

## 🚀 Getting Started

### For Teams (30 minutes)
```bash
cd /path/to/new-project
# Follow: .sdd-integration/CHECKLIST.md
# Result: Project ready for development
```

### For Developers (5 min + ongoing)
```bash
# Already integrated? Start here:
# Read: .sdd-core/_START_HERE.md
# Follow: 7-phase development workflow
# Implement: Features with full governance
```

### For AI Agents (auto-onboarded)
```bash
# Framework provides: .ai-index.md (seed knowledge)
# Agent learns: Constitution, rules, architecture
# Agent executes: Full 7-phase workflow
```

### For DevOps
```bash
# Get governance info:
sdd governance load

# Validate system:
sdd governance validate

# Generate configs:
sdd governance generate
```

---

## 🏥 Operations & Production

**Running SDD in production? Start here:**

| Need | Guide | Time |
|------|-------|------|
| **Operational overview** | [.sdd-core/OPERATIONS-INDEX.md](./.sdd-core/OPERATIONS-INDEX.md) | 10 min |
| **Daily operations** | [.sdd-core/OPERATIONS.md](./.sdd-core/OPERATIONS.md) | Ongoing |
| **Deploy to production** | [.sdd-core/DEPLOYMENT.md](./.sdd-core/DEPLOYMENT.md) | 30-50 min |
| **Monitor system health** | [.sdd-core/MONITORING.md](./.sdd-core/MONITORING.md) | Ongoing |
| **Maintenance & upkeep** | [.sdd-core/MAINTENANCE.md](./.sdd-core/MAINTENANCE.md) | Scheduled |

**Quick reference:**
```bash
# Health check
./scripts/health-check.sh

# Governance validation
sdd governance validate

# Load configuration
sdd governance load
```

→ **Full operations guide:** [.sdd-core/OPERATIONS-INDEX.md](./.sdd-core/OPERATIONS-INDEX.md)

---

## 📝 License

![License](https://img.shields.io/badge/License-MIT-green)

**MIT License** — Free to use, modify, and distribute in personal or commercial projects.

See [LICENSE](./LICENSE) file for full text.

---

## 🤝 Contributing

This is a mature framework. Contributions should:
- Maintain world-class separation of concerns
- Preserve constitutional layer
- Document all decisions
- Pass 45+ quality criteria

For details: [.sdd-core/spec/CANONICAL/specifications/definition-of-done.md](./.sdd-core/spec/CANONICAL/specifications/definition-of-done.md)

---

## 📞 Support

**Questions?**
- Read: [.sdd-core/spec/guides/reference/FAQ.md](./.sdd-core/spec/guides/reference/FAQ.md)
- Search: [.sdd-core/NAVIGATION.md](./.sdd-core/NAVIGATION.md)
- Emergency: [.sdd-core/spec/guides/emergency/](./.sdd-core/spec/guides/emergency/)

---

**SDD v3.0 — Production Ready**  
Built by teams for teams. Fully tested and operational.

For machine learning seed: [.ai-index.md](./.ai-index.md)  
To integrate: [.sdd-integration/README.md](./.sdd-integration/README.md)  
To develop: [.sdd-core/_START_HERE.md](./.sdd-core/_START_HERE.md)  
To use CLI: `sdd --help`
