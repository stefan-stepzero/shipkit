# Claude Code Skills Integration

Understanding how Claude Code's native skill system works and opportunities for Shipkit integration.

---

## How Claude Code Skills Work

### The Core Mechanism

Claude Code has a **native skill system** — skills are first-class primitives, not plugins.

**Skill locations (in priority order):**
1. **Project-level:** `.claude/skills/{skill-name}/SKILL.md`
2. **User-level:** `~/.claude/skills/{skill-name}/SKILL.md`

**Auto-discovery:** Claude Code automatically loads skills from these directories at session start. No explicit "install" command needed — just put the files there.

### Skill File Structure

```
skill-name/
├── SKILL.md          # Required - main instructions
├── scripts/          # Optional - executable helpers
├── references/       # Optional - additional docs
└── assets/           # Optional - supporting files
```

### SKILL.md Format

```yaml
---
name: skill-name              # Required: 1-64 chars, lowercase + hyphens
description: What it does     # Required: max 1024 chars
license: MIT                  # Optional
compatibility: claude-code    # Optional
metadata:                     # Optional: key-value pairs
  category: frontend
---

# Skill Title

Instructions and content in Markdown...
```

**Key behavior:** The entire SKILL.md file is loaded into Claude's context when the skill is activated.

---

## Example: frontend-design Skill

**Source:** [anthropics/skills](https://github.com/anthropics/skills/tree/main/skills/frontend-design)

### Frontmatter

```yaml
---
name: frontend-design
description: Create distinctive, production-grade frontend interfaces with high design quality...
license: Complete terms in LICENSE.txt
---
```

### Structure

| Section | Purpose |
|---------|---------|
| **Introduction** | Establish goal: avoid "generic AI slop aesthetics" |
| **Design Thinking Framework** | Commit to bold aesthetic before coding |
| **Frontend Aesthetics Guidelines** | Typography, color, motion, composition, backgrounds |

### Key Instruction from the Skill

> "Choose a clear conceptual direction and execute it with precision."
> "No design should be the same — vary themes, fonts, and approaches across projects."

### What This Skill Does

When loaded, it biases Claude toward:
- Distinctive typography (not system fonts)
- Cohesive color palettes with CSS variables
- Intentional motion and animation
- Breaking generic grid layouts
- Atmospheric backgrounds and textures

**Without this skill:** Claude defaults to safe, generic UI patterns.
**With this skill:** Claude commits to bold aesthetic directions.

---

## Installation Methods

### Method 1: Native Claude Code Plugin System (Recommended)

Claude Code has a **built-in plugin marketplace**. This is the official way to install skills.

```bash
# Step 1: Register the Anthropic marketplace (one-time)
/plugin marketplace add anthropics/claude-code

# Step 2: Install the skill
/plugin install frontend-design@claude-code-plugins
```

**Other plugin commands:**
```bash
/plugin list                    # See installed plugins
/plugin update frontend-design  # Update a plugin
/plugin remove frontend-design  # Uninstall
```

**Known marketplaces:**
| Marketplace | Command | Skills |
|-------------|---------|--------|
| Anthropic Official | `/plugin marketplace add anthropics/claude-code` | frontend-design, pdf, xlsx, mcp-builder, etc. |
| Obra Superpowers | `/plugin marketplace add obra/superpowers-marketplace` | brainstorming, writing-plans, verification, etc. |

**Third-party marketplaces are supported!** Anyone can create a marketplace.

### Method 2: Manual Download (For Custom/External Skills)

For skills not in the official marketplace:

```bash
# Create skills directory
mkdir -p .claude/skills/frontend-design

# Download the skill
curl -sL -o .claude/skills/frontend-design/SKILL.md \
  https://raw.githubusercontent.com/anthropics/skills/main/skills/frontend-design/SKILL.md
```

Next Claude Code session will auto-discover it.

### Method 3: skills.sh CLI (Third-Party)

```bash
npx skills add anthropics/skills frontend-design
```

**Note:** This is a third-party CLI (built by Vercel), not part of Claude Code. Has Windows compatibility issues (symlink problems). Use native plugin system instead when possible.

### Method 4: Full Repo Clone

```bash
# Clone all Anthropic skills
git clone https://github.com/anthropics/skills.git ~/.claude/skills-repo

# Symlink specific skills
ln -s ~/.claude/skills-repo/skills/frontend-design ~/.claude/skills/frontend-design
```

---

## What Skills Are Available

### Official Anthropic Skills (github.com/anthropics/skills)

| Skill | Purpose |
|-------|---------|
| `frontend-design` | Distinctive UI aesthetics |
| `skill-creator` | Create new skills |
| `pdf`, `xlsx`, `pptx`, `docx` | Document handling |
| `webapp-testing` | Web application testing |
| `mcp-builder` | Build MCP servers |
| `canvas-design` | Visual/canvas design |
| `theme-factory` | Theme generation |

### Community Skills (via skills.sh)

| Skill | Source | Purpose |
|-------|--------|---------|
| `vercel-react-best-practices` | vercel-labs | React patterns |
| `supabase-postgres-best-practices` | supabase | Database patterns |
| `brainstorming`, `writing-plans` | obra/superpowers | Workflow patterns |
| `tailwind-v4-shadcn` | jezweb | Styling patterns |

See `EXTERNAL-SKILLS-DIRECTORY.md` for full catalog.

---

## Shipkit Integration Opportunities

### Current State

Shipkit has its own skills in `install/skills/shipkit-*/SKILL.md`. These are installed to `.claude/skills/` via the Shipkit installer.

### Opportunity 1: Phase-Based Skill Loading

Load external skills based on project phase:

| Phase | Auto-Load Skills |
|-------|------------------|
| Discovery | `brainstorming`, `writing-plans` |
| Prototyping | `frontend-design`, `vercel-react-best-practices` |
| Implementation | `supabase-postgres-best-practices`, stack-specific skills |
| Polish | `frontend-design`, `seo-audit` |

**Implementation:**
```markdown
# shipkit-skill-loader (proposed)

1. Read .shipkit/project-status.md for current phase
2. Read .shipkit/stack.md for technology
3. Recommend relevant external skills
4. Download to .claude/skills/ on user approval
5. Clear when phase changes
```

### Opportunity 2: Stack-Matched Skills

Auto-suggest skills based on detected stack:

```
Stack Detection:
├── Next.js detected → suggest vercel-react-best-practices
├── Supabase detected → suggest supabase-postgres-best-practices
├── Tailwind detected → suggest tailwind-v4-shadcn
└── Prisma detected → suggest postgresql-table-design
```

### Opportunity 3: Session-Scoped Loading

Instead of permanent installation, load skills temporarily:

```bash
# Load for this session only (to .claude/skills/_temp/)
/shipkit-load-skill frontend-design

# Clear temporary skills
/shipkit-clear-skills
```

**Benefits:**
- No skill accumulation
- Context-appropriate skills only
- Easy to experiment

### Opportunity 4: Skill Recommendations in shipkit-project-status

Add to `/shipkit-project-status` output:

```markdown
## Recommended Skills

Based on your phase (Prototyping) and stack (Next.js + Supabase):

| Skill | Why | Load? |
|-------|-----|-------|
| frontend-design | You're building UI | [y/n] |
| supabase-postgres-best-practices | Using Supabase | [y/n] |
| vercel-react-best-practices | Next.js patterns | [y/n] |

Run `/shipkit-load-skills` to install recommended skills.
```

### Opportunity 5: Skill Catalog as Context

Instead of loading full skills, create a reference catalog Claude reads:

```markdown
# .shipkit/skill-catalog.md

## Available Skills for This Project

### Frontend
- **frontend-design** - Bold UI aesthetics, anti-generic patterns
  Load with: `/shipkit-load-skill frontend-design`

### Database
- **supabase-postgres-best-practices** - RLS, queries, auth
  Load with: `/shipkit-load-skill supabase-postgres`

...
```

Claude knows what's available without loading everything.

---

## Implementation Priority

| Opportunity | Effort | Value | Priority |
|-------------|--------|-------|----------|
| Skill catalog as context | Low | Medium | 🟢 Quick win |
| Recommendations in project-status | Low | High | 🟢 Quick win |
| Stack-matched suggestions | Medium | High | 🟡 Next |
| Phase-based loading | Medium | High | 🟡 Next |
| Session-scoped loading | High | Medium | 🔴 Later |

### Recommended First Step

Add skill recommendations to `shipkit-project-status`:

1. Detect stack from `stack.md`
2. Map stack → recommended skills (hardcoded initially)
3. Show recommendations in status output
4. Provide native plugin commands to install

**Example output:**
```markdown
## Recommended Plugins

Based on your stack (Next.js + Tailwind + Supabase):

| Plugin | Why | Install |
|--------|-----|---------|
| frontend-design | Building UI components | `/plugin install frontend-design@claude-code-plugins` |

To add the Anthropic marketplace (one-time):
/plugin marketplace add anthropics/claude-code
```

No new skill needed — just enhance existing `shipkit-project-status`.

### Native Plugin System Implications

The `/plugin` command system changes our integration approach:

| Original Idea | Better Approach |
|---------------|-----------------|
| Build custom skill loader | Leverage native `/plugin` commands |
| Manage skills in `.claude/skills/` manually | Let Claude Code manage via plugin system |
| Session-scoped temporary loading | Use `/plugin install` / `/plugin remove` |

**What Shipkit should do:**
1. **Recommend** plugins based on context (stack, phase)
2. **Provide commands** user can run (not try to install ourselves)
3. **Document** which plugins work well with Shipkit stack
4. **Only use manual loading** for non-marketplace skills (community skills, custom skills)

---

## Technical Notes

### Native Plugin System

Claude Code's plugin system provides:

| Command | Purpose |
|---------|---------|
| `/plugin marketplace add <source>` | Register a marketplace |
| `/plugin install <name>@<marketplace>` | Install a plugin/skill |
| `/plugin list` | Show installed plugins |
| `/plugin update <name>` | Update a plugin |
| `/plugin remove <name>` | Uninstall a plugin |

**Known marketplaces:**
- `anthropics/claude-code` → Official Anthropic skills (frontend-design, pdf, xlsx, etc.)

### Skill Loading Behavior

- Skills are loaded at session start
- Adding a skill mid-session requires session restart (or explicit load)
- Multiple skills can be active simultaneously
- Skills don't conflict — they're all just context
- Native plugins are managed separately from manual `.claude/skills/` files

### Skill Size Considerations

- Large skills consume context tokens
- `frontend-design` is ~2-3K tokens
- `vercel-react-best-practices` is ~4-5K tokens
- Loading 5+ skills = significant context usage

**Implication:** Phase-based loading is valuable — don't load all skills all the time.

### Windows Compatibility

- Symlinks require admin privileges on Windows
- skills.sh CLI fails silently on Windows
- **Recommendation:** Always use direct file copy, not symlinks

```bash
# Windows-safe installation
curl -sL -o .claude/skills/frontend-design/SKILL.md ^
  https://raw.githubusercontent.com/anthropics/skills/main/skills/frontend-design/SKILL.md
```

---

---

## Creating a Shipkit Marketplace

**Third-party marketplaces ARE supported.** Shipkit can create its own marketplace as a distribution channel.

### How Third-Party Marketplaces Work

The format follows GitHub repository conventions:

```bash
# Users register marketplace (one-time)
/plugin marketplace add owner/marketplace-repo

# Users install plugins
/plugin install plugin-name@marketplace-name
```

**Example (Obra Superpowers):**
```bash
/plugin marketplace add obra/superpowers-marketplace
/plugin install superpowers@superpowers-marketplace
```

### Marketplace Structure

Create a GitHub repo with `.claude-plugin/` directory:

```
shipkit-marketplace/
├── .claude-plugin/
│   ├── marketplace.json    # Marketplace definition
│   └── plugin.json         # Plugin metadata (if single plugin)
├── skills/
│   ├── shipkit-project-status/
│   │   └── SKILL.md
│   ├── shipkit-spec/
│   │   └── SKILL.md
│   └── ...
└── README.md
```

### marketplace.json Format

```json
{
  "name": "shipkit-lite",
  "description": "Shipkit - Framework for shipping production-ready MVPs",
  "owner": {
    "name": "Shipkit",
    "email": "contact@shipkit.dev"
  },
  "plugins": [
    {
      "name": "shipkit-lite",
      "version": "1.0.0",
      "description": "Complete Shipkit skill suite",
      "source": "./"
    }
  ]
}
```

### User Installation Flow

```bash
# 1. Register Shipkit marketplace (one-time)
/plugin marketplace add shipkit/shipkit-marketplace

# 2. Install Shipkit
/plugin install shipkit-lite@shipkit-marketplace
```

### Benefits of Native Marketplace

| Benefit | Description |
|---------|-------------|
| **Official distribution** | Users install via native Claude Code commands |
| **Version management** | `/plugin update` handles updates |
| **Discoverability** | Listed when users browse marketplaces |
| **No custom installer** | Leverage Claude Code's built-in system |
| **Easy uninstall** | `/plugin remove` cleanly removes |

### Shipkit Distribution Options

| Method | Pros | Cons |
|--------|------|------|
| **Native marketplace** | Official feel, version management, easy install | Need to maintain marketplace repo |
| **Manual installer script** | Full control, works offline | Extra step for users |
| **Direct SKILL.md download** | Simplest, transparent | No version management |

### Recommendation

**Create a Shipkit marketplace** as the primary distribution:
1. Create `shipkit/shipkit-marketplace` repo
2. Add `.claude-plugin/marketplace.json`
3. Include all shipkit-skills as a single plugin
4. Users install with two commands

**Keep manual option** as fallback for:
- Users who prefer transparency
- Offline installation
- Custom/modified installations

### Implementation Checklist

- [ ] Create `shipkit-marketplace` GitHub repo
- [ ] Add `.claude-plugin/marketplace.json`
- [ ] Structure skills in marketplace format
- [ ] Test installation flow
- [ ] Document in Shipkit README
- [ ] Add to shipkit-project-status recommendations

---

## Related Documents

- `EXTERNAL-SKILLS-DIRECTORY.md` — Full catalog of available skills
- `SKILL-ECOSYSTEM-REDESIGN.md` — Proposed better approach to skill management
- `PERSISTENCE-SKILLS-SPEC.md` — New Shipkit skills (preferences, learnings, codebase-index)
- `SHIPKIT-STACK-TOOLING.md` — Stack-specific tools including relevant skills
