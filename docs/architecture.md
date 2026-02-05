# Shipkit

## At a Glance

- **Status:** In Progress
- **GitHub:** https://github.com/user/shipkit
- **Icon:** Boxes
- **Color:** text-blue-400

## The Hook

Can structured workflows and persistent context files solve Claude's fundamental limitation—that it forgets everything between sessions?

## Research Question

Claude is trained on human coding patterns but lacks what makes human developers effective: memory and session continuity. Every conversation starts fresh. Claude doesn't remember yesterday's architecture decisions, the trade-offs you discussed, or why you chose that stack.

**The hypothesis:** If skills force human decisions to be explicit and persist them in files that survive sessions, Claude can maintain institutional knowledge and product thinking consistency across an entire project lifecycle.

**The test:** Build a complete product development workflow as Claude Code skills and see if it produces better outcomes than raw Claude Code alone.

## Why This Matters

Every Claude Code user hits the same wall: context evaporates. You repeat yourself, Claude contradicts earlier decisions, and accumulated knowledge disappears. This isn't a bug—it's architectural. Claude has no persistent memory.

This matters because:
- **Solo developers** can't afford to re-explain context every session
- **Teams** need shared understanding that doesn't live in one person's head
- **Products** require consistent decisions across weeks/months of development

If we can solve this for product development, the pattern generalizes to any domain requiring continuity.

## Methodology

### Core Approach
Layer structured workflows on top of Claude Code using its native primitives:
- **Skills** (slash commands) that guide specific workflows
- **Agent personas** that provide domain expertise
- **Context files** (`.shipkit/`) that persist decisions
- **Hooks** that auto-load context at session start

### The Skill Value Test
Every skill must pass one criterion: does it do something Claude can't do well without instruction?

| Needs a Skill | No Skill Needed |
|---------------|-----------------|
| Define project vision | Debug this error |
| Capture architecture decisions | Implement the login feature |
| Create feature specifications | Write unit tests |
| Document integration patterns | Refactor this code |

### What We Built

**17 skills across 6 categories:**

| Category | Skills | Purpose |
|----------|--------|---------|
| Vision & Discovery | `why-project`, `product-discovery`, `spec` | Capture what/why/who |
| Planning | `plan`, `prototyping`, `prototype-to-spec` | Transform specs to implementation |
| Context & Status | `project-context`, `project-status`, `work-memory` | Track state across sessions |
| Knowledge Persistence | `architecture-memory`, `data-contracts`, `integration-docs` | Preserve technical decisions |
| Quality | `ux-audit`, `user-instructions` | Verification and user-facing tasks |
| Communication | `communications` | Visualize project state as HTML |

**7 agent personas:**
- **Project Manager** — Coordination, status tracking, context management
- **Product Owner** — Pragmatic "smallest thing to learn" thinking
- **Architect** — Solo Dev MVP Stack expertise (Next.js/Supabase/Vercel)
- **Implementer** — TDD-lite: test critical paths, manual test UI
- **Reviewer** — Blocks on security/integrity, suggests on polish
- **Researcher** — Integration troubleshooting from authoritative sources
- **UX Designer** — Pattern-first rapid prototyping

**Persistent context files:**
```
.shipkit/
├── why.md              # Vision, problem, solution, success criteria
├── stack.md            # Framework, database, deployment choices
├── architecture.md     # Append-only decision log with rationale
├── schema.md           # Data model
├── progress.md         # Session summaries (48-hour window, auto-archives)
├── specs/active/       # Feature specs with Given/When/Then
├── plans/              # Implementation plans
└── data-contracts.md   # Data shapes across layers
```

## Key Findings

### 1. Context Over Defaults Works
Claude has strong implicit preferences from training (modular architecture, TypeScript strict mode, comprehensive error handling). When `why.md` says "MVP in 2 weeks, solo dev," skills that check context first produce simpler, more appropriate solutions.

**Before context:** "I'll create separate components for each widget with a shared state management layer..."

**After context:** "Given your MVP timeline, I'll keep this simple—one Dashboard component with inline state."

### 2. Append-Only Logs Beat Overwritten Files
Architecture decisions need history. When a skill appends to `architecture.md` instead of overwriting, Claude can detect contradictions and track what superseded what.

### 3. Progressive Disclosure Is Essential
Loading all context upfront wastes tokens and confuses Claude. Skills that load only what they need (~1-2K tokens) perform better than those that dump everything.

### 4. Skills Should Be Small
Effective skills are <300 lines. They do one thing: force one decision, create one artifact. Skills that try to do too much get ignored.

### 5. The 48-Hour Window
Session progress older than 48 hours is noise. Auto-archiving by month keeps `progress.md` lean while preserving searchable history.

## Implications

### For Claude Code Users
- **Persist decisions, not just code.** The `.shipkit/` pattern works for any domain. Create context files for what matters.
- **Force explicit decisions early.** A skill that asks "why are you building this?" before "how should I build it?" produces better outcomes.
- **Check context before applying defaults.** Claude's training defaults aren't wrong—they're context-blind.

### For Tool Builders
- **Build ON Claude Code, not beside it.** Use its primitives (skills, hooks, agents). Don't create parallel systems.
- **Skills should capture human decisions, not automate Claude tasks.** If Claude does it well naturally, you don't need a skill.
- **Token budgets matter.** Design for ~1500-2500 tokens per skill invocation.

### For the Broader Question
Persistent context files are a viable solution to Claude's memory limitation—but they require discipline. The framework has to enforce writing decisions down, or entropy wins.

## Limitations

- **Tested primarily on solo/small team MVPs.** Unclear how patterns scale to larger teams or longer projects.
- **Opinionated stack.** Agent personas assume Next.js/Supabase/Vercel. Different stacks would need different personas.
- **Requires user discipline.** Skills can guide, but users who skip the "why" and jump to implementation still get suboptimal results.
- **No quantitative comparison.** "Better outcomes" is based on qualitative observation, not A/B testing.

## Technical Details

### Integration System
Every skill connects through 7 files:
1. `SKILL.md` — Skill definition and prompts
2. `manifest.json` — Registration and metadata
3. `settings.json` — Permissions
4. `router hook` — Intent detection and routing
5. `session hook` — Context auto-loading
6. `shared components` — Reusable prompt fragments
7. `detect skill` — Auto-triggers follow-up skills

### Token Budget
- Session start: ~400-500 tokens (master + stack + architecture summary)
- Per skill: ~1500-2500 tokens (skill definition + specific context)
- Never load full codebase upfront

### Quality Enforcement
- Skills include embedded checklists for artifact validation
- "Iron laws" and "red flag" tables prevent common mistakes
- Cross-referencing sections define skill handoffs

## What I Learned

**Skills that teach methodology outperform skills that generate artifacts.** A skill that explains "how to write a good spec" and asks clarifying questions produces better specs than one that templates them.

**Examples bias output dangerously.** Including example output in a skill prompt biases Claude toward that format AND content. Use examples sparingly, for format only.

**The real product is the context files.** The skills are scaffolding. The durable value is the decisions captured in `.shipkit/` that let the next session pick up where this one left off.

**Less is more.** Early versions had 25+ skills. Consolidating to 17 improved usability without losing capability. Users don't read menus—they need obvious next actions.
