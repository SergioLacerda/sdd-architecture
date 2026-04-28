# End-to-End Phase 4 Testing Guide

**Purpose**: Validate complete governance system integration from sdd_wizard to enforcement

**Scope**: Wizard → AHP Layer 4 → Enforcement → Quiz → Health States  
**Time**: ~30 minutes  
**Complexity**: Comprehensive  

---

## Test Environment Setup

### Prerequisites
- [ ] All Phase 4 files created (governance seedlings, compliance validator)
- [ ] Agent Handshake Protocol Layer 4 extended with GovernanceComplianceValidator
- [ ] Governance quiz questions added (4 new questions)
- [ ] Project has git initialized
- [ ] Python 3.8+ available

### Prepare Test Environment
```bash
# 1. Create test directory
mkdir -p /tmp/sdd-test && cd /tmp/sdd-test

# 2. Initialize git
git init
git config user.email "test@example.com"
git config user.name "Test User"

# 3. Copy SDD codebase
cp -r /home/sergio/dev/sdd-architecture/* .

# 4. Verify files exist
ls -la packages/governance_compliance.py
ls -la EXECUTION/quiz_questions.json
ls -la packages/agent_handshake.py
```

---

## Test 1: Governance Compliance Validator

**Goal**: Verify GovernanceComplianceValidator works correctly

```bash
# Test 1.1: No governance (NOT_CONNECTED state)
cd /tmp/sdd-test
rm -rf .sdd  # Remove if exists
python3 packages/governance_compliance.py --verify
# Expected: compliance_percentage = 0%, violations list all 7 policies
```

Expected output:
```
❌ Governance: NON-COMPLIANT (0/7 policies passed, 0%)
Violations:
  ❌ Policy 1: governance-core.json not found at .sdd/governance-core.json
  ❌ Policy 2: Invalid JSON - No file found
  ...
```

**Test 1.2**: Check fix steps
```bash
python3 packages/governance_compliance.py --fix-steps
# Expected: Shows "Run wizard" as first step
```

**Test 1.3**: Enforcement check
```bash
python3 packages/governance_compliance.py --enforcement-check
# Expected: "Enforcement Level: none" or "No governance found"
```

✅ **Pass Criteria**: All 3 commands work without errors

---

## Test 2: Wizard Integration

**Goal**: Verify wizard creates valid governance structure

```bash
# Test 2.1: Run wizard (automated mode for testing)
python3 EXECUTION/SCRIPTS/phase-0-agent-onboarding.py --test-mode
# Or interactive:
python3 EXECUTION/SCRIPTS/phase-0-agent-onboarding.py

# Provide answers:
# Domain: test-domain
# Language: Python
# Enforcement: standard
# Architect: alice@test.com
# Governance: bob@test.com
# Operations: charlie@test.com
# Seedling: yes
```

**Test 2.2**: Verify files created
```bash
ls -la .sdd/governance-core.json
ls -la .sdd/seedlings/test-domain/
cat .sdd/governance-core.json | python3 -m json.tool
# Expected: Valid JSON with all required fields
```

**Test 2.3**: Run compliance check again
```bash
python3 packages/governance_compliance.py --verify
# Expected: 100% compliance (7/7 policies)
# Enforcement: standard
```

✅ **Pass Criteria**: Compliance shows 100%, enforcement set to standard

---

## Test 3: Agent Handshake Protocol Integration

**Goal**: Verify AHP Layer 4 includes governance compliance

### Prerequisite: Update agent_handshake.py
If not already done:
```bash
# Make backup
cp packages/agent_handshake.py packages/agent_handshake.py.bak

# Apply Layer 4 extension from LAYER_4_INTEGRATION.md
# (Insert the updated _layer_4_governance_health method)
```

### Tests
```bash
# Test 3.1: Run AHP in silent mode
python3 packages/agent_handshake.py --mode=silent
# Expected: Shows state (🟢 HEALTHY or similar)
```

**Test 3.2**: Run AHP in compact mode
```bash
python3 packages/agent_handshake.py --mode=compact
# Expected: Shows governance compliance percentage
# Example:
# 🧠 SDD STATUS
# State: 🟢 HEALTHY
# Confidence: 85%
# Checks: ... governance compliance: 100% (7/7 policies) ...
```

**Test 3.3**: Run AHP in verbose mode
```bash
python3 packages/agent_handshake.py --mode=verbose
# Expected: Detailed report including:
#   - governance compliance: 100% (7/7 policies) ✓
#   - enforcement level: Set to: standard ✓
#   - Authority checks ✓
#   - Phase progression ✓
```

✅ **Pass Criteria**: AHP reports governance compliance checks, state is HEALTHY

---

## Test 4: Enforcement Behavior

**Goal**: Verify enforcement modes work as documented

### Test 4.1: STRICT mode blocking
```bash
# Edit governance to set strict enforcement
cat .sdd/governance-core.json | python3 -c "
import json, sys
data = json.load(sys.stdin)
data['policies']['enforcement'] = 'strict'
print(json.dumps(data, indent=2))
" > .sdd/governance-core.json.tmp
mv .sdd/governance-core.json.tmp .sdd/governance-core.json

# Try to bypass
python3 packages/agent_handshake.py --force --skip-checks --mode=compact
# Expected: ❌ Manual bypass is disabled
```

### Test 4.2: STANDARD mode allowing architect bypass
```bash
# Update to standard
cat .sdd/governance-core.json | python3 -c "
import json, sys
data = json.load(sys.stdin)
data['policies']['enforcement'] = 'standard'
print(json.dumps(data, indent=2))
" > .sdd/governance-core.json.tmp
mv .sdd/governance-core.json.tmp .sdd/governance-core.json

# Should allow (with proper role)
python3 packages/agent_handshake.py --mode=compact
# Expected: 🟢 HEALTHY (bypass not actively blocking in normal flow)
```

### Test 4.3: PERMISSIVE mode allowing all bypasses
```bash
# Update to permissive
cat .sdd/governance-core.json | python3 -c "
import json, sys
data = json.load(sys.stdin)
data['policies']['enforcement'] = 'permissive'
print(json.dumps(data, indent=2))
" > .sdd/governance-core.json.tmp
mv .sdd/governance-core.json.tmp .sdd/governance-core.json

# Should allow bypasses
python3 packages/agent_handshake.py --mode=compact
# Expected: 🟢 HEALTHY (minimal enforcement)
```

✅ **Pass Criteria**: All 3 enforcement modes work as documented

---

## Test 5: Quiz Integration

**Goal**: Verify governance quiz questions work

### Prerequisite: Add governance questions
If not already done, add the 4 governance questions from GOVERNANCE_QUIZ_EXTENSION.md

### Tests
```bash
# Test 5.1: List governance topic
python3 EXECUTION/quiz_executor.py --list-topics | grep governance
# Expected: Shows "governance" with 4 questions

# Test 5.2: Run governance quiz silently
python3 EXECUTION/quiz_executor.py --topic=governance --mode=silent
# Expected: Shows final score

# Test 5.3: Run with specific difficulty
python3 EXECUTION/quiz_executor.py --topic=governance --difficulty=easy --mode=silent
# Expected: Only easy questions shown

# Test 5.4: Check exit code (pass = 0, fail = 1)
python3 EXECUTION/quiz_executor.py --topic=governance --mode=silent
echo "Exit code: $?"
# Expected: 0 if score >= 70%, 1 if < 70%
```

✅ **Pass Criteria**: Governance quiz runs, filters work, exit codes correct

---

## Test 6: Semantic Triggering

**Goal**: Verify AHP semantic trigger activates on governance keywords

```bash
# Test 6.1: Create test script that checks should_run_handshake
python3 << 'EOF'
import sys
sys.path.insert(0, 'packages')
from agent_handshake import AgentHandshakeProtocol

ahp = AgentHandshakeProtocol()

# Test casual input
casual = "Hi, how are you?"
print(f"Casual input triggers handshake: {ahp.should_run_handshake(casual)}")
# Expected: False

# Test technical input
technical = "How should I implement governance policies?"
print(f"Technical input triggers handshake: {ahp.should_run_handshake(technical)}")
# Expected: True

# Test governance keyword
governance = "Tell me about seedlings"
print(f"Governance keyword triggers handshake: {ahp.should_run_handshake(governance)}")
# Expected: True (if seedlings in technical keywords)

# Test architecture keyword
arch = "What's the architecture pattern?"
print(f"Architecture keyword triggers handshake: {ahp.should_run_handshake(arch)}")
# Expected: True
EOF
```

✅ **Pass Criteria**: Technical and governance keywords trigger, casual doesn't

---

## Test 7: State Machine Transitions

**Goal**: Verify health states transition correctly based on governance state

```bash
# Test 7.1: Start with no governance (NOT_CONNECTED → PARTIAL → HEALTHY)
rm -rf .sdd

# Step 1: NOT_CONNECTED (no governance)
python3 packages/agent_handshake.py --mode=compact
# Expected state: ❌ NOT_CONNECTED or similar

# Step 2: Run wizard (create governance)
python3 EXECUTION/SCRIPTS/phase-0-agent-onboarding.py
# (Use test answers from earlier)

# Step 3: PARTIAL (governance exists but incomplete)
# Manually remove one required field:
python3 << 'EOF'
import json
data = json.load(open('.sdd/governance-core.json'))
del data['authority']['architect']  # Remove architect
with open('.sdd/governance-core.json', 'w') as f:
    json.dump(data, f)
EOF
python3 packages/agent_handshake.py --mode=compact
# Expected state: 🟡 PARTIAL or MISCONFIGURED

# Step 4: Fix and return to HEALTHY
python3 << 'EOF'
import json
data = json.load(open('.sdd/governance-core.json'))
data['authority']['architect'] = ['alice@test.com']
with open('.sdd/governance-core.json', 'w') as f:
    json.dump(data, f)
EOF
python3 packages/agent_handshake.py --mode=compact
# Expected state: 🟢 HEALTHY
```

✅ **Pass Criteria**: States transition as documented, actions update appropriately

---

## Test 8: JSON Export

**Goal**: Verify AHP exports compliance data as JSON

```bash
# Test 8.1: Export mode
python3 packages/agent_handshake.py --mode=silent --format=json > /tmp/ahp-result.json

# Verify JSON valid
python3 -m json.tool /tmp/ahp-result.json > /dev/null && echo "✓ Valid JSON"

# Check governance fields
python3 << 'EOF'
import json
result = json.load(open('/tmp/ahp-result.json'))
assert 'state' in result, "Missing state"
assert 'confidence' in result, "Missing confidence"
assert 'checks' in result, "Missing checks"
print("✓ All required fields present")
EOF
```

✅ **Pass Criteria**: JSON export works, contains governance data

---

## Test 9: End-to-End User Journey

**Goal**: Simulate complete user journey from zero to HEALTHY

```bash
# 1. Fresh project with no governance
rm -rf .sdd
echo "Step 1: Initial state (no governance)"
python3 packages/agent_handshake.py --mode=compact

# 2. Run wizard
echo "Step 2: Running wizard..."
# Would be interactive; skip for automated testing
python3 EXECUTION/SCRIPTS/phase-0-agent-onboarding.py --test-mode

# 3. Verify governance created
echo "Step 3: Governance created"
python3 packages/governance_compliance.py --verify

# 4. Check AHP state
echo "Step 4: AHP validation"
python3 packages/agent_handshake.py --mode=compact

# 5. Run quiz
echo "Step 5: Governance quiz"
python3 EXECUTION/quiz_executor.py --topic=governance --mode=silent

# 6. Final health check
echo "Step 6: Final health check"
python3 packages/agent_handshake.py --mode=verbose

# Expected flow:
# ❌ NOT_CONNECTED → 🟡 PARTIAL → 🟢 HEALTHY
```

✅ **Pass Criteria**: Full journey completes, state progresses correctly

---

## Test 10: Error Handling

**Goal**: Verify graceful error handling

```bash
# Test 10.1: Corrupted JSON
echo '{ "invalid": json }' > .sdd/governance-core.json
python3 packages/governance_compliance.py --verify
# Expected: Shows JSON error, not a crash

# Test 10.2: Missing fields in governance-core.json
echo '{}' > .sdd/governance-core.json
python3 packages/governance_compliance.py --verify
# Expected: Shows missing field violations

# Test 10.3: Non-existent project root
python3 packages/governance_compliance.py --project-root=/tmp/nonexistent --verify
# Expected: Handles gracefully or shows clear error

# Test 10.4: Permission denied
chmod 000 .sdd/governance-core.json
python3 packages/governance_compliance.py --verify
chmod 644 .sdd/governance-core.json
# Expected: Handles permission error gracefully
```

✅ **Pass Criteria**: All errors handled with clear messages, no crashes

---

## Test Summary

| Test | Status | Notes |
|------|--------|-------|
| 1: Compliance Validator | ⏳ Run | Verify validator works |
| 2: Wizard Integration | ⏳ Run | Check governance created |
| 3: AHP Layer 4 | ⏳ Run | Verify compliance checks included |
| 4: Enforcement Modes | ⏳ Run | Test all 3 enforcement levels |
| 5: Quiz Integration | ⏳ Run | Test governance questions |
| 6: Semantic Triggering | ⏳ Run | Test AHP activation |
| 7: State Machine | ⏳ Run | Test health state transitions |
| 8: JSON Export | ⏳ Run | Test data export format |
| 9: User Journey | ⏳ Run | End-to-end flow |
| 10: Error Handling | ⏳ Run | Test graceful errors |

---

## Success Criteria

✅ **All Tests Pass** = Phase 4 Complete

Minimum requirements:
- [ ] Compliance validator works (Test 1)
- [ ] Wizard creates valid governance (Test 2)
- [ ] AHP includes governance checks (Test 3)
- [ ] Enforcement modes work as documented (Test 4)
- [ ] Quiz questions functional (Test 5)
- [ ] State machine transitions correctly (Test 7)
- [ ] End-to-end journey works (Test 9)

---

## Debugging Tips

### If compliance validator fails
```bash
# Check Python syntax
python3 packages/governance_compliance.py --help

# Run with verbose error
python3 -u packages/governance_compliance.py --verify 2>&1
```

### If AHP Layer 4 fails
```bash
# Check import
python3 -c "from governance_compliance import GovernanceComplianceValidator; print('✓ Import OK')"

# Run individual layer
python3 << 'EOF'
import sys
sys.path.insert(0, 'packages')
from agent_handshake import AgentHandshakeProtocol
ahp = AgentHandshakeProtocol()
state, results = ahp._layer_4_governance_health()
print(f"Layer 4 state: {state}")
for r in results:
    print(f"  {r.name}: {r.message}")
EOF
```

### If quiz fails
```bash
# Check quiz file syntax
python3 -m json.tool EXECUTION/quiz_questions.json

# List all topics
python3 EXECUTION/quiz_executor.py --list-topics
```

---

**Testing Status**: Ready  
**Estimated Duration**: 30-45 minutes  
**Difficulty**: Advanced  
**Cleanup**: `rm -rf /tmp/sdd-test` after testing
