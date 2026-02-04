# Community Skills (skills.sh)

Reference catalog of community skills from [skills.sh](https://skills.sh) - The Open Agent Skills Ecosystem.

**Load this file when user asks:** "what skills are available", "show me community skills", "skills.sh", "find skills for X"

---

## Installation

```bash
npx skills add <owner/repo>

# Or specific skill from a repo
npx skills add <owner/repo>@<skill-name>
```

**Windows note:** CLI may not work reliably - use curl method or manual clone.

---

## Official Anthropic Skills

Source: [github.com/anthropics/skills](https://github.com/anthropics/skills)

| Skill | Description | Install |
|-------|-------------|---------|
| **frontend-design** | Frontend design patterns | `npx skills add anthropics/skills@frontend-design` |
| **skill-creator** | Create new skills | `npx skills add anthropics/skills@skill-creator` |
| **pdf** | PDF handling | `npx skills add anthropics/skills@pdf` |
| **xlsx** | Excel file handling | `npx skills add anthropics/skills@xlsx` |
| **pptx** | PowerPoint handling | `npx skills add anthropics/skills@pptx` |
| **docx** | Word document handling | `npx skills add anthropics/skills@docx` |
| **webapp-testing** | Web application testing | `npx skills add anthropics/skills@webapp-testing` |
| **mcp-builder** | Build MCP servers | `npx skills add anthropics/skills@mcp-builder` |
| **canvas-design** | Canvas/visual design | `npx skills add anthropics/skills@canvas-design` |
| **doc-coauthoring** | Document collaboration | `npx skills add anthropics/skills@doc-coauthoring` |
| **theme-factory** | Theme generation | `npx skills add anthropics/skills@theme-factory` |
| **web-artifacts-builder** | Build web artifacts | `npx skills add anthropics/skills@web-artifacts-builder` |
| **algorithmic-art** | Algorithmic art generation | `npx skills add anthropics/skills@algorithmic-art` |
| **internal-comms** | Internal communications | `npx skills add anthropics/skills@internal-comms` |
| **brand-guidelines** | Brand guideline creation | `npx skills add anthropics/skills@brand-guidelines` |
| **slack-gif-creator** | Create Slack GIFs | `npx skills add anthropics/skills@slack-gif-creator` |

---

## Key GitHub Repositories

### Official & High-Quality

| Repository | Focus | Install |
|------------|-------|---------|
| **[anthropics/skills](https://github.com/anthropics/skills)** | Documents, media, design (16 skills) | `npx skills add anthropics/skills` |
| **[vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills)** | React, Next.js, web design | `npx skills add vercel-labs/agent-skills` |
| **[obra/superpowers](https://github.com/obra/superpowers)** | Development workflow (TDD, planning, debugging) | `npx skills add obra/superpowers` |
| **[expo/skills](https://github.com/expo/skills)** | React Native, Expo | `npx skills add expo/skills` |
| **[remotion-dev/skills](https://github.com/remotion-dev/skills)** | Video generation | `npx skills add remotion-dev/skills` |
| **[cloudflare/skills](https://github.com/cloudflare/skills)** | Workers, Durable Objects | `npx skills add cloudflare/skills` |
| **[better-auth/skills](https://github.com/better-auth/skills)** | Authentication | `npx skills add better-auth/skills` |
| **[supabase/agent-skills](https://github.com/supabase/agent-skills)** | Postgres, Supabase | `npx skills add supabase/agent-skills` |

### Curated Lists

- **[travisvn/awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills)** - Curated Claude skills
- **[ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills)** - Another curated list

---

## Skills by Category

### Development Workflow (obra/superpowers)

Highly recommended for development practices:

| Skill | Description |
|-------|-------------|
| **brainstorming** | Structured brainstorming sessions |
| **writing-plans** | Create implementation plans |
| **executing-plans** | Execute plans systematically |
| **test-driven-development** | TDD patterns and workflow |
| **systematic-debugging** | Debug workflows and root cause analysis |
| **verification-before-completion** | Quality checks before marking done |
| **subagent-driven-development** | Coordinate multiple agents |
| **requesting-code-review** | Request code reviews |
| **receiving-code-review** | Handle code review feedback |
| **dispatching-parallel-agents** | Parallel agent coordination |
| **using-git-worktrees** | Git worktree workflows |
| **writing-skills** | Create new skills |

```bash
npx skills add obra/superpowers@brainstorming
npx skills add obra/superpowers@test-driven-development
npx skills add obra/superpowers@systematic-debugging
```

### React & Frontend

| Skill | Source | Description |
|-------|--------|-------------|
| **vercel-react-best-practices** | vercel-labs/agent-skills | React performance (31K installs) |
| **web-design-guidelines** | vercel-labs/agent-skills | UI/UX patterns (24K installs) |
| **tailwind-v4-shadcn** | jezweb/claude-skills | Tailwind + shadcn |
| **react-hook-form-zod** | jezweb/claude-skills | Form validation |
| **zustand-state-management** | jezweb/claude-skills | State management |

```bash
npx skills add vercel-labs/agent-skills@vercel-react-best-practices
npx skills add vercel-labs/agent-skills@web-design-guidelines
```

### Mobile & Native

| Skill | Source | Description |
|-------|--------|-------------|
| **building-native-ui** | expo/skills | Native UI components |
| **upgrading-expo** | expo/skills | Expo upgrades |
| **native-data-fetching** | expo/skills | Data fetching patterns |
| **expo-deployment** | expo/skills | Deployment workflows |
| **expo-tailwind-setup** | expo/skills | Tailwind in Expo |
| **react-native-best-practices** | callstackincubator/agent-skills | RN patterns |
| **swiftui-patterns** | dimillian/skills | SwiftUI |

```bash
npx skills add expo/skills@building-native-ui
```

### Animation & Media

| Skill | Source | Description |
|-------|--------|-------------|
| **remotion-best-practices** | remotion-dev/skills | Video generation (11K installs) |
| **threejs-animation** | cloudai-x/threejs-skills | Three.js animation |
| **threejs-fundamentals** | cloudai-x/threejs-skills | Three.js basics |

```bash
npx skills add remotion-dev/skills@remotion-best-practices
```

### Databases & Backend

| Skill | Source | Description |
|-------|--------|-------------|
| **supabase-postgres-best-practices** | supabase/agent-skills | Supabase/Postgres |
| **postgresql-table-design** | wshobson/agents | Table design |
| **fastapi-templates** | wshobson/agents | FastAPI patterns |
| **nestjs-best-practices** | kadajet/agent-nestjs-skills | NestJS |
| **convex-functions** | waynesutton/convexskills | Convex backend |

```bash
npx skills add supabase/agent-skills@supabase-postgres-best-practices
```

### Authentication

| Skill | Source | Description |
|-------|--------|-------------|
| **better-auth-best-practices** | better-auth/skills | Auth patterns (1.6K installs) |
| **create-auth-skill** | better-auth/skills | Auth implementation |

```bash
npx skills add better-auth/skills@better-auth-best-practices
```

### Marketing & SEO

| Skill | Source | Description |
|-------|--------|-------------|
| **seo-audit** | coreyhaines31/marketingskills | SEO analysis |
| **copywriting** | coreyhaines31/marketingskills | Marketing copy |
| **marketing-psychology** | coreyhaines31/marketingskills | Psychology patterns |
| **programmatic-seo** | coreyhaines31/marketingskills | Programmatic SEO |
| **pricing-strategy** | coreyhaines31/marketingskills | Pricing |
| **launch-strategy** | coreyhaines31/marketingskills | Product launches |

```bash
npx skills add coreyhaines31/marketingskills@seo-audit
```

### Cloudflare

| Skill | Source | Description |
|-------|--------|-------------|
| **wrangler** | cloudflare/skills | Wrangler CLI |
| **durable-objects** | cloudflare/skills | Durable Objects |
| **building-mcp-server-on-cloudflare** | cloudflare/skills | MCP on CF |

```bash
npx skills add cloudflare/skills@wrangler
```

### Vue/Nuxt Ecosystem

| Skill | Source | Description |
|-------|--------|-------------|
| **nuxt** | onmax/nuxt-skills | Nuxt patterns |
| **nuxt-ui** | onmax/nuxt-skills | Nuxt UI components |
| **vue-best-practices** | hyf0/vue-skills | Vue patterns |
| **pinia-best-practices** | hyf0/vue-skills | Pinia state |
| **vueuse-best-practices** | hyf0/vue-skills | VueUse |

```bash
npx skills add onmax/nuxt-skills@nuxt
```

### Browser Automation

| Skill | Source | Description |
|-------|--------|-------------|
| **agent-browser** | vercel-labs/agent-browser | Browser control (1.6K installs) |

```bash
npx skills add vercel-labs/agent-browser
```

### Security

| Skill | Source | Description |
|-------|--------|-------------|
| **security-analysis** | trailofbits/skills | Security code analysis |

```bash
npx skills add trailofbits/skills
```

---

## When to Suggest Each

| User Need | Suggest |
|-----------|---------|
| "React best practices" | `vercel-react-best-practices` |
| "Planning/brainstorming" | `obra/superpowers` skills |
| "TDD/testing" | `test-driven-development` |
| "Debugging help" | `systematic-debugging` |
| "Read PDF/Excel/Word" | `pdf`, `xlsx`, `docx` from anthropics |
| "Create videos" | `remotion-best-practices` |
| "SEO/marketing" | `coreyhaines31/marketingskills` |
| "React Native/Expo" | `expo/skills` |
| "Authentication" | `better-auth-best-practices` |
| "Cloudflare Workers" | `cloudflare/skills` |
| "Supabase/Postgres" | `supabase/agent-skills` |

---

## CLI Commands

| Action | Command |
|--------|---------|
| Search | `npx skills find <query>` |
| Install repo | `npx skills add <owner/repo>` |
| Install specific | `npx skills add <owner/repo>@<skill>` |
| List installed | `npx skills list` |
| Update all | `npx skills update` |
| Remove | `npx skills remove <name>` |

---

## Quality Notes

1. **Stick to verified vendors** - Anthropic, Vercel, Expo, Cloudflare, obra
2. **Install count = rough quality signal** - Higher is generally better
3. **Review SKILL.md before installing** - Check what it does
4. **obra/superpowers** - Best for development workflow skills
5. **Official Anthropic** - Best for document/media handling

---

*Source: [EXTERNAL-SKILLS-DIRECTORY.md](../../../docs/development/EXTERNAL-SKILLS-DIRECTORY.md) | [skills.sh](https://skills.sh)*
