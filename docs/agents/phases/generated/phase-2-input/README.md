# Phase 1: Governance Rules Templates

**Generated:** 2026-04-25T22:05:53.857054

## Configuration

- **Language:** Python
- **Adoption Level:** FULL

## What You Have

Raw templates for all mandates and guidelines, organized by category:
- `mandates-*.md` — Core architectural rules (hard, non-negotiable)
- `guidelines-*.md` — Best practices (soft, customizable)

Total: 2 mandates + 151 guidelines

## Status Field Defaults

Each rule starts with:
```
**Status:** required: true
**Customizable:** true/false
**Optional:** false
```

## Phase 2: What to Do Now

### Step 1: Edit the Files

For each `.md` file in this folder:

1. **Open** in your editor
2. **Read** each rule (understand what it does)
3. **For each rule**, decide its status:
   - Keep as required: `required: true` → Include in final governance
   - Make optional: `optional: true` → Skip this rule
   - Make customizable: `custom: true` → Include but allow customization

### Step 2: Change Status Lines

Find lines like:
```markdown
**Status:** `required: true` (Default: include)
```

Change to ONE of:
```markdown
**Status:** `required: true`
**Status:** `optional: true`
**Status:** `custom: true`
```

### Step 3: Run Phase 3

Once you've edited the markdown files, just run:

```bash
./wizard.sh
# Choose: [3] Phase 3
```

Phase 3 will:
1. Read your edited markdown files from this folder
2. Parse the status fields (required/optional/custom)
3. Skip items marked as optional
4. Compile to final governance JSON

No need to convert to YAML or move files - edit in place!

## Questions?

- Mandates: Always required (cannot customize)
- Guidelines: Can be required/optional/custom
- Default: Everything starts as required (you decide what to change)
