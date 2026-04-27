# 🤖 AI Agent Integration Guide

*How to understand and integrate with the SDD Wizard*

---

## 🎯 Quick Overview

The SDD Wizard is a **7-phase orchestrator** that:
1. Validates governance specifications
2. Loads compiled artifacts
3. Filters rules by user preferences  
4. Generates complete project structures

This guide explains how AI agents can **understand, invoke, and bridge** the wizard workflow.

---

## 📍 What is the Wizard?

**Location:** `_core/.sdd-wizard/src/wizard.py`  
**Entry Point:** `./wizard.sh` (wrapper script)  
**Purpose:** Transform governance specifications → Executable projects

### The 7 Phases (High-Level)

```
Phase 1: Validate SOURCE (.sdd-core/) → Check syntax
Phase 2: Load COMPILED (.sdd-runtime/) → Deserialize artifacts
Phase 3: Filter Mandates → User selects which rules apply
Phase 4: Filter Guidelines → Filter by language/user choice
Phase 5: Apply Template → Copy & customize scaffolds
Phase 6: Generate Project → Create directory structure
Phase 7: Validate Output → Verify generated files
```

---

## 🧠 How AI Understands Each Phase

### Phase 1: Validate SOURCE
**What:** Check .sdd-core/ has valid mandate.spec + guidelines.dsl  
**Input:** File paths  
**Output:** ✅ Valid or ❌ Errors  
**AI Understanding:** "Architect specifications exist and are syntactically correct"

### Phase 2: Load COMPILED
**What:** Deserialize .sdd-runtime/mandate.bin + guidelines.bin  
**Input:** Binary/JSON artifacts  
**Output:** Python dicts  
**AI Understanding:** "Pre-compiled governance is available and ready to use"

### Phase 3-4: Filter
**What:** Keep only rules user selected + filter by language  
**Input:** All mandates + guidelines  
**Output:** Filtered subset  
**AI Understanding:** "Apply user preferences to governance rules"

### Phase 5-7: Generate & Validate
**What:** Create files + verify integrity  
**Input:** Filtered rules + template scaffolds  
**Output:** Complete project  
**AI Understanding:** "Transform rules into executable code"

---

## 🔄 How to Invoke the Wizard

### Mode 1: Interactive (User-Guided)

```bash
./wizard.sh
# Asks: Language? Mandates? Output location?
# Then runs phases 1-7 automatically
```

**When AI receives this flow:**
1. User runs `./wizard.sh`
2. Wizard asks questions
3. User answers
4. Wizard executes phases 1-7
5. Project is created
6. User starts developing

**AI's role:** Can monitor logs, suggest next steps, help with generated code

### Mode 2: Non-Interactive (Automated)

```bash
./wizard.sh \
  --language python \
  --mandates M001,M002 \
  --output ~/my-project/
```

**When AI uses this:**
```python
import subprocess

result = subprocess.run([
    "./wizard.sh",
    "--language", "python",
    "--mandates", "M001",
    "--output", "/tmp/test-project",
    "--verbose"
], cwd="/home/sergio/dev/sdd-architecture")

# AI can parse output and verify success
if result.returncode == 0:
    print("✅ Project generated successfully")
else:
    print("❌ Wizard failed, parse errors")
```

### Mode 3: Test Phases (For Understanding)

```bash
./wizard.sh --test-phases 1-2
# Run only phases 1-2 (validate + load)
# Useful for debugging
```

**When AI tests phases:**
```bash
# Test each phase individually
python3 _core/.sdd-wizard/src/wizard.py --test-phases 1
python3 _core/.sdd-wizard/src/wizard.py --test-phases 1-3
python3 _core/.sdd-wizard/src/wizard.py --test-phases 1-7
```

---

## 🌱 Seedling Integration

Seedlings are **local IDE configurations** that help AI agents and IDEs understand the SDD project structure.

### Where Seedlings Live

```
.vscode/
├── README.md                           ← VS Code documentation
├── health-check.md                     ← Semantic trigger detection
└── extensions/                         ← Recommended extensions

.cursor/
├── README.md                           ← Cursor documentation
├── rules/
│   ├── health-check.md                 ← Agent Handshake Protocol
│   └── spec.mdc                        ← Cursor-specific rules
└── settings.json                       ← IDE settings

.ia/
├── README.md                           ← AI agent documentation
├── system-prompt.md                    ← Universal AI instructions
└── .copilot-instructions.md            ← Copilot native format

.github/
├── workflows/                          ← 10 automated workflows
├── copilot-instructions.md             ← Copilot GitHub integration
└── pull_request_template.md            ← PR guidelines
```

### How Seedlings Collaborate

```
Developer runs: ./wizard.sh
        ↓
Wizard asks: Language? Mandates? Output?
        ↓
Seedlings detect: "User is using IDE X"
        ↓
Seedling loads: Health check rules
        ↓
Seedling validates: Project structure
        ↓
Seedling suggests: Next steps based on health
```

### Example: Health Check Integration

**File:** `.cursor/rules/health-check.md`

```
When user types: "estou conectado?" (am I connected?)
Cursor detects: "Technical context + project reference"
Cursor runs: python _core/agent_handshake.py --mode=silent
Result: 🟢 HEALTHY | Confidence: 92%
Cursor responds: "Yes, your SDD setup is fully operational"
```

**AI's understanding:** Seedlings allow **implicit validation** without user asking for it.

---

## 🎯 Template Generation Flow

### The Complete Flow

```
User Input (language, mandates)
        ↓
Phase 1: Validate SOURCE
  ├─ Read: .sdd-core/mandate.spec
  ├─ Read: .sdd-core/guidelines.dsl
  └─ Validate: Syntax correct? ✓
        ↓
Phase 2: Load COMPILED
  ├─ Read: .sdd-runtime/mandate.bin
  ├─ Read: .sdd-runtime/guidelines.bin
  └─ Deserialize: Python dicts ready ✓
        ↓
Phase 3-4: Filter
  ├─ Filter mandates: Keep M001 (user selected)
  ├─ Filter guidelines: Keep G01-G50 (language=python)
  └─ Result: Filtered governance ✓
        ↓
Phase 5: Apply Template
  ├─ Copy: .sdd-wizard/templates/python/
  ├─ Substitute: Placeholders {language}, {mandates}
  └─ Result: Customized scaffold ✓
        ↓
Phase 6: Generate Project
  ├─ Create: ~/my-project/
  ├─ Write: All project files
  └─ Result: Complete structure ✓
        ↓
Phase 7: Validate Output
  ├─ Verify: All files exist
  ├─ Check: Integrity
  └─ Result: Ready to use ✓
        ↓
Output: ~/my-project/.sdd/CANONICAL/
  ├─ mandate.spec (filtered)
  ├─ guidelines.dsl (filtered by language)
  ├─ metadata.json (audit trail)
  └─ All templates applied
```

---

## 💡 AI Integration Examples

### Example 1: Monitor Wizard Execution

```python
import subprocess
import json
from pathlib import Path

# Run wizard
result = subprocess.run(
    ["./wizard.sh", "--language", "python", "--verbose"],
    capture_output=True,
    text=True,
    cwd="/path/to/sdd-architecture"
)

# Parse output
if "Phase 7: Validate Output" in result.stdout:
    print("✅ All phases completed")
    
    # Check generated project
    project_path = Path("/path/to/generated/project")
    if (project_path / ".sdd" / "CANONICAL").exists():
        print("✅ Specifications found")
        
        # Read metadata for audit trail
        metadata = json.load(open(project_path / ".sdd" / "metadata.json"))
        print(f"Generated at: {metadata['generated_at']}")
        print(f"Mandates: {metadata['user_selections']['mandates_chosen']}")
```

### Example 2: Bridge Wizard for User

```python
def run_wizard_for_user(language, mandates, output_dir):
    """AI bridges wizard execution and explains what happened"""
    
    import subprocess
    
    cmd = [
        "./wizard.sh",
        "--language", language,
        "--mandates", ",".join(mandates),
        "--output", output_dir,
        "--verbose"
    ]
    
    print(f"🧙 Running wizard with:")
    print(f"  Language: {language}")
    print(f"  Mandates: {', '.join(mandates)}")
    print(f"  Output: {output_dir}")
    print()
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Project generated successfully!")
        print()
        print("Next steps:")
        print(f"1. cd {output_dir}")
        print("2. cat .sdd/CANONICAL/mandate.spec")
        print("3. make test")
    else:
        print("❌ Wizard failed:")
        print(result.stderr)
        return None
    
    return output_dir
```

### Example 3: Parse Generated Metadata

```python
import json
from pathlib import Path

project_dir = Path("/path/to/generated/project")
metadata_file = project_dir / ".sdd" / "metadata.json"

if metadata_file.exists():
    metadata = json.load(open(metadata_file))
    
    print("📊 Project Metadata:")
    print(f"  Version: {metadata['version']}")
    print(f"  Generated: {metadata['generated_at']}")
    print(f"  Language: {metadata['user_selections']['language']}")
    print(f"  Mandates: {metadata['user_selections']['mandates_chosen']}")
    print(f"  Source Commit: {metadata['source_commit_hash']}")
    print()
    print("This metadata proves the project came from verified governance!")
```

---

## 🔍 Key Files for AI Integration

| File | Purpose | When AI Reads It |
|---|---|---|
| `wizard.py` | Core orchestrator | Understanding workflow |
| `interactive_mode.py` | User questionnaire | Understanding prompts |
| `.sdd-runtime/mandate.bin` | Compiled mandates | Phase 2 (load) |
| `.sdd-wizard/templates/` | Project scaffolds | Phase 5 (apply) |
| `.sdd/metadata.json` | Audit trail | After generation |
| `.cursor/rules/health-check.md` | Semantic rules | IDE integration |

---

## 🚀 Advanced Integration

### Running Phases Individually

```bash
# Phase 1 only: Validate
python3 _core/.sdd-wizard/src/wizard.py --test-phases 1

# Phase 1-2: Validate + Load
python3 _core/.sdd-wizard/src/wizard.py --test-phases 1-2

# All phases
python3 _core/.sdd-wizard/src/wizard.py --test-phases 1-7
```

### Debugging Phases

```bash
# Verbose output for debugging
./wizard.sh --verbose

# Dry-run (preview without creating files)
./wizard.sh --language python --dry-run

# Test with specific mandates
./wizard.sh --mandates M001,M002 --verbose
```

### Custom Integration

```python
# Import wizard directly
import sys
sys.path.insert(0, "_core/.sdd-wizard/src")

from wizard import WizardOrchestrator

# Create orchestrator
wizard = WizardOrchestrator(repo_root="/path/to/sdd-architecture")

# Run specific phase
success, report = wizard.run_phase_1()
if success:
    print(f"✅ Phase 1: {report}")
else:
    print(f"❌ Phase 1 failed")

# Run full pipeline
success = wizard.run_full_pipeline(
    language="python",
    mandates=["M001"],
    output_dir="/tmp/test-project"
)
```

---

## 🤖 How to Work with CI/CD Automation

The SDD Framework runs **10 GitHub Actions workflows** that validate every push and PR. As an AI agent, you should understand these workflows when helping with development.

### The 10 Workflows (For AI Understanding)

**Quality Gates (must pass before merge):**
1. **Health Check** - Validates 10 system checks (Git, structure, governance, Python, dependencies)
2. **Tests** - Runs 124 tests across Python 3.8-3.12 (must have 100% pass rate)
3. **Lint** - Code quality checks (pylint, mypy, black, type hints)
4. **Governance Enforce** - Validates 4 immutable mandates + 151 guidelines
5. **Validate Workflows** - Ensures all workflow YAML is syntactically correct

**Monitoring & Reporting:**
6. **Compliance Report** - Daily dashboard of governance metrics
7. **Integration** - Tests wizard, compiler, CLI integration end-to-end
8. **Dependencies** - Weekly security scan for package vulnerabilities

**Deployment:**
9. **Docs** - Auto-generates documentation (pushed to main only)
10. **Release** - Builds releases, publishes to PyPI (tag-based)

### When You Suggest Code Changes

**Check these before suggesting code:**
1. Will it break any of the 10 workflows?
2. Does it maintain 100% test coverage?
3. Does it comply with 4 immutable mandates?
4. Does it follow the 151 guidelines for the language?

**Example concern:**
```
❌ BAD: Suggesting code that disables tests
   "Skip this test for now with @skip"
   
✅ GOOD: Fix the root cause first
   "Let's make the test pass by fixing the logic"
```

### How CI/CD Integrates with Wizard

The wizard system passes through CI/CD gates:
1. **Development** - You write code locally, run pre-commit checks
2. **Push** - All 10 workflows run automatically
3. **PR Review** - Workflows show status (all must pass)
4. **Merge** - Code integrated only if all workflows pass
5. **Production** - Docs and releases auto-generated

### Pre-Push Hook (Local)

Before pushing, users see:
```
[PRE-PUSH] Starting final validation before push...
→ Running full health check (fresh, no cache)...
✓ Health check passed (10/10)
→ Verifying governance enforcement level...
✓ Enforcement mode: STRICT
→ Checking compliance percentage...
✓ Fully compliant (100%)
[PRE-PUSH] All checks passed. Push allowed.
```

**If it fails, suggest:**
```bash
# Run locally to see what failed
python3 _core/health_check.py --verbose
python3 _core/run-all-tests.py
python3 _core/tools/governance_compliance.py --verify
```

### ⚠️ Git Hooks: Framework vs Client Projects

**SDD Architecture framework hook:**
- Validates governance + health
- Blocks push if governance compliance fails
- Located: `.git/hooks/pre-push` (framework repo)

**Client project hooks (future):**
- Should validate project quality ONLY
- Should NOT validate framework governance
- Should NOT block for SDD Architecture compliance
- Example: Validates tests pass, lint OK, but not SDD mandates

---

## 📚 Related Documentation

- [README.md](README.md) — Main entry point
- [readme-detailed.md](readme-detailed.md) — 7-phase technical details
- [.github/workflows/](.github/workflows/) — All 10 workflow definitions
- [_core/.sdd-wizard/WORKFLOW_FLOW.md](_core/.sdd-wizard/WORKFLOW_FLOW.md) — Complete orchestration
- [_core/.sdd-wizard/AI_AGENT_GUIDE.md](_core/.sdd-wizard/AI_AGENT_GUIDE.md) — Detailed AI guide
- [.cursor/README.md](.cursor/README.md) — Cursor IDE integration

---

**For AI Agents:** This guide lets you understand, invoke, and integrate with the wizard. Use it when:
- Implementing wizard support in your tool
- Bridging wizard execution for users
- Understanding project generation flow
- Integrating with seedlings

*Last Updated: April 26, 2026*
