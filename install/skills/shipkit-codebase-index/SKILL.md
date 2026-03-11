---
name: shipkit-codebase-index
description: "Generate project index for faster codebase navigation. Triggers: 'index codebase', 'create index', 'map project'."
context: fork
model: haiku
allowed-tools: Read, Glob, Grep, Bash, Write
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

### Completion Tracking (MANDATORY)

Before starting analysis, create tasks for each index section:

1. `TaskCreate`: "Run generator script (base index)"
2. `TaskCreate`: "Detect framework"
3. `TaskCreate`: "Identify entry points"
4. `TaskCreate`: "Map concepts to files (with verification)"
5. `TaskCreate`: "Identify core files (with import counts)"
6. `TaskCreate`: "Determine skip list"
7. `TaskCreate`: "Write completed codebase-index.json"
8. `TaskCreate`: "Verify all 5 Claude-filled fields are populated"

**Rules:**
- `TaskUpdate` each task to `completed` only after the section has verified data (not guesses)
- The final verification task requires reading the written file and confirming: framework, entryPoints, concepts, coreFiles, and skip are all non-empty
- Do NOT declare done if any field is empty or contains placeholder values

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

**Read the generated index**, then fill in the empty fields.

**USE SUBAGENT FOR CONCEPT MAPPING** - Launch Explore subagent for efficient parallel scanning:

```
Task tool with subagent_type: "Explore"
Prompt: "Scan codebase to build navigation index. Find and report:

1. FRAMEWORK: Check for next.config.*, vite.config.*, nuxt.config.*, etc.
2. ENTRY POINTS: Find main app entry, layout, API routes directory, database schema
3. CONCEPTS: Map these concepts to files:
   - auth: files handling authentication, sessions, login
   - database: db connections, models, schema
   - payments: billing, subscriptions, checkout
   - api: API route handlers
   - components: reusable UI components
4. CORE FILES: Files imported by 5+ other files (high fan-in)

For each concept, list the actual file paths found.
For core files, include import count."
```

**Why subagent**: Concept mapping requires scanning multiple directories and patterns in parallel. Explore agent is optimized for this and reduces main conversation context.

**Fallback** (if subagent unavailable) - Manual detection:

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

### Step 2.5: Verification Requirements

Before claiming any index entry, verify it with tool calls:

| Claim | Required Verification |
|-------|----------------------|
| "Config file exists" | `Glob: pattern="next.config.*"` returns match |
| "Entry point at X" | `Read: file_path="X"` succeeds AND contains valid component/export |
| "Concept maps to files" | `Grep: pattern="concept-keyword"` returns matches |
| "Core file (highly imported)" | `Grep: pattern="import.*from.*filename"` returns high count |

**Verification sequence for each entry type:**

```
Config files:
  1. Glob: pattern="[config-pattern]"
  2. If empty → don't include in index
  3. If found → add to configFiles with verified path

Entry points:
  1. Glob: pattern="[entry-path]"
  2. If empty → mark as "unverified" or skip
  3. If found → Read file, confirm it exports something meaningful
  4. Add to entryPoints with status: "verified"

Concepts:
  1. Grep: pattern="[concept-keyword]" glob="**/*.{ts,tsx}"
  2. List ALL matching files
  3. If 0 matches → don't add concept
  4. If matches → add concept with verified file list

Core files:
  1. Grep: pattern="import.*from.*[filename]" glob="**/*.{ts,tsx}"
  2. Count imports per file
  3. Files with >5 imports → core files
  4. Include import count in index
```

**Mark unverified entries:** If verification cannot be completed, mark entry as `status: "unverified"` in index rather than guessing.

**See also:** `shared/references/VERIFICATION-PROTOCOL.md` for standard verification patterns.

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
  "generated": "YYYY-MM-DD",
  "scripts": { "<name>": "<command>" },
  "recentlyActive": ["path/to/file.ts"],
  "directories": ["src/app", "src/components"],
  "configFiles": ["next.config.js", "tsconfig.json"],
  "framework": "next.js (app router)",
  "entryPoints": { "app": "...", "api": "...", "database": "..." },
  "concepts": { "auth": [...], "database": [...] },
  "coreFiles": ["src/lib/db.ts"],
  "skip": ["src/legacy/"]
}
```

**Full schema reference:** See `references/output-schema.md`

**Realistic example:** See `references/example.json`

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
