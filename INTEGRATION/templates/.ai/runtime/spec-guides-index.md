# 📚 SPEC-GUIDES Index

**Remote Location:** SPEC_PATH/docs/ia/guides/  
**Purpose:** Quick reference to all operational guides  
**Updated:** [auto-filled by agent]  

---

## 🎯 Onboarding Guides

### PHASE 0: Agent-Driven Initialization
**File:** onboarding/PHASE-0-AGENT-ONBOARDING.md  
**Time:** 30-40 minutes  
**What:** 6-step agent workspace initialization  
**Read when:** First time joining project  
**Key sections:**
- Step 1-3: Setup (config, framework, directories)
- Step 4-6: Validation (quiz, knowledge, commit)

### PHASE 0: Workflow Documentation
**File:** onboarding/PHASE-0-FLOW.md  
**Time:** 10 minutes (skim)  
**What:** Three states of workspace (seed → init → ready)  
**Read when:** Understanding PHASE 0 purpose  
**Key sections:**
- Three states explained
- Agent journey example
- Old vs new approach

### AGENT_HARNESS: 7-Phase Protocol
**File:** onboarding/AGENT_HARNESS.md  
**Time:** 40 minutes first read, 10 min reference  
**What:** Complete development workflow (phases 1-7)  
**Read when:** Starting real work (after PHASE 0)  
**Key phases:**
- Phase 1: Lock to Rules
- Phase 2: Check Execution State
- Phase 3: Choose PATH (A/B/C/D)
- Phase 4: Load Context
- Phase 5: Implement
- Phase 6: Validate
- Phase 7: Checkpoint

### VALIDATION_QUIZ
**File:** onboarding/VALIDATION_QUIZ.md  
**Time:** 10-15 minutes  
**What:** SDD knowledge validation (5 questions)  
**Required score:** 4/5 (80%)  
**Take when:** During PHASE 0 (mandatory)

---

## 🏃 Runtime Guides

### Context-Aware Usage
**File:** runtime/CONTEXT_AWARE_USAGE.md  
**Time:** 20 minutes first read, 5 min reference  
**What:** How to use .ai/context-aware/ infrastructure  
**Read when:** Need to track tasks, discoveries, metrics  
**Key sections:**
- Task-progress pattern
- Analysis discoveries
- Runtime state metrics
- Handoff workflow

### Example: Task Progress
**File:** runtime/example-task-progress.md  
**Time:** 15 minutes  
**What:** Real workflow example with actual tasks  
**Read when:** Implementing your first feature  
**Shows:** Complete task lifecycle

### Runtime Index
**File:** runtime/_INDEX.md  
**Time:** 5 minutes  
**What:** Navigation guide for all runtime docs  
**Read when:** Lost, need to find something

---

## 🔧 Operational Guides (7 total)

### Guide 1: Task Management
**File:** operational/task-management.md  
**When:** Managing multiple concurrent tasks  
**Key:** Thread isolation, checkpoint tracking

### Guide 2: Code Review Process
**File:** operational/code-review.md  
**When:** Submitting PR, reviewing others' code  
**Key:** Checklist, common issues, approval criteria

### Guide 3: Dependency Management
**File:** operational/dependency-management.md  
**When:** Adding/updating dependencies  
**Key:** Approval process, testing, documentation

### Guide 4: Performance Optimization
**File:** operational/performance-optimization.md  
**When:** Optimizing critical paths  
**Key:** Profiling, benchmarking, trade-offs

### Guide 5: Security & Compliance
**File:** operational/security-compliance.md  
**When:** Handling sensitive data, compliance requirements  
**Key:** Data protection, audit trail, validation

### Guide 6: Deployment & Rollback
**File:** operational/deployment-rollback.md  
**When:** Shipping to production  
**Key:** Checklist, rollback procedure, monitoring

### Guide 7: Incident Response
**File:** operational/incident-response.md  
**When:** Production issues, system failures  
**Key:** Detection, escalation, resolution, postmortem

---

## 🚨 Emergency Procedures (5 runbooks)

### Runbook 1: Pre-Commit Hook Failure
**File:** emergency/PRE_COMMIT_HOOK_FAILURE.md  
**When:** Hook prevents commit  
**Recovery:** 5-step recovery procedure

### Runbook 2: File Corruption
**File:** emergency/AUTO_FIX_CORRUPTION_RECOVERY.md  
**When:** Files are corrupted/unreadable  
**Recovery:** Detection + automatic recovery

### Runbook 3: CANONICAL Corruption
**File:** emergency/CANONICAL_CORRUPTION_RECOVERY.md  
**When:** Immutable files are modified  
**Recovery:** Restoration from git history

### Runbook 4: CI/CD Gate Failure
**File:** emergency/CI_CD_GATE_FAILURE.md  
**When:** All PRs blocked by CI failure  
**Recovery:** Diagnosis + fix procedure

### Runbook 5: Metrics Corruption
**File:** emergency/METRICS_CORRUPTION_RECOVERY.md  
**When:** Runtime metrics are invalid  
**Recovery:** Reset + re-calibration

---

## 🔍 How to Search This Index

**Use this mapping:**

| You Need | Find In | Search For |
|----------|---------|-----------|
| "How do I start?" | onboarding/PHASE-0 | "first time", "initialization" |
| "What do I do next?" | onboarding/AGENT_HARNESS | "phases 1-7", "workflow" |
| "How do I track work?" | runtime/CONTEXT_AWARE_USAGE | "task-progress", "discovery" |
| "Something broke" | emergency/ | error type |
| "How do I review code?" | operational/code-review | "PR", "approval", "checklist" |
| "Production issue" | emergency/incident-response | "incident", "postmortem" |

---

## 📊 Guide Levels

### Level 1: Essential (Required Reading)
- PHASE 0 (onboarding)
- AGENT_HARNESS (workflow)
- CONTEXT_AWARE_USAGE (tracking)

### Level 2: Important (First Implementation)
- VALIDATION_QUIZ (knowledge check)
- Example: Task Progress (real workflow)
- Code Review Process (collaboration)

### Level 3: Reference (As Needed)
- All Operational Guides (daily work)
- Emergency Procedures (trouble)
- Specifications in CANONICAL (details)

---

## ⏰ Recommended Reading Schedule

### Day 1 (Onboarding)
- PHASE 0 guide (30 min)
- VALIDATION_QUIZ (15 min)
- AGENT_HARNESS overview (20 min)

### Day 2-3 (Ramp Up)
- Full AGENT_HARNESS (40 min)
- CONTEXT_AWARE_USAGE (20 min)
- Example: Task Progress (15 min)

### Week 1+ (As Needed)
- Reference guides as needed
- Emergency procedures if issues arise
- Operational guides for specific tasks

---

**Location:** .ai/runtime/spec-guides-index.md  
**SPEC Version:** 2.1  
**Authority:** spec-architecture (remote, source of truth)
