---
name: lite-work-memory
description: Captures session summaries in append-only progress log. At session end, prompts for what was accomplished or infers from conversation. Logs completed work, files changed, status, blockers, next steps to .shipkit-lite/progress.md with date headers.
---

# work-memory-lite - Session Progress Tracking

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
- `/lite-implement` completes a feature
- `/lite-quality-confidence` verifies feature
- End of work session
- Before switching context to different feature

---

## Prerequisites

**Optional but creates richer context**:
- `.shipkit-lite/progress.md` - Append to existing history
- `.shipkit-lite/implementations.md` - Reference completed features
- `.shipkit-lite/plans/*.md` - Reference what was planned

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
.shipkit-lite/progress.md

# Check recent implementations (optional)
.shipkit-lite/implementations.md

# Check active tasks (optional)
.shipkit-lite/user-tasks/active.md
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
- Skills invoked (plan-lite, implement-lite, etc.)

**Extract**:
- Concrete deliverables (what exists now that didn't before)
- Key decisions (what was decided and why)
- Blockers encountered (what stopped progress)
- Next steps discussed (what was suggested/planned)

**Don't hallucinate**: Only log what actually happened. If uncertain, ask user to clarify.

---

### Step 4: Append to Progress Log

**Use Write tool to append to**: `.shipkit-lite/progress.md`

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

👉 Next session:
  [Next steps from log]

Ready to continue or end session?
```

**Suggest contextually**:

**If feature just completed**:
```
👉 Options:
  1. /lite-quality-confidence - Verify before shipping
  2. /lite-session-continuity - Prepare context for next session
  3. End session
```

**If feature in progress**:
```
👉 Next session:
  Continue implementation: [next task from plan]
  Consider: /lite-session-continuity to preserve context
```

**If blocked**:
```
👉 Before next session:
  Resolve: [blocker description]
  Then: [next task]
```

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

## Integration with Other Skills

**Before work-memory-lite**:
- `/lite-implement` - Completes features
- `/lite-quality-confidence` - Verifies work
- Any development work session

**After work-memory-lite**:
- `/lite-session-continuity` - Prepares detailed handoff for next session (optional)
- End session with clear record

**Complementary**:
- Works alongside implementations.md (detailed feature docs)
- Works alongside architecture.md (decision rationale)
- Provides timeline view that other files don't

---

## Context Files This Skill Reads

**Optional** (for richer context):
- `.shipkit-lite/progress.md` - Previous session history
- `.shipkit-lite/implementations.md` - Recently completed features
- `.shipkit-lite/user-tasks/active.md` - Tasks in progress

**None required** - Can start fresh if files don't exist.

---

## Context Files This Skill Writes

**Appends to**:
- `.shipkit-lite/progress.md` - Session summaries (append-only, never delete)

**Never modifies**:
- Other context files (read-only)

---

## Lazy Loading Behavior

**This skill loads context ON DEMAND**:

1. User invokes `/lite-work-memory`
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

## Success Criteria

Session is logged when:
- [ ] Date header added
- [ ] Completed work listed
- [ ] Files changed documented
- [ ] Status indicated with emoji
- [ ] Blockers noted (if any)
- [ ] Next steps specified
- [ ] Appended to progress.md (not overwritten)

---

## Common Scenarios

### Scenario 1: Feature Just Completed

```
User: "Log what we did today"

Claude:
1. Ask: "What did we accomplish?"
   User: "Built the recipe sharing feature"
2. Ask: "Any blockers?"
   User: "None, it's shipped"
3. Ask: "What's next?"
   User: "Add analytics tracking"
4. Read .shipkit-lite/progress.md
5. Append session:
   ## [2025-01-15] | Recipe Sharing Feature
   **Completed**: Recipe sharing feature
   **Files**: ShareButton.tsx, share/[token]/page.tsx, api/share/route.ts
   **Status**: ✓ Shipped
   **Next Steps**: Add analytics tracking
```

### Scenario 2: Work In Progress

```
User: "Save progress, I need to stop"

Claude:
1. Ask: "What did we get done?"
   User: "Started the sharing feature, got the UI done but API not finished"
2. Ask: "What's blocking?"
   User: "Need to figure out auth for the share token"
3. Ask: "Next session plan?"
   User: "Finish the API, add tests"
4. Append session:
   ## [2025-01-15] | Sharing Feature (Partial)
   **Completed**: Share button UI component
   **Files**: ShareButton.tsx
   **Status**: 🚧 In Progress
   **Blockers**: Need to design auth for share tokens
   **Next Steps**: Implement share API, add token auth, write tests
```

### Scenario 3: Infer from Conversation

```
User: "Just infer what we did"

Claude:
1. Review conversation history
2. Note:
   - Created 3 files (ShareButton.tsx, route.ts, types.ts)
   - Discussed token-based auth approach
   - Ran tests, all passing
   - Suggested analytics as next step
3. Read progress.md
4. Append session:
   ## [2025-01-15] | Recipe Sharing Implementation
   **Completed**:
   - Share button component with copy-to-clipboard
   - Share API endpoint with token generation
   - Type definitions for sharing
   **Files**:
   - `components/ShareButton.tsx` - Share UI
   - `app/api/share/route.ts` - Token generation
   - `types/sharing.ts` - Type definitions
   **Key Decisions**:
   - Token-based sharing (UUID v4, 24hr expiry)
   - Copy-to-clipboard using navigator.clipboard
   **Status**: ✓ Shipped
   **Next Steps**: Add analytics tracking for share events
```

### Scenario 4: Debugging Session

```
User: "Log this debugging session"

Claude:
1. Ask: "What bug did we fix?"
   User: "Share button wasn't working in Safari"
2. Ask: "What was the issue?"
   User: "Clipboard API needs https, was failing in dev"
3. Ask: "How did we fix it?"
   User: "Added fallback to document.execCommand"
4. Append session:
   ## [2025-01-15] | Safari Clipboard Bug Fix
   **Completed**: Fixed share button Safari compatibility
   **Files**: `components/ShareButton.tsx` - Added clipboard fallback
   **Key Decisions**:
   - Use navigator.clipboard with fallback to execCommand for Safari/http
   - Show error toast if both methods fail
   **Status**: ✓ Shipped
   **Next Steps**: Test on mobile Safari, consider adding share sheet API
```

### Scenario 5: Multiple Features in One Session

```
User: "We did a lot today, log it all"

Claude:
1. Ask: "What did we complete?"
   User: "Share feature, analytics, and dark mode toggle"
2. Ask: "Any issues?"
   User: "Analytics is shipping errors to console, need to debug"
3. Ask: "Next session?"
   User: "Fix analytics errors, add user settings page"
4. Append session:
   ## [2025-01-15] | Multi-Feature Session
   **Completed**:
   - Recipe sharing with token-based auth (✓ shipped)
   - Dark mode toggle in settings (✓ shipped)
   - Analytics tracking (🚧 partial - has bugs)
   **Files**:
   - `components/ShareButton.tsx` - Share UI
   - `app/api/share/route.ts` - Share API
   - `components/DarkModeToggle.tsx` - Theme toggle
   - `lib/analytics.ts` - Event tracking (buggy)
   **Status**: 🚧 In Progress
   **Blockers**: Analytics throwing console errors on page load
   **Next Steps**:
   - Debug analytics initialization
   - Add user settings page
   - Test dark mode persistence
   **Session Duration**: ~3 hours
```

---

## Tips for Effective Session Logging

**Be specific**:
- "Added share button" → "Share button with copy-to-clipboard and success toast"
- "Fixed bug" → "Fixed Safari clipboard API fallback"
- "Updated API" → "Added token-based auth to share endpoint"

**Log decisions**:
- Document WHY, not just WHAT
- Future you will thank present you
- "Used UUID v4 because crypto.randomUUID() has better browser support than custom tokens"

**Track blockers honestly**:
- Don't hide problems
- Note impact: "Blocking deployment" vs "Nice to have"
- Include what's needed to unblock

**Make next steps actionable**:
- ❌ "Continue working on feature"
- ✅ "Implement POST endpoint, add validation, write integration test"

**Include file paths**:
- Absolute or relative (but consistent)
- Makes it easy to find code later
- Shows scope of changes

---

## Progress Log as Project History

**Over time, progress.md becomes**:
- Timeline of feature evolution
- Record of architectural decisions
- Log of blockers and resolutions
- Reference for "when did we do X?"
- Handoff document for new team members
- Evidence of progress for stakeholders

**Example entry after 10 sessions**:
```markdown
## [2025-01-15] | Recipe Sharing Feature ✓
## [2025-01-14] | Dark Mode Implementation ✓
## [2025-01-13] | Analytics Integration (Partial) 🚧
## [2025-01-12] | User Authentication Refactor ✓
## [2025-01-11] | Database Schema Migration ✓
## [2025-01-10] | Initial Project Setup ✓
## [2025-01-09] | Planning & Architecture ✓
## [2025-01-08] | Product Discovery Complete ✓
## [2025-01-07] | User Research & Personas ✓
## [2025-01-06] | Strategic Thinking & Constitution ✓
```

**You can grep/search this file** to answer:
- "When did we add dark mode?" → Search for "dark mode"
- "What was that auth decision?" → Search for "auth"
- "What's still in progress?" → Search for "🚧"

---

## When to Upgrade to Full /work-memory

**Lite is sufficient for**:
- Solo developers or small teams
- POC/MVP projects
- Session-by-session tracking
- Simple "what did we do?" questions

**Upgrade to full /work-memory when**:
- Need automatic metrics (LoC, complexity, coverage)
- Want git commit integration
- Require time tracking/velocity
- Managing multiple developers
- Need sprint/milestone planning
- Stakeholder reporting with charts

---

**Remember**: The goal is a simple, consistent log of what happened. Write entries as if you're explaining to future you what you did and why. Keep it brief but informative.
