# 🎯 Integration Flow — Intention Detection Refactor

**How Integration Now Works (v2 — Intention-Driven)**

---

## 📍 The Problem We Solved

**Before:** Integration asked "Choose LITE or FULL?" at the start  
**Issue:** Team didn't know their intention yet; decision was premature

**After:** Integration answers "What's your intention?" AFTER technical setup  
**Benefit:** Team understands their project before choosing governance level

---

## ✅ How Integration Works Now

```
┌─────────────────────────────────────────┐
│ PHASE 1: Technical Setup (STEPS 1-5)    │
├─────────────────────────────────────────┤
│ - STEP 1: Create directories            │
│ - STEP 2: Copy templates                │
│ - STEP 3: Configure .spec.config        │
│ - STEP 4: Validate installation         │
│ - STEP 5: Commit changes                │
│                                         │
│ ✅ RESULT: Project ready technically    │
│ ❌ NOT YET: Adoption level unknown      │
└─────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────┐
│ PHASE 2: Intention Detection (STEP 6)   │
├─────────────────────────────────────────┤
│ Answer 5 questions:                     │
│  1️⃣  Team size? (1-5, 5-20, 20+)       │
│  2️⃣  Project type? (learning, internal, production) │
│  3️⃣  Compliance needs? (none, internal, regulatory) │
│  4️⃣  AI agents? (no, maybe, yes)       │
│  5️⃣  Error cost? (low, medium, high)   │
│                                         │
│ ✅ RESULT: Know your governance needs   │
│ ✅ UPDATE: .spec.config with adoption   │
└─────────────────────────────────────────┘
                     ↓
           ┌─────────┴─────────┐
           │                   │
      LITE level            FULL level
      (5 rules)             (16 rules)
      (10 DoD)              (45 DoD)
           │                   │
           └─────────┬─────────┘
                     ↓
           ✅ PROJECT INTEGRATED
         (ready for EXECUTION)
```

---

## 🤔 The 5 Questions (STEP 6)

### Question 1: Team Size
- **A (1-5):** Small, learning-focused team
- **B (5-20):** Growing team, balanced approach
- **C (20+):** Large team, formal structure

### Question 2: Project Type
- **A:** Learning, experimentation, hobby
- **B:** Internal tool, MVP, prototyping
- **C:** Production service, business-critical, customer-facing

### Question 3: Compliance
- **A:** No requirements, no audits
- **B:** Internal standards, team agreements
- **C:** Regulatory (SOC2, HIPAA), formal audits

### Question 4: AI Agents
- **A:** No, manual coding
- **B:** Maybe, experimental
- **C:** Yes, agents are core

### Question 5: Error Cost
- **A:** Low, rollback easy
- **B:** Medium, rollback takes hours
- **C:** High, affects reputation, $$$

---

## 📊 Scoring

| Count | Result |
|-------|--------|
| Mostly A | 🟢 LITE (15 min setup) |
| Mixed A+B | Either (edge case) |
| Mostly C | 🔵 FULL (40 min setup) |

---

## 🔧 Technical Changes

### New File
- `INTEGRATION/STEP_6.md` — Complete intention detection guide with 5 questions

### Updated Files
- `INTEGRATION/README.md` — Explains 2-phase process
- `INTEGRATION/CHECKLIST.md` — STEP 1-5 for everyone, STEP 6 for adoption
- `INTEGRATION/STEP_3.md` — Notes that adoption_level goes in STEP 6
- `ONBOARDING-FLOW.md` — Updated Flow 2 diagram
- `adoption/INDEX.md` — Added reference to STEP_6

### Timeline Changes
- **Before:** Choose adoption (5 min) + setup (20 min) = 25 min total
- **Now:** Setup (20 min) + detect intention (10 min) = 30 min total
- **Advantage:** Intention is informed, not rushed

---

## 🎯 Key Insight

**Technical setup is objective** (copy files, configure paths)  
**Adoption choice is subjective** (depends on team, project, risk)

→ We separated these concerns  
→ Technical setup first (everyone does same thing)  
→ Then understand your project  
→ Then choose LITE or FULL based on answers

---

## 📍 Entry Points

| Role | Start | Next | Time |
|------|-------|------|------|
| Tech Lead | INTEGRATION/README | STEP_1-5 + STEP_6 | 30 min |
| Developer | After integration | EXECUTION/_START_HERE | 15-40 min |
| AI Agent | Check .spec.config | Confirm adoption_level | varies |

---

## ✅ Success Criteria

After all 6 integration steps:
- ✅ `.spec.config` has `spec_path` (STEP 3)
- ✅ `.spec.config` has `adoption_level` (STEP 6)
- ✅ Team documented their intention (STEP 6)
- ✅ Ready to execute with appropriate governance

---

## 🚀 Next

1. **For teams integrating now:** Follow INTEGRATION/ STEP_1-6
2. **For teams already integrated:** Answer the 5 questions, update `.spec.config`
3. **For developers:** Check your `.spec.config` adoption_level before starting AGENT_HARNESS

---

**Framework evolves with your feedback. This is working well!**
