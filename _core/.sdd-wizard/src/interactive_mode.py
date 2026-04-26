#!/usr/bin/env python3
"""
Interactive mode for SDD Wizard v3 - Phase-based template generation

4-phase flow:
1. Phase 1: Generate markdown templates (asks: language, adoption_level)
2. Phase 2: Manual user customization (instructions only)
3. Phase 3: Compile templates
4. Phase 4: Generate project structure
"""

import sys
import json
from pathlib import Path
from datetime import datetime


class InteractiveWizard:
    """Interactive guide for SDD Wizard v3"""
    
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.config = {}
    
    def print_header(self, title: str, icon: str = "🧙"):
        """Print formatted header"""
        print(f"\n{icon} {title}")
        print("=" * 70)
    
    def show_phase_menu(self) -> str:
        """Show menu to choose which phase to start at"""
        self.print_header("SDD Wizard v3 - Choose Starting Phase", "🧙")
        print(f"\nStarted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        print("""Which phase would you like to run?

  [1] Phase 1: Generate governance templates
              (Asks for programming language)
              ✅ Start here or use to reset/regenerate

  [2] Phase 2: How to customize templates
              (Shows step-by-step instructions)
              ✅ Use this for guidance on editing

  [3] Phase 3: Compile governance
              (Reads edited markdown → final JSON)
              ✅ Use after editing Phase 1 output
""")
        
        choice = input("Select phase (1-3): ").strip()
        return choice
    
    def ask_user_preferences(self) -> dict:
        """Ask user for preferences: programming language"""
        self.print_header("User Preferences Setup", "⚙️")
        
        # Ask for language
        print("""\n1️⃣  Which language would you like examples in?
(This is for code examples only - governance applies to all languages)

  [1] Python
  [2] Java
  [3] TypeScript
""")
        language_choice = input("Select language (1-3): ").strip()
        language_map = {'1': 'Python', '2': 'Java', '3': 'TypeScript'}
        language = language_map.get(language_choice, 'Python')
        print(f"   ✅ Selected: {language}")
        
        # Default adoption level (FULL)
        adoption_level = 'FULL'
        
        config = {
            'language': language,
            'adoption_level': adoption_level,
            'generated_at': datetime.now().isoformat()
        }
        
        return config
    
    def save_config(self, config: dict) -> Path:
        """Save configuration to wizard-config.json"""
        repo_root = self.repo_root
        if repo_root.name == '_core':
            repo_root = repo_root.parent
        
        config_dir = repo_root / '_core' / 'sdd-generated'
        config_dir.mkdir(parents=True, exist_ok=True)
        
        config_path = config_dir / 'wizard-config.json'
        
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        return config_path
    
    def phase_1_generate_templates(self) -> bool:
        """Execute Phase 1: Generate templates with user preferences"""
        self.print_header("PHASE 1: Generate Governance Templates", "📝")
        
        try:
            from orchestration.phase_wizard_v3 import Phase1Generator
            
            # Collect user preferences
            config = self.ask_user_preferences()
            self.config = config
            
            # Save config
            config_path = self.save_config(config)
            print(f"\n✅ Configuration saved to: {config_path}")
            
            # Adjust repo_root if we're inside _core (wizard.sh changes to _core)
            repo_root = self.repo_root
            if repo_root.name == '_core':
                repo_root = repo_root.parent
            
            sdd_core_path = repo_root / '_core'
            output_path = repo_root / 'sdd-generated' / 'phase-1-choices'
            
            generator = Phase1Generator(sdd_core_path, output_path, verbose=True, config=config)
            result = generator.run()
            
            if result['success']:
                print(f"""
✅ Phase 1 Complete!

📝 Templates generated: {output_path}
   Language: {config.get('language')}
   Adoption: {config.get('adoption_level')}

Next steps:
1. Review markdown files in phase-1-choices/
2. Edit status fields (required/optional/custom)
3. Run Phase 2 for step-by-step instructions
4. Run Phase 3 to compile
""")
            
            return result['success']
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def phase_2_show_instructions(self) -> bool:
        """Show Phase 2 instructions - Two manual review steps"""
        self.print_header("PHASE 2: Review & Customize Governance", "📋")
        
        # Adjust repo_root if we're inside _core
        repo_root = self.repo_root
        if repo_root.name == '_core':
            repo_root = repo_root.parent
        
        phase1_path = repo_root / 'sdd-generated' / 'phase-1-choices'
        output_path = repo_root / 'sdd-generated' / 'phase-2-input'
        
        print(f"""
═══════════════════════════════════════════════════════════════════
PHASE 2: TWO MANUAL REVIEW STEPS
═══════════════════════════════════════════════════════════════════

📂 LOCATION OF YOUR TEMPLATES:
   {phase1_path}

📌 GOVERNANCE STRUCTURE:
   • Mandates (M001, M002): Immutable core rules → ALWAYS REQUIRED
   • Guidelines (G01-G150): Customizable soft rules → YOU DECIDE

═══════════════════════════════════════════════════════════════════
STEP 1: REVIEW & CLASSIFY EACH CRITERION
═══════════════════════════════════════════════════════════════════

FILE ORGANIZATION (by category):
  ├─ mandates-*.md          (Hard rules - cannot be changed)
  └─ guidelines-*.md        (Soft rules - you decide status)

FOR EACH GUIDELINE, SET ITS STATUS:

  [A] REQUIRED (Default)
      → Mandatory in your project
      → Status: `required: true`
      → Example: Core security checks, mandatory testing

  [B] CUSTOMIZABLE
      → Optional but can be customized to fit your needs
      → Status: `custom: true`
      → Example: Code style preferences, flexibility allowed

  [C] OPTIONAL
      → Skip entirely - not relevant to your project
      → Status: `optional: true`
      → Example: Guidelines for unused frameworks, irrelevant rules

EDITING INSTRUCTIONS:
  1. Open each markdown file
  2. Find the **Status:** field (each rule has one)
  3. Change the value:
     FROM: **Status:** `required: true` (default)
     TO:   **Status:** `custom: true` OR `optional: true`
  4. Save file (no YAML conversion needed)

═══════════════════════════════════════════════════════════════════
STEP 2: SAVE REVIEWED FILES TO OUTPUT DIRECTORY
═══════════════════════════════════════════════════════════════════

OUTPUT LOCATION:
  {output_path}

ACTION:
  Copy all your REVIEWED & EDITED markdown files from:
    {phase1_path}
  Into:
    {output_path}

FILES TO COPY:
  ✓ mandates-*.md (even if unchanged)
  ✓ guidelines-*.md (with your status changes)
  ✓ README.md (for reference)

═══════════════════════════════════════════════════════════════════
AFTER PHASE 2: RUN PHASE 3
═══════════════════════════════════════════════════════════════════

Phase 3 will:
  1. Read your reviewed markdown files from phase-2-input
  2. Parse all Status fields (required/custom/optional)
  3. Skip items marked as optional
  4. Compile into final governance JSON

═══════════════════════════════════════════════════════════════════

ℹ️  KEY POINTS FOR AI UNDERSTANDING:
   - Governance has 2 immutable mandates (M001, M002)
   - 150 customizable guidelines (G01-G150) with user-selectable status
   - Status field enables filtering: required/custom/optional
   - Phase 2 is purely manual review (no automation)
   - Phase 3 automates compilation of reviewed decisions

""")
        
        input("\nPress ENTER when you've completed Phase 2...")
        return True
    
    def phase_4_generate_project(self) -> bool:
        """Execute Phase 4-6: Generate project structure from compiled governance"""
        self.print_header("PHASE 4-6: Generate Project Structure", "🏗️")
        
        try:
            from orchestration.phase_4_5_6_generator import run_phase_4_5_6_generator
            
            # Adjust repo_root if we're inside _core
            repo_root = self.repo_root
            if repo_root.name == '_core':
                repo_root = repo_root.parent
            
            # Load config from wizard-config.json
            config_path = repo_root / '_core' / 'sdd-generated' / 'wizard-config.json'
            
            if not config_path.exists():
                print(f"\n❌ Configuration not found!")
                print("You must run Phase 1 first to set preferences.")
                return False
            
            with open(config_path, 'r') as f:
                config = json.load(f)
            
            # Check if Phase 3 completed
            phase3_output = repo_root / 'sdd-generated' / 'final-output'
            if not phase3_output.exists():
                print(f"\n❌ Phase 3 output not found!")
                print("You must run Phase 3 first to compile governance.")
                return False
            
            # Output base is the project root where .sdd/ will be created
            # For now, use sdd-generated directory as the output base
            output_base = repo_root / 'sdd-generated'
            
            # Run Phase 4-6 generator
            result = run_phase_4_5_6_generator(repo_root, output_base, config)
            
            if result['success']:
                print(f"""
✅ Phase 4-6 Complete!

📊 Output Summary:
   Mandates: {result['mandates']}
   Guidelines: {result['guidelines']}
   Categories: {', '.join(result['categories'])}
   
📂 Location: {result['output_path']}

🎯 Next Steps:
   1. Review .sdd/source/ for governance organization
   2. Review .sdd/runtime/README.md for agent pre-cache instructions
   3. Configure seedlings (.vscode, .cursor, .ia)
   4. Commit to version control
""")
                return True
            else:
                print(f"\n❌ Phase 4-6 generation failed!")
                for error in result.get('errors', []):
                    print(f"   • {error}")
                return False
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def phase_3_compile_templates(self) -> bool:
        """Execute Phase 3: Compile edited templates to governance JSON"""
        self.print_header("PHASE 3: Compile Governance", "⚙️")
        
        # Adjust repo_root if we're inside _core
        repo_root = self.repo_root
        if repo_root.name == '_core':
            repo_root = repo_root.parent
        
        # Phase 3 reads edited markdown from phase-2-input
        markdown_path = repo_root / 'sdd-generated' / 'phase-2-input'
        
        if not markdown_path.exists():
            print(f"\n❌ Templates not found: {markdown_path}")
            print("\nYou need to:")
            print("1. Run Phase 1 to generate templates")
            print("2. Copy edited files to phase-2-input/")
            print("3. Run Phase 3 to compile")
            return False
        
        try:
            from orchestration.phase_wizard_v3 import Phase3Compiler
            
            output_path = repo_root / 'sdd-generated' / 'final-output'
            
            compiler = Phase3Compiler(markdown_path, output_path, repo_root, verbose=True)
            result = compiler.run()
            
            if result['success']:
                print(f"""
✅ PHASE 3 COMPLETE! 🎉

📊 COMPILATION RESULTS:
   ✓ Mandates: {result.get('mandates', 0)}
   ✓ Guidelines: {result.get('guidelines', 0)}
   ✓ Output Files: {', '.join(result.get('files', []))}
   ✓ Location: {result.get('output_path')}

═══════════════════════════════════════════════════════════════════
YOUR GOVERNANCE IS READY TO DEPLOY
═══════════════════════════════════════════════════════════════════

📂 STEP 1: IMPORT TO YOUR PROJECT
   Copy the entire .sdd/ folder to your project root:
   
   cp -r {result.get('output_path')} /path/to/your/project/.sdd/

📍 STEP 2: UPDATE SEEDLING TEMPLATES
   The wizard generates template references for AI tools:
   
   ✓ .vscode/settings.json        (VS Code AI settings)
   ✓ .cursor/rules/sdd-rules.md   (Cursor AI context)
   ✓ .ia/system-prompt.md         (Your AI system prompt)
   
   Review & customize these seedling files for your AI agents
   to understand your governance structure.

🔗 STEP 3: INTEGRATE WITH YOUR WORKFLOW
   Reference your governance in:
   ✓ CI/CD pipelines
   ✓ Pull request templates
   ✓ Development guidelines
   ✓ Architecture decision records (ADRs)

ℹ️  For AI understanding:
   Your 2 immutable mandates (M001, M002) and 150 customizable 
   guidelines are now compiled and ready for validation automation.

""")
                return True
            else:
                print(f"\n❌ Failed: {result.get('error', 'Unknown error')}")
                return False
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def run(self) -> bool:
        """Main interactive flow"""
        try:
            choice = self.show_phase_menu()
            
            if choice == '1':
                return self.phase_1_generate_templates()
            elif choice == '2':
                return self.phase_2_show_instructions()
            elif choice == '3':
                return self.phase_3_compile_templates()
            else:
                print("\n❌ Invalid choice. Please select 1, 2, or 3.")
                return False
        
        except KeyboardInterrupt:
            print("\n\n❌ Wizard cancelled by user")
            return False
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
            return False


def run_interactive_wizard(repo_root: Path) -> bool:
    """Entry point for interactive wizard"""
    wizard = InteractiveWizard(repo_root)
    return wizard.run()
