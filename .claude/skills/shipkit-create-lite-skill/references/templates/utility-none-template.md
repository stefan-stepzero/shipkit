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
3. {{ACTION_6}}

---

### Step 3: {{STEP_3_NAME}}

**{{STEP_3_OBJECTIVE}}**:

1. {{ACTION_7}}
2. {{ACTION_8}}

---

### Step 4: Report Results

**Provide summary to user:**

```
{{REPORT_FORMAT}}
```

**No file output** - This skill {{SKILL_FUNCTION}} without creating files.

---

## What Makes This "Lite"

**Included**:
- ✅ {{LITE_FEATURE_1}}
- ✅ {{LITE_FEATURE_2}}
- ✅ No file clutter (reporting only)

**Not included** (vs full {{FULL_SKILL_NAME}}):
- ❌ {{EXCLUDED_FEATURE_1}}
- ❌ {{EXCLUDED_FEATURE_2}}

**Philosophy**: {{LITE_PHILOSOPHY}}

---

## When This Skill Integrates with Others

### Can Be Used {{USAGE_PATTERN}}
- {{INTEGRATION_CONTEXT_1}}
- {{INTEGRATION_CONTEXT_2}}

### Typical Workflow
1. {{WORKFLOW_STEP_1}}
2. User invokes `{{SKILL_NAME}}`
3. {{WORKFLOW_STEP_3}}
4. Resume previous work

### Related Skills
- `{{RELATED_SKILL_1}}` - {{RELATIONSHIP_1}}
- `{{RELATED_SKILL_2}}` - {{RELATIONSHIP_2}}

---

## Context Files This Skill Reads

**Reads** (if exist):
- `{{READ_FILE_1}}` - {{READ_PURPOSE_1}}
- `{{READ_FILE_2}}` - {{READ_PURPOSE_2}}
- `{{READ_FILE_3}}` - {{READ_PURPOSE_3}}

**If missing**: {{MISSING_READ_BEHAVIOR}}

---

## Context Files This Skill Writes

**Write Strategy: NONE** (Utility provides guidance/reporting, no file output)

**This skill:**
- ❌ Does not create output files
- ✅ Reads context files for analysis
- ✅ Reports findings to user
- ✅ Provides recommendations

**Why NONE:**
- {{WHY_NONE_1}}
- {{WHY_NONE_2}}
- {{WHY_NONE_3}}

---

## Success Criteria

Utility is successful when:
- [ ] {{SUCCESS_CRITERION_1}}
- [ ] {{SUCCESS_CRITERION_2}}
- [ ] {{SUCCESS_CRITERION_3}}
- [ ] User has clear next steps

---

## Common Scenarios

### Scenario 1: {{SCENARIO_1_NAME}}

```
User: "{{USER_REQUEST}}"

Claude:
1. Read {{CONTEXT_FILES}}
2. Analyze {{ANALYSIS_TARGET}}
3. Report:
   {{REPORT_EXAMPLE}}
4. Suggest: {{NEXT_STEP}}
```

---

**Remember**: This skill provides information and guidance, not file artifacts. {{CLOSING_PHILOSOPHY}}
