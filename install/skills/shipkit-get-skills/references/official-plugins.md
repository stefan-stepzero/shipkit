# Official Claude Code Plugins

Reference catalog of official plugins from the `claude-code-plugins` marketplace (anthropics/claude-code).

**Load this file when user asks:** "what plugins are available", "show me official plugins", "what's in the marketplace", "list plugins"

---

## Installation

```bash
# Add marketplace (may already be present)
/plugin marketplace add anthropics/claude-code

# Install a plugin
/plugin install <plugin-name>@claude-code-plugins
```

---

## Recommended Plugins

These provide genuine capability improvements:

| Plugin | Purpose | Why Valuable |
|--------|---------|--------------|
| **frontend-design** | Better UI/UX aesthetics | Injects design guidance Claude lacks by default. Avoids generic "AI slop" UI. |
| **security-guidance** | Security vulnerability warnings | PreToolUse hook catches issues before they happen (XSS, injection, eval, etc.) |
| **commit-commands** | Git workflow automation | `/commit`, `/commit-push-pr`, `/clean_gone` commands |

```bash
# Install recommended
/plugin install frontend-design@claude-code-plugins
/plugin install security-guidance@claude-code-plugins
/plugin install commit-commands@claude-code-plugins
```

---

## All Official Plugins

### Git & PR Workflow

| Plugin | Contains | Description |
|--------|----------|-------------|
| **commit-commands** | `/commit`, `/commit-push-pr`, `/clean_gone` | Analyzes changes, drafts commit messages, creates PRs automatically |
| **code-review** | `/code-review` + 4 agents | Parallel PR review with confidence scoring (80+ threshold). Posts to PR or terminal. |
| **pr-review-toolkit** | `/pr-review-toolkit:review-pr` + 6 agents | Deep review: comments, tests, errors, types, code quality, simplification |

### Feature Development

| Plugin | Contains | Description |
|--------|----------|-------------|
| **feature-dev** | `/feature-dev` + 3 agents | 7-phase workflow: Discovery → Exploration → Questions → Architecture → Implementation → Review → Summary |
| **frontend-design** | Skill (auto-invoked) | Distinctive UI guidance: bold typography, meaningful animations, avoids generic patterns |

### Automation & Hooks

| Plugin | Contains | Description |
|--------|----------|-------------|
| **hookify** | `/hookify`, `/hookify:list`, `/hookify:configure` | Create hooks from markdown files. Block dangerous commands, warn about patterns. |
| **ralph-wiggum** | `/ralph-loop`, `/cancel-ralph` | Self-referential AI loops. Keeps running same prompt until completion promise. |
| **security-guidance** | PreToolUse hook | Warns about security issues: command injection, XSS, eval, pickle, os.system |

### Plugin & SDK Development

| Plugin | Contains | Description |
|--------|----------|-------------|
| **plugin-dev** | `/plugin-dev:create-plugin` + 7 skills | Comprehensive toolkit for building Claude Code plugins |
| **agent-sdk-dev** | `/new-sdk-app` + 2 verifiers | Scaffolds Claude Agent SDK apps (Python/TypeScript) |

### Output Styles

| Plugin | Contains | Description |
|--------|----------|-------------|
| **explanatory-output-style** | SessionStart hook | Adds "★ Insight" boxes explaining implementation choices |
| **learning-output-style** | SessionStart hook | Requests user write code at decision points (pedagogical) |

### Migration

| Plugin | Contains | Description |
|--------|----------|-------------|
| **claude-opus-4-5-migration** | Skill | Updates model strings, beta headers for Opus 4.5 |

---

## When to Suggest Each

| User Need | Suggest |
|-----------|---------|
| "Help with commits/git" | `commit-commands` |
| "Review my PR" | `code-review` or `pr-review-toolkit` |
| "Building UI/frontend" | `frontend-design` |
| "Security concerns" | `security-guidance` |
| "Create custom hooks" | `hookify` |
| "Run overnight/autonomous" | `ralph-wiggum` |
| "Building a plugin" | `plugin-dev` |
| "Building Agent SDK app" | `agent-sdk-dev` |

---

## Plugins vs Skills

| Aspect | Official Plugins | skills.sh |
|--------|------------------|-----------|
| Source | anthropics/claude-code | Community repos |
| Install | `/plugin install X@claude-code-plugins` | `npx skills add owner/repo` |
| Contains | Commands, agents, skills, hooks, MCP | Skills only (SKILL.md) |
| Best for | Git workflow, code review, hooks | Domain-specific skills |

**Rule of thumb:** Check official plugins first for common dev workflows, skills.sh for specialized/domain needs.

---

## Plugin Management

```bash
# List installed
/plugin

# Enable/disable
/plugin enable <name>
/plugin disable <name>

# Uninstall
/plugin uninstall <name>

# Update marketplace
/plugin marketplace update claude-code-plugins
```

---

*Source: github.com/anthropics/claude-code | Marketplace: claude-code-plugins | Updated: February 2026*
