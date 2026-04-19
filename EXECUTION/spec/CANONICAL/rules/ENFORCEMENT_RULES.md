# Enforcement Rules

Mecanismo de validação para garantir que SPEC seja seguido em todos os projetos.

## ✅ Validação Obrigatória

### Rule 1: Paths Must Reference Correct Layer

**Validação:** 
```bash
grep -r "CANONICAL/" docs/ia/CANONICAL/ | wc -l
# Deve usar: CANONICAL/
# NÃO deve usar: /specs/, /runtime/, /rules-old/
```

**Enforcement:** Pre-commit hook + linting

### Rule 2: CANONICAL Must Be Identical Across Projects

**Validação:**
```bash
diff docs/ia/CANONICAL/rules/ia-rules.md \
     /path/to/game-master-api/docs/ia/CANONICAL/rules/ia-rules.md
# Resultado: 0 diferenças (idênticos)
```

**Enforcement:** CI gate na pipeline

### Rule 3: No Project-Specific Files in CANONICAL/

**Validação:**
```bash
find CANONICAL/ -name "*rpg*" -o -name "*game*" -o -name "*[project]*"
# Resultado: nenhum arquivo (vazio)
```

**Enforcement:** Architecture tests (pytest)

### Rule 4: Each Project Has Its own custom/ Folder

**Validação:**
```bash
ls docs/ia/custom/
# Resultado: _TEMPLATE/, rpg-narrative-server/, game-master-api/, etc.
# Cada projeto = 1 pasta
```

**Enforcement:** Linting rules

### Rule 5: ARCHIVE is Read-Only

**Validação:**
```bash
git log --oneline docs/ia/ARCHIVE/ | wc -l
# Deve ter ZERO commits com modificação (apenas mv/add)
```

**Enforcement:** Pre-commit hook (git config)

## 🔧 Ferramentas de Validação

### Pre-commit Hook

```bash
# .git/hooks/pre-commit
#!/bin/bash

# 1. Verificar paths
if grep -r "docs/specs\|/runtime/" docs/ia/CANONICAL/; then
  echo "❌ ERRO: Paths incorretos em CANONICAL/"
  exit 1
fi

# 2. Verificar ARCHIVE read-only
if git diff --cached docs/ia/ARCHIVE/ | grep -E "^-|^+"; then
  echo "❌ ERRO: Tentativa de modificar ARCHIVE/"
  exit 1
fi

echo "✅ CANONICAL enforcement rules OK"
```

### Architecture Tests (pytest)

```python
# tests/architecture/test_spec_enforcement.py

def test_canonical_identical_across_projects():
    """CANONICAL/ deve ser idêntico entre todos projetos"""
    rpg_canonical = Path("docs/ia/CANONICAL")
    
    # Se houver outros projetos, verificar igualdade
    for other_canonical in find_all_projects():
        assert_files_identical(rpg_canonical, other_canonical)

def test_no_project_names_in_canonical():
    """Sem nomes de projeto em CANONICAL/"""
    for file in find_all_files("docs/ia/CANONICAL"):
        content = file.read_text()
        assert "rpg-narrative-server" not in content
        assert "[PROJECT_NAME]" in content or "generic" in content

def test_archive_not_modified():
    """ARCHIVE/ não pode sofrer modificação (apenas movimentação)"""
    # Verificar que último commit em ARCHIVE foi 'mv', não 'edit'
    ...

def test_custom_folders_isolated():
    """Pastas custom/ não devem ter imports cruzados"""
    rpg_custom = Path("docs/ia/custom/rpg-narrative-server")
    game_custom = Path("docs/ia/custom/game-master-api")
    
    # Não deve haver references entre projetos
    assert no_cross_references(rpg_custom, game_custom)
```

### CI/CD Gate

```yaml
# .github/workflows/spec-enforcement.yml

name: SPEC Enforcement

on: [pull_request]

jobs:
  enforce:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Check CANONICAL identity
        run: |
          # Se há múltiplos projetos, verificar igualdade
          for dir in docs/ia/custom/*/; do
            diff <(find docs/ia/CANONICAL -type f) \
                 <(find "$dir"/CANONICAL -type f) || exit 1
          done
      
      - name: Run pytest enforcement rules
        run: pytest tests/architecture/test_spec_enforcement.py -v
      
      - name: Check paths
        run: |
          if grep -r "docs/specs\|/runtime/" docs/ia/CANONICAL/; then
            echo "❌ Invalid paths in CANONICAL/"
            exit 1
          fi
```

## 📋 Checklist de Validação Manual

Antes de fazer push em CANONICAL/:

- [ ] Nenhum nome de projeto específico (deve ter `[PROJECT_NAME]` ou `generic`)
- [ ] Todos os paths apontam para `/CANONICAL/`, `/DEVELOPMENT/`, `/REALITY/`, `/ARCHIVE/`
- [ ] Sem referências a `docs/specs/`, `/runtime/`, ou estrutura antiga
- [ ] Se criando novo arquivo, é aplicável a TODOS os projetos?
- [ ] Arquitetura tests passam (`pytest tests/architecture/`)
- [ ] Pre-commit hook passou

## 🚨 Violações Encontradas & Corrigidas

### ❌ ia-rules.md

**Problema:** Paths antigos `/runtime/`, `/specs/`
**Status:** ✅ SERÁ CORRIGIDO na próxima phase
**Impacto:** Agentes leem documentação errada
**Fix:** Atualizar para `/CANONICAL/`, `/DEVELOPMENT/`

### ✅ architecture.md

**Status:** ✅ OK — Paths corretos

### ✅ definition_of_done.md

**Status:** ✅ OK — Sem nomes de projeto

## 📅 Review Schedule

- **Weekly:** Pre-commit hooks (automático)
- **Monthly:** CI/CD gates (automático)
- **Quarterly (3 meses):** Manual review por Arquiteto
  - Verificar aderência geral
  - Identificar novos gaps
  - Validar novas especificações

---

**Enforcer:** Arquitetura + Governance  
**Última revisão:** 2026-04-19  
**Próxima revisão:** 2026-07-19 (3 meses)
