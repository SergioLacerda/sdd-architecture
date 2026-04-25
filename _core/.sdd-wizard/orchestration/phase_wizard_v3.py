#!/usr/bin/env python3
"""
SDD Wizard v3 - 3-Phase Flow with Multiple Status-aware Files

Phase 1: Generate markdown templates with status fields
  Input: mandate.spec, guidelines.dsl
  Output: /sdd-generated/phase-1-choices/ (Multiple .md files by category)
  
Phase 2: Manual user marking of templates  
  Action: User edits markdown files, changes status values
  Output: /sdd-generated/phase-3-input/ (User creates YAML from marked files)
  
Phase 3: Compile marked templates with fingerprints
  Input: /sdd-generated/phase-3-input/ (User-created YAML)
  Output: /sdd-generated/phase-4-output/ (JSON with fingerprints)
"""

import json
import re
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime

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
    
    def __init__(self, sdd_core_path: Path, output_path: Path, verbose: bool = False):
        self.sdd_core_path = sdd_core_path
        self.output_path = output_path
        self.verbose = verbose
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
                        f.write(f"**Status:** `required: true` (Default: mandatory)\n\n")
                        f.write(f"**Customizable:** `false` (Hard rules cannot be modified)\n\n")
                        f.write(f"**Optional:** `false` (Not negotiable)\n\n")
                        
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
                        f.write(f"**Status:** `required: true` (Default: include)\n\n")
                        f.write(f"**Customizable:** `true` (Change below if needed)\n\n")
                        f.write(f"**Optional:** `false` (Included by default)\n\n")
                        
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
        
        print(f"  ✅ Generated {len(self.mandates)} mandates")
        print(f"  ✅ Generated {len(self.guidelines)} guidelines")
        print(f"  📂 Output: {self.output_path}")
        print(f"\n📋 NEXT STEPS:")
        print(f"   1. Review files in: {self.output_path}")
        print(f"   2. Edit status fields for each rule (required/optional/custom)")
        print(f"   3. Run wizard Phase 3 to compile")
        
        return {
            'success': True,
            'mandate_count': len(self.mandates),
            'guideline_count': len(self.guidelines),
            'output_path': str(self.output_path),
            'mandates': [m.to_dict() for m in self.mandates],
            'guidelines': [g.to_dict() for g in self.guidelines]
        }


class Phase3Compiler:
    """Compile edited markdown templates to governance JSON"""
    
    def __init__(self, markdown_input_path: Path, output_path: Path, repo_root: Path, verbose: bool = False):
        """
        Args:
            markdown_input_path: Path to phase-1-choices/ folder with edited markdown files
            output_path: Where to write governance JSON
            repo_root: Root of sdd-architecture repo
            verbose: Print detailed logs
        """
        self.markdown_input_path = markdown_input_path
        self.output_path = output_path
        self.repo_root = repo_root
        self.verbose = verbose
    
    def log(self, message: str):
        if self.verbose:
            print(f"  ℹ️  {message}")
    
    def parse_markdown_status(self, content: str) -> str:
        """Extract status from markdown content"""
        # Match: **Status:** `required: true` or **Status:** `optional: true`
        match = re.search(r'\*\*Status:\*\*\s*`(required|optional|custom):\s*(?:true|false)`', content)
        if match:
            return match.group(1)
        return 'required'  # Default if not found
    
    def parse_markdown_items(self) -> Dict[str, List[Dict[str, Any]]]:
        """Parse edited markdown files from phase-1-choices"""
        mandates = []
        guidelines = []
        
        try:
            # Find all .md files in phase-1-choices
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
                    
                    self.log(f"Parsed {item_id}: {title} (status: {status})")
            
            return {'mandates': mandates, 'guidelines': guidelines}
        
        except Exception as e:
            print(f"  ❌ Error parsing markdown: {e}")
            return {'mandates': [], 'guidelines': []}
    
    def compile_with_pipeline_builder(self, items: Dict[str, List[Dict]]) -> bool:
        """Use existing pipeline_builder to compile"""
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
            
            self.output_path.mkdir(parents=True, exist_ok=True)
            
            core_file = self.output_path / 'governance-core.json'
            client_file = self.output_path / 'governance-client.json'
            
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
        """Execute Phase 3: Read edited markdown and compile"""
        print("\n⚙️  PHASE 3: Compile Governance from Edited Templates")
        print("=" * 70)
        print(f"  📂 Reading from: {self.markdown_input_path}")
        
        # Parse edited markdown files
        items = self.parse_markdown_items()
        mandates_count = len(items['mandates'])
        guidelines_count = len(items['guidelines'])
        
        print(f"  ✅ Parsed {mandates_count} mandates, {guidelines_count} guidelines")
        print(f"  ℹ️  (Skipped optional items)")
        
        # Compile with PipelineBuilder
        if not self.compile_with_pipeline_builder(items):
            return {'success': False, 'error': 'Failed to compile'}
        
        print(f"  ✅ Compiled governance artifacts")
        print(f"  📂 Output: {self.output_path}")
        
        return {
            'success': True,
            'output_path': str(self.output_path),
            'files': ['governance-core.json', 'governance-client.json'],
            'mandates': mandates_count,
            'guidelines': guidelines_count
        }
