# 📚 Runtime Guides Index

**Location:** `docs/ia/guides/runtime/`  
**Purpose:** Show how agents create and use dynamic context-aware  
**Audience:** AI Agents, developers  

---

## 📖 Files in This Guide

### 1. **README.md** (START HERE)
- Overview of context-aware pattern
- How it differs from SPECIALIZATIONS
- Quick 2-minute start guide
- 3 core concepts

**Read this first to understand what context-aware is.**

---

### 2. **CONTEXT_AWARE_USAGE.md** (MAIN GUIDE)
- Complete agent workflow
- How to create task progress files
- How to document analysis
- How to track runtime state
- Pre-flight checklist
- Common mistakes

**Read this when starting work on a project.**

---

### 3. **example-task-progress.md** (TEMPLATE)
- Real example: Agent starts, works, completes
- Shows task-progress structure
- Demonstrates handoff between agents
- Copy this structure for your tasks

**Use this as a template for your task tracking.**

---

### 4. **example-analysis.md** (COMING SOON)
- Real example: Agent discovers issue and documents
- Shows how to analyze and report findings
- Demonstrates how next agent reuses findings

---

### 5. **example-runtime-state.md** (COMING SOON)
- Real example: Tracking performance metrics
- Showing system health over time
- Documenting active threads

---

## 🎯 How to Use These Guides

### For New Projects

1. **Copy the structure:**
   ```bash
   cp -r /path/to/spec-architecture/.ai your-project/.ai
   ```

2. **Read README.md** in your new project:
   ```bash
   cat your-project/.ai/context-aware/README.md
   ```

3. **Read this guide's CONTEXT_AWARE_USAGE.md:**
   ```bash
   cat docs/ia/guides/runtime/CONTEXT_AWARE_USAGE.md
   ```

4. **Use the example templates** as you work

---

### For Existing Projects (like rpg-narrative-server)

1. **Check that .ai/context-aware/ exists:**
   ```bash
   ls -la .ai/context-aware/
   ```

2. **Read the project README:**
   ```bash
   cat .ai/context-aware/README.md
   ```

3. **Check current state:**
   ```bash
   cat .ai/context-aware/task-progress/_current.md
   cat .ai/context-aware/analysis/_current-issues.md
   ```

4. **Add to current task progress:**
   ```bash
   vi .ai/context-aware/task-progress/_current.md
   # Add your task
   ```

---

## 📊 Context-Aware at a Glance

```
What is it?
  Folder with Markdown files for dynamic project context
  
Where is it?
  .ai/context-aware/ in each project
  
What goes in it?
  - Task progress (what's being worked on)
  - Analysis (discoveries and issues found)
  - Runtime state (live system metrics)
  
When to update?
  During work (at start and end of each task)
  
Who updates it?
  AI agents and developers
  
What's the benefit?
  - No duplicate investigation between sessions
  - Clear handoff between agents
  - Shared knowledge across team
  - Persistent context (survives session transitions)
  
Is it different from SPECIALIZATIONS?
  YES! SPECIALIZATIONS are static (how we build)
  context-aware is dynamic (what we learned today)
```

---

## 🔄 Quick Workflow Reminder

### Session 1: You Start Work
```bash
# 1. Check what's active
cat .ai/context-aware/task-progress/_current.md

# 2. Read issues
cat .ai/context-aware/analysis/_current-issues.md

# 3. Review state
cat .ai/context-aware/runtime-state/_current.md

# 4. Begin work (you're caught up!)
```

### During Work: You Discover Something
```bash
# 1. Document the finding
cat > .ai/context-aware/analysis/[issue-name].md << 'EOF'
[Your analysis]
EOF

# 2. Update current issues
vi .ai/context-aware/analysis/_current-issues.md

# 3. Commit
git add .ai/context-aware/
git commit -m "📝 Document issue: [name]"
```

### Session End: You Finish a Task
```bash
# 1. Mark task complete
vi .ai/context-aware/task-progress/_current.md

# 2. Update analysis
vi .ai/context-aware/analysis/_current-issues.md

# 3. Update runtime state
vi .ai/context-aware/runtime-state/_current.md

# 4. Commit
git add .ai/context-aware/
git commit -m "✅ Task complete: [name]"

# 5. Next agent will pick this up!
```

---

## 🎓 Key Files Outside This Folder

**In spec-architecture:**
- `docs/ia/CANONICAL/rules/ia-rules.md` — Framework rules (immutable)
- `docs/ia/CUSTOM/[PROJECT]/SPECIALIZATIONS/` — Project patterns (static)

**In each project:**
- `.ai/context-aware/` — Project discoveries (dynamic) ← YOU ARE HERE
- `docs/ia/` or referenced via `.spec.config` — General architecture

**Relationship:**
```
CANONICAL (immutable rules)
  ↓
SPECIALIZATIONS (project patterns, static)
  ↓
context-aware (runtime discoveries, dynamic) ← THIS GUIDE
  ↓
execution-state (thread assignment, per-task)
```

---

## ✅ Checklist: Understanding Context-Aware

- [ ] I know what context-aware is (dynamic ≠ static)
- [ ] I know where it lives (.ai/context-aware/)
- [ ] I know what goes in each folder (task-progress, analysis, runtime-state)
- [ ] I know when to update it (start and end of work)
- [ ] I know how to commit it (git add .ai/context-aware/)
- [ ] I understand the benefit (no duplicate work)
- [ ] I'm ready to start using it

If you checked all boxes: **You're ready!**

---

## 🚀 Next Steps

1. **Read CONTEXT_AWARE_USAGE.md** (main guide)
2. **Copy structure to your project** (if new)
3. **Review example-task-progress.md** (template)
4. **Start tracking your first task** (practice)
5. **Commit your context** (share with team)

---

## 📞 If You're Stuck

1. **Is context-aware not working?**
   - Check: `.ai/context-aware/README.md` exists
   - Check: Subfol ders (task-progress, analysis, runtime-state) exist
   - Check: Files are readable

2. **Don't know what to document?**
   - Document anything you discover
   - If unsure, it's probably worth documenting
   - Next agent will thank you!

3. **Breaking changes in SPECIALIZATIONS?**
   - Document in context-aware/analysis
   - Update execution-state
   - Alert team for review

4. **Need help?**
   - See the project's `.ai/context-aware/README.md`
   - Check examples in this folder
   - Ask team for precedent

---

## 📈 Metrics: Is It Working?

You'll know context-aware is working if:

✅ **Second agent doesn't re-investigate** — They read analysis and move forward  
✅ **Task handoffs are smooth** — Next agent knows what was done  
✅ **Issues are tracked** — Not forgotten after session  
✅ **Performance metrics persist** — Known bottlenecks stay in focus  
✅ **Commits reference context** — "Fixes issue #X from analysis"

If these aren't happening: Review and update more frequently!

---

**Ready to start using context-aware? Pick a file above and begin!** 🚀
