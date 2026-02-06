# Skill Reference

Complete reference for all 23 Shipkit skills.

---

## Quick Reference

| Category | Skill | Purpose |
|----------|-------|---------|
| **Core** | `shipkit-master` | Workflow orchestration |
| | `shipkit-project-status` | Health check and gaps |
| | `shipkit-project-context` | Codebase scanning |
| | `shipkit-codebase-index` | Semantic indexing |
| | `shipkit-claude-md` | CLAUDE.md management |
| **Discovery** | `shipkit-why-project` | Vision definition |
| | `shipkit-product-discovery` | Personas and journeys |
| | `shipkit-spec` | Feature specification |
| | `shipkit-plan` | Implementation planning |
| | `shipkit-prototyping` | Rapid UI mockups |
| | `shipkit-prototype-to-spec` | Extract learnings |
| **Implementation** | `shipkit-architecture-memory` | Decision logging |
| | `shipkit-data-contracts` | Type definitions |
| | `shipkit-integration-docs` | External API patterns |
| **Quality** | `shipkit-verify` | Quality verification |
| | `shipkit-preflight` | Production readiness |
| | `shipkit-ux-audit` | UX analysis |
| | `shipkit-user-instructions` | User-facing docs |
| | `shipkit-communications` | Visual reports |
| | `shipkit-work-memory` | Session continuity |
| **System** | `shipkit-detect` | Auto-triggered detection |
| | `shipkit-get-skills` | Find Claude Code skills |
| | `shipkit-get-mcps` | Find MCP servers |

---

## Core Workflow (5 skills)

### shipkit-master

**Purpose:** Meta skill for workflow orchestration. Shows available skills and suggests next steps.

**When to use:**
- Starting a new session
- Unsure what skill to use next
- Need workflow guidance

**Reads:** All `.shipkit/` context files
**Writes:** Nothing (guidance only)

---

### shipkit-project-status

**Purpose:** Health check showing what context exists, what's missing, and gaps to address.

**When to use:**
- Starting work on a project
- Feeling lost about project state
- Checking what documentation exists

**Reads:** All `.shipkit/` files
**Writes:** Nothing (report only)

**Example output:**
```
✅ why.md exists
✅ stack.md exists
⚠️ No active specs
⚠️ architecture.md has no entries

Suggested: Create a spec with /shipkit-spec
```

---

### shipkit-project-context

**Purpose:** Scans codebase to detect tech stack, frameworks, and project structure.

**When to use:**
- First time setting up Shipkit
- After major stack changes
- Need to document existing project

**Reads:** Project files (package.json, etc.)
**Writes:** `.shipkit/stack.md`

---

### shipkit-codebase-index

**Purpose:** Creates semantic index mapping concepts to files for faster navigation.

**When to use:**
- Large codebase (>50 files)
- Claude struggles to find relevant files
- Want to reduce glob/grep usage

**Reads:** Project source files
**Writes:** `.shipkit/codebase-index.json`

---

### shipkit-claude-md

**Purpose:** Manages and updates CLAUDE.md with project-specific learnings and preferences.

**When to use:**
- Want to add project-specific rules
- Need to update working preferences
- Discovered patterns Claude should follow

**Reads:** Current `CLAUDE.md`
**Writes:** `CLAUDE.md` (updates)

---

## Discovery & Planning (6 skills)

### shipkit-why-project

**Purpose:** Defines project vision, constraints, and success criteria.

**When to use:**
- Starting a new project
- Project direction is unclear
- Need to document "why" for future sessions

**Questions asked:**
- What problem are you solving?
- Who is this for?
- What does success look like?
- What constraints exist?

**Reads:** Nothing
**Writes:** `.shipkit/why.md`

---

### shipkit-product-discovery

**Purpose:** Creates user personas and journey maps.

**When to use:**
- Need to understand target users
- Planning user-facing features
- Want structured user research

**Reads:** `.shipkit/why.md`
**Writes:** `.shipkit/personas/*.md`

---

### shipkit-spec

**Purpose:** Creates feature specifications with acceptance criteria.

**When to use:**
- Before implementing any non-trivial feature
- Need to clarify requirements
- Want documented acceptance criteria

**Reads:** `.shipkit/why.md`, `.shipkit/stack.md`
**Writes:** `.shipkit/specs/active/*.md`

**Spec includes:**
- Overview
- User flow
- Acceptance criteria (Given/When/Then)
- Technical approach

---

### shipkit-plan

**Purpose:** Creates implementation plans from specs.

**When to use:**
- After creating a spec
- Before starting implementation
- Need task breakdown

**Reads:** `.shipkit/specs/active/*.md`
**Writes:** `.shipkit/plans/*.md`

---

### shipkit-prototyping

**Purpose:** Creates rapid HTML prototypes for UI validation.

**When to use:**
- Need to validate UI before coding
- Want quick visual mockup
- Testing interaction patterns

**Reads:** Spec if exists
**Writes:** `.shipkit-mockups/*.html`

---

### shipkit-prototype-to-spec

**Purpose:** Extracts validated patterns from prototypes into specs.

**When to use:**
- After prototyping session
- Before deleting prototype
- Want to preserve learnings

**Reads:** `.shipkit-mockups/*/iterations.md`
**Writes:** Updates `.shipkit/specs/active/*.md`

---

## Implementation (3 skills)

### shipkit-architecture-memory

**Purpose:** Logs architecture decisions with rationale (append-only).

**When to use:**
- Made a significant technical decision
- Chose between alternatives
- Want future sessions to know "why"

**Reads:** Nothing
**Writes:** `.shipkit/architecture.md` (append)

**Entry format:**
```markdown
## 2026-02-03: [Decision Title]

**Decision:** What you decided

**Rationale:** Why you decided it

**Alternatives considered:** What else you considered

**Trade-offs:** What you're giving up
```

---

### shipkit-data-contracts

**Purpose:** Defines data shapes and types across layers.

**When to use:**
- Defining API request/response shapes
- Creating database schemas
- Need consistent types

**Reads:** `.shipkit/specs/active/*.md`
**Writes:** `.shipkit/types.md`

---

### shipkit-integration-docs

**Purpose:** Fetches and caches current API patterns for external services.

**When to use:**
- Integrating with external API (Stripe, Supabase, etc.)
- Need current best practices
- Want security patterns

**Reads:** `.shipkit/stack.md`
**Writes:** `references/[service]-patterns.md`

**Supported services:**
- Lemon Squeezy, Stripe, Paddle (payments)
- Supabase, PlanetScale (database)
- OpenAI, Anthropic (AI)
- Resend, SendGrid (email)
- Clerk, Auth0 (auth)

---

## Quality & Documentation (6 skills)

### shipkit-verify

**Purpose:** Verifies implementation quality across 12 dimensions.

**When to use:**
- After completing a feature
- Before merging/shipping
- Quality checkpoint

**Reads:** Spec, plan, implementation
**Writes:** Verification report

**Dimensions checked:**
- Spec compliance
- Acceptance criteria
- Error handling
- Security basics
- Performance
- Accessibility

---

### shipkit-preflight

**Purpose:** Production readiness audit before deployment.

**When to use:**
- Before first deployment
- After major changes
- Production checklist

**Reads:** Codebase, configuration
**Writes:** Preflight report

---

### shipkit-ux-audit

**Purpose:** Analyzes UX patterns and suggests improvements.

**When to use:**
- UI feels off
- Want UX review
- Checking consistency

**Reads:** UI components
**Writes:** UX audit report

---

### shipkit-user-instructions

**Purpose:** Tracks manual tasks that need user action.

**When to use:**
- Need user to do something (sign up for service, etc.)
- Tracking setup steps
- Deployment prerequisites

**Reads:** Nothing
**Writes:** `.shipkit/user-instructions.md`

---

### shipkit-communications

**Purpose:** Creates visual HTML reports and formatted communications.

**When to use:**
- Need to share project status
- Want visual summary
- Creating stakeholder update

**Reads:** `.shipkit/` context
**Writes:** HTML report

---

### shipkit-work-memory

**Purpose:** Captures session progress for continuity.

**When to use:**
- End of work session
- Before long break
- Switching contexts

**Reads:** Recent work
**Writes:** `.shipkit/progress.md`

---

## System (3 skills)

### shipkit-detect

**Purpose:** Auto-triggered pattern detection that creates work queues.

**When to use:** Never invoked directly — triggered by hooks after other skills complete.

**Modes:**
- `services` — Detects external services in specs
- `contracts` — Detects data structures in plans
- `changes` — Detects modified files
- `ux-gaps` — Detects UX review needs

**Reads:** Various based on mode
**Writes:** `.shipkit/.queues/*.md`

---

### shipkit-get-skills

**Purpose:** Discovers and helps install community Claude Code skills.

**When to use:**
- Looking for specific capability
- Want to extend Claude Code
- Exploring skill ecosystem

**Reads:** Nothing
**Writes:** Installation instructions

---

### shipkit-get-mcps

**Purpose:** Discovers and helps install MCP servers.

**When to use:**
- Need external tool integration
- Looking for MCP capabilities
- Extending Claude Code

**Reads:** Nothing
**Writes:** MCP configuration

---

## Natural Capabilities (No Skill Needed)

These are things Claude does well without skills:

| Task | Just Ask |
|------|----------|
| Debug code | "Debug this error" |
| Implement feature | "Implement the login from the plan" |
| Write tests | "Add tests for this function" |
| Refactor | "Refactor this to use hooks" |
| Document code | "Add JSDoc to this file" |
| Fix bugs | "Fix the null pointer in checkout" |

**Rule:** If Claude can do it well without guidance, don't use a skill.

---

## Skill Workflows

### New Feature

```
/shipkit-spec → /shipkit-plan → (implement) → /shipkit-verify
```

### New Project

```
/shipkit-why-project → /shipkit-project-context → /shipkit-spec → ...
```

### Session End

```
/shipkit-work-memory
```

### Architecture Decision

```
/shipkit-architecture-memory
```

### External Integration

```
/shipkit-integration-docs → (implement)
```
