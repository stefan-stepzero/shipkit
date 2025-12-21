---
description: "Use when analyzing competitive landscape and market dynamics using Porter's Five Forces"
---

# Market Analysis

## Agent Personas

**Load:** `.claude/agents/discovery-agent.md` + `.claude/agents/researcher-agent.md`

Adopt: Discovery for strategic framing, Researcher for competitive intel gathering and verification.

## Purpose
Analyze market structure using Porter's Five Forces and competitive landscape. Broader than just competitors - understand the entire ecosystem.

## When to Trigger
User says:
- "What's the competitive landscape?"
- "Analyze the market"
- "Who else is solving this?"
- "How does the market work?"

Or uploads:
- Competitive research
- Market reports
- Competitor screenshots

## Prerequisites
- Strategy defined (where we're playing)
- Personas defined (who competitors target)
- JTBD defined (what solutions exist)

## Inputs
- Strategy (`.prodkit/strategy/business-canvas.md`)
- Personas (`.prodkit/discovery/personas.md`)
- JTBD (`.prodkit/discovery/jobs-to-be-done-current.md`)
- User-provided research (from `.prodkit/inputs/market/`)

## Process

### 1. Research Using Web Search

**IMPORTANT**: Use the `WebSearch` tool to gather information.

Search for:
- **Direct competitors**: Companies solving the same JTBD
- **Indirect competitors**: Alternative solutions to the same problem
- **Adjacent products**: Could expand into this space

For each competitor, document:
- Name and website URL
- Positioning statement
- Target users
- Key features
- Pricing model
- Strengths
- Weaknesses
- Market share (if publicly available)

### 2. Porter's Five Forces Analysis

Analyze each force:

**Competitive Rivalry**: How intense is competition?
- Number of competitors
- Market maturity
- Product differentiation
- High/Medium/Low intensity

**Threat of New Entrants**: Barriers to entry?
- Capital requirements
- Technology barriers
- Network effects
- Regulatory hurdles
- High/Medium/Low threat

**Bargaining Power of Buyers**: Can customers negotiate?
- Switching costs
- Price sensitivity
- Availability of alternatives
- High/Medium/Low power

**Bargaining Power of Suppliers**: Platform dependencies?
- Dependence on APIs (Slack, Google, etc.)
- Alternative data sources
- Supplier concentration
- High/Medium/Low power

**Threat of Substitutes**: What alternatives exist?
- Different approaches to same problem
- "Do nothing" option viability
- High/Medium/Low threat

### 3. Market Sizing (if possible)

- **TAM** (Total Addressable Market)
- **SAM** (Serviceable Addressable Market)
- **SOM** (Serviceable Obtainable Market)

### 4. Call Script

```bash
.prodkit/scripts/bash/analyze-market.sh \
  --rivalry "High - 10+ tools in async collaboration space (Slack, Loom, Notion)" \
  --new-entrants "Low barriers - many AI tools launching monthly" \
  --buyer-power "High - easy to switch, low lock-in, free alternatives available" \
  --supplier-power "Medium - dependent on Slack/email APIs, but alternatives exist" \
  --substitutes "High - can use existing tools + discipline, meetings, manual summaries" \
  --competitors "Notion,Asana,Slack,Loom,Linear,Twist" \
  --market-size "12B TAM in team productivity software (Gartner 2024)"
```

## Outputs
- `.prodkit/discovery/market-analysis.md`

## Constraints
- **DO NOT** create files manually
- **ALWAYS** use `analyze-market.sh` script
- **MUST** use WebSearch tool for competitive research
- **INCLUDE** URLs to competitor websites
- **CITE** sources for market size data

## Next Steps
After market analyzed:
- Define brand guidelines (how to differentiate visually/tonally)

## Context
This is **Step 4 of 9** in the ProdKit sequential workflow.
