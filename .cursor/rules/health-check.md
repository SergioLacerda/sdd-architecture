# Cursor: SDD Architecture Health Check Rule

**Status**: Enables implicit context validation for Cursor IDE before technical responses.

## Rule Definition

```yaml
name: "SDD Health Check"
description: "Validates SDD Architecture project health before technical operations"
trigger: "technical_context"
handler: "_core/agent_handshake.py"
```

## Semantic Trigger Patterns

This rule activates when user input contains **technical context keywords**:

### Triggers Activation ✅
- "estou conectado ao sdd-architecture?" → Technical query
- "como estruturar um novo componente?" → Implementation question
- "qual é a arquitetura do projeto?" → Architecture question
- "implemente uma nova feature" → Technical request
- "valide a estrutura .sdd" → Validation request
- Mentions of `.sdd`, `.vscode`, `.cursor`, `.ia` → Path references
- Mentions of `governance`, `seedlings`, `phases` → Domain keywords

### Suppresses Activation ❌
- "oi, tudo bem?" → Casual greeting (multi-word casual phrase)
- "obrigado pela ajuda" → Casual thanks
- "qual é seu nome?" → Personal question (no technical keywords)
- "thanks for helping" → Casual English phrase

## Rule Behavior

### Step 1: Detection
When you type a technical question, Cursor detects the context:

```
User types: "estou conectado ao sdd-architecture?"
             ↓
Cursor semantic detector runs
             ↓
Matches "estou conectado" + ".sdd" keywords
             ↓
Activation threshold reached → Execute rule
```

### Step 2: Health Check
Cursor silently invokes AHP:

```bash
python _core/agent_handshake.py --mode=silent
```

### Step 3: Response Adaptation
Based on health state, Cursor adjusts response:

```
If HEALTHY 🟢:
  "I can help with SDD architecture questions with full confidence."

If PARTIAL 🟡:
  "I can help, but note: some runtime components are incomplete.
   Run: python EXECUTION/SCRIPTS/phase-0-agent-onboarding.py"

If NOT_CONNECTED ❌:
  "I can provide general guidance. For SDD-specific advice,
   initialize the project first."
```

## Implementation Details

### File Location
- **Rule File**: `.cursor/rules/health-check.md` (this file)
- **Handler**: `_core/agent_handshake.py`
- **State Cache**: `.ai/runtime/governance-state.json`
- **Config**: `.spec.config` or `.sdd-core/spec.config`

### Handler Invocation
```python
from pathlib import Path
sys.path.insert(0, str(Path.cwd() / "_core"))
from agent_handshake import AgentHandshakeProtocol

ahp = AgentHandshakeProtocol()
result = ahp.validate(output_mode="silent", force_recheck=False)

# Use result.state for adaptive behavior
# result.confidence for response depth
# result.actions for next steps
```

### Caching Strategy
- **TTL**: 30 minutes
- **Cache File**: `.ai/runtime/governance-state.json`
- **Force Recheck**: Pass `--force` flag to override cache
- **Performance**: Cached checks complete in <10ms

## Rule States & Actions

| State | Symbol | Action | Confidence |
|-------|--------|--------|------------|
| HEALTHY | 🟢 | Proceed with full assistance | 85-100% |
| PARTIAL | 🟡 | Assist with caution, suggest fixes | 65-84% |
| NOT_INITIALIZED | ⚠️ | Suggest initialization | 50-64% |
| MISCONFIGURED | ⚠️ | Alert user, guide repair | 30-49% |
| NOT_CONNECTED | ❌ | Provide generic guidance | 0-29% |

## Example Interactions

### Scenario 1: Healthy Project
```
You: "como documentar uma seedling?"
Cursor: [Health check: HEALTHY 🟢, Confidence: 92%]
Cursor: "Based on your SDD governance structure, here's 
         the recommended documentation pattern for seedlings..."
```

### Scenario 2: Not Initialized
```
You: "valide minha estrutura .sdd"
Cursor: [Health check: NOT_INITIALIZED ⚠️, Confidence: 58%]
Cursor: "I can help validate .sdd structure. First, initialize 
         the project with: python EXECUTION/SCRIPTS/phase-0-agent-onboarding.py"
```

### Scenario 3: Casual Query
```
You: "oi, como você está?"
Cursor: [Rule not triggered - no technical keywords]
Cursor: "Hi! I'm doing well. How can I help?"
```

## Documentation & Reference

- **Full AHP Guide**: `docs/guides/HEALTH_CHECK_GUIDE.md`
- **AHP Source Code**: `_core/agent_handshake.py` (658 lines, fully documented)
- **Configuration**: `.spec.config`
- **Architecture Reference**: `context/INDEX.md`

## Maintenance

- **Version**: 1.0
- **Last Updated**: 2026-04-26
- **Status**: ✅ Active
- **Author**: SDD Architecture Team
- **Dependencies**: Python 3.8+, `_core/agent_handshake.py`

---

**Note**: This rule is agnóstic and can be adapted for any governed system, not just SDD.
