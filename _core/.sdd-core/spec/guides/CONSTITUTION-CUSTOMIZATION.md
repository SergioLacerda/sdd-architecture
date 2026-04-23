# 🛠️ Constitution Customization Guide

**How to adapt SDD framework to your specific project needs**

---

## When to Customize

**You should customize your Constitution if:**
- ✅ Your domain has different scale needs (embedded vs cloud)
- ✅ Your tech stack differs from Python/FastAPI
- ✅ Your team has different constraints
- ✅ You need fewer/more layers than the standard architecture
- ✅ You want to emphasize certain principles over others

**You should NOT customize if:**
- ❌ You just want to skip a rule because it's inconvenient (try LITE first)
- ❌ You haven't tried following the standard Constitution yet
- ❌ You're unsure why a rule exists

---

## What's Immutable vs Flexible

### ✅ Immutable Core (DO NOT CHANGE)

These 5 principles must stay in every SDD Constitution:

1. **Clean separation of concerns** — Business logic isolated from infrastructure
2. **Explicit governance** — Rules documented, not implicit
3. **Test discipline** — Tests validate every feature
4. **Progressive scaling** — Start simple, grow structure as needed
5. **Traceability** — Every decision documented

### ✅ Flexible (You Choose)

These aspects can be customized:

- **Number of layers** — 4-layer, 6-layer, 8-layer depending on your needs
- **Specific ports** — What adapter contracts your domain needs
- **Testing strategy** — Unit/integration/e2e ratio for your scale
- **Async requirements** — Optional if not applicable (embedded systems)
- **Tools & frameworks** — Use what fits your stack
- **Rule count** — ULTRA-LITE (3) → LITE (5) → FULL (16)
- **DoD criteria** — Customize what "done" means for your team

---

## Step-by-Step Customization

### Step 1: Choose Your Baseline

**Option A: Customize ULTRA-LITE (Fastest)**
- Start with `/EXECUTION/spec/guides/adoption/templates/lite-constitution.yaml`
- Modify the 5 principles for your domain
- Takes: 15 minutes

**Option B: Customize LITE (Recommended)**
- Start with `/EXECUTION/spec/guides/adoption/LITE-ADOPTION.md`
- Create your own `constitution.md`
- Takes: 30 minutes

**Option C: Specialize FULL (Advanced)**
- Start with `/EXECUTION/spec/CANONICAL/rules/constitution.md`
- Create a specialization in `/EXECUTION/spec/custom/[your-project]/`
- Takes: 1-2 hours

### Step 2: Identify Your Constraints

Answer these questions:

1. **What's your scale?**
   - Solo dev → ULTRA-LITE
   - Small team (< 5) → LITE
   - Production system → FULL

2. **What's your primary I/O pattern?**
   - Async (web services) → Keep async-first principle
   - Synchronous (CLI) → Customize async requirement
   - Mixed → Add async where needed

3. **How many architectural layers do you need?**
   - Embedded system (fixed infra) → 4-layer
   - Standard web app → 6-8 layer
   - Complex domain → 8+ layers

4. **What tests matter most?**
   - Solo dev → Unit tests only
   - Small team → Unit + Integration
   - Production → Unit + Integration + E2E + Security

5. **What's your biggest risk?**
   - Data corruption → Add persistence validation
   - Performance → Add latency benchmarks
   - Security → Add security tests
   - Scale → Add load testing

### Step 3: Create Your Constitution

Create `.ai/constitution.md` in your project:

```markdown
# [Your Project] Constitution

**Version:** 2.1-lite-custom  
**Team:** [Your team]  
**Baseline:** SDD LITE with customizations

## Core Principles

### Principle 1: Clean Separation
[Explain for your domain]

### Principle 2: ...
[etc.]

## Your 3-5 Rules

### Rule 1: ...
### Rule 2: ...
### Rule 3: ...

## Definition of Done (5 items)

- [ ] Feature implemented
- [ ] Tests passing
- [ ] [Your #3]
- [ ] [Your #4]
- [ ] [Your #5]

## Customizations from SDD LITE

**We changed:**
- [Async requirement waived because: embedded system]
- [Simplified to 4-layer because: fixed infrastructure]
- [Added: load testing requirement]

**We kept:**
- [Clean separation]
- [Explicit rules]
- [Test discipline]
```

### Step 4: Document Your Deviations

For each customization, explain:

1. **What** — What principle/rule did you change?
2. **Why** — Why was the standard version not suitable?
3. **How** — What's your alternative?
4. **Validation** — How do you validate this works?

**Example:**

```markdown
## Customization: No Async-First

**What:** We removed the "async-first" principle

**Why:** 
- Embedded system with single-threaded event loop
- All I/O is sequential and blocking
- Async would add unnecessary complexity

**How:**
- Single-threaded execution model
- Clear sequential I/O operations
- All functions are `def`, not `async def`

**Validation:**
- Code review: Verify no async/await in codebase
- Tests: No asyncio usage

**Trade-off:**
- ❌ Can't handle high concurrency
- ✅ Simpler for developers
- ✅ Appropriate for embedded constraints
```

### Step 5: Validate Your Custom Constitution

**Add these to your CI/CD:**

```bash
# Validate your constitution syntax
python -c "import yaml; yaml.safe_load(open('.ai/constitution.yaml'))"

# Check your code matches the constitution
pytest tests/constitution/

# Example test:
def test_no_framework_in_domain():
    """Validate customization: no framework imports in domain"""
    result = os.system('grep -r "import fastapi" src/domain/')
    assert result != 0, "Framework leaked into domain!"

def test_layer_separation():
    """Validate customization: 4-layer separation"""
    # Check that your 4 layers exist
    assert os.path.exists('src/domain/')
    assert os.path.exists('src/services/')
    assert os.path.exists('src/adapters/')
    assert os.path.exists('src/main.py')
```

### Step 6: Version Your Constitution

Track changes like you'd track code:

```markdown
# [Your Project] Constitution

**Version:** 2.1-lite-custom-v1.2  
**Last Updated:** 2026-04-20  
**Updated By:** [Who changed it]  
**Changed:** [What changed from v1.1]

## Change History

### v1.2 (2026-04-20)
- Added load testing requirement (Rule 3)
- Increased concurrent entity requirement from 10 to 20

### v1.1 (2026-04-15)
- Simplified to 4-layer architecture
- Waived async-first for embedded system

### v1.0 (2026-04-10)
- Initial custom constitution based on SDD LITE
```

---

## Common Customizations

### 1. Embedded System (No Async)

**Baseline:** LITE or FULL  
**Changes:** Remove async-first principle

**Your Constitution:**

```markdown
## Core Principles

### Principle 1: Clean Separation
[Same as SDD]

### Principle 2: Single-Threaded Execution
All code runs on a single thread with sequential I/O.
Async/await is not used. Functions are synchronous.

### Principle 3: Clear Ownership
Each module owns its resources. No shared mutable state.

### Principle 4: ...
[Continue with SDD principles]
```

### 2. CLI Tool (No HTTP Layer)

**Baseline:** LITE  
**Changes:** Simplify from 8-layer to 5-layer (no HTTP adapters)

**Your layers:**
```
src/
├── domain/           # Business logic
├── services/         # Use cases
├── ports/            # Abstract interfaces
├── adapters/         # Filesystem, database, external APIs
└── cli/              # Click/Typer command definitions
```

### 3. Data Pipeline (Focus on Resilience)

**Baseline:** LITE  
**Changes:** Add failure recovery, add checkpointing

**Additional rules:**

```markdown
### Rule 4: Checkpointing
Every pipeline stage has a checkpoint.
If failure occurs, resume from last checkpoint (not restart).

### Rule 5: Dead Letter Queue
Failed items go to DLQ for manual review, not retry loops.
```

### 4. Microservice (Focus on Contract Testing)

**Baseline:** FULL  
**Changes:** Emphasize API contracts, add integration tests

**Additional rules:**

```markdown
### Rule X: API Contract Testing
Every endpoint has a contract test.
Consumer contracts defined in OpenAPI/Pact.
Producer validates against consumer contracts.
```

---

## Template: Custom Constitution

```markdown
# [Project Name] Constitution

**Baseline:** SDD [ULTRA-LITE|LITE|FULL]  
**Version:** 2.1-custom-v1.0  
**Date:** [Today]  

## Our Context

**Team:** [Size, skills]  
**Domain:** [What problem we solve]  
**Scale:** [Concurrent users/entities]  
**Constraints:** [Time, resources, infrastructure]

## Core Principles (5)

### Principle 1: [Name]
**SDD Baseline:** [How SDD does it]  
**Our Version:** [How we adapt it]  
**Why:** [Justification]  

[Repeat for 5 principles]

## Rules (3-5)

### Rule 1: ...
### Rule 2: ...
### Rule 3: ...

## Definition of Done

- [ ] Feature implemented
- [ ] Tests passing
- [ ] [Your #3]
- [ ] [Your #4]
- [ ] [Your #5]

## Deviations from SDD

[List what you changed and why]

## Validation

[How you verify this works]

## Team Sign-Off

- [Name]: [Date]
- [Name]: [Date]

## References

- [SDD Baseline Document]
- [Your project architecture]
- [Additional standards]
```

---

## When Customization Goes Wrong

### 🚨 Red Flags

If you find yourself doing these, **stop and reconsider:**

- ❌ "Skipping tests because they're inconvenient"
  → Use ULTRA-LITE instead, it has fewer requirements

- ❌ "Removing all validation"
  → Validation is core; find minimal-viable validation instead

- ❌ "No documentation of why we changed it"
  → Every customization must have written justification

- ❌ "Constitution is 50+ pages"
  → You've strayed from SDD; simplify or go back to standard

- ❌ "Keep changing the constitution every sprint"
  → Too unstable; lock it for 6 months minimum

### ✅ Signs of Good Customization

- ✅ Constitution is 2-4 pages
- ✅ Every change is documented with rationale
- ✅ Team agrees on it (sign-off document)
- ✅ Validation is automated (tests or linting)
- ✅ You can explain each customization in < 2 minutes

---

## Next Steps

1. **Choose your baseline** — ULTRA-LITE, LITE, or FULL?
2. **Answer the 5 constraint questions** (Step 2)
3. **Create your constitution** (Step 3)
4. **Get team buy-in** (sign-off)
5. **Add validation tests** (Step 4)
6. **Commit to git** with history
7. **Review quarterly** — Does it still fit?

---

## Getting Help

**Question:** "Can I customize [X]?"

| Component | Can Customize | Recommendation |
|-----------|---------------|-----------------|
| **Number of layers** | ✅ Yes | Document why (4, 6, or 8) |
| **Specific rules** | ✅ Yes | Keep immutable core (5 principles) |
| **Testing approach** | ✅ Yes | Maintain test pyramid concept |
| **Async requirement** | ✅ Yes | Only if truly not applicable |
| **Documentation** | ✅ Yes | Match your team's workflow |
| **Clean separation** | ❌ No | This is immutable core |
| **Explicit governance** | ❌ No | This is immutable core |
| **Test discipline** | ❌ No | This is immutable core |

**Need more help?**
- See [HONEST-CRITIQUE-CONSTITUTION.md](../HONEST-CRITIQUE-CONSTITUTION.md) for framework's honest limitations
- See [LITE-ADOPTION.md](./adoption/LITE-ADOPTION.md) for simplified baseline
- Ask in project's GitHub discussions

---

**Remember: Customization is not weakness. It's how frameworks grow.** 🚀

Your custom constitution = your team's agreed-upon standards.
That's more valuable than following a template perfectly.
