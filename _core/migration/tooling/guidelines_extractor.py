"""Extract v2.1 guidelines from spec/guides/"""

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List


@dataclass
class Guideline:
    """Represents a v2.1 guideline"""

    id: str
    title: str
    description: str
    category: str
    examples: List[str] = None

    def __post_init__(self):
        if self.examples is None:
            self.examples = []


class GuidelinesExtractor:
    """Extract SOFT rules from v2.1 spec/guides/"""

    def __init__(self):
        self.guidelines: List[Guideline] = []

    def extract_from_directory(self, guides_dir: Path) -> List[Guideline]:
        """Extract guidelines from all markdown files in guides directory"""
        if not guides_dir.exists():
            return []

        for md_file in sorted(guides_dir.glob("*.md")):
            self._extract_from_file(md_file)

        return self.guidelines

    def _extract_from_file(self, file_path: Path):
        """Extract guidelines from a single markdown file"""
        content = file_path.read_text(encoding="utf-8")

        # Look for guideline sections
        # Pattern: ## <Title> or ### <Title>
        section_pattern = r"^#+\s+([^#\n]+)$"

        matches = list(re.finditer(section_pattern, content, re.MULTILINE))

        for idx, match in enumerate(matches):
            title = match.group(1).strip()

            # Skip if looks like a table of contents or special section
            if title.lower() in ["table of contents", "overview", "index"]:
                continue

            start_pos = match.start()
            if idx + 1 < len(matches):
                end_pos = matches[idx + 1].start()
            else:
                end_pos = len(content)

            section_content = content[start_pos:end_pos]

            # Extract guideline info
            description = self._extract_content(section_content, 200)
            examples = self._extract_examples(section_content)
            category = self._infer_category(title)

            guide_id = f"G{str(len(self.guidelines) + 1).zfill(2)}"

            guideline = Guideline(id=guide_id, title=title, description=description, category=category, examples=examples)
            self.guidelines.append(guideline)

    def _extract_content(self, text: str, max_length: int = 200) -> str:
        """Extract content summary from section"""
        # Remove code blocks
        cleaned = re.sub(r"```.*?```", "", text, flags=re.DOTALL)

        # Split by newlines and get first few lines
        lines = cleaned.split("\n")
        content_lines = []

        for line in lines:
            line = line.strip()
            # Skip markdown formatting, headers, empty lines
            if line and not line.startswith("#") and not line.startswith("*"):
                content_lines.append(line)
                if len("\n".join(content_lines)) > max_length:
                    break

        content = " ".join(content_lines)
        if len(content) > max_length:
            content = content[:max_length].rsplit(" ", 1)[0] + "..."

        return content

    def _extract_examples(self, text: str) -> List[str]:
        """Extract code examples from section"""
        examples = []

        # Look for code blocks
        code_pattern = r"```(?:python|javascript|bash|shell|java|go)?\n(.*?)\n```"
        matches = re.findall(code_pattern, text, re.DOTALL)

        for match in matches:
            # Take first line or first 100 chars
            example = match.strip().split("\n")[0]
            if example:
                examples.append(example[:100])

        return examples

    def _infer_category(self, title: str) -> str:
        """Infer guideline category from title"""
        title_lower = title.lower()

        categories = {
            "naming": ["naming", "name", "convention"],
            "documentation": ["doc", "comment", "readme", "changelog"],
            "testing": ["test", "mock", "fixture"],
            "code-style": ["style", "format", "lint", "spacing"],
            "communication": ["communication", "tone", "language"],
            "git": ["git", "commit", "branch", "pr", "push"],
            "performance": ["performance", "optimize", "slow", "cache"],
        }

        for category, keywords in categories.items():
            if any(kw in title_lower for kw in keywords):
                return category

        return "general"

    def to_dict(self) -> Dict[str, Any]:
        """Convert guidelines to dictionary"""
        return {
            "guidelines": [
                {"id": g.id, "title": g.title, "description": g.description, "category": g.category, "examples": g.examples}
                for g in self.guidelines
            ],
            "metadata": {"total": len(self.guidelines), "version": "2.1", "format": "extracted"},
        }
