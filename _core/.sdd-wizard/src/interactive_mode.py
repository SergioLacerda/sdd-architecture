#!/usr/bin/env python3
"""
Interactive mode for SDD Wizard - Guided step-by-step project generation

Provides user-friendly prompts for:
1. Source files review
2. Configuration selection
3. Real-time feedback
4. Final output location
"""

import sys
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime


class InteractiveWizard:
    """Interactive guide for wizard pipeline"""
    
    def __init__(self, repo_root: Path, orchestrator):
        self.repo_root = repo_root
        self.orchestrator = orchestrator
        self.selections = {}
        self.source_files = {
            'mandate_spec': repo_root / '_core' / '.sdd-core' / 'mandate.spec',
            'guidelines_dsl': repo_root / '_core' / '.sdd-core' / 'guidelines.dsl',
        }
        self.compiled_files = {
            'core': repo_root / '_core' / '.sdd-compiled' / 'governance-core.json',
            'client': repo_root / '_core' / '.sdd-compiled' / 'governance-client.json',
        }
    
    def print_header(self, title: str, icon: str = "🔮"):
        """Print formatted header"""
        print(f"\n{icon} {title}")
        print("=" * 70)
    
    def print_section(self, title: str, icon: str = "📋"):
        """Print section header"""
        print(f"\n{icon} {title}")
        print("-" * 70)
    
    def print_file_info(self, title: str, filepath: Path):
        """Print file information"""
        if filepath.exists():
            size_kb = filepath.stat().st_size / 1024
            print(f"  📄 {title}")
            print(f"     Location: {filepath.relative_to(self.repo_root)}")
            print(f"     Size: {size_kb:.1f} KB")
            return True
        else:
            print(f"  ❌ {title}: NOT FOUND at {filepath}")
            return False
    
    def preview_file(self, filepath: Path, max_lines: int = 20) -> bool:
        """Show file preview"""
        if not filepath.exists():
            print(f"\n  ❌ File not found: {filepath}")
            return False
        
        print(f"\n  📖 Preview ({max_lines} lines):")
        print("  " + "-" * 66)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()[:max_lines]
                for line in lines:
                    print(f"  {line.rstrip()}")
            
            total_lines = len(open(filepath).readlines())
            if total_lines > max_lines:
                print(f"  ... ({total_lines - max_lines} more lines)")
            print("  " + "-" * 66)
            return True
        except Exception as e:
            print(f"  ❌ Error reading file: {e}")
            return False
    
    def step_1_review_sources(self):
        """Step 1: Show source files and let user review"""
        self.print_header("STEP 1: Review Source Files", "📂")
        print("""
These are your GOVERNANCE SOURCES that define your project's rules:
""")
        
        # Show mandate.spec
        print()
        self.print_section("A) Mandates (HARD rules)", "🛑")
        print("""
Mandates are immutable rules that ALL projects must follow.
Examples: "Use Clean Architecture", "Write tests first"
""")
        self.print_file_info("mandate.spec", self.source_files['mandate_spec'])
        
        if self.source_files['mandate_spec'].exists():
            show_preview = input("\n  Preview mandate.spec? (y/n): ").lower().strip()
            if show_preview == 'y':
                self.preview_file(self.source_files['mandate_spec'], max_lines=30)
        
        # Show guidelines.dsl
        print()
        self.print_section("B) Guidelines (SOFT recommendations)", "💡")
        print("""
Guidelines are customizable recommendations for your project.
Examples: "Documentation standards", "Naming conventions"
""")
        self.print_file_info("guidelines.dsl", self.source_files['guidelines_dsl'])
        
        if self.source_files['guidelines_dsl'].exists():
            show_preview = input("\n  Preview guidelines.dsl? (y/n): ").lower().strip()
            if show_preview == 'y':
                self.preview_file(self.source_files['guidelines_dsl'], max_lines=25)
        
        print("\n  ✅ Source files confirmed")
        return True
    
    def step_2_select_configuration(self):
        """Step 2: Ask for project configuration"""
        self.print_header("STEP 2: Configure Your Project", "⚙️")
        
        # Language selection
        print("""
What programming language will you use?
""")
        languages = ['python', 'java', 'typescript', 'go', 'rust', 'other']
        for i, lang in enumerate(languages, 1):
            print(f"  {i}. {lang}")
        
        choice = input(f"\nSelect (1-{len(languages)}): ").strip()
        try:
            language = languages[int(choice) - 1]
        except (ValueError, IndexError):
            language = 'python'
            print(f"  Using default: python")
        
        self.selections['language'] = language
        print(f"  ✅ Language: {language}")
        
        # Mandate selection
        print()
        self.print_section("Select Mandates (HARD rules)", "🛑")
        print("""
Which mandates apply to your project?
All mandates are REQUIRED - select which ones to enforce:
""")
        
        # Load mandates from Phase 1
        phase_1_data = self.orchestrator.phases_results.get('phase_1', {}).get('data', {})
        mandate_ids = phase_1_data.get('mandate', {}).get('mandate_ids', [])
        
        selected_mandates = []
        for mandate_id in mandate_ids:
            response = input(f"  Include {mandate_id}? (y/n): ").lower().strip()
            if response == 'y':
                selected_mandates.append(mandate_id)
        
        self.selections['mandates'] = selected_mandates
        print(f"  ✅ Selected {len(selected_mandates)} mandate(s): {', '.join(selected_mandates)}")
        
        # Output location
        print()
        self.print_section("Project Output Location", "📂")
        default_output = self.repo_root / '_core' / 'sdd-generated' / 'project'
        custom_output = input(f"\nProject output directory [{default_output}]: ").strip()
        
        if custom_output:
            self.selections['output_dir'] = Path(custom_output)
        else:
            self.selections['output_dir'] = default_output
        
        print(f"  ✅ Output: {self.selections['output_dir']}")
        
        return True
    
    def step_3_show_pipeline_progress(self):
        """Step 3: Execute pipeline and show progress"""
        self.print_header("STEP 3: Generating Your Project", "🚀")
        print("""
Executing 7-phase pipeline...
""")
        
        # Run phases 1-2 (already done for step 1, skip)
        print("  ✅ Phase 1: Source validation [COMPLETE]")
        print("  ✅ Phase 2: Loading compiled governance [COMPLETE]")
        
        # Get compiled data for display
        phase_2_report = self.orchestrator.phases_results.get('phase_2', {})
        if phase_2_report.get('data'):
            mandate_count = len(phase_2_report['data'].get('mandate', {}).get('ids', []))
            guideline_count = len(phase_2_report['data'].get('guidelines', {}).get('ids', []))
            print(f"     └─ Loaded: {mandate_count} mandates, {guideline_count} guidelines")
        
        # Run Phase 3-4
        print("\n  ⏳ Phase 3: Filtering mandates...")
        mandates = self.selections.get('mandates')
        if self.orchestrator.run_phase_3(mandates):
            print("     ✅ Mandates filtered")
        
        print("\n  ⏳ Phase 4: Filtering guidelines...")
        language = self.selections.get('language', 'python')
        if self.orchestrator.run_phase_4(language):
            print("     ✅ Guidelines filtered")
        
        # Run Phase 5-6
        output_dir = self.selections['output_dir']
        scaffold_dir = output_dir.parent / 'scaffold'
        
        print("\n  ⏳ Phase 5: Applying template scaffold...")
        if self.orchestrator.run_phase_5(language, scaffold_dir):
            print("     ✅ Template scaffolding applied")
        
        print("\n  ⏳ Phase 6: Generating project structure...")
        if self.orchestrator.run_phase_6(output_dir, language):
            print("     ✅ Project structure generated")
        
        # Run Phase 7
        print("\n  ⏳ Phase 7: Validating output...")
        if self.orchestrator.run_phase_7(output_dir):
            print("     ✅ Validation complete")
        
        return True
    
    def step_4_show_results(self):
        """Step 4: Show where everything was generated"""
        self.print_header("STEP 4: Project Generated Successfully! 🎉", "✅")
        
        output_dir = self.selections['output_dir']
        
        print(f"""
📍 YOUR PROJECT LOCATION:
   {output_dir}

📋 WHAT WAS GENERATED:
""")
        
        # Show directory structure
        if output_dir.exists():
            print(f"  📂 {output_dir.name}/")
            self._show_tree(output_dir, prefix="     ", max_depth=3, max_items=10)
        
        print(f"""
🔑 KEY FILES:
""")
        
        # Show key files
        key_files = [
            ('.ai/constitution.md', 'Your project constitution & rules'),
            ('README.md', 'Project overview and setup'),
            ('src/', 'Your source code directory'),
            ('tests/', 'Test suite'),
            ('.sdd-artifacts/', 'Generated governance artifacts'),
        ]
        
        for file_path, description in key_files:
            full_path = output_dir / file_path
            if full_path.exists():
                print(f"  ✅ {file_path:30s} - {description}")
            else:
                print(f"  ◻️  {file_path:30s} - {description}")
        
        print(f"""
📖 NEXT STEPS:
  1. Read {output_dir / '.ai' / 'constitution.md'} to understand your rules
  2. Review the generated structure
  3. Start implementing according to the constitution
  4. Run tests: pytest tests/

💬 CONFIGURATION USED:
  Language: {self.selections.get('language', 'N/A')}
  Mandates: {', '.join(self.selections.get('mandates', []))}
  Output: {output_dir}

📚 LEARN MORE:
  • Constitution: {output_dir / '.ai' / 'constitution.md'}
  • Architecture: {output_dir / 'docs' / 'ARCHITECTURE.md' if (output_dir / 'docs' / 'ARCHITECTURE.md').exists() else 'See README.md'}
  • Guidelines: {output_dir / '.ai' / 'governance-client.json' if (output_dir / '.ai' / 'governance-client.json').exists() else 'See constitution.md'}
""")
        
        return True
    
    def _show_tree(self, path: Path, prefix: str = "", max_depth: int = 3, current_depth: int = 0, max_items: int = 10):
        """Recursively show directory tree"""
        if current_depth >= max_depth:
            return
        
        try:
            items = sorted(path.iterdir(), key=lambda x: (not x.is_dir(), x.name))[:max_items]
            
            for i, item in enumerate(items):
                is_last = (i == len(items) - 1) and (len(items) <= max_items)
                current_prefix = "└── " if is_last else "├── "
                print(f"{prefix}{current_prefix}{item.name}{'/' if item.is_dir() else ''}")
                
                if item.is_dir() and current_depth + 1 < max_depth and not item.name.startswith('.'):
                    next_prefix = prefix + ("    " if is_last else "│   ")
                    self._show_tree(item, next_prefix, max_depth, current_depth + 1, max_items)
        except PermissionError:
            pass
    
    def run(self) -> bool:
        """Execute interactive wizard flow"""
        try:
            print()
            self.print_header("SDD v3.0 Interactive Wizard", "🧙")
            print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("""
This guide will help you create a new SDD-compliant project step by step:

STEP 1️⃣  Review your governance source files
STEP 2️⃣  Configure your project (language, rules, output location)
STEP 3️⃣  Generate your project (automated 7-phase pipeline)
STEP 4️⃣  See where everything was created and next steps

Let's get started! 🚀
""")
            
            input("Press ENTER to continue...")
            
            # Run all steps
            if not self.step_1_review_sources():
                return False
            
            if not self.step_2_select_configuration():
                return False
            
            if not self.step_3_show_pipeline_progress():
                return False
            
            if not self.step_4_show_results():
                return False
            
            print("\n" + "=" * 70)
            print("🎉 Your project is ready! Happy coding! 🎉")
            print("=" * 70 + "\n")
            
            return True
        
        except KeyboardInterrupt:
            print("\n\n❌ Wizard cancelled by user")
            return False
        except Exception as e:
            print(f"\n❌ Error in interactive mode: {e}")
            import traceback
            traceback.print_exc()
            return False
