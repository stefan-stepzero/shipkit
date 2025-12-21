---
name: prod-user-stories
description: "Use when translating future-state journeys into actionable product requirements"
---

# User Stories

## Agent Persona

**Load:** `.claude/agents/discovery-agent.md`

Adopt: User-value focused, testable outcomes, prioritization mindset.

## Purpose
Translate future-state journeys into actionable product requirements using standard user story format with MoSCoW prioritization.

## When to Trigger
User says:
- "What features do we need?"
- "Write user stories"
- "Turn these into requirements"
- "What should we build first?"

## Prerequisites
- Personas defined
- Future-state journeys designed
- Interaction patterns defined
- Value proposition clear

## Inputs
- Personas (`.prodkit/discovery/personas.md`)
- Future-state journeys (`.prodkit/design/future-state-journeys.md`)
- Interaction patterns (`.prodkit/design/interaction-patterns.md`)
- Value proposition (`.prodkit/strategy/value-proposition.md`)

## Process

### 1. Extract Stories from Journeys

For each **critical moment** in user journeys, create stories.

**User Story Format**:
```
As [persona]
I want [capability/interaction pattern]
So that [value proposition outcome]
```

**Acceptance Criteria** (use Given-When-Then):
```
Given [context/precondition]
When [action/trigger]
Then [expected result]
```

**Example**:
```
As Sarah the Engineering Manager
I want to see a digest of overnight updates from my team
So that I can catch up in under 60 seconds

Acceptance criteria:
- Given I open the app in the morning
  When the digest loads
  Then I see all Slack messages, PRs, and emails from the last 8-12 hours

- Given I'm viewing the digest
  When I click on an item
  Then it expands to show full context without leaving the page

- Given I've reviewed an item
  When I click "Mark as read"
  Then it's removed from my digest and won't appear again
```

### 2. Apply MoSCoW Prioritization

For each story, assign priority:

**Must Have**: MVP is broken without this
- Core value proposition
- Basic usability
- Critical user journey steps

**Should Have**: Important but can launch without
- Quality of life improvements
- Secondary features
- Nice polish

**Could Have**: Nice to have if time permits
- Delight features
- Edge cases
- Advanced functionality

**Won't Have**: Explicitly out of scope for now
- Future versions
- Low-value requests
- Complexity traps

### 3. Validate Against Personas

Every story must:
- Map to a specific persona
- Solve a documented pain point
- Deliver the value proposition

### 4. Call Script for Each Story

```bash
.prodkit/scripts/bash/create-stories.sh \
  --persona "Sarah the Engineering Manager" \
  --story "As Sarah, I want to see a digest of overnight updates, so I can catch up in under 60 seconds" \
  --acceptance "Given I open app in morning | When digest loads | Then I see all updates from last 8-12 hours" \
  --priority "Must have"
```

Repeat for each story. The script appends to the same file.

## Outputs
- `.prodkit/requirements/user-stories.md`

## Constraints
- **DO NOT** create files manually
- **ALWAYS** use `create-stories.sh` script
- **EVERY** story must map to a persona
- **EVERY** story must have acceptance criteria
- **MUST** prioritize with MoSCoW
- **NO** technical implementation details (focus on user value)

## Best Practices

**Good Stories**:
- User-focused (As [persona]...)
- Testable (clear acceptance criteria)
- Independent (can be built separately)
- Negotiable (details can be discussed)
- Valuable (delivers user outcome)
- Estimable (team can size it)
- Small (can be completed in one iteration)

**Bad Stories**:
- "As a developer, I want to use React..."
- "Implement database schema for users"
- "Build API endpoint for /users"

## Next Steps
After stories written:
- Identify assumptions and risks
- Define success metrics
- Optional: Run trade-off analysis to validate scope

## Context
This is **Step 7 of 9** in the ProdKit sequential workflow.
