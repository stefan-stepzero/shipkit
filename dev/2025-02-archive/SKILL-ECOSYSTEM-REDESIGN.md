# Skill Ecosystem Redesign

A better approach to external skills - transparent, context-aware, and temporary.

---

## Problems with Current Approach (skills.sh)

| Issue | Impact |
|-------|--------|
| Popularity-ranked leaderboard | Vercel skills dominate, not necessarily best for your use case |
| Permanent installation | Skills accumulate, no easy way to manage/remove |
| Opaque install process | Unclear where files go, symlink complexity |
| No context awareness | Same skills recommended regardless of project phase |
| OS compatibility issues | Symlinks fail on Windows, falls back silently |
| Closed source CLI | `skills` npm package not on GitHub, wraps open `add-skill` |

**Architecture discovered:**
- `skills.sh` is built by Vercel (not prominently disclosed)
- Uses [vercel-labs/add-skill](https://github.com/vercel-labs/add-skill) (open source)
- `skills` npm package adds telemetry for leaderboard ranking
- Installs to `.agents/skills/` canonical location, symlinks to agent-specific dirs

---

## Proposed Better Approach

### Core Principles

1. **Transparent** - Open catalog where you understand what each skill does
2. **Context-aware** - Recommends skills based on your project/phase
3. **Temporary** - Load skills for a session, clear when done
4. **OS-agnostic** - Simple copy, no symlinks
5. **Project-scoped** - Skills live in project, not global

### Three Components

#### 1. Skill Catalog (`shipkit-skill-catalog`)

A browsable, categorized reference of external skills:

```
Categories:
├── Discovery & Planning
│   ├── brainstorming (obra/superpowers)
│   ├── writing-plans (obra/superpowers)
│   └── executing-plans (obra/superpowers)
├── Implementation
│   ├── vercel-react-best-practices (vercel-labs)
│   ├── test-driven-development (obra/superpowers)
│   └── systematic-debugging (obra/superpowers)
├── Quality & Review
│   ├── verification-before-completion (obra/superpowers)
│   ├── requesting-code-review (obra/superpowers)
│   └── receiving-code-review (obra/superpowers)
└── Technology-Specific
    ├── React: vercel-react-best-practices
    ├── Expo: expo/skills collection
    ├── Vue/Nuxt: onmax/nuxt-skills
    └── ...
```

Each entry includes:
- What it does (1-2 sentences)
- When to use it (project phase, situation)
- Source repo
- Sample prompt showing skill in action

#### 2. Skill Recommender (`shipkit-skill-recommender`)

A skill/workflow that:

```
Input: Project context
- Stack (from .shipkit/stack.md or detection)
- Phase (discovery, prototyping, implementation, testing, launch)
- Current task/goal

Output: Recommended skills with reasoning
- "For React prototyping, I recommend:"
  - vercel-react-best-practices - React patterns and conventions
  - brainstorming - Structured ideation for features
  - writing-plans - Capture your approach before coding

- "Load these? [y/n/select]"
```

Decision logic:
```
IF phase == "discovery" THEN
  recommend: brainstorming, writing-plans

IF phase == "prototyping" THEN
  recommend: writing-plans, executing-plans, {stack-specific}

IF phase == "implementation" THEN
  recommend: test-driven-development, {stack-specific}

IF phase == "review" THEN
  recommend: verification-before-completion, code-review skills
```

#### 3. Skill Loader (`shipkit-skill-loader`)

Simple, OS-agnostic loading:

```bash
# Load a skill (fetch to .claude/skills/)
/load-skill obra/superpowers brainstorming

# Load multiple skills
/load-skills discovery  # Loads discovery-phase skills

# List loaded skills
/list-skills

# Clear skills (end of phase/session)
/clear-skills [--all | skill-name]
```

Implementation (simple curl, no symlinks):
```bash
fetch_skill() {
  repo=$1   # e.g., "obra/superpowers"
  skill=$2  # e.g., "brainstorming"
  dest=".claude/skills/$skill"

  mkdir -p "$dest"
  curl -sL "https://raw.githubusercontent.com/$repo/main/skills/$skill/SKILL.md" \
    -o "$dest/SKILL.md"
}
```

---

## User Flow Example

```
User: "Starting a new React dashboard project"

Claude: "I'll help you get set up. What phase are you in?
  1. Discovery (understanding requirements)
  2. Prototyping (exploring approaches)
  3. Implementation (building features)
  4. Testing/Review"

User: "2 - Prototyping"

Claude: "For React prototyping, I recommend loading these skills:

  Discovery & Planning:
  - brainstorming - Structured ideation for features
  - writing-plans - Capture approach before coding

  React-Specific:
  - vercel-react-best-practices - React patterns (31K installs)

  Load these for this session? They'll be available in .claude/skills/"

User: "yes"

Claude: [Fetches skills to .claude/skills/]
"Loaded 3 skills. You can:
  - /list-skills to see what's loaded
  - /clear-skills when moving to next phase

Ready to start prototyping!"
```

---

## Comparison

| Aspect | skills.sh | Proposed Approach |
|--------|-----------|-------------------|
| Discovery | Leaderboard browsing | Context-aware recommendations |
| Decision | "Most popular" | "Right for your phase" |
| Installation | Permanent, global | Temporary, project-scoped |
| Management | No uninstall | Clear when done |
| Transparency | Telemetry-driven | Open catalog with reasoning |
| OS Support | Symlink issues | Simple copy |

---

## Implementation Priority

### Phase 1: Catalog
- [x] Created `EXTERNAL-SKILLS-DIRECTORY.md` with repo list
- [x] Created `external-skills-reference/` for downloaded skills
- [ ] Organize by use case, not just by source
- [ ] Add "when to use" for each skill

### Phase 2: Loader
- [ ] Simple bash/node script to fetch skills
- [ ] `/load-skill` command
- [ ] `/clear-skills` command
- [ ] Works on Windows, Mac, Linux

### Phase 3: Recommender
- [ ] Reads project context (.shipkit/ files)
- [ ] Maps phase → skill recommendations
- [ ] Interactive selection
- [ ] Integrates with shipkit-project-status

---

## Open Questions

1. **Where should loaded skills live?**
   - `.claude/skills/` (standard location)
   - `.claude/skills/_external/` (separate from project skills)
   - Temp directory (truly ephemeral)

2. **How to handle skill updates?**
   - Re-fetch on load?
   - Version pinning?
   - Cache with TTL?

3. **Should recommendations be automatic?**
   - Auto-suggest on phase change?
   - Only when user asks?
   - Gentle reminder in session start?

4. **Integration with Shipkit skills?**
   - External skills complement shipkit-skills
   - Some external skills might replace shipkit-skills
   - Need clear delineation

---

## Distribution Options

How to distribute a skill loader CLI without requiring users to install anything.

### Option A: npx from GitHub (no npm publish needed)

`npx` can run directly from a GitHub repo - no npm registry required.

**Setup:**
```
repo/
├── package.json
├── cli.js          # Entry point (must have shebang)
└── src/
    └── ...
```

**package.json:**
```json
{
  "name": "shipkit-skill-loader",
  "version": "1.0.0",
  "bin": {
    "skill-loader": "./cli.js"
  },
  "type": "module"
}
```

**cli.js:**
```javascript
#!/usr/bin/env node
import { execSync } from 'child_process';

const [repo, skill] = process.argv.slice(2);
const dest = `.claude/skills/${skill}`;
const url = `https://raw.githubusercontent.com/${repo}/main/skills/${skill}/SKILL.md`;

execSync(`mkdir -p ${dest}`);
execSync(`curl -sL "${url}" -o "${dest}/SKILL.md"`);
console.log(`Loaded ${skill} to ${dest}`);
```

**Usage:**
```bash
npx github:your-org/skill-loader obra/superpowers brainstorming
```

### Option B: Shell script (no node required)

Simplest approach - just bash. Users curl and run.

**load-skill.sh:**
```bash
#!/bin/bash
set -e

REPO=$1      # e.g., "obra/superpowers"
SKILL=$2     # e.g., "brainstorming"
DEST=".claude/skills/$SKILL"

if [ -z "$REPO" ] || [ -z "$SKILL" ]; then
  echo "Usage: load-skill <owner/repo> <skill-name>"
  echo "Example: load-skill obra/superpowers brainstorming"
  exit 1
fi

URL="https://raw.githubusercontent.com/$REPO/main/skills/$SKILL/SKILL.md"

mkdir -p "$DEST"
curl -sL "$URL" -o "$DEST/SKILL.md"

if [ -f "$DEST/SKILL.md" ]; then
  echo "✓ Loaded $SKILL to $DEST"
else
  echo "✗ Failed to load $SKILL"
  exit 1
fi
```

**Usage options:**

```bash
# Run directly from GitHub (one-liner)
curl -sL https://raw.githubusercontent.com/your-org/repo/main/load-skill.sh | bash -s obra/superpowers brainstorming

# Or download once and reuse
curl -sL https://raw.githubusercontent.com/your-org/repo/main/load-skill.sh -o ~/.local/bin/load-skill
chmod +x ~/.local/bin/load-skill
load-skill obra/superpowers brainstorming
```

### Option C: Publish to npm (for `npx package-name`)

If you want the cleanest UX (`npx skill-loader`), publish to npm:

```bash
# 1. Create npm account at npmjs.com
# 2. Login locally
npm login

# 3. Publish (from package directory)
npm publish

# 4. Users can now run
npx skill-loader obra/superpowers brainstorming
```

### Recommendation

| Approach | Pros | Cons |
|----------|------|------|
| **npx from GitHub** | No npm account, npm-style UX | Requires node |
| **Shell script** | No dependencies, auditable | Less polished UX |
| **npm publish** | Cleanest UX (`npx name`) | Requires npm account, maintenance |

For Shipkit: **Start with shell script** (Option B) for simplicity, upgrade to npm later if needed.

---

## Resources

- [vercel-labs/add-skill](https://github.com/vercel-labs/add-skill) - Open source installer (reference for agent detection)
- [skills.sh](https://skills.sh) - Current directory (for browsing available skills)
- [HN Discussion](https://news.ycombinator.com/item?id=46697908) - Criticism and context
- `claude-code-best-practices/EXTERNAL-SKILLS-DIRECTORY.md` - Our catalog
- `claude-code-best-practices/external-skills-reference/` - Downloaded skills for comparison
