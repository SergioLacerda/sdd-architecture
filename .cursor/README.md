# .cursor Directory - Cursor IDE Seedling Configuration

This directory contains Cursor IDE-specific rules and configuration for the SDD Architecture project.

## Files

### `rules/health-check.md`
**Purpose**: Cursor native rule that implements Agent Handshake Protocol (AHP) for semantic health validation.

**Features**:
- Automatic activation on technical queries
- Suppression on casual conversation
- Confidence-based response adaptation
- Silent mode (no user-visible output)
- State-driven action recommendations

**Trigger Keywords**:
- **Activate**: "estou conectado", "código", "arquivo", ".sdd", "governance", "arquitetura"
- **Suppress**: "oi", "olá", "obrigado", casual greetings

**Example**:
```
You:   "como estruturar um novo seedling?"
Rule:  [Detects technical context → runs AHP → gets confidence]
Cursor: "Based on your SDD governance (HEALTHY, 92% confidence),
         here's the recommended seedling structure..."
```

### `rules/spec.mdc`
**Purpose**: Specification rules for domain specialization context.

## How It Works

### Semantic Detection Flow
```
User Input
  ↓
Does it have technical keywords? (.sdd, código, governance, etc)
  ├─ Yes → Has casual keywords? (oi, olá, obrigado, etc)
  │         ├─ Yes → Skip AHP
  │         └─ No → Run AHP
  └─ No → Skip AHP
```

### Confidence Scoring
Once AHP runs, Cursor adapts response based on project health:

| Confidence | Response Style |
|-----------|-----------------|
| 85-100% (HEALTHY 🟢) | Technical depth, all features available |
| 65-84% (PARTIAL 🟡) | Assist with caution, suggest fixes |
| 50-64% (NOT_INITIALIZED) | General guidance, suggest phase-0 |
| 30-49% (MISCONFIGURED) | Alert + repair suggestions |
| 0-29% (NOT_CONNECTED) | Generic assistance only |

## Manual Validation

```bash
# Check health (used by rule)
python packages/agent_handshake.py --mode=silent
# Output: 🧠 SDD: [status]

# See detailed validation
python packages/agent_handshake.py --mode=compact
# Output: Summary with 4-layer check results
```

## Integration with Cursor

1. **You type a technical question**
   ```
   You: "estou conectado ao sdd-architecture?"
   ```

2. **Rule detects technical context**
   ```
   - Keyword "estou conectado" detected ✓
   - Keyword ".sdd" detected ✓
   - No casual suppressors ✓
   → Activation threshold reached
   ```

3. **Cursor runs health check**
   ```bash
   python packages/agent_handshake.py --mode=silent
   State: HEALTHY | Confidence: 92%
   ```

4. **Cursor adapts response**
   ```
   Cursor: "🟢 I can help with SDD Architecture questions.
            Your project is fully operational. [detailed response]"
   ```

## Rule Behavior

### Technical Queries (Rule Active)
- "implementar novo código" → Active
- "qual é a estrutura .sdd?" → Active
- "como usar as seedlings?" → Active
- "governance rules" → Active

### Casual Queries (Rule Suppressed)
- "oi, tudo bem?" → Suppressed
- "qual é seu nome?" → Suppressed
- "thanks for helping" → Suppressed
- "como você está?" → Suppressed

## Caching

Health checks are cached for **30 minutes**:
```bash
# Uses cache (fast, <10ms)
python packages/agent_handshake.py --mode=silent
💾 Cached (5m old)

# Forces fresh validation
python packages/agent_handshake.py --force --mode=silent
```

## Documentation

- **Full Rule Details**: `rules/health-check.md`
- **AHP Specification**: `packages/agent_handshake.py` (658 lines, documented)
- **Configuration**: `.spec.config` or `.sdd-core/spec.config`
- **Architecture Reference**: `context/INDEX.md`

## Quick Reference

| Action | Command | Purpose |
|--------|---------|---------|
| Check Health | `python packages/agent_handshake.py --mode=compact` | See detailed status |
| Force Recheck | `python packages/agent_handshake.py --force --mode=compact` | Bypass 30min cache |
| See Full Report | `python packages/agent_handshake.py --mode=verbose` | 4-layer analysis |
| Silent Check | `python packages/agent_handshake.py --mode=silent` | Minimal output |

---

**Version**: 1.0 | **Status**: ✅ Active  
**Last Updated**: 2026-04-26  
**Author**: SDD Architecture Team
