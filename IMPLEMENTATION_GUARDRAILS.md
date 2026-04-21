# Implementation Guardrails: Planejamento → Código → Documentação

**Objetivo:** Evitar gap entre planejamento, documentação e execução  
**Aplicável a:** v3.1-beta.1 e releases futuras  
**Owner:** Development team + User

---

## 🚨 THE GAP (What We're Fixing)

```
BEFORE (This session):
Planejamento (vago/conhecimento do usuário)
         ↓ (sem comunicação clara)
Documentação (interpretação do agente)
         ↓ (pode estar errada!)
Execução (risco de código errado)

AFTER (With guardrails):
Planejamento (ESCRITO, ASSINADO pelo usuário)
         ↓ (com documento assinado)
Spec Design (VERIFICADO antes de código)
         ↓ (código só começa se spec ok)
Código + Testes (IMPLEMENTAM spec exatamente)
         ↓ (code review verifica alinhamento)
Documentação (ATUALIZADA com código, não depois)
```

---

## 📋 GUARDRAIL 1: Design Review (Before Code)

### When to Apply
- [ ] Qualquer feature nova
- [ ] Qualquer mudança em arquitetura
- [ ] Qualquer mudança de camada (MANDATE, GUIDELINES, OPERATIONS)
- [ ] Qualquer modificação no compilador ou RTK

### Process

```
Step 1: Design Document (Written First)
  ├─ Arquivo: FEATURE_DESIGN_<name>.md
  ├─ Conteúdo:
  │  ├─ Problem statement
  │  ├─ Proposed solution
  │  ├─ Architecture diagram
  │  ├─ Data flow
  │  ├─ Dependencies
  │  ├─ Edge cases
  │  └─ Backward compatibility notes
  └─ Location: /docs/designs/

Step 2: Review by User (Before Implementation)
  ├─ User reads design
  ├─ User confirms: "This matches what I intended?"
  ├─ User signals: "Approved ✅" or "Revise ❌"
  └─ No code starts until ✅

Step 3: Specification Lock
  ├─ Design marked as LOCKED
  ├─ Changes during implementation require user approval
  ├─ Prevents scope creep
  └─ Ensures alignment stays intact
```

### Example Design Document Template

```markdown
# Feature Design: <Feature Name>

## Problem
[What problem does this solve?]

## Solution
[How will we solve it?]

## Architecture
[Diagram or text description]

## Data Flow
[How data moves through the system]

## Implementation Plan
- [ ] Component A
- [ ] Component B
- [ ] Tests for each
- [ ] Documentation

## Edge Cases
[What can go wrong?]

## Backward Compatibility
[Does this break existing code?]

## Verification
[How will we know this is correct?]
```

---

## 📋 GUARDRAIL 2: Specification Document (Technical Spec)

### When to Apply
- [ ] Before implementing any new component
- [ ] Before modifying existing APIs
- [ ] Before changing data structures

### Content

```
Spec Document must include:

1. DATA STRUCTURES
   ├─ Input format (type, validation rules)
   ├─ Output format (type, validation rules)
   └─ Internal representations

2. ALGORITHMS
   ├─ Steps in order
   ├─ Complexity analysis
   ├─ Edge case handling
   └─ Error scenarios

3. INTEGRATION POINTS
   ├─ What calls this?
   ├─ What does this call?
   ├─ Dependencies
   └─ State management

4. TEST CASES (Written Before Code!)
   ├─ Happy path
   ├─ Edge cases
   ├─ Error cases
   └─ Performance requirements

5. REFERENCE IMPLEMENTATION
   ├─ Pseudo-code or working example
   └─ Demonstrates correctness
```

### Location & Format

```
File: docs/specs/COMPONENT_<name>.md
  
Example:
  docs/specs/COMPONENT_compilation_model.md
  docs/specs/COMPONENT_operations_layer.md
```

---

## 📋 GUARDRAIL 3: Code Matches Design

### Code Review Checklist

```
Before merging any PR, reviewer checks:

[ ] Code implements DESIGN as specified
[ ] Code implements SPEC as specified
[ ] No features added beyond scope
[ ] All edge cases handled
[ ] All error paths tested
[ ] No ambiguity in logic
[ ] Architecture layers respected
    ├─ MANDATE layer unchanged?
    ├─ GUIDELINES layer customizable?
    ├─ OPERATIONS layer stateful?
[ ] No breaking changes to APIs
[ ] Documentation updated
[ ] Tests all passing (111/111)
[ ] No new warnings or errors
```

### Code Comment Format

```python
# When code makes a design decision:

def critical_function():
    # DESIGN: [reference to design doc]
    # SPEC: [reference to spec section]
    # DECISION: [why we chose this approach]
    pass
```

---

## 📋 GUARDRAIL 4: Tests Verify Decisions

### Test Structure

```
For each DESIGN DECISION, there's a TEST:

Design says: "MANDATE is immutable"
     ↓
Test: test_mandate_immutability()
     ↓
Validates: MANDATE cannot be changed at runtime

Design says: "RTK patterns match 50+ types"
     ↓
Test: test_rtk_pattern_coverage()
     ↓
Validates: All 50+ patterns work correctly

Design says: "Compilation produces immutable binary"
     ↓
Test: test_compiled_binary_immutable()
     ↓
Validates: Binary cannot be tampered with
```

### Test File Convention

```
For FEATURE_DESIGN_<name>.md, create:
  tests/test_design_<name>.py

Examples:
  FEATURE_DESIGN_compilation_model.md → test_design_compilation_model.py
  FEATURE_DESIGN_operations_layer.md → test_design_operations_layer.py
```

---

## 📋 GUARDRAIL 5: Documentation Updated with Code

### Documentation Sync Points

```
WHEN CODE CHANGES:

1. DESIGN document updated (if design changed)
2. SPEC updated (if spec changed)
3. API_REFERENCE.md updated (if API changed)
4. CODE updated with comments
5. TESTS updated to match new behavior
6. USER_GUIDE.md updated (if user-facing)
7. CHANGELOG.md updated (for release)

NO DOCUMENTATION IS LEFT BEHIND!
```

### Documentation Checklist (Before Code Merge)

```
[ ] Design doc updated (if applicable)
[ ] Spec doc updated (if applicable)
[ ] API reference updated
[ ] Code comments added
[ ] Docstrings complete
[ ] README updated (if needed)
[ ] CHANGELOG updated
[ ] Examples updated (if applicable)
[ ] Troubleshooting guide updated (if applicable)
```

---

## 🔄 Implementation Workflow (Using Guardrails)

```
Feature Request Received
    ↓
1. DESIGN PHASE (User + Agent)
   ├─ Write FEATURE_DESIGN_<name>.md
   ├─ Include diagrams, data flow
   ├─ User reviews & approves
   └─ Design LOCKED
    ↓
2. SPEC PHASE (Agent)
   ├─ Write COMPONENT_<name>.md
   ├─ Include data structures, algorithms
   ├─ Include test cases (before code!)
   └─ Ready for implementation
    ↓
3. DEVELOPMENT PHASE (Agent)
   ├─ Implement exactly to spec
   ├─ Code comments reference design
   ├─ Write tests from spec
   ├─ All tests green (111/111)
   └─ Code review against design
    ↓
4. DOCUMENTATION PHASE (Agent)
   ├─ Update all docs together
   ├─ Add examples if applicable
   ├─ Update CHANGELOG
   ├─ Verify documentation complete
   └─ Ready for release
    ↓
5. VERIFICATION PHASE (User)
   ├─ Test that it works as intended
   ├─ Verify design matches implementation
   ├─ Confirm documentation is clear
   └─ Sign off: Ready to release
    ↓
6. RELEASE
   └─ Tag version, publish
```

---

## 📊 Guardrails Checklist (v3.1-beta.1)

### Features in v3.1-beta.1

```
Feature 1: 3-Layer MANDATE/GUIDELINES/OPERATIONS
  [ ] Design doc: FEATURE_DESIGN_3layer_model.md
  [ ] Spec doc: COMPONENT_3layer_architecture.md
  [ ] Code: Reflects design exactly
  [ ] Tests: Verify each layer behavior
  [ ] Docs: ARCHITECTURE.md explains model

Feature 2: 2-Stage Compilation (Override System)
  [ ] Design doc: FEATURE_DESIGN_compilation.md
  [ ] Spec doc: COMPONENT_compilation_model.md
  [ ] Code: Compiler implements 2 stages
  [ ] Tests: Stage 1 + Stage 2 verified
  [ ] Docs: COMPILER.md explains stages

Feature 3: Dynamic Feature Selection (Wizard)
  [ ] Design doc: FEATURE_DESIGN_wizard.md
  [ ] Spec doc: COMPONENT_wizard_selection.md
  [ ] Code: Wizard asks questions, compiles
  [ ] Tests: All profiles (IDE + atomic) work
  [ ] Docs: QUICK_START.md shows wizard flow

Feature 4: .sdd/ Root Structure
  [ ] Design doc: FEATURE_DESIGN_sdd_structure.md
  [ ] Spec doc: COMPONENT_directory_structure.md
  [ ] Code: Structure created correctly
  [ ] Tests: Idempotence verified
  [ ] Docs: CONFIGURATION.md explains structure

Feature 5: RTK Patterns (50+)
  [ ] Design doc: FEATURE_DESIGN_rtk_patterns.md
  [ ] Spec doc: COMPONENT_pattern_system.md
  [ ] Code: All 50+ patterns working
  [ ] Tests: Pattern matching verified
  [ ] Docs: RTK.md lists all patterns

Feature 6: MessagePack Binary Format
  [ ] Design doc: FEATURE_DESIGN_msgpack_format.md
  [ ] Spec doc: COMPONENT_binary_encoding.md
  [ ] Code: Encoder/decoder complete
  [ ] Tests: Performance verified
  [ ] Docs: Explain format, compatibility
```

---

## 🎯 Key Principles (To Remember)

```
1. DESIGN FIRST, CODE LATER
   ├─ Never code before design approval
   ├─ Design catches mistakes early
   └─ Saves time on rewrites

2. SPEC DRIVES TESTS
   ├─ Tests written from spec
   ├─ Tests verify spec compliance
   └─ Code must pass all tests

3. CODE EQUALS DOCUMENTATION
   ├─ Code comments explain decisions
   ├─ Tests document behavior
   ├─ Examples show usage
   └─ No "hidden knowledge"

4. NO SURPRISES
   ├─ User approves design before code
   ├─ Code does exactly what design says
   ├─ Tests prove it works
   └─ Documentation explains it clearly

5. AMBIGUITY = FAILURE
   ├─ Anything unclear = design flaw
   ├─ Resolve before coding
   ├─ Document the resolution
   └─ Test to prove it works
```

---

## 📝 Guardrails Implementation Status (v3.1-beta.1)

```
NOW APPLYING TO:
├─ [ ] 3-Layer Architecture Design
├─ [ ] 2-Stage Compilation Spec
├─ [ ] Wizard Feature Selection Spec
├─ [ ] .sdd/ Directory Structure Spec
├─ [ ] RTK Pattern System Spec
└─ [ ] MessagePack Binary Format Spec

STARTING WITH:
└─ [ ] FEATURE_DESIGN_3layer_model.md (to be created)
```

---

**Status:** Guardrails defined and ready to use  
**Next:** Create design docs for each v3.1-beta.1 feature  
**Benefit:** Zero ambiguity, zero surprises, 100% alignment
