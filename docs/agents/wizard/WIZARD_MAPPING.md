# 🎯 Mapeamento Completo: Suas Perguntas → Respostas do Wizard

## Sua Pergunta Original

> "Como faço para que o wizard me oriente passo a passo:
> 1. Me diga onde estão os source para eu ler e escolher
> 2. Onde informo o input com os dados escolhidos  
> 3. Onde ele segue os demais passos
> 4. Onde foram gerados os templates finais"

---

## ✅ Resposta: Sistema Implementado

Agora o wizard faz EXATAMENTE isso! Veja o mapeamento:

---

## 1️⃣ "Me diga onde estão os source para eu ler e escolher"

### Onde vê na tela:
```
PASSO 1️⃣: Review Source Files
======================================================================

📋 A) Mandates (HARD rules)
----------------------------------------------------------------------

  📄 mandate.spec
     Location: packages/.sdd-core/mandate.spec      ← AQUI
     Size: 0.7 KB

  Preview mandate.spec? (y/n): y                 ← VOCÊ ESCOLHE VER

📋 B) Guidelines (SOFT recommendations)
----------------------------------------------------------------------

  📄 guidelines.dsl
     Location: packages/.sdd-core/guidelines.dsl    ← AQUI
     Size: 27.6 KB

  Preview guidelines.dsl? (y/n): y               ← VOCÊ ESCOLHE VER
```

### Onde estão os files:
- **Source 1:** `/home/sergio/dev/sdd-architecture/packages/.sdd-core/mandate.spec`
  - Contém: 2 mandates (M001, M002)
  - Tamanho: ~0.7 KB
  - Tipo: Regras HARD (obrigatórias)

- **Source 2:** `/home/sergio/dev/sdd-architecture/packages/.sdd-core/guidelines.dsl`
  - Contém: 150 guidelines (G01-G150)
  - Tamanho: ~27.6 KB
  - Tipo: Recomendações SOFT (customizáveis)

### O que você faz:
```
Preview mandate.spec? (y/n): y     ← Você digita: y ou n
Preview guidelines.dsl? (y/n): y   ← Você digita: y ou n
```

✅ **Resultado:** Você vê exatamente onde os sources estão e pode previsualizá-los

---

## 2️⃣ "Onde informo o input com os dados escolhidos"

### Onde vê na tela:
```
PASSO 2️⃣: Configure Your Project
======================================================================

What programming language will you use?

  1. python
  2. java
  3. typescript
  4. go
  5. rust
  6. other

Select (1-6): 1                    ← AQUI: Input 1

  ✅ Language: python

📋 Select Mandates (HARD rules)
----------------------------------------------------------------------

  Include M001? (y/n): y           ← AQUI: Input 2
  Include M002? (y/n): y           ← AQUI: Input 3

  ✅ Selected 2 mandate(s): M001, M002

📋 Project Output Location
----------------------------------------------------------------------

Project output directory [default]: /your/custom/path  ← AQUI: Input 4
```

### Quais são os inputs:

| Input | Pergunta | Opções | Default |
|-------|----------|--------|---------|
| #1 | Linguagem? | python, java, typescript, go, rust, other | python |
| #2 | Incluir M001? | y/n | n |
| #3 | Incluir M002? | y/n | n |
| #4 | Diretório saída? | Qualquer path | `packages/sdd-generated/project` |

### O que você digita:
```
Select (1-6): 1
Include M001? (y/n): y
Include M002? (y/n): y
Project output directory [...]: <ENTER>
```

### Dados armazenados:
```python
{
    'language': 'python',
    'mandates': ['M001', 'M002'],
    'output_dir': Path('/home/sergio/dev/sdd-architecture/packages/sdd-generated/project')
}
```

✅ **Resultado:** Seus inputs são coletados e salvos para usar no próximo passo

---

## 3️⃣ "Onde ele segue os demais passos"

### Onde vê na tela:
```
PASSO 3️⃣: Generating Your Project
======================================================================

Executing 7-phase pipeline...

  ✅ Phase 1: Source validation [COMPLETE]
  ✅ Phase 2: Loading compiled governance [COMPLETE]
     └─ Loaded: 2 mandates, 150 guidelines

  ⏳ Phase 3: Filtering mandates...
     ✅ Mandates filtered

  ⏳ Phase 4: Filtering guidelines...
     ✅ Guidelines filtered

  ⏳ Phase 5: Applying template scaffold...
     ✅ Template scaffolding applied

  ⏳ Phase 6: Generating project structure...
     ✅ Project structure generated

  ⏳ Phase 7: Validating output...
     ✅ Validation complete
```

### O que cada fase faz:

| Fase | O Quê | Entrada | Saída |
|------|-------|---------|-------|
| **1** | Valida sources | mandate.spec, guidelines.dsl | ✅ Validado |
| **2** | Carrega compiled | governance-core.json, governance-client.json | ✅ Carregado (2 mandates, 150 guidelines) |
| **3** | Filtra mandates | Mandates de Phase 2 + Seus inputs | ✅ M001, M002 selecionados |
| **4** | Filtra guidelines | Guidelines de Phase 2 + Linguagem (python) | ✅ 150 guidelines filtradas |
| **5** | Aplica templates | Templates base + Suas escolhas | ✅ Scaffolding pronto |
| **6** | Gera projeto | Mandates + Guidelines + Templates | ✅ Estrutura completa |
| **7** | Valida output | Projeto gerado | ✅ Validação OK |

### Fluxo de dados:

```
Phase 1
  mandate.spec + guidelines.dsl
  ↓
Phase 2
  governance-core.json + governance-client.json
  + fingerprint validation
  ↓
Phase 3 (usa: seus inputs M001, M002)
  Filtra mandates selecionados
  ↓
Phase 4 (usa: sua linguagem python)
  Filtra guidelines por linguagem
  ↓
Phase 5
  Aplica templates base
  ↓
Phase 6
  Gera estrutura completa do projeto
  ↓
Phase 7
  Valida output
  ↓
✅ Projeto pronto!
```

### Você vê em tempo real:
```
✅ Phase 1: Source validation [COMPLETE]  ← Passou
✅ Phase 2: Loading compiled governance [COMPLETE]  ← Passou
⏳ Phase 3: Filtering mandates...  ← Executando
```

✅ **Resultado:** Você vê o progresso de cada passo sendo executado automaticamente

---

## 4️⃣ "Onde foram gerados os templates finais"

### Onde vê na tela:
```
PASSO 4️⃣: Project Generated Successfully! 🎉
======================================================================

📍 YOUR PROJECT LOCATION:
   /home/sergio/dev/sdd-architecture/packages/sdd-generated/project  ← AQUI

📋 WHAT WAS GENERATED:
  📂 project/
     ├── .ai/
     │   ├── constitution.md
     │   ├── governance-core.json
     │   └── governance-client.json
     ├── src/
     ├── tests/
     ├── docs/
     │   └── ARCHITECTURE.md
     ├── .sdd-artifacts/
     └── README.md

🔑 KEY FILES:
  ✅ .ai/constitution.md         - Your project constitution & rules
  ✅ README.md                   - Project overview and setup
  ✅ src/                        - Your source code directory
  ✅ tests/                      - Test suite
  ✅ docs/ARCHITECTURE.md        - Architecture documentation
```

### Localização exata:

```
/home/sergio/dev/sdd-architecture/packages/sdd-generated/project/
├── .ai/
│   ├── constitution.md           ← TEMPLATE 1: Sua constituição customizada
│   ├── governance-core.json      ← TEMPLATE 2: Governança core (2 mandates)
│   └── governance-client.json    ← TEMPLATE 3: Governança client (150 guidelines)
├── src/
│   ├── __init__.py
│   └── main.py                   ← TEMPLATE 4: Python project scaffold
├── tests/
│   ├── __init__.py
│   ├── test_architecture.py      ← TEMPLATE 5: Teste de arquitetura
│   └── conftest.py               ← TEMPLATE 6: Test fixtures
├── docs/
│   ├── ARCHITECTURE.md           ← TEMPLATE 7: Documentação de arquitetura
│   └── API.md                    ← TEMPLATE 8: Documentação de API
├── .sdd-artifacts/
│   └── [governance artifacts]
├── .gitignore
├── README.md                     ← TEMPLATE 9: Project README
├── pyproject.toml                ← TEMPLATE 10: Python config
└── pytest.ini                    ← TEMPLATE 11: Test configuration
```

### O que cada arquivo é:

| Arquivo | Tipo | Propósito |
|---------|------|----------|
| `.ai/constitution.md` | **TEMPLATE** | Suas regras + mandates + guidelines |
| `.ai/governance-*.json` | **ARTEFATO** | Governança compilada para seu projeto |
| `src/` | **SCAFFOLD** | Estrutura de código Python pronta |
| `tests/` | **SCAFFOLD** | Estrutura de testes pronta |
| `docs/ARCHITECTURE.md` | **TEMPLATE** | Arquitetura documenta conforme mandates |
| `README.md` | **TEMPLATE** | Overview do projeto |
| `pyproject.toml` | **TEMPLATE** | Configuração Python |

### Próximos passos mostrados:
```
📖 NEXT STEPS:
  1. Read /home/sergio/dev/sdd-architecture/packages/sdd-generated/project/.ai/constitution.md
  2. Review the generated structure
  3. Start implementing according to the constitution
  4. Run tests: pytest tests/

💬 CONFIGURATION USED:
  Language: python
  Mandates: M001, M002
  Output: /home/sergio/dev/sdd-architecture/packages/sdd-generated/project
```

✅ **Resultado:** Você vê EXATAMENTE onde tudo foi criado e sabe por onde começar

---

## 📊 Resumo: Cada Pergunta Sua → Cada Resposta do Wizard

### Sua Pergunta #1: "Me diga onde estão os source"
**✅ Resposta:**
- PASSO 1 mostra: `packages/.sdd-core/mandate.spec` e `packages/.sdd-core/guidelines.dsl`
- Você pode ver preview de cada um
- Localização exata mostrada em tela

### Sua Pergunta #2: "Onde informo o input com dados"
**✅ Resposta:**
- PASSO 2 pergunta 4 coisas:
  1. Linguagem: `1` (python)
  2. Incluir M001: `y`
  3. Incluir M002: `y`
  4. Diretório saída: `<ENTER>`

### Sua Pergunta #3: "Onde ele segue os demais passos"
**✅ Resposta:**
- PASSO 3 mostra em tempo real 7 fases executando:
  - Phase 1-7 com progresso visual
  - Você vê cada uma passar
  - Status: ✅ ou ⏳ mostrado

### Sua Pergunta #4: "Onde foram gerados templates"
**✅ Resposta:**
- PASSO 4 mostra:
  - Localização exata: `/home/sergio/.../sdd-generated/project/`
  - Estrutura completa criada
  - Cada arquivo-chave com seu propósito
  - Próximos passos

---

## 🎯 Fluxo Completo: Input → Output

```
Você executa:
./wizard.sh
    ↓
PASSO 1: Mostra sources (packages/.sdd-core/mandate.spec, guidelines.dsl)
    ↓ (você escolhe: visualizar? y/n)
PASSO 2: Coleta inputs (linguagem, mandates, output)
    ↓ (você digita: 1, y, y, <ENTER>)
PASSO 3: Executa pipeline (7 fases automáticas)
    ↓ (sistema processa tudo)
PASSO 4: Mostra resultado (exatamente onde foi criado)
    ↓ (você vê o full path + estrutura)
✅ Pronto! Seu projeto está em:
   /home/sergio/dev/sdd-architecture/packages/sdd-generated/project/
```

---

## 🔍 Como Encontrar Cada Coisa

| Você Quer | Está Em | Visto Em |
|-----------|---------|----------|
| Ver mandates | `packages/.sdd-core/mandate.spec` | Passo 1 - Preview |
| Ver guidelines | `packages/.sdd-core/guidelines.dsl` | Passo 1 - Preview |
| Dar sua linguagem | Passo 2 | `Select (1-6): _` |
| Dar seus mandates | Passo 2 | `Include M001? (y/n): _` |
| Ver progresso | Passo 3 | `Phase N: Status` |
| Saber onde criou | Passo 4 | `YOUR PROJECT LOCATION:` |
| Começar a codificar | Passo 4 | `.ai/constitution.md` |

---

## ✨ Resumo

```
✅ PASSO 1: Sources + Preview
   Você vê exatamente onde estão os files e pode visualizá-los

✅ PASSO 2: Sua Configuração  
   Você digita: linguagem, mandates, output directory

✅ PASSO 3: Execução Automática
   Sistema roda 7 fases, você vê progresso em tempo real

✅ PASSO 4: Resultados Finais
   Você vê EXATAMENTE onde tudo foi criado + próximos passos
```

**Tudo que você pediu, implementado! 🚀**
