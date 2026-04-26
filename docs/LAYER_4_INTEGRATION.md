# Agent Handshake Protocol - Layer 4 Extension

**Purpose**: Integrate GovernanceComplianceValidator into AHP for comprehensive governance health checks

**Status**: Ready for integration  
**File**: `_core/agent_handshake.py`

---

## Integration Steps

### Step 1: Add Import

At the top of `agent_handshake.py`, add:

```python
from governance_compliance import GovernanceComplianceValidator
```

### Step 2: Update _layer_4_governance_health Method

Find the existing `_layer_4_governance_health` method (around line 345) and replace it with:

```python
def _layer_4_governance_health(self) -> Tuple[str, List[ValidationResult]]:
    """
    Layer 4: GOVERNANCE HEALTH - Comprehensive compliance validation
    
    Enhanced to validate all 7 mandatory governance policies:
    1. governance-core.json exists
    2. Valid JSON format
    3. At least one active seedling
    4. All authority roles assigned
    5. Enforcement level set
    6. PHASE 0 completed
    7. Overall health passes
    
    Returns: (state, results)
    """
    results = []
    
    # Initialize compliance validator
    validator = GovernanceComplianceValidator(self.project_root)
    is_compliant, compliance_results = validator.validate_all()
    
    # Create validation result for compliance check
    compliance_percentage = compliance_results['compliance_percentage']
    passed = compliance_results['policies_passed']
    total = compliance_results['policies_checked']
    
    results.append(ValidationResult(
        name="governance compliance",
        passed=is_compliant,
        message=f"{compliance_percentage:.0f}% compliant ({passed}/{total} policies)",
        layer="GOVERNANCE_HEALTH"
    ))
    
    # Check enforcement level
    enforcement = compliance_results['enforcement_level']
    enforcement_valid = enforcement in ['strict', 'standard', 'permissive']
    
    results.append(ValidationResult(
        name="enforcement level",
        passed=enforcement_valid,
        message=f"Set to: {enforcement}" if enforcement_valid else "Not configured",
        layer="GOVERNANCE_HEALTH"
    ))
    
    # Check for violations and include in actions
    if compliance_results['violations']:
        self.actions.extend([
            f"Fix governance: {v}" 
            for v in compliance_results['violations'][:3]  # Top 3 violations
        ])
    
    # Determine layer state based on compliance
    if is_compliant:
        layer_state = "HEALTHY"
    elif compliance_percentage >= 70:
        layer_state = "PARTIAL"  # Most policies met
    elif compliance_percentage >= 30:
        layer_state = "DEGRADED"  # Some policies met
    else:
        layer_state = "CRITICAL"  # Few policies met
    
    return layer_state, results
```

### Step 3: Add Enforcement Check Method

Add this method to the AgentHandshakeProtocol class:

```python
def _check_enforcement_allows_bypass(self, enforcement_level: str = None) -> bool:
    """
    Check if current enforcement level allows manual bypass
    
    Used to determine if --force flag should work
    """
    if enforcement_level is None:
        validator = GovernanceComplianceValidator(self.project_root)
        _, results = validator.validate_all()
        enforcement_level = results['enforcement_level']
    
    return enforcement_level == 'permissive'
```

### Step 4: Update Semantic Trigger

Update the `should_run_handshake` method to also trigger on governance keywords:

```python
def should_run_handshake(self, user_input: str) -> bool:
    """
    Determine if handshake should run based on semantic analysis
    
    Enhanced: Also triggers on governance-related queries
    """
    # Original implementation
    casual_keywords = [
        'hi', 'hello', 'thanks', 'okay', 'sure',
        'question', 'ask', 'what', 'how', 'when',
        'where', 'why', 'who', 'which', 'whose'
    ]
    
    technical_keywords = [
        'architecture', 'phase', 'domain', 'seedling',
        'governance', 'policy', 'compliance', 'enforcement',
        'authority', 'validation', 'health', 'handshake',
        'deploy', 'schema', 'design', 'pattern', 'implement'
    ]
    
    input_lower = user_input.lower()
    
    # Check for technical context
    has_technical = any(keyword in input_lower for keyword in technical_keywords)
    
    # Check for casual-only context
    words = input_lower.split()
    all_casual = all(word in casual_keywords for word in words if len(word) > 2)
    
    if all_casual and not has_technical:
        return False  # Purely casual, skip handshake
    
    # Check enforcement level
    validator = GovernanceComplianceValidator(self.project_root)
    _, results = validator.validate_all()
    enforcement = results['enforcement_level']
    
    if enforcement == 'strict':
        # Always run handshake for strict mode
        return True
    
    # Run for technical topics
    return has_technical
```

### Step 5: Add Verbose Compliance Report

Add this method for detailed compliance output:

```python
def _format_compliance_report(self, validation_results: List[ValidationResult]) -> str:
    """Format compliance checks for verbose output"""
    if not validation_results:
        return ""
    
    lines = ["\nGovernance Health Checks:"]
    for result in validation_results:
        emoji = "✓" if result.passed else "✗"
        lines.append(f"  {emoji} {result.name}: {result.message}")
    
    return "\n".join(lines)
```

---

## Testing the Integration

After making changes, test Layer 4:

```bash
# Test 1: Check if layer runs without errors
python _core/agent_handshake.py --mode=verbose

# Expected output includes governance compliance checks

# Test 2: Verify compliance validator is called
python3 << 'EOF'
import sys
sys.path.insert(0, '_core')
from agent_handshake import AgentHandshakeProtocol

ahp = AgentHandshakeProtocol()
result = ahp.validate(output_mode='verbose')
print(f"State: {result.state}")
print(f"Governance health checks completed: {'governance compliance' in str(result.checks)}")
EOF

# Test 3: Verify enforcement blocking
# Create a scenario where enforcement is 'strict' and test --force flag
python _core/agent_handshake.py --force --skip-checks --mode=compact
```

---

## Integration Verification

After integration, verify these work:

### 1. Layer 4 Includes Compliance
```bash
python _core/agent_handshake.py --mode=verbose
```
Output should show governance compliance percentage

### 2. Enforcement Level Detected
```bash
python3 << 'EOF'
import sys
sys.path.insert(0, '_core')
from governance_compliance import GovernanceComplianceValidator
from pathlib import Path

validator = GovernanceComplianceValidator(Path('.'))
_, results = validator.validate_all()
print(f"Enforcement: {results['enforcement_level']}")
print(f"Compliance: {results['compliance_percentage']:.0f}%")
EOF
```

### 3. Bypass Check Works
```bash
python3 << 'EOF'
import sys
sys.path.insert(0, '_core')
from agent_handshake import AgentHandshakeProtocol

ahp = AgentHandshakeProtocol()
can_bypass = ahp._check_enforcement_allows_bypass()
print(f"Can bypass checks: {can_bypass}")
EOF
```

---

## After Integration

Once integrated, these features become available:

### For Users
- Health check shows governance compliance percentage
- AHP blocks operations if enforcement = strict
- Semantic trigger activates on governance keywords
- Detailed compliance report in verbose mode

### For AI Agents
- Can detect if governance is compliant
- Can show fix steps if violations exist
- Can enforce bypass restrictions
- Can adapt responses based on enforcement level

### For Operations
- CI/CD pipelines can enforce compliance
- Pull requests can require governance checks
- Audit logs track compliance status
- Reports available in multiple formats

---

## Rollback (If Needed)

If integration causes issues:

```bash
# Revert to original _layer_4_governance_health:
git diff HEAD~ _core/agent_handshake.py | grep -A50 "_layer_4_governance_health"

# Then manually edit or:
git checkout HEAD -- _core/agent_handshake.py
```

---

## Next Steps

1. ✅ Make integration changes above
2. ✅ Run verification tests
3. ⏳ Add governance questions to quiz_executor.py
4. ⏳ Test end-to-end: wizard → AHP Layer 4 → enforcement
5. ⏳ Create Phase 5 documentation

---

**Integration Ready**: Yes  
**Estimated Time**: 10-15 minutes  
**Risk Level**: Low (extends existing method, backward compatible)  
**Testing Required**: Yes (see Testing section)
