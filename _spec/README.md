# _spec/ - Specification & Documentation

This directory contains all specification documents, design decisions, guides, and governance items documentation for the SDD framework.

## Structure

```
_spec/
├── docs/                   # Main documentation
│   ├── INDEX.md
│   ├── TEST_RUNNER_GUIDE.md
│   ├── CHANGELOG.md (moved from root)
│   └── ...
│
├── Workflow Documentation
│   ├── PHASE_2_OUTPUT_ANALYSIS.md
│   ├── PHASE_2_VALIDATION_CHECKLIST.md
│   ├── PHASE_3_WIZARD_INTEGRATION.md
│   └── CHECKPOINT_DOCUMENTATION_RESTRUCTURING.md
│
├── Architecture & Design
│   ├── ARCHITECTURE.md
│   ├── DESIGN.md
│   └── decisions/
│
├── Governance Items Spec
│   ├── governance_specification.md
│   ├── CONSTITUTION.md
│   └── ...
│
├── Guides (onboarding, troubleshooting, reference)
│   ├── guides/
│   ├── onboarding/
│   ├── troubleshooting/
│   └── reference/
│
├── AI & Agent Configuration
│   ├── .ai/                # AI agent configuration
│   ├── .ai-index.md        # AI index for agent onboarding
│   └── copilot-instructions.md
│
└── Context & History
    ├── context/            # Historical analysis
    ├── CHANGELOG.md        # Version history
    └── RELEASE_NOTES.md
```

## Quick Start (Documentation)

```bash
# View main documentation index
cat docs/INDEX.md

# AI agent entry point
cat .ai-index.md

# View phase documentation
cat PHASE_3_WIZARD_INTEGRATION.md

# View guides
cat guides/README.md
```

## Key Documents

| Document | Purpose | Audience |
|----------|---------|----------|
| [docs/INDEX.md](docs/INDEX.md) | Main docs index | Everyone |
| [.ai-index.md](.ai-index.md) | AI agent guide | AI Agents |
| [PHASE_3_WIZARD_INTEGRATION.md](PHASE_3_WIZARD_INTEGRATION.md) | Wizard integration | Developers |
| [CHANGELOG.md](CHANGELOG.md) | Version history | Everyone |
| [TEST_RUNNER_GUIDE.md](docs/TEST_RUNNER_GUIDE.md) | Testing guide | Developers |

## Sections

### 📚 Documentation (`docs/`)
- Main documentation index
- API documentation
- User guides
- Testing guides

### 🏗️ Architecture & Design
- Architecture specifications
- Design decisions (ADRs)
- System diagrams
- Design patterns

### 📋 Workflow Documentation
- PHASE_*.md files documenting each phase
- Analysis of outputs
- Validation checklists
- Implementation guides

### 📖 Guides
- **Onboarding/** - Getting started guides
- **Troubleshooting/** - Common issues and fixes
- **Reference/** - API reference, command reference
- **Guides/** - How-to guides and tutorials

### 🤖 AI & Agent Configuration
- AI agent configuration files
- Instruction sets for agents
- AI context and prompts

### 📊 Governance Items
- Governance specifications (mandates, guidelines, rules)
- Constitution templates
- Governance item documentation

### 📈 Context & History
- Changelog documenting all releases
- Historical analysis and decisions
- Release notes
- Previous implementation notes

## Documentation Standards

All documentation follows **IA-FIRST** format:

```markdown
# Title (H1)

⚡ IA-FIRST DESIGN NOTICE
- Structure: H1 → H2 (sections) → H3 (subsections) → Lists
- All lists use `-` (not numbers or bullets)
- All links use `[text](path.md)` format (no backticks)
- All constraints marked with emoji (✅, ❌, ⚠️, etc.)

## Section (H2)

### Subsection (H3)

- Item 1
- Item 2
  - Nested item
```

## Audience Guides

### 👨‍💻 For Developers
Start with:
1. [docs/INDEX.md](docs/INDEX.md) - Overview (5 min)
2. [PHASE_3_WIZARD_INTEGRATION.md](PHASE_3_WIZARD_INTEGRATION.md) - Current work (10 min)
3. [docs/TEST_RUNNER_GUIDE.md](docs/TEST_RUNNER_GUIDE.md) - Running tests (5 min)

### 🤖 For AI Agents
Start with:
1. [.ai-index.md](.ai-index.md) - Complete AI guide
2. [.ai/](./ai/) - AI configuration files

### 📦 For Integration
Start with:
1. [PHASE_3_WIZARD_INTEGRATION.md](PHASE_3_WIZARD_INTEGRATION.md) - Integration overview
2. [docs/INDEX.md](docs/INDEX.md) - Full documentation

## Navigation

- **What's the current status?** → [PHASE_3_WIZARD_INTEGRATION.md](PHASE_3_WIZARD_INTEGRATION.md)
- **How do I run tests?** → [docs/TEST_RUNNER_GUIDE.md](docs/TEST_RUNNER_GUIDE.md)
- **What changed?** → [CHANGELOG.md](CHANGELOG.md)
- **I'm an AI agent** → [.ai-index.md](.ai-index.md)
- **I need help** → [guides/troubleshooting/](guides/troubleshooting/)
- **I want to learn** → [guides/onboarding/](guides/onboarding/)

## Contributing to Documentation

1. Use IA-FIRST format
2. Keep documents concise
3. Add emoji markers for status
4. Link to related documents
5. Include code examples for technical docs
6. Add timestamps for time-sensitive docs

## See Also

- [Root README.md](../README.md) - Main documentation
- [_core/ README.md](_core/README.md) - Code/implementation structure
- [Implementation docs](docs/) - Full documentation
