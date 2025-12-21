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
- Verify skills syntax matches current spec
- Ensure agent persona format is correct
- Validate hook patterns are supported
- Confirm settings.json schema is current

**When uncertain about Claude Code features:**
- Don't guess or assume
- Check the official documentation first
- Test in a real Claude Code environment
- Ask the user if documentation is unclear

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

#