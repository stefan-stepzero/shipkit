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
- Receiver hook configured (PreToolUse — `mission-control-receiver.py`)
- Stop hook configured (Stop — `shipkit-relentless-stop-hook.py`)

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
2. **You check the inbox** for pending commands
3. **If command found:** Execute it, mark `.inflight` → `.processed`, reset backoff
4. **If no command:** Increment `idle_count`, sleep for backoff duration, try to stop
5. **Stop hook blocks** → you loop back to step 2

---

## CRITICAL: Loop Mechanism

### Idle Cycle (No Command)

1. Read state file to get current `idle_count`
2. No command was injected by the receiver hook — nothing to do
3. Increment `idle_count` in state file
4. Calculate sleep: `min(10 * 2^idle_count, 300)` seconds
5. Run `sleep N` via Bash — **this is your only output, no commentary**
6. Try to stop → Stop hook blocks → next iteration

### Active Cycle (Command Received)

1. Receiver hook injected a command via `additionalContext` — you'll see it with a filepath
2. Acknowledge briefly: "Received: [summary of command]"
3. Execute the command fully (normal output here)
4. Rename the `.inflight` file to `.processed` via Bash
5. Reset `idle_count: 0` in state file
6. Try to stop → Stop hook blocks → back to fast polling

### Shutdown

If a command contains "shutdown", "exit standby", or "stop standby":
1. Delete `.shipkit/standby-state.local.md`
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

Commands arrive as files in the inbox queue:

```
~/.shipkit-mission-control/.shipkit/mission-control/inbox/{sessionId}/
  1738899990000.processed   ← you finished, marked done (oldest)
  1738900000000.inflight    ← receiver hook claimed, you're working on it
  1738900010000.json        ← pending (newest, server wrote)
```

**States:** `.json` → `.inflight` → `.processed`

The receiver hook handles `.json` → `.inflight`. **You** handle `.inflight` → `.processed`.

The `.inflight` filepath is included in the `additionalContext` injection. Use it to rename when done:

```bash
mv /path/to/1738900000000.inflight /path/to/1738900000000.processed
```

---

## Process

### Step 0: Parse Arguments

Extract `--max N` from input (default: 500).

### Step 1: Create State File

**Write to:** `.shipkit/standby-state.local.md`

```markdown
---
skill: standby
iteration: 0
max_iterations: [from --max or 500]
idle_count: 0
enabled: true
completion_promise: "Operator sent shutdown command or standby mode deactivated"
---
You are in standby mode. Await Mission Control commands.
If a command was injected via additionalContext, execute it and mark the .inflight file as .processed.
If no command, increment idle_count, sleep for backoff duration, and stop.
Minimize output during idle polls. No reasoning, no commentary — just sleep.
After completing a command, reset idle_count to 0 in this file.
```

**Verify the state file was created before proceeding.**

### Step 2: Confirm Standby Activated

Output a brief confirmation:

```
Standby mode activated. Polling Mission Control for commands.
Max iterations: 500 | Backoff: 10s → 300s
Send commands from the dashboard at http://localhost:7777
To exit: send "shutdown" from dashboard, or delete .shipkit/standby-state.local.md
```

### Step 3: Begin Polling

1. Check if a command was injected via `additionalContext`
2. **If yes:** Process it (active cycle above)
3. **If no:** Read `idle_count` from state file, increment it, sleep, stop

**Idle output format (entire response):**
```
[sleep Ns]
```

That's it. One Bash call. No other text.

### Step 4: After Processing a Command

1. Rename `.inflight` → `.processed`
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
- Receiver hook configured (PreToolUse)
- Stop hook configured (Stop)

**Works with:**
- Any command sent from Mission Control dashboard
- Operator can dispatch any skill or instruction remotely

---

## Context Files

**Reads:**
- `.shipkit/standby-state.local.md` (state tracking)

**Writes:**
- `.shipkit/standby-state.local.md` (temporary, deleted on shutdown)

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
