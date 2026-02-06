# Mission Control - Multi-Instance Claude Code Monitor

**Status:** Spec / Concept
**Created:** 2026-02-07

---

## Problem Statement

When running multiple Claude Code instances across different VS Code windows (e.g., parallel workstreams, different projects), there's no unified way to:

1. **Monitor** what each instance is doing without switching windows
2. **Inject prompts** into specific instances remotely
3. **Coordinate** work across instances
4. **Track** progress across all active sessions

Currently requires manual window-switching and copy-pasting between instances.

---

## Vision

A "Mission Control" dashboard that:
- Shows all active Claude Code instances in one view
- Displays current task/status for each instance
- Allows clicking a button to inject a prompt into any instance
- Provides event timeline/logs across all instances

---

## Architecture

### High-Level Design

```
┌────────────────────────────────────────────────────────────────┐
│                      MISSION CONTROL                            │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Web Dashboard                                            │  │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐         │  │
│  │  │ Instance 1  │ │ Instance 2  │ │ Instance 3  │         │  │
│  │  │ shipkit     │ │ client-app  │ │ api-server  │         │  │
│  │  │ ───────────│ │ ───────────│ │ ───────────│         │  │
│  │  │ Running:    │ │ Idle        │ │ Running:    │         │  │
│  │  │ /spec       │ │             │ │ tests       │         │  │
│  │  │ ───────────│ │ ───────────│ │ ───────────│         │  │
│  │  │ [Inject]    │ │ [Inject]    │ │ [Inject]    │         │  │
│  │  └─────────────┘ └─────────────┘ └─────────────┘         │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              │                                  │
│                              ▼                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Server (Node.js / Python)                                │  │
│  │  - HTTP API for dashboard                                 │  │
│  │  - WebSocket hub for real-time updates                    │  │
│  │  - Command queue per instance                             │  │
│  │  - Event storage (SQLite or in-memory)                    │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────┘
         ▲                    ▲                    ▲
         │ WS                 │ WS                 │ WS
         │                    │                    │
┌────────┴────────┐  ┌────────┴────────┐  ┌────────┴────────┐
│   Claude Code   │  │   Claude Code   │  │   Claude Code   │
│   Instance 1    │  │   Instance 2    │  │   Instance 3    │
│   (VS Code)     │  │   (VS Code)     │  │   (Terminal)    │
└─────────────────┘  └─────────────────┘  └─────────────────┘
```

### Components

#### 1. Reporter Hook (Client-Side)

Installed in each Claude Code instance via hooks. Reports events to the server.

**Hook triggers:**
- `PreToolUse` - Tool about to execute
- `PostToolUse` - Tool completed
- `Notification` - Status messages
- `Stop` - Session ending

**Data sent:**
```json
{
  "instanceId": "uuid-or-project-hash",
  "projectName": "sg-shipkit",
  "projectPath": "/path/to/project",
  "event": "PostToolUse",
  "tool": "Edit",
  "timestamp": 1707300000,
  "status": "success",
  "metadata": {
    "file": "src/index.ts",
    "currentTask": "Implementing auth flow"
  }
}
```

#### 2. Command Receiver Hook (Client-Side)

Checks for pending commands from Mission Control.

**Options:**

**Option A: File-Based Polling**
```
~/.claude/mission-control/commands/{instance-id}.json
```
- Hook checks file on each turn
- If command exists, surfaces it to Claude
- Simple, no persistent connection needed
- Latency: depends on hook frequency

**Option B: WebSocket Persistent**
- Hook maintains WebSocket to server
- Receives commands in real-time
- More complex, better UX
- Requires connection management

**Option C: Hybrid MCP Server**
- MCP server runs locally
- Claude has `check_mission_control` tool
- Can poll or be pushed to
- Clean integration with Claude's tool model

#### 3. Central Server

**Endpoints:**
```
GET  /api/instances          - List all connected instances
GET  /api/instances/:id      - Get instance details
POST /api/instances/:id/command  - Queue command for instance
GET  /api/events             - Event log (filterable)
WS   /ws                     - Real-time event stream
```

**Storage:**
- In-memory for MVP (instances, recent events)
- SQLite for persistence (optional)

#### 4. Web Dashboard

**Views:**
- **Grid View**: Cards for each instance (status, current task)
- **Timeline View**: Chronological events across all instances
- **Instance Detail**: Full event log for one instance

**Actions:**
- Inject prompt (text input + send button)
- Pause/resume instance (if supported)
- Copy session context

---

## Prompt Injection Mechanism

The trickiest part. Claude Code doesn't have a direct "inject prompt" API.

### Approach 1: Notification Hook Response

Hooks can return messages that appear to the user. A hook could:
1. Check for pending commands
2. Return command as a "notification" to Claude
3. Claude sees it as system context

**Limitation:** This appears as system message, not user prompt.

### Approach 2: Stdin Injection (Terminal Only)

For terminal-based Claude Code:
```bash
echo "Your injected prompt" > /proc/{pid}/fd/0
```

**Limitation:** Only works for terminal, not VS Code extension.

### Approach 3: VS Code Extension API

If running Claude Code in VS Code:
- Extension could expose command injection API
- Would require custom VS Code extension

**Limitation:** Requires extension development.

### Approach 4: File-Watch + Skill

Create a skill that watches for commands:
```markdown
# Mission Control Receiver

Watch `~/.claude/mission-control/inbox.json` for commands.
When a command appears, execute it and clear the file.
```

Claude would need to be "listening" (skill running).

**Limitation:** Requires Claude to actively run the skill.

### Approach 5: Hook-Based Command Surface

Most promising for MVP:

```python
# PreToolUse hook - runs before every tool
import json
import os

COMMAND_FILE = os.path.expanduser("~/.claude/mission-control/command.json")

def main():
    if os.path.exists(COMMAND_FILE):
        with open(COMMAND_FILE) as f:
            command = json.load(f)
        os.remove(COMMAND_FILE)

        # Return as user instruction
        print(json.dumps({
            "result": f"[MISSION CONTROL] User instruction: {command['prompt']}"
        }))
```

This surfaces the command in the tool result, which Claude will see and act on.

---

## Implementation Phases

### Phase 1: Monitoring Only (MVP)

**Deliverables:**
- [ ] Reporter hook (sends events to server)
- [ ] Simple Express/FastAPI server
- [ ] Basic HTML dashboard (no framework)
- [ ] Instance list with status

**Effort:** 1-2 days

### Phase 2: Command Injection

**Deliverables:**
- [ ] Command queue in server
- [ ] Receiver hook (file-based)
- [ ] "Inject Prompt" button in UI
- [ ] Command status tracking

**Effort:** 1-2 days

### Phase 3: Rich Dashboard

**Deliverables:**
- [ ] React/Vue dashboard
- [ ] Real-time WebSocket updates
- [ ] Event timeline view
- [ ] Instance detail view
- [ ] Search/filter events

**Effort:** 2-3 days

### Phase 4: Advanced Features

**Deliverables:**
- [ ] Persistent storage (SQLite)
- [ ] Session replay
- [ ] Multi-user support
- [ ] Authentication
- [ ] Instance grouping/tagging

**Effort:** 3-5 days

---

## Technical Decisions

### Server Technology

| Option | Pros | Cons |
|--------|------|------|
| **Node.js + Express** | Fast dev, WebSocket native | Another runtime |
| **Python + FastAPI** | Matches hooks language | Needs async handling |
| **Bun** | Fast, TypeScript native | Less mature |

**Recommendation:** Node.js + Express (or Bun) for WebSocket simplicity.

### Dashboard Technology

| Option | Pros | Cons |
|--------|------|------|
| **Plain HTML + JS** | Zero build, fast MVP | Limited for rich UI |
| **React** | Component model, ecosystem | Build step |
| **Vue** | Simpler than React | Smaller ecosystem |
| **Svelte** | Minimal bundle | Less common |

**Recommendation:** Plain HTML for Phase 1, React for Phase 3.

### Instance Identification

How to uniquely identify each Claude Code instance?

| Option | Pros | Cons |
|--------|------|------|
| Project path hash | Deterministic | Conflicts if same project twice |
| Random UUID per session | Always unique | No persistence |
| User-assigned name | Meaningful | Manual step |
| PID + timestamp | Unique | Not human-readable |

**Recommendation:** Project path hash + session timestamp for uniqueness + readability.

---

## Validated Technical Capabilities (Feb 2026)

Research against official Claude Code docs, GitHub CHANGELOG, and community examples confirms:

### Hook Events Available

| Event | When Fires | Use for Mission Control |
|-------|------------|------------------------|
| `SessionStart` | New session begins | Register instance with server |
| `UserPromptSubmit` | User sends message | Track activity |
| `PreToolUse` | Before tool executes | Check for pending commands |
| `PostToolUse` | After tool completes | Report tool execution (async) |
| `Stop` | Session ending | Deregister instance |
| `SubagentStart/Stop` | Subagent lifecycle | Track parallel work |

### Hook Input (via stdin JSON)

```json
{
  "session_id": "abc123",           // Perfect for instance ID!
  "transcript_path": "/path/to/transcript.json",
  "cwd": "/project/path",
  "permission_mode": "default",
  "hook_event_name": "PostToolUse",
  "tool_name": "Edit",
  "tool_input": { "file_path": "..." }
}
```

### Hook Output Mechanisms

| Field | Effect | Best For |
|-------|--------|----------|
| `additionalContext` | Injected into Claude's context | Command injection! |
| `updatedInput` | Modify tool parameters | Input transformation |
| `systemMessage` | Notification to user/Claude | Status updates |
| `decision: "block"` | Prevent tool execution | Gating |

### Async Hooks

```json
{
  "hooks": {
    "PostToolUse": [{
      "command": "python mission-control-reporter.py",
      "async": true,
      "timeout": 5000
    }]
  }
}
```

- Non-blocking (Claude continues immediately)
- Results delivered next conversation turn
- Ideal for external server communication

### Limitations Confirmed

1. **No persistent connections** - Each hook invocation is independent
2. **600s default timeout** - Configurable per-hook
3. **Async output timing** - Delivered next turn, not immediately
4. **Hook config snapshot** - Captured at session start

### Validated: Command Injection via `additionalContext`

```python
# PreToolUse hook - checks for pending commands
import json
import sys
import os

COMMAND_FILE = os.path.expanduser("~/.claude/mission-control/inbox.json")

def main():
    if os.path.exists(COMMAND_FILE):
        with open(COMMAND_FILE) as f:
            cmd = json.load(f)
        os.remove(COMMAND_FILE)

        # This gets injected into Claude's context!
        print(json.dumps({
            "additionalContext": f"[MISSION CONTROL] Operator instruction: {cmd['prompt']}"
        }))

if __name__ == "__main__":
    main()
```

This is **proven to work** - similar pattern used in Shipkit's existing hooks.

---

## Recommendation Logic: Hardcoded vs Dynamic

Two approaches for generating skill recommendations:

### Option A: Hardcoded in Server (Current)

```javascript
const SKILL_KNOWLEDGE = {
    "shipkit-spec": {
        suggests: ["shipkit-plan", "shipkit-architecture-memory"],
        staleAfterDays: 14
    },
    // ... static rules
};
```

**Pros:**
- Simple, no external dependencies
- Fast, predictable
- Works offline

**Cons:**
- Can't adapt to project context
- Needs code changes for new skills
- Generic recommendations

### Option B: Controller Instance Analyzes (Preferred)

The controller Claude Code instance periodically runs an analysis skill:

```
Controller Instance:
├── Runs server in background
├── Has dashboard open
├── Periodically runs /mission-control analyze
│   ├── Reads skill usage data from server
│   ├── Reads each codebase's .shipkit/ context
│   ├── Uses Claude reasoning to prioritize
│   └── Updates server recommendations via API
```

**Pros:**
- Context-aware (knows project state)
- Adapts to new skills automatically
- Smarter prioritization
- Can learn patterns across codebases

**Cons:**
- Requires active controller instance
- Uses Claude API tokens
- More complex

### Hybrid Approach (Recommended)

1. **Server has basic hardcoded rules** (staleness, simple deps)
2. **Controller can run `/mission-control analyze`** to update with smarter recommendations
3. **Recommendations have source field** ("basic" vs "analyzed")

```
POST /api/recommendations
{
  "projectPath": "/path/to/project",
  "recommendations": [...],
  "source": "claude-analysis",
  "analyzedAt": "2026-02-07T..."
}
```

---

## Remaining Open Questions

1. **Multi-User Scenarios**
   - Should Mission Control support multiple users?
   - How to handle authentication?

2. **Scalability**
   - How many instances can we realistically monitor?
   - Event storage limits?

3. **Security**
   - Commands could be injected maliciously
   - Need authentication/authorization model

4. **Dashboard Technology**
   - Plain HTML vs React for rich UI
   - WebSocket vs SSE for real-time updates

---

## Related Ideas

- **Cross-Instance Context Sharing**: Share discoveries between instances
- **Task Routing**: Automatically route tasks to appropriate instance
- **Load Balancing**: Distribute work across instances
- **Session Recording**: Record and replay Claude sessions
- **Analytics Dashboard**: Aggregate metrics across all instances

---

## Shipkit Integration

### Singleton Server Pattern

Only ONE Mission Control server runs, regardless of how many Claude Code instances exist.

```
  Instance 1          Instance 2          Instance 3
      │                   │                   │
      ▼                   ▼                   ▼
  ┌────────┐          ┌────────┐          ┌────────┐
  │Server  │          │Server  │          │Server  │
  │running?│          │running?│          │running?│
  └───┬────┘          └───┬────┘          └───┬────┘
      │ NO                │ YES               │ YES
      ▼                   ▼                   ▼
  Start server ───────► Connect ◄─────────Connect
  (first wins)
```

**Coordination logic in hook:**
1. Ping `localhost:7777/health`
2. If no response → start server as detached background process
3. Connect and report events

**Race condition handling:**
- If two instances start simultaneously, both may try to start server
- Only one will succeed binding to port 7777
- Other fails silently, retries connection
- No harm done

### Component Mapping

| Component | Install Location | Runtime Location |
|-----------|------------------|------------------|
| Reporter hook | `~/.claude/hooks/mission-control-reporter.py` | Runs in each instance |
| Receiver hook | `~/.claude/hooks/mission-control-receiver.py` | Runs in each instance |
| Server | `~/.shipkit-mission-control/server/` | Hub (auto-created) |
| Dashboard | `~/.shipkit-mission-control/dashboard/` | Hub (auto-created) |
| Data | `~/.shipkit-mission-control/.shipkit/mission-control/` | Hub |
| Skill | `~/.claude/skills/shipkit-mission-control/` | Installed everywhere |

### Hub Structure (Auto-Created on First Use)

```
~/.shipkit-mission-control/          # Created by /mission-control start
├── server/
│   └── index.js                     # Node.js server
├── dashboard/
│   └── index.html                   # Mobile-responsive UI
├── .shipkit/
│   └── mission-control/
│       ├── codebases/               # Per-codebase analytics (persisted)
│       │   ├── sg-shipkit.json
│       │   └── client-app.json
│       ├── inbox/                   # Command queue per session
│       │   └── {session-id}.json
│       ├── events.jsonl             # Append-only event log
│       └── config.json              # Server configuration
├── server.log                       # Server output
└── README.md
```

### Server Lifecycle

| Event | Behavior |
|-------|----------|
| Any instance starts | Hooks are passive, do nothing until server exists |
| User runs `/mission-control start` | That instance becomes controller, starts server |
| Other instances' hooks detect server | Start reporting automatically |
| All Claude instances close | Server keeps running (orphaned) |
| `/mission-control stop` | Skill kills server process |
| Server crashes | Hooks silently stop reporting until restarted |
| System reboot | User must run `/mission-control start` again |

### Installation Philosophy

**Single installation, passive hooks:**
- All instances get the skill and hooks
- Hooks only report IF server is already running (zero overhead otherwise)
- Skill file is just markdown (no runtime cost)
- User explicitly designates controller by running `/mission-control start`
- No separate "controller add-on" needed

### Settings

```json
// install/settings/shipkit.settings.json
{
  "missionControl": {
    "enabled": true,
    "port": 7777,
    "autoStart": true
  }
}
```

Users can disable if they don't want the overhead.

---

## Next Steps

1. Validate hook capabilities (can they maintain WebSocket?)
2. Prototype reporter hook + minimal server
3. Test command injection via hook response
4. Build MVP dashboard
5. Iterate based on real usage

---

## Dashboard Design

### UI Hierarchy

```
┌─────────────────────────────────────────────────────────────┐
│  HEADER                                                      │
│  📡 Mission Control          [Active: 3] [Total: 5] [Events]│
└─────────────────────────────────────────────────────────────┘
│                                                              │
│  ┌─────────────────────────────┐ ┌────────────────────────┐ │
│  │ INSTANCES (grouped by repo) │ │ EVENT STREAM           │ │
│  │                             │ │                        │ │
│  │ ┌─────────────────────────┐ │ │ 📝 Edit in sg-shipkit  │ │
│  │ │ 📁 sg-shipkit           │ │ │ 🔨 Bash in client-app  │ │
│  │ │ P:/Projects/sg-shipkit  │ │ │ ⚡ Skill: /spec        │ │
│  │ │ 👥 2 instances ⚡ 12 skills│ │ │ 📖 Read in api-server │ │
│  │ │                         │ │ │ ...                    │ │
│  │ │ ● Active - Edit (2m ago)│ │ │                        │ │
│  │ │   [Inject] [Skills]     │ │ │                        │ │
│  │ │ ● Active - Bash (5m ago)│ │ │                        │ │
│  │ │   [Inject] [Skills]     │ │ │                        │ │
│  │ │                         │ │ │                        │ │
│  │ │ 🟠 RECOMMENDATIONS      │ │ │                        │ │
│  │ │ ● work-memory stale     │ │ │                        │ │
│  │ │   [Run /work-memory]    │ │ │                        │ │
│  │ └─────────────────────────┘ │ │                        │ │
│  │                             │ │                        │ │
│  │ ┌─────────────────────────┐ │ │                        │ │
│  │ │ 📁 client-app           │ │ │                        │ │
│  │ │ ...                     │ │ │                        │ │
│  │ └─────────────────────────┘ │ │                        │ │
│  └─────────────────────────────┘ └────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### Key UI Components

| Component | Purpose |
|-----------|---------|
| **Header Stats** | Active/total instances, event count, uptime |
| **Codebase Groups** | Group instances by repo/project path |
| **Instance Cards** | Status dot, last tool, time, inject/skills buttons |
| **Recommendations** | Per-codebase skill suggestions with priority |
| **Event Stream** | Real-time tool execution feed with icons |
| **Quick Skills Modal** | Grid of Shipkit skills to send to instance |

### Skill-Based Quick Actions

Instead of generic buttons, the dashboard shows Shipkit skills:

```
┌──────────────────────────────────────────┐
│ QUICK ACTIONS                            │
│ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐      │
│ │ 📊 │ │ 📝 │ │ 🔨 │ │ 🧪 │ │ ✅ │      │
│ │Stat│ │Work│ │Buil│ │Test│ │Veri│      │
│ └────┘ └────┘ └────┘ └────┘ └────┘      │
│                                          │
│ RECOMMENDATIONS                          │
│ ● shipkit-work-memory stale (2d) [Run]   │
│ ● After /spec, consider /plan    [Run]   │
│                                          │
│ ALL SKILLS                               │
│ [Grid of all Shipkit skills...]          │
└──────────────────────────────────────────┘
```

---

## References

- Claude Code Hooks: https://docs.anthropic.com/en/docs/claude-code/hooks
- Claude Code GitHub: https://github.com/anthropics/claude-code
