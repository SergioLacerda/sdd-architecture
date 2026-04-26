# .ia Directory - AI Integration Seedlings

This directory contains system prompts and integration files for AI assistants (Claude, GPT-4, Copilot, etc.).

## Files

### `system-prompt.md`
**Purpose**: Universal system prompt for any AI assistant working with the SDD Architecture project.

**Usage**:
- Load at the beginning of AI sessions
- Provides context about project structure, governance, and phases
- Defines when to run Agent Handshake Protocol (AHP)
- Explains how to adapt responses based on project health

**Integration Points**:
- VS Code Copilot chat context
- Claude system message
- GPT-4 system prompt
- Any custom AI integration

## How AHP Works

When you ask a technical question about the project, the AI:

1. **Detects Context**: Is this a technical/architectural question?
   - Keywords: "estou conectado", "código", ".sdd", "governance"
   - Suppresses: "oi", "obrigado", casual greetings

2. **Runs Validation**: Checks project health (cached for 30 min)
   ```bash
   python _core/agent_handshake.py --mode=silent
   ```

3. **Adapts Response**: Uses confidence score (0-100%)
   - HEALTHY 🟢 (85-100%): Full technical assistance
   - PARTIAL 🟡 (50-84%): Assist with caution + suggestions
   - NOT_CONNECTED ❌ (0-49%): General guidance

## Example Workflow

```
You:    "estou conectado ao sdd-architecture?"
AI:     [AHP runs silently: state=HEALTHY, confidence=92%]
AI:     "🟢 Yes, you're fully connected to the SDD Architecture 
         project. I can assist with governance, seedlings, phases, 
         and implementation patterns."

You:    "como criar uma nova seedling?"
AI:     "Here's the recommended approach based on your SDD governance..."
         [Uses full confidence for technical depth]
```

## Documentation

- **Full AHP Guide**: See `docs/guides/HEALTH_CHECK_GUIDE.md`
- **AHP Source Code**: `_core/agent_handshake.py` (658 lines)
- **System Prompt Details**: Read `system-prompt.md` in this directory

---

**Version**: 1.0 | **Status**: ✅ Production Ready
