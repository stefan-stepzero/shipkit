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
agent: shipkit-orch-direction-agent    # spawns this agent
```

## Agent Taxonomy

### Orchestrators (4)

Loop dispatchers that check artifacts, invoke skills, and manage feedback cycles. They never produce domain artifacts.

| Agent | Scope | maxTurns |
|-------|-------|----------|
| **shipkit-orch-master** | Sequential dispatch: direction → planning → shipping | 200 |
| **shipkit-orch-direction** | Strategic artifacts + coherence review cycle | 120 |
| **shipkit-orch-planning** | Definitions/specs + alignment review cycle | 100 |
| **shipkit-orch-shipping** | Implementation + verification + release gate | 150 |

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
    ├── shipkit-orch-master-agent.md
    ├── shipkit-orch-direction-agent.md
    ├── shipkit-orch-planning-agent.md
    ├── shipkit-orch-shipping-agent.md
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
