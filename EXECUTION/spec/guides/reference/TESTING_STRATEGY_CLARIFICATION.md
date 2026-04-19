# 🧪 TESTING STRATEGY CLARIFICATION

**Version:** 1.0  
**Status:** Resolves role conflict between testing.md and testing_strategy_spec.md  
**Purpose:** Clear guidance on which testing doc to use when

---

# 🎯 THE ISSUE

You have TWO testing documents:

1. **testing.md** — "How to test each layer"
2. **testing_strategy_spec.md** — "Rules that tests must follow"

They seem redundant. They're not. They're complementary. This doc explains:

- **WHAT each one does**
- **WHEN to use each**
- **HOW they work together**

---

# 📖 DOCUMENT ROLES (CLEAR)

## testing_strategy_spec.md

**Type:** Normative (defines rules, not patterns)

**Purpose:** Enforce QUALITY and STRUCTURE

**Contains:**
- ✅ Testing PRINCIPLES (not implementation details)
- ✅ Testing RULES (isolation, async, no mocking adapters)
- ✅ Testing VALIDATION CRITERIA (deterministic, isolated, readable)
- ✅ Testing ANTI-PATTERNS (what NOT to do)

**Think of it as:** "The Constitution of Testing"

**When to use:**
- When validating if a test is correct
- When questioning if a test follows rules
- When reviewing a test for quality
- When deciding if a pattern is allowed

**Example questions it answers:**
- "Can I mock this adapter?" → No, mock ports only
- "Should this test be deterministic?" → Yes, always
- "Is this test design wrong?" → Check anti-patterns section

---

## testing.md

**Type:** Practical (defines patterns with code examples)

**Purpose:** Show HOW to implement tests correctly

**Contains:**
- ✅ Testing PATTERNS by layer (code examples for each)
- ✅ Testing STRATEGIES (unit vs integration vs contract)
- ✅ Testing FIXTURES and FAKES (reusable test components)
- ✅ Testing EXAMPLES with actual code
- ✅ Testing CHECKLIST by test level

**Think of it as:** "The Cookbook of Testing"

**When to use:**
- When implementing a test
- When unsure of the pattern for a layer
- When looking for code examples
- When learning how to mock ports
- When setting up test fixtures

**Example questions it answers:**
- "How do I test a UseCase?" → Mock the port, see example
- "What's a fake adapter?" → See implementation and when to use
- "How do I set up an integration test?" → See the pattern
- "How do I validate error handling?" → See the test example

---

# 🔄 HOW THEY WORK TOGETHER

### Workflow

1. **You're implementing a test**
2. **Read testing.md** → Find the layer pattern
3. **Read testing_strategy_spec.md** → Validate it follows the rules
4. **Implement** → Using both as guide and validator

### Example: Testing a UseCase

```
Task: Write test for GetPlayerUseCase

Step 1: Read testing.md
  └─ Find "UseCase Tests" section
     ├─ See pattern: Mock port, call usecase, assert result
     ├─ See example code
     └─ Copy the pattern

Step 2: Read testing_strategy_spec.md
  └─ Validate rules:
     ├─ Mock Ports? ✅ Yes, that's the pattern
     ├─ Call real infrastructure? ✅ No, mock it
     ├─ Test contract vs implementation? ✅ Contract
     ├─ Use async/await? ✅ Yes, await the coroutine
     └─ Is this deterministic? ✅ Yes, no randomness

Step 3: Write the test
  └─ Use pattern from testing.md
  └─ Validate with rules from testing_strategy_spec.md
  └─ Submit!
```

---

# 🎯 QUICK DECISION TREE

### "I need to write a test. What do I read?"

```
"I'm implementing a new test"
  ↓
→ Start with testing.md
   (Find your layer, see the pattern)
  ↓
→ Then check testing_strategy_spec.md
   (Validate you're following the rules)
  ↓
→ Implement with confidence!
```

### "I'm reviewing a test. Is it correct?"

```
"Does this test pass validation?"
  ↓
→ Start with testing_strategy_spec.md
   (Check against rules: isolation, async, etc.)
  ↓
→ Then verify pattern in testing.md
   (Is the pattern correct for this layer?)
  ↓
→ Approve or request changes!
```

### "I'm confused about a pattern. Which doc?"

```
"What's the RIGHT way to do this?"
  ↓
→ Read testing.md
   (See the pattern with examples)
  ↓
→ If still confused, read testing_strategy_spec.md
   (Understand the underlying rules)
  ↓
→ Now you know why the pattern exists!
```

---

# 📋 CROSS-REFERENCE TABLE

| Need | File | Section |
|------|------|---------|
| I need to test Domain layer | testing.md | "Domain Tests" |
| Domain tests must follow what rules? | testing_strategy_spec.md | "Test Structure Rules" |
| I need to test UseCase layer | testing.md | "UseCase Tests" |
| UseCase tests must follow what rules? | testing_strategy_spec.md | "Mocking Strategy" |
| I need to test Adapter layer | testing.md | "Adapter Tests" |
| Adapter tests must follow what rules? | testing_strategy_spec.md | "Isolation Rules" |
| I need to test Route/Interface | testing.md | "Interface Tests" |
| Interface tests must follow what rules? | testing_strategy_spec.md | "Contract Awareness" |
| Can I mock this? | testing_strategy_spec.md | "Mocking Strategy" |
| What's a Fake vs Mock? | testing.md | "Mocking Strategy" section |
| How do I assert correctly? | testing.md | "Behavior Validation" |
| Are my tests deterministic? | testing_strategy_spec.md | "Test Quality Criteria" |
| Is my test isolated? | testing_strategy_spec.md | "Isolation Rules" |
| Is my test readable? | testing_strategy_spec.md | "Test Quality Criteria" |
| Common test mistakes? | testing_strategy_spec.md | "Anti-Patterns" |
| How to set up fixtures? | testing.md | "Fixtures and Fakes" |
| Vector Index testing? | testing.md | "Vector Index Testing" |

---

# 🧠 MENTAL MODEL

Think of it this way:

```
testing_strategy_spec.md = RULES (Guard Rails)
                           "You can NOT do this"
                           "This MUST be true"

testing.md = PATTERNS (Road Map)
             "Do it THIS way"
             "Here's an example"

Together = Complete Testing System
           Rules prevent mistakes
           Patterns show the way
```

---

# ✅ RESOLUTION: NOT DUPLICATE, COMPLEMENTARY

**Old confusion:** "These say the same thing"

**New clarity:** 
- testing_strategy_spec.md = What to validate
- testing.md = How to implement

**Together they answer:**
- ✅ "Is my test correct?" (via testing_strategy_spec.md)
- ✅ "How do I write a good test?" (via testing.md)

---

# 🔄 UPDATED FILE USAGE

### testing_strategy_spec.md

**Status:** ✅ NORMATIVE — Keep as-is

**Purpose:** Enforce testing quality standards

**When to reference:** During code review, test validation

**Updated description:**
```
Normative specification of testing quality.

Defines:
- Testing rules (what must be true)
- Testing validation criteria (how to verify correctness)
- Anti-patterns (what to avoid)

Use this to:
1. Validate test quality
2. Enforce testing discipline
3. Review test structure
4. Ensure isolation and determinism

Pair with testing.md for implementation patterns.
```

---

### testing.md

**Status:** ✅ PRACTICAL — Keep as-is

**Purpose:** Guide test implementation with patterns and examples

**When to reference:** During test implementation

**Updated description:**
```
Practical guide to testing with patterns and examples.

Defines:
- Testing patterns by layer (with code)
- Testing strategies (unit, integration, contract)
- Fixture and fake adapter implementations
- Testing checklist and validation

Use this to:
1. Implement tests correctly
2. Find code examples for your layer
3. Understand fake vs mock adapters
4. Set up test fixtures

Pair with testing_strategy_spec.md for quality validation.
```

---

# 🎯 EXAMPLE: Complete Test Workflow

### Implement Domain Test

1. **Open:** testing.md (section: "Domain Tests")
   - See pattern: Pure functions, no mocks
   - See example code
   - Copy structure

2. **Implement test**

3. **Validate:** testing_strategy_spec.md
   - [ ] No mocks? ✅
   - [ ] Deterministic? ✅
   - [ ] Isolated? ✅
   - [ ] Readable? ✅

4. **Approved!** ✅

### Implement UseCase Test

1. **Open:** testing.md (section: "UseCase Tests")
   - See pattern: Mock ports, call usecase
   - See example with AsyncMock
   - Copy structure

2. **Implement test**

3. **Validate:** testing_strategy_spec.md
   - [ ] Mocking ports only? ✅
   - [ ] No real infrastructure? ✅
   - [ ] Async/await correct? ✅
   - [ ] Testing behavior not implementation? ✅

4. **Approved!** ✅

---

# 🚀 CONCLUSION

**Before (Confusing):**
- Two similar-looking test docs
- Unclear which to use when
- Risk of confusion about requirements

**After (Clear):**
- testing_strategy_spec.md = Rules (validator)
- testing.md = Patterns (implementer)
- Use together: Read pattern, then validate

**Key Insight:** 
They're not duplicates. They're partners.
- One says "how to build correctly"
- One says "here's the correct result"
- Together they ensure quality.

---

# 📚 REFERENCES

- `/docs/ia/CANONICAL/specifications/testing.md` → Patterns and examples
- `/docs/ia/specs/_shared/testing_strategy_spec.md` → Rules and validation
- `/docs/ia/IMPLEMENTATION_ROADMAP.md` → When to read each (Step 6-7)
- `/docs/ia/CANONICAL/specifications/definition_of_done.md` → Validation checklist
