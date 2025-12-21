---
description: "Use anytime to transform ProdKit working docs into polished HTML stakeholder communications"
---

# Communicator

## Agent Persona

**Load:** `.claude/agents/discovery-agent.md`

Adopt: Audience-aware, storytelling focus, distills complexity into clarity.

## Purpose
Transform ProdKit working docs (markdown) into polished, visually rich HTML stakeholder communications.

**Can run ANYTIME** after artifacts exist.

## When to Trigger
User says:
- "Create an investor deck"
- "Make a one-pager for executives"
- "I need to present this to the team"
- "Turn this into a customer brief"
- "Generate a product summary"
- "Create stakeholder documentation"

## Inputs
- One or more ProdKit artifacts from `.prodkit/`
- Target audience
- Optional: Format preference

## Audiences

**investors**: Pitch deck style
- Focus: Opportunity, traction, ask
- Tone: Confident, data-driven
- Includes: Market size, competitive advantage, business model

**team**: Internal alignment
- Focus: Context for developers, design rationale
- Tone: Collaborative, detailed
- Includes: Technical constraints, user needs, success metrics

**execs**: Executive summary
- Focus: Recommendation with risks, ROI
- Tone: Strategic, concise
- Includes: Business case, risks, next steps

**customers**: Product brief
- Focus: Value proposition, benefits
- Tone: User-focused, compelling
- Includes: Problems solved, how it works, pricing

**developers**: Technical context
- Focus: Product requirements, design constraints
- Tone: Specific, actionable
- Includes: User stories, journeys, brand guidelines

## Formats (all HTML)

**onepager**: Single-page document
- Print-ready
- Self-contained
- Visual hierarchy
- Perfect for handouts

**memo**: Multi-section narrative
- Detailed exploration
- Sections with deep-dive
- Good for async reading

**summary**: Executive summary format
- TL;DR at top
- Key points highlighted
- Supporting details below

## Process

### 1. Identify Artifacts to Include

Ask user or infer from request:

Common combinations:
- **Investor pitch**: strategy, market, personas, metrics
- **Team onboarding**: all artifacts
- **Customer brief**: personas, JTBD, value prop, journeys
- **Executive summary**: strategy, risks, metrics, trade-offs

### 2. Select Appropriate Template

Match audience + format:
- `investors-onepager.template.html`
- `team-memo.template.html`
- `execs-summary.template.html`
- `customers-brief.template.html`
- `developers-context.template.html`

### 3. Read Source Artifacts

Read the specified `.prodkit/` files to extract content.

**IMPORTANT**: Actually read the files, don't make up content.

### 4. Transform Content for Audience

**For investors**:
- Emphasize market opportunity
- Highlight traction metrics
- Show competitive advantage
- Include the ask

**For team**:
- Full product context
- Design rationale
- Technical considerations
- Success metrics

**For execs**:
- Business case
- Risk assessment
- Recommendation
- Resource requirements

**For customers**:
- Problem they relate to
- How product solves it
- Value delivered
- Social proof (if available)

**For developers**:
- User needs driving features
- Interaction patterns
- Brand constraints
- Acceptance criteria

### 5. Call Script

```bash
.prodkit/scripts/bash/generate-communication.sh \
  --artifacts "strategy,personas,market,metrics" \
  --audience "investors" \
  --format "onepager"
```

Or for team memo:

```bash
.prodkit/scripts/bash/generate-communication.sh \
  --artifacts "all" \
  --audience "team" \
  --format "memo"
```

## Outputs

HTML file in `.prodkit/comms/`:
- Filename pattern: `[date]-[audience]-[format].html`
- Example: `2024-12-20-investors-onepager.html`

## Constraints
- **DO NOT** create HTML manually
- **ALWAYS** use `generate-communication.sh` script
- **HTML must be self-contained** (inline CSS, no external resources)
- **MUST be print-ready** (PDF via browser print)
- **ACTUALLY READ** source artifacts (don't invent data)

## HTML Requirements

Generated HTML must:
- Include all CSS inline (no external stylesheets)
- Be responsive (looks good on screen and print)
- Have print-specific styles (@media print)
- Use professional typography and spacing
- Include visual hierarchy (headings, sections, callouts)
- Have proper metadata (title, description)

## Use Cases

**Fundraising**:
- Investor onepager
- Pitch deck supplement
- Business plan summary

**Team Alignment**:
- Product kickoff memo
- Developer context doc
- Design handoff

**Stakeholder Updates**:
- Executive summary
- Board deck content
- Strategic review

**Customer Communication**:
- Product launch announcement
- Feature explainer
- Value proposition page

**Sales Enablement**:
- One-pager for sales team
- Customer pitch deck
- Demo script

## Tips for Effective Communications

**Know Your Audience**:
- Investors care about ROI
- Team needs context
- Execs want recommendations
- Customers want value

**Be Visual**:
- Use color to highlight
- Break up text with sections
- Include metrics in callout boxes
- Use whitespace generously

**Be Concise**:
- Lead with key insight
- Support with details
- Cut fluff ruthlessly

**Be Specific**:
- Use real numbers
- Name actual competitors
- Quote real users (if available)

## Context
This is an **ASYNC** skill - can be called anytime, not part of sequential workflow.
