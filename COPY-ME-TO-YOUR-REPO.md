# ShipKit Installation Instructions

**Instructions for Claude Code / LLM:**

When you see this file in a project, the user wants you to install the ShipKit framework (34 Claude Code skills for product development: DevKit + ProdKit + Agent Personas).

---

## Installation Method 1: Sibling Directory (Recommended)

**Use this method when the user has ShipKit in a folder alongside their project.**

```
Projects/
├── shipkit/           # ShipKit repository
└── their-project/     # User's project (you are here)
```

### Step 1: Ask for the ShipKit Location

Ask the user: **"Where is the ShipKit folder located relative to this project?"**

Common answers:
- "In the parent directory" → `../shipkit/`
- "Next to this project" → `../shipkit/`
- A specific path → Use exactly what they provide

### Step 2: Verify the Path

```bash
ls ../shipkit/install.sh
```

If the file exists, proceed. If not, ask for the correct path.

### Step 3: Run the Installer

```bash
bash ../shipkit/install.sh --preset solo
```

**Replace** `../shipkit/` with the actual path if different.

---

## Installation Method 2: Inside Project

**Use this method when the user has placed ShipKit inside their project folder.**

```
their-project/
├── shipkit/           # ShipKit repository (inside project)
├── src/
└── ...
```

### Step 1: Ask for the Folder Name

Ask the user: **"What did you name the ShipKit folder inside your project?"**

Common answers:
- "shipkit" → `./shipkit/`
- "claude-skills" → `./claude-skills/`
- A specific name → Use exactly what they provide

### Step 2: Verify the Path

```bash
ls ./shipkit/install.sh
```

### Step 3: Run the Installer

```bash
bash ./shipkit/install.sh --preset solo
```

**Note:** After installation, the user may want to add the ShipKit source folder to `.gitignore` since all necessary files are copied to `.claude/`, `.devkit/`, and `.prodkit/`.

---

## Installation Method 3: Direct from GitHub

**Coming Soon**

This method will allow one-command installation directly from GitHub without needing to download the repository first.

```bash
# COMING SOON - Not yet available
bash install.sh --github https://github.com/user/shipkit.git --preset solo
```

---

## Installation Presets

| Preset | Skills | Best For |
|--------|--------|----------|
| `--preset solo` | 34 skills + 5 agents | Solo developers (recommended) |
| `--all` | 34 skills + 5 agents | Teams, full infrastructure |
| `--devkit-only` | 23 skills + 5 agents | Already have product specs |
| `--prodkit-only` | 11 skills | Product discovery only |

**If the user doesn't specify, use `--preset solo`.**

---

## Verify Installation

After installation completes, confirm these directories were created:

```bash
ls -la .claude/skills/ .devkit/ .prodkit/ CLAUDE.md
```

You should see:
- `.claude/skills/` - Skill definitions (devkit/, prodkit/, meta/)
- `.claude/agents/` - 5 agent persona files
- `.devkit/` - DevKit workspace (specs, scripts, templates)
- `.prodkit/` - ProdKit workspace (discovery artifacts)
- `CLAUDE.md` - Session instructions

### Expected Output

```
Installation complete! ShipKit has been installed with 34 skills.

Installed:
  ✓ DevKit (23 skills)
  ✓ ProdKit (11 skills)
  ✓ Agent Personas (5 agents)
  ✓ Session hooks
  ✓ CLAUDE.md

Next steps:
  1. Start with /strategic-thinking (product discovery)
  2. Or jump to /specify (if you already have requirements)
```

---

## What Gets Installed

```
your-project/
│
├── CLAUDE.md                       # Project instructions
├── .claude/
│   ├── settings.json               # Hook configuration
│   ├── constitution.md             # Created by /constitution-builder
│   ├── agents/                     # 5 agent personas
│   │   ├── discovery-agent.md
│   │   ├── architect-agent.md
│   │   ├── implementer-agent.md
│   │   ├── reviewer-agent.md
│   │   └── researcher-agent.md
│   ├── hooks/                      # Session start scripts
│   └── skills/
│       ├── meta/                   # Meta-skill (enforcement)
│       ├── devkit/                 # 23 DevKit skills
│       └── prodkit/                # 11 ProdKit skills
│
├── .devkit/                        # DevKit workspace
│   ├── scripts/
│   ├── templates/
│   └── specs/
│
└── .prodkit/                       # ProdKit workspace
    ├── scripts/
    ├── templates/
    ├── strategy/
    ├── discovery/
    └── requirements/
```

---

## Quick Start After Installation

### Full Product Development
```
/strategic-thinking → /personas → /jobs-to-be-done → /market-analysis →
/user-stories → /constitution-builder --product → /specify → /plan →
/tasks → /implement
```

### Technical Feature Only
```
/constitution-builder --technical → /specify → /plan → /tasks → /implement
```

### Quick Implementation
```
/brainstorming → /using-git-worktrees → /implement → /finishing-a-development-branch
```

---

## Troubleshooting

### "install.sh not found"
The path to ShipKit is incorrect. Ask the user to verify where they placed the ShipKit folder.

### "Permission denied"
Run: `chmod +x /path/to/shipkit/install.sh`

### ".claude folder already exists"
The installer will merge with existing content. Existing skills won't be overwritten unless they're ShipKit skills.

---

## Framework Overview

**ShipKit** = DevKit (23 skills) + ProdKit (11 skills) + Agent Personas (5)

| Component | Purpose |
|-----------|---------|
| **DevKit** | Technical specs, implementation, TDD, code review |
| **ProdKit** | Product discovery, strategy, user research |
| **Agent Personas** | Specialized behaviors (Discovery, Architect, Implementer, Reviewer, Researcher) |

All 34 skills work 100% locally. No external APIs required.

Inspired by: [GitHub's Spec-Kit](https://github.com/github/spec-kit) | [obra's Superpowers](https://github.com/anthropics/claude-code-superpowers)
