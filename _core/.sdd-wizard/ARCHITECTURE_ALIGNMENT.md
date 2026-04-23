# Architecture Alignment: v3.0 Governance Model

**Document Version:** 3.0  
**Last Updated:** April 22, 2026  
**Status:** ✅ Aligned with CORE+CLIENT model

---

## Overview

The SDD v3.0 Wizard implements a **CORE+CLIENT governance model** that eliminates the need for predefined profiles (LITE/FULL) through user-driven customization.

**Key Principle:** Users choose which governance items to implement, not frameworks choosing for them.

---

## Governance Architecture

### ✅ What Exists: CORE+CLIENT Separation

```
.sdd-core/
├── governance-core.json          ← 4 IMMUTABLE items
│   ├── M001: Clean Architecture (HARD mandate)
│   ├── M002: Performance SLOs (HARD mandate)
│   └── [2 other CORE items]
│
├── governance-client.json        ← 151 CUSTOMIZABLE items  
│   ├── G01-G150: Soft guidelines
│   ├── G151: Optional guidelines
│   └── [rules, decisions, etc.]
│
└── [mandate.spec, guidelines.dsl] ← Source format
```

### ✅ Fingerprinting Strategy: SALT Protection

**CORE fingerprint = SALT**

```
Core Items (Immutable)
       ↓
   SHA-256 Hash (SALT)
       ↓
   Embedded in Client Metadata
       ↓
   Prevents tampering with Core
```

**Why:** CORE items define the "constitution" that cannot be bypassed.  
Client items can be customized, but CORE integrity is cryptographically verified.

---

## What Doesn't Exist: Why Profiles Are Gone

### ❌ v2.1 Model (BEFORE)

```
Framework Says:
├── LITE Profile    → 50 essential guidelines
├── FULL Profile    → All 151 guidelines  
└── ULTRA-LITE      → Just mandates (deprecated)

Problem: Users forced into predefined buckets
```

### ✅ v3.0 Model (NOW)

```
User Chooses:
├── Implement CORE mandates (M001, M002)           ← Always
├── Implement X guidelines from CLIENT (G01-G150) ← Your choice
└── Skip guidelines that don't fit your project   ← Your choice

Result: No need for profiles!
```

**Why This Works:**

1. **User autonomy** — Choose exactly what you need
2. **No artificial buckets** — Not LITE or FULL, just "what matters to us"
3. **Fingerprint protection** — CORE cannot be bypassed
4. **Scalable** — Same model works for 1-person teams and 500-person orgs

---

## Wizard Implementation

### Pipeline Overview

```
Phase 1: Validate SOURCE
├─ Check mandate.spec exists
└─ Check guidelines.dsl exists

    ↓

Phase 2: Load COMPILED
├─ Deserialize governance-core.json
├─ Deserialize governance-client.json
└─ Validate SALT fingerprints

    ↓

Phase 3: Filter Mandates (User Choice)
├─ Load all CORE items
├─ User selects which CORE to implement
└─ (Usually: all of them, since they're inegociáveis)

    ↓

Phase 4: Filter Guidelines (User Choice)
├─ Load all CLIENT items
├─ Filter by language (python/java/js)
├─ User customizes: pick which guidelines to follow
└─ (No profile filtering - that's the point!)

    ↓

Phase 5-7: Generate + Validate
├─ Create project structure
├─ Validate SALT preserved
└─ Project ready for use
```

### Key Design Decisions

#### 1. No Profile Parameter ❌
```python
# WRONG (v2.1 style):
phase_4_filter_guidelines(guidelines, language='python', profile='lite')

# RIGHT (v3.0 style):
phase_4_filter_guidelines(guidelines, language='python')
# User customization happens separately, not via predefined profiles
```

#### 2. No Priority Metadata ❌
```python
# WRONG (would enable profiles):
guidelines = {
    'G001': {'priority': 1, 'name': '...'},  # Only FULL
    'G002': {'priority': 2, 'name': '...'},  # LITE or FULL
}

# RIGHT (v3.0):
guidelines = {
    'G001': {'name': '...', 'tags': ['python']},
    'G002': {'name': '...', 'tags': ['java']},
}
# Priority comes from user implementation plan, not metadata
```

#### 3. No Version Field in Runtime Metadata ❌
```python
# WRONG (versioning implies retrocompat):
metadata = {
    'version': '3.0',
    'compiled_at': '2026-04-22T16:57:00',
}

# RIGHT (v3.0):
metadata = {
    'compiled_at': '2026-04-22T16:57:00',
    # version not needed - v3.0 is production-ready, no legacy support
}
```

---

## Governance Flow: User Perspective

### Scenario: Small Python Team (5 people)

```
$ python wizard.py --language python --output ~/my-project

🧙 SDD v3.0 Wizard - Project Generator

📋 Review Your Governance
├─ CORE Mandates (Immutable)
│  ├─ M001: Clean Architecture
│  └─ M002: Performance SLOs
│
└─ CLIENT Guidelines (Customizable)
   ├─ G001-G150: Available guidelines
   └─ Which do you want to implement?

👤 Your Customization
├─ Language: Python
├─ Mandates: M001, M002 (all CORE)
├─ Guidelines: G001, G002, G005, G010, ... (your selection)
└─ Output: ~/my-project/

✅ Generated Project
├─ .sdd/CANONICAL/mandate.spec
├─ .sdd/CANONICAL/guidelines.dsl
├─ src/
└─ tests/
```

### Scenario: Enterprise Production Service

```
Same flow, different customization:
├─ Language: Python
├─ Mandates: M001, M002 (all CORE)
├─ Guidelines: ALL G001-G150 (strict enterprise compliance)
└─ Additional rules from .sdd-core/rules/ (project-specific)
```

**Key Point:** Same framework, different customization levels - no LITE/FULL distinction needed.

---

## Alignment Checklist

- ✅ CORE items are immutable (protected by SALT)
- ✅ CLIENT items are customizable (user chooses what to implement)
- ✅ Fingerprinting validates integrity (prevents tampered governance)
- ✅ No predefined profiles (users choose what they need)
- ✅ Language filtering available (for practical narrowing)
- ✅ No version field in runtime metadata (no retrocompat required)
- ✅ Wizard respects user autonomy (doesn't force framework choices)

---

## Implementation Details

### compile_artifacts.py

**Purpose:** Convert mandate.spec and guidelines.dsl to runtime format

**Changes in v3.0:**
- Removed `version` field from metadata (no retrocompat needed)
- Generate clean JSON format (schema: compile_time + source + artifacts)
- No profile-specific compilation

### phase_4_filter_guidelines.py

**Purpose:** Filter guidelines by language (python/java/js)

**Changes in v3.0:**
- Removed `profile` parameter
- Language filtering remains (practical, not framework-imposed)
- User customization handled separately (not in wizard)

### wizard.py

**Purpose:** CLI orchestrator for project generation

**Changes in v3.0:**
- Removed `--profile` CLI flag
- Language selection still available (`--language`)
- Mandates still customizable (`--mandates`)

---

## FAQ

### Q: How do users customize without LITE/FULL profiles?

**A:** They choose which guidelines to implement in their `.sdd/client/governance-client.json`. The wizard generates the base structure; users adapt it.

### Q: What if a user only wants essential guidelines?

**A:** They don't implement the rest. CORE mandates (M001, M002) are always active; everything else is optional. No predefined "LITE" package needed.

### Q: Why no version in metadata?

**A:** v3.0 is production-ready with no legacy support. There's no versioning strategy that would justify adding a `version` field. It would only add noise to the spec.

### Q: How is governance integrity protected?

**A:** SALT strategy: CORE fingerprint is embedded in CLIENT metadata. If someone tampers with CORE items, the SALT check fails, preventing invalid overrides.

### Q: Can enterprise teams use this?

**A:** Yes. They implement all guidelines (or a strict subset) + their own rules from `.sdd-core/rules/`. The model scales from solo dev to 500-person org.

---

## Migration Notes

### From v2.1 to v3.0

| Feature | v2.1 | v3.0 | Migration |
|---------|------|------|-----------|
| Profiles (LITE/FULL) | ✅ Yes | ❌ No | Remove profile param from calls |
| `--profile` CLI flag | ✅ Yes | ❌ No | Use `--language` instead |
| Priority metadata | ❌ No | ❌ No | Not added (not needed) |
| Version in metadata | ⚠️ Sometimes | ❌ No | Remove from compile |
| CORE+CLIENT separation | ❌ No | ✅ Yes | New in v3.0 |
| Fingerprinting (SALT) | ❌ No | ✅ Yes | New in v3.0 |

---

## Summary

**The SDD v3.0 Wizard is fully aligned with the CORE+CLIENT governance model.**

✅ **No profiles needed** — Users choose what to implement  
✅ **CORE protected by SALT** — Immutable constitution preserved  
✅ **CLIENT customizable** — User autonomy maximized  
✅ **Scaled-agnostic** — Works for teams of any size  
✅ **Production-ready** — No legacy support needed

Profiles were a framework decision; v3.0 returns that decision to users.
