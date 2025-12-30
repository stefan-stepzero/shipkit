---
name: lite-component-knowledge
description: Documents components >200 LOC by comparing file modification times against documentation timestamps. Only documents new/changed components using timestamp-based freshness checking. Appends to implementations.md with metadata tracking.
---

# component-knowledge-lite - Timestamp-Based Component Documentation

**Purpose**: Document components intelligently by checking modification times against last documentation, avoiding redundant work and token waste.

---

## When to Invoke

**User triggers**:
- "Document this component"
- "Update component docs"
- "What changed since last documentation?"
- "Document new components"

**After**:
- `/lite-implement` has created new components
- Component files have been modified
- Any time user wants fresh documentation

---

## Prerequisites

**Optional but helpful**:
- Existing docs: `.shipkit-lite/implementations.md`
- Spec/plan context: `.shipkit-lite/specs/active/[feature].md`

**No strict prerequisites** - can document at any time.

---

## Process

### Step 1: Confirm What to Document

**Before doing anything**, ask user 2-3 questions:

1. **Which components should I check?**
   - "Specific component(s)?" (user provides path)
   - "All components in a directory?" (e.g., src/components/)
   - "Scan entire project?"

2. **What level of detail?**
   - "Quick summary (1-2 paragraphs per component)?"
   - "Detailed docs (purpose, props, patterns, usage)?"
   - "Minimal (just what changed)?"

3. **Documentation scope?**
   - "Only components >200 LOC?"
   - "Include smaller components?"
   - "Skip utility/helper files?"

**Why ask first**: Don't scan thousands of files if user wants specific component documented.

---

### Step 2: Check Documentation Freshness

**Read existing documentation metadata**:

```bash
# Read implementations.md to find last documentation timestamp
.shipkit-lite/implementations.md
```

**Look for metadata header** (at top of file):
```markdown
<!-- Component Documentation Metadata
Last Full Scan: 2025-01-15T14:30:00Z
Documented Files:
- src/components/RecipeCard.tsx (2025-01-15T14:25:00Z)
- src/components/UserProfile.tsx (2025-01-14T10:00:00Z)
-->
```

**If metadata missing**: This is first documentation run, scan all components.

---

### Step 3: Find Changed Files Using Bash

**Use bash find command to identify new/changed files**:

```bash
# Find files newer than implementations.md
find src/components -type f -name "*.tsx" -newer .shipkit-lite/implementations.md

# Or find files newer than specific timestamp (from metadata)
find src/components -type f -name "*.tsx" -newermt "2025-01-15 14:30:00"

# Count lines in changed files (skip if <200 LOC)
wc -l [changed-file-paths]
```

**Filter logic**:
- Only components >200 LOC (configurable based on user answer)
- Skip test files (*.test.tsx, *.spec.tsx)
- Skip utility files if requested

**Output to user**:
```
🔍 Freshness check:
  • implementations.md last updated: 2025-01-15 14:30:00
  • Found 23 total components
  • 21 already documented
  • 2 changed since last doc:
    - src/components/RecipeCard.tsx (450 LOC) ⚠️ Modified
    - src/components/NewFeature.tsx (320 LOC) ✨ New

📊 Token savings: Reading 2 files (~770 LOC) instead of all 23 (~5,200 LOC)
   → 92% reduction

Proceed with documenting these 2 components?
```

---

### Step 4: Read Only Changed Components

**For each changed component, read the file**:

```bash
# Use Read tool for each changed file
Read(src/components/RecipeCard.tsx)
Read(src/components/NewFeature.tsx)
```

**Extract from each file**:
1. **Purpose**: What does this component do? (1-2 sentences)
2. **Pattern**: React patterns used (hooks, context, state management)
3. **Props/API**: Key props or function signatures
4. **Key decisions**: Why was it built this way?
5. **Usage locations**: Where is it used? (grep for imports if needed)
6. **Dependencies**: External libraries used
7. **State management**: Local state, context, or external store?

**Token budget**: ~200-500 tokens per component analysis.

---

### Step 5: Generate Documentation

**Use Write tool to APPEND to implementations.md**:

**Location**: `.shipkit-lite/implementations.md`

**Format** (append to end of file):

```markdown
---

## Component: [ComponentName] - Documented [Date]

**File**: `[file-path]`
**Size**: [LOC] lines
**Last Modified**: [timestamp from file]
**Documented**: [current timestamp]

### Purpose
[1-2 sentence description of what this component does]

### Pattern & Architecture
- **Type**: [Presentational/Container/Page/Layout/etc.]
- **Rendering**: [CSR/SSR/Static]
- **State**: [Local useState/Context/Redux/Zustand/None]
- **Data fetching**: [None/useQuery/useEffect/Server Component/etc.]

### Props/API
```typescript
interface Props {
  [key props extracted from file]
}
```

### Key Decisions
- **[Decision 1]**: [Why this approach]
- **[Decision 2]**: [Rationale]

### Usage Locations
- [File 1 that imports this]
- [File 2 that imports this]

### Dependencies
- [External library 1]
- [External library 2]

### Notes
[Any non-obvious implementation details, gotchas, or future improvements]

---
```

**Before appending, update metadata header**:

```markdown
<!-- Component Documentation Metadata
Last Full Scan: [current timestamp]
Documented Files:
- src/components/RecipeCard.tsx ([current timestamp])
- src/components/UserProfile.tsx (2025-01-14T10:00:00Z)
- src/components/NewFeature.tsx ([current timestamp])
-->
```

---

### Step 6: Suggest Next Step

**After documentation complete**:

```
✅ Component documentation updated

📁 Updated: .shipkit-lite/implementations.md

📋 Documented:
  • RecipeCard.tsx (450 LOC) - Updated existing docs
  • NewFeature.tsx (320 LOC) - New documentation

🔖 Metadata updated:
  • Last scan: [timestamp]
  • Total documented: 23 components

👉 Next options:
  1. /lite-quality-confidence - Pre-ship verification
  2. /lite-work-memory - Log this session's progress
  3. /lite-route-knowledge - Document API routes/pages
  4. Continue implementing

What would you like to do?
```

---

## What Makes This "Lite"

**Included**:
- ✅ Timestamp-based freshness checking
- ✅ Incremental documentation (only changed files)
- ✅ LOC filtering (skip small utilities)
- ✅ Purpose, pattern, props, decisions
- ✅ Metadata tracking

**Not included** (vs full component-knowledge):
- ❌ Dependency graph analysis
- ❌ Performance profiling
- ❌ Accessibility audit
- ❌ Visual regression testing
- ❌ Storybook integration
- ❌ Automated prop extraction via AST parsing

**Philosophy**: Document what changed efficiently, not comprehensive component catalog.

---

## Freshness Algorithm

**How timestamp checking works**:

```
IF implementations.md doesn't exist:
  → Document all components
ELSE:
  → Read metadata header for last scan timestamp
  → Use bash find -newermt to get changed files
  → Read only changed files
  → Update only changed documentation
  → Update metadata header
```

**Example savings**:

| Scenario | Total Components | Changed | Tokens Without Freshness | Tokens With Freshness | Savings |
|----------|------------------|---------|--------------------------|----------------------|---------|
| Initial scan | 0 | 0 | 0 | 0 | N/A |
| After 1 week | 23 | 2 | ~5,000 | ~400 | 92% |
| After 1 day | 23 | 1 | ~5,000 | ~200 | 96% |
| No changes | 23 | 0 | ~5,000 | ~50 | 99% |

**This is the "lite" advantage**: Only read what changed.

---

## Integration with Other Skills

**Before component-knowledge-lite**:
- `/lite-implement` - Creates components
- `/lite-plan` - May reference component architecture

**After component-knowledge-lite**:
- `/lite-quality-confidence` - Verify component quality
- `/lite-work-memory` - Log documentation work
- `/lite-route-knowledge` - Document routes that use these components

**During implement-lite**:
- After completing complex component (>200 LOC), suggest:
  ```
  Component complete. Document it?
  → /lite-component-knowledge
  ```

---

## Context Files This Skill Reads

**Always reads**:
- `.shipkit-lite/implementations.md` - Existing docs + metadata

**Conditionally reads**:
- Component files (only changed ones based on timestamps)
- `.shipkit-lite/specs/active/[feature].md` - Context for why component exists
- `.shipkit-lite/architecture.md` - Patterns to reference

---

## Context Files This Skill Writes

**Write Strategy: APPEND (with metadata header update)**

**Primary output**:
- `.shipkit-lite/implementations.md`
  - **Strategy**: APPEND
  - **Content**: Component documentation entries appended to end of file
  - **Metadata**: Header updated each run with new timestamps and file list
  - **Why APPEND**: Preserves historical documentation trail showing component evolution over time. Essential for tracking when components were documented and enabling timestamp-based freshness checking (the core "lite" optimization).

**Never modifies**:
- Component source files (read-only analysis)
- Specs, plans, architecture

**Archive behavior**: None (APPEND keeps all history in single file)

**When history matters**: Always. Each documentation run appends new entries with timestamps, creating an audit trail of component changes. The metadata header tracks latest state while the body preserves full chronological history.

---

## Lazy Loading Behavior

**This skill loads minimally**:

1. User invokes `/lite-component-knowledge`
2. Claude asks: "Which components to check?"
3. Claude reads implementations.md metadata (~100 tokens)
4. Claude runs bash find to identify changed files (~50 tokens)
5. **Only if changes found**: Claude reads changed components (~200-500 tokens each)
6. Claude appends documentation
7. Total context: ~500-2000 tokens (vs ~5000+ if reading all components)

**Not loaded unless needed**:
- Unchanged components
- Unrelated specs/plans
- User tasks
- Other documentation

---

## Success Criteria

Documentation is complete when:
- [ ] Metadata header updated with current timestamp
- [ ] All changed components documented
- [ ] Each component doc includes: purpose, pattern, props, decisions, usage
- [ ] LOC threshold respected (skip small files)
- [ ] Timestamp-based freshness check performed
- [ ] User can see what changed vs what's already documented

---

## Template Structure

**Complete documentation templates**: See `references/documentation-templates.md`

**Includes**:
- Metadata header format (for timestamp tracking)
- Component entry template (for each documented component)
- ISO 8601 timestamp format
- Example filled templates

---

## Common Scenarios

### Scenario 1: First Documentation Run

```
User: "Document all components"

Claude:
1. Ask: "Scan which directory? Default: src/components/"
2. Ask: "LOC threshold? Default: >200 LOC"
3. User confirms
4. implementations.md doesn't exist
5. Glob src/components/**/*.tsx
6. Count LOC for each file
7. Filter: Keep only files >200 LOC
8. Read each file
9. Extract: purpose, pattern, props, decisions, usage
10. Create implementations.md with metadata header
11. Append all component docs
```

### Scenario 2: Incremental Update (Most Common)

```
User: "Update component docs"

Claude:
1. Read implementations.md metadata header
2. Last scan: 2025-01-15T14:30:00Z
3. Run: find src/components -type f -name "*.tsx" -newermt "2025-01-15 14:30:00"
4. Found 2 changed files
5. Read only those 2 files
6. Extract documentation
7. Update existing entries OR append new entries
8. Update metadata header with new timestamp
9. Report: "Documented 2 changed components (21 unchanged)"
```

### Scenario 3: No Changes Detected

```
User: "Document components"

Claude:
1. Read implementations.md metadata
2. Last scan: 1 hour ago
3. Run: find src/components -newer .shipkit-lite/implementations.md
4. No files found
5. Output:
   "No components changed since last documentation (1 hour ago).
    All 23 components are up to date.

    Run anyway to re-document everything? (not recommended)"
```

### Scenario 4: Specific Component

```
User: "Document RecipeCard component"

Claude:
1. Skip timestamp check (user specified exact file)
2. Read src/components/RecipeCard.tsx
3. Extract documentation
4. Update/append to implementations.md
5. Update metadata for just this file
```

---

## Tips for Effective Component Documentation

**Keep it focused**:
- Purpose in 1-2 sentences max
- Only key props (not every prop)
- Major decisions only (not every line choice)

**Use grep for usage**:
```bash
# Find where component is imported
grep -r "import.*RecipeCard" src/
```

**Extract patterns efficiently**:
- Look for useState/useEffect/useContext/useQuery near top
- Check if file exports default or named
- Scan for external imports (libraries)

**When to document**:
- After implementing complex component (>200 LOC)
- Before PR/merge (document what you built)
- After modifying existing component significantly

**When NOT to document**:
- Tiny utility components (<50 LOC)
- Test files
- Component is obvious (basic button wrapper)

**When to upgrade to full /component-knowledge**:
- Need dependency graph analysis
- Building component library
- Multiple teams sharing components
- Require accessibility audit
- Performance profiling needed

---

## Metadata Format Specification

**Complete metadata specification**: See `references/documentation-templates.md`

**Key details**:
- Timestamp format: ISO 8601 (YYYY-MM-DDTHH:MM:SSZ)
- Tracks: Last full scan timestamp + per-file timestamps
- Enables: Incremental updates via timestamp comparison
- Provides: Audit trail of documentation changes

---

**Remember**: This skill's superpower is efficiency. By checking timestamps and reading only changed files, it saves 90%+ tokens compared to naive "read everything" approach. Perfect for POC/MVP where components evolve rapidly.
