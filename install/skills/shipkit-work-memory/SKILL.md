---
name: shipkit-work-memory
description: "Log session progress and save resume state. Infers from conversation and git. Triggers: 'log progress', 'session summary', 'checkpoint', 'save progress', 'end session'."
argument-hint: "[checkpoint name]"
---

# shipkit-work-memory - Session Progress & Resume State

**Purpose**: Capture session progress and resume state by inferring from conversation and git. User confirms, Claude does the work.

**Output**: `.shipkit/progress.json` — A timeline graph artifact ideal for session history visualization.

---

## When to Invoke

**User triggers**:
- "End session"
- "Log progress"
- "Save checkpoint"
- "What did we do?"
- "Save session"

**Suggested after**:
- Long implementation sessions
- Before context gets full
- Before switching tasks
- End of work session

---

## Prerequisites

**None required** - Can start fresh.

**Uses if available**:
- `.shipkit/progress.json` - Merge with existing sessions
- Git - For modified files detection

---

## JSON Schema (Quick Reference)

**This skill outputs `.shipkit/progress.json` using the Shipkit JSON Artifact Convention.**

```json
{
  "$schema": "shipkit-artifact",
  "type": "work-memory",
  "version": "1.0",
  "lastUpdated": "2025-01-15T10:00:00Z",
  "source": "shipkit-work-memory",
  "summary": { "totalSessions", "currentPhase", "lastSessionDate", "activeWorkstream", "blockers", "momentum" },
  "sessions": [{ "id", "date", "duration", "workstream", "phase", "accomplished", "filesModified", "decisions", "gotchas", "blockers", "nextSteps", "status" }],
  "workstreams": [{ "id", "name", "status", "startDate", "sessions", "completionEstimate" }],
  "resumePoint": { "lastSession", "immediateNextStep", "context", "openFiles", "relatedArtifacts" },
  "timeline": [{ "date", "event", "type" }]
}
```

**Full schema and field reference**: See `references/output-schema.md`

**Realistic example**: See `references/example.json`

---

## Process

### Step 1: Analyze Session (Inference)

**Scan conversation for tool calls:**
```
Look for Edit/Write/Read calls → files touched
Most recent Edit/Write → likely resume point
```

**Extract from discussion:**
- What was being built/fixed → current task
- Problems/errors encountered → gotchas
- "Next we should..." or "TODO" mentions → next steps
- Choices made with rationale → decisions

**Run git status:**
```bash
git status --porcelain
```
→ Modified/added files = files changed this session

---

### Step 2: Generate Summary

**Build summary from inference:**

```
Task: [Inferred from conversation topic]
Status: [in-progress | complete | blocked]
Last file: [Most recent Edit/Write target]
Modified: [Count from git status]
Next: [Extracted from "next" mentions or inferred]
Gotchas: [Errors hit, surprises discovered]
Decisions: [Choices made with rationale]
```

---

### Step 3: Present for Confirmation

**Show user what was captured:**

```
Session Summary (inferred)

Task: Auth implementation
Status: in-progress
Last file: src/api/auth/login.ts
Modified: 4 files
Next: Add JWT generation
Gotcha: Prisma must import from @/lib/prisma

Completed:
- User schema added
- Password hashing utils
- Login endpoint started

Save to progress.json? [y/n]
```

**If user says no or wants changes:**
- Ask what to adjust
- Update and re-confirm

**If user says yes:**
- Proceed to Step 4

---

### Step 4: Update progress.json

**Write strategy:**

1. Read existing `.shipkit/progress.json` (if exists)
2. Parse existing JSON (or initialize empty structure with artifact envelope)
3. Generate a new session ID by incrementing the highest existing session ID
4. Append new session object to `sessions` array
5. Update or create `workstreams` entry for the current workstream
6. OVERWRITE `resumePoint` with current session's resume context
7. Append new timeline events (milestones, decisions from this session)
8. Recalculate `summary` fields (`totalSessions`, `lastSessionDate`, `blockers`, `momentum`, etc.)
9. Set `lastUpdated` to current ISO datetime
10. Write the complete JSON to `.shipkit/progress.json`

**Initialization (first session):**

When no `progress.json` exists, create the full structure:

```json
{
  "$schema": "shipkit-artifact",
  "type": "work-memory",
  "version": "1.0",
  "lastUpdated": "<current ISO datetime>",
  "source": "shipkit-work-memory",
  "summary": {
    "totalSessions": 1,
    "currentPhase": "<inferred>",
    "lastSessionDate": "<today>",
    "activeWorkstream": "<inferred>",
    "blockers": 0,
    "momentum": "high"
  },
  "sessions": [ "<new session object>" ],
  "workstreams": [ "<new workstream object>" ],
  "resumePoint": { "<current resume state>" },
  "timeline": [ "<initial events>" ]
}
```

**Subsequent sessions:**

- Read and parse existing JSON
- Append to `sessions`, update `workstreams`, overwrite `resumePoint`
- Append to `timeline`
- Recalculate `summary`

---

### Step 5: Confirm Save

```
Progress saved to .shipkit/progress.json

Resume Point: src/api/auth/login.ts
Next: Add JWT generation

To resume next session, I'll read progress.json and pick up where we left off.
```

---

### Step 6: Auto-Archive (48-Hour Window)

**After saving, archive old session entries:**

1. Find session entries older than 48 hours
2. Move them to `.shipkit/archives/progress-archive-YYYY-MM.json` (same artifact envelope format)
3. Remove archived sessions from `progress.json` to keep it focused on recent work
4. Update `summary.totalSessions` to reflect only active sessions
5. Keep `timeline` entries intact (they are lightweight and useful for visualization)

**Archive file structure:**
```json
{
  "$schema": "shipkit-artifact",
  "type": "work-memory-archive",
  "version": "1.0",
  "lastUpdated": "<archive date>",
  "source": "shipkit-work-memory",
  "summary": {
    "totalSessions": 3,
    "dateRange": "2025-01-01 to 2025-01-13"
  },
  "sessions": [ "<archived session objects>" ]
}
```

**Notify:**
```
Archived 3 old sessions to archives/progress-archive-2025-01.json
```

---

## Inference Patterns

### Detecting Current Task

**Look for patterns in conversation:**
- "Let's work on [X]" → task is X
- "Implementing [X]" → task is X
- Most discussed topic → likely the task
- Spec/plan being followed → task from spec name

### Detecting Resume Point

**Priority order:**
1. Last Edit tool call → that file
2. Last Write tool call → that file
3. Most discussed file → likely resume point
4. Git: most recently modified → fallback

### Detecting Next Steps

**Look for:**
- "Next we need to..."
- "TODO: ..."
- "After this, we should..."
- "Still need to..."
- Incomplete items from plan

### Detecting Gotchas

**Look for:**
- Errors encountered and resolved
- "Turns out..." or "Actually..."
- Surprising behavior discovered
- Workarounds implemented
- Import path corrections

### Detecting Decisions

**Look for:**
- "Let's use X instead of Y"
- "Going with X because..."
- Trade-off discussions
- Architecture choices

### Detecting Workstream

**Look for:**
- Recurring topic across multiple sessions
- Feature name or epic name mentioned
- Related files being modified together
- If unclear, use the primary task name as the workstream name

---

## Session Start Integration

**When session starts and progress.json exists:**

Claude (via master or session hook) should:
1. Read and parse `.shipkit/progress.json`
2. Extract `resumePoint` object
3. Surface it to user:

```
Resume Point from last session:

Task: Auth implementation (workstream: Authentication flow)
Last file: src/middleware/auth.ts
Next: Add rate limiting to auth endpoints
Context: JWT auth is working, need to harden before deployment

Continue from here?
```

---

## What Makes This Effective

**Claude does the work:**
- Infers from conversation (no user questions)
- Parses git status (no manual file listing)
- Extracts gotchas from errors hit
- Finds next steps from discussion

**User just confirms:**
- Review summary
- Say yes or adjust
- Done

**Next session is easy:**
- `resumePoint` in progress.json has everything needed
- Claude reads it, surfaces context
- Seamless continuation

**Dashboard-ready data:**
- `summary` object powers dashboard cards at a glance
- `timeline` array enables visual session history graphs
- `workstreams` track feature-level progress across sessions

---

## Context Files This Skill Reads

| File | Purpose |
|------|---------|
| `.shipkit/progress.json` | Existing progress (if any) |
| Conversation history | Tool calls, discussion |
| Git status | Modified files |

---

## Context Files This Skill Writes

| File | Strategy | Description |
|------|----------|-------------|
| `.shipkit/progress.json` | Overwrite `resumePoint`, append to `sessions`/`timeline`, recalculate `summary` | Primary work memory artifact |
| `.shipkit/archives/progress-archive-YYYY-MM.json` | Create/append | Archived sessions older than 48 hours |

---

## When This Skill Integrates with Others

### Before This Skill

Any development work:
- Implementation sessions
- Debugging sessions
- Feature building

### After This Skill

- End session with clear state
- Next session reads `resumePoint` from progress.json
- Seamless continuation

### Complementary

- `shipkit-architecture-memory` - Decisions in detail
- `shipkit-project-status` - Overall health check (reads `summary` from progress.json)

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

---

<!-- SECTION:success-criteria -->
## Success Criteria

- [ ] Task inferred from conversation
- [ ] Last file detected from tool calls
- [ ] Modified files from git status
- [ ] Next steps extracted from discussion
- [ ] Gotchas captured from errors/surprises
- [ ] Decisions captured with rationale
- [ ] progress.json written with valid artifact envelope (`$schema`, `type`, `version`, `lastUpdated`, `source`, `summary`)
- [ ] Session entry appended to `sessions` array
- [ ] `resumePoint` overwritten with current state
- [ ] `timeline` updated with session events
- [ ] `workstreams` updated or created
- [ ] `summary` recalculated
- [ ] User only needed to confirm
<!-- /SECTION:success-criteria -->