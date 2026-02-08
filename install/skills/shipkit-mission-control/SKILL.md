---
name: shipkit-mission-control
description: Launch Mission Control dashboard to monitor and command multiple Claude Code instances
---

# shipkit-mission-control - Multi-Instance Monitor & Command Center

**Purpose**: Monitor all active Claude Code instances from one dashboard, inject prompts remotely.

**What it does**: Checks the Mission Control server status, shows the dashboard URL, and analyzes codebases for recommendations.

---

## When to Invoke

**User triggers**:
- "Open mission control"
- "Monitor my Claude instances"
- "Start the dashboard"
- "I want to see all my sessions"
- "Check mission control status"

**Use cases**:
- Running multiple Claude Code instances across different projects
- Want to monitor progress without switching windows
- Need to inject a prompt into a specific instance remotely

---

## Prerequisites

- Node.js installed (for server)
- Mission Control server running in a separate terminal

---

## Process

### Step 1: Check Server Status

Check if Mission Control server is running:

```bash
curl -s http://localhost:7777/health
```

### Step 2: Report Status

**If server IS running** (response includes `"status":"ok"`):

Get the local network IP:

**Windows:**
```bash
ipconfig | findstr /i "IPv4"
```

**macOS/Linux:**
```bash
hostname -I | awk '{print $1}'
```

Tell user:
```
Mission Control is running

Dashboard URLs:
   Local:   http://localhost:7777
   Network: http://<local-ip>:7777

Status:
   Hub: ~/.shipkit-mission-control/
   Connected instances: <count from health response>
   Version: <version from health response>

Tips:
   Stop server: /shipkit-mission-control stop
   Open dashboard: /shipkit-mission-control open
   Analyze codebases: /shipkit-mission-control analyze
```

**If server is NOT running:**

Tell user:
```
Mission Control is not running.

To start it, open a separate terminal and run:
   python .shipkit/scripts/mission-control.py

Then come back here and run /shipkit-mission-control again to see the status.
```

---

## Arguments

| Argument | Description |
|----------|-------------|
| (none) | Check server status and show dashboard URL |
| `start` | Same as (none) but remind user to start in a separate terminal |
| `stop` | Stop the running server |
| `status` | Check server status without starting |
| `open` | Open dashboard in browser |
| `analyze` | Analyze all codebases and update recommendations |

---

## Stop Command

To stop the Mission Control server:

**Find and kill process on port 7777:**

**Windows:**
```bash
for /f "tokens=5" %a in ('netstat -aon ^| find ":7777"') do taskkill /F /PID %a
```

**macOS/Linux:**
```bash
lsof -ti:7777 | xargs kill -9
```

---

## Open Command

Open the dashboard in the default browser:

**Windows:**
```bash
start http://localhost:7777
```

**macOS:**
```bash
open http://localhost:7777
```

**Linux:**
```bash
xdg-open http://localhost:7777
```

---

## Analyze Command

When running `/shipkit-mission-control analyze`, the controller instance:

### Step 1: Fetch Current Data

```bash
curl -s http://localhost:7777/api/codebases
```

This returns all tracked codebases with their skill usage data.

### Step 2: For Each Codebase, Analyze Context

For each codebase in the response:

1. **Read the .shipkit/ context files** (if accessible):
   - `.shipkit/why.json` - Project vision and goals
   - `.shipkit/specs/active/*.json` - Active specifications
   - `.shipkit/plans/active/*.json` - Implementation plans
   - `.shipkit/implementations.json` - What's been built

2. **Analyze skill usage patterns**:
   - Which skills have been used recently?
   - Which skills are stale (not used in X days)?
   - What's the project phase? (discovery, planning, implementation, polish)

3. **Generate smart recommendations**:
   - Based on project phase, suggest appropriate skills
   - Identify gaps (e.g., specs exist but no plan)
   - Prioritize by urgency and impact

### Step 3: Update Server Recommendations

For each codebase, POST updated recommendations:

```bash
curl -X POST http://localhost:7777/api/recommendations \
  -H "Content-Type: application/json" \
  -d '{
    "projectPath": "/path/to/project",
    "recommendations": [
      {
        "type": "phase",
        "skill": "shipkit-plan",
        "message": "Specs exist but no plan - ready to plan implementation",
        "priority": "high",
        "action": "/shipkit-plan"
      }
    ],
    "source": "claude-analysis",
    "analyzedAt": "2026-02-07T..."
  }'
```

### Step 4: Report Summary

Tell the user:
- How many codebases were analyzed
- Key recommendations generated
- Any codebases that couldn't be analyzed (not accessible)

---

## Example Analysis Output

```
Mission Control Analysis Complete

Analyzed 3 codebases:

my-framework (~projects/my-framework)
   Phase: Active Development
   Recommendations:
   [HIGH] /shipkit-verify - No quality check in 5 days
   [MED] /shipkit-work-memory - Log recent progress

client-app (~projects/client-app)
   Phase: Planning
   Recommendations:
   [HIGH] /shipkit-plan - Spec exists, ready for planning
   [LOW] /shipkit-architecture-memory - Log tech decisions

api-server (~projects/api-server)
   Phase: Discovery
   Recommendations:
   [HIGH] /shipkit-project-context - No context scan yet
   [MED] /shipkit-spec - Define first feature
```

---

## Architecture Overview

```
                    MISSION CONTROL SERVER (http://localhost:7777)
                    --- /              - Dashboard UI
                    --- /health        - Liveness check
                    --- /api/instances - List connected instances
                    --- /api/events    - Receive events from hooks
                    --- /api/command   - Queue command for instance

        HTTP POST (events)           File write (commands)

  Each Claude Code Instance
  --- Reporter Hook (PostToolUse) -> sends events to server
  --- Receiver Hook (PreToolUse)  -> checks for commands
```

---

## What Makes This "Lite"

**Included**:
- Single-server architecture (no databases)
- File-based command injection (simple, reliable)
- React + Vite dashboard with graph visualization (React Flow)
- Artifact viewer with interactive architecture diagrams, ER diagrams, journey maps
- User-visible foreground server process (Ctrl+C to stop)

**Not included**:
- Authentication (local network use only)
- Multi-user support
- Remote access beyond LAN (binds to 0.0.0.0 for local network access from mobile devices)

**Philosophy**: Simple monitoring for local development. Not a production ops tool.

---

## Troubleshooting

### Server won't start
- Check if port 7777 is in use: `netstat -an | grep 7777`
- Check Node.js is installed: `node --version`
- Check server files exist: `~/.shipkit-mission-control/server/index.js`

### No instances showing
- Hooks may not be installed - run `/shipkit-update`
- Check hook is firing - look for HTTP requests in server logs
- Verify session has `session_id` in hook input

### Commands not being received
- Check inbox file exists: `~/.shipkit-mission-control/.shipkit/mission-control/inbox/{session_id}.json`
- Verify PreToolUse hook is configured in settings

---

## Files Installed

| Path | Purpose |
|------|---------|
| `~/.shipkit-mission-control/server/index.js` | Node.js API server |
| `~/.shipkit-mission-control/server/package.json` | Server metadata |
| `~/.shipkit-mission-control/dashboard/dist/` | Built React dashboard |
| `.shipkit/scripts/mission-control.py` | Startup script (run in separate terminal) |
| Hooks: `shipkit-mission-control-reporter.py` | Event reporter hook |
| Hooks: `shipkit-mission-control-receiver.py` | Command receiver hook |

---

## Integration with Other Skills

### Before This Skill
- No prerequisites - can be started anytime

### After This Skill
- Continue normal work - monitoring runs in background

### Works Alongside
- All other skills - monitoring is passive
- `/shipkit-implement-independently` - monitor parallel implementations
