# ⚡ Runtime Indices Specification

**Authority:** SPEC v2.1  
**Status:** Mandatory (created during PHASE 0)  
**Location:** `.ai/runtime/`  
**Updated:** April 19, 2026

---

## 🎯 Purpose

Specify the 3 runtime indices that agents create during PHASE 0 to enable efficient document discovery and context awareness.

**Key Insight:** Agents shouldn't spend time finding docs; indices make everything searchable.

---

## 📌 Two-Tier Index System

**Framework Tier (EXECUTION/spec/runtime/):**
- **Files:** `spec-canonical-index.md`, `spec-guides-index.md`, `search-keywords.md`
- **Purpose:** Templates for projects to copy and customize
- **Updated:** Quarterly (when framework changes)
- **Audience:** Reference for all projects

**Project Tier (.ai/runtime/):**
- **Files:** Same names as framework tier, but project-specific
- **Purpose:** Each project maintains its own runtime indices
- **Updated:** Per-project basis (can diverge from framework)
- **Audience:** Project-specific usage

**How It Works:**
1. SPEC framework provides template indices at `EXECUTION/spec/runtime/`
2. During project initialization (PHASE 0), templates are copied to `.ai/runtime/`
3. Projects customize their indices as needed
4. Framework indices serve as reference defaults

---

## 📇 Three Required Indices

### Index 1: spec-canonical-index.md

**Purpose:** Quick reference to all CANONICAL authority documents  
**Location:** `.ai/runtime/spec-canonical-index.md`  
**Created by:** PHASE 0 automation  
**Updated:** Quarterly (when CANONICAL changes)

**Structure:**

```markdown
# 📇 SPEC-CANONICAL Index

[Introduction]

## 🔴 Core Documents (Read in This Order)

### 1. Constitution
**File:** SPEC_PATH/EXECUTION/spec/CANONICAL/constitution.md
**What:** 15 immutable principles
**When:** First time onboarding

### 2. Rules (IA-RULES)
**File:** SPEC_PATH/EXECUTION/spec/CANONICAL/rules/ia-rules.md
**What:** 16 mandatory execution protocols
**When:** Before every implementation

### 3. Decisions (ADRs)
**Directory:** SPEC_PATH/EXECUTION/spec/CANONICAL/decisions/
**Count:** 6+ ADRs
**When:** Understanding why architecture is this way

#### ADR-001: Spec-Driven Development Pattern
...

### 4. Specifications
**Directory:** SPEC_PATH/EXECUTION/spec/CANONICAL/specifications/
**Count:** 5+ comprehensive specs
...

## 🔍 How to Search This Index

[Search table]

## 📊 Quick Reference

### By Topic

**Architecture:**
- decisions/ADR-002 (8-layer)
- specifications/architecture.md
- specifications/patterns.md

## 📖 Reading Paths

### Path 1: New Agent (Full Understanding - 1 hour)
### Path 2: Implementing Feature (30 min)
### Path 3: Debugging Issue (15 min)
### Path 4: Design Decision (20 min)
```

**Key Sections:**
1. Introduction (purpose + links)
2. Core documents list (constitution, rules, ADRs, specs)
3. Search mapping (keyword → file)
4. Reading paths (by use case)
5. Update frequency

**Purpose:** When agent asks "where are the rules?", they read this index instead of searching.

---

### Index 2: spec-guides-index.md

**Purpose:** Quick reference to all operational guides  
**Location:** `.ai/runtime/spec-guides-index.md`  
**Created by:** PHASE 0 automation  
**Updated:** Monthly (when guides added/changed)

**Structure:**

```markdown
# 📚 SPEC-GUIDES Index

[Introduction]

## 🎯 Onboarding Guides

### PHASE 0: Agent-Driven Initialization
**File:** SPEC_PATH/docs/ia/guides/onboarding/PHASE-0-AGENT-ONBOARDING.md
**Time:** 30-40 minutes
**What:** 6-step agent workspace initialization

### AGENT_HARNESS: 7-Phase Protocol
**File:** SPEC_PATH/docs/ia/guides/onboarding/AGENT_HARNESS.md
**Time:** 40 minutes first read, 10 min reference
**What:** Complete development workflow

## 🏃 Runtime Guides

### Context-Aware Usage
**File:** SPEC_PATH/docs/ia/guides/runtime/CONTEXT_AWARE_USAGE.md
**Time:** 20 minutes first read, 5 min reference

### Example: Task Progress
**File:** SPEC_PATH/docs/ia/guides/runtime/example-task-progress.md
**Time:** 15 minutes

## 🔧 Operational Guides (7 total)

### Guide 1: Task Management
...

## 🚨 Emergency Procedures (5 runbooks)

### Runbook 1: Pre-Commit Hook Failure
...

## 🔍 How to Search This Index

[Search table for common questions]

## 📊 Guide Levels

### Level 1: Essential (Required Reading)
### Level 2: Important (First Implementation)
### Level 3: Reference (As Needed)

## ⏰ Recommended Reading Schedule

### Day 1 (Onboarding)
### Day 2-3 (Ramp Up)
### Week 1+ (As Needed)
```

**Key Sections:**
1. Onboarding guides (PHASE 0, AGENT_HARNESS, VALIDATION_QUIZ)
2. Runtime guides (context, examples)
3. Operational guides (7 specific guides)
4. Emergency procedures (5 runbooks)
5. Search mapping
6. Guide levels (essential, important, reference)
7. Reading schedule

**Purpose:** When agent asks "how do I start?", they find answer here instead of wondering.

---

### Index 3: search-keywords.md

**Purpose:** Keyword-to-document mapping for on-demand discovery  
**Location:** `.ai/runtime/search-keywords.md`  
**Created by:** PHASE 0 automation  
**Updated:** As new patterns emerge

**Structure:**

```markdown
# 🔍 Search Keywords — Quick Discovery

[Introduction]

## 📌 Keyword to Document Mapping

### Architecture & Structure

| Keyword | Found In | Reason |
|---------|----------|--------|
| architecture | CANONICAL/specifications/architecture.md | 8-layer structure |
| layers | CANONICAL/specifications/architecture.md | Domain, usecases, etc |
| domain | CANONICAL/specifications/architecture.md | Core business logic |
| ports | CANONICAL/decisions/ADR-003 | Dependency inversion |
| adapters | CANONICAL/decisions/ADR-003 | Infrastructure abstraction |

### Rules & Governance

| Keyword | Found In | Reason |
|---------|----------|--------|
| rules | CANONICAL/rules/ia-rules.md | 16 mandatory protocols |
| mandatory | CANONICAL/rules/ia-rules.md | Non-negotiable |
| protocols | CANONICAL/rules/ia-rules.md | Execution guidelines |

### Testing & Quality

| Keyword | Found In | Reason |
|---------|----------|--------|
| testing | CANONICAL/specifications/testing.md | Test patterns |
| TDD | CANONICAL/specifications/testing.md | Test-driven development |
| unit test | CANONICAL/specifications/testing.md | Single unit tests |

### [More categories...]

## 🎯 Common Scenarios

### Scenario: "I don't know what rules apply"
**Search:** rules, mandatory
**Go to:** CANONICAL/rules/ia-rules.md
**Result:** 16 mandatory protocols

### Scenario: "How do I structure my code?"
**Search:** architecture, layers, domain
**Go to:** CANONICAL/specifications/architecture.md

### [More scenarios...]

## 💡 Pro Tips

**Tip 1:** Most questions answered in these 3 files:
1. CANONICAL/rules/ia-rules.md (rules)
2. guides/onboarding/AGENT_HARNESS.md (workflow)
3. guides/runtime/CONTEXT_AWARE_USAGE.md (tracking)

## 🔄 When to Update This

**Add entry when:**
- New document created
- New keyword helps discovery
- Common question patterns emerge
```

**Key Sections:**
1. Keyword mappings (organized by topic)
2. Common scenarios (keyword → solution)
3. Pro tips
4. When to update

**Purpose:** When agent asks "where do I find [concept]?", they search keywords instead of wandering.

---

## 🚀 Creating Runtime Indices (PHASE 0 Step)

### Automated Approach

```bash
# In PHASE 0 automation script:

# 1. Generate spec-canonical-index.md
python scripts/generate-canonical-index.py \
  --spec-path $spec_path \
  --output .ai/runtime/spec-canonical-index.md

# 2. Generate spec-guides-index.md
python scripts/generate-guides-index.py \
  --spec-path $spec_path \
  --output .ai/runtime/spec-guides-index.md

# 3. Generate search-keywords.md
python scripts/generate-keywords-index.py \
  --spec-path $spec_path \
  --output .ai/runtime/search-keywords.md
```

### Manual Approach (If Automation Fails)

```bash
# Copy templates
cp SPEC_PATH/templates/.ai/runtime/* .ai/runtime/

# Edit each with project-specific details
# Run: agent verifies indices are created
```

---

## ✅ Verification

**After PHASE 0, verify indices exist:**

```bash
# Check all 3 exist
ls -la .ai/runtime/
# Expected output:
# spec-canonical-index.md
# spec-guides-index.md
# search-keywords.md

# Verify they're not empty
wc -l .ai/runtime/*.md
# Expected: each > 50 lines

# Verify links work
grep "SPEC_PATH" .ai/runtime/*.md | head -5
# Expected: contains actual spec_path, not placeholder
```

---

## 📈 Maintenance

**Weekly:** No maintenance needed (read-only after creation)

**Monthly:** 
- Check if new guides added to SPEC → update indices
- Check if new patterns discovered → add to keywords

**Quarterly:**
- Re-generate all indices from SPEC source
- Verify all links still valid
- Update reading paths if guides changed

---

## 🔄 Update Cycle

### When SPEC Framework Updates

```
1. SPEC changes (new ADR, new guide, etc.)
2. .ai/runtime indices should reflect this
3. Automated: re-generation scripts run
4. Manual: agent reviews and updates
5. Commit: "docs: update runtime indices per SPEC v2.1.X"
```

### When New Patterns Discovered

```
1. Agent discovers new keyword/pattern
2. Adds to search-keywords.md
3. Documents which file teaches this
4. Commits in regular checkpoint
5. Next agent benefits from discovery
```

---

## 🎯 Success Criteria

Indices are working if:

✅ **Discoverability:** Agent asks question → finds answer in index  
✅ **Accuracy:** Links point to correct documents  
✅ **Completeness:** All CANONICAL docs indexed  
✅ **Freshness:** Updated quarterly  
✅ **Usability:** Clear keyword mapping  

---

## 📚 Related Documents

- PHASE 0: `guides/onboarding/PHASE-0-AGENT-ONBOARDING.md`
- Context-Aware: `guides/runtime/CONTEXT_AWARE_USAGE.md`
- CANONICAL Index: See `.ai/runtime/spec-canonical-index.md`
- Guides Index: See `.ai/runtime/spec-guides-index.md`
- Keywords: See `.ai/runtime/search-keywords.md`

---

## ✨ Why Indices Matter

**Without indices:**
- Agent searches for "where do I find rules?"
- Agent digs through docs/ia folder
- Agent reads 5 README files to navigate
- 30+ minutes wasted

**With indices:**
- Agent searches "rules" in search-keywords.md
- Finds: `ia-rules.md` in CANONICAL/rules/
- Opens document directly
- 1 minute saved × 100 uses = 100 hours saved

---

**Authority:** SPEC v2.1 Framework  
**Status:** Mandatory (created during PHASE 0)  
**Effective Date:** April 19, 2026
