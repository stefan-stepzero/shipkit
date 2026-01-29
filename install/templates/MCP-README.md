# MCP Server Configuration

Shipkit automatically configures **Context7 MCP server** during installation to keep your AI assistant up-to-date with the latest documentation.

---

## What is Context7?

**Context7** is an MCP (Model Context Protocol) server that fetches version-aware, current documentation from official sources and injects it into Claude's context when you need it.

**Package:** `@upstash/context7-mcp`
**Maintained by:** Upstash

---

## Why This Matters

Language models are trained on static data, which means suggestions can be:
- ❌ **Outdated** - Using older API versions or deprecated methods
- ❌ **Incorrect** - Hallucinating functions that don't exist
- ❌ **Generic** - Not reflecting the specific library version you're using

Context7 solves this by fetching **live, version-specific documentation** when you need it.

---

## How to Use Context7

Simply add `use context7` to any prompt where you want current documentation:

### Examples

```
Create a Next.js 14 app with server components. use context7
```

```
Write a Stripe webhook handler with signature validation. use context7
```

```
Build a Supabase query with RLS policies. use context7
```

```
Create a MongoDB aggregation pipeline. use context7
```

**What happens:** Context7 fetches the latest official docs for the mentioned technology and injects them into Claude's context, ensuring accurate, up-to-date responses.

---

## Configuration File

**Location:** `.mcp.json` (in your project root)

**Default configuration:**
```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp@latest"]
    }
  }
}
```

**On Windows with native (non-WSL) environment:** If you encounter issues, try wrapping with `cmd /c`:
```json
{
  "mcpServers": {
    "context7": {
      "command": "cmd",
      "args": ["/c", "npx", "-y", "@upstash/context7-mcp@latest"]
    }
  }
}
```

---

## Verifying Connection

**Check MCP server status:**
```
/mcp
```

This shows:
- All connected MCP servers
- Connection status
- Available tools from each server

**Test Context7:**
```
What tools does the context7 server provide?
```

---

## Adding More MCP Servers

You can add additional MCP servers to `.mcp.json`:

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp@latest"]
    },
    "your-server": {
      "type": "http",
      "url": "https://api.example.com/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_TOKEN"
      }
    }
  }
}
```

**Or use CLI:**
```bash
claude mcp add your-server --transport http https://api.example.com/mcp --scope project
```

---

## Troubleshooting

### Context7 not responding

**Check connection:**
```
/mcp
```

**Restart Claude Code:**
- Close and reopen Claude Code session
- MCP servers connect on startup

### Permission errors

If you see `EACCES` or permission errors:
```bash
# Clear npm cache
npm cache clean --force

# Try installing package first
npx @upstash/context7-mcp@latest
```

### Alternative runtimes

**Using Bun:**
```json
{
  "mcpServers": {
    "context7": {
      "command": "bunx",
      "args": ["-y", "@upstash/context7-mcp@latest"]
    }
  }
}
```

**Using Deno:**
```json
{
  "mcpServers": {
    "context7": {
      "command": "deno",
      "args": ["run", "--allow-net", "npm:@upstash/context7-mcp"]
    }
  }
}
```

---

## References

- [Context7 Installation Guide](https://apidog.com/blog/context7-mcp-server/)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Upstash Context7 Package](https://www.npmjs.com/package/@upstash/context7-mcp)

---

**Pro tip:** Add "use context7" to prompts in `/shipkit-integration-docs` skill to fetch latest security best practices for Stripe, Supabase, OpenAI, etc.
