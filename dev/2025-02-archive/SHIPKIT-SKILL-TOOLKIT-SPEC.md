# shipkit-skill-toolkit Spec

A meta-skill that helps users discover, evaluate, and install skills from multiple sources.

---

## The Problem

Users face a fragmented landscape:

| Source | Install Method | Discovery |
|--------|---------------|-----------|
| Anthropic Official | `/plugin install X@claude-code-plugins` | ? |
| Obra Superpowers | `/plugin install X@superpowers-marketplace` | GitHub |
| skills.sh catalog | `npx skills add owner/repo` | skills.sh website |
| Manual/Community | `curl` to `.claude/skills/` | GitHub, word of mouth |
| Shipkit | Installer script | This repo |

**No unified way to:**
- See what's available across sources
- Get recommendations for your context
- Know which installation method to use
- Understand what each skill does before installing

---

## The Solution: shipkit-skill-toolkit

A skill that serves as a **skill concierge** — helping users navigate the ecosystem.

### Core Functions

| Function | What It Does |
|----------|--------------|
| **Discover** | Show available skills by category/source |
| **Recommend** | Suggest skills based on stack/phase |
| **Explain** | Describe what a skill does before installing |
| **Install** | Provide correct install command for any skill |
| **Manage** | List installed skills, suggest cleanup |

---

## User Flows

### Flow 1: "What skills are available?"

```
User: /skill-toolkit

Claude: "What would you like to do?
1. Browse skills by category
2. Get recommendations for your project
3. Search for a specific skill
4. See what's installed
5. Learn about a specific skill"

User: "1"

Claude: "## Skills by Category

### Frontend & Design
| Skill | Source | Install |
|-------|--------|---------|
| frontend-design | Anthropic | `/plugin install frontend-design@claude-code-plugins` |
| vercel-react-best-practices | Vercel | `curl ...` or skills.sh |
| tailwind-v4-shadcn | Community | `curl ...` |

### Workflow & Planning
| Skill | Source | Install |
|-------|--------|---------|
| brainstorming | Obra | `/plugin install superpowers@superpowers-marketplace` |
| writing-plans | Obra | (included in superpowers) |
| verification-before-completion | Obra | (included in superpowers) |

### Database & Backend
| Skill | Source | Install |
|-------|--------|---------|
| supabase-postgres-best-practices | Supabase | `curl ...` |

..."
```

### Flow 2: "What should I install for my project?"

```
User: /skill-toolkit recommend

Claude: "I'll check your project context...

Reading .shipkit/stack.md... Next.js + Supabase + Tailwind
Reading .shipkit/project-status.md... Phase: Implementation

## Recommended Skills

### High Priority (matches your stack)
| Skill | Why | Install |
|-------|-----|---------|
| frontend-design | Building UI with Tailwind | `/plugin install frontend-design@claude-code-plugins` |
| supabase-postgres-best-practices | Using Supabase | See below |

### Useful for Implementation Phase
| Skill | Why | Install |
|-------|-----|---------|
| verification-before-completion | Quality checks | `/plugin install superpowers@superpowers-marketplace` |

### Setup Commands

First time? Register marketplaces:
```
/plugin marketplace add anthropics/claude-code
/plugin marketplace add obra/superpowers-marketplace
```

Then install:
```
/plugin install frontend-design@claude-code-plugins
/plugin install superpowers@superpowers-marketplace
```

For Supabase (not in marketplace):
```
mkdir -p .claude/skills/supabase-patterns
curl -sL -o .claude/skills/supabase-patterns/SKILL.md \
  https://raw.githubusercontent.com/supabase/agent-skills/main/skills/supabase-postgres-best-practices/SKILL.md
```

Shall I run any of these?"
```

### Flow 3: "Tell me about a skill before I install"

```
User: /skill-toolkit explain frontend-design

Claude: "## frontend-design

**Source:** Anthropic Official
**Install:** `/plugin install frontend-design@claude-code-plugins`

### What It Does
Biases Claude toward distinctive, bold UI design instead of generic patterns.

### Key Instructions It Provides
- Commit to aesthetic direction before coding
- Use distinctive typography (not system fonts)
- Cohesive color palettes with CSS variables
- Intentional motion and animation
- Break generic grid layouts

### When to Use
- Building user-facing UI
- Want to avoid 'AI slop' generic aesthetics
- Prototyping distinctive designs

### When NOT to Use
- Internal tools where aesthetics don't matter
- Following existing design system strictly

### Size
~2-3K tokens when loaded

Want to install it?"
```

### Flow 4: "What do I have installed?"

```
User: /skill-toolkit list

Claude: "## Installed Skills

### Via Plugin System
Run `/plugin list` to see plugin-installed skills.

### Via .claude/skills/
| Skill | Location | Source |
|-------|----------|--------|
| shipkit-project-status | .claude/skills/shipkit-project-status/ | Shipkit |
| shipkit-spec | .claude/skills/shipkit-spec/ | Shipkit |
| supabase-patterns | .claude/skills/supabase-patterns/ | Manual install |

### Recommendations
- You have 12 Shipkit skills loaded (~15K tokens)
- Consider removing supabase-patterns if not actively using Supabase
- frontend-design would complement your current setup

To remove a manual skill:
```
rm -rf .claude/skills/skill-name
```

To remove a plugin:
```
/plugin remove plugin-name
```"
```

---

## Skill Catalog Data

The skill needs a reference catalog. Options:

### Option A: Embedded Catalog (Simple)

Hardcode known skills in the SKILL.md itself:

```markdown
## Known Skills Catalog

### Anthropic Official (via /plugin)
- frontend-design: Distinctive UI aesthetics
- pdf: PDF handling
- xlsx: Excel handling
- mcp-builder: Build MCP servers

### Obra Superpowers (via /plugin)
- superpowers: Bundle including brainstorming, writing-plans, verification, etc.

### Community (via curl)
- vercel-react-best-practices: React patterns
- supabase-postgres-best-practices: Supabase patterns
...
```

**Pros:** Simple, no external dependencies
**Cons:** Gets stale, needs manual updates

### Option B: Reference File (Maintainable)

Keep catalog in separate file skill loads:

```
shipkit-skill-toolkit/
├── SKILL.md
└── references/
    └── skill-catalog.md
```

**Pros:** Easier to update catalog separately
**Cons:** Slightly more complex

### Option C: Fetch Live (Dynamic)

Fetch from skills.sh or GitHub at runtime:

```markdown
When user asks to browse, fetch current catalog from:
- https://skills.sh/api/skills (if available)
- GitHub API for known repos
```

**Pros:** Always current
**Cons:** Requires network, slower, API may not exist

### Recommendation: Option B

Start with embedded + reference file. Update periodically. Add live fetching later if needed.

---

## Installation Method Decision Tree

```
Is skill in Anthropic marketplace?
├── Yes → /plugin install X@claude-code-plugins
└── No
    ├── Is it in another marketplace (Obra, etc)?
    │   ├── Yes → /plugin install X@marketplace-name
    │   └── No
    │       ├── Is it on skills.sh?
    │       │   ├── Yes (and not Windows) → npx skills add owner/repo
    │       │   └── No or Windows → curl method
    │       └── Manual curl to .claude/skills/
```

The skill encodes this logic and provides the right command.

---

## Stack → Skill Mapping

```yaml
# Hardcoded recommendations by stack component

next.js:
  - frontend-design (Anthropic)
  - vercel-react-best-practices (Community)

react:
  - frontend-design (Anthropic)
  - vercel-react-best-practices (Community)

supabase:
  - supabase-postgres-best-practices (Community)

tailwind:
  - tailwind-v4-shadcn (Community)
  - frontend-design (Anthropic)

prisma:
  - postgresql-table-design (Community)

typescript:
  - (most skills assume TypeScript)

# Phase recommendations
discovery:
  - brainstorming (Obra)
  - writing-plans (Obra)

implementation:
  - verification-before-completion (Obra)
  - test-driven-development (Obra)

review:
  - verification-before-completion (Obra)
```

---

## SKILL.md Structure

```markdown
---
name: shipkit-skill-toolkit
description: Discover, evaluate, and install skills from multiple sources
---

# Skill Toolkit

Help users navigate the skill ecosystem.

## Activation

Triggered by:
- `/skill-toolkit` or `/shipkit-skill-toolkit`
- "what skills are available"
- "recommend skills for my project"
- "how do I install [skill-name]"

## Behavior

### On Invocation

1. Ask what user wants to do:
   - Browse by category
   - Get recommendations
   - Search for specific skill
   - List installed
   - Explain a skill

2. Based on choice, provide relevant information

### For Recommendations

1. Read `.shipkit/stack.md` for technology
2. Read `.shipkit/project-status.md` for phase
3. Match against skill catalog
4. Provide install commands

### For Installation Help

1. Identify skill source (Anthropic, Obra, Community)
2. Provide correct install command
3. Note any prerequisites (marketplace registration)

## Skill Catalog

[Reference: references/skill-catalog.md]

## Installation Methods

### Anthropic Marketplace
```
/plugin marketplace add anthropics/claude-code
/plugin install SKILL@claude-code-plugins
```

### Obra Marketplace
```
/plugin marketplace add obra/superpowers-marketplace
/plugin install superpowers@superpowers-marketplace
```

### Manual (Community Skills)
```
mkdir -p .claude/skills/SKILL-NAME
curl -sL -o .claude/skills/SKILL-NAME/SKILL.md \
  https://raw.githubusercontent.com/OWNER/REPO/main/skills/SKILL/SKILL.md
```

## Output Format

Always provide:
1. Clear skill description
2. Exact install command (copy-pasteable)
3. Any prerequisites
4. Token cost estimate if known
```

---

## Integration with Existing Skills

### With shipkit-project-status

Add skill recommendations to status output:

```markdown
## Recommended Skills

Based on your stack and phase, consider:
- frontend-design (not installed)
- supabase-postgres-best-practices (not installed)

Run `/skill-toolkit` for installation help.
```

### With shipkit-project-context

After detecting stack, mention relevant skills:

```markdown
## Detected Stack
- Next.js (App Router)
- Supabase
- Tailwind

## Available Skills for This Stack
Run `/skill-toolkit recommend` to see skills that match your stack.
```

---

## Implementation Priority

| Component | Effort | Value | Priority |
|-----------|--------|-------|----------|
| Basic catalog (embedded) | Low | High | 🟢 Do first |
| Recommendation logic | Low | High | 🟢 Do first |
| Install command generator | Low | High | 🟢 Do first |
| Skill explanation | Medium | Medium | 🟡 Next |
| Installed skill listing | Medium | Low | 🔴 Later |
| Live catalog fetching | High | Low | 🔴 Later |

### MVP Scope

1. Hardcoded catalog of ~20 useful skills
2. Stack → skill recommendations
3. Correct install commands for each source
4. Basic skill descriptions

---

## Open Questions

1. **Should this be one skill or multiple?**
   - One skill (simpler) vs separate browse/recommend/install skills

2. **How to keep catalog current?**
   - Manual updates vs automated fetching

3. **Should it actually run install commands?**
   - Just provide commands (safer) vs offer to execute

4. **Integration with Shipkit marketplace?**
   - When Shipkit has its own marketplace, this skill should recommend it

---

## Related Documents

- `SKILL-ECOSYSTEM-REDESIGN.md` — Original skill ecosystem ideas
- `CLAUDE-CODE-SKILLS-INTEGRATION.md` — Plugin system documentation
- `EXTERNAL-SKILLS-DIRECTORY.md` — Current skill catalog
- `SHIPKIT-STACK-TOOLING.md` — Stack-specific skill recommendations
