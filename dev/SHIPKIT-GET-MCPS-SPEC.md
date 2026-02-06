# shipkit-get-mcps Specification

**Purpose:** Discover and install MCP servers with token budget awareness.

---

## Core Concept

MCPs (Model Context Protocol servers) add tools and capabilities to Claude, but each one costs context tokens (5k-20k). This skill helps users discover MCPs, understand their token cost, and install them to `.mcp.json`.

---

## Why This Skill Exists

| Without Skill | With Skill |
|---------------|------------|
| User must know MCP ecosystem | User says "I need database access" |
| User manually edits .mcp.json | Claude handles config |
| No visibility into token costs | Budget displayed before install |
| No discovery mechanism | Search MCP Registry + web |

The value is **discovery + budget awareness**.

---

## Triggers

| Trigger | Action |
|---------|--------|
| `/get-mcps` | Interactive menu |
| `/get-mcps <query>` | Search for specific MCP |
| `/get-mcps budget` | Show current token usage |
| "Is there an MCP for Postgres?" | Search and present |
| "What MCPs are available?" | Show popular/recommended |

---

## Workflow

### Step 1: Understand Intent

```
User: I need to interact with my Supabase database

Claude: I can search for MCPs that provide Supabase integration.
        Want me to look?
```

### Step 2: Search

Options:
- Query MCP Registry API: `registry.modelcontextprotocol.io`
- Web search: `"MCP server supabase site:github.com"`

### Step 3: Present Results with Token Costs

```
Found 2 MCPs for "supabase":

  [1] @supabase/mcp-server (~8k tokens)
      Official Supabase MCP - database queries, auth, storage
      Source: npm

  [2] supabase-mcp (~6k tokens)
      Community Supabase integration - queries only
      Source: github.com/user/supabase-mcp

Your current MCP budget:
  context7      ~5k tokens
  ─────────────────────────
  Total         ~5k tokens (2.5% of 200k)

Install one? Enter number or [s] to search again
```

### Step 4: Install

```
User: 1

Claude: Installing @supabase/mcp-server...

Adding to .mcp.json:
  "supabase": {
    "command": "npx",
    "args": ["-y", "@supabase/mcp-server"]
  }

✓ Added to .mcp.json

⚠ Restart Claude Code to activate the new MCP.

New budget:
  context7      ~5k tokens
  supabase      ~8k tokens
  ─────────────────────────
  Total         ~13k tokens (6.5% of 200k)
```

---

## Commands

| Command | Description |
|---------|-------------|
| `/get-mcps` | Interactive discovery |
| `/get-mcps <query>` | Search by keyword |
| `/get-mcps list` | Show installed MCPs |
| `/get-mcps budget` | Show token usage breakdown |
| `/get-mcps remove <name>` | Remove MCP from config |

---

## Discovery Sources

| Source | Method | Reliability |
|--------|--------|-------------|
| **MCP Registry** | API call to registry.modelcontextprotocol.io | High (official) |
| **Web search** | Search GitHub, mcp.so, mcpservers.org | Medium (broader) |
| **Shipkit manifest** | Local recommended list | High (curated) |

Priority: Shipkit manifest → MCP Registry → Web search

---

## Token Budget Display

```
/get-mcps budget

━━━━━━━━━━━━━━━━━━━━━━━━━━━
MCP Token Budget
━━━━━━━━━━━━━━━━━━━━━━━━━━━

Installed MCPs:
  context7        ~5k tokens
  playwright      ~13.7k tokens
  supabase        ~8k tokens
  ─────────────────────────────
  Total           ~26.7k tokens

Context budget:  200k tokens
MCP overhead:    ~13% of context

Tip: Disable unused MCPs in .mcp.json to reduce overhead.
```

---

## Skill Definition

```yaml
---
name: shipkit-get-mcps
description: Discover and install MCP servers with token budget awareness
invoke: user
model: haiku
tools:
  - Bash
  - Read
  - Write
  - WebFetch
  - WebSearch
---
```

---

## Installation Logic

### Adding to .mcp.json

```python
# Pseudo-code
def install_mcp(name, package, args):
    config_path = ".mcp.json"

    # Read existing config
    if exists(config_path):
        config = read_json(config_path)
    else:
        config = {"mcpServers": {}}

    # Check if already installed
    if name in config["mcpServers"]:
        return "Already installed"

    # Handle Windows npx wrapper
    if platform == "Windows" and command == "npx":
        entry = {"command": "cmd", "args": ["/c", "npx"] + args}
    else:
        entry = {"command": "npx", "args": args}

    config["mcpServers"][name] = entry
    write_json(config_path, config)

    return "Installed"
```

---

## Edge Cases

### No .mcp.json Exists

```
No .mcp.json found. Create one?

This file configures MCP servers for Claude Code.

[y] Yes, create  [n] Cancel
```

Creates:
```json
{
  "mcpServers": {}
}
```

### MCP Already Installed

```
supabase is already installed.

Current config:
  command: npx
  args: ["-y", "@supabase/mcp-server"]

[u] Update args  [r] Remove  [b] Back
```

### High Token Budget Warning

```
⚠ Warning: This will bring your MCP overhead to ~45k tokens (22% of context).

High MCP usage can reduce available context for conversations.

Consider:
  - Removing unused MCPs
  - Using MCPs only when needed (disable in .mcp.json)

[y] Install anyway  [n] Cancel
```

### Prerequisites Required

```
⚠ playwright MCP requires browser binaries.

Run this first:
  npx playwright install

Then run /get-mcps install playwright again.

[c] Continue anyway  [b] Back
```

---

## What This Skill Does NOT Do

- **Manage skills** → Use `/get-skills` instead
- **Start/stop MCPs** → Claude Code handles this
- **Debug MCP issues** → Manual troubleshooting

---

## Success Metrics

1. **Easy discovery** — User describes need, finds MCPs
2. **Budget awareness** — Token costs visible before install
3. **Safe installs** — Prerequisites checked, warnings shown
4. **Clean config** — .mcp.json stays valid

---

## Open Questions

1. **Token estimation** — How accurate can we be?
   - Could read from manifest or estimate from tool count
   - Recommendation: Use approximate ranges (~5k, ~10k, ~20k)

2. **MCP Registry API** — Is it stable enough to rely on?
   - v0.1 frozen as of Oct 2025
   - Recommendation: Use it, fall back to web search

3. **Disabled MCPs** — Show them separately?
   - Recommendation: Yes, show as "disabled" with option to re-enable

---

## Relationship to Other Skills

| Skill | Relationship |
|-------|--------------|
| `shipkit-get-skills` | Sibling — skills are separate ecosystem |
| `shipkit-project-status` | Could show MCP budget in status |
| `shipkit-codebase-index` | MCPs might be noted in index |
