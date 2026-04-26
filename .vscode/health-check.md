# VS Code: SDD Architecture Health Check

**Purpose**: Validates SDD Architecture project health on startup or before technical operations.

**Trigger**: Automatically invoked via VS Code settings when:
- Opening workspace for first time in session
- Running AI chat commands with technical intent
- Detecting context keywords (`.sdd`, `governance`, `architecture`, etc.)

## Implementation

This seedling integrates **Agent Handshake Protocol (AHP)** from `_core/agent_handshake.py`.

### Health Check Flow

```
User opens VS Code / starts coding
  ↓
VS Code loads workspace
  ↓
AHP semantic detector runs
  ↓
Is this a technical/contextual question?
  ├─ YES → Run validation → Show status (silent/compact/verbose)
  └─ NO  → Skip → Continue normally
```

### Quick Status

To manually check health:

```bash
# Silent (minimal output)
python _core/agent_handshake.py --mode=silent

# Compact (summary)
python _core/agent_handshake.py --mode=compact

# Verbose (detailed report)
python _core/agent_handshake.py --mode=verbose

# Force fresh check (bypass cache)
python _core/agent_handshake.py --force --mode=compact
```

## Health States

| State | Symbol | Meaning | Action |
|-------|--------|---------|--------|
| HEALTHY | 🟢 | Fully operational | Proceed normally |
| PARTIAL | 🟡 | Runtime incomplete | Run suggested fix |
| NOT_INITIALIZED | ⚠️ | Phase 0 needed | Execute PHASE_0_ENTRY_POINTS |
| MISCONFIGURED | ⚠️ | Config broken | Review `.spec.config` |
| NOT_CONNECTED | ❌ | No governance | Proceed with caution |

## Validation Details

The health check validates 4 layers:

1. **Discovery Layer** - Is governance present?
   - `.spec.config` detected
   - `.sdd/` directory structure
   - `governance-core.json` readable

2. **Link Validation Layer** - Are connections valid?
   - Config parses correctly
   - `spec_path` accessible
   - `_core` framework present

3. **Runtime Validation Layer** - Is it operational?
   - `.ai/runtime/` initialized
   - State cache functional
   - PHASE 0 marker exists

4. **Governance Health Layer** - Is it healthy?
   - `governance-core.json` integrity
   - Critical subsystems present
   - Structural coherence

## Caching

Health checks are cached for **30 minutes** to avoid redundant validation.

```bash
# Check uses cache if available
python _core/agent_handshake.py --mode=compact
💾 Cached (8s old)

# Force fresh validation
python _core/agent_handshake.py --force --mode=compact
```

## AI Copilot Integration

When working with VS Code Copilot or similar AI:

```
You: "estou conectado ao sdd-architecture?"
AI: [AHP runs silently]
AI: "🟢 HEALTHY - I can assist with technical questions about the architecture."

You: "como codificar um novo componente?"
AI: [Uses AHP confidence score for response depth]
AI: "Based on your SDD governance, here's the recommended approach..."
```

## Documentation

- **Full Guide**: `docs/guides/HEALTH_CHECK_GUIDE.md`
- **AHP Specification**: See `_core/agent_handshake.py` (inline docs)
- **Configuration**: `.spec.config` or `.sdd-core/spec.config`

---

**Version**: 1.0 | **Last Updated**: 2026-04-26 | **Status**: ✅ Operational
