---
name: shipkit-codebase-index
description: "Generate project index for faster codebase navigation. Triggers: 'index codebase', 'create index', 'map project'."
context: fork
model: haiku
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
  - Write
---

# shipkit-codebase-index - Codebase Navigation Index

**Purpose**: Generate a lightweight index so Claude can navigate your codebase without wasteful exploration.

---

## When to Invoke

**User triggers**:
- "Index the codebase"
- "Create a project map"
- "Generate codebase index"

**Auto-suggested when**:
- Session hook detects no index exists
- Index is older than 14 days

---

## Process

### Step 1: Run Generator Script

```bash
python .claude/skills/shipkit-codebase-index/scripts/generate_index.py
```

**Script provides (100% reliable data):**
- `scripts` — from package.json
- `recentlyActive` — files from git history (last 14 days)
- `directories` — which common directories exist
- `configFiles` — which config files exist

**Script leaves empty (Claude fills in):**
- `framework`
- `entryPoints`
- `concepts`
- `coreFiles`
- `skip`

### Step 2: Claude Analyzes and Completes Index

**Read the generated index**, then fill in the empty fields:

1. **Detect framework** from `configFiles`:
   - `next.config.js` → Next.js
   - `vite.config.ts` → Vite
   - `prisma/schema.prisma` → uses Prisma
   - etc.

2. **Identify entry points** by checking which files exist:
   - `src/app/page.tsx` → app entry
   - `src/app/layout.tsx` → layout
   - `src/app/api/` → API routes
   - `prisma/schema.prisma` → database schema

3. **Map concepts to files** by scanning the codebase:
   - Look for auth-related files → `concepts.auth`
   - Look for database files → `concepts.database`
   - Look for payment/billing → `concepts.payments`
   - etc.

4. **Identify core files** — files that are imported by many others

5. **Ask user about skip list**:
   - "Any folders I should skip? (legacy, deprecated, etc.)"

### Step 3: Update the Index

```python
import json

with open('.shipkit/codebase-index.json') as f:
    index = json.load(f)

index['framework'] = 'next.js (app router)'
index['entryPoints'] = {
    'app': 'src/app/page.tsx',
    'layout': 'src/app/layout.tsx',
    'api': 'src/app/api/',
    'database': 'prisma/schema.prisma'
}
index['concepts'] = {
    'auth': ['src/lib/auth.ts', 'src/middleware.ts'],
    'database': ['src/lib/db.ts', 'prisma/schema.prisma'],
    # ... more concepts
}
index['coreFiles'] = ['src/lib/db.ts', 'src/lib/auth.ts']
index['skip'] = ['src/legacy/']

with open('.shipkit/codebase-index.json', 'w') as f:
    json.dump(index, f, indent=2)
```

### Step 4: Confirm to User

```
✅ Codebase index complete at .shipkit/codebase-index.json

Framework: next.js (app router)
Entry points: 4 (app, layout, api, database)
Concepts: 3 (auth, database, payments)
Recently active: 15 files
Skip: src/legacy/

I'll use this index to navigate faster.
```

---

## Division of Labor

| Task | Script | Claude |
|------|--------|--------|
| Parse package.json scripts | ✅ | |
| Get recently active files (git) | ✅ | |
| List existing directories | ✅ | |
| List existing config files | ✅ | |
| **Detect framework** | | ✅ |
| **Identify entry points** | | ✅ |
| **Map concepts to files** | | ✅ |
| **Identify core files** | | ✅ |
| **Determine skip list** | | ✅ |

**Principle**: Script does 100% reliable mechanical tasks. Claude does anything requiring judgment.

---

## Output: `.shipkit/codebase-index.json`

```json
{
  "generated": "2025-01-27",

  "scripts": {
    "dev": "next dev",
    "build": "next build"
  },

  "recentlyActive": [
    "src/app/api/payments/route.ts",
    "src/components/Checkout.tsx"
  ],

  "directories": [
    "src/app", "src/components", "src/lib", "prisma"
  ],

  "configFiles": [
    "next.config.js", "tsconfig.json", "prisma/schema.prisma"
  ],

  "framework": "next.js (app router)",

  "entryPoints": {
    "app": "src/app/page.tsx",
    "api": "src/app/api/",
    "database": "prisma/schema.prisma"
  },

  "concepts": {
    "auth": ["src/lib/auth.ts", "src/middleware.ts"],
    "database": ["src/lib/db.ts", "prisma/schema.prisma"]
  },

  "coreFiles": ["src/lib/db.ts", "src/lib/auth.ts"],

  "skip": ["src/legacy/"]
}
```

---

## How Claude Uses the Index

| Field | Question | How It Helps |
|-------|----------|--------------|
| `concepts` | "Where is auth?" | Direct lookup → file list |
| `entryPoints` | "Where do I start?" | Go-to files |
| `recentlyActive` | "What's being worked on?" | Recent focus |
| `coreFiles` | "What's important?" | High-dependency files |
| `skip` | "Should I read this?" | Avoid wasted context |
| `configFiles` | "What tools are used?" | Stack understanding |

---

## What Makes This "Lite"

**Included**:
- ✅ Git-based activity tracking
- ✅ Concept → file mapping
- ✅ Simple JSON format

**Not included**:
- ❌ Full dependency graphs
- ❌ Export analysis
- ❌ Complex scoring algorithms

**Philosophy**: Script does reliable work, Claude does intelligent work.

---

## Context Files This Skill Writes

- `.shipkit/codebase-index.json` — Complete replacement on each run

---

## Completion Checklist

- [ ] Script ran and created base index
- [ ] Framework detected
- [ ] Entry points identified
- [ ] Concepts mapped to files
- [ ] Core files identified
- [ ] User confirmed skip list (if any)
- [ ] Index saved

<!-- Shipkit v1.2.0 -->
