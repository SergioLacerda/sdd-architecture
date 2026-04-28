# GitHub Actions CI/CD Documentation

**Last Updated**: April 26, 2026  
**Status**: ✅ Production Ready

---

## Overview

This project uses GitHub Actions for comprehensive CI/CD automation. The workflows ensure code quality, compliance, and reliability across all commits and pull requests.

---

## Workflows Summary

### 🏥 Health Check (`health-check.yml`)
**Purpose**: Validate SDD Architecture health  
**Triggers**: Push (main/develop), PR, Daily at 2 AM UTC, Manual  
**Duration**: ~5 minutes

**What it does**:
- Runs 10-point health check
- Validates agent handshake protocol
- Generates health reports
- Comments on PRs with status

**Status Badges**:
- ✅ All checks passing: PR approved for merge
- ⚠️ Degraded: PR blocked, manual review needed
- ❌ Failed: PR blocked, must fix before merge

---

### 🧪 Tests (`tests.yml`)
**Purpose**: Run unit test suite  
**Triggers**: Push (paths: tests/, packages/), PR, Manual  
**Duration**: ~10 minutes

**What it does**:
- Discovers and runs all tests
- Generates coverage reports
- Uploads results to Codecov
- Comments on PRs with test status

**Requirements**:
- Tests must pass to merge PR
- Coverage targets: 80%+ for core modules

**Command to run locally**:
```bash
pytest tests/ -v --cov=packages
```

---

### 🔍 Lint & Code Quality (`lint.yml`)
**Purpose**: Check code quality and security  
**Triggers**: Push (paths: packages/, tests/), PR, Manual  
**Duration**: ~8 minutes

**Tools**:
- **Black**: Code formatting
- **isort**: Import sorting
- **Flake8**: Linting
- **mypy**: Type checking
- **pylint**: Code complexity
- **Bandit**: Security scanning
- **Safety**: Dependency vulnerabilities

**What it does**:
- Checks code formatting
- Validates import organization
- Scans for security issues
- Generates detailed reports
- Comments on PRs

**Command to run locally**:
```bash
black packages/ tests/
isort packages/ tests/
flake8 packages/ tests/
mypy packages/
pylint packages/
bandit -r packages/ tests/
```

---

### 📚 Documentation (`docs.yml`)
**Purpose**: Build and deploy documentation  
**Triggers**: Push (main, paths: docs/), PR, Manual  
**Duration**: ~10 minutes

**What it does**:
- Validates markdown syntax
- Checks documentation structure
- Builds MkDocs site
- Deploys to GitHub Pages (main only)
- Validates required files

**Requirements**:
- README.md must exist
- docs/INDEX.md must exist
- All documentation links must be valid

**Deployed to**: `https://<owner>.github.io/<repo>/`

---

### 🔐 Governance Enforce (`governance-enforce.yml`)
**Purpose**: Enforce project governance policies  
**Triggers**: Push (main/develop), PR (opened/updated)  
**Duration**: ~3 minutes

**What it does**:
- Validates compliance with policies
- Checks enforcement level
- Blocks non-compliant PRs
- Provides fix suggestions
- Requires architect approval

**Fix locally**:
```bash
python3 packages/governance_compliance.py --verify
python3 packages/governance_compliance.py --fix-steps
```

---

### 📊 Compliance Report (`compliance-report.yml`)
**Purpose**: Weekly compliance reporting  
**Triggers**: Weekly (Monday 9 AM UTC), Manual  
**Duration**: ~5 minutes

**What it does**:
- Generates compliance percentage
- Runs health checks
- Measures performance metrics
- Creates weekly reports
- Uploads artifacts

**Reports include**:
- Compliance status
- Health metrics
- Performance benchmarks
- Trend analysis

---

### 🚀 Release (`release.yml`)
**Purpose**: Create and publish releases  
**Triggers**: Push to main (with tags), Manual  
**Duration**: ~5 minutes

**What it does**:
- Creates git tags and GitHub releases
- Generates changelog
- Publishes release notes
- Uploads release artifacts
- Notifies team

**Usage**:
```bash
# Automatic (on tag push)
git tag v3.1.0
git push origin v3.1.0

# Or manual trigger through GitHub
```

---

### 📦 Dependencies (`dependencies.yml`)
**Purpose**: Check for outdated packages  
**Triggers**: Weekly (Monday 2 AM UTC), Manual  
**Duration**: ~2 minutes

**What it does**:
- Lists outdated packages
- Generates dependency report
- Uploads for review

**Note**: Dependabot handles automatic updates

---

### ✅ Integration Tests (`integration.yml`)
**Purpose**: Comprehensive integration testing  
**Triggers**: Push (main/develop), PR, Daily at midnight UTC, Manual  
**Duration**: ~20 minutes

**What it does**:
- Tests on Python 3.8, 3.9, 3.10, 3.11, 3.12
- Runs full health check
- Validates governance
- Runs agent handshake
- Benchmarks performance

**Matrix Testing**: Ensures compatibility across 5 Python versions

---

### 🔧 Validate Workflows (`validate-workflows.yml`)
**Purpose**: Validate workflow files  
**Triggers**: Changes to .github/workflows/, Manual  
**Duration**: ~2 minutes

**What it does**:
- Validates YAML syntax
- Lists all workflows
- Checks triggers
- Verifies permissions
- Looks for exposed secrets

---

## Triggering Workflows

### Automatically
Workflows trigger automatically based on events:

```yaml
on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM UTC
  workflow_dispatch:  # Manual trigger
```

### Manually
From GitHub UI:
1. Go to **Actions** tab
2. Select workflow
3. Click **Run workflow**
4. Choose branch and inputs

From CLI:
```bash
gh workflow run health-check.yml -r main
```

---

## PR Workflow

Every pull request automatically:

```
1. ✓ Runs all tests (pytest)
2. ✓ Checks code quality (lint.yml)
3. ✓ Validates governance (governance-enforce.yml)
4. ✓ Checks health (health-check.yml)
5. ✓ Validates documentation (docs.yml)
6. ✓ Comments with results
```

**PR can only be merged if**:
- ✅ All checks pass
- ✅ Code review approved (required)
- ✅ Architect approval (for governance changes)
- ✅ Governance compliance verified

---

## Artifacts & Reports

All workflows upload artifacts that are kept for:
- Test results: 30 days
- Coverage reports: 30 days
- Security reports: 30 days
- Documentation: 7 days
- Releases: 90 days

View artifacts:
1. Go to **Actions** tab
2. Click on workflow run
3. Scroll to **Artifacts** section
4. Download desired files

---

## Notifications & Comments

Workflows automatically:
- ✅ Comment on PRs with status
- ✅ Report health check results
- ✅ List test failures
- ✅ Show code quality issues
- ✅ Provide fix suggestions

Example PR comment:
```
✅ Health Check: 10/10 checks passed
🧪 Tests: 95/95 passed
🔍 Code Quality: 2 issues found
📚 Documentation: Valid
🔐 Governance: Compliant
```

---

## Debugging Failed Workflows

### View logs
1. Go to **Actions** tab
2. Click on failed workflow run
3. Click on failed job
4. Expand steps to see logs

### Common failures

| Symptom | Cause | Fix |
|---------|-------|-----|
| Tests fail | Code bug | Fix code, commit, push |
| Lint fails | Formatting | `black packages/ tests/` |
| Health check fails | Missing files | Check `/core` structure |
| Governance fails | Policy violation | `python3 packages/governance_compliance.py --fix-steps` |
| Docs fail | Invalid markdown | Check `docs/INDEX.md` exists |

### Rerun workflow
```bash
# Via GitHub UI
Click "Re-run all jobs"

# Via CLI
gh run rerun <run-id>
```

---

## Performance

Average workflow execution times:

| Workflow | Time | Critical? |
|----------|------|-----------|
| Health Check | 5m | ✅ Yes |
| Tests | 10m | ✅ Yes |
| Lint | 8m | ⚠️ Advisory |
| Governance | 3m | ✅ Yes |
| Docs | 10m | ⚠️ Advisory |
| Integration | 20m | ⚠️ Weekly |
| Release | 5m | ⚠️ Manual |

**Total PR check time**: ~15-20 minutes

---

## Customization

### Edit workflow
1. Go to `.github/workflows/<name>.yml`
2. Edit in GitHub web editor or locally
3. Commit and push to main
4. Workflow automatically uses new version

### Add new trigger
Edit the `on:` section:
```yaml
on:
  push:
    branches: [ main ]
    paths:
      - 'src/**'  # Only run if src/ changes
```

### Skip workflow
```bash
git commit -m "message" --skip-ci  # Skip all workflows
```

---

## Secrets & Environment Variables

### Repository Secrets
Set in GitHub: **Settings → Secrets → Actions**

Required secrets (optional, only if using):
- `CODECOV_TOKEN`: For Codecov integration
- `GITHUB_TOKEN`: Auto-provided by GitHub

### Environment Variables
Set in workflow YAML:
```yaml
env:
  PYTHON_VERSION: '3.10'
  CACHE_KEY: v1
```

---

## Best Practices

1. **Keep workflows simple**: Single responsibility per workflow
2. **Use caching**: For pip, Docker layers
3. **Fail fast**: Stop on first error
4. **Timeout**: Set reasonable limits
5. **Artifacts**: Keep for analytics
6. **Secrets**: Never hardcode credentials
7. **Concurrency**: Cancel old runs on new push
8. **Notifications**: Keep team informed

---

## Troubleshooting

### Workflow not running
- [ ] Check trigger conditions
- [ ] Verify branch name
- [ ] Check `.github/workflows/` file permissions

### Jobs taking too long
- [ ] Check for infinite loops
- [ ] Use concurrency to cancel old runs
- [ ] Add timeouts to steps

### Artifacts not uploading
- [ ] Check path syntax (use quotes)
- [ ] Verify files exist before upload
- [ ] Check retention-days setting

### Secret not accessible
- [ ] Verify secret name matches
- [ ] Use correct syntax: `${{ secrets.NAME }}`
- [ ] Check repository/environment scope

---

## Related Documentation

- [Health Check Guide](HEALTH_CHECK_GUIDE.md)
- [Governance Policies](../MANDATORY_POLICIES.md)
- [Git Hooks Guide](GIT_HOOKS_GUIDE.md)
- [Performance Optimization](PERFORMANCE_OPTIMIZATION.md)
- [Troubleshooting](TROUBLESHOOTING.md)

---

## Support

For issues with workflows:
1. Check [Troubleshooting](#troubleshooting) section
2. Review workflow logs in GitHub Actions
3. Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
4. Contact the architect team

---

**Last Updated**: April 26, 2026  
**Maintained By**: GitHub Copilot  
**Status**: ✅ Production Ready
