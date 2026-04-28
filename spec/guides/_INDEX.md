# 📚 GUIDES INDEX — On-Demand Reading

**Purpose:** Navigate guides by role, task, or time budget  
**Status:** ✅ Optimized for selective loading  
**Last Updated:** 2026-04-19

---

## 🎯 I need help with...

### **"I'm new to the project"**
→ **Time:** 30 minutes  
→ **What to read:**
1. [FIRST_SESSION_SETUP.md](onboarding/FIRST_SESSION_SETUP.md) (15 min)
2. [QUICK_START.md](onboarding/QUICK_START.md) (5 min)
3. [VALIDATION_QUIZ.md](onboarding/VALIDATION_QUIZ.md) (10 min)

**Outcome:** Understand SPEC framework and your role

---

### **"I'm implementing a bug fix"** (PATH A: 1.5h)
→ **Time:** 15 minutes reading  
→ **What to read:**
1. [FIRST_SESSION_SETUP.md](onboarding/FIRST_SESSION_SETUP.md) §1-3 (5 min)
2. `/EXECUTION/spec/custom/_TEMPLATE/SPECIALIZATIONS/ia-rules-rpg-specific.md` (5 min)
3. `/EXECUTION/spec/custom/_TEMPLATE/reality/limitations/known_issues.md` (5 min)

**Outcome:** Understand bug, execute fix, avoid breaking other code

---

### **"I'm implementing a simple feature"** (PATH B: 2h)
→ **Time:** 20 minutes reading  
→ **What to read:**
1. [QUICK_START.md](onboarding/QUICK_START.md) (3 min)
2. `/EXECUTION/spec/CANONICAL/rules/constitution.md` — sections 1-3 (10 min)
3. `/EXECUTION/spec/CANONICAL/specifications/architecture.md` — Layer overview (7 min)

**Outcome:** Design feature, follow principles, make it testable

---

### **"I'm implementing a complex feature"** (PATH C: 3-4h)
→ **Time:** 45 minutes reading  
→ **What to read:**
1. [QUICK_START.md](onboarding/QUICK_START.md) (3 min)
2. `/EXECUTION/spec/CANONICAL/rules/constitution.md` — ALL sections (20 min)
3. `/EXECUTION/spec/CANONICAL/specifications/architecture.md` — ALL (15 min)
4. `/EXECUTION/spec/CANONICAL/decisions/` — Relevant ADRs (7 min)

**Outcome:** Understand system deeply, design correctly, no rework

---

### **"I'm working on parallel development threads"** (PATH D: Variable)
→ **Time:** 30 minutes reading  
→ **What to read:**
1. [FIRST_SESSION_SETUP.md](onboarding/FIRST_SESSION_SETUP.md) (15 min)
2. `/EXECUTION/spec/custom/_TEMPLATE/SPECIALIZATIONS/ia-rules-rpg-specific.md#development-threads` (10 min)
3. `/EXECUTION/spec/custom/_TEMPLATE/development/execution-state/_current.md` (5 min)

**Outcome:** Understand thread boundaries, avoid conflicts, coordinate changes

---

## 🔍 I'm stuck with...

### **"A commit hook failed"**
→ **Read:** [CI/CD validation guide](../operational/README.md)
→ **Time:** 10 minutes

### **"A test is failing"**
→ **Read:**  
1. [IMPLEMENTATION_ROADMAP.md](implementation/IMPLEMENTATION_ROADMAP.md) (find similar feature)
2. `/EXECUTION/spec/CANONICAL/specifications/testing.md` (understand test types)
→ **Time:** 15 minutes

### **"Performance is slow"**
→ **Read:**  
1. `/EXECUTION/spec/CANONICAL/specifications/performance.md` (SLO targets)
2. [Performance SLOs](/EXECUTION/spec/CANONICAL/specifications/performance.md)
→ **Time:** 20 minutes

### **"I don't understand an ADR decision"**
→ **Read:**  
1. Relevant ADR in `/EXECUTION/spec/CANONICAL/decisions/`
2. Project specialization in `/EXECUTION/spec/custom/_TEMPLATE/SPECIALIZATIONS/`
→ **Time:** 15 minutes

---

## 👥 By Role

### **Backend Developer**
**Priority reading:**
1. `/EXECUTION/spec/CANONICAL/rules/constitution.md` (principles)
2. `/EXECUTION/spec/CANONICAL/specifications/architecture.md` (design)
3. `/EXECUTION/spec/custom/_TEMPLATE/SPECIALIZATIONS/` (project specifics)

**Optional:**
- `/EXECUTION/spec/CANONICAL/decisions/` (understand why)
- `/EXECUTION/spec/CANONICAL/specifications/security-model.md` (implement auth)

### **DevOps / SRE**
**Priority reading:**
1. `/EXECUTION/spec/CANONICAL/specifications/observability.md` (logging/metrics)
2. `/EXECUTION/spec/CANONICAL/specifications/performance.md` (SLOs)
3. [CI/CD validation guide](../operational/README.md)

**Optional:**
- `/EXECUTION/spec/CANONICAL/specifications/security-model.md` (hardening)

### **Product Manager**
**Priority reading:**
1. [YOUR_VISION_IMPLEMENTED.md](context/YOUR_VISION_IMPLEMENTED.md) (overview)
2. `/EXECUTION/spec/CANONICAL/rules/backward-compatibility-policy.md` (when breaking changes allowed)
3. `/EXECUTION/spec/custom/_TEMPLATE/README.md` (project status)

**Optional:**
- `/EXECUTION/spec/CANONICAL/specifications/performance.md` (performance targets)

### **Architect**
**Priority reading:**
1. `/EXECUTION/spec/CANONICAL/rules/constitution.md` (ALL)
2. `/EXECUTION/spec/CANONICAL/specifications/architecture.md` (ALL)
3. `/EXECUTION/spec/CANONICAL/decisions/` (ALL ADRs)

**Optional:**
- `/EXECUTION/spec/custom/_TEMPLATE/reality/` (understand system)

---

## ⏱️ By Time Budget

### **5 minutes** (Quick question)
- [QUICK_START.md](onboarding/QUICK_START.md)
- Specific ADR title or one section

### **15 minutes** (Quick decision)
- One principle from `/EXECUTION/spec/CANONICAL/rules/constitution.md`
- One specification from `/EXECUTION/spec/CANONICAL/specifications/`
- Project specialization overview

### **30 minutes** (Daily work)
- [FIRST_SESSION_SETUP.md](onboarding/FIRST_SESSION_SETUP.md)
- Relevant PATH from [QUICK_START.md](onboarding/QUICK_START.md)
- Project-specific guides

### **1 hour** (In-depth understanding)
- Full `/EXECUTION/spec/CANONICAL/rules/constitution.md`
- Full `/EXECUTION/spec/CANONICAL/specifications/architecture.md`
- Relevant ADRs (2-3)

### **2+ hours** (Deep learning)
- Complete `/EXECUTION/spec/CANONICAL/` layer
- Complete `/EXECUTION/spec/custom/_TEMPLATE/` layer
- Relevant guides for your role

---

## 🗺️ Documentation Map

### **CANONICAL Layer** (Generic, all projects inherit)
Used when: Understanding principles, learning patterns, implementing across projects

```
CANONICAL/
├─ rules/ (execute these)
│  ├─ ia-rules.md (how agents work)
│  ├─ constitution.md (15 principles)
│  ├─ backward-compatibility-policy.md (breaking changes)
│  └─ conventions.md (naming, style)
├─ specifications/ (implement these)
│  ├─ architecture.md (8-layer design)
│  ├─ security-model.md (auth/authz)
│  ├─ observability.md (logging/tracing)
│  ├─ performance.md (SLO targets)
│  └─ testing.md (test strategy)
└─ decisions/ (understand rationale)
   ├─ ADR-001: 8-layer Clean Architecture
   ├─ ADR-002: Async-First (no blocking)
   ├─ ADR-003: Ports & Adapters
   ├─ ADR-004: Vector Index Strategy
   ├─ ADR-005: Thread Isolation
   └─ ADR-006: Append-Only Storage
```

### **SPECIALIZATIONS Layer** (Project-specific)
Used when: Implementing [PROJECT_NAME] features

```
custom/[PROJECT_NAME]/SPECIALIZATIONS/
├─ ia-rules-rpg-specific.md (project paths & services)
├─ constitution-rpg-specific.md (campaigns & concurrency)
└─ (more specializations as project grows)
```

### **Guides Layer** (Navigation & learning)
Used when: Lost, stuck, or learning

```
guides/
├─ onboarding/ (first time only)
├─ navigation/ (find things)
├─ implementation/ (how to build)
├─ reference/ (look things up)
└─ context/ (project status)
```

---

## 🚀 Reading Flow Examples

### **Example 1: I want to add campaign search**

```
1. START: Read PATH for feature complexity
   → guides/onboarding/QUICK_START.md (3 min)
   → Decide: PATH B or C?

2. PRINCIPLES: Understand constraints
   → /EXECUTION/spec/CANONICAL/rules/constitution.md § 1,3,6 (15 min)
   (Clean Architecture, Ports&Adapters, Performance)

3. ARCHITECTURE: Understand how search fits
   → /EXECUTION/spec/CANONICAL/specifications/architecture.md (10 min)

4. PROJECT: Understand campaign structure
   → /EXECUTION/spec/custom/_TEMPLATE/SPECIALIZATIONS/constitution-rpg-specific.md (10 min)

5. IMPLEMENTATION: Design search
   → Create feature, follow principles
   → Write tests before code
   → Run compliance checks

6. COMMIT: Make changes
   → Pre-commit hooks validate
   → Push to PR
   → CI/CD validates
   → Review + merge

Total: 50 minutes reading + implementation time
```

### **Example 2: Bug fix in campaign isolation**

```
1. QUICK: Understand what to read
   → guides/onboarding/QUICK_START.md § PATH A (2 min)

2. BUG: Understand the issue
   → /EXECUTION/spec/custom/_TEMPLATE/reality/limitations/known_issues.md (5 min)

3. RULES: Know hard constraints
   → /EXECUTION/spec/custom/_TEMPLATE/SPECIALIZATIONS/ia-rules-rpg-specific.md § Campaign Isolation (10 min)

4. FIX: Implement fix
   → Fix code (quick, focused)

5. TEST: Verify fix
   → Run isolation tests
   → Run compliance checks

Total: 20 minutes reading + fix time
```

---

## ✅ Loading Optimization Checklist

When reading docs:

- [ ] Know your time budget (5, 15, 30, 60+ minutes)
- [ ] Know your role (backend, devops, PM, architect)
- [ ] Know your task (bug fix, feature, learning)
- [ ] Read ONLY what's relevant
- [ ] Use this index to navigate
- [ ] Skip CANONICAL if you understand principles
- [ ] Skip project specializations if not working on [PROJECT_NAME]
- [ ] Bookmark guides you'll use repeatedly

---

**Version:** 1.0 (Initial)  
**Status:** ✅ Active  
**Owner:** All Developers
