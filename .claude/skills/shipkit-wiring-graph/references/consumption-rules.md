# Artifact Consumption Rules

Deterministic rules for deriving `expectedReaders` in DOC-025's `artifactFlow`. Each rule matches artifacts to skills that should logically consume them based on skill classification and purpose.

These rules are applied during Step 2.7 of wiring graph generation. The validator (W-108) then compares `expectedReaders` against actual `readers` to find gaps.

---

## Skill Classifications

Before applying rules, classify each skill:

| Classification | Skills | Purpose |
|---------------|--------|---------|
| **direction-producer** | why-project, vision, stage | Produce direction artifacts |
| **definition-producer** | product-discovery, product-definition, engineering-definition | Produce definition artifacts |
| **goals-producer** | product-goals, engineering-goals | Produce goal criteria |
| **planning-producer** | spec-roadmap, spec, plan, test-cases, user-instructions | Produce planning artifacts |
| **reviewer-direction** | review-direction | Assesses direction coherence |
| **reviewer-planning** | review-planning | Assesses planning completeness |
| **reviewer-shipping** | verify, preflight | Assesses implementation + release readiness |
| **qa-sub** | ux-audit, semantic-qa, qa-visual, prompt-audit, scale-ready | Specialized QA dispatched by reviewer-shipping |
| **orchestrator** | master, orch-direction, orch-planning, orch-shipping | Dispatch and monitor loops |
| **utility** | metrics, work-memory, user-instructions, claude-md, communications | Lightweight tools |
| **infrastructure** | update, get-skills, get-mcps | Framework management |
| **context-scanner** | project-context, codebase-index | Scan and index project |

---

## Consumption Rules

### Rule 1: Reviewers read all artifacts in their scope

**reviewer-direction** should read ALL direction + definition artifacts:
- `.shipkit/why.json`
- `.shipkit/vision.json` (if separate)
- `.shipkit/goals/strategic.json`
- `.shipkit/goals/product.json`
- `.shipkit/goals/engineering.json`
- `.shipkit/product-discovery.json`
- `.shipkit/product-definition.json`
- `.shipkit/engineering-definition.json`
- `.shipkit/metrics/latest.json`

**reviewer-planning** should read ALL planning artifacts + key direction artifacts:
- Everything it currently reads PLUS:
- `.shipkit/plans/*.json` (the plans it's supposed to review)
- `.shipkit/goals/strategic.json`

**reviewer-shipping** (verify, preflight) should read:
- verify: specs, plans, product-definition, engineering-definition, goals/product, goals/engineering, codebase-index, architecture
- preflight: verification-report, goals/product, goals/engineering, goals/strategic, metrics/latest, plus everything it currently reads

### Rule 2: Goals skills read their source definitions

**product-goals** should read:
- `.shipkit/product-definition.json` (features to derive criteria from)
- `.shipkit/product-discovery.json` (user needs context)
- `.shipkit/goals/strategic.json` (stage context)
- `.shipkit/why.json` (project constraints)
- `.shipkit/metrics/latest.json` (for --evaluate mode)

**engineering-goals** should read:
- `.shipkit/engineering-definition.json` (mechanisms to derive criteria from)
- `.shipkit/goals/strategic.json` (stage context)
- `.shipkit/goals/product.json` (cross-reference product criteria)
- `.shipkit/stack.json` (calibrate to actual technology)
- `.shipkit/metrics/latest.json` (for --evaluate mode)

### Rule 3: Spec/plan skills read goals and definitions

**spec** should read:
- `.shipkit/product-definition.json`, `.shipkit/engineering-definition.json`
- `.shipkit/goals/product.json`, `.shipkit/goals/engineering.json`
- `.shipkit/stack.json`, `.shipkit/codebase-index.json`
- `.shipkit/spec-roadmap.json`

**spec-roadmap** should read:
- `.shipkit/product-definition.json`, `.shipkit/engineering-definition.json`
- `.shipkit/goals/strategic.json`, `.shipkit/goals/*.json`
- `.shipkit/why.json`
- `.shipkit/codebase-index.json`

**plan** should read:
- `.shipkit/specs/`, `.shipkit/engineering-definition.json`
- `.shipkit/goals/engineering.json`
- `.shipkit/stack.json`, `.shipkit/codebase-index.json`

### Rule 4: Stage reads metrics and roadmap

**stage** should read:
- `.shipkit/goals/strategic.json`, `.shipkit/goals/product.json`, `.shipkit/goals/engineering.json`
- `.shipkit/metrics/latest.json` (measured progress)
- `.shipkit/spec-roadmap.json` (roadmap completion)

### Rule 5: Feedback loop — producers read reviewer output

Skills that a reviewer assesses should read that reviewer's assessment on re-dispatch:
- **spec**, **plan** should read `.shipkit/reviews/planning-assessment.json`
- Direction producers don't need this (reviewer-direction writes to direction-assessment.json which orch-direction reads for re-dispatch routing)

### Rule 6: QA sub-skills read relevant definitions

**ux-audit** should read:
- `.shipkit/product-discovery.json` (personas, pain points)
- `.shipkit/product-definition.json` (UX patterns, features)

**test-cases** should read:
- `.shipkit/product-discovery.json` (user scenarios)
- `.shipkit/engineering-definition.json` (component structure)

**scale-ready** should read:
- `.shipkit/engineering-definition.json` (mechanisms, components)

### Rule 7: Communications reads feature + QA context

**communications** should read:
- `.shipkit/product-definition.json` (feature descriptions)
- `.shipkit/specs/` (shipped feature details)
- `.shipkit/spec-roadmap.json` (shipped vs upcoming)
- `.shipkit/verification-report.json` (QA status)

### Rule 8: Orchestrators read their loop's key state artifacts

This is already well-covered. Orchestrators read the artifacts they need for dispatch routing. No additional rules needed.

---

## Applying Rules

For each artifact in `artifactFlow`:
1. Identify which rules apply based on the artifact path
2. Collect all skills that match the rule conditions
3. Set `expectedReaders` = union of rule-derived readers
4. Set `missingReaders` = `expectedReaders` minus actual `readers`
5. Exclude skills listed in `knownIssues` with `severity: "by-design"` from `missingReaders`

---

## Exempt Artifacts

These artifacts are exempt from consumption completeness checks:
- Archive artifacts (`.shipkit/archives/`, `.shipkit/communications/archive/`)
- Local state files (`.shipkit/team-state.local.json`, `.shipkit/orchestration.json`)
- Self-referencing artifacts (where the only expected reader is the writer itself)
- Infrastructure artifacts (`.claude/`, `CLAUDE.md`, `.mcp.json`)
