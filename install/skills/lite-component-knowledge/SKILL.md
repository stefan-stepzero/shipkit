---
name: lite-component-knowledge
description: "Use when documenting a React/UI component after implementation. Triggers: 'document component', 'how does X component work', 'component docs'."
---

# component-knowledge-lite - Per-File Component Documentation

**Purpose**: Document components with one file per component, enabling easy staleness detection and clean replacement when components change.

---

## When to Invoke

**User triggers**:
- "Document this component"
- "Update component docs"
- "How does [ComponentName] work?"
- "Document new components"

**After**:
- `/lite-implement` has created new components
- Component files have been modified
- Any time user wants fresh documentation

---

## Prerequisites

**Optional but helpful**:
- Existing docs: `.shipkit-lite/implementations/components/`
- Spec/plan context: `.shipkit-lite/specs/active/[feature].md`

**No strict prerequisites** - can document at any time.

---

## File Structure

```
.shipkit-lite/
  implementations/
    components/
      ComicConverter.md     ← One file per component (REPLACED on update)
      UserAvatar.md
      LoginForm.md
    routes/                 ← Managed by /lite-route-knowledge
      ...
    index.md                ← Auto-generated TOC with staleness
```

**Key principle**: One component = one file. No duplicates, no stale entries.

---

## Process

### Step 0: Check for Queue (Auto-Detect Mode)

**First, check if running in queue-driven mode**:

Read file (if exists): `.shipkit-lite/.queues/components-to-document.md`

**If queue file exists and has pending items**:
1. Parse the `## Pending` section for components needing documentation
2. For each pending component, proceed to Step 2
3. Move item from Pending to Completed in queue

**If queue file doesn't exist or is empty**:
- Continue to Step 1 (manual mode)

---

### Step 1: Identify Component to Document

**Ask user**:

1. **Which component?**
   - "Specific component?" (user provides name or path)
   - "Scan for undocumented components?"
   - "Scan for stale component docs?"

**If scanning**, use staleness detection:

```bash
# Find component source files
find src/components app/components -name "*.tsx" -o -name "*.jsx" 2>/dev/null

# For each component, check if doc exists and compare mtimes
```

**Output**:
```
🔍 Component scan:

| Component | Source | Doc | Status |
|-----------|--------|-----|--------|
| ComicConverter | 2h ago | 5d ago | ⚠️ STALE |
| UserAvatar | 3d ago | 2d ago | ✅ Fresh |
| LoginForm | 1h ago | missing | ❌ Undocumented |

Found 1 stale, 1 undocumented. Document these?
```

---

### Step 2: Read Component Source

**Read the component file**:

```bash
Read(src/components/ComicConverter.tsx)
```

**Extract**:
1. **Purpose**: What does this component do? (1-2 sentences)
2. **Props/API**: Interface and key props
3. **Pattern**: React patterns used (hooks, context, state)
4. **Dependencies**: External libraries
5. **Key decisions**: Why built this way?
6. **Usage**: Where is it imported? (grep if needed)
7. **Gotchas**: Non-obvious behavior, common errors

---

### Step 3: Write Component Documentation

**Write to individual file** (REPLACE strategy):

**Location**: `.shipkit-lite/implementations/components/[ComponentName].md`

**Template**:

```markdown
# [ComponentName]

> [One-line purpose]

**Source**: `[file-path]`
**Documented**: [YYYY-MM-DD HH:MM]
**Source Modified**: [timestamp from file]

## Purpose

[1-2 sentence description]

## Props/API

```typescript
interface [ComponentName]Props {
  [key props]
}
```

## Pattern & Architecture

- **Type**: [Presentational/Container/Page/Layout]
- **Rendering**: [CSR/SSR/Static]
- **State**: [Local/Context/Redux/Zustand/None]
- **Data fetching**: [None/useQuery/Server Component]

## Key Decisions

- **[Decision]**: [Rationale]

## Dependencies

- [Library]: [What it's used for]

## Usage

Imported by:
- `[file1]`
- `[file2]`

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

## Components

| Component | Documented | Source Modified | Status |
|-----------|------------|-----------------|--------|
| [ComicConverter](components/ComicConverter.md) | 2h ago | 2h ago | ✅ Fresh |
| [UserAvatar](components/UserAvatar.md) | 5d ago | 1d ago | ⚠️ Stale |

## Routes

| Route | Documented | Source Modified | Status |
|-------|------------|-----------------|--------|
| [api-comic](routes/api-comic.md) | 1d ago | 1d ago | ✅ Fresh |

---

**Staleness threshold**: Doc is stale if source modified after documentation.
```

**Index generation logic**:
1. Glob `.shipkit-lite/implementations/components/*.md`
2. For each doc, extract source path from frontmatter
3. Compare doc mtime vs source file mtime
4. Generate table with status

---

### Step 5: Confirm to User

**Output**:
```
✅ Component documented

📁 Created/Updated: .shipkit-lite/implementations/components/ComicConverter.md
📋 Index updated: .shipkit-lite/implementations/index.md

📊 Status:
  • Total components documented: 5
  • Fresh: 4
  • Stale: 1 (UserAvatar - source changed)

🔗 Source: src/components/ComicConverter.tsx
```

---

## Completion Checklist

Copy and track:
- [ ] Read component source file
- [ ] Extracted props, patterns, decisions
- [ ] Wrote to `implementations/components/[Name].md`
- [ ] Updated `implementations/index.md`

---

## What Makes This "Lite"

**Included**:
- ✅ One file per component (easy staleness detection)
- ✅ Replace strategy (no duplicates)
- ✅ Auto-generated index with status
- ✅ Source mtime comparison
- ✅ Purpose, props, patterns, gotchas

**Not included** (vs full component-knowledge):
- ❌ Dependency graph analysis
- ❌ Performance profiling
- ❌ Accessibility audit
- ❌ Storybook integration

---

## Write Strategy

**Strategy: REPLACE (per-file)**

| Location | Strategy | Rationale |
|----------|----------|-----------|
| `implementations/components/[Name].md` | **REPLACE** | One source of truth per component |
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
for each component doc in implementations/components/:
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

## Integration with Other Skills

**Before**:
- `/lite-implement` - Creates components (may queue for documentation)
- `/lite-post-implement-check` - May add to `.queues/components-to-document.md`

**After**:
- `/lite-quality-confidence` - Verify documentation exists
- `/lite-route-knowledge` - Document routes that use components

---

## Common Scenarios

### Scenario 1: Document Specific Component

```
User: "Document ComicConverter"

Claude:
1. Read src/components/ComicConverter.tsx
2. Extract purpose, props, patterns, decisions
3. Write to .shipkit-lite/implementations/components/ComicConverter.md
4. Regenerate index.md
5. Report success
```

### Scenario 2: Scan for Stale Docs

```
User: "Check component docs freshness"

Claude:
1. Glob implementations/components/*.md
2. For each, compare doc mtime vs source mtime
3. Report: "2 components have stale docs"
4. Offer to update them
```

### Scenario 3: Document All New Components

```
User: "Document undocumented components"

Claude:
1. Find all component source files
2. Check which have docs in implementations/components/
3. List undocumented ones
4. Ask which to document
5. Document each, regenerate index
```

---

## Tips

**Keep docs focused**:
- Purpose in 1-2 sentences
- Only key props (not every prop)
- Major decisions only

**Gotchas section is crucial**:
- Document API quirks
- Note required parameters
- Capture error causes and fixes
- This prevents repeat mistakes!

**When to document**:
- After implementing complex component
- Before PR/merge
- After fixing a bug (update gotchas!)

**When NOT to document**:
- Tiny utility components (<50 LOC)
- Component is self-explanatory

---

**Remember**: One file per component. Replace, don't append. Staleness detection keeps knowledge fresh.

---

## Context Files This Skill Reads

**Optional:**
- `.shipkit-lite/specs/active/[feature].md` - Feature context for component being documented
- `.shipkit-lite/.queues/components-to-document.md` - Queue of components needing documentation

**Source Files:**
- `src/components/**/*.tsx` - Component source files to document

---

## Context Files This Skill Writes

**Creates/Updates:**
- `.shipkit-lite/implementations/components/[Name].md` - Per-component documentation
  - **Write Strategy:** REPLACE (one source of truth per component)
- `.shipkit-lite/implementations/index.md` - Auto-generated TOC with staleness status
  - **Write Strategy:** REGENERATE (always reflects current state)

---

<!-- SECTION:success-criteria -->
## Success Criteria

Component Knowledge is complete when:
- [ ] Component source file has been read and analyzed
- [ ] Purpose, props, patterns, and decisions extracted
- [ ] Documentation written to `implementations/components/[Name].md`
- [ ] Index file regenerated at `implementations/index.md`
- [ ] Staleness status is accurate (doc timestamp vs source timestamp)
<!-- /SECTION:success-criteria -->

<!-- SECTION:after-completion -->
## After Completion

**Guardrails Check:** Before moving to next task, verify:

1. **Persistence** - Has important context been saved to `.shipkit-lite/`?
2. **Prerequisites** - Does the next action need a spec or plan first?
3. **Session length** - Long session? Consider `/lite-work-memory` for continuity.

**Natural capabilities** (no skill needed): Implementation, debugging, testing, refactoring, code documentation.

**Suggest skill when:** User needs to make decisions, create persistence, or check project status.
<!-- /SECTION:after-completion -->
