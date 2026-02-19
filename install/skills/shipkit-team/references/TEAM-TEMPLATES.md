# Team Templates

Pre-built team compositions for common scenarios. Reference these when creating teams.

---

## Template 1: Feature Implementation (from plan)

**When:** You have a plan.json and want to build it.

```
Create an agent team to implement: {plan.overview.goal}

Read context files:
- .shipkit/plans/todo/{feature}.json (plan with tasks)
- .shipkit/specs/todo/{feature}.json (acceptance criteria)
- .shipkit/stack.json (project patterns)
- .shipkit/architecture.json (design decisions)

Teammates:
- N implementers (Sonnet): one per file ownership cluster
- 1 reviewer (Opus): validates completed tasks against spec

Rules:
- Each implementer owns distinct file paths — no overlap
- Implementers use /shipkit-build-relentlessly + /shipkit-test-relentlessly
- Reviewer reads completed work, validates against spec, messages implementers directly
- Lead verifies phase gates, runs /shipkit-verify + /shipkit-preflight when done
- Lead does NOT implement — coordinate only
```

**Model selection:** Sonnet for implementers (cost-effective), Opus for reviewer (reasoning depth).

---

## Template 2: Code Review

**When:** You want thorough multi-perspective review of a PR or changeset.

```
Create an agent team to review {target}:

Teammates:
- Security reviewer (Opus): Token handling, input validation, OWASP Top 10, secrets exposure
- Performance reviewer (Sonnet): Query patterns, caching, bundle size, render cycles
- Correctness reviewer (Sonnet): Edge cases, error paths, test coverage, spec compliance

Rules:
- All teammates are READ-ONLY — no file edits
- Each reviewer produces a findings report with severity ratings
- Reviewers challenge each other's findings via direct messaging
- Lead synthesizes into unified review with: Critical / Warning / Suggestion categories
```

**Model selection:** Opus for security (highest stakes), Sonnet for others.

---

## Template 3: Debug Investigation

**When:** Root cause is unclear, multiple theories possible.

```
Create an agent team to investigate: {problem description}

Context: {symptoms, error logs, affected code paths}

Teammates:
- Investigator 1 (Sonnet): Hypothesis — {theory A}
- Investigator 2 (Sonnet): Hypothesis — {theory B}
- Investigator 3 (Sonnet): Hypothesis — {theory C}

Rules:
- Each investigator explores their theory independently
- Investigators MUST try to disprove each other's theories via messaging
- Share evidence (file paths, log lines, reproduction steps)
- Lead synthesizes: which theory has the strongest evidence?
- After consensus, lead creates fix plan
```

**Model selection:** Sonnet for all (investigation is breadth, not depth).

---

## Template 4: Research Sprint

**When:** Evaluating options, comparing technologies, or exploring solutions.

```
Create an agent team to research: {topic}

Teammates:
- Researcher 1 (Sonnet): Evaluate {option A} — features, performance, migration, community
- Researcher 2 (Sonnet): Evaluate {option B} — features, performance, migration, community
- Researcher 3 (Sonnet): Evaluate {option C} — features, performance, migration, community

Rules:
- All researchers use IDENTICAL evaluation criteria
- Each produces a structured report with the same sections
- Lead synthesizes into comparison matrix
- Researchers can message each other to cross-check claims
```

**Model selection:** Sonnet for all. Use Haiku if evaluation is shallow.

---

## Template 5: Full Pipeline (Autonomous)

**When:** You want spec → plan → implement → review in one team session. Phase 2 vision.

```
Create an agent team to build: {feature description}

Read context: .shipkit/stack.json, .shipkit/architecture.json

Phase 1 — Specification:
- Spawn PO teammate (Opus): Run /shipkit-spec, produce spec.json
- Require plan approval from lead before proceeding

Phase 2 — Planning:
- Spawn Architect teammate (Opus): Run /shipkit-plan from spec, produce plan.json
- Require plan approval from lead before proceeding

Phase 3 — Implementation:
- After plan approved, spawn N implementers (Sonnet) from plan task clusters
- Spawn reviewer (Opus) to validate alongside

Phase 4 — Quality:
- Lead runs /shipkit-verify + /shipkit-preflight
- Report results

Rules:
- PO reads .shipkit/why.json and .shipkit/goals.json for project context
- Architect reads spec.json and follows codebase patterns
- Implementers follow plan.json tasks with file ownership boundaries
- Reviewer validates against spec acceptance criteria
- Lead approves each phase gate before next phase starts
```

**Model selection:** Opus for PO/Architect/Reviewer (reasoning-heavy), Sonnet for implementers.

**Risk:** Spec and plan quality depend on how well `.shipkit/` context captures user intent. Best with well-populated context files.
