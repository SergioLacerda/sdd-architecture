# Architecture Decision: No Symlinks Required

**Date:** 2026-04-19  
**Status:** DECIDED  
**Impact:** All new projects + agent onboarding  

---

## 📋 Context

Previous approach required symlinks:
```
projects/
└── rpg-narrative-server/
    └── docs/ia → symlink to ../spec-architecture/docs/ia
```

**Problems:**
- ❌ Fragile (breaks on different machines)
- ❌ Not portable (relative paths fail)
- ❌ Magic (unclear why symlink exists)
- ❌ Git-coupled (adds complexity)

---

## ✅ Decision: Use `.spec.config` Instead

**Single declarative configuration file:**

```ini
# .spec.config
[spec]
spec_path = ../spec-architecture  # ← ONE LINE solves everything
```

**Benefits:**
- ✅ Single source of truth (one file)
- ✅ Human-readable (INI format)
- ✅ Machine-readable (scripts parse it)
- ✅ Portable (works on any machine)
- ✅ Git-friendly (no symlinks)
- ✅ Discoverable (agents find it automatically)

---

## 🏗️ New Architecture

### Old Approach (Symlinks)
```
rpg-narrative-server/
├── docs/
│   ├── ia → ../../spec-architecture/docs/ia  (symlink)
│   └── [project docs]
└── tests/spec_validation/                    (local copy)
```

**Problems:**
- Symlink path hardcoded (breaks on move)
- Tests duplicated locally
- Fragile relative paths

### New Approach (.spec.config)
```
rpg-narrative-server/
├── .spec.config                    ← ⭐ EVERYTHING IS HERE
├── .github/copilot-instructions.md
├── .vscode/ai-rules.md
├── .cursor/rules/spec.mdc
├── docs/
│   └── [project docs only]
└── tests/
    ├── unit/                       (your tests)
    ├── integration/                (your tests)
    └── specs-ia-units/             ⭐ SPEC compliance tests
```

**Advantages:**
- One config file (not multiple symlinks)
- Declarative (what, not how)
- No magic
- Clear intent

---

## 🔄 How It Works

### Agent Join Workflow

```python
# 1. Agent reads .github/copilot-instructions.md
# 2. Instruction: "Read .spec.config"

config = configparser.ConfigParser()
config.read(".spec.config")

# 3. Get spec-architecture path
spec_path = config.get("spec", "spec_path")
spec_path = Path(spec_path).expanduser().resolve()

# 4. Verify it exists
assert (spec_path / "/EXECUTION/spec/CANONICAL/rules/ia-rules.md").exists()

# 5. Run setup
subprocess.run([sys.executable, spec_path / "docs/ia/SCRIPTS/setup-wizard.py"])

# 6. Agent follows AGENT_HARNESS protocol
# (Everything else is at spec_path)
```

**No symlinks needed. Everything is declarative.**

---

## 📁 What's Where?

| What | Where | Managed By |
|------|-------|-----------|
| SPEC rules | `spec-architecture/EXECUTION/spec/CANONICAL/` | spec-architecture |
| Project onboarding | `your-project/.github/copilot-instructions.md` | Template |
| Config | `your-project/.spec.config` | Template (edit spec_path) |
| Project tests | `your-project/tests/specs-ia-units/` | Your team |
| SPEC tests | `spec-architecture/tests/spec_validation/` | spec-architecture |

---

## 🚀 Implementation

### What Changed?

1. **spec-architecture** gets `.spec.config` (pointing to itself)
   ```ini
   spec_path = .
   ```

2. **Any new project** gets `.spec.config` (pointing to spec-architecture)
   ```ini
   spec_path = ../spec-architecture  # OR your path
   ```

3. **No symlinks anywhere** (except maybe optional convenience symlinks)

### For Existing Projects?

**Option A: Remove symlink (recommended)**
```bash
rm docs/ia
# Nothing replaces it - agents read .spec.config instead
```

**Option B: Keep symlink for convenience (optional)**
```bash
# Keep symlink but it's now optional
# Agents don't rely on it - they use .spec.config
```

---

## 🎯 Benefits Summary

| Aspect | Symlinks | .spec.config |
|--------|----------|-------------|
| Portability | ❌ Breaks on move | ✅ Works anywhere |
| Git coupling | ❌ Complex | ✅ Simple |
| Clarity | ❌ Magic | ✅ Declarative |
| Scalability | ❌ Per-project setup | ✅ One template |
| Maintenance | ❌ Multiple symlinks | ✅ One config |
| Human-readable | ❌ Need to check symlink | ✅ INI format |
| Machine-readable | ⚠️ Fragile | ✅ Robust |

---

## ✅ What Gets Committed?

```bash
your-project/
├── .spec.config                    ✅ Commit (config)
├── .github/
│   └── copilot-instructions.md     ✅ Commit (template)
├── .vscode/
│   └── ai-rules.md                 ✅ Commit (template)
├── .cursor/
│   └── rules/spec.mdc              ✅ Commit (template)
├── tests/specs-ia-units/
│   ├── __init__.py                 ✅ Commit
│   ├── README.md                   ✅ Commit
│   └── test_*.py                   ✅ Commit (your tests)
└── docs/ia                         ❌ .gitignore (if symlink exists)
```

---

## 🔗 One-Time Setup for spec-architecture

Move spec-architecture to be self-aware:

```bash
# In spec-architecture root
cat > .spec.config << 'EOF'
[spec]
spec_path = .
min_version = 2.1
EOF

git add .spec.config
git commit -m "🔧 Add .spec.config (points to self)"
```

---

## 🚀 New Project Template

When creating new project:

```bash
# 1. Copy .spec.config
cp /home/sergio/dev/spec-architecture/.spec.config your-project/

# 2. Edit spec_path ONLY
vi your-project/.spec.config
# Change: spec_path = ../spec-architecture (or your path)

# 3. Copy templates (all generic, no edits needed)
cp -r /home/sergio/dev/spec-architecture/templates/* your-project/

# 4. Commit
git add .
git commit -m "🔧 Initialize SPEC Architecture"
```

**That's it.** No symlink setup, no complexity.

---

## 📊 Comparison: Before vs After

### BEFORE (Symlinks)
```
Setup complexity: HIGH
- Create symlink: ln -s
- Verify path: correct?
- Move project: breaks
- New machine: fails

Onboarding: Manual
- "Edit docs/ia symlink"
- "Run setup script"
- Unclear where scripts are
```

### AFTER (.spec.config)
```
Setup complexity: LOW
- Copy .spec.config
- Edit one line (spec_path)
- Commit
- Done

Onboarding: Automatic
- Agent reads .spec.config
- Agent finds spec-architecture
- Agent runs setup from spec-architecture
- Clear, declarative
```

---

## 🎓 Why This Works

1. **Decoupling:** Projects don't assume directory structure
2. **Declarative:** "Where is spec-architecture?" answered in one file
3. **Scalable:** Same pattern works for any project
4. **Discoverable:** Agents find `.spec.config` automatically
5. **Portable:** Same file works on any machine (just edit spec_path)

---

## ✨ Result

**Old way:** Symlinks + relative paths = fragile, non-portable  
**New way:** One config file = robust, portable, scalable

**Principle:** Configuration > Magic Paths

---

**Decision Made:** 2026-04-19  
**Implementation:** In progress  
**Status:** RECOMMENDED for all new projects
