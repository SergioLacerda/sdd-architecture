# 📐 SDD v3.0 Architecture & Workflow

**Date:** April 21, 2026  
**Status:** Architecture Finalized (Simplified Paths)

---

## 🎯 Overview: Source → Compile → Template → Deliver

```
┌─────────────────────────────────────────────────────────────────┐
│ VOCÊ (Arquiteto) edita FONTE                                   │
├─────────────────────────────────────────────────────────────────┤
│ .sdd-core/mandate.spec                                         │
│ .sdd-core/guidelines.dsl                                       │
│ (sem /CANONICAL - paths simplificados)                         │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ↓ COMPILADOR (.sdd-compiler/)
┌─────────────────────────────────────────────────────────────────┐
│ COMPILADO (automático, via CI/CD)                              │
├─────────────────────────────────────────────────────────────────┤
│ .sdd-runtime/mandate.bin (msgpack)                             │
│ .sdd-runtime/guidelines.bin (msgpack)                          │
│ .sdd-runtime/metadata.json                                     │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ├─→ Lê .sdd-template/ (scaffold pré-pronto)
                     │
                     ↓ WIZARD (sob demanda)
┌─────────────────────────────────────────────────────────────────┐
│ TEMPLATE FINAL (estrutura .sdd pronta para deploy)             │
├─────────────────────────────────────────────────────────────────┤
│ Cliente recebe (.sdd/ - ponto final de entrega):              │
│ ├── Specs compiladas                                           │
│ ├── Guidelines filtradas                                       │
│ ├── Examples prontos                                           │
│ └── Orientações ao usuário                                     │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📍 Directory Structure & Responsibilities

### 1️⃣ SOURCE - You Edit Here (SIMPLIFIED PATHS)

```
.sdd-core/                          (Fonte - você edita)
├── mandate.spec                    
│   ├─ Location: .sdd-core/ (raiz, NÃO em subdirectory)
│   ├─ Origin: Extracted from v2.1
│   ├─ Format: SDD DSL (spec-v1)
│   ├─ Content: 2 mandates (M001, M002)
│   ├─ You: Edit to change hard rules
│   └─ Lifecycle: Committed to main via PR only
│
└── guidelines.dsl                  
    ├─ Location: .sdd-core/ (raiz, NÃO em subdirectory)
    ├─ Origin: Extracted from v2.1
    ├─ Format: SDD DSL (spec-v1)
    ├─ Content: 150 guidelines
    ├─ You: Edit to change soft patterns
    └─ Lifecycle: Committed to main via PR only
```

**Your workflow:**
```bash
# 1. Edit source (root level, WITHOUT /CANONICAL)
vim .sdd-core/mandate.spec
vim .sdd-core/guidelines.dsl

# 2. Commit via PR (ADR-008 compliance!)
git checkout -b wip/update-mandate-X
git add .sdd-core/
git commit -m "feat: Update mandate/guideline"
git push origin wip/update-mandate-X
# → Create PR → Architect reviews → Architect merges
```

---

### 2️⃣ TEMPLATE SCAFFOLD - Pre-Built Files

```
.sdd-template/                      (Parte do SDD-ARCHITECTURE)
├── base/                           (Arquivos copiados para .sdd/ no produto)
│   ├── README-SDD.md               (Guia de setup para cliente)
│   ├── metadata-template.json      (Template de metadata com placeholders)
│   ├── .github/workflows/
│   │   └── sdd-validation.yml      (GitHub Actions workflow)
│   └── examples/                   (Exemplos de código seguindo mandates)
│
├── profiles/                       (Templates específicos de profile - v3.2+)
│   ├── ultra-lite/
│   ├── lite/
│   └── full/
│
└── languages/                      (Scaffolds específicos de linguagem)
    ├── java/
    ├── python/
    └── js/
```

**Propósito de .sdd-template/:**
- Arquivos pré-prontos para mover para `.sdd/` final
- Wizard lê daqui + `.sdd-runtime/` + `.sdd-core/`
- Scaffold **pertence a sdd-architecture** (você gerencia)
- Não modificado em runtime
- Cached para gerar templates rápido

---

### 3️⃣ COMPILED OUTPUT - Auto-Generated

```
.sdd-runtime/                       (Auto-gerado, never commit)
├── mandate.bin                     
│   ├─ Origin: Compiled from .sdd-core/mandate.spec
│   ├─ Format: MessagePack binary
│   ├─ Size: ~5-10 KB
│   ├─ Usage: Wizard reads (fast load)
│   └─ Lifecycle: Regenerated on source change
│
├── guidelines.bin                  
│   ├─ Origin: Compiled from .sdd-core/guidelines.dsl
│   ├─ Format: MessagePack binary
│   ├─ Size: ~20-30 KB
│   ├─ Usage: Wizard reads (fast load)
│   └─ Lifecycle: Regenerated on source change
│
└── metadata.json                   
    ├─ Version: "3.0"
    ├─ Tier: "lite" (or "pro", "enterprise" in future)
    ├─ Format: "spec-v1"
    ├─ Compiled-at: timestamp
    └─ Source-hash: SHA256 of source files
```

**Auto-generation via CI/CD:**
```bash
# On commit to .sdd-core/
python .sdd-compiler/src/compile.py \
  --mandate .sdd-core/mandate.spec \
  --guidelines .sdd-core/guidelines.dsl \
  --output .sdd-runtime/
# Result: .bin files + metadata.json updated
```

---

### 4️⃣ CLIENT TEMPLATE FINAL - Delivery Point

```
my-project/                         (Que cliente recebe do Wizard)
├── .sdd/                           (Ponto final de entrega)
│   ├── CANONICAL/
│   │   ├── mandate.spec           (subset: selecionado pelo user, compilado)
│   │   └── guidelines.dsl         (subset: específico da linguagem)
│   ├── metadata.json              (timestamp, audit trail)
│   ├── examples/                  (Exemplos de código seguindo mandates)
│   └── README-SDD.md              (Orientações ao usuário)
│
├── .sdd-guidelines/               (OBRIGATÓRIO - sempre incluído)
│   ├── README.md                  (visão geral de guidelines)
│   ├── general.md                 (boas práticas gerais)
│   ├── git.md                     (workflow de git)
│   ├── testing.md                 (estratégias de teste)
│   ├── naming.md                  (convenções de nome)
│   ├── docs.md                    (padrões de documentação)
│   ├── performance.md             (guidelines de performance)
│   └── style.md                   (estilo de código)
│
├── src/                           (Estrutura específica da linguagem)
├── [arquivos de build]            (pom.xml, requirements.txt, package.json)
├── .github/workflows/             (CI/CD com SDD validation)
└── README.md                      (README do projeto)
```

**Client Delivery Contains:**
- `.sdd/` = Especificações compiladas (imutável, read-only)
- `.sdd-guidelines/` = **OBRIGATÓRIO** (sempre incluído, organizado por tópico)
- `.sdd/examples/` = Exemplos de código seguindo mandates
- `.github/workflows/` = SDD validation em CI/CD
- NO `.sdd-core/` (apenas source, localização do arquiteto)
- NO `.sdd-runtime/` (artefato intermediário, não shipped)
- NO `.sdd-template/` (build time only)

---

## 🔄 Complete Workflow Example

**Scenario:** You update M001 → User generates Java template

### Step 1: You Edit Source
```bash
cd /sdd-architecture
# Edit directly in .sdd-core/ (sem subdirectories, sem /CANONICAL)
vim .sdd-core/mandate.spec
# Update M001: Clean Architecture description

# Commit via PR (ADR-008!)
git checkout -b wip/update-m001
git add .sdd-core/mandate.spec
git commit -m "docs: Clarify M001 Clean Architecture"
git push origin wip/update-m001
# → Create PR on GitHub
# → Architect reviews
# → Architect merges to main
```

### Step 2: CI/CD Compiles (Automatic)
```bash
# On merge to main, CI/CD pipeline:
python .sdd-compiler/src/compile.py \
  --mandate .sdd-core/mandate.spec \
  --guidelines .sdd-core/guidelines.dsl \
  --output .sdd-runtime/
# Result: .sdd-runtime/mandate.bin updated with your changes
```

### Step 3: User Runs Wizard
```bash
$ python .sdd-extensions/wizard.py

? Choose language: [1] Java [2] Python [3] JS
> 1

? Choose mandates:
  [✓] M001: Clean Architecture (sua versão atualizada!)
  [ ] M002: Test-Driven Development
> Select M001

? Choose profile: [1] ULTRA-LITE [2] LITE [3] FULL
> 2

? Output destination: /tmp/my-java-project
[INFO] Reading .sdd-runtime/mandate.bin (suas mudanças!)
[INFO] Reading .sdd-runtime/guidelines.bin
[INFO] Loading .sdd-template/base
[INFO] Filtering guidelines for Java profile...
[INFO] Creating .sdd/ with compiled specs...
[INFO] Creating .sdd-guidelines/ organized by topic...
[INFO] Copying CI/CD workflow from .sdd-template/
[SUCCESS] Template ready: /tmp/my-java-project/
```

### Step 4: Client Uses Project
```bash
cd /tmp/my-java-project

# Read your updated mandates (in .sdd/)
cat .sdd/CANONICAL/mandate.spec

# Review guidelines organized by topic
cat .sdd-guidelines/git.md

# Follow SDD setup guide
cat README-SDD.md

# Run tests with SDD validation
mvn clean test
```

---

## 🗂️ Path Summary (SIMPLIFIED)

| Purpose | Path | Who | When | Format |
|---------|------|-----|------|--------|
| **SOURCE** | `.sdd-core/` | Architect edits | Via PR | `.spec`, `.dsl` |
| **SCAFFOLD** | `.sdd-template/` | Part of tool | Managed | `.md`, `.json`, `.yml` |
| **COMPILED** | `.sdd-runtime/` | CI/CD generates | On commit | `.bin`, `.json` |
| **FINAL** | `.sdd/` | Client receives | from sdd_wizard | `.spec`, `.json`, `.md` |
| **GUIDELINES** | `.sdd-guidelines/` | Client reads | In template | `.md` files |

**Key Changes from v2.1:**
1. ✅ Paths simplified (NO `/CANONICAL` in source)
2. ✅ `.sdd-template/` separates scaffold from runtime
3. ✅ `.sdd/` is the clean delivery point (client receives)
4. ✅ Binary compilation (50%+ smaller, 3-5x faster)
5. ✅ ADR-008 enforced (PR-only workflow)
6. ✅ 100% auditability (metadata.json)

---

## 📋 Implementation Checklist

- [x] v2.1 migration complete (extract → validate → cutover)
- [x] v3.0 tag created
- [x] `.sdd-core/mandate.spec` + `.guidelines.dsl` source live
- [x] `.sdd-template/` scaffold created with base files
- [x] Compiler paths updated to use `.sdd-core/` (no /CANONICAL)
- [x] Architecture documented (this file)
- [ ] Phase 6A: `.sdd-runtime/` CI/CD integration
- [ ] Phase 6B: Wizard integration with template
- [ ] Phase 6C: GitHub branch protection (ADR-008)
- [ ] Phase 6D: Client template generation test
