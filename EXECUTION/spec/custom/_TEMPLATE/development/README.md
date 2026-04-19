# [PROJECT_NAME] - Execution State

Documentação do estado de execução ativo do projeto **[PROJECT_NAME]**.

## 📋 Conteúdo

```
development/
├── _current.md              # Estado atual do projeto (MANDATORY)
├── execution-state/         # Estado de execução detalhado
│   ├── _current.md         # Ponto atual de execução
│   └── threads/            # Threads de trabalho (se multi-thread)
├── checkpoints/            # Snapshots de progresso
├── decisions-in-progress/  # Decisões não finalizadas
└── blockers-and-risks/     # Problemas e riscos
```

## 🔄 Atualização

Este diretório **MUDA FREQUENTEMENTE** durante desenvolvimento.

- `_current.md` atualizado após cada sessão
- Checkpoints criados em milestones importantes
- Removidos quando finalizados (mover para ARCHIVE/)

## 🔗 Referência

- Leia: `/docs/ia/guides/onboarding/QUICK_START.md` antes de começar
- Regras: `/docs/ia/CANONICAL/rules/ia-rules.md` (MANDATORY)
- Estado compartilhado: `/docs/ia/development/_SHARED/`

---

**Sincronização com CANONICAL:** Automática (herda 100%)  
**Especialização:** Específica do projeto [PROJECT_NAME]
