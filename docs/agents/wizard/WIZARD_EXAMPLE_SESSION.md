# 🧙 Exemplo Prático: Sessão Interativa do Wizard

Este arquivo mostra **exatamente** o que você verá quando executa `./wizard.sh` em modo interativo.

---

## 📺 Sessão Completa

```
~/dev/sdd-architecture$ ./wizard.sh

🧙 SDD v3.0 Interactive Wizard
======================================================================
Started: 2026-04-25 16:14:31

This guide will help you create a new SDD-compliant project step by step:

STEP 1️⃣  Review your governance source files
STEP 2️⃣  Configure your project (language, rules, output location)
STEP 3️⃣  Generate your project (automated 7-phase pipeline)
STEP 4️⃣  See where everything was created and next steps

Let's get started! 🚀

Press ENTER to continue...
```
**Você digita:** `<ENTER>`

---

## PASSO 1️⃣: Revisar Arquivos Fonte

```
📂 STEP 1: Review Source Files
======================================================================

These are your GOVERNANCE SOURCES that define your project's rules:


📋 A) Mandates (HARD rules)
------================================================================

Mandates are immutable rules that ALL projects must follow.
Examples: "Use Clean Architecture", "Write tests first"

  📄 mandate.spec
     Location: packages/.sdd-core/mandate.spec
     Size: 0.7 KB

  Preview mandate.spec? (y/n): 
```
**Você digita:** `y`

```
  📖 Preview (30 lines):
  ----------------------------------------------------------------------
  # SDD v3.0 - MANDATE Specification
  # Generated from v2.1 constitution
  # Generated: 2026-04-21T17:55:17.894942

  mandate M001 {
    type: HARD
    title: "Clean Architecture"
    description: "All systems must implement 8-layer Clean Architecture"
    category: architecture
    rationale: "Foundation enables testability and replaceability"
    validation: {
      commands: [
        "pytest tests/architecture/ -v",
      ]
    }
  }

  mandate M002 {
    type: HARD
    title: "Test-Driven Development"
    description: "All code must be written using TDD (tests first)"
    category: testing
    rationale: "Ensures quality and design clarity"
    validation: {
      commands: [
        "pytest --cov",
      ]
    }
  }
  ----------------------------------------------------------------------

📋 B) Guidelines (SOFT recommendations)
----------------------------------------------------------------------

Guidelines are customizable recommendations for your project.
Examples: "Documentation standards", "Naming conventions"

  📄 guidelines.dsl
     Location: packages/.sdd-core/guidelines.dsl
     Size: 27.6 KB

  Preview guidelines.dsl? (y/n): 
```
**Você digita:** `y`

```
  📖 Preview (25 lines):
  ----------------------------------------------------------------------
  # SDD v3.0 - GUIDELINES Specification
  # Generated from v2.1 guides
  # Generated: 2026-04-21T14:22:09.763692

  guideline G01 {
    type: SOFT
    title: "🛠️ Constitution Customization Guide"
    description: "---"
    category: general
  }

  guideline G02 {
    type: SOFT
    title: "When to Customize"
    description: "- ✅ Your domain has different scale needs..."
    category: general
  }

  guideline G03 {
    type: SOFT
    title: "What's Immutable vs Flexible"
    description: ""
    category: general
  }

  ... (147 more guidelines)
  ----------------------------------------------------------------------

  ✅ Source files confirmed
```

---

## PASSO 2️⃣: Configurar Seu Projeto

```
⚙️  STEP 2: Configure Your Project
======================================================================

What programming language will you use?

  1. python
  2. java
  3. typescript
  4. go
  5. rust
  6. other

Select (1-6): 
```
**Você digita:** `1`

```
  ✅ Language: python

📋 Select Mandates (HARD rules)
----------------------------------------------------------------------

Which mandates apply to your project?
All mandates are REQUIRED - select which ones to enforce:

  Include M001? (y/n): 
```
**Você digita:** `y`

```
  Include M002? (y/n): 
```
**Você digita:** `y`

```
  ✅ Selected 2 mandate(s): M001, M002

📋 Project Output Location
----------------------------------------------------------------------

Project output directory [/home/sergio/dev/sdd-architecture/packages/sdd-generated/project]: 
```
**Você digita:** `<ENTER>` (usar default)

```
  ✅ Output: /home/sergio/dev/sdd-architecture/packages/sdd-generated/project
```

---

## PASSO 3️⃣: Gerando Seu Projeto

```
🚀 STEP 3: Generating Your Project
======================================================================

Executing 7-phase pipeline...

  ✅ Phase 1: Source validation [COMPLETE]
  ✅ Phase 2: Loading compiled governance [COMPLETE]
     └─ Loaded: 2 mandates, 150 guidelines

  ⏳ Phase 3: Filtering mandates...
     ✅ Mandates filtered

  ⏳ Phase 4: Filtering guidelines...
     ✅ Guidelines filtered

  ⏳ Phase 5: Applying template scaffold...
     ✅ Template scaffolding applied

  ⏳ Phase 6: Generating project structure...
     ✅ Project structure generated

  ⏳ Phase 7: Validating output...
     ✅ Validation complete
```

---

## PASSO 4️⃣: Resultados - Onde Tudo Foi Gerado

```
✅ STEP 4: Project Generated Successfully! 🎉
======================================================================

📍 YOUR PROJECT LOCATION:
   /home/sergio/dev/sdd-architecture/packages/sdd-generated/project

📋 WHAT WAS GENERATED:
  📂 project/
     ├── .ai/
     │   ├── constitution.md
     │   ├── governance-core.json
     │   └── governance-client.json
     ├── src/
     ├── tests/
     ├── docs/
     │   └── ARCHITECTURE.md
     ├── .sdd-artifacts/
     └── README.md

🔑 KEY FILES:
  ✅ .ai/constitution.md         - Your project constitution & rules
  ✅ README.md                   - Project overview and setup
  ✅ src/                        - Your source code directory
  ✅ tests/                      - Test suite
  ✅ docs/ARCHITECTURE.md        - Architecture documentation

📖 NEXT STEPS:
  1. Read /home/sergio/dev/sdd-architecture/packages/sdd-generated/project/.ai/constitution.md to understand your rules
  2. Review the generated structure
  3. Start implementing according to the constitution
  4. Run tests: pytest tests/

💬 CONFIGURATION USED:
  Language: python
  Mandates: M001, M002
  Output: /home/sergio/dev/sdd-architecture/packages/sdd-generated/project

📚 LEARN MORE:
  • Constitution: /home/sergio/dev/sdd-architecture/packages/sdd-generated/project/.ai/constitution.md
  • Architecture: /home/sergio/dev/sdd-architecture/packages/sdd-generated/project/docs/ARCHITECTURE.md
  • Guidelines: /home/sergio/dev/sdd-architecture/packages/sdd-generated/project/.ai/governance-client.json

======================================================================
🎉 Your project is ready! Happy coding! 🎉
======================================================================
```

---

## 🎯 O Que Acontece em Cada Passo

### ✅ Passo 1: Review Source Files
- Mostra **localização exata** dos arquivos de governança
- Oferece **previews** dos conteúdos
- Você verifica se está tudo certo antes de continuar

### ✅ Passo 2: Configure Your Project
- Pergunta **linguagem** (python, java, typescript, etc)
- Pergunta quais **mandates** aplicam ao seu projeto
- Pergunta **diretório de saída** (com default inteligente)

### ✅ Passo 3: Generating Your Project
- Executa **7 fases do pipeline** automaticamente
- Mostra **progresso em tempo real**
- Cada fase valida, filtra, aplica templates, gera estrutura

### ✅ Passo 4: Project Generated
- Mostra **exatamente onde** o projeto foi criado
- Exibe **estrutura completa** do diretório gerado
- Lista **arquivos-chave** e seu propósito
- Dá **próximos passos** (leia constitution, rode testes)

---

## 📍 Localizações de Tudo

| O Quê | Localização |
|-------|-------------|
| **Arquivos Source** | `packages/.sdd-core/` |
| ├─ mandate.spec | `packages/.sdd-core/mandate.spec` |
| ├─ guidelines.dsl | `packages/.sdd-core/guidelines.dsl` |
| **Governança Compilada** | `packages/.sdd-compiled/` |
| ├─ governance-core.json | `packages/.sdd-compiled/governance-core.json` |
| ├─ governance-client.json | `packages/.sdd-compiled/governance-client.json` |
| **Projeto Gerado** | *(configurable, default abaixo)* |
| ├─ Constitution | `<output>/.ai/constitution.md` |
| ├─ Governance Artifacts | `<output>/.ai/governance-*.json` |
| ├─ Source Code | `<output>/src/` |
| ├─ Tests | `<output>/tests/` |
| └─ Docs | `<output>/docs/` |

---

## 🔄 Fluxo Completo

```
Você executa: ./wizard.sh
    ↓
Wizard entra em MODO INTERATIVO
    ↓
PASSO 1: Mostra source files (mandate.spec, guidelines.dsl)
    ↓
PASSO 2: Coleta sua configuração
    ├─ Linguagem? (python, java, typescript...)
    ├─ Quais mandates? (M001, M002, etc)
    └─ Diretório de saída?
    ↓
PASSO 3: Executa 7 fases do pipeline
    ├─ Phase 1: Valida source files
    ├─ Phase 2: Carrega governance compilada
    ├─ Phase 3: Filtra mandates selecionados
    ├─ Phase 4: Filtra guidelines por linguagem
    ├─ Phase 5: Copia templates
    ├─ Phase 6: Gera estrutura do projeto
    └─ Phase 7: Valida output
    ↓
PASSO 4: Mostra resultados
    ├─ Localização exata do projeto
    ├─ Estrutura de diretórios criada
    ├─ Arquivos-chave e seus propósitos
    └─ Próximos passos
    ↓
✅ Pronto! Seu projeto está criado
```

---

## 💡 Dicas

1. **Sempre prefira modo interativo**: Oferece orientação clara
2. **Customize os sources se necessário**: Edite `packages/.sdd-core/mandate.spec` e `guidelines.dsl`, então rode o wizard novamente
3. **Verifique o diretório de saída**: Default é `packages/sdd-generated/project` - customize se precisar
4. **Leia a constitution gerada**: Entenda as regras do seu projeto em `.ai/constitution.md`

---

**Pronto! Agora você sabe exatamente como o wizard funciona! 🚀**
