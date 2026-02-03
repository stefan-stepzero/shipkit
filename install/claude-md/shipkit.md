<!-- BEGIN Shipkit v1.1.0 -->
# Shipkit

Solo dev framework for shipping MVPs. AI-assisted, fast iteration, production-ready core paths.

---

## Core Rules

1. **Context over defaults** — Check `.shipkit/` before assuming. Project decisions override training defaults.
2. **MVP quality** — Core paths bulletproof, everything else minimal. Ship > perfect.
3. **Stay focused** — Do what's asked. No unsolicited refactoring or "improvements."
4. **Ask before generating** — 2-3 clarifying questions, then build.
5. **Skills for persistence only** — Use skills to capture decisions or create memory. Everything else, just do it.
6. **Solo patterns** — No PR workflows, no "future developer" docs, no unnecessary abstraction.
7. **Compact at 75%** — Run `/compact` manually around 75% context usage to avoid losing work.

---

## Working Preferences

<!-- Your preferences. Claude follows these each session. Edit as needed. -->

- **Verbosity:** Concise — skip explanations unless asked
- **Confirmations:** Just do it for small changes, confirm for destructive ops
- **Code style:** Match existing codebase
- **Scope:** Stay focused on what's asked

---

## Context Files

All project context lives in `.shipkit/`:

| File | Purpose |
|------|---------|
| `why.md` | Vision, constraints, approach |
| `stack.md` | Tech choices (auto-scanned) |
| `architecture.md` | Decisions log (append-only) |
| `progress.md` | Session continuity |
| `codebase-index.json` | Navigation index (concept → files) |
| `specs/active/` | Feature specs |
| `plans/active/` | Implementation plans |

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
| Plan implementation steps | `/shipkit-plan` |
| Quick UI mockup | `/shipkit-prototyping` |
| Extract prototype learnings | `/shipkit-prototype-to-spec` |

### Knowledge & Memory
| When... | Use |
|---------|-----|
| Log architecture decision | `/shipkit-architecture-memory` |
| Define data shapes & types | `/shipkit-data-contracts` |
| Fetch external API patterns | `/shipkit-integration-docs` |
| Update CLAUDE.md with learnings | `/shipkit-claude-md` |
| End session / checkpoint | `/shipkit-work-memory` |

### Quality & Communication
| When... | Use |
|---------|-----|
| Verify work before commit | `/shipkit-verify` |
| Production readiness audit | `/shipkit-preflight` |
| Audit UX patterns | `/shipkit-ux-audit` |
| Track manual tasks for user | `/shipkit-user-instructions` |
| Create visual HTML report | `/shipkit-communications` |

### Ecosystem
| When... | Use |
|---------|-----|
| Find and install community skills | `/shipkit-get-skills` |
| Find and install MCP servers | `/shipkit-get-mcps` |

**No skill needed for:** implementing, debugging, testing, refactoring, documenting code.

---

## Meta-Behavior

**When user asks to remember something** (e.g., "remember this", "save this for next time", "add to CLAUDE.md"):
- Determine type: style/behavior → Working Preferences, technical/pattern → Project Learnings
- Ask scope: project-wide (root) or folder-specific
- Append to appropriate section
- Confirm what was added

**Do NOT auto-suggest** — Don't ask "Should I remember this?" after corrections. Only persist when user explicitly requests it.

**To remove a learning:** User says "remove the learning about X" — just edit the file directly.

---

## Project Learnings

<!-- Mistakes corrected and project-specific knowledge. Claude checks this to avoid repeating errors. -->

*(None yet — learnings will be added as the project evolves)*

<!-- END Shipkit v1.1.0 -->
