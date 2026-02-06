# Codebase Index Design

Reducing token waste from Claude's codebase exploration loops.

---

## The Problem

Claude spends excessive tokens doing the list → read → filter → repeat loop:

```
Claude: "Let me explore the project structure..."
→ Glob **/*.ts (lists 200 files)
→ Read file1.ts (500 lines, not what I need)
→ Read file2.ts (300 lines, not what I need)
→ Read file3.ts (finally found it)
= 1000s of tokens wasted
```

This happens **every session** because Claude has no memory of the codebase.

### Why This Matters

- Token usage explodes on "understand the project" tasks
- Same exploration repeated every conversation
- Slow response times while Claude reads irrelevant files
- Context window filled with file contents instead of actual work

---

## Proposed Solutions

### 1. Codebase Index File

A single MD file Claude reads first - the "map" of the project.

**Location:** `.shipkit/codebase-index.md`

**Contents:**
```markdown
# Codebase Index

Last updated: 2025-01-23

## Quick Reference

- **Entry point:** `src/index.ts`
- **Config:** `config/` directory
- **Tests:** `tests/` (Jest)

## Scripts

| Script | Purpose | Location |
|--------|---------|----------|
| `npm run build` | Compile TypeScript | `scripts/build.ts` |
| `npm run test` | Run test suite | `scripts/test.ts` |
| `npm run deploy` | Deploy to prod | `scripts/deploy.ts` |
| `npm run lint` | ESLint check | package.json |

## Key Files

| File | Purpose | Key Exports |
|------|---------|-------------|
| `src/index.ts` | Main entry point | `app`, `start()` |
| `src/api/routes.ts` | API route definitions | `router` |
| `src/db/schema.ts` | Database schema | `User`, `Post` |
| `src/utils/auth.ts` | Auth helpers | `verifyToken()` |

## Directory Structure

```
src/
├── api/          # REST API handlers
│   ├── routes.ts    # Route definitions
│   └── middleware/  # Express middleware
├── db/           # Database layer
│   ├── schema.ts    # Prisma/Drizzle schema
│   └── queries.ts   # Query functions
├── services/     # Business logic
└── utils/        # Shared utilities

scripts/          # Build/deploy scripts
tests/            # Test files (mirrors src/)
config/           # Environment configs
```

## Architecture Notes

- API follows REST conventions
- Database: PostgreSQL via Prisma
- Auth: JWT tokens, middleware in `src/api/middleware/auth.ts`
- Error handling: Centralized in `src/utils/errors.ts`
```

**Result:** Claude reads ~300 tokens once, knows where everything is.

---

### 2. File Header Convention

Standard header at top of each file (first 5-15 lines):

```typescript
/**
 * @file User API routes
 * @purpose CRUD operations for user management
 * @key-exports userRouter
 * @dependencies
 *   - src/db/users.ts (database queries)
 *   - src/utils/auth.ts (authentication)
 * @related src/api/middleware/auth.ts
 */

import { Router } from 'express';
// ... rest of file
```

**Benefits:**
- Claude reads first 10-20 lines, understands file purpose
- No need to read entire file to determine relevance
- Self-documenting, helps humans too

**Header Template:**
```
@file        - Filename/description
@purpose     - What this file does (1-2 sentences)
@key-exports - Main exports other files use
@dependencies - What this file imports (key ones)
@related     - Related files to check
```

---

### 3. Auto-Generated Index

Script that generates the index automatically:

```bash
#!/bin/bash
# generate-codebase-index.sh

OUTPUT=".shipkit/codebase-index.md"

echo "# Codebase Index" > $OUTPUT
echo "Generated: $(date)" >> $OUTPUT
echo "" >> $OUTPUT

# Extract package.json scripts
echo "## Scripts" >> $OUTPUT
jq -r '.scripts | to_entries | .[] | "| \(.key) | \(.value) |"' package.json >> $OUTPUT

# List key directories
echo "## Structure" >> $OUTPUT
tree -d -L 2 src/ >> $OUTPUT

# Extract file headers (first comment block)
echo "## File Summaries" >> $OUTPUT
for file in src/**/*.ts; do
  header=$(head -20 "$file" | grep -A5 "@purpose" | head -1)
  echo "- $file: $header" >> $OUTPUT
done
```

**When to run:**
- Git hook (pre-commit)
- Session start hook
- Manual when structure changes

---

## Implementation Plan

### Phase 1: Manual Index (Now)
- [ ] Create `.shipkit/codebase-index.md` template
- [ ] Document in CLAUDE.md to read index first
- [ ] Add to `shipkit-project-context` skill

### Phase 2: File Headers (Convention)
- [ ] Define header format standard
- [ ] Add headers to key files
- [ ] Create snippet/template for new files

### Phase 3: Automation (Later)
- [ ] Script to generate index from codebase
- [ ] Hook to regenerate on changes
- [ ] Validate headers exist on commit

---

## Integration Points

### With CLAUDE.md
```markdown
## Before Exploring Codebase
Always read `.shipkit/codebase-index.md` first.
This file contains the project map - scripts, key files, structure.
Only explore further if the index doesn't answer your question.
```

### With shipkit-project-context
The codebase index becomes part of project context loading:
```
/project-context
→ Loads why.md, stack.md, architecture.md
→ Also loads codebase-index.md
→ Claude has full picture without exploration
```

### With Session Start Hook
```python
# shipkit-session-start.py
# Remind Claude to check index before exploring
print("TIP: Check .shipkit/codebase-index.md before exploring files")
```

---

## Token Savings Estimate

| Scenario | Without Index | With Index | Savings |
|----------|---------------|------------|---------|
| "What scripts are available?" | ~2000 (reads package.json, scripts/) | ~300 (reads index) | 85% |
| "Where is auth handled?" | ~5000 (explores multiple files) | ~500 (index + 1 file) | 90% |
| "Understand project structure" | ~10000 (full exploration) | ~300 (reads index) | 97% |

---

## Open Questions

1. **How detailed should the index be?**
   - Too sparse: Claude still has to explore
   - Too detailed: Index itself becomes large

2. **How to keep it updated?**
   - Manual: Gets stale
   - Auto: Might miss context/purpose

3. **Should Claude update it?**
   - After exploring, Claude could add findings to index
   - Risk: Index grows unbounded

4. **File headers - enforce or suggest?**
   - Linting rule (enforce)
   - Convention in contributing guide (suggest)
