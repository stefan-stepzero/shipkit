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

**Auto-triggered** (if applicable):
- {{AUTO_TRIGGER}} (when {{AUTO_CONDITION}})

**Workflow position**:
- {{WORKFLOW_CONTEXT}}

---

## Prerequisites

**Optional**:
- {{OPTIONAL_FILE_1}} ({{WHY_HELPFUL_1}})

**If missing**: {{FALLBACK_BEHAVIOR}}

---

## Process

### Step 0: Quick Exit Check (If Applicable)

**If this utility runs frequently, check for recent output:**

```markdown
1. Check if `{{OUTPUT_PATH}}` exists and modified < {{TIME_THRESHOLD}} ago

2. If recent:
   - Show: "Found recent {{OUTPUT_TYPE}} ({{TIME_AGO}})"
   - Ask: "Use this or regenerate?"
   - If "use" → Exit early
   - If "regenerate" → Proceed to Step 1

3. If not recent or doesn't exist:
   - Proceed to Step 1
```

---

### Step 1: {{STEP_1_NAME}}

**{{STEP_1_OBJECTIVE}}**:

1. {{ACTION_1}}
2. {{ACTION_2}}
3. {{ACTION_3}}

---

### Step 2: {{STEP_2_NAME}}

**{{STEP_2_OBJECTIVE}}**:

1. {{ACTION_4}}
2. {{ACTION_5}}

---

### Step 3: Generate Output

**Create file using Write tool**:

**Location**: `{{OUTPUT_PATH}}`

**Format**:
```markdown
{{OUTPUT_FORMAT_EXAMPLE}}
```

---

### Step 4: Report to User

**Output to user**:
```
✅ {{OUTPUT_TYPE}} {{ACTION_VERB}}

📁 Location: {{OUTPUT_PATH}}

📋 Summary:
  • {{SUMMARY_POINT_1}}
  • {{SUMMARY_POINT_2}}

{{#if_next_step}}
👉 Next: {{NEXT_SUGGESTION}}
{{/if_next_step}}
```

---

## What Makes This "Lite"

**Included**:
- ✅ {{LITE_FEATURE_1}}
- ✅ {{LITE_FEATURE_2}}
- ✅ Quick and focused

**Not included** (vs full {{FULL_SKILL_NAME}}):
- ❌ {{EXCLUDED_FEATURE_1}}
- ❌ {{EXCLUDED_FEATURE_2}}

**Philosophy**: {{LITE_PHILOSOPHY}}

---

## When This Skill Integrates with Others

### Can Be Used {{USAGE_PATTERN}}
- {{INTEGRATION_CONTEXT_1}}
- {{INTEGRATION_CONTEXT_2}}

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

**Write Strategy: OVERWRITE**

**Creates/Updates**:
- `{{OUTPUT_PATH}}` - {{OUTPUT_DESCRIPTION}}

**Update Behavior**:
- Overwrites file each time
- {{OVERWRITE_RATIONALE}}

**Why OVERWRITE:**
- {{WHY_OVERWRITE_1}}
- {{WHY_OVERWRITE_2}}

---

## Success Criteria

Utility is successful when:
- [ ] {{SUCCESS_CRITERION_1}}
- [ ] {{SUCCESS_CRITERION_2}}
- [ ] {{SUCCESS_CRITERION_3}}

---

**Remember**: This is a utility skill - keep it simple and focused. {{CLOSING_PHILOSOPHY}}
