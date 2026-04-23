# 🏗️ SDD v3.0 Architecture: Source vs Compiled

**Status:** REQUIRES ARCHITECT APPROVAL  
**Date:** April 21, 2026

---

## Current State (INCORRECT)

Compilados estão na **raiz do projeto** (❌ errado):
```
/home/sergio/dev/sdd-architecture/
├── guidelines.dsl.compiled.json      ❌ RAIZ (incorreto)
├── mandate.spec.compiled.json        ❌ RAIZ (incorreto)
├── .sdd-core/CANONICAL/
│   └── mandate.spec                  ✅ FONTE
├── .sdd-guidelines/
│   └── guidelines.dsl                ✅ FONTE
└── .sdd-compiler/
    └── src/                          (compilador, mas outputs não definidos)
```

---

## Proposed Architecture (NEED YOUR DECISION)

### Option A: Compile in-place (local to each tier)
```
.sdd-core/CANONICAL/
├── mandate.spec                      ✅ FONTE (editar aqui)
├── mandate.spec.compiled.json        ⚙️ COMPILADO (gerado)
└── mandate.spec.msgpack              ⚙️ COMPILADO (gerado)

.sdd-guidelines/
├── guidelines.dsl                    ✅ FONTE (editar aqui)
├── guidelines.dsl.compiled.json      ⚙️ COMPILADO (gerado)
└── guidelines.dsl.msgpack            ⚙️ COMPILADO (gerado)
```

**Pros:** Everything local, easy to find  
**Cons:** Source + compiled mixed

---

### Option B: Separate compiled to .sdd-compiler/output/
```
.sdd-core/CANONICAL/
└── mandate.spec                      ✅ FONTE (editar aqui)

.sdd-guidelines/
└── guidelines.dsl                    ✅ FONTE (editar aqui)

.sdd-compiler/output/
├── mandate.spec.compiled.json        ⚙️ COMPILADO (gerado)
├── mandate.spec.msgpack              ⚙️ COMPILADO (gerado)
├── guidelines.dsl.compiled.json      ⚙️ COMPILADO (gerado)
└── guidelines.dsl.msgpack            ⚙️ COMPILADO (gerado)
```

**Pros:** Clean separation of source/compiled  
**Cons:** Need to look in compiler/ for outputs

---

### Option C: Compile to .sdd-runtime/ (for wizard)
```
.sdd-core/CANONICAL/
└── mandate.spec                      ✅ FONTE (editar aqui)

.sdd-guidelines/
└── guidelines.dsl                    ✅ FONTE (editar aqui)

.sdd-runtime/
├── mandate.bin (msgpack)             ⚙️ COMPILADO (wizard lê isso)
├── guidelines.bin (msgpack)          ⚙️ COMPILADO (wizard lê isso)
└── metadata.json                     ⚙️ TEMPO DE EXECUÇÃO

.sdd-extensions/
└── (carrega de .sdd-runtime/)
```

**Pros:** Single destination for wizard, extensions, runtime  
**Cons:** Adiciona diretório novo

---

## Where Wizard Reads From

```
Wizard initialization flow:

1. Wizard starts
2. Reads: .sdd-runtime/ (or wherever Option A/B/C defines)
3. Loads:
   - mandate.bin (hard rules)
   - guidelines.bin (soft rules, customizable)
   - metadata.json (versioning)
4. Presents to user:
   - Profile selection
   - Customization options
   - Final output
```

---

## Recommendation

**Option C** (wizard-focused) is cleanest:

```
📝 FONTE (você edita):
  .sdd-core/CANONICAL/mandate.spec
  .sdd-guidelines/guidelines.dsl

⚙️ COMPILADO (gerado automaticamente):
  .sdd-runtime/mandate.bin (msgpack)
  .sdd-runtime/guidelines.bin (msgpack)

🚀 TEMPO DE EXECUÇÃO (wizard lê):
  .sdd-runtime/ (toda a configuração)
  .sdd-extensions/ (carrega de .sdd-runtime/)
```

---

## Questions for You

1. **Source Location**: Correto `.sdd-core/CANONICAL/` e `.sdd-guidelines/`?

2. **Compiled Location**: Qual preferência?
   - Option A: Compilados ao lado do source
   - Option B: Compilados em `.sdd-compiler/output/`
   - Option C: Compilados em `.sdd-runtime/` (recomendado)

3. **File Cleanup**: Arquivos compilados atuais na raiz devem ser:
   - Movidos para o destino correto
   - Deletados (regenerados automaticamente)

4. **Wizard Integration**: Como wizard acessa os compilados?
   - Lê de `.sdd-runtime/`?
   - Lê de `.sdd-compiler/output/`?
   - Outro lugar?

5. **ADR-008 Process**: Devo:
   - Desfazer commits em main (revert)
   - Recriar em branch WIP
   - Criar PR para você revisar antes de merge

---

## Current Errors to Fix

```
❌ guidelines.dsl.compiled.json    (raiz - incorreto)
❌ mandate.spec.compiled.json      (raiz - incorreto)

✅ Devem estar em:
   - Option A: .sdd-core/CANONICAL/ e .sdd-guidelines/
   - Option B: .sdd-compiler/output/
   - Option C: .sdd-runtime/
```

---

## Approval Needed

**Please decide:**
1. Which architecture option (A/B/C)
2. Whether to revert main commits + create PR (ADR-008)
3. Confirmation of source locations

Then I'll:
1. Move files to correct locations
2. Revert main if needed + create WIP branch
3. Create PR for your review
4. Await approval before merging
