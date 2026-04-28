# _spec/ - Formal Specifications & Architecture

This directory contains all formal specification documents, architecture decisions, guides, and governance definitions for the SDD framework.

**Note:** Implementation context, project history, and workflow documentation has been moved to `/docs` for cleaner separation between "what we should do" (spec) and "how we're doing it" (docs).

## Structure

```
_spec/
├── architecture/                    # Architecture & Design
│   ├── decisions/                  # Architecture Decision Records (ADRs)
│   └── specifications/             # Detailed specifications
│
├── custom/                          # Project Specializations
│   └── _TEMPLATE/                  # Template for new projects
│
├── guides/                          # Implementation Guides
│   ├── adoption/                   # Adoption guides
│   ├── emergency/                  # Emergency procedures
│   ├── onboarding/                 # Getting started guides
│   ├── operational/                # Operational guides
│   ├── reference/                  # API/command reference
│   └── troubleshooting/            # Common issues & fixes
│
├── indices/                         # Search indices
│   ├── spec-canonical-index.md
│   ├── spec-guides-index.md
│   └── search-keywords.md
│
├── .ai/                             # AI Agent Configuration
│   ├── context-aware/              # Context-aware patterns
│   └── ...
│
├── .ai-index.md                    # AI index for agent onboarding
├── guidelines.dsl                  # DSL for governance guidelines
├── mandate.spec                    # Governance mandate specification
├── INDEX.md                        # Index of specifications
└── README.md                       # This file
```

## Quick Start

```bash
# View AI agent index (entry point for AI agents)
cat .ai-index.md

# View architecture decisions
cat architecture/decisions/

# View guides
cat guides/README.md

# View governance specifications
cat guidelines.dsl mandate.spec
```

## Key Documents

| Document | Purpose | Audience |
|----------|---------|----------|
| [.ai-index.md](.ai-index.md) | AI agent guide | AI Agents |
| [guidelines.dsl](guidelines.dsl) | Governance guidelines specification | Architects |
| [mandate.spec](mandate.spec) | Governance mandates | Everyone |
| [architecture/decisions/](architecture/decisions/) | Architecture decisions | Developers |
| [guides/](guides/) | Implementation guides | Developers |

## Sections

### 🏗️ Architecture & Design
- Architecture specifications in `architecture/specifications/`
- Architecture decisions (ADRs) in `architecture/decisions/`
- System design patterns and principles

### 🎯 Custom Projects
- `custom/_TEMPLATE/` - Template for creating new project specializations
- Shows how to extend SPEC for project-specific needs

### 📖 Guides
- **adoption/** - Adoption strategies (LITE, FULL, ULTRA-LITE)
- **emergency/** - Emergency procedures and recovery
- **onboarding/** - Getting started guides
- **operational/** - Operational procedures
- **reference/** - API/command reference
- **troubleshooting/** - Common issues & solutions

### 🤖 AI & Agent Configuration
- AI agent configuration files in `.ai/`
- `.ai-index.md` - Master index for AI agent operations
- Context-aware patterns and instructions

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
1. [_spec/README.md](README.md) - Overview (this file)
2. [architecture/decisions/](architecture/decisions/) - Architecture decisions (10 min)
3. [guides/adoption/](guides/adoption/) - Adoption guide for your team (15 min)
4. [guides/operational/](guides/operational/) - Operational procedures (10 min)

For implementation context and workflow history, see `/docs/`.

### 🤖 For AI Agents
Start with:
1. [.ai-index.md](.ai-index.md) - Complete AI guide
2. [.ai/](./ai/) - AI configuration files

### 📦 For Integration
Start with:
1. [guides/adoption/](guides/adoption/) - Adoption options
2. [architecture/decisions/](architecture/decisions/) - Architecture decisions

For implementation history and workflow documentation, see `/docs/`.

## Navigation

- **What's the current status?** → See [/docs/](../docs/) for workflow documentation
- **How do I run tests?** → See [/docs/TEST_RUNNER_GUIDE.md](../docs/TEST_RUNNER_GUIDE.md)
- **What changed?** → [/docs/CHANGELOG.md](../docs/CHANGELOG.md)
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

- [Root README.md](../README.md) - Main project documentation
- [docs/ README.md](../docs/README.md) - Implementation context and workflow documentation
- [packages/ README.md](../packages/README.md) - Code/implementation structure
