---
name: shipkit-ux-audit
description: "Use when auditing implemented UI for missing UX patterns. Triggers: 'audit UX', 'check UX', 'missing patterns', 'UX gaps'."
argument-hint: "<component or area>"
context: fork
agent: shipkit-ux-designer-agent
allowed-tools:
  - Read
  - Glob
  - Grep
---

# shipkit-ux-audit - Lightweight UX Guidance

**Purpose**: Ensures UI patterns stay consistent and user-friendly across the application by providing UX guidance based on general best practices, existing patterns in the project, and optional user-specified personas (e.g., ADHD-friendly, elderly users).

---

## When to Invoke

**User triggers**:
- "What's the best UX pattern for this?"
- "How should this UI work?"
- "UX guidance for [component]"
- "Make this accessible"
- "Check UX consistency"

**Before**:
- Building new UI components
- Implementing forms, modals, toggles, lists, buttons
- Creating user interactions

**During**:
- Reviewing implemented UI
- Refining user experience
- Fixing UX inconsistencies

---

## Prerequisites

**Optional but helpful**:
- Existing patterns documented: `.shipkit/implementations.json`
- Architecture decisions: `.shipkit/architecture.json`
- Stack info: `.shipkit/stack.json`

**No prerequisites required** - Can provide general guidance even for new projects.

---

## Process

### Step 0: Check for Queue (Auto-Detect Mode)

**First, check if running in queue-driven mode**:

Read file (if exists): `.shipkit/.queues/ux-audit-needed.md`

**If queue file exists and has pending items**:
1. Parse the `## Pending` section for components needing UX audit
2. For each pending component:
   - Audit loading states, error handling, accessibility (Step 2-4 logic)
   - Document findings in component documentation
   - Move item from Pending to Completed in queue
3. Skip Step 1 questions (components already identified)
4. Continue with Step 2-5 for each component

**If queue file doesn't exist or is empty**:
- Continue to Step 1 (manual mode - ask user what they're building)

---

### Step 1: (Manual Mode) Confirm What User is Building

**Before providing guidance**, ask 2-3 questions:

1. **What UI element are you building?**
   - If not clear from user's message, ask specifically
   - Examples: "Form? Modal? Toggle? List? Button?"

2. **Any specific UX concerns or user needs?**
   - "Do you have specific accessibility requirements?"
   - "Any target user personas?" (e.g., ADHD-friendly, elderly users, mobile-first)
   - "Known constraints?" (e.g., must work offline, low bandwidth)

3. **Is this a new pattern or matching existing?**
   - "Have you built similar UI before in this project?"
   - Will check implementations.json to verify

**Why ask**: Tailor guidance to actual needs, not generic advice.

---

### Step 2: Read Existing Context

**Check for established patterns**:

```bash
# Existing UI patterns (if file exists)
.shipkit/implementations.json

# Architecture decisions about UX (if file exists)
.shipkit/architecture.json

# Tech stack (to know UI framework constraints)
.shipkit/stack.json

# Previous UX decisions (if file exists)
.shipkit/ux-decisions.json
```

**Verification before claiming patterns:**

| Claim | Required Verification |
|-------|----------------------|
| "Similar pattern exists" | `Grep: pattern="[component type]" path="implementations.json"` returns matches |
| "No existing pattern" | Grep returns 0 matches for component type AND related keywords |
| "Established UX decision" | Check `ux-decisions.json` decisions array for similar component |

**Never claim** "no similar component" without actually grepping implementations.json.

**Auto-detect**:
- Similar components in implementations.json
- Previous UX decisions in ux-decisions.json
- UI framework from stack.json (React, Vue, Svelte, etc.)

**Token budget**: Keep context reading under 1500 tokens.

---

### Step 3: Explore Actual UI Components

**Before generating guidance, examine the real code — not just JSON metadata.**

UX decisions based on `.shipkit/` context files alone miss actual component patterns, inconsistencies between components, and accessibility gaps that only show up in source code.

**Launch explore agents** — Use the Task tool with `subagent_type: Explore`:

```
Agent 1 - Component patterns: "Find UI components related to [component type]
in the codebase. Look for: existing component implementations, state management
patterns (loading/error/empty states), form handling patterns, modal patterns,
and shared UI utilities. Report: what patterns are established, which components
handle states well vs poorly, what UI library/primitives are in use."

Agent 2 - Consistency and gaps: "Scan all UI components for consistency in
UX patterns. Look for: components missing loading states, inconsistent error
handling, missing accessibility attributes (aria-*, role, tabIndex), hardcoded
strings that should be accessible, missing keyboard handlers, touch target sizes.
Report: which components follow good patterns, which have gaps, and what the
most common UX debt is."
```

**Launch both agents in parallel** — they are independent scans.

**Synthesize findings** — Before generating UX guidance, note:
- Established patterns to reference (e.g., "your existing modals use X pattern — follow that")
- Inconsistencies to flag (e.g., "3 forms validate inline, 2 don't — which is the standard?")
- Accessibility gaps in existing code that should be fixed alongside the new work
- UI library capabilities that inform what patterns are practical

**If exploration reveals inconsistencies**: Surface to user. Example: *"Your existing components handle loading states inconsistently — ListPage uses skeletons but DetailPage shows nothing. Should we standardize?"*

**Token budget**: Each explore agent should return a focused summary (~500 tokens).

**When to skip**: If providing guidance for a brand new project with no existing UI code.

---

### Step 4: Generate UX Guidance

**Provide terminal output AND log to `.shipkit/ux-decisions.json`**.

**Terminal output template**:

```
UX Guidance: [Component Name]

**Recommended Pattern**: [Pattern name and type]

**Why**: [1-2 sentence rationale based on principles below]

**Implementation Checklist**:
- [Specific implementation detail 1]
- [Specific implementation detail 2]
- [Specific implementation detail 3]
- [Accessibility requirement 1]
- [Accessibility requirement 2]

**Accessibility Notes**:
- [WCAG requirement 1]
- [WCAG requirement 2]
- [Keyboard interaction]
- [Screen reader consideration]

**[IF pattern exists in implementations.json or ux-decisions.json]**
**Existing Pattern Match**: [ComponentName]
- Reuse: [specific pattern to follow]
- Location: [file path or decision ID]

**[IF new pattern being established]**
**New Pattern**: This establishes a new pattern for your project

**Next Steps**:
- [Specific action 1]
- Run `/shipkit-architecture-memory` to log this pattern (if new)
- Run `implement (no skill needed)` when ready to build
```

---

### Step 5: Log UX Decision to JSON

**After providing terminal guidance, update `.shipkit/ux-decisions.json`**:

**If file doesn't exist**, create with initial structure:
```json
{
  "$schema": "shipkit-artifact",
  "type": "ux-decisions",
  "version": "1.0",
  "lastUpdated": "{current date}",
  "source": "shipkit-ux-audit",
  "summary": {
    "totalDecisions": 0,
    "totalGaps": 0,
    "byCategory": {
      "form": 0, "modal": 0, "toggle": 0, "list": 0,
      "button": 0, "navigation": 0, "feedback": 0, "other": 0
    },
    "byPersona": {
      "general": 0, "adhd-friendly": 0, "elderly": 0,
      "mobile-first": 0, "low-bandwidth": 0, "accessibility-first": 0
    }
  },
  "decisions": [],
  "gaps": []
}
```

**Add decision to array**:
```json
{
  "id": "UX-{next sequential number}",
  "component": "{Component name}",
  "category": "{form|modal|toggle|list|button|navigation|feedback|other}",
  "pattern": "{Specific pattern applied}",
  "decision": "{What was decided}",
  "rationale": "{Why this pattern - 1-2 sentences}",
  "accessibility": ["{WCAG requirements}"],
  "existingMatch": "{Reference or null}",
  "persona": "{general|adhd-friendly|elderly|mobile-first|low-bandwidth|accessibility-first}",
  "checklist": ["{Implementation requirements}"],
  "date": "{YYYY-MM-DD}"
}
```

**Update summary counts** after adding decision.

**Why log as JSON?**
- Enables programmatic queries (e.g., "all form decisions")
- Consistency checks across components
- Dashboard/reporting integration
- Other skills can reference patterns by ID

---

### Step 6: Identify and Log Gaps

**When auditing existing UI**, if patterns are missing:

**Add to gaps array**:
```json
{
  "id": "GAP-{next sequential number}",
  "component": "{Component or area}",
  "missingPatterns": ["{patterns needed}"],
  "priority": "{high|medium|low}",
  "notes": "{additional context or null}",
  "identifiedDate": "{YYYY-MM-DD}"
}
```

**Update `summary.totalGaps`** count.

**Priority guidelines**:
- `high`: Accessibility violations, security concerns, major usability issues
- `medium`: Missing feedback states, inconsistent patterns
- `low`: Polish items, nice-to-haves

---

### Step 7: Apply Progressive Disclosure

**Only share relevant principles** - Don't dump entire UX knowledge base.

**Quick reference by component type**:

#### For Forms:
- Inline validation, clear errors, submit button states, field focus, progressive disclosure

#### For Modals:
- Escape to close, focus trap, backdrop click, return focus, ARIA labels

#### For Toggles/Switches:
- Immediate feedback, loading state, undo option, confirmation for destructive

#### For Lists:
- Empty states, loading skeletons, virtualization, optimistic updates

#### For Buttons:
- Loading states, disabled states, success feedback, 44px touch target

**Apply relevant UX principles:**
1. **Cognitive Load Reduction** - Minimize choices, clear hierarchy, progressive disclosure
2. **Immediate Feedback** - Respond to every action within 100ms
3. **Reversibility** - Allow undo for destructive actions
4. **Consistency** - Match existing patterns in the project
5. **Accessibility** - WCAG 2.1 AA minimum (always required)
6. **Error Prevention** - Validate early, confirm destructive actions
7. **Mobile-First** - Touch targets 44px+, thumb zones, responsive design

---

## Step 8: Suggest Next Steps

---

## Completion Checklist

Copy and track:
- [ ] Explored actual UI components (patterns + consistency gaps)
- [ ] Reviewed implemented components against findings
- [ ] Checked against UX pattern checklist
- [ ] Documented decisions in ux-decisions.json
- [ ] Logged gaps with priorities

---

## What Makes This "Lite"

**Included**:
- General UX best practices (inline in SKILL.md)
- Common pattern guidance (forms, modals, toggles, lists, buttons)
- WCAG 2.1 AA accessibility basics
- Progressive disclosure (only relevant principles)
- Reads existing patterns from implementations.json
- Adapts to user personas (ADHD, elderly, etc. if specified)
- JSON output for programmatic consumption

**Not included** (vs full ux-coherence):
- No comprehensive UX library
- No design system templates
- No detailed research methodologies
- No usability testing frameworks
- No analytics integration

**Philosophy**: Provide good-enough UX guidance for POC/MVP, not comprehensive design system.

---

## When This Skill Integrates with Others

### Before This Skill

- `/shipkit-spec` - Creates feature requirements
  - **When**: Spec defines UI components needed
  - **Why**: UX guidance shapes how specified features should work
  - **Trigger**: Spec mentions forms, modals, toggles, or other UI elements

- `/shipkit-plan` - Plans implementation approach
  - **When**: Plan describes UI component structure
  - **Why**: UX patterns inform component architecture choices
  - **Trigger**: Plan needs UX pattern decisions before implementation

- `/shipkit-project-context` - Generates stack information
  - **When**: Stack includes UI framework (React, Vue, Svelte)
  - **Why**: UX guidance references stack.json to understand UI framework capabilities
  - **Trigger**: Need to know what UI primitives are available

### After This Skill

- `/shipkit-architecture-memory` - Logs architectural decisions
  - **When**: UX pattern becomes project-wide standard
  - **Why**: Document established UX patterns for future consistency
  - **Trigger**: New pattern created that should be reused across components

- `implement (no skill needed)` - Implements components
  - **When**: UX guidance complete, ready to build
  - **Why**: Implementation follows UX patterns and accessibility requirements
  - **Trigger**: User confirms "ready to implement"

- `document components manually` - Documents components
  - **When**: Component built and needs documentation
  - **Why**: Document UX decisions made for component
  - **Trigger**: Component complete, add to implementations.json

---

## Context Files This Skill Reads

**Optionally reads**:
- `.shipkit/implementations.json` - Existing UI components/patterns
- `.shipkit/architecture.json` - Past architectural decisions
- `.shipkit/stack.json` - UI framework info
- `.shipkit/ux-decisions.json` - Previous UX decisions

**Never reads**:
- Specs, plans, tasks (not relevant for UX guidance)

---

## Context Files This Skill Writes

**Writes to**:
- `.shipkit/ux-decisions.json` - Logs each UX decision with pattern, rationale, and accessibility requirements

**Write Strategy**: **READ-MODIFY-WRITE**
- Read existing file (or create if missing)
- Append new decision to `decisions` array
- Append new gaps to `gaps` array (if auditing)
- Update `summary` counts
- Update `lastUpdated` timestamp
- Write complete file back

**Why JSON?**
- Enables queries like "show all modal decisions"
- Supports gap tracking and resolution
- Dashboard integration for UX coverage
- Other skills can reference decisions by ID

---

## Lazy Loading Behavior

**This skill loads context on demand**:

1. User invokes `/shipkit-ux-audit`
2. Claude asks what component user is building
3. Claude reads ux-decisions.json (if exists) for existing decisions
4. Claude optionally reads implementations.json for similar patterns
5. Claude provides terminal guidance
6. Claude updates `.shipkit/ux-decisions.json`
7. Total context: ~500-1500 tokens (focused)

**Not loaded**:
- Specs, plans, tasks, progress logs (not needed)

---

<!-- SECTION:after-completion -->
## After Completion

**Guardrails Check:** Before moving to next task, verify:

1. **Persistence** - Has important context been saved to `.shipkit/`?
2. **Prerequisites** - Does the next action need a spec or plan first?
3. **Session length** - Long session? Consider `/shipkit-work-memory` for continuity.

**Natural capabilities** (no skill needed): Implementation, debugging, testing, refactoring, code documentation.

**Suggest skill when:** User needs to make decisions, create persistence, or check project status.
<!-- /SECTION:after-completion -->

<!-- SECTION:success-criteria -->
## Success Criteria

Guidance is complete when:
- [ ] User's component type identified
- [ ] Actual UI components explored for existing patterns and gaps
- [ ] Relevant UX principles shared (not all principles)
- [ ] Specific implementation checklist provided
- [ ] Accessibility requirements included
- [ ] Existing patterns referenced (if applicable)
- [ ] UX decision logged to `.shipkit/ux-decisions.json`
- [ ] Summary counts updated
- [ ] Gaps identified and logged (if auditing existing UI)
- [ ] Next steps suggested (implement or log architectural decision)
<!-- /SECTION:success-criteria -->
---

## Common Scenarios

- **Reusing existing patterns** - Check ux-decisions.json and implementations.json first, reference by ID
- **Creating new patterns** - Provide guidance, log decision with new ID
- **Accessibility-focused requests** - Apply persona adaptations (see below)
- **Reviewing existing UI** - Audit against pattern checklists, log gaps

---

## Tips for Effective UX Guidance

**Be specific**:
- "Use Switch component with aria-checked" (not "make it accessible")
- "44px touch target" (not "mobile-friendly")
- "Toast with undo for 5 seconds" (not "allow reversal")

**Reference existing patterns**:
- Check ux-decisions.json for decisions by component type
- Reuse patterns when applicable
- Only create new patterns when necessary

**Progressive disclosure**:
- Share only relevant principles (not all 7)
- Focus on component-specific guidance
- Don't overwhelm with theory

**Accessibility is not optional**:
- Always include basic WCAG checklist
- Keyboard navigation always required
- Screen reader support always required

**When to defer to full /ux-coherence**:
- Complex design systems
- Multi-platform consistency (web + mobile apps)
- Comprehensive accessibility audits
- User research and testing
- Advanced interaction patterns

---

## User Persona Adaptations

**When user specifies a persona, adapt guidance accordingly.**

**Persona adaptations:**
- **ADHD-Friendly** - Minimize options, auto-save, no timers, clear success feedback
- **Elderly Users** - Large text/targets, high contrast, confirmations, easy undo
- **Mobile-First** - Touch targets 44px+, thumb zones, swipe gestures, no hover-only
- **Low-Bandwidth** - Minimize media, loading skeletons, offline support, optimistic updates
- **Accessibility-First** - Beyond WCAG AA: keyboard efficiency, excellent screen reader support

**Adapt principles to persona, but maintain accessibility baseline.**

---

**Remember**: Good UX is invisible. Users shouldn't think about the interface - it should just work. When in doubt, choose the pattern that requires the least cognitive load and follows existing conventions.

**Schema reference**: See `references/output-schema.md` for complete JSON schema.
**Example**: See `references/example.json` for a sample output.
