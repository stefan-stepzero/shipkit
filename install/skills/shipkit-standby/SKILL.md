---
name: shipkit-standby
description: AFK daemon mode. Polls Mission Control for commands with exponential backoff. Activate before going AFK.
argument-hint: "[--max N]"
triggers:
  - standby
  - standby mode
  - go afk
  - daemon mode
  - wait for commands
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - Task
---

# shipkit-standby

Turns this Claude Code instance into an AFK daemon. Polls Mission Control for commands with exponential backoff. When a command arrives, executes it at full speed, then returns to standby.

---

## CRITICAL: Fully Autonomous

**This skill runs WITHOUT user interaction.** The operator is AFK.

- **NEVER** use AskUserQuestion
- **NEVER** ask for confirmation
- **ALWAYS** process Mission Control commands immediately
- **ALWAYS** mark commands as processed after completion
- **Minimize output during idle polls** — no reasoning, no commentary, just check and sleep

---

## When to Invoke

**User triggers:**
- "Go into standby mode"
- "Wait for Mission Control commands"
- "Daemon mode"
- "I'm going AFK"

**Use cases:**
- Operator is away but wants to send commands from the Mission Control dashboard
- Long-running monitoring where work is dispatched remotely
- Multi-instance orchestration from the dashboard

---

## Prerequisites

- Mission Control server running (`/shipkit-mission-control start`)
- Stop hook configured (Stop — `shipkit-relentless-stop-hook.py`)
- Receiver hook bypass is automatic (no special config needed — when standby is active, the receiver hook defers to standby's direct polling)

---

## Session ID

Your session-start context includes `Session ID: {sid8}`.
Use this 8-character ID in all state file names below. If not found in session context, use `unknown`.

---

## Arguments

```
/shipkit-standby [--max N]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--max N` | No | 500 | Maximum poll iterations before auto-exit |

---

## How It Works

1. **You create a state file** with standby configuration
2. **Each iteration, the stop hook tells you the exact inbox path** to poll
3. **You actively Glob the inbox** for `.inflight` (stale recovery) and `.json` (new commands)
4. **If command found:** Claim `.json` → `.inflight`, read & execute, mark `.inflight` → `.processed`, reset backoff
5. **If no command:** Increment `idle_count`, sleep for backoff duration, try to stop
6. **Stop hook blocks** → you loop back to step 3

**Key design:** Standby polls the inbox directly each iteration (active polling). The receiver hook is bypassed when standby is active to prevent race conditions.

---

## CRITICAL: Loop Mechanism

### Active Cycle (Command Found)

Each iteration, the stop hook provides the exact inbox path. Follow this sequence:

1. **Recover stale `.inflight` first:** Glob `{inbox_path}/*.inflight` — if found, read and execute the oldest, then rename `.inflight` → `.processed`
2. **Check for new commands:** Glob `{inbox_path}/*.json` — if found, take the oldest:
   a. Rename `.json` → `.inflight` (claim it) via Bash `mv`
   b. Read the `.inflight` file (JSON with a `prompt` field)
   c. Acknowledge briefly: "Received: [summary]"
   d. Execute the `prompt` fully (normal output here)
   e. Rename `.inflight` → `.processed` via Bash `mv`
3. Reset `idle_count: 0` in state file
4. Try to stop → Stop hook blocks → back to fast polling

### Idle Cycle (No Command)

1. Glob returns no `.inflight` or `.json` files (or inbox directory doesn't exist)
2. Read state file to get current `idle_count`
3. Increment `idle_count` in state file
4. Calculate sleep: `min(10 * 2^idle_count, 300)` seconds
5. Run `sleep N` via Bash — **this is your only output, no commentary**
6. Try to stop → Stop hook blocks → next iteration

### Shutdown

If a command prompt contains "shutdown", "exit standby", or "stop standby":
1. Delete `.shipkit/standby-state.{sid8}.local.md`
2. Stop — the hook will allow it since the state file is gone

---

## Backoff Schedule

| idle_count | Sleep duration |
|------------|---------------|
| 0          | 10s            |
| 1          | 20s            |
| 2          | 40s            |
| 3          | 80s            |
| 4          | 160s           |
| 5+         | 300s (cap)     |

After processing a command, `idle_count` resets to 0 (fast polling resumes).

---

## Command Lifecycle

Commands arrive as files in the inbox queue. **Standby handles the entire lifecycle.**

```
~/.shipkit-mission-control/.shipkit/mission-control/inbox/{full-session-id}/
  1738899990000.processed   ← you finished, marked done (oldest)
  1738900000000.inflight    ← you claimed it, now execute & mark processed
  1738900010000.json        ← pending (newest, server wrote)
```

**States:** `.json` → `.inflight` → `.processed`

**You** handle the entire lifecycle: `.json` → `.inflight` (claim) → `.processed` (done).
The receiver hook is bypassed when standby is active.

**Important:** The inbox uses the **full session UUID** (not sid8). The stop hook provides the exact path each iteration — use it directly.

```bash
# Claim a command
mv "{inbox_path}/1738900010000.json" "{inbox_path}/1738900010000.inflight"
# After execution, mark done
mv "{inbox_path}/1738900000000.inflight" "{inbox_path}/1738900000000.processed"
```

---

## Process

### Step 0: Parse Arguments

Extract `--max N` from input (default: 500).

### Step 1: Create State File

**Write to:** `.shipkit/standby-state.{sid8}.local.md`

```markdown
---
skill: standby
iteration: 0
max_iterations: [from --max or 500]
idle_count: 0
enabled: true
completion_promise: "Operator sent shutdown command or standby mode deactivated"
---
You are in standby mode. Actively poll the inbox for Mission Control commands.
Each iteration, the stop hook provides the inbox path — Glob it for .json and .inflight files.
If a command is found: claim .json→.inflight, read & execute, mark .inflight→.processed, reset idle_count to 0.
If no command: increment idle_count, sleep for backoff duration, and stop.
Minimize output during idle polls. No reasoning, no commentary — just sleep.
```

**Verify the state file was created before proceeding.**

### Step 2: Confirm Standby Activated

Output a brief confirmation:

```
Standby mode activated. Polling Mission Control for commands.
Max iterations: 500 | Backoff: 10s → 300s
Send commands from the dashboard at http://localhost:7777
To exit: send "shutdown" from dashboard, or delete .shipkit/standby-state.{sid8}.local.md
```

### Step 3: Begin Polling

The stop hook provides the exact inbox path each iteration. Follow its instructions:

1. **Glob for `.inflight` files** (stale recovery) — if found, execute & mark `.processed`
2. **Glob for `.json` files** (new commands) — if found, claim → execute → mark `.processed`
3. **If neither found** — idle cycle: increment `idle_count`, sleep, stop

The stop hook's `reason` message contains the full inbox path and step-by-step instructions.
Follow them exactly each iteration.

**Idle output format (entire response):**
```
[sleep Ns]
```

That's it. One Bash call. No other text.

### Step 4: After Processing a Command

1. Rename `.inflight` → `.processed` (the stop hook instructions include this)
2. Write `idle_count: 0` in state file
3. Brief summary: "Completed: [what was done]"
4. Try to stop → loop continues

---

## Constraints

- **Max iterations**: Default 500 (safety cap for very long AFK sessions)
- **Fully autonomous**: NO user prompts, NO confirmations
- **Minimal idle footprint**: One Bash sleep call per idle cycle, no other output
- **Always mark done**: After completing any command, rename `.inflight` → `.processed`
- **Always reset backoff**: Set `idle_count: 0` after processing a command
- **Shutdown keywords**: "shutdown", "exit standby", "stop standby" → delete state file and exit

---

## Integration with Other Skills

**Requires:**
- Mission Control server running (`/shipkit-mission-control start`)
- Stop hook configured (Stop — provides inbox path and polling instructions each iteration)

**Automatic:**
- Receiver hook bypass: when standby state file exists, the receiver hook returns empty (no race condition)

**Works with:**
- Any command sent from Mission Control dashboard
- Operator can dispatch any skill or instruction remotely

---

## Context Files

**Reads:**
- `.shipkit/standby-state.{sid8}.local.md` (state tracking)

**Writes:**
- `.shipkit/standby-state.{sid8}.local.md` (temporary, deleted on shutdown)

---

<!-- SECTION:success-criteria -->
## Success Criteria

- [ ] State file created with standby configuration
- [ ] Polling loop running with exponential backoff
- [ ] Commands received and executed from Mission Control
- [ ] `.inflight` files renamed to `.processed` after completion
- [ ] `idle_count` resets to 0 after command processing
- [ ] Shutdown command exits standby cleanly
<!-- /SECTION:success-criteria -->

---

<!-- SECTION:after-completion -->
## After Completion

Standby mode exited. The operator is back or sent a shutdown command.
<!-- /SECTION:after-completion -->
