# File 7: Update install/settings/shipkit.settings.json

**Purpose**: Add skill permission to the allow list

**File**: `install/settings/shipkit.settings.json`

---

## Step 1: Read and Parse JSON

**Current structure**:
```json
{
  "permissions": {
    "allow": [
      "Read",
      "Write(src/**)",
      ...
      "Skill(shipkit-master)",
      "Skill(shipkit-project-status)",
      "Skill(shipkit-project-context)",
      ...
    ],
    "deny": [...]
  },
  "hooks": {...},
  "skills": {...}
}
```

---

## Step 2: Find Skill Permissions Section

**Locate the `Skill(...)` entries** in the `allow` array:

```json
"allow": [
  "Read",
  "Write(src/**)",
  ... (many file and bash permissions) ...

  "Skill(shipkit-master)",
  "Skill(shipkit-project-status)",
  "Skill(shipkit-project-context)",
  "Skill(shipkit-spec)",
  "Skill(shipkit-architecture-memory)",
  "Skill(shipkit-ux-coherence)",
  "Skill(shipkit-data-consistency)",
  "Skill(shipkit-plan)",
  "Skill(shipkit-implement)",
  "Skill(shipkit-component-knowledge)",
  "Skill(shipkit-route-knowledge)",
  "Skill(shipkit-document-artifact)",
  "Skill(shipkit-quality-confidence)",
  "Skill(shipkit-user-instructions)",
  "Skill(shipkit-integration-guardrails)",
  "Skill(shipkit-work-memory)",
  "Skill(shipkit-debug-systematically)",
  "Skill(shipkit-communications)",
  "Skill(shipkit-why-project)",
  "Skill(shipkit-whats-next)"
],
```

---

## Step 3: Add New Skill Permission

**Add as last Skill(...) entry** (before closing array bracket):

```json
"Skill(shipkit-whats-next)",
"Skill(shipkit-NEW-SKILL)"  <-- NEW (comma on previous line)
],
```

**Complete example**:

```json
"allow": [
  ... (other permissions) ...

  "Skill(shipkit-master)",
  "Skill(shipkit-project-status)",
  "Skill(shipkit-project-context)",
  "Skill(shipkit-spec)",
  "Skill(shipkit-architecture-memory)",
  "Skill(shipkit-ux-coherence)",
  "Skill(shipkit-data-consistency)",
  "Skill(shipkit-plan)",
  "Skill(shipkit-implement)",
  "Skill(shipkit-component-knowledge)",
  "Skill(shipkit-route-knowledge)",
  "Skill(shipkit-document-artifact)",
  "Skill(shipkit-quality-confidence)",
  "Skill(shipkit-user-instructions)",
  "Skill(shipkit-integration-guardrails)",
  "Skill(shipkit-work-memory)",
  "Skill(shipkit-debug-systematically)",
  "Skill(shipkit-communications)",
  "Skill(shipkit-why-project)",
  "Skill(shipkit-whats-next)",
  "Skill(shipkit-user-stories)"  <-- NEW
],
```

---

## Step 4: Validate JSON Syntax

**Critical points**:
1. **Comma placement**: Last item in array should NOT have trailing comma
2. **Quotes**: Use double quotes, not single quotes
3. **Format**: `Skill(shipkit-{skill-name})` with parentheses
4. **Indentation**: Maintain 6-space indentation for skill entries

**Validation command**:
```bash
python -c "import json; json.load(open('install/settings/shipkit.settings.json'))"
```

**Expected output**:
- Success: No output (exit code 0)
- Failure: JSON syntax error message

---

## Step 5: Optional - Maintain Alphabetical Order

**Current order** (not strictly alphabetical):
- Appears to be in logical/creation order
- `shipkit-master` first (master orchestrator)
- Other skills in rough order of typical usage

**Recommendation**: Add new skills at the **end** of the list (easier to track additions)

**Alternative**: Maintain alphabetical order if that's the pattern

---

## Complete Before/After Example

**Before**:
```json
{
  "permissions": {
    "allow": [
      "Read",
      "Write(src/**)",
      "Bash(git:*)",

      "Skill(shipkit-master)",
      "Skill(shipkit-project-status)",
      "Skill(shipkit-whats-next)"
    ],
    "deny": [
      "Bash(sudo:*)"
    ]
  }
}
```

**After** (adding "shipkit-user-stories"):
```json
{
  "permissions": {
    "allow": [
      "Read",
      "Write(src/**)",
      "Bash(git:*)",

      "Skill(shipkit-master)",
      "Skill(shipkit-project-status)",
      "Skill(shipkit-whats-next)",
      "Skill(shipkit-user-stories)"  <-- NEW
    ],
    "deny": [
      "Bash(sudo:*)"
    ]
  }
}
```

---

## Automation Pattern

**Using Python inline**:

```python
import json
from pathlib import Path

# Read settings
settings_path = Path('install/settings/shipkit.settings.json')
settings = json.loads(settings_path.read_text())

# Add skill permission
skill_permission = 'Skill(shipkit-{skill-name})'
if skill_permission not in settings['permissions']['allow']:
    settings['permissions']['allow'].append(skill_permission)

# Write back with proper formatting
settings_path.write_text(json.dumps(settings, indent=2) + '\n')

print(f"✓ Added {skill_permission} to settings.json")
```

---

## Why This Permission is Needed

**Claude Code permission system**:
- By default, skills are DENIED unless explicitly allowed
- `Skill(...)` permission grants Claude the ability to invoke the skill
- Without this permission, skill exists but cannot be used

**Permission format**:
```
Skill({skill-name})
```

**Examples**:
- `Skill(shipkit-spec)` - Allow invoking /shipkit-spec
- `Skill(shipkit-plan)` - Allow invoking /shipkit-plan
- `Skill(*)` - Allow ALL skills (not recommended)

---

## Common Mistakes

**❌ Missing parentheses**
```json
"Skill:shipkit-user-stories"  <-- ERROR: Wrong format
"Skill-shipkit-user-stories"  <-- ERROR: Wrong format
```

**❌ Trailing comma on last item**
```json
"Skill(shipkit-whats-next)",
"Skill(shipkit-user-stories)",  <-- ERROR: Trailing comma
]
```

**❌ Missing comma before new item**
```json
"Skill(shipkit-whats-next)"
"Skill(shipkit-user-stories)"  <-- ERROR: No comma between items
]
```

**❌ Single quotes instead of double quotes**
```json
'Skill(shipkit-user-stories)'  <-- ERROR: Must use double quotes
```

**❌ Inconsistent indentation**
```json
      "Skill(shipkit-whats-next)",
"Skill(shipkit-user-stories)"  <-- ERROR: Inconsistent indentation
```

**❌ Adding to wrong section**
```json
"deny": [
  "Skill(shipkit-user-stories)"  <-- ERROR: Should be in "allow"
]
```

---

## Validation Checklist

After updating:
- [ ] JSON syntax is valid (run Python validation)
- [ ] Permission uses correct format: `Skill(shipkit-{skill-name})`
- [ ] Entry is in `permissions.allow` array (NOT `deny`)
- [ ] Comma placement is correct
- [ ] Indentation matches existing entries
- [ ] No trailing comma on last array item

---

## Report Format

After updating, report:

```
✓ File 7: Updated settings.json
  - Added permission: Skill(shipkit-{skill-name})
  - Location: permissions.allow array
  - JSON syntax validated ✓
```
