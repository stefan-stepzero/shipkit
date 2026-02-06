# shipkit-checkpoint Spec

A skill for saving session state to enable multi-session task continuity.

---

## The Problem

Long tasks span multiple sessions, but context is lost:

```
Session 1:
- Started implementing auth
- Finished user schema
- Finished password hashing
- Started login endpoint (50% done)
- [Context filled up / session ended]

Session 2:
Claude: "How can I help you today?"
User: "Continue the auth work"
Claude: "What auth work? Let me explore the codebase..."
→ Wastes tokens re-discovering what was done
→ May redo work or miss context
```

---

## The Solution

Save explicit checkpoint before session ends. Resume from checkpoint in new session.

### Output: `.shipkit/checkpoint.md`

```markdown
# Session Checkpoint

**Created:** 2025-01-27 14:30
**Task:** Implementing user authentication
**Status:** In Progress (60% complete)

---

## Completed

- [x] Database schema for users table
  - File: `prisma/schema.prisma` (lines 15-28)
  - Added User model with email, passwordHash, createdAt

- [x] Password hashing utility
  - File: `src/utils/auth.ts`
  - Using bcrypt with 12 rounds
  - Exports: `hashPassword()`, `verifyPassword()`

- [x] Auth types defined
  - File: `src/types/auth.ts`
  - LoginInput, LoginOutput, RegisterInput

---

## In Progress

- [ ] Login endpoint
  - File: `src/api/auth/login.ts`
  - Route handler created, validation done
  - **Stopped at:** JWT generation (line 34)
  - **Next step:** Import jsonwebtoken, create token with user.id

---

## Pending

- [ ] JWT token generation utility
- [ ] Register endpoint
- [ ] Protected route middleware
- [ ] Token refresh endpoint
- [ ] Logout (invalidate refresh token)

---

## Key Decisions Made

| Decision | Rationale |
|----------|-----------|
| bcrypt over argon2 | Simpler, widely supported |
| JWT expiry: 15min | Short-lived, refresh token for persistence |
| Refresh in httpOnly cookie | XSS protection |
| No email verification | MVP, add later |

---

## Context for Next Session

### Files to Open First
1. `src/api/auth/login.ts` — Continue from line 34
2. `src/utils/auth.ts` — Reference for password verify

### Gotchas Discovered
- Prisma client must be imported from `@/lib/prisma`, not generated directly
- Our error format is `{ data: null, error: { code, message } }`

### Test State
- No tests written yet (will add after endpoints complete)

---

## To Resume

```
/resume
```
or
```
"Continue the auth implementation from my checkpoint"
```

Claude should:
1. Read this checkpoint
2. Open `src/api/auth/login.ts`
3. Continue from JWT generation
```

---

## User Flows

### Creating a Checkpoint

**Explicit save:**
```
User: /checkpoint

Claude: "I'll save the current session state.

**Current task:** Implementing user authentication

**Progress summary:**
- ✅ User schema (prisma/schema.prisma)
- ✅ Password utils (src/utils/auth.ts)
- 🔄 Login endpoint (src/api/auth/login.ts) — 50% done
- ⬜ JWT utils, register, middleware, refresh, logout

**Key decisions:**
- bcrypt for passwords
- 15min JWT expiry
- Refresh tokens in httpOnly cookies

Save this checkpoint to .shipkit/checkpoint.md?"

User: "Yes"

Claude: [Saves checkpoint]
"Checkpoint saved. To resume in a new session:
- Say 'continue from checkpoint' or run /resume
- I'll pick up exactly where we left off"
```

**Context-aware prompt:**
```
[Claude detects session has been long / context filling up]

Claude: "We've made good progress on auth. Before we continue,
should I save a checkpoint? This will help us resume cleanly
if we need to start a new session."
```

### Resuming from Checkpoint

```
User: /resume
— or —
User: "Continue from where we left off"

Claude: [Reads checkpoint.md]

"Resuming from checkpoint (2025-01-27 14:30):

**Task:** User authentication
**Status:** 60% complete

**Last working on:** Login endpoint (src/api/auth/login.ts)
**Stopped at:** JWT generation (line 34)

**Next step:** Import jsonwebtoken and create token

Let me open that file and continue..."

[Opens file, continues from exact point]
```

### Checkpoint Not Found

```
User: /resume

Claude: "No checkpoint found at .shipkit/checkpoint.md.

Would you like me to:
1. Check project-status.md for recent work
2. Scan recent git commits to understand state
3. Start fresh — tell me what you're working on"
```

---

## Skill Behavior

### On `/checkpoint`

1. Summarize current session:
   - What task were we working on?
   - What's completed?
   - What's in progress (with specific locations)?
   - What's pending?

2. Capture decisions made this session

3. Note context for resume:
   - Files to open
   - Gotchas discovered
   - Current state

4. Save to `.shipkit/checkpoint.md`

### On `/resume`

1. Read `.shipkit/checkpoint.md`
2. Summarize state for user
3. Open relevant files
4. Continue from exact stopping point

### Checkpoint Freshness

```markdown
**Checkpoint age warnings:**
- < 24 hours: "Resuming from recent checkpoint"
- 1-7 days: "Checkpoint is X days old. Things may have changed."
- > 7 days: "Checkpoint is stale. Verify state before continuing."
```

---

## SKILL.md Structure

```markdown
---
name: shipkit-checkpoint
description: Save session state for multi-session task continuity
---

# Session Checkpoint

Save your progress to resume seamlessly in a new session.

## Commands

- `/checkpoint` — Save current state
- `/resume` — Load checkpoint and continue

## When to Checkpoint

- Before ending a long session
- When context is getting full
- Before switching to a different task
- At natural breakpoints (feature complete, etc.)

## What Gets Saved

1. **Task:** What you're working on
2. **Completed:** What's done (with file locations)
3. **In Progress:** Current work (exact line/position)
4. **Pending:** What's left
5. **Decisions:** Choices made this session
6. **Context:** Files to open, gotchas, test state

## On Checkpoint

I'll summarize the session and ask for confirmation before saving.

## On Resume

I'll:
1. Read the checkpoint
2. Summarize where we left off
3. Open the relevant files
4. Continue from the exact stopping point

## Output Location
`.shipkit/checkpoint.md`

## Relationship to Other Files

| File | Difference |
|------|------------|
| `progress.md` | High-level project progress (shipkit-work-memory) |
| `checkpoint.md` | Specific session state for resume |
| `project-status.md` | Overall project health |

Checkpoint is more granular — exact file positions, specific next steps.
```

---

## Relationship to Existing Skills

| Skill | Relationship |
|-------|-------------|
| **shipkit-work-memory** | Appends to progress.md (high-level). Checkpoint is detailed session state. |
| **shipkit-project-status** | Shows overall health. Checkpoint is task-specific resume point. |
| **shipkit-plan** | Plans are what to do. Checkpoint is where you stopped. |

### Overlap with shipkit-work-memory

```
shipkit-work-memory (progress.md):
"2025-01-27: Worked on auth. Completed user schema and password utils.
Login endpoint in progress."

shipkit-checkpoint (checkpoint.md):
"Login endpoint: src/api/auth/login.ts, stopped at line 34,
next step is JWT generation, use jsonwebtoken library..."
```

**work-memory = journal (what happened)**
**checkpoint = save game (exact state to resume)**

---

## When to Suggest Checkpointing

Claude should proactively suggest checkpointing when:

1. **Long session:** > 30 minutes of active work
2. **Significant progress:** Multiple files created/modified
3. **Natural breakpoint:** Feature complete, test passing
4. **Before context risk:** If Claude could detect context filling
5. **Task switch:** "Before we switch to X, should I checkpoint Y?"

---

## Checkpoint Lifecycle

```
Session 1:
  Work → Work → Work → /checkpoint → [saved]

Session 2:
  /resume → Continue → Work → /checkpoint → [updated]

Session 3:
  /resume → Finish task → Delete checkpoint (task complete)
```

### Clearing Checkpoints

```
User: "Auth is done, clear the checkpoint"

Claude: "Checkpoint cleared. The auth implementation is complete.

Should I update progress.md with a summary of what was built?"
```

---

## Edge Cases

### Multiple Tasks in Flight

```
User: "I was working on auth but need to switch to payments"

Claude: "I'll checkpoint the auth work first, then we can start payments.

[Saves auth checkpoint]

Note: Only one checkpoint.md exists. If you need to checkpoint
payments too, the auth checkpoint will be overwritten.

Alternative: I can save to checkpoint-auth.md and checkpoint-payments.md"
```

**Decision:** Support named checkpoints?
- `checkpoint.md` — default/current
- `checkpoint-{name}.md` — named for multi-task

### Checkpoint + Git State Mismatch

```
User: /resume

Claude: [Reads checkpoint, checks git]

"⚠️ The checkpoint references files that have changed since it was created:
- src/api/auth/login.ts: Modified after checkpoint
- src/utils/auth.ts: Unchanged

Someone (or another session) modified login.ts.
Should I:
1. Show the diff and update my understanding
2. Proceed with checkpoint (may be outdated)
3. Discard checkpoint and assess current state"
```

---

## Open Questions

1. **Named checkpoints or single checkpoint?**
   - Single is simpler
   - Named allows parallel tasks

2. **Auto-checkpoint?**
   - Periodically save?
   - On certain triggers?
   - Only manual?

3. **Checkpoint expiry?**
   - Auto-delete after 7 days?
   - Keep until manually cleared?

4. **Git integration?**
   - Include commit hash in checkpoint?
   - Warn if files changed since checkpoint?

---

## Implementation Checklist

- [ ] Create SKILL.md
- [ ] Define checkpoint.md template
- [ ] Implement /checkpoint command
- [ ] Implement /resume command
- [ ] Add staleness detection
- [ ] Add proactive checkpoint suggestions
- [ ] Integrate with 7-file system
- [ ] Test resume accuracy
