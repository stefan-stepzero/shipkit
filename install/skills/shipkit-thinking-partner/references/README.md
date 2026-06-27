# Thinking Partner References

Cognitive frameworks and discussion styles for structured thinking.

## Frameworks

| Framework | Best For | File |
|-----------|----------|------|
| Decision Matrix | Binary or multi-option choices with clear criteria | `frameworks/decision-matrix.md` |
| First Principles | Challenging assumptions, rethinking from scratch | `frameworks/first-principles.md` |
| Pre-Mortem | Risk assessment, failure prevention | `frameworks/pre-mortem.md` |
| Consequence Mapping | Understanding ripple effects of decisions | `frameworks/consequence-mapping.md` |
| Devil's Advocate | Stress-testing a preferred option | `frameworks/devils-advocate.md` |
| Option Evaluation Rubric | Comparing multiple options across weighted dimensions | `frameworks/option-evaluation-rubric.md` |

## Discussion Styles

See `discussion-styles.md` for the four conversation modes:
- **Socratic** — Question-led discovery
- **Direct** — Structured analysis with clear recommendations
- **Framework-Guided** — Step-by-step framework application
- **Adversarial** — Autonomous resource-advocate debate (see below)

## Adversarial Mode

The thinking-partner's autonomous debate mode. A panel of 3-5 resource advocates (from a pool of 8) argues a concrete decision over 3 rounds, then the orchestrator synthesizes a tension map + decision matrix.

- `adversarial-mode.md` — Debate orchestration: dispatch protocol, round structure, synthesis template, token budget.
- `resource-advocates.md` — The pool of 8 advocates (time, cost, scope, ux, tech-debt, risk, scale, simplicity) with stance, rhetorical style, and natural enemies.

Advocates are dispatched via the `shipkit-resource-advocate` infrastructure skill (`shipkit-resource-advocate-agent` persona). Not user-invoked.

## Framework Selection Guide

| Problem Pattern | Recommended Framework |
|----------------|----------------------|
| "Should we use A or B?" | Decision Matrix |
| "Why are we doing it this way?" | First Principles |
| "What could go wrong?" | Pre-Mortem |
| "What are the ripple effects?" | Consequence Mapping |
| "I'm leaning toward X..." | Devil's Advocate |
| "We have 3+ options to evaluate" | Option Evaluation Rubric |
| "I don't know where to start" | First Principles → then others |
