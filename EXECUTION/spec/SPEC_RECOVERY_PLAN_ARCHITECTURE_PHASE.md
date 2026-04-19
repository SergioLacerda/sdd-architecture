# 📐 REVISED SPEC RECOVERY PLAN v2.2 — Architecture Phase

**Date:** April 19, 2026  
**Context:** Architecture design phase (before real development)  
**Focus:** Complete documentation + Contracts + Checkpoints  
**Timeline:** This week (architecture stabilization)

---

## 🎯 PRIORITY REFRAME

### What Changed

```
OLD MINDSET (v1.0):
  "Ship 4 features with tests + CI/CD integration"
  → Premature optimization for production

NEW MINDSET (Architecture Phase):
  "Build unambiguous contracts + checkpoints"
  "Define decision gates + emergency procedures"
  "Create context for AI agents (not humans)"
  → Preparation for real development
```

### Your Key Points Acknowledged

✅ **Gaps will be filled during real development**
- Metrics collection: Real usage data
- Multi-project scaling: Second project in production
- CI/CD integration: Applied to final product

✅ **Focus NOW is architecture clarity**
- Complete ambiguous documentation
- Define contracts between components
- Create checkpoints for validation
- Establish emergency/rollback procedures

✅ **AI agents must understand SPEC as law**
- setup-wizard.py = how agents load context
- validate-ia-first.py = blocking validation rule
- generate-specializations.py = cache strategy per project

---

## 🔧 BUG #1: AMBIGUOUS OPERATIONAL PARAMETERS

### Problem → Solution Framework

#### A) setup-wizard.py — WHO EXECUTES? WHEN?

**Current Gap:**
```
setup-wizard.py exists but:
  ❓ Who calls it? Manual? Hook? Agent?
  ❓ When should it be called?
  ❓ What context does it initialize?
  ❓ What happens if it fails?
```

**Architecture-Phase Solution:**

Create: `/docs/ia/CANONICAL/specifications/agent-context-initialization.md`

```markdown
# Agent Context Initialization Contract

## Overview
When an AI agent begins work, it MUST initialize context per SPEC.
`setup-wizard.py` is the canonical tool for this.

## Entry Point: setup-wizard.py

### Invocation
Agent runs ONCE at session start:
```bash
python docs/ia/SCRIPTS/setup-wizard.py \
  --task-type [bug-fix|feature|complex|parallel] \
  --project [project-name] \
  --output-format [json|markdown|minimal]
```

### Contract: What Agent Receives

```json
{
  "context": {
    "mandatory_docs": ["ia-rules.md", "constitution.md"],
    "optional_docs": ["ADR-001.md", "..."],
    "contextual_docs": {
      "bug-fix": ["REALITY/limitations/known_issues.md"],
      "feature": ["CANONICAL/architecture.md"],
      "complex": ["CANONICAL/decisions/ADR-*.md"]
    }
  },
  "execution_rules": {
    "must_read_before_coding": ["ia-rules.md"],
    "checkpoints_required": ["compliance_check", "spec_validation"],
    "blocking_violations": ["path_outside_custom/", "project_name_in_CANONICAL/"]
  },
  "emergency_contact": {
    "coordination_doc": "docs/ia/development/execution-state/_current.md",
    "conflict_resolution": "ALWAYS ask user before proceeding"
  }
}
```

### Contract: What Happens on Failure

```
Exit Code 1: Missing SPECIALIZATIONS_CONFIG.md
  → Fallback: Use project defaults
  → Agent action: Load QUICK_START.md instead
  → Log: "setup-wizard failed, using defaults"

Exit Code 2: Incompatible Python version
  → Fallback: None
  → Agent action: STOP, ask user for environment fix
  → Message: "Python 3.10+ required"

Exit Code 3: Custom project not recognized
  → Agent action: Verify project path
  → Fallback: Use CANONICAL docs only
```

### Validation Checkpoint

Before writing ANY code:
```bash
# Agent validates setup was successful
python -c "
  import sys
  setup_ok = check_setup_wizard_output()
  if not setup_ok:
    print('SETUP FAILED - cannot proceed')
    sys.exit(1)
"
```

## Why This Matters for Architecture

`setup-wizard.py` output = **CONTRACT between SPEC and agents**.
If agent gets this, it knows:
  ✅ Which docs are mandatory
  ✅ Which violations are blocking
  ✅ What checkpoints to hit
  ✅ When to ask user (emergency contact)

Without this contract: Agents guess (wrong choices).
With this contract: Agents make deterministic decisions.
```

**Status:** ⏳ TODO (Create this spec, test with mock agent)

---

#### B) validate-ia-first.py — WHEN IS IT BLOCKING?

**Current Gap:**
```
validate-ia-first.py exists but:
  ❓ Is it blocking in pre-commit?
  ❓ Is it blocking in CI/CD?
  ❓ What triggers auto-fix mode?
  ❓ Is auto-fix safe to apply?
```

**Architecture-Phase Solution:**

Create: `/docs/ia/CANONICAL/specifications/documentation-validation-contract.md`

```markdown
# Documentation Validation Contract

## IA-FIRST Format Enforcement

### When validate-ia-first.py Runs

1. **Pre-commit (AGENT MUST PASS)**
   ```bash
   # Trigger: Agent modifies any .md file
   validate-ia-first.py --audit [modified-files]
   
   Exit Code 0: ✅ All docs pass IA-FIRST rules
   Exit Code 1: ❌ BLOCKING - Fix required, cannot commit
   Exit Code 2: ⚠️ WARNING - Can force with --force (use sparingly)
   ```

2. **CI/CD (AGENT MUST PASS)**
   ```bash
   # Job: spec-validation-enforcement
   validate-ia-first.py --audit docs/ia/ --strict
   
   Failure = PR blocked (non-bypassable)
   Success = PR can merge
   ```

### The Rules

IA-FIRST format is non-negotiable:

```
Rule #1: Heading Hierarchy (H1 → H2 → H3 → Lists)
  ✅ # Title                    (one per file)
  ✅ ## Section                 (group related ideas)
  ✅ ### Subsection             (split complex ideas)
  ✅ - List items               (specific points)
  ❌ # Title, then ### Subsection (skip hierarchy = blocked)

Rule #2: Links ONLY in markdown format
  ✅ [text](path.md)
  ❌ `[text](path.md)`          (backticks = blocked)
  ❌ [[wikilink]]               (blocked)

Rule #3: Emoji markers for decisions
  ✅ ✅ Approved/done
  ✅ ❌ Rejected/invalid
  ✅ 🎯 Target state
  ✅ 🔴 Critical issue
  ✅ 🟡 Warning/attention needed

Rule #4: Complex ideas → Lists, NOT prose
  ✅ When to use setup-wizard:
     - New development session
     - After environment reset
     - When context lost
  ❌ Prose paragraph (4+ sentences = blocked)
```

### What Auto-Fix Does (--fix flag)

```
Safe operations (auto-applied):
  ✅ Add missing H1 header
  ✅ Fix heading hierarchy (H1 → H2 → H3)
  ✅ Remove backticks from links
  ✅ Add emoji markers (suggests, not auto)

Unsafe operations (require --force):
  ⚠️ Restructure entire doc
  ⚠️ Remove prose paragraphs
  ⚠️ Reorder sections significantly
```

### Decision Gate for Auto-Fix

```
When validate-ia-first.py --fix is called:

1. Dry-run: Show what would change
   ```bash
   validate-ia-first.py --fix --dry-run docs/ia/
   # Output: List of changes
   ```

2. User confirms: "Apply these changes?"
   ```
   If YES:
     - Apply changes
     - Commit with message: "🔧 IA-FIRST format auto-fix"
     - Note in _current.md (checkpoint)
   
   If NO:
     - Stop
     - Ask user to fix manually
   ```

3. After changes:
   ```bash
   validate-ia-first.py --audit docs/ia/
   # Must pass (exit 0)
   ```

## Why This Contract Matters

When agent (or human) modifies docs:
  ✅ Clear when changes are blocking
  ✅ Clear what auto-fix will do
  ✅ Clear when manual intervention needed
  ✅ Clear confirmation points
```

**Status:** ⏳ TODO (Create this spec, integrate to CI/CD job)

---

#### C) generate-specializations.py — CONFIG PATH? IDEMPOTENCY?

**Current Gap:**
```
generate-specializations.py exists but:
  ❓ Where does SPECIALIZATIONS_CONFIG.md live?
  ❓ Is it idempotent? (run 2x = same result?)
  ❓ What's cached? What's regenerated?
  ❓ Per-project cache strategy?
```

**Architecture-Phase Solution:**

Create: `/docs/ia/CANONICAL/specifications/project-specialization-contract.md`

```markdown
# Project Specialization Generation Contract

## Directory Structure Contract

```
/docs/ia/
├── SPECIALIZATIONS.template.md          ← Generic template
├── SCRIPTS/generate-specializations.py  ← Generator
└── custom/
    ├── rpg-narrative-server/
    │   ├── SPECIALIZATIONS_CONFIG.md     ← Project-specific config
    │   ├── specializations/
    │   │   ├── constitution-specific.md  ← Generated (read-only)
    │   │   ├── ia-rules-specific.md      ← Generated (read-only)
    │   │   └── index.md                  ← Generated (read-only)
    │   └── .specializations-cache       ← Idempotency checkpoint
    └── [other-project]/
        ├── SPECIALIZATIONS_CONFIG.md
        └── specializations/
            └── ...
```

## Config Location: /docs/ia/custom/[PROJECT]/SPECIALIZATIONS_CONFIG.md

Must contain:
```yaml
project:
  name: rpg-narrative-server
  domain: RPG Narrative Engine
  team_size: 3-5
  repo_url: github.com/user/rpg-narrative-server

scale:
  concurrent_entities: 50-200 campaigns
  users: 10-50 concurrent
  storage: PostgreSQL + ChromaDB

technology:
  language: Python 3.11+
  framework: FastAPI + discord.py
  database: PostgreSQL
  vector_store: ChromaDB + HNSW

domain_objects:
  - Campaign (game session container)
  - Character (player entity)
  - NPC (non-player character)
  - Event (narrative event)
  - Memory (context storage)
  - Message (discord message)
  - Thread (decision isolation)
```

## Invocation & Idempotency

### Generation Process

```bash
# From PROJECT root:
cd docs/ia/custom/rpg-narrative-server

# Run generator
python ../../../SCRIPTS/generate-specializations.py \
  --project rpg-narrative-server \
  --config SPECIALIZATIONS_CONFIG.md

# What happens:
1. Load SPECIALIZATIONS_CONFIG.md (required)
2. Load SPECIALIZATIONS.template.md (from parent)
3. Map template → project-specific
4. Generate: specializations/constitution-specific.md
5. Generate: specializations/ia-rules-specific.md
6. Generate: specializations/index.md
7. Create: .specializations-cache (checksum file)
8. Report: "Generated X files (Y bytes changed)"
```

### Idempotency Guarantee

```
Contract: Running twice = SAME RESULT

Checkpoint file: .specializations-cache
Content:
  timestamp: 2026-04-19T14:32:00Z
  config_hash: sha256(SPECIALIZATIONS_CONFIG.md)
  template_hash: sha256(SPECIALIZATIONS.template.md)
  files_generated: ["constitution-specific.md", "ia-rules-specific.md", "index.md"]
  file_checksums: {
    "constitution-specific.md": "sha256:...",
    "ia-rules-specific.md": "sha256:...",
    "index.md": "sha256:..."
  }

When running again:
  1. Check if SPECIALIZATIONS_CONFIG.md changed (hash compare)
  2. If unchanged: Use cache, skip regeneration ✅
  3. If changed: Regenerate all files
  4. Update cache file
  
Result: Idempotent (can run 10x, same output)
```

### Safety Gate

```bash
# Before running generator:
python ../../../SCRIPTS/generate-specializations.py \
  --project rpg-narrative-server \
  --dry-run \
  --verbose

# Output shows:
#   Config: SPECIALIZATIONS_CONFIG.md (valid ✅)
#   Template: ../SPECIALIZATIONS.template.md (v1.0)
#   Will generate: 3 files (247 KB)
#   Estimated time: 2.3 seconds
#   Changes vs cache:
#     - constitution-specific.md: +15 lines
#     - ia-rules-specific.md: -3 lines
#     - index.md: +1 line
#
# Question: Apply changes? (Y/n)
```

## Per-Project Cache Strategy

Agent learns: For project X, I can:
```
Generate fresh:
  python generate-specializations.py --project X --force

Use cache (faster):
  python generate-specializations.py --project X

Invalidate cache:
  rm .specializations-cache
  python generate-specializations.py --project X

Result: Agent optimizes context loading per project
```

## Why This Contract Matters

Agents understand:
  ✅ Where config lives (custom/[project]/)
  ✅ Generator is idempotent (safe to run multiple times)
  ✅ Cache strategy per project (optimization opportunity)
  ✅ Generated files are read-only (don't edit them)
  ✅ Checkpoint file tracks what was generated (diff future runs)
```

**Status:** ⏳ TODO (Implement cache mechanism, document per-project strategies)

---

## 📋 BUG #2: ZERO TESTES

### Reframing for Architecture Phase

You're correct: At architecture stage, testing is limited.

But we CAN create **architectural validation contracts**:

```markdown
# Architectural Compliance Tests (Design-Phase)

## Test Purpose
NOT "does feature work" (too early)
BUT "does architecture follow rules"

## Contract Tests (Executable Specifications)

### Test 1: SPEC Layer Isolation
```python
def test_canonical_has_no_project_names():
    """CANONICAL must be 100% generic."""
    for file in CANONICAL_FILES:
        content = read(file)
        for project in PROJECTS:
            assert project not in content, \
                f"Project '{project}' found in CANONICAL - VIOLATION"

def test_reality_must_project_scoped():
    """REALITY must be in custom/[project]/."""
    for project in PROJECTS:
        assert exists(f"custom/{project}/reality/")
        assert not exists(f"REALITY/{project}/"), \
            f"Root REALITY dir found - VIOLATION"
```

### Test 2: Specializations Are Valid
```python
def test_specializations_config_exists():
    """Each project must have SPECIALIZATIONS_CONFIG.md."""
    for project in PROJECTS:
        config = f"custom/{project}/SPECIALIZATIONS_CONFIG.md"
        assert exists(config), \
            f"Project {project} missing config"
        
        # Validate structure
        yaml = load_yaml(config)
        required = ["project", "scale", "technology"]
        assert all(k in yaml for k in required)

def test_generated_specializations_are_readonly():
    """Generated files must not be edited manually."""
    for project in PROJECTS:
        index_file = f"custom/{project}/specializations/index.md"
        content = read(index_file)
        assert "# AUTO-GENERATED" in content, \
            f"Generated file missing marker: {index_file}"
```

### Test 3: Emergency Procedures Are Documented
```python
def test_emergency_procedures_exist():
    """All 7 emergency scenarios must have runbooks."""
    procedures = [
        "EMERGENCY_PROCEDURES.md",
        "guides/operational/ADDING_NEW_PROJECT.md",
        "guides/operational/TROUBLESHOOTING_SPEC_VIOLATIONS.md",
        "guides/troubleshooting/SETUP_WIZARD_FAILURES.md",
        "guides/troubleshooting/VALIDATE_IA_FIRST_FAILURES.md",
    ]
    for proc in procedures:
        assert exists(f"docs/ia/{proc}"), \
            f"Missing emergency procedure: {proc}"
```

## Where These Live

```
tests/spec_validation/
├── test_layer_isolation.py      ← Layer contracts
├── test_specializations.py      ← Project contracts
├── test_emergency_procedures.py ← Operational contracts
└── test_ai_context.py           ← Agent context contracts
```

## Status

✅ Can write these NOW (architecture validation)
⏳ Implementation tests defer to real development
```

**Status:** ✅ Testable at architecture level (contracts + validation rules)

---

## 🚨 BUG #4: ZERO EMERGENCY PROCEDURES — MANDATORY FIX

### Your Requirements → Implementation

#### Rule 1: "SPEC Canônica é Absoluta"

Create: `/docs/ia/CANONICAL/specifications/spec-authority.md`

```markdown
# SPEC Authority & Immutability Contract

## Axiom 1: CANONICAL is Absolute Authority

```
CANONICAL/rules/ia-rules.md — IMMUTABLE LAW
  "Agents MUST enforce ia-rules.md"
  "Humans may QUESTION ia-rules.md"
  "But NOT ignore ia-rules.md"

CANONICAL/specifications/* — BINDING SPECIFICATIONS
  "Agents MUST follow specs"
  "Humans may REQUEST spec changes"
  "But changes require DECISION in ADRs"

custom/[project]/* — PROJECT-SPECIFIC (project team decision)
  "Agents adapt to project specializations"
  "Humans maintain project specializations"
```

## Axiom 2: Conflict Resolution is BLOCKING

When agent (or human) detects SPEC conflict:
```
Priority 1: Read entire ia-rules.md
Priority 2: Read relevant CANONICAL/specifications/*
Priority 3: Check custom/[project]/ for project-specific override
Priority 4: If still ambiguous → BLOCK and ALERT USER

NEVER guess. NEVER proceed without clarity.
```

## Axiom 3: All Changes Must Leave Audit Trail

Every modification to SPEC:
```
In git:
  commit message = explicit reason
  commit author = who decided

In docs:
  /docs/ia/development/execution-state/_current.md
    - What changed
    - Why it changed
    - Impact on active work
```
```

**Status:** ⏳ TODO (Create authority.md)

---

#### Rule 2: "Conflitos Graves → Travar e Solicitar Avaliação"

Create: `/docs/ia/guides/operational/CONFLICT_RESOLUTION.md`

```markdown
# Conflict Resolution Procedure

## When to Trigger

Agent detects: Different rules give CONFLICTING guidance

Example:
```
ia-rules.md says: "Always validate paths before modifying"
but
custom/rpg-narrative-server/context says: "Fast path for cache updates"

Result: CONFLICT (cannot follow both)
```

## Procedure

### Step 1: Agent Recognizes Conflict (5 min)

```python
# Agent pseudocode
if rule_A contradicts rule_B:
    print("CONFLICT DETECTED:")
    print(f"  Source A: {rule_A.source}")
    print(f"  Source B: {rule_B.source}")
    print(f"  Contradiction: {conflict_description}")
    print("")
    print("ACTION: Cannot proceed. Waiting for user...")
    BLOCK_EXECUTION()
```

### Step 2: Agent Escalates to User

Format:
```
🚨 SPEC CONFLICT DETECTED 🚨

I detected conflicting rules and cannot proceed safely.

Conflict:
  Rule A: [docs/ia/CANONICAL/rules/ia-rules.md line 45]
    "Always validate paths before modifying docs"
  
  Rule B: [docs/ia/custom/rpg-narrative-server/context.md]
    "Cache updates can skip validation for performance"
  
  Problem: I can't follow both. Which takes priority?

Suggested Resolution:
  Option 1: Rule A is universal (always validate)
  Option 2: Rule B is exception (cache updates are exempt)
  Option 3: New rule (create hybrid approach)

Decision needed from: User/Architect
Status: BLOCKED (waiting for user decision)

Checkpoint marker added to: docs/ia/development/execution-state/_current.md
```

### Step 3: User Decides

User responds with decision:
```
Decision: Rule A takes priority universally.
Reason: Consistency > Performance at this stage.
Action: Remove Rule B exception, or clarify it applies only to [specific case].

Next: Agent removes exception, updates docs, continues.
```

Or:

```
Decision: Rule B is valid exception (cache updates).
Reason: Performance critical for local development.
Action: Update Rule A to document this exception.

Next: Agent documents exception, continues.
```

### Step 4: Document in DECISIONS.md

```markdown
## Decision: Cache Update Validation Exception

Date: 2026-04-19
Requester: AI Agent (context loading)
Decision: Rule B (cache exception) takes priority over Rule A (validate all)

Rationale:
  - Local development performance > consistency for cache-only updates
  - Risk: Cached data could diverge from source
  - Mitigation: Validation still runs on next cache refresh

Status: Active
Review date: 2026-05-19 (re-evaluate if issues arise)
```

## Why This Matters

Without this procedure:
  ❌ Agent guesses (wrong choice, bugs introduced)
  ❌ Agent ignores both rules (chaos)

With this procedure:
  ✅ Agent escalates explicitly
  ✅ User makes informed decision
  ✅ Decision documented forever
  ✅ Same conflict recognized next time (reuse decision)
```

**Status:** ⏳ TODO (Create conflict-resolution.md)

---

#### Rule 3: "Checkpoints Quebram → Sinal para Rollback"

Create: `/docs/ia/guides/operational/CHECKPOINT_VALIDATION.md`

```markdown
# Checkpoint Validation & Rollback Contract

## What is a Checkpoint?

Checkpoint = Safe stopping point where SPEC is valid.

```
Checkpoint saved when:
  ✅ All validation passes
  ✅ SPEC layers intact
  ✅ No conflicts remain
  ✅ Audit trail complete

Checkpoint format:
  File: /docs/ia/development/execution-state/_current.md
  Content:
    timestamp: 2026-04-19T14:32:00Z
    state: SPEC v2.2 validated
    changed_files: ["WORLD_CLASS_REVIEW_V2.md", ...]
    status: ✅ READY FOR NEXT PHASE
```

## Checkpoint Validation Process

```bash
# Run validation:
python docs/ia/SCRIPTS/validate-spec-checkpoint.py

Output:
  Layer isolation: ✅ PASS
  Authority rules: ✅ PASS
  Emergency procedures: ✅ PASS
  Conflict detection: ✅ PASS
  
  Result: ✅ CHECKPOINT VALID
```

## If Checkpoint Breaks

### Scenario A: Validation Fails

```
[CHECKPOINT VALIDATION FAILED]

Issue: Layer isolation broken
  File: docs/ia/WORLD_CLASS_REVIEW_V2.md
  Problem: References "custom/rpg-narrative-server/" as if it's CANONICAL

Location: docs/ia/WORLD_CLASS_REVIEW_V2.md:542
  Text: "Apply this rule to all projects..."
  Error: Should say "Apply to custom/[project]/" not globally

Action needed:
  [ ] Fix file manually
  [ ] Or rollback to last checkpoint?

Recommendation: ROLLBACK (you changed 5 files, error could be subtle)
```

### Rollback Procedure

Agent detects checkpoint broken → Asks user:

```
🚨 CHECKPOINT INVALID 🚨

Last valid checkpoint: 2026-04-19T14:32:00Z
Current state broken (5 files modified)

Problem: Layer isolation rule violated

Options:
  1. ROLLBACK: Return to last checkpoint
     git checkout [COMMIT_HASH]
     (Lose 5 file changes, but return to valid state)
     
  2. FIX: Modify files to fix validation
     (Keep changes, fix validation errors)
     
  3. FORCE: Ignore validation (NOT RECOMMENDED)
     (Creates unstable checkpoint)

Recommended: ROLLBACK + careful retry

User decision needed: [1/2/3/?]
```

### User Confirms Rollback

```
User: "ROLLBACK, please"

Agent action:
  1. Stop current work
  2. Display what will be lost:
     - docs/ia/WORLD_CLASS_REVIEW_V2.md (11KB, 500 lines)
     - docs/ia/QUALITY_REGRESSION_ACTION_PLAN.md (15KB)
     - docs/ia/SPEC_AUDIT_SUMMARY.md (8KB)
     - docs/ia/guides/operational/CONFLICT_RESOLUTION.md (NEW)
  
  3. Confirm: "Rollback these 4 files to commit 5196d06?"
     User: "YES"
  
  4. Execute: git reset --hard HEAD~1
  
  5. Verify: python validate-spec-checkpoint.py
     Result: ✅ CHECKPOINT VALID
  
  6. Log: "Rollback completed to 5196d06, reason: validation failure"
     Saved to: /docs/ia/development/execution-state/_current.md
```

## Checkpoint Frequency

```
Create checkpoint after:
  ✅ SPEC layer changes complete
  ✅ All validation passes
  ✅ Emergency procedures tested
  ✅ User confirmed stable state

Do NOT checkpoint during:
  ❌ Active conflicts (unresolved)
  ❌ Validation failures
  ❌ Ambiguous state (user unsure)
```

## Why This Matters

Without checkpoints:
  ❌ Break something → spend 2 hours fixing
  ❌ No audit trail what was broken
  
With checkpoints:
  ✅ Break something → rollback to last good state (2 min)
  ✅ Complete audit trail
  ✅ Safe to experiment (know rollback is always available)
```

**Status:** ⏳ TODO (Create checkpoint-validation.md)

---

#### Rule 4: "SEMPRE Confirmar Antes de Aplicar Comandos GIT"

Create: `/docs/ia/guides/operational/GIT_COMMAND_CONFIRMATION.md`

```markdown
# GIT Command Confirmation Protocol

## The Rule

```
NO git command executes without:
  1. Agent shows EXACTLY what will happen
  2. User confirms YES or NO
  3. User has chance to abort
```

## Implementation

### Pattern for All GIT Commands

```python
# Agent template for ANY git command

def git_command_with_confirmation(cmd, description):
    """Execute git command only with user confirmation."""
    
    print(f"🔹 {description}")
    print(f"   Command: {cmd}")
    print("")
    
    # Show impact
    if "commit" in cmd:
        print("Files affected:")
        for file in get_changed_files():
            size_before = get_size(file, "HEAD")
            size_after = get_size(file, "working")
            delta = size_after - size_before
            print(f"  {file} ({delta:+d} bytes)")
    
    if "reset" in cmd or "revert" in cmd:
        print("Will discard:")
        for file in get_affected_files():
            print(f"  ❌ {file} (will be lost)")
    
    print("")
    print("Proceed? (yes/no)")
    user_response = input("> ").strip().lower()
    
    if user_response != "yes":
        print("❌ Aborted by user")
        return False
    
    print(f"✅ Confirmed. Executing...")
    execute(cmd)
    return True
```

### Specific Commands & Confirmation

#### Command: git commit

```
Agent shows:
  Files changed: 5
  Insertions: 247
  Deletions: 18
  Commit message: "📐 Create SPEC authority contracts"

Confirmation prompt:
  "Commit these 5 files? (yes/no)"
  User: "yes"

Execute: git commit -m "..."
```

#### Command: git reset --hard

```
Agent shows:
  WARNING: Will discard ALL uncommitted changes
  
  Files to be lost:
    ❌ docs/ia/QUALITY_REGRESSION_ACTION_PLAN.md (15KB)
    ❌ docs/ia/guides/operational/CONFLICT_RESOLUTION.md (NEW)
    ❌ docs/ia/development/execution-state/_current.md (MODIFIED)
  
  Recovery: git reflog (shows history, can recover)

Confirmation:
  "This cannot be undone easily. Discard 3 files? (yes/no)"
  User: "yes" (must explicitly confirm)

Execute: git reset --hard HEAD~1
```

#### Command: git revert / git cherry-pick

```
Agent shows:
  Action: Revert commit 5196d06
  Commit message: "🔍 Critical audit reveals regressions"
  
  Will undo:
    - WORLD_CLASS_REVIEW_V2.md creation
    - QUALITY_REGRESSION_ACTION_PLAN.md creation
    - SPEC_AUDIT_SUMMARY.md creation
  
  Result: Return to commit 56ecbda
  
Confirmation:
  "Revert 3 files? (yes/no)"
  User: "yes"

Execute: git revert 5196d06
```

## Decision Points

All critical decisions must be EXPLICIT:

```
WHEN TO CONFIRM:
  ✅ Any commit (what/why)
  ✅ Any reset/revert (impact)
  ✅ Any branch changes (destination)
  ✅ Any force push (danger)
  ✅ Any file deletion (recovery risk)
  ✅ Any conflict resolution (which side wins)

NEVER CONFIRM:
  ❌ git status (informational)
  ❌ git log (informational)
  ❌ git diff (informational)
  ❌ git branch -l (informational)
```

## Emergency Override

If user says "skip confirmation" (risky):
```
User: "git commit --no-verify --skip-confirmation"

Agent: ⚠️ DANGEROUS MODE ENABLED
  You are skipping safety confirmations.
  
  Proceed with full responsibility? (type 'CONFIRM' to continue)
  User: "CONFIRM"
  
Agent: ⚠️ OK, proceeding without confirmation gates
  (But logging all commands to execution log)

After command:
  Log: "Command executed without confirmation: git commit"
  Mark in _current.md: "USER OVERRIDE - dangerous mode"
```

## Why This Matters

Without confirmations:
  ❌ git reset --hard → oops, lost 2 days of work
  ❌ git revert → wrong commit reverted

With confirmations:
  ✅ User sees impact before happening
  ✅ User can abort at last second
  ✅ All changes audited + confirmed
```

**Status:** ⏳ TODO (Create git-confirmation.md protocol)

---

## 📋 REVISED RECOVERY PLAN (Architecture Phase)

### PRIORITY 1: Documentation Contracts (This Week)

**Effort: 12 hours**

```
[✅] 1. Agent Context Initialization Contract
      File: agent-context-initialization.md
      Time: 2h
      Deliverable: setup-wizard.py behavior spec

[✅] 2. Documentation Validation Contract  
      File: documentation-validation-contract.md
      Time: 2h
      Deliverable: validate-ia-first.py blocking rules

[✅] 3. Project Specialization Contract
      File: project-specialization-contract.md
      Time: 2h
      Deliverable: generate-specializations.py idempotency

[✅] 4. SPEC Authority & Immutability
      File: spec-authority.md
      Time: 1h
      Deliverable: Immutability axioms

[✅] 5. Conflict Resolution Procedure
      File: operational/CONFLICT_RESOLUTION.md
      Time: 2h
      Deliverable: Escalation & decision procedure

[✅] 6. Checkpoint Validation & Rollback
      File: operational/CHECKPOINT_VALIDATION.md
      Time: 2h
      Deliverable: Checkpoint contracts + rollback

[✅] 7. GIT Command Confirmation Protocol
      File: operational/GIT_COMMAND_CONFIRMATION.md
      Time: 1h
      Deliverable: User confirmation for all git commands
```

---

### PRIORITY 2: Architectural Tests (Next Week)

**Effort: 6 hours (defer to real development start)**

```
[⏳] 1. Layer Isolation Tests
      File: tests/spec_validation/test_layer_isolation.py
      Time: 2h
      
[⏳] 2. Specializations Tests
      File: tests/spec_validation/test_specializations.py
      Time: 2h
      
[⏳] 3. Emergency Procedures Tests
      File: tests/spec_validation/test_emergency_procedures.py
      Time: 2h
```

---

### PRIORITY 3: Integration to CI/CD (Real Development)

**Effort: 4 hours (apply when developing rpg-narrative-server)**

```
[⏳] 1. Add validation-ia-first.py job to spec-enforcement.yml
[⏳] 2. Add checkpoint-validation job
[⏳] 3. Add git-confirmation to pre-commit hooks
[⏳] 4. Add conflict detection to CI/CD
```

---

### PRIORITY 4: Metrics & Collection (Production)

**Effort: TBD (real usage data)**

```
[⏳] Collect real metrics during actual development
[⏳] Create feedback loops from production
```

---

## 🎯 UPDATED SUCCESS CRITERIA

### For v2.2 (Architecture Complete)

✅ All 7 operational contracts documented  
✅ Conflict resolution procedure clear  
✅ Rollback procedure clear  
✅ GIT confirmation protocol enforced  
✅ Authority rules immutable  
✅ Checkpoint validation defined  
✅ Architectural tests defined (not all implemented)

### For Real Development (rpg-narrative-server)

✅ Integrate validation to CI/CD  
✅ Run architectural compliance tests  
✅ Collect real metrics from team  
✅ Create second project (scaling validation)  

### For Production (5+ projects)

✅ Multi-project conflict resolution proven  
✅ Metrics show improvements held  
✅ Emergency procedures tested  
✅ Rollback procedures automatic  

---

## 📁 NEW FILES TO CREATE THIS WEEK

```
docs/ia/CANONICAL/specifications/
├── agent-context-initialization.md
├── documentation-validation-contract.md
├── project-specialization-contract.md
├── spec-authority.md

docs/ia/guides/operational/
├── CONFLICT_RESOLUTION.md
├── CHECKPOINT_VALIDATION.md
├── GIT_COMMAND_CONFIRMATION.md
└── [existing emergency procedures refined]
```

**Total new documentation: ~8 KB**  
**Total effort: 12 hours**  
**Timeline: This week (2h/day)**

---

## ✅ ACKNOWLEDGMENTS

You are 100% correct on:

1. ✅ **Gaps filled during real development** — Metrics, multi-project, CI/CD integration deferred
2. ✅ **Focus NOW is architecture clarity** — Contracts, checkpoints, decision gates
3. ✅ **AI agents must understand SPEC** — Context initialization, validation, conflicts
4. ✅ **No premature optimization** — Tests deferred, metrics deferred, scaling deferred
5. ✅ **User confirmation always** — Never blind git commands, always explain impact

This revised plan aligns with your vision: **Solid architecture first, implementation later.**

---

## 🚀 NEXT STEP

Ready to start PRIORITY 1 this week?

Task allocation:
- Monday (2h): agent-context-initialization.md + documentation-validation-contract.md  
- Tuesday (2h): project-specialization-contract.md + spec-authority.md
- Wednesday (2h): CONFLICT_RESOLUTION.md + CHECKPOINT_VALIDATION.md
- Thursday (2h): GIT_COMMAND_CONFIRMATION.md + review all 7

Should I begin Monday?
