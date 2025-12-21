# Shipkit Development Instructions

**You are developing the shipkit framework - an architectural layer on top of Claude Code.**

This repo contains shipkit: a complete product development framework delivered as Claude Code skills, agents, and constitutions.

**Core Principle:** Shipkit extends Claude Code with structured workflows. All development must align with official Claude Code documentation and patterns.

---

## What is Shipkit?

**Shipkit = Claude Code + Structured Product Workflow**

Claude Code provides:
- Skills system (slash commands)
- Agent personas (subagent contexts)
- MCP servers
- Hooks
- Settings & permissions

Shipkit adds:
- 37 pre-built skills (product discovery → implementation)
- 5 specialized agent personas
- Constitution templates (project rules)
- Unified workspace structure (`.shipkit/`)
- Specification-driven development workflow

**We build ON TOP of Claude Code, not alongside it.**

---

## Development Principles

### 1. Always Align with Claude Code Documentation

**Before implementing ANY feature:**
- Check official Claude Code docs: `https://docs.anthropic.com/claude/docs/claude-code`
- Verify skills syntax matches current spec
- Ensure agent persona format is correct
- Validate hook patterns are supported
- Confirm settings.json schema is current

**When uncertain about Claude Code features:**
- Don't guess or assume
- Check the official documentation first
- Test in a real Claude Code environment
- Ask the user if documentation is unclear

### 2. Shipkit is a Layer, Not a Fork

**What this means:**
- ✅ We create skills that work with Claude Code
- ✅ We provide agent personas Claude Code loads
- ✅ We supply constitutions Claude Code reads
- ✅ We organize workflows using Claude Code primitives
- ❌ We don't modify Claude Code itself
- ❌ We don't bypass Claude Code features
- ❌ We don't create parallel systems

**Example:**
- **Right:** Create a `/specify` skill that uses Claude Code's skill system
- **Wrong:** Build a custom command parser outside Claude Code

### 3. Test in Real Claude Code Environment

**Every change must be validated:**
1. Install shipkit in a test project using `install.sh`
2. Start Claude Code in that project
3. Run the modified skill/feature
4. Verify it works as expected
5. Check that constitutions load correctly
6. Ensure agents activate properly

**Don't develop in a vacuum.** Shipkit only matters if it works in Claude Code.

---

## Repository Structure

```
shipkit/
  install/                    # Everything users install
    skills/                   # 37 skills (directory/skill.md format)
    agents/                   # 5 agent personas
    constitutions/            # 4 constitution templates
    workspace/                # Scripts and templates for .shipkit/
    hooks/                    # Session start hooks
    CLAUDE.md                 # Usage instructions (for user projects)

  install.sh                  # Installer (copies install/ → target project)
  CLAUDE.md                   # THIS FILE - Development instructions
  README.md                   # User-facing documentation
  help/                       # Reference documentation
```

**Clean separation:**
- `install/` = what users get
- Everything else = framework development

---

## Key Development Tasks

### Adding a New Skill

1. **Check Claude Code skill format:**
   ```bash
   # Read official docs first!
   # Ensure you understand current skill.md schema
   ```

2. **Create skill directory:**
   ```bash
   mkdir install/skills/my-new-skill
   ```

3. **Write skill.md following Claude Code spec:**
   ```markdown
   ---
   description: Brief description
   handoffs:
     - label: Next Step
       agent: agent-name
       prompt: What to do next
   scripts:
     sh: path/to/script.sh
   ---

   ## Agent Persona
   Load: .claude/agents/agent-name.md

   ## Steps
   [Your skill implementation]
   ```

4. **Test in Claude Code:**
   ```bash
   cd ~/test-project
   bash ~/shipkit/install.sh
   # Start Claude Code
   # Run: /my-new-skill
   ```

5. **Verify agent loads correctly**
6. **Ensure handoffs work**
7. **Update `install/CLAUDE.md` routing tables**

### Modifying an Agent Persona

1. **Check Claude Code agent format:**
   - Agents are just markdown files
   - Claude Code loads them into context
   - They define personality, constraints, approach

2. **Edit agent file:**
   ```bash
   vim install/agents/my-agent.md
   ```

3. **Test by running skill that loads this agent**

4. **Verify persona behavior matches intent**

### Updating Constitution Templates

1. **Understand constitution layering:**
   ```
   .claude/constitutions/
     core.md              # Always loaded
     product/             # Loaded by product skills
       strategy.md
       audience.md
       ...
     technical/           # Loaded by technical skills
       tech-stack.md
       architecture.md
       ...
   ```

2. **Edit template:**
   ```bash
   vim install/constitutions/b2c-saas/core.md
   ```

3. **Test that skills load correct sections**

4. **Verify token efficiency** (skills shouldn't load everything)

### Modifying the Installer

1. **Keep it radically simple:**
   - One command install
   - Copy `install/` → target project
   - Create `.shipkit/` workspace
   - Install selected constitution template

2. **Test installation:**
   ```bash
   cd ~/test-project
   bash ~/shipkit/install.sh --constitution b2c-saas
   ```

3. **Verify all files copied correctly**

4. **Check that Claude Code recognizes skills**

---

## Aligning with Claude Code

### Official Documentation

**Primary source of truth:**
- Claude Code features: `https://docs.anthropic.com/claude/docs/claude-code`
- Skill system documentation
- Agent/subagent patterns
- Hook system
- Settings & permissions

**When documentation conflicts with your assumptions:**
- Documentation wins
- Update shipkit to match
- Don't try to work around it

### Claude Code Primitives

**Skills:**
- Must be in `.claude/skills/[skill-name]/skill.md` format
- Follow frontmatter schema exactly
- Handoffs use agent references
- Scripts are optional but useful

**Agents:**
- Live in `.claude/agents/[name].md`
- Just markdown files with personality/constraints
- Loaded when skill specifies them
- No special format beyond markdown

**Constitutions:**
- Live in `.claude/constitutions/`
- Skills specify which sections to load
- Layered (core + product + technical)
- Token-efficient selective loading

**Hooks:**
- Defined in `.claude/settings.json`
- Trigger on events (SessionStart, etc.)
- Run shell commands
- Can pass context to skills

**Workspace:**
- `.shipkit/` is our convention
- Not a Claude Code primitive
- Just organized file storage
- Skills read/write here

### What Claude Code Doesn't Provide

**Things shipkit adds:**
- Specific skill implementations (37 skills)
- Opinionated workflow (discovery → spec → code)
- Constitution templates (b2c-saas, etc.)
- Unified workspace structure
- Product discovery skills
- Specification-driven development

**These are all built USING Claude Code primitives, not replacing them.**

---

## Common Development Patterns

### When Adding Features

**Always ask:**
1. Does Claude Code already support this?
2. Are we using Claude Code correctly?
3. Is there official documentation?
4. Have we tested in real Claude Code environment?
5. Does this add value or just complexity?

### When Debugging

**Check:**
1. Is skill.md format correct?
2. Does agent file exist at specified path?
3. Is constitution section loading?
4. Are hooks triggering correctly?
5. Is settings.json valid JSON?

### When Users Report Issues

**Diagnose:**
1. Is this a shipkit bug or Claude Code behavior?
2. Does it work with fresh install?
3. Is their settings.json corrupted?
4. Are file paths correct?
5. Is Claude Code version compatible?

---

## Testing Strategy

### Local Testing

1. **Create test project:**
   ```bash
   mkdir ~/shipkit-test
   cd ~/shipkit-test
   git init
   ```

2. **Install shipkit:**
   ```bash
   bash ~/shipkit/install.sh --constitution b2c-saas
   ```

3. **Start Claude Code:**
   ```bash
   # In Claude Code CLI or IDE
   ```

4. **Test workflows:**
   ```bash
   /strategic-thinking
   /personas
   /specify
   /implement
   ```

5. **Verify:**
   - Skills execute
   - Agents load
   - Constitutions apply
   - Files created in `.shipkit/`

### Integration Testing

**Test complete workflows:**
- Full product discovery (9 sequential skills)
- Spec → Plan → Tasks → Implement
- Git workflows (worktrees, branching, PRs)
- TDD integration
- Code review flow

### Regression Testing

**After any change:**
- Re-install in test project
- Run key skills
- Check nothing broke
- Verify new feature works

---

## Avoiding Common Mistakes

### ❌ Don't Assume Claude Code Features

**Bad:**
```markdown
# Assuming Claude Code supports XYZ
Let's use this cool feature I imagined...
```

**Good:**
```markdown
# Check docs first
Looking at Claude Code documentation...
This feature is supported, here's how...
```

### ❌ Don't Build Parallel Systems

**Bad:**
```bash
# Creating custom skill parser
./shipkit-runner my-command
```

**Good:**
```bash
# Using Claude Code's skill system
/my-skill
```

### ❌ Don't Bypass Claude Code

**Bad:**
```markdown
# Implementing custom agent loading
Load my agent from custom location...
```

**Good:**
```markdown
# Using Claude Code's agent system
Load: .claude/agents/my-agent.md
```

### ❌ Don't Ignore Documentation

**Bad:**
```markdown
# Making up skill format
My custom frontmatter fields...
```

**Good:**
```markdown
# Following Claude Code skill spec
---
description: ...
handoffs: ...
scripts: ...
---
```

---

## Architecture Philosophy

### Radically Simple

**Every feature must earn its place:**
- Does it simplify the user's workflow?
- Can it be simpler?
- Does it align with Claude Code patterns?
- Is it tested in real environment?

### Opinionated but Flexible

**Strong defaults:**
- Constitution templates (b2c-saas, b2b-saas, etc.)
- Sequential workflows (discovery → spec → code)
- Unified workspace (`.shipkit/`)

**Escape hatches:**
- Users can modify constitutions
- Skills are just markdown (readable, editable)
- Scripts are bash/PowerShell (transparent)

### Built on Claude Code

**We don't replace, we extend:**
- Skills use Claude Code's system
- Agents use Claude Code's loading
- Constitutions use Claude Code's reading
- Hooks use Claude Code's triggering

**If Claude Code adds a feature:**
- We adopt it
- We don't compete with it
- We build on top of it

---

## Resources

### Official Documentation
- **Claude Code:** `https://docs.anthropic.com/claude/docs/claude-code`
- **Skills:** Check latest skill.md schema
- **Agents:** Subagent documentation
- **MCP:** Model Context Protocol
- **API:** Anthropic API docs

### Shipkit-Specific
- **Skill Examples:** `install/skills/`
- **Agent Examples:** `install/agents/`
- **Constitution Examples:** `install/constitutions/`
- **Installer:** `install.sh`
- **User Docs:** `README.md`

### Key Schemas

**Agent schema:**
---
name: your-sub-agent-name
description: Description of when this subagent should be invoked
tools: tool1, tool2, tool3  # Optional - inherits all tools if omitted
model: sonnet  # Optional - specify model alias or 'inherit'
permissionMode: default  # Optional - permission mode for the subagent
skills: skill1, skill2  # Optional - skills to auto-load
---

Your subagent's system prompt goes here. This can be multiple paragraphs
and should clearly define the subagent's role, capabilities, and approach
to solving problems.

Include specific instructions, best practices, and any constraints
the subagent should follow.

-----------------

**Skill Schema**
---
name: your-skill-name
description: Brief description of what this Skill does and when to use it
---

# Your Skill Name

## Instructions
Provide clear, step-by-step guidance for Claude.

## Examples
Show concrete examples of using this Skill.

For advanced usage, see [reference.md](reference.md).

Run the helper script:
```bash
python scripts/helper.py input.txt
```
---

**Skill File Structure**
my-skill/
├── SKILL.md (required)
├── reference.md (optional documentation)
├── examples.md (optional examples)
├── scripts/
│   └── helper.py (optional utility)
└── templates/
    └── template.txt (optional template)



### Questions to Ask Yourself

**Before implementing:**
- Have I checked Claude Code documentation?
- Am I using Claude Code primitives correctly?
- Does this align with official patterns?
- Can I test this in real Claude Code?

**After implementing:**
- Did I test in Claude Code environment?
- Does it work as expected?
- Is it simpler than before?
- Did I update documentation?

**When stuck:**
- What does Claude Code documentation say?
- How do official Claude Code examples work?
- Am I overcomplicating this?
- Should I ask the user?

---

## Remember

**Shipkit is successful when:**
1. It makes product development faster
2. It works seamlessly in Claude Code
3. It stays aligned with Claude Code evolution
4. Users understand and adopt it
5. It remains radically simple

**Shipkit fails when:**
1. It breaks in Claude Code
2. It conflicts with Claude Code patterns
3. It becomes complex and hard to maintain
4. It tries to replace Claude Code features
5. Development happens without testing

---

**Build with Claude Code, not against it. Test everything. Keep it simple.**
