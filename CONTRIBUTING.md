# Contributing to Shipkit

Thank you for your interest in contributing to Shipkit! This document provides guidelines for contributing.

## Ways to Contribute

### 1. Report Bugs

Found a bug? Please open an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Claude Code version)

### 2. Suggest Features

Have an idea? Open a feature request issue with:
- Clear description of the feature
- Use case / problem it solves
- Any implementation ideas

### 3. Propose New Skills

Skills are the core of Shipkit. To propose a new skill:

1. **Check the Skill Value Test** — Does it pass?
   - Forces human decisions to be explicit? (vision, trade-offs, priorities)
   - Creates persistence Claude lacks? (memory that survives sessions)
   - If Claude does it well without instruction, it's a natural capability, not a skill

2. **Open an issue** using the "New Skill Proposal" template

3. **Include:**
   - Skill name (use `shipkit-` prefix)
   - Problem it solves
   - What context it reads/writes
   - Why it's not a natural capability

### 4. Submit Pull Requests

#### For Bug Fixes
1. Fork the repo
2. Create a branch: `fix/description`
3. Make your changes
4. Submit PR with description of the fix

#### For New Skills
1. Fork the repo
2. Create a branch: `skill/skill-name`
3. Create skill in `install/skills/shipkit-[name]/`
4. Follow the skill structure (see below)
5. Update `install/profiles/shipkit.manifest.json`
6. Submit PR

## Skill Structure

Every skill must have:

```
install/skills/shipkit-[name]/
└── SKILL.md
```

### SKILL.md Requirements

```markdown
---
name: shipkit-[name]
description: "One-line description with trigger phrases"
---

# shipkit-[name] - Title

**Purpose**: What problem this skill solves

---

## When to Invoke
[Trigger conditions]

## Prerequisites
[Required context files]

## Process
[Step-by-step process]

## Success Criteria
[How to know it's complete]

## Context Files This Skill Reads
[List of files]

## Context Files This Skill Writes
[List of files with write strategy: CREATE, APPEND, REPLACE]
```

### Skill Quality Checklist

Before submitting:
- [ ] Passes the Skill Value Test (not a natural capability)
- [ ] Has clear trigger conditions
- [ ] Documents prerequisites
- [ ] Documents context files read/written
- [ ] Has success criteria
- [ ] Uses `shipkit-` prefix
- [ ] Added to manifest.json

## Development Setup

1. Clone the repo
2. Test installation in a scratch project:
   ```bash
   mkdir test-project && cd test-project
   python ../shipkit/installers/install.py
   ```
3. Make changes to skills/agents
4. Re-run installer to test

## Code Style

- **Skills**: Follow existing SKILL.md patterns
- **Python**: Follow PEP 8
- **Markdown**: Use consistent headers and formatting

## Questions?

Open an issue with the "question" label.

---

Thank you for contributing to Shipkit!
