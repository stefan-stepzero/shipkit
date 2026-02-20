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
| Check project health | `/shipkit-project-status` |
| Index codebase for navigation | `/shipkit-codebase-index` |

### Spec & Planning
| When... | Use |
|---------|-----|
| Create feature specification | `/shipkit-spec` |
| Process feedback into investigated bug specs | `/shipkit-feedback-bug` |
| Plan implementation steps | `/shipkit-plan` |
| Map goals to features | `/shipkit-product-definition` |
| Think through decisions | `/shipkit-thinking-partner` |

### Knowledge & Memory
| When... | Use |
|---------|-----|
| Log architecture decision | `/shipkit-architecture-memory` |
| Define data shapes & types | `/shipkit-data-contracts` |
| Fetch external API patterns | `/shipkit-integration-docs` |
| Update CLAUDE.md with learnings | `/shipkit-claude-md` |
| End session / checkpoint | `/shipkit-work-memory` |

### Execution
| When... | Use |
|---------|-----|
| Build/compile until success | `/shipkit-build-relentlessly` |
| Test until all pass | `/shipkit-test-relentlessly` |
| Lint until clean | `/shipkit-lint-relentlessly` |
| Generate test case specs | `/shipkit-test-cases` |
| Parallel implementation in worktree | `/shipkit-implement-independently` |
| Create agent team from plan | `/shipkit-team` |
| Clean up stale worktrees | `/shipkit-cleanup-worktrees` |

### Quality & Communication
| When... | Use |
|---------|-----|
| Verify work before commit | `/shipkit-verify` |
| Production readiness audit | `/shipkit-preflight` |
| Scale & enterprise readiness | `/shipkit-scale-ready` |
| Audit LLM prompt architecture | `/shipkit-prompt-audit` |
| Audit UX patterns | `/shipkit-ux-audit` |
| Track manual tasks for user | `/shipkit-user-instructions` |
| Create visual HTML report | `/shipkit-communications` |

### System
| When... | Use |
|---------|-----|
| Install or update Shipkit | `/shipkit-update` |
| Find and install community skills | `/shipkit-get-skills` |
| Find and install MCP servers | `/shipkit-get-mcps` |
| AFK daemon / standby mode | `/shipkit-standby` |

**No skill needed for:** implementing, debugging, testing, refactoring, documenting code.

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
