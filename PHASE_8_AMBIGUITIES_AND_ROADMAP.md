# Phase 8: Sinalizando Ambiguidades e Roadmap de Implementação

**Data:** April 21, 2026  
**Status:** Review completo + Sinalização de ambiguidades + Roadmap executivo

---

## 🚨 AMBIGUIDADES IDENTIFICADAS

### Ambiguidade #1: "OPERATIONS Layer" - Escopo Não Definido

**Menção no Planejamento:**
```
"nomes de camadas padronizados: MANDATE, GUIDELINES, OPERATIONS"
```

**Status:** ⚠️ AMBÍGUO

**Problema:**
- Não está claro o que exatamente OPERATIONS deve fazer
- Não há especificação de responsabilidades
- Interface não definida
- Relação com RTK + Compilador não documentada

**Hipóteses (precisa confirmação):**
```
Opção A: OPERATIONS = Query Layer
   └─ Busca otimizada em MANDATE + GUIDELINES
   └─ Cache de resultados compilados
   └─ Interface: search(), get(), list()

Opção B: OPERATIONS = Execution/Runtime Layer
   └─ Aplicar mandates durante desenvolvimento
   └─ Hook de linting em IDE
   └─ Relatórios de compliance

Opção C: OPERATIONS = Client State Management
   └─ Gerenciar estado de specializations
   └─ Persist/load de customizations
   └─ Sync de múltiplos projetos

Opção D: Híbrido (A+B+C)
   └─ Tudo acima em coordenação
```

**Recomendação:** ✅ **DECIDIR em v3.2 kickoff qual é o escopo**

---

### Ambiguidade #2: "Fingerprints" + "RTK Overrides" - Implementação Vaga

**Menção no Planejamento:**
```
"Compilador para MANDATE e GUIDELINE, RTK + fingerprints (simplifica overrides)"
```

**Status:** ⚠️ AMBÍGUO

**Problema:**
- RTK patterns funcionam como fingerprints ✅
- Mas "simplifica overrides" não está claro
- Não há implementação de override system
- Fluxo de como overrides são aplicados não documentado

**Hipóteses (precisa confirmação):**
```
Opção A: Override por Pattern
   └─ User override: "UUID patterns → custom regex"
   └─ Salvo em .sdd/custom/overrides.yaml
   └─ Compilador respeita overrides

Opção B: Override por Especialização
   └─ User cria Extension com patterns customizados
   └─ Substitui patterns padrão do RTK
   └─ Plugin loader carrega override

Opção C: Override em OPERATIONS layer
   └─ Runtime: user define exceções
   └─ Não persiste, aplicado em sessão
   └─ Simples mas não duradouro

Opção D: Não há override system formal
   └─ Extensions são a forma de customização
   └─ Não há "override" explícito
```

**Recomendação:** ✅ **DEFINIR sistema de overrides em v3.2**

---

### Ambiguidade #3: "Cliente Autosuficiente" - Como Funciona?

**Menção no Planejamento:**
```
"Wizard unificado. client sera autosuficiente"
```

**Status:** ⚠️ AMBÍGUO

**Problema:**
- "Autosuficiente" significa o quê exatamente?
- Sem servidor? Sem dependências? Sem ID?
- Fluxo de setup não especificado
- Relação com Wizard não clara

**Hipóteses (precisa confirmação):**
```
Opção A: Autossuficiente = Standalone
   └─ Não precisa de servidor central
   └─ Funciona offline
   └─ Cada projeto = instância independente

Opção B: Autossuficiente = Self-configuring
   └─ Wizard detecta e configura automaticamente
   └─ User não precisa fazer setup manual
   └─ Dados de telemetry coletados automaticamente

Opção C: Autossuficiente = Self-healing
   └─ Detecta compliance issues
   └─ Sugere correções
   └─ Aplica fixes automaticamente

Opção D: Híbrido (A+B+C)
```

**Recomendação:** ✅ **ESPECIFICAR em v3.2 design document**

---

### Ambiguidade #4: "Múltiplos Perfis" - Exatos Perfis Não Definidos

**Menção no Planejamento:**
```
"estrutura final do client resolve perfis diferentes(IDE, projeto isolado)"
```

**Status:** ⚠️ PARCIALMENTE DEFINIDO

**Problema:**
- Apenas 2 perfis mencionados (IDE, isolado)
- Terceiro perfil "enterprise/centralizado" não documentado
- Diferenças entre perfis não especificadas
- Como Wizard seleciona perfil não está claro

**Hipóteses (precisa confirmação):**
```
Perfil 1: IDE (mencionado)
   ├─ Real-time linting?
   ├─ Inline warnings?
   ├─ Quick-fix suggestions?
   └─ Plugin do VS Code? IntelliJ? Ambos?

Perfil 2: Projeto Isolado (mencionado)
   ├─ CLI-based?
   ├─ Docker-friendly?
   ├─ Git-friendly?
   └─ Como é disparado?

Perfil 3: Enterprise/Centralizado (implícito)
   ├─ Multi-project sync?
   ├─ Centralized cache?
   ├─ Server-based?
   └─ Billing/licensing?

Como Wizard escolhe?
   └─ User input? Auto-detect? Config file?
```

**Recomendação:** ✅ **DETALHAR cada perfil em v3.2 design**

---

### Ambiguidade #5: "Pacotes" Substituídos por Wizard - Transição Não Clara

**Menção no Planejamento:**
```
"remocao de pacotes(ultra lite, lite, full), sera suprido por wizard"
```

**Status:** ⚠️ AMBÍGUO

**Problema:**
- Conceito de "packages" pré-definidos vs Wizard dinâmico não claro
- Como user escolhe "lite" vs "full" no Wizard?
- Quais features existem em cada nível?
- Downgrade path se escolher errado?

**Hipóteses (precisa confirmação):**
```
Fluxo Antigo (v3.0):
   ├─ User escolhe: ultra-lite, lite, ou full
   ├─ Download package pré-compilado
   ├─ Instala tudo naquele nível

Fluxo Novo (Wizard v3.2):
   ├─ User roda: sdd-wizard --setup
   ├─ Wizard detecta project type
   ├─ Wizard pergunta: "Which features?"
   │  └─ RTK only?
   │  └─ RTK + Compiler?
   │  └─ RTK + Compiler + Extensions?
   ├─ Wizard instala apenas selecionado
   └─ User pode re-rodar wizard para mudar

Nomes dos Níveis em v3.2?
   ├─ Permanecem: ultra-lite, lite, full?
   ├─ Mudam para: minimal, standard, extended?
   ├─ Dinâmicos: user seleciona features?
```

**Recomendação:** ✅ **DETALHAR feature levels em v3.2**

---

### Ambiguidade #6: "Centralizado na Root" - Estrutura Exata Não Fixa

**Menção no Planejamento:**
```
"centralizado estrutura no cliente, pensamos apartir do root simplificando idempotencia"
```

**Status:** ✅ IMPLEMENTADO MAS COM QUESTÕES

**O que está claro:**
- Tudo em .sdd/

**O que não está claro:**
- Quanto do código core fica em .sdd/?
- Onde fica o runtime (agora em .sdd-rtk, .sdd-compiler, .sdd-extensions)?
- Esses diretórios movem para .sdd/ em v3.2?
- Ou permanecem na raiz do projeto?

**Estrutura Atual:**
```
projeto-cliente/
├── .sdd/                  ← Dados do usuário
│   ├── mandate.spec
│   ├── guidelines.dsl
│   └── custom/
├── .sdd-rtk/              ← Core (na raiz, não em .sdd/)
├── .sdd-compiler/         ← Core (na raiz, não em .sdd/)
└── .sdd-extensions/       ← Core (na raiz, não em .sdd/)
```

**Questão:**
```
Em v3.2, estrutura será:
   Opção A: Tudo em .sdd/ (incluindo core)
   Opção B: Core fora de .sdd/, dados em .sdd/ (atual)
   Opção C: Módulos relocáveis (user escolhe)
```

**Recomendação:** ✅ **CONFIRMAR em v3.2 - Não é blocker para v3.1**

---

## 📊 MATRIZ DE AMBIGUIDADES

| Item | Clareza | Blocker? | v3.1? | v3.2? |
|------|---------|----------|-------|-------|
| OPERATIONS layer | 🔴 Vago | Não | ❌ | ✅ |
| Override system | 🔴 Vago | Não | ❌ | ✅ |
| Autossuficiência | 🔴 Vago | Não | ❌ | ✅ |
| Múltiplos perfis | 🟡 Parcial | Não | ✅ Base | ✅ Detalhe |
| Feature levels | 🔴 Vago | Não | ❌ | ✅ |
| Estrutura root | 🟡 Parcial | Não | ✅ OK | ✅ Refine |

---

## ✅ ITENS SEM AMBIGUIDADE (CLAROS)

```
✅ MANDATE
   └─ Bem definido, implementado, testado

✅ GUIDELINES
   └─ Bem definido, implementado, testado

✅ RTK + Fingerprints
   └─ RTK patterns = fingerprints
   └─ Bem implementado (50+ patterns, 31/31 testes)

✅ Compilador
   └─ DSL → MessagePack
   └─ Bem implementado (25/25 testes)

✅ Extension Framework
   └─ Bem definido, production-ready (17/17 testes)

✅ Estrutura Centralizada em .sdd/
   └─ Implementado, funcional, idempotente

✅ v3.1-beta.1 Scope
   └─ RTK + Compiler + Extensions
   └─ Cristalino
```

---

## 🚀 ROADMAP DE IMPLEMENTAÇÃO: v3.1-beta.1 → v3.2

### v3.1-beta.1 (THIS WEEK) ✅
```
✅ FINALIZAR:
   ├─ Documentação das 3 camadas (MANDATE, GUIDELINES, RTK)
   ├─ API Reference para cada módulo
   ├─ Quick Start guide (5 min)
   ├─ Migration guide (v3.0 → v3.1)
   └─ Release notes

✅ EMPACOTAR:
   ├─ .sdd-rtk/ (50+ patterns, engine, tests)
   ├─ .sdd-compiler/ (DSL compiler, msgpack, tests)
   ├─ .sdd-extensions/ (framework, 2 examples, tests)
   └─ Complete documentation

✅ RELEASE:
   └─ v3.1-beta.1 com 111/111 testes
```

### v3.2 (NEXT) - RESOLVA AMBIGUIDADES
```
🔄 DESIGN PHASE:
   ├─ [ ] Define OPERATIONS layer scope
   │      └─ Query? Runtime? State Management?
   │
   ├─ [ ] Define override system
   │      └─ Per-pattern? Per-specialization? Runtime-only?
   │
   ├─ [ ] Define "autossuficiência"
   │      └─ Standalone? Self-configuring? Self-healing?
   │
   ├─ [ ] Define múltiplos perfis
   │      └─ IDE (qual IDE?), Isolado (como?), Enterprise (quais features?)
   │
   ├─ [ ] Define feature levels
   │      └─ ultra-lite, lite, full? Ou custom?
   │
   └─ [ ] Finalize estrutura root
            └─ Tudo em .sdd/? Ou core fora?

🛠️ IMPLEMENTATION PHASE:
   ├─ [ ] SDD Wizard (ProjectDetector, Generator)
   ├─ [ ] OPERATIONS layer
   ├─ [ ] IDE integration (VS Code?)
   ├─ [ ] Override system
   └─ [ ] Profile templates

📊 VALIDATION PHASE:
   ├─ [ ] Real telemetry collection (seus projetos)
   ├─ [ ] Case studies
   ├─ [ ] Performance benchmarks
   └─ [ ] Release v3.2-beta.1
```

---

## 🎯 SÍNTESE PARA DECISÃO

**PERGUNTA CRÍTICA para v3.2 planning:**

1. **OPERATIONS Layer**
   - [ ] Query engine + cache
   - [ ] Execution/linting hooks
   - [ ] Client state management
   - [ ] Híbrido (todas acima)

2. **Override System**
   - [ ] Per-pattern customization
   - [ ] Via Extensions
   - [ ] Runtime-only
   - [ ] Não há (Extensions são suficientes)

3. **Autossuficiência**
   - [ ] Standalone (no server)
   - [ ] Self-configuring (Wizard)
   - [ ] Self-healing (auto-fixes)
   - [ ] Híbrido

4. **Perfis Exatos**
   - [ ] IDE (VS Code?), Isolado, Enterprise
   - [ ] Outros perfis além desses?
   - [ ] Como escolher perfil?

5. **Feature Levels**
   - [ ] Nomes: ultra-lite, lite, full (manter)
   - [ ] Nomes novos?
   - [ ] Dinâmicos (user seleciona)?

6. **Estrutura Root**
   - [ ] Tudo em .sdd/
   - [ ] Core fora, dados em .sdd/
   - [ ] Híbrido (relocável)

---

## 📌 PRÓXIMOS PASSOS IMEDIATOS

### NOW (v3.1-beta.1 - This Week):
1. ✅ Sinalizar ambiguidades (FEITO ✅)
2. ⏳ Finalizar documentação v3.1
3. ⏳ Release v3.1-beta.1 com 111/111 testes

### SOON (v3.2 Planning):
1. 📋 Resolver cada ambiguidade com decisões claras
2. 🛠️ Criar design documents para cada feature
3. 🚀 Implementar com ambiguidades resolvidas

---

## ✨ CONCLUSÃO

**Confiança v3.1-beta.1: 99%** ✅
- Nenhuma ambiguidade bloqueia esta release
- Tudo planejado e implementado

**Itens para v3.2: 6 ambiguidades claras** ⚠️
- Não são problemas, são decisões futuras
- Todas sinalizadas
- Todas resolvíveis

**Recomendação:** 
- ✅ Release v3.1-beta.1 YA
- 📋 Criar decision document para v3.2
- 🚀 Kick-off v3.2 com essas resoluções

---

**Status:** Ready for v3.1-beta.1 implementation + v3.2 planning
