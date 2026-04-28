"""Generate AI agent seed configurations."""

from pathlib import Path
from typing import Any, Dict, List, Tuple


def generate_agent_seeds(output_dir: Path, config: Dict[str, Any]) -> List[Tuple[str, Path, str]]:
    """
    Generate agent seed templates for different AI platforms.

    Args:
        output_dir: Directory to save agent seeds
        config: Governance configuration dictionary

    Returns:
        List of tuples: (agent_name, file_path, status)
    """
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    # Get governance items
    items = config.get("items", [])
    mandatory_rules = [i for i in items if i.get("type") == "rule" and i.get("is_immutable")]
    customizable_items = [i for i in items if not i.get("is_immutable")]

    results = []

    # 1. Cursor Agent Seed
    cursor_content = _generate_cursor_seed(config, mandatory_rules, customizable_items)
    cursor_path = output_dir / "cursor-agent.md"
    cursor_path.write_text(cursor_content, encoding="utf-8")
    results.append(("Cursor IDE", cursor_path, "✓ Generated"))

    # 2. Copilot Agent Seed
    copilot_content = _generate_copilot_seed(config, mandatory_rules, customizable_items)
    copilot_path = output_dir / "copilot-agent.md"
    copilot_path.write_text(copilot_content, encoding="utf-8")
    results.append(("GitHub Copilot", copilot_path, "✓ Generated"))

    # 3. Generic Agent Seed
    generic_content = _generate_generic_seed(config, mandatory_rules, customizable_items)
    generic_path = output_dir / "generic-agent.md"
    generic_path.write_text(generic_content, encoding="utf-8")
    results.append(("Generic AI", generic_path, "✓ Generated"))

    return results


def _generate_cursor_seed(config: Dict[str, Any], mandatory_rules: List[Dict], customizable_items: List[Dict]) -> str:
    """Generate Cursor IDE specific agent seed."""
    return f"""# Cursor Agent Configuration

## Governance Context
- **Core Fingerprint**: {config.get("core_fingerprint", "N/A")[:32]}
- **Status**: Production Ready
- **Total Items**: {len(config.get("items", []))}

## Mandatory Governance Rules
These rules must be enforced in every implementation:

{_format_rules(mandatory_rules)}

## Governance Checklist
Before implementing any feature:
- [ ] Validate against mandatory rules
- [ ] Check for conflicts with existing items
- [ ] Ensure customizable items are respected
- [ ] Verify fingerprints match core specification

## Customizable Items
Your project can customize {len(customizable_items)} governance items.

See `_spec/architecture/` for complete specification.

## Integration Points
- Load governance: `from sdd_wizard.governance_runtime_loader import GovernanceRuntimeLoader`
- Validate changes: Use `validate_governance_path()` from CLI
- Generate templates: `sdd governance generate`
"""


def _generate_copilot_seed(config: Dict[str, Any], mandatory_rules: List[Dict], customizable_items: List[Dict]) -> str:
    """Generate GitHub Copilot agent seed."""
    return f"""# GitHub Copilot Governance Context

## Architecture Context
This codebase follows a Self-Documented Domain (SDD) architecture with governance enforcement.

- **Core Fingerprint**: {config.get("core_fingerprint", "N/A")[:32]}
- **Client Fingerprint**: {config.get("client_fingerprint", "N/A")[:32]}
- **Items Protected**: 4 core immutable + {len(customizable_items)} customizable

## Critical Rules (Immutable)

{_format_rules(mandatory_rules)}

## Before Suggesting Code
1. Check mandatory rules above
2. Respect customizable governance items
3. Validate against `wizard/compiled/` specifications
4. Use provided templates from `wizard/templates/`

## Key Resources
- Specifications: `_spec/architecture/specifications/`
- Decisions: `_spec/architecture/decisions/`

## Governance Validation
Run `sdd governance validate` to ensure compliance before commits.
"""


def _generate_generic_seed(config: Dict[str, Any], mandatory_rules: List[Dict], customizable_items: List[Dict]) -> str:
    """Generate generic AI agent seed."""
    return f"""# AI Agent Governance Configuration

## Specification Summary
- **Architecture**: Self-Documented Domain (SDD)
- **Governance Model**: 2-file approach (core immutable + client customizable)
- **Total Managed Items**: {len(config.get("items", []))}
- **Enforcement Level**: Strict (fingerprint-based verification)

## Governance Fingerprints
```
Core Fingerprint:   {config.get("core_fingerprint", "N/A")}
Client Fingerprint: {config.get("client_fingerprint", "N/A")}
Salt-Based:         Core fingerprint embedded in client metadata
```

## Mandatory Rules

{_format_rules(mandatory_rules)}

## Implementation Guidelines

### When Implementing Features:
1. Load governance context: `GovernanceRuntimeLoader`
2. Check mandatory rules (immutable)
3. Respect customizable items (can be extended)
4. Use provided templates: `wizard/templates/`
5. Validate before commit: `sdd governance validate`

### When Generating Code:
- Follow mandatory rules strictly
- Suggest customization points for governance items
- Respect core fingerprint (do not modify)
- Reference CANONICAL specifications

### Integration Workflow:
```
1. Load: sdd governance load
2. Validate: sdd governance validate
3. Generate: sdd governance generate
4. Implement: Follow templates + rules
5. Verify: sdd governance validate
6. Commit: git commit
```

## Directory Structure
```
Framework:
  ├── _spec/             # Specification authority
  │   ├── architecture/  # Architecture decisions & specs
  │   │   ├── decisions/     # Architecture Decision Records
  │   │   └── specifications/ # Technical specifications
  │   ├── guides/        # Adoption, operational guides
  │   ├── custom/        # Project specializations
  │   └── SCRIPTS/       # Validation scripts
  ├── packages/            # Core infrastructure
  │   └── wizard/  # Wizard runtime
  └── sdd-generated/    # User output
```

## Key Commands
```bash
# Display governance summary
sdd governance load

# Validate governance integrity
sdd governance validate

# Generate agent seeds and templates
sdd governance generate
```

## Resources
- Full Specification: `_spec/architecture/`
- Runtime Loader: `packages/wizard/governance_runtime_loader.py`
- CLI: `sdd --help`
"""


def _format_rules(rules: List[Dict]) -> str:
    """Format rules as markdown list."""
    if not rules:
        return "No mandatory rules defined."

    formatted = []
    for i, rule in enumerate(rules, 1):
        name = rule.get("name", f"Rule {i}")
        description = rule.get("description", "No description")
        formatted.append(f"{i}. **{name}**: {description}")

    return "\n".join(formatted)
