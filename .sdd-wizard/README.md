# 🎼 .sdd-wizard/ - The Motor of SDD v3.0

**The central orchestrator that transforms architect specifications into client-ready projects**

---

## 🎯 Purpose

The Wizard is the **engine** that drives the entire SDD workflow:

```
Architect edits source → CI/CD compiles → WIZARD ORCHESTRATES → Client gets project
  (.sdd-core/)        (.sdd-runtime/)     (generates all layers)      (.sdd/)
```

Without the Wizard, users would need to manually:
- Filter which mandates to include
- Organize guidelines by language & profile
- Create directory structures
- Substitute templates
- Validate outputs

**The Wizard automates all 7 phases** with auditability at every step.

---

## 📚 Documentation Structure

### [ORCHESTRATION.md](ORCHESTRATION.md)
**"How the Wizard Works - The Technical Blueprint"**

Defines:
- Wizard's core role (central orchestrator)
- 7-phase orchestration pipeline
- Implementation phases (v3.0 → v3.3+)
- Key design decisions (stateless, always-fresh, immutable, auditable)
- Complete implementation structure (7 subdirectories)
- Usage examples (interactive, non-interactive, verbose)

**Start here to understand the architecture.**

### [WORKFLOW_FLOW.md](WORKFLOW_FLOW.md)
**"Complete End-to-End Flow - See It All Work"**

Describes:
- Complete system architecture (all 4 layers)
- Layer interactions & data flow
- Decision points & filtering logic
- Mandate/guideline propagation examples
- Immutability & safety guarantees
- Error handling strategies
- Versioning & audit trail mechanics
- State machine (all states & transitions)
- Complete user journey (3 days of work)

**Read this to see the full picture of how everything connects.**

---

## 🏗️ Directory Structure

```
.sdd-wizard/                        (Wizard motor - SDD v3.0)
├── ORCHESTRATION.md                (Architecture & design)
├── WORKFLOW_FLOW.md                (Complete end-to-end flow)
├── README.md                        (This file)
├── src/                            (Core implementation)
│   ├── wizard.py                   (Main orchestrator entry point)
│   ├── loader.py                   (Load SOURCE + COMPILED)
│   ├── validator.py                (Validate inputs)
│   ├── filter.py                   (Filter mandates & guidelines)
│   ├── generator.py                (Generate final project)
│   ├── user_input.py               (Interactive prompts)
│   └── config.py                   (Config & constants)
├── orchestration/                  (7-phase pipeline)
│   ├── phase_1_validate.py         (Validate SOURCE)
│   ├── phase_2_load_compiled.py    (Load COMPILED)
│   ├── phase_3_filter_mandates.py  (User mandate selection)
│   ├── phase_4_filter_guidelines.py(Language + profile filtering)
│   ├── phase_5_apply_scaffold.py   (Load & apply templates)
│   ├── phase_6_generate.py         (Generate project structure)
│   └── phase_7_validate.py         (Validate output)
├── generators/                     (Template & artifact generation)
│   ├── manifest_generator.py       (Generate project manifest)
│   ├── metadata_generator.py       (Generate metadata.json)
│   └── guideline_markdown.py       (Generate .md from categories)
├── validators/                     (Validation logic)
│   ├── source_validator.py         (Validate .sdd-core/)
│   ├── compiled_validator.py       (Validate .sdd-runtime/)
│   ├── output_validator.py         (Validate generated template)
│   └── dependency_validator.py     (Check dependencies)
└── tests/                          (Test suite)
    ├── test_orchestration.py       (End-to-end tests)
    ├── test_phases.py              (Individual phase tests)
    ├── test_filtering.py           (Filter logic tests)
    └── test_generators.py          (Generator tests)
```

---

## 🔄 The 7-Phase Pipeline

```
Phase 1: VALIDATE SOURCE          → Check .sdd-core/ integrity
Phase 2: LOAD COMPILED            → Read .sdd-runtime/ binary
Phase 3: FILTER MANDATES          → User selects which mandates
Phase 4: FILTER GUIDELINES        → Filter by language + profile
Phase 5: APPLY SCAFFOLD           → Load .sdd-template/ base
Phase 6: GENERATE PROJECT         → Create directory structure
Phase 7: VALIDATE OUTPUT          → Verify deliverable
```

Each phase:
- Has one responsibility
- Can be tested independently
- Produces clear output
- Fails gracefully with error messages

---

## 🎯 Key Features (v3.0)

✅ **Stateless Execution**
- Each run is independent
- No persistent state
- Idempotent output

✅ **Always Fresh**
- Always reads latest .sdd-core/
- Always reads latest .sdd-runtime/
- Uses latest .sdd-template/

✅ **Immutable Delivery**
- Generated `.sdd/` is read-only
- Client cannot edit specs
- Client customizations → `.sdd-custom/` (v3.2+)

✅ **Fully Auditable**
- metadata.json tracks everything
- Source version tracked
- User selections recorded
- Compile timestamp captured

---

## 🚀 Usage Examples

### Interactive Mode (v3.0+)
```bash
$ python .sdd-wizard/src/wizard.py

? Choose language: [1] Java [2] Python [3] JS
> 1

? Choose mandates:
  [✓] M001: Clean Architecture
  [ ] M002: Test-Driven Development
> Select M001

? Choose profile: [1] ULTRA-LITE [2] LITE [3] FULL
> 2

? Output destination: ~/my-java-project
[INFO] Running PHASE 1: Validate SOURCE...
[INFO] Running PHASE 2: Load COMPILED...
[INFO] Running PHASE 3: Filter mandates...
[INFO] Running PHASE 4: Filter guidelines...
[INFO] Running PHASE 5: Apply scaffold...
[INFO] Running PHASE 6: Generate project...
[INFO] Running PHASE 7: Validate output...
[SUCCESS] Project ready: ~/my-java-project/

Next steps:
  1. cd ~/my-java-project
  2. cat README-SDD.md
  3. mvn clean test
```

### Non-Interactive Mode (v3.1+)
```bash
python .sdd-wizard/src/wizard.py \
  --language java \
  --mandates M001,M002 \
  --profile lite \
  --output ~/my-java-project/ \
  --verbose
```

### Dry-Run Mode (for testing)
```bash
python .sdd-wizard/src/wizard.py \
  --language python \
  --mandates M001 \
  --profile full \
  --dry-run \
  --verbose
```

---

## 📊 Data Flow

```
USER INPUT (wizard prompts)
    ↓
Phase 1-2: LOAD ARTIFACTS
    ├─ .sdd-core/ (SOURCE)
    ├─ .sdd-runtime/ (COMPILED)
    └─ .sdd-template/ (SCAFFOLD)
    ↓
Phase 3-4: FILTER
    ├─ Mandate selection (user chooses)
    ├─ Language filtering (remove irrelevant)
    └─ Profile filtering (keep essential)
    ↓
Phase 5: APPLY TEMPLATES
    ├─ Load base files
    ├─ Substitute placeholders
    └─ Load language-specific templates
    ↓
Phase 6: GENERATE
    ├─ Create directory structure
    ├─ Write filtered specs
    ├─ Generate .md files
    └─ Copy templates
    ↓
Phase 7: VALIDATE
    ├─ Check file existence
    ├─ Verify integrity
    └─ Run basic tests
    ↓
OUTPUT: /path/to/my-project/
    ├── .sdd/
    ├── .sdd-guidelines/
    ├── src/
    └── [build files]
```

---

## 🔗 Integration Points

### Reads FROM:
- `.sdd-core/mandate.spec` (SOURCE - architect edits)
- `.sdd-core/guidelines.dsl` (SOURCE - architect edits)
- `.sdd-runtime/mandate.bin` (COMPILED - CI/CD generates)
- `.sdd-runtime/guidelines.bin` (COMPILED - CI/CD generates)
- `.sdd-runtime/metadata.json` (METADATA - CI/CD generates)
- `.sdd-template/base/` (SCAFFOLD - part of wizard)
- `.sdd-template/profiles/` (SCAFFOLD - part of wizard)
- `.sdd-template/languages/` (SCAFFOLD - part of wizard)

### Writes TO:
- `{output_dir}/.sdd/CANONICAL/` (filtered specs)
- `{output_dir}/.sdd-guidelines/` (organized guides)
- `{output_dir}/.sdd/metadata.json` (audit trail)
- `{output_dir}/src/` (project structure)
- `{output_dir}/.github/workflows/` (CI/CD)
- `{output_dir}/[build-files]` (pom.xml, requirements.txt, etc.)

---

## 📈 Implementation Roadmap

### Phase A: Orchestrator Core (v3.0) - NOW
- [x] Directory structure planned
- [x] 7-phase pipeline documented
- [ ] Core implementations (wizard.py, orchestration phases)
- [ ] Test suite
- [ ] Documentation (this file + ORCHESTRATION.md + WORKFLOW_FLOW.md)

### Phase B: Advanced Filtering (v3.1)
- [ ] Category-based guideline organization
- [ ] Language-specific examples
- [ ] Profile-specific content selection
- [ ] Non-interactive CLI mode

### Phase C: Customization (v3.2)
- [ ] `.sdd-custom/` support in client projects
- [ ] Local mandate extensions
- [ ] Guideline remixing

### Phase D: CI/CD Integration (v3.3+)
- [ ] GitHub Actions trigger
- [ ] Automated template updates
- [ ] Version tracking & deprecation warnings

---

## 🧪 Testing Strategy

```
test_orchestration.py
├─ test_end_to_end_java        (Full workflow → Java)
├─ test_end_to_end_python      (Full workflow → Python)
└─ test_end_to_end_js          (Full workflow → JS)

test_phases.py
├─ test_phase_1_validate       (SOURCE validation)
├─ test_phase_2_load_compiled  (COMPILED loading)
├─ test_phase_3_filter_mandates(Mandate filtering)
├─ test_phase_4_filter_guidelines(Language + profile)
├─ test_phase_5_apply_scaffold (Template loading)
├─ test_phase_6_generate       (Project generation)
└─ test_phase_7_validate       (Output validation)

test_filtering.py
├─ test_mandate_selection      (User selection logic)
├─ test_language_filtering     (Java/Python/JS filters)
└─ test_profile_filtering      (lite/full profiles)

test_generators.py
├─ test_metadata_generation    (metadata.json creation)
├─ test_markdown_generation    (.md files)
└─ test_placeholder_substitution({{}} → values)
```

All tests:
- Use fixtures for sample data
- Mock external dependencies
- Verify output immutability
- Test error conditions

---

## 🔐 Security & Safety

✅ **Immutable Specifications**
- `.sdd/CANONICAL/` marked read-only
- Client cannot modify inherited specs
- Customizations go to `.sdd-custom/` (v3.2)

✅ **Validated Inputs**
- User selections validated against available mandates
- Language/profile combinations checked
- Destination paths sanitized

✅ **Safe File Operations**
- File creation with proper permissions
- Atomic writes (no partial states)
- Rollback on error

✅ **Audit Trail**
- metadata.json records everything
- Can trace back to source commit
- Versioning support for updates

---

## 📝 Configuration

See `src/config.py` for:
- Supported languages (java, python, js)
- Profile levels (ultra-lite, lite, full)
- Category definitions for guidelines
- Placeholder naming conventions
- Error messages & logging

---

## 🤝 Contributing

To add new features:
1. Extend orchestration phases
2. Add tests first (TDD)
3. Update documentation
4. Create PR with ADR-008 compliance

---

## 📞 Support & Debugging

### Enable verbose logging:
```bash
python .sdd-wizard/src/wizard.py --verbose
```

### Dry-run mode (no file writes):
```bash
python .sdd-wizard/src/wizard.py --dry-run
```

### Check integrity:
```bash
python .sdd-wizard/src/validator.py --check-all
```

### View full manifest:
```bash
python .sdd-wizard/src/generator.py --manifest-only
```

---

## 🎓 Learning Resources

1. **Start here:** Read [ORCHESTRATION.md](ORCHESTRATION.md)
2. **See it in action:** Read [WORKFLOW_FLOW.md](WORKFLOW_FLOW.md)
3. **Explore code:** Check `orchestration/` subdirectory
4. **Run tests:** `pytest .sdd-wizard/tests/ -v`
5. **Try it:** `python .sdd-wizard/src/wizard.py --help`

---

## 🚀 Next Steps

Once Phase A is complete:

1. Implement each phase in `orchestration/` directory
2. Add validators in `validators/` directory
3. Add generators in `generators/` directory
4. Write comprehensive test suite
5. Document edge cases & error handling
6. Create CLI interface (argparse)
7. Add progress indicators & logging
8. Deploy to CI/CD for automated testing

---

**Last Updated:** April 21, 2026  
**Status:** Architecture Defined (Phase A Planning)  
**Version:** 3.0
