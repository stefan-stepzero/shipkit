# shipkit-extensions Specification

**Purpose:** Post-install manager for MCPs and skills. Browse, compare installed vs available, and install new extensions from a curated manifest.

---

## Core Concept

After initial Shipkit installation, users may want to add more MCPs or skills. This skill provides a unified interface to:

1. See what's installed
2. Browse what's available
3. Install new extensions
4. Understand token costs (for MCPs)

---

## Two Extension Types

| Type | What It Is | Installed To | Token Impact |
|------|------------|--------------|--------------|
| **MCP** | Model Context Protocol server | `.mcp.json` | Yes (~5k-20k per MCP) |
| **Skill** | Slash command / workflow | `.claude/skills/<name>/` | Minimal (loaded on-demand) |

---

## Data Sources

### Stock Manifest

The skill reads from `shipkit.manifest.json` which contains:

```json
{
  "mcps": {
    "recommended": [
      {
        "name": "context7",
        "command": "npx",
        "args": ["-y", "@upstash/context7-mcp@latest"],
        "purpose": "Documentation lookup for libraries",
        "tokens": "~5k"
      },
      {
        "name": "playwright",
        "command": "npx",
        "args": ["@playwright/mcp@latest"],
        "purpose": "E2E testing, cross-browser automation",
        "tokens": "~13.7k",
        "prereq": "npx playwright install"
      }
    ]
  },
  "skills": {
    "definitions": ["shipkit-master", "shipkit-spec", ...],
    "optional": [
      {
        "name": "shipkit-advanced-debugging",
        "purpose": "Deep debugging workflows",
        "source": "bundled"
      }
    ]
  }
}
```

### Installed State

**MCPs:** Read from `.mcp.json`
**Skills:** Read from `.claude/skills/` directory

---

## Triggers

| Trigger | Action |
|---------|--------|
| `/extensions` | Show interactive menu |
| `/shipkit-extensions` | Same as above |
| `/extensions mcps` | Show MCP list only |
| `/extensions skills` | Show skills list only |
| `/extensions install <name>` | Install specific extension |
| "What MCPs are available?" | Show MCP list |
| "Install playwright" | Install specific MCP |

---

## Interactive Flow

### Step 1: Show Menu

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Shipkit Extensions
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

What would you like to do?

  [1] Browse MCPs (Model Context Protocol servers)
  [2] Browse Skills (slash commands)
  [3] Show installed extensions
  [4] Check for updates
```

### Step 2a: Browse MCPs

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Available MCPs
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  ✓ context7        - Documentation lookup (~5k tokens)
  ✓ playwright      - E2E testing, cross-browser (~13.7k tokens)
    chrome-devtools - Performance debugging (~19k tokens)

  ✓ = installed

Token budget note: Each MCP adds to your context usage.
Current: ~18.7k tokens used by MCPs

Enter number to install, or [b] Back
```

### Step 2b: Browse Skills

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Available Skills
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Installed (19):
  shipkit-master, shipkit-spec, shipkit-plan, ...

Optional (not installed):
  [1] shipkit-advanced-debugging - Deep debugging workflows
  [2] shipkit-competitive-analysis - Market research

Enter number to install, or [b] Back
```

### Step 3: Install Confirmation

```
Install chrome-devtools MCP?

  Purpose: Performance debugging, network analysis
  Tokens: ~19k added to context

  ⚠ This will increase your MCP token usage to ~37.7k

  [y] Yes, install  [n] Cancel
```

### Step 4: Install & Post-Install

```
✓ Added chrome-devtools to .mcp.json

Restart Claude Code to activate the new MCP.

Usage tips:
  - Use for performance traces and Core Web Vitals
  - Deep network request inspection
  - Console error analysis
```

---

## Installation Logic

### Installing an MCP

1. Read current `.mcp.json`
2. Add new MCP entry to `mcpServers`
3. Write updated `.mcp.json`
4. Check for prerequisites
5. Show post-install instructions

```python
# Pseudo-code
def install_mcp(name, manifest):
    mcp = find_mcp_in_manifest(name)

    current = read_json(".mcp.json")

    if name in current["mcpServers"]:
        return "Already installed"

    # Handle Windows npx wrapper
    if platform == "Windows" and mcp["command"] == "npx":
        entry = {"command": "cmd", "args": ["/c", "npx"] + mcp["args"]}
    else:
        entry = {"command": mcp["command"], "args": mcp["args"]}

    current["mcpServers"][name] = entry
    write_json(".mcp.json", current)

    if mcp.get("prereq"):
        print(f"⚠ Run this first: {mcp['prereq']}")

    return "Installed"
```

### Installing a Skill

1. Check if skill exists in bundled skills
2. Copy skill folder to `.claude/skills/<name>/`
3. Show usage instructions

```python
# Pseudo-code
def install_skill(name, source_dir):
    skill_src = source_dir / "skills" / name
    skill_dest = Path(".claude/skills") / name

    if skill_dest.exists():
        return "Already installed"

    shutil.copytree(skill_src, skill_dest)

    return "Installed"
```

---

## Token Budget Display

MCPs have significant token costs. The skill should help users understand their budget:

```
Current MCP Token Usage
━━━━━━━━━━━━━━━━━━━━━━━

  context7        ~5k tokens
  playwright      ~13.7k tokens
  ─────────────────────────
  Total           ~18.7k tokens

Context budget: 200k tokens
MCP overhead:   ~9% of context

Tip: Disable unused MCPs in .mcp.json to reduce overhead.
```

---

## Skill Definition

```yaml
---
name: shipkit-extensions
description: Browse and install MCPs and skills
invoke: user
model: haiku
tools:
  - Read
  - Write
  - Glob
  - Bash  # For checking prerequisites
---
```

---

## Commands

| Command | Description |
|---------|-------------|
| `/extensions` | Interactive menu |
| `/extensions list` | Show all installed |
| `/extensions mcps` | Browse MCPs |
| `/extensions skills` | Browse skills |
| `/extensions install <name>` | Install by name |
| `/extensions remove <name>` | Remove extension |
| `/extensions budget` | Show token usage |

---

## Edge Cases

### MCP Already Installed

```
chrome-devtools is already installed.

Current config in .mcp.json:
  command: npx
  args: chrome-devtools-mcp@latest

[r] Reinstall  [u] Update to latest  [b] Back
```

### Prerequisite Not Met

```
⚠ playwright requires browser binaries.

Run this command first:
  npx playwright install

Then run /extensions install playwright again.

[c] Continue anyway (may not work)  [b] Back
```

### No .mcp.json Exists

```
No .mcp.json found. Create one?

This file configures MCP servers for Claude Code.

[y] Yes, create  [n] Cancel
```

Creates minimal:
```json
{
  "mcpServers": {}
}
```

### Skill Source Not Found

```
Skill 'shipkit-advanced-debugging' not found in bundled skills.

This skill may be:
  - Part of a different Shipkit edition
  - A community skill (not yet supported)
  - Misspelled

Available skills: [list]
```

---

## Future: Community Extensions

The manifest could support external sources:

```json
{
  "mcps": {
    "recommended": [...],
    "community": [
      {
        "name": "supabase",
        "source": "npm:@supabase/mcp",
        "purpose": "Supabase database integration",
        "tokens": "~8k"
      }
    ]
  }
}
```

For v1, stick to bundled extensions only.

---

## Files Modified

| File | Action |
|------|--------|
| `.mcp.json` | Add/remove MCP entries |
| `.claude/skills/<name>/` | Copy skill folders |

---

## Success Metrics

1. **Easy discovery** — Users can see what's available
2. **Informed decisions** — Token costs visible before install
3. **Safe installs** — Prerequisites checked, confirmations required
4. **Clean uninstall** — Can remove extensions cleanly

---

## Relationship to Installer

| Installer | shipkit-extensions |
|-----------|-------------------|
| Runs once at setup | Runs anytime post-install |
| Interactive prompts | Skill-based interface |
| Copies all bundled skills | Adds optional/missing extensions |
| Creates initial .mcp.json | Modifies existing .mcp.json |

They share the same manifest as source of truth.

---

## Open Questions

1. **Community extensions** — Should we support npm/GitHub sources in v1?
   - Recommendation: No, keep v1 simple (bundled only)

2. **Update checking** — Should skill check for newer versions?
   - Recommendation: Show "check for updates" but don't auto-update

3. **Disable vs Remove** — Should MCPs be disabled (commented) or removed?
   - Recommendation: Remove for simplicity, user can re-add

4. **Skill dependencies** — Some skills might depend on others
   - Recommendation: Document dependencies, don't enforce in v1
