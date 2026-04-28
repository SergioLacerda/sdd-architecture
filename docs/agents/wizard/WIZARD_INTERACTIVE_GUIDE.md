# 🧙 SDD Wizard - Interactive Mode Guide

## Como Usar o Wizard Passo a Passo

O wizard fornece orientação completa em **4 etapas interativas**:

---

## ✅ PASSO 1️⃣: Revise os Arquivos Fonte

### Onde estão os arquivos source?

```
📂 /home/sergio/dev/sdd-architecture
├── packages/
│   └── .sdd-core/
│       ├── mandate.spec       ← ⬅️ MANDATES (Regras HARD)
│       └── guidelines.dsl     ← ⬅️ GUIDELINES (Recomendações)
```

### Como funciona?

1. O wizard **mostra o caminho** de cada arquivo:
   ```
   📄 mandate.spec
      Location: packages/.sdd-core/mandate.spec
      Size: 0.7 KB
   ```

2. Você pode **visualizar o conteúdo** (primeiras 20-30 linhas):
   ```
   Preview mandate.spec? (y/n): y
   
   # SDD v3.0 - MANDATE Specification
   mandate M001 {
     type: HARD
     title: "Clean Architecture"
     ...
   }
   ```

3. Mesma coisa para `guidelines.dsl`:
   - Mostra localização
   - Oferece visualizar preview
   - Mostra 150 diretrizes disponíveis

---

## ✅ PASSO 2️⃣: Configure Seu Projeto

### Onde informar os dados de entrada?

O wizard faz **3 perguntas interativas**:

#### 1. Escolha a Linguagem
```
What programming language will you use?

  1. python
  2. java
  3. typescript
  4. go
  5. rust
  6. other

Select (1-6): 1
✅ Language: python
```

#### 2. Selecione os Mandates (Regras HARD)
```
Select Mandates (HARD rules)

Which mandates apply to your project?
All mandates are REQUIRED - select which ones to enforce:

  Include M001? (y/n): y
  Include M002? (y/n): y

✅ Selected 2 mandate(s): M001, M002
```

#### 3. Defina o Diretório de Saída
```
Project Output Location

Project output directory [/home/sergio/dev/sdd-architecture/packages/sdd-generated/project]: 

✅ Output: /home/sergio/dev/sdd-architecture/packages/sdd-generated/project
```

---

## ✅ PASSO 3️⃣: Gere Seu Projeto

### O que acontece nesta etapa?

O wizard **executa o pipeline automaticamente** e mostra progresso em **tempo real**:

```
🚀 Executing 7-phase pipeline...

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

### Cada fase faz:
- **Phase 1**: Valida `mandate.spec` e `guidelines.dsl`
- **Phase 2**: Carrega governance compilada (`governance-core.json`, `governance-client.json`)
- **Phase 3**: Filtra mandates selecionados
- **Phase 4**: Filtra guidelines por linguagem
- **Phase 5**: Copia templates de scaffold
- **Phase 6**: Gera estrutura completa do projeto
- **Phase 7**: Valida projeto gerado

---

## ✅ PASSO 4️⃣: Veja Onde Tudo Foi Gerado

### Localização do Projeto Gerado

```
📍 YOUR PROJECT LOCATION:
   /home/sergio/dev/sdd-architecture/packages/sdd-generated/project
```

### Estrutura Gerada

```
📂 project/
   ├── .ai/
   │   ├── constitution.md          ← Sua constituição personalizada
   │   ├── governance-core.json
   │   └── governance-client.json
   ├── src/                         ← Seu código-fonte
   ├── tests/                       ← Suite de testes
   ├── docs/
   │   ├── ARCHITECTURE.md
   │   └── [outros docs]
   ├── .sdd-artifacts/             ← Artefatos SDD
   └── README.md                    ← Overview do projeto
```

### Arquivos-Chave

```
✅ .ai/constitution.md          - Sua constituição & regras do projeto
✅ README.md                    - Overview e setup do projeto
✅ src/                         - Seu diretório de código-fonte
✅ tests/                       - Suite de testes
✅ docs/ARCHITECTURE.md         - Documentação de arquitetura
```

---

## 🚀 Como Executar o Wizard

### Modo Interativo (Padrão)
```bash
cd /home/sergio/dev/sdd-architecture
./setup.sh              # Setup uma única vez (se não feito)
./wizard.sh             # Executa em modo INTERATIVO
```

### Modo Automático (Sem Perguntas)
```bash
./wizard.sh --language python --mandates M001,M002 --output ~/my-project
```

### Ver Ajuda
```bash
./wizard.sh --help
```

---

## 📋 Checklist: Seu Projeto Está Pronto!

Após a conclusão, você terá:

- [x] ✅ Constitution personalizada (`.ai/constitution.md`)
- [x] ✅ Governance artifacts compilados (`.sdd-artifacts/`)
- [x] ✅ Estrutura de project gerada
- [x] ✅ Tests scaffold (pronto para adicionar tests)
- [x] ✅ Documentation scaffold
- [x] ✅ README com instruções
- [x] ✅ Source code directory estruturado

---

## 🔍 Exemplos de Uso

### Exemplo 1: Novo Desenvolvedor Criando Primeiro Projeto
```bash
# Passo 1: Setup (uma única vez)
./setup.sh

# Passo 2: Wizard interativo
./wizard.sh

# Segue os 4 passos interativos:
# 1. Lê os source files
# 2. Seleciona language, mandates, output
# 3. Wizard gera automaticamente
# 4. Vê onde o projeto foi criado
```

### Exemplo 2: Rodar Wizard Sem Interação
```bash
./wizard.sh --language python --mandates M001,M002
```

### Exemplo 3: Testar as Fases (para desenvolvimento)
```bash
./wizard.sh --test-phases 1-7 --verbose
```

---

## 📚 Próximos Passos

Depois que o wizard terminar:

```
1. 📖 Leia sua constituição:
   cat /home/sergio/dev/sdd-architecture/packages/sdd-generated/project/.ai/constitution.md

2. 🏗️  Entenda a arquitetura:
   cat /home/sergio/dev/sdd-architecture/packages/sdd-generated/project/docs/ARCHITECTURE.md

3. 🧪 Inicie os testes:
   cd /home/sergio/dev/sdd-architecture/packages/sdd-generated/project
   pytest tests/ -v

4. 💻 Comece a codificar:
   # Siga as regras em .ai/constitution.md
```

---

## ❓ Perguntas Comuns

### P: Como mudo o diretório de saída?
**R:** No PASSO 2, quando perguntado "Project output directory", digite o novo caminho.

### P: Posso rodar o wizard sem modo interativo?
**R:** Sim! Use `--language python --mandates M001 --output ~/my-project`

### P: O que fazer se o wizard falhar?
**R:** Execute com `--verbose` para mais detalhes:
```bash
./wizard.sh --verbose
```

### P: Onde estão os source files originais?
**R:** Em `packages/.sdd-core/`:
- `mandate.spec` - Mandates DSL
- `guidelines.dsl` - Guidelines DSL

### P: Posso customizar os source files?
**R:** Sim! Edit em `packages/.sdd-core/` e rode o wizard novamente.

---

## 🎯 Resumo: Os 4 Passos do Wizard

| Passo | O Que Faz | Entrada | Saída |
|-------|-----------|---------|-------|
| 1️⃣ Review Sources | Mostra onde estão os files | Ver preview (y/n) | ✅ Confirmed |
| 2️⃣ Configure | Pergunta linguagem, mandates, output | Suas escolhas | Selections salvas |
| 3️⃣ Generate | Executa 7-phase pipeline | Automático | Projeto criado |
| 4️⃣ Results | Mostra onde tudo foi criado | View (automático) | Project location |

---

**Pronto! Seu projeto SDD está criado e pronto para desenvolvimento! 🚀**
