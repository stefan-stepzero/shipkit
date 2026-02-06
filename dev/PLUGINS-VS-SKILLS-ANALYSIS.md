# Plugins vs Skills: Analysis for Shipkit

## The Core Question

Should Shipkit be distributed as:
1. **Skills only** (current approach via `.claude/skills/`)
2. **A plugin** (via `.claude-plugin/` with marketplace distribution)
3. **Hybrid** (some components as plugin, some as skills)

---

## Key Differences

| Aspect | Skills | Plugins |
|--------|--------|---------|
| **Contains** | SKILL.md files only | Commands, agents, skills, hooks, MCP servers |
| **Distribution** | `npx skills add` or manual copy | `/plugin install` from marketplace |
| **Namespace** | Flat (conflicts possible) | Namespaced `plugin:component` |
| **Auto-discovery** | `.claude/skills/` scanned | `.claude-plugin/plugin.json` registered |
| **User invocation** | Auto-triggered by context | Commands explicit (`/command`), skills auto |
| **Updates** | Manual `npx skills update` | Auto-update from marketplace |
| **Hooks** | Not supported | Full hook support (PreToolUse, etc.) |
| **MCP servers** | Not supported | Built-in MCP configuration |
| **Settings** | Via CLAUDE.md | Via `.local.md` files + hooks |

---

## What Shipkit Currently Has

```
install/
├── skills/           # 24 skills
├── agents/           # 6 agents
├── hooks/            # 2 hooks (session-start, after-skill-router)
├── settings/         # Settings JSON
└── claude-md/        # CLAUDE.md template
```

### Components That ARE Plugin-Compatible

| Component | Current Location | Plugin Equivalent |
|-----------|-----------------|-------------------|
| Skills | `install/skills/shipkit-*/` | `skills/shipkit-*/SKILL.md` |
| Agents | `install/agents/` | `agents/*.md` |
| Hooks | `install/shared/hooks/` | `hooks/hooks.json` + scripts |

### Components That Need Adaptation

| Component | Current | Plugin Pattern |
|-----------|---------|----------------|
| Session init | Python hook | SessionStart hook in hooks.json |
| Skill routing | Python hook | Could be hook or skill |
| Settings | JSON file | `.local.md` pattern |
| CLAUDE.md install | Template copy | Would need install command |

---

## Plugin Structure for Shipkit

If Shipkit became a plugin:

```
shipkit/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   └── shipkit-master.md       # Main orchestrator as command
├── agents/
│   ├── product-owner.md
│   ├── ux-designer.md
│   ├── architect.md
│   ├── implementer.md
│   ├── reviewer.md
│   └── researcher.md
├── skills/
│   ├── shipkit-spec/
│   ├── shipkit-plan/
│   ├── shipkit-architecture-memory/
│   └── ... (24 skills)
├── hooks/
│   ├── hooks.json
│   └── scripts/
│       ├── session-start.py
│       └── skill-router.py
└── .mcp.json                    # If any MCP integrations
```

---

## Pros & Cons

### Staying Skills-Only

**Pros:**
- Simpler distribution (just copy files)
- Works with any agent tool (Cursor, Copilot, etc.)
- No plugin system dependency
- Users can pick individual skills

**Cons:**
- No hooks (can't auto-run on session start)
- No commands (no `/shipkit-master`)
- No namespace protection
- Manual updates only
- Agents need separate installation

### Converting to Plugin

**Pros:**
- Full hook support (session start, skill routing)
- Commands for key workflows (`/shipkit`, `/shipkit-spec`)
- Namespace protection (`shipkit:skill-name`)
- Auto-updates from marketplace
- Single installation includes everything
- MCP server integration possible

**Cons:**
- Only works with Claude Code (not Cursor, etc.)
- More complex distribution
- Users can't pick individual components
- Requires plugin system understanding

### Hybrid Approach

**Option A: Plugin + Skills Separately**
- Core workflow as plugin (master, hooks, commands)
- Individual skills also available via skills.sh
- Users choose: full plugin OR à la carte skills

**Option B: Plugin That Installs Skills**
- Plugin with install command
- `/shipkit-install` copies skills to project
- Best of both worlds but complex

---

## What Would Change

### If Plugin

1. **Directory structure** → Standard plugin layout
2. **shipkit-master** → Becomes `/shipkit` command
3. **Session hook** → hooks.json SessionStart
4. **Skill router** → hooks.json or skill
5. **Distribution** → Marketplace + `plugin.json`
6. **Updates** → Automatic from marketplace

### User Experience Change

**Current (Skills):**
```
# Manual installation
python install.py

# Usage
"help me with specs"  → Claude auto-loads shipkit-spec skill
```

**As Plugin:**
```
# One-time install
/plugin marketplace add anthropics/shipkit
/plugin install shipkit@anthropics

# Usage
/shipkit              → Main workflow command
"help me with specs"  → shipkit:spec skill auto-loads
```

---

## Recommendation

### Short-term: Stay Skills + Add Commands Reference

Keep current skills approach but:
1. Document how users could invoke as commands
2. Add reference to official plugins users might want
3. Keep cross-agent compatibility

### Medium-term: Evaluate Hybrid

Consider:
1. Creating a minimal Shipkit plugin with just hooks + commands
2. Keeping skills installable separately
3. Plugin enhances but isn't required

### Long-term: Full Plugin (Maybe)

If Claude Code becomes dominant:
1. Convert to full plugin
2. Publish to marketplace
3. Keep skills.sh version for other agents

---

## Key Questions to Answer

1. **Who is the target user?**
   - Claude Code only → Plugin makes sense
   - Multi-agent (Cursor, Copilot) → Skills better

2. **How important are hooks?**
   - Essential → Need plugin
   - Nice-to-have → Skills sufficient

3. **Distribution preference?**
   - Marketplace discoverability → Plugin
   - Manual control → Skills

4. **Update frequency?**
   - Frequent updates → Plugin auto-update valuable
   - Stable releases → Manual updates fine

---

## Action Items

- [ ] Decide target audience (Claude Code only vs multi-agent)
- [ ] Evaluate hook importance for Shipkit workflow
- [ ] Test plugin-dev to understand full plugin creation
- [ ] Consider creating minimal "shipkit-core" plugin
- [ ] Keep skills.sh distribution regardless
