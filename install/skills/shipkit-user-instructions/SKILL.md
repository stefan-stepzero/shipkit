---
name: shipkit-user-instructions
description: "Use when there are manual tasks the user must complete. Triggers: 'create task', 'track TODO', 'user needs to', 'manual step required'."
---

# shipkit-user-instructions - Task Tracking for Manual User Actions

**Purpose**: Prevent manual tasks from being lost in chat by maintaining a persistent JSON tracking file for tasks that require user action outside Claude's control.

**What it does**: Captures manual tasks the user must complete, tracks their status, and persists them in `.shipkit/user-tasks.json` — a structured JSON artifact readable by Claude, machine-readable by other tools, and the single source of truth for user action items.

**Output format**: JSON — follows the Shipkit artifact convention for dashboard integration.

---

## When to Invoke

**Auto-trigger scenarios** (other skills invoke this):
- Missing environment variables detected (shipkit-integration-docs)
- Package installation needed (implement)
- External service configuration required (Lemon Squeezy webhooks, API keys)
- Database migrations need running
- Deploy configuration needed
- Git repository setup required

**Manual invocation**:
- User says: "Track this task", "Add to my todo", "Remind me to..."
- Claude realizes: "I need the user to do X before I can continue"

**Philosophy**: If Claude can't do it directly, track it so it doesn't get forgotten.

---

## Prerequisites

**Optional**:
- `.shipkit/` directory (will create if missing)

**No hard prerequisites** - This skill can run anytime.

---

## Process

### Step 1: Confirm Task Details

**Before creating task entry**, ask user 2-3 questions:

1. **What specific task needs to be done?**
   - "Set up Lemon Squeezy webhook?"
   - "Configure webhook endpoint?"
   - "Set environment variable?"
   - (Let user describe or Claude infers from context)

2. **Why is this needed?**
   - "For local webhook testing during development"
   - "To enable payment processing"
   - "To connect to production database"

3. **How urgent is this?**
   - "Blocking me right now?" → 🔴 High priority
   - "Needed before deploy?" → 🟡 Medium priority
   - "Nice to have later?" → 🟢 Low priority

**Why ask**: Ensure task is clear and actionable before tracking it.

---

### Step 2: Add Task to user-tasks.json

**Use Write tool to create/update**: `.shipkit/user-tasks.json`

**If file doesn't exist**, create it with the initial structure (see JSON Schema section below).

**If file exists**, read it, add the new task to the `tasks` array, recompute `summary`, and overwrite the file.

**New task entry fields**:
- `id` — Kebab-case slug (e.g., `"configure-lemon-squeezy-webhook"`)
- `title` — Human-readable task name
- `description` — 1-2 sentence explanation of why this task is necessary
- `status` — `"active"` for new tasks
- `priority` — `"high"`, `"medium"`, or `"low"` (from Step 1)
- `steps` — Array of specific action strings
- `verification` — Array of criteria to confirm task is done
- `relatedFeature` — Feature name or `null`
- `triggeredBy` — Skill name that triggered this or `"manual"`
- `createdAt` — ISO date (YYYY-MM-DD)
- `completedAt` — `null` for new tasks

**Example - Lemon Squeezy Webhook Task**:
```json
{
  "id": "configure-lemon-squeezy-webhook",
  "title": "Configure Lemon Squeezy Webhook",
  "description": "Webhook configuration enables Lemon Squeezy to notify your app of payment events (order_created, subscription_created). Without this, users won't get access after payment.",
  "status": "active",
  "priority": "high",
  "steps": [
    "Go to Lemon Squeezy dashboard → Settings → Webhooks",
    "Add webhook URL: https://your-domain.com/api/webhooks/lemonsqueezy",
    "Select events: order_created, subscription_created, subscription_updated",
    "Copy the signing secret",
    "Add to .env.local: LEMONSQUEEZY_WEBHOOK_SECRET=...",
    "Add API key: LEMONSQUEEZY_API_KEY=..."
  ],
  "verification": [
    ".env.local contains LEMONSQUEEZY_WEBHOOK_SECRET",
    ".env.local contains LEMONSQUEEZY_API_KEY",
    "Test purchase triggers webhook (use test mode)"
  ],
  "relatedFeature": "Payment processing",
  "triggeredBy": "shipkit-integration-docs",
  "createdAt": "2025-01-15",
  "completedAt": null
}
```

---

### Step 3: Confirm Task Tracked

**Output to user** (formatted summary, not raw JSON):
```
Task tracked.

Location: .shipkit/user-tasks.json

  Task: [Task Title]
  Priority: High
  Status: active

  Total tasks: X active, Y completed, Z deferred

Next: Complete the task steps, then tell me "Task [X] done" so I can mark it complete.

Should I continue with other work, or wait for you to complete this?
```

---

### Step 4: Support Task Status Updates

**When user says**: "I'm working on task X", "Started the Lemon Squeezy setup"

**Action**: Read `.shipkit/user-tasks.json`, find the task by id or title match, update its `status` field from `"active"` to `"in-progress"`, recompute `summary`, and overwrite the file.

**Confirmation**:
```
Updated task status to in-progress.

  Task: [Task Title]
  Status: in-progress

Let me know when it's done!
```

---

### Step 5: Mark Tasks Completed

**When user says**: "Task done", "Finished the Lemon Squeezy setup", "Webhook is configured"

**Process**:

1. **Verify completion** (ask user):
   - "Did you complete all verification steps?"
   - "Can you confirm [specific verification]?"

2. **Read `.shipkit/user-tasks.json`** and find the task by id or title match

3. **Update the task entry**:
   - Set `status` to `"completed"`
   - Set `completedAt` to current date (YYYY-MM-DD)

4. **Recompute `summary`** counts

5. **Overwrite `.shipkit/user-tasks.json`** with updated content

6. **Confirm to user**:
```
Task marked complete.

  Task: [Task Title]
  Completed: [YYYY-MM-DD]

  Remaining: X active, Y completed, Z deferred

Ready to continue with [next step]?
```

**Note**: Completed tasks remain in user-tasks.json with `status: "completed"`. They are not moved to a separate file — the single JSON file is the source of truth for all task states.

---

### Step 6: List Tasks (On Demand)

**When user says**: "What tasks do I have?", "Show my todos", "What's pending?"

**Action**:
1. Read `.shipkit/user-tasks.json`
2. Parse the `tasks` array and `summary` object
3. Show formatted summary (not raw JSON):

```
User Tasks

  High Priority:
  1. Configure Lemon Squeezy Webhook (active)
  2. Set up production database (in-progress)

  Medium Priority:
  1. Install Docker for local development (active)

  Low Priority:
  (none)

  Summary: 3 active, 0 completed, 0 deferred

View full details in .shipkit/user-tasks.json
```

---

## Completion Checklist

Copy and track:
- [ ] Identified manual task for user
- [ ] Created clear step-by-step instructions
- [ ] Added to `.shipkit/user-tasks.json`
- [ ] Summary counts recomputed
- [ ] User confirmed task is clear

---

## What Makes This "Lite"

**Included**:
- Task tracking with statuses (active/in-progress/completed/deferred)
- Priority levels (high/medium/low)
- Structured task entries with verification steps
- Single consolidated JSON file with summary counts
- List tasks on demand

**Not included** (vs full user-instructions):
- Recurring tasks or reminders
- Task dependencies graph
- Time tracking or estimates
- Task assignment to team members
- Integration with external task managers
- Automated task completion detection

**Philosophy**: Simple todo tracking for manual actions. Not a full task management system.

---

## When This Skill Integrates with Others

### Before This Skill

- `/shipkit-integration-docs` - Fetches integration documentation
  - **When**: Preparing to integrate with external services
  - **Why**: May identify missing configuration or manual setup tasks
  - **Trigger**: Integration docs reveal setup steps requiring user action

- `implement (no skill needed)` - Discovers missing dependencies
  - **When**: Implementation needs packages, database setup, external services
  - **Why**: Track installation/setup tasks so they aren't forgotten
  - **Trigger**: Code requires dependency not yet installed

- `/shipkit-project-context` - Identifies environment requirements
  - **When**: Context generation detects missing environment configuration
  - **Why**: Track setup tasks needed before development can proceed
  - **Trigger**: stack.json generation reveals missing env vars or tools

- `verify manually` - Pre-deployment checklist
  - **When**: Quality check reveals manual deploy configuration needed
  - **Why**: Track deployment tasks (DNS, webhooks, secrets) before shipping
  - **Trigger**: Deployment readiness check finds missing configuration

### After This Skill

- `/shipkit-project-status` - Displays active task count
  - **When**: User asks "what's the project status?"
  - **Why**: Show pending user tasks as part of overall project health
  - **Trigger**: Status check reads user-tasks.json summary to count pending tasks

- `/shipkit-work-memory` - Logs task events
  - **When**: Tasks created or completed
  - **Why**: Track task lifecycle in session memory for continuity
  - **Trigger**: Task added or status changed in user-tasks.json

---

## Context Files This Skill Reads

**May read** (to check existing tasks):
- `.shipkit/user-tasks.json` - All tasks (active, completed, deferred)

**Usually starts from scratch** - Doesn't need to read context first.

---

## Context Files This Skill Writes

**Write Strategy: OVERWRITE**

**Creates/Updates**:
- `.shipkit/user-tasks.json` - Structured user tasks (JSON artifact)

**Update Behavior**:
- File doesn't exist → Create with initial schema structure
- File exists → Read, modify tasks array, recompute summary, overwrite entire file
- Each write REPLACES entire file contents
- All task states (active, completed, deferred) live in the same file

**Never modifies**:
- Other `.shipkit/` files (read-only from this skill's perspective)

---

## Lazy Loading Behavior

**This skill is lightweight by default**:

1. User invokes `/shipkit-user-instructions` OR other skill triggers it
2. Claude asks 2-3 questions about task
3. Claude reads/creates `.shipkit/user-tasks.json` and adds entry
4. Total context loaded: ~200-400 tokens (minimal for JSON)

**Only loads more context when**:
- User asks "What tasks do I have?" → Read user-tasks.json
- Updating task status → Read user-tasks.json

**Not loaded unless needed**:
- Specs, plans, implementations
- Other context files
- Session logs

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

Task tracking is complete when:
- [ ] Task entry created in user-tasks.json
- [ ] All required fields present (id, title, description, status, priority, steps, verification, createdAt)
- [ ] Summary counts are accurate
- [ ] Output conforms to JSON schema
- [ ] User understands what needs to be done
- [ ] User knows how to update status
- [ ] Clear verification criteria defined
- [ ] User knows how to mark complete
- [ ] File saved to `.shipkit/user-tasks.json`
<!-- /SECTION:success-criteria -->
---

## JSON Schema (Quick Reference)

```json
{
  "$schema": "shipkit-artifact",
  "type": "user-tasks",
  "version": "1.0",
  "lastUpdated": "YYYY-MM-DD",
  "source": "shipkit-user-instructions",
  "summary": { "total": 0, "byStatus": {...}, "byPriority": {...} },
  "tasks": [{ "id": "...", "title": "...", "status": "...", "priority": "...", "steps": [...], ... }]
}
```

**Full schema and field reference:** See `references/output-schema.md`

**Realistic example:** See `references/example.json`

### Key Fields

| Field | Type | Description |
|-------|------|-------------|
| `tasks[].id` | string | Slug identifier (kebab-case) |
| `tasks[].status` | enum | `"active"`, `"in-progress"`, `"completed"`, `"deferred"` |
| `tasks[].priority` | enum | `"high"`, `"medium"`, `"low"` |
| `tasks[].steps` | string[] | Specific actions the user must take |
| `tasks[].verification` | string[] | How to confirm the task is done |

### Summary Object

The `summary` field MUST be kept in sync with the `tasks` array. Recompute it every time the file is written.

---

## Shipkit Artifact Convention

This skill follows the **Shipkit JSON artifact convention** -- a standard structure for all `.shipkit/*.json` files.

**Required envelope fields:** `$schema`, `type`, `version`, `lastUpdated`, `source`, `summary`

**Full convention details:** See `references/output-schema.md`

---

**Remember**: This skill exists because chat history scrolls away. Tasks don't. Capture them, track them, complete them.