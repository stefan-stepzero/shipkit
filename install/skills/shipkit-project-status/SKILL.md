---
name: shipkit-project-status
description: "Use when user asks about project health or needs orientation. Triggers: 'what's the status', 'project health', 'where are we', 'what's done'."
model: haiku
context: fork
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---

# shipkit-project-status - Project Health Dashboard

**Purpose**: Scan `.shipkit/` context files to provide instant project health summary, identify documentation gaps, and suggest next actions based on detected issues.

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
- `.shipkit/` exists (if missing, will suggest setup)

---

## Process

### Step 1: Check if Shipkit Exists

**Before scanning, check if directory exists**:

```bash
# Check for .shipkit/ directory
if [ ! -d ".shipkit" ]; then
  echo "❌ No .shipkit/ directory found"
  echo ""
  echo "Run /shipkit-project-context to initialize project context"
  exit
fi
```

**If missing**: Tell user to run `/shipkit-project-context` first.

---

### Step 2: Scan Core Context Files

**Scan these files for existence and freshness**:

```bash
# Core context files to check
.shipkit/stack.json
.shipkit/architecture.md
.shipkit/implementations.md
.shipkit/progress.md
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

**stack.json**:
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

**Verification before claiming gaps:**

| Gap Claim | Required Verification |
|-----------|----------------------|
| "Undocumented file" | Glob confirms file exists + Grep in implementations.md returns 0 |
| "Stale documentation" | Compare file mtime vs doc mtime (use stat) |
| "Missing spec" | Glob for `specs/active/*.md` matching feature name returns empty |
| "Orphan plan" | Plan exists but Grep for implementation references returns 0 |

**Never claim "undocumented" without:**
1. `Glob`: Confirming the file exists
2. `Grep`: Searching implementations.md for the filename
3. If Grep returns 0: File is undocumented (valid gap)

**Gap types to detect**:
- Large files (>200 LOC) not documented in implementations.md
- package.json modified more recently than stack.json
- Database migration files newer than schema.md (if it exists)
- Active specs with no corresponding plans
- Plans with no implementation notes

---

### Step 5: Scan Specs, Plans, and Tasks

**Check workflow progress**:

```bash
# Count active specs
ls -1 .shipkit/specs/active/*.md 2>/dev/null | wc -l

# Count plans
ls -1 .shipkit/plans/*.md 2>/dev/null | wc -l

# Count user tasks
if [ -f ".shipkit/user-tasks/active.md" ]; then
  grep -c "^- \[ \]" .shipkit/user-tasks/active.md
fi
```

**Workflow gap detection**:
- If specs exist but no plans → Need `/shipkit-plan`
- If plans exist but no implementation notes → Need `implement (no skill needed)`
- If tasks exist but all unchecked → Work stalled

---

### Step 5.5: Analyze Skill Usage

**Read skill usage tracking data**:

```bash
# Check if tracking file exists
if [ -f ".shipkit/skill-usage.json" ]; then
  cat .shipkit/skill-usage.json
fi
```

**Parse JSON to extract**:
1. Total invocations count
2. Top 5 most-used skills (by count)
3. Skills never used (0 invocations)
4. Stale skills (not used in 14+ days)
5. Skills that might help current state

**Cross-reference with project state**:
- If active specs exist but `/shipkit-plan` not used recently → Suggest it
- If implementation in progress but `/shipkit-verify` never used → Suggest it
- If approaching release but `/shipkit-preflight` stale → Suggest it

**Skill categories for analysis**:
- **Discovery**: shipkit-product-discovery, shipkit-why-project, shipkit-project-context
- **Planning**: shipkit-spec, shipkit-plan, shipkit-prototyping
- **Implementation**: shipkit-architecture-memory, shipkit-data-contracts, shipkit-integration-docs
- **Quality**: shipkit-verify, shipkit-preflight, shipkit-ux-audit

---

### Step 6: Generate Status Report

**Write health summary to `.shipkit/status.json`** AND display formatted summary in terminal.

**Use Write tool to create/overwrite**: `.shipkit/status.json`

The output MUST conform to the JSON Schema below. This is a strict contract -- mission control and other skills depend on this structure.

**Terminal display**: After writing the JSON file, display a human-readable formatted summary to the user (not raw JSON). Example:

```
Status saved.

Location: .shipkit/status.json

  Health Score: 72/100
  Core Context: 3/4 files present (1 stale)
  Specs: 2 active | Plans: 0 | Tasks: 5 active

  Gaps Found: 4
    - stack.json is stale (2 days, package.json modified since)
    - 2 undocumented files >200 LOC
    - Active specs have no plans

  Top Recommendations:
    1. /shipkit-project-context (stack is stale)
    2. /shipkit-plan for recipe-sharing spec
    3. Document large components manually

  Skill Usage: 47 total invocations, 2 never used, 2 stale
```

---

## JSON Schema

```json
{
  "$schema": "shipkit-artifact",
  "type": "project-status",
  "version": "1.0",
  "lastUpdated": "YYYY-MM-DD",
  "source": "shipkit-project-status",

  "summary": {
    "healthScore": 72,
    "totalSpecs": 2,
    "totalPlans": 0,
    "totalTasks": 5,
    "gapsFound": 4,
    "coreFilesPresent": 3,
    "coreFilesTotal": 4
  },

  "coreContext": [
    {
      "file": "stack.json",
      "exists": true,
      "freshness": "aging",
      "lastModified": "2025-12-26",
      "sizeBytes": 1240,
      "notes": "package.json modified more recently"
    },
    {
      "file": "architecture.md",
      "exists": true,
      "freshness": "fresh",
      "lastModified": "2025-12-27",
      "sizeBytes": 3420,
      "itemCount": 12,
      "notes": "12 decisions logged"
    },
    {
      "file": "implementations.md",
      "exists": true,
      "freshness": "fresh",
      "lastModified": "2025-12-28",
      "sizeBytes": 5100,
      "itemCount": 23,
      "notes": "23 components documented"
    },
    {
      "file": "progress.md",
      "exists": true,
      "freshness": "fresh",
      "lastModified": "2025-12-28",
      "sizeBytes": 2800,
      "itemCount": 8,
      "notes": "8 sessions logged"
    }
  ],

  "workflow": {
    "specs": {
      "activeCount": 2,
      "files": ["specs/active/recipe-sharing.md", "specs/active/user-profile.md"]
    },
    "plans": {
      "count": 0,
      "files": []
    },
    "tasks": {
      "activeCount": 5,
      "completedCount": 0
    }
  },

  "gaps": [
    {
      "id": "stale-stack",
      "severity": "warning",
      "category": "freshness",
      "description": "stack.json is stale (2 days old, package.json modified since)",
      "suggestedAction": "/shipkit-project-context"
    },
    {
      "id": "undocumented-auth",
      "severity": "warning",
      "category": "undocumented",
      "description": "src/lib/auth.ts (347 lines) not documented in implementations.md",
      "file": "src/lib/auth.ts",
      "lineCount": 347,
      "suggestedAction": "Document component manually"
    },
    {
      "id": "undocumented-datatable",
      "severity": "warning",
      "category": "undocumented",
      "description": "src/components/DataTable.tsx (215 lines) not documented in implementations.md",
      "file": "src/components/DataTable.tsx",
      "lineCount": 215,
      "suggestedAction": "Document component manually"
    },
    {
      "id": "specs-without-plans",
      "severity": "critical",
      "category": "workflow-gap",
      "description": "2 active specs have no corresponding plans",
      "suggestedAction": "/shipkit-plan"
    }
  ],

  "skillUsage": {
    "totalInvocations": 47,
    "mostUsed": [
      { "skill": "shipkit-spec", "count": 12 },
      { "skill": "shipkit-plan", "count": 8 },
      { "skill": "shipkit-project-context", "count": 6 }
    ],
    "neverUsed": ["shipkit-ux-audit", "shipkit-data-contracts"],
    "stale": [
      { "skill": "shipkit-verify", "daysSinceUse": 21, "count": 2 },
      { "skill": "shipkit-preflight", "daysSinceUse": 18, "count": 1 }
    ]
  },

  "recommendations": [
    {
      "priority": 1,
      "action": "/shipkit-project-context",
      "reason": "Stack context is stale — package.json modified more recently"
    },
    {
      "priority": 2,
      "action": "/shipkit-plan",
      "reason": "Active specs (recipe-sharing, user-profile) have no plans"
    },
    {
      "priority": 3,
      "action": "Document components manually",
      "reason": "2 large files (>200 LOC) are undocumented"
    }
  ]
}
```

### Field Reference

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `$schema` | string | yes | Always `"shipkit-artifact"` -- identifies as Shipkit-managed file |
| `type` | string | yes | Always `"project-status"` -- artifact type for routing/rendering |
| `version` | string | yes | Schema version for forward compatibility |
| `lastUpdated` | string | yes | ISO date of last status check |
| `source` | string | yes | Always `"shipkit-project-status"` |
| `summary` | object | yes | Aggregated counts for dashboard rendering |
| `summary.healthScore` | number | yes | 0-100 score based on freshness, gaps, and workflow state |
| `summary.totalSpecs` | number | yes | Count of active specs |
| `summary.totalPlans` | number | yes | Count of plans |
| `summary.totalTasks` | number | yes | Count of active user tasks |
| `summary.gapsFound` | number | yes | Total number of detected gaps |
| `summary.coreFilesPresent` | number | yes | How many of 4 core context files exist |
| `summary.coreFilesTotal` | number | yes | Always 4 (stack, architecture, implementations, progress) |
| `coreContext` | array | yes | Status of each core `.shipkit/` context file |
| `coreContext[].file` | string | yes | Filename (relative to `.shipkit/`) |
| `coreContext[].exists` | boolean | yes | Whether the file exists |
| `coreContext[].freshness` | enum | yes | `"fresh"` (<24h) \| `"aging"` (1-7d) \| `"stale"` (>7d) \| `"missing"` |
| `coreContext[].lastModified` | string | no | ISO date of last modification (omit if missing) |
| `coreContext[].sizeBytes` | number | no | File size in bytes (omit if missing) |
| `coreContext[].itemCount` | number | no | Count of documented items (decisions, components, sessions) |
| `coreContext[].notes` | string | no | Human-readable summary of file state |
| `workflow` | object | yes | Status of specs, plans, and tasks |
| `workflow.specs.activeCount` | number | yes | Number of active spec files |
| `workflow.specs.files` | string[] | yes | Paths to active spec files |
| `workflow.plans.count` | number | yes | Number of plan files |
| `workflow.plans.files` | string[] | yes | Paths to plan files |
| `workflow.tasks.activeCount` | number | yes | Number of active (unchecked) tasks |
| `workflow.tasks.completedCount` | number | yes | Number of completed tasks |
| `gaps` | array | yes | Detected documentation and workflow gaps |
| `gaps[].id` | string | yes | Slug identifier for the gap |
| `gaps[].severity` | enum | yes | `"critical"` \| `"warning"` \| `"info"` |
| `gaps[].category` | enum | yes | `"freshness"` \| `"undocumented"` \| `"workflow-gap"` \| `"missing"` |
| `gaps[].description` | string | yes | Human-readable description of the gap |
| `gaps[].file` | string | no | File path associated with gap (if applicable) |
| `gaps[].lineCount` | number | no | Line count for undocumented file gaps |
| `gaps[].suggestedAction` | string | yes | Skill or action to resolve the gap |
| `skillUsage` | object | no | Skill usage analytics (omit if no tracking data) |
| `skillUsage.totalInvocations` | number | yes | Total tracked invocations |
| `skillUsage.mostUsed` | array | yes | Top skills by usage count |
| `skillUsage.neverUsed` | string[] | yes | Skills with 0 invocations |
| `skillUsage.stale` | array | yes | Skills not used in 14+ days |
| `recommendations` | array | yes | Prioritized next actions |
| `recommendations[].priority` | number | yes | Priority rank (1 = highest) |
| `recommendations[].action` | string | yes | Skill command or action to take |
| `recommendations[].reason` | string | yes | Why this action is recommended |

### Summary Object

The `summary` field MUST be kept in sync with the scan results. It exists so the dashboard can render overview cards without traversing the full structure. Recompute it every time the file is written.

### Health Score Calculation

Compute `healthScore` (0-100) based on weighted factors:

| Factor | Weight | Scoring |
|--------|--------|---------|
| Core files present | 30 | 0 pts per missing, 7.5 pts per existing |
| Core files freshness | 25 | 0 pts stale, 12.5 pts aging, 25 pts all fresh |
| Workflow completeness | 25 | Specs+plans+tasks scored proportionally |
| Documentation coverage | 20 | Based on ratio of documented vs undocumented large files |

---

### Step 7: Determine Next Action Suggestions

**Based on detected gaps, suggest ONE priority action**:

**Decision logic**:

```
IF .shipkit/ doesn't exist:
  → "Run /shipkit-project-context to initialize"

ELSE IF stack.json is stale (>7 days) OR package.json newer than stack.json:
  → "Run /shipkit-project-context to refresh stack"

ELSE IF active specs exist AND no plans exist:
  → "Run /shipkit-plan for [spec-name]"

ELSE IF plans exist AND no implementation notes:
  → "Run implement (no skill needed) to start coding"

ELSE IF large undocumented files exist:
  → "Run document components manually to document [file]"

ELSE IF no architectural decisions logged:
  → "Run /shipkit-architecture-memory to log decisions"

ELSE IF user tasks all unchecked:
  → "Start working on tasks or update with /shipkit-user-instructions"

ELSE:
  → "Project is healthy! Continue development."
```

**Skill usage recommendations** (additive, shown in SKILL USAGE section):

```
IF active specs exist AND /shipkit-plan not used in 7+ days:
  → "💡 You have active specs → consider /shipkit-plan"

IF implementation in progress AND /shipkit-verify never used:
  → "💡 Implementation phase → /shipkit-verify would help"

IF plans completed AND /shipkit-preflight stale (14+ days):
  → "💡 Approaching release? → /shipkit-preflight for final checks"

IF quality skills never used (verify, preflight, ux-audit):
  → "💡 Quality skills unused → consider adding quality checks"

IF discovery skills stale AND no recent specs:
  → "💡 No recent discovery → /shipkit-product-discovery for new features"
```

---

## Health Check Logic

### Status Indicators

**Use these symbols consistently**:
- ✓ = Healthy (exists, fresh, complete)
- ⚠ = Warning (exists but issues detected)
- ✗ = Critical (missing or severely outdated)

### Freshness and Gap Detection

The bash commands for freshness checking and gap detection are documented inline in Steps 1-5 above.

---

## Shipkit Artifact Convention

This skill follows the **Shipkit JSON artifact convention** -- a standard structure for all `.shipkit/*.json` files that enables mission control visualization.

**Every JSON artifact MUST include these top-level fields:**

```json
{
  "$schema": "shipkit-artifact",
  "type": "<artifact-type>",
  "version": "1.0",
  "lastUpdated": "YYYY-MM-DD",
  "source": "<skill-name>",
  "summary": { ... }
}
```

- `$schema` -- Always `"shipkit-artifact"`. Lets the reporter hook identify files to ship to mission control.
- `type` -- The artifact type (`"project-status"`, `"goals"`, `"spec"`, etc.). Dashboard uses this for rendering.
- `version` -- Schema version. Bump when fields change.
- `lastUpdated` -- When this file was last written.
- `source` -- Which skill wrote this file.
- `summary` -- Aggregated data for dashboard cards. Structure varies by type.

Skills that haven't migrated to JSON yet continue writing markdown. The reporter hook ships both: JSON artifacts get structured dashboard rendering, markdown files fall back to metadata-only (exists, date, size).

---

## Completion Checklist

Copy and track:
- [ ] Scanned `.shipkit/` for context files
- [ ] Checked freshness and completeness
- [ ] Reported gaps and suggested actions

---

## What Makes This "Lite"

**Included**:
- ✅ Fast scanning (<5 seconds)
- ✅ Core context file checks (stack, architecture, implementations, progress)
- ✅ Basic gap detection (large files, stale docs, workflow gaps)
- ✅ JSON artifact output (`.shipkit/status.json`) + terminal summary
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

## When This Skill Integrates with Others

### Before This Skill
- None - This skill can run anytime for orientation
  - **When**: User wants to check project health
  - **Why**: Need current status before deciding what to work on
  - **Trigger**: User asks "what's the status?", "what should I do?", or session start

### After This Skill
- Suggests skill dynamically based on detected gaps
  - **When**: After status scan completes
  - **Why**: Status identifies what's missing or stale - next action should fix it
  - **Trigger**: Specific gap detected

**Common suggestions**:

- `/shipkit-project-context` - When stack.json is stale or missing
  - **When**: package.json modified after stack.json OR .shipkit/ doesn't exist
  - **Why**: Stale stack causes wrong tech assumptions
  - **Trigger**: Freshness check fails

- `/shipkit-plan` - When specs exist but no plans
  - **When**: Found .shipkit/specs/active/*.md but no .shipkit/plans/*.md
  - **Why**: Specs without plans block implementation
  - **Trigger**: Workflow gap detected

- `document components manually` - When large files undocumented
  - **When**: Found src/**/*.ts files >200 LOC not mentioned in implementations.md
  - **Why**: Undocumented code becomes unmaintainable
  - **Trigger**: Gap detection finds undocumented files

- `implement (no skill needed)` - When plans exist but no implementation notes
  - **When**: Found plans/*.md but no recent implementation entries
  - **Why**: Plans without execution are just ideas
  - **Trigger**: Workflow gap detected

---

## Context Files This Skill Reads

**Always attempts to read**:
- `.shipkit/stack.json`
- `.shipkit/architecture.md`
- `.shipkit/implementations.md`
- `.shipkit/progress.md`

**Conditionally reads**:
- `.shipkit/specs/active/*.md` (glob to count)
- `.shipkit/plans/*.md` (glob to count)
- `.shipkit/user-tasks/active.md` (if exists)
- `.shipkit/schema.md` (if exists)
- `.shipkit/types.md` (if exists)
- `.shipkit/skill-usage.json` (if exists, for usage analytics)

**Also checks**:
- `package.json` (for stack freshness comparison)
- `src/**/*.{ts,tsx,js,jsx}` (for undocumented large files)

---

## Context Files This Skill Writes

**Write Strategy: OVERWRITE**

**Creates/Updates**:
- `.shipkit/status.json` - Project health status (JSON artifact)

**Rationale**: Status is a point-in-time snapshot. Each invocation completely replaces the previous status report. Old status data has no historical value -- if stack was stale yesterday and you fixed it, you don't need to remember it was stale. Users want the latest health check, not an archive of past statuses.

**Content written** (see JSON Schema section for full structure):
- Artifact metadata (`$schema`, `type`, `version`, `lastUpdated`, `source`)
- Summary with health score and counts
- Core context file inventory with freshness
- Workflow status (specs, plans, tasks)
- Detected gaps with severity and suggested actions
- Skill usage analytics (if tracking data exists)
- Prioritized recommendations

**Update Behavior**:
- Each write REPLACES entire file contents
- No archiving or history preservation
- No File Exists Workflow (always overwrite -- status is ephemeral)

**Why OVERWRITE instead of APPEND**:
- Status is ephemeral (yesterday's status is irrelevant)
- Prevents file bloat (skill runs frequently: session start, after changes, when lost)
- No use case for historical status comparison
- Users want "what's the state NOW" not "show me all past status checks"

---

<!-- SECTION:after-completion -->
## After Completion

**Guardrails Check:** Before moving to next task, verify:

1. **Persistence** - Has important context been saved to `.shipkit/`?
2. **Prerequisites** - Does the next action need a spec or plan first?
3. **Session length** - Long session? Consider `/shipkit-work-memory` for continuity.

**Natural capabilities** (no skill needed): Implementation, debugging, testing, refactoring, code documentation.

**Suggest skill when:** User needs to make decisions, create persistence, or check project status.
<!-- /SECTION:after-completion -->

<!-- SECTION:success-criteria -->
## Success Criteria

Status check is complete when:
- [ ] All core context files scanned
- [ ] Freshness calculated for each file
- [ ] Documented items counted
- [ ] Gaps detected and listed
- [ ] Workflow status checked
- [ ] Skill usage analyzed (if tracking data exists)
- [ ] Prioritized next action suggested
- [ ] Output conforms to JSON schema (all required fields present)
- [ ] Summary field counts are accurate
- [ ] Status report written to `.shipkit/status.json` (OVERWRITE previous)
- [ ] Terminal summary displayed (human-readable format, not raw JSON)
<!-- /SECTION:success-criteria -->
---

## Example Output Scenarios

See the JSON Schema section above for the complete structure. The JSON adapts to project state:
- **Healthy Project**: `healthScore` near 100, empty `gaps` array, no critical recommendations
- **Stale Stack**: Gap entry with `category: "freshness"`, recommendation to run `/shipkit-project-context`
- **Workflow Gap**: Gap entry with `category: "workflow-gap"`, missing specs/plans highlighted
- **Fresh Project**: All `coreContext` entries have `freshness: "fresh"`, high health score

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
- Review skill usage insights to identify workflow gaps (e.g., never using quality checks)

**When to upgrade to full /shipkit-project-status**:
- Need team collaboration metrics
- Need test coverage analysis
- Need dependency vulnerability scanning
- Need performance benchmarks

---

## Special Notes

**This skill is unique**:
- Writes single status file (`.shipkit/status.json`) using OVERWRITE strategy
- Fast execution (<5 seconds)
- Terminal output shows human-readable summary (not raw JSON)
- Can run anytime - safe to invoke frequently

**Design decisions**:
- Uses bash for file scanning (glob, stat, wc, grep)
- Writes status snapshot to persistent file (`.shipkit/status.json`)
- Follows Shipkit JSON artifact convention (`$schema`, `type`, `version`, etc.)
- OVERWRITE strategy (point-in-time data, no historical value)
- Focused on actionability (suggests next skill)
- Optimized for POC/MVP context (doesn't check production concerns)

**Freshness logic**:
- Compares file timestamps
- Detects package.json changes vs stack.json
- Flags large undocumented files
- Identifies workflow bottlenecks

---

**Remember**: This is an orientation tool. Run it when you need to know "where am I?" and "what should I do next?". It's designed to be fast, informative, and actionable.