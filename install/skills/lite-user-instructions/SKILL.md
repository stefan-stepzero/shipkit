---
name: lite-user-instructions
description: Tracks manual tasks Claude needs user to complete by maintaining active and completed task lists. Use when Claude detects missing config, needs packages installed, requires external service setup, or any manual action from user.
---

# user-instructions-lite - Task Tracking for Manual User Actions

**Purpose**: Prevent manual tasks from being lost in chat by maintaining persistent markdown tracking files for tasks that require user action outside Claude's control.

---

## When to Invoke

**Auto-trigger scenarios** (other skills invoke this):
- Missing environment variables detected (integration-guardrails-lite)
- Package installation needed (implement-lite)
- External service configuration required (Stripe webhooks, API keys)
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
- `.shipkit-lite/` directory (will create if missing)
- `.shipkit-lite/user-tasks/` directory (will create if missing)

**No hard prerequisites** - This skill can run anytime.

---

## Process

### Step 1: Confirm Task Details

**Before creating task entry**, ask user 2-3 questions:

1. **What specific task needs to be done?**
   - "Install Stripe CLI?"
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

**Use Write tool to append to**: `.shipkit-lite/user-tasks/active.md`

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
- Skill: [which skill triggered this, e.g., /lite-integration-guardrails]

---
```

**Example - Stripe Webhook Task**:
```markdown
## [2025-01-15 14:30] Configure Stripe Webhook Secret

**Priority**: 🔴 High

**Why needed**:
Local webhook testing requires Stripe CLI to forward events to localhost. Without this, payment flow testing will fail.

**Steps**:
1. Install Stripe CLI: `brew install stripe/stripe-cli/stripe` (Mac) or download from stripe.com/docs/stripe-cli
2. Login to Stripe: `stripe login`
3. Forward webhooks: `stripe listen --forward-to localhost:3000/api/webhooks/stripe`
4. Copy the webhook signing secret (starts with `whsec_`)
5. Add to `.env.local`: `STRIPE_WEBHOOK_SECRET=whsec_...`

**Verification**:
- [ ] `.env.local` contains `STRIPE_WEBHOOK_SECRET`
- [ ] `stripe listen` command runs without errors
- [ ] Test payment triggers webhook in terminal

**Status**: ⏳ Pending

**Related work**:
- Feature: Payment processing
- Skill: /lite-integration-guardrails

---
```

---

### Step 3: Confirm Task Tracked

**Output to user**:
```
✅ Task tracked in active tasks

📁 Location: .shipkit-lite/user-tasks/active.md

📋 Task: [Task Title]
🔴 Priority: High

Next: Complete the task steps, then tell me "Task [X] done" so I can move it to completed.md

Should I continue with other work, or wait for you to complete this?
```

---

### Step 4: Support Task Status Updates

**When user says**: "I'm working on task X", "Started the Stripe setup"

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

**When user says**: "Task done", "Finished the Stripe setup", "Webhook is configured"

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
   - Location: `.shipkit-lite/user-tasks/completed.md`
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
1. Read `.shipkit-lite/user-tasks/active.md`
2. Parse all task entries
3. Show summary:

```
📋 Active User Tasks

**High Priority (🔴)**:
1. Configure Stripe Webhook Secret (⏳ Pending)
2. Set up production database (🚧 In Progress)

**Medium Priority (🟡)**:
1. Install Docker for local development (⏳ Pending)

**Low Priority (🟢)**:
(none)

Total: 3 active tasks

View full details in .shipkit-lite/user-tasks/active.md
```

---

### Step 7: Suggest Next Skill

**After creating task**, suggest based on context:

**If task is blocking**:
- "This task is blocking further progress. I'll wait for you to complete it."
- "Once done, we can continue with [previous skill]"

**If task is not blocking**:
- "This task can be done later. Should we continue with [next skill]?"
- Options:
  - Continue with `/lite-implement` if coding
  - Continue with `/lite-plan` if planning
  - Continue with `/lite-quality-confidence` if verifying

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

## Integration with Other Skills

**Triggered by these skills**:
- `/lite-integration-guardrails` - Missing API keys, webhook secrets
- `/lite-implement` - Package installation, database setup
- `/lite-project-context` - Environment variable requirements
- `/lite-quality-confidence` - Deploy configuration, DNS setup

**Can trigger**:
- Nothing (this is a tracking-only skill)

**Used by**:
- `/lite-project-status` - Shows active task count
- `/lite-work-memory` - Logs when tasks created/completed

---

## Context Files This Skill Reads

**May read** (to check existing tasks):
- `.shipkit-lite/user-tasks/active.md` - Current active tasks
- `.shipkit-lite/user-tasks/completed.md` - Completed task archive

**Usually starts from scratch** - Doesn't need to read context first.

---

## Context Files This Skill Writes

**Creates/Updates**:
- `.shipkit-lite/user-tasks/active.md` - Active task list
  - **Write Strategy**: OVERWRITE AND REPLACE
  - **Why**: Active tasks are mutable state (status changes, removals). Small working set (1-10 tasks). Complete file replacement maintains clean structure.
  - **Implementation**: Read entire file → Modify in memory → Write entire file back

- `.shipkit-lite/user-tasks/completed.md` - Completed task archive
  - **Write Strategy**: APPEND
  - **Why**: Completed tasks are immutable historical records. Never edited or removed. Chronological log of accomplished work.
  - **Implementation**: Read existing content → Append new completed task entry → Write combined content back

**Never modifies**:
- Other `.shipkit-lite/` files (read-only from this skill's perspective)

---

## Lazy Loading Behavior

**This skill is lightweight by default**:

1. User invokes `/lite-user-instructions` OR other skill triggers it
2. Claude asks 2-3 questions about task
3. Claude appends to `.shipkit-lite/user-tasks/active.md`
4. Total context loaded: ~100-200 tokens (minimal)

**Only loads more context when**:
- User asks "What tasks do I have?" → Read active.md
- Moving task to completed → Read active.md + completed.md

**Not loaded unless needed**:
- Specs, plans, implementations
- Other context files
- Session logs

---

## Success Criteria

Task tracking is complete when:
- [ ] Task entry created in active.md
- [ ] All required fields present (title, priority, why, steps, verification, status)
- [ ] User understands what needs to be done
- [ ] User knows how to update status
- [ ] Clear verification criteria defined
- [ ] User knows how to mark complete

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

## Common Scenarios

### Scenario 1: Missing Environment Variable

```
integration-guardrails-lite detects missing STRIPE_API_KEY

Claude:
1. Invoke /lite-user-instructions
2. Ask: "This blocks payment testing. High priority?"
3. User: "Yes"
4. Create task entry:
   - Title: "Add Stripe API Key to .env.local"
   - Priority: 🔴 High
   - Steps: 1. Get key from Stripe dashboard, 2. Add to .env.local
   - Verification: File contains STRIPE_API_KEY
5. Suggest: "This blocks progress. I'll wait for completion before continuing."
```

### Scenario 2: Package Installation

```
implement-lite realizes @stripe/stripe-js package needed

Claude:
1. Auto-invoke /lite-user-instructions
2. Create task:
   - Title: "Install Stripe.js package"
   - Priority: 🟡 Medium
   - Steps: npm install @stripe/stripe-js
   - Verification: Package in package.json
3. Suggest: "I can continue with other components while you install this."
```

### Scenario 3: User Manually Adds Task

```
User: "Remind me to configure the domain DNS after we deploy"

Claude:
1. Invoke /lite-user-instructions
2. Ask: "What DNS records need configuring?"
3. User describes
4. Create task:
   - Title: "Configure production DNS records"
   - Priority: 🟢 Low
   - Steps: [DNS setup steps]
   - Verification: Domain resolves to production
5. Confirm: "Tracked for later. Let's continue with [current work]."
```

### Scenario 4: Task Completed

```
User: "I finished setting up the Stripe webhook"

Claude:
1. Ask: "Did you verify the webhook secret is in .env.local and stripe listen works?"
2. User: "Yes"
3. Read active.md
4. Update task status to ✅ Completed [timestamp]
5. Copy entry to completed.md
6. Remove from active.md
7. Confirm: "✅ Task archived. Ready to continue implementing payment flow?"
```

### Scenario 5: Check Active Tasks

```
User: "What do I need to do?"

Claude:
1. Read .shipkit-lite/user-tasks/active.md
2. Parse entries
3. Show summary by priority
4. Suggest tackling high-priority items first
```

---

## Tips for Effective Task Tracking

**Be specific in steps**:
- ✅ "Run `stripe listen --forward-to localhost:3000/api/webhooks/stripe`"
- ❌ "Set up Stripe webhooks"

**Make verification concrete**:
- ✅ "File `.env.local` contains `STRIPE_WEBHOOK_SECRET` starting with `whsec_`"
- ❌ "Stripe is configured"

**Set priority honestly**:
- 🔴 High = Blocks current work
- 🟡 Medium = Needed before deploy/merge
- 🟢 Low = Future improvement

**Keep tasks atomic**:
- One task = One clear outcome
- If task has 10+ steps, break into multiple tasks

**Update status regularly**:
- Move tasks to "In Progress" when starting
- Don't let tasks stay "Pending" forever
- Archive completed tasks promptly

---

## When to Create Tasks vs. Just Telling User

**Create task entry when**:
- Multiple steps involved
- Could be forgotten in chat history
- Needs verification criteria
- User will do it later (not immediately)
- Part of larger workflow that continues after

**Just tell user when**:
- Single obvious action: "Please type 'y' to confirm"
- Immediate response needed: "Which option do you prefer?"
- Conversational clarification: "Should I continue?"

**The rule**: If it's a "todo" not a "respond", track it.

---

## Error Handling

**If `.shipkit-lite/` directory doesn't exist**:
- Create it automatically
- Create `user-tasks/` subdirectory
- Create `active.md` with header
- Proceed with task entry

**If task entry is malformed in active.md**:
- Don't fail silently
- Tell user: "Task entry format is inconsistent. I'll recreate it."
- Rewrite the entry properly

**If user marks task complete but verification fails**:
- Don't move to completed.md
- Update status to: "⚠️ Verification failed"
- Ask user to re-do verification steps

---

**Remember**: This skill exists because chat history scrolls away. Tasks don't. Capture them, track them, complete them.
