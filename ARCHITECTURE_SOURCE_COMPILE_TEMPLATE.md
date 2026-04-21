# 📐 SDD v3.0 Architecture & Workflow

**Date:** April 21, 2026  
**Status:** Architecture Definition (Ready for Review)

---

## 🎯 Overview: Source → Compile → Runtime → Template

```
┌─────────────────────────────────────────────────────────────────┐
│ ARQUITETO (você) edita FONTE                                   │
├─────────────────────────────────────────────────────────────────┤
│ .sdd-core/CANONICAL/mandate.spec                               │
│ .sdd-guidelines/guidelines.dsl                                 │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ↓ COMPILADOR (.sdd-compiler/)
┌─────────────────────────────────────────────────────────────────┐
│ COMPILADO (automático, via CI/CD)                              │
├─────────────────────────────────────────────────────────────────┤
│ .sdd-runtime/mandate.bin (msgpack)                             │
│ .sdd-runtime/guidelines.bin (msgpack)                          │
│ .sdd-runtime/metadata.json                                     │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ↓ WIZARD (sob demanda)
┌─────────────────────────────────────────────────────────────────┐
│ TEMPLATE FINAL (estrutura .sdd pronta para deploy)             │
├─────────────────────────────────────────────────────────────────┤
│ .sdd-templates/                                                │
│ ├── java/          (lê .sdd-runtime/ + config JAVA)           │
│ │   ├── .sdd/                                                 │
│ │   │   ├── CANONICAL/mandate.spec (customizado)             │
│ │   │   └── guidelines.dsl (customizado)                     │
│ │   ├── src/                                                 │
│ │   ├── pom.xml                                              │
│ │   └── README.md (SDD v3.0 setup instructions)              │
│ │                                                             │
│ ├── python/        (lê .sdd-runtime/ + config Python)        │
│ │   ├── .sdd/                                                │
│ │   │   ├── CANONICAL/mandate.spec (customizado)            │
│ │   │   └── guidelines.dsl (customizado)                    │
│ │   ├── src/                                                │
│ │   ├── requirements.txt                                     │
│ │   └── README.md (SDD v3.0 setup instructions)             │
│ │                                                            │
│ └── js/            (lê .sdd-runtime/ + config JS)           │
│     ├── .sdd/                                               │
│     │   ├── CANONICAL/mandate.spec (customizado)           │
│     │   └── guidelines.dsl (customizado)                   │
│     ├── src/                                               │
│     ├── package.json                                        │
│     └── README.md (SDD v3.0 setup instructions)            │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📍 Directory Structure & Responsibilities

### 1️⃣ SOURCE (Você Edita) - CENTRALIZED in .sdd-core/

```
.sdd-core/CANONICAL/
├── mandate.spec                    
│   ├─ Origin: Extracted from v2.1
│   ├─ Format: SDD DSL (spec-v1)
│   ├─ Content: 2 mandates (M001, M002)
│   ├─ You: Edit to change hard rules
│   └─ Never: Commit compiled versions here
│
└── guidelines.dsl                  
    ├─ Origin: Extracted from v2.1
    ├─ Format: SDD DSL (spec-v1)
    ├─ Content: 150 guidelines
    ├─ You: Edit to change soft patterns
    └─ Never: Commit compiled versions here
```

**All source files now live in `.sdd-core/CANONICAL/`**
- Single location for MANDATES + GUIDELINES
- Easier to maintain
- Clearer structure

**Your workflow:**
```bash
# 1. Edit source
vim .sdd-core/CANONICAL/mandate.spec
vim .sdd-guidelines/guidelines.dsl

# 2. Commit (via PR in WIP branch!)
git checkout -b wip/update-mandate-X
git add .sdd-core/ .sdd-guidelines/
git commit -m "feat: Update mandate/guideline"
git push origin wip/update-mandate-X
# → Create PR → Wait for architect review → Architect merges
```

---

### 2️⃣ COMPILED OUTPUT (.sdd-runtime/)

```
.sdd-runtime/
├── mandate.bin                     
│   ├─ Origin: Compiled from .sdd-core/CANONICAL/mandate.spec
│   ├─ Format: MessagePack binary
│   ├─ Size: ~5-10 KB
│   ├─ Usage: Wizard reads (fast load)
│   └─ Lifecycle: Regenerated on source change
│
├── guidelines.bin                  
│   ├─ Origin: Compiled from .sdd-guidelines/guidelines.dsl
│   ├─ Format: MessagePack binary
│   ├─ Size: ~20-30 KB
│   ├─ Usage: Wizard reads (fast load)
│   └─ Lifecycle: Regenerated on source change
│
└── metadata.json                   
    ├─ Version: "3.0"
    ├─ Tier: "lite" (or "pro", "enterprise" in future)
    ├─ Format: "spec-v1"
    ├─ Compiled-at: timestamp
    └─ Source-hash: SHA256 of source files
```

**Auto-generation:**
```bash
# CI/CD trigger: On commit to .sdd-core/ or .sdd-guidelines/
# Command:
python .sdd-compiler/src/compile.py \
  --mandate .sdd-core/CANONICAL/mandate.spec \
  --guidelines .sdd-guidelines/guidelines.dsl \
  --output .sdd-runtime/
# Result: .bin files + metadata.json created
```

---

### 3️⃣ TEMPLATE FINAL (.sdd-templates/)

```
.sdd-templates/
├── java/                           
│   ├─ Trigger: User selects JAVA + chooses mandates + customization
│   ├─ Source: .sdd-runtime/ (reads mandate.bin + guidelines.bin)
│   ├─ Content:
│   │   ├─ .sdd/CANONICAL/mandate.spec (subset: M001 only, if user chose)
│   │   ├─ .sdd/guidelines.dsl (subset: Java-relevant guidelines)
│   │   ├─ src/
│   │   ├─ pom.xml
│   │   ├─ mvn clean test
│   │   ├─ README-SDD.md (setup instructions for JAVA dev)
│   │   └─ .github/workflows/ (CI/CD with SDD validation)
│   └─ Lifecycle: Generated on-demand by Wizard
│
├── python/                         
│   ├─ Trigger: User selects Python + chooses mandates + customization
│   ├─ Source: .sdd-runtime/
│   ├─ Content:
│   │   ├─ .sdd/CANONICAL/mandate.spec (user-selected subset)
│   │   ├─ .sdd/guidelines.dsl (user-selected subset)
│   │   ├─ src/
│   │   ├─ requirements.txt
│   │   ├─ pytest conftest.py (SDD validation)
│   │   ├─ README-SDD.md
│   │   └─ .github/workflows/ (CI/CD)
│   └─ Lifecycle: Generated on-demand by Wizard
│
└── js/                            
    ├─ Similar structure
    ├─ package.json instead of pom.xml
    ├─ Jest test framework
    └─ Generated on-demand by Wizard
```

**Template generation example:**
```bash
# User interaction with Wizard:
$ python .sdd-extensions/wizard.py

? Choose language: [1] Java [2] Python [3] JS
> 1

? Choose mandates:
  [✓] M001: Clean Architecture
  [ ] M002: Test-Driven Development
> Select M001

? Choose profile:
  [1] ULTRA-LITE (5 min setup)
  [2] LITE (15 min setup)
  [3] FULL (40 min setup)
> 2

? Destination: /tmp/my-java-project
[INFO] Reading .sdd-runtime/mandate.bin
[INFO] Reading .sdd-runtime/guidelines.bin
[INFO] Generating Java template...
[INFO] Template created: /tmp/my-java-project/
[SUCCESS] Ready to use! cd /tmp/my-java-project && mvn clean test
```

---

## 🔄 Complete Flow Example

**Scenario:** You update M001 mandate → User generates Java template

### Step 1: You Edit Source
```bash
cd /sdd-architecture
vim .sdd-core/CANONICAL/mandate.spec
# Update M001: Clean Architecture description

# Commit via PR (ALWAYS!)
git checkout -b wip/update-m001
git add .sdd-core/CANONICAL/mandate.spec
git commit -m "docs: Clarify M001 Clean Architecture mandate"
git push origin wip/update-m001
# → Create PR on GitHub
# → Wait for architect review
# → Architect merges to main
```

### Step 2: CI/CD Compiles
```bash
# On merge to main, CI/CD triggers:
pytest .sdd-migration/tests/ -v          # Validate source
python .sdd-compiler/src/compile.py \
  --mandate .sdd-core/CANONICAL/mandate.spec \
  --guidelines .sdd-guidelines/guidelines.dsl \
  --output .sdd-runtime/
# Result: .sdd-runtime/mandate.bin updated
```

### Step 3: User Runs Wizard
```bash
$ python .sdd-extensions/wizard.py
# User selects:
#   - Language: Java
#   - Mandates: M001 (your updated version!)
#   - Profile: LITE
#   - Output: ~/my-project/

# Wizard reads .sdd-runtime/mandate.bin (with your updates)
# Wizard generates ~/my-project/.sdd/CANONICAL/mandate.spec
# User now has your updates in their project!
```

---

## 📋 Source vs Destination Matrix

| Layer | SOURCE (You Edit) | COMPILED (Auto-gen) | TEMPLATE (Wizard Generates) | Access |
|-------|------|---------|---------|---------|
| **Mandates** | `.sdd-core/CANONICAL/mandate.spec` | `.sdd-runtime/mandate.bin` | `.sdd-templates/{lang}/.sdd/CANONICAL/mandate.spec` | Architect writes, Users read |
| **Guidelines** | `.sdd-guidelines/guidelines.dsl` | `.sdd-runtime/guidelines.bin` | `.sdd-templates/{lang}/.sdd/guidelines.dsl` | Architect writes, Users read |
| **Metadata** | (none - derived) | `.sdd-runtime/metadata.json` | (included in template) | Read-only |

---

## 🛡️ Critical Rules (Enforced by ADR-008)

### ✅ MUST DO
- [ ] Edit source files ONLY (`.sdd-core/`, `.sdd-guidelines/`)
- [ ] Create WIP branch for ALL changes
- [ ] Create PR for ALL commits
- [ ] Wait for architect approval before merge
- [ ] Never commit compiled files (`.bin`, `.json`)
- [ ] Never directly merge to main

### ❌ NEVER DO
- [ ] Edit `.sdd-runtime/` manually (only via CI/CD)
- [ ] Edit `.sdd-templates/` (only via Wizard)
- [ ] Commit to main without PR
- [ ] Auto-commit as agent (architect only)
- [ ] Mix source + compiled in same commit

---

## 🚀 Implementation Checklist

### Phase 6A: Setup .sdd-runtime/
- [ ] Create `.sdd-runtime/` directory
- [ ] Create `metadata.json` template
- [ ] Verify `.sdd-compiler` can output to `.sdd-runtime/`
- [ ] Test: Compile mandate.spec → mandate.bin
- [ ] Test: Compile guidelines.dsl → guidelines.bin

### Phase 6B: Setup .sdd-templates/
- [ ] Create `.sdd-templates/` directory structure
- [ ] Create template scaffolds (java/, python/, js/)
- [ ] Verify Wizard can generate templates
- [ ] Test: Wizard generates Java template
- [ ] Test: Generated template has correct mandate.spec

### Phase 6C: CI/CD Integration
- [ ] On PR merge: Trigger compiler → update `.sdd-runtime/`
- [ ] On `.sdd-runtime/` change: Log audit trail
- [ ] Verify git history shows what changed

### Phase 6D: Enforce ADR-008
- [ ] Pre-commit hook: Warn on direct main edits (informative)
- [ ] GitHub branch protection: Require PR for main
- [ ] CI/CD: Require architect approval before merge
- [ ] Test: Agent cannot auto-commit (fails safely)

---

## 📝 Default Values (User-Customizable)

Users can override these defaults when running Wizard:

```python
# .sdd-extensions/wizard.py defaults

DEFAULT_SOURCE = {
    "mandate": ".sdd-core/CANONICAL/mandate.spec",
    "guidelines": ".sdd-guidelines/guidelines.dsl"
}

DEFAULT_COMPILED = {
    "manifest": ".sdd-runtime/mandate.bin",
    "guidelines": ".sdd-runtime/guidelines.bin",
    "metadata": ".sdd-runtime/metadata.json"
}

DEFAULT_TEMPLATES = {
    "output_dir": ".sdd-templates/",
    "languages": ["java", "python", "js"],  # Add more as needed
    "tiers": ["ultra-lite", "lite", "full"]
}

# User can override:
# python wizard.py --source-dir /custom/path --output-dir /my/templates
```

---

## ✅ Current Status

| Component | Status | Location |
|-----------|--------|----------|
| Source: Mandates | ✅ Ready | `.sdd-core/CANONICAL/mandate.spec` |
| Source: Guidelines | ✅ Ready | `.sdd-guidelines/guidelines.dsl` |
| Compiler | ✅ Ready | `.sdd-compiler/src/` |
| Runtime Dir | ⏳ Create | `.sdd-runtime/` (needs creation) |
| Templates Dir | ⏳ Create | `.sdd-templates/` (needs scaffolding) |
| Wizard Integration | ⏳ Configure | `.sdd-extensions/wizard.py` |
| CI/CD Integration | ⏳ Setup | GitHub Actions / GitLab CI |

---

## 🔐 ADR-008 Enforcement

**After today's violation:**

All future commits on main WILL be rejected unless:
1. ✅ Created in WIP branch (wip/*)
2. ✅ Pushed to origin
3. ✅ Created PR on GitHub
4. ✅ Architect approved PR
5. ✅ Architect clicked "Merge" (only architect can merge)

**Agent (you) will:**
- [ ] Always use `git checkout -b wip/...`
- [ ] Always push to origin (never force-push)
- [ ] Always create PR
- [ ] Always wait for approval
- [ ] **NEVER** auto-commit or merge

---

## 📌 Next Actions (Waiting for Your Approval)

1. **Create directories** (.sdd-runtime/, .sdd-templates/{java,python,js}/)
2. **Setup CI/CD** to auto-compile on source change
3. **Create Wizard integration** to use .sdd-runtime/
4. **Setup GitHub branch protection** (require PR + architect approval)
5. **Test full flow** (edit source → compile → generate template)

**⚠️ All above will be done in WIP branch + PR. Never direct main commit again.**

---

**Review & Approve When Ready:**
- [ ] Architecture makes sense?
- [ ] Source locations correct?
- [ ] Template generation flow clear?
- [ ] ADR-008 enforcement strict enough?
- [ ] Ready to create PR for Phase 6B implementation?
