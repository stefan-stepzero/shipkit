# ProdKit - Product Discovery & Strategy Skills

This folder contains the ProdKit framework: 11 Claude Code skills for comprehensive product discovery, strategy, and requirements definition.

## Purpose

ProdKit skills guide you from initial business strategy to detailed product requirements, ensuring you build the right product for the right users before writing any code.

## Structure

### Sequential Workflow (9 skills)
Execute these in order for complete product discovery:

1. **strategic-thinking** - Define business strategy and value proposition (Playing to Win + Lean Canvas)
2. **personas** - Identify target user personas with demographics, goals, and pain points
3. **jobs-to-be-done** - Map current state workflows and understand what job users hire your product to do
4. **market-analysis** - Analyze competitive landscape using Porter's Five Forces
5. **brand-guidelines** - Define visual direction, personality, and brand identity
6. **interaction-design** - Design future state user journeys and workflows
7. **user-stories** - Write actionable requirements with MoSCoW prioritization
8. **assumptions-and-risks** - Identify strategic risks and validate assumptions
9. **success-metrics** - Define KPIs and instrumentation for measuring success

### Async Skills (2 skills)
Call these anytime during the workflow:

- **trade-off-analysis** - Prioritize features by ROI and effort (BUILD/DEFER/CUT)
- **communicator** - Generate stakeholder communications (HTML one-pagers, decks, reports)

## Workflow Integration

**ProdKit → devkit → Development**

1. **Product Discovery (ProdKit)** - Define *what* to build and *why*
   - Output: Complete product context in `.prodkit/`

2. **Technical Specification (devkit)** - Define *how* to build it
   - Output: Technical specs in `.devkit/specs/`

3. **Development (devkit)** - Build it with quality
   - Output: Shipped feature

## Creating New Skills

Use the `_template.md` as a starting point for creating additional ProdKit skills tailored to your workflow.

## Output Location

All ProdKit artifacts are generated in `.prodkit/` workspace:
- `.prodkit/strategy/` - Business canvas, value proposition
- `.prodkit/discovery/` - Personas, JTBD, market analysis
- `.prodkit/brand/` - Brand guidelines, visual direction
- `.prodkit/design/` - Interaction design, user journeys
- `.prodkit/requirements/` - User stories, acceptance criteria
- `.prodkit/metrics/` - Success metrics, KPIs
- `.prodkit/analysis/` - Trade-off analysis, risk assessments
- `.prodkit/comms/` - Stakeholder communications (HTML)
