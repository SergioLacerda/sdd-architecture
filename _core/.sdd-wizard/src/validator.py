"""
SDD v3.0 Wizard - Phase 1: Validate SOURCE (.sdd-core/)

Validates that source DSL files have correct syntax and structure
"""

import re
from typing import Dict, List, Tuple


class SourceValidator:
    """Validate SOURCE files (mandate.spec, guidelines.dsl)"""

    MANDATE_PATTERN = r'mandate\s+(M\d+)\s*\{'
    GUIDELINE_PATTERN = r'guideline\s+(G\d+)\s*\{'

    @staticmethod
    def validate_dsl_syntax(text: str, file_type: str = "dsl") -> List[str]:
        """Validate basic DSL syntax (balanced braces, etc)"""
        errors = []

        # Check for balanced braces
        if text.count('{') != text.count('}'):
            errors.append(f"Unbalanced braces: {text.count('{')} opening, {text.count('}')} closing")

        # Check for balanced quotes
        double_quotes = text.count('"')
        if double_quotes % 2 != 0:
            errors.append(f"Odd number of double quotes: {double_quotes}")

        # Basic sanity: should not be empty
        if not text.strip():
            errors.append("File is empty")

        return errors

    @staticmethod
    def validate_mandate_spec(mandate_text: str) -> Dict[str, any]:
        """Validate mandate.spec structure"""
        result = {
            'valid': True,
            'errors': [],
            'warnings': [],
            'statistics': {
                'mandate_count': 0,
                'mandate_ids': [],
                'lines': len(mandate_text.split('\n')),
                'bytes': len(mandate_text.encode('utf-8')),
            }
        }

        # Syntax validation
        syntax_errors = SourceValidator.validate_dsl_syntax(mandate_text, "mandate")
        if syntax_errors:
            result['valid'] = False
            result['errors'].extend(syntax_errors)
            return result

        # Find all mandates
        mandates = re.findall(r'mandate\s+(M\d+)', mandate_text)
        result['statistics']['mandate_count'] = len(mandates)
        result['statistics']['mandate_ids'] = list(dict.fromkeys(mandates))  # Unique, preserve order

        # Check for duplicates
        if len(mandates) != len(set(mandates)):
            duplicates = [m for m in set(mandates) if mandates.count(m) > 1]
            result['errors'].append(f"Duplicate mandate IDs: {duplicates}")
            result['valid'] = False

        # Check sequential IDs (M001, M002, etc.)
        if mandates:
            expected_ids = [f"M{str(i+1).zfill(3)}" for i in range(len(set(mandates)))]
            actual_ids = sorted(set(mandates))
            if actual_ids != expected_ids:
                result['warnings'].append(
                    f"Non-sequential mandate IDs. Found: {actual_ids}, Expected: {expected_ids}"
                )

        # Check for empty mandates (mandate M001 {} with nothing inside)
        empty_mandates = re.findall(r'mandate\s+M\d+\s*\{\s*\}', mandate_text)
        if empty_mandates:
            result['errors'].append(f"Empty mandates found: {len(empty_mandates)}")
            result['valid'] = False

        return result

    @staticmethod
    def validate_guidelines_dsl(guidelines_text: str) -> Dict[str, any]:
        """Validate guidelines.dsl structure"""
        result = {
            'valid': True,
            'errors': [],
            'warnings': [],
            'statistics': {
                'guideline_count': 0,
                'guideline_ids': [],
                'lines': len(guidelines_text.split('\n')),
                'bytes': len(guidelines_text.encode('utf-8')),
            }
        }

        # Syntax validation
        syntax_errors = SourceValidator.validate_dsl_syntax(guidelines_text, "guidelines")
        if syntax_errors:
            result['valid'] = False
            result['errors'].extend(syntax_errors)
            return result

        # Find all guidelines
        guidelines = re.findall(r'guideline\s+(G\d+)', guidelines_text)
        result['statistics']['guideline_count'] = len(guidelines)
        result['statistics']['guideline_ids'] = list(dict.fromkeys(guidelines))

        # Check for duplicates
        if len(guidelines) != len(set(guidelines)):
            duplicates = [g for g in set(guidelines) if guidelines.count(g) > 1]
            result['errors'].append(f"Duplicate guideline IDs: {duplicates}")
            result['valid'] = False

        # Check for empty guidelines
        empty_guidelines = re.findall(r'guideline\s+G\d+\s*\{\s*\}', guidelines_text)
        if empty_guidelines:
            result['errors'].append(f"Empty guidelines found: {len(empty_guidelines)}")
            result['valid'] = False

        # Warning if no guidelines found (but file exists, might be template)
        if not guidelines:
            result['warnings'].append("No guidelines found in file")

        return result

    @staticmethod
    def validate_source_files(mandate_text: str, guidelines_text: str) -> Tuple[bool, Dict]:
        """Validate both source files together"""
        mandate_result = SourceValidator.validate_mandate_spec(mandate_text)
        guidelines_result = SourceValidator.validate_guidelines_dsl(guidelines_text)

        # Combine results
        combined = {
            'valid': mandate_result['valid'] and guidelines_result['valid'],
            'mandate': mandate_result,
            'guidelines': guidelines_result,
            'errors': mandate_result['errors'] + guidelines_result['errors'],
            'warnings': mandate_result['warnings'] + guidelines_result['warnings'],
        }

        return (combined['valid'], combined)
