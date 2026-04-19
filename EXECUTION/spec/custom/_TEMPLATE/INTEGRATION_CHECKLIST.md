# SPEC Integration Checklist

Para integrar este projeto com o framework SPEC, siga este checklist.

## Fase 1: Setup (30 min)

- [ ] Copiar estrutura de `/docs/ia/custom/_TEMPLATE/` para `/docs/ia/custom/[PROJECT_NAME]/`
- [ ] Atualizar `README.md` com nome e descrição do projeto
- [ ] Atualizar `.github/copilot-instructions.md` com novo path `/docs/ia/custom/[PROJECT_NAME]/`
- [ ] Criar `.vscode/ai-rules.json` com paths atualizados (copiar de outro projeto)

## Fase 2: Customização (2-3 horas)

### REALITY (Estado Observado)

- [ ] Documentar em `reality/current-system-state/` os serviços do projeto
- [ ] Listar limitações em `reality/limitations/`
- [ ] Documentar constraints específicos do projeto

### DEVELOPMENT (Execução Ativa)

- [ ] Criar `development/execution-state/_current.md`
- [ ] Setup de threads de trabalho (se multi-thread)
- [ ] Documentar riscos em `development/blockers-and-risks/`

## Fase 3: Validação (1 hora)

- [ ] Verificar herança de `/docs/ia/CANONICAL/` (deve ser 100% igual)
- [ ] Validar paths em `CANONICAL/rules/ia-rules.md` apontam para novo projeto
- [ ] Testar navegação usando `/docs/ia/_INDEX.md` (master index)
- [ ] Confirmar compliance com enforcement rules

## Fase 4: Melhorias World-Class (ON DEMAND)

Quando implementar melhorias de qualidade, aplicar em CANONICAL/ primeiro (todos herdam):

- [ ] Observabilidade: CANONICAL/specifications/observability.md (novo)
- [ ] Segurança: CANONICAL/rules/security-model.md (novo)
- [ ] Performance: CANONICAL/specifications/performance.md (novo)
- [ ] Compliance: CANONICAL/specifications/compliance.md (novo)
- [ ] Testes: CANONICAL/specifications/testing.md (expandido)

---

**Tempo total:** ~4 horas (setup + customização + validação)
