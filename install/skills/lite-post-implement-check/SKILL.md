---
name: lite-post-implement-check
description: Hidden detection skill that scans for recently modified components and routes after implementation, creating documentation queues. Auto-triggered after /lite-implement completes. System skill - not user-invocable.
---

# lite-post-implement-check - Implementation Change Detection

**Purpose**: Automatically detect new/modified components and routes after implementation and create queues for documentation.

**Type**: System skill (hidden from users, auto-triggered)

**Trigger**: After `/lite-implement` completes

---

## What This Skill Does

**Detection:**
1. Scans for recently modified files (last 60 minutes by default)
2. Identifies:
   - Components in `src/components/`, `app/components/`, etc.
   - Routes in `src/app/*/route.ts`, `src/api/`, etc.
   - Service integrations (imports from external packages)
3. Categorizes changes by type

**Queue Creation:**
1. Creates `.shipkit-lite/.queues/components-to-document.md` if components found
2. Creates `.shipkit-lite/.queues/routes-to-document.md` if routes found
3. Creates `.shipkit-lite/.queues/integrations-used.md` if new service usage detected

**Output:**
- Queue files ready for documentation skills
- Terminal message suggesting next actions

---

## Detection Logic

**File patterns:**
```python
COMPONENT_PATTERNS = [
    'src/components/**/*.tsx',
    'src/components/**/*.jsx',
    'app/components/**/*.tsx',
    'components/**/*.tsx',
]

ROUTE_PATTERNS = [
    'src/app/**/route.ts',
    'src/app/**/route.js',
    'src/api/**/*.ts',
    'app/api/**/*.ts',
]

SERVICE_IMPORTS = {
    'stripe': 'from "stripe"',
    'supabase': 'from "@supabase/supabase-js"',
    'openai': 'from "openai"',
    's3': 'from "@aws-sdk/client-s3"',
}
```

**Time window:**
- Default: Files modified in last 60 minutes
- Configurable via environment variable

---

## Queue Files Created

### 1. components-to-document.md
Lists recently modified components that need documentation

### 2. routes-to-document.md
Lists recently created/modified routes that need API documentation

### 3. integrations-used.md
Lists newly detected service integrations that need pattern verification

---

## Script Location

**Detection script:** `scripts/detect-changes.py`

**Usage:**
```bash
python scripts/detect-changes.py [--since-minutes 60]
```

---

## Integration with Other Skills

### Before This Skill
- `/lite-implement` - Implements features, modifies files

### After This Skill
- `/lite-component-knowledge` - Documents components from queue
- `/lite-route-knowledge` - Documents routes from queue
- `/lite-integration-docs` - Verifies integration patterns from queue

---

## Context Files This Skill Reads

**Scans:**
- `src/components/**/*` - Component files
- `src/app/**/route.*` - Route files
- `src/api/**/*` - API files
- File modification times (last 60 min)

---

## Context Files This Skill Writes

**Creates:**
- `.shipkit-lite/.queues/components-to-document.md`
- `.shipkit-lite/.queues/routes-to-document.md`
- `.shipkit-lite/.queues/integrations-used.md`

---

## Edge Cases

**No recent changes:**
- Exit silently, no queues created

**File already in queue:**
- Don't duplicate, update modification time

**Multiple file types in one component:**
- Group by component name (e.g., Button.tsx + Button.test.tsx → Button)

---

**Remember**: Runs automatically after implementation to catch documentation needs before they're forgotten.
