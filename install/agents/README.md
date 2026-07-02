# Shipkit Agents

Specialized agent configurations for the Shipkit workflow. Agents are invoked via skills with `context: fork` + `agent:` frontmatter.

## Architecture

```
Orchestrators dispatch. Workers produce. Nothing runs inline.
```

Every agent is either an **orchestrator** (checks artifacts, dispatches skills, reports done) or a **worker** (personified domain expert, produces artifacts). Workers are further split into **producers** (create artifacts) and **reviewers** (assess artifact quality).

## How Agents Are Invoked

Skills with `context: fork` + `agent: {agent-name}` in their frontmatter spawn the named agent in a forked context. The agent runs with its own tools, model, and persona. Results persist via `.shipkit/` artifacts.

```yaml
# In a skill's frontmatter:
context: fork
agent: shipkit-visionary-agent    # spawns this agent
```

## Agent Taxonomy

### Orchestrators (0)

Orchestration lives entirely in the **`shipkit-orchestrate` engine** (runs inline in the
main session; phase skills call it). All forked loop-orchestrators — master, planning,
shipping, and now **direction** — have been retired. The engine + thin phase callers
(`shipkit-direction`, `shipkit-ship`, review) replace them. There are no orchestrator agents.

### Producer Workers (4)

Domain experts that create artifacts. They never dispatch to other skills or manage other agents.

| Agent | Domain | maxTurns |
|-------|--------|----------|
| **shipkit-visionary** | Strategic vision, project purpose, stage assessment | 50 |
| **shipkit-product-owner** | User needs, product definition, feature specs, test cases | 50 |
| **shipkit-architect** | System design, engineering decisions, implementation plans | 50 |
| **shipkit-thinking-partner** | Socratic questioning, decision exploration | 30 |

### Judgment Workers / Reviewers (3)

Each loop has a dedicated reviewer that assesses artifacts and writes structured reports. Orchestrators read these reports to decide whether to re-dispatch producers.

| Agent | Loop | Assessment Focus | maxTurns |
|-------|------|-----------------|----------|
| **shipkit-reviewer-direction** | Direction | Strategic coherence: vision ↔ why, goals complete, stage realistic | 40 |
| **shipkit-reviewer-planning** | Planning | Alignment: definitions agree, specs cover roadmap, no gaps | 50 |
| **shipkit-reviewer-shipping** | Shipping | Quality: code meets spec, tests pass, security, UX | 60 |

## Naming Convention

```
Orchestrators:  shipkit-orch-{scope}-agent.md
Producers:      shipkit-{role}-agent.md
Reviewers:      shipkit-reviewer-{loop}-agent.md
```

## Universal Loop Pattern

Every loop follows the same cycle:

```
1. Orchestrator dispatches producer skills → artifacts created
2. Orchestrator dispatches reviewer skill → assessment written
3. Orchestrator reads assessment
4. If pass → done
5. If gaps → re-dispatch specific producers → re-review
```

The orchestrator makes routing decisions. The reviewer provides evidence.

## Installation

Agents are installed to `.claude/agents/` when you run `/shipkit-update`:

```
.claude/
└── agents/
    ├── shipkit-visionary-agent.md
    ├── shipkit-product-owner-agent.md
    ├── shipkit-architect-agent.md
    ├── shipkit-reviewer-direction-agent.md
    ├── shipkit-reviewer-planning-agent.md
    ├── shipkit-reviewer-shipping-agent.md
    └── shipkit-thinking-partner-agent.md
```

## Model Selection

Orchestrators use `model: sonnet` for efficient routing. Producers use `model: opus` for deep domain work. Reviewers use `model: sonnet` for judgment. Implementation is handled by general-purpose teammates spawned by the shipping orchestrator.
