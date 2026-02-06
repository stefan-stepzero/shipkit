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

**Before**:
- {{PREREQUISITE_SKILL}} (this creates {{WHAT_PREREQUISITE_PROVIDES}})

**Workflow position**:
- {{WORKFLOW_CONTEXT}}

---

## Prerequisites

**Recommended**:
- {{RECOMMENDED_FILE_1}} ({{WHY_NEEDED_1}})
- {{RECOMMENDED_FILE_2}} ({{WHY_NEEDED_2}})

**Optional but helpful**:
- {{OPTIONAL_FILE_1}}
- {{OPTIONAL_FILE_2}}

**If missing**: {{FALLBACK_BEHAVIOR}}

---

## Process

### Step 1: {{STEP_1_NAME}}

**Before generating anything**, ask user 2-3 clarifying questions:

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

# {{CONTEXT_TYPE_3}}
{{CONTEXT_FILE_3}}
```

**Token budget**: Keep context reading under {{TOKEN_BUDGET}} tokens.

**If files don't exist**: {{MISSING_FILES_BEHAVIOR}}

---

### Step 3: Generate {{OUTPUT_TYPE}}

**Create file using Write tool**:

**Location**: `{{OUTPUT_PATH}}`

**Use kebab-case for filename**: {{FILENAME_EXAMPLE_1}}, {{FILENAME_EXAMPLE_2}}

---

## {{OUTPUT_TYPE}} Template Structure

**Every {{OUTPUT_TYPE}} MUST follow this template**:

```markdown
# {{OUTPUT_TITLE}}

**Created**: [YYYY-MM-DD]
**Status**: Active

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

**Use this checklist to validate before proceeding to {{NEXT_STEP}}:**

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
- [ ] {{QUALITY_CHECK_9}}

---

**⚠️ Before running {{NEXT_SKILL}}, ensure all checklist items are ✓**

---

## Next Steps

**After {{OUTPUT_TYPE}} approval:**
1. Run {{NEXT_SKILL_1}} to {{NEXT_ACTION_1}}
2. Or run {{NEXT_SKILL_2}} for {{NEXT_ACTION_2}} (optional)
3. Or run {{NEXT_SKILL_3}} to {{NEXT_ACTION_3}}

---

## References

- {{REFERENCE_1}}: {{REFERENCE_PATH_1}}
- {{REFERENCE_2}}: {{REFERENCE_PATH_2}}
- {{REFERENCE_3}}: {{REFERENCE_PATH_3}}
```

---

### Step 4: Validate Completeness

**Before saving {{OUTPUT_TYPE}}, verify**:

- [ ] {{VALIDATION_CHECK_1}}
- [ ] {{VALIDATION_CHECK_2}}
- [ ] {{VALIDATION_CHECK_3}}
- [ ] {{VALIDATION_CHECK_4}}
- [ ] Quality checklist embedded in output
- [ ] Next steps suggest appropriate skills

---

### Step 5: Save and Suggest Next Step

**Use Write tool to create**: `{{OUTPUT_PATH}}`

**Output to user**:
```
✅ {{OUTPUT_TYPE}} created

📁 Location: {{OUTPUT_PATH}}

📋 Summary:
  • {{SUMMARY_STAT_1}}
  • {{SUMMARY_STAT_2}}
  • {{SUMMARY_STAT_3}}

🎯 Completeness:
  • {{COMPLETENESS_CHECK_1}}: ✓
  • {{COMPLETENESS_CHECK_2}}: ✓
  • {{COMPLETENESS_CHECK_3}}: ✓
  • Quality checklist: ✓

👉 Next steps:
  1. {{NEXT_SKILL_1}} - {{NEXT_DESCRIPTION_1}}
  2. {{NEXT_SKILL_2}} - {{NEXT_DESCRIPTION_2}} (optional)
  3. {{NEXT_SKILL_3}} - {{NEXT_DESCRIPTION_3}} (if needed)

Ready to {{NEXT_ACTION}}?
```

---

## What Makes This "Lite"

**Included**:
- ✅ {{LITE_FEATURE_1}}
- ✅ {{LITE_FEATURE_2}}
- ✅ {{LITE_FEATURE_3}}
- ✅ {{LITE_FEATURE_4}}

**Not included** (vs full {{FULL_SKILL_NAME}}):
- ❌ {{EXCLUDED_FEATURE_1}}
- ❌ {{EXCLUDED_FEATURE_2}}
- ❌ {{EXCLUDED_FEATURE_3}}
- ❌ {{EXCLUDED_FEATURE_4}}

**Philosophy**: {{LITE_PHILOSOPHY}}

---

## When This Skill Integrates with Others

### Before {{SKILL_NAME}}
- `{{PREREQUISITE_SKILL_1}}` - {{WHY_PREREQUISITE_1}}
- User {{USER_TRIGGER}}

### After {{SKILL_NAME}}
- `{{NEXT_SKILL_SEQUENTIAL_1}}` - {{WHY_NEXT_1}}
- `{{NEXT_SKILL_OPTIONAL_1}}` - {{WHY_OPTIONAL_1}} (optional)
- `{{NEXT_SKILL_OPTIONAL_2}}` - {{WHY_OPTIONAL_2}} (optional)

### Can Interrupt {{SKILL_NAME}}
- `{{INTERRUPT_SKILL}}` - When {{INTERRUPT_TRIGGER}}

---

## Context Files This Skill Reads

**Recommended** (read if exist):
- `{{READ_FILE_1}}` - {{READ_PURPOSE_1}}
- `{{READ_FILE_2}}` - {{READ_PURPOSE_2}}
- `{{READ_FILE_3}}` - {{READ_PURPOSE_3}}

**Optional** (read if relevant):
- `{{OPTIONAL_READ_1}}` - {{OPTIONAL_PURPOSE_1}}

**If missing**: {{MISSING_READ_BEHAVIOR}}

---

## Context Files This Skill Writes

**Write Strategy: MULTIPLE FILES** (see SKILL-QUALITY-AND-PATTERNS.md Part 2.1 - Quick Exit Check)

**Creates**:
- `{{OUTPUT_PATH}}` - {{OUTPUT_DESCRIPTION}}

**Update Behavior**:
- Each invocation creates a NEW file with unique name
- Previous files remain unchanged
- No overwriting or versioning needed

**Quick Exit Check** (Pattern 2.1):
```markdown
### Step 0: Check for Recent Output (Quick Exit)

**Before starting, check if output already exists from recent run**:

1. List files in {{OUTPUT_DIRECTORY}}:
   ```bash
   ls -lt {{OUTPUT_DIRECTORY}} | head -5
   ```

2. If most recent file is < 5 minutes old:
   - Show user: "Found recent {{OUTPUT_TYPE}}: {{FILENAME}}"
   - Ask: "Use this or create new?"
   - If "use this" → Exit early (save tokens)
   - If "create new" → Proceed with Step 1

3. If no recent file or > 5 minutes old:
   - Proceed with Step 1 normally
```

**Why MULTIPLE:**
- {{WHY_MULTIPLE_1}}
- {{WHY_MULTIPLE_2}}
- {{WHY_MULTIPLE_3}}

---

## Lazy Loading Behavior

**This skill loads context ON DEMAND**:

1. User invokes `{{SKILL_NAME}}`
2. Master tells Claude to read this SKILL.md
3. Claude asks {{NUM_QUESTIONS}} clarifying questions
4. Claude reads {{CONTEXT_FILES}} (~{{CONTEXT_TOKENS}} tokens)
5. Claude generates {{OUTPUT_TYPE}}
6. Total context loaded: ~{{TOTAL_TOKENS}} tokens (focused)

**Not loaded unless needed**:
- {{NOT_LOADED_1}}
- {{NOT_LOADED_2}}
- {{NOT_LOADED_3}}

---

## Success Criteria

{{OUTPUT_TYPE}} is complete when:
- [ ] {{SUCCESS_CRITERION_1}}
- [ ] {{SUCCESS_CRITERION_2}}
- [ ] {{SUCCESS_CRITERION_3}}
- [ ] {{SUCCESS_CRITERION_4}}
- [ ] Quality checklist embedded and complete
- [ ] File saved to `{{OUTPUT_PATH}}`

---

## Common Scenarios

### Scenario 1: {{SCENARIO_1_NAME}}

```
User: "{{USER_REQUEST_1}}"

Claude:
1. Ask: "{{CLARIFYING_Q_1}}"
   User: "{{USER_ANSWER_1}}"
2. Ask: "{{CLARIFYING_Q_2}}"
   User: "{{USER_ANSWER_2}}"
3. Read {{CONTEXT_FILE_EXAMPLE}}
4. Generate {{OUTPUT_TYPE}} with:
   - {{OUTPUT_ELEMENT_1}}
   - {{OUTPUT_ELEMENT_2}}
   - {{OUTPUT_ELEMENT_3}}
5. Save to {{OUTPUT_PATH_EXAMPLE}}
6. Suggest: {{NEXT_SKILL_EXAMPLE}} next
```

### Scenario 2: {{SCENARIO_2_NAME}}

```
User: "{{USER_REQUEST_2}}"

Claude:
1. Check {{PREREQUISITE_CHECK}}
2. {{ACTION_IF_MISSING}}
3. {{ACTION_IF_EXISTS}}
```

---

## Tips for Effective {{OUTPUT_TYPE_PLURAL}}

**{{TIP_CATEGORY_1}}**:
- {{TIP_1}}
- {{TIP_2}}

**{{TIP_CATEGORY_2}}**:
- {{TIP_3}}
- {{TIP_4}}

**{{TIP_CATEGORY_3}}**:
- {{TIP_5}}
- {{TIP_6}}

**When to upgrade to full {{FULL_SKILL_COMMAND}}**:
- {{UPGRADE_REASON_1}}
- {{UPGRADE_REASON_2}}
- {{UPGRADE_REASON_3}}

---

**Remember**: This is a lightweight {{OUTPUT_TYPE}} for POC/MVP work. {{CLOSING_PHILOSOPHY}}
