---
name: constitution-builder
description: "Build project constitution. Called after /strategic-thinking (product) and before /specify (technical)."
scripts:
  sh: scripts/bash/build-constitution.sh --json --phase "{PHASE}"
  ps: scripts/powershell/build-constitution.ps1 -Json -Phase "{PHASE}"
---

# Constitution Builder

## Overview

Builds project constitution at two key points:

```
/strategic-thinking
        ↓
/constitution-builder --product   ← After strategy defined
        ↓
... rest of ProdKit ...
        ↓
/constitution-builder --technical ← Before /specify
        ↓
/specify → /plan → /tasks → /implement
```

## When Called

| Phase | Trigger | Creates |
|-------|---------|---------|
| `--product` | After `/strategic-thinking` | Product principles, brand, UX rules |
| `--technical` | Before `/specify` (or after `/plan`) | Tech stack, architecture, code rules |

## Phase 1: Product Constitution

**Trigger:** `/strategic-thinking` completes → suggest `/constitution-builder --product`

**Reads from:**
- `.prodkit/strategy/business-canvas.md` (if exists)
- Conversation context from strategic-thinking

### Product Interview

**Q1: Project Type**
```
What are you building?

A) SaaS product (multi-tenant, subscription)
B) Consumer app (single user focus)
C) Internal tool (business users)
D) Open source library
E) Prototype/MVP
```

**Q2: Brand Voice**
```
How should user-facing content sound?

A) Professional and formal
B) Friendly and conversational
C) Technical and precise
D) Playful and casual
```

**Q3: UX Principles** (select all that apply)
```
Which UX rules are non-negotiable?

- [ ] Destructive actions require confirmation
- [ ] Forms show inline validation
- [ ] Loading states for actions >200ms
- [ ] Error messages suggest resolution
- [ ] Mobile-first responsive design
- [ ] Keyboard navigation support
- [ ] Dark mode support
```

**Q4: Accessibility**
```
Accessibility requirements?

A) WCAG 2.1 AA (standard)
B) WCAG 2.1 AAA (strict)
C) Basic (semantic HTML, alt text)
D) None (prototype)
```

### Product Constitution Output

Run script: `{SCRIPT}` with `--phase product`

Creates/updates `.claude/constitution.md`:

```markdown
# Project Constitution

## Product Principles

### Project Type
[SaaS/Consumer/Internal/Library/MVP]

### Brand Voice
- Tone: [Professional/Friendly/Technical/Playful]
- Error messages must be [helpful and suggest resolution]
- [Additional brand rules]

### UX Requirements
- [ ] Destructive actions require confirmation
- [ ] Forms show inline validation before submit
- [ ] Loading states required for actions >200ms
- [Other selected rules]

### Accessibility
- Standard: [WCAG level]
- All images must have alt text
- All forms must have labels

---
*Product constitution created: [DATE]*
*Technical section pending: Run /constitution-builder --technical*
```

---

## Phase 2: Technical Constitution

**Trigger:** Before `/specify` OR after `/plan` completes

**Reads from:**
- `.claude/constitution.md` (product section)
- `.devkit/specs/XXX/plan.md` (if exists)
- Conversation context

### Technical Interview

**Q1: Team Size**
```
Who's building this?

A) Solo developer + AI
B) Small team (2-5) + AI
C) Larger team (5+) + AI
```

**Q2: Tech Stack** (confirm from plan.md or ask)
```
Confirm your tech stack:

Frontend: [React/Vue/Svelte/None]
Backend: [Node/Python/Go/None]
Database: [PostgreSQL/MySQL/MongoDB/SQLite]
Hosting: [Vercel/Railway/AWS/Self-hosted]
```

**Q3: Architecture Constraints**
```
Key architectural decisions:

Authentication:
A) Custom (JWT + passwords)
B) Third-party (Clerk/Auth0/Supabase)
C) Framework (NextAuth/etc)
D) None yet

API Style:
A) REST
B) GraphQL
C) tRPC
D) Mix
```

**Q4: Code Quality**
```
Testing requirements:

A) TDD required (tests before code)
B) Tests required (can write after)
C) Tests for critical paths only
D) No tests (prototype)

Coverage target:
A) >80%
B) >60%
C) No target
```

**Q5: File Organization**
```
Code organization:

A) Feature-based (co-locate related files)
B) Type-based (all models together)
C) Framework conventions
```

**Q6: AI Agent Rules**
```
How should AI agents work?

Dependencies:
A) Minimize (prefer stdlib)
B) Use established libraries
C) Ask before adding

File creation:
A) Create new files for features
B) Edit existing when extending
C) Agent decides
```

### Technical Constitution Output

Run script: `{SCRIPT}` with `--phase technical`

Updates `.claude/constitution.md`:

```markdown
# Project Constitution

## Product Principles
[Existing product section]

---

## Technical Standards

### Team & Process
- Team size: [Solo/Small/Large]
- AI agents: [Enabled/Limited]

### Tech Stack
- Frontend: [X]
- Backend: [X]
- Database: [X]
- Hosting: [X]

### Architecture
- Authentication: [approach]
- API style: [REST/GraphQL/tRPC]
- [Other constraints]

### Code Quality
- Testing: [TDD/Required/Critical-only/None]
- Coverage: [target]
- Functions must be <50 lines
- Files must be <300 lines

### File Organization
- Pattern: [Feature/Type/Framework]
- [Specific rules]

### AI Agent Rules
- Dependencies: [policy]
- File creation: [policy]
- Always run tests before marking done
- Never commit secrets

---
*Technical constitution added: [DATE]*
*Full constitution ready for /specify*
```

---

## Script Interface

```bash
# Product phase
scripts/bash/build-constitution.sh --json --phase product

# Technical phase
scripts/bash/build-constitution.sh --json --phase technical

# Output
{
  "constitution_file": ".claude/constitution.md",
  "phase": "product|technical",
  "created": "2024-12-21",
  "status": "created|updated"
}
```

---

## Integration with Workflow

**After strategic-thinking:**
```
✅ Strategy complete.

📁 Created: .prodkit/strategy/business-canvas.md

👉 **Next step:** `/constitution-builder --product` - Define product principles

Would you like to build the product constitution now?
```

**Before specify:**
```
Before creating the spec, let's complete the constitution.

👉 Running `/constitution-builder --technical` to define technical standards...
```

---

## The Key Rule

**Constitutions must be TESTABLE.**

| Bad | Good |
|-----|------|
| "Write clean code" | "Functions <50 lines" |
| "Be secure" | "Validate all input with Zod" |
| "Good UX" | "Loading state if >200ms" |

If you can't fail a code review for violating it, it doesn't belong.
