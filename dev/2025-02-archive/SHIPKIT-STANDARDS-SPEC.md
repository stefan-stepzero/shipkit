# shipkit-standards Spec

A skill for capturing and enforcing project-specific quality standards.

---

## The Problem

Claude knows many "best practices" but doesn't know YOUR project's standards:

| Claude's Default | Your Project Might Say |
|------------------|------------------------|
| Comprehensive error handling | Happy path only for MVP |
| Full test coverage | Test critical paths only |
| Semantic HTML everywhere | Speed over semantics for internal tool |
| All inputs validated | Trust internal APIs |

**Result:** Claude applies generic best practices when you have specific standards.

---

## The Solution

Capture project-specific standards in `.shipkit/standards.md` that Claude reads before making quality decisions.

### What It Is

- **Human decisions made explicit** — You decide what "quality" means for this project
- **Not a checklist Claude runs** — Context that shapes Claude's behavior
- **Project-scoped** — Different projects have different standards

### What It's NOT

- Not automated linting (that's ESLint's job)
- Not CI/CD checks (that's GitHub Actions)
- Not universal best practices (Claude already knows those)

---

## Output: `.shipkit/standards.md`

```markdown
# Project Standards

Quality standards for this project. Claude should follow these over generic best practices.

---

## Code Quality

### Must Have
- [ ] TypeScript strict mode (no `any` unless commented why)
- [ ] Functions under 50 lines
- [ ] No console.log in committed code (use logger)

### Should Have
- [ ] JSDoc on exported functions
- [ ] Descriptive variable names (no single letters except loops)

### Won't Have (Intentionally)
- Comprehensive error handling — MVP, happy path focus
- 100% type coverage — pragmatic over perfect

---

## Testing

### What We Test
- Business logic (services/)
- API endpoints (integration tests)
- Auth flows (critical path)

### What We Don't Test
- UI components (visual, hard to test)
- Trivial getters/setters
- Third-party library wrappers

### Testing Patterns
- Prefer integration over unit tests
- Use real database (test container), not mocks
- One assertion per test

---

## Frontend

### Accessibility
- Keyboard navigation: Required for primary flows only
- Color contrast: 4.5:1 minimum
- Screen reader: Not required for MVP

### Performance
- Largest Contentful Paint: Under 2.5s
- No performance optimization unless measured problem

### Patterns
- Server components by default
- Client components only for interactivity
- No global state library — use React context

---

## API Design

### Conventions
- RESTful (plural nouns, HTTP verbs)
- JSON responses always have `{ data, error }` shape
- Timestamps in ISO 8601

### Validation
- Validate all external input (user, webhooks)
- Trust internal service calls
- Use Zod schemas

### Errors
- 4xx for client errors (with message)
- 5xx for server errors (generic message, log details)
- No stack traces in production responses

---

## Security

### Must Have
- Input validation on all user-facing endpoints
- Parameterized queries (Prisma handles this)
- Auth middleware on protected routes
- No secrets in code or logs

### For Later (Post-MVP)
- Rate limiting
- CSRF protection
- Security headers

---

## Git & Code Review

### Commits
- Conventional commits (feat:, fix:, etc.)
- Atomic commits (one logical change)
- No WIP commits on main

### What Needs Review
- Nothing — solo dev, no review process

### Branch Strategy
- main: production
- dev: integration
- feature/*: feature work

---

## Documentation

### Required
- README with setup instructions
- API endpoints documented (in code or Postman)

### Not Required
- JSDoc on every function
- Architecture decision records
- Detailed component docs

---

## Performance

### Approach
- Don't optimize prematurely
- Measure before optimizing
- Good enough > perfect

### Acceptable
- N+1 queries in admin pages (low traffic)
- Full page reloads for rare actions
- No caching until needed

---

## Notes

Last updated: 2025-01-27

These standards reflect our MVP priorities:
- Ship fast, iterate on feedback
- Quality where it matters (auth, payments)
- Pragmatic everywhere else
```

---

## User Flow

### Initial Capture

```
User: /standards

Claude: "I'll help you define project standards. This captures YOUR quality
decisions so I follow them instead of generic best practices.

Let me ask about a few areas:

1. **Testing:** What's your testing philosophy?
   - Test everything (TDD)
   - Test critical paths only
   - Minimal testing (MVP speed)
   - No tests yet

2. **Error handling:** How thorough?
   - Comprehensive (handle all edge cases)
   - Pragmatic (happy path + obvious errors)
   - Minimal (let it crash, fix later)

3. **Documentation:** What level?
   - Thorough (JSDoc, README, ADRs)
   - Pragmatic (README + inline comments)
   - Minimal (self-documenting code only)

..."

User: [Answers questions]

Claude: "Based on your answers, here's your standards.md:

[Shows draft]

Should I save this to .shipkit/standards.md?"
```

### Incremental Updates

```
User: "Actually, we decided to use Zod for all validation"

Claude: "I'll add that to your standards. Should I update standards.md?"

User: "Yes"

Claude: [Adds to API Design > Validation section]
```

### Reference During Work

```
User: "Implement the user profile endpoint"

Claude: [Reads standards.md first]
"Based on your project standards:
- I'll validate input with Zod (your validation standard)
- I'll return { data, error } shape (your API convention)
- I won't add comprehensive error handling (MVP focus)
- I'll write an integration test (your testing standard)

[Implements accordingly]"
```

---

## Skill Behavior

### On Invocation (`/standards`)

1. Check if `standards.md` exists
2. If not: Run question flow to create it
3. If yes: Show current standards, offer to update

### Question Categories

| Category | Key Questions |
|----------|--------------|
| **Testing** | What to test? What patterns? Coverage goals? |
| **Code Quality** | Must-haves? Nice-to-haves? Intentional gaps? |
| **Frontend** | Accessibility level? Performance targets? |
| **API** | Conventions? Validation? Error format? |
| **Security** | MVP requirements? Post-MVP items? |
| **Documentation** | Required docs? Skip what? |

### Integration with Other Skills

| Skill | How It Uses Standards |
|-------|----------------------|
| shipkit-plan | Plans reference applicable standards |
| shipkit-spec | Specs note quality requirements |
| shipkit-verify | Checks against standards (if we build it) |
| All implementation | Claude reads standards before coding |

---

## SKILL.md Structure

```markdown
---
name: shipkit-standards
description: Capture project-specific quality standards
---

# Project Standards

Define YOUR project's quality standards so Claude follows them instead of
generic best practices.

## Activation

- `/standards` or `/shipkit-standards`
- "Define our project standards"
- "What are our coding standards?"

## Behavior

### First Run (No standards.md)
1. Ask questions about testing, code quality, frontend, API, security, docs
2. Generate standards.md from answers
3. Save to .shipkit/standards.md

### Subsequent Runs (standards.md exists)
1. Show current standards
2. Ask if user wants to update any section
3. Update specific sections as needed

### During Development
Claude should read standards.md before:
- Implementing features
- Writing tests
- Making architectural decisions
- Reviewing code

## Output Location
`.shipkit/standards.md`

## Key Principle

Standards capture HUMAN DECISIONS about quality trade-offs.
They're not "what's best" — they're "what's right for THIS project."

Examples of valid standards:
- "No tests for UI components" (intentional trade-off)
- "Happy path only" (MVP speed)
- "Trust internal APIs" (pragmatic)

These override Claude's defaults.
```

---

## What Standards Should NOT Include

| Don't Include | Why | Where It Belongs |
|---------------|-----|------------------|
| Linting rules | ESLint handles this | `.eslintrc` |
| Formatting | Prettier handles this | `.prettierrc` |
| Type checking | TypeScript handles this | `tsconfig.json` |
| Generic best practices | Claude already knows | Training |
| Step-by-step procedures | Too prescriptive | Skills or docs |

**Standards = decisions and trade-offs, not rules that tools enforce.**

---

## Relationship to Other Context Files

| File | What It Captures | Overlap |
|------|------------------|---------|
| `why.md` | Project purpose, constraints | Standards reflect constraints |
| `architecture.md` | Technical decisions | Standards are quality decisions |
| `preferences.md` | User's working style | Standards are project quality |
| `stack.md` | Technology choices | Standards may be tech-specific |

**Standards.md is about QUALITY decisions, not architecture or preferences.**

---

## Open Questions

1. **How detailed should sections be?**
   - Too sparse: Claude still guesses
   - Too detailed: Becomes prescriptive checklist

2. **Should standards evolve automatically?**
   - Claude notices a pattern and suggests addition?
   - Only on explicit user update?

3. **Section organization?**
   - By concern (testing, security, etc.)
   - By importance (must/should/won't)
   - Both?

4. **How to handle conflicts?**
   - Standards says "no tests for UI"
   - User asks "write tests for this component"
   - Follow user's immediate request, or reference standards?

---

## Implementation Checklist

- [ ] Create SKILL.md with question flow
- [ ] Define standards.md template
- [ ] Add to shipkit-project-context loading
- [ ] Add to CLAUDE.md ("read standards before implementing")
- [ ] Integrate with 7-file system
- [ ] Test question flow covers key areas
