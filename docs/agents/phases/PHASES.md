# Migration Phases (v2.1 → v3.0)

## Timeline: Weeks 1-6

---

## Phase 1: Setup (Week 1, Day 1)

**Objective:** Prepare tooling + test extraction on sample

### Checklist

- [ ] Create .sdd-migration/ directory
- [ ] Add tooling scripts (5 files)
- [ ] Add test suite
- [ ] Create input/SOURCES.md (file list)
- [ ] Verify tooling runs without errors
- [ ] Test on sample (fixtures/v2_sample.md)
- [ ] Output appears in output/ (not empty)

### Commands

```bash
mkdir -p .sdd-migration/{tooling,tests/fixtures,input,output,reports}
cp tooling/*.py .sdd-migration/tooling/
pytest .sdd-migration/tests/test_migration_v2_to_v3.py::test_extraction_sample -v
```

**Done when:** `output/mandate.spec` exists and has content

---

## Phase 2: Full Extraction (Week 1, Days 2-5)

**Objective:** Extract all v2.1 content → v3.0 format

### Checklist

- [ ] Run full migration: `python tooling/migrate.py --full`
- [ ] Check output files exist:
  - [ ] output/mandate.spec (not empty)
  - [ ] output/guidelines.dsl (not empty)
- [ ] Check reports generated:
  - [ ] reports/extraction_report.json
  - [ ] reports/validation_report.json
- [ ] No errors in output
- [ ] Manual review of output/mandate.spec (first 100 lines look right?)
- [ ] Manual review of output/guidelines.dsl (content makes sense?)

### Commands

```bash
cd .sdd-migration
python tooling/migrate.py --full
cat output/mandate.spec | head -100
cat output/guidelines.dsl
```

**Done when:** Both output files exist + look reasonable

---

## Phase 3: Validation (Week 2, Days 1-3)

**Objective:** Validate content parity (no data loss)

### Checklist

- [ ] Run extraction validation:
  ```bash
  pytest tests/test_migration_v2_to_v3.py::test_principle_count -v
  pytest tests/test_migration_v2_to_v3.py::test_no_empty_fields -v
  pytest tests/test_migration_v2_to_v3.py::test_sequential_ids -v
  ```
- [ ] All tests pass
- [ ] No orphaned mandates
- [ ] All descriptions populated
- [ ] All validation commands present
- [ ] Run agent loader test (v3.0 format works):
  ```bash
  pytest tests/test_migration_v2_to_v3.py::test_agent_loader_v3 -v
  ```
- [ ] DSL syntax OK (parseability test)

### Expected Output

```
===== test session starts =====
test_principle_count PASSED
test_no_empty_fields PASSED
test_sequential_ids PASSED
test_validation_commands_present PASSED
test_agent_loader_v3_with_migrated_content PASSED
test_dsl_syntax_valid PASSED

===== 6 passed in 1.2s =====
```

**Done when:** All tests pass ✅

---

## Phase 4: Refinement (Week 2, Days 4-5)

**Objective:** Fix any issues, document changes

### Checklist

- [ ] Review validation report: `reports/validation_report.json`
- [ ] If failures, fix tooling + re-extract:
  ```bash
  python tooling/migrate.py --full
  pytest tests/ -v
  ```
- [ ] Document any manual edits (if needed):
  - [ ] Edit output/mandate.spec (if necessary)
  - [ ] Update reports/MANUAL_EDITS.md (log changes)
- [ ] Final review of output files
- [ ] Get sign-off from team

### Manual Edit Example

If found issues during review:

```markdown
# output/MANUAL_EDITS.md (if needed)

## Edit 1: M005 description clarification
- Original: "Async-first..."
- Changed to: "Async-first (no blocking calls on event loop)"
- Reason: Clarity for new readers

## Edit 2: M012 validation command fix
- Original: pytest command had typo
- Fixed to: correct path
- Reason: Command must be runnable
```

**Done when:** All output files approved + ready to move

---

## Phase 5: Cutover (Week 3, Day 1)

**Objective:** Move output → permanent location + cleanup v2.1

### ⚠️ CRITICAL: Follow CUTOVER.md exactly!

See [CUTOVER.md](CUTOVER.md) for step-by-step instructions.

### Pre-cutover Checklist

- [ ] Validation tests all pass
- [ ] output/mandate.spec reviewed
- [ ] output/guidelines.dsl reviewed
- [ ] Team agreed on changes
- [ ] Git working tree clean (no uncommitted changes)

### Cutover Checklist

- [ ] Run cutover script (or manual steps in CUTOVER.md)
- [ ] Verify .sdd-core/CANONICAL/mandate.spec exists
- [ ] Verify .sdd-guidelines/guidelines.dsl exists
- [ ] Verify v2.1 structure deleted (EXECUTION/spec/CANONICAL/rules)
- [ ] Git shows correct changes
- [ ] Git tag v3.0.0 created
- [ ] RELEASE_v3.0.md created

**Done when:** All files in place + git committed + tagged

---

## Phase 6: Documentation (Week 3-4)

**Objective:** Update docs to reflect v3.0

### Checklist

- [ ] Update README.md (remove tiers, add wizard)
- [ ] Create GETTING-STARTED-WITH-WIZARD.md
- [ ] Create MIGRATION_v2_to_v3.md (for community)
- [ ] Update EXECUTION/spec/guides/ (reflect v3.0)
- [ ] Create v3.0 adoption guides
- [ ] Verify all links work

**Done when:** Docs updated + reviewed

---

## Summary: Weekly Breakdown

```
Week 1 (Days 1-5):
  Day 1: Setup tooling ✅
  Day 2-5: Full extraction + manual review
  
Week 2 (Days 1-5):
  Day 1-3: Validation tests + fixes
  Day 4-5: Refinement + sign-off
  
Week 3 (Day 1):
  Cutover (move output → final location)
  
Week 3-4:
  Documentation updates

Total effort: ~80 hours (1 dev, ~2 weeks focused)
```

---

## Rollback Plan (if needed)

If something goes wrong during cutover:

```bash
# Before committing, you can always:
git checkout -- .  # Undo changes
rm -rf .sdd-core/ .sdd-guidelines/  # Remove migrated files
# Back to v2.1 state
```

**After commit:** Use git revert to back out (tag as experimental)

---

## Success Criteria

- ✅ All mandates extracted (count matches v2.1)
- ✅ All mandates populated (no empty fields)
- ✅ All validation tests pass
- ✅ Agent loader works with v3.0 format
- ✅ DSL syntax valid
- ✅ v2.1 structure cleaned up
- ✅ v3.0 structure in place
- ✅ Git history clean (single logical commit)
- ✅ Team sign-off obtained
