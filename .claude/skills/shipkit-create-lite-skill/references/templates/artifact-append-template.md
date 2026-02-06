---
name: {{SKILL_NAME}}
description: {{DESCRIPTION}}
---

# {{SKILL_NAME}} - {{TITLE}}

**Purpose**: {{PURPOSE_EXPANDED}}

---

## When to Invoke

**User triggers**:
- {{TRIGGER_1}}
- {{TRIGGER_2}}
- {{TRIGGER_3}}

**Can interrupt**:
- {{INTERRUPT_WORKFLOW_1}} (when {{INTERRUPT_CONDITION_1}})
- {{INTERRUPT_WORKFLOW_2}} (when {{INTERRUPT_CONDITION_2}})

**Workflow position**:
- {{WORKFLOW_CONTEXT}}

---

## Prerequisites

**Optional**:
- {{OPTIONAL_FILE_1}} ({{WHY_HELPFUL_1}})
- {{OPTIONAL_FILE_2}} ({{WHY_HELPFUL_2}})

**If missing**: {{FALLBACK_BEHAVIOR}}

---

## Process

### Step 1: {{STEP_1_NAME}}

**Ask user 2-3 clarifying questions**:

1. **{{QUESTION_1}}**
   - {{QUESTION_1_DETAIL}}

2. **{{QUESTION_2}}**
   - {{QUESTION_2_DETAIL}}

3. **{{QUESTION_3}}**
   - {{QUESTION_3_DETAIL}}

**Why ask first**: {{RATIONALE_FOR_QUESTIONS}}

---

### Step 2: Read Existing File and Check for Duplicates

**Duplicate Detection Pattern** (see SKILL-QUALITY-AND-PATTERNS.md Part 2.4):

```markdown
1. Read existing file: `{{OUTPUT_PATH}}`

2. Scan for similar entries:
   - Search for {{DUPLICATE_KEY_1}}
   - Search for {{DUPLICATE_KEY_2}}
   - Check last {{NUM_ENTRIES}} entries

3. If duplicate found:
   - Show user: "Found existing entry: {{EXAMPLE_ENTRY}}"
   - Ask: "Update this or add new?"
   - If "update" → Edit existing entry
   - If "add new" → Proceed with append

4. If no duplicate:
   - Proceed with append
```

**Why duplicate check**: {{WHY_DUPLICATE_CHECK}}

---

### Step 3: Generate Entry

**Entry template**:

```markdown
## {{ENTRY_TITLE_FORMAT}}

**Date**: {{DATE_FORMAT}}
**Context**: {{CONTEXT_FORMAT}}

---

### {{SECTION_1_NAME}}

{{SECTION_1_CONTENT_GUIDE}}

---

### {{SECTION_2_NAME}}

{{SECTION_2_CONTENT_GUIDE}}

---

### {{SECTION_3_NAME}}

{{SECTION_3_CONTENT_GUIDE}}

---
```

---

### Step 4: Append to File

**Use Edit tool to append**:

**Location**: `{{OUTPUT_PATH}}`

**Append at**: {{APPEND_LOCATION}} ({{WHY_THIS_LOCATION}})

**Format**:
```markdown
[Existing content]

---

## {{NEW_ENTRY}}

[New entry content]
```

---

### Step 5: Confirm and Suggest Next Step

**Output to user**:
```
✅ {{ENTRY_TYPE}} added to {{OUTPUT_FILE}}

📁 Location: {{OUTPUT_PATH}}

📝 Entry summary:
  • {{SUMMARY_POINT_1}}
  • {{SUMMARY_POINT_2}}
  • {{SUMMARY_POINT_3}}

📊 Total entries: {{TOTAL_COUNT}}

👉 Next steps:
  1. {{NEXT_SKILL_1}} - {{NEXT_DESCRIPTION_1}}
  2. Continue with {{WORKFLOW_NAME}}

Ready to proceed?
```

---

## Entry Quality Checklist

**Every entry MUST include**:

### {{QUALITY_CATEGORY_1}}
- [ ] {{QUALITY_CHECK_1}}
- [ ] {{QUALITY_CHECK_2}}
- [ ] {{QUALITY_CHECK_3}}

### {{QUALITY_CATEGORY_2}}
- [ ] {{QUALITY_CHECK_4}}
- [ ] {{QUALITY_CHECK_5}}
- [ ] {{QUALITY_CHECK_6}}

### {{QUALITY_CATEGORY_3}}
- [ ] {{QUALITY_CHECK_7}}
- [ ] {{QUALITY_CHECK_8}}

---

## What Makes This "Lite"

**Included**:
- ✅ {{LITE_FEATURE_1}}
- ✅ {{LITE_FEATURE_2}}
- ✅ {{LITE_FEATURE_3}}
- ✅ Duplicate detection (avoid redundant entries)

**Not included** (vs full {{FULL_SKILL_NAME}}):
- ❌ {{EXCLUDED_FEATURE_1}}
- ❌ {{EXCLUDED_FEATURE_2}}
- ❌ {{EXCLUDED_FEATURE_3}}

**Philosophy**: {{LITE_PHILOSOPHY}}

---

## When This Skill Integrates with Others

### Can Interrupt ANY Skill When
- {{INTERRUPT_TRIGGER_1}}
- {{INTERRUPT_TRIGGER_2}}
- {{INTERRUPT_TRIGGER_3}}

### After {{SKILL_NAME}}
- Resume previous workflow
- {{OPTIONAL_NEXT_1}} (if {{CONDITION_1}})

### Related Skills
- `{{RELATED_SKILL_1}}` - {{RELATIONSHIP_1}}
- `{{RELATED_SKILL_2}}` - {{RELATIONSHIP_2}}

---

## Context Files This Skill Reads

**Optional** (read if exist):
- `{{READ_FILE_1}}` - {{READ_PURPOSE_1}}
- `{{READ_FILE_2}}` - {{READ_PURPOSE_2}}

**If missing**: {{MISSING_READ_BEHAVIOR}}

---

## Context Files This Skill Writes

**Write Strategy: APPEND** (see SKILL-QUALITY-AND-PATTERNS.md Part 2.4 - Duplicate Detection)

**Updates**:
- `{{OUTPUT_PATH}}` - {{OUTPUT_DESCRIPTION}}

**Update Behavior**:
- Reads existing file first
- Checks for duplicates (last {{NUM_CHECK}} entries)
- Appends new entry at {{APPEND_LOCATION}}
- Preserves all existing content
- No archiving needed (running log)

**Duplicate Detection** (Pattern 2.4):
- Search for similar {{DUPLICATE_KEY}}
- If found → Ask user to update or add new
- If not found → Append automatically

**Why APPEND:**
- {{WHY_APPEND_1}}
- {{WHY_APPEND_2}}
- {{WHY_APPEND_3}}

**File structure**:
```markdown
# {{FILE_TITLE}}

**Purpose**: {{FILE_PURPOSE}}

---

## Entry 1 (oldest)
[content]

---

## Entry 2
[content]

---

## Entry 3 (newest)
[content]
```

---

## Lazy Loading Behavior

**This skill loads context ON DEMAND**:

1. User invokes `{{SKILL_NAME}}` (or triggered by condition)
2. Master tells Claude to read this SKILL.md
3. Claude asks {{NUM_QUESTIONS}} questions
4. Claude reads {{OUTPUT_PATH}} (~{{CONTEXT_TOKENS}} tokens)
5. Claude checks for duplicates
6. Claude appends entry
7. Total context loaded: ~{{TOTAL_TOKENS}} tokens

**Not loaded unless needed**:
- {{NOT_LOADED_1}}
- {{NOT_LOADED_2}}

---

## Success Criteria

Entry is complete when:
- [ ] {{SUCCESS_CRITERION_1}}
- [ ] {{SUCCESS_CRITERION_2}}
- [ ] {{SUCCESS_CRITERION_3}}
- [ ] No duplicate entries created
- [ ] Entry quality checklist passed
- [ ] Appended to `{{OUTPUT_PATH}}`

---

## Common Scenarios

### Scenario 1: {{SCENARIO_1_NAME}}

```
User: "{{USER_REQUEST_1}}"

Claude:
1. Read {{OUTPUT_PATH}}
2. Check for similar entry ({{DUPLICATE_SEARCH}})
3. No duplicate found
4. Generate entry with:
   - {{ENTRY_ELEMENT_1}}
   - {{ENTRY_ELEMENT_2}}
5. Append to {{OUTPUT_PATH}}
6. Resume previous workflow
```

### Scenario 2: {{SCENARIO_2_NAME}} (Duplicate Found)

```
Claude detects: {{DUPLICATE_TRIGGER}}

Claude:
1. Read {{OUTPUT_PATH}}
2. Find existing entry: "{{EXISTING_ENTRY_TITLE}}"
3. Ask: "Update existing or add new?"
   User: "Update"
4. Edit existing entry with new info
5. Resume workflow
```

---

## Tips for Effective {{ENTRY_TYPE_PLURAL}}

**{{TIP_CATEGORY_1}}**:
- {{TIP_1}}
- {{TIP_2}}

**{{TIP_CATEGORY_2}}**:
- {{TIP_3}}
- {{TIP_4}}

**When to upgrade to full {{FULL_SKILL_COMMAND}}**:
- {{UPGRADE_REASON_1}}
- {{UPGRADE_REASON_2}}

---

**Remember**: This is an ongoing log. Each entry builds project knowledge over time. {{CLOSING_PHILOSOPHY}}
