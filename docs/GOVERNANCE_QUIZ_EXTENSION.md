# Adding Governance Questions to Quiz System

**Purpose**: Extend quiz_questions.json with governance compliance validation questions

**Current Status**: quiz_executor.py has 12 questions, 6 topics  
**Extension**: Add 4 governance questions for enforcement validation

---

## New Questions to Add

### Question 1: Mandatory Policies (Easy)

```json
{
  "id": 13,
  "topic": "governance",
  "difficulty": "easy",
  "question": "Which of the following is NOT one of the 7 mandatory governance policies?",
  "options": {
    "A": "governance-core.json must exist",
    "B": "At least one active seedling must be defined",
    "C": "All developers must have architect role",
    "D": "Enforcement level must be explicitly set"
  },
  "correct": "C",
  "explanation": "Policy: All authority roles must be assigned, but not everyone needs architect role. Architect, governance, and operations roles must be assigned to someone (can be same person). Answer C correctly identifies the false statement."
}
```

### Question 2: Enforcement Levels (Medium)

```json
{
  "id": 14,
  "topic": "governance",
  "difficulty": "medium",
  "question": "In STRICT enforcement mode, what happens when a developer tries to use --force flag to bypass governance checks?",
  "options": {
    "A": "The --force flag is accepted and checks are skipped",
    "B": "The --force flag is ignored and checks are blocked",
    "C": "User is prompted to enter architect approval code",
    "D": "The operation proceeds with a warning message"
  },
  "correct": "B",
  "explanation": "Strict mode provides maximum enforcement. Manual bypass is completely disabled - the --force flag is ignored and the operation is blocked. Users must fix the underlying issue causing the check to fail. Answer B is correct."
}
```

### Question 3: Authority Roles (Medium)

```json
{
  "id": 15,
  "topic": "governance",
  "difficulty": "medium",
  "question": "You are setting up governance for your project. Which authority roles MUST be assigned for compliance?",
  "options": {
    "A": "Only architect role is required",
    "B": "Architect and governance roles are required",
    "C": "All three roles (architect, governance, operations) must be assigned",
    "D": "Any two of the three roles are sufficient"
  },
  "correct": "C",
  "explanation": "Policy 4 requires ALL three authority roles to be assigned. They can be assigned to the same person if needed (e.g., in small teams), but all three roles must have at least one email address. Answer C is correct."
}
```

### Question 4: Compliance Checking (Hard)

```json
{
  "id": 16,
  "topic": "governance",
  "difficulty": "hard",
  "question": "Your governance compliance check reports: \"3 policies passed, 7 policies total, 43% compliance\". What is the MOST critical action?",
  "options": {
    "A": "Continue working; 43% is acceptable for development phase",
    "B": "Run compliance validator to identify specific violations",
    "C": "Change enforcement level to 'permissive'",
    "D": "Delete governance-core.json and start fresh"
  },
  "correct": "B",
  "explanation": "At 43% compliance, 4 policies are failing. The correct action is to identify which policies are violated using: python3 _core/tools/governance_compliance.py --verify --fix-steps. This shows exactly what needs to be fixed. Answer B is correct."
}
```

---

## How to Add Questions

### Method 1: Manual Edit

1. Open `EXECUTION/quiz_questions.json`
2. Add the new questions to the `questions` array
3. Save file
4. Verify JSON syntax: `python3 -m json.tool EXECUTION/quiz_questions.json`

### Method 2: Python Script

```python
#!/usr/bin/env python3
"""Add governance questions to quiz_questions.json"""

import json
from pathlib import Path

quiz_file = Path("EXECUTION/quiz_questions.json")

# Load existing
with open(quiz_file, 'r') as f:
    data = json.load(f)

# New governance questions
new_questions = [
    {
        "id": 13,
        "topic": "governance",
        "difficulty": "easy",
        "question": "Which of the following is NOT one of the 7 mandatory governance policies?",
        "options": {
            "A": "governance-core.json must exist",
            "B": "At least one active seedling must be defined",
            "C": "All developers must have architect role",
            "D": "Enforcement level must be explicitly set"
        },
        "correct": "C",
        "explanation": "Policy: All authority roles must be assigned, but not everyone needs architect role. Architect, governance, and operations roles must be assigned to someone (can be same person). Answer C correctly identifies the false statement."
    },
    {
        "id": 14,
        "topic": "governance",
        "difficulty": "medium",
        "question": "In STRICT enforcement mode, what happens when a developer tries to use --force flag to bypass governance checks?",
        "options": {
            "A": "The --force flag is accepted and checks are skipped",
            "B": "The --force flag is ignored and checks are blocked",
            "C": "User is prompted to enter architect approval code",
            "D": "The operation proceeds with a warning message"
        },
        "correct": "B",
        "explanation": "Strict mode provides maximum enforcement. Manual bypass is completely disabled - the --force flag is ignored and the operation is blocked. Users must fix the underlying issue causing the check to fail. Answer B is correct."
    },
    {
        "id": 15,
        "topic": "governance",
        "difficulty": "medium",
        "question": "You are setting up governance for your project. Which authority roles MUST be assigned for compliance?",
        "options": {
            "A": "Only architect role is required",
            "B": "Architect and governance roles are required",
            "C": "All three roles (architect, governance, operations) must be assigned",
            "D": "Any two of the three roles are sufficient"
        },
        "correct": "C",
        "explanation": "Policy 4 requires ALL three authority roles to be assigned. They can be assigned to the same person if needed (e.g., in small teams), but all three roles must have at least one email address. Answer C is correct."
    },
    {
        "id": 16,
        "topic": "governance",
        "difficulty": "hard",
        "question": "Your governance compliance check reports: \"3 policies passed, 7 policies total, 43% compliance\". What is the MOST critical action?",
        "options": {
            "A": "Continue working; 43% is acceptable for development phase",
            "B": "Run compliance validator to identify specific violations",
            "C": "Change enforcement level to 'permissive'",
            "D": "Delete governance-core.json and start fresh"
        },
        "correct": "B",
        "explanation": "At 43% compliance, 4 policies are failing. The correct action is to identify which policies are violated using: python3 _core/tools/governance_compliance.py --verify --fix-steps. This shows exactly what needs to be fixed. Answer B is correct."
    }
]

# Add to quiz data
data['questions'].extend(new_questions)

# Update metadata
data['statistics']['total_questions'] = len(data['questions'])
data['statistics']['topics']['governance'] = 4  # Up from 0

# Save
with open(quiz_file, 'w') as f:
    json.dump(data, f, indent=2)

print(f"✓ Added 4 governance questions")
print(f"✓ Total questions: {len(data['questions'])}")
print(f"✓ Governance topic now has 4 questions")
```

### Method 3: Command Line

```bash
# Verify current state
python3 -c "import json; d=json.load(open('EXECUTION/quiz_questions.json')); print(f\"Topics: {list(d.get('statistics', {}).get('topics', {}).keys())}\")"

# After adding, verify
python3 EXECUTION/quiz_executor.py --list-topics
```

---

## Verification Steps

After adding questions:

```bash
# 1. Verify JSON syntax
python3 -m json.tool EXECUTION/quiz_questions.json > /dev/null && echo "✓ Valid JSON"

# 2. List topics (should include governance)
python3 EXECUTION/quiz_executor.py --list-topics

# 3. Run governance quiz
python3 EXECUTION/quiz_executor.py --topic=governance --mode=silent

# 4. Test individual questions
python3 EXECUTION/quiz_executor.py --topic=governance --mode=interactive
```

---

## Expected Test Results

After adding and verifying:

```
Topics:
  - governance (4 questions)
  - [existing topics...]

Governance Quiz Results:
  - Question 1 (Easy): Tests policy knowledge
  - Question 2 (Medium): Tests enforcement mode behavior
  - Question 3 (Medium): Tests authority role requirements
  - Question 4 (Hard): Tests compliance troubleshooting

Pass threshold: 70% (need 3/4 correct)
```

---

## Integration with AHP

When AHP Layer 4 is enhanced with compliance checking:

1. If governance compliance < 70%, suggest running quiz
2. If compliance >= 70% and user passes governance quiz → state = HEALTHY
3. If compliance >= 70% but user fails quiz → state = PARTIAL

Example AHP output:
```
🧠 SDD STATUS
State: 🟡 PARTIAL
Confidence: 65%

Actions:
  ✓ Governance compliance: 100% (7/7 policies)
  ✗ Knowledge validation: 60% (2/4 quiz questions passed)
  
Suggestion: Complete governance quiz to reach HEALTHY state
  python3 EXECUTION/quiz_executor.py --topic=governance
```

---

## Questions Summary

| ID | Topic | Difficulty | Focus |
|----|-------|-----------|-------|
| 13 | governance | easy | Mandatory policies understanding |
| 14 | governance | medium | Enforcement level behavior |
| 15 | governance | medium | Authority role requirements |
| 16 | governance | hard | Compliance troubleshooting |

**Total**: 4 new questions  
**Total Quiz**: 16 questions (up from 12)  
**New Topics**: governance (4 questions)  
**Existing Topics**: 5 (unchanged)  
**Pass Rate**: Still 70%

---

## Next Steps

1. ✅ Add questions to quiz_questions.json
2. ✅ Verify with quiz_executor.py
3. ⏳ Integrate governance quiz checks into AHP Layer 4
4. ⏳ Test end-to-end: governance check → AHP → quiz → state determination

---

**Status**: Ready to implement  
**Time Estimate**: 5-10 minutes  
**Testing**: Required (see Verification Steps)  
**Risk**: Low (backward compatible extension)
