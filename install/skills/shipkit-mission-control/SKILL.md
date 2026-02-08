---
name: shipkit-mission-control
description: Check Mission Control status, open dashboard, analyze codebases, and send commands
---

# shipkit-mission-control - Mission Control Client

**Purpose**: Thin client for the standalone Mission Control dashboard. Checks server status, opens the dashboard, and analyzes codebases for recommendations.

**Mission Control is a standalone project.** The server and dashboard live in their own repo: https://github.com/stefan-stepzero/sg-shipkit-missioncontrol

---

## When to Invoke

**User triggers**:
- "Open mission control"
- "Monitor my Claude instances"
- "Check mission control status"
- "Analyze my codebases"

---

## Prerequisites

- Mission Control server running in a separate terminal
- Start it from the MC repo: `python start.py` or `node server/index.js`

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
   Open dashboard: /shipkit-mission-control open
   Analyze codebases: /shipkit-mission-control analyze
```

**If server is NOT running:**

Tell user:
```
Mission Control is not running.

To start it:
   1. Clone: git clone https://github.com/stefan-stepzero/sg-shipkit-missioncontrol
   2. Start: cd sg-shipkit-missioncontrol && python start.py

Then come back here and run /shipkit-mission-control again to see the status.
```

---

## Arguments

| Argument | Description |
|----------|-------------|
| (none) | Check server status and show dashboard URL |
| `status` | Check server status |
| `open` | Open dashboard in browser |
| `analyze` | Analyze all codebases and update recommendations |

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
   - `.shipkit/specs/{todo,active,parked,shipped}/*.json` - Specifications by status
   - `.shipkit/plans/{todo,active,parked,shipped}/*.json` - Plans by status
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

## Troubleshooting

### Server won't start
- Check if port 7777 is in use: `netstat -an | grep 7777`
- Check Node.js is installed: `node --version`
- Get the MC repo: https://github.com/stefan-stepzero/sg-shipkit-missioncontrol

### No instances showing
- Hooks may not be installed - run `/shipkit-update`
- Check hook is firing - look for HTTP requests in server logs
- Verify session has `session_id` in hook input

### Commands not being received
- Check inbox directory exists: `~/.shipkit-mission-control/.shipkit/mission-control/inbox/`
- Verify standby mode is active in the target instance

---

## Integration with Other Skills

### Before This Skill
- No prerequisites - can be started anytime

### After This Skill
- Continue normal work - monitoring runs in background

### Works Alongside
- All other skills - monitoring is passive
- `/shipkit-implement-independently` - monitor parallel implementations
- `/shipkit-standby` - receives commands from Mission Control
