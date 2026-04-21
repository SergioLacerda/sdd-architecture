"""Phase 2: Load and deserialize compiled artifacts from .sdd-runtime/

This phase loads the compiled mandate.bin and guidelines.bin files from
the .sdd-runtime/ directory and deserializes them into usable data structures.

The compiled format uses MessagePack with indexed references to a string pool
for efficient storage. This phase reconstructs the original data structure.
"""

from pathlib import Path
from typing import Tuple, Dict, Any, List
import sys

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.loader import ArtifactLoader


def _reconstruct_guideline(guide_dict: Dict, string_pool: List[str]) -> Dict:
    """
    Reconstruct a guideline from indexed format to expanded format
    
    Converts index references (title_idx, description_idx, etc.) to actual strings
    from the string pool.
    """
    return {
        'id': guide_dict.get('id', 0),
        'type': guide_dict.get('type', 'SOFT'),
        'title': string_pool[guide_dict['title_idx']] if 'title_idx' in guide_dict else '',
        'description': string_pool[guide_dict['description_idx']] if 'description_idx' in guide_dict else '',
        'category': string_pool[guide_dict['category']] if isinstance(guide_dict.get('category'), int) else guide_dict.get('category', ''),
        'tags': [],  # Will be populated based on category
        'priority': guide_dict.get('priority', 2),  # Default to priority 2
    }


def _reconstruct_guidelines(compiled_data: Dict, string_pool: List[str]) -> Dict:
    """Reconstruct guidelines from indexed format"""
    guidelines = {}
    compiled_guidelines = compiled_data.get('guidelines', [])
    
    for guide_dict in compiled_guidelines:
        expanded = _reconstruct_guideline(guide_dict, string_pool)
        guide_id = f"G{expanded['id']:02d}"
        guidelines[guide_id] = expanded
    
    return guidelines


def _reconstruct_mandate(mandate_dict: Dict, string_pool: List[str]) -> Dict:
    """Reconstruct a mandate from indexed format"""
    return {
        'id': mandate_dict.get('id', ''),
        'title': string_pool[mandate_dict['title_idx']] if 'title_idx' in mandate_dict else '',
        'description': string_pool[mandate_dict['description_idx']] if 'description_idx' in mandate_dict else '',
        'priority': mandate_dict.get('priority', 1),
    }


def _reconstruct_mandates(compiled_data: Dict, string_pool: List[str]) -> Dict:
    """Reconstruct mandates from indexed format"""
    mandates = {}
    compiled_mandates = compiled_data.get('mandates', [])
    
    for mandate_dict in compiled_mandates:
        expanded = _reconstruct_mandate(mandate_dict, string_pool)
        mandate_id = expanded.get('id', '')
        if mandate_id:
            mandates[mandate_id] = expanded
    
    return mandates


def phase_2_load_compiled(repo_root: Path = Path.cwd()) -> Tuple[bool, Dict]:
    """
    Load and deserialize compiled artifacts from .sdd-runtime/
    
    Args:
        repo_root: Repository root directory
    
    Returns:
        (success: bool, report: Dict)
        report contains:
            - phase: 'PHASE_2_LOAD_COMPILED'
            - status: 'SUCCESS' | 'FAILED'
            - checks: dict of validation checks performed
            - data: dict with loaded mandate and guideline data
            - statistics: counts of mandates and guidelines
            - errors: list of error messages
            - warnings: list of warning messages
    """
    
    report = {
        'phase': 'PHASE_2_LOAD_COMPILED',
        'status': 'PENDING',
        'checks': {
            'mandate_bin_exists': False,
            'guidelines_bin_exists': False,
            'metadata_exists': False,
            'artifacts_deserialize': False,
            'data_reconstruction': False,
        },
        'data': {
            'mandate': {},
            'guidelines': {},
        },
        'statistics': {
            'mandate_count': 0,
            'guideline_count': 0,
            'string_pool_size': 0,
        },
        'errors': [],
        'warnings': [],
        '_artifacts': {},  # Internal: raw compiled data
    }
    
    # Step 1: Check .sdd-runtime/ exists
    sdd_runtime = repo_root / ".sdd-runtime"
    if not sdd_runtime.exists():
        report['errors'].append(f'.sdd-runtime directory not found at {sdd_runtime}')
        report['status'] = 'FAILED'
        return (False, report)
    
    # Step 2: Check files exist
    mandate_bin = sdd_runtime / "mandate.bin"
    guidelines_bin = sdd_runtime / "guidelines.bin"
    metadata_json = sdd_runtime / "metadata.json"
    
    if not mandate_bin.exists():
        report['warnings'].append(f'mandate.bin not found (optional)')
    else:
        report['checks']['mandate_bin_exists'] = True
    
    if not guidelines_bin.exists():
        report['errors'].append(f'guidelines.bin not found')
        report['status'] = 'FAILED'
        return (False, report)
    
    report['checks']['guidelines_bin_exists'] = True
    
    if not metadata_json.exists():
        report['warnings'].append(f'metadata.json not found (optional)')
    else:
        report['checks']['metadata_exists'] = True
    
    # Step 3: Load artifacts
    try:
        loader = ArtifactLoader(repo_root)
        
        # Try to load mandate (may not exist)
        mandate_compiled = {}
        try:
            mandate_compiled = loader.load_compiled_mandate()
        except FileNotFoundError:
            report['warnings'].append('Mandate compiled artifacts not found')
        
        # Load guidelines (required)
        guidelines_compiled = loader.load_compiled_guidelines()
        
        # Load metadata
        metadata = {}
        try:
            metadata = loader.load_metadata()
        except FileNotFoundError:
            pass
        
        report['checks']['artifacts_deserialize'] = True
        report['_artifacts']['mandate'] = mandate_compiled
        report['_artifacts']['guidelines'] = guidelines_compiled
        report['_artifacts']['metadata'] = metadata
        
    except Exception as e:
        report['errors'].append(f'Failed to deserialize compiled artifacts: {e}')
        report['status'] = 'FAILED'
        return (False, report)
    
    # Step 4: Reconstruct data from indexed format
    try:
        string_pool = guidelines_compiled.get('string_pool', [])
        report['statistics']['string_pool_size'] = len(string_pool)
        
        # Reconstruct mandates
        if mandate_compiled:
            reconstructed_mandates = _reconstruct_mandates(mandate_compiled, string_pool)
            report['data']['mandate'] = reconstructed_mandates
            report['statistics']['mandate_count'] = len(reconstructed_mandates)
        else:
            # If mandate.bin doesn't exist, use empty dict
            report['data']['mandate'] = {}
            report['statistics']['mandate_count'] = 0
        
        # Reconstruct guidelines
        reconstructed_guidelines = _reconstruct_guidelines(guidelines_compiled, string_pool)
        report['data']['guidelines'] = reconstructed_guidelines
        report['statistics']['guideline_count'] = len(reconstructed_guidelines)
        
        report['checks']['data_reconstruction'] = True
        
    except Exception as e:
        report['errors'].append(f'Failed to reconstruct data: {e}')
        report['status'] = 'FAILED'
        return (False, report)
    
    # Step 5: Validate results
    if report['statistics']['guideline_count'] == 0:
        report['errors'].append('No guidelines loaded')
        report['status'] = 'FAILED'
        return (False, report)
    
    # Success
    report['status'] = 'SUCCESS'
    return (True, report)
