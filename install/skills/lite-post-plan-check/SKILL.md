---
name: lite-post-plan-check
description: Hidden detection skill that scans implementation plans for data structure definitions (types, interfaces, schemas) and creates data contracts queue. Auto-triggered after /lite-plan completes. System skill - not user-invocable.
---

# lite-post-plan-check - Plan Data Structure Detection

**Purpose**: Automatically detect data structure definitions in plans and create queue for validating contracts across layers.

**Type**: System skill (hidden from users, auto-triggered)

**Trigger**: After `/lite-plan` completes

---

## What This Skill Does

**Detection:**
1. Reads the most recently created plan in `.shipkit-lite/plans/`
2. Scans for data structure mentions (User, Post, type definitions, interfaces, schemas)
3. Identifies which data types need contract validation

**Queue Creation:**
1. If data structures detected, creates `.shipkit-lite/.queues/define-data-contracts.md`
2. Lists each type with layers involved (database → backend → frontend)
3. Provides clear action items for `/lite-data-contracts`

**Output:**
- Queue file ready for `/lite-data-contracts` to process
- Terminal message suggesting next action

---

## When to Invoke

**Auto-triggered:**
- SessionStop hook after `/lite-plan` completes
- OR lite-milestone-detector routes to this skill

**Manual invocation:**
- Not intended for manual use
- Marked as system skill in manifest

---

## Detection Logic

**Data Structure Indicators:**

```python
STRUCTURE_PATTERNS = {
    'type_definitions': [
        r'type\s+(\w+)',           # type User = {...}
        r'interface\s+(\w+)',      # interface User {...}
        r'(\w+)\s*:\s*{',          # User: {...}
    ],
    'database_schemas': [
        r'CREATE TABLE\s+(\w+)',   # CREATE TABLE users
        r'schema\.(\w+)',          # schema.users
        r'table:\s*"(\w+)"',       # table: "users"
    ],
    'api_contracts': [
        r'POST\s+/api/(\w+)',      # POST /api/users
        r'GET\s+/api/(\w+)',       # GET /api/posts
        r'returns.*{',              # API returns {... }
    ],
}

# Common data types that often need contracts
COMMON_TYPES = ['User', 'Post', 'Comment', 'Product', 'Order', 'Session', 'Profile']
```

**Detection Algorithm:**
1. Read plan markdown content
2. Scan for type definitions, database schemas, API contracts
3. Extract entity names (User, Post, etc.)
4. Identify layers involved (database, backend, frontend)
5. Flag types that appear in multiple layers (need contracts!)

---

## Queue File Format

**Creates:** `.shipkit-lite/.queues/define-data-contracts.md`

**Content:**
```markdown
# Data Contracts To Define

**Created:** 2025-12-30 15:45
**Reason:** Plan defines data structures

## Pending

- [ ] User
  - Mentioned in: plans/auth-implementation.md
  - Layers: Database (users table) → API (GET /api/users/:id) → Frontend (User interface)
  - Contract needed: Define shape across all layers, prevent type mismatches

- [ ] Post
  - Mentioned in: plans/content-management.md
  - Layers: Database (posts table) → API (POST /api/posts) → Frontend (Post interface)
  - Contract needed: Ensure metadata field is consistently typed

## Completed

<!-- Items move here after /lite-data-contracts validates contracts -->
```

---

## Process

**Step 1: Find Latest Plan**
```python
from pathlib import Path
import os

def find_latest_plan():
    plans_dir = Path('.shipkit-lite/plans')
    if not plans_dir.exists():
        return None

    plans = list(plans_dir.glob('*.md'))
    if not plans:
        return None

    # Return most recently modified plan
    latest = max(plans, key=lambda p: os.path.getmtime(p))
    return latest
```

**Step 2: Detect Data Structures**
```python
import re

def detect_data_structures(plan_path):
    content = plan_path.read_text()

    detected_types = set()

    # Pattern 1: Type/Interface definitions
    type_matches = re.findall(r'(?:type|interface)\s+(\w+)', content)
    detected_types.update(type_matches)

    # Pattern 2: Database tables
    table_matches = re.findall(r'CREATE TABLE\s+(\w+)', content, re.IGNORECASE)
    detected_types.update(table_matches)

    # Pattern 3: Common entity names in caps
    for common_type in COMMON_TYPES:
        if common_type in content:
            detected_types.add(common_type)

    return detected_types
```

**Step 3: Identify Layers**
```python
def identify_layers(plan_content, type_name):
    """Determine which layers mention this type"""
    layers = []

    # Check for database mentions
    if any(keyword in plan_content.lower() for keyword in ['table', 'schema', 'sql', 'database']):
        if type_name.lower() in plan_content.lower():
            layers.append('Database')

    # Check for API mentions
    if any(keyword in plan_content.lower() for keyword in ['api', 'endpoint', 'route', 'get', 'post']):
        layers.append('Backend API')

    # Check for frontend mentions
    if any(keyword in plan_content.lower() for keyword in ['component', 'props', 'interface', 'frontend']):
        layers.append('Frontend')

    return layers
```

**Step 4: Create Queue**
```python
from datetime import datetime

def create_queue(detected_types, plan_path, plan_content):
    if not detected_types:
        print("✓ No data structures detected in plan")
        return

    queue_dir = Path('.shipkit-lite/.queues')
    queue_dir.mkdir(parents=True, exist_ok=True)

    queue_path = queue_dir / 'define-data-contracts.md'

    content = f"""# Data Contracts To Define

**Created:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Reason:** Plan defines data structures

## Pending

"""

    for type_name in sorted(detected_types):
        layers = identify_layers(plan_content, type_name)
        layers_str = ' → '.join(layers) if layers else 'Unknown layers'

        content += f"- [ ] {type_name}\n"
        content += f"  - Mentioned in: {plan_path.relative_to('.')}\n"
        content += f"  - Layers: {layers_str}\n"
        content += f"  - Contract needed: Define consistent shape across all layers\n\n"

    content += """## Completed

<!-- Items move here after /lite-data-contracts validates contracts -->
"""

    queue_path.write_text(content)

    print(f"✓ Created data contracts queue with {len(detected_types)} types")
    print(f"\n💡 Next: Run /lite-data-contracts to validate contracts")
```

---

## Script Location

**Detection script:** `scripts/detect-data-structures.py`

**Invocation:**
```bash
python .claude/skills/lite-post-plan-check/scripts/detect-data-structures.py
```

**Returns:**
- Exit 0: Success (queue created or no data structures detected)
- Exit 1: Error (plan not found, permissions issue)

---

## Integration with lite-whats-next

**After queue created:**
1. lite-whats-next scans `.shipkit-lite/.queues/`
2. Finds `define-data-contracts.md` queue
3. Suggests: "Run /lite-data-contracts - 3 types need contract validation"
4. User runs skill, contracts validated, reference created

---

## When This Skill Integrates with Others

### Before This Skill

**lite-plan** - Creates implementation plan
- **When**: Plan saved to plans/
- **Why**: Plan content is what we scan for data structure definitions
- **Trigger**: SessionStop after lite-plan completes

### After This Skill

**lite-data-contracts** - Validates data shape contracts
- **When**: Queue file exists with pending types
- **Why**: Prevents type mismatches between database → backend → frontend
- **Trigger**: lite-whats-next suggests it based on queue

---

## Context Files This Skill Reads

**Required:**
- `.shipkit-lite/plans/*.md` - Latest plan to scan

**Optional:**
- `.shipkit-lite/specs/active/*.md` - Related spec for additional context

---

## Context Files This Skill Writes

**Writes:**
- `.shipkit-lite/.queues/define-data-contracts.md` - Queue for data contracts

**Write Strategy:** CREATE or APPEND
- If queue doesn't exist: Create new
- If queue exists: Append new types to Pending section

---

## Success Criteria

Detection is successful when:
- [ ] Latest plan scanned for data structure mentions
- [ ] All types identified with layers
- [ ] Queue file created (if types found)
- [ ] Queue format matches template
- [ ] Terminal output suggests next action

---

## Edge Cases

**No plan exists:**
- Exit silently (nothing to detect)
- Don't create queue file

**Type already in queue:**
- Don't duplicate queue entries
- Update "Mentioned in" to include new plan

**Type mentioned but no layers detected:**
- Still add to queue with "Unknown layers"
- User can clarify during contract validation

---

**Remember**: This is a system skill - users never invoke it directly. It runs automatically after plans are created to enable proactive data contract validation.
