# 🏗️ How Each Layer Works

**Understanding the 6-layer governance hierarchy**

---

## Overview

SDD uses a 6-layer hierarchy where each layer builds on the previous. Earlier layers are more authoritative.

```
Layer 1: Constitutional (immutable principles)
  ↓
Layer 2: Rules (mandatory requirements)
  ↓
Layer 3: Architecture (decisions explaining WHY)
  ↓
Layer 4: Specifications (HOW to implement)
  ↓
Layer 5: Guides (step-by-step instructions)
  ↓
Layer 6: Custom (project-specific specializations)
```

---

## Layer 1: Constitutional

**File:** `CANONICAL/rules/constitution.md`  
**Authority:** Immutable (never changes)  
**Purpose:** Define core philosophy  
**Count:** 15 principles

### What It Does
Sets foundational beliefs about SDD. Never modifies. If constitution conflicts with anything below it, constitution wins.

### Example Principles
- "Governance is automated, not bureaucratic"
- "AI agents are first-class citizens"
- "Every decision is documented"

### When You Read It
PHASE 1 of AGENT_HARNESS (first thing, 5 minutes)

### How It Applies
You don't "follow" constitution - you live it. It explains what we believe.

---

## Layer 2: Rules

**File:** `CANONICAL/rules/ia-rules.md`  
**Authority:** Mandatory  
**Purpose:** Non-negotiable requirements  
**Count:** 16 rules

### What It Does
Specifies what you MUST do. Breaking a rule = PR rejected. No exceptions.

### Example Rules
- Rule 1: "Ports Mandatory" — Never import infrastructure directly
- Rule 3: "Tests During Implementation" — Always TDD
- Rule 5: "Thread Isolation" — Only modify YOUR thread

### When You Read It
PHASE 1 of AGENT_HARNESS (right after constitution, 10 minutes)

### How It Applies
Check rules before coding. Verify PR satisfies all 16.

---

## Layer 3: Architecture

**Location:** `CANONICAL/decisions/ADR-*.md`  
**Authority:** Explains mandatory decisions  
**Purpose:** Why each rule exists  
**Count:** 6+ ADRs

### What It Does
Justifies the rules. If a rule seems unfair, read the ADR.

### Example ADRs
- ADR-001: Why clean 8-layer architecture?
- ADR-003: Why ports/adapters pattern?
- ADR-005: Why thread isolation mandatory?

### When You Read It
As needed during PHASE 2-4. When you have questions about WHY.

### How It Applies
Understanding WHY makes following rules easier. Helps in code reviews.

---

## Layer 4: Specifications

**Location:** `CANONICAL/specifications/`  
**Authority:** Technical standards  
**Purpose:** HOW to implement correctly  
**Count:** 8+ files

### What It Does
Detailed patterns and standards. "Here's how to structure code that satisfies rules."

### Examples
- `definition-of-done.md` — 45+ completion criteria
- `communication.md` — How to document decisions
- `testing.md` — Testing patterns for each layer

### When You Read It
PHASE 5 (Implementation). Use as reference while coding.

### How It Applies
Follow patterns when implementing features.

---

## Layer 5: Guides

**Location:** `CANONICAL/guides/`  
**Authority:** Operational procedures  
**Purpose:** Step-by-step help  
**Count:** 20+ guides

### What It Does
Instructions for specific scenarios.

### Examples
- `AGENT_HARNESS.md` — Full 7-phase workflow
- `DEVELOPMENT_WORKFLOW_VALIDATION.md` — How to validate your workflow
- `emergency/` — What to do when things break

### When You Read It
On-demand. When you need help with a specific phase or problem.

### How It Applies
Follow step-by-step when stuck.

---

## Layer 6: Custom

**Location:** `CANONICAL/custom/[PROJECT]/`  
**Authority:** Project-specific only  
**Purpose:** Specializations for YOUR project  
**Count:** Varies per project

### What It Does
Documentation specific to your project. Can extend/clarify layers 1-5 but never contradict them.

### Examples
- `development/execution-state/` — Who's working on what
- `SPECIALIZATIONS/` — Project-specific patterns
- `reality/` — Observed system facts

### When You Read It
When working on a specific project. First thing before PHASE 5.

### How It Applies
Adapt patterns to your project reality while staying within framework.

---

## Authority Hierarchy

**When documents conflict, use this priority:**

1. 🔴 **Constitution** (immutable)
   - Never changes
   - Example: "All decisions documented"

2. 🟠 **Rules** (mandatory)
   - Can only be removed by vote
   - Example: "No direct infrastructure imports"

3. 🟡 **ADRs** (architecture decisions)
   - Explain why rules exist
   - Can be superseded by new ADR vote
   - Example: "Here's why thread isolation matters"

4. 🟢 **Specifications** (technical standards)
   - Describe HOW to satisfy rules
   - Can be clarified or extended
   - Example: "Here's the testing pattern"

5. 🔵 **Guides** (procedures)
   - Helper documentation
   - Can be updated anytime
   - Example: "Steps to run PHASE 0"

6. 🟣 **Custom** (project-specific)
   - Never overrides layers 1-5
   - Can only clarify or extend
   - Example: "Our project calls it 'Campaign' not 'Project'"

---

## Example: Following All 6 Layers

**Scenario:** "How do I write tests?"

### Layer 1 - Constitution
✅ "Every decision is documented" (applies to tests too)

### Layer 2 - Rules
✅ Rule 3: "Tests During Implementation" (TDD always)

### Layer 3 - Architecture
✅ ADR-004: "Isolated Testing" (why tests are isolated)

### Layer 4 - Specifications
✅ `testing.md` — "Here's the pattern:
- Write test first
- Then code
- Then refactor"

### Layer 5 - Guides
✅ `TEST_FAILURE_GUIDE.md` — "If test fails during PHASE 5, do X"

### Layer 6 - Custom
✅ Project docs might say: "We use pytest, not unittest"

**Result:** You follow all 6 layers in concert.

---

## Quick Reference

| Layer | Authority | Change? | Read When |
|-------|-----------|---------|-----------|
| Constitution | Highest | Never | PHASE 1 |
| Rules | Mandatory | Rarely | PHASE 1 |
| ADRs | Decisions | Via vote | On-demand |
| Specs | Standards | Easy | PHASE 5 |
| Guides | Procedures | Always | On-demand |
| Custom | Project | Yes | Per project |

---

**Want specific layer docs?** → [NAVIGATION.md](../../../NAVIGATION.md)
