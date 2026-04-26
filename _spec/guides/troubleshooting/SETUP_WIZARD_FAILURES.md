# 🧙 SETUP WIZARD Failures — Troubleshooting Guide

**For:** Developers running `setup-wizard.py` and encountering errors  
**Time to Resolution:** 2-10 minutes (most cases)  
**Quick Test:** `python _core/.sdd-wizard/SCRIPTS/setup-wizard.py --test`

---

## 🎯 Quick Navigation

| Symptom | Cause | Fix | Time |
|---------|-------|-----|------|
| **ImportError: No module named 'questionary'** | Dependencies not installed | Run `pip install -e .[dev]` | 2 min |
| **Python version too old** | Python < 3.10 | Upgrade Python to 3.10+ | 5 min |
| **venv not activated** | Not in virtual environment | `source venv/bin/activate` (Linux/Mac) or `.\venv\Scripts\activate` (Windows) | 1 min |
| **File not found: SPECIALIZATIONS_CONFIG.md** | Config missing for project | Create config or use default | 3 min |
| **Wizard runs but doesn't save profile** | Permissions issue | Check ~/.dev-profile permissions | 2 min |
| **Timeout or hanging** | Slow system or stuck input | Ctrl+C and retry | 1 min |

---

## 📋 Common Errors & Fixes

### Error 1: ImportError - questionary module not found

**Symptom:**
```
$ python _core/.sdd-wizard/SCRIPTS/setup-wizard.py
ImportError: No module named 'questionary'
```

**Diagnosis (1 minute):**
```bash
# Step 1: Check if venv is active
which python
# Should show path like: /path/to/venv/bin/python
# If it shows system python, venv is NOT active

# Step 2: Check Python version
python --version
# Should be 3.10+

# Step 3: List installed packages
pip list | grep questionary
# Should show questionary in list
```

**Fix:**

**Option A: Install dependencies (recommended)**
```bash
# Activate venv first
source venv/bin/activate  # Linux/Mac
# OR
.\venv\Scripts\activate   # Windows

# Install all dev dependencies
pip install -e .[dev]
# This installs questionary + all other deps

# Verify
python _core/.sdd-wizard/SCRIPTS/setup-wizard.py
# Should now work
```

**Option B: Install questionary only**
```bash
pip install questionary
```

**Why it matters:**
questionary is used for interactive prompts in the wizard. Without it, the script can't ask questions.

---

### Error 2: Python version too old

**Symptom:**
```
$ python _core/.sdd-wizard/SCRIPTS/setup-wizard.py
SyntaxError: invalid syntax
# (or similar Python version incompatibility)
```

**Diagnosis (1 minute):**
```bash
python --version
# If: Python 3.9.x or lower → TOO OLD
# If: Python 3.10.x or higher → OK
```

**Fix:**

**On macOS:**
```bash
# Using Homebrew
brew install python@3.11

# Verify
python3.11 --version
```

**On Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv

# Verify
python3.11 --version
```

**On Windows:**
Download from python.org and install Python 3.11+

**After upgrading:**
```bash
# Create new venv with new Python
python3.11 -m venv venv
source venv/bin/activate
pip install -e .[dev]
python _core/.sdd-wizard/SCRIPTS/setup-wizard.py
```

---

### Error 3: venv not activated

**Symptom:**
```
$ python _core/.sdd-wizard/SCRIPTS/setup-wizard.py
ImportError: questionary not found
# But you installed it!
```

**Diagnosis (1 minute):**
```bash
# Check if venv is active
echo $VIRTUAL_ENV  # Linux/Mac
echo %VIRTUAL_ENV%  # Windows (in CMD)

# If empty or shows different path → venv not active
```

**Fix:**

**Linux/macOS:**
```bash
source venv/bin/activate
# Prompt should now show: (venv) $
```

**Windows (Command Prompt):**
```
.\venv\Scripts\activate.bat
REM Prompt should now show: (venv) C:\...
```

**Windows (PowerShell):**
```
.\venv\Scripts\Activate.ps1
# Prompt should now show: (venv) PS C:\...
```

**Verify:**
```bash
which python  # Linux/Mac
# OR
where python  # Windows (in CMD)

# Should show path within venv folder
```

---

### Error 4: File not found - SPECIALIZATIONS_CONFIG.md

**Symptom:**
```
$ python _core/.sdd-wizard/SCRIPTS/setup-wizard.py
Error: Config not found at docs/ia/custom/my-project/SPECIALIZATIONS_CONFIG.md
```

**Cause:**
Project-specific configuration file doesn't exist.

**Diagnosis (1 minute):**
```bash
ls -la docs/ia/custom/
# Check if your project folder exists
# Check if SPECIALIZATIONS_CONFIG.md exists in it
```

**Fix:**

**Option A: Use default project (rpg-narrative-server)**
```bash
# The wizard should auto-detect rpg-narrative-server
python _core/.sdd-wizard/SCRIPTS/setup-wizard.py

# If prompted for project name, just press Enter for default
```

**Option B: Create config for your project**
```bash
# Create project folder
mkdir -p docs/ia/custom/my-project

# Create config file
cat > docs/ia/custom/my-project/SPECIALIZATIONS_CONFIG.md << EOF
# SPECIALIZATIONS_CONFIG

PROJECT_NAME=my-project
LANGUAGE=python
ASYNC_FRAMEWORK=fastapi
MAX_CONCURRENT_ENTITIES=100
PRIMARY_DOMAIN_OBJECTS=campaigns,users,games
TEAM_SIZE=5
EOF

# Now run wizard
python _core/.sdd-wizard/SCRIPTS/setup-wizard.py
```

**Option C: Skip wizard, read docs directly**
```bash
# Just read the docs manually
cat docs/ia/guides/onboarding/AGENT_HARNESS.md
```

---

### Error 5: Profile not saved

**Symptom:**
```
✅ Profile saved to /home/user/.dev-profile
# But next time, profile not loaded
```

**Diagnosis (1 minute):**
```bash
# Check if profile file exists
cat ~/.dev-profile
# Should show saved preferences

# Check file permissions
ls -la ~/.dev-profile
# Should be readable (r--) for owner
```

**Fix:**

**Option A: Check file permissions**
```bash
# Make file readable
chmod 644 ~/.dev-profile

# Retry wizard
python _core/.sdd-wizard/SCRIPTS/setup-wizard.py --load-profile
```

**Option B: Delete and recreate profile**
```bash
rm ~/.dev-profile

# Run wizard again (will create new profile)
python _core/.sdd-wizard/SCRIPTS/setup-wizard.py
```

**Option C: Manual profile creation**
```bash
cat > ~/.dev-profile << EOF
PATH=A
CONTEXT=Quick
EXPERIENCE=Familiar
EOF

# Now load it
python _core/.sdd-wizard/SCRIPTS/setup-wizard.py --load-profile
```

---

## 🧪 Test Mode

**To verify setup-wizard works without user input:**

```bash
python _core/.sdd-wizard/SCRIPTS/setup-wizard.py --test

# Output:
# ✅ Questionnaire logic: PASS
# ✅ Doc loading: PASS
# ✅ Profile saving: PASS
# ✅ All tests passed
```

**When to use:**
- After fresh Python/venv setup (verify everything works)
- In CI/CD (automated validation)
- Troubleshooting (isolate the failure)

---

## 🔧 Developer Commands

**Run wizard interactively:**
```bash
python _core/.sdd-wizard/SCRIPTS/setup-wizard.py
```

**Run with mock responses (for testing):**
```bash
python _core/.sdd-wizard/SCRIPTS/setup-wizard.py --test
```

**Load previous profile:**
```bash
python _core/.sdd-wizard/SCRIPTS/setup-wizard.py --load-profile
```

**View timing information:**
```bash
python _core/.sdd-wizard/SCRIPTS/setup-wizard.py 2>&1 | grep -i "seconds"
# Shows how long each phase took
```

---

## 📊 Status: Implementation Details

**Current Wizard Capabilities:**
- ✅ Interactive questionnaire (PATH A/B/C/D selection)
- ✅ Auto-loads relevant documentation
- ✅ Saves user profile for faster re-runs
- 🚀 Timing measurement (measures setup duration)
- 🚀 --test mode (validates without user input)

**PHASE 2 Additions:**
- 🎯 Timing decorator: Logs `setup_wizard_seconds: X`
- 🎯 --test mode for CI/CD validation
- 🎯 Integration to spec-enforcement.yml

---

## 🚨 Emergency Recovery

**If wizard completely breaks:**

```bash
# Skip wizard, read docs manually
cat docs/ia/guides/onboarding/AGENT_HARNESS.md

# Follow PHASE 1-7 manually:
# 1. Read constitution.md (3 min)
# 2. Read ia-rules.md (2 min)
# 3. Take VALIDATION_QUIZ (5 min)
# ... etc
```

**Or ask for help:**
```bash
# Slack message:
"setup-wizard.py fails with: [paste error]
Platform: [Windows/Mac/Linux]
Python: [version]
Help?"
```

---

## 🔗 Related Docs

- [AGENT_HARNESS.md](../onboarding/AGENT_HARNESS.md) — Main entry point
- [setup-wizard.py](../../../SCRIPTS/setup-wizard.py) — Source code
- [Emergency Procedures](../emergency/) — If all else fails

---

**Last Updated:** 2026-04-19  
**Status:** Complete (v1.0)  
**Test:** `python _core/.sdd-wizard/SCRIPTS/setup-wizard.py --test`
