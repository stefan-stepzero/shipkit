# File 4: Update install/profiles/shipkit.manifest.json

**Purpose**: Add new skill to the manifest definitions array

**File**: `install/profiles/shipkit.manifest.json`

---

## Step 1: Read and Parse JSON

**Current structure**:
```json
{
  "edition": "shipkit",
  "description": "Lightweight Shipkit for POCs, side projects, and rapid iteration",

  "settingsFile": "shipkit.settings.json",
  "claudeMdFile": "shipkit.md",

  "skills": {
    "definitions": [
      "shipkit-master",
      "shipkit-project-status",
      "shipkit-project-context",
      ...
    ],
    "workspace": []
  },

  "agents": []
}
```

---

## Step 2: Add Skill to Definitions Array

**Find the `skills.definitions` array**:

```json
"skills": {
  "definitions": [
    "shipkit-master",
    "shipkit-project-status",
    "shipkit-project-context",
    "shipkit-spec",
    "shipkit-architecture-memory",
    "shipkit-ux-coherence",
    "shipkit-data-consistency",
    "shipkit-plan",
    "shipkit-implement",
    "shipkit-component-knowledge",
    "shipkit-route-knowledge",
    "shipkit-document-artifact",
    "shipkit-quality-confidence",
    "shipkit-user-instructions",
    "shipkit-integration-guardrails",
    "shipkit-work-memory",
    "shipkit-debug-systematically",
    "shipkit-communications",
    "shipkit-why-project",
    "shipkit-whats-next"
  ],
  "workspace": []
}
```

**Add new skill** (as last item before closing bracket):

```json
"skills": {
  "definitions": [
    "shipkit-master",
    "shipkit-project-status",
    "shipkit-project-context",
    "shipkit-spec",
    "shipkit-architecture-memory",
    "shipkit-ux-coherence",
    "shipkit-data-consistency",
    "shipkit-plan",
    "shipkit-implement",
    "shipkit-component-knowledge",
    "shipkit-route-knowledge",
    "shipkit-document-artifact",
    "shipkit-quality-confidence",
    "shipkit-user-instructions",
    "shipkit-integration-guardrails",
    "shipkit-work-memory",
    "shipkit-debug-systematically",
    "shipkit-communications",
    "shipkit-why-project",
    "shipkit-whats-next",
    "shipkit-NEW-SKILL"  <-- NEW (note: comma on previous line)
  ],
  "workspace": []
}
```

---

## Step 3: Validate JSON Syntax

**Critical points**:
1. **Comma placement**: Last item should NOT have trailing comma
2. **Quotes**: Use double quotes, not single quotes
3. **Indentation**: Maintain 2-space indentation

**Before adding** (last item has NO comma):
```json
    "shipkit-whats-next"
  ],
```

**After adding** (previous last item NOW has comma):
```json
    "shipkit-whats-next",
    "shipkit-NEW-SKILL"
  ],
```

---

## Step 4: Validate with Python

**Validation command**:
```bash
python -c "import json; json.load(open('install/profiles/shipkit.manifest.json'))"
```

**Expected output**:
- Success: No output (exit code 0)
- Failure: JSON syntax error message

**Common errors**:
```
JSONDecodeError: Expecting ',' delimiter
→ Missing comma between array items

JSONDecodeError: Expecting value
→ Extra trailing comma on last item
```

---

## Step 5: Visual Diff Check

**Before**:
```json
{
  "skills": {
    "definitions": [
      ... 19 skills ...
    ]
  }
}
```

**After**:
```json
{
  "skills": {
    "definitions": [
      ... 20 skills ...  <-- Count increased by 1
    ]
  }
}
```

---

## Complete Example

**Before**:
```json
{
  "edition": "shipkit",
  "skills": {
    "definitions": [
      "shipkit-master",
      "shipkit-project-status",
      "shipkit-whats-next"
    ],
    "workspace": []
  },
  "agents": []
}
```

**After** (adding "shipkit-user-stories"):
```json
{
  "edition": "shipkit",
  "skills": {
    "definitions": [
      "shipkit-master",
      "shipkit-project-status",
      "shipkit-whats-next",
      "shipkit-user-stories"  <-- NEW
    ],
    "workspace": []
  },
  "agents": []
}
```

---

## Automation Pattern

**Using Python inline**:

```python
import json
from pathlib import Path

# Read manifest
manifest_path = Path('install/profiles/shipkit.manifest.json')
manifest = json.loads(manifest_path.read_text())

# Add skill to definitions
skill_name = 'shipkit-{skill-name}'
if skill_name not in manifest['skills']['definitions']:
    manifest['skills']['definitions'].append(skill_name)

# Write back with proper formatting
manifest_path.write_text(json.dumps(manifest, indent=2) + '\n')

print(f"✓ Added {skill_name} to manifest.json")
```

---

## Common Mistakes

**❌ Trailing comma on last item**
```json
"shipkit-whats-next",
"shipkit-NEW-SKILL",  <-- ERROR: Trailing comma
]
```

**❌ Missing comma before new item**
```json
"shipkit-whats-next"
"shipkit-NEW-SKILL"  <-- ERROR: No comma between items
]
```

**❌ Single quotes instead of double quotes**
```json
'shipkit-NEW-SKILL'  <-- ERROR: Must use double quotes
```

**❌ Inconsistent indentation**
```json
  "shipkit-whats-next",
"shipkit-NEW-SKILL"  <-- ERROR: Inconsistent indentation
```

---

## Report Format

After updating, report:

```
✓ File 4: Updated manifest.json
  - Added "shipkit-{skill-name}" to definitions array
  - Total skills: {count}
  - JSON syntax validated ✓
```
