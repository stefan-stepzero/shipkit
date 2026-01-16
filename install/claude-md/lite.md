# Shipkit Lite - Project Instructions

**You are working with Shipkit Lite** - a framework for shipping production-ready MVPs for SaaS applications.

**Context:** Solo developer or tiny team. AI-assisted development (you + human). Ship fast, iterate on real feedback.

---

## The Shipkit Mindset

### MVP ≠ Low Quality

**Production-ready MVP means:**
- ✅ Core user paths work flawlessly
- ✅ Authentication and authorization are solid
- ✅ Payment flows are bulletproof (money is involved)
- ✅ Errors are handled gracefully for users
- ✅ Basic security (input validation, SQL injection prevention, CSRF)

**MVP means we skip:**
- ❌ Comprehensive test coverage (test critical paths only)
- ❌ Edge cases for non-critical features
- ❌ Performance optimization beyond basics
- ❌ Features users haven't asked for yet

**The rule:** Core paths bulletproof. Everything else minimal.

---

### Context Over Defaults

**You have implicit defaults from training. This project has explicit context.**

Before making architectural decisions, **always check:**
1. `.shipkit-lite/why.md` - Project scope, constraints, approach
2. `.shipkit-lite/architecture.md` - Decisions already made
3. `.shipkit-lite/stack.md` - Technology choices

**If context exists → follow it, even if different from "best practice"**
**If context is missing → ask, don't assume**

Example:
- Your default: Modular architecture, comprehensive error handling
- Project context (why.md): "MVP in 2 weeks, solo dev"
- Your behavior: Simple structure, error handling for critical paths only

---

### Solo Dev Patterns (Not Team Patterns)

**Skip team ceremony:**
- ❌ Don't suggest PR workflows (no team to review)
- ❌ Don't create documentation for "other developers" (there are none)
- ❌ Don't add abstraction layers for "future flexibility"
- ❌ Don't suggest code review processes

**Do solo-appropriate things:**
- ✅ Self-documenting code (clear names, obvious structure)
- ✅ Inline comments for "why", not "what"
- ✅ Minimal abstractions (duplicate code is fine if it's clearer)
- ✅ Direct solutions over flexible ones

---

### AI-First Code Patterns

**The next developer is also an AI (future Claude sessions). Optimize for:**

| Do This | Not This |
|---------|----------|
| One concept per file | Multiple concerns interleaved |
| Explicit imports | Barrel files or re-exports |
| "Why" comments | "What" comments (code shows what) |
| Flat structures | Deep nesting |
| Obvious patterns | Clever abstractions |
| Self-contained functions | Functions requiring full codebase context |

**Why:** Each session starts fresh. Code should be understandable without remembering the whole project.

---

### Modular by Default (Parallel-Agent Friendly)

**Small files with clear contracts enable parallel AI work.**

**Structure for AI collaboration:**
```
feature/
  types.ts        # Contracts first (inputs, outputs, shared types)
  [name].ts       # Implementation (imports from types.ts)
  [name].test.ts  # Tests (optional, critical paths only)
```

**Rules:**
| Rule | Why |
|------|-----|
| **< 200 lines per file** | Fits in context window, easy to reason about |
| **Types/interfaces at boundaries** | Clear contracts between modules |
| **No circular dependencies** | Each file can be worked on in isolation |
| **Explicit exports** | Know exactly what a module provides |
| **Colocate related code** | Feature folder > scattered files |

**Parallel agent benefit:**
- Agent A works on `auth/` module
- Agent B works on `billing/` module
- No conflicts because contracts are defined upfront
- Each agent only needs to load its module + shared types

**Contract-first development:**
```typescript
// 1. Define the contract (types.ts)
export interface CreateUserInput { email: string; name: string }
export interface CreateUserOutput { id: string; createdAt: Date }

// 2. Implement against contract ([name].ts)
export async function createUser(input: CreateUserInput): Promise<CreateUserOutput> {
  // Implementation here
}
```

**Why contracts matter for AI:**
- Clear inputs/outputs = less guessing
- TypeScript catches mismatches
- Other modules can be built against contracts before implementation exists

---

### SaaS Defaults

**For SaaS MVPs, always consider:**

| Concern | Default Approach |
|---------|------------------|
| Multi-tenancy | User ID on every table from day 1 |
| Auth | Supabase Auth + RLS policies |
| Payments | Lemon Squeezy webhooks (they handle tax) |
| Onboarding | First-run experience matters for conversion |
| Errors | Log to console + user-friendly messages |
| Analytics | Basic events from day 1 (sign up, purchase, key actions) |

---

### Shipping > Perfecting

**Launch with known limitations:**
- Document what's not done in `progress.md`
- "Good enough" beats "not shipped"
- Real user feedback > hypothetical requirements
- Technical debt is fine if consciously chosen

**Stop refining when:**
- Core feature works
- User can complete their goal
- Code is readable (not perfect)

---

## Why Skills Exist

**You are trained on human coding patterns, but you operate under different constraints.**

| You (Claude) | Human Coder |
|--------------|-------------|
| No memory between sessions | Remembers yesterday |
| Context-limited | Knows entire project history |
| Each session starts fresh | Picks up where they left off |
| Doesn't know what skills exist | Knows their own tools |

**Shipkit Lite skills compensate for these AI-specific limitations:**
- They create **persistence** you don't naturally have
- They capture **human decisions** you can't make
- They provide **discoverability** so you know what's available

**Without these skills, you'll code like someone with memory - but you don't have memory.**

---

## Critical Rules

1. **ALL context lives in `.shipkit-lite/`** - Never create context files outside this folder
2. **Skills capture decisions or create persistence** - Don't invoke skills for things you can do naturally
3. **Ask before generating** - 2-3 questions, then generate
4. **Load context lazily** - Only read files when needed
5. **Check for existing context first** - You don't "just know" what exists; check `.shipkit-lite/`

---

## File Structure

```
.shipkit-lite/
  why.md                # Strategic vision (human decisions)
  stack.md              # Tech stack (auto-scanned)
  architecture.md       # Decisions log (append-only)
  types.md              # TypeScript types
  progress.md           # Session continuity (work memory)
  specs/
    active/             # Pending feature specs
    implemented/        # Completed feature specs
  plans/
    active/             # Pending implementation plans
    implemented/        # Completed implementation plans
  .queues/              # Auto-generated work queues
```

---

## Available Skills

### Vision & Discovery (Human Decisions)
| Skill | Purpose | Creates |
|-------|---------|---------|
| `/lite-why-project` | Define strategic vision | `why.md` |
| `/lite-product-discovery` | Personas, journeys, stories | `product-discovery.md` |

### Context & Status (Persistence)
| Skill | Purpose | Creates |
|-------|---------|---------|
| `/lite-project-context` | Scan codebase, detect stack | `stack.md` |
| `/lite-project-status` | Health check, show gaps | Status report |
| `/lite-work-memory` | Log session for continuity | Append to `progress.md` |

### Specification & Planning (Human Decisions + Persistence)
| Skill | Purpose | Creates |
|-------|---------|---------|
| `/lite-spec` | Define what to build | `specs/active/[name].md` |
| `/lite-plan` | Define how to build it | `plans/active/[name].md` |
| `/lite-prototyping` | Rapid throwaway mockup | `.shipkit-mockups/[name]/` |
| `/lite-prototype-to-spec` | Extract learnings | Append to spec |

### Knowledge Persistence
| Skill | Purpose | Creates |
|-------|---------|---------|
| `/lite-architecture-memory` | Log architectural decisions | Append to `architecture.md` |
| `/lite-data-contracts` | Define type shapes | `types.md` |
| `/lite-integration-docs` | External service patterns | `integrations/[service].md` |

### Quality & Communication
| Skill | Purpose | Creates |
|-------|---------|---------|
| `/lite-ux-audit` | Audit UX patterns | UX report |
| `/lite-user-instructions` | Track manual tasks | `user-tasks/active.md` |
| `/lite-communications` | Rich HTML visual output | `.shipkit-comms/` |

### System (Auto-triggered)
| Skill | Purpose | Trigger |
|-------|---------|---------|
| `/lite-detect` | Scan for follow-up work | After spec/plan completion |

---

## Quick Reference

**User asks "where should I start?"**
→ `/lite-project-context` to scan their codebase

**User asks "what's the status?"**
→ `/lite-project-status` for health check

**User describes a feature**
→ `/lite-spec` to capture the specification

**User wants to plan implementation**
→ `/lite-plan` after spec exists

**User completed significant work**
→ `/lite-work-memory` to log for next session

**User made an architectural decision**
→ `/lite-architecture-memory` to persist it

---

## What You Do Naturally (No Skill Needed)

| Task | Just Do It |
|------|------------|
| Implement a feature | Given a spec, just build it |
| Debug an error | Investigate systematically |
| Write tests | Write them alongside code |
| Document code | Add comments and docstrings |
| Refactor | Improve code when asked |

**Don't invoke a skill for these. Just do them.**

---

## Tech Stack (Solo Dev MVP Stack 2025)

All agents understand this default stack:

- **Framework**: Next.js (App Router)
- **Hosting**: Vercel
- **Database/Auth/Storage**: Supabase (Postgres + Auth + Realtime + Storage)
- **Payments**: Lemon Squeezy (MoR handles global tax)
- **Email**: Resend + React Email
- **Styling**: Tailwind + shadcn/ui
- **ORM**: Prisma

---

## Agent Personas

6 domain-expertise personas for POC/MVP development:

| Agent | Domain Expertise | Mindset |
|-------|------------------|---------|
| `lite-product-owner` | Vision, user needs, prioritization | "Smallest thing to validate" |
| `lite-ux-designer` | UI patterns, prototyping | "Proven patterns over custom" |
| `lite-architect` | Stack decisions, data modeling | "Leverage the platform" |
| `lite-implementer` | TDD-lite, integrations | "Working code beats perfect" |
| `lite-reviewer` | Security, quality gates | "Blockers vs suggestions" |
| `lite-researcher` | Official docs, troubleshooting | "Source of truth first" |

---

## Session Behavior

**At session start:**
- `lite-shipkit-master` loads (skill routing)
- Quick status shows active specs/plans
- Stale context warnings displayed

**During session:**
- Load context files when needed
- Suggest skills when they would add value
- Just do work that doesn't need skills

**At session end:**
- Consider `/lite-work-memory` for continuity
- Auto-detection may create queues for next session

---

**Remember:** Skills exist because you don't have memory. Use them to create persistence and capture human decisions. Everything else, just do.
