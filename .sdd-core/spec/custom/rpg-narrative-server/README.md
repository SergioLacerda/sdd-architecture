# RPG Narrative Server - Projeto de Demonstração SPEC

**Status:** ✅ Active  
**SPEC Integration:** ✅ Complete (2026-04-19)

---

## 📖 O que é este projeto?

**rpg-narrative-server** é a implementação de demonstração do framework SPEC (Sistema de Princípios e Especificações).

Este projeto showcases:
- ✅ Clean Architecture 8-layer
- ✅ Async-first design (Python FastAPI + asyncio)
- ✅ Ports & Adapters hexagonal architecture
- ✅ Vector search integration (ChromaDB)
- ✅ Event sourcing pattern
- ✅ Thread isolation (AI agent + campaign runtime)
- ✅ Enterprise-grade governance

---

## 🏗️ Stack Técnico

- **Runtime:** Python 3.11/3.12
- **API:** FastAPI + Pydantic
- **Discord:** discord.py bot interface
- **Vector DB:** ChromaDB + HNSW indexing
- **Message Bus:** Blinker (signal/event dispatch)
- **Storage:** PostgreSQL (planned, currently JSON)
- **Testing:** pytest with golden test patterns

---

## 📚 Documentação SPEC

### Globalizada (Compartilhada entre Projetos)

**Todos os projetos herdam 100% de CANONICAL/**
- `/EXECUTION/spec/CANONICAL/rules/` — Regras obrigatórias
- `/EXECUTION/spec/CANONICAL/specifications/` — Arquitetura, testes, definição de done
- `/EXECUTION/spec/CANONICAL/decisions/` — 6 ADRs sobre arquitetura

### Especializada (Específica deste Projeto)

**Documentação de rpg-narrative-server**
- `/EXECUTION/spec/custom/rpg-narrative-server/reality/` — Estado observado do sistema
- `/EXECUTION/spec/custom/rpg-narrative-server/development/` — Trabalho em progresso
- `/EXECUTION/spec/custom/rpg-narrative-server/INTEGRATION_RESULTS.md` — Detalhes de integração

---

## 🚀 Como Navegar

### "Quero entender as REGRAS"
→ `/EXECUTION/spec/CANONICAL/rules/ia-rules.md` (16 protocolos obrigatórios)

### "Quero entender a ARQUITETURA"
→ `/EXECUTION/spec/CANONICAL/specifications/architecture.md` (8-layer blueprint)

### "Qual é o estado atual do sistema?"
→ `/EXECUTION/spec/custom/rpg-narrative-server/reality/current-system-state/`

### "Qual é o trabalho em progresso?"
→ `/EXECUTION/spec/custom/rpg-narrative-server/development/execution-state/_current.md`

### "Como reutilizar SPEC em outro projeto?"
→ `/docs/ia/guides/navigation/REUSABILITY_GUIDE.md`

### "Quero start um novo projeto igual a este?"
→ Copie `/EXECUTION/spec/custom/_TEMPLATE/` para `/EXECUTION/spec/custom/meu-projeto/`

---

## 📊 Arquitetura

```
Clean Architecture 8-Layer (Mandatory ADR-001)
┌────────────────────────────────────────┐
│ 1. Infrastructure Layer (FastAPI)      │ 🔌 Adapters
├────────────────────────────────────────┤
│ 2. Framework Layer (Blinker Bus)       │ 🔌 Ports
├────────────────────────────────────────┤
│ 3. Interfaces Layer (Controllers)      │ 🎯 API boundary
├────────────────────────────────────────┤
│ 4. Application Layer (UseCases)        │ 🎯 Orchestration
├────────────────────────────────────────┤
│ 5. Domain Layer (Entities)             │ ✨ Business logic
├────────────────────────────────────────┤
│ 6. Shared Kernel Layer                 │ 📦 Common utilities
├────────────────────────────────────────┤
│ 7. Bootstrap Layer (Dependency Inject) │ ⚙️ Setup
├────────────────────────────────────────┤
│ 8. Vector Layer (ChromaDB wrapper)     │ 🔌 Search adapter
└────────────────────────────────────────┘

No Infrastructure Leakage (Mandatory ADR-003)
```

---

## 🧵 Thread Isolation (ADR-005)

Sistema suporta 2 níveis de isolamento:

1. **AI Agent Thread** — Executor de narrativas
   - Isola thread de IA para não bloquear
   - Timeout enforcement
   - Result caching

2. **Campaign Runtime** — Execução de campanha
   - Isolado por campanha (multitenancy)
   - Event sourcing com versionamento
   - Checkpointing obrigatório

---

## ⚡ Async-First (ADR-002)

**Obrigatório:** 100% da codebase é async

```python
# ✅ Correto
async def process_narrative():
    result = await service.generate()
    return result

# ❌ Errado (bloqueante)
def process_narrative():
    result = service.generate()  # Blocking!
```

---

## 🔒 Compliance & Quality Gates

Cada PR deve passar:

1. **Architecture Tests** (pytest)
   - Layer boundaries validadas
   - Sem cycles detectados
   - Ports não bypassados

2. **Code Quality**
   - Coverage 95%+ (domain layer)
   - Type checking ✅
   - Linting ✅

3. **Definition of Done**
   - 45+ item checklist (see CANONICAL/)
   - ADR se decisão arquitetural
   - Performance benchmarks
   - Security review

---

## 📅 Roadmap Melhorias

Planejado para adicionar em CANONICAL/ (todos projetos herdam):

| Área | Status | ETA |
|------|--------|-----|
| Observability Contract | 🚀 WIP | 2026-05-31 |
| Security Model | 🚀 WIP | 2026-06-15 |
| Performance SLOs | 🚀 WIP | 2026-06-01 |
| Compliance Gates | 🚀 WIP | 2026-06-15 |
| Pre-commit Hooks | ⏳ Planned | 2026-06-30 |
| Pytest Enforcement | ⏳ Planned | 2026-06-30 |

---

## 👥 Como Contribuir

1. **Leia primeiro:** `/docs/ia/.github/copilot-instructions.md` (10 min)
2. **Escolha PATH:** Bug fix? Feature? Refactor?
3. **Siga checklist:** `/EXECUTION/spec/CANONICAL/specifications/definition_of_done.md`
4. **Test:** Siga patterns em `/EXECUTION/spec/CANONICAL/specifications/testing.md`
5. **Document:** ADR se decisão, ou update de REALITY/

---

## 🔗 Referências Rápidas

- **Master Index:** `/docs/ia/_INDEX.md`
- **Architecture:** `/EXECUTION/spec/CANONICAL/specifications/architecture.md`
- **Rules:** `/EXECUTION/spec/CANONICAL/rules/ia-rules.md`
- **ADRs:** `/EXECUTION/spec/CANONICAL/decisions/`
- **Reusability:** `/docs/ia/guides/navigation/REUSABILITY_GUIDE.md`
- **Current State:** `custom/rpg-narrative-server/reality/`
- **Active Work:** `custom/rpg-narrative-server/development/`

---

## 📞 Suporte

- **Dúvida sobre arquitetura?** → Veja CANONICAL/decisions/ (ADRs)
- **Encontrou bug/limitation?** → Document em reality/limitations/
- **Quer melhor observability?** → Contribute ao WIP em CANONICAL/specifications/observability.md
- **Quer integrar SPEC em outro projeto?** → Siga `/EXECUTION/spec/custom/_TEMPLATE/INTEGRATION_CHECKLIST.md`

---

**Mantido por:** IA Governance Framework  
**Framework:** SPEC v1.0 (Multi-Project)  
**Última atualização:** 2026-04-19  
**Status:** ✅ Production-Ready
