# Quick Reference: SDD v3.0

**Para respostas rápidas sem ler documento inteiro**

---

## ❓ Quick Q&A

### Paths

**Q: Onde é que agentes executam?**  
A: `.sdd-runtime/` (compiled + working + audit + checkpoint)

**Q: Onde é que o Wizard coloca outputs?**  
A: `.sdd-compiled/` (2 arquivos msgpack)

**Q: Qual é a diferença?**  
A: `.sdd-compiled/` = output do wizard | `.sdd-runtime/` = agent working dir

---

### Arquivos

**Q: Quais são os 2 arquivos do Wizard?**  
A:
1. `governance-core.compiled.msgpack` (readonly, não customizável)
2. `governance-client-template.compiled.msgpack` (writable, customizável)

**Q: O que vai em cada um?**  
A:
- CORE: Constitution + ADRs + items marcados NÃO-customizable
- CLIENT: items marcados CUSTOMIZABLE

---

### Separação

**Q: Como sei o que é CORE vs CLIENT?**  
A: User marca cada item no Wizard com flag "customizable: true/false"
- True → CLIENT (editable)
- False → CORE (locked)

**Q: Posso editar CORE no agent?**  
A: ❌ NÃO. É readonly.

**Q: Posso editar CLIENT no agent?**  
A: ✅ SIM. Pode customizar.

---

### Fingerprinting

**Q: Como funciona o salt?**  
A: 
- fingerprint_core = SHA-256(core_data)
- fingerprint_client = SHA-256(fingerprint_core + client_data)
- Core fingerprint virou "salt" para client

**Q: Por que usar salt?**  
A: Se core muda, client fingerprint fica invalido (detecta mudança)

---

### Fases

**Q: Quais são as 4 fases?**  
A:
1. Pipeline (consolidar → JSON intermediário)
2. Compiler (gerar 2 arquivos)
3. Tests (validar)
4. Deploy (commit + tag)

**Q: Em que ordem?**  
A: Sequencial (cada uma bloqueia a próxima)

**Q: Quanto tempo?**  
A: ~4-5 dias total

---

### Business Rules

**Q: Quantas regras de negócio?**  
A: 6 (todas maturadas)

**Q: Quais são?**  
A:
1. 4 níveis de criticidade (CORE_IMMUTABLE, STRUCTURAL, BEHAVIORAL, CUSTOMIZABLE)
2. Customizable flags (user marca)
3. Criticidade de guardrails (OBRIGATÓRIO/ALERTA/OPCIONAL)
4. Fingerprinting com salt
5. Imutabilidade em compilação
6. Rastreabilidade completa

---

### User Interaction

**Q: O que o user faz no Wizard?**  
A:
1. Vê Constitution + ADRs (info-only)
2. Marca cada rule/guardrail (customizable? sim/não)
3. Define criticidade (OBRIGATÓRIO/ALERTA/OPCIONAL)
4. Confirma

**Q: O que o agent faz no runtime?**  
A:
1. Carrega CORE (read-only)
2. Customiza CLIENT (se quiser)
3. Executa sob governance final

---

## 🔢 Números-Chave

| Métrica | Valor |
|---------|-------|
| Níveis de criticidade | 4 |
| Business rules | 6 |
| Arquivos de output | 2 (CORE + CLIENT) |
| Fases de implementação | 4 |
| Tempo total (Fases 1-4) | 4-5 dias |
| Fingerprint layers | 2 (core + client com salt) |
| Diretórios em .sdd-runtime | 4 (compiled, working, audit, checkpoint) |

---

## 📋 Decisões Críticas

| Decisão | Valor | Razão |
|---------|-------|-------|
| 1 ou 2 arquivos output? | **2** | Clareza + segurança |
| CORE é mutável? | **Não** | Integridade |
| CLIENT é mutável? | **Sim** | Flexibilidade |
| Fingerprint strategy? | **Com salt** | Detecta mudanças core |
| Base para agents? | **.sdd-runtime** | Executáo local |

---

## ✅ Checklist (Antes de Começar)

```
[ ] Entendi: 4 níveis de criticidade
[ ] Entendi: 2 arquivos físicos (CORE + CLIENT)
[ ] Entendi: Paths (.sdd-core, .sdd-compiled, .sdd-runtime)
[ ] Entendi: 6 business rules
[ ] Entendi: Fingerprinting com salt
[ ] Aprovado: Pronto para Phase 1?
```

---

## 🚀 Começar

1. Ler: `.sdd-runtime/wizard/ARCHITECTURE_v3.0_CONSOLIDATED.md`
2. Se OK → Começar Phase 1
3. Se dúvidas → Ver seção relevante em ARCHITECTURE...md

---

**Última atualização:** April 22, 2026
