# Shipkit Lite - Project Instructions

**You are working with Shipkit Lite** - a lightweight framework for POC/MVP development.

## Critical Rules

1. **ALL context lives in `.shipkit-lite/`** - Never create context or documentation files outside this folder
2. **Skills are pure guidance** - Use Read/Write tools directly, no script execution
3. **Ask before generating** - 2-3 questions, then generate (avoid wasted tokens)
4. **Only update changed files** - Use timestamps to detect freshness
5. **Append, don't replace** - Files accumulate context over time

---

## CRITICAL: Always Use /lite-whats-next After Skills

**After completing ANY lite skill, you MUST immediately invoke `/lite-whats-next`:**

**Why this is mandatory:**
- Prevents users from getting stuck ("what do I do next?")
- Enforces optimal workflow order (Vision → Understand → Co-design → Execute → Document)
- Detects gaps and warns about missing dependencies
- Provides intelligent, context-aware guidance

**Workflow:**
1. Complete a skill (e.g., `/lite-spec`)
2. **IMMEDIATELY invoke `/lite-whats-next`** (not optional!)
3. `/lite-whats-next` analyzes project state and suggests next step
4. Present the suggestion to user

**Violation examples:**
- ❌ Completing `/lite-spec` and saying "Spec created. What would you like to do next?"
- ❌ Completing `/lite-implement` and just moving on
- ❌ Suggesting next skill manually instead of using `/lite-whats-next`
- ✅ Completing `/lite-spec` then invoking `/lite-whats-next` → presenting its analysis
- ✅ After ANY skill completes, invoke `/lite-whats-next` automatically

**Exception:** If user explicitly says "skip workflow guidance" or "I'll decide what's next"

**This is as important as "Skills Must Use Skills" - it's not a suggestion, it's a requirement.**

---

## File Structure You'll Create

```
.shipkit-lite/
  stack.md              # Tech stack (auto-scanned)
  architecture.md       # Decisions log (append-only)
  implementations.md    # Component/route docs (append-only)
  types.md              # TypeScript types
  specs/active/         # Feature specs
  plans/                # Implementation plans
```

## Skill Invocation

**Project Setup:**
- `/lite-why-project` - Define strategic vision (who/why/where)
- `/lite-project-context` - Scan codebase, create stack.md
- `/lite-project-status` - Health check, show gaps

**Feature Development:**
- `/lite-spec` - Write spec → `specs/active/[name].md`
- `/lite-prototyping` - Rapid UI mockup → `.shipkit-mockups/[name]/`
- `/lite-prototype-to-spec` - Extract prototype learnings → append to spec
- `/lite-architecture-memory` - Log decision → append to `architecture.md`
- `/lite-plan` - Create plan → `plans/[name].md`
- `/lite-implement` - Build feature with TDD guidance

**Documentation:**
- `/lite-component-knowledge` - Document components → append to `implementations.md`
- `/lite-route-knowledge` - Document routes → append to `implementations.md`
- `/lite-document-artifact` - Create standalone doc → `docs/[category]/[name].md`
- `/lite-communications` - Create visual HTML from any lite content

**Quality & Process:**
- `/lite-quality-confidence` - Pre-ship checks
- `/lite-user-instructions` - Track manual tasks → `user-tasks/active.md`
- `/lite-work-memory` - Log session → append to `progress.md`

**Utilities:**
- `/lite-whats-next` - Smart workflow guidance (MANDATORY after every skill)
- `/lite-ux-coherence` - Check UX consistency
- `/lite-data-consistency` - Manage types/schemas
- `/lite-integration-guardrails` - Service integration warnings
- `/lite-debug-systematically` - 4-phase debugging

## Workflow Pattern

**Typical flow:**
```
/lite-project-context (once)
  → /lite-spec (per feature)
    → /lite-plan
      → /lite-implement
        → /lite-component-knowledge
          → /lite-quality-confidence
```

**Rules:**
- **ALWAYS invoke `/lite-whats-next` immediately after completing any skill**
- Run `/lite-project-status` when user asks for health check
- Load context files lazily (only when needed)
- Check timestamps before regenerating (avoid duplicate work)
- Let `/lite-whats-next` decide workflow order (don't hardcode suggestions)

## Context Loading

**Session start loads:**
- `lite-shipkit-master` skill (orchestrator)
- `stack.md` (if exists)
- `architecture.md` (if exists)

**Load on-demand:**
- `implementations.md` - When documenting components/routes
- `types.md` - When checking type consistency
- `specs/` - When planning implementation
- `plans/` - When implementing

## Protected Files (Read-Only)

Skills create these via Write tool. You read them, but only update via the skill:

- `stack.md` - Update via `/lite-project-context`
- `architecture.md` - Append via `/lite-architecture-memory`
- `implementations.md` - Append via `/lite-component-knowledge` or `/lite-route-knowledge`
- `specs/` - Create via `/lite-spec`
- `plans/` - Create via `/lite-plan`

## Quick Reference

**User asks "where should I start?"**
→ Run `/lite-project-context` to scan their codebase

**User asks "what's the status?"**
→ Run `/lite-project-status` to show health check

**User describes a feature**
→ Run `/lite-spec` to create specification

**User asks "how do I build this?"**
→ Run `/lite-plan` after spec exists

**User asks "start coding"**
→ Run `/lite-implement` after plan exists

**User completed work**
→ Suggest `/lite-component-knowledge` or `/lite-work-memory`

---

**Remember:** Shipkit Lite is about speed and efficiency. Ask questions, load context lazily, suggest next steps proactively.
