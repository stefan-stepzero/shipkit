# Getting Started with Shipkit

A quick guide to installing Shipkit and using it for your first project.

---

## What is Shipkit?

Shipkit is a collection of **Claude Code skills** that help you build products faster. It provides:

- **Structured workflows** — Skills guide you from idea to shipped product
- **Persistent context** — Decisions survive between sessions in `.shipkit/` files
- **Best practices** — Built-in patterns for specs, plans, and architecture

**Key insight:** Claude is powerful but forgets everything between sessions. Shipkit solves this by capturing your decisions in files that persist.

---

## Installation

### Prerequisites

- Node.js 18+ (for npx)
- A project directory (new or existing)
- Claude Code CLI installed

### Install Shipkit

```bash
cd your-project
npx shipkit-dev init
```

Add `-y` for non-interactive mode with defaults: `npx shipkit-dev init -y`

The installer will:
1. Create `.claude/skills/` with all Shipkit skills
2. Create `.claude/agents/` with agent personas
3. Set up session hooks in `.claude/settings.json`
4. Create `.shipkit/` workspace directory
5. Generate `CLAUDE.md` with workflow instructions

### Verify Installation

After installation, your project should have:

```
your-project/
├── CLAUDE.md                    # Workflow guide (edit this!)
├── .claude/
│   ├── settings.json            # Permissions + hooks
│   ├── skills/                  # 23 skill definitions
│   ├── agents/                  # 7 agent personas
│   └── hooks/                   # Session hooks
└── .shipkit/                    # Your workspace (grows as you work)
```

---

## Your First Workflow

### 1. Start a New Session

Open Claude Code in your project directory. The session hook will automatically load Shipkit context.

### 2. Define Your Project Vision

```
/shipkit-why-project
```

This skill asks clarifying questions and creates `.shipkit/why.json` — the foundation for all future decisions.

### 3. Scan Your Codebase (if existing project)

```
/shipkit-project-context
```

This detects your tech stack and creates `.shipkit/stack.json`.

### 4. Create a Feature Spec

```
/shipkit-spec "Add user authentication"
```

Creates a specification in `.shipkit/specs/active/`. The spec captures:
- What you're building
- Acceptance criteria
- Technical approach

### 5. Plan the Implementation

```
/shipkit-plan
```

Creates an implementation plan referencing your spec.

### 6. Build It

Implementation is a **natural capability** — just ask Claude to build what's in the plan. No skill needed.

### 7. Verify Quality

```
/shipkit-verify
```

Checks your implementation against the spec and flags issues.

---

## Core Workflow

```
/shipkit-why-project       →  Define vision & constraints
        ↓
/shipkit-project-context   →  Scan codebase, detect stack
        ↓
/shipkit-spec              →  Create feature specification
        ↓
/shipkit-plan              →  Plan implementation steps
        ↓
(implement)                →  Build it (natural capability)
        ↓
/shipkit-verify            →  Verify quality
```

---

## Key Concepts

### Skills vs Natural Capabilities

**Skills** are for things Claude can't do well without guidance:
- Capturing human decisions (vision, trade-offs)
- Creating persistent context (architecture decisions)
- Enforcing workflows (spec → plan → implement)

**Natural capabilities** don't need skills:
- Debugging code
- Implementing features
- Writing tests
- Refactoring

### The `.shipkit/` Directory

All project context lives here:

| File | Purpose |
|------|---------|
| `why.json` | Vision, constraints, approach |
| `stack.json` | Tech choices (auto-scanned) |
| `architecture.json` | Decisions log (append-only) |
| `progress.json` | Session continuity |
| `specs/active/` | Feature specifications |
| `plans/` | Implementation plans |

**Commit these files!** They're the institutional memory of your project.

### Agent Personas

Shipkit includes 7 specialized agents:

| Agent | Use For |
|-------|---------|
| `shipkit-project-manager-agent` | Coordination, status, context |
| `shipkit-product-owner-agent` | Vision, requirements, priorities |
| `shipkit-ux-designer-agent` | UI/UX patterns, prototyping |
| `shipkit-architect-agent` | Technical decisions, stack choices |
| `shipkit-implementer-agent` | Code implementation |
| `shipkit-reviewer-agent` | Code review, quality checks |
| `shipkit-researcher-agent` | Research, troubleshooting |

---

## Common Tasks

### Check Project Status

```
/shipkit-project-status
```

Shows what context exists, what's missing, and suggests next steps.

### Log an Architecture Decision

```
/shipkit-architecture-memory
```

Appends a decision to `.shipkit/architecture.json` with rationale.

### Define Product Features

```
/shipkit-product-definition
```

Maps goals to a feature portfolio with dependency ordering and coverage analysis.

### End a Session

```
/shipkit-work-memory
```

Captures what you did and what's next for session continuity.

---

## Tips

1. **Always check context first** — Skills read `.shipkit/` files before making decisions
2. **Commit your context files** — They're the memory of your project
3. **Use specs for features** — Even small features benefit from a quick spec
4. **Let Claude implement** — Don't create skills for things Claude does well naturally
5. **Run `/shipkit-project-status` when stuck** — It shows gaps and suggests next steps

---

## Next Steps

- Read the [Skill Reference](skill-reference.md) for all available skills
- See [Examples](examples/) for complete workflow walkthroughs
- Check [Creating Skills](creating-skills.md) if you want to contribute

---

## Getting Help

- **In Claude Code:** `/help` shows available commands
- **Project status:** `/shipkit-project-status` shows gaps
- **Issues:** [GitHub Issues](https://github.com/user/shipkit/issues)
