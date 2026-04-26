# 🧙 SDD Wizard - Documentation Index

## 📚 Guias Disponíveis

Escolha o documento certo para seu objetivo:

---

### ⚡ **Precisa Começar AGORA? (2 min)**
👉 **[WIZARD_QUICK_START.md](WIZARD_QUICK_START.md)**
- TL;DR de como funciona
- Comandos essenciais
- FAQ rápido
- Localizações-chave

---

### 🎯 **Quer Saber Exatamente Onde Cada Coisa Está?**
👉 **[WIZARD_MAPPING.md](WIZARD_MAPPING.md)**
- Sua pergunta → Resposta do wizard
- Mapeamento completo (1-4 do que você perguntou)
- Onde digitar inputs
- Onde ver resultados
- Estrutura dos arquivos gerados

---

### 🧙 **Quer Guia Completo com Todos os Detalhes?**
👉 **[WIZARD_INTERACTIVE_GUIDE.md](WIZARD_INTERACTIVE_GUIDE.md)**
- Os 4 passos explicados em profundidade
- Como cada passo funciona
- Checklist final
- Próximos passos de desenvolvimento
- Exemplos de uso

---

### 📺 **Quer Ver Um Exemplo Real de Sessão?**
👉 **[WIZARD_EXAMPLE_SESSION.md](WIZARD_EXAMPLE_SESSION.md)**
- Transcrição completa de uma sessão interativa
- Exatamente o que você vê e digita
- Output em tempo real
- Respostas passo a passo

---

## 📖 Comparação Rápida

| Documento | Duração | Melhor Para | Tipo |
|-----------|---------|-----------|------|
| WIZARD_QUICK_START.md | 2 min | Começar rápido | Reference |
| WIZARD_MAPPING.md | 10 min | Entender fluxo completo | Guide |
| WIZARD_INTERACTIVE_GUIDE.md | 15 min | Aprender cada passo em detalhe | Tutorial |
| WIZARD_EXAMPLE_SESSION.md | 10 min | Ver exemplo real | Example |
| README.md (section) | 5 min | Overview no contexto | Overview |

---

## 🚀 Por Onde Começar?

### Cenário 1: "Quero usar o wizard AGORA"
```
1. Leia: WIZARD_QUICK_START.md (2 min)
2. Execute: ./setup.sh && ./wizard.sh
3. Done! ✅
```

### Cenário 2: "Quero entender como funciona"
```
1. Leia: WIZARD_MAPPING.md (suas 4 perguntas mapeadas)
2. Veja: WIZARD_EXAMPLE_SESSION.md (exemplo real)
3. Rode: ./wizard.sh (experimente!)
```

### Cenário 3: "Quero aprender todos os detalhes"
```
1. Leia: WIZARD_INTERACTIVE_GUIDE.md (completo)
2. Veja: WIZARD_EXAMPLE_SESSION.md (concreto)
3. Pratique: ./wizard.sh múltiplas vezes
```

### Cenário 4: "Tenho dúvidas específicas"
```
1. Procure em: WIZARD_MAPPING.md (índice por pergunta)
2. Ou em: WIZARD_INTERACTIVE_GUIDE.md (índice por tópico)
3. Veja exemplo em: WIZARD_EXAMPLE_SESSION.md
```

---

## 🎯 Encontrar Resposta Rápida

### "Onde estão os arquivos source?"
→ [WIZARD_MAPPING.md - Seção 1](WIZARD_MAPPING.md#1-me-diga-onde-estão-os-source-para-eu-ler-e-escolher)

### "Como digito minha configuração?"
→ [WIZARD_MAPPING.md - Seção 2](WIZARD_MAPPING.md#2-onde-informo-o-input-com-os-dados-escolhidos)

### "O que acontece quando o wizard roda?"
→ [WIZARD_MAPPING.md - Seção 3](WIZARD_MAPPING.md#3-onde-ele-segue-os-demais-passos)

### "Onde foi meu projeto criado?"
→ [WIZARD_MAPPING.md - Seção 4](WIZARD_MAPPING.md#4-onde-foram-gerados-os-templates-finais)

### "Como cada passo funciona em detalhe?"
→ [WIZARD_INTERACTIVE_GUIDE.md](WIZARD_INTERACTIVE_GUIDE.md)

### "Quero ver um exemplo completo?"
→ [WIZARD_EXAMPLE_SESSION.md](WIZARD_EXAMPLE_SESSION.md)

### "Preciso de resumo rápido?"
→ [WIZARD_QUICK_START.md](WIZARD_QUICK_START.md)

---

## 📱 Usando a Documentação

### No Terminal
```bash
# Ver quick start
cat WIZARD_QUICK_START.md | less

# Ver mapeamento
cat WIZARD_MAPPING.md | less

# Ver guia completo
cat WIZARD_INTERACTIVE_GUIDE.md | less

# Ver exemplo
cat WIZARD_EXAMPLE_SESSION.md | less
```

### No VS Code
- Abra qualquer documento `.md`
- Use Ctrl+F para buscar keywords
- Clique em headers para navegação

---

## 🔍 Índice por Tópico

### "Localizações e Diretórios"
- [WIZARD_QUICK_START.md - Localizações-Chave](WIZARD_QUICK_START.md#-localizações-chave)
- [WIZARD_MAPPING.md - Localização exata](WIZARD_MAPPING.md#4-onde-foram-gerados-os-templates-finais)
- [WIZARD_INTERACTIVE_GUIDE.md - Estrutura gerada](WIZARD_INTERACTIVE_GUIDE.md#estrutura-gerada)

### "Como Rodar o Wizard"
- [WIZARD_QUICK_START.md - Comandos](WIZARD_QUICK_START.md#-comandos)
- [WIZARD_INTERACTIVE_GUIDE.md - Como executar](WIZARD_INTERACTIVE_GUIDE.md#-como-executar-o-wizard)
- [WIZARD_EXAMPLE_SESSION.md - Exemplo real](WIZARD_EXAMPLE_SESSION.md#-sessão-completa)

### "O Que O Wizard Faz"
- [WIZARD_MAPPING.md - Fluxo de dados](WIZARD_MAPPING.md#fluxo-de-dados)
- [WIZARD_INTERACTIVE_GUIDE.md - 4 passos](WIZARD_INTERACTIVE_GUIDE.md#-passo-1%EF%B8%8F-revise-os-arquivos-fonte)

### "Inputs e Configuração"
- [WIZARD_MAPPING.md - Seção 2](WIZARD_MAPPING.md#2-onde-informo-o-input-com-os-dados-escolhidos)
- [WIZARD_EXAMPLE_SESSION.md - Passo 2](WIZARD_EXAMPLE_SESSION.md#passo-2%EF%B8%8F-configurar-seu-projeto)

### "Arquivos Gerados"
- [WIZARD_MAPPING.md - Templates finais](WIZARD_MAPPING.md#4-onde-foram-gerados-os-templates-finais)
- [WIZARD_INTERACTIVE_GUIDE.md - Arquivos-chave](WIZARD_INTERACTIVE_GUIDE.md#arquivos-chave)

---

## ✅ Checklist: Depois de Ler a Documentação

- [ ] Li pelo menos um documento
- [ ] Entendo onde os sources estão
- [ ] Sei como rodar o wizard
- [ ] Conheço os 4 passos
- [ ] Sei onde meu projeto será criado
- [ ] Pronto para rodar: `./wizard.sh`

---

## 🎓 Learning Path

### Iniciante
```
1. WIZARD_QUICK_START.md (2 min)
2. WIZARD_EXAMPLE_SESSION.md (10 min)
3. ./wizard.sh (experimente!)
```

### Intermedi­ário
```
1. WIZARD_INTERACTIVE_GUIDE.md (15 min)
2. WIZARD_MAPPING.md (10 min)
3. ./wizard.sh (pratique configurações diferentes)
```

### Avançado
```
1. Leia: .sdd-wizard/src/interactive_mode.py
2. Customize: adicione novos inputs ou fases
3. Estenda: integre com seu pipeline
```

---

## 📞 Suporte Rápido

### "Onde vejo X na tela?"
→ [WIZARD_EXAMPLE_SESSION.md](WIZARD_EXAMPLE_SESSION.md) (procure por "X" em todo o arquivo)

### "Como faço X?"
→ [WIZARD_INTERACTIVE_GUIDE.md](WIZARD_INTERACTIVE_GUIDE.md) (procure por "How to X")

### "O que é X?"
→ [WIZARD_QUICK_START.md](WIZARD_QUICK_START.md#resumo-rápido-como-funciona-o-wizard-interativo) (glossário)

---

## 📊 Estatísticas da Documentação

| Documento | Tamanho | Seções | Tempo Leitura |
|-----------|---------|--------|---------------|
| WIZARD_QUICK_START.md | ~2 KB | 8 | 2 min |
| WIZARD_MAPPING.md | ~8 KB | 5 + tabelas | 10 min |
| WIZARD_INTERACTIVE_GUIDE.md | ~12 KB | 8 + exemplos | 15 min |
| WIZARD_EXAMPLE_SESSION.md | ~10 KB | 4 (full session) | 10 min |
| **TOTAL** | **~32 KB** | **~25** | **~37 min** |

---

## 🚀 Comece Agora!

### Opção 1: Leia rápido e comece
```bash
# 2 min de leitura
cat WIZARD_QUICK_START.md

# Depois rode
./setup.sh && ./wizard.sh
```

### Opção 2: Entenda o mapeamento
```bash
# 10 min de leitura
cat WIZARD_MAPPING.md

# Depois rode
./wizard.sh
```

### Opção 3: Aprenda tudo
```bash
# 30+ min de aprendizado
cat WIZARD_INTERACTIVE_GUIDE.md
cat WIZARD_EXAMPLE_SESSION.md

# Depois pratique
./wizard.sh
```

---

**Pronto! Escolha seu documento e comece! 🚀**
