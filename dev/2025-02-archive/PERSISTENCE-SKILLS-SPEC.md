# Persistence Skills Spec

Three new skills addressing true memory gaps in AI-assisted development.

---

## Overview

| Skill | Purpose | Output File | Trigger |
|-------|---------|-------------|---------|
| **shipkit-preferences** | Capture user working style | `preferences.md` | User request, or after repeated corrections |
| **shipkit-learnings** | Persist corrections & discoveries | `learnings.md` | After user correction, or project-specific discovery |
| **shipkit-codebase-index** | Project map to avoid exploration | `codebase-index.md` | Session start, after structure changes |

### Why These Three?

All three address **true capability gaps** (Claude cannot persist memory between sessions), not discipline gaps. They pass the Skill Value Test:

| Skill | Creates persistence Claude lacks? | Forces human decisions explicit? |
|-------|-----------------------------------|----------------------------------|
| shipkit-preferences | ✅ Working style survives sessions | ✅ User must articulate preferences |
| shipkit-learnings | ✅ Corrections survive sessions | - |
| shipkit-codebase-index | ✅ Project structure survives sessions | - |

---

## 1. shipkit-preferences

### Purpose

Capture user's working style preferences so Claude doesn't re-learn them every session.

### Problem It Solves

```
Session 1: "Be more concise" → Claude adjusts
Session 2: Claude is verbose again → "I said be concise"
Session 3: Claude is verbose again → User frustrated
```

### Output: `.shipkit/preferences.md`

```markdown
# Working Preferences

How I like to work with Claude on this project.

## Communication Style

- **Verbosity:** Concise - skip explanations unless I ask
- **Confirmations:** Don't ask for confirmation on small changes
- **Questions:** Ask upfront if requirements are unclear, not mid-task

## Code Style

- **Indentation:** 2 spaces
- **Quotes:** Single quotes
- **Semicolons:** No (rely on ASI)
- **Naming:** camelCase functions, PascalCase components
- **Comments:** Only for non-obvious logic

## Git & Commits

- **Commit style:** Conventional commits (feat:, fix:, etc.)
- **Commit scope:** Group related changes, not file-by-file
- **Branch naming:** feature/description, fix/description

## Testing Approach

- **When to test:** New business logic, bug fixes
- **Skip tests for:** Trivial getters, UI tweaks, prototypes
- **Test style:** Integration over unit where possible

## Working Style

- **Ask vs assume:** Assume for small decisions, ask for architectural
- **Scope creep:** Stay focused on what I asked, don't add extras
- **Refactoring:** Only if I ask, don't "improve" surrounding code
```

### User Flow

**Initial capture (explicit):**
```
User: /preferences

Claude: "I'll help capture your working preferences. Let me ask a few questions:

1. **Communication:** How verbose should I be?
   - Detailed explanations
   - Concise, skip explanations
   - Minimal, just code

2. **Confirmation:** When should I ask before acting?
   - Always confirm changes
   - Only for destructive/large changes
   - Just do it, I'll correct if needed

3. **Code style:** Do you have specific conventions?
   [If yes, asks follow-ups]

..."

→ Creates preferences.md from answers
```

**Incremental capture (implicit):**
```
User: "Be more concise, you don't need to explain everything"

Claude: "Got it, I'll be more concise. Should I save this preference for future sessions?"

User: "Yes"

Claude: [Updates preferences.md with: Verbosity: Concise]
```

### Skill Behavior

1. **On invocation:** Ask structured questions, create preferences.md
2. **On correction:** Offer to persist the correction
3. **On session start:** Read preferences.md, apply to responses

### Integration Points

- **shipkit-session-start hook:** Load preferences.md into context
- **CLAUDE.md:** Reference preferences.md for working style
- **Other skills:** Respect preferences (e.g., shipkit-plan uses preferred commit style)

---

## 2. shipkit-learnings

### Purpose

Persist corrections and project-specific discoveries so Claude doesn't repeat mistakes.

### Problem It Solves

```
Session 1: "Don't use moment.js, use date-fns" → Claude switches
Session 2: Claude suggests moment.js again → User corrects again
Session 3: Same mistake → User very frustrated
```

### Output: `.shipkit/learnings.md`

```markdown
# Project Learnings

Corrections and discoveries that should persist across sessions.

---

## Corrections

Things I got wrong that I shouldn't repeat.

### 2025-01-23

- **Don't use moment.js** → Use date-fns instead (moment is deprecated, larger bundle)
- **API response format:** Returns `{ data: [] }` not `{ results: [] }`
- **Auth middleware order:** Must come BEFORE rate limiter, not after

### 2025-01-20

- **Don't refactor utils/** → It's intentionally simple, leave it alone
- **Test file location:** Use `__tests__/` folder, not `.test.ts` suffix

---

## Project-Specific Knowledge

Things that aren't obvious from the code.

### Architecture

- **Why no ORM:** Team decided raw SQL for performance, don't suggest Prisma
- **Monorepo structure:** packages/ are internal only, don't publish to npm

### Gotchas

- **CI takes 10+ min:** Don't suggest "just run CI" for quick checks
- **Staging env:** Often out of sync, don't trust it for testing

### Conventions

- **Feature flags:** All new features behind flags in `config/features.ts`
- **Error codes:** Use ERROR_CODES enum, don't create new string errors
```

### User Flow

**After correction:**
```
User: "No, our API returns { data: items } not { items: [] }"

Claude: "Thanks for the correction. I'll use { data: items } for the API response format.

Should I save this to learnings so I remember next session?"

User: "Yes"

Claude: [Adds to learnings.md under today's date]
"Added to learnings.md. I won't make this mistake again."
```

**Explicit capture:**
```
User: /learning "We tried Redis caching before, it caused more problems than it solved due to invalidation complexity"

Claude: [Adds to learnings.md under Project-Specific Knowledge]
"Got it. I've recorded this so I won't suggest Redis caching for this project."
```

**Proactive discovery:**
```
Claude: [While exploring code, finds unusual pattern]
"I notice you're using a custom date formatter instead of a library. Is this intentional? If so, I can add this to learnings so I don't suggest date-fns."

User: "Yes, we need specific timezone handling the libraries don't support well"

Claude: [Adds to learnings.md]
```

### Skill Behavior

1. **After user correction:** Offer to persist (don't auto-save without asking)
2. **On explicit /learning:** Add directly to file
3. **On discovery:** Ask if it should be persisted
4. **On session start:** Read learnings.md, apply to suggestions

### Integration Points

- **shipkit-session-start hook:** Load learnings.md into context
- **CLAUDE.md:** "Check learnings.md before suggesting libraries/patterns"
- **Error recovery:** When Claude makes a mistake, prompt "Should I add this to learnings?"

### What NOT to Capture

- Temporary issues ("the server is down")
- One-time fixes ("fixed the typo")
- General programming knowledge (Claude already knows)

Only capture **project-specific** corrections that would recur.

---

## 3. shipkit-codebase-index

### Purpose

Generate a project map so Claude doesn't waste tokens re-exploring every session.

### Problem It Solves

```
Every session:
Claude: "Let me explore the project structure..."
→ Glob **/*.ts (lists 200 files)
→ Read file1.ts (500 lines, not relevant)
→ Read file2.ts (300 lines, not relevant)
→ Read file3.ts (finally found it)
= 1000s of tokens wasted, repeated every conversation
```

### Output: `.shipkit/codebase-index.md`

```markdown
# Codebase Index

Quick reference for project structure. Read this before exploring files.

Last updated: 2025-01-23

---

## Quick Reference

| What | Where |
|------|-------|
| Entry point | `src/index.ts` |
| API routes | `src/api/routes/` |
| Database | `src/db/` (Prisma) |
| Config | `config/` |
| Tests | `tests/` (Vitest) |

---

## Scripts

| Command | Purpose |
|---------|---------|
| `npm run dev` | Start dev server (port 3000) |
| `npm run build` | Production build |
| `npm run test` | Run tests |
| `npm run lint` | ESLint check |
| `npm run db:migrate` | Run migrations |

---

## Directory Structure

```
src/
├── index.ts          # App entry, server setup
├── api/
│   ├── routes/       # Route handlers by domain
│   │   ├── auth.ts      # /auth/* endpoints
│   │   ├── users.ts     # /users/* endpoints
│   │   └── posts.ts     # /posts/* endpoints
│   └── middleware/   # Express middleware
│       ├── auth.ts      # JWT verification
│       └── validate.ts  # Request validation
├── db/
│   ├── schema.prisma # Database schema
│   ├── client.ts     # Prisma client instance
│   └── migrations/   # Migration files
├── services/         # Business logic
│   ├── auth.ts       # Auth logic (JWT, passwords)
│   └── email.ts      # Email sending
└── utils/            # Shared utilities
    ├── errors.ts     # Custom error classes
    └── logger.ts     # Logging setup

config/               # Environment configs
tests/                # Test files (mirrors src/)
scripts/              # Build/deploy scripts
```

---

## Key Files

| File | Purpose | Key Exports |
|------|---------|-------------|
| `src/index.ts` | App entry | `app`, `startServer()` |
| `src/api/routes/auth.ts` | Auth endpoints | `authRouter` |
| `src/db/client.ts` | DB connection | `prisma` |
| `src/services/auth.ts` | Auth logic | `hashPassword()`, `verifyToken()` |
| `src/utils/errors.ts` | Error handling | `AppError`, `NotFoundError` |

---

## Architecture Notes

- **API pattern:** REST, Express routers grouped by domain
- **Auth:** JWT tokens, refresh tokens in httpOnly cookies
- **Database:** PostgreSQL via Prisma ORM
- **Validation:** Zod schemas in `src/api/validators/`
- **Error handling:** Centralized in `src/middleware/errorHandler.ts`
```

### User Flow

**Explicit generation:**
```
User: /codebase-index

Claude: "I'll analyze the project structure and create an index.

[Reads package.json, explores key directories, identifies patterns]

Created .shipkit/codebase-index.md with:
- 12 key files documented
- 8 npm scripts listed
- Directory structure mapped
- Architecture notes captured

This will save exploration time in future sessions."
```

**Auto-suggestion (session start):**
```
[Session starts, no codebase-index.md exists]

Claude: "I notice there's no codebase index yet. Would you like me to create one? This will help me navigate the project faster in future sessions."
```

**Update after changes:**
```
User: "I just restructured the api/ folder"

Claude: "Should I update the codebase index to reflect the new structure?"
```

### Generation Approach

**What to include:**
1. **package.json scripts** — Parse and list with descriptions
2. **Entry points** — Find main, bin entries
3. **Directory structure** — 2-3 levels deep, with purpose annotations
4. **Key files** — Files with many imports, entry points, configs
5. **Architecture notes** — Patterns observed (REST, GraphQL, monorepo, etc.)

**What to skip:**
- Generated files (dist/, .next/, node_modules/)
- Test files (list folder, not individual files)
- Assets (images, fonts)
- Lock files

**Heuristics for "key files":**
- Entry points (index.ts, main.ts, app.ts)
- Most imported files
- Config files (*.config.ts)
- Schema files (schema.prisma, schema.graphql)
- Route definitions

### Skill Behavior

1. **On invocation:** Analyze project, generate index
2. **On session start (hook):** Check for index, suggest creation if missing
3. **After structural changes:** Offer to update index
4. **Always:** Read index before exploring (instruction in CLAUDE.md)

### Integration Points

- **shipkit-session-start hook:**
  ```python
  if not exists('.shipkit/codebase-index.md'):
      print("TIP: Run /codebase-index to create a project map")
  ```
- **CLAUDE.md:** "Always read codebase-index.md before exploring files"
- **shipkit-project-context:** Include codebase-index in context loading

### Token Savings Estimate

| Task | Without Index | With Index | Savings |
|------|---------------|------------|---------|
| "What scripts are available?" | ~2000 tokens | ~300 tokens | 85% |
| "Where is auth handled?" | ~5000 tokens | ~500 tokens | 90% |
| "Understand project structure" | ~10000 tokens | ~300 tokens | 97% |

---

## Implementation Order

### Phase 1: shipkit-codebase-index (Highest ROI)

1. Create skill that generates index from project analysis
2. Add "read index first" instruction to CLAUDE.md
3. Add hook to suggest index creation on session start

**Why first:** Immediate token savings every session. Already designed in detail.

### Phase 2: shipkit-preferences

1. Create skill with question flow
2. Create preferences.md template
3. Add "apply preferences" instruction to CLAUDE.md
4. Add "offer to save preference" pattern to correction handling

**Why second:** High impact on user experience. Reduces repeated corrections.

### Phase 3: shipkit-learnings

1. Create skill for explicit learning capture
2. Create learnings.md template
3. Add "offer to persist correction" pattern
4. Add "check learnings before suggesting" instruction

**Why third:** Requires pattern change in how Claude responds to corrections. More nuanced.

---

## File Locations

All outputs go in `.shipkit/`:

```
.shipkit/
├── why.md              # (existing) Project purpose
├── stack.md            # (existing) Technology choices
├── architecture.md     # (existing) Architecture decisions
├── project-status.md   # (existing) Current phase
├── preferences.md      # (NEW) User working style
├── learnings.md        # (NEW) Corrections & discoveries
└── codebase-index.md   # (NEW) Project structure map
```

---

## Success Metrics

| Skill | Success Indicator |
|-------|-------------------|
| shipkit-codebase-index | Reduced "let me explore" messages, faster task starts |
| shipkit-preferences | Fewer repeated style corrections from user |
| shipkit-learnings | Fewer repeated mistakes, user stops saying "I told you before" |

---

## Open Questions

1. **Auto-update codebase-index?**
   - On every session start? (might be stale)
   - Only when user asks? (simpler)
   - Detect structural changes? (complex)

2. **Learnings scope?**
   - Project-specific only? (cleaner)
   - User-wide learnings across projects? (more value, more complex)

3. **Preferences inheritance?**
   - User-global preferences + project overrides?
   - Project-only? (simpler)

4. **Skill invocation or auto-trigger?**
   - Explicit /command only?
   - Auto-suggest when relevant?
   - Both?

---

## Related Documents

- `CODEBASE-INDEX-DESIGN.md` — Detailed design for codebase index
- `CONTEXT-GAPS-INVENTORY.md` — Analysis that identified these gaps
- `SKILL-ECOSYSTEM-REDESIGN.md` — External skills loading approach
