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

### Step 2: Scan Foundation Files (Phase 1)

**These are the critical foundation artifacts that all other skills depend on.**

Per the Skill Artifact Dependency Graph, Phase 1 files are:

```bash
# Foundation files (required for healthy project)
.shipkit/why.json              # Vision & purpose (from /shipkit-why-project)
.shipkit/stack.json            # Tech context (from /shipkit-project-context)
.shipkit/schema.json           # Data model (from /shipkit-project-context)
.shipkit/codebase-index.json   # Code understanding (from /shipkit-codebase-index)
```

**Also check these Phase 2+ files if they exist**:

```bash
# Phase 2: Discovery
.shipkit/goals.json            # Strategic goals (from /shipkit-goals)

# Phase 3: Design (cross-cutting)
.shipkit/architecture.json     # Tech decisions (from /shipkit-architecture-memory)

# Phase 5: Implementation
.shipkit/progress.json         # Session continuity (from /shipkit-work-memory)
```

**For each file, check**:
1. Does it exist?
2. When was it last modified? (use `stat` command)
3. Is content meaningful (>50 bytes)?

**Freshness indicators**:
- ✓ Modified within last 24 hours = Fresh
- ⚠ Modified 1-7 days ago = Aging
- ✗ Modified >7 days ago OR missing = Stale

**Foundation completeness**:
- 4/4 foundation files = Ready for development
- 3/4 foundation files = Minor gap
- 2/4 or fewer = Critical gaps (suggest foundation skills first)

---

### Step 3: Count Documented Items

**Parse each context file and count documented elements**:

**stack.json**:
- Count sections (Framework, Database, Key Libraries, etc.)
- Extract tech stack summary

**architecture.json**:
- Count decisions (count markdown H2/H3 headings)
- Extract recent decisions

**implementations.json**:
- Count documented components/routes (count items in components and routes arrays)
- Extract file paths mentioned

**progress.json**:
- Count session entries
- Get last session date

---

### Step 4: Detect Gaps

**Use bash commands to find undocumented components**:

```bash
# Find all TypeScript/JavaScript files >200 LOC
find src -type f \( -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.jsx" \) -exec wc -l {} + | awk '$1 > 200 {print $2}'

# Cross-reference with implementations.json
# Files NOT mentioned in implementations.json are gaps
```

**Verification before claiming gaps:**

| Gap Claim | Required Verification |
|-----------|----------------------|
| "Undocumented file" | Glob confirms file exists + file path not in implementations.json |
| "Stale documentation" | Compare file mtime vs doc mtime (use stat) |
| "Missing spec" | Glob for `specs/active/*.json` matching feature name returns empty |
| "Orphan plan" | Plan exists but Grep for implementation references returns 0 |

**Never claim "undocumented" without:**
1. `Glob`: Confirming the file exists
2. `Read`: Parsing implementations.json for the filename
3. If Grep returns 0: File is undocumented (valid gap)

**Gap types to detect**:
- Large files (>200 LOC) not documented in implementations.json
- package.json modified more recently than stack.json
- Database migration files newer than schema.json (if it exists)
- Active specs with no corresponding plans
- Plans with no implementation notes

---

### Step 5: Scan Specs, Plans, and Tasks

**Check workflow progress**:

```bash
# Count active specs
ls -1 .shipkit/specs/active/*.json 2>/dev/null | wc -l

# Count plans
ls -1 .shipkit/plans/active/*.json 2>/dev/null | wc -l

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

  Foundation (Phase 1): 3/4 files
    ✓ why.json (fresh)
    ✓ stack.json (aging - 3 days)
    ✓ schema.json (fresh)
    ✗ codebase-index.json (missing)

  Discovery: goals.json ✓ | architecture.json ✓
  Workflow: 2 specs | 0 plans | 5 tasks

  Gaps Found: 3
    - codebase-index.json missing (run /shipkit-codebase-index)
    - Active specs have no plans
    - 2 undocumented files >200 LOC

  Top Recommendations:
    1. /shipkit-codebase-index (foundation incomplete)
    2. /shipkit-plan for recipe-sharing spec
    3. Document large components manually

  Skill Usage: 47 total invocations, 2 never used
```

---

## JSON Schema

**Full schema**: See `references/output-schema.md`
**Example output**: See `references/example.json`

### Quick Reference

```json
{
  "$schema": "shipkit-artifact",
  "type": "project-status",
  "version": "1.1",
  "lastUpdated": "YYYY-MM-DD",
  "source": "shipkit-project-status",
  "summary": {
    "healthScore": 0-100,
    "totalSpecs": number,
    "totalPlans": number,
    "totalTasks": number,
    "gapsFound": number,
    "foundationFilesPresent": number,
    "foundationFilesTotal": 4
  },
  "foundation": [{ "file", "exists", "freshness", "lastModified?", "sizeBytes?", "notes?" }],
  "discovery": [{ "file", "exists", "freshness", "lastModified?", "notes?" }],
  "workflow": {
    "specs": { "activeCount", "files" },
    "plans": { "count", "files" },
    "tasks": { "activeCount", "completedCount" }
  },
  "gaps": [{ "id", "severity", "category", "description", "file?", "lineCount?", "suggestedAction" }],
  "skillUsage?": { "totalInvocations", "mostUsed", "neverUsed", "stale" },
  "recommendations": [{ "priority", "action", "reason" }]
}
```

### Key Fields

| Field | Description |
|-------|-------------|
| `summary.healthScore` | 0-100 score based on foundation completeness, freshness, and workflow state |
| `summary.foundationFilesPresent` | Count of Phase 1 files present (why, stack, schema, codebase-index) |
| `foundation[].freshness` | `"fresh"` (<24h) \| `"aging"` (1-7d) \| `"stale"` (>7d) \| `"missing"` |
| `gaps[].severity` | `"critical"` \| `"warning"` \| `"info"` |
| `gaps[].category` | `"foundation"` \| `"freshness"` \| `"undocumented"` \| `"workflow-gap"` |

---

### Step 7: Determine Next Action Suggestions

**Based on detected gaps, suggest ONE priority action**:

**Decision logic** (prioritizes foundation files first):

```
IF .shipkit/ doesn't exist:
  → "Run /shipkit-project-context to initialize"

# Foundation checks (Phase 1) - these block everything else
ELSE IF why.json missing:
  → "Run /shipkit-why-project to define project vision"

ELSE IF stack.json missing OR stale (>7 days) OR package.json newer than stack.json:
  → "Run /shipkit-project-context to scan/refresh tech stack"

ELSE IF codebase-index.json missing AND project has >10 source files:
  → "Run /shipkit-codebase-index to accelerate code understanding"

# Discovery checks (Phase 2)
ELSE IF goals.json missing AND why.json exists:
  → "Run /shipkit-goals to define strategic goals"

# Workflow checks (Phase 3+)
ELSE IF active specs exist AND no plans exist:
  → "Run /shipkit-plan for [spec-name]"

ELSE IF plans exist AND no implementation notes:
  → "Start implementing (no skill needed)"

ELSE IF large undocumented files exist:
  → "Document large components manually"

ELSE IF no architectural decisions logged AND implementation in progress:
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

This skill follows the **Shipkit JSON artifact convention**. See `references/output-schema.md` for full documentation.

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

**Common suggestions** (prioritized by phase):

**Foundation (Phase 1) - suggest first if missing**:

- `/shipkit-why-project` - When why.json is missing
  - **When**: No .shipkit/why.json exists
  - **Why**: Vision drives all other decisions
  - **Trigger**: Foundation check fails

- `/shipkit-project-context` - When stack.json is stale or missing
  - **When**: package.json modified after stack.json OR .shipkit/ doesn't exist
  - **Why**: Stale stack causes wrong tech assumptions
  - **Trigger**: Foundation freshness check fails

- `/shipkit-codebase-index` - When codebase-index.json is missing
  - **When**: Project has >10 source files but no index
  - **Why**: Index accelerates all exploration skills
  - **Trigger**: Foundation check fails

**Discovery (Phase 2)**:

- `/shipkit-goals` - When goals.json is missing but why.json exists
  - **When**: Foundation complete but no strategic goals defined
  - **Why**: Goals guide spec prioritization
  - **Trigger**: Discovery gap detected

**Workflow (Phase 3+)**:

- `/shipkit-plan` - When specs exist but no plans
  - **When**: Found .shipkit/specs/active/*.json but no .shipkit/plans/active/*.json
  - **Why**: Specs without plans block implementation
  - **Trigger**: Workflow gap detected

- `implement (no skill needed)` - When plans exist but no implementation notes
  - **When**: Found plans/active/*.json but no recent implementation entries
  - **Why**: Plans without execution are just ideas
  - **Trigger**: Workflow gap detected

---

## Context Files This Skill Reads

**Foundation files (Phase 1 - always checks)**:
- `.shipkit/why.json` - Project vision and purpose
- `.shipkit/stack.json` - Tech stack context
- `.shipkit/schema.json` - Data model
- `.shipkit/codebase-index.json` - Code understanding accelerator

**Discovery/Design files (Phase 2-3 - checks if exist)**:
- `.shipkit/goals.json` - Strategic goals
- `.shipkit/architecture.json` - Tech decisions
- `.shipkit/contracts.json` - Data contracts

**Workflow files (checks for progress)**:
- `.shipkit/specs/active/*.json` (glob to count)
- `.shipkit/plans/active/*.json` (glob to count)
- `.shipkit/user-tasks/active.md` (if exists)
- `.shipkit/progress.json` - Session continuity
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
- **New Project**: `foundationFilesPresent: 0`, suggests `/shipkit-why-project` first
- **Foundation Incomplete**: `foundationFilesPresent: 2/4`, gap with `category: "foundation"`, suggests missing foundation skill
- **Healthy Project**: `foundationFilesPresent: 4/4`, `healthScore` near 100, empty `gaps` array
- **Stale Stack**: Gap entry with `category: "freshness"`, recommendation to run `/shipkit-project-context`
- **Workflow Gap**: Gap entry with `category: "workflow-gap"`, specs exist but no plans
- **Ready for Development**: All `foundation` entries exist and fresh, discovery files present

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