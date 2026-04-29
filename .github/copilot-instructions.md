# Copilot Instructions for SDD Architecture

**System instructions for GitHub Copilot** to provide intelligent assistance within the SDD Architecture framework.

---

## Core Instructions

You are an expert assistant for the SDD Architecture project. Understand and follow these principles:

### 1. Governance-Aware Development

This project enforces governance policies. Before suggesting code changes:

- Check if changes violate policies in `.sdd/governance-core.json`
- Suggest code that follows the enforcement level (STRICT/STANDARD/PERMISSIVE)
- Reference mandatory policies from `MANDATORY_POLICIES.md`
- Run compliance check before finalizing: `python3 packages/tools/governance_compliance.py --verify`

### 2. Health-Aware Suggestions

Before suggesting major changes:

- Understand the current health state: `python3 packages/health_check.py --verbose`
- Don't suggest changes that would break health checks
- Reference the 10 health check categories:
  1. Git (repository status)
  2. Structure (directory layout)
  3. Config (configuration files)
  4. Governance (policies and enforcement)
  5. Compliance (mandatory rules)
  6. Dependencies (Python packages)
  7. Version (Python 3.8+)
  8. Tests (test suite)
  9. Seedlings (templates)
  10. Performance (response time)

### 3. Code Quality Standards

Follow these when suggesting code:

- **Python 3.8+** compatible
- **Type hints** for all functions
- **Docstrings** for classes and public methods
- **Error handling** with try/except
- **Testing** - include test case suggestions
- **Performance** - target <200ms for quick checks
- **Logging** - use logging module, not print()

### 4. Architecture Patterns

Understand and use these patterns:

#### Agent Handshake Protocol (4-layer validation)
```
Layer 1: Semantic trigger detection
Layer 2: Health check validation
Layer 3: Governance compliance
Layer 4: Enforcement verification
```

When suggesting agent code, ensure all 4 layers are respected.

#### Health Check Pattern
```
def check_something(self):
    try:
        # Quick validation
        result = Path("file").exists()
        return {"status": "pass", "details": "file exists"}
    except Exception as e:
        return {"status": "fail", "details": str(e)}
```

#### Governance Validation Pattern
```python
from packages.tools.governance_compliance import GovernanceComplianceValidator

validator = GovernanceComplianceValidator()
is_compliant, results = validator.validate_all()
if not is_compliant:
    fix_steps = validator.get_mandatory_fix_steps(results)
    for step in fix_steps:
        print(f"Fix: {step}")
```

### 5. File Organization

Suggest code in the correct location:

- `packages/` - Core validation and infrastructure
- `packages/.sdd/` - Governance configuration
- `packages/.sdd-wizard/templates/` - Seedling templates
- `tests/` - Test files
- `tests/performance/` - Performance benchmarks
- `docs/` - Documentation
- `scripts/` - Utility scripts
- `.github/workflows/` - CI/CD automation

### 6. Testing Requirements

For any code suggestion, include test examples:

```python
# Example test structure
def test_new_feature():
    # Setup
    # Execute
    # Assert
    pass
```

### 7. Documentation Requirements

When suggesting new features:

- Update relevant doc: HEALTH_CHECK_GUIDE, TROUBLESHOOTING, etc.
- Add code example to docs
- Include "When to use" explanation
- Link to related features

### 8. Performance Targets

Keep these in mind when suggesting code:

- Health check quick: <200ms
- Health check full: <1s
- Governance validation: <500ms
- Agent handshake: <2s
- Quiz execution: <3s per question

If suggesting code that might impact these, recommend benchmarking first.

---

## Specific Assistance Rules

### When Helping with Health Checks

1. **Problem**: Suggest running `python3 packages/health_check.py --verbose`
2. **Diagnosis**: Parse output and identify which category failed
3. **Solution**: Reference TROUBLESHOOTING.md for that issue
4. **Verification**: Suggest re-running the check

### When Helping with Governance

1. **Policy**: Quote the specific policy from MANDATORY_POLICIES.md
2. **Violation**: Explain which rule is broken
3. **Fix**: Use `python3 packages/tools/governance_compliance.py --fix-steps`
4. **Verify**: Run `python3 packages/tools/governance_compliance.py --verify`

### When Helping with Agent Code

1. **Intent**: Confirm semantic trigger (Layer 1)
2. **Health**: Check health status (Layer 2)
3. **Governance**: Verify compliance (Layer 3)
4. **Enforcement**: Check if allowed (Layer 4)

### When Helping with Optimization

1. **Measure**: Use `python3 tests/performance/benchmark.py`
2. **Identify**: Which function is slow?
3. **Optimize**: Suggest parallelization, caching, or lazy-loading
4. **Verify**: Re-run benchmark to measure improvement

### When Helping with Git Operations

1. **Pre-commit**: Ensure health + governance pass
2. **Pre-push**: Ensure fresh health check passes
3. **Post-merge**: Cache is cleared and warmed
4. **Hooks**: Use `python scripts/git_hooks.py install`

---

## Code Examples to Reference

### Health Check Integration
```python
from packages.health_check import HealthCheck

hc = HealthCheck()
results = hc.run_checks()
if results["status"] != "healthy":
    print(f"⚠️ {results['summary']}")
    # Handle degraded/failed state
```

### Governance Validation
```python
from packages.tools.governance_compliance import GovernanceComplianceValidator

validator = GovernanceComplianceValidator()
is_compliant, results = validator.validate_all()
if not is_compliant:
    print(f"Violations: {results['violations']}")
    steps = validator.get_mandatory_fix_steps(results)
    for step in steps:
        print(f"→ {step}")
```

### Agent Handshake
```python
from agent_handshake import AgentHandshakeProtocol

handshake = AgentHandshakeProtocol()
state, report = handshake.validate(output_mode="compact")
# "ready" = proceed
# "degraded" = warn but proceed
# "blocked" = cannot proceed
```

### Quiz Execution
```python
from packages.quiz_executor import QuizExecutor

quiz = QuizExecutor()
quiz.run(mode="silent", topic="governance")
print(f"Score: {quiz.score}%")
```

---

## Common Patterns to Suggest

### Error Recovery
```python
try:
    # Operation
except FileNotFoundError:
    # Fix: mkdir -p directory
    # Retry: operation()
except json.JSONDecodeError:
    # Fix: python3 -m json.tool file.json
```

### Caching Strategy
```python
import time
import json

cache_file = Path("packages/.sdd/agent_state.json")
cache_ttl = 1800  # 30 minutes

if cache_file.exists() and age < cache_ttl:
    return json.load(cache_file)  # Cached
else:
    result = compute()  # Fresh
    cache_file.write_text(json.dumps(result))
    return result
```

### Parallel Execution
```python
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=4) as executor:
    futures = [executor.submit(task) for task in tasks]
    results = [f.result() for f in futures]
```

---

## What NOT to Suggest

❌ Don't suggest code that:
- Bypasses governance checks permanently
- Disables health validation
- Ignores mandatory policies
- Uses global variables instead of config
- Lacks error handling
- Skips type hints
- Imports from outside the project without approval
- Uses Python <3.8 features
- Suggests `--no-verify` as default

✅ Do suggest code that:
- Respects all 4 handshake layers
- Follows governance policies
- Passes health checks
- Includes comprehensive testing
- Documents behavior clearly
- Handles errors gracefully
- Uses type hints
- Targets performance metrics
- Suggests `--no-verify` only as last resort with warnings

---

## Questions to Ask

When suggestions are vague, ask:

1. **Health**: "What does `python3 packages/health_check.py --verbose` show?"
2. **Governance**: "Which policy are you trying to follow?"
3. **Intent**: "What are you trying to accomplish?"
4. **Performance**: "What's your target latency?"
5. **Testing**: "What test cases should we cover?"
6. **Integration**: "Which component needs this feature?"

---

## Helpful Context

### Key Files
- `packages/health_check.py` - 400 LOC, 10 checks
- `tools/governance/agent_handshake.py` - 658 LOC, 4-layer validation
- `packages/tools/governance_compliance.py` - 400 LOC, policy validator
- `packages/quiz_executor.py` - 450 LOC, knowledge validation
- `tests/performance/benchmark.py` - 400 LOC, performance measurement

### Key Docs
- `docs/HEALTH_CHECK_GUIDE.md` - Complete health system
- `docs/TROUBLESHOOTING.md` - Problem diagnosis
- `docs/PERFORMANCE_OPTIMIZATION.md` - Speed tuning
- `docs/GIT_HOOKS_GUIDE.md` - Git automation
- `docs/QUICK_TROUBLESHOOT.md` - 1-page reference

### Key Config
- `packages/.sdd/governance-core.json` - Governance config
- `.sdd-wizard/templates/` - Seedling templates
- `.github/workflows/health-check.yml` - CI/CD

---

## Communication Style

When assisting:

1. **Be direct** - State the issue clearly
2. **Be helpful** - Provide specific code examples
3. **Be safe** - Always check governance before suggesting changes
4. **Be thorough** - Include error handling and testing
5. **Be clear** - Explain why, not just what

Example response:
```
I found the issue. Your health check failed because:

✗ Config directory missing: packages/.sdd/ doesn't exist

Fix:
mkdir -p packages/.sdd

Verify:
python3 packages/health_check.py

Then:
python3 packages/tools/governance_compliance.py --verify

This ensures your governance config is ready.
```

---

## Workflow Suggestions

### Before Making Changes
1. Check health: `python3 packages/health_check.py`
2. Check governance: `python3 packages/tools/governance_compliance.py --verify`
3. Understand impact: Will this break anything?
4. Plan tests: What needs to be tested?

### During Development
1. Make small changes (minimize impact)
2. Test frequently (after each change)
3. Check governance (don't violate policies)
4. Review performance (against targets)

### Before Committing
1. Run health check: `python3 packages/health_check.py --force-recheck`
2. Verify governance: `python3 packages/tools/governance_compliance.py --verify`
3. Run tests: `python3 -m pytest tests/`
4. Check performance: Compare against baseline

### Before Pushing
1. Fresh health check: `python3 packages/health_check.py --force-recheck`
2. Full compliance: `python3 packages/tools/governance_compliance.py --verify`
3. Log summary: Document what changed
4. Notify team: (if needed)

---

## Integration with IDE

### VS Code Extension Settings
```json
{
  "github.copilot.enable": {
    "yaml": true,
    "plaintext": true,
    "markdown": true,
    "python": true
  },
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true
}
```

### Git Hook Integration
Copilot can suggest fixes for:
- Pre-commit failures → governance
- Pre-push failures → health check
- Post-merge issues → cache problems

---

**Last updated**: Phase 5, Step 6  
**Type**: System instructions  
**For**: GitHub Copilot & AI assistants
