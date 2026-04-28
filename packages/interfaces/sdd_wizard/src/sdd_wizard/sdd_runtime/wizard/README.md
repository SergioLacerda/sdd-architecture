# SDD v3.0 Wizard Reference

**Diretório:** `.sdd-runtime/wizard/`  
**Propósito:** Documentação consolidada de referência para SDD v3.0 implementation  
**Status:** Ready for Phase 1

---

## � VERSION ALERT: Use v3.0-MATURED_ARCHITECTURE.md

⚠️ **IMPORTANT:** Two versions of architecture documentation exist:

| Document | Version | Use Case | Status |
|----------|---------|----------|--------|
| **v3.0-MATURED_ARCHITECTURE.md** | **CURRENT** | **Implement from THIS** | ✅ Active |
| ARCHITECTURE_v3.0_CONSOLIDATED.md | Deprecated | Historical reference | ⚠️ Outdated |

**Why two versions?**
- v3.0-consolidated: Initial planning (file-level security, 4 levels)
- v3.0-matured: Evolved understanding (hash-level audit, 3 layers, single compiled)

**See Evolution Section:** In v3.0-MATURED_ARCHITECTURE.md → "Evolution Note"

## 📄 Documentos Disponíveis

### 1. ARCHITECTURE_v3.0_CONSOLIDATED.md (PRINCIPAL ✅)
```
Arquivo: .sdd-runtime/wizard/ARCHITECTURE_v3.0_CONSOLIDATED.md
Status: CURRENT (nível anterior combinado)

Conteúdo:
  ✅ Executive Summary
  ✅ 6 Business Rules (maturadas)
  ✅ 2-Phase Flow (WIZARD → CLIENT)
  ✅ 2 Files (CORE + CLIENT)
  ✅ Fingerprinting com Salt Strategy
  ✅ Paths Clarification
  ✅ 4-Phase Implementation Plan
```

**Uso:** PRINCIPAL. Use este para Phase 1. Este é o entendimento combinado.

---

## 🔍 Quick Navigation

### Por Seção:

**Se precisa entender:**
- Architecture geral → Seção "2-Phase Flow"
- Onde os arquivos vivem → Seção "Paths Clarification"
- Como separar CORE/CLIENT → Seção "CORE vs CLIENT Separation"
- O que fazer em cada fase → Seção "4-Phase Implementation Plan"
- Se tudo tá pronto → Seção "Success Criteria & Checklist"

### Por Pessoa:

**Architects:**
- Leia: Executive Summary + 6 Business Rules + 2-Phase Flow
- Décida: Este entendimento está aprovado?

**Engineers (Phase 1):**
- Leia: Paths Clarification + "PHASE 1: Pipeline" em Implementation Plan
- Faça: Criar `.sdd-core/pipeline_builder.py`

**Engineers (Phase 2):**
- Leia: CORE vs CLIENT Separation + "PHASE 2: Compiler" em Implementation Plan
- Faça: Refactor `.sdd-compiler/compiler.py`

**Agents (Runtime):**
- Leia: Paths Clarification + "PHASE 2: CLIENT" em 2-Phase Flow
- Use: `.sdd-runtime/` como base para execução

---

## 🚀 Implementation Phases (from v3.0-CONSOLIDATED.md)

### Phase 1: Pipeline (1-2 dias)
**What:** Consolidar múltiplos arquivos em 1 JSON intermediário  
**Where:** `.sdd-core/pipeline_builder.py`  
**Output:** `governance-consolidated-3.0.json`  
**Ref:** ARCHITECTURE_v3.0_CONSOLIDATED.md → "PHASE 1"

### Phase 2: Compiler (1-2 dias)
**What:** Gerar 2 arquivos separados (CORE + CLIENT)  
**Where:** `.sdd-compiler/compiler.py`  
**Output:** `.sdd-compiled/` (2 msgpack files)  
**Ref:** ARCHITECTURE_v3.0_CONSOLIDATED.md → "PHASE 2"

### Phase 3: Tests (1 dia)
**What:** Validar idempotência, integridade, fingerprinting  
**Where:** `tests/test_*.py`  
**Tests:** 5+ integration tests  
**Ref:** ARCHITECTURE_v3.0_CONSOLIDATED.md → "PHASE 3"

### Phase 4: Deploy (0.5-1 dia)
**What:** Git commit + tag + ready for Phase 5  
**Checklist:** ARCHITECTURE_v3.0_CONSOLIDATED.md → "PHASE 4 Checklist"  
**Output:** Git tag `v3.0-pipeline-compiler-complete`

---

## � Directory Structure (from v3.0-MATURED_ARCHITECTURE.md)

**On SDD-ARCHITECTURE (Wizard Source):**
```
.sdd-core/
├── CANONICAL/mandates.spec
├── CANONICAL/decisions/ADR-*.md
├── CANONICAL/rules/
└── pipeline_builder.py

.sdd-compiler/
└── compiler.py
```

**On Client (After Wizard Deployment):**
```
PROJECT_ROOT/
└── .sdd/                          ← CENTRALIZED
    ├── .sdd-core/
    │   ├── mandates.spec
    │   └── compiled.msgpack       ← FINAL COMPILED
    ├── .sdd-guidelines/
    │   └── guidelines.dsl
    ├── .sdd-metadata.json         ← HASH DETECTOR
    └── .sdd-operations/
        ├── cache/
        ├── checkpoints/
        ├── audit/
        └── state/
```

**Patterns Supported:**
- IDE: `.sdd/` in workspace root, symlinks in projects
- Isolated: `.sdd/` in project root

See v3.0-MATURED_ARCHITECTURE.md → "Directory Structure" for detailed explanation.

---

## ✅ Pre-Implementation Checklist

```bash
[ ] Abrir e ler: ARCHITECTURE_v3.0_CONSOLIDATED.md
[ ] Validar: Executive Summary + 6 Business Rules
[ ] Validar: Paths Clarification (tudo faz sentido?)
[ ] Validar: CORE vs CLIENT Separation (2 arquivos, salt strategy)
[ ] Validar: 2-Phase Flow (wizard → client flow claro?)
[ ] Validar: 4-Phase Implementation Plan (fases sequenciadas?)
[ ] Decisão: Tudo aprovado? SIM → Começar PHASE 1 ✅
```

---

## 🔗 How to Use These Documents

### For Reading:
```bash
# PRINCIPAL:
cat ARCHITECTURE_v3.0_CONSOLIDATED.md

# Ou no editor:
code ARCHITECTURE_v3.0_CONSOLIDATED.md
```

### For Reference During Implementation:
```bash
# Keep this open in VS Code during development
# Use Ctrl+F to search for specific section:
# - "PHASE 1" for pipeline work
# - "PHASE 2" for compiler work
# - "CORE vs CLIENT" for separation logic
# - "Success Criteria" for acceptance tests
```

---

## 🆘 Troubleshooting Reference

**Q: Não entendi a separação CORE vs CLIENT**  
A: Seção "CORE vs CLIENT Separation" → Visual "What Goes Where"

**Q: Não entendo qual é o path de runtime para agents**  
A: Seção "Paths Clarification" → "AGENT Runtime Paths"

**Q: Qual é a diferença entre .sdd-compiled e .sdd-runtime?**  
A: Seção "Paths Clarification" → "Data Flow (File Movement)"

**Q: Como funciona o fingerprinting com salt?**  
A: Seção "6 Business Rules" → "Regra 4: Fingerprinting com Salt"

**Q: Qual é o checklist para Phase 1?**  
A: Seção "4-Phase Implementation Plan" → "PHASE 1: Deliverables"

---

## 📊 Document Versions at a Glance

| File | Purpose | Status |
|------|---------|--------|
| **ARCHITECTURE_v3.0_CONSOLIDATED.md** | Principal reference | ✅ Current |
| QUICK_REFERENCE.md | Fast Q&A | ✅ Useful |
| README.md (this file) | Navigation | ✅ Current |

---

## 🎯 Next Action

1. **Abrir:** `ARCHITECTURE_v3.0_CONSOLIDATED.md`
   
2. **Validar (30 min):**
   - Executive Summary: problema → solução clear?
   - 6 Business Rules: fazem sentido?
   - 2 Files (CORE + CLIENT): diferença clara?
   - Salt strategy: como core fingerprint vira salt para client?
   - Paths: WIZARD → .sdd-compiled → AGENT → .sdd-runtime?

3. **Aprovar:**
   - Tudo OK? → Começar PHASE 1 ✅
   - Ajustes? → Que mudar?

---

**Status: ✅ Ready for Phase 1 Implementation (v3.0-consolidated)**
