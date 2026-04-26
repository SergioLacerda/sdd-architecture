#!/usr/bin/env python3
"""
SDD Architecture - Layer 4 Governance Compliance Extension

This module extends agent_handshake.py Layer 4 with comprehensive governance
compliance checking against the 7 mandatory policies.

To integrate into agent_handshake.py:
1. Copy methods into the AgentHandshakeProtocol class
2. Update _layer_4_governance_health() to call these methods
3. Or import this module and use it alongside AHP

Mandatory Policies Validated:
1. governance-core.json exists
2. Valid JSON format
3. At least one active seedling
4. All authority roles assigned
5. Enforcement level set
6. PHASE 0 completed
7. Overall health check passes
"""

import hashlib
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class GovernanceComplianceValidator:
    """Validates governance against mandatory policies"""

    # The 7 mandatory policies
    MANDATORY_POLICIES = {
        'policy_1_file_exists': "governance-core.json must exist",
        'policy_2_valid_json': "governance-core.json must be valid JSON",
        'policy_3_active_seedlings': "At least one active seedling must be defined",
        'policy_4_authority_roles': "All authority roles must be assigned",
        'policy_5_enforcement_level': "Enforcement level must be set (strict/standard/permissive)",
        'policy_6_phase_0_complete': "PHASE 0 must be marked as completed",
        'policy_7_health_check': "Overall health check must pass"
    }

    def __init__(self, project_root: Path):
        self.project_root = project_root
        # Prioritize .ai/ (Wizard output) then .sdd/ (Standard client)
        self.governance_path = project_root / ".ai" / "governance-core.json"
        if not self.governance_path.exists():
            self.governance_path = project_root / ".sdd" / "governance-core.json"
        self.violations: List[str] = []
        self.warnings: List[str] = []
        self.config: Optional[Dict] = None

    def validate_all(self) -> Tuple[bool, Dict]:
        """
        Run all 7 mandatory policy checks
        
        Returns:
            (is_compliant: bool, results: dict with details)
        """
        results = {
            'policies_checked': 0,
            'policies_passed': 0,
            'policies_failed': 0,
            'violations': [],
            'warnings': [],
            'compliance_percentage': 0.0,
            'enforcement_level': None,
            'missing_fields': []
        }

        # Policy 1: File exists
        results['policies_checked'] += 1
        if self.governance_path.exists():
            results['policies_passed'] += 1
        else:
            results['policies_failed'] += 1
            results['violations'].append(f"Policy 1: governance-core.json not found at {self.governance_path}")
            return False, results

        # Optional Integrity Check (Fingerprint)
        if getattr(self, 'integrity_requested', False):
            ok, msg = self.check_integrity()
            if not ok:
                results['violations'].append(f"Policy 0: Integrity Failure - {msg}")
                results['policies_failed'] += 1
                return False, results

        # Load config (needed for remaining checks)
        try:
            with open(self.governance_path, 'r') as f:
                self.config = json.load(f)
        except json.JSONDecodeError as e:
            results['policies_checked'] += 1
            results['policies_failed'] += 1
            results['violations'].append(f"Policy 2: Invalid JSON - {str(e)}")
            return False, results

        # Policy 2: Valid JSON (already passed above)
        results['policies_checked'] += 1
        results['policies_passed'] += 1

        # Policy 3: Active seedlings
        results['policies_checked'] += 1
        active_seedlings = self.config.get('seedlings', {}).get('active', [])
        if active_seedlings:
            results['policies_passed'] += 1
        else:
            results['policies_failed'] += 1
            results['violations'].append("Policy 3: No active seedlings defined in seedlings.active")

        # Policy 4: Authority roles
        authority = self.config.get('authority', {})
        for role in ['architect', 'governance', 'operations']:
            results['policies_checked'] += 1
            if authority.get(role):
                results['policies_passed'] += 1
            else:
                results['policies_failed'] += 1
                results['violations'].append(f"Policy 4: '{role}' role not assigned in authority")
                results['missing_fields'].append(f"authority.{role}")

        # Policy 5: Enforcement level
        results['policies_checked'] += 1
        enforcement = self.config.get('policies', {}).get('enforcement')
        results['enforcement_level'] = enforcement
        if enforcement in ['strict', 'standard', 'permissive']:
            results['policies_passed'] += 1
        else:
            results['policies_failed'] += 1
            results['violations'].append(f"Policy 5: Invalid enforcement level '{enforcement}' (must be strict/standard/permissive)")

        # Policy 6: PHASE 0 completion
        results['policies_checked'] += 1
        completed = self.config.get('phases', {}).get('completed', [])
        if 0 in completed:
            results['policies_passed'] += 1
        else:
            results['policies_failed'] += 1
            results['violations'].append("Policy 6: PHASE 0 not marked as completed in phases.completed")

        # Calculate compliance percentage
        if results['policies_checked'] > 0:
            results['compliance_percentage'] = (results['policies_passed'] / results['policies_checked']) * 100

        # Policy 7: Overall health (depends on all others)
        results['policies_checked'] += 1
        if results['policies_failed'] == 0:  # All policies passed
            results['policies_passed'] += 1
            is_compliant = True
        else:
            results['policies_failed'] += 1
            is_compliant = False

        results['violations'] = list(set(results['violations']))  # Deduplicate
        return is_compliant, results

    def get_mandatory_fix_steps(self, results: Dict) -> List[str]:
        """
        Generate step-by-step fixes for policy violations
        
        Returns:
            List of fix commands/steps
        """
        fixes = []

        if not self.governance_path.exists():
            fixes.append("Step 1: Run wizard to create governance")
            fixes.append("  python EXECUTION/SCRIPTS/phase-0-agent-onboarding.py")
            return fixes

        if not self.config:
            fixes.append("Step 1: Fix JSON syntax in .sdd/governance-core.json")
            fixes.append("  python3 -m json.tool .sdd/governance-core.json")
            return fixes

        step = 1

        # Fix missing seedlings
        if "Policy 3" in " ".join(results['violations']):
            fixes.append(f"Step {step}: Add active seedling")
            fixes.append("  Edit .sdd/governance-core.json and set:")
            fixes.append('    "seedlings": { "active": ["my-domain"] }')
            step += 1

        # Fix missing authority roles
        missing_roles = [v.split("'")[1] for v in results['violations'] if 'role not assigned' in v]
        if missing_roles:
            fixes.append(f"Step {step}: Assign authority roles")
            for role in missing_roles:
                fixes.append(f"  Add {role} to authority in .sdd/governance-core.json:")
                fixes.append(f'    "{role}": ["user@example.com"]')
            step += 1

        # Fix enforcement level
        if "Policy 5" in " ".join(results['violations']):
            fixes.append(f"Step {step}: Set enforcement level")
            fixes.append("  Edit .sdd/governance-core.json and set:")
            fixes.append('    "enforcement": "standard"')
            step += 1

        # Fix PHASE 0
        if "Policy 6" in " ".join(results['violations']):
            fixes.append(f"Step {step}: Mark PHASE 0 as completed")
            fixes.append("  Edit .sdd/governance-core.json and set:")
            fixes.append('    "phases": { "completed": [0] }')
            step += 1

        fixes.append(f"\nStep {step}: Verify compliance")
        fixes.append("  python3 _core/governance_compliance.py --verify")

        return fixes

    def sign_governance(self) -> bool:
        """Calculates and writes the cryptographic fingerprint to seal the file"""
        try:
            if not self.governance_path.exists():
                return False

            with open(self.governance_path, 'r') as f:
                raw_data = json.load(f)

            if 'metadata' not in raw_data:
                raw_data['metadata'] = {}

            # Remove existing fingerprint to calculate fresh hash
            raw_data['metadata'].pop('fingerprint', None)
            actual = hashlib.sha256(json.dumps(raw_data, sort_keys=True).encode()).hexdigest()
            raw_data['metadata']['fingerprint'] = actual

            with open(self.governance_path, 'w') as f:
                json.dump(raw_data, f, indent=2)
            return True
        except Exception:
            return False

    def check_integrity(self) -> Tuple[bool, str]:
        """Verifies the cryptographic fingerprint of the governance file"""
        try:
            with open(self.governance_path, 'r') as f:
                raw_data = json.load(f)

            expected = raw_data.get('metadata', {}).get('fingerprint')
            if not expected:
                return True, "No fingerprint found (skipping)"

            # Calculate fingerprint excluding the fingerprint field itself
            content = raw_data.copy()
            content.get('metadata', {}).pop('fingerprint', None)
            actual = hashlib.sha256(json.dumps(content, sort_keys=True).encode()).hexdigest()

            return (True, "Valid") if actual == expected else (False, f"Mismatch: {actual}")
        except Exception as e:
            return False, str(e)

    def enforcement_check(self) -> Tuple[str, str]:
        """
        Check enforcement level and return enforcement behavior
        
        Returns:
            (level: str, behavior: str)
        """
        if not self.config:
            return 'none', 'No governance found'

        level = self.config.get('policies', {}).get('enforcement', 'unknown')

        behaviors = {
            'strict': 'Manual bypass disabled, violations block operations',
            'standard': 'Manual bypass allowed only for architect, some violations allowed',
            'permissive': 'Manual bypass allowed, warnings only',
            'unknown': 'Enforcement level not set'
        }

        return level, behaviors.get(level, 'Unknown enforcement level')

    def can_bypass_check(self, enforcement_level: str, user_role: Optional[str] = None) -> bool:
        """
        Determine if user can bypass governance checks
        
        Args:
            enforcement_level: The enforcement level from config
            user_role: Optional role (architect, governance, operations)
        
        Returns:
            True if bypass is allowed
        """
        if enforcement_level == 'strict':
            return False
        elif enforcement_level == 'standard':
            return user_role == 'architect'
        elif enforcement_level == 'permissive':
            return True
        else:
            return False

    def format_report(self, results: Dict, style: str = 'compact') -> str:
        """
        Format compliance check results for display
        
        Args:
            results: Results from validate_all()
            style: 'compact', 'verbose', 'json'
        
        Returns:
            Formatted report string
        """
        if style == 'json':
            return json.dumps(results, indent=2)

        compliance = results['compliance_percentage']
        passed = results['policies_passed']
        total = results['policies_checked']

        if compliance >= 100:
            emoji = '🟢'
            status = 'COMPLIANT'
        elif compliance >= 70:
            emoji = '🟡'
            status = 'PARTIAL'
        else:
            emoji = '❌'
            status = 'NON-COMPLIANT'

        if style == 'compact':
            return f"{emoji} Governance: {status} ({passed}/{total} policies passed, {compliance:.0f}%)"

        # Verbose style
        lines = [
            f"\n{'='*60}",
            "GOVERNANCE COMPLIANCE REPORT",
            f"{'='*60}",
            f"Status: {emoji} {status}",
            f"Compliance: {compliance:.1f}% ({passed}/{total})",
            f"Enforcement: {results['enforcement_level']}",
        ]

        if results['violations']:
            lines.append(f"\nVIOLATIONS ({len(results['violations'])}):")
            for v in results['violations']:
                lines.append(f"  ❌ {v}")

        if results['warnings']:
            lines.append(f"\nWARNINGS ({len(results['warnings'])}):")
            for w in results['warnings']:
                lines.append(f"  ⚠️  {w}")

        if results['missing_fields']:
            lines.append("\nMISSING FIELDS:")
            for f in results['missing_fields']:
                lines.append(f"  • {f}")

        lines.append(f"\n{'='*60}\n")
        return '\n'.join(lines)


# ========== INTEGRATION WITH AHP ==========

def extend_layer_4_governance_health(ahp_instance, compliance_validator: GovernanceComplianceValidator) -> Tuple[str, List]:
    """
    Enhanced Layer 4 that includes compliance checks
    
    To use in agent_handshake.py:
    
    Replace the _layer_4_governance_health method with:
    
    def _layer_4_governance_health(self):
        validator = GovernanceComplianceValidator(self.project_root)
        return extend_layer_4_governance_health(self, validator)
    """
    is_compliant, results = compliance_validator.validate_all()

    # Create ValidationResult objects for AHP
    validation_results = []

    # Add compliance check as main layer 4 result
    from dataclasses import dataclass

    @dataclass
    class ValidationResult:
        name: str
        passed: bool
        message: str
        layer: str

    compliance_msg = f"{results['compliance_percentage']:.0f}% compliant ({results['policies_passed']}/{results['policies_checked']} policies)"
    validation_results.append(ValidationResult(
        name="governance compliance",
        passed=is_compliant,
        message=compliance_msg,
        layer="GOVERNANCE_HEALTH"
    ))

    # Add enforcement level check
    enforcement = results['enforcement_level']
    validation_results.append(ValidationResult(
        name="enforcement level",
        passed=enforcement in ['strict', 'standard', 'permissive'],
        message=f"Set to: {enforcement}",
        layer="GOVERNANCE_HEALTH"
    ))

    # Determine state based on compliance
    if is_compliant:
        layer_state = "HEALTHY"
    elif results['compliance_percentage'] >= 50:
        layer_state = "DEGRADED"
    else:
        layer_state = "CRITICAL"

    return layer_state, validation_results


# ========== CLI INTERFACE ==========

if __name__ == "__main__":
    import argparse
    import sys

    parser = argparse.ArgumentParser(description="SDD Governance Compliance Validator")
    parser.add_argument('--verify', action='store_true', help="Verify governance compliance")
    parser.add_argument('--fix-steps', action='store_true', help="Show fix steps for violations")
    parser.add_argument('--enforcement-check', action='store_true', help="Check enforcement level")
    parser.add_argument('--format', choices=['compact', 'verbose', 'json'], default='verbose', help="Output format")
    parser.add_argument('--project-root', default='.', help="Project root directory")
    parser.add_argument('--check-integrity', action='store_true', help="Validate SHA-256 fingerprints")
    parser.add_argument('--sign', action='store_true', help="Generate and embed integrity fingerprint")

    args = parser.parse_args()

    project_root = Path(args.project_root)
    validator = GovernanceComplianceValidator(project_root)
    validator.integrity_requested = args.check_integrity

    if args.sign:
        success = validator.sign_governance()
        sys.exit(0 if success else 1)

    if args.verify or not args.fix_steps and not args.enforcement_check:
        is_compliant, results = validator.validate_all()
        print(validator.format_report(results, args.format))
        sys.exit(0 if is_compliant else 1)

    if args.fix_steps:
        is_compliant, results = validator.validate_all()
        if not is_compliant:
            fixes = validator.get_mandatory_fix_steps(results)
            print("\nFIX STEPS:")
            for fix in fixes:
                print(fix)
        else:
            print("✓ All governance policies are met")
        sys.exit(0 if is_compliant else 1)

    if args.enforcement_check:
        is_compliant, results = validator.validate_all()
        level, behavior = validator.enforcement_check()
        print(f"\nEnforcement Level: {level}")
        print(f"Behavior: {behavior}")
        sys.exit(0 if is_compliant else 1)
