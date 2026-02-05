---
name: shipkit-user-instructions
description: "Use when there are manual tasks the user must complete. Triggers: 'create task', 'track TODO', 'user needs to', 'manual step required'."
---

# shipkit-user-instructions - Task Tracking for Manual User Actions

**Purpose**: Prevent manual tasks from being lost in chat by maintaining persistent markdown tracking files for tasks that require user action outside Claude's control.

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
- `.shipkit/user-tasks/` directory (will create if missing)

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

### Step 2: Create Task Entry in active.md

**Use Write tool to append to**: `.shipkit/user-tasks/active.md`

**If file doesn't exist**, create it with header:
```markdown
# Active User Tasks

Tasks that require manual action outside Claude Code's control.

**Status Legend**:
- ⏳ Pending - Not started yet
- 🚧 In Progress - User is working on it
- ✅ Completed - Done (will be moved to completed.md)

---
```

**Then append task entry**:

```markdown
## [YYYY-MM-DD HH:MM] [Task Title]

**Priority**: [🔴 High / 🟡 Medium / 🟢 Low]

**Why needed**:
[1-2 sentence explanation of why this task is necessary]

**Steps**:
1. [Specific action 1]
2. [Specific action 2]
3. [Specific action 3]

**Verification**:
- [ ] [How to verify task is complete]

**Status**: ⏳ Pending

**Related work**:
- Feature: [feature name if applicable]
- Skill: [which skill triggered this, e.g., /shipkit-integration-docs]

---
```

**Example - Lemon Squeezy Webhook Task**:
```markdown
## [2025-01-15 14:30] Configure Lemon Squeezy Webhook

**Priority**: 🔴 High

**Why needed**:
Webhook configuration enables Lemon Squeezy to notify your app of payment events (order_created, subscription_created). Without this, users won't get access after payment.

**Steps**:
1. Go to Lemon Squeezy dashboard → Settings → Webhooks
2. Add webhook URL: `https://your-domain.com/api/webhooks/lemonsqueezy`
3. Select events: `order_created`, `subscription_created`, `subscription_updated`
4. Copy the signing secret
5. Add to `.env.local`: `LEMONSQUEEZY_WEBHOOK_SECRET=...`
6. Add API key: `LEMONSQUEEZY_API_KEY=...`

**Verification**:
- [ ] `.env.local` contains `LEMONSQUEEZY_WEBHOOK_SECRET`
- [ ] `.env.local` contains `LEMONSQUEEZY_API_KEY`
- [ ] Test purchase triggers webhook (use test mode)

**Status**: ⏳ Pending

**Related work**:
- Feature: Payment processing
- Skill: /shipkit-integration-docs

---
```

---

### Step 3: Confirm Task Tracked

**Output to user**:
```
✅ Task tracked in active tasks

📁 Location: .shipkit/user-tasks/active.md

📋 Task: [Task Title]
🔴 Priority: High

Next: Complete the task steps, then tell me "Task [X] done" so I can move it to completed.md

Should I continue with other work, or wait for you to complete this?
```

---

### Step 4: Support Task Status Updates

**When user says**: "I'm working on task X", "Started the Lemon Squeezy setup"

**Action**: Update task status from ⏳ Pending to 🚧 In Progress

**Use Edit tool**:
```markdown
**Status**: 🚧 In Progress
```

**Confirmation**:
```
✅ Updated task status to In Progress

You can continue working. Let me know when it's done!
```

---

### Step 5: Move Completed Tasks

**When user says**: "Task done", "Finished the Lemon Squeezy setup", "Webhook is configured"

**Process**:

1. **Verify completion** (ask user):
   - "Did you complete all verification steps?"
   - "Can you confirm [specific verification]?"

2. **Read active.md** to find the task entry

3. **Update task status** to ✅ Completed with completion timestamp:
```markdown
**Status**: ✅ Completed [2025-01-15 16:45]
```

4. **Copy entire task entry** (with completion timestamp)

5. **Append to completed.md**:
   - Location: `.shipkit/user-tasks/completed.md`
   - If doesn't exist, create with header:
   ```markdown
   # Completed User Tasks

   Tasks that have been finished and verified.

   ---
   ```

6. **Remove task entry from active.md**

7. **Confirm to user**:
```
✅ Task marked complete and archived

📁 Moved from: active.md → completed.md
⏱️  Completed: [timestamp]

Great! Ready to continue with [next step]?
```

---

### Step 6: List Active Tasks (On Demand)

**When user says**: "What tasks do I have?", "Show my todos", "What's pending?"

**Action**:
1. Read `.shipkit/user-tasks/active.md`
2. Parse all task entries
3. Show summary:

```
📋 Active User Tasks

**High Priority (🔴)**:
1. Configure Lemon Squeezy Webhook (⏳ Pending)
2. Set up production database (🚧 In Progress)

**Medium Priority (🟡)**:
1. Install Docker for local development (⏳ Pending)

**Low Priority (🟢)**:
(none)

Total: 3 active tasks

View full details in .shipkit/user-tasks/active.md
```

---

## Completion Checklist

Copy and track:
- [ ] Identified manual task for user
- [ ] Created clear step-by-step instructions
- [ ] Added to `.shipkit/user-tasks/active.md`
- [ ] User confirmed task is clear

---

## What Makes This "Lite"

**Included**:
- ✅ Active task tracking (pending/in-progress/completed)
- ✅ Priority levels (high/medium/low)
- ✅ Structured task entries with verification steps
- ✅ Move completed tasks to archive
- ✅ List active tasks on demand

**Not included** (vs full user-instructions):
- ❌ Recurring tasks or reminders
- ❌ Task dependencies graph
- ❌ Time tracking or estimates
- ❌ Task assignment to team members
- ❌ Integration with external task managers
- ❌ Automated task completion detection

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
  - **Trigger**: stack.md generation reveals missing env vars or tools

- `verify manually` - Pre-deployment checklist
  - **When**: Quality check reveals manual deploy configuration needed
  - **Why**: Track deployment tasks (DNS, webhooks, secrets) before shipping
  - **Trigger**: Deployment readiness check finds missing configuration

### After This Skill

- `/shipkit-project-status` - Displays active task count
  - **When**: User asks "what's the project status?"
  - **Why**: Show pending user tasks as part of overall project health
  - **Trigger**: Status check reads active.md to count pending tasks

- `/shipkit-work-memory` - Logs task events
  - **When**: Tasks created or completed
  - **Why**: Track task lifecycle in session memory for continuity
  - **Trigger**: Task added to active.md or moved to completed.md

---

## Context Files This Skill Reads

**May read** (to check existing tasks):
- `.shipkit/user-tasks/active.md` - Current active tasks
- `.shipkit/user-tasks/completed.md` - Completed task archive

**Usually starts from scratch** - Doesn't need to read context first.

---

## Context Files This Skill Writes

**Creates/Updates**:
- `.shipkit/user-tasks/active.md` - Active task list
  - **Write Strategy**: OVERWRITE AND REPLACE
  - **Why**: Active tasks are mutable state (status changes, removals). Small working set (1-10 tasks). Complete file replacement maintains clean structure.
  - **Implementation**: Read entire file → Modify in memory → Write entire file back

- `.shipkit/user-tasks/completed.md` - Completed task archive
  - **Write Strategy**: APPEND
  - **Why**: Completed tasks are immutable historical records. Never edited or removed. Chronological log of accomplished work.
  - **Implementation**: Read existing content → Append new completed task entry → Write combined content back

**Never modifies**:
- Other `.shipkit/` files (read-only from this skill's perspective)

---

## Lazy Loading Behavior

**This skill is lightweight by default**:

1. User invokes `/shipkit-user-instructions` OR other skill triggers it
2. Claude asks 2-3 questions about task
3. Claude appends to `.shipkit/user-tasks/active.md`
4. Total context loaded: ~100-200 tokens (minimal)

**Only loads more context when**:
- User asks "What tasks do I have?" → Read active.md
- Moving task to completed → Read active.md + completed.md

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
- [ ] Task entry created in active.md
- [ ] All required fields present (title, priority, why, steps, verification, status)
- [ ] User understands what needs to be done
- [ ] User knows how to update status
- [ ] Clear verification criteria defined
- [ ] User knows how to mark complete
<!-- /SECTION:success-criteria -->
---

## Task Entry Template

**Use this exact structure for every task**:

```markdown
## [YYYY-MM-DD HH:MM] [Task Title]

**Priority**: [🔴 High / 🟡 Medium / 🟢 Low]

**Why needed**:
[1-2 sentence explanation]

**Steps**:
1. [Action 1]
2. [Action 2]
3. [Action 3]

**Verification**:
- [ ] [Check 1]
- [ ] [Check 2]

**Status**: [⏳ Pending / 🚧 In Progress / ✅ Completed [timestamp]]

**Related work**:
- Feature: [feature name or "N/A"]
- Skill: [which skill triggered this or "Manual"]

---
```

**All fields are required** - Don't skip any.

---

**Remember**: This skill exists because chat history scrolls away. Tasks don't. Capture them, track them, complete them.