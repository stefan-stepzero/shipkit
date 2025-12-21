---
name: brainstorming
description: "Use ANY TIME ambiguity is detected - vague requirements, multiple approaches, or unclear decisions. Can interrupt any skill."
---

# Brainstorming

## Agent Personas

**Load:** `.claude/agents/discovery-agent.md`

Adopt: Curious, asks why, challenges assumptions, explores alternatives, user-centric.

**For deep research:** Also load `.claude/agents/researcher-agent.md` - systematic research, cross-reference sources.

## Overview

Conversational discovery that can be triggered **at any point** when ambiguity is detected. Not just a first step - use it whenever you hit uncertainty.

```
Can interrupt any skill:
  /specify → unclear requirement? → /brainstorming → resume /specify
  /plan → multiple approaches? → /brainstorming → resume /plan
  /implement → vague task? → /brainstorming → resume /implement
```

## Detection Triggers

**Invoke `/brainstorming` when you detect:**

| Trigger | Example |
|---------|---------|
| Vague requirement | "Add authentication" (what kind?) |
| Multiple valid approaches | REST vs GraphQL, SQL vs NoSQL |
| Missing information | No error handling specified |
| User uncertainty | "I'm not sure", "what do you think?" |
| Ambiguous scope | "Make it fast" (how fast? what metric?) |
| Conflicting requirements | Security vs convenience trade-off |
| Technical decision needed | Which library? What pattern? |

**Red flags in requirements:**
- "etc.", "and so on", "similar things"
- "appropriate", "suitable", "as needed"
- "fast", "secure", "scalable" (without metrics)
- Missing edge cases or error handling
- No success criteria defined

## How to Invoke Mid-Skill

When you detect ambiguity during another skill:

```
I'm pausing /specify because I've hit an ambiguity:

[State the specific unclear point]

Let me explore this with you before continuing.

---

[Run brainstorming process]

---

✅ Clarified. Resuming /specify with:
- [Decision made]
- [Approach chosen]
```

## The Process

### 1. State the Ambiguity
Be specific about what's unclear:
```
"The spec says 'add user authentication' but doesn't specify:
- Authentication method (password, OAuth, magic link?)
- Session handling (JWT, cookies, both?)
- Password requirements (if applicable)"
```

### 2. Ask One Question at a Time
- One question per message
- Prefer multiple choice when possible
- Focus on: purpose, users, constraints, trade-offs

**Example:**
```
What type of authentication fits your users best?

A) Email/password (simple, you manage credentials)
B) OAuth only (Google, GitHub - no password management)
C) Magic links (passwordless, email-based)
D) Multiple options (let users choose)

Which direction?
```

### 3. Explore Trade-offs
When there are multiple valid approaches:
- Present 2-3 options with pros/cons
- Lead with your recommendation
- Explain why you recommend it

### 4. Confirm Understanding
Before resuming the interrupted skill:
```
Let me confirm what we decided:

- Authentication: OAuth (Google + GitHub)
- Session: JWT with 24h expiry
- No password management needed

Does this capture it correctly?
```

### 5. Resume Original Skill
```
✅ Clarified. Resuming /specify.

Incorporating:
- OAuth authentication (Google, GitHub)
- JWT sessions, 24h expiry
- No password flows needed
```

## When to Use

**Use `/brainstorming` when:**
- Starting with a vague idea (before /specify)
- Mid-/specify when requirements are unclear
- Mid-/plan when technical approach is uncertain
- Mid-/tasks when task scope is ambiguous
- Mid-/implement when implementation details are vague
- Any time user says "I'm not sure" or "what do you think"

**Don't interrupt for:**
- Minor details that have reasonable defaults
- Choices that don't significantly impact the outcome
- Things you can reasonably infer from context

## Key Principles

- **One question at a time** - Don't overwhelm
- **Multiple choice preferred** - Easier to answer
- **State the ambiguity clearly** - User should understand why you're asking
- **Minimal interruption** - Get clarity, resume quickly
- **YAGNI** - Cut unnecessary features during exploration

## Output

Brainstorming produces:
- Shared understanding of the unclear point
- Decision documented in conversation
- Ready to resume the interrupted skill

**No files created** - the conversation IS the output. The calling skill incorporates the decisions.
