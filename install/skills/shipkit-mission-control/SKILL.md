---
name: shipkit-mission-control
description: Launch Mission Control dashboard to monitor and command multiple Claude Code instances
---

# shipkit-mission-control - Multi-Instance Monitor & Command Center

**Purpose**: Monitor all active Claude Code instances from one dashboard, inject prompts remotely.

**What it does**: Starts the Mission Control server (if not running), opens the web dashboard, and manages the monitoring infrastructure.

---

## When to Invoke

**User triggers**:
- "Open mission control"
- "Monitor my Claude instances"
- "Start the dashboard"
- "I want to see all my sessions"

**Use cases**:
- Running multiple Claude Code instances across different projects
- Want to monitor progress without switching windows
- Need to inject a prompt into a specific instance remotely

---

## Prerequisites

- Node.js installed (for server)
- Multiple Claude Code instances running (to have something to monitor)

---

## Process

### Step 1: Check/Create Hub Directory

The Mission Control hub lives at `~/.shipkit-mission-control/`. Check if it exists:

**Windows:** `%USERPROFILE%\.shipkit-mission-control\`
**macOS/Linux:** `~/.shipkit-mission-control/`

If the hub doesn't exist, create the full structure:

```
~/.shipkit-mission-control/
├── server/
│   ├── index.js          # Node.js API server
│   └── package.json      # Server metadata
├── dashboard/
│   ├── dist/             # Built React app (served by server)
│   │   ├── index.html
│   │   └── assets/       # JS, CSS bundles
│   ├── src/              # React source (for development)
│   ├── package.json      # Dashboard dependencies
│   └── vite.config.ts    # Vite configuration
├── .shipkit/
│   └── mission-control/
│       ├── codebases/    # Per-codebase analytics
│       ├── inbox/        # Command queue
│       └── config.json   # Server configuration
└── README.md
```

**Create directories:**
```bash
mkdir -p ~/.shipkit-mission-control/server
mkdir -p ~/.shipkit-mission-control/dashboard/dist
mkdir -p ~/.shipkit-mission-control/.shipkit/mission-control/codebases
mkdir -p ~/.shipkit-mission-control/.shipkit/mission-control/inbox
```

### Step 2: Ensure Server and Dashboard Files Exist

Check if `~/.shipkit-mission-control/server/index.js` exists.

If NOT, copy from Shipkit install location:
- `install/mission-control/server/` → `~/.shipkit-mission-control/server/`
- `install/mission-control/dashboard/dist/` → `~/.shipkit-mission-control/dashboard/dist/`

The dashboard is a React + Vite app. The pre-built `dist/` folder is included in Shipkit. For development:
```bash
cd ~/.shipkit-mission-control/dashboard && npm install && npm run dev
```
This starts a Vite dev server on port 5173 with API proxy to port 7777.

### Step 3: Create Config (if missing)

If `~/.shipkit-mission-control/.shipkit/mission-control/config.json` doesn't exist, create it:

```json
{
  "port": 7777,
  "host": "0.0.0.0",
  "createdAt": "<current timestamp>",
  "version": "1.0.0"
}
```

### Step 4: Check Server Status

Check if Mission Control server is already running:

```bash
curl -s http://localhost:7777/health
```

If response is `{"status":"ok"}`, server is running. Skip to Step 6.

### Step 5: Start Server

Start the Mission Control server as a background process from the hub:

**Windows:**
```bash
cd %USERPROFILE%\.shipkit-mission-control && start /B node server\index.js
```

**macOS/Linux:**
```bash
cd ~/.shipkit-mission-control && nohup node server/index.js > server.log 2>&1 &
```

Wait 2 seconds for server to initialize, then verify:
```bash
curl -s http://localhost:7777/health
```

### Step 6: Get Network Address

Get the local network IP so user can access from mobile:

**Windows:**
```bash
ipconfig | findstr /i "IPv4"
```

**macOS/Linux:**
```bash
hostname -I | awk '{print $1}'
```

### Step 7: Report Status

Tell user:
```
✅ Mission Control is running

📍 Dashboard URLs:
   Local:   http://localhost:7777
   Network: http://<local-ip>:7777  ← Use this on mobile

📊 Status:
   Hub: ~/.shipkit-mission-control/
   Connected instances: <count>

💡 Tips:
   • Other Claude instances will auto-report when active
   • Access from phone: http://<local-ip>:7777
   • Stop server: /mission-control stop
   • Update recommendations: /mission-control analyze
```

### Step 8: Open Dashboard (optional)

If user wants, open browser:

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

## Arguments

| Argument | Description |
|----------|-------------|
| (none) | Start server and show status |
| `start` | Start server and open dashboard |
| `stop` | Stop the running server |
| `status` | Check server status without starting |
| `open` | Open dashboard in browser (start server if needed) |
| `analyze` | Analyze all codebases and update recommendations |

---

## Analyze Command

When running `/mission-control analyze`, the controller instance:

### Step 1: Fetch Current Data

```bash
curl -s http://localhost:7777/api/codebases
```

This returns all tracked codebases with their skill usage data.

### Step 2: For Each Codebase, Analyze Context

For each codebase in the response:

1. **Read the .shipkit/ context files** (if accessible):
   - `.shipkit/vision.md` - Project goals
   - `.shipkit/specs/` - Active specifications
   - `.shipkit/plans/` - Implementation plans
   - `.shipkit/implementations.md` - What's been built

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
📊 Mission Control Analysis Complete

Analyzed 3 codebases:

📁 sg-shipkit (P:/Projects/sg-shipkit)
   Phase: Active Development
   Recommendations:
   • [HIGH] /shipkit-verify - No quality check in 5 days
   • [MED] /shipkit-work-memory - Log recent progress

📁 client-app (P:/Projects/client-app)
   Phase: Planning
   Recommendations:
   • [HIGH] /shipkit-plan - Spec exists, ready for planning
   • [LOW] /shipkit-architecture-memory - Log tech decisions

📁 api-server (P:/Projects/api-server)
   Phase: Discovery
   Recommendations:
   • [HIGH] /shipkit-project-context - No context scan yet
   • [MED] /shipkit-spec - Define first feature
```

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

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│  MISSION CONTROL SERVER (http://localhost:7777)             │
│  ├── /              - Dashboard UI                          │
│  ├── /health        - Liveness check                        │
│  ├── /api/instances - List connected instances              │
│  ├── /api/events    - Receive events from hooks             │
│  └── /api/command   - Queue command for instance            │
└─────────────────────────────────────────────────────────────┘
        ▲ HTTP POST (events)           │ File write (commands)
        │                              ▼
┌───────┴──────────────────────────────┴──────────────────────┐
│  Each Claude Code Instance                                   │
│  ├── Reporter Hook (PostToolUse) → sends events to server   │
│  └── Receiver Hook (PreToolUse)  → checks for commands      │
└──────────────────────────────────────────────────────────────┘
```

---

## What Makes This "Lite"

**Included**:
- Single-server architecture (no databases)
- File-based command injection (simple, reliable)
- React + Vite dashboard with graph visualization (React Flow)
- Artifact viewer with interactive architecture diagrams, ER diagrams, journey maps
- Auto-start on first use

**Not included**:
- Authentication (local use only)
- Multi-user support
- Remote access (localhost only, but network IP shown for mobile access)

**Philosophy**: Simple monitoring for local development. Not a production ops tool.

---

## Troubleshooting

### Server won't start
- Check if port 7777 is in use: `netstat -an | grep 7777`
- Check Node.js is installed: `node --version`
- Check server files exist: `~/.claude/mission-control/server/index.js`

### No instances showing
- Hooks may not be installed - run `/shipkit-update`
- Check hook is firing - look for HTTP requests in server logs
- Verify session has `session_id` in hook input

### Commands not being received
- Check inbox file exists: `~/.claude/mission-control/inbox/{session_id}.json`
- Verify PreToolUse hook is configured in settings

---

## Files Installed

| Path | Purpose |
|------|---------|
| `~/.shipkit-mission-control/server/index.js` | Node.js API server |
| `~/.shipkit-mission-control/server/package.json` | Server metadata |
| `~/.shipkit-mission-control/dashboard/dist/` | Built React dashboard |
| `~/.shipkit-mission-control/dashboard/src/` | React source code |
| `~/.shipkit-mission-control/dashboard/package.json` | Dashboard dependencies |
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
