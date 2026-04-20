# ✅ INTEGRATION — 5-Step Checklist

**Quick reference for adding your project to SDD framework**

**Total time:** 20-30 minutes (5 min buffer = 30 min guaranteed)

---

## 📋 The Process

```
STEP 1: Setup
   ↓ (5 min)
STEP 2: Templates
   ↓ (5 min)
STEP 3: Config
   ↓ (2 min)
STEP 4: Validate
   ↓ (5 min)
STEP 5: Commit
   ↓ (3 min)
✅ DONE
```

---

## ✅ Step 1: Setup Project Structure

**Goal:** Prepare your project directory

```bash
# Navigate to your project
cd /path/to/your-project

# Verify git is initialized
git status

# Create directories (if not present)
mkdir -p .github .vscode .cursor scripts .ai
```

**Expected result:**
```
your-project/
├── .github/
├── .vscode/
├── .cursor/
├── scripts/
├── .ai/
└── (existing project files)
```

**Status check:**
```bash
ls -la | grep "^\."
# Should show: .github, .vscode, .cursor, scripts, .ai
```

**Stuck?** → See [STEP_1.md](./STEP_1.md)

---

## ✅ Step 2: Copy Templates

**Goal:** Copy SDD template files to your project

```bash
# From sdd-architecture root:
cd /path/to/sdd-architecture

# Copy all templates
cp -r INTEGRATION/templates/* /path/to/your-project/
```

**Expected files copied:**
```
.spec.config              → project root
.github/copilot-instructions.md
.vscode/ai-rules.md
.vscode/settings.json
.cursor/rules/spec.mdc
.pre-commit-config.yaml   → project root
scripts/setup-precommit-hook.sh
.ai/README.md
```

**Verify:**
```bash
cd /path/to/your-project
cat .spec.config | head -5
# Should show: spec_path = ...
```

**Stuck?** → See [STEP_2.md](./STEP_2.md)

---

## ✅ Step 3: Configure .spec.config

**Goal:** Point to sdd-architecture (2 lines to edit!)

```bash
cd /path/to/your-project

# Open .spec.config
nano .spec.config  # or your favorite editor

# Edit lines:
# Line 2: spec_path = ../sdd-architecture
#         (or absolute path if not sibling directory)
```

**Example .spec.config:**
```ini
[spec]
spec_path = ../sdd-architecture
# spec_path = /home/sergio/dev/sdd-architecture  # alternative: absolute path
```

**Verify:**
```bash
cat .spec.config | grep spec_path
# Should show: spec_path = ../sdd-architecture
```

**Stuck?** → See [STEP_3.md](./STEP_3.md)

---

## ✅ Step 4: Run Validation

**Goal:** Verify everything is setup correctly

```bash
cd /path/to/your-project

# Run PHASE 0 setup
python $(grep spec_path .spec.config | cut -d' ' -f3)/docs/ia/SCRIPTS/phase-0-agent-onboarding.py
```

**Expected output:**
```
✅ Framework verified
✅ .ai/context-aware/ created
✅ .ai/runtime/ created
VALIDATION_QUIZ: Pass 8/10 questions (≥80%)
```

**After script:**
```bash
ls -la .ai/
# Should show: context-aware/, runtime/

cat .ai/runtime/search-keywords.md
# Should have 703 lines
```

**Stuck?** → See [STEP_4.md](./STEP_4.md)

---

## ✅ Step 5: Commit to Git

**Goal:** Save all changes to version control

```bash
cd /path/to/your-project

# Stage all new files
git add .spec.config .github/ .vscode/ .cursor/ .pre-commit-config.yaml scripts/ .ai/

# Verify what's staged
git status

# Commit
git commit -m "feat: Integrate SDD framework governance"
```

**Expected result:**
```
[main xxxxxxx] feat: Integrate SDD framework governance
 X files changed, XXX insertions(+)
 create mode 100644 .spec.config
 create mode 100644 .github/copilot-instructions.md
 ...
```

**Verify:**
```bash
git log -1 --oneline
# Should show your commit

git status
# Should show: On branch main, nothing to commit
```

**Stuck?** → See [STEP_5.md](./STEP_5.md)

---

## 🎉 Complete!

After all 5 steps:

- ✅ `.spec.config` points to sdd-architecture
- ✅ All SDD templates are in place
- ✅ `.ai/` infrastructure created
- ✅ Changes committed to git
- ✅ **Your project is ready for development with SDD AGENT_HARNESS**

---

## 🚀 What's Next?

Your developers can now:

1. Read: [EXECUTION/_START_HERE.md](../EXECUTION/_START_HERE.md)
2. Follow: AGENT_HARNESS 7-phase workflow
3. Implement: Features using governance rules

---

## 🆘 Troubleshooting Quick Links

| Problem | Solution |
|---------|----------|
| `.spec.config` not found | Check: did Step 2 copy work? Try manual: `cp INTEGRATION/templates/.spec.config .` |
| Python script fails | Check: `cat .spec.config` spec_path is correct |
| `.ai/` not created | Run Step 4 again, capture full output |
| Can't commit | Check: `git status`, make sure `.spec.config` is staged |
| Still stuck | See full guides: STEP_1_*.md through STEP_5_*.md |

---

## 📊 Progress Tracking

- [ ] Step 1: Project structure ready
- [ ] Step 2: Templates copied
- [ ] Step 3: .spec.config configured
- [ ] Step 4: Validation passed
- [ ] Step 5: Committed to git

✅ **All done?** Your project is now part of SDD framework!

---

**Estimated time:** 30 minutes  
**Complexity:** Simple (follow steps)  
**Next:** Developers read EXECUTION/_START_HERE.md
