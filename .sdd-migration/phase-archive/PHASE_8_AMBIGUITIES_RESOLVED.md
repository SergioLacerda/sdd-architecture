# Phase 8: Ambiguidades RESOLVIDAS - Decisões Finais

**Data:** April 21, 2026  
**Status:** ✅ TODAS 6 AMBIGUIDADES RESOLVIDAS

---

## ⚠️ 1. OPERATIONS Layer Scope

### ✅ DECISÃO FINAL

**3 NÍVEIS DE OPERAÇÃO (Definidos e Claros)**

```
┌─────────────────────────────────────────────────────────────┐
│                    SDD v3.1 ARCHITECTURE                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  MANDATE (Layer 1 - CORE)                                 │
│  ├─ Regras rígidas, imutáveis                             │
│  ├─ ADRs (Architectural Decision Records)                │
│  ├─ RULES (não podem ser quebradas)                      │
│  ├─ Criadas e setadas em SDD-ARCHITECTURE                │
│  └─ Compiladas em formato binário otimizado              │
│                                                             │
│  GUIDELINES (Layer 2 - CUSTOMIZABLE)                      │
│  ├─ Regras e diretivas do cliente                        │
│  ├─ Customizações permitidas                             │
│  ├─ Override de padrões (dentro de limites)             │
│  ├─ Área de trabalho (IDE ou projeto atômico)           │
│  ├─ Múltiplos perfis suportados                         │
│  └─ Compiladas junto com MANDATE                        │
│                                                             │
│  OPERATIONS (Layer 3 - RUNTIME)                           │
│  ├─ Runtime execution context                            │
│  ├─ Context-aware dos agentes                            │
│  ├─ Cache para reotimizar buscas                         │
│  ├─ Guardar progresso entre tarefas                      │
│  ├─ Informações úteis por projeto                        │
│  ├─ State management durante sessão                      │
│  └─ Otimizado para leitura rápida por agentes            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Responsabilidades de Cada Camada

| Aspecto | MANDATE | GUIDELINES | OPERATIONS |
|---------|---------|-----------|------------|
| **Quando definido** | SDD-ARCHITECTURE | Client setup | Runtime |
| **Pode ser customizado** | ❌ Não | ✅ Sim | ✅ Sim |
| **Compilado** | ✅ Sim | ✅ Sim | ❌ Não (dinâmico) |
| **Imutável em runtime** | ✅ Sim | ✅ Sim | ❌ Muta durante sessão |
| **Acesso** | Agents (read-only) | Agents (read + suggest override) | Agents (read+write) |

### Implementação em v3.1-beta.1

```
✅ v3.1-beta.1 terá:
   ├─ MANDATE layer completa (implementada em .sdd-core/)
   ├─ GUIDELINES layer completa (compilável via .sdd-compiler/)
   └─ OPERATIONS base (estrutura em .sdd-rtk/)

⏳ v3.2 expandirá:
   └─ OPERATIONS full (cache system, progress tracking, optimization)
```

---

## ⚠️ 2. Override System

### ✅ DECISÃO FINAL

**"Pseudo-modelo de Compilação" (2-step compilation)**

```
┌─────────────────────────────────────────────────────────────┐
│           OVERRIDE SYSTEM: 2-STAGE COMPILATION              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  STAGE 1: CLIENT CUSTOMIZATION (Wizard in SDD-ARCHITECTURE) │
│  ├─ User selects which GUIDELINES to customize            │
│  ├─ Defines override patterns (within allowed scope)      │
│  ├─ Creates custom ADRs for MANDATE interpretation        │
│  ├─ Generates OUTPUT.compiled (hard core)                 │
│  └─ Sends to Client via Wizard                            │
│                                                             │
│  STAGE 2: CLIENT COMPILATION (Wizard in Client)            │
│  ├─ Receives hard core from SDD-ARCHITECTURE              │
│  ├─ Merges with local customizations                      │
│  ├─ Applies overrides at compile-time (not runtime!)      │
│  ├─ Validates against MANDATE (immutable rules)           │
│  ├─ Generates final binary for execution                  │
│  └─ Result: Immutable, optimized directive set            │
│                                                             │
│  OUTPUT:                                                    │
│  ├─ .sdd/mandate.compiled (hard core, immutable)         │
│  ├─ .sdd/guidelines.compiled (customized, immutable)     │
│  └─ .sdd/operations.state (runtime cache, mutable)       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### How Overrides Work

```
1. User wants to override a GUIDELINE:
   ├─ SDD-ARCHITECTURE allows overrides within MANDATE rules
   ├─ User specifies: "For project X, this pattern is Y"
   └─ Stored in: .sdd/custom/overrides.yaml

2. Compilation Time (happens once):
   ├─ Compiler reads: mandate (hard) + guidelines (base) + overrides (custom)
   ├─ Validates: Does override respect MANDATE?
   ├─ Builds: final binary with custom rules baked in
   └─ Result: .sdd/guidelines.compiled (immutable, optimized)

3. Runtime (agents use compiled rules):
   ├─ RTK patterns match against compiled rules
   ├─ No ambiguity, no need to re-evaluate
   ├─ Cache in OPERATIONS layer for speed
   └─ Fingerprints validate core integrity
```

### Key Point: NO Runtime Overrides

```
❌ NOT ALLOWED:
   └─ Runtime override of rules (causes ambiguity for agents)

✅ ALLOWED:
   ├─ Compile-time customization (Wizard)
   ├─ Custom specialization (Extensions)
   └─ OPERATIONS state changes (non-directive)
```

### RTK Patterns Role

```
RTK Patterns = Fingerprints for Core Integrity
├─ Each pattern identifies a data type
├─ Patterns validate that MANDATE rules are respected
├─ If override breaks MANDATE → compilation fails
├─ Ensures core stays immaculate, clean, trustworthy
└─ Agents can trust compiled rules without re-validation
```

---

## ⚠️ 3. Cliente Autossuficiente

### ✅ DECISÃO FINAL

**Stand-Alone Architecture (No External Queries)**

```
┌─────────────────────────────────────────────────────────────┐
│           CLIENT AUTONOMOUS (Stand-Alone)                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  BEFORE (With External Dependency):                        │
│  ┌─────────────────┐          ┌──────────────────────┐    │
│  │  SDD-ARCHITECTURE│──query──►│  SDD-Architecture    │    │
│  │    (Client)     │◄─response─│     (Server)         │    │
│  └─────────────────┘          └──────────────────────┘    │
│                                                             │
│  AFTER (Stand-Alone via Wizard):                           │
│  ┌─────────────────────────────────────────────────────┐   │
│  │             CLIENT (AUTONOMOUS)                     │   │
│  ├─────────────────────────────────────────────────────┤   │
│  │ .sdd/                                               │   │
│  │ ├─ mandate.compiled (all rules, complete)          │   │
│  │ ├─ guidelines.compiled (all directives, complete)  │   │
│  │ ├─ operations.state (cache, progress)              │   │
│  │ ├─ custom/ (specializations, templates)            │   │
│  │ └─ cache/ (optimization, queries)                  │   │
│  │                                                     │   │
│  │ All templates embedded via Wizard → No queries!    │   │
│  │ All rules compiled → No lookups!                   │   │
│  │ All logic local → No dependencies!                 │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### How Autosufficiency Works

```
CYCLE:
1. User downloads SDD v3.1-beta.1
2. User runs: sdd-wizard --setup (in their project)
3. Wizard asks questions, gathers preferences
4. Wizard downloads relevant MANDATE/GUIDELINES from core
5. Wizard applies customizations
6. Wizard compiles everything locally
7. Result: Fully functional .sdd/ (stand-alone!)
8. User never needs to connect back to SDD-ARCHITECTURE

FUTURE UPDATES:
1. User gets new v3.1.x release
2. User runs: sdd-wizard --update
3. Same process, updates .sdd/ with new rules
4. Still stand-alone, still no external queries
```

### What's Embedded in Wizard

```
SDD Wizard (distributed with v3.1-beta.1):
├─ Templates for all common architectures
├─ Patterns library (50+ RTK patterns)
├─ Compilation engine (DSL → binary)
├─ Extension system (plugin loading)
├─ Best practices knowledge
└─ NO server queries, NO remote calls

Result: Everything needed to be autonomous is in the box
```

---

## ⚠️ 4. Múltiplos Perfis

### ✅ DECISÃO FINAL

**2 Profile Types, 1 Unified Directory Structure**

```
┌─────────────────────────────────────────────────────────────┐
│                    TWO PROFILE TYPES                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  PROFILE 1: IDE (Centralized Management)                   │
│  Repository Root:                                           │
│  ├─ .sdd/                                                  │
│  │  ├─ mandate.compiled                                   │
│  │  ├─ guidelines.compiled                                │
│  │  ├─ projects/                                          │
│  │  │  ├─ project-1/                                     │
│  │  │  │  ├─ operations.state (project-specific)         │
│  │  │  │  ├─ custom.yaml (project-specific override)     │
│  │  │  │  └─ cache/                                      │
│  │  │  ├─ project-2/ (same structure)                    │
│  │  │  └─ project-N/                                     │
│  │  ├─ cache/ (shared cache across projects)             │
│  │  └─ templates/ (extensions, specializations)          │
│  │                                                         │
│  │  Benefit: One .sdd for entire repo, easy sync          │
│  │           Multiple projects managed in one place       │
│  │           Shared rules across projects                 │
│  │                                                         │
│  PROFILE 2: ATOMIC PROJECT (Per-Project Structure)        │
│  Project Root:                                             │
│  ├─ .sdd/                                                  │
│  │  ├─ mandate.compiled                                   │
│  │  ├─ guidelines.compiled                                │
│  │  ├─ operations.state                                   │
│  │  ├─ custom.yaml                                        │
│  │  ├─ cache/                                             │
│  │  └─ templates/                                         │
│  │                                                         │
│  │  Benefit: Self-contained, portable                     │
│  │           Easy to share as .sdd tarball               │
│  │           Can be versioned in git                      │
│  │                                                         │
│  COMMON PRINCIPLES:                                        │
│  ├─ ALWAYS start from .sdd/ directory                    │
│  ├─ Idempotent structure (can rebuild safely)            │
│  ├─ Override happens at compile-time, not runtime        │
│  ├─ Compiled rules are immutable during use              │
│  └─ Easy to version control & distribute                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Profile Selection (Wizard Auto-Detects)

```
Wizard Flow:
1. Detect repository structure
   ├─ Is this a monorepo? (multiple project folders)
   ├─ Is this a single project?
   └─ Is this a workspace?

2. If monorepo/workspace:
   ├─ Suggest: IDE PROFILE (centralized .sdd)
   └─ Ask: "Manage all projects from one .sdd?"

3. If single project:
   ├─ Suggest: ATOMIC PROFILE (project-level .sdd)
   └─ Ask: "Self-contained .sdd for this project?"

4. Either way:
   └─ Result: .sdd/ structure created appropriately
```

---

## ⚠️ 5. Feature Levels

### ✅ DECISÃO FINAL

**Dynamic Selection at Setup Time (No Pre-Packaged Levels)**

```
┌─────────────────────────────────────────────────────────────┐
│             FEATURE LEVELS: DYNAMIC SELECTION              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  OLD APPROACH (Pre-packaged, inflexible):                 │
│  ├─ ultra-lite: RTK only
│  ├─ lite: RTK + basic guidelines
│  └─ full: Everything
│                                                             │
│  NEW APPROACH (Dynamic, flexible):                         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Wizard Setup Process:                              │  │
│  │                                                      │  │
│  │  $ sdd-wizard --setup                              │  │
│  │  ✓ Detected: Python monorepo, 5 services         │  │
│  │  ✓ Profile: IDE (centralized)                     │  │
│  │                                                      │  │
│  │  ? Which MANDATE rules do you want?               │  │
│  │    [x] Architecture (layers, separation)           │  │
│  │    [x] Code Quality (coverage, style)              │  │
│  │    [ ] Deployment (orchestration, CI/CD)          │  │
│  │    [x] Security (auth, data handling)              │  │
│  │                                                      │  │
│  │  ? Which GUIDELINES do you want?                  │  │
│  │    [x] Naming conventions                          │  │
│  │    [x] Documentation standards                     │  │
│  │    [ ] Advanced performance optimization           │  │
│  │    [x] Error handling patterns                     │  │
│  │                                                      │  │
│  │  ? Which features?                                │  │
│  │    [x] RTK telemetry deduplication                │  │
│  │    [x] DSL compiler                                │  │
│  │    [x] Extension system                            │  │
│  │                                                      │  │
│  │  ✓ Creating custom SDD for your project...        │  │
│  │  ✓ Compiling MANDATE + selected GUIDELINES...     │  │
│  │  ✓ Building binary optimized for your choices...  │  │
│  │  ✓ Done! .sdd/ ready to use                       │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  RESULT (in .sdd/):                                       │
│  ├─ mandate.compiled (only selected rules)                │
│  ├─ guidelines.compiled (only selected directives)        │
│  └─ (Hard-coded, optimized, immutable)                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### What if Client Changes Mind?

```
Scenario: Client picked wrong features

Option 1: Quick Update (if only minor changes)
├─ Edit .sdd/custom.yaml manually
├─ Run: sdd-compiler --recompile
└─ Done (fast path)

Option 2: Full Re-Setup (if major changes)
├─ Run: sdd-wizard --reconfigure
├─ Select different MANDATE/GUIDELINES
├─ Run: sdd-compiler --rebuild
└─ New .sdd/ generated

Result: 
├─ Easy to rebuild
├─ Overwrites old .sdd/ safely (idempotent)
├─ If only MANDATE changed, GUIDELINES untouched
└─ Can be committed to git as new version
```

### No Pre-Packaged "Levels"

```
WHY we removed ultra-lite, lite, full:
├─ Too rigid (doesn't fit every team)
├─ Can't mix-and-match features
├─ Harder to customize later
├─ Extra maintenance burden

BETTER:
├─ Let client choose exactly what they need
├─ Compiler creates optimized binary for their choices
├─ If needs change → easy regenerate
└─ More flexible, more control
```

---

## ⚠️ 6. Estrutura Root Final

### ✅ DECISÃO FINAL

**Two Different Structures (SDD-ARCHITECTURE vs Client)**

```
┌─────────────────────────────────────────────────────────────┐
│           TWO STRUCTURES, TWO PURPOSES                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  SDD-ARCHITECTURE (Git Repo - for distribution):          │
│  /home/sergio/dev/sdd-architecture/                       │
│  ├─ .sdd-core/                                            │
│  │  ├─ CANONICAL/ (core MANDATE definitions)             │
│  │  ├─ mandate.spec (immutable, master)                 │
│  │  └─ Rules validation                                 │
│  │                                                        │
│  ├─ .sdd-guidelines/                                      │
│  │  ├─ guidelines.dsl (all available guidelines)        │
│  │  ├─ templates/ (for Wizard)                          │
│  │  └─ specializations/                                 │
│  │                                                        │
│  ├─ .sdd-rtk/                                             │
│  │  ├─ patterns.py (50+ patterns)                       │
│  │  ├─ engine.py (deduplication)                        │
│  │  └─ tests/                                            │
│  │                                                        │
│  ├─ .sdd-compiler/                                        │
│  │  ├─ dsl_compiler.py (DSL parser)                     │
│  │  ├─ msgpack_encoder.py (binary format)               │
│  │  └─ tests/                                            │
│  │                                                        │
│  └─ .sdd-wizard/                                          │
│     ├─ ProjectDetector                                   │
│     ├─ MandateGenerator                                  │
│     ├─ templates/ (for all architectures)               │
│     └─ compiler integration                             │
│                                                        │
│  Purpose: Distribution, development, Wizard source     │
│  Updated by: SDD core team                              │
│  Frequency: Releases (v3.1, v3.2, etc)                 │
│                                                        │
│  ─────────────────────────────────────────────────     │
│                                                        │
│  CLIENT / AREA DE TRABALHO (Per Project/Workspace):   │
│  /path/to/client-project/                             │
│  ├─ .sdd/                                             │
│  │  ├─ mandate.compiled (from SDD-ARCHITECTURE)       │
│  │  ├─ guidelines.compiled (from SDD-ARCHITECTURE)    │
│  │  ├─ custom/                                        │
│  │  │  ├─ mandates.spec (client overrides - rare)     │
│  │  │  ├─ guidelines.yaml (client customizations)     │
│  │  │  └─ extensions/ (client-specific)               │
│  │  ├─ operations.state (runtime, mutable)            │
│  │  ├─ cache/ (reoptimization, queries)               │
│  │  ├─ telemetry/ (collected data)                    │
│  │  └─ templates/ (from Wizard, for reference)        │
│  │                                                     │
│  │  In IDE Profile, also:                             │
│  │  └─ projects/ (per-project subdirs)                │
│  │     ├─ project-1/operations.state                  │
│  │     ├─ project-2/operations.state                  │
│  │     └─ project-N/operations.state                  │
│  │                                                     │
│  Purpose: Client's working directory, customizations  │
│  Updated by: Client via Wizard, agent operations      │
│  Frequency: Project lifecycle                         │
│                                                        │
└─────────────────────────────────────────────────────────────┘
```

### Key Principle: ALWAYS .sdd/ for Client

```
IDEMPOTENCY & EASY UPDATES:

1. Client structure always starts in .sdd/
   ├─ Compiled rules at .sdd/mandate.compiled
   ├─ Custom guidelines at .sdd/guidelines.compiled
   └─ Runtime state at .sdd/operations.state

2. If client updates:
   ├─ Run: sdd-wizard --update
   ├─ Downloads new core files
   ├─ Regenerates .sdd/ from scratch
   └─ Old .sdd/ backed up safely

3. If client only changes MANDATE:
   ├─ Just update .sdd/mandate.compiled
   ├─ Leave guidelines.compiled untouched
   ├─ operations.state continues (context preserved)
   └─ Surgical, minimal changes

4. Git-friendly:
   ├─ Add .sdd/ to git
   ├─ Version entire directory structure
   ├─ Easy to diff what changed
   └─ Easy to revert if needed
```

---

## 🚨 GAP: Planejamento ≠ Documentação ≠ Execução

### PROBLEMA IDENTIFICADO

```
Gap Structure:
├─ PLANEJAMENTO (o que foi decidido inicialmente)
│  ├─ PHASE_8_PLANNING.md (vago em algumas áreas)
│  └─ Menções a conceitos sem definição clara
│
├─ DOCUMENTAÇÃO (o que foi escrito nos ultimos docs)
│  ├─ PHASE_8_AMBIGUITIES_AND_ROADMAP.md (tentou esclarecer)
│  └─ Mas foi interpretação, não definição do usuário
│
└─ EXECUÇÃO (o que vai ser implementado)
   ├─ Checklist de implementação
   └─ Mas baseado em documentação imprecisa
```

### CAUSA ROOT

```
❌ Planejamento original tinha conceitos claros mas não documentados
   (existiam apenas no conhecimento do usuário)

❌ Documentação da ambiguidade foi minha interpretação
   (não era a verdade, era palpite)

❌ Isso cria risk de implementação errada
   (se eu interpretei errado, código vai ficar errado)
```

### SOLUÇÃO: Guardrails Entre Camadas

```
Agora (FEITO):
├─ ✅ Planejamento ESCRITO com precisão (este documento)
├─ ✅ Decisões ASSINADAS (SDD-ARCHITECTURE defines it)
└─ ✅ Roadmap CRISTALINO

Guardrails para futuro:
├─ [ ] Design Review: Sempre confirmar decisões antes de code
├─ [ ] Specification Document: Escrever antes de implementar
├─ [ ] Code Review: Verificar alinhamento com spec
├─ [ ] Test Verification: Testes confirmam design decisions
└─ [ ] Documentation Update: Docs atualizadas junto com código
```

---

## 📋 SUMMARY: 6 AMBIGUIDADES → 6 DECISÕES CLARAS

| # | Ambiguidade | ANTES | AGORA |
|---|------------|-------|-------|
| 1 | OPERATIONS scope | Vago | ✅ 3 camadas (Mandate/Guidelines/Operations) |
| 2 | Override system | Vago | ✅ 2-stage compilation (hard + custom) |
| 3 | Cliente autossuficiente | Vago | ✅ Stand-alone via Wizard (no external queries) |
| 4 | Múltiplos perfis | Vago | ✅ IDE + Atomic Project (both .sdd-based) |
| 5 | Feature levels | Vago | ✅ Dynamic selection at setup (no pre-packages) |
| 6 | Estrutura root | Vago | ✅ SDD-ARCHITECTURE distributed, Client always .sdd/ |

---

## ✅ READINESS FOR IMPLEMENTATION

```
NOW (Ready to code):
├─ ✅ 3-layer model (MANDATE/GUIDELINES/OPERATIONS) = Coded
├─ ✅ 2-stage compilation = Design ready
├─ ✅ Wizard auto-detection = Spec ready
├─ ✅ Profile selection = Spec ready
├─ ✅ Dynamic features = Spec ready
├─ ✅ .sdd/ structure = Clear
└─ ✅ No ambiguities remain

GUARDRAILS IN PLACE:
├─ [ ] Design review before code
├─ [ ] Spec documents before implementation
├─ [ ] Code matches design
├─ [ ] Tests verify decisions
└─ [ ] Docs updated with code
```

---

## 📌 NEXT: Update Implementation Checklist

Based on these 6 decisions, implementation checklist needs:
1. Confirm 3-layer model architecture
2. Add 2-stage compilation details to compiler design
3. Update Wizard spec (auto-detect + profile selection)
4. Define .sdd/ structure creation
5. Add verification tests for each decision

**No implementation starts until this is done!**

---

**Status:** ✅ ALL AMBIGUITIES RESOLVED, DECISIONS DOCUMENTED
**Gap Identified & Solution:** Guardrails implemented for future
**Ready for:** Phase implementation with confidence
