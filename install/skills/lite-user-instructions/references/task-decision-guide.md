# When to Create Tasks vs. Just Telling User

Decision guide for whether to create a task entry or just communicate directly.

---

## Create Task Entry When

Use `/lite-user-instructions` to create a tracked task when:

- **Multiple steps involved** - Task requires 2+ distinct actions
- **Could be forgotten in chat history** - Conversation will continue beyond this
- **Needs verification criteria** - Success isn't obvious
- **User will do it later** - Not doing it immediately
- **Part of larger workflow** - Work continues after task completion

**Examples:**
- "Install Stripe CLI, configure webhook endpoint, add secret to .env"
- "Deploy to Vercel after we finish feature X"
- "Configure DNS records after domain purchase"
- "Run database migration when ready"

---

## Just Tell User When

Skip task tracking and communicate directly when:

- **Single obvious action** - "Please type 'y' to confirm"
- **Immediate response needed** - "Which option do you prefer?"
- **Conversational clarification** - "Should I continue?"
- **Quick decision** - "Use TypeScript or JavaScript?"
- **Inline answer** - "What should the button text be?"

**Examples:**
- "Should I create the component in `components/` or `features/`?"
- "Do you want me to continue implementing or wait?"
- "Which API endpoint: `/api/users` or `/api/v1/users`?"

---

## The Rule

**If it's a "todo" → track it**

**If it's a "respond" → just ask**

---

## Edge Cases

**Borderline scenarios:**

| Situation | Decision | Reasoning |
|-----------|----------|-----------|
| "Please confirm before I continue" | Just ask | Immediate response |
| "Please review the PR when ready" | Create task | Will do later, might forget |
| "Which color: blue or green?" | Just ask | Simple choice |
| "Install these 5 packages" | Create task | Multiple steps, verification needed |
| "Does this look right?" | Just ask | Immediate feedback |
| "Test the feature after deploy" | Create task | Future action, verification needed |

---

**Remember:** Chat history scrolls away. Tasks don't. When in doubt, track it.
