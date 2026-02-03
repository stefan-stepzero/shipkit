---
name: shipkit-work-memory
description: "Log session progress and save resume state. Infers from conversation and git. Triggers: 'log progress', 'session summary', 'checkpoint', 'save progress', 'end session'."
argument-hint: "[checkpoint name]"
---

# shipkit-work-memory - Session Progress & Resume State

**Purpose**: Capture session progress and resume state by inferring from conversation and git. User confirms, Claude does the work.

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
- `.shipkit/progress.md` - Append to existing
- Git - For modified files detection

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
Status: [🚧 In Progress | ✓ Complete | ❌ Blocked]
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
📋 Session Summary (inferred)

**Task:** Auth implementation
**Status:** 🚧 In Progress
**Last file:** src/api/auth/login.ts
**Modified:** 4 files
**Next:** Add JWT generation
**Gotcha:** Prisma must import from @/lib/prisma

**Completed:**
- User schema added
- Password hashing utils
- Login endpoint started

Save to progress.md? [y/n]
```

**If user says no or wants changes:**
- Ask what to adjust
- Update and re-confirm

**If user says yes:**
- Proceed to Step 4

---

### Step 4: Update progress.md

**File structure:**

```markdown
# Project Progress Log

## Resume Point
<!-- OVERWRITTEN each session -->

**Task:** Auth implementation
**Status:** 🚧 In Progress
**Last file:** src/api/auth/login.ts
**Next:** Add JWT generation

**Gotchas:**
- Prisma must import from @/lib/prisma
- Error format is { data: null, error: { code, message } }

**Updated:** 2025-01-27 14:30

---

## Session Log
<!-- APPENDED -->

### 2025-01-27 | Auth Implementation

**Completed:**
- User schema in prisma/schema.prisma
- Password utils in src/utils/auth.ts
- Login endpoint started

**Files Modified:**
- prisma/schema.prisma
- src/utils/auth.ts
- src/api/auth/login.ts
- src/types/auth.ts

**Decisions:**
- bcrypt over argon2 (simpler, widely supported)
- 15min JWT expiry (short-lived, use refresh tokens)

**Status:** 🚧 In Progress

---
```

**Write strategy:**
1. Read existing progress.md (if exists)
2. OVERWRITE Resume Point section
3. APPEND new session entry to Session Log
4. Write file

---

### Step 5: Confirm Save

```
✅ Progress saved to .shipkit/progress.md

📍 Resume Point: src/api/auth/login.ts
🎯 Next: Add JWT generation

To resume next session, I'll read progress.md and pick up where we left off.
```

---

### Step 6: Auto-Archive (48-Hour Window)

**After saving, archive old entries:**

1. Find entries older than 48 hours
2. Move to `.shipkit/archives/progress-archive-YYYY-MM.md`
3. Keep progress.md focused on recent work

**Notify:**
```
📦 Archived 3 old sessions to archives/
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

---

## Session Start Integration

**When session starts and progress.md exists:**

Claude (via master or session hook) should:
1. Read Resume Point section
2. Surface it to user:

```
📍 Resume Point from last session:

Task: Auth implementation
Last file: src/api/auth/login.ts
Next: Add JWT generation

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
- Resume Point at top of progress.md
- Claude reads it, surfaces context
- Seamless continuation

---

## Context Files This Skill Reads

- `.shipkit/progress.md` - Existing progress (if any)
- Conversation history - Tool calls, discussion
- Git status - Modified files

---

## Context Files This Skill Writes

**Overwrites:**
- `.shipkit/progress.md` → Resume Point section

**Appends:**
- `.shipkit/progress.md` → Session Log section

**Creates if needed:**
- `.shipkit/archives/progress-archive-YYYY-MM.md`

---

## When This Skill Integrates with Others

### Before This Skill

Any development work:
- Implementation sessions
- Debugging sessions
- Feature building

### After This Skill

- End session with clear state
- Next session reads Resume Point
- Seamless continuation

### Complementary

- `shipkit-architecture-memory` - Decisions in detail
- `shipkit-project-status` - Overall health check

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
- [ ] Resume Point section overwritten
- [ ] Session entry appended
- [ ] User only needed to confirm
<!-- /SECTION:success-criteria -->

<!-- Shipkit v1.2.0 -->
