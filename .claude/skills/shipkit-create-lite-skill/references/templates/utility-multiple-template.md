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

**If missing**: {{FALLBACK_BEHAVIOR}}

---

## Process

### Step 1: {{STEP_1_NAME}}

**{{STEP_1_OBJECTIVE}}**:

1. {{ACTION_1}}
2. {{ACTION_2}}

---

### Step 2: {{STEP_2_NAME}}

**{{STEP_2_OBJECTIVE}}**:

1. {{ACTION_3}}
2. {{ACTION_4}}

---

### Step 3: Generate Output

**Create file using Write tool**:

**Location**: `{{OUTPUT_PATH}}`

**Naming pattern**: {{NAMING_PATTERN_EXAMPLE}}

**Format**:
```markdown
{{OUTPUT_FORMAT_EXAMPLE}}
```

---

### Step 4: Report to User

**Output to user**:
```
✅ {{OUTPUT_TYPE}} created

📁 Location: {{OUTPUT_PATH}}

📋 Content:
  • {{SUMMARY_POINT_1}}
  • {{SUMMARY_POINT_2}}

👉 Next: {{NEXT_SUGGESTION}}
```

---

## What Makes This "Lite"

**Included**:
- ✅ {{LITE_FEATURE_1}}
- ✅ {{LITE_FEATURE_2}}
- ✅ Multiple files for organization

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

**If missing**: {{MISSING_READ_BEHAVIOR}}

---

## Context Files This Skill Writes

**Write Strategy: MULTIPLE FILES**

**Creates**:
- `{{OUTPUT_PATH}}` - {{OUTPUT_DESCRIPTION}}
- Each invocation creates a new file with unique name

**File naming**:
- Pattern: {{NAMING_PATTERN}}
- Example: {{NAMING_EXAMPLE}}

**Why MULTIPLE:**
- {{WHY_MULTIPLE_1}}
- {{WHY_MULTIPLE_2}}

---

## Success Criteria

Utility is successful when:
- [ ] {{SUCCESS_CRITERION_1}}
- [ ] {{SUCCESS_CRITERION_2}}
- [ ] File created in correct location

---

**Remember**: Each invocation creates a separate file. {{CLOSING_PHILOSOPHY}}
