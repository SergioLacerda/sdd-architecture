# 🔍 FAQ — Frequently Asked Questions

**Common questions about SDD framework**

---

## General Questions

### Q: What is SDD?

**A:** Specification-Driven Development with Autonomous Governance. A framework that makes AI agents first-class citizens in development.

### Q: How long does it take to learn?

**A:** 
- PHASE 0 (setup): 20-30 minutes
- Understanding rules: 15-20 minutes
- Running through first feature: 1-4 hours depending on complexity

### Q: Do I have to use all of it?

**A:** No. Integrate what makes sense:
- If you have AI agents: Use EXECUTION flow
- If adding projects: Use INTEGRATION flow
- Can adopt incrementally

---

## Development Questions

### Q: When do I write tests?

**A:** During PHASE 5 (Implementation) using TDD: write test first, then code.

### Q: What if I find a rule doesn't apply to me?

**A:** 
1. Read the ADR that explains WHY the rule exists
2. If still conflicts, discuss with team
3. Document decision in checkpoint

### Q: How do I know if my code is "done"?

**A:** Check `definition-of-done.md` (45+ criteria). Use the checklist during PHASE 6.

---

## Governance Questions

### Q: Who enforces the rules?

**A:** You do + pre-commit hooks + tests. Automation handles most checks.

### Q: Can multiple people work on same task?

**A:** No. Each thread is isolated to one developer/agent. Check `execution-state/` before starting.

### Q: What if someone else is working on my task?

**A:** Contact them, coordinate, or work on different task. Never modify same files.

---

## Getting Help

**Can't find what you need?** → [NAVIGATION.md](../../../NAVIGATION.md)

**Have other questions?** → See project's `custom/[PROJECT]/` docs
