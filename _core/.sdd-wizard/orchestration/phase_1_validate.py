"""
SDD v3.0 Wizard - Phase 1: Validate SOURCE (.sdd-core/)

Ensures source DSL files are syntactically correct and reference-valid
"""

from pathlib import Path
from typing import Dict, Tuple
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.validator import SourceValidator


def phase_1_validate_source(repo_root: Path = Path.cwd()) -> Tuple[bool, Dict]:
    """
    Phase 1: Validate SOURCE layer (.sdd-core/)
    
    Input: .sdd-core/mandate.spec and .sdd-core/guidelines.dsl
    
    Checks:
    - Files exist
    - DSL syntax valid (balanced braces, etc.)
    - Mandate/guideline IDs valid (M001, M002, etc.)
    - No duplicate IDs
    - No empty definitions
    
    Output: Validation report
    
    Returns:
        (success: bool, validation_report: dict)
    """
    sdd_core = repo_root / ".sdd-core"
    report = {
        'phase': 'PHASE_1_VALIDATE_SOURCE',
        'status': 'PENDING',
        'checks': {
            'mandate_spec_exists': False,
            'guidelines_dsl_exists': False,
            'mandate_spec_valid': False,
            'guidelines_dsl_valid': False,
        },
        'data': {},
        'errors': [],
        'warnings': [],
    }
    
    # Check files exist
    mandate_file = sdd_core / "mandate.spec"
    guidelines_file = sdd_core / "guidelines.dsl"
    
    if not mandate_file.exists():
        report['errors'].append(f"mandate.spec not found at {mandate_file}")
        report['status'] = 'FAILED'
        return (False, report)
    report['checks']['mandate_spec_exists'] = True
    
    if not guidelines_file.exists():
        report['errors'].append(f"guidelines.dsl not found at {guidelines_file}")
        report['status'] = 'FAILED'
        return (False, report)
    report['checks']['guidelines_dsl_exists'] = True
    
    # Load files
    try:
        mandate_text = mandate_file.read_text(encoding='utf-8')
        guidelines_text = guidelines_file.read_text(encoding='utf-8')
    except Exception as e:
        report['errors'].append(f"Error reading files: {e}")
        report['status'] = 'FAILED'
        return (False, report)
    
    # Validate syntax and structure
    valid, validation = SourceValidator.validate_source_files(mandate_text, guidelines_text)
    
    if not valid:
        report['errors'].extend(validation['errors'])
        report['status'] = 'FAILED'
        report['data'] = validation
        return (False, report)
    
    report['checks']['mandate_spec_valid'] = validation['mandate']['valid']
    report['checks']['guidelines_dsl_valid'] = validation['guidelines']['valid']
    report['warnings'].extend(validation['warnings'])
    report['data'] = {
        'mandate': validation['mandate']['statistics'],
        'guidelines': validation['guidelines']['statistics'],
        'mandate_text': mandate_text,
        'guidelines_text': guidelines_text,
    }
    report['status'] = 'SUCCESS'
    
    return (True, report)
