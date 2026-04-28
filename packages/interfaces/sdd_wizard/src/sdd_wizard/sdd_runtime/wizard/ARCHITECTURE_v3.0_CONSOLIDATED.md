# SDD v3.0: Consolidated Architecture Guide

**Documento Consolidado: Entendimento Completo SDD v3.0**  
**Data:** April 22, 2026 | **Versão:** 3.0-architecture-v1  
**Propósito:** Guia de referência completo para WIZARD e implementação  
**Status:** Ready for implementation

---

## 📋 Table of Contents

1. **Executive Summary**
2. **6 Business Rules (Maturadas)**
3. **Paths Clarification (WIZARD → AGENT → RUNTIME)**
4. **2-Phase Flow End-to-End**
5. **4-Phase Implementation Plan**
6. **CORE vs CLIENT Separation**
7. **Success Criteria & Checklist**

---

## 🎯 Executive Summary

### Problem
- Wizard espera entrada única, mas temos múltiplos arquivos de governança
- Sem automação clara: copy-paste, links quebrados, inconsistência
- Precisa separar CORE (imutável) de CLIENT (customizável)

### Solution
**2-Phase Pipeline Architecture com separação por arquivo:**

1. **WIZARD Phase:** Consolida múltiplos arquivos → gera 2 outputs (CORE + CLIENT)
2. **CLIENT Phase:** Agent carrega CORE (read-only) + customiza CLIENT (writable)
3. **RUNTIME Phase:** Agent executa sob governance final (CORE + CLIENT merged)

### Key Features
✅ Entrada única consolidada (governance-consolidated-3.0.json)  
✅ Saída separada: 2 arquivos físicos (CORE + CLIENT)  
✅ Fingerprinting com salt (core travado + client derivado)  
✅ User selections declarativas (customizable flags)  
✅ Idempotente + rastreável  

---

## 📐 6 Business Rules (Maturadas)

### Regra 1: Pipeline de 4 Níveis de Criticidade

```
NÍVEL 1: CORE_IMMUTABLE
  - Constitution (15 princípios)
  - Customizable: ❌ NUNCA
  - User action: Ver/entender apenas
  
NÍVEL 2: STRUCTURAL
  - ADRs (decisões arquiteturais)
  - Customizable: ❌ NUNCA (referência)
  - User action: Estudar rationale apenas
  
NÍVEL 3: BEHAVIORAL
  - Rules (16 obrigatórias)
  - Guardrails (proteções user-defined)
  - Customizable: ✅ SIM (user marca)
  - User action: Selecionar criticidade (OBRIGATÓRIO/ALERTA/OPCIONAL)
  
NÍVEL 4: CUSTOMIZABLE
  - Guidelines (convenções, padrões)
  - Customizable: ✅ SIM (user marca)
  - User action: Selecionar alternativas (language, naming, etc)
```

**Princípio:** Nível 1-2 são SEMPRE CORE (não customizáveis). Nível 3-4 dependem da marcação user.

---

### Regra 2: Customizable Flags (User Marcação)

**No WIZARD, user marca cada item (Nível 3-4):**

```yaml
Tipo A: NÃO CUSTOMIZÁVEL (→ CORE - immutable)
  - testing_required: User marca NÃO-custom
  - backup_deploy: User marca NÃO-custom
  - naming_convention: User marca NÃO-custom
  
Tipo B: CUSTOMIZÁVEL (→ CLIENT - editable)
  - commit_logging: User marca CUSTOMIZABLE
  - slack_notify: User marca CUSTOMIZABLE
  - language_convention: User marca CUSTOMIZABLE
```

**Regra de Ouro:** O que user SELECIONA + marca NÃO-CUSTOMIZABLE vira CORE. Resto vira CLIENT.

---

### Regra 3: Criticidade de Guardrails (User-Defined)

User escolhe para cada guardrail:

```
OBRIGATÓRIO  → Bloqueia fluxo se falhar (hard constraint)
ALERTA       → Aviso mas prossegue (soft constraint)
OPCIONAL     → Pode desabilitar (nice-to-have)
```

Exemplo:
- "Backup before deploy" = OBRIGATÓRIO (crítico)
- "Commit logging" = ALERTA (importante mas flexível)
- "Slack notification" = OPCIONAL (nice-to-have)

---

### Regra 4: Fingerprinting com Salt (2-Layer)

```
LAYER 1 (CORE):
  fingerprintpackages = SHA-256(core_data)
  - Calculado no WIZARD
  - Travado no client (read-only)
  - Nunca recalcula
  
LAYER 2 (CLIENT):
  fingerprint_client = SHA-256(fingerprintpackages + client_data)
  - fingerprintpackages atua como SALT
  - Calculado no CLIENT (local)
  - Recalcula quando user customiza
```

Benefício:
- ✅ Simples (uma linha de hash)
- ✅ Seguro (client antigo invalida se core muda)
- ✅ Rastreável (sabe exatamente o que mudou)
- ✅ Idempotente (mesmos dados = mesmo hash)

---

### Regra 5: Imutabilidade em Compilação

```
WIZARD Compile:
  - Gera: governance-core.compiled.msgpack (READONLY)
  - Gera: governance-client-template.compiled.msgpack (WRITABLE)
  - Ambos armazenados em .sdd-compiled/
  - Ambos distribuídos para agent
  
CLIENT Compile (Local - Agent):
  - Carrega CORE (nunca toca)
  - Copia CLIENT template → .sdd-runtime/working/
  - USER CUSTOMIZA apenas CLIENT (se quiser)
  - Local compiler recalcula fingerprints
  - Armazena em .sdd-runtime/working/
```

**Regra:** Uma vez compilado, é freeze-point (imutável até próximo compile).

---

### Regra 6: Rastreabilidade Completa

Cada item DEVE ter:
- `id`: Identificador único
- `source`: Arquivo de origem (.spec, ADR-*.md, rules.md, guidelines.dsl)
- `customizable`: Boolean (user marked)
- `priority`: Nível de criticidade (1-4)

---

## 📍 Paths Clarification (Complete)

### WIZARD Production Paths

```
.sdd-core/                           (SOURCE - read-only)
├── mandate.spec
├── guidelines.dsl
└── CANONICAL/
    ├── decisions/ADR-*.md
    ├── rules/rules.md
    └── guardrails/custom-*.yaml

.sdd-compiler/                       (COMPILER module)
└── compiler.py

.sdd-compiled/                       (WIZARD OUTPUT - for distribution)
├── governance-core.compiled.msgpack
├── governance-client-template.compiled.msgpack
├── metadata-core.json
└── metadata-client-template.json
```

### AGENT Runtime Paths (WHERE AGENTS EXECUTE)

```
.sdd-runtime/                        ← AGENTES USAM AQUI
│
├── compiled/                        (Read-only reference from .sdd-compiled/)
│   ├── governance-core.compiled.msgpack
│   ├── governance-client-template.compiled.msgpack
│   ├── metadata-core.json
│   └── metadata-client-template.json
│
├── working/                         (Agent customizations - writable)
│   ├── governance-client.compiled.msgpack (customized version)
│   ├── metadata-client.json (updated fingerprints)
│   └── config.json (agent-specific settings)
│
├── audit/                           (Compliance tracking - writable)
│   ├── compliance-report.json
│   ├── audit-YYYY-MM-DD.log
│   └── violations.log
│
└── checkpoint/                      (Task state preservation)
    ├── task-001.checkpoint
    └── .checkpoint-index.json
```

### Data Flow (File Movement)

```
WIZARD PHASE:
  .sdd-core/ files
    ↓ pipeline_builder.py
  governance-consolidated-3.0.json (temp)
    ↓ compiler.py
  GENERATES:
    → governance-core.compiled.msgpack
    → governance-client-template.compiled.msgpack
    → metadata files
    ↓
  .sdd-compiled/ (DELIVERABLE)

AGENT SETUP:
  .sdd-compiled/ (from sdd_wizard)
    ↓ client_initializer.py
  COPIES:
    .sdd-compiled/ → .sdd-runtime/compiled/ (readonly)
    governance-client-template → .sdd-runtime/working/ (writable)

AGENT EXECUTION:
  .sdd-runtime/compiled/ (CORE - immutable)
  + .sdd-runtime/working/ (CLIENT - customized)
    ↓ governance_engine.py
  = Governance FINAL
    ↓ validates action
    ↓ logs to .sdd-runtime/audit/
    ↓ saves checkpoint to .sdd-runtime/checkpoint/
```

---

## 🔄 2-Phase Flow (End-to-End)

### PHASE 1: WIZARD (Selection + Compilation)

**Input:** User interaction + .sdd-core/

```
Step 1: Wizard lê governance-consolidated-3.0.json
        (gerado por pipeline_builder.py em fase anterior)

Step 2: Apresenta 4 níveis ao user:
        - Nível 1-2: Pre-selecionados (não customizáveis)
        - Nível 3-4: User marca cada item (customizable?)
        
Step 3: User customiza guardrails:
        - Seleciona criticidade (OBRIGATÓRIO/ALERTA/OPCIONAL)
        - Define que pode customizar (ou não)
        
Step 4: User revisa seleção + confirma

Step 5: Compiler recebe consolidado + selections:
        - Separa CORE (seleções NÃO-customizable)
        - Separa CLIENT (seleções CUSTOMIZABLE)
        - Calcula fingerprints (core + client com salt)
        
Step 6: Deploy em .sdd-compiled/:
        - governance-core.compiled.msgpack (immutable)
        - governance-client-template.compiled.msgpack (template)
        - metadata-core.json
        - metadata-client-template.json

Output: .sdd-compiled/ (ready for client workspace)
```

### PHASE 2: CLIENT (Customization + Execution)

**Input:** .sdd-compiled/ (TWO FILES from sdd_wizard)

```
Step 1: Agent copies .sdd-compiled/ → .sdd-runtime/compiled/
        - Cria estrutura local para runtime
        
Step 2: Client initialization:
        - Verifica fingerprintpackages (valida integridade)
        - Carrega CORE como READ-ONLY reference (user nunca toca)
        - Copia CLIENT template → .sdd-runtime/working/
        
Step 3: User/Agent customiza (optional, APENAS items em CLIENT):
        ✅ PODE: Mudar criticidade (OBRIGATÓRIO → ALERTA)
        ✅ PODE: Selecionar conventions
        ❌ NÃO PODE: Tocar em items do CORE (locked)
        
Step 4: Local compiler (durante customização):
        - Recompila CLIENT com customizações user
        - Recalcula fingerprint_client = SHA-256(salt + custom_data)
        - Armazena em .sdd-runtime/working/
        
Step 5: Validation:
        - Verifica CORE não foi tocado (fingerprintpackages estável)
        - Verifica CLIENT customizations OK (fingerprint_client recalculado)
        - Detecta divergências via fingerprints
        
Step 6: Runtime:
        - CORE (from .sdd-runtime/compiled/) = IMUTÁVEL
        - CLIENT (from .sdd-runtime/working/) = CUSTOMIZADO
        - Governance FINAL = CORE + CLIENT combined
        - Agent executa sob governance final
        - Audit logs em .sdd-runtime/audit/
        - Task checkpoints em .sdd-runtime/checkpoint/

Output: Governança aplicada em .sdd-runtime/
```

---

## 🔧 4-Phase Implementation Plan

### PHASE 1: Pipeline Implementation (Est. 1-2 dias)

**Goal:** Consolidar múltiplos arquivos → governance-consolidated-3.0.json

**Module:** `.sdd-core/pipeline_builder.py`

```python
class PipelineBuilder:
    def load_sources(self):
        # Carrega:
        # - mandate.spec (Nível 1 + Nível 4)
        # - guidelines.dsl (Nível 4)
        # - ADRs (Nível 2)
        # - rules.md (Nível 3)
        # - guardrails/*.yaml (Nível 3)
        
    def organize_by_level(self):
        # Ordena por 4 níveis de criticidade
        
    def consolidate(self):
        # Mescla em estrutura única
        
    def calculate_fingerprint(self):
        # SHA-256 de todo o consolidado
        
    def save(self):
        # Salva em governance-consolidated-3.0.json
```

**Deliverables:**
- ✅ `.sdd-core/pipeline_builder.py`
- ✅ `governance-consolidated-3.0.json` (intermediário, descartável)
- ✅ 4 níveis presentes + fingerprint

**Tests:**
- [ ] File exists e válido JSON
- [ ] 4 níveis presentes
- [ ] Fingerprint calculado corretamente

---

### PHASE 2: Compiler Refactoring (Est. 1-2 dias)

**Goal:** Compiler gera 2 arquivos (CORE + CLIENT) baseado em seleções

**Module:** `.sdd-compiler/compiler.py` (refactored)

```python
class GovernanceCompiler:
    def __init__(self, consolidated_file: str):
        self.consolidated = load_json(consolidated_file)
        
    def set_user_selections(self, selections: Dict):
        # Recebe customizable flags por item
        
    def compile(self) -> Dict:
        # Separa CORE (não-customizable)
        # Separa CLIENT (customizable)
        # Calcula fingerprints
        
    def _separate_by_customizable(self):
        # CORE recebe: Nível 1-2 + items marcados NÃO-custom
        # CLIENT recebe: items marcados CUSTOMIZABLE
        
    def _calculate_fingerprintpackages(self):
        # SHA-256(core_data)
        
    def _calculate_fingerprint_client(self):
        # SHA-256(fingerprintpackages + client_data)  [SALT]
        
    def save_outputs(self):
        # Salva em .sdd-compiled/:
        # - governance-core.compiled.msgpack
        # - governance-client-template.compiled.msgpack
        # - metadata files
```

**Deliverables:**
- ✅ 2 arquivos msgpack (CORE + CLIENT)
- ✅ Metadata files (readonly flags, fingerprints)
- ✅ Em .sdd-compiled/ (ready for distribution)

**Tests:**
- [ ] 2 arquivos gerados
- [ ] CORE readonly (metadata)
- [ ] CLIENT writable (metadata)
- [ ] Fingerprints diferentes
- [ ] Salt strategy correto

---

### PHASE 3: Tests + Validation (Est. 1 dia)

**Goal:** Verificar idempotência, integridade, fingerprinting

**Tests:**
```python
test_pipeline_idempotent()
    # Running pipeline 2x = same fingerprint

test_compiler_generates_two_files()
    # CORE and CLIENT generated

test_fingerprintpackages_stable()
    # CORE fingerprint doesn't change

test_fingerprint_client_with_salt()
    # CLIENT fingerprint derived correctly using core as salt

test_selections_respected()
    # Customizable flags honored correctly

test_end_to_end()
    # .sdd-core → consolidated → compiled → 2 files
```

**Success:** All tests passing (5/5+)

---

### PHASE 4: Deploy + Documentation (Est. 0.5-1 dia)

**Goal:** Finalizar, documentar, deploy

**Checklist:**
```bash
[ ] governance-consolidated-3.0.json exists
[ ] .sdd-compiled/governance-core.compiled.msgpack exists
[ ] .sdd-compiled/governance-client-template.compiled.msgpack exists
[ ] Metadata files present + correct
[ ] All tests passing (5/5+)
[ ] Git working tree clean
[ ] No broken links/references
[ ] README updated
[ ] CHANGELOG updated
```

**Deliverables:**
- ✅ Git commit + tag (v3.0-pipeline-compiler-complete)
- ✅ Ready for PHASE 5 (Wizard integration)

---

## 🔐 CORE vs CLIENT Separation (Critical)

### Visual: What Goes Where

```
WIZARD USER SELECTION:
┌────────────────────────────────────┬──────────────┬──────────┐
│ Item                               │ Custom?      │ Destino  │
├────────────────────────────────────┼──────────────┼──────────┤
│ Constitution (15 princ.)           │ NÃO (obrig)  │ CORE     │
│ ADR-007-microservices              │ NÃO (obrig)  │ CORE     │
│ ADR-008-async-messaging            │ NÃO (obrig)  │ CORE     │
│ testing_required (Rule)            │ NÃO (user)   │ CORE     │
│ commit_logging (Rule)              │ SIM (user)   │ CLIENT   │
│ backup_deploy (Guardrail)          │ NÃO (user)   │ CORE     │
│ slack_notify (Guardrail)           │ SIM (user)   │ CLIENT   │
│ naming_convention (Guideline)      │ SIM (user)   │ CLIENT   │
└────────────────────────────────────┴──────────────┴──────────┘

RESULT ON DISK:

CORE FILE (governance-core.compiled.msgpack)
├── Constitution
├── ADR-007
├── ADR-008
├── testing_required
└── backup_deploy
Metadata: readonly=true, fingerprintpackages=SHA256(...)

CLIENT FILE (governance-client-template.compiled.msgpack)
├── commit_logging
├── slack_notify
└── naming_convention
Metadata: readonly=false, fingerprintpackages_salt=..., fingerprint_client=SHA256(...)
```

### Runtime: What Agent Can Do

```
PHASE 2 - AGENT CUSTOMIZATION:

✅ PODE fazer (em CLIENT):
  - commit_logging: ALERTA → OBRIGATÓRIO
  - slack_notify: OPCIONAL → ALERTA
  - naming_convention: en_US → pt_BR
  
❌ NÃO PODE fazer (em CORE - locked):
  - testing_required: mudar criticidade
  - backup_deploy: mudar criticidade
  - Constitution: mexer em qualquer princípio
  - ADRs: mexer em qualquer decisão
```

---

## ✅ Success Criteria & Checklist

### Technical Success Criteria

- ✅ Pipeline cria consolidado (1 arquivo intermediário)
- ✅ Compiler gera 2 arquivos (CORE + CLIENT)
- ✅ Fingerprints calculados (core stable + client com salt)
- ✅ User selections respected (customizable flags honored)
- ✅ Idempotência verificada (mesma entrada = mesmo output)
- ✅ Tests passing 100% (5+)
- ✅ Code committed + tagged
- ✅ Zero broken links/references

### Business Success Criteria

- ✅ CORE é 100% imutável (read-only no client)
- ✅ CLIENT é customizável apenas em items permitidos
- ✅ Fingerprinting detecta mudanças (sem bloquear)
- ✅ Fluxo 2-fases claro (WIZARD → CLIENT)
- ✅ Rastreabilidade completa (origem de cada item)

### Pre-Implementation Checklist

```bash
[ ] Architecture understood (este documento)
[ ] Paths clarificados (.sdd-core, .sdd-compiled, .sdd-runtime)
[ ] CORE vs CLIENT separation claro (2 arquivos físicos)
[ ] 2-Phase flow claro (WIZARD → CLIENT)
[ ] Business rules validadas (6 rules)
[ ] 4-Phase implementation plan approved
[ ] Development environment ready
[ ] Git repository clean
```

---

## 🚀 Next Steps

1. **Validar este documento** (toda equipe)
   - Paths fazem sentido?
   - Fluxo está claro?
   - Business rules aprovadas?

2. **Kickoff PHASE 1** (Pipeline)
   - Criar `.sdd-core/pipeline_builder.py`
   - Testar consolidação
   - Entregar `governance-consolidated-3.0.json`

3. **Kickoff PHASE 2** (Compiler)
   - Refactor `.sdd-compiler/compiler.py`
   - 2-file output (CORE + CLIENT)
   - Fingerprinting com salt

4. **Kickoff PHASE 3** (Tests)
   - 5+ integration tests
   - Idempotence verification
   - 2-file separation validation

5. **Kickoff PHASE 4** (Deploy)
   - Final checklist
   - Git commit + tag
   - Announce ready

---

## 📝 Document Control

| Version | Date | Status | Path |
|---------|------|--------|------|
| 1.0 | Apr 22, 2026 | Ready | `.sdd-runtime/wizard/ARCHITECTURE_v3.0_CONSOLIDATED.md` |

**Purpose:** Single source of truth for SDD v3.0 implementation  
**Audience:** Architects, engineers, AI agents  
**Access:** Read-only (reference), committed to git

---

## 🔗 Related Documents

- `.sdd-core/pipeline_builder.py` (Phase 1 implementation)
- `.sdd-compiler/compiler.py` (Phase 2 implementation)
- `.sdd-runtime/` (Agent execution base)
- `.sdd-compiled/` (Wizard output)

---

**Status:** ✅ Ready for Phase 1 Implementation
