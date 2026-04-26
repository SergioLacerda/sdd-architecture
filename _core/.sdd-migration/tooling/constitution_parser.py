"""Parse v2.1 constitution markdown to extract mandates"""
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List


@dataclass
class Mandate:
    """Represents a v2.1 principle/mandate"""
    id: str
    title: str
    description: str
    category: str
    rationale: str = ""
    validation: List[str] = None

    def __post_init__(self):
        if self.validation is None:
            self.validation = []


class ConstitutionParser:
    """Parse v2.1 EXECUTION/spec/CANONICAL/rules/constitution.md"""

    def __init__(self):
        self.mandates: List[Mandate] = []

    def parse_file(self, file_path: Path) -> List[Mandate]:
        """Parse constitution markdown file and extract mandates"""
        content = file_path.read_text(encoding='utf-8')
        self.mandates = self._extract_mandates(content)
        return self.mandates

    def _extract_mandates(self, content: str) -> List[Mandate]:
        """Extract mandate blocks from markdown"""
        mandates = []

        # Pattern: ## 🎯 CORE PRINCIPLE: <Title>
        principle_pattern = r'##\s+🎯\s+CORE PRINCIPLE:\s+(.+?)\n'
        principle_matches = list(re.finditer(principle_pattern, content))

        for idx, match in enumerate(principle_matches):
            title = match.group(1).strip()
            start_pos = match.start()

            # Find content until next principle or end
            if idx + 1 < len(principle_matches):
                end_pos = principle_matches[idx + 1].start()
            else:
                end_pos = len(content)

            principle_block = content[start_pos:end_pos]

            # Extract components
            description = self._extract_section(principle_block, 'THE PRINCIPLE')
            rationale = self._extract_section(principle_block, 'RATIONALE') or "Foundation principle"
            validation = self._extract_validation(principle_block)

            # Infer category from title
            category = self._infer_category(title)

            mandate_id = f"M{str(len(mandates) + 1).zfill(3)}"

            mandate = Mandate(
                id=mandate_id,
                title=title,
                description=description,
                category=category,
                rationale=rationale,
                validation=validation
            )
            mandates.append(mandate)

        return mandates

    def _extract_section(self, text: str, section_name: str) -> str:
        """Extract content of a named section"""
        pattern = rf'\*\*{section_name}\*\*\s*\n(.*?)(?=\n\*\*|\Z)'
        match = re.search(pattern, text, re.DOTALL)
        if match:
            content = match.group(1).strip()
            # Remove markdown formatting
            content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
            return content.strip()
        return ""

    def _extract_validation(self, text: str) -> List[str]:
        """Extract validation commands"""
        commands = []

        # Look for code blocks
        code_pattern = r'```(?:bash|shell)?\n(.*?)\n```'
        matches = re.findall(code_pattern, text, re.DOTALL)

        for match in matches:
            # Extract individual commands
            lines = match.strip().split('\n')
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#'):
                    commands.append(line)

        return commands

    def _infer_category(self, title: str) -> str:
        """Infer category from title"""
        title_lower = title.lower()

        categories = {
            'architecture': ['architecture', 'layer', 'clean'],
            'testing': ['test', 'tdd', 'coverage'],
            'async': ['async', 'concurrency', 'parallel'],
            'ci/cd': ['pipeline', 'ci', 'cd', 'deploy'],
            'documentation': ['doc', 'comment', 'readme'],
            'code-quality': ['quality', 'lint', 'format', 'style'],
        }

        for category, keywords in categories.items():
            if any(kw in title_lower for kw in keywords):
                return category

        return 'general'

    def to_dict(self) -> Dict[str, Any]:
        """Convert parsed mandates to dictionary"""
        return {
            'mandates': [
                {
                    'id': m.id,
                    'title': m.title,
                    'description': m.description,
                    'category': m.category,
                    'rationale': m.rationale,
                    'validation': m.validation
                }
                for m in self.mandates
            ],
            'metadata': {
                'total': len(self.mandates),
                'version': '2.1',
                'format': 'parsed'
            }
        }
