# 🔗 INTEGRATION.md — How to Add Your Project to SPEC

**For:** Engineering teams integrating SPEC with new projects  
**Time:** 30 minutes for full setup  
**Complexity:** Medium  

---

## 📋 Integration Pattern

```
/home/sergio/dev/
├── spec-architecture/           ← SPEC source of truth (standalone repo)
│   ├── docs/ia/
│   ├── tests/spec_validation/
│   └── README.md
│
└── your-project/               ← Your project (any framework)
    ├── docs/ia → ../spec-architecture/docs/ia  (symlink)
    ├── .github/copilot-instructions.md         (references spec-architecture)
    ├── .vscode/ai-rules.md                     (references spec-architecture)
    ├── .cursor/                                (references spec-architecture)
    ├── src/
    ├── tests/
    │   └── specs-ia-units/     ← Project-specific SPEC validation tests
    └── README.md
```

---

## 🚀 Setup Steps (5 min each)

### Step 1: Create Symlink to spec-architecture

```bash
cd /home/sergio/dev/your-project

# Remove existing docs/ia if present (save backup first!)
# mkdir -p backups && mv docs/ia backups/ia-backup

# Create symlink to spec-architecture
ln -s ../spec-architecture/docs/ia docs/ia

# Verify it works
ls docs/ia/CANONICAL/rules/ia-rules.md  # Should resolve ✅

# Verify SPEC tests are accessible
ls ../spec-architecture/tests/spec_validation/  # Should show 3 test files ✅
```

### Step 2: Update Configuration Files

**Update:** `.github/copilot-instructions.md`

```markdown
# Change from:
START NOW: /docs/ia/guides/onboarding/AGENT_HARNESS.md

# Change to:
START NOW: /../spec-architecture/docs/ia/guides/onboarding/AGENT_HARNESS.md

# All paths starting with /docs/ia/ now use:
/../spec-architecture/docs/ia/
```

**Update:** `.vscode/ai-rules.md`

```markdown
# Add at top:
# Links to shared SPEC framework
# See: /../spec-architecture/docs/ia/CANONICAL/rules/ia-rules.md

# Quick reference
- Governance: See /../spec-architecture/docs/ia/guides/onboarding/AGENT_HARNESS.md
- Rules: See /../spec-architecture/docs/ia/CANONICAL/rules/ia-rules.md
```

### Step 3: Create Project Specialization Config

**Create:** `docs/ia/custom/YOUR_PROJECT/SPECIALIZATIONS_CONFIG.md`

```markdown
# SPECIALIZATIONS CONFIG — YOUR_PROJECT

**Project:** your-project
**Language:** python
**Status:** In Development

---

## Project Parameters

PROJECT_NAME=your-project
LANGUAGE=python
ASYNC_FRAMEWORK=fastapi
MAX_CONCURRENT_ENTITIES=100
PRIMARY_DOMAIN_OBJECTS=entity1,entity2,entity3
TEAM_SIZE=3
MATURITY_LEVEL=alpha

---

**Generated:** 2026-04-19
**Status:** Configuration template
```

### Step 4: Generate Project Specializations

```bash
# Run generator (available in spec-architecture)
python ../spec-architecture/docs/ia/SCRIPTS/generate-specializations.py --project your-project

# Verify output
ls docs/ia/custom/your-project/SPECIALIZATIONS/
# Should show:
# - constitution-your-project-specific.md
# - ia-rules-your-project-specific.md
```

### Step 5: Create Project-Specific SPEC Validation Tests

**Create:** `tests/specs-ia-units/` folder structure

```bash
mkdir -p tests/specs-ia-units
```

---

## 📝 `tests/specs-ia-units/` Mandate

This folder contains tests that validate your project's compliance with SPEC architecture.

### Structure

```
tests/specs-ia-units/
├── __init__.py
├── test_layer_isolation.py       (Verify clean layer separation)
├── test_port_contracts.py        (Verify port abstraction)
├── test_thread_isolation.py      (Verify thread-safe modifications)
├── test_specialization_compliance.py  (Verify your specializations)
└── test_architecture_contracts.py    (Verify domain contracts)
```

### Purpose

These tests validate that:
- ✅ Your code follows SPEC layer architecture
- ✅ Domain layer doesn't import infrastructure
- ✅ Ports are used correctly
- ✅ Thread isolation is maintained
- ✅ Contracts are satisfied
- ✅ Your specializations are followed

### Example: test_layer_isolation.py

```python
"""Test that layers are isolated according to SPEC."""

import pytest
from pathlib import Path


class TestLayerIsolation:
    """Verify clean layer separation."""
    
    def test_domain_does_not_import_infrastructure(self):
        """Domain layer should not directly import infrastructure."""
        domain_files = Path("src/domain").rglob("*.py")
        
        for file in domain_files:
            content = file.read_text()
            assert "from src.infrastructure" not in content, \
                f"{file}: domain imports infrastructure directly"
    
    def test_ports_used_for_abstractions(self):
        """Infrastructure should be accessed only through ports."""
        domain_files = Path("src/domain").rglob("*.py")
        
        for file in domain_files:
            content = file.read_text()
            # Should use Port classes, not direct implementations
            if "SQLAlchemy" in content or "PostgreSQL" in content:
                assert "Port" in content, \
                    f"{file}: uses concrete DB, should use port"
    
    def test_application_layer_orchestrates(self):
        """Application layer should coordinate domain + infrastructure."""
        # Verify application layer exists
        app_layer = Path("src/application")
        assert app_layer.exists(), "Missing application layer"
        assert list(app_layer.glob("*.py")), "Application layer is empty"


class TestPortContracts:
    """Verify port abstraction contracts."""
    
    def test_all_ports_have_adapters(self):
        """Every port should have >= 1 adapter."""
        ports = Path("src/domain/ports").glob("*.py")
        
        for port_file in ports:
            port_name = port_file.stem
            adapter_files = list(Path("src/infrastructure/adapters").glob(f"*{port_name}*.py"))
            assert len(adapter_files) > 0, \
                f"Port {port_name} has no adapters"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
```

### Running Tests

```bash
# Run all architecture validation tests
pytest tests/specs-ia-units/ -v

# Run specific category
pytest tests/specs-ia-units/test_layer_isolation.py -v

# Run with coverage
pytest tests/specs-ia-units/ --cov=src --cov-report=html
```

---

## ✅ Integration Checklist

Before considering integration complete:

- [ ] Symlink created: `docs/ia → ../spec-architecture/docs/ia`
- [ ] Symlink verified: `ls docs/ia/CANONICAL/` works ✅
- [ ] `.github/copilot-instructions.md` updated
- [ ] `.vscode/ai-rules.md` updated
- [ ] `.cursor/` updated (if using Cursor IDE)
- [ ] `docs/ia/custom/YOUR_PROJECT/SPECIALIZATIONS_CONFIG.md` created
- [ ] Specializations generated: `constitution-*.md` and `ia-rules-*.md` exist
- [ ] `tests/specs-ia-units/` folder created
- [ ] At least 3 architecture tests written
- [ ] All tests passing: `pytest tests/specs-ia-units/ -v`
- [ ] Team trained on AGENT_HARNESS (10 min each)
- [ ] First feature started using new governance

**Estimated total time:** 30-45 minutes

---

## 🔄 Common Integration Issues

### Issue 1: Symlink doesn't work on Windows

**Solution:** Use `mklink` instead of `ln -s`

```cmd
# Windows PowerShell (admin)
New-Item -ItemType SymbolicLink -Path docs/ia -Target ..\spec-architecture\docs\ia
```

### Issue 2: CI/CD can't find symlinked files

**Solution:** CI/CD needs to follow symlinks

```yaml
# In .github/workflows/ci.yml
- name: Follow symlinks
  run: git config core.symlinks true

- name: Validate SPEC
  run: python ../spec-architecture/docs/ia/SCRIPTS/validate-ia-first.py --audit docs/ia/
```

### Issue 3: IDE doesn't resolve symlinks

**Solution:** Add symlink resolution to IDE settings

```json
// .vscode/settings.json
{
  "python.analysis.include": [
    "../spec-architecture/docs/ia"
  ]
}
```

---

## 🚀 After Integration

### Day 1: Team Onboarding
- Every developer reads AGENT_HARNESS (30 min)
- Team reviews specialization (15 min)
- First task assigned with SPEC workflow

### Week 1: Validation
- First 3 PRs follow SPEC discipline
- Architecture tests passing
- No violations in CI/CD

### Month 1: Mastery
- Team comfortable with layers
- Port contracts naturalized
- Thread isolation working

---

## 📚 Key Documents

After integration, your team should know:

| Document | Purpose | Read Time |
|----------|---------|-----------|
| [AGENT_HARNESS.md](../spec-architecture/docs/ia/guides/onboarding/AGENT_HARNESS.md) | 7-phase onboarding | 30 min |
| [ia-rules.md](../spec-architecture/docs/ia/CANONICAL/rules/ia-rules.md) | 16 mandatory rules | 20 min |
| [architecture.md](../spec-architecture/docs/ia/CANONICAL/specifications/architecture.md) | 8-layer architecture | 25 min |
| [Your SPECIALIZATIONS](../spec-architecture/docs/ia/custom/YOUR_PROJECT/SPECIALIZATIONS_CONFIG.md) | Project-specific rules | 10 min |

---

## 🔗 Support

**After integration, if you have issues:**

1. Check [AGENT_HARNESS.md emergency procedures](../spec-architecture/docs/ia/guides/emergency/)
2. Review your project specialization
3. Run architecture validation tests: `pytest tests/specs-ia-units/ -v`
4. Post in team channel with: error + test output + what you were doing

---

## 📞 Maintenance

**Updating SPEC?**

Since `docs/ia` is now a symlink to `spec-architecture`, all projects automatically get the update. No action needed.

**New rule added to SPEC?**

1. SPEC maintainer updates `/home/sergio/dev/spec-architecture/docs/ia/CANONICAL/`
2. Your project automatically sees the change (via symlink)
3. Update your `SPECIALIZATIONS_CONFIG.md` if needed
4. Run tests: `pytest tests/specs-ia-units/ -v`

---

**Last Updated:** 2026-04-19  
**Status:** Integration Guide v1.0  
**Tested With:** 1 project (rpg-narrative-server), ready for 2+

