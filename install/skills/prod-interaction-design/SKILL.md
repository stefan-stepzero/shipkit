---
name: prod-interaction-design
description: "Use when designing future-state user journeys and interaction patterns (TO-BE vision)"
---

# Interaction Design

## Agent Persona

**Load:** `.claude/agents/discovery-agent.md`

Adopt: User-journey focused, thinks in flows, anticipates friction points.

## Purpose
Define **FUTURE STATE**: Ideal user journeys and interaction patterns for how users will accomplish their goals with our product.

**Focus**: TO-BE vision, not current state.

## When to Trigger
User says:
- "How do users accomplish [X]?"
- "What's the user flow?"
- "Design the interaction"
- "Map the user journey"

## Prerequisites
- Personas defined (who is using this)
- JTBD current state (what needs to improve)
- Value proposition (what outcome we deliver)
- Brand guidelines (how it should feel)

## Inputs
- Personas (`.prodkit/discovery/personas.md`)
- JTBD (`.prodkit/discovery/jobs-to-be-done-current.md`)
- Value proposition (`.prodkit/strategy/value-proposition.md`)
- Brand guidelines (`.prodkit/brand/`)

## Process

### 1. For Each Key Job-to-Be-Done, Design the Ideal Journey

**Entry Point**: How does the user start?
- What triggers the journey?
- Where do they enter the product?
- First screen they see

**Critical Moments**: Where must we deliver value?
- Key decision points
- Moments of insight
- "Aha!" moments
- High-value interactions

**Decision Points**: Where does user choose a path?
- Branching logic
- Filters/options
- Personalization

**Success State**: What does completion look like?
- End goal achieved
- Next action suggested
- Satisfaction indicators

**Error States**: What can go wrong?
- Common errors
- Recovery paths
- Prevention strategies

### 2. Define Interaction Patterns

**Navigation Paradigm**:
- Sidebar / Top nav / Command palette
- Breadcrumbs / Back button
- Search prominence

**Primary Actions**:
- Buttons / Shortcuts / Gestures
- Keyboard-first vs Mouse-first
- Quick actions

**Feedback Mechanisms**:
- Success: Toasts / Inline / Modals
- Progress: Loading states / Skeletons
- Errors: Inline / Banner / Modal

**Loading States**:
- Skeleton screens
- Progress indicators
- Optimistic updates

**Empty States**:
- First-time user
- No results
- Onboarding cues

**Error Recovery**:
- Undo/redo
- Retry logic
- Clear next steps

### 3. Map to Brand Personality

Ensure patterns align with brand guidelines:
- Speed vs Delight
- Minimal vs Helpful
- Professional vs Playful

### 4. Call Script for Each Journey

```bash
.prodkit/scripts/bash/create-journey.sh \
  --persona "Sarah the Engineering Manager" \
  --journey "Morning team catchup" \
  --entry "Opens app first thing in morning (7 AM)" \
  --moments "1. See overnight digest (30s), 2. Identify blockers (20s), 3. Respond to urgent items (10s)" \
  --decisions "Expand for details vs Mark as read vs Share with team" \
  --success "Fully caught up in under 60 seconds, confident nothing critical was missed" \
  --errors "No updates (empty state), API failures (retry), Misclassified urgency (feedback loop)" \
  --patterns "Feed-based navigation, one-click expand, quick action buttons, keyboard shortcuts (j/k to navigate)"
```

Repeat for each critical journey.

## Outputs
- `.prodkit/design/future-state-journeys.md`
- `.prodkit/design/interaction-patterns.md`

## Constraints
- **DO NOT** create files manually
- **ALWAYS** use `create-journey.sh` script
- **FOCUS** on IDEAL experience, not technical constraints
- **REFERENCE** brand personality in interaction choices
- **MAP** to current-state JTBD (show improvement)

## Next Steps
After journeys designed:
- Write user stories (translate journeys into requirements)

## Context
This is **Step 6 of 9** in the ProdKit sequential workflow.
