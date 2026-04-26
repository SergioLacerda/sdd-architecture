"""Validate migration content parity"""
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List, Tuple


@dataclass
class ValidationResult:
    """Validation result for a check"""
    check_name: str
    passed: bool
    message: str
    details: Dict[str, Any] = None

    def __post_init__(self):
        if self.details is None:
            self.details = {}


class MigrationValidator:
    """Validate migration output"""

    def __init__(self):
        self.results: List[ValidationResult] = []

    def validate_mandate_spec(self, spec_file: Path, expected_count: int = 15) -> bool:
        """Validate mandate.spec DSL file"""
        if not spec_file.exists():
            self.results.append(ValidationResult(
                check_name="mandate_spec_exists",
                passed=False,
                message=f"mandate.spec not found at {spec_file}"
            ))
            return False

        content = spec_file.read_text(encoding='utf-8')

        # Check mandate count
        mandate_pattern = r'mandate (M\d+)'
        matches = re.findall(mandate_pattern, content)

        if len(matches) != expected_count:
            self.results.append(ValidationResult(
                check_name="mandate_count",
                passed=False,
                message=f"Expected {expected_count} mandates, found {len(matches)}",
                details={"expected": expected_count, "found": len(matches)}
            ))
        else:
            self.results.append(ValidationResult(
                check_name="mandate_count",
                passed=True,
                message=f"Correct mandate count: {len(matches)}",
                details={"count": len(matches)}
            ))

        # Check for empty fields
        empty_fields = self._find_empty_fields(content)
        if empty_fields:
            self.results.append(ValidationResult(
                check_name="empty_fields",
                passed=False,
                message=f"Found empty fields: {len(empty_fields)}",
                details={"empty_fields": empty_fields[:5]}
            ))
        else:
            self.results.append(ValidationResult(
                check_name="empty_fields",
                passed=True,
                message="No empty fields found",
            ))

        # Check ID sequencing
        ids_valid, invalid_ids = self._validate_ids(matches)
        if not ids_valid:
            self.results.append(ValidationResult(
                check_name="sequential_ids",
                passed=False,
                message=f"Non-sequential IDs found: {invalid_ids[:5]}",
                details={"invalid": invalid_ids}
            ))
        else:
            self.results.append(ValidationResult(
                check_name="sequential_ids",
                passed=True,
                message="All IDs properly sequenced",
                details={"ids": matches}
            ))

        # Check syntax validity
        syntax_valid, syntax_errors = self._validate_dsl_syntax(content)
        if not syntax_valid:
            self.results.append(ValidationResult(
                check_name="dsl_syntax",
                passed=False,
                message=f"DSL syntax errors found: {len(syntax_errors)}",
                details={"errors": syntax_errors[:3]}
            ))
        else:
            self.results.append(ValidationResult(
                check_name="dsl_syntax",
                passed=True,
                message="DSL syntax is valid",
            ))

        return all(r.passed for r in self.results if r.check_name.startswith('mandate'))

    def validate_guidelines_dsl(self, dsl_file: Path) -> bool:
        """Validate guidelines.dsl file"""
        if not dsl_file.exists():
            self.results.append(ValidationResult(
                check_name="guidelines_dsl_exists",
                passed=False,
                message=f"guidelines.dsl not found at {dsl_file}"
            ))
            return False

        content = dsl_file.read_text(encoding='utf-8')

        # Check guideline count (should have some)
        guideline_pattern = r'guideline (G\d+)'
        matches = re.findall(guideline_pattern, content)

        if len(matches) == 0:
            self.results.append(ValidationResult(
                check_name="guidelines_count",
                passed=False,
                message="No guidelines found in dsl file",
            ))
        else:
            self.results.append(ValidationResult(
                check_name="guidelines_count",
                passed=True,
                message=f"Found {len(matches)} guidelines",
                details={"count": len(matches)}
            ))

        return len(matches) > 0

    def _find_empty_fields(self, content: str) -> List[str]:
        """Find empty field declarations in DSL"""
        empty_patterns = [
            r'title:\s*""',
            r'description:\s*""',
            r'rationale:\s*""',
        ]

        empty_fields = []
        for pattern in empty_patterns:
            matches = re.findall(pattern, content)
            empty_fields.extend(matches)

        return empty_fields

    def _validate_ids(self, ids: List[str]) -> Tuple[bool, List[str]]:
        """Validate ID sequencing"""
        expected = [f'M{str(i).zfill(3)}' for i in range(1, len(ids) + 1)]
        invalid = [id for id in ids if id not in expected]

        return len(invalid) == 0, invalid

    def _validate_dsl_syntax(self, content: str) -> Tuple[bool, List[str]]:
        """Validate basic DSL syntax"""
        errors = []

        # Check for balanced braces
        open_braces = content.count('{')
        close_braces = content.count('}')
        if open_braces != close_braces:
            errors.append(f"Unbalanced braces: {open_braces} open, {close_braces} close")

        # Check for proper string quotes
        string_pattern = r':\s+"[^"]*"'
        strings = re.findall(string_pattern, content)
        if len(strings) == 0 and 'title:' in content:
            errors.append("No properly quoted strings found")

        return len(errors) == 0, errors

    def get_report(self) -> Dict[str, Any]:
        """Get validation report"""
        passed = sum(1 for r in self.results if r.passed)
        total = len(self.results)

        return {
            'summary': {
                'passed': passed,
                'total': total,
                'success_rate': f"{(passed/total*100):.1f}%" if total > 0 else "0%"
            },
            'results': [asdict(r) for r in self.results]
        }

    def save_report(self, output_path: Path):
        """Save validation report to JSON"""
        report = self.get_report()
        output_path.write_text(
            json.dumps(report, indent=2, default=str),
            encoding='utf-8'
        )
