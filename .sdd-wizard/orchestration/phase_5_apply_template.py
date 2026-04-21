"""Phase 5: Apply template scaffold and customizations

Copies template files from .sdd-template/ and applies language/profile customizations
"""

from pathlib import Path
from typing import Tuple, Dict, Any
import shutil
import json


def _get_language_template_dir(language: str) -> Path:
    """Get language-specific template directory"""
    wizard_root = Path(__file__).parent.parent
    return wizard_root.parent / ".sdd-template" / "languages" / language


def _get_profile_template_dir(profile: str) -> Path:
    """Get profile-specific template directory"""
    wizard_root = Path(__file__).parent.parent
    return wizard_root.parent / ".sdd-template" / "profiles" / profile


def _get_base_template_dir() -> Path:
    """Get base template directory"""
    wizard_root = Path(__file__).parent.parent
    return wizard_root.parent / ".sdd-template" / "base"


def _copy_template_files(
    source_dir: Path,
    target_dir: Path,
    ignored_patterns: list = None
) -> Tuple[int, list]:
    """Copy template files from source to target directory
    
    Returns:
        (files_copied, errors)
    """
    if not source_dir.exists():
        return (0, [f"Template directory not found: {source_dir}"])
    
    errors = []
    files_copied = 0
    
    try:
        for item in source_dir.rglob('*'):
            if item.is_file():
                # Calculate relative path
                rel_path = item.relative_to(source_dir)
                target_file = target_dir / rel_path
                
                # Create parent directories
                target_file.parent.mkdir(parents=True, exist_ok=True)
                
                # Copy file
                shutil.copy2(item, target_file)
                files_copied += 1
    except Exception as e:
        errors.append(f"Error copying template files: {e}")
    
    return (files_copied, errors)


def _apply_placeholder_replacements(
    text: str,
    replacements: Dict[str, str]
) -> str:
    """Replace placeholders in text
    
    Args:
        text: Text content with placeholders
        replacements: Dict of {placeholder: value}
    
    Returns:
        Text with placeholders replaced
    """
    result = text
    for placeholder, value in replacements.items():
        result = result.replace(f"{{{{{placeholder}}}}}", str(value))
    
    return result


def _customize_file_for_language(
    file_path: Path,
    language: str
) -> Tuple[bool, str]:
    """Apply language-specific customizations to a file
    
    Returns:
        (success, message)
    """
    if not file_path.exists():
        return (False, f"File not found: {file_path}")
    
    try:
        # Read file
        content = file_path.read_text(encoding='utf-8')
        
        # Language-specific placeholders
        replacements = {
            'LANGUAGE': language.upper(),
            'language': language.lower(),
        }
        
        # Apply replacements
        customized = _apply_placeholder_replacements(content, replacements)
        
        # Write back
        file_path.write_text(customized, encoding='utf-8')
        
        return (True, f"Customized for {language}")
    except Exception as e:
        return (False, f"Error customizing file: {e}")


def _customize_file_for_profile(
    file_path: Path,
    profile: str
) -> Tuple[bool, str]:
    """Apply profile-specific customizations to a file
    
    Returns:
        (success, message)
    """
    if not file_path.exists():
        return (False, f"File not found: {file_path}")
    
    try:
        content = file_path.read_text(encoding='utf-8')
        
        # Profile-specific placeholders
        replacements = {
            'PROFILE': profile.upper(),
            'profile': profile.lower(),
        }
        
        customized = _apply_placeholder_replacements(content, replacements)
        file_path.write_text(customized, encoding='utf-8')
        
        return (True, f"Customized for {profile} profile")
    except Exception as e:
        return (False, f"Error customizing file: {e}")


def phase_5_apply_template(
    scaffolding_dir: Path,
    language: str = 'python',
    profile: str = 'full',
    repo_root: Path = Path.cwd()
) -> Tuple[bool, Dict[str, Any]]:
    """Apply template scaffold and customizations
    
    Args:
        scaffolding_dir: Output directory for scaffolding
        language: Target language (java|python|js)
        profile: Profile level (lite|full)
        repo_root: Repository root
    
    Returns:
        (success, report)
    """
    report = {
        'phase': 'PHASE_5_APPLY_TEMPLATE',
        'status': 'PENDING',
        'data': {},
        'statistics': {
            'base_files_copied': 0,
            'language_files_copied': 0,
            'profile_files_copied': 0,
            'customizations_applied': 0,
        },
        'warnings': [],
        'errors': [],
    }
    
    try:
        # Create scaffolding directory
        scaffolding_dir.mkdir(parents=True, exist_ok=True)
        
        # 1. Copy base templates
        base_dir = _get_base_template_dir()
        if not base_dir.exists():
            report['errors'].append(f"Base template directory not found: {base_dir}")
            report['status'] = 'FAILED'
            return (False, report)
        
        base_copied, base_errors = _copy_template_files(base_dir, scaffolding_dir)
        report['statistics']['base_files_copied'] = base_copied
        if base_errors:
            report['warnings'].extend(base_errors)
        
        # 2. Copy language-specific templates
        lang_dir = _get_language_template_dir(language)
        if lang_dir.exists():
            lang_copied, lang_errors = _copy_template_files(lang_dir, scaffolding_dir)
            report['statistics']['language_files_copied'] = lang_copied
            if lang_errors:
                report['warnings'].extend(lang_errors)
        else:
            report['warnings'].append(f"Language template not found: {lang_dir}")
        
        # 3. Copy profile-specific templates
        profile_dir = _get_profile_template_dir(profile)
        if profile_dir.exists():
            profile_copied, profile_errors = _copy_template_files(profile_dir, scaffolding_dir)
            report['statistics']['profile_files_copied'] = profile_copied
            if profile_errors:
                report['warnings'].extend(profile_errors)
        else:
            report['warnings'].append(f"Profile template not found: {profile_dir}")
        
        # 4. Apply customizations
        customizations_count = 0
        for file_path in scaffolding_dir.rglob('*'):
            if file_path.is_file() and file_path.suffix in ['.md', '.json', '.yml', '.yaml', '.txt', '.cfg']:
                # Apply language customization
                success, msg = _customize_file_for_language(file_path, language)
                if success:
                    customizations_count += 1
                
                # Apply profile customization
                success, msg = _customize_file_for_profile(file_path, profile)
                if success:
                    customizations_count += 1
        
        report['statistics']['customizations_applied'] = customizations_count
        
        # 5. Create required directories
        (scaffolding_dir / '.sdd' / 'CANONICAL').mkdir(parents=True, exist_ok=True)
        (scaffolding_dir / '.sdd-guidelines').mkdir(parents=True, exist_ok=True)
        (scaffolding_dir / 'src').mkdir(parents=True, exist_ok=True)
        
        report['data'] = {
            'scaffolding_dir': str(scaffolding_dir),
            'language': language,
            'profile': profile,
            'total_files': base_copied + report['statistics']['language_files_copied'] + report['statistics']['profile_files_copied'],
        }
        
        report['status'] = 'SUCCESS'
        return (True, report)
    
    except Exception as e:
        report['errors'].append(str(e))
        report['status'] = 'FAILED'
        return (False, report)
