# Tips for Effective Task Tracking

Guidelines for creating clear, actionable task entries.

---

## Be Specific in Steps

**Good:**
- ✅ "Run `stripe listen --forward-to localhost:3000/api/webhooks/stripe`"

**Bad:**
- ❌ "Set up Stripe webhooks"

**Why:** Specificity ensures the user knows exactly what command to run.

---

## Make Verification Concrete

**Good:**
- ✅ "File `.env.local` contains `STRIPE_WEBHOOK_SECRET` starting with `whsec_`"

**Bad:**
- ❌ "Stripe is configured"

**Why:** Concrete verification criteria make it obvious when the task is complete.

---

## Set Priority Honestly

- 🔴 **High** = Blocks current work (must do now)
- 🟡 **Medium** = Needed before deploy/merge (do soon)
- 🟢 **Low** = Future improvement (do later)

**Don't:**
- Mark everything as High
- Under-prioritize blocking tasks

**Do:**
- Be realistic about urgency
- Adjust priority if circumstances change

---

## Keep Tasks Atomic

**One task = One clear outcome**

**Good:**
- "Install Stripe CLI"
- "Configure webhook endpoint"
- "Add webhook secret to .env.local"

**Bad:**
- "Set up Stripe webhooks and configure payments and test everything"

**Why:** If a task has 10+ steps, break into multiple tasks.

---

## Update Status Regularly

**Task lifecycle:**
1. ⏳ **Pending** - Not started yet
2. 🚧 **In Progress** - Currently working on it
3. ✅ **Completed** - Done and verified

**Best practices:**
- Move tasks to "In Progress" when starting
- Don't let tasks stay "Pending" forever
- Archive completed tasks promptly (move to completed.md)
- If blocked, add a new task for the blocker

---

**Remember:** Good task tracking = specific steps + concrete verification + honest priority
