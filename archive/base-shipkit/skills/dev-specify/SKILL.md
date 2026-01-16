---
name: dev-specify
description: Create feature specifications from natural language descriptions by extracting requirements from user stories, interaction design, and brand guidelines. Use when the user asks to "spec", "specify", "create specification for" a feature, provides a feature description after product discovery, or says "I want to build [feature]" or "Add [feature]".
---

# Feature Specification

## Agent Persona

**Load:** `.claude/agents/dev-architect-agent.md`

Adopt: Systematic, documents trade-offs, favors simplicity, tests assumptions.

## Purpose

Create a comprehensive feature specification from a natural language feature description, grounded in product artifacts (user stories, interaction design, brand guidelines) and technical constitution.

**Key principle:** Extract from product artifacts, don't invent requirements.

## When to Trigger

User says:
- "Create a spec for [feature]"
- "Specify [feature]"
- "/dev-specify [feature description]"

Or provides natural language feature description after product discovery.

## Prerequisites

**Required:**
- Technical constitution (`.shipkit/skills/dev-constitution/outputs/constitution.md`)

**Recommended:**
- User stories (`.shipkit/skills/prod-user-stories/outputs/user-stories.md`)
- Interaction design (`.shipkit/skills/prod-interaction-design/outputs/interaction-design.md`)
- Brand guidelines (`.shipkit/skills/prod-brand-guidelines/outputs/brand-guidelines.md`)

If product artifacts missing, spec will be less grounded (but still possible).

## Inputs

**From user:**
- Natural language feature description (e.g., "Add user authentication", "Real-time notifications")

**From product artifacts:**
- User stories → Primary story this implements, acceptance criteria, user value
- Interaction design → User journeys, UI patterns, screen flows
- Brand guidelines → Visual style, component usage, tone of voice, accessibility
- Jobs-to-be-done → Core job, forces, anxieties
- Success metrics → Performance targets, reliability requirements
- Technical constitution → Tech stack, quality standards, constraints

## Process

### 1. Run Script

```bash
.shipkit/skills/dev-specify/scripts/create-spec.sh "Add user authentication"
```

Script will:
- Generate numbered spec directory (e.g., `specs/001/`)
- Copy template to `specs/001/spec.md`
- List available product artifacts
- Indicate ready for Claude

**For updates/clarifications:**
```bash
# Update existing spec (archives old version)
.shipkit/skills/dev-specify/scripts/create-spec.sh --update --spec 001

# Resolve [NEEDS_CLARIFICATION] markers
.shipkit/skills/dev-specify/scripts/create-spec.sh --clarify --spec 001
```

### 2. Read References

Read all files in the skill's references directory:
```bash
.shipkit/skills/dev-specify/references/
```

**If >2 files exist:** Ask the user which files are most relevant for this task.

This includes built-in guidance (reference.md, examples.md) and any user-added files (PDFs, research, notes).

---

### 3. Read Context

**Claude:** Read these files to ground the spec:

```bash
# Product artifacts (extract requirements)
.shipkit/skills/prod-user-stories/outputs/user-stories.md
.shipkit/skills/prod-interaction-design/outputs/interaction-design.md
.shipkit/skills/prod-brand-guidelines/outputs/brand-guidelines.md
.shipkit/skills/prod-jobs-to-be-done/outputs/jobs-to-be-done.md
.shipkit/skills/prod-success-metrics/outputs/success-metrics.md

# Technical constraints
.shipkit/skills/dev-constitution/outputs/constitution.md

# Template and guidance
.shipkit/skills/dev-specify/templates/spec-template.md
.shipkit/skills/dev-specify/references/reference.md
.shipkit/skills/dev-specify/references/examples.md
```

### 4. Extract from Product Artifacts

**From user stories:**
- Find primary story this feature implements
- Extract acceptance criteria → Functional requirements
- Extract user personas → UX considerations
- Extract priority (MoSCoW) → Scope decisions

**From interaction design:**
- Extract relevant user journey steps
- Extract screen flows and UI patterns
- Extract interaction details (taps, swipes, feedback)

**From brand guidelines:**
- Extract visual style requirements (colors, typography)
- Extract component usage (which design system components)
- Extract tone of voice for error messages/labels
- Extract accessibility standards (WCAG level)

**From jobs-to-be-done:**
- Extract core job this feature helps complete
- Extract forces (pushes/pulls, anxieties/habits)

**From success metrics:**
- Extract performance targets (latency, uptime)
- Extract metrics to track for this feature
- Extract success thresholds

**From technical constitution:**
- Extract tech stack to use
- Extract architecture patterns to follow
- Extract quality standards (testing, coverage)
- Extract performance/security requirements

### 5. Fill Template Conversationally

Use template structure, fill each section by asking user questions:

#### Overview
- **Problem:** What user/business problem exists? (from user stories + user input)
- **Solution:** What are we building? (high-level, from feature description)
- **Value:** Why build this? (user value + business value from stories/metrics)

#### User Stories
- **Primary Story:** Which user story from prod-user-stories does this implement?
- **Related Stories:** Any supporting stories?

#### Scope
- **In Scope:** What's included? (from user story acceptance criteria)
- **Out of Scope:** What's explicitly NOT included? (prevent scope creep)

#### User Experience
- **User Journey:** Extract from interaction-design
- **Key Interactions:** User actions → System responses
- **UI Requirements:** Extract from brand-guidelines

#### Functional Requirements
- Each requirement = one testable behavior
- Format: **[Name]**
  - Description: What it does
  - Acceptance: Given-When-Then (from user story)

#### Non-Functional Requirements
- **Performance:** Targets from success metrics/constitution
- **Security:** Auth/data protection from constitution
- **Reliability:** Uptime targets from success metrics
- **Accessibility:** WCAG level from brand guidelines

#### Technical Constraints
- Extract from dev-constitution (tech stack, patterns, quality standards)

#### Dependencies
- **External:** Third-party services, APIs, libraries
- **Internal:** Features that must exist first, shared components

#### Data Requirements
- **Data Models:** Key entities (defer schema to dev-plan)
- **Data Flow:** Where data comes from → how it's processed → where it goes

#### Edge Cases & Error Handling
- **Edge Cases:** Unusual but valid scenarios
- **Error States:** What can go wrong, user messages, recovery

#### Success Criteria
- **Done When:** Checklist of completion criteria
- **Metrics:** What to measure (from success metrics)

#### Open Questions
- Use `[NEEDS_CLARIFICATION: question]` for ambiguities
- Questions for product team
- Technical unknowns (okay - dev-plan will address)

### 5. Handle Ambiguities

**When requirements are unclear:**
- Add `[NEEDS_CLARIFICATION: specific question]` markers
- Don't invent answers - mark for clarification
- User can run `--clarify` later to resolve

**Example:**
```markdown
### Authentication
Users can log in with email/password or OAuth.

[NEEDS_CLARIFICATION: Which OAuth providers? Google? GitHub? Facebook?]
[NEEDS_CLARIFICATION: Password requirements? Use constitution defaults or custom?]
```

### 6. Write to Output File

**DO NOT** write manually to protected outputs.

Fill the spec content and Claude will write it to:
`.shipkit/skills/dev-specify/outputs/specs/NNN/spec.md`

### 7. Verify Quality

Before finalizing, check:
- [ ] Grounded in product artifacts (not invented)
- [ ] References specific user stories
- [ ] Requirements are testable (Given-When-Then)
- [ ] Scope is explicit (in/out)
- [ ] Edge cases considered
- [ ] Error handling specified
- [ ] Success criteria measurable
- [ ] Technical constraints from constitution

## Outputs

- `.shipkit/skills/dev-specify/outputs/specs/NNN/spec.md` (PROTECTED)
- `.shipkit/skills/dev-specify/outputs/specs/registry.txt` (Registry mapping)

## Constraints

- **DO NOT** create spec files manually (they're protected)
- **ALWAYS** run the script first
- **MUST** ground in product artifacts (extract, don't invent)
- **MUST** include testable acceptance criteria (Given-When-Then)
- **HIGH-LEVEL** - Defer technical decisions to dev-plan
- **USE MARKERS** - [NEEDS_CLARIFICATION] for ambiguities

## Extraction Examples

### From User Story to Spec

**User Story:**
```
As a mobile user
I want to save articles offline
So I can read during my commute

Acceptance:
- Save button available on articles
- Articles accessible without network
- Saved articles sync when online
```

**Extract to Spec:**
```markdown
## Problem
Mobile users (60% of traffic) lose access when offline, can't read saved content.

## Functional Requirements

1. **Offline Save**
   - Description: Save article for offline reading
   - Acceptance:
     - Given: User is viewing article
     - When: User taps save button
     - Then: Article is saved locally, accessible without network

2. **Auto-Sync**
   - Description: Sync saved articles when connection restores
   - Acceptance:
     - Given: User has offline saves and comes online
     - When: Connection detected
     - Then: Articles sync to server within 5s
```

### From Interaction Design to UX

**Interaction Design:**
```
Article Reading Journey - Step 5:
User sees bookmark icon (heart), taps to save, sees brief animation + "Saved!"
```

**Extract to Spec:**
```markdown
## User Experience

### Key Interactions
1. User taps heart icon → Brief scale animation → Toast "Saved!" → Icon fills

### UI Requirements
- Icon: Heart (Feather icon set, per brand)
- Animation: Scale 1.0 → 1.2 → 1.0 (200ms)
- Toast: "Saved!" (brand green, 2s duration)
```

### From Brand Guidelines to UI

**Brand Guidelines:**
```
Primary: Blue #4A90E2
Tone: Friendly, conversational
Accessibility: WCAG AA minimum
```

**Extract to Spec:**
```markdown
## UI Requirements
- Primary action buttons: Blue #4A90E2 (per brand)
- Error messages: Friendly tone ("Oops! Couldn't save. Try again?")
- Accessibility: WCAG AA, keyboard navigation, screen reader labels
```

## Next Steps

After spec created:
- Review with stakeholders
- Resolve any [NEEDS_CLARIFICATION] markers: `/dev-specify --clarify --spec N-name`
- When approved, create technical plan: `/dev-plan`

## Context

This is the **second dev skill** in the development pipeline.

**Workflow:**
```
dev-constitution (done)
         ↓
dev-specify "feature description" ← YOU ARE HERE
         ↓
dev-plan (next)
         ↓
dev-tasks
         ↓
dev-implement
```

## Common Mistakes to Avoid

1. **Inventing requirements** - Not grounded in user stories → Extract from product artifacts
2. **Over-specifying technical details** - "Use PostgreSQL JSONB with GIN index" → Defer to dev-plan
3. **Under-specifying user behavior** - "User can search" → "User enters term → sees results <2s, ranked by relevance"
4. **Ignoring product artifacts** - Making up UI without checking brand guidelines → Extract from brand-guidelines
5. **Vague success criteria** - "Works well" → "95% save success rate, <200ms p95 latency"

## Clarification Workflow

**Create spec:**
```bash
/dev-specify "Add OAuth login"
# Creates specs/003/spec.md
# May include [NEEDS_CLARIFICATION] markers
```

**Resolve ambiguities:**
```bash
/dev-specify --clarify --spec 003
# Claude finds markers, asks questions, updates spec
```

**Update spec later:**
```bash
/dev-specify --update --spec 003
# Archives old version, updates with new info
```
