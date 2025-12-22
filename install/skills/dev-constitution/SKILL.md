---
name: dev-constitution
description: Create technical development standards from product strategy defining architecture, design, and coding principles for your product. Use when the user says "create technical standards", "define development principles", "set up technical constitution", "what are our coding standards", or after completing product discovery. Run once before the dev pipeline.
---

# Technical Constitution

## Agent Persona

**Load:** `.claude/agents/dev-architect-agent.md`

Adopt: Systematic, thinks in constraints and trade-offs, prefers simplicity, questions complexity.

## Purpose

Create a **lean, high-level** technical constitution defining architecture, design, and coding principles for your product.

**Critical:** Keep <500 words. This constitution is read by ALL dev skills (specify, plan, tasks, implement), so token efficiency matters.

## When to Trigger

User says:
- "Create technical standards"
- "Define our development principles"
- "Set up technical constitution"
- "What are our coding standards?"
- After completing product discovery (prod-* skills)

Or explicitly:
- `/dev-constitution`
- `/dev-constitution --create`

## Prerequisites

**Recommended (not required):**
- Product user stories (`.shipkit/skills/prod-user-stories/outputs/user-stories.md`)
- Business strategy (`.shipkit/skills/prod-strategic-thinking/outputs/business-canvas.md`)
- Success metrics (`.shipkit/skills/prod-success-metrics/outputs/success-metrics.md`)

If product artifacts missing, constitution will be minimal but still useful.

## Inputs

**From product artifacts (if available):**
- User stories → Tech stack hints, performance needs, security requirements
- Strategy → Product stage (POC/MVP/Established), scale expectations, constraints
- Success metrics → Performance targets, reliability requirements
- Assumptions & risks → Technical risks to mitigate

**From user conversation:**
- Team expertise (what tech does team know?)
- Existing codebase (greenfield or brownfield?)
- Compliance needs (GDPR, SOC2, etc.)
- Organizational constraints (cloud provider, approved languages, etc.)

## Process

### 1. Run Script

```bash
.shipkit/skills/dev-constitution/scripts/create-constitution.sh
```

**Available flags:**
- `--create` - Force creation (default: auto-detects mode)
- `--update` - Update existing constitution with versioning
- `--archive` - Archive current version and create new
- `--skip-prereqs` - Skip prerequisite checks
- `--interactive` - Force interactive mode (ignore product artifacts)
- `--cancel` - Cancel operation

**Script behavior:**

The script auto-detects the best mode:

**Extraction Mode (if product artifacts found):**
- Scans for 10 product artifacts (strategic-thinking, personas, user-stories, etc.)
- Lists which artifacts were found
- Claude will auto-extract technical constraints from them
- User reviews and refines the draft

**Interactive Mode (if no product artifacts):**
- Claude asks clarifying questions
- User provides technical preferences directly
- Constitution built from conversation

**Force interactive:** Use `--interactive` to ignore product artifacts and build via dialogue only.

Script output:
- Check for existing constitution (if exists, ask to --update or --archive)
- Scan and list available product artifacts (10 potential sources)
- Point to template and references
- Indicate mode (extraction or interactive)
- Ready for Claude

### 2. Read Context

**Claude:** Read these files to understand the product:

```bash
# Product artifacts (extract technical implications)
.shipkit/skills/prod-user-stories/outputs/user-stories.md
.shipkit/skills/prod-strategic-thinking/outputs/business-canvas.md
.shipkit/skills/prod-success-metrics/outputs/success-metrics.md
.shipkit/skills/prod-assumptions-and-risks/outputs/assumptions-and-risks.md
.shipkit/skills/prod-constitution-builder/outputs/product-constitution.md

# Template and guidance
.shipkit/skills/dev-constitution/templates/constitution-template.md
.shipkit/skills/dev-constitution/references/reference.md
.shipkit/skills/dev-constitution/references/examples.md
```

### 3. Ask Clarifying Questions

**Determine product stage first (critical for appropriateness):**
- POC: Speed > everything. Minimal quality gates.
- MVP: Balance pragmatism with quality. Some technical debt OK.
- Established: Optimize for reliability and maintainability.

**Then ask:**
- Team's tech expertise? (Python/JavaScript/Go/etc.)
- Existing codebase or greenfield?
- Compliance requirements? (GDPR, SOC2, PCI, HIPAA?)
- Cloud provider? (AWS/GCP/Azure/self-hosted?)
- Team size and growth plans?
- Known constraints? (approved tech list, legacy integrations?)

### 4. Extract from Product Artifacts

**From user stories:**
- Mobile app mentioned? → Consider React Native, Flutter
- Real-time collaboration? → WebSockets, event-driven architecture
- Works offline? → Offline-first principles
- Payment processing? → PCI compliance, secure APIs

**From strategy:**
- "Launch in 6 weeks" → Speed-focused POC approach
- "Series B funding" → MVP quality, plan for scale
- "10,000 daily users" → Performance and reliability standards

**From success metrics:**
- "99.9% uptime" → Fault tolerance, monitoring, redundancy
- "Sub-200ms latency" → Performance budgets, caching strategies
- "80% mobile users" → Mobile-first design

### 5. Fill Template (Conversationally)

Use template structure, fill each section:

#### 1. Technical Principles
- **Architecture:** How systems are organized (monolith/microservices/layered)
- **Design:** How code is structured (SOLID, composition patterns)
- **Code Quality:** What good code looks like (readability, DRY/KISS/YAGNI balance)

#### 2. Constraints & Non-Negotiables
- **Must Have:** Security, compliance, performance targets
- **Must Avoid:** Known anti-patterns, over-engineering traps

#### 3. Tech Stack
- List core technologies with **brief** rationale (why this choice?)
- Match product stage (POC = speed, MVP = balance, Established = optimize)

#### 4. Quality Standards
- **Testing:** Coverage targets, TDD policy, required test types
- **Performance:** Key metrics with acceptable ranges
- **Security:** Authentication approach, vulnerability scanning

#### 5. Development Workflow
- **Branching:** Strategy (feature branches? trunk-based?)
- **Reviews:** Requirements (who reviews? what must pass?)
- **CI/CD:** What checks must pass before deploy?
- **Documentation:** What must be documented?

### 6. Write to Output File

**DO NOT** write manually to `.shipkit/skills/dev-constitution/outputs/constitution.md`.

The file is PROTECTED. Instead, provide the filled constitution content and Claude will write it (settings.json allows skill execution context to write).

### 7. Verify Token Efficiency

**Target: <500 words total**

If constitution is >500 words:
- Remove prose, use bullet points
- Defer details to dev workflow ("API contracts defined in dev-plan")
- Link to external docs instead of explaining
- Remove redundant explanations

**Good rule:** If something can be specified later (dev-plan, dev-tasks), don't put it in constitution.

## Outputs

- `.shipkit/skills/dev-constitution/outputs/constitution.md` (PROTECTED)

## Constraints

- **DO NOT** create `constitution.md` manually (it's protected)
- **ALWAYS** run the script first
- **MUST** keep <500 words (token efficiency)
- **HIGH-LEVEL only** - no implementation details
- **PRODUCT-AWARE** - ground in product artifacts, not generic advice
- **STAGE-APPROPRIATE** - POC/MVP/Established have different needs

## Token Efficiency Examples

❌ **Verbose (100 words):**
> "We believe that code readability is of paramount importance and should be the primary consideration when writing code. Developers should prioritize clear, self-documenting code that can be easily understood by other team members. This includes using descriptive variable names, writing functions that do one thing well, and avoiding overly complex nested logic that is difficult to follow."

✅ **Concise (12 words):**
> "Readability first. Self-documenting code, single-purpose functions, avoid deep nesting."

**Saved:** 88 words × average 1.3 tokens/word = ~114 tokens!

## Next Steps

After constitution created:
- Constitution is now consumed by all dev skills
- Ready to create feature specs: `/dev-specify "feature description"`
- Update constitution when product stage changes: `/dev-constitution --update`

## Context

This is the **first dev skill** in the development pipeline. Run it ONCE after product discovery, before creating any specs.

**Workflow:**
```
Product Discovery (prod-* skills)
         ↓
dev-constitution --create (ONCE, sets standards) ← YOU ARE HERE
         ↓
Per-feature pipeline:
  dev-specify → dev-plan → dev-tasks → dev-implement → dev-finish
```

## Common Mistakes to Avoid

1. **Too detailed** - "All API endpoints return JSON with { status, data, message }" → This goes in API specs, not constitution
2. **Too generic** - "Write clean code, follow best practices" → Useless platitudes
3. **Too long** - >1000 words → Will waste tokens in every dev skill
4. **Not product-aware** - Copying a template without considering user stories, strategy, stage
5. **Wrong abstraction level** - Specifying file structures, function signatures → These emerge in dev-plan/implement

## When to Update Constitution

Re-run `/dev-constitution --update` when:
- Product stage changes (POC → MVP → Established)
- Major technical decision (switching frameworks, adding microservices)
- New constraints (compliance requirements, performance SLAs)
- Team learns a hard lesson (add anti-pattern to "Must Avoid")

Script will auto-archive old version before updating.
