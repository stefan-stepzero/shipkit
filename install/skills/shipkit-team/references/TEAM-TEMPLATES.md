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

## Template 5: Full Pipeline

**When:** You want the full lifecycle — discovery → definition → spec → architecture → plan → implement → verify — in one team session.

**Command:** `/shipkit-team --template pipeline "Build a [product description]"`

See the **Pipeline Template** section in the main skill file for full phase details, artifact DAG, gate logic, and optional skills per phase.

**Summary:**
```
Phase 1: Discovery        — why → discovery (+ project-context parallel)
Phase 2: Solution Design   — definition → goals
Phase 3: Specification     — batch specs from product-definition
Phase 4: Architecture      — solution architect proposes from all context
Phase 5: Planning          — one plan per spec, dependency-ordered
Phase 6: Implementation    — parallel team build + verify + preflight
```

**Model selection:** Sonnet for PO/Architect/Implementers, Opus for Spec (Phase 3) and Reviewer (Phase 6).

**Risk:** Vision quality depends on the product goal passed in `$ARGUMENTS`. Be specific — "Build a spaced repetition learning app for medical students" is better than "Build a learning app".

---

## Template 6: Worktree Parallel Implementation

**When:** You have independent clusters with no file overlap and want each to produce its own PR for incremental merge.

**Command:** `/shipkit-team recipe-sharing --worktree`

```
For each cluster, spawn a worktree-isolated agent:

Agent tool parameters:
  subagent_type: "general-purpose"
  isolation: "worktree"
  run_in_background: true
  prompt: {self-contained worker prompt with inlined context}

Reviewer agent (no worktree):
  subagent_type: "general-purpose"
  run_in_background: true
  prompt: {reviewer instructions — validates PRs via gh pr diff}

Lead (you):
  - Renders progress table
  - Sends PR URLs to reviewer as agents complete
  - Merges approved PRs
  - Runs /shipkit-verify on merged state
  - Verifies phase gates before spawning next phase
```

**Branch naming:** `impl/{cluster-slug}` (e.g., `impl/recipe-api`, `impl/recipe-ui`)

**PR flow per cluster:**
1. Agent implements tasks in isolated worktree
2. Agent runs build/test/lint relentlessly
3. Agent commits, pushes, opens PR against source branch
4. Reviewer validates PR against spec acceptance criteria
5. Lead merges approved PRs

**Model selection:** Sonnet for all (worktree agents have narrow focused scope).

**When NOT to use:**
- Clusters share types/interfaces across boundaries
- Work requires real-time coordination between agents
- Only 1-2 clusters (shared mode is simpler)
