# .vscode Directory - VS Code Seedling Triggers

This directory contains VS Code-specific configuration and integration files for the SDD Architecture project.

## Files

### `health-check.md`
**Purpose**: Seedling trigger for VS Code integration of Agent Handshake Protocol (AHP).

**Features**:
- Validates project health on workspace startup
- Supports 3 output modes (silent/compact/verbose)
- Caches validation for 30 minutes
- Semantic detection of technical vs casual queries
- Integrates with VS Code Copilot

**Quick Commands**:
```bash
# Check health status
python _core/agent_handshake.py --mode=compact

# Force fresh validation
python _core/agent_handshake.py --force --mode=compact

# See full report
python _core/agent_handshake.py --mode=verbose
```

### `ai-rules.md`
**Purpose**: AI assistant rules and behavior guidelines for VS Code Copilot.

**References**: The health-check seedling for contextual validation.

## Integration with Copilot

When you use VS Code Copilot:

1. **Technical Query Detection**
   - You ask: "estou conectado ao sdd-architecture?"
   - Copilot detects: "technical + context keywords"
   - Runs: AHP validation silently

2. **Health-Based Response**
   - State: HEALTHY 🟢
   - Confidence: 92%
   - Response: "Full SDD Architecture assistance available"

3. **Non-Technical Query**
   - You ask: "oi, como você está?"
   - Copilot detects: "casual greeting, no technical keywords"
   - Skips: AHP validation
   - Response: "Hi! How can I help?"

## Quick Start

1. **Open VS Code** in the sdd-architecture directory
2. **Ask Copilot** a technical question about the project
3. **Copilot runs AHP** automatically (in background, silent mode)
4. **Get intelligent response** based on project health

## Manual Health Check

```bash
# From project root
python _core/agent_handshake.py --mode=silent
# Output: 🧠 SDD: [status]

python _core/agent_handshake.py --mode=compact
# Output: Detailed check list with recommendations

python _core/agent_handshake.py --mode=verbose
# Output: Full 4-layer validation report
```

## Health States

| State | Symbol | Meaning |
|-------|--------|---------|
| HEALTHY | 🟢 | Fully operational, proceed with confidence |
| PARTIAL | 🟡 | Runtime incomplete, see suggestions |
| NOT_INITIALIZED | ⚠️ | Phase 0 setup needed |
| MISCONFIGURED | ⚠️ | Configuration broken, review `.spec.config` |
| NOT_CONNECTED | ❌ | No governance detected, use general guidance |

## Documentation

- **Full Guide**: `.vscode/health-check.md` (in this directory)
- **AHP Details**: `_core/agent_handshake.py`
- **Architecture**: `context/INDEX.md`

---

**Version**: 1.0 | **Status**: ✅ Active
