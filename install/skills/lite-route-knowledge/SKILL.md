---
name: lite-route-knowledge
description: "Use when documenting API routes or endpoints after implementation. Triggers: 'document route', 'API docs', 'endpoint docs', 'route documentation'."
---

# route-knowledge-lite - Per-File Route Documentation

**Purpose**: Document routes with one file per route, enabling easy staleness detection and clean replacement when routes change.

---

## When to Invoke

**User triggers**:
- "Document this route"
- "Document this page"
- "Update route docs"
- "How does [route] work?"
- "Document new routes"

**After**:
- `/lite-implement` has created new routes
- Route files have been modified
- Any time user wants fresh documentation

---

## Prerequisites

**Optional but helpful**:
- Existing docs: `.shipkit-lite/implementations/routes/`
- Spec/plan context: `.shipkit-lite/specs/active/[feature].md`
- Stack defined: `.shipkit-lite/stack.md` (for framework patterns)

**No strict prerequisites** - can document at any time.

---

## File Structure

```
.shipkit-lite/
  implementations/
    routes/
      dashboard.md           ← One file per route (REPLACED on update)
      api-user-profile.md
      settings.md
    components/              ← Managed by /lite-component-knowledge
      ...
    index.md                 ← Auto-generated TOC with staleness
```

**Key principle**: One route = one file. No duplicates, no stale entries.

---

## Process

### Step 0: Check for Queue (Auto-Detect Mode)

**First, check if running in queue-driven mode**:

Read file (if exists): `.shipkit-lite/.queues/routes-to-document.md`

**If queue file exists and has pending items**:
1. Parse the `## Pending` section for routes needing documentation
2. For each pending route, proceed to Step 2
3. Move item from Pending to Completed in queue

**If queue file doesn't exist or is empty**:
- Continue to Step 1 (manual mode)

---

### Step 1: Identify Route to Document

**Ask user**:

1. **Which route?**
   - "Specific route?" (user provides name or path)
   - "Scan for undocumented routes?"
   - "Scan for stale route docs?"

**If scanning**, use staleness detection:

```bash
# Find route source files based on framework
find app -name "page.tsx" -o -name "route.ts" 2>/dev/null

# For each route, check if doc exists and compare mtimes
```

**Output**:
```
🔍 Route scan:

| Route | Source | Doc | Status |
|-------|--------|-----|--------|
| /dashboard | 2h ago | 5d ago | ⚠️ STALE |
| /profile | 3d ago | 2d ago | ✅ Fresh |
| /api/user | 1h ago | missing | ❌ Undocumented |

Found 1 stale, 1 undocumented. Document these?
```

---

### Step 2: Read Route Source

**Read the route file**:

```bash
Read(app/dashboard/page.tsx)
# or
Read(app/api/user/profile/route.ts)
```

**Extract**:
1. **Route path**: What URL does this handle?
2. **Data fetching**: Server Component / Client / Hybrid / API
3. **Auth**: Middleware, guards, server-side checks, RLS
4. **Request/Response**: Types and schemas (for API routes)
5. **Dependencies**: Hooks, components, utilities
6. **Key decisions**: Why built this way?
7. **Gotchas**: Non-obvious behavior, common errors

---

### Step 3: Write Route Documentation

**Write to individual file** (REPLACE strategy):

**Location**: `.shipkit-lite/implementations/routes/[route-slug].md`

**Naming convention**:
- `/dashboard` → `dashboard.md`
- `/api/user/profile` → `api-user-profile.md`
- `/settings/[id]` → `settings-id.md`

**Template**:

```markdown
# [Route Path]

> [One-line purpose]

**Source**: `[file-path]`
**Documented**: [YYYY-MM-DD HH:MM]
**Source Modified**: [timestamp from file]

## Purpose

[1-2 sentence description]

## Data Strategy

- **Fetching**: [Server Component / Client Component / Hybrid / API Route]
- **Method**: [Direct query / Hook / Server Action / REST]
- **Sources**: [Database tables, APIs, etc.]

## Auth

- **Protected**: [Yes/No]
- **Method**: [Middleware / Component guard / Server-side / RLS]
- **Requires**: [Authenticated user / Specific role / Public]

## RLS Policies (if applicable)

- `[policy_name]`: [Description of what it allows]

## Request/Response (API routes only)

```typescript
// Request
interface [Route]Request {
  [fields]
}

// Response
interface [Route]Response {
  [fields]
}
```

## Dependencies

- **Hooks**: [list]
- **Components**: [list]
- **Utils**: [list]
- **Actions**: [Server Actions used]

## Key Decisions

- **[Decision]**: [Rationale]

## Gotchas & Common Errors

| Issue | Cause | Fix |
|-------|-------|-----|
| [Error] | [Why] | [Solution] |

## Notes

[Any other relevant details]
```

---

### Step 4: Update Index

**Regenerate index file**:

**Location**: `.shipkit-lite/implementations/index.md`

```markdown
# Implementations Index

*Auto-generated. Do not edit manually.*

**Last Updated**: [timestamp]

## Routes

| Route | Documented | Source Modified | Status |
|-------|------------|-----------------|--------|
| [/dashboard](routes/dashboard.md) | 2h ago | 2h ago | ✅ Fresh |
| [/api/user](routes/api-user-profile.md) | 5d ago | 1d ago | ⚠️ Stale |

## Components

| Component | Documented | Source Modified | Status |
|-----------|------------|-----------------|--------|
| [ComicConverter](components/ComicConverter.md) | 1d ago | 1d ago | ✅ Fresh |

---

**Staleness threshold**: Doc is stale if source modified after documentation.
```

**Index generation logic**:
1. Glob `.shipkit-lite/implementations/routes/*.md`
2. For each doc, extract source path from frontmatter
3. Compare doc mtime vs source file mtime
4. Generate table with status

---

### Step 5: Confirm to User

**Output**:
```
✅ Route documented

📁 Created/Updated: .shipkit-lite/implementations/routes/dashboard.md
📋 Index updated: .shipkit-lite/implementations/index.md

📊 Status:
  • Total routes documented: 5
  • Fresh: 4
  • Stale: 1 (api-user - source changed)

🔗 Source: app/dashboard/page.tsx
```

---

## Completion Checklist

Copy and track:
- [ ] Read route source file
- [ ] Extracted data strategy, auth, dependencies
- [ ] Wrote to `implementations/routes/[slug].md`
- [ ] Updated `implementations/index.md`

---

## What Makes This "Lite"

**Included**:
- ✅ One file per route (easy staleness detection)
- ✅ Replace strategy (no duplicates)
- ✅ Auto-generated index with status
- ✅ Source mtime comparison
- ✅ Data fetching, auth, RLS, dependencies

**Not included** (vs full route-knowledge):
- ❌ Performance metrics (load time, bundle size)
- ❌ SEO metadata extraction
- ❌ API contract validation
- ❌ Route param validation
- ❌ Internationalization detection

---

## Write Strategy

**Strategy: REPLACE (per-file)**

| Location | Strategy | Rationale |
|----------|----------|-----------|
| `implementations/routes/[slug].md` | **REPLACE** | One source of truth per route |
| `implementations/index.md` | **REGENERATE** | Always reflects current state |

**Why REPLACE beats APPEND**:
- No duplicate entries
- Easy to detect staleness (compare mtimes)
- Clean git diffs (one file changed)
- Selective loading (read only what you need)

**History preservation**: Git tracks file history. Each documentation update is a commit showing what changed.

---

## Staleness Detection

**Algorithm**:

```python
for each route doc in implementations/routes/:
    source_path = extract from doc header
    doc_mtime = file modification time of doc
    source_mtime = file modification time of source

    if source_mtime > doc_mtime:
        status = "STALE"
    else:
        status = "FRESH"
```

**Session start integration**: The session-start hook checks this and warns about stale docs.

---

## When This Skill Integrates with Others

### Before This Skill

**lite-implement** - Creates routes
- **When**: Implementation has created new routes
- **Why**: New routes need documentation
- **Trigger**: User asks "document route" or queue has pending items

**lite-post-implement-check** - Detects changes after implementation
- **When**: Implementation complete, changes detected
- **Why**: Adds routes to documentation queue
- **Trigger**: Creates `.queues/routes-to-document.md` with pending routes

### After This Skill

**lite-quality-confidence** - Verifies implementation quality
- **When**: Route documented, ready for quality check
- **Why**: Confirms documentation exists and is fresh
- **Trigger**: Quality audit checks for route documentation

**lite-component-knowledge** - Documents components
- **When**: Route uses components that need documentation
- **Why**: Routes and components are often documented together
- **Trigger**: User wants complete implementation documentation

---

## Context Files This Skill Reads

**Optional:**
- `.shipkit-lite/specs/active/[feature].md` - Feature context for route
- `.shipkit-lite/stack.md` - Framework patterns (Next.js App Router, etc.)
- `.shipkit-lite/.queues/routes-to-document.md` - Queue of routes needing documentation

**Source Files:**
- `app/**/page.tsx` - Next.js page routes
- `app/**/route.ts` - Next.js API routes
- `src/api/**/*.ts` - API route handlers

---

## Context Files This Skill Writes

**Creates/Updates:**
- `.shipkit-lite/implementations/routes/[slug].md` - Per-route documentation
  - **Write Strategy:** REPLACE (one source of truth per route)
- `.shipkit-lite/implementations/index.md` - Auto-generated TOC with staleness status
  - **Write Strategy:** REGENERATE (always reflects current state)

---

<!-- SECTION:success-criteria -->
## Success Criteria

Route Knowledge is complete when:
- [ ] Route source file has been read and analyzed
- [ ] Data strategy, auth, and dependencies extracted
- [ ] Documentation written to `implementations/routes/[slug].md`
- [ ] Index file regenerated at `implementations/index.md`
- [ ] Staleness status is accurate (doc timestamp vs source timestamp)
<!-- /SECTION:success-criteria -->

---

## Common Scenarios

### Scenario 1: Document Specific Route

```
User: "Document /dashboard"

Claude:
1. Read app/dashboard/page.tsx
2. Extract data strategy, auth, dependencies
3. Write to .shipkit-lite/implementations/routes/dashboard.md
4. Regenerate index.md
5. Report success
```

### Scenario 2: Scan for Stale Docs

```
User: "Check route docs freshness"

Claude:
1. Glob implementations/routes/*.md
2. For each, compare doc mtime vs source mtime
3. Report: "2 routes have stale docs"
4. Offer to update them
```

### Scenario 3: Document All New Routes

```
User: "Document undocumented routes"

Claude:
1. Find all route source files (based on framework)
2. Check which have docs in implementations/routes/
3. List undocumented ones
4. Ask which to document
5. Document each, regenerate index
```

---

## Tips

**Keep docs focused**:
- Purpose in 1-2 sentences
- Key data strategy info
- Auth requirements clearly stated

**Gotchas section is crucial**:
- Document API quirks
- Note auth edge cases
- Capture error causes and fixes
- This prevents repeat mistakes!

**When to document**:
- After implementing new route
- Before PR/merge
- After fixing a routing bug

**When NOT to document**:
- Simple static pages with no data/auth
- Redirects or trivial wrappers

---

**Remember**: One file per route. Replace, don't append. Staleness detection keeps knowledge fresh.

<!-- SECTION:after-completion -->
## After Completion

**Guardrails Check:** Before moving to next task, verify:

1. **Persistence** - Has important context been saved to `.shipkit-lite/`?
2. **Prerequisites** - Does the next action need a spec or plan first?
3. **Session length** - Long session? Consider `/lite-work-memory` for continuity.

**Natural capabilities** (no skill needed): Implementation, debugging, testing, refactoring, code documentation.

**Suggest skill when:** User needs to make decisions, create persistence, or check project status.
<!-- /SECTION:after-completion -->
