# Shipkit Light Development Instructions

**You are developing Shipkit Light - a streamlined product development framework built on Claude Code.**

This repo contains Shipkit Light: a focused, lightweight framework delivered as Claude Code skills, agents, and constitutions.

> **Note:** The full Shipkit framework (dev-*, prod-* skills) has been archived to `archive/base-shipkit/`. This repo now exclusively supports Shipkit Light.

**Core Principle:** Shipkit Light extends Claude Code with structured workflows. All development must align with official Claude Code documentation and patterns.

---

## What is Shipkit Light?

**Shipkit Light = Claude Code + Streamlined Product Workflow**

Claude Code provides:
- Skills system (slash commands)
- Agent personas (subagent contexts)
- MCP servers
- Hooks
- Settings & permissions

Shipkit Light adds:
- 19 pre-built lite skills (product discovery → implementation)
- 6 specialized lite agent personas
- Constitution templates (project rules)
- Unified workspace structure (`.shipkit-lite/`)
- Specification-driven development workflow

**We build ON TOP of Claude Code, not alongside it.**

---

## Active Components

### Lite Skills (19 total)
All skills use the `lite-` prefix and are located in `install/skills/`:

**Core Workflow:**
- `lite-shipkit-master` - Meta skill for workflow orchestration
- `lite-project-status` - Health check and gap analysis
- `lite-project-context` - Codebase scanning, stack detection

**Discovery & Planning:**
- `lite-product-discovery` - Personas, journeys, user stories
- `lite-why-project` - Strategic vision definition
- `lite-spec` - Feature specification
- `lite-plan` - Implementation planning
- `lite-prototyping` - Rapid UI mockups (structured prototype location)
- `lite-prototype-to-spec` - Extract learnings from prototypes

**Implementation:**
- `lite-architecture-memory` - Decision logging
- `lite-data-contracts` - Type definitions (Zod patterns)
- `lite-component-knowledge` - Component documentation
- `lite-route-knowledge` - Route documentation
- `lite-integration-docs` - Integration patterns

**Quality & Documentation:**
- `lite-ux-audit` - UX analysis and patterns
- `lite-user-instructions` - User-facing documentation
- `lite-communications` - Rich HTML visual output
- `lite-work-memory` - Session memory and context

**System Skills (auto-triggered):**
- `lite-detect` - Unified detection and queue creation (modes: services, contracts, changes, ux-gaps)

### Lite Agents (6 total)
Located in `install/agents/`:
- `lite-product-owner-agent.md` - Product/vision focus
- `lite-ux-designer-agent.md` - UX/design perspective
- `lite-architect-agent.md` - Technical architecture focus
- `lite-implementer-agent.md` - Implementation focus
- `lite-reviewer-agent.md` - Code review/quality focus
- `lite-researcher-agent.md` - Research/discovery focus

### Configuration Files
- `install/profiles/lite.manifest.json` - Skill/agent manifest
- `install/settings/lite.settings.json` - Permissions and configuration
- `install/claude-md/lite.md` - Project instructions
- `install/shared/hooks/lite-session-start.py` - Session initialization
- `install/shared/hooks/lite-after-skill-router.py` - Auto-detection routing

---

## Development Principles

### 1. Always Align with Claude Code Documentation

**Before implementing ANY feature:**
- Check official Claude Code docs: `https://docs.anthropic.com/claude/docs/claude-code`
- Check local best practices: `claude-code-best-practices/`
- Verify skills syntax matches current spec
- Ensure agent persona format is correct
- Validate hook patterns are supported
- Confirm settings.json schema is current

**When uncertain about Claude Code features:**
- Don't guess or assume
- Check `claude-code-best-practices/REFERENCES-BEST-PRACTICES.md` FIRST (primary reference)
- Check `claude-code-best-practices/` folder for additional materials
- Check the official documentation
- Test in a real Claude Code environment
- Ask the user if documentation is unclear

**Primary Reference:** `claude-code-best-practices/REFERENCES-BEST-PRACTICES.md`
- **Read this FIRST when creating or modifying skills**
- Extracted best patterns from Obra (methodology) and Speckit (quality enforcement)
- Documents Shipkit's hybrid approach and innovations
- Includes quick reference cheat sheets and pattern selection guide

**Reference folder:** `claude-code-best-practices/` contains:
- **REFERENCES-BEST-PRACTICES.md** - PRIMARY REFERENCE (start here)
- **BUILDING-LITE-SKILLS.md** - LITE SKILL QUALITY GUIDE (creating/editing lite skills)
- Official Claude Code documentation extracts
- Skill authoring best practices
- Agent persona guidelines
- Comparative analysis (shipkit vs speckit vs obra)
- Source repositories (obra-repo/, speckit/)

**When creating or editing Lite skills:**
- **MUST READ**: `claude-code-best-practices/BUILDING-LITE-SKILLS.md`
- Covers 7-file integration system (manifest, hooks, routing, etc.)
- Defines quality standards (cross-references, checklists, Iron Laws, etc.)
- Production-ready = Integration (7 files) + Quality (Part 10)
- DO NOT skip quality standards - they ensure causality, discoverability, and maintainability

### 2. The Skill Value Test (CRITICAL)

**Before creating, keeping, or modifying ANY skill, apply this test:**

A skill is VALUABLE if it does one of these:
1. **Forces human decisions to be explicit** - Vision, trade-offs, priorities, domain knowledge
2. **Creates persistence Claude lacks** - Institutional memory that survives sessions

A skill is REDUNDANT if:
- **Claude does it well without instruction** - Debugging, documenting, implementing, communicating

#### What Claude is Naturally Good At (Don't Create Skills For These)

| Capability | Why No Skill Needed |
|------------|---------------------|
| Debugging | Show error → Claude investigates systematically |
| Implementing | Given a spec, Claude builds it |
| Documenting code | "Document this" works without a skill |
| Communicating | Tone, formatting, structure are built-in |
| Prototyping | "Build a quick prototype" just works |

#### What Claude Cannot Do (Skills ARE Valuable Here)

| Gap | Why Skill Helps |
|-----|-----------------|
| **Know the vision** | Only humans know WHY this project exists |
| **Make trade-offs** | "X over Y because Z" requires human judgment |
| **Understand users** | Personas, journeys require human insight |
| **Model the domain** | Data contracts reflect business reality |
| **Remember across sessions** | Claude has no memory - skills create persistence |
| **Know what's missing** | Gap analysis requires structured prompting |

#### The Litmus Test

Before creating a skill, ask:

> "If I just asked Claude to do this without a skill, would it work?"

- If YES → Don't create the skill
- If NO (because it requires human input or persistence) → Create the skill

#### Examples

| Request | Skill Needed? | Why |
|---------|---------------|-----|
| "Debug this error" | ❌ No | Claude debugs naturally |
| "Document our architecture decisions" | ✅ Yes | Requires human decisions + persistence |
| "Implement the login feature" | ❌ No | Claude implements when given spec |
| "Define our user personas" | ✅ Yes | Requires human insight about users |
| "Write unit tests" | ❌ No | Claude writes tests naturally |
| "What's our technology stack?" | ✅ Yes | Creates persistent stack.md |

**This principle is non-negotiable. Every skill in Shipkit Light must pass this test.**

---

### 3. Claude's AI-Specific Limitations (Why Skills Exist)

**Claude is trained on human coding patterns but operates under fundamentally different constraints.**

#### The Awareness Gap

Claude doesn't naturally "know":
- **Its own nature** - Ephemeral, no memory, context-limited
- **That it needs to persist things** - Humans naturally remember; Claude doesn't
- **AI-optimized patterns** - Training data reflects human workflows, not AI workflows
- **What skills are available** - Unless explicitly told at session start

#### Human Coder vs AI Coder

| Aspect | Human Coder | AI Coder (Claude) |
|--------|-------------|-------------------|
| Memory | Persistent - remembers yesterday | Ephemeral - each session is new |
| Context | Unlimited - knows entire project history | Limited - only sees what's loaded |
| Continuity | Natural - picks up where they left off | Requires explicit handoff artifacts |
| Self-awareness | Knows their limitations | Trained on human patterns, unaware of own constraints |

#### Why This Matters for Shipkit Light

Skills exist to **compensate for AI-specific limitations** that Claude isn't naturally aware of:

- `/lite-work-memory` - Creates the session continuity Claude lacks
- `/lite-architecture-memory` - Persists decisions Claude would otherwise forget
- `/lite-project-context` - Explicitly loads context Claude can't "just know"
- `/lite-shipkit-master` - Tells Claude what skills exist (discoverability)

**Without these skills, Claude will code like a human who has memory - but it doesn't.**

#### The Implication

Don't assume Claude will naturally:
- Save important decisions (it won't unless told)
- Know to check for existing context (it needs prompting)
- Understand session boundaries (it thinks in continuous time)
- Suggest appropriate skills (it doesn't know they exist)

**Shipkit Light skills make the implicit explicit - compensating for what AI training data doesn't teach.**

---

### 4. Shipkit Light is a Layer, Not a Fork

**What this means:**
- ✅ We create skills that work with Claude Code
- ✅ We provide agent personas Claude Code loads
- ✅ We supply constitutions Claude Code reads
- ✅ We organize workflows using Claude Code primitives
- ❌ We don't modify Claude Code itself
- ❌ We don't bypass Claude Code features
- ❌ We don't create parallel systems

**Example:**
- **Right:** Create a `/lite-spec` skill that uses Claude Code's skill system
- **Wrong:** Build a custom command parser outside Claude Code

### 5. Use Simple File Operations - Don't Overcomplicate

**CRITICAL: When editing files, use the simplest available tool.**

**For file edits:**
1. **Read** the file first (required before Write)
2. **Write** the file with new content
3. Done.

**DO NOT:**
- ❌ Use complex bash heredocs or cat commands
- ❌ Use Python scripts for simple file writes
- ❌ Create temporary files and copy them
- ❌ Use sed/awk when Write tool is simpler
- ❌ Overthink the operation

**Right:** `Read(file.md)` then `Write(file.md, new_content)`

**Wrong:** Complex bash heredocs, Python scripts, temp files

**Exception:** Bash IS appropriate for git, tests, builds, system operations.

**If you catch yourself writing complex bash for a simple file edit, STOP and use Read + Write instead.**

---

### 6. MECE Skill Coverage (Mutually Exclusive, Collectively Exhaustive)

**Every development action should map to exactly one of:**
1. A specific skill (for human decisions or persistence)
2. A declared "natural capability" (for things Claude does well without instruction)

**Nothing should fall through to unstructured territory.**

#### The MECE Principle

| Category | Coverage | Examples |
|----------|----------|----------|
| Human Decisions | Skills | Vision, specs, architecture choices, user research |
| Persistence Needs | Skills | Session memory, component docs, route docs |
| Natural Capabilities | No skill | Implementation, debugging, testing, refactoring |

**If an action doesn't clearly fit either category, it's a gap in the framework.**

#### Why This Matters

Without MECE coverage:
```
User: "Add a login feature"
Claude: *starts coding immediately*
→ No spec, no plan, monolithic mess
```

With MECE coverage:
```
User: "Add a login feature"
Claude: *checks* Does spec exist? No → suggest /lite-spec first
→ Structured, intentional development
```

#### Guardrails, Not Chains

The goal is **coverage assurance**, not **mandatory chaining**.

- ❌ "After every skill, you MUST invoke /lite-whats-next"
- ✅ "Before acting on a feature request, check: Does a spec exist? Does a plan exist?"

**Rules enforce coverage. Skills capture decisions and create persistence.**

---

### 7. Prompt Engineering Trade-offs

**When writing skills, understand the cost of specificity.**

#### The Specificity-Flexibility Trade-off

| More Specific | More Flexible |
|---------------|---------------|
| Better format consistency | Better edge case handling |
| More predictable output | More adaptable to context |
| Narrower applicability | Broader applicability |

#### Examples Bias Output

Every example in a prompt shifts the probability distribution:

```markdown
# This biases toward the example format AND content
Example output:
- User: John, 35, software engineer
- Pain point: Too many meetings
```

Claude will now lean toward:
- Similar age ranges
- Similar professions
- Similar pain point framing

**Examples are powerful but costly.** Use them for format, not content.

#### Principles for Skill Prompts

1. **Be specific about structure, flexible about content**
   - ✅ "Output as markdown table with columns: X, Y, Z"
   - ❌ "Output like this example: [detailed example]"

2. **Constraints should enable, not restrict**
   - ✅ "Ask 2-3 clarifying questions before generating"
   - ❌ "Ask these exact questions: [list]"

3. **Prefer principles over prescriptions**
   - ✅ "Ensure the spec is implementation-agnostic"
   - ❌ "Never mention React, Vue, or Angular in specs"

4. **Test edge cases**
   - Does the skill work for a CLI tool? A mobile app? An API?
   - If not, the prompt is too specific

---

## Working Documents - Where to Create and Find Tracking Documents

### What Are Working Documents?

Working documents are files Claude Code creates to track:
- Implementation progress and status
- Migration plans and restructuring efforts
- Skill completion references
- Architecture decision records
- Development plans and specifications
- Task breakdowns and checklists
- Any other documents created to organize, plan, or track work

### Where to Create Working Documents

**ALWAYS create working documents in:**
```
claude-working-documents/
```

**Examples of working documents:**
- `RESTRUCTURING-PLAN.md` - Track skill migration progress
- `LITE-SKILLS-STATUS.md` - Skill implementation reference
- `MIGRATION-STATUS.md` - Migration tracking
- `IMPLEMENTATION-NOTES.md` - Development notes
- `ARCHITECTURE-DECISIONS.md` - ADR documents

### When to Create Working Documents

Create a working document in `claude-working-documents/` when:
1. The user asks to "track progress" or "create a plan"
2. You need to document implementation status across multiple sessions
3. You're tracking a multi-step migration or restructuring
4. You need a reference document for completed work
5. You're documenting architecture decisions
6. You're breaking down a large task into phases

### Naming Convention

Use UPPERCASE-WITH-HYPHENS.md for working documents:
- ✅ `SKILL-MIGRATION-PLAN.md`
- ✅ `LITE-SKILLS-STATUS.md`
- ✅ `IMPLEMENTATION-NOTES.md`
- ❌ `notes.md` (too vague)
- ❌ `temp.md` (unclear purpose)

### Where to Look for Working Documents

**ALWAYS check `claude-working-documents/` FIRST when:**
1. The user references a "plan" or "status document"
2. You need to check implementation progress
3. You're resuming work from a previous session
4. The user asks "what's the status of X"
5. You need context about completed or in-progress work

### What NOT to Put in Working Documents

**Don't create working documents for:**
- Temporary scratch notes (use memory)
- Single-session todos (use TodoWrite tool)
- User-facing documentation (goes in appropriate docs/ folder)
- Code or implementation files (goes in src/, lib/, etc.)
- Product artifacts (goes in .shipkit-lite/skills/*/outputs/)

**Keep `claude-working-documents/` focused on tracking and planning documents only.**

---

## Archived Components

The full Shipkit framework (dev-*, prod-*, shipkit-* skills and non-lite agents) has been archived to `archive/base-shipkit/`. See `archive/base-shipkit/README.md` for restoration instructions if needed.
