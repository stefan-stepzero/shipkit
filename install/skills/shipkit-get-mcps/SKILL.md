---
name: shipkit-get-mcps
description: Discover and install MCP servers for enhanced Claude capabilities
argument-hint: "<search query>"
allowed-tools:
  - Bash
  - Read
  - Write
  - WebFetch
  - WebSearch
---

# shipkit-get-mcps - MCP Discovery & Installation

**Purpose**: Discover and install MCP (Model Context Protocol) servers to extend Claude's capabilities.

**Core value**: User knows to ask — Claude handles discovery and installation.

---

## Why This Skill Exists

**You don't naturally know what MCPs exist or that they could help.**

| Without Skill | With Skill |
|---------------|------------|
| User doesn't know MCPs exist | User invokes `/get-mcps` |
| User manually searches, edits config | Claude searches, presents options, installs |
| User misses useful capabilities | Claude suggests relevant MCPs |

---

## When to Invoke

**User says:**
- "Get MCPs for database"
- "Is there an MCP for Playwright?"
- "I need browser automation"
- "Find MCPs", "Search MCPs"
- "Add an MCP for Supabase"
- "What MCPs are available?"
- "Show me popular MCPs"
- "Recommend an MCP"

**Auto-suggest when:**
- User struggles with a task that an MCP could help with
- User asks about external service integration

**For catalog questions:** Load `references/popular-mcps.md` and present options.

---

## Prerequisites

**Required:**
- Node.js installed (most MCPs use npx)
- Internet connection for discovery

**Not required:**
- No manifest or registry account needed
- Claude searches on behalf of user

---

## Process

### Step 1: Understand Need

When user mentions a need:

```
User: I need to interact with my database

Claude: I can search for MCPs that provide database integration.
        What database are you using? (Postgres, Supabase, MongoDB, etc.)
```

If user invokes directly with query:
```
User: /get-mcps supabase

→ Skip to Step 2
```

---

### Step 2: Find MCPs

**First, check the curated catalog:**
→ Read `references/popular-mcps.md` for common MCPs (databases, browsers, dev tools, etc.)

**If user asks "what's available" or wants to browse:**
→ Present options from the catalog grouped by category

**If not in catalog, search these sources:**

1. **MCP Registry** (official)
   ```
   WebFetch: registry.modelcontextprotocol.io
   ```

2. **mcp.so** (community directory)
   ```
   WebSearch: "<query> MCP server site:mcp.so"
   ```

3. **mcpservers.org** (curated collection)
   ```
   WebSearch: "<query> site:mcpservers.org"
   ```

4. **GitHub** (source repos)
   ```
   WebSearch: "<query> MCP server site:github.com"
   ```

---

### Step 3: Present Options

Format results clearly:

```
Found 2 MCPs for "supabase":

  [1] @supabase/mcp-server (official)
      Database queries, auth, storage, realtime
      Source: npm

  [2] supabase-mcp (community)
      Lightweight Supabase integration
      Source: github.com/user/supabase-mcp

Install one? Enter number, or [s] to search again
```

---

### Step 4: Install Selected MCP

**Read current config:**
```bash
cat .mcp.json 2>/dev/null || echo "{}"
```

**Add new MCP entry:**

For Unix/Mac:
```json
{
  "mcpServers": {
    "supabase": {
      "command": "npx",
      "args": ["-y", "@supabase/mcp-server"]
    }
  }
}
```

For Windows (detect via platform):
```json
{
  "mcpServers": {
    "supabase": {
      "command": "cmd",
      "args": ["/c", "npx", "-y", "@supabase/mcp-server"]
    }
  }
}
```

**Write updated config:**
- Merge with existing mcpServers
- Preserve other MCPs
- Validate JSON before writing

---

### Step 5: Post-Install

```
✓ Added supabase to .mcp.json

⚠ Restart Claude Code to activate the new MCP.

The MCP will be available after restart. You'll have access to:
  - Database query tools
  - Auth management
  - Storage operations
```

---

### Step 6: Handle Edge Cases

#### MCP requires prerequisites

```
⚠ playwright MCP requires browser binaries.

Run this first:
  npx playwright install

Then restart Claude Code.
```

#### No .mcp.json exists

```
No .mcp.json found. Creating one...

✓ Created .mcp.json with supabase MCP
```

Create minimal config:
```json
{
  "mcpServers": {
    "supabase": { ... }
  }
}
```

#### MCP already installed

```
supabase is already in .mcp.json

Current config:
  command: npx
  args: ["-y", "@supabase/mcp-server"]

[u] Update args  [r] Remove  [b] Back
```

#### No results found

```
No MCPs found for "quantum computing".

Try:
  - Broader terms: "database", "api", "automation"
  - Check mcp.so directly: https://mcp.so
  - The capability might not have an MCP yet
```

---

## Commands

| Command | Description |
|---------|-------------|
| `/get-mcps` | Interactive discovery prompt |
| `/get-mcps <query>` | Search by keyword |
| `/get-mcps list` | Show installed MCPs from .mcp.json |
| `/get-mcps remove <name>` | Remove MCP from config |

---

## Discovery Sources

| Source | URL | Type |
|--------|-----|------|
| MCP Registry | registry.modelcontextprotocol.io | Official |
| mcp.so | mcp.so | Community |
| mcpservers.org | mcpservers.org | Curated |
| GitHub | github.com (search) | Source repos |

---

## Platform Detection

Detect platform and adjust config:

```
Windows:
  command: "cmd"
  args: ["/c", "npx", "-y", "<package>"]

Unix/Mac:
  command: "npx"
  args: ["-y", "<package>"]
```

Check platform via environment or ask user if unclear.

---

## Context Files This Skill Reads

- `.mcp.json` — Current MCP configuration

---

## Context Files This Skill Writes

- `.mcp.json` — Add/update MCP entries

**Write Strategy: MERGE**
- Read existing config
- Add new MCP to mcpServers
- Preserve existing MCPs
- Write back

---

## When This Skill Integrates with Others

### Relationship: Standalone Utility

This skill operates independently. It helps users extend Claude's capabilities.

**Complements:**
- `/shipkit-project-status` — Could suggest useful MCPs
- `/shipkit-project-context` — Stack detection might suggest MCPs

**Sibling:**
- `/shipkit-get-skills` — Same pattern for skill discovery

---

<!-- SECTION:after-completion -->
## After Completion

**Guardrails Check:** Before moving to next task, verify:

1. **Persistence** - Has important context been saved to `.shipkit/`?
2. **Prerequisites** - Does the next action need a spec or plan first?
3. **Session length** - Long session? Consider `/shipkit-work-memory` for continuity.

**Natural capabilities** (no skill needed): Implementation, debugging, testing, refactoring, code documentation.

**Suggest skill when:** User needs to make decisions, create persistence, or check project status.
<!-- /SECTION:after-completion -->

---

## Success Criteria

- [ ] User can discover MCPs through conversation
- [ ] Search covers official and community sources
- [ ] Installation handles platform differences
- [ ] Restart reminder always shown
- [ ] Prerequisites flagged when known