# Agent Personas

Specialized agent configurations for the shipkit workflow.

## Available Agents

| Agent | Role | Used By |
|-------|------|---------|
| **Discovery** | Product discovery, strategy, user research | ProdKit skills |
| **Architect** | Technical planning, specifications | `/specify`, `/plan`, `/tasks` |
| **Implementer** | TDD-focused coding | `/implement` (subagent mode) |
| **Reviewer** | Code review, quality gates | `/implement` (review stages) |
| **Researcher** | Deep research, exploration | `/brainstorming`, research phases |

## How They're Used

### Skill-Triggered Loading

Each skill specifies which agent persona to load. Look for the "Agent Persona" section at the top of each skill:

```markdown
## Agent Persona

**Load:** `.claude/agents/architect-agent.md`

Adopt: Systematic thinking, spec completeness focus, documents trade-offs.
```

When a skill runs, Claude reads the persona file and adopts that personality.

### In Subagent Mode (`/implement`)

```
Controller (you) manages workflow
        ↓
Dispatch Implementer Agent for task
        ↓
Dispatch Reviewer Agent (spec compliance)
        ↓
Dispatch Reviewer Agent (code quality)
        ↓
Controller verifies and marks complete
```

### In Discovery (`/brainstorming`)

```
Discovery Agent leads conversation
        ↓
Researcher Agent for deep dives
        ↓
Discovery Agent synthesizes
```

## Agent Prompt Structure

Each agent file contains:
- **Role**: What they do
- **When Used**: Which skills use them
- **Personality**: How they behave
- **Approach**: Their methodology
- **Key Behaviors**: Specific actions
- **Constraints**: What they don't do
- **Prompt Template**: How to invoke them

## Customization

You can customize agents in your project by:
1. Copying to `.claude/agents/`
2. Modifying for your needs
3. The local version takes precedence

## Installation

Agents are installed automatically when you run:

**PowerShell (Windows):**
```powershell
installers\install.ps1
```

**Bash (macOS/Linux):**
```bash
bash installers/install.sh
```

They're copied to `.claude/agents/` in your project.
