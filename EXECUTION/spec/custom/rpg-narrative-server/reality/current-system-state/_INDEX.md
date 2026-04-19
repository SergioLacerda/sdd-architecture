# 📍 ESTADO ATUAL DO SISTEMA (Current System State)

**Propósito**: Documentação da realidade atual (não especificação ideal)  
**Para**: Agents implementando features que precisam entender contratos, limitações, bugs reais  
**Diferença**: `/docs/ia/specs/` é "como DEVERIA ser", aqui é "como REALMENTE é"

---

## 🎯 Consultas Sob Medida (Adaptive Queries)

Guides usam este diretório para **consultas especializadas** baseadas no tipo de work:

### 🐛 Se é BUG FIX
```
Leia:
  → rag_pipeline.md (para entender o fluxo onde o bug está)
  → services.md (serviço afetado)
  → known_issues.md (pode já estar documentado!)
  → contracts.md (garantias que você não pode quebrar)
```

### ✨ Se é FEATURE SIMPLES (1-2 layers)
```
Leia:
  → contracts.md (quais ports você vai usar?)
  → storage_limitations.md (se envolve storage)
  → rag_pipeline.md (se toca em RAG)
  → data_models.md (estruturas esperadas)
```

### 🚀 Se é FEATURE COMPLEXA (3+ layers)
```
Leia:
  → rag_pipeline.md (pode afetar retrieval?)
  → services.md (orquestração)
  → threading_concurrency.md (se paralelo/async)
  → scaling_constraints.md (se não escala, por quê?)
  → known_issues.md (para não repetir erros)
  → contracts.md (ports afetadas)
```

### 🔗 Se é MULTI-THREAD
```
Leia:
  → threading_concurrency.md (limitações thread/async)
  → contracts.md (ExecutorPort)
  → known_issues.md (race conditions)
```

### 💾 Se envolve STORAGE
```
Leia:
  → storage_limitations.md (constraints atuais)
  → contracts.md (StoragePorts)
  → known_issues.md (data loss scenarios)
```

### 📊 Se precisa SCALING
```
Leia:
  → scaling_constraints.md (por quê não escala hoje)
  → storage_limitations.md (bottleneck)
  → threading_concurrency.md (concorrência)
  → rag_pipeline.md (índice distribuído?)
```

---

## 📑 ARQUIVOS

### `rag_pipeline.md`
```
- Component diagram do RAG real
- 8 componentes com detalhes
- 6 limitações do pipeline
- Fallback behaviors
```
**Ler se**: Bug em retrieval, nova expansão, ranking change

---

### `services.md`
```
- 8 serviços principais
- Entry points reais
- Responsabilidades
- Error handling atual
```
**Ler se**: Bug em usecase, orquestração, integração

---

### `contracts.md`
```
- 9 Ports (interfaces)
- Garantias de cada port
- Implementações atuais
- O que pode mudar, o que não
```
**Ler se**: Implementando novo adapter, tocando em portas

---

### `storage_limitations.md`
```
- Single-file JSON
- Sem transactions
- Sem criptografia
- Sem distributed locking
- Sem queryability
```
**Ler se**: Feature com persistence, multi-instance, ou performance

---

### `threading_concurrency.md`
```
- Single-threaded event loop
- Sem distributed locking
- Lazy-init races
- No task queue persistence
- CPU-bound delegation
```
**Ler se**: Feature paralela, async, ou background tasks

---

### `scaling_constraints.md`
```
- IVF in-memory only
- Semantic cache in-memory
- Campaigns all-in-memory
- Hardcoded concurrency=5
- No batch pooling
```
**Ler se**: Feature que precisa escalar, performance crítica

---

### `known_issues.md`
```
- 11 bugs/edge cases documentados
- 🔴 Critical (data loss)
- 🟡 Medium (workaround exists)
- 🟢 Low (acceptable for now)
- Por trigger, causa, impacto, mitigação
```
**Ler se**: Qualquer feature (para não repetir erros)

---

### `data_models.md`
```
- LLMRequest / LLMResponse
- NarrativeMemory
- PlayerActionEvent
- DiceExpression
- API schemas
- Storage structure
```
**Ler se**: Feature que toca em DTOs, serialização, API

---

## 🔗 MAPA DE RELAÇÕES

```
rag_pipeline.md
  ├─→ services.md (quem chama o RAG)
  ├─→ contracts.md (ports usados)
  └─→ known_issues.md (bugs em retrieval)

services.md
  ├─→ contracts.md (ports que usam)
  ├─→ threading_concurrency.md (async patterns)
  ├─→ data_models.md (DTOs)
  └─→ known_issues.md (bugs por serviço)

storage_limitations.md
  ├─→ contracts.md (StoragePorts)
  ├─→ known_issues.md (data loss, races)
  └─→ threading_concurrency.md (locking issues)

scaling_constraints.md
  ├─→ storage_limitations.md (bottleneck)
  ├─→ threading_concurrency.md (concurrency limit)
  └─→ rag_pipeline.md (índice distribuído?)
```

---

## 💡 EXEMPLO DE CONSULTA ADAPTATIVA

**Agent está implementando**: "Add priority tier to event memory"

**Guide (IMPLEMENTATION_ROADMAP.md) diz**:
```
"This modifies NarrativeMemory (data model) + storage layer"
→ Carregue: /docs/ia/current-system-state/data_models.md
→ Carregue: /docs/ia/current-system-state/storage_limitations.md
→ Carregue: /docs/ia/current-system-state/known_issues.md (data loss)
→ Evite: threading_concurrency.md (não paralelo)
→ Evite: scaling_constraints.md (scope é local)

Total context: ~25KB (não 56KB!)
```

---

## ✅ REGRAS DE USO

1. **Consulta específica**: Leia APENAS os arquivos relevantes
2. **Sem carregar tudo**: current-system-state/ é GRANDE se completo
3. **Combina com specs/**: CURRENT_SYSTEM_STATE + CONSTITUTION = decisões informadas
4. **Atualiza com código**: Se descobrir novo bug, add a known_issues.md
5. **Reusa queries**: Se dois agents fazem coisa similar, reuså mesmos arquivos

---

## 📊 CONTEXTO POR QUERY

| Query | Arquivos | KB | Economia |
|-------|----------|----|---------| 
| Bug fix simples | services.md + known_issues.md | ~15KB | 75% |
| Feature simples | contracts.md + data_models.md | ~18KB | 68% |
| Feature complexa | rag_pipeline + services + contracts + known_issues | ~40KB | 30% |
| Multi-thread | threading_concurrency + contracts + known_issues | ~22KB | 61% |
| Storage feature | storage_limitations + contracts + data_models | ~25KB | 55% |
| Scaling | scaling_constraints + storage + threading | ~28KB | 50% |

**Sem consultas sob medida** (tudo): 56KB  
**Com consultas sob medida**: 15-40KB (média 73% economia!)

---

## 🚀 PRÓXIMA AÇÃO

1. Guides (QUICK_START.md, INDEX.md, etc) referenciam este índice
2. Para cada PATH (A/B/C/D), specify quais arquivos carregar
3. Agents consultam sob medida conforme trabalham
4. Result: Contexto otimizado + knowledge específico + sem surpresas

