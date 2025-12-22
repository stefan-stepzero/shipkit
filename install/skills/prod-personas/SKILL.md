---
name: prod-personas
description: "Use when defining target user personas with demographics, goals, and pain points"
---

# Personas

## Agent Persona

**Load:** `.claude/agents/discovery-agent.md`

Adopt: Empathy-driven, asks about real behaviors, avoids stereotypes, grounds in evidence.

## Purpose
Define target user personas with demographics, goals, pain points, and behavioral patterns.

## When to Trigger
User says:
- "Who are our users?"
- "Let's create personas"
- "Our target customer is..."
- "Define our user personas"

Or uploads:
- User research documents
- Survey results
- Interview transcripts

## Prerequisites
- Strategy defined (`.prodkit/strategy/business-canvas.md` exists)

## Inputs
- Strategy (who we're building for)
- User research (optional, from `.prodkit/inputs/personas/`)
- Market analysis (optional)

## Process

### Step 0: Check Product Constitution (Recommended)

**If product constitution exists:**
- Read `.shipkit/skills/prod-constitution-builder/outputs/product-constitution.md`
- Project type guides persona depth:
  - **POC:** 1 persona (primary user only - validate with minimal scope)
  - **Side Project MVP:** 1-2 personas (keep minimal)
  - **Experimental:** 1 persona (who will test the experiment hypothesis)
  - **B2C Greenfield:** 2-3 personas (primary + secondary user types)
  - **B2B Greenfield:** 3-5 personas (decision maker, end user, admin, influencer)
  - **Existing Project:** Document existing user types already served

**If constitution doesn't exist:** Default to 2-3 personas (medium depth)

---

### 1. Determine Number of Personas

Ask: "How many distinct user types do we have?"
- **Recommended**: 1-3 personas (stay focused)
- **Too many**: Dilutes focus, hard to prioritize

### 2. For Each Persona, Gather Information

**Name**: Give them a memorable name
- Example: "Sarah the Engineering Manager"

**Demographics**:
- Age range
- Role/title
- Experience level
- Company size

**Goals**: What are they trying to achieve?
- Professional goals
- Personal goals
- Success metrics

**Pain Points**: What frustrates them today?
- Current problems
- Intensity (how painful?)
- Frequency (how often?)

**Current Behavior**: How do they solve the problem now?
- Tools they use
- Workflows they follow
- Workarounds they've created

**Tech Savviness**: Comfort with technology
- High/Medium/Low
- Influences feature complexity

**Decision Factors**: What influences their choices?
- Price sensitivity
- Brand preferences
- Feature priorities

### 3. Call Script for Each Persona

```bash
.prodkit/scripts/bash/create-persona.sh \
  --name "Sarah the Engineering Manager" \
  --age "35-45" \
  --role "Engineering Manager, Series B startup" \
  --goals "Stay aligned with remote team across timezones" \
  --pains "Spends 2+ hours daily catching up on Slack, email, PRs" \
  --behaviors "Checks Slack first thing AM, scans updates, messages blockers" \
  --tech-savvy "High" \
  --decision-factors "Efficiency, reliability, team adoption"
```

Repeat for each persona.

## Outputs
- `.prodkit/discovery/personas.md` (all personas in one file)

## Constraints
- **DO NOT** create `personas.md` manually
- **ALWAYS** use `create-persona.sh` script
- **MINIMUM** 1 persona, **MAXIMUM** 3 personas
- **USE** real, relatable names for personas

## Next Steps
After personas defined:
- Define jobs-to-be-done (what job does each persona hire your product to do?)

## Context
This is **Step 2 of 9** in the ProdKit sequential workflow.
