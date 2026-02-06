# Hooks Utilization Audit

**Status:** Implemented
**Last Updated:** 2026-02-06
**Implementation:** PreCompact hook created. Remaining items moved to REMAINING-ENHANCEMENTS.md

## Purpose

Review which Claude Code hook types Shipkit is using versus what's available, identify gaps and opportunities.

## Available Hook Types

| Hook | When it fires | Current Shipkit Usage |
|------|---------------|----------------------|
| `SessionStart` | New session, resume, clear, compact | YES - session-start.py |
| `SessionEnd` | Session ends | NO |
| `UserPromptSubmit` | Before user prompt processed | NO |
| `PreToolUse` | Before tool execution | NO |
| `PostToolUse` | After tool execution | YES - skill tracking |
| `SubagentStart` | When subagent starts | NO |
| `SubagentStop` | When subagent stops | NO |
| `PermissionRequest` | When tool requests permission | NO |
| `Setup` | Via --init, --init-only, --maintenance flags | NO |
| `PreCompact` | Before context compaction | NO |
| `Stop` | When Claude stops working | YES - after-skill-router, relentless-stop |

---

## Current Shipkit Hooks (Detailed Analysis)

### 1. session-start.py
**Location:** `.claude/hooks/session-start.py`
**Hook type:** SessionStart (matcher: `startup|resume|clear|compact`)
**Lines of code:** ~630

**What it does:**
1. **Loads shipkit-master skill** - Outputs the master routing table for skill selection
2. **Update check** - Checks GitHub for newer Shipkit version (rate-limited to once/day, 3s timeout)
3. **Quick status table** - Shows stack freshness, last session, active specs/plans, pending user tasks
4. **Freshness warnings** - Alerts if stack is stale, implementation docs outdated, specs/plans aging
5. **Smart recommendation** - Suggests next action based on project state:
   - No stack → `/shipkit-project-context`
   - Pending tasks → `/shipkit-user-instructions`
   - Active plan → "Continue implementing"
   - Active spec → `/shipkit-plan`
6. **Loads core context files** - why.md, stack.md (if fresh), architecture.md
7. **Codebase index summary** - Shows concepts and entry points from codebase-index.json
8. **Skill usage summary** - Highlights stale skills (not used in 14+ days)
9. **Context file manifest** - Table of available `.shipkit/` files with ages

**Value provided:** Essential for session continuity - gives Claude the context it would otherwise lack.

---

### 2. after-skill-router.py
**Location:** `.claude/hooks/after-skill-router.py`
**Hook type:** Stop
**Lines of code:** ~90

**What it does:**
1. **Reads breadcrumb file** - Checks `.shipkit/.last-skill` for parent skill name
2. **Routes to detection** - Maps parent skills to detection modes:
   - `shipkit-spec` → runs `shipkit-detect --mode=services`
   - `shipkit-plan` → runs `shipkit-detect --mode=contracts`
3. **Clears breadcrumb** - Removes `.last-skill` after reading
4. **Runs detection** - Executes the detect script to scan artifacts

**Value provided:** Creates causality chains between skills (spec → detect services → integration-docs).

---

### 3. shipkit-track-skill-usage.py
**Location:** `.claude/hooks/shipkit-track-skill-usage.py`
**Hook type:** PostToolUse (matcher: `Skill`)
**Lines of code:** ~100

**What it does:**
1. **Reads skill invocation** - Extracts skill name from hook input
2. **Tracks usage stats** - Updates `.shipkit/skill-usage.json`:
   - Total invocations
   - Per-skill count, firstUsed, lastUsed timestamps
3. **Creates tracking file** - Initializes if doesn't exist

**Value provided:** Enables stale skill detection shown in session-start summary.

---

### 4. shipkit-relentless-stop-hook.py
**Location:** `.claude/hooks/shipkit-relentless-stop-hook.py`
**Hook type:** Stop (timeout: 180s)
**Lines of code:** ~190

**What it does:**
1. **Quick exit check** - If no `.shipkit/relentless-state.local.md`, allows stop immediately
2. **Parses state file** - Reads YAML frontmatter: skill, task, completion_promise, iteration, max_iterations
3. **Checks enabled flag** - If `enabled: false`, allows stop without cleanup
4. **Enforces iteration limit** - Allows stop at max_iterations, cleans up state file
5. **Blocks stop** - Returns `decision: block` with reason containing:
   - Current iteration progress
   - Completion promise
   - Task description
   - Instructions for Claude to continue

**Value provided:** Powers the relentless execution loop for build/test/lint skills.

---

## Gap Analysis - Unused Hooks

### SessionEnd
**Fires when:** Session ends (user exits, terminal closes)

**Potential Shipkit uses:**
1. **Auto-save progress.md** - Capture session summary automatically
2. **Clean up temporary files** - Remove `.last-skill` breadcrumbs, `.local.md` files
3. **Session metrics** - Track session duration, token usage patterns

**Priority:** MEDIUM - Progress tracking is valuable but users may prefer manual control

---

### UserPromptSubmit
**Fires when:** Before user's prompt is processed by Claude

**Potential Shipkit uses:**
1. **Intent detection** - Pre-analyze prompt to auto-load relevant context
2. **Prompt enhancement** - Add project context to user prompts
3. **Guard rails** - Warn before destructive operations mentioned in prompt

**Priority:** LOW - Could be useful but risks being intrusive or slowing down interaction

---

### PreToolUse
**Fires when:** Before any tool is executed

**Potential Shipkit uses:**
1. **Write guards** - Warn before modifying protected context files (architecture.md, etc.)
2. **Command logging** - Track all bash commands for audit/replay
3. **Confirmation prompts** - Extra confirmation for dangerous operations

**Priority:** MEDIUM - Write guards could prevent accidental context corruption

---

### SubagentStart / SubagentStop
**Fires when:** Subagent (agent persona) starts/stops

**Potential Shipkit uses:**
1. **Agent logging** - Track which agents are invoked and their outcomes
2. **Context injection** - Load agent-specific context at start
3. **Agent metrics** - Usage patterns of different agent personas
4. **Handoff artifacts** - Automatically capture agent output for next session

**Priority:** MEDIUM - Useful for agent workflow optimization

---

### PermissionRequest
**Fires when:** Tool requests permission from user

**Potential Shipkit uses:**
1. **Permission logging** - Track permission denials for workflow refinement
2. **Auto-allow patterns** - Suggest adding commonly-allowed patterns to settings

**Priority:** LOW - Mostly diagnostic value, not core workflow

---

### Setup
**Fires when:** `--init`, `--init-only`, or `--maintenance` flags used

**Potential Shipkit uses:**
1. **First-run wizard** - Guide new users through initial setup
2. **Health check** - Verify Shipkit installation integrity
3. **Maintenance tasks** - Clean stale files, update indexes
4. **Version migration** - Automatic upgrades between Shipkit versions

**Priority:** HIGH - This is the natural place for installation/maintenance workflows

---

### PreCompact
**Fires when:** Before context compaction (conversation getting long)

**Potential Shipkit uses:**
1. **Auto-save progress** - Capture current state before compaction loses it
2. **Context prioritization** - Identify what context should survive compaction
3. **Work-in-progress checkpoint** - Save implementation status
4. **Warning to user** - Alert that context is about to be compressed

**Priority:** HIGH - Critical for preventing context loss during long sessions

---

## Recommendations

### Priority 1: PreCompact Hook (HIGH VALUE)
**Why:** Context loss during compaction is a major pain point. Auto-saving progress before compaction directly addresses Shipkit's core value proposition: session continuity.

**Implementation:**
- Auto-append to progress.md with current state
- Save current file being edited, last command results
- Summarize what was being worked on
- Keep it fast (<3s) to not delay compaction

---

### Priority 2: Setup Hook (HIGH VALUE)
**Why:** Natural fit for installation and maintenance. Currently, Shipkit has no automated setup - users run an external installer. Setup hook could provide:
- Post-install verification
- Periodic health checks
- Version migration

**Implementation:**
- `--init` runs first-time setup wizard
- `--maintenance` runs cleanup and health check
- Verify all skills are properly linked
- Check for common misconfigurations

---

### Priority 3: SessionEnd Hook (MEDIUM VALUE)
**Why:** Automatic progress capture at session end completes the session lifecycle.

**Implementation:**
- Quick summary append to progress.md
- Clean up `.local.md` temporary files
- Keep it very fast - user is leaving

**Caution:** Don't block exit or slow down session termination.

---

### Priority 4: SubagentStart Hook (MEDIUM VALUE)
**Why:** Shipkit has 7 agent personas. Tracking and contextualizing agent usage improves workflow.

**Implementation:**
- Log agent invocations to `.shipkit/agent-usage.json`
- Optionally inject agent-specific context
- Capture agent handoff summary at stop

---

### Priority 5: PreToolUse for Write Guards (MEDIUM VALUE)
**Why:** Protect critical context files from accidental modification.

**Implementation:**
- Warn before Write to architecture.md, stack.md, schema.md
- Allow override with explicit confirmation
- Log protected file access attempts

**Caution:** Don't be overly restrictive - false positives frustrate users.

---

### NOT Recommended

**UserPromptSubmit** - Too intrusive, slows interaction
**PermissionRequest** - Limited practical value
**PostToolUse for other tools** - Already tracking what matters (skills)

---

## Implementation Plan

### Phase 1: Critical (Next Release)
1. **PreCompact hook** - Auto-save before compaction
   - File: `shipkit-precompact-hook.py`
   - Appends checkpoint to progress.md
   - Fast execution (<3s target)

### Phase 2: Quality of Life
2. **Setup hook** - Installation verification and maintenance
   - File: `shipkit-setup-hook.py`
   - Verify installation integrity
   - Run cleanup/health check

3. **SessionEnd hook** - Clean exit
   - File: `shipkit-session-end-hook.py`
   - Append session summary
   - Clean temp files

### Phase 3: Advanced
4. **SubagentStart/Stop hooks** - Agent workflow tracking
   - Files: `shipkit-agent-start-hook.py`, `shipkit-agent-stop-hook.py`
   - Usage logging
   - Optional context injection

5. **PreToolUse write guard** - Context protection
   - File: `shipkit-write-guard-hook.py`
   - Protect critical `.shipkit/` files

---

## Appendix: Hook Configuration Reference

Current hooks in `shipkit.settings.json`:

```json
"hooks": {
  "SessionStart": [
    {
      "matcher": "startup|resume|clear|compact",
      "hooks": [{ "type": "command", "command": "python -X utf8 .claude/hooks/session-start.py" }]
    }
  ],
  "PostToolUse": [
    {
      "matcher": "Skill",
      "hooks": [{ "type": "command", "command": "python -X utf8 .claude/hooks/shipkit-track-skill-usage.py" }]
    }
  ],
  "Stop": [
    { "hooks": [{ "type": "command", "command": "python -X utf8 .claude/hooks/after-skill-router.py" }] },
    { "hooks": [{ "type": "command", "command": "python -X utf8 .claude/hooks/shipkit-relentless-stop-hook.py", "timeout": 180 }] }
  ]
}
```

To add new hooks, extend this configuration with the new hook types.
