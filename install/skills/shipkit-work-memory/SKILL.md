---
name: shipkit-work-memory
description: "Use when logging session progress or summarizing work done. Triggers: 'log progress', 'session summary', 'what did we do', 'save progress'."
---

# shipkit-work-memory - Session Progress Tracking

**Purpose**: Create a historical record of project evolution by capturing session summaries with completed work, files changed, current status, blockers, and next steps.

---

## When to Invoke

**User triggers**:
- "End session"
- "Log what we did today"
- "Record progress"
- "Save session summary"
- "What did we accomplish?"

**Suggested after**:
- `implement (no skill needed)` completes a feature
- `verify manually` verifies feature
- End of work session
- Before switching context to different feature

---

## Prerequisites

**Optional but creates richer context**:
- `.shipkit/progress.md` - Append to existing history
- `.shipkit/implementations.md` - Reference completed features
- `.shipkit/plans/*.md` - Reference what was planned

**If missing**: Start fresh progress.md file.

---

## Process

### Step 1: Ask Before Inferring

**Before generating anything**, ask user 2-3 questions to get accurate summary:

1. **What did we accomplish this session?**
   - "What features/components did we complete?"
   - "What problems did we solve?"
   - Let user describe in their own words

2. **Any blockers or issues?**
   - "Anything blocking progress?"
   - "Any decisions deferred?"
   - "Technical debt created?"

3. **What's next?**
   - "What should we tackle next session?"
   - "Any prep work needed?"
   - "Priorities for next time?"

**Why ask first**: User knows context Claude might have missed. Avoid hallucinating accomplishments.

**If user says "just infer from conversation"**:
- Review conversation history
- Identify concrete actions taken
- Note files created/modified
- Extract key decisions made
- Identify blockers mentioned
- Look for explicit next steps discussed

---

### Step 2: Gather Context

**Read to understand current state**:

```bash
# Check if progress history exists
.shipkit/progress.md

# Check recent implementations (optional)
.shipkit/implementations.md

# Check active tasks (optional)
.shipkit/user-tasks/active.md
```

**Token budget**: Keep context reading under 1000 tokens.

---

### Step 3: Infer from Conversation (if needed)

**If user asked Claude to infer, analyze the session**:

**Look for evidence of**:
- Files created/modified (Read/Write/Edit tool calls)
- Features implemented (mention of components, routes, APIs)
- Tests written/run (bash commands, test output)
- Decisions made (architectural choices, tech selections)
- Bugs fixed (debugging sessions, error resolutions)
- Documentation created (markdown files)
- Skills invoked (shipkit-plan, implement, etc.)

**Extract**:
- Concrete deliverables (what exists now that didn't before)
- Key decisions (what was decided and why)
- Blockers encountered (what stopped progress)
- Next steps discussed (what was suggested/planned)

**Don't hallucinate**: Only log what actually happened. If uncertain, ask user to clarify.

---

### Step 4: Append to Progress Log

**Use Write tool to append to**: `.shipkit/progress.md`

**If file doesn't exist**, create with header:
```markdown
# Project Progress Log

Historical record of development sessions, decisions, and evolution.

---
```

**Then append session entry**:

```markdown
## [YYYY-MM-DD] | Session Summary

**Completed**:
- [Feature/component 1 with brief description]
- [Feature/component 2 with brief description]
- [Bug fix/improvement with description]

**Files Created/Modified**:
- `path/to/file1.tsx` - [What was done]
- `path/to/file2.ts` - [What was done]
- `path/to/file3.md` - [What was done]

**Key Decisions**:
- [Decision 1]: [Rationale]
- [Decision 2]: [Rationale]

**Status**: [✓ Shipped | 🚧 In Progress | ⏸️ Paused | ❌ Blocked]

**Blockers** (if any):
- [Blocker 1]: [Description and impact]
- [Blocker 2]: [Description and impact]

**Next Steps**:
- [Next task 1]
- [Next task 2]
- [Next task 3]

**Session Duration**: [Approximate time if known]

**Notes**:
- [Any additional context or observations]

---
```

**Status icons guide**:
- ✓ Shipped - Feature complete and merged/deployed
- 🚧 In Progress - Actively working, not complete
- ⏸️ Paused - Work stopped, will resume later
- ❌ Blocked - Cannot proceed without resolution

---

### Step 5: Suggest Next Skill

**Output to user**:
```
✅ Session logged to progress.md

📅 Date: [YYYY-MM-DD]
📝 Summary:
  • [X] features/components completed
  • [Y] files created/modified
  • [Z] decisions logged

🎯 Status: [status emoji + description]
```

---

### Step 6: Auto-Archive Old Sessions (48-Hour Window)

**After appending session, automatically archive entries older than 48 hours:**

**Process:**
1. Calculate cutoff date: `current_date - 48 hours`
2. Scan progress.md for entries older than cutoff
3. If old entries found:
   - Group by month (YYYY-MM)
   - Append to `.shipkit/archives/progress-archive-YYYY-MM.md`
   - Remove from progress.md
   - Notify user

**Archive file structure:**
```
.shipkit/
  progress.md              # Last 48 hours only (3-5 sessions)
  archives/
    progress-archive-2025-12.md   # December sessions
    progress-archive-2025-11.md   # November sessions
    progress-archive-2025-10.md   # October sessions
```

**Archive file format:**
```markdown
# Progress Archive: December 2025

Archived sessions from December 2025. For recent sessions, see progress.md.

---

## [2025-12-28] | Feature Implementation
[... session entry ...]

## [2025-12-27] | Bug Fix
[... session entry ...]
```

**Notification to user:**
```
📦 Archived 3 sessions (>48hrs old) to archives/progress-archive-2025-12.md

Recent working memory: last 48 hours (4 sessions)
Searchable history: archives/ folder
```

**Why 48-hour window:**
- Keeps progress.md under 500 lines (~200-400 tokens to load)
- True "working memory" - recent context for active work
- Archives preserve full history by month
- Easy to search archives if needed: "When did we add X?"

**Creating archives/ folder:**
- If doesn't exist: create `.shipkit/archives/`
- If archive file doesn't exist: create with header
- If archive file exists: append old entries

---

## Completion Checklist

Copy and track:
- [ ] Summarized session accomplishments
- [ ] Noted decisions made
- [ ] Appended to `.shipkit/progress.md`

---

## What Makes This "Lite"

**Included**:
- ✅ Session-by-session progress log
- ✅ Completed work tracking
- ✅ File change log
- ✅ Key decisions capture
- ✅ Blockers documentation
- ✅ Next steps planning

**Not included** (vs full work-memory):
- ❌ Automatic code metrics (LoC, complexity)
- ❌ Test coverage tracking
- ❌ Commit history integration
- ❌ Time tracking
- ❌ Velocity calculations
- ❌ Sprint/milestone planning

**Philosophy**: Simple append-only log. Enough to resume work next session, not project management overhead.

---

## When This Skill Integrates with Others

### Before This Skill

- `implement (no skill needed)` - Completes features
  - **When**: Feature implementation finished
  - **Why**: Log what was built before context is lost
  - **Trigger**: User says "feature is done" or "implement (no skill needed)" completes

- `verify manually` - Verifies work
  - **When**: Quality verification complete
  - **Why**: Log verification results and confidence level
  - **Trigger**: Quality check passes/fails with findings

- Any development work session
  - **When**: Ending active work session
  - **Why**: Capture progress while context is fresh
  - **Trigger**: User says "end session", "log progress", or "save work"

### After This Skill

- `/shipkit-work-memory` - Prepares detailed handoff
  - **When**: Session ending, need rich context for next time
  - **Why**: Combines progress log with active context for seamless resume
  - **Trigger**: User wants comprehensive handoff document beyond simple log

- End session with clear record
  - **When**: Work session complete, progress logged
  - **Why**: Future sessions can reference what was accomplished
  - **Trigger**: Progress logged, user ready to close session

### Complementary Usage

Works alongside other context files:
- `implementations.md` - Detailed feature documentation (what exists)
- `architecture.md` - Decision rationale (why choices made)
- `progress.md` - Timeline view (when things happened)

Each provides different view of project evolution.

---

## Context Files This Skill Reads

**Optional** (for richer context):
- `.shipkit/progress.md` - Previous session history
- `.shipkit/implementations.md` - Recently completed features
- `.shipkit/user-tasks/active.md` - Tasks in progress

**None required** - Can start fresh if files don't exist.

---

## Context Files This Skill Writes

**Appends to**:
- `.shipkit/progress.md` - Session summaries (append-only, never delete)

**Never modifies**:
- Other context files (read-only)

---

## Lazy Loading Behavior

**This skill loads context ON DEMAND**:

1. User invokes `/shipkit-work-memory`
2. Claude asks what was accomplished (or gets approval to infer)
3. Claude reads progress.md if it exists (~200-500 tokens)
4. Claude optionally reads implementations.md to reference recent work (~300 tokens)
5. Claude appends session summary
6. Total context: ~500-1000 tokens (focused)

**Not loaded unless needed**:
- Specs/plans (not relevant for session summary)
- Full implementations.md (only if user wants to reference)
- Other skills' outputs

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

Session is logged when:
- [ ] Date header added
- [ ] Completed work listed
- [ ] Files changed documented
- [ ] Status indicated with emoji
- [ ] Blockers noted (if any)
- [ ] Next steps specified
- [ ] Appended to progress.md (not overwritten)
<!-- /SECTION:success-criteria -->
---

## Common Scenarios

**See `references/common-scenarios.md` for detailed examples:**
- Scenario 1: Feature Just Completed
- Scenario 2: Work In Progress
- Scenario 3: Infer from Conversation
- Scenario 4: Debugging Session
- Scenario 5: Multiple Features in One Session

---

## Tips for Effective Session Logging

**See `references/tips.md` for detailed guidance on:**
- Being specific in descriptions
- Logging decisions (WHY not just WHAT)
- Tracking blockers honestly
- Making next steps actionable
- Including file paths
- Using progress log as project history

**See `referencessee docs.md` for when to upgrade to full /work-memory.**

---

## Reference Documentation

**This skill provides detailed guidance in reference files:**

**Process Examples:**
- `references/common-scenarios.md` - 5 session logging scenarios (feature complete, WIP, inferred, debugging, multi-feature)

**Best Practices:**
- `references/tips.md` - Effective session logging tips, using progress as history
- `referencessee docs.md` - When to upgrade upgrade work-memory

**How to use references:**
- Main SKILL.md provides the logging process workflow
- Reference files provide examples and best practices
- Keep session entries brief but informative
- Let auto-archiving handle history management
