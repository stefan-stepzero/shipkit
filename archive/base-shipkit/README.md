# Archived: Base Shipkit (Full Framework)

**Archived Date:** January 2026

This folder contains the original full Shipkit framework components that have been deprecated in favor of **Shipkit Light**.

## Why Archived?

Shipkit Light provides a streamlined, focused approach that covers the essential product development workflow without the complexity of the full framework. Going forward, all repositories will use Shipkit Light exclusively.

## What's Here

### Skills (25 total)
- **dev-*** (11 skills): Development workflow skills
  - constitution, discussion, finish, implement, plan, progress, roadmap, specify, systematic-debugging, tasks, writing-skills
- **prod-*** (12 skills): Product management skills
  - assumptions-and-risks, brand-guidelines, communicator, constitution-builder, discussion, interaction-design, jobs-to-be-done, market-analysis, personas, strategic-thinking, success-metrics, user-stories
- **shipkit-*** (2 skills): Master orchestration
  - shipkit-master, shipkit-status

### Agents (6 total)
- any-researcher-agent.md
- dev-architect-agent.md
- dev-implementer-agent.md
- dev-reviewer-agent.md
- prod-product-designer-agent.md
- prod-product-manager-agent.md

### Configuration
- `profiles/default.manifest.json` - Full Shipkit skill manifest
- `settings/default.settings.json` - Full Shipkit permissions
- `claude-md/default.md` - Full Shipkit project instructions
- `hooks/session-start.py` - Full Shipkit session hook
- `hooks/suggest-next-skill.py` - Full Shipkit workflow hook

### Workspace
- `workspace/` - Skill output templates and scripts for the full framework

## Restoration

If you need to restore the full Shipkit framework:

1. Copy contents from `archive/base-shipkit/` back to `install/`
2. Use the `default.manifest.json` profile during installation
3. Install with the default settings

## Shipkit Light

The active framework is now **Shipkit Light**, located in `install/` with all `lite-*` prefixed components.

See `install/profiles/lite.manifest.json` for the active skill manifest.
