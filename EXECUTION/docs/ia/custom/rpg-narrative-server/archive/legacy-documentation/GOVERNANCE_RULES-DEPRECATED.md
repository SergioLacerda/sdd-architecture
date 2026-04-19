# 🔒 GOVERNANCE RULES — Imutável

**These files define PERMANENT RULES for the system.**

Do NOT change without strong technical reason and full checkpoint documentation.

---

## 📋 Immutable Governance Layer

| File | Purpose | Change Frequency |
|------|---------|------------------|
| [ia-rules.md](./ia-rules.md) | 16 execution protocols (mandatory) | Rare (only major violations found) |
| [specs/constitution.md](./specs/constitution.md) | System principles & design philosophy | Rare (architectural decisions) |
| [specs/_shared/architecture.md](./specs/_shared/architecture.md) | Design patterns & Clean Architecture | Rare (major refactoring) |
| [specs/_shared/conventions.md](./specs/_shared/conventions.md) | Naming, style, code organization | Rare (team agreement needed) |
| [specs/_shared/definition_of_done.md](./specs/_shared/definition_of_done.md) | Merge criteria & validation rules | Rare (process improvements) |
| [specs/_shared/feature-checklist.md](./specs/_shared/feature-checklist.md) | 8-layer implementation blueprint | Rare (methodology change) |
| [specs/_shared/testing.md](./specs/_shared/testing.md) | Testing patterns & validation approach | Rare (quality standards change) |

---

## 🚨 When to Change Governance

**If you want to modify any governance rule:**

1. **Read** [constitution.md](./specs/constitution.md) first
   - Ask: Does this violate any principle?

2. **Document WHY** (not just WHAT)
   - What problem does the change solve?
   - What was broken about the old rule?
   - Why now and not before?

3. **Update checkpoint** in [specs/runtime/execution_state.md](./specs/runtime/execution_state.md)
   ```markdown
   ## Governance Change
   - Date: YYYY-MM-DD
   - File: [filename.md]
   - Reason: [explanation]
   - Breaking Change: YES/NO
   - Affected Work: [what threads/features]
   ```

4. **Flag as BREAKING if**
   - Changes ia-rules.md (16 protocols)
   - Changes architecture.md (design patterns)
   - Changes definition_of_done.md (merge criteria)
   
   **BREAKING CHANGES require:**
   - All agents to re-read documentation
   - Code review of all related code
   - Checkpoint marked with 🔴 BREAKING

5. **Notify agents** in FIRST_SESSION_SETUP.md or guides
   - Add section "Recent Governance Changes"
   - Explain impact clearly

---

## ✅ What CAN Change in Governance Files

**Minor updates (low risk):**
- Clarifications to existing rules
- Better examples in feature-checklist.md
- Formatting/wording improvements
- Links/references updates

**These do NOT require BREAKING change flag**

---

## 💡 Philosophy

**Why immutable governance?**

```
❌ Problem: Rules change too often → agents confused
✅ Solution: Governance is STABLE, state is DYNAMIC

Rules should survive:
  - Implementation details changing
  - Bugs being fixed
  - Services being refactored
  - Storage systems evolving
  - New features being added

But rules CAN change when:
  - Core principles prove wrong
  - New architectural patterns discovered
  - Team agrees on better standards
  - Scale requires new constraints
```

---

## 📊 Governance vs Runtime

```
GOVERNANCE (Immutable)
├── What is RIGHT?
├── What are principles?
├── What patterns work?
├── What's the standard?
└── How do we validate?

RUNTIME (Mutable)
├── What's happening NOW?
├── What threads active?
├── What state are we in?
├── What bugs found?
└── What limits discovered?
```

---

## 🔗 Related Files

**For Runtime State** (mutable, changes frequently):
→ See [RUNTIME_STATE.md](./RUNTIME_STATE.md)

**For Current System State** (reality vs ideal):
→ See [current-system-state/](./current-system-state/)

**For Implementation Guidance**:
→ See [guides/](./guides/)

---

## 🎓 For New Agents

When starting a session:
1. ✅ Read [ia-rules.md](./ia-rules.md) (part of governance)
2. ✅ Read [specs/constitution.md](./specs/constitution.md) (part of governance)
3. ✅ Then check [RUNTIME_STATE.md](./RUNTIME_STATE.md) (see current state)

Don't assume governance rules have changed. They're stable by design.

If you find a governance rule conflicts with reality:
- **Document in** [current-system-state/known_issues.md](./current-system-state/known_issues.md) (gap between ideal vs real)
- **Do NOT change** the governance rule without asking
