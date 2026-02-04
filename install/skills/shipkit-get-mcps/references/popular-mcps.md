# Popular MCP Servers

Reference catalog of popular and official MCP servers for Claude Code.

**Load this file when user asks:** "what MCPs are available", "show me popular MCPs", "list MCPs", "recommend an MCP"

---

## Quick Install

```json
// Add to .mcp.json
{
  "mcpServers": {
    "server-name": {
      "command": "npx",
      "args": ["-y", "@package/name"]
    }
  }
}
```

**Windows:** Use `"command": "cmd", "args": ["/c", "npx", "-y", "@package/name"]`

---

## Recommended MCPs

High-value MCPs that enhance Claude's capabilities significantly:

| MCP | Purpose | Install Package |
|-----|---------|-----------------|
| **filesystem** | Read/write files with access controls | `@modelcontextprotocol/server-filesystem` |
| **postgres** | Query PostgreSQL databases | `@modelcontextprotocol/server-postgres` |
| **playwright-mcp** | Browser automation (Microsoft official) | `@anthropic/mcp-server-playwright` |
| **memory** | Persistent knowledge graph memory | `@modelcontextprotocol/server-memory` |
| **fetch** | Web content fetching for LLM use | `@modelcontextprotocol/server-fetch` |

---

## Official Reference Servers

From [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers):

| MCP | Description | Package |
|-----|-------------|---------|
| **everything** | Reference/test server with all features | `@modelcontextprotocol/server-everything` |
| **fetch** | Web content fetching and conversion | `@modelcontextprotocol/server-fetch` |
| **filesystem** | Secure file operations | `@modelcontextprotocol/server-filesystem` |
| **git** | Read, search, manipulate git repos | `@modelcontextprotocol/server-git` |
| **memory** | Knowledge graph persistent memory | `@modelcontextprotocol/server-memory` |
| **sequential-thinking** | Dynamic problem-solving | `@modelcontextprotocol/server-sequential-thinking` |
| **time** | Time and timezone conversion | `@modelcontextprotocol/server-time` |

---

## By Category

### Databases

| MCP | Description | Package/Repo |
|-----|-------------|--------------|
| **postgres** | PostgreSQL with schema inspection | `@modelcontextprotocol/server-postgres` |
| **sqlite** | SQLite with analysis features | `@modelcontextprotocol/server-sqlite` |
| **supabase** | Supabase tables, config, data | `supabase-community/supabase-mcp` |
| **redis** | Redis data management and search | `@redis/mcp-server` |
| **mongodb** | MongoDB database operations | `mongodb-lens` |

### Browser Automation

| MCP | Description | Package/Repo |
|-----|-------------|--------------|
| **playwright** | Microsoft official, accessibility snapshots | `@anthropic/mcp-server-playwright` |
| **browserbase** | Cloud browser automation | `@browserbase/mcp-server-browserbase` |
| **browsermcp** | Local Chrome automation | `browsermcp/mcp` |
| **selenium** | Selenium WebDriver automation | `selenium-mcp-server` |

### Developer Tools

| MCP | Description | Package/Repo |
|-----|-------------|--------------|
| **jira** | Jira projects, issues, comments | `@aashari/mcp-server-atlassian-jira` |
| **confluence** | Confluence pages, spaces | `@aashari/mcp-server-atlassian-confluence` |
| **github** | GitHub repos, issues, PRs | `@modelcontextprotocol/server-github` |
| **buildkite** | CI/CD pipeline management | `@buildkite/mcp-server` |
| **circleci** | Fix CircleCI build failures | `@circleci/mcp-server` |
| **docker** | Docker Hub interactions | `@docker/hub-mcp` |

### Communication

| MCP | Description | Package/Repo |
|-----|-------------|--------------|
| **slack** | Slack DMs, channels, search | `jtalk22/slack-mcp-server` |
| **teams** | Microsoft Teams messaging | `@inditetech/mcp-teams-server` |
| **discord** | Discord server management | `discord-mcp-server` |
| **email** | Email sending/reading | Various implementations |

### Cloud & Infrastructure

| MCP | Description | Package/Repo |
|-----|-------------|--------------|
| **aws** | AWS service integration | `@awslabs/mcp` |
| **cloudflare** | Workers, KV, R2, D1 | `@cloudflare/mcp-server` |
| **terraform** | Provider discovery, modules | `@hashicorp/terraform-mcp-server` |
| **pulumi** | Infrastructure operations | `@pulumi/mcp-server` |
| **kubernetes** | K8s cluster management | `kubernetes-mcp-server` |

### Code Execution

| MCP | Description | Package/Repo |
|-----|-------------|--------------|
| **run-python** | Secure Python sandbox | `pydantic/mcp-run-python` |
| **run-js** | Secure JavaScript sandbox | `yepcode/mcp-server-js` |
| **container** | Containerized code execution | `dagger/container-use` |

### Productivity

| MCP | Description | Package/Repo |
|-----|-------------|--------------|
| **notion** | Notion pages and databases | `notion-mcp-server` |
| **linear** | Linear issues and projects | `linear-mcp-server` |
| **todoist** | Todoist task management | `todoist-mcp-server` |
| **google-drive** | Google Drive file access | `google-drive-mcp` |

---

## When to Suggest Each

| User Need | Suggest |
|-----------|---------|
| "Access my database" | `postgres`, `sqlite`, `supabase`, `mongodb` |
| "Automate browser" | `playwright` (recommended), `browserbase` |
| "Work with files" | `filesystem` |
| "Remember things across sessions" | `memory` |
| "Fetch web content" | `fetch` |
| "Git operations" | `git` |
| "Jira/Confluence" | `jira`, `confluence` |
| "Slack messages" | `slack` |
| "CI/CD pipelines" | `buildkite`, `circleci` |
| "AWS/cloud" | `aws`, `cloudflare`, `terraform` |
| "Run code safely" | `run-python`, `run-js` |

---

## Discovery Sources

| Source | URL | Description |
|--------|-----|-------------|
| Official Registry | registry.modelcontextprotocol.io | Official MCP registry |
| mcp.so | mcp.so | Community directory |
| mcpservers.org | mcpservers.org | Curated collection |
| awesome-mcp-servers | github.com/punkpeye/awesome-mcp-servers | Community list |
| mcp-awesome.com | mcp-awesome.com | Quality-verified list |

---

## Installation Patterns

### NPM Package (most common)
```json
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "POSTGRES_CONNECTION_STRING": "postgresql://..."
      }
    }
  }
}
```

### Python Package
```json
{
  "mcpServers": {
    "custom-python": {
      "command": "uvx",
      "args": ["mcp-server-custom"]
    }
  }
}
```

### Docker
```json
{
  "mcpServers": {
    "containerized": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "mcp-server-image"]
    }
  }
}
```

---

## Platform Notes

**Windows users:** Most npx-based MCPs need cmd wrapper:
```json
{
  "command": "cmd",
  "args": ["/c", "npx", "-y", "@package/name"]
}
```

**After adding MCP:** Restart Claude Code to activate.

---

*Sources: [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) | [awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers) | [MCP Registry](https://registry.modelcontextprotocol.io/)*
