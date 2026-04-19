# 🔍 Search Keywords — Quick Discovery

**Purpose:** Keyword mapping to find documentation under demand  
**Updated:** [auto-filled by agent]  
**Usage:** When you don't know the exact file name, search here first  

---

## 📌 Keyword to Document Mapping

### Architecture & Structure

| Keyword | Found In | Reason |
|---------|----------|--------|
| architecture | CANONICAL/specifications/architecture.md | 8-layer structure |
| layers | CANONICAL/specifications/architecture.md | Domain, usecases, etc |
| domain | CANONICAL/specifications/architecture.md | Core business logic |
| ports | CANONICAL/decisions/ADR-003 | Dependency inversion |
| adapters | CANONICAL/decisions/ADR-003 | Infrastructure abstraction |
| infrastructure | CANONICAL/specifications/architecture.md | Tech layer |
| clean code | CANONICAL/specifications/architecture.md | Code organization |

### Rules & Governance

| Keyword | Found In | Reason |
|---------|----------|--------|
| rules | CANONICAL/rules/ia-rules.md | 16 mandatory protocols |
| mandatory | CANONICAL/rules/ia-rules.md | Non-negotiable |
| protocols | CANONICAL/rules/ia-rules.md | Execution guidelines |
| constitution | CANONICAL/constitution.md | 15 principles |
| principles | CANONICAL/constitution.md | Foundation |
| immutable | CANONICAL/constitution.md | Never changes |
| governance | CANONICAL/rules/ia-rules.md | Control framework |

### Testing & Quality

| Keyword | Found In | Reason |
|---------|----------|--------|
| testing | CANONICAL/specifications/testing.md | Test patterns |
| TDD | CANONICAL/specifications/testing.md | Test-driven development |
| unit test | CANONICAL/specifications/testing.md | Single unit tests |
| integration test | CANONICAL/specifications/testing.md | Multiple units |
| contract test | CANONICAL/specifications/testing.md | Port testing |
| golden test | CANONICAL/specifications/testing.md | Full flow test |
| coverage | CANONICAL/specifications/testing.md | Coverage requirements |
| quality | CANONICAL/specifications/testing.md | QA approach |

### Development Workflow

| Keyword | Found In | Reason |
|---------|----------|--------|
| PHASE 0 | guides/onboarding/PHASE-0 | Agent initialization |
| onboarding | guides/onboarding/PHASE-0 | First-time setup |
| AGENT_HARNESS | guides/onboarding/AGENT_HARNESS | 7-phase workflow |
| workflow | guides/onboarding/AGENT_HARNESS | Development process |
| PATH A/B/C/D | guides/onboarding/AGENT_HARNESS | Work selection |
| phases | guides/onboarding/AGENT_HARNESS | 1-7 protocol phases |
| quiz | guides/onboarding/VALIDATION_QUIZ | Knowledge check |
| validation | guides/onboarding/VALIDATION_QUIZ | Learning verification |

### Context Management

| Keyword | Found In | Reason |
|---------|----------|--------|
| context-aware | guides/runtime/CONTEXT_AWARE_USAGE | Dynamic infrastructure |
| task-progress | guides/runtime/CONTEXT_AWARE_USAGE | Task tracking |
| analysis | guides/runtime/CONTEXT_AWARE_USAGE | Discovery storage |
| discovery | guides/runtime/CONTEXT_AWARE_USAGE | Learning record |
| runtime-state | guides/runtime/CONTEXT_AWARE_USAGE | Metrics tracking |
| handoff | guides/runtime/CONTEXT_AWARE_USAGE | Agent transition |
| checkpoint | guides/runtime/CONTEXT_AWARE_USAGE | Work documentation |

### Collaboration & Code Review

| Keyword | Found In | Reason |
|---------|----------|--------|
| code review | guides/operational/code-review.md | PR process |
| PR | guides/operational/code-review.md | Pull request |
| approval | guides/operational/code-review.md | Merge criteria |
| collaboration | guides/operational/code-review.md | Team work |
| thread isolation | CANONICAL/decisions/ADR-004 | Concurrent work |
| concurrent | CANONICAL/decisions/ADR-004 | Multiple developers |

### Operations & Deployment

| Keyword | Found In | Reason |
|---------|----------|--------|
| deployment | guides/operational/deployment-rollback.md | Production release |
| rollback | guides/operational/deployment-rollback.md | Reverting changes |
| production | guides/operational/deployment-rollback.md | Live environment |
| monitoring | guides/operational/deployment-rollback.md | Health check |
| performance | guides/operational/performance-optimization.md | Speed optimization |
| security | guides/operational/security-compliance.md | Data protection |
| compliance | guides/operational/security-compliance.md | Regulations |

### Emergency & Troubleshooting

| Keyword | Found In | Reason |
|---------|----------|--------|
| error | guides/emergency/ | Problem resolution |
| broken | guides/emergency/ | System failure |
| incident | guides/emergency/incident-response.md | Production issue |
| recovery | guides/emergency/ | Fix procedure |
| emergency | guides/emergency/ | Crisis handling |
| hook failure | guides/emergency/PRE_COMMIT_HOOK_FAILURE.md | Pre-commit error |
| corruption | guides/emergency/AUTO_FIX_CORRUPTION_RECOVERY.md | Data corruption |
| CI/CD | guides/emergency/CI_CD_GATE_FAILURE.md | Build failure |

---

## 🎯 Common Scenarios

### Scenario: "I don't know what rules apply"
**Search:** rules, mandatory  
**Go to:** CANONICAL/rules/ia-rules.md  
**Result:** 16 mandatory protocols

### Scenario: "How do I structure my code?"
**Search:** architecture, layers, domain  
**Go to:** CANONICAL/specifications/architecture.md  
**Result:** 8-layer clean architecture guide

### Scenario: "Should I write tests first?"
**Search:** TDD, testing, quality  
**Go to:** CANONICAL/specifications/testing.md  
**Result:** Yes, TDD is mandatory (Rule 4)

### Scenario: "How do I manage my work?"
**Search:** task-progress, context-aware, checkpoint  
**Go to:** guides/runtime/CONTEXT_AWARE_USAGE.md  
**Result:** Task tracking in .ai/context-aware/

### Scenario: "Something in production broke"
**Search:** incident, emergency, error  
**Go to:** guides/emergency/incident-response.md  
**Result:** 5-step incident response procedure

### Scenario: "I'm new, where do I start?"
**Search:** PHASE 0, onboarding, workflow  
**Go to:** guides/onboarding/PHASE-0-AGENT-ONBOARDING.md  
**Result:** 6-step initialization

---

## 💡 Pro Tips

**Tip 1:** Most questions answered in these 3 files:
1. CANONICAL/rules/ia-rules.md (rules)
2. guides/onboarding/AGENT_HARNESS.md (workflow)
3. guides/runtime/CONTEXT_AWARE_USAGE.md (tracking)

**Tip 2:** Before asking for help:
1. Search this file
2. Go to suggested document
3. Read completely
4. If still unclear, ask with context

**Tip 3:** When troubleshooting:
1. Note exact error
2. Search keywords here
3. Follow recovery procedure
4. Document in analysis/ what you learned

---

## 🔄 When to Update This

**Add entry when:**
- New document created in spec-architecture
- New keyword helps agents discover docs
- Common question patterns emerge
- Mapping becomes unclear or outdated

**Update frequency:** ~once per month or per new guide

---

**Location:** .ai/runtime/search-keywords.md  
**Purpose:** On-demand context discovery  
**Authority:** Agent-driven updates + spec-architecture sync
