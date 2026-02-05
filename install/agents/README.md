# Shipkit Agents (Subagents)

Specialized subagent configurations for the Shipkit workflow. These follow Claude Code's official subagent specification.

## How Subagents Work

Subagents are **not** invoked directly by skills or users. Instead:

1. **Claude auto-delegates** based on the agent's `description` field matching the task
2. Each subagent runs in its own context with its own system prompt
3. Subagents can have **preloaded skills** for domain knowledge
4. Results return to the main conversation when the subagent completes

**Key insight:** The `description` field drives delegation. Write descriptions that clearly state when the agent should be used.

## Available Agents

| Agent | Role | Delegates When |
|-------|------|----------------|
| **shipkit-project-manager** | Coordination & context | Project status, context management, workflow orchestration |
| **shipkit-product-owner** | Vision & requirements | Defining what to build, user research, feature prioritization |
| **shipkit-ux-designer** | UI/UX design | Designing interfaces, UX reviews, wireframes |
| **shipkit-architect** | Technical decisions | Planning features, data models, technical choices |
| **shipkit-implementer** | Code implementation | Building features, fixing bugs, writing tests |
| **shipkit-reviewer** | Code review & quality | Reviewing code, security checks, validation |
| **shipkit-researcher** | Research & analysis | Documentation lookup, API research, troubleshooting |

## Agent Format

Each agent uses Claude Code's subagent YAML frontmatter:

```markdown
---
name: shipkit-architect
description: Technical architect for system design... Use when planning features...
tools: Read, Glob, Grep, Write, Edit, Bash
model: opus
permissionMode: default
memory: project
skills: shipkit-plan, shipkit-architecture-memory
---

You are a Technical Architect...
```

### Frontmatter Fields

| Field | Purpose |
|-------|---------|
| `name` | Unique identifier |
| `description` | **Drives auto-delegation** - when Claude sees matching tasks |
| `tools` | Tools the subagent can access |
| `model` | Model to use (opus, sonnet, haiku) |
| `permissionMode` | Permission level (default, acceptEdits, bypassPermissions) |
| `memory` | Memory scope (user, project, local) |
| `skills` | Preloaded skills for domain knowledge |

## Skills ↔ Agents Relationship

**One-way relationship:**

- ❌ Skills cannot invoke agents
- ✅ Agents can have skills preloaded

When an agent has `skills: shipkit-plan`, it gets that skill's knowledge automatically loaded.

## How Delegation Happens

```
User: "Plan the authentication feature"
         ↓
Claude sees "plan" + "feature" matches architect description
         ↓
Auto-delegates to shipkit-architect subagent
         ↓
Architect uses its tools + preloaded skills
         ↓
Results return to main conversation
```

## Hybrid Mode: Skills + Agents

Shipkit supports **both** direct skill invocation and agent delegation:

| Mode | How | When to Use |
|------|-----|-------------|
| **Direct** | `/shipkit-plan` | Explicit control, know exactly what skill you want |
| **Natural** | "Plan the auth feature" | Let Claude route to appropriate agent |

**Both work together:**
- Skills remain user-invocable with `/skill-name`
- Agents auto-delegate based on task matching
- You choose: explicit control OR natural language

**Example workflows:**

```
# Direct mode - you control
/shipkit-project-status
/shipkit-plan auth feature
/shipkit-build-relentlessly

# Natural mode - Claude routes
"What's the project status?"        → project-manager
"Plan the authentication feature"   → architect
"Build until it compiles"           → implementer
```

## Installation

Agents are installed to `.claude/agents/` when you run `/shipkit-update`:

```
.claude/
└── agents/
    ├── shipkit-project-manager.md
    ├── shipkit-product-owner.md
    ├── shipkit-ux-designer.md
    ├── shipkit-architect.md
    ├── shipkit-implementer.md
    ├── shipkit-reviewer.md
    └── shipkit-researcher.md
```

## Customization

To customize an agent for your project:

1. Edit the file in `.claude/agents/`
2. Modify the system prompt (markdown body)
3. Adjust tools, skills, or model as needed
4. Local changes take precedence

## Model Selection

All Shipkit agents default to `opus` for highest quality reasoning. Consider using `sonnet` or `haiku` for:

- High-volume, repetitive tasks
- Simple lookups or searches
- Cost-sensitive workflows

## Reference

- [Claude Code Subagents Documentation](https://docs.anthropic.com/en/docs/claude-code/sub-agents)
- [Shipkit Skills](../skills/)
