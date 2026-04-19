# 🔗 INTEGRATION — Add Your Project to SDD Framework

**For:** Teams integrating a new (or existing) project with SDD governance  
**Duration:** 30 minutes  
**Complexity:** Simple (no decisions, just follow steps)  
**Outcome:** Project ready for development with SDD AGENT_HARNESS  

---

## 🎯 What is Integration?

Integration = copying SDD templates to your project + configuring a single reference file.

After integration:
- ✅ Your project knows where SDD framework lives
- ✅ Developers can use AGENT_HARNESS workflow
- ✅ Governance hooks are active
- ✅ Project-specific docs can be created

---

## 🚀 5-Step Process

| Step | What | Time |
|------|------|------|
| **1** | Setup project structure | 5 min |
| **2** | Copy templates from INTEGRATION/templates/ | 5 min |
| **3** | Edit `.spec.config` (2 lines!) | 2 min |
| **4** | Run validation script | 5 min |
| **5** | Git commit | 3 min |

**Total:** 20 minutes (5 min buffer = 30 min guaranteed)

---

## 📋 Before You Start

Make sure you have:
- ✅ Your project repository (git init already done)
- ✅ Access to this sdd-archtecture repo
- ✅ Python 3.8+ installed (for validation script)
- ✅ 30 minutes uninterrupted time

---

## ✅ Success Criteria

After completing these 5 steps, your project should have:

```
your-project/
├── .spec.config                    ← Points to ../sdd-archtecture
├── .github/copilot-instructions.md ← From templates/
├── .vscode/ai-rules.md             ← From templates/
├── .pre-commit-config.yaml         ← From templates/
├── scripts/setup-precommit-hook.sh ← From templates/
├── .cursor/rules/spec.mdc          ← From templates/
└── .ai/
    ├── context-aware/
    │   ├── task-progress/
    │   ├── analysis/
    │   └── runtime-state/
    └── runtime/
        ├── README.md
        ├── search-keywords.md
        ├── spec-canonical-index.md
        └── spec-guides-index.md
```

And:
- ✅ `.spec.config` correctly points to sdd-archtecture
- ✅ Validation script ran successfully
- ✅ Git shows new files ready to commit
- ✅ Developer can read docs in `.ai/runtime/`

---

## 📍 Next: Follow the Checklist

[→ INTEGRATION/CHECKLIST.md](./CHECKLIST.md) — Step-by-step with commands

Or go directly to a specific step:
- [STEP_1.md](./STEP_1.md)
- [STEP_2.md](./STEP_2.md)
- [STEP_3.md](./STEP_3.md)
- [STEP_4.md](./STEP_4.md)
- [STEP_5.md](./STEP_5.md)

---

**Status:** Ready to integrate  
**Support:** See STEP_X_* files for troubleshooting
