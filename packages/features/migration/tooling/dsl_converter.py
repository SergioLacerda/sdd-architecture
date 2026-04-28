"""Convert v2.1 mandates to v3.0 DSL format"""

from datetime import datetime
from typing import Any, Dict, List


class DSLConverter:
    """Convert parsed mandates to v3.0 DSL format"""

    @staticmethod
    def convert_mandates(mandates: List[Dict[str, Any]]) -> str:
        """Convert mandate list to .spec DSL format"""
        lines = [
            "# SDD v3.0 - MANDATE Specification",
            "# Generated from v2.1 constitution",
            f"# Generated: {datetime.utcnow().isoformat()}",
            "",
        ]

        for mandate in mandates:
            lines.extend(DSLConverter._format_mandate(mandate))
            lines.append("")

        return "\n".join(lines)

    @staticmethod
    def _format_mandate(mandate: Dict[str, Any]) -> List[str]:
        """Format a single mandate in DSL"""
        lines = []

        mandate_id = mandate.get("id", "M000")
        title = mandate.get("title", "Untitled")
        description = mandate.get("description", "")
        category = mandate.get("category", "general")
        rationale = mandate.get("rationale", "")
        validation = mandate.get("validation", [])

        lines.append(f"mandate {mandate_id} {{")
        lines.append("  type: HARD")
        lines.append(f'  title: "{DSLConverter._escape_string(title)}"')
        lines.append(f'  description: "{DSLConverter._escape_string(description)}"')
        lines.append(f"  category: {category}")

        if rationale:
            lines.append(f'  rationale: "{DSLConverter._escape_string(rationale)}"')

        # Add validation commands
        if validation:
            lines.append("  validation: {")
            lines.append("    commands: [")
            for cmd in validation:
                lines.append(f'      "{DSLConverter._escape_string(cmd)}",')
            lines.append("    ]")
            lines.append("  }")

        lines.append("}")

        return lines

    @staticmethod
    def _escape_string(s: str) -> str:
        """Escape string for DSL format"""
        s = s.replace("\\", "\\\\")
        s = s.replace('"', '\\"')
        s = s.replace("\n", "\\n")
        return s

    @staticmethod
    def convert_guidelines(guidelines: List[Dict[str, Any]]) -> str:
        """Convert guideline list to .dsl format"""
        lines = [
            "# SDD v3.0 - GUIDELINES Specification",
            "# Generated from v2.1 guides",
            f"# Generated: {datetime.utcnow().isoformat()}",
            "",
        ]

        for guideline in guidelines:
            lines.extend(DSLConverter._format_guideline(guideline))
            lines.append("")

        return "\n".join(lines)

    @staticmethod
    def _format_guideline(guideline: Dict[str, Any]) -> List[str]:
        """Format a single guideline in DSL"""
        lines = []

        guide_id = guideline.get("id", "G00")
        title = guideline.get("title", "Untitled")
        description = guideline.get("description", "")
        category = guideline.get("category", "general")
        examples = guideline.get("examples", [])

        lines.append(f"guideline {guide_id} {{")
        lines.append("  type: SOFT")
        lines.append(f'  title: "{DSLConverter._escape_string(title)}"')
        lines.append(f'  description: "{DSLConverter._escape_string(description)}"')
        lines.append(f"  category: {category}")

        # Add examples if present
        if examples:
            lines.append("  examples: [")
            for example in examples:
                lines.append(f'    "{DSLConverter._escape_string(example)}",')
            lines.append("  ]")

        lines.append("}")

        return lines
