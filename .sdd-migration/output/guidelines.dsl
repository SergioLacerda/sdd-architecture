# SDD v3.0 - GUIDELINES Specification
# Generated from v2.1 guides
# Generated: 2026-04-21T17:55:17.895245

guideline G01 {
  type: SOFT
  title: "🛠️ Constitution Customization Guide"
  description: "---"
  category: general
}

guideline G02 {
  type: SOFT
  title: "When to Customize"
  description: "- ✅ Your domain has different scale needs (embedded vs cloud) - ✅ Your tech stack differs from Python/FastAPI - ✅ Your team has different constraints - ✅ You need fewer/more layers than the standard..."
  category: general
}

guideline G03 {
  type: SOFT
  title: "What's Immutable vs Flexible"
  description: ""
  category: general
}

guideline G04 {
  type: SOFT
  title: "✅ Immutable Core (DO NOT CHANGE)"
  description: "These 5 principles must stay in every SDD Constitution: 1. **Clean separation of concerns** — Business logic isolated from infrastructure 2. **Explicit governance** — Rules documented, not implicit..."
  category: general
}

guideline G05 {
  type: SOFT
  title: "✅ Flexible (You Choose)"
  description: "These aspects can be customized: - **Number of layers** — 4-layer, 6-layer, 8-layer depending on your needs - **Specific ports** — What adapter contracts your domain needs - **Testing strategy** —..."
  category: general
}

guideline G06 {
  type: SOFT
  title: "Step-by-Step Customization"
  description: ""
  category: general
}

guideline G07 {
  type: SOFT
  title: "Step 1: Choose Your Baseline"
  description: "- Start with `/EXECUTION/spec/guides/adoption/templates/lite-constitution.yaml` - Modify the 5 principles for your domain - Takes: 15 minutes - Start with..."
  category: general
}

guideline G08 {
  type: SOFT
  title: "Step 2: Identify Your Constraints"
  description: "Answer these questions: 1. **What's your scale?** - Solo dev → ULTRA-LITE - Small team (< 5) → LITE - Production system → FULL 2. **What's your primary I/O pattern?** - Async (web services) → Keep..."
  category: general
}

guideline G09 {
  type: SOFT
  title: "Step 3: Create Your Constitution"
  description: "Create `.ai/constitution.md` in your project: ```markdown"
  category: general
}

guideline G10 {
  type: SOFT
  title: "[Your Project] Constitution"
  description: ""
  category: git
}

guideline G11 {
  type: SOFT
  title: "Core Principles"
  description: ""
  category: git
}

guideline G12 {
  type: SOFT
  title: "Principle 1: Clean Separation"
  description: "[Explain for your domain]"
  category: git
}

guideline G13 {
  type: SOFT
  title: "Principle 2: ..."
  description: "[etc.]"
  category: git
}

guideline G14 {
  type: SOFT
  title: "Your 3-5 Rules"
  description: ""
  category: general
}

guideline G15 {
  type: SOFT
  title: "Rule 1: ..."
  description: ""
  category: general
}

guideline G16 {
  type: SOFT
  title: "Rule 2: ..."
  description: ""
  category: general
}

guideline G17 {
  type: SOFT
  title: "Rule 3: ..."
  description: ""
  category: general
}

guideline G18 {
  type: SOFT
  title: "Definition of Done (5 items)"
  description: "- [ ] Feature implemented - [ ] Tests passing - [ ] [Your #3] - [ ] [Your #4] - [ ] [Your #5]"
  category: general
}

guideline G19 {
  type: SOFT
  title: "Customizations from SDD LITE"
  description: "- [Async requirement waived because: embedded system] - [Simplified to 4-layer because: fixed infrastructure] - [Added: load testing requirement] - [Clean separation] - [Explicit rules] - [Test..."
  category: general
}

guideline G20 {
  type: SOFT
  title: "Step 4: Document Your Deviations"
  description: "For each customization, explain: 1. **What** — What principle/rule did you change? 2. **Why** — Why was the standard version not suitable? 3. **How** — What's your alternative? 4. **Validation** —..."
  category: documentation
}

guideline G21 {
  type: SOFT
  title: "Customization: No Async-First"
  description: "- Embedded system with single-threaded event loop - All I/O is sequential and blocking - Async would add unnecessary complexity - Single-threaded execution model - Clear sequential I/O operations -..."
  category: general
}

guideline G22 {
  type: SOFT
  title: "Step 5: Validate Your Custom Constitution"
  description: "```bash"
  category: general
}

guideline G23 {
  type: SOFT
  title: "Validate your constitution syntax"
  description: "python -c \"import yaml; yaml.safe_load(open('.ai/constitution.yaml'))\""
  category: general
}

guideline G24 {
  type: SOFT
  title: "Check your code matches the constitution"
  description: "pytest tests/constitution/"
  category: general
}

guideline G25 {
  type: SOFT
  title: "Example test:"
  description: "def test_no_framework_in_domain(): \"\"\"Validate customization: no framework imports in domain\"\"\" result = os.system('grep -r \"import fastapi\" src/domain/') assert result != 0, \"Framework leaked into..."
  category: testing
}

guideline G26 {
  type: SOFT
  title: "Step 6: Version Your Constitution"
  description: "Track changes like you'd track code: ```markdown"
  category: general
}

guideline G27 {
  type: SOFT
  title: "[Your Project] Constitution"
  description: ""
  category: git
}

guideline G28 {
  type: SOFT
  title: "Change History"
  description: ""
  category: general
}

guideline G29 {
  type: SOFT
  title: "v1.2 (2026-04-20)"
  description: "- Added load testing requirement (Rule 3) - Increased concurrent entity requirement from 10 to 20"
  category: general
}

guideline G30 {
  type: SOFT
  title: "v1.1 (2026-04-15)"
  description: "- Simplified to 4-layer architecture - Waived async-first for embedded system"
  category: general
}

guideline G31 {
  type: SOFT
  title: "v1.0 (2026-04-10)"
  description: "- Initial custom constitution based on SDD LITE ``` ---"
  category: general
}

guideline G32 {
  type: SOFT
  title: "Common Customizations"
  description: ""
  category: general
}

guideline G33 {
  type: SOFT
  title: "1. Embedded System (No Async)"
  description: "```markdown"
  category: general
}

guideline G34 {
  type: SOFT
  title: "Core Principles"
  description: ""
  category: git
}

guideline G35 {
  type: SOFT
  title: "Principle 1: Clean Separation"
  description: "[Same as SDD]"
  category: git
}

guideline G36 {
  type: SOFT
  title: "Principle 2: Single-Threaded Execution"
  description: "All code runs on a single thread with sequential I/O. Async/await is not used. Functions are synchronous."
  category: git
}

guideline G37 {
  type: SOFT
  title: "Principle 3: Clear Ownership"
  description: "Each module owns its resources. No shared mutable state."
  category: git
}

guideline G38 {
  type: SOFT
  title: "Principle 4: ..."
  description: "[Continue with SDD principles] ```"
  category: git
}

guideline G39 {
  type: SOFT
  title: "2. CLI Tool (No HTTP Layer)"
  description: ""
  category: general
  examples: [
    "src/",
  ]
}

guideline G40 {
  type: SOFT
  title: "3. Data Pipeline (Focus on Resilience)"
  description: "```markdown"
  category: general
}

guideline G41 {
  type: SOFT
  title: "Rule 4: Checkpointing"
  description: "Every pipeline stage has a checkpoint. If failure occurs, resume from last checkpoint (not restart)."
  category: general
}

guideline G42 {
  type: SOFT
  title: "Rule 5: Dead Letter Queue"
  description: "Failed items go to DLQ for manual review, not retry loops. ```"
  category: general
}

guideline G43 {
  type: SOFT
  title: "4. Microservice (Focus on Contract Testing)"
  description: "```markdown"
  category: testing
}

guideline G44 {
  type: SOFT
  title: "Rule X: API Contract Testing"
  description: "Every endpoint has a contract test. Consumer contracts defined in OpenAPI/Pact. Producer validates against consumer contracts. ``` ---"
  category: testing
}

guideline G45 {
  type: SOFT
  title: "Template: Custom Constitution"
  description: "```markdown"
  category: general
}

guideline G46 {
  type: SOFT
  title: "[Project Name] Constitution"
  description: ""
  category: naming
}

guideline G47 {
  type: SOFT
  title: "Our Context"
  description: ""
  category: general
}

guideline G48 {
  type: SOFT
  title: "Core Principles (5)"
  description: ""
  category: git
}

guideline G49 {
  type: SOFT
  title: "Principle 1: [Name]"
  description: "[Repeat for 5 principles]"
  category: naming
}

guideline G50 {
  type: SOFT
  title: "Rules (3-5)"
  description: ""
  category: general
}

guideline G51 {
  type: SOFT
  title: "Rule 1: ..."
  description: ""
  category: general
}

guideline G52 {
  type: SOFT
  title: "Rule 2: ..."
  description: ""
  category: general
}

guideline G53 {
  type: SOFT
  title: "Rule 3: ..."
  description: ""
  category: general
}

guideline G54 {
  type: SOFT
  title: "Definition of Done"
  description: "- [ ] Feature implemented - [ ] Tests passing - [ ] [Your #3] - [ ] [Your #4] - [ ] [Your #5]"
  category: general
}

guideline G55 {
  type: SOFT
  title: "Deviations from SDD"
  description: "[List what you changed and why]"
  category: general
}

guideline G56 {
  type: SOFT
  title: "Validation"
  description: "[How you verify this works]"
  category: general
}

guideline G57 {
  type: SOFT
  title: "Team Sign-Off"
  description: "- [Name]: [Date] - [Name]: [Date]"
  category: general
}

guideline G58 {
  type: SOFT
  title: "References"
  description: "- [SDD Baseline Document] - [Your project architecture] - [Additional standards] ``` ---"
  category: general
}

guideline G59 {
  type: SOFT
  title: "When Customization Goes Wrong"
  description: ""
  category: general
}

guideline G60 {
  type: SOFT
  title: "🚨 Red Flags"
  description: "If you find yourself doing these, **stop and reconsider:** - ❌ \"Skipping tests because they're inconvenient\" → Use ULTRA-LITE instead, it has fewer requirements - ❌ \"Removing all validation\" →..."
  category: general
}

guideline G61 {
  type: SOFT
  title: "✅ Signs of Good Customization"
  description: "- ✅ Constitution is 2-4 pages - ✅ Every change is documented with rationale - ✅ Team agrees on it (sign-off document) - ✅ Validation is automated (tests or linting) - ✅ You can explain each..."
  category: general
}

guideline G62 {
  type: SOFT
  title: "Next Steps"
  description: "1. **Choose your baseline** — ULTRA-LITE, LITE, or FULL? 2. **Answer the 5 constraint questions** (Step 2) 3. **Create your constitution** (Step 3) 4. **Get team buy-in** (sign-off) 5. **Add..."
  category: general
}

guideline G63 {
  type: SOFT
  title: "Getting Help"
  description: "| Component | Can Customize | Recommendation | |-----------|---------------|-----------------| | **Number of layers** | ✅ Yes | Document why (4, 6, or 8) | | **Specific rules** | ✅ Yes | Keep..."
  category: general
}

guideline G64 {
  type: SOFT
  title: "⚡ IA-FIRST MARKDOWN SPECIFICATION"
  description: "---"
  category: general
}

guideline G65 {
  type: SOFT
  title: "📋 Overview"
  description: "IA-FIRST (AI-First) is a markdown format designed for: - ✅ Machine parsing (AI agents, scripts) - ✅ Clarity (humans and machines) - ✅ Consistency (no format variations) - ✅ Efficiency (reduced..."
  category: general
}

guideline G66 {
  type: SOFT
  title: "🎯 The 4 Core Rules"
  description: ""
  category: general
}

guideline G67 {
  type: SOFT
  title: "Rule 1: Heading Hierarchy (H1 → H2 → H3 → Lists)"
  description: "```markdown ✅ CORRECT:"
  category: general
}

guideline G68 {
  type: SOFT
  title: "Main Title (H1 — One per document)"
  description: ""
  category: documentation
}

guideline G69 {
  type: SOFT
  title: "Section (H2 — Major topics)"
  description: ""
  category: general
}

guideline G70 {
  type: SOFT
  title: "Subsection (H3 — Sub-topics)"
  description: "- Item 1 - Item 2 - Nested item ❌ WRONG:"
  category: general
}

guideline G71 {
  type: SOFT
  title: "Title (H1)"
  description: ""
  category: general
}

guideline G72 {
  type: SOFT
  title: "Skipped levels (H4 — no H2/H3)"
  description: "❌ WRONG:"
  category: general
}

guideline G73 {
  type: SOFT
  title: "Title (H1)"
  description: ""
  category: general
}

guideline G74 {
  type: SOFT
  title: "Section (H2)"
  description: ""
  category: general
}

guideline G75 {
  type: SOFT
  title: "Prose text without heading"
  description: "Some paragraph text here (shouldn't exist without H3) - Items follow prose ``` ---"
  category: git
}

guideline G76 {
  type: SOFT
  title: "Rule 2: Links Use Markdown Format ONLY"
  description: "---"
  category: code-style
}

guideline G77 {
  type: SOFT
  title: "Rule 3: Emoji Markers for Decisions"
  description: "---"
  category: general
}

guideline G78 {
  type: SOFT
  title: "Rule 4: Lists for Complex Ideas"
  description: "---"
  category: general
}

guideline G79 {
  type: SOFT
  title: "🔧 How to Apply IA-FIRST"
  description: ""
  category: general
}

guideline G80 {
  type: SOFT
  title: "Option A: Auto-Fix (Recommended)"
  description: "This automatically: - ✅ Fixes heading hierarchy - ✅ Adds missing IA-FIRST notice - ✅ Suggests emoji markers - ✅ Reports non-markdown links"
  category: general
  examples: [
    "python docs/ia/SCRIPTS/validate-ia-first.py --fix --audit docs/ia/",
  ]
}

guideline G81 {
  type: SOFT
  title: "Option B: Manual Application"
  description: ""
  category: general
}

guideline G82 {
  type: SOFT
  title: "Step 1: Add IA-FIRST Header"
  description: "Place this after your H1 title: ```markdown"
  category: general
}

guideline G83 {
  type: SOFT
  title: "Document Title"
  description: ""
  category: documentation
}

guideline G84 {
  type: SOFT
  title: "⚡ IA-FIRST DESIGN NOTICE"
  description: "- Structure: H1 → H2 (sections) → H3 (subsections) → Lists - All lists use `-` (not numbers or bullets) - All links use `[text](path.md)` format (no backticks) - All constraints marked with emoji (✅,..."
  category: general
}

guideline G85 {
  type: SOFT
  title: "Step 2: Add Status Metadata"
  description: ""
  category: general
}

guideline G86 {
  type: SOFT
  title: "Step 3: Restructure to H2/H3 Hierarchy"
  description: "```markdown"
  category: general
}

guideline G87 {
  type: SOFT
  title: "My Document"
  description: ""
  category: documentation
}

guideline G88 {
  type: SOFT
  title: "⚡ IA-FIRST DESIGN NOTICE"
  description: "[As above]"
  category: general
}

guideline G89 {
  type: SOFT
  title: "Major Topic 1"
  description: ""
  category: general
}

guideline G90 {
  type: SOFT
  title: "Subtopic 1.1"
  description: ""
  category: general
}

guideline G91 {
  type: SOFT
  title: "Subtopic 1.2"
  description: ""
  category: general
}

guideline G92 {
  type: SOFT
  title: "Major Topic 2"
  description: ""
  category: general
}

guideline G93 {
  type: SOFT
  title: "Subtopic 2.1"
  description: "- Item A - Item B - Nested detail ```"
  category: general
}

guideline G94 {
  type: SOFT
  title: "Step 4: Replace Prose with Lists"
  description: "```markdown"
  category: git
  examples: [
    "**After (lists):**",
  ]
}

guideline G95 {
  type: SOFT
  title: "Architecture Layers"
  description: "System components: - Storage layer: handles all data persistence - Index layer: maintains vector index for similarity search - Generation layer: calls the LLM ``` ---"
  category: general
}

guideline G96 {
  type: SOFT
  title: "✅ Validation Checklist"
  description: "Before committing documentation changes: ---"
  category: general
  examples: [
    "Document Structure:",
  ]
}

guideline G97 {
  type: SOFT
  title: "🔍 Examples"
  description: ""
  category: general
}

guideline G98 {
  type: SOFT
  title: "Example 1: Before (Non-IA-FIRST)"
  description: "```markdown"
  category: general
}

guideline G99 {
  type: SOFT
  title: "Configuration"
  description: "The system uses immutable configuration files. These files define important parameters like the maximum number of concurrent campaigns and the LLM model to use. You can't change them after startup...."
  category: general
}

guideline G100 {
  type: SOFT
  title: "Example 1: After (IA-FIRST)"
  description: "```markdown"
  category: general
}

guideline G101 {
  type: SOFT
  title: "Configuration Management"
  description: ""
  category: general
}

guideline G102 {
  type: SOFT
  title: "⚡ IA-FIRST DESIGN NOTICE"
  description: "[Standard notice...]"
  category: general
}

guideline G103 {
  type: SOFT
  title: "Immutable Configuration"
  description: "Immutable config defines critical parameters: - MAX_CONCURRENT_CAMPAIGNS: limit on parallel campaigns - LLM_MODEL_VERSION: AI model selection - VECTOR_INDEX_DIMENSION: embedding dimension 1. Edit..."
  category: general
}

guideline G104 {
  type: SOFT
  title: "Mutable Configuration"
  description: "Mutable config can change live without redeployment: - LLM_TEMPERATURE: within bounds [0.0, 1.0] - CACHE_TTL_SECONDS: within bounds [60, 3600] - RETRY_BACKOFF_MS: within bounds [100, 10000] 🎯..."
  category: general
}

guideline G105 {
  type: SOFT
  title: "Configuration Storage"
  description: "Config locations by type: | Type | Location | Mutable? | |------|----------|----------| | Immutable | pyproject.toml | No | | Secrets | Kubernetes secrets | Admin only | | Mutable | Admin dashboard |..."
  category: general
}

guideline G106 {
  type: SOFT
  title: "📊 Impact on AI Parsing"
  description: ""
  category: general
}

guideline G107 {
  type: SOFT
  title: "Before (Non-IA-FIRST)"
  description: ""
  category: general
  examples: [
    "Agent reads document:",
  ]
}

guideline G108 {
  type: SOFT
  title: "After (IA-FIRST)"
  description: "---"
  category: general
  examples: [
    "Agent reads document:",
  ]
}

guideline G109 {
  type: SOFT
  title: "🔗 References"
  description: "- [validate-ia-first.py](../SCRIPTS/validate-ia-first.py) — Automated validation - [Quality Audit](../../../../context/runtime-state/analysis/WORLD_CLASS_REVIEW.md) — Architecture review - [Example:..."
  category: general
}

guideline G110 {
  type: SOFT
  title: "⚠️ Common Mistakes"
  description: "| Mistake | Impact | Fix | |---------|--------|-----| | Mixing prose + lists in H2 | AI confusion | Use lists only | | Backtick links `[text](path)` | Parser error | Remove backticks | | H1 → H4..."
  category: general
}

guideline G111 {
  type: SOFT
  title: "✅ Next Steps"
  description: "1. **Audit existing docs:** `python validate-ia-first.py --audit docs/ia/` 2. **Auto-fix:** `python validate-ia-first.py --fix --audit docs/ia/` 3. **Review changes:** Check git diff 4. **Commit:**..."
  category: general
}

guideline G112 {
  type: SOFT
  title: "📚 GUIDES ORGANIZATION"
  description: "New structure for guides by purpose: ---"
  category: general
  examples: [
    "guides/",
  ]
}

guideline G113 {
  type: SOFT
  title: "🟢 ONBOARDING"
  description: "When starting a new agent session: 1. **FIRST_SESSION_SETUP.md** — 15-minute orientation - Understand documentation structure - Lock to ia-rules.md - Choose your PATH - Check execution state - Load..."
  category: general
}

guideline G114 {
  type: SOFT
  title: "🔵 IMPLEMENTATION"
  description: "When building features: 1. **IMPLEMENTATION_ROADMAP.md** — Step-by-step process - Full workflow from idea to merge - Checkpoints along the way - Integration points 2. **DESIGN_DECISIONS.md** — Making..."
  category: general
}

guideline G115 {
  type: SOFT
  title: "🟣 NAVIGATION"
  description: "Finding what you need: 1. **INDEX.md** — \"I need X, where do I go?\" - Master reference - 30+ questions mapped to docs - Document matrix 2. **CONTEXT_INDEX.md** — Semantic search guide - How to search..."
  category: general
}

guideline G116 {
  type: SOFT
  title: "🟡 CONTEXT"
  description: "Background and historical information: 1. **DELIVERY_SUMMARY.md** — What was delivered - New files created - Files changed - Impact metrics 2. **FINAL_STATUS.md** — Completion checklist -..."
  category: general
}

guideline G117 {
  type: SOFT
  title: "📋 REFERENCE"
  description: "Lookup tables and definitions: 1. **FAQ.md** — Common questions and answers - \"Why X?\" type questions - \"How do I Y?\" type questions - Links to detailed docs 2. **GLOSSARY.md** — Terminology - Terms..."
  category: general
}

guideline G118 {
  type: SOFT
  title: "QUICK NAVIGATION"
  description: "---"
  category: general
}

guideline G119 {
  type: SOFT
  title: "MIGRATION NOTE"
  description: "Old structure (flat): New structure (organized): Old files still exist at root level for compatibility during transition."
  category: general
  examples: [
    "guides/",
    "guides/",
  ]
}

guideline G120 {
  type: SOFT
  title: "📚 GUIDES INDEX — On-Demand Reading"
  description: "---"
  category: general
}

guideline G121 {
  type: SOFT
  title: "🎯 I need help with..."
  description: ""
  category: general
}

guideline G122 {
  type: SOFT
  title: "**\"I'm new to the project\"**"
  description: "→ **Time:** 30 minutes → **What to read:** 1. [FIRST_SESSION_SETUP.md](onboarding/FIRST_SESSION_SETUP.md) (15 min) 2. [QUICK_START.md](onboarding/QUICK_START.md) (5 min) 3...."
  category: git
}

guideline G123 {
  type: SOFT
  title: "**\"I'm implementing a bug fix\"** (PATH A: 1.5h)"
  description: "→ **Time:** 15 minutes reading → **What to read:** 1. [FIRST_SESSION_SETUP.md](onboarding/FIRST_SESSION_SETUP.md) §1-3 (5 min) 2...."
  category: general
}

guideline G124 {
  type: SOFT
  title: "**\"I'm implementing a simple feature\"** (PATH B: 2h)"
  description: "→ **Time:** 20 minutes reading → **What to read:** 1. [QUICK_START.md](onboarding/QUICK_START.md) (3 min) 2. `/EXECUTION/spec/CANONICAL/rules/constitution.md` — sections 1-3 (10 min) 3...."
  category: general
}

guideline G125 {
  type: SOFT
  title: "**\"I'm implementing a complex feature\"** (PATH C: 3-4h)"
  description: "→ **Time:** 45 minutes reading → **What to read:** 1. [QUICK_START.md](onboarding/QUICK_START.md) (3 min) 2. `/EXECUTION/spec/CANONICAL/rules/constitution.md` — ALL sections (20 min) 3...."
  category: general
}

guideline G126 {
  type: SOFT
  title: "**\"I'm working on parallel development threads\"** (PATH D: Variable)"
  description: "→ **Time:** 30 minutes reading → **What to read:** 1. [FIRST_SESSION_SETUP.md](onboarding/FIRST_SESSION_SETUP.md) (15 min) 2...."
  category: general
}

guideline G127 {
  type: SOFT
  title: "🔍 I'm stuck with..."
  description: ""
  category: general
}

guideline G128 {
  type: SOFT
  title: "**\"A commit hook failed\"**"
  description: "→ **Read:** [CI/CD validation guide](../operational/README.md) → **Time:** 10 minutes"
  category: git
}

guideline G129 {
  type: SOFT
  title: "**\"A test is failing\"**"
  description: "→ **Read:** 1. [IMPLEMENTATION_ROADMAP.md](implementation/IMPLEMENTATION_ROADMAP.md) (find similar feature) 2. `/EXECUTION/spec/CANONICAL/specifications/testing.md` (understand test types) →..."
  category: testing
}

guideline G130 {
  type: SOFT
  title: "**\"Performance is slow\"**"
  description: "→ **Read:** 1. `/EXECUTION/spec/CANONICAL/specifications/performance.md` (SLO targets) 2. [Performance SLOs](/EXECUTION/spec/CANONICAL/specifications/performance.md) → **Time:** 20 minutes"
  category: performance
}

guideline G131 {
  type: SOFT
  title: "**\"I don't understand an ADR decision\"**"
  description: "→ **Read:** 1. Relevant ADR in `/EXECUTION/spec/CANONICAL/decisions/` 2. Project specialization in `/EXECUTION/spec/custom/rpg-narrative-server/SPECIALIZATIONS/` → **Time:** 15 minutes ---"
  category: general
}

guideline G132 {
  type: SOFT
  title: "👥 By Role"
  description: ""
  category: general
}

guideline G133 {
  type: SOFT
  title: "**Backend Developer**"
  description: "1. `/EXECUTION/spec/CANONICAL/rules/constitution.md` (principles) 2. `/EXECUTION/spec/CANONICAL/specifications/architecture.md` (design) 3...."
  category: general
}

guideline G134 {
  type: SOFT
  title: "**DevOps / SRE**"
  description: "1. `/EXECUTION/spec/CANONICAL/specifications/observability.md` (logging/metrics) 2. `/EXECUTION/spec/CANONICAL/specifications/performance.md` (SLOs) 3. [CI/CD validation..."
  category: general
}

guideline G135 {
  type: SOFT
  title: "**Product Manager**"
  description: "1. [YOUR_VISION_IMPLEMENTED.md](context/YOUR_VISION_IMPLEMENTED.md) (overview) 2. `/EXECUTION/spec/CANONICAL/rules/backward-compatibility-policy.md` (when breaking changes allowed) 3...."
  category: git
}

guideline G136 {
  type: SOFT
  title: "**Architect**"
  description: "1. `/EXECUTION/spec/CANONICAL/rules/constitution.md` (ALL) 2. `/EXECUTION/spec/CANONICAL/specifications/architecture.md` (ALL) 3. `/EXECUTION/spec/CANONICAL/decisions/` (ALL ADRs) -..."
  category: general
}

guideline G137 {
  type: SOFT
  title: "⏱️ By Time Budget"
  description: ""
  category: general
}

guideline G138 {
  type: SOFT
  title: "**5 minutes** (Quick question)"
  description: "- [QUICK_START.md](onboarding/QUICK_START.md) - Specific ADR title or one section"
  category: general
}

guideline G139 {
  type: SOFT
  title: "**15 minutes** (Quick decision)"
  description: "- One principle from `/EXECUTION/spec/CANONICAL/rules/constitution.md` - One specification from `/EXECUTION/spec/CANONICAL/specifications/` - Project specialization overview"
  category: general
}

guideline G140 {
  type: SOFT
  title: "**30 minutes** (Daily work)"
  description: "- [FIRST_SESSION_SETUP.md](onboarding/FIRST_SESSION_SETUP.md) - Relevant PATH from [QUICK_START.md](onboarding/QUICK_START.md) - Project-specific guides"
  category: general
}

guideline G141 {
  type: SOFT
  title: "**1 hour** (In-depth understanding)"
  description: "- Full `/EXECUTION/spec/CANONICAL/rules/constitution.md` - Full `/EXECUTION/spec/CANONICAL/specifications/architecture.md` - Relevant ADRs (2-3)"
  category: general
}

guideline G142 {
  type: SOFT
  title: "**2+ hours** (Deep learning)"
  description: "- Complete `/EXECUTION/spec/CANONICAL/` layer - Complete `/EXECUTION/spec/custom/rpg-narrative-server/` layer - Relevant guides for your role ---"
  category: general
}

guideline G143 {
  type: SOFT
  title: "🗺️ Documentation Map"
  description: ""
  category: documentation
}

guideline G144 {
  type: SOFT
  title: "**CANONICAL Layer** (Generic, all projects inherit)"
  description: "Used when: Understanding principles, learning patterns, implementing across projects"
  category: git
  examples: [
    "CANONICAL/",
  ]
}

guideline G145 {
  type: SOFT
  title: "**SPECIALIZATIONS Layer** (Project-specific)"
  description: "Used when: Implementing rpg-narrative-server features"
  category: git
  examples: [
    "custom/rpg-narrative-server/SPECIALIZATIONS/",
  ]
}

guideline G146 {
  type: SOFT
  title: "**Guides Layer** (Navigation & learning)"
  description: "Used when: Lost, stuck, or learning ---"
  category: general
  examples: [
    "guides/",
  ]
}

guideline G147 {
  type: SOFT
  title: "🚀 Reading Flow Examples"
  description: ""
  category: general
}

guideline G148 {
  type: SOFT
  title: "**Example 1: I want to add campaign search**"
  description: ""
  category: general
  examples: [
    "1. START: Read PATH for feature complexity",
  ]
}

guideline G149 {
  type: SOFT
  title: "**Example 2: Bug fix in campaign isolation**"
  description: "---"
  category: general
  examples: [
    "1. QUICK: Understand what to read",
  ]
}

guideline G150 {
  type: SOFT
  title: "✅ Loading Optimization Checklist"
  description: "When reading docs: - [ ] Know your time budget (5, 15, 30, 60+ minutes) - [ ] Know your role (backend, devops, PM, architect) - [ ] Know your task (bug fix, feature, learning) - [ ] Read ONLY what's..."
  category: general
}
