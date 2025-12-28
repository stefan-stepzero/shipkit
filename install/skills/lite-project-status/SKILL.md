---
name: lite-project-status
description: Provides instant project health summary by scanning .shipkit-lite context files, detecting gaps, checking freshness, and suggesting next actions. Use when user asks "what's the state?", "project status?", or needs orientation.
---

# project-status-lite - Project Health Dashboard

**Purpose**: Scan `.shipkit-lite/` context files to provide instant project health summary, identify documentation gaps, and suggest next actions based on detected issues.

---

## When to Invoke

**User triggers**:
- "What's the state?"
- "Project status?"
- "What should I work on?"
- "Show me project health"
- "Where am I?"

**After**:
- Session start (orientation)
- Coming back to project after time away
- Before starting new work (sanity check)

---

## Prerequisites

**Optional**:
- `.shipkit-lite/` exists (if missing, will suggest setup)

---

## Process

### Step 1: Check if Shipkit Lite Exists

**Before scanning, check if directory exists**:

```bash
# Check for .shipkit-lite/ directory
if [ ! -d ".shipkit-lite" ]; then
  echo "❌ No .shipkit-lite/ directory found"
  echo ""
  echo "Run /lite-project-context to initialize project context"
  exit
fi
```

**If missing**: Tell user to run `/lite-project-context` first.

---

### Step 2: Scan Core Context Files

**Scan these files for existence and freshness**:

```bash
# Core context files to check
.shipkit-lite/stack.md
.shipkit-lite/architecture.md
.shipkit-lite/implementations.md
.shipkit-lite/progress.md
```

**For each file, check**:
1. Does it exist?
2. When was it last modified? (use `stat` command)
3. Is content meaningful (>50 bytes)?

**Freshness indicators**:
- ✓ Modified within last 24 hours = Fresh
- ⚠ Modified 1-7 days ago = Aging
- ✗ Modified >7 days ago OR missing = Stale

---

### Step 3: Count Documented Items

**Parse each context file and count documented elements**:

**stack.md**:
- Count sections (Framework, Database, Key Libraries, etc.)
- Extract tech stack summary

**architecture.md**:
- Count decisions (count markdown H2/H3 headings)
- Extract recent decisions

**implementations.md**:
- Count documented components/routes (count H2 sections)
- Extract file paths mentioned

**progress.md**:
- Count session entries
- Get last session date

---

### Step 4: Detect Gaps

**Use bash commands to find undocumented components**:

```bash
# Find all TypeScript/JavaScript files >200 LOC
find src -type f \( -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.jsx" \) -exec wc -l {} + | awk '$1 > 200 {print $2}'

# Cross-reference with implementations.md
# Files NOT mentioned in implementations.md are gaps
```

**Gap types to detect**:
- Large files (>200 LOC) not documented in implementations.md
- package.json modified more recently than stack.md
- Database migration files newer than schema.md (if it exists)
- Active specs with no corresponding plans
- Plans with no implementation notes

---

### Step 5: Scan Specs, Plans, and Tasks

**Check workflow progress**:

```bash
# Count active specs
ls -1 .shipkit-lite/specs/active/*.md 2>/dev/null | wc -l

# Count plans
ls -1 .shipkit-lite/plans/*.md 2>/dev/null | wc -l

# Count user tasks
if [ -f ".shipkit-lite/user-tasks/active.md" ]; then
  grep -c "^- \[ \]" .shipkit-lite/user-tasks/active.md
fi
```

**Workflow gap detection**:
- If specs exist but no plans → Need `/lite-plan`
- If plans exist but no implementation notes → Need `/lite-implement`
- If tasks exist but all unchecked → Work stalled

---

### Step 6: Generate Status Report

**Write health summary to `.shipkit-lite/status.md`** AND display in terminal:

**Include timestamp at top**:
```bash
# Add timestamp to status report
echo "Last Updated: $(date '+%Y-%m-%d %H:%M:%S')" > .shipkit-lite/status.md
echo "" >> .shipkit-lite/status.md
```

**Format**:
```
Last Updated: 2025-12-28 14:32:15

📊 Project Status (.shipkit-lite)

════════════════════════════════════════════════════

CORE CONTEXT

✓ Stack: documented (Next.js 14, Supabase, Tailwind)
⚠ Stack freshness: 2 days old
  → package.json modified today
  → Run /lite-project-context to refresh

✓ Architecture: 12 decisions logged
  → Last updated: 1 day ago

⚠ Implementations: 23 components documented
  → 2 undocumented files >200 LOC:
     • src/lib/auth.ts (347 lines)
     • src/components/DataTable.tsx (215 lines)
  → Run /lite-component-knowledge to document

✓ Progress: 8 sessions logged
  → Last session: 6 hours ago

════════════════════════════════════════════════════

WORKFLOW STATUS

✓ Specs: 2 active
  • recipe-sharing.md
  • user-profile.md

✗ Plans: 0 plans found
  → Run /lite-plan for active specs

✗ Implementations: No implementation notes
  → Run /lite-implement after planning

⚠ User Tasks: 5 active, 0 completed
  → Tasks defined but no progress

════════════════════════════════════════════════════

SUGGESTED NEXT ACTIONS

Priority 1: Run /lite-project-context (stack is stale)
Priority 2: Run /lite-plan for recipe-sharing spec
Priority 3: Document large components with /lite-component-knowledge

════════════════════════════════════════════════════
```

---

### Step 7: Determine Next Action Suggestions

**Based on detected gaps, suggest ONE priority action**:

**Decision logic**:

```
IF .shipkit-lite/ doesn't exist:
  → "Run /lite-project-context to initialize"

ELSE IF stack.md is stale (>7 days) OR package.json newer than stack.md:
  → "Run /lite-project-context to refresh stack"

ELSE IF active specs exist AND no plans exist:
  → "Run /lite-plan for [spec-name]"

ELSE IF plans exist AND no implementation notes:
  → "Run /lite-implement to start coding"

ELSE IF large undocumented files exist:
  → "Run /lite-component-knowledge to document [file]"

ELSE IF no architectural decisions logged:
  → "Run /lite-architecture-memory to log decisions"

ELSE IF user tasks all unchecked:
  → "Start working on tasks or update with /lite-user-instructions"

ELSE:
  → "Project is healthy! Continue development."
```

---

## Health Check Logic

### Status Indicators

**Use these symbols consistently**:
- ✓ = Healthy (exists, fresh, complete)
- ⚠ = Warning (exists but issues detected)
- ✗ = Critical (missing or severely outdated)

### Freshness Calculation

```bash
# Get file modification time in seconds since epoch
file_modified=$(stat -c %Y "$file" 2>/dev/null)

# Get current time
now=$(date +%s)

# Calculate age in days
age_days=$(( (now - file_modified) / 86400 ))

if [ $age_days -le 1 ]; then
  echo "✓ Fresh (modified today)"
elif [ $age_days -le 7 ]; then
  echo "⚠ Aging (modified $age_days days ago)"
else
  echo "✗ Stale (modified $age_days days ago)"
fi
```

### Gap Detection Patterns

**Large undocumented files**:
```bash
# Find files >200 LOC
large_files=$(find src -type f \( -name "*.ts" -o -name "*.tsx" \) -exec wc -l {} + | awk '$1 > 200 {print $2}')

# Check if mentioned in implementations.md
for file in $large_files; do
  if ! grep -q "$file" .shipkit-lite/implementations.md; then
    echo "⚠ Undocumented: $file"
  fi
done
```

**Stale stack**:
```bash
# Compare package.json and stack.md timestamps
if [ package.json -nt .shipkit-lite/stack.md ]; then
  echo "⚠ Stack outdated: package.json modified after stack.md"
fi
```

**Workflow gaps**:
```bash
# Specs without plans
spec_count=$(ls -1 .shipkit-lite/specs/active/*.md 2>/dev/null | wc -l)
plan_count=$(ls -1 .shipkit-lite/plans/*.md 2>/dev/null | wc -l)

if [ $spec_count -gt $plan_count ]; then
  echo "⚠ $((spec_count - plan_count)) specs have no plans"
fi
```

---

## What Makes This "Lite"

**Included**:
- ✅ Fast scanning (<5 seconds)
- ✅ Core context file checks (stack, architecture, implementations, progress)
- ✅ Basic gap detection (large files, stale docs, workflow gaps)
- ✅ Terminal output only (no file creation)
- ✅ Actionable suggestions

**Not included** (vs full shipkit-status):
- ❌ Deep codebase analysis
- ❌ Dependency vulnerability scanning
- ❌ Test coverage reports
- ❌ Performance metrics
- ❌ Git history analysis
- ❌ Team collaboration metrics

**Philosophy**: Quick health check to orient developer, not comprehensive audit.

---

## Integration with Other Skills

**Before project-status-lite**:
- Session start (user wants orientation)
- Any time (user wants to check state)

**After project-status-lite**:
- Suggests skill based on detected gaps
- User follows suggestion or ignores

---

## Context Files This Skill Reads

**Always attempts to read**:
- `.shipkit-lite/stack.md`
- `.shipkit-lite/architecture.md`
- `.shipkit-lite/implementations.md`
- `.shipkit-lite/progress.md`

**Conditionally reads**:
- `.shipkit-lite/specs/active/*.md` (glob to count)
- `.shipkit-lite/plans/*.md` (glob to count)
- `.shipkit-lite/user-tasks/active.md` (if exists)
- `.shipkit-lite/schema.md` (if exists)
- `.shipkit-lite/types.md` (if exists)

**Also checks**:
- `package.json` (for stack freshness comparison)
- `src/**/*.{ts,tsx,js,jsx}` (for undocumented large files)

---

## Context Files This Skill Writes

**Creates**: `.shipkit-lite/status.md`

**Write Strategy**: **OVERWRITE AND REPLACE**

**Rationale**: Status is a point-in-time snapshot. Each invocation completely replaces the previous status report. Old status data has no historical value - if stack was stale yesterday and you fixed it, you don't need to remember it was stale. Users want the latest health check, not an archive of past statuses.

**Content written**:
- Timestamp of status check
- Core context health (stack, architecture, implementations, progress)
- Workflow status (specs, plans, implementations, tasks)
- Detected gaps and warnings
- Prioritized next action suggestions

**When file is updated**:
- Every time `/lite-project-status` is invoked
- Completely overwrites previous content
- No archiving or history preservation

**Why OVERWRITE instead of APPEND**:
- Status is ephemeral (yesterday's status is irrelevant)
- Prevents file bloat (skill runs frequently: session start, after changes, when lost)
- No use case for historical status comparison
- Users want "what's the state NOW" not "show me all past status checks"

---

## Success Criteria

Status check is complete when:
- [ ] All core context files scanned
- [ ] Freshness calculated for each file
- [ ] Documented items counted
- [ ] Gaps detected and listed
- [ ] Workflow status checked
- [ ] Prioritized next action suggested
- [ ] Status report written to `.shipkit-lite/status.md` (OVERWRITE previous)
- [ ] Terminal summary displayed (same content as file)

---

## Example Output Scenarios

### Scenario 1: Healthy Project

```
📊 Project Status (.shipkit-lite)

════════════════════════════════════════════════════

CORE CONTEXT

✓ Stack: documented (Next.js 14, Supabase, Tailwind)
  → Last updated: 3 hours ago

✓ Architecture: 8 decisions logged
  → Last updated: 1 day ago

✓ Implementations: 15 components documented
  → All large files documented

✓ Progress: 12 sessions logged
  → Last session: 2 hours ago

════════════════════════════════════════════════════

WORKFLOW STATUS

✓ Specs: 1 active (user-profile.md)
✓ Plans: 1 plan exists (user-profile-plan.md)
✓ Implementations: 3 components implemented
✓ User Tasks: 8 active, 12 completed

════════════════════════════════════════════════════

SUGGESTED NEXT ACTIONS

✓ Project is healthy!

Next: Continue implementing user-profile feature
      Run /lite-implement to continue coding

════════════════════════════════════════════════════
```

### Scenario 2: Stale Stack

```
📊 Project Status (.shipkit-lite)

════════════════════════════════════════════════════

CORE CONTEXT

⚠ Stack: outdated
  → Last updated: 5 days ago
  → package.json modified today (new dependencies added)
  → Run /lite-project-context to refresh

✓ Architecture: 3 decisions logged
✓ Implementations: 7 components documented
✓ Progress: 4 sessions logged

════════════════════════════════════════════════════

SUGGESTED NEXT ACTIONS

Priority 1: Run /lite-project-context (stack is stale)

════════════════════════════════════════════════════
```

### Scenario 3: Workflow Gap

```
📊 Project Status (.shipkit-lite)

════════════════════════════════════════════════════

CORE CONTEXT

✓ Stack: documented (Next.js 14, Supabase)
✓ Architecture: 6 decisions logged
⚠ Implementations: 10 components documented
  → 3 undocumented files >200 LOC
✓ Progress: 6 sessions logged

════════════════════════════════════════════════════

WORKFLOW STATUS

✓ Specs: 3 active
  • recipe-sharing.md
  • user-profile.md
  • notification-system.md

✗ Plans: 0 plans found
  → Specs exist but no implementation plans

════════════════════════════════════════════════════

SUGGESTED NEXT ACTIONS

Priority 1: Run /lite-plan for recipe-sharing spec
Priority 2: After planning, run /lite-implement
Priority 3: Document large components with /lite-component-knowledge

════════════════════════════════════════════════════
```

### Scenario 4: Fresh Project

```
📊 Project Status (.shipkit-lite)

════════════════════════════════════════════════════

CORE CONTEXT

✗ Directory not found: .shipkit-lite/

════════════════════════════════════════════════════

SUGGESTED NEXT ACTIONS

Initialize project context:
→ Run /lite-project-context to scan codebase and generate:
  • stack.md (from package.json)
  • schema.md (from migrations)
  • Initial context files

════════════════════════════════════════════════════
```

---

## Tips for Effective Status Checks

**When to run**:
- Start of every session (orientation)
- After major changes (added dependencies, refactored)
- When feeling lost (what should I work on?)
- Before planning new features (understand current state)

**How to interpret**:
- ✓ symbols = Keep going
- ⚠ symbols = Address soon (not urgent)
- ✗ symbols = Address now (blocking issue)

**Follow suggestions**:
- Suggested skills are prioritized by impact
- Don't ignore stale stack warnings (can cause confusion)
- Document large files before they become unmaintainable

**When to upgrade to full /shipkit-status**:
- Need team collaboration metrics
- Need test coverage analysis
- Need dependency vulnerability scanning
- Need performance benchmarks

---

## Special Notes

**This skill is unique**:
- Writes single status file (`.shipkit-lite/status.md`) using OVERWRITE strategy
- Fast execution (<5 seconds)
- Terminal output mirrors file content
- Can run anytime - safe to invoke frequently

**Design decisions**:
- Uses bash for file scanning (glob, stat, wc, grep)
- Writes status snapshot to persistent file (`.shipkit-lite/status.md`)
- OVERWRITE strategy (point-in-time data, no historical value)
- Focused on actionability (suggests next skill)
- Optimized for POC/MVP context (doesn't check production concerns)

**Freshness logic**:
- Compares file timestamps
- Detects package.json changes vs stack.md
- Flags large undocumented files
- Identifies workflow bottlenecks

---

**Remember**: This is an orientation tool. Run it when you need to know "where am I?" and "what should I do next?". It's designed to be fast, informative, and actionable.
