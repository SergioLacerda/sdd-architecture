# IA-FIRST Execution Rules — game-master-api Specialization

**Project:** game-master-api  
**Version:** 1.0  
**Generated:** 2026-04-19T12:55:46.101988  
**Based on:** /EXECUTION/spec/CANONICAL/rules/ia-rules.md

---

## 📋 Overview

This document specifies the 16 execution protocols from CANONICAL adapted for game-master-api.

**Critical ports:** StoragePort, LLMPort  
**Concurrent threads:** WorkerThread  
**Max parallel work:** 4 threads

---

## ✅ Protocol Specializations (16 Total)

### Protocol 1: Read CANONICAL Rules First

**Generic:** "Every agent session starts by reading ia-rules.md"

**game-master-api requirement:**
```
Every agent session MUST:
  1. Read: /EXECUTION/spec/CANONICAL/rules/ia-rules.md (5 min)
  2. Read: /EXECUTION/spec/CANONICAL/rules/constitution.md (5 min)
  3. Read: /EXECUTION/spec/custom/game-master-api/SPECIALIZATIONS/ia-rules-game-master-api-specific.md (3 min)
  4. Choose task PATH: A/B/C/D from QUICK_START.md

Result: Agent understands both generic and game-master-api-specific rules
Time: ~15 min before starting work
```

---

### Protocol 2-16: [Additional Protocols]

[Each protocol would follow similar specialization pattern...]

---

## 🔗 References

- Generic rules: [CANONICAL/rules/ia-rules.md](../../CANONICAL/rules/ia-rules.md)
- Constitutional specialization: [constitution-game-master-api-specific.md](./constitution-game-master-api-specific.md)
- Configuration: [SPECIALIZATIONS_CONFIG.md](./SPECIALIZATIONS_CONFIG.md)

