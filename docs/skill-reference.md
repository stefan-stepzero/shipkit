# Skill Reference

Complete reference for all 36 Shipkit skills.

---

## Quick Reference

| Category | Skill | Purpose |
|----------|-------|---------|
| **Core** | `shipkit-master` | Workflow orchestration |
| | `shipkit-project-status` | Health check and gaps |
| | `shipkit-project-context` | Codebase scanning |
| | `shipkit-codebase-index` | Semantic indexing |
| | `shipkit-claude-md` | CLAUDE.md management |
| **Discovery & Planning** | `shipkit-why-project` | Vision definition |
| | `shipkit-product-discovery` | Personas, journeys, user needs |
| | `shipkit-product-definition` | Solution blueprint (mechanisms, patterns, features) |
| | `shipkit-goals` | Success criteria & stage gates |
| | `shipkit-spec` | Feature specification |
| | `shipkit-feedback-bug` | Bug investigation (5 Whys) |
| | `shipkit-plan` | Implementation planning |
| | `shipkit-thinking-partner` | Cognitive decision frameworks |
| **Implementation** | `shipkit-architecture-memory` | Architecture decisions & proposals |
| | `shipkit-data-contracts` | Type definitions |
| | `shipkit-integration-docs` | External API patterns |
| **Execution** | `shipkit-test-cases` | Code-anchored test case specs |
| | `shipkit-build-relentlessly` | Build until compiles |
| | `shipkit-test-relentlessly` | Test until green |
| | `shipkit-lint-relentlessly` | Lint until clean |
| | `shipkit-implement-independently` | Parallel isolated implementation |
| | `shipkit-team` | Agent team from plan |
| | `shipkit-cleanup-worktrees` | Clean stale worktrees |
| **Quality & Docs** | `shipkit-verify` | Quality verification |
| | `shipkit-preflight` | Production readiness |
| | `shipkit-scale-ready` | Scale & enterprise audit |
| | `shipkit-prompt-audit` | LLM prompt audit |
| | `shipkit-semantic-qa` | Semantic QA for API/UI |
| | `shipkit-qa-visual` | Visual QA with Playwright |
| | `shipkit-ux-audit` | UX analysis |
| | `shipkit-user-instructions` | User-facing docs |
| | `shipkit-communications` | Visual reports |
| | `shipkit-work-memory` | Session continuity |
| **System** | `shipkit-update` | Install/update Shipkit |
| | `shipkit-get-skills` | Find Claude Code skills |
| | `shipkit-get-mcps` | Find MCP servers |

*System infrastructure (not counted — auto-triggered, not user-invocable):*
- `shipkit-detect` — Pattern detection and queue creation (hook infrastructure)

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
✅ why.json exists
✅ stack.json exists
⚠️ No active specs
⚠️ architecture.json has no entries

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
**Writes:** `.shipkit/stack.json`

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

## Discovery & Planning (8 skills)

### shipkit-why-project

**Purpose:** Defines project vision, purpose, and constraints.

**When to use:**
- Starting a new project
- Project direction is unclear
- Need to document "why" for future sessions

**Reads:** Nothing
**Writes:** `.shipkit/why.json`

---

### shipkit-product-discovery

**Purpose:** Lightweight product discovery — personas, pain points, journeys, and opportunities.

**When to use:**
- Need to understand target users
- Planning user-facing features
- Want structured user research

**Reads:** `.shipkit/why.json`
**Writes:** `.shipkit/product-discovery.json`

---

### shipkit-product-definition

**Purpose:** Creates a solution blueprint: core mechanisms, UX patterns, differentiators, design decisions, and features grounded in those mechanisms.

**When to use:**
- After product discovery, before defining success criteria
- Need to design HOW the product works, not just WHAT it does
- Want mechanism-level thinking before jumping to features

**Reads:** `.shipkit/product-discovery.json`, `.shipkit/why.json`, `.shipkit/stack.json`
**Writes:** `.shipkit/product-definition.json`

---

### shipkit-goals

**Purpose:** Defines measurable success criteria with thresholds and verification methods, organized into stage gates that determine feature phasing (now/next/later).

**When to use:**
- After product definition, before creating specs
- Need to define what "done" looks like for each stage
- Want measurable criteria derived from the solution blueprint

**Reads:** `.shipkit/product-definition.json`, `.shipkit/product-discovery.json`, `.shipkit/why.json`
**Writes:** `.shipkit/goals.json`

---

### shipkit-spec

**Purpose:** Creates feature specifications with acceptance criteria.

**When to use:**
- Before implementing any non-trivial feature
- Need to clarify requirements
- Want documented acceptance criteria

**Reads:** `.shipkit/why.json`, `.shipkit/stack.json`, `.shipkit/product-definition.json`
**Writes:** `.shipkit/specs/active/*.json`

---

### shipkit-feedback-bug

**Purpose:** Processes user feedback or bug reports into investigated specs using 5 Whys root cause analysis.

**When to use:**
- Bug report needs investigation
- User feedback needs structured analysis
- Want to trace symptoms to root causes

**Reads:** Codebase, `.shipkit/specs/`
**Writes:** `.shipkit/specs/active/*.json`

---

### shipkit-plan

**Purpose:** Creates implementation plans from specs.

**When to use:**
- After creating a spec
- Before starting implementation
- Need task breakdown

**Reads:** `.shipkit/specs/active/*.json`
**Writes:** `.shipkit/plans/active/*.json`

---

### shipkit-thinking-partner

**Purpose:** Structured thinking partner for decisions using cognitive frameworks (pre-mortem, inversion, etc.).

**When to use:**
- Facing a difficult decision
- Want to stress-test an approach
- Need to think through trade-offs

**Reads:** Context as needed
**Writes:** Nothing (conversation only)

---

## Implementation (3 skills)

### shipkit-architecture-memory

**Purpose:** Two modes: (1) Solution Architect — proposes complete architecture from goals, stack, and specs. (2) Decision Logger — logs individual architecture decisions.

**When to use:**
- Starting a new project (solution architect mode)
- Made a significant technical decision (decision logger mode)
- Chose between alternatives
- Want future sessions to know "why"

**Reads:** `.shipkit/goals.json`, `.shipkit/stack.json`, `.shipkit/specs/`, `.shipkit/architecture.json`
**Writes:** `.shipkit/architecture.json`

---

### shipkit-data-contracts

**Purpose:** Defines data shapes and types across layers.

**When to use:**
- Defining API request/response shapes
- Creating database schemas
- Need consistent types

**Reads:** `.shipkit/specs/active/*.json`
**Writes:** `.shipkit/contracts.json`

---

### shipkit-integration-docs

**Purpose:** Fetches and caches current API patterns for external services.

**When to use:**
- Integrating with external API (Stripe, Supabase, etc.)
- Need current best practices
- Want security patterns

**Reads:** `.shipkit/stack.json`
**Writes:** `references/[service]-patterns.md`

---

## Execution (7 skills)

### shipkit-test-cases

**Purpose:** Generates code-anchored test case specs from implementation.

**When to use:**
- Need test coverage plan
- Want structured test cases before writing tests
- Preparing test strategy

**Reads:** Source code, specs
**Writes:** Test case specifications

---

### shipkit-build-relentlessly

**Purpose:** Runs build until it compiles, fixing errors iteratively.

**When to use:** After code changes, need clean build.

---

### shipkit-test-relentlessly

**Purpose:** Runs tests until green, fixing failures iteratively.

**When to use:** After implementation, need passing tests.

---

### shipkit-lint-relentlessly

**Purpose:** Runs linter until clean, fixing violations iteratively.

**When to use:** Before commit, need clean lint.

---

### shipkit-implement-independently

**Purpose:** Implements a feature in an isolated git worktree for parallel development.

**When to use:**
- Feature can be built independently
- Want to avoid branch conflicts
- Need parallel implementation

---

### shipkit-team

**Purpose:** Creates an agent team from an implementation plan for parallel execution.

**When to use:**
- Plan has 3+ parallel tasks
- Want coordinated multi-agent execution
- Need phase-gated parallel work

**Reads:** `.shipkit/plans/active/*.json`, `.shipkit/specs/active/*.json`

---

### shipkit-cleanup-worktrees

**Purpose:** Cleans up stale git worktrees from previous implementations.

**When to use:** Worktrees accumulating, need cleanup.

---

## Quality & Documentation (10 skills)

### shipkit-verify

**Purpose:** Verifies implementation quality across multiple dimensions.

**When to use:**
- After completing a feature
- Before merging/shipping
- Quality checkpoint

**Reads:** Spec, plan, implementation
**Writes:** Verification report

---

### shipkit-preflight

**Purpose:** Production readiness audit before deployment.

**When to use:**
- Before first deployment
- After major changes
- Production checklist

---

### shipkit-scale-ready

**Purpose:** Scale and enterprise readiness audit.

**When to use:**
- Preparing for growth
- Enterprise requirements check
- Infrastructure readiness

---

### shipkit-prompt-audit

**Purpose:** Audits LLM prompt architecture for quality and security.

**When to use:**
- Building LLM-powered features
- Reviewing prompt design
- Checking for prompt injection risks

---

### shipkit-semantic-qa

**Purpose:** Semantic QA for API outputs and UI screenshots.

**When to use:**
- Validating API response quality
- Checking UI against requirements
- Semantic correctness checks

---

### shipkit-qa-visual

**Purpose:** Visual QA with Playwright — UI goals + autonomous test generation.

**When to use:**
- Need visual regression testing
- Want autonomous UI test generation
- Checking UI rendering

---

### shipkit-ux-audit

**Purpose:** Analyzes UX patterns and suggests improvements.

**When to use:**
- UI feels off
- Want UX review
- Checking consistency

---

### shipkit-user-instructions

**Purpose:** Tracks manual tasks that need user action.

**When to use:**
- Need user to do something (sign up for service, etc.)
- Tracking setup steps
- Deployment prerequisites

**Writes:** `.shipkit/user-instructions.md`

---

### shipkit-communications

**Purpose:** Creates visual HTML reports and formatted communications.

**When to use:**
- Need to share project status
- Want visual summary
- Creating stakeholder update

---

### shipkit-work-memory

**Purpose:** Captures session progress for continuity.

**When to use:**
- End of work session
- Before long break
- Switching contexts

**Writes:** `.shipkit/progress.json`

---

## System (3 skills)

### shipkit-update

**Purpose:** Installs or updates Shipkit from GitHub.

**When to use:**
- New installation
- Updating to latest version

---

### shipkit-get-skills

**Purpose:** Discovers and helps install community Claude Code skills.

**When to use:**
- Looking for specific capability
- Want to extend Claude Code

---

### shipkit-get-mcps

**Purpose:** Discovers and helps install MCP servers.

**When to use:**
- Need external tool integration
- Looking for MCP capabilities

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

### New Product (Full Discovery)

```
/shipkit-why-project → /shipkit-product-discovery → /shipkit-product-definition
    → /shipkit-goals → /shipkit-spec → /shipkit-plan → (implement) → /shipkit-verify
```

### New Feature (Existing Product)

```
/shipkit-spec → /shipkit-plan → (implement) → /shipkit-verify
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
