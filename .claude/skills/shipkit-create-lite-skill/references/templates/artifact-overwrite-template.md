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

### Step 0: Check for Existing File (Quick Exit + File Exists Workflow)

**Quick Exit Check** (see SKILL-QUALITY-AND-PATTERNS.md Part 2.1):

```markdown
1. Check if `{{OUTPUT_PATH}}` exists

2. If exists AND modified < 5 minutes ago:
   - Show user: "Found recent {{OUTPUT_TYPE}} (modified {{TIME_AGO}})"
   - Ask: "Use this or regenerate?"
   - If "use this" → Exit early (save tokens)
   - If "regenerate" → Proceed to Step 1

3. If exists AND modified > 5 minutes ago:
   - Proceed to File Exists Workflow (Step 0b)

4. If doesn't exist:
   - Skip to Step 1 (generate new)
```

**File Exists Workflow** (see SKILL-QUALITY-AND-PATTERNS.md Part 2.2):

```markdown
### Step 0b: File Already Exists

File exists: `{{OUTPUT_PATH}}`

**Options:**

1. **View** - Show current contents, then ask what to do
2. **Update** - Read existing, ask what to change, regenerate with updates
3. **Replace** - Archive old version, generate completely new
4. **Cancel** - Exit without changes

**User choice:**

**If View:**
- Display current file
- Ask: "Keep this, update it, or replace?"
- Go to Update/Replace/Cancel

**If Update:**
- Read existing file
- Ask: "What should change?"
- Regenerate incorporating updates
- Use Write tool to overwrite

**If Replace:**
- Archive current version (see Archive Before Overwrite pattern)
- Proceed to Step 1 (generate new)

**If Cancel:**
- Exit, no changes made
```

---

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

### Step 2: Read Existing Context

**Read these files to understand project context**:

```bash
# {{CONTEXT_TYPE_1}}
{{CONTEXT_FILE_1}}

# {{CONTEXT_TYPE_2}}
{{CONTEXT_FILE_2}}
```

**Token budget**: Keep context reading under {{TOKEN_BUDGET}} tokens.

**If files don't exist**: {{MISSING_FILES_BEHAVIOR}}

---

### Step 3: Generate {{OUTPUT_TYPE}}

**Create file using Write tool** (overwrites if exists):

**Location**: `{{OUTPUT_PATH}}`

---

## {{OUTPUT_TYPE}} Template Structure

**The {{OUTPUT_TYPE}} MUST follow this template**:

```markdown
# {{OUTPUT_TITLE}}

**Last Updated**: [YYYY-MM-DD]

---

## {{SECTION_1_NAME}}

{{SECTION_1_CONTENT_GUIDE}}

---

## {{SECTION_2_NAME}}

{{SECTION_2_CONTENT_GUIDE}}

---

## {{SECTION_3_NAME}}

{{SECTION_3_CONTENT_GUIDE}}

---

## Quality Checklist

**Validate {{OUTPUT_TYPE}} meets standards:**

### {{QUALITY_CATEGORY_1}}
- [ ] {{QUALITY_CHECK_1}}
- [ ] {{QUALITY_CHECK_2}}
- [ ] {{QUALITY_CHECK_3}}

### {{QUALITY_CATEGORY_2}}
- [ ] {{QUALITY_CHECK_4}}
- [ ] {{QUALITY_CHECK_5}}

### {{QUALITY_CATEGORY_3}}
- [ ] {{QUALITY_CHECK_6}}
- [ ] {{QUALITY_CHECK_7}}

---

**⚠️ Review this checklist before using {{OUTPUT_TYPE}} for {{NEXT_STEP}}**
```

---

### Step 4: Archive Old Version (If Replacing)

**Archive Before Overwrite Pattern** (see SKILL-QUALITY-AND-PATTERNS.md Part 2.5):

```markdown
**If user chose "Replace" in Step 0:**

1. Create archive directory: `{{ARCHIVE_PATH}}`

2. Copy existing file with timestamp:
   ```bash
   cp {{OUTPUT_PATH}} {{ARCHIVE_PATH}}/{{OUTPUT_FILENAME}}.{{TIMESTAMP}}.md
   ```

3. Add archive note to new file:
   ```markdown
   **Previous version**: See {{ARCHIVE_PATH}}/{{OUTPUT_FILENAME}}.{{TIMESTAMP}}.md
   ```

4. Write new file (overwrites current)
```

**Why archive**: {{WHY_ARCHIVE}}

---

### Step 5: Save and Suggest Next Step

**Use Write tool to create/overwrite**: `{{OUTPUT_PATH}}`

**Output to user**:
```
✅ {{OUTPUT_TYPE}} {{ACTION_VERB}}

📁 Location: {{OUTPUT_PATH}}

📋 Summary:
  • {{SUMMARY_POINT_1}}
  • {{SUMMARY_POINT_2}}
  • {{SUMMARY_POINT_3}}

{{#if_archived}}
📦 Previous version archived: {{ARCHIVE_PATH}}/{{FILENAME}}
{{/if_archived}}

👉 Next steps:
  1. {{NEXT_SKILL_1}} - {{NEXT_DESCRIPTION_1}}
  2. {{NEXT_SKILL_2}} - {{NEXT_DESCRIPTION_2}} (optional)

Ready to {{NEXT_ACTION}}?
```

---

## What Makes This "Lite"

**Included**:
- ✅ {{LITE_FEATURE_1}}
- ✅ {{LITE_FEATURE_2}}
- ✅ Quick exit check (avoid regenerating recent files)
- ✅ File exists workflow (view/update/replace/cancel)

**Not included** (vs full {{FULL_SKILL_NAME}}):
- ❌ {{EXCLUDED_FEATURE_1}}
- ❌ {{EXCLUDED_FEATURE_2}}
- ❌ {{EXCLUDED_FEATURE_3}}

**Philosophy**: {{LITE_PHILOSOPHY}}

---

## When This Skill Integrates with Others

### Before {{SKILL_NAME}}
- {{PREREQUISITE_CONTEXT}}

### After {{SKILL_NAME}}
- `{{NEXT_SKILL_1}}` - {{WHY_NEXT_1}}
- `{{NEXT_SKILL_2}}` - {{WHY_NEXT_2}} (optional)

### When {{SKILL_NAME}} Runs Again
- File exists workflow activates
- User can view/update/replace existing file

---

## Context Files This Skill Reads

**Optional** (read if exist):
- `{{READ_FILE_1}}` - {{READ_PURPOSE_1}}
- `{{READ_FILE_2}}` - {{READ_PURPOSE_2}}

**If missing**: {{MISSING_READ_BEHAVIOR}}

---

## Context Files This Skill Writes

**Write Strategy: OVERWRITE** (see SKILL-QUALITY-AND-PATTERNS.md Part 2.2 - File Exists Workflow)

**Creates/Updates**:
- `{{OUTPUT_PATH}}` - {{OUTPUT_DESCRIPTION}}

**Update Behavior**:
- File exists → File Exists Workflow (view/update/replace/cancel)
- Recent file (< 5 min) → Quick Exit Check (use or regenerate)
- Replace → Archive old version first
- Update → Read existing, incorporate changes
- Each write REPLACES entire file contents

**Archive location** (if replacing):
- `{{ARCHIVE_PATH}}/{{FILENAME}}.{{TIMESTAMP}}.md`

**Why OVERWRITE:**
- {{WHY_OVERWRITE_1}}
- {{WHY_OVERWRITE_2}}
- {{WHY_OVERWRITE_3}}

---

## Lazy Loading Behavior

**This skill loads context ON DEMAND**:

1. User invokes `{{SKILL_NAME}}`
2. Master tells Claude to read this SKILL.md
3. Claude checks if file exists (Quick Exit Check)
4. If regenerating: Ask {{NUM_QUESTIONS}} questions
5. Read {{CONTEXT_FILES}} (~{{CONTEXT_TOKENS}} tokens)
6. Generate {{OUTPUT_TYPE}}
7. Total context loaded: ~{{TOTAL_TOKENS}} tokens

**Not loaded unless needed**:
- {{NOT_LOADED_1}}
- {{NOT_LOADED_2}}

---

## Success Criteria

{{OUTPUT_TYPE}} is complete when:
- [ ] {{SUCCESS_CRITERION_1}}
- [ ] {{SUCCESS_CRITERION_2}}
- [ ] {{SUCCESS_CRITERION_3}}
- [ ] Quality checklist embedded
- [ ] File saved to `{{OUTPUT_PATH}}`
- [ ] Old version archived (if replaced)

---

## Common Scenarios

### Scenario 1: {{SCENARIO_1_NAME}} (First Time)

```
User: "{{USER_REQUEST_1}}"

Claude:
1. Check {{OUTPUT_PATH}} (doesn't exist)
2. Ask: "{{CLARIFYING_Q_1}}"
   User: "{{USER_ANSWER_1}}"
3. Read {{CONTEXT_FILE_EXAMPLE}}
4. Generate {{OUTPUT_TYPE}}
5. Save to {{OUTPUT_PATH}}
```

### Scenario 2: {{SCENARIO_2_NAME}} (File Exists)

```
User: "{{USER_REQUEST_2}}"

Claude:
1. Check {{OUTPUT_PATH}} (exists, modified {{TIME_AGO}})
2. Show: "File exists. Options: View/Update/Replace/Cancel"
   User: "Update"
3. Read existing file
4. Ask: "What should change?"
   User: "{{CHANGE_REQUEST}}"
5. Regenerate with updates
6. Overwrite {{OUTPUT_PATH}}
```

### Scenario 3: Quick Exit (Recent File)

```
User: "{{USER_REQUEST_3}}"

Claude:
1. Check {{OUTPUT_PATH}} (exists, modified 2 minutes ago)
2. Show: "Found recent {{OUTPUT_TYPE}} (2 min ago). Use this or regenerate?"
   User: "Use this"
3. Exit (saved tokens, no regeneration)
```

---

## Tips for Effective {{OUTPUT_TYPE_PLURAL}}

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

**Remember**: This file is your {{OUTPUT_PURPOSE}}. Update it as {{UPDATE_FREQUENCY}}. {{CLOSING_PHILOSOPHY}}
