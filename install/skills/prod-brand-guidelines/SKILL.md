---
name: prod-brand-guidelines
description: "Use when defining brand personality, voice, tone, and visual direction. Creates comprehensive brand guidelines covering values, traits, communication style, and visual identity. References brand archetypes and provides context-specific tone guidance."
---

# prod-brand-guidelines

Define brand personality, voice, tone, and visual direction.

## When to Use

User says:
- "Define our brand personality"
- "What should our visual style be?"
- "How should we sound in the product?"
- "Brand guidelines"
- "Visual direction"

## Prerequisites

- Strategic thinking complete (`.shipkit/skills/prod-strategic-thinking/outputs/business-canvas.md`)
- Market analysis complete (`.shipkit/skills/prod-market-analysis/outputs/market-analysis.md`)

If prerequisites missing, suggest running `/prod-strategic-thinking` and `/prod-market-analysis` first.

## What This Skill Does

Creates comprehensive brand guidelines covering:
1. **Brand Personality:** Core values, traits, archetypes
2. **Voice & Tone:** Consistent voice, context-dependent tone variations
3. **Visual Direction:** Colors, typography, visual style
4. **Usage Examples:** Real applications across contexts

## Agent Persona

**Load:** `.claude/agents/prod-product-designer-agent.md`

Adopt: Creative, empathetic designer who thinks about user emotions and visual consistency.

## Execution Steps

### 1. Run the Script

```bash
bash .shipkit/skills/prod-brand-guidelines/scripts/create-brand-guidelines.sh
```

**If script exits with decision needed:**
- `FILE_EXISTS`: Ask user if they want to --update, --archive, or --cancel
- `PREREQUISITE_MISSING`: Ask user if they want to --skip-prereqs or run prerequisite first

**Rerun with chosen flag:**
```bash
bash .shipkit/skills/prod-brand-guidelines/scripts/create-brand-guidelines.sh --update
```

### 2. Read Context Artifacts

Before defining brand, read:
- `.shipkit/skills/prod-strategic-thinking/outputs/business-canvas.md` - positioning
- `.shipkit/skills/prod-personas/outputs/personas.md` - target users
- `.shipkit/skills/prod-market-analysis/outputs/market-analysis.md` - competitor brands

### 3. Read References

Read all files in the skill's references directory:
```bash
.shipkit/skills/prod-brand-guidelines/references/
```

**If >2 files exist:** Ask the user which files are most relevant for this task.

This includes built-in guidance (reference.md, examples.md) and any user-added files (PDFs, research, notes).

### 4. Guide Brand Definition

Use **dialogue-driven approach** to define each section:

#### Brand Personality
Ask user about:
- Core values (what does brand stand for?)
- Personality traits (3-5 specific, actionable traits)
- Brand archetype (Hero, Creator, Caregiver, Explorer, etc.)

Ensure specificity:
- Bad: "Innovative and user-focused"
- Good: "The engineer who explains things clearly, not the expert who talks over your head"

#### Voice & Tone
Define:
- Consistent voice characteristics (professional, casual, technical, etc.)
- Tone variations by context (onboarding, errors, success, marketing)
- Language do's and don'ts

Write examples for each tone variation.

#### Visual Direction
Discuss:
- Color palette (2-3 primary, 2-3 secondary, functional colors)
- Typography (1-2 font families maximum)
- Visual style (minimal/maximal, modern/classic, serious/playful)
- Iconography style

Reference personas:
- What colors/styles resonate with target users?

Reference market analysis:
- How do competitors brand themselves?
- How should we differentiate?

#### Create Examples
Apply brand to real scenarios:
- Marketing headline
- Onboarding message
- Error message
- Empty state
- Success confirmation

Test if it feels authentic.

### 5. Write to Output File

Fill `.shipkit/skills/prod-brand-guidelines/outputs/brand-guidelines.md` with:
- All brand personality sections
- Complete voice/tone guide with examples
- Full visual direction specifications
- Example applications

Use the template structure, but adapt based on product maturity:
- **POC:** Keep it simple (2-3 values, basic palette, one font)
- **MVP:** Standard guidelines
- **Established:** Comprehensive system

### 6. Validate Brand Guidelines

Run through testing checklist:

**The Swap Test:**
Could competitor use these same guidelines?
- If YES → Be more specific

**The Cringe Test:**
Read voice examples out loud.
- If sounds robotic → Rewrite to be more human

**The Alignment Test:**
Do voice, tone, and visuals support same personality?
- If NO → Adjust to be consistent

**The Persona Test:**
Would target users resonate with this brand?
- If NO → Reference personas and adjust

## Key Behaviors

### Be Specific, Not Generic
- Challenge vague traits like "innovative, user-focused, quality"
- Ask: "How does this show up? Give me a concrete example"
- Ensure brand could only describe THIS product, not any competitor

### Ensure Consistency
- Voice, tone, and visuals must align
- Don't mix casual voice with formal visuals
- Don't mix playful personality with serious tone

### Reference Context
- Check personas: Does brand appeal to target users?
- Check market analysis: How does this differentiate from competitors?
- Check strategy: Does brand support positioning?

### Make It Actionable
- Every guideline should have examples
- Designers/writers should be able to USE this immediately
- Include both do's and don'ts

### Acknowledge Constraints
- For POC/MVP: Keep it simple, focus on essentials
- For established products: Can be more comprehensive
- Never create complexity for its own sake

## Common Mistakes to Avoid

### Generic Corporate Speak
User: "Our values are innovation, quality, and customer focus"
→ Challenge: "Those could describe any company. What's SPECIFIC to you?"

### Mismatched Elements
User defines playful voice but wants corporate blue + serif fonts
→ Flag: "Your voice says playful, but visuals say formal. Let's align these."

### No Differentiation
Brand could apply to any competitor
→ Ask: "How is your brand different from [competitor X]?"

### Aspirational vs. Authentic
Brand is what they WISH they were, not what they ARE
→ Ask: "Is this who you are TODAY, or who you want to be in 3 years?"

## Output Format

The brand guidelines file should be:
- **Comprehensive:** Covers personality, voice, tone, visuals
- **Specific:** Concrete examples, not abstract concepts
- **Actionable:** Team can use it immediately
- **Differentiated:** Unique to this product

## What Happens Next

After brand guidelines complete:
- Use guidelines in `/prod-interaction-design` for UI patterns
- Reference voice/tone in `/prod-user-stories` for microcopy
- Apply visual direction throughout product

## Success Criteria

Brand guidelines are complete when:
- ✅ Core values are specific (not generic)
- ✅ Personality traits have concrete examples
- ✅ Voice and tone examples feel authentic
- ✅ Visual direction aligns with personality
- ✅ Real application examples are provided
- ✅ Guidelines differentiate from competitors
- ✅ Team can use guidelines immediately

## Notes

- This is a living document - update as brand evolves
- All design decisions should reference these guidelines
- When in doubt, favor clarity over cleverness
- Be honest about who you are TODAY, not aspirational future
