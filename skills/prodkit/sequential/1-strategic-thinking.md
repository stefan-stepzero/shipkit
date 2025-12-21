---
description: "Use when defining product strategy, business model, or value proposition"
---

# Strategic Thinking

## Agent Persona

**Load:** `.claude/agents/discovery-agent.md`

Adopt: Strategic lens, challenges assumptions, explores "what if", keeps user at center.

## Purpose
Define the product's strategic direction, business model, and value proposition using the Playing to Win framework combined with Lean Canvas.

## When to Trigger
User says:
- "What should we build?"
- "Let's define our strategy"
- "What's our product strategy?"
- "Help me figure out our business model"
- "What's our value proposition?"

## Inputs
- User conversation about business goals
- Market research (optional, from .prodkit/inputs/strategy/)
- Competitive context (optional)

## Process

### 1. Ask Playing to Win Questions

Ask the user about:

**Winning Aspiration**: What does success look like in 3-5 years?
- Example: "Be the #1 async collaboration tool for remote engineering teams"

**Where to Play**: Which market segment/customers?
- Example: "Remote-first engineering teams, 10-100 people, Series A-C startups"

**How to Win**: What's your unique advantage?
- Example: "AI-powered digest that cuts morning catchup from 2 hours to 5 minutes"

**Core Capabilities**: What must you be great at?
- Example: "AI summarization, Slack/email integration, contextual understanding"

**Management Systems**: How will you measure/reinforce this?
- Example: "Weekly user interviews, NPS tracking, time-saved metrics"

### 2. Gather Lean Canvas Elements

Ask about:

**Problem** (top 3):
- What are the biggest pain points?

**Customer Segments**:
- Who specifically has this problem?

**Unique Value Proposition**:
- One sentence: What outcome do you deliver?

**Solution** (top 3 features):
- What will solve the problem?

**Channels**:
- How will customers discover you?

**Revenue Streams**:
- How will you make money?

**Cost Structure**:
- What are the major costs?

**Key Metrics**:
- What numbers matter most?

**Unfair Advantage**:
- What can't be easily copied?

### 3. Call Script

Once you have all information, call the script:

```bash
.prodkit/scripts/bash/create-strategy.sh \
  --winning-aspiration "..." \
  --where-to-play "..." \
  --how-to-win "..." \
  --capabilities "..." \
  --systems "..." \
  --problem "..." \
  --segments "..." \
  --value-prop "..." \
  --solution "..." \
  --channels "..." \
  --revenue "..." \
  --costs "..." \
  --metrics "..." \
  --unfair-advantage "..."
```

## Outputs
- `.prodkit/strategy/business-canvas.md`
- `.prodkit/strategy/value-proposition.md`

## Constraints
- **DO NOT** create files manually
- **ALWAYS** use `create-strategy.sh` script
- **ENSURE** all Playing to Win questions are answered
- **EXTRACT** value proposition for easy reference

## Next Step

**After completing this skill, suggest:**

```
✅ Strategic thinking complete.

📁 Created:
- .prodkit/strategy/business-canvas.md
- .prodkit/strategy/value-proposition.md

👉 **Next step:** `/constitution-builder --product` - Define product principles (brand voice, UX rules, accessibility)

Would you like to build the product constitution now?
```

## Context
This is **Step 1 of 9** in the ProdKit sequential workflow.

After constitution: `/personas` → `/jobs-to-be-done` → ... → `/success-metrics`
