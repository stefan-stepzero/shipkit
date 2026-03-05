---
name: shipkit-smoketest
description: Manages and reads results from the shipkit-testing harness. Sets up test agents/skills, reads results, and analyzes findings.
user-invocable: true
---

# Shipkit Smoke Test

Manages the test harness at `P:/Projects2/shipkit-testing/` to validate Claude Code agent/skill behavior. All test logic and hypotheses live here — the test repo stays dumb.

## Test Harness Location

`P:/Projects2/shipkit-testing/`

## Current Tests

### T1: Agent Frontmatter Loading

**Hypothesis:** Agent frontmatter (`tools`, `disallowedTools`, `model`, `skills`, `permissionMode`, `memory`) is ONLY applied when a skill references the agent via the `agent:` field in its YAML frontmatter. When an agent is spawned via `Agent(subagent_type: "general-purpose")` with the persona pasted into the prompt, the frontmatter configuration is ignored.

**Test design:** Agent `test-agent` declares `disallowedTools: Bash`. Skill `/test-frontmatter` loads it via `agent:` + `context: fork`. 10 frontmatter checks (A1-A10) + skill chaining (B, C) + agent spawning (D).

### T2: Pipeline Delegation

**Hypothesis:** The 3-loop orchestration pipeline works end-to-end via gateway skills with `context: fork` + `agent:`.

**Test design:** 4 agents, each with unique secret (passphrase + computation) in `references/secret.md`. 8 validation checks (4 passphrases + 4 computations).

| Agent | Gateway Skill | Secret Computation | Expected | Output |
|-------|--------------|-------------------|----------|--------|
| Visionary | `/test-vision` | fibonacci(12) | 144 | `.shipkit/why.json` |
| PO | `/test-product` | first 8 primes | [2,3,5,7,11,13,17,19] | `.shipkit/product-definition.json` |
| Architect | `/test-engineering` | gcd(252, 105) | 21 | `.shipkit/engineering-definition.json` |
| PM | `/test-verify` | caesar("PIPELINE", 3) | "SLSHOLQH" | `.shipkit/verification-report.json` |

### T3: Custom Agent Types

**Hypothesis:** The Agent tool may accept custom `subagent_type` values matching `.claude/agents/` definitions (e.g., `subagent_type: "test-visionary-agent"`). If it only accepts built-in types, the test falls back to `"general-purpose"`.

**Test design:** Inline skill invokes Agent tool with custom type, then probes what the subagent can do (Bash, CLAUDE.md, Skill tool). Includes a marker skill (`test-t3-marker`) to verify skill invocation.

### T4: Tools Field Semantics

**Hypothesis:** The `tools:` field in agent frontmatter could be either a whitelist (only listed tools available) or a preload hint (all tools still available, listed ones just preloaded). The A5 surprise from T1 (Edit worked despite not being in `tools:` list) suggests preload hint.

**Test design:** 3 agents with different configs test the same 4 tools (Bash, Edit, Grep, Glob):

| Agent | `tools:` | `disallowedTools:` |
|-------|---------|-------------------|
| A | `Read, Write` | _(none)_ |
| B | _(omitted)_ | `Edit, Bash` |
| C | `Read, Write, Grep` | `Bash` |

If whitelist: A gets 0,0,0,0. If preload hint: A gets 1,1,1,1.

### T5: Fork Isolation

**Hypothesis:** `context: fork` creates an isolated environment, but filesystem access may leak through (the A9 surprise suggested partial isolation).

**Test design:** Runner writes a canary file before forking. Forked agent checks:
1. Can it see the pre-fork canary file?
2. Do its own writes persist after fork completes?
3. Can it see CLAUDE.md?
4. Can it see parent message history?

### T6: Subagent Skill Invocation

**Hypothesis:** A subagent spawned via Agent tool CAN invoke project skills using the Skill tool.

**Test design:** Inline skill spawns `Agent(general-purpose)` with prompt to invoke `/test-vision`. Checks if `.shipkit/why.json` is created with correct passphrase.

### T7: Team Skills (Experimental)

**Hypothesis:** A team lead with `Task` tool can create teammates who invoke skills.

**Test design:** Team lead agent creates a teammate, teammate tries to invoke `/test-vision`. Requires `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`.

### T8: Typed Teams (Experimental)

**Hypothesis:** Typed teammates created with `Task(agent_type)` get the specified agent's frontmatter applied.

**Test design:** Team lead creates `Task(test-visionary)` teammate, checks if model/identity/secret access matches `test-visionary-agent` frontmatter.

## Modes

### `read` (default) — Read test results

Read `P:/Projects2/shipkit-testing/results/FULL-REPORT.txt` (or `REPORT.txt` for T1 only). Analyze findings.

### `setup` — Set up or reset test harness

Write/overwrite all test agents and skills in the test repo.

### `clean` — Clear results

Delete all result files from `P:/Projects2/shipkit-testing/results/`.

### `pipeline` — Pipeline delegation test

Subcommands:
- `pipeline read` — Run validation script and report results
- `pipeline clean` — Remove pipeline artifacts for re-run

### `add` — Add a new test

When given a new hypothesis to test, create the necessary agent/skill files in the test repo and update this skill's documentation.

## Usage

```
/shipkit-smoketest              → read results (full report)
/shipkit-smoketest read         → read results (full report)
/shipkit-smoketest setup        → write/reset test harness files
/shipkit-smoketest clean        → clear all results
/shipkit-smoketest pipeline     → pipeline validation
/shipkit-smoketest pipeline read  → pipeline validation
/shipkit-smoketest pipeline clean → clean pipeline artifacts
/shipkit-smoketest add          → add a new test (describe the hypothesis)
```
