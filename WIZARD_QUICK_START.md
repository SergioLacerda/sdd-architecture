# 🧙 SDD Wizard - Quick Start (2 min read)

## Resumo Rápido: Como Funciona o Wizard Interativo

### ⚡ TL;DR - 30 segundos

```bash
./setup.sh              # Setup (uma vez)
./wizard.sh             # Wizard interativo (responda 4 perguntas)
                        # ↓
                        # Seu projeto está em:
                        # _core/sdd-generated/project
```

---

## 🎯 Os 4 Passos

### 1️⃣ Review Source Files (2 min)
```
"Onde estão os arquivos de governança?"
→ Mostra: _core/.sdd-core/mandate.spec (regras hard)
→ Mostra: _core/.sdd-core/guidelines.dsl (recomendações)
→ Você: Pode previsualizá-los (y/n)
```

### 2️⃣ Configure Your Project (1 min)
```
"Qual linguagem?"         → Digite: 1 (python)
"Incluir M001?"          → Digite: y
"Incluir M002?"          → Digite: y
"Diretório de saída?"    → Aperte ENTER (default)
```

### 3️⃣ Generating Your Project (2-5 min)
```
Automático! Wizard executa 7 fases:
Phase 1 ✅ Valida sources
Phase 2 ✅ Carrega governance
Phase 3 ✅ Filtra mandates
Phase 4 ✅ Filtra guidelines
Phase 5 ✅ Aplica templates
Phase 6 ✅ Gera projeto
Phase 7 ✅ Valida output
```

### 4️⃣ See Results (1 min)
```
Mostra EXATAMENTE onde tudo foi criado:
📍 /home/sergio/dev/sdd-architecture/_core/sdd-generated/project

Arquivos gerados:
📄 .ai/constitution.md - Suas regras do projeto
📄 README.md - Overview
📂 src/ - Code
📂 tests/ - Tests
📂 docs/ - Documentation
```

---

## 📍 Localizações-Chave

| O Quê | Onde |
|-------|------|
| **Arquivos de Entrada** | `_core/.sdd-core/` |
| Regras (mandates) | `_core/.sdd-core/mandate.spec` |
| Recomendações (guidelines) | `_core/.sdd-core/guidelines.dsl` |
| **Projeto Gerado** | `_core/sdd-generated/project/` |
| Seu constitution | `.ai/constitution.md` |
| Seu código | `src/` |
| Seus testes | `tests/` |

---

## ✅ Checklist: Depois que o Wizard Termina

- [x] Projeto criado em `_core/sdd-generated/project/`
- [x] `.ai/constitution.md` com suas regras
- [x] `src/` com estrutura básica de código
- [x] `tests/` com scaffolding de testes
- [x] `README.md` com instruções
- [x] `.ai/governance-*.json` com governance compilada

**Próximo passo:** Leia `.ai/constitution.md` e comece a codificar!

---

## 🚀 Comandos

```bash
# Wizard em modo INTERATIVO (guiado, recomendado)
./wizard.sh

# Wizard em modo AUTOMÁTICO (sem perguntas)
./wizard.sh --language python --mandates M001,M002

# Testar fases específicas (para dev)
./wizard.sh --test-phases 1-7 --verbose

# Ver ajuda
./wizard.sh --help
```

---

## ❓ FAQ Rápido

**P: Sempre preciso rodar setup.sh?**  
R: Não, apenas uma vez. Depois é só `./wizard.sh`

**P: Posso mudar o diretório de saída?**  
R: Sim, no Passo 2, quando pergunta "Project output directory"

**P: Onde estão os sources que o wizard usa?**  
R: Em `_core/.sdd-core/mandate.spec` e `guidelines.dsl`

**P: Posso customizar as regras?**  
R: Sim, edite os sources e rode `./wizard.sh` novamente

**P: Como posso ver mais detalhes?**  
R: Leia [WIZARD_INTERACTIVE_GUIDE.md](WIZARD_INTERACTIVE_GUIDE.md) ou [WIZARD_EXAMPLE_SESSION.md](WIZARD_EXAMPLE_SESSION.md)

---

## 📚 Próximo Nível

Quer entender mais? Leia:
- [WIZARD_INTERACTIVE_GUIDE.md](WIZARD_INTERACTIVE_GUIDE.md) - Guia completo de cada passo
- [WIZARD_EXAMPLE_SESSION.md](WIZARD_EXAMPLE_SESSION.md) - Exemplo real de uma sessão completa

---

**Pronto para começar?**
```bash
./wizard.sh
```
🚀
