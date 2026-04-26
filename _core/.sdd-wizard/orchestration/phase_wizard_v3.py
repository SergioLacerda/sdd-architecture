#!/usr/bin/env python3
"""
SDD Wizard v3 - 3-Phase Flow with Status-aware Governance

Phase 1: Generate markdown templates with status fields
  Input: mandate.spec, guidelines.dsl from _core/.sdd-core/
  Output: /sdd-generated/phase-1-choices/ (Multiple .md files by category)
  
Phase 2: Manual user review & customization
  Input: /sdd-generated/phase-1-choices/ (generated templates)
  Action: User copies to phase-2-input/, edits status values
  Output: /sdd-generated/phase-2-input/ (User-edited markdown templates)
  
Phase 3: Compile & fingerprint governance
  Input: /sdd-generated/phase-2-input/ (user-edited markdown)
  Output: /sdd-generated/final-output/ (Compiled JSON with SALT fingerprints)
"""

import json
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple

try:
    import yaml
except ImportError:
    yaml = None


@dataclass
class Mandate:
    """Represents a mandate from mandate.spec"""
    id: str
    type: str
    title: str
    description: str
    category: str
    rationale: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'type': self.type,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'rationale': self.rationale
        }


@dataclass
class Guideline:
    """Represents a guideline from guidelines.dsl"""
    id: str
    type: str
    title: str
    description: str
    category: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'type': self.type,
            'title': self.title,
            'description': self.description,
            'category': self.category
        }


class Phase1Generator:
    """Generate markdown templates from documentation with status fields"""

    def __init__(self, sdd_core_path: Path, output_path: Path, verbose: bool = False, config: dict = None):
        self.sdd_core_path = sdd_core_path
        self.output_path = output_path
        self.verbose = verbose
        self.config = config or {}
        self.language = config.get('language', 'Python') if config else 'Python'
        self.adoption_level = config.get('adoption_level', 'FULL') if config else 'FULL'
        self.mandates: List[Mandate] = []
        self.guidelines: List[Guideline] = []

    def log(self, message: str):
        if self.verbose:
            print(f"  ℹ️  {message}")

    def parse_mandate_spec(self) -> bool:
        """Parse mandate.spec file"""
        mandate_file = self.sdd_core_path / '.sdd-core' / 'mandate.spec'
        if not mandate_file.exists():
            print(f"  ❌ mandate.spec not found at {mandate_file}")
            return False

        content = mandate_file.read_text(encoding='utf-8')

        # Parse mandate blocks: mandate M001 { ... }
        pattern = r'mandate\s+(\w+)\s*\{([^}]+)\}'
        for match in re.finditer(pattern, content, re.MULTILINE | re.DOTALL):
            mandate_id = match.group(1)
            mandate_content = match.group(2)

            title = self._extract_field(mandate_content, 'title')
            desc = self._extract_field(mandate_content, 'description')
            type_ = self._extract_field(mandate_content, 'type')
            category = self._extract_field(mandate_content, 'category')
            rationale = self._extract_field(mandate_content, 'rationale')

            mandate = Mandate(
                id=mandate_id,
                type=type_,
                title=title,
                description=desc,
                category=category,
                rationale=rationale
            )
            self.mandates.append(mandate)
            self.log(f"Parsed mandate {mandate_id}: {title}")

        return len(self.mandates) > 0

    def parse_guidelines_dsl(self) -> bool:
        """Parse guidelines.dsl file"""
        guidelines_file = self.sdd_core_path / '.sdd-core' / 'guidelines.dsl'
        if not guidelines_file.exists():
            print(f"  ❌ guidelines.dsl not found at {guidelines_file}")
            return False

        content = guidelines_file.read_text(encoding='utf-8')

        # Parse guideline blocks: guideline G01 { ... }
        pattern = r'guideline\s+(\w+)\s*\{([^}]+)\}'
        for match in re.finditer(pattern, content, re.MULTILINE | re.DOTALL):
            guideline_id = match.group(1)
            guideline_content = match.group(2)

            title = self._extract_field(guideline_content, 'title')
            desc = self._extract_field(guideline_content, 'description')
            type_ = self._extract_field(guideline_content, 'type')
            category = self._extract_field(guideline_content, 'category')

            guideline = Guideline(
                id=guideline_id,
                type=type_,
                title=title,
                description=desc,
                category=category
            )
            self.guidelines.append(guideline)
            if len(self.guidelines) <= 5:
                self.log(f"Parsed guideline {guideline_id}: {title}")

        if len(self.guidelines) > 5:
            self.log(f"... and {len(self.guidelines) - 5} more guidelines")

        return len(self.guidelines) > 0

    def _extract_field(self, content: str, field: str) -> str:
        """Extract field value from content block"""
        pattern = rf'{field}:\s*"([^"]*)"'
        match = re.search(pattern, content)
        return match.group(1) if match else ""

    def generate_markdown_templates(self) -> bool:
        """Generate markdown files by category with status fields"""
        self.output_path.mkdir(parents=True, exist_ok=True)
        self.log(f"Creating output directory: {self.output_path}")

        # Group mandates by category
        if self.mandates:
            mandates_by_cat = {}
            for mandate in self.mandates:
                if mandate.category not in mandates_by_cat:
                    mandates_by_cat[mandate.category] = []
                mandates_by_cat[mandate.category].append(mandate)

            for category, mandates in mandates_by_cat.items():
                filename = self.output_path / f'mandates-{category}.md'
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(f"# Mandates - {category.upper()}\n\n")
                    f.write("⚠️ HARD RULES - These are mandatory by default\n\n")

                    for mandate in mandates:
                        f.write(f"## {mandate.id}: {mandate.title}\n\n")
                        f.write(f"**Type:** {mandate.type}\n\n")
                        f.write(f"**Description:** {mandate.description}\n\n")
                        if mandate.rationale:
                            f.write(f"**Rationale:** {mandate.rationale}\n\n")

                        # NEW: Status fields with defaults
                        f.write("**Status:** `required: true` (Default: mandatory)\n\n")
                        f.write("**Customizable:** `false` (Hard rules cannot be modified)\n\n")
                        f.write("**Optional:** `false` (Not negotiable)\n\n")

                        f.write("---\n\n")

                self.log(f"Created {filename}")

        # Group guidelines by category
        if self.guidelines:
            guidelines_by_cat = {}
            for guideline in self.guidelines:
                if guideline.category not in guidelines_by_cat:
                    guidelines_by_cat[guideline.category] = []
                guidelines_by_cat[guideline.category].append(guideline)

            for category, guidelines in guidelines_by_cat.items():
                filename = self.output_path / f'guidelines-{category}.md'
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(f"# Guidelines - {category.upper()}\n\n")
                    f.write("💡 SOFT RECOMMENDATIONS - These are optional/customizable\n\n")

                    for guideline in guidelines:
                        f.write(f"## {guideline.id}: {guideline.title}\n\n")
                        f.write(f"**Type:** {guideline.type}\n\n")
                        if guideline.description:
                            f.write(f"**Description:** {guideline.description}\n\n")

                        # NEW: Status fields with defaults
                        f.write("**Status:** `required: true` (Default: include)\n\n")
                        f.write("**Customizable:** `true` (Change below if needed)\n\n")
                        f.write("**Optional:** `false` (Included by default)\n\n")

                        f.write("### To Customize This Rule:\n\n")
                        f.write("Change the Status line above to ONE of:\n")
                        f.write("- `required: true` — Keep as mandatory\n")
                        f.write("- `optional: true` — Skip this rule\n")
                        f.write("- `custom: true` — Include but customizable\n\n")

                        f.write("---\n\n")

                self.log(f"Created {filename}")

        # Generate README with instructions
        readme = self.output_path / 'README.md'
        with open(readme, 'w', encoding='utf-8') as f:
            f.write(f"""# Phase 1: Governance Rules Templates

**Generated:** {datetime.now().isoformat()}

## Configuration

- **Language:** {self.language}
- **Adoption Level:** {self.adoption_level}

## What You Have

Raw templates for all mandates and guidelines, organized by category:
- `mandates-*.md` — Core architectural rules (hard, non-negotiable)
- `guidelines-*.md` — Best practices (soft, customizable)

Total: {len(self.mandates)} mandates + {len(self.guidelines)} guidelines

## Status Field Defaults

Each rule starts with:
```
**Status:** required: true
**Customizable:** true/false
**Optional:** false
```

## Phase 2: What to Do Now

### Step 1: Edit the Files

For each `.md` file in this folder:

1. **Open** in your editor
2. **Read** each rule (understand what it does)
3. **For each rule**, decide its status:
   - Keep as required: `required: true` → Include in final governance
   - Make optional: `optional: true` → Skip this rule
   - Make customizable: `custom: true` → Include but allow customization

### Step 2: Change Status Lines

Find lines like:
```markdown
**Status:** `required: true` (Default: include)
```

Change to ONE of:
```markdown
**Status:** `required: true`
**Status:** `optional: true`
**Status:** `custom: true`
```

### Step 3: Run Phase 3

Once you've edited the markdown files, just run:

```bash
./wizard.sh
# Choose: [3] Phase 3
```

Phase 3 will:
1. Read your edited markdown files from this folder
2. Parse the status fields (required/optional/custom)
3. Skip items marked as optional
4. Compile to final governance JSON

No need to convert to YAML or move files - edit in place!

## Questions?

- Mandates: Always required (cannot customize)
- Guidelines: Can be required/optional/custom
- Default: Everything starts as required (you decide what to change)
""")
        self.log(f"Created {readme}")

        return True

    def run(self) -> Dict[str, Any]:
        """Execute Phase 1"""
        print("\n📝 PHASE 1: Generate Governance Templates")
        print("=" * 70)

        if not self.parse_mandate_spec():
            return {'success': False, 'error': 'Failed to parse mandate.spec'}

        if not self.parse_guidelines_dsl():
            return {'success': False, 'error': 'Failed to parse guidelines.dsl'}

        if not self.generate_markdown_templates():
            return {'success': False, 'error': 'Failed to generate markdown templates'}

        # Create input directory for Phase 2 user review
        phase2_input = self.output_path.parent / 'phase-2-input'
        phase2_input.mkdir(parents=True, exist_ok=True)
        self.log("Created phase-2-input directory (ready for Phase 2 customization)")

        print(f"  ✅ Generated {len(self.mandates)} mandates")
        print(f"  ✅ Generated {len(self.guidelines)} guidelines")
        print(f"  📂 Templates: {self.output_path}")
        print(f"  📂 Ready for Phase 2: {phase2_input}")
        print("\n📋 NEXT STEPS:")
        print(f"   1. Review files in: {self.output_path}")
        print("   2. Edit status fields for each rule (required/optional/custom)")
        print("   3. Run wizard Phase 3 to compile")

        return {
            'success': True,
            'mandate_count': len(self.mandates),
            'guideline_count': len(self.guidelines),
            'output_path': str(self.output_path),
            'mandates': [m.to_dict() for m in self.mandates],
            'guidelines': [g.to_dict() for g in self.guidelines]
        }


class Phase3Compiler:
    """Compile edited markdown templates to governance JSON with complete project structure"""

    def __init__(self, markdown_input_path: Path, output_path: Path, repo_root: Path, verbose: bool = False):
        """
        Args:
            markdown_input_path: Path to phase-2-input/ folder with edited markdown files
            output_path: Base output path (sdd-generated/final-output)
            repo_root: Root of sdd-architecture repo
            verbose: Print detailed logs
        """
        self.markdown_input_path = markdown_input_path
        self.output_path = output_path
        self.repo_root = repo_root
        self.verbose = verbose
        self.language = 'Python'  # default
        self.config = {}
        self.selected_guidelines = []  # Track which guidelines are selected (required/custom)

    def log(self, message: str):
        if self.verbose:
            print(f"  ℹ️  {message}")

    def load_wizard_config(self) -> bool:
        """Load wizard configuration to get selected language"""
        try:
            config_path = self.repo_root / 'sdd-generated' / 'wizard-config.json'
            if config_path.exists():
                with open(config_path, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
                    self.language = self.config.get('language', 'Python')
                    self.log(f"Loaded config: language={self.language}")
                    return True
            else:
                self.log(f"Config not found at {config_path}, using default language: Python")
                return True
        except Exception as e:
            print(f"  ❌ Error loading config: {e}")
            return False

    def create_sdd_structure(self) -> bool:
        """Create .sdd/source and .sdd/runtime directories"""
        try:
            sdd_dir = self.output_path / '.sdd'
            source_dir = sdd_dir / 'source'
            runtime_dir = sdd_dir / 'runtime'

            source_dir.mkdir(parents=True, exist_ok=True)
            runtime_dir.mkdir(parents=True, exist_ok=True)

            self.log(f"Created .sdd structure: {sdd_dir}")
            return True
        except Exception as e:
            print(f"  ❌ Error creating .sdd structure: {e}")
            return False

    def copy_language_templates(self) -> bool:
        """Copy language-specific templates to templates/, conditionally include CI/CD workflows"""
        try:
            templates_dir = self.repo_root / '_core' / '.sdd-wizard' / 'templates'
            language_lower = self.language.lower()

            # Map language names to template directory names
            language_dir_map = {
                'python': 'python',
                'java': 'java',
                'typescript': 'js',  # TypeScript/JavaScript use same templates in js/ folder
            }

            template_dir_name = language_dir_map.get(language_lower, language_lower)

            # Copy language-specific templates
            language_template_dir = templates_dir / 'languages' / template_dir_name
            if language_template_dir.exists():
                target_dir = self.output_path / 'templates'
                target_dir.mkdir(parents=True, exist_ok=True)

                import shutil
                for item in language_template_dir.rglob('*'):
                    if item.is_file():
                        rel_path = item.relative_to(language_template_dir)
                        target_file = target_dir / rel_path
                        target_file.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(item, target_file)

                self.log(f"Copied {language_lower} language templates to templates/")

            # Copy base templates, but selectively include .github/workflows
            base_template_dir = templates_dir / 'base'
            if base_template_dir.exists():
                target_dir = self.output_path / 'templates'
                target_dir.mkdir(parents=True, exist_ok=True)

                import shutil
                for item in base_template_dir.rglob('*'):
                    if item.is_file():
                        rel_path = item.relative_to(base_template_dir)

                        # Check if this is a workflow file
                        is_workflow_file = '.github' in rel_path.parts and 'workflows' in rel_path.parts

                        # Only copy workflow files if G151 is selected
                        if is_workflow_file and 'G151' not in self.selected_guidelines:
                            self.log(f"Skipping workflow template (G151 not selected): {rel_path}")
                            continue

                        target_file = target_dir / rel_path
                        target_file.parent.mkdir(parents=True, exist_ok=True)
                        # Don't overwrite language-specific templates
                        if not target_file.exists():
                            shutil.copy2(item, target_file)

                if 'G151' in self.selected_guidelines:
                    self.log("Copied base templates with CI/CD workflow (G151 selected)")
                else:
                    self.log("Copied base templates (workflow skipped - G151 not selected)")

            return True
        except Exception as e:
            print(f"  ❌ Error copying language templates: {e}")
            import traceback
            traceback.print_exc()
            return False

    def copy_seedlings(self) -> bool:
        """Copy seedling templates from .sdd-integration/templates to seedling/ directory"""
        try:
            # Look for seedling templates in .sdd-integration
            source_seedling_dir = self.repo_root / '_core' / '.sdd-integration' / 'templates'

            if not source_seedling_dir.exists():
                self.log(f"Seedling templates directory not found at {source_seedling_dir}, skipping")
                return True

            target_seedling_dir = self.output_path / 'seedling'
            target_seedling_dir.mkdir(parents=True, exist_ok=True)

            import shutil

            # Copy .ia, .github, .vscode, .cursor directories if they exist
            for seedling_type in ['.ia', '.github', '.vscode', '.cursor']:
                source_path = source_seedling_dir / seedling_type
                if source_path.exists():
                    target_path = target_seedling_dir / seedling_type
                    target_path.mkdir(parents=True, exist_ok=True)

                    for item in source_path.rglob('*'):
                        if item.is_file():
                            rel_path = item.relative_to(source_path)
                            target_file = target_path / rel_path
                            target_file.parent.mkdir(parents=True, exist_ok=True)
                            shutil.copy2(item, target_file)

            self.log("Copied seedling templates (.ia, .github, .vscode, .cursor) to final-output/seedling")
            return True
        except Exception as e:
            print(f"  ❌ Error copying seedlings: {e}")
            import traceback
            traceback.print_exc()
            return False

    def parse_markdown_status(self, content: str) -> str:
        """Extract status from markdown content"""
        # Match: **Status:** `required: true` or **Status:** `optional: true`
        match = re.search(r'\*\*Status:\*\*\s*`(required|optional|custom):\s*(?:true|false)`', content)
        if match:
            return match.group(1)
        return 'required'  # Default if not found

    def parse_markdown_items(self) -> Dict[str, List[Dict[str, Any]]]:
        """Parse edited markdown files from phase-2-input"""
        mandates = []
        guidelines = []

        try:
            # Find all .md files in phase-2-input
            md_files = list(self.markdown_input_path.glob('*.md'))

            if not md_files:
                print(f"  ❌ No markdown files found in {self.markdown_input_path}")
                return {'mandates': [], 'guidelines': []}

            for md_file in md_files:
                content = md_file.read_text(encoding='utf-8')

                # Parse items: ## ID: Title
                pattern = r'## ([GM]\d+):\s*(.+?)\n(.*?)(?=##|$)'
                for match in re.finditer(pattern, content, re.DOTALL):
                    item_id = match.group(1)
                    title = match.group(2).strip()
                    item_content = match.group(3)

                    # Get status
                    status = self.parse_markdown_status(item_content)

                    # Skip optional items
                    if status == 'optional':
                        self.log(f"Skipping optional item {item_id}")
                        continue

                    item = {
                        'id': item_id,
                        'title': title,
                        'status': status,
                        'type': 'HARD' if item_id.startswith('M') else 'SOFT'
                    }

                    if item_id.startswith('M'):
                        mandates.append(item)
                    else:
                        guidelines.append(item)
                        # Store guideline ID for conditional template generation
                        self.selected_guidelines.append(item_id)

                    self.log(f"Parsed {item_id}: {title} (status: {status})")

            return {'mandates': mandates, 'guidelines': guidelines}

        except Exception as e:
            print(f"  ❌ Error parsing markdown: {e}")
            return {'mandates': [], 'guidelines': []}

    def compile_with_pipeline_builder(self, items: Dict[str, List[Dict]]) -> bool:
        """Use existing pipeline_builder to compile governance to .sdd/source"""
        try:
            import sys
            builder_path = self.repo_root / '_core' / 'build_scripts'
            sys.path.insert(0, str(builder_path))
            from pipeline_builder import PipelineBuilder

            self.log("Importing PipelineBuilder...")

            spec_path = self.repo_root / '_spec'
            builder = PipelineBuilder(spec_path)
            self.log(f"Building with spec path: {spec_path}")

            result = builder.build()
            self.log("Build complete")

            # Create directories
            sdd_source = self.output_path / '.sdd' / 'source'
            sdd_source.mkdir(parents=True, exist_ok=True)

            # Write to .sdd/source/
            core_file = sdd_source / 'governance-core.json'
            client_file = sdd_source / 'governance-client.json'

            with open(core_file, 'w', encoding='utf-8') as f:
                json.dump(result['governance_core'], f, indent=2)
            self.log(f"Wrote {core_file}")

            with open(client_file, 'w', encoding='utf-8') as f:
                json.dump(result['governance_client'], f, indent=2)
            self.log(f"Wrote {client_file}")

            return True
        except Exception as e:
            print(f"  ❌ Pipeline builder error: {e}")
            import traceback
            traceback.print_exc()
            return False

    def load_compiled_governance(self) -> Tuple[List[Dict], List[Dict]]:
        """Load mandates and guidelines from compiled governance JSONs"""
        try:
            source_dir = self.output_path / '.sdd' / 'source'
            core_file = source_dir / 'governance-core.json'
            client_file = source_dir / 'governance-client.json'

            mandates = []
            guidelines = []

            # Load mandates from governance-core.json
            if core_file.exists():
                with open(core_file, 'r', encoding='utf-8') as f:
                    governance_core = json.load(f)

                for item in governance_core.get('items', []):
                    if item['type'] == 'MANDATE':
                        mandates.append(item)

            # Load guidelines from governance-client.json
            if client_file.exists():
                with open(client_file, 'r', encoding='utf-8') as f:
                    governance_client = json.load(f)

                for item in governance_client.get('items', []):
                    if item['type'] == 'GUIDELINE':
                        guidelines.append(item)

            self.log(f"Loaded {len(mandates)} mandates and {len(guidelines)} guidelines")
            return mandates, guidelines
        except Exception as e:
            print(f"  ❌ Error loading compiled governance: {e}")
            import traceback
            traceback.print_exc()
            return [], []

    def generate_mandates_file(self, mandates: List[Dict]) -> bool:
        """Generate mandates.md with IA-FIRST optimization"""
        try:
            mandates_dir = self.output_path / '.sdd' / 'source' / 'mandates'
            mandates_dir.mkdir(parents=True, exist_ok=True)

            mandates_file = mandates_dir / 'mandates.md'

            content = f"""# Mandates - SDD v3.0

⚡ IA-FIRST DESIGN NOTICE
- **Status**: Architecture-level governance rules
- **Optimization**: Optimized for AI agent parsing
- **Version**: 3.0
- **Language**: {self.language}
- **Generated**: {datetime.now().isoformat()}

## Core Mandates

Mandatory rules that CANNOT be customized or skipped.

"""

            for mandate in mandates:
                content += f"""## {mandate['id']}: {mandate['title']}

**Criticality**: {mandate.get('criticality', 'MANDATORY')}
**Customizable**: No

{mandate.get('description', mandate.get('content', 'No description available'))}

"""

            with open(mandates_file, 'w', encoding='utf-8') as f:
                f.write(content)

            self.log(f"Generated mandates.md ({len(mandates)} mandates)")
            return True
        except Exception as e:
            print(f"  ❌ Error generating mandates.md: {e}")
            import traceback
            traceback.print_exc()
            return False

    def generate_guidelines_files(self, guidelines: List[Dict]) -> bool:
        """Generate guidelines organized by category"""
        try:
            guidelines_dir = self.output_path / '.sdd' / 'source' / 'guidelines'
            guidelines_dir.mkdir(parents=True, exist_ok=True)

            # Organize by category
            by_category = {}
            for guideline in guidelines:
                cat = guideline.get('category', 'general')
                if cat not in by_category:
                    by_category[cat] = []
                by_category[cat].append(guideline)

            # Generate file for each category
            for category, items in sorted(by_category.items()):
                filename = category.lower().replace(' ', '-')
                filepath = guidelines_dir / f'{filename}.md'

                content = f"""# {category.title()} Guidelines

⚡ IA-FIRST DESIGN NOTICE
- **Status**: Customizable best practices
- **Optimization**: Optimized for AI agent parsing
- **Category**: {category.title()}
- **Count**: {len(items)} guidelines
- **Generated**: {datetime.now().isoformat()}

## Overview

Guidelines in this category provide structured recommendations for {category.lower()}.

"""

                for guideline in items:
                    content += f"""## {guideline['id']}: {guideline['title']}

**Type**: {guideline.get('type', 'GUIDELINE')}
**Status**: {guideline.get('status', 'required')}
**Customizable**: {'Yes' if guideline.get('customizable', True) else 'No'}

{guideline.get('description', guideline.get('content', 'No description available'))}

"""

                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)

                self.log(f"Generated {filename}.md ({len(items)} guidelines)")

            return True
        except Exception as e:
            print(f"  ❌ Error generating guidelines files: {e}")
            import traceback
            traceback.print_exc()
            return False

    def generate_source_readme(self, mandates: List[Dict], guidelines: List[Dict]) -> bool:
        """Generate README.md with agent instructions for .sdd/source"""
        try:
            source_dir = self.output_path / '.sdd' / 'source'
            readme_file = source_dir / 'README.md'

            # Get categories from guidelines
            categories = sorted(set(g.get('category', 'general') for g in guidelines))
            if not categories:
                categories = ['general']
            categories_list = '\n'.join(f'- {cat.title()}' for cat in categories)

            # Build guidelines file references
            guidelines_refs = '\n'.join(f'- {cat.lower()}.md' for cat in categories)

            content = f"""# .sdd/source - Governance Source of Truth

⚡ **For AI Agents: This is your primary query directory**

## Overview

This directory contains the **compiled and optimized** governance specifications that agents should reference.

**Generated**: {datetime.now().isoformat()}
**Language**: {self.language}

## Directory Structure

```
.sdd/source/
├── mandates/
│   └── mandates.md              ← Read mandates first (hard rules)
├── guidelines/
│   ├── {categories[0]}.md
│   ├── {categories[1] if len(categories) > 1 else 'other'}.md
│   └── (organized by category)
└── README.md                    ← This file
```

## For AI Agents: How to Use This

### 1. Query Mandates First

Always read `.sdd/source/mandates/mandates.md` to understand **hard rules** that CANNOT be customized.

```bash
cat .sdd/source/mandates/mandates.md
```

### 2. Query Relevant Guidelines

Based on the task, read relevant guidelines:

```bash
# For category-related work
cat .sdd/source/guidelines/category.md
```

### 3. Use As Pre-Cache Context

These files are **optimized for AI parsing** (IA-FIRST format):
- Flat hierarchy (H2 sections, no skipped levels)
- Clear lists instead of prose
- Emoji markers for decisions
- Markdown links only
- No nested HTML or complex formatting

This reduces token usage when including in agent context.

### 4. Reference in Agent Prompts

Example agent prompt structure:

```
You are a development assistant following SDD (Specification-Driven Development).

MANDATES (Hard Rules):
<read from .sdd/source/mandates/mandates.md>

GUIDELINES (Best Practices):
<read from .sdd/source/guidelines/{{relevant-category}}.md>

TASK:
<your specific task>
```

## Pre-Cache Strategy

For optimal performance when using these with agents:

1. **Load once**: Read governance files once per session
2. **Cache in memory**: Store in agent context/memory
3. **Reference later**: Use markdown file references instead of re-reading
4. **Update on changes**: Re-read if .sdd/source files change

## File Organization

### Mandates (Non-customizable)
- Location: `.sdd/source/mandates/mandates.md`
- Count: {len(mandates)}
- Rule: **MUST** be followed (no exceptions)

### Guidelines (Customizable)
- Location: `.sdd/source/guidelines/`
- Count: {len(guidelines)}
- Rule: Should be followed (exceptions allowed with documentation)

### Categories Covered

{categories_list}

## Next Steps

1. **Read Mandates**: Start with `.sdd/source/mandates/mandates.md`
2. **Browse Guidelines**: Review `.sdd/source/guidelines/` for your domain
3. **Use in Tasks**: Reference these when making decisions
4. **Cache Strategically**: Load once, reuse across multiple agent calls

---

**Generated by SDD Wizard v3.0**
"""

            with open(readme_file, 'w', encoding='utf-8') as f:
                f.write(content)

            self.log("Generated .sdd/source/README.md")
            return True
        except Exception as e:
            print(f"  ❌ Error generating source README: {e}")
            import traceback
            traceback.print_exc()
            return False
        """Use existing pipeline_builder to compile governance to .sdd/source"""
        try:
            import sys
            builder_path = self.repo_root / '_core' / 'build_scripts'
            sys.path.insert(0, str(builder_path))
            from pipeline_builder import PipelineBuilder

            self.log("Importing PipelineBuilder...")

            spec_path = self.repo_root / '_spec'
            builder = PipelineBuilder(spec_path)
            self.log(f"Building with spec path: {spec_path}")

            result = builder.build()
            self.log("Build complete")

            # Create directories
            sdd_source = self.output_path / '.sdd' / 'source'
            sdd_source.mkdir(parents=True, exist_ok=True)

            # Write to .sdd/source/
            core_file = sdd_source / 'governance-core.json'
            client_file = sdd_source / 'governance-client.json'

            with open(core_file, 'w', encoding='utf-8') as f:
                json.dump(result['governance_core'], f, indent=2)
            self.log(f"Wrote {core_file}")

            with open(client_file, 'w', encoding='utf-8') as f:
                json.dump(result['governance_client'], f, indent=2)
            self.log(f"Wrote {client_file}")

            return True
        except Exception as e:
            print(f"  ❌ Pipeline builder error: {e}")
            import traceback
            traceback.print_exc()
            return False

    def run(self) -> Dict[str, Any]:
        """Execute Phase 3: Read edited markdown and compile with complete structure"""
        print("\n⚙️  PHASE 3: Compile Governance from Edited Templates")
        print("=" * 70)
        print(f"  📂 Reading from: {self.markdown_input_path}")

        # Load configuration
        if not self.load_wizard_config():
            return {'success': False, 'error': 'Failed to load config'}

        # Create .sdd structure
        if not self.create_sdd_structure():
            return {'success': False, 'error': 'Failed to create .sdd structure'}

        # Parse edited markdown files
        items = self.parse_markdown_items()
        mandates_count = len(items['mandates'])
        guidelines_count = len(items['guidelines'])

        print(f"  ✅ Parsed {mandates_count} mandates, {guidelines_count} guidelines")
        print("  ℹ️  (Skipped optional items)")

        # Compile with PipelineBuilder
        if not self.compile_with_pipeline_builder(items):
            return {'success': False, 'error': 'Failed to compile'}

        # Copy language-specific templates
        if not self.copy_language_templates():
            return {'success': False, 'error': 'Failed to copy language templates'}

        # Copy seedlings
        if not self.copy_seedlings():
            return {'success': False, 'error': 'Failed to copy seedlings'}

        # Generate AI-optimized files (.sdd/source/mandates/, guidelines/, README.md)
        mandates, guidelines = self.load_compiled_governance()

        if mandates or guidelines:
            if not self.generate_mandates_file(mandates):
                return {'success': False, 'error': 'Failed to generate mandates.md'}

            if not self.generate_guidelines_files(guidelines):
                return {'success': False, 'error': 'Failed to generate guidelines files'}

            if not self.generate_source_readme(mandates, guidelines):
                return {'success': False, 'error': 'Failed to generate source README'}

        print("  ✅ Compiled governance artifacts")
        print("  ✅ Generated complete .sdd structure")
        print(f"  📂 Output: {self.output_path}")

        return {
            'success': True,
            'output_path': str(self.output_path),
            'language': self.language,
            'files': ['governance-core.json', 'governance-client.json', 'templates/', 'seedling/', 'mandates.md', 'guidelines/'],
            'mandates': len(mandates),
            'guidelines': len(guidelines)
        }
