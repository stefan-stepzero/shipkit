# Common Task Tracking Scenarios

Practical examples of how lite-user-instructions works in different situations.

---

## Scenario 1: Missing Environment Variable

```
integration-guardrails-lite detects missing LEMONSQUEEZY_API_KEY

Claude:
1. Invoke /lite-user-instructions
2. Ask: "This blocks payment testing. High priority?"
3. User: "Yes"
4. Create task entry:
   - Title: "Add Lemon Squeezy API Key to .env.local"
   - Priority: 🔴 High
   - Steps: 1. Get key from Lemon Squeezy dashboard, 2. Add to .env.local
   - Verification: File contains LEMONSQUEEZY_API_KEY
5. Suggest: "This blocks progress. I'll wait for completion before continuing."
```

---

## Scenario 2: Package Installation

```
implement-lite realizes @lemonsqueezy/lemonsqueezy.js package needed

Claude:
1. Auto-invoke /lite-user-instructions
2. Create task:
   - Title: "Install Lemon Squeezy SDK"
   - Priority: 🟡 Medium
   - Steps: npm install @lemonsqueezy/lemonsqueezy.js
   - Verification: Package in package.json
3. Suggest: "I can continue with other components while you install this."
```

---

## Scenario 3: User Manually Adds Task

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

---

## Scenario 4: Task Completed

```
User: "I finished setting up the Lemon Squeezy webhook"

Claude:
1. Ask: "Did you verify the webhook secret and API key are in .env.local?"
2. User: "Yes"
3. Read active.md
4. Update task status to ✅ Completed [timestamp]
5. Copy entry to completed.md
6. Remove from active.md
7. Confirm: "✅ Task archived. Ready to continue implementing payment flow?"
```

---

## Scenario 5: Check Active Tasks

```
User: "What do I need to do?"

Claude:
1. Read .shipkit-lite/user-tasks/active.md
2. Parse entries
3. Show summary by priority
4. Suggest tackling high-priority items first
```

---

**See main SKILL.md for task entry template and process steps.**
