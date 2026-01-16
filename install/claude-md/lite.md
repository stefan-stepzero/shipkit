# Shipkit Lite - Project Instructions

**You are working with Shipkit Lite** - a lightweight framework for POC/MVP development.

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
  implementations/
    index.md            # Auto-generated TOC
    components/         # Per-component docs
    routes/             # Per-route docs
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
| `/lite-component-knowledge` | Document components | `implementations/components/` |
| `/lite-route-knowledge` | Document routes | `implementations/routes/` |
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
