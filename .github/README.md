# .github Directory - GitHub Actions & Workflows

This directory contains GitHub-specific automation and CI/CD configurations for the SDD Architecture project.

## Workflows

### `workflows/health-check.yml`
**Purpose**: Automated SDD Architecture health validation on every push and pull request.

**Trigger Events**:
- ✓ Push to `main` branch
- ✓ Pull requests against `main`
- ✓ Daily schedule (2 AM UTC)
- ✓ Manual trigger via workflow_dispatch

**Jobs**:

#### 1. `health-check` (Main Validation)
Runs all 4 validation engines:
- **health_check.py**: 10 explicit checks (git, structure, deps, governance)
- **diagnostics_test.py**: 14 diagnostic tests (structure + config + imports + git)
- **agent_handshake.py**: AHP implicit validation (4 layers, 5 states)
- **agent_confidence.py**: Confidence scoring (5 metrics)

**Output Artifacts**:
- `health-report.json`: Explicit validation report
- `diagnostics-report.json`: Diagnostic test results
- `ahp-report.json`: Implicit AHP validation
- `confidence-report.json`: Confidence metrics

**Retention**: 30 days

#### 2. `integration-test` (AHP Verification)
Tests the AHP programmatic API:
- ✓ Semantic trigger detection (8 test cases)
- ✓ State machine validation
- ✓ JSON output format
- ✓ Caching mechanism

#### 3. `summary` (Result Aggregation)
Generates GitHub Actions summary with:
- Component status table
- Overall validation result
- Links to artifacts

### PR Comments

Workflow automatically comments on pull requests with:
```
## 🧠 SDD Architecture Health Check

**State**: 🟢 HEALTHY
**Confidence**: 92%
**Checks Passed**: 34/34

### Health Summary
[Summary text from health_check.py]

### Next Steps
[Suggested actions from AHP]
```

## Health States & Actions

| State | Symbol | Outcome | Action |
|-------|--------|---------|--------|
| HEALTHY | 🟢 | ✅ Pass | Proceed with merge |
| PARTIAL | 🟡 | ⚠️ Warn | Suggest fixes before merge |
| NOT_INITIALIZED | ⚠️ | ⚠️ Warn | Suggest phase-0 setup |
| MISCONFIGURED | ⚠️ | ❌ Fail | Fix config before merge |
| NOT_CONNECTED | ❌ | ❌ Fail | Initialize before merge |

## Success/Failure Rules

**Workflow Passes** (✅) if:
- State = HEALTHY or PARTIAL
- All 4 validation engines complete
- Artifacts generated successfully

**Workflow Fails** (❌) if:
- State = MISCONFIGURED or NOT_CONNECTED
- Any validation engine errors
- Core checks fail

## Running Locally

To simulate the GitHub Actions workflow locally:

```bash
# Run all health checks
python _core/health_check.py --json > health-report.json
python _core/diagnostics_test.py --json > diagnostics-report.json
python _core/agent_handshake.py --mode=compact --json > ahp-report.json
python _core/agent_confidence.py --json > confidence-report.json

# Parse results
cat ahp-report.json | jq '.state, .confidence'
```

## Workflow Configuration

**Python Version**: 3.10  
**OS**: Ubuntu Latest  
**Timeout**: 10 minutes  
**Permissions**:
- `contents: read` (check code)
- `checks: write` (create check annotations)
- `pull-requests: write` (comment on PRs)

## Scheduled Runs

Daily validation at **2 AM UTC**:
```yaml
schedule:
  - cron: '0 2 * * *'
```

This ensures your project health is continuously monitored even without code changes.

## Artifacts

All reports are uploaded to GitHub Actions artifacts:
- **Name**: `health-reports`
- **Files**: 4 JSON reports
- **Retention**: 30 days

Access via: Actions → Health Check → Run details → Artifacts

## Documentation

- **Full Workflow Details**: `workflows/health-check.yml` (in this directory)
- **Health Check Engine**: `_core/health_check.py`
- **AHP Details**: `_core/agent_handshake.py`
- **Diagnostics**: `_core/diagnostics_test.py`
- **Confidence Evaluation**: `_core/agent_confidence.py`

## Troubleshooting

### Workflow Fails with "State: MISCONFIGURED"
1. Check `.spec.config` syntax (JSON)
2. Verify `.sdd/governance-core.json` exists
3. Ensure `_core/` directory is present

### Workflow Fails with "State: NOT_CONNECTED"
1. Create `.spec.config` file
2. Initialize `.sdd/` directory structure
3. Run PHASE 0 onboarding

### Artifacts Not Found
- Check GitHub Actions run logs
- Verify upload step completed
- Check 30-day retention hasn't expired

---

**Version**: 1.0 | **Status**: ✅ Production Ready  
**Last Updated**: 2026-04-26  
**Author**: SDD Architecture Team
