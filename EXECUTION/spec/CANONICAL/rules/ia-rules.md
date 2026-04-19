# 🤖 AI RULES — EXECUTION PROTOCOL (FINAL)

---

## 📋 IA-FIRST DESIGN NOTICE

> **This documentation is designed for AI analysis AND human reading.**
> 
> **Structure guarantees for AI agents:**
> - Consistent heading hierarchy (H1→H2→H3 → content)
> - Explicit section markers (🔴 CRITICAL vs 🟢 SAFE)
> - Structured lists (not prose paragraphs)
> - Clear cross-references with `[text](path)` format
> - Single idea per section (easy to parse/reuse)
> - No language mixing (English only)
> - Metadata in headers using emojis (🚀, ✅, ❌, 🎯)

**If you modify this file:**
1. Preserve heading hierarchy
2. Use lists instead of prose
3. Add emoji markers for quick scanning
4. Never mix Portuguese + English
5. Keep one idea per section

---

## 🧠 1. Execution Awareness (MANDATORY)

Before any action:

1. Read:
   - `/EXECUTION/spec/custom/[PROJECT_NAME]/development/execution-state/_current.md`

2. If applicable:
   - Check active thread in `/EXECUTION/spec/custom/[PROJECT_NAME]/development/execution-state/threads/`

3. Never assume implicit state

> **See also:** [Project-Specific Instantiation](../../custom/rpg-narrative-server/SPECIALIZATIONS/ia-rules-rpg-specific.md)

---

## ⚖️ 2. Source of Truth Priority

Authority order:

1. `/EXECUTION/spec/CANONICAL/rules/ia-rules.md` (execution rules)
2. `/EXECUTION/spec/custom/[PROJECT_NAME]/development/execution-state/_current.md` (project state)
3. `/EXECUTION/spec/custom/[PROJECT_NAME]/development/execution-state/threads/*` (active threads)
4. `/EXECUTION/spec/CANONICAL/specifications/` (immutable architecture)
5. `/EXECUTION/spec/custom/[PROJECT_NAME]/reality/` (observed state)

If conflict arises:
→ ALWAYS prioritize CANONICAL (immutable authority)

> **For rpg-narrative-server project:** See [Project State Mapping](../../custom/rpg-narrative-server/SPECIALIZATIONS/ia-rules-rpg-specific.md#source-of-truth-paths)

---

## 🎯 3. Task Execution Rules

- Follow "Next Actions" strictly
- Do not skip steps
- Do not anticipate future implementations

---

## 🚫 4. Hard Constraints (Generic)

NEVER:

- Introduce breaking changes without proper deprecation (see [Backward Compatibility Policy](./backward-compatibility-policy.md))
- Modify infrastructure outside scope
- Infer external service behavior (treat as black box)
- Create unnecessary abstractions
- Refactor without explicit business reason documented

> **Project-specific constraints:** See [rpg-narrative-server specializations](../../custom/rpg-narrative-server/SPECIALIZATIONS/ia-rules-rpg-specific.md#hard-constraints)

---

## 🧩 5. Module Isolation

Each module must be:

- Independent
- Replaceable
- Testable in isolation

Communication only via explicit contracts

---

## 📦 6. External Service Rule (Generic)

All external services (search indexes, LLMs, databases) operate as BLACK BOX components.

**Reference:** `/EXECUTION/spec/CANONICAL/specifications/architecture.md#external-services-black-box`

**Key Points:**
- Access ONLY via Port abstractions (Ports & Adapters)
- Treat as non-authoritative data sources
- Never couple domain logic to implementation
- Mock ports in tests, never actual implementations
- Must have fallback/degradation behavior
- Never assume behavior beyond contract

For detailed rules, examples, and testing patterns:
→ See [architecture.md](/EXECUTION/spec/CANONICAL/specifications/architecture.md#external-services-black-box)

**Project-specific examples:**
→ See [rpg-narrative-server vector index rules](../../custom/rpg-narrative-server/SPECIALIZATIONS/ia-rules-rpg-specific.md#external-services)

---

## 🧪 7. Test-Driven Behavior

If tests fail:

1. DO NOT ignore
2. DO NOT bypass
3. Fix root cause

**CRITICAL:** Never modify production code to satisfy tests.

**Reference:** `/EXECUTION/spec/CANONICAL/specifications/testing.md`

For comprehensive testing strategies:
→ See [testing.md](/EXECUTION/spec/CANONICAL/specifications/testing.md)

---

## 🧵 8. Thread Isolation

If working in a thread:

- Do NOT access other threads
- Do NOT mix decisions
- Do NOT share implicit state

---

## 📍 9. Checkpointing Protocol

After relevant changes:

MANDATORY:

1. Update:
   - /EXECUTION/spec/custom/rpg-narrative-server/development/execution-state/_current.md

2. Create:
   - new checkpoint in /EXECUTION/spec/custom/rpg-narrative-server/development/checkpoints/

---

## 🧬 10. Change Discipline

Every change must:

- Have clear reason
- Have mapped impact
- Respect architecture

---

## 🧠 11. Cognitive Load Reduction

The AI must:

- Prefer simplicity
- Avoid premature abstraction
- Avoid multiple paths

---

## 🔍 12. Decision Transparency

Always make explicit:

- What was decided
- Why it was decided
- Expected impact

---

## 🚀 13. Execution Mode

Always assume:

> The system is incomplete and evolving

Expected behavior:

- Incremental
- Safe
- Traceable

---

## 🤖 14. AI Handoff Compliance

Always respect blocks:

"🤖 AI Handoff"

They define:

- Real scope
- Limits
- Next action

---

## ❌ 15. Anti-Patterns (FORBIDDEN)

- "Refactor everything"
- "Improve general architecture" without context
- Create coupling between modules
- Ignore current state
- Work outside defined flow

---

## ✅ 16. Definition of Done

A task is only complete if:

- Code implemented
- Tests passing
- execution_state updated
- checkpoint created

---

## 🔚 Final Directive

You are not designing a system.

You are **continuing a running system**.

Priority is:

→ Consistency > Elegance
→ Current state > Idealization