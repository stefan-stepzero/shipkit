# Shipkit Development Instructions

**You are developing the shipkit framework - an architectural layer on top of Claude Code.**

This repo contains shipkit: a complete product development framework delivered as Claude Code skills, agents, and constitutions.

**Core Principle:** Shipkit extends Claude Code with structured workflows. All development must align with official Claude Code documentation and patterns.

---

## What is Shipkit?

**Shipkit = Claude Code + Structured Product Workflow**

Claude Code provides:
- Skills system (slash commands)
- Agent personas (subagent contexts)
- MCP servers
- Hooks
- Settings & permissions

Shipkit adds:
- 37 pre-built skills (product discovery → implementation)
- 5 specialized agent personas
- Constitution templates (project rules)
- Unified workspace structure (`.shipkit/`)
- Specification-driven development workflow

**We build ON TOP of Claude Code, not alongside it.**

---

## Development Principles

### 1. Always Align with Claude Code Documentation

**Before implementing ANY feature:**
- Check official Claude Code docs: `https://docs.anthropic.com/claude/docs/claude-code`
- Check local best practices: `Claude Code Best practise/claude-code-references/`
- Verify skills syntax matches current spec
- Ensure agent persona format is correct
- Validate hook patterns are supported
- Confirm settings.json schema is current

**When uncertain about Claude Code features:**
- Don't guess or assume
- Check `claude-code-best-practices/REFERENCES-BEST-PRACTICES.md` FIRST (primary reference)
- Check `claude-code-best-practices/` folder for additional materials
- Check the official documentation
- Test in a real Claude Code environment
- Ask the user if documentation is unclear

**Primary Reference:** `claude-code-best-practices/REFERENCES-BEST-PRACTICES.md`
- **Read this FIRST when creating or modifying skills**
- Extracted best patterns from Obra (methodology) and Speckit (quality enforcement)
- Documents Shipkit's hybrid approach and innovations
- Includes quick reference cheat sheets and pattern selection guide

**Reference folder:** `claude-code-best-practices/` contains:
- **REFERENCES-BEST-PRACTICES.md** - PRIMARY REFERENCE (start here)
- **BUILDING-LITE-SKILLS.md** - LITE SKILL QUALITY GUIDE (creating/editing lite skills)
- Official Claude Code documentation extracts
- Skill authoring best practices
- Agent persona guidelines
- Comparative analysis (shipkit vs speckit vs obra)
- Source repositories (obra-repo/, speckit/)

**When creating or editing Lite skills:**
- **MUST READ**: `claude-code-best-practices/BUILDING-LITE-SKILLS.md`
- Covers 7-file integration system (manifest, hooks, routing, etc.)
- Defines quality standards (cross-references, checklists, Iron Laws, etc.)
- Production-ready = Integration (7 files) + Quality (Part 10)
- DO NOT skip quality standards - they ensure causality, discoverability, and maintainability

### 2. Shipkit is a Layer, Not a Fork

**What this means:**
- ✅ We create skills that work with Claude Code
- ✅ We provide agent personas Claude Code loads
- ✅ We supply constitutions Claude Code reads
- ✅ We organize workflows using Claude Code primitives
- ❌ We don't modify Claude Code itself
- ❌ We don't bypass Claude Code features
- ❌ We don't create parallel systems

**Example:**
- **Right:** Create a `/specify` skill that uses Claude Code's skill system
- **Wrong:** Build a custom command parser outside Claude Code

### 3. Use Simple File Operations - Don't Overcomplicate

**CRITICAL: When editing files, use the simplest available tool.**

**For file edits:**
1. **Read** the file first (required before Write)
2. **Write** the file with new content
3. Done.

**DO NOT:**
- ❌ Use complex bash heredocs or cat commands
- ❌ Use Python scripts for simple file writes
- ❌ Create temporary files and copy them
- ❌ Use sed/awk when Write tool is simpler
- ❌ Overthink the operation

**Right:** `Read(file.md)` then `Write(file.md, new_content)`

**Wrong:** Complex bash heredocs, Python scripts, temp files

**Exception:** Bash IS appropriate for git, tests, builds, system operations.

**If you catch yourself writing complex bash for a simple file edit, STOP and use Read + Write instead.**

---

## Working Documents - Where to Create and Find Tracking Documents

### What Are Working Documents?

Working documents are files Claude Code creates to track:
- Implementation progress and status
- Migration plans and restructuring efforts
- Skill completion references
- Architecture decision records
- Development plans and specifications
- Task breakdowns and checklists
- Any other documents created to organize, plan, or track work

### Where to Create Working Documents

**ALWAYS create working documents in:**
```
claude-working-documents/
```

**Examples of working documents:**
- `RESTRUCTURING-PLAN.md` - Track skill migration progress
- `DEV-SKILLS-COMPLETE-REFERENCE.md` - Skill implementation reference
- `DEV-FINISH-IMPLEMENTATION.md` - Specific skill implementation notes
- `MIGRATION-STATUS.md` - Migration tracking
- `IMPLEMENTATION-NOTES.md` - Development notes
- `ARCHITECTURE-DECISIONS.md` - ADR documents

### When to Create Working Documents

Create a working document in `Claude Working Documents/` when:
1. The user asks to "track progress" or "create a plan"
2. You need to document implementation status across multiple sessions
3. You're tracking a multi-step migration or restructuring
4. You need a reference document for completed work
5. You're documenting architecture decisions
6. You're breaking down a large task into phases

### Naming Convention

Use UPPERCASE-WITH-HYPHENS.md for working documents:
- ✅ `SKILL-MIGRATION-PLAN.md`
- ✅ `PROD-SKILLS-STATUS.md`
- ✅ `IMPLEMENTATION-NOTES.md`
- ❌ `notes.md` (too vague)
- ❌ `temp.md` (unclear purpose)

### Where to Look for Working Documents

**ALWAYS check `claude-working-documents/` FIRST when:**
1. The user references a "plan" or "status document"
2. You need to check implementation progress
3. You're resuming work from a previous session
4. The user asks "what's the status of X"
5. You need context about completed or in-progress work

**Example:**
```
User: "What's the status of the dev skills migration?"
You: [Check claude-working-documents/RESTRUCTURING-PLAN.md first]
```

### What NOT to Put in Working Documents

**Don't create working documents for:**
- Temporary scratch notes (use memory)
- Single-session todos (use TodoWrite tool)
- User-facing documentation (goes in appropriate docs/ folder)
- Code or implementation files (goes in src/, lib/, etc.)
- Product artifacts (goes in .shipkit/skills/*/outputs/)

**Keep `claude-working-documents/` focused on tracking and planning documents only.**

---

      IMPORTANT: this context may or may not be relevant to your tasks. You should not respond to this context unless it is highly relevant to your task.
