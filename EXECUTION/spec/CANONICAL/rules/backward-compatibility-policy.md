# 📋 Backward Compatibility Policy v1.0

**Effective Date:** 2026-04-19  
**Status:** ✅ Production-Ready  
**Scope:** All public APIs and critical dependencies  
**Owner:** Chief Architect

---

## 🎯 PURPOSE

This policy defines when breaking changes are allowed, how they must be communicated, and what support timeline applies.

**Core Principle:** Breaking changes are expensive. Avoid them. When necessary, support old versions in parallel for at least 6 months.

---

## 📊 SEMANTIC VERSIONING RULES

All public APIs follow Semantic Versioning (SemVer): MAJOR.MINOR.PATCH

### PATCH Version (1.0.x → 1.0.1)
**Changes allowed:**
- ✅ Bug fixes
- ✅ Security patches
- ✅ Performance improvements
- ✅ Internal refactoring

**Breaking?** NO
**Release process:** Direct merge + immediate deployment
**User action:** None (automatic update safe)

### MINOR Version (1.0.0 → 1.1.0)
**Changes allowed:**
- ✅ New features (backward compatible)
- ✅ New optional parameters
- ✅ New endpoints
- ✅ Deprecated methods (with warnings)

**Breaking?** NO
**Release process:** Feature branch → code review → merge → deployment
**User action:** None (automatic update safe)

### MAJOR Version (1.0.0 → 2.0.0)
**Changes allowed:**
- ⚠️ Remove deprecated features
- ⚠️ Change parameter types
- ⚠️ Change error codes
- ⚠️ Remove endpoints
- ⚠️ Restructure data formats

**Breaking?** YES
**Release process:** RFC → Architecture review → feature branch → code review → merge → deployment
**User action:** REQUIRED (manual upgrade needed)

---

## 🚨 BREAKING CHANGE DEFINITION

A breaking change is ANY modification that:

1. **Changes existing API contract**
   - Parameter type changed: `int` → `string`
   - Parameter removed
   - Return type changed
   - Required field added (no default)

2. **Changes expected behavior**
   - Response time changes > 2x
   - Error codes renumbered
   - Response format restructured
   - Endpoint moved or removed

3. **Changes system assumptions**
   - New required configuration
   - Removes authentication method
   - Changes data consistency model
   - Removes supported storage backend

4. **Changes dependency contracts**
   - Updates major version of core dependency
   - Removes support for Python version
   - Changes database schema incompatibly

---

## 📜 DEPRECATION PROCESS

### Stage 1: Announce Deprecation (Release N)

**In Release N:**

```python
import warnings

@deprecated(version="1.5.0", removed_in="2.0.0", 
           reason="Use new_function() instead")
def old_function():
    """This function is deprecated."""
    warnings.warn(
        "old_function() is deprecated. Use new_function() instead. "
        "Will be removed in 2.0.0.",
        DeprecationWarning,
        stacklevel=2
    )
    # ... implementation
```

**User sees:** `DeprecationWarning` in logs/console

**Timeline:** 6 months advance notice minimum

**Documentation:** 
- Update API docs: "⚠️ DEPRECATED - Use X instead"
- Update changelog: "Deprecation notice: ..."
- Update README migration guide

### Stage 2: Grace Period (Releases N+1 → N+5)

**Behavior:**
- Old function still works
- Warning shown on every use
- Performance not degraded
- No new development on deprecated code

**User action:** Migrate to new function (optional but encouraged)

**Timeline:** 6+ months (through multiple releases)

### Stage 3: Final Removal (Release N+6)

**In Major Release:**
- Remove deprecated code
- Remove warnings
- Document migration path
- Provide upgrade guide

**User action:** REQUIRED for versions after N+6

---

## 🔄 API VERSIONING STRATEGY

### URL-Based Versioning (Recommended)

```
/api/v1/campaigns    # Old API (deprecated)
/api/v2/campaigns    # New API (current)
/api/v3/campaigns    # Future API
```

**Benefits:**
- Clear version in URL
- Easy to route differently
- Old clients work unchanged
- New clients use new version

**Implementation:**

```python
# src/interfaces/http/routers/v1.py
@router.get("/campaigns")
async def list_campaigns_v1(skip: int = 0, limit: int = 10):
    # Old implementation
    return campaigns

# src/interfaces/http/routers/v2.py
@router.get("/campaigns")
async def list_campaigns_v2(
    skip: int = 0, 
    limit: int = 10,
    filter: Optional[str] = None  # New parameter
):
    # New implementation with backward-compat shim
    return campaigns_with_filter(skip, limit, filter)

# src/interfaces/http/main.py
app.include_router(v1.router, prefix="/api/v1")
app.include_router(v2.router, prefix="/api/v2")
```

### Header-Based Versioning (Alternative)

```
GET /campaigns
Accept-Version: 1.0.0

# or

GET /campaigns
API-Version: 2
```

---

## 🛡️ BACKWARD COMPATIBILITY GUARANTEES

### Data Format Compatibility

**Guarantee:** Old data always readable by new code

```python
# Old format (v1)
{ "user_id": 123, "campaign": "c1" }

# New format (v2) - add optional field
{ 
    "user_id": 123, 
    "campaign": "c1",
    "tenant_id": "default"  # Optional, defaults to "default"
}

# Migrations handle both
if "tenant_id" not in data:
    data["tenant_id"] = "default"
```

### API Response Compatibility

**Guarantee:** Old fields always present in new responses

```python
# Old response (v1)
{
    "id": 1,
    "name": "Dragon",
    "hp": 100
}

# New response (v2) - add new field
{
    "id": 1,
    "name": "Dragon",
    "hp": 100,
    "max_hp": 150  # New field, doesn't break old clients
}

# Old clients ignore max_hp (not in schema)
# New clients can use it
```

### Error Code Compatibility

**Guarantee:** Error codes don't change meaning

```python
# Never do this (breaking):
# 400 meant "invalid input" in v1
# Don't change it to mean "rate limited" in v2

# Instead:
# 400 = invalid input (always)
# 429 = rate limited (new in v2)
```

---

## 📅 SUPPORT TIMELINE

### Version Support Schedule

```
Release Timeline:
├─ v1.0.0: Jan 2026  (Release)
├─ v1.5.0: Jul 2026  (Deprecation: old_feature)
├─ v2.0.0: Jan 2027  (Major: old_feature removed)
│   └─ v1.0.0 - v1.x: Receive security patches only
├─ v2.5.0: Jul 2027  (New deprecation)
└─ v3.0.0: Jan 2028  (Next major)

Deprecated features timeline:
- old_feature deprecated in v1.5.0 (announced)
- old_feature warnings in v1.6.0, v1.7.0, v1.8.0 (grace period)
- old_feature removed in v2.0.0 (major version)

Total support: 12+ months (6 month notice + 6 month grace)
```

### Support Tiers

| Version | Status | Support | Security Patches |
|---------|--------|---------|------------------|
| v3.x | Stable | Full | ✅ Yes |
| v2.x | LTS | Bug fixes only | ✅ Yes |
| v1.x | EOL | None | ⚠️ Critical only |
| v0.x | Alpha | None | ❌ No |

---

## 🔧 BREAKING CHANGE APPROVAL PROCESS

### Step 1: Document the Change (RFC)

Create `/docs/ia/DEVELOPMENT/breaking-changes/breaking-change-NAME.md`:

```markdown
# Breaking Change: Remove old_function()

## Summary
Remove deprecated old_function() and require use of new_function()

## Affected APIs
- DELETE: GET /api/v1/old-endpoint
- CHANGE: PATCH /campaigns response format

## Deprecation Removed
- Announced in v1.5.0 (Jan 2026)
- Deprecated in v1.6.0 - v1.x (Jan 2026 - Dec 2026)
- Removed in v2.0.0 (Jan 2027)

## Migration Path
See docs/MIGRATION_v1_to_v2.md

## Backward Compat Shim
None - v2.0.0 requires code changes

## Risk Level
🟡 Medium - Affects old_function() users (10% of users)
```

### Step 2: Architect Review

- Chief Architect reviews RFC
- Questions addressed
- Migration guide approved

### Step 3: Feature Development

- Create feature branch: `breaking-change/remove-old-function`
- Implement change
- Add removal date to docs
- Update CHANGELOG

### Step 4: Code Review

- Full team review
- Verify migration path documented
- Check for undocumented side effects

### Step 5: Release

- Merge to main
- Tag as MAJOR version
- Deploy with announcement
- Send notification to users

---

## 📢 USER COMMUNICATION

### Deprecation Announcement

**Timing:** When deprecation added to code

**Medium:** 
- Email to active users
- Blog post
- Changelog entry
- In-app warning

**Template:**

```
Subject: DEPRECATION NOTICE: old_function() will be removed

Dear API User,

We are deprecating old_function() effective v1.5.0 (released Jan 2026).

📋 What's changing:
- old_function() will be removed in v2.0.0 (Jan 2027)

✅ What to do:
1. Review: docs/MIGRATION_v1_to_v2.md
2. Update your code to use new_function()
3. Test against v2.0.0-beta
4. Deploy updated code before Jan 2027

❓ Questions?
- Check FAQ: docs/faq.md#old_function_removal
- Email support@example.com

Timeline:
- v1.5.0 (Jan 2026): Deprecation warnings start
- v1.6.0 - v1.9.0: Grace period (updates recommended)
- v2.0.0 (Jan 2027): Feature removed (upgrade required)

We recommend upgrading to v2.0.0 immediately after release.

Best regards,
The Development Team
```

### Migration Guide

**Location:** `/docs/migration/MIGRATION_v1_to_v2.md`

**Contains:**
- What's breaking
- Why it's breaking
- How to fix your code
- Example before/after
- Troubleshooting

**Example:**

```markdown
# Migration Guide: v1 → v2

## Breaking Changes

### 1. old_function() Removed

**Before (v1):**
```python
from api import old_function
result = old_function(x=5)
```

**After (v2):**
```python
from api import new_function
result = new_function(value=5)  # Parameter renamed
```

### 2. Response Format Changed

**Before (v1):**
```json
{ "id": 1, "data": "value" }
```

**After (v2):**
```json
{ "id": 1, "content": "value", "version": 2 }
```

Update your parsing code to use `content` instead of `data`.

## Testing

Use v2.0.0-beta to test before final upgrade:

```bash
pip install --upgrade api==2.0.0-beta
pytest tests/  # Run your tests
```

## Support

- Questions? Email support@example.com
- Bug? Report at github.com/project/issues
```

---

## 🔍 TOOLS & AUTOMATION

### Backward Compatibility Checker

```python
# tools/check_backward_compat.py

def check_api_changes(old_spec, new_spec):
    """Check for breaking changes between API versions."""
    
    breaking_changes = []
    
    # Check removed endpoints
    old_endpoints = {e["path"] for e in old_spec}
    new_endpoints = {e["path"] for e in new_spec}
    
    removed = old_endpoints - new_endpoints
    if removed:
        breaking_changes.append(f"Removed endpoints: {removed}")
    
    # Check parameter changes
    for endpoint in old_endpoints & new_endpoints:
        old_params = get_parameters(old_spec, endpoint)
        new_params = get_parameters(new_spec, endpoint)
        
        # Required parameters added = breaking
        added_required = {
            p for p in new_params 
            if p not in old_params and p.required
        }
        if added_required:
            breaking_changes.append(
                f"Required params added to {endpoint}: {added_required}"
            )
        
        # Response fields removed = breaking
        old_response = get_response(old_spec, endpoint)
        new_response = get_response(new_spec, endpoint)
        removed_fields = set(old_response) - set(new_response)
        if removed_fields:
            breaking_changes.append(
                f"Response fields removed from {endpoint}: {removed_fields}"
            )
    
    return breaking_changes

# Run in CI/CD
breaking = check_api_changes(old_api_spec, new_api_spec)
if breaking:
    print("ERROR: Breaking changes detected:")
    for change in breaking:
        print(f"  - {change}")
    exit(1)
```

### Deprecation Detector

```python
# tools/deprecation_stats.py

def count_deprecations():
    """Count active deprecation warnings."""
    
    deprecated = []
    
    for file in find_python_files("src/"):
        for decorator in find_decorators(file, "@deprecated"):
            deprecated.append({
                "file": file,
                "function": extract_function_name(decorator),
                "removed_in": extract_version(decorator),
            })
    
    # Group by removal version
    by_version = group_by(deprecated, "removed_in")
    
    # Alert if many deprecations in same version
    for version, items in by_version.items():
        if len(items) > 5:
            print(f"⚠️  WARNING: {len(items)} deprecations in {version}")
    
    return deprecated
```

### Version Compatibility Matrix

```bash
# Generate compatibility matrix
python tools/generate_compat_matrix.py

# Output:
# 
# API Client Compatibility Matrix
# ┌─────────────────────────────────┐
# │       │  v1.0  │  v1.5  │  v2.0 │
# ├─────────────────────────────────┤
# │  v1.0 │   ✅    │   ✅    │   ❌  │
# │  v1.5 │   ✅    │   ✅    │   ❌  │
# │  v2.0 │   ❌    │   ❌    │   ✅  │
# └─────────────────────────────────┘
```

---

## 📊 METRICS & MONITORING

### Track Deprecation Usage

```python
# metrics.py

deprecation_usage = Counter(
    'deprecated_function_calls_total',
    'Number of calls to deprecated functions',
    ['function_name', 'version']
)

# In deprecated function:
@deprecated(removed_in="2.0.0")
def old_function():
    deprecation_usage.labels(
        function_name='old_function',
        version='1.5.0'
    ).inc()
```

### Measure Migration Progress

```bash
# What % of users on old API version?
SELECT 
    api_version, 
    COUNT(*) as client_count,
    COUNT(*) / SUM(COUNT(*)) OVER () as percentage
FROM api_clients
GROUP BY api_version

# Results:
# api_version │ client_count │ percentage
# ────────────┼──────────────┼────────────
#      v1.0   │    10        │    10%
#      v1.5   │    50        │    50%
#      v2.0   │    40        │    40%

# 50% of users still on v1.5 - need migration reminder
```

---

## ✅ CHECKLIST: BREAKING CHANGE APPROVAL

Before a breaking change can be approved:

- [ ] RFC written and reviewed
- [ ] Migration guide prepared
- [ ] Deprecation period started (6+ months before removal)
- [ ] Users notified via email/blog
- [ ] Feature branch created and reviewed
- [ ] Tests verify both old and new behavior
- [ ] Backward compat shim provided (if possible)
- [ ] Documentation updated
- [ ] CHANGELOG entry added
- [ ] Metrics show <10% of users affected
- [ ] Support team trained on migration
- [ ] CEO/Legal approves if revenue impact
- [ ] Release notes prepared

---

## 🎯 EXCEPTIONS & APPEALS

### When Breaking Changes Allowed Without 6-Month Notice

1. **Security Fix**
   - Breaking change required to patch vulnerability
   - Requires security team + architect approval
   - 2-week notice minimum
   - Example: Remove insecure authentication method

2. **Critical Bug Fix**
   - Current behavior causes data loss or corruption
   - Requires architect + CEO approval
   - 1-week notice minimum
   - Example: Fix that was causing campaign data loss

3. **Beta/Alpha APIs**
   - APIs marked `@beta` or `@alpha` have no compatibility guarantees
   - Deprecation process does not apply
   - Break freely during beta phase

### Appeal Process

Developer disagrees with 6-month minimum?

1. Document rationale in RFC
2. Request architect review
3. Present business case (time-to-market, user impact)
4. Executive decision (CEO or CTO)
5. Minimum reduced if compelling reasons

---

## 📞 CONTACT & GOVERNANCE

**Questions about backward compatibility policy?**
- Email: architecture@example.com
- Slack: #architecture-decisions

**Updating this policy?**
- Propose changes via RFC
- Needs architect + engineering lead approval
- Document rationale

**Violation Reports?**
- Email: compliance@example.com
- All violations reviewed within 1 week

---

**Version:** 1.0 (Initial Release)  
**Status:** ✅ Approved  
**Effective:** 2026-04-19  
**Next Review:** 2026-10-19 (6 months)  
**Owner:** Chief Architect  
**Enforcement:** Mandatory for all breaking changes
