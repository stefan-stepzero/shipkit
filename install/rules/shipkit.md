# Shipkit Framework Rules

<!-- Framework-managed file. Updated via /shipkit-update. Do not edit manually. -->

## Core Rules

1. **Context over defaults** — Check `.shipkit/` before assuming. Project decisions override training defaults.
2. **MVP quality** — Core paths bulletproof, everything else minimal. Ship > perfect.
3. **Stay focused** — Do what's asked. No unsolicited refactoring or "improvements."
4. **Ask before generating** — 2-3 clarifying questions, then build.
5. **Skills for persistence only** — Use skills to capture decisions or create memory. Everything else, just do it.
6. **Solo patterns** — No PR workflows, no "future developer" docs, no unnecessary abstraction.
7. **Save before compact** — When you see the PreCompact warning, run `/shipkit-work-memory` to save progress.

---

## Working Smart

### Decompose Before Starting
Before diving into work, assess the task shape:

| You notice... | Do this instead of working inline |
|---|---|
| Task touches 3+ independent files | Parallel agents, one per file/area |
| Code changes could break things | `isolation: worktree` — review before merging |
| Need to understand unfamiliar code | Fork an Explore agent (Haiku) before coding |
| Generating large output (>200 lines) | Write sections to files, then combine |
| Task will need 10+ tool calls | Fork it — keep main conversation for coordination |
| Multiple research questions | Parallel background agents, each writes to a file |
| Repetitive changes across many files | `/batch` — spawns parallel worktree agents |

### Write to Files, Not Just Context
Context gets compacted. Files persist. Default to disk.

- **Research findings** → write to a file before acting on them
- **Agent results** → each agent writes to a named output file, not just return text
- **Intermediate state** → if a task has phases, write phase output to disk between phases
- **Large generated content** → write to disk first, present summary to user

### Orient Before Acting
- **Read before editing** — always read a file before modifying it
- **Search before creating** — Grep/Glob to check if a function, component, or pattern already exists
- **Understand the test setup** — check for test files and test commands before implementing
- **Check `.shipkit/` context** — architecture decisions, stack choices, and specs may already answer your question

### Verify After Changing
- **Run tests** if a test command is known (check `package.json` scripts, Makefile, etc.)
- **Check imports** after multi-file changes — verify no broken references
- **Spot-check output** — after generating config, data files, or code, read back a sample to verify correctness
- **QA delegated work** — always review Sonnet/Haiku agent output before presenting as done

### Model Budget
Don't waste expensive models on cheap tasks:
- **Haiku**: file search, codebase exploration, audit, validation, reading/summarizing
- **Sonnet**: code changes, research, data processing, multi-step tasks
- **Opus**: complex architecture, ambiguous design, nuanced writing — or when the user is present and expects it

---

## Quality Standards

### AI Agent Accessibility
All interactive UI elements must include:
- `data-testid` attribute (naming: `{component}-{action}`, e.g., `login-submit-btn`, `sidebar-nav-link`)
- ARIA roles for custom widgets (`combobox`, `dialog`, `menu`, `tablist`)
- State attributes (`aria-expanded`, `aria-checked`, `aria-selected`, `data-state`)

**Why:** Enables AI-driven QA (Claude in Chrome, Playwright), E2E testing, and accessibility compliance. Without these, AI agents cannot reliably interact with or verify UI elements.

---

## Context Files

All project context lives in `.shipkit/`:

| File | Purpose |
|------|---------|
| `why.json` | Vision, constraints, approach |
| `product-discovery.json` | User needs, personas, journeys |
| `product-definition.json` | Product blueprint (features, patterns, differentiators) |
| `engineering-definition.json` | Engineering blueprint (mechanisms, components) |
| `goals.json` | Success criteria & stage gates |
| `stack.json` | Tech choices (auto-scanned) |
| `architecture.json` | Decisions log (append-only) |
| `progress.json` | Session continuity |
| `codebase-index.json` | Navigation index (concept → files) |
| `specs/active/*.json` | Feature specs |
| `plans/active/*.json` | Implementation plans |

**Always check context before making architectural decisions.**

---

## Codebase Navigation

If `.shipkit/codebase-index.json` exists:
1. Read it FIRST before globbing or exploring files
2. Use `concepts` to find feature-related files
3. Use `entryPoints` to find starting points
4. Check `skip` to avoid wasting context on irrelevant files
5. Don't glob or explore if the index answers the question

**The index is injected at session start.** Use the concept mappings shown there for quick navigation.

---

## Skills Reference

### Vision & Discovery
| When... | Use |
|---------|-----|
| Define project vision | `/shipkit-why-project` |
| Create personas & journeys | `/shipkit-product-discovery` |
| Scan codebase, detect stack | `/shipkit-project-context` |
| Index codebase for navigation | `/shipkit-codebase-index` |
| Set strategic direction & stage | `/shipkit-vision` |
| Define project stage & constraints | `/shipkit-stage` |

### Solution Design
| When... | Use |
|---------|-----|
| Design solution blueprint | `/shipkit-product-definition` |
| Design technical approach | `/shipkit-engineering-definition` |
| Set up design system, tokens, brand direction | `/shipkit-design-system` |
| Define user-outcome success criteria | `/shipkit-product-goals` |
| Define technical performance criteria | `/shipkit-engineering-goals` |

### Spec & Planning
| When... | Use |
|---------|-----|
| Prioritize which specs to write first | `/shipkit-spec-roadmap` |
| Create feature specification | `/shipkit-spec` |
| Process feedback into investigated bug specs | `/shipkit-feedback-bug` |
| Plan implementation steps | `/shipkit-plan` |
| Think through decisions | `/shipkit-thinking-partner` |

### Knowledge & Memory
| When... | Use |
|---------|-----|
| Update CLAUDE.md with learnings | `/shipkit-claude-md` |
| End session / checkpoint | `/shipkit-work-memory` |

### Execution
| When... | Use |
|---------|-----|
| Generate test case specs | `/shipkit-test-cases` |

### Quality & Communication
| When... | Use |
|---------|-----|
| Verify work before commit | `/shipkit-review-shipping` |
| Production readiness audit | `/shipkit-preflight` |
| Scale & enterprise readiness | `/shipkit-scale-ready` |
| Audit LLM prompt architecture | `/shipkit-prompt-audit` |
| Audit UX patterns | `/shipkit-ux-audit` |
| Semantic QA for API/LLM outputs | `/shipkit-semantic-qa` |
| Track & visualize metrics | `/shipkit-metrics` |
| Visual QA with Playwright | `/shipkit-qa-visual` |
| Track manual tasks for user | `/shipkit-user-instructions` |
| Create visual HTML report | `/shipkit-communications` |

### System
| When... | Use |
|---------|-----|
| Install or update Shipkit | `/shipkit-update` |
| Find and install community skills | `/shipkit-get-skills` |
| Find and install MCP servers | `/shipkit-get-mcps` |


**No skill needed for:** implementing, debugging, testing, refactoring, documenting code.

**Built-in commands:**
- `/simplify` — Launches 3 parallel agents (reuse, quality, efficiency) to review changed code and auto-fix issues. Good for post-implementation cleanup.
- `/batch <instruction>` — Decomposes a large mechanical change into 5–30 independent units, spawns parallel worktree agents that each open a PR. For migrations, bulk refactors, mass renames.
- Use `/simplify` for code cleanup after writing. Use `/shipkit-review-shipping` for comprehensive spec-aligned review (12 quality dimensions).
- The shipping orchestrator manages Agent Teams directly for parallel implementation.

---

## Meta-Behavior

**When user asks to remember something** (e.g., "remember this", "save this for next time", "add to CLAUDE.md"):
- Determine type: style/behavior → Working Preferences, technical/pattern → Project Learnings
- Ask scope: project-wide (root) or folder-specific
- Append to appropriate section in CLAUDE.md
- Confirm what was added

**Do NOT auto-suggest** — Don't ask "Should I remember this?" after corrections. Only persist when user explicitly requests it.

**To remove a learning:** User says "remove the learning about X" — edit CLAUDE.md directly.

---

## Auto Memory

Claude Code maintains persistent memory across sessions in `~/.claude/projects/<project-hash>/memory/`. Key files:

| File | Purpose |
|------|---------|
| `MEMORY.md` | Always loaded - keep concise (<200 lines) |
| `*.md` | Additional memory files linked from MEMORY.md |

**Usage:**
- Use `/shipkit-work-memory` to save session progress
- Manual edits to MEMORY.md persist across sessions
- Link to other files in memory directory for detailed notes

**Note:** Auto memory is separate from `.shipkit/` context files. Use `.shipkit/` for project artifacts (specs, plans, architecture), auto memory for session-to-session learnings.

---

## Sandbox Mode

If sandbox mode is enabled, `.claude/skills/` is write-protected. Shipkit install/update requires either:
- Sandbox disabled during install, or
- `.claude/` added to `sandbox.filesystem.allowWrite`
