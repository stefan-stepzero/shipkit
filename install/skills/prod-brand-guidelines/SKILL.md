---
name: prod-brand-guidelines
description: "Use when defining brand personality, visual direction, and interaction patterns"
---

# Brand Guidelines

## Agent Persona

**Load:** `.claude/agents/discovery-agent.md`

Adopt: Brand-aware, connects personality to user needs, consistent voice.

## Purpose
Define brand personality, visual direction, and interaction patterns. 80/20 focus: Capture enough to guide development, not a full brand book.

## When to Trigger
User says:
- "How should this look?"
- "What's our visual style?"
- "Define our brand"
- "What's the personality of this product?"

## Prerequisites
- Personas defined (who are we speaking to?)
- Market analysis complete (how to differentiate)
- Strategy defined (brand aligns with positioning)

## Inputs
- Personas (`.prodkit/discovery/personas.md`)
- Market analysis (`.prodkit/discovery/market-analysis.md`)
- Strategy (`.prodkit/strategy/business-canvas.md`)

## Process

### 1. Define Brand Personality

If the brand were a person, how would you describe them?

**Adjectives** (choose 3-5):
- Examples: professional, approachable, efficient, playful, serious, trustworthy, innovative

**Tone of Voice**:
- Formal vs Casual
- Serious vs Playful
- Expert vs Friendly
- Concise vs Descriptive

**Brand Voice**:
- How you communicate with users
- Example: "We're direct but empathetic. We respect your time."

### 2. Visual Direction

**Color Palette** (3-5 colors with rationale):
- Primary color + why
- Secondary colors + why
- Accent colors
- Example: "Calming blues (#2563EB) for stressed managers, neutral grays for readability"

**Typography Direction** (not specific fonts):
- Sans-serif vs Serif
- Modern vs Classic
- Geometric vs Humanist
- Readability priorities
- Example: "Clean sans-serif, high readability for scanning dense information"

**Visual Style**:
- Modern / Classic / Retro
- Minimal / Detailed
- Flat / Dimensional
- Playful / Serious

**Imagery Style**:
- Photography / Illustration / Abstract / Icons
- Realistic / Stylized
- Color treatment

### 3. Interaction Patterns

**Animation Speed**:
- Fast / Medium / Slow
- Energetic / Calm
- Respect user's time vs Delightful

**Feedback Style**:
- Subtle / Obvious
- Toasts / Inline / Modals
- Sound effects or silent

**Error Handling**:
- Apologetic / Matter-of-fact
- Helpful / Technical
- Example: "Friendly but not overly apologetic"

### 4. Competitive Differentiation

How does this FEEL different from competitors?
- Reference specific competitors from market analysis
- What feeling do you want users to have?

### 5. Reference Examples

**2-3 products** with similar visual feel:
- Product name + URL
- Specific elements to emulate (not copy)
- What you like about their approach

### 6. Call Script

```bash
.prodkit/scripts/bash/create-brand.sh \
  --personality "Professional, efficient, trustworthy, respectful of time" \
  --colors "Blue (#2563EB) calm/trust, Gray (#64748B) neutral/professional, Green (#10B981) success/positive" \
  --typography "Clean sans-serif, high readability, modern minimal" \
  --visual-style "Modern minimal, data-driven, spacious layout" \
  --animation "Quick and subtle - respect user's time, no gratuitous motion" \
  --error-handling "Matter-of-fact but helpful - show path forward" \
  --differentiation "Notion=infinite canvas (overwhelming), Asana=project board (task-focused), Slack=stream (chaotic). Us=morning digest dashboard (calm + focused)" \
  --references "Linear (speed + polish), Superhuman (efficiency + keyboard-first), Stripe Docs (clarity)"
```

## Outputs
- `.prodkit/brand/personality.md`
- `.prodkit/brand/visual-direction.md`
- `.prodkit/brand/reference-examples.md`

## Constraints
- **DO NOT** create files manually
- **ALWAYS** use `create-brand.sh` script
- **EVERY** decision must tie back to personas
- **INCLUDE** the WHY for each choice
- **REFERENCE** competitors for differentiation

## Next Steps
After brand defined:
- Design interaction flows (future state journeys)

## Context
This is **Step 5 of 9** in the ProdKit sequential workflow.
