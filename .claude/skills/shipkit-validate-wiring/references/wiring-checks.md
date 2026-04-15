# Wiring Check Catalog

Reference checklist for `/shipkit-validate-wiring --static` mode. Each check runs against DOC-025 JSON data.

## Suppression via knownIssues

Before reporting a finding, check if it matches a `knownIssues` entry in DOC-025:
- If `severity: "by-design"` → suppress entirely (do not report)
- If `severity: "info"` → downgrade to NOTE
- If `severity: "resolved"` → skip (issue was fixed)
- Match by comparing `affectedSkills`, `affectedArtifacts`, or `id` fields

This prevents known, intentional design choices from being flagged on every run.

---

## BLOCK Severity (must fix before release)

### W-001: Agent Binding Exists
**Check**: For every skill with an `agent:` field in frontmatter, the referenced agent file must exist in DOC-025's agents map.
**Data source**: `skills[*].frontmatter.agent` → `agents[agentName]`
**Failure**: Skill references an agent that doesn't exist — dispatch will fail at runtime.

### W-002: Skill Binding Exists
**Check**: For every agent with a `skills:` list in frontmatter, each referenced skill must exist in DOC-025's skills map.
**Data source**: `agents[*].frontmatter.skills` → `skills[skillName]`
**Failure**: Agent references a skill that doesn't exist.

### W-003: Dispatch Target Exists
**Check**: For every `/shipkit-*` dispatch reference found in skill/agent body text, the target skill directory must exist in DOC-025's skills map.
**Data source**: `skills[*].dispatches` + `agents[*].dispatches` → `skills[targetName]`
**Failure**: Body text dispatches to a skill that doesn't exist — Skill tool call will fail.

### W-004: Artifact Writer Exists
**Check**: For every artifact path that appears in any skill's `reads` list, there must be at least one skill that has it in its `writes` list.
**Data source**: `skills[*].reads` → exists in some `skills[*].writes`
**Failure**: A skill reads an artifact that no skill produces — will hit missing file at runtime.
**Exception**: Artifacts from user input or external sources (README, codebase, user input) are exempt.

### W-005: Tool Conflict
**Check**: For every skill with `allowed-tools` in frontmatter, cross-reference against its bound agent's `disallowedTools`. The intersection must be empty.
**Data source**: `toolRestrictions[*].conflicts`
**Failure**: Skill allows a tool that its agent disallows — ambiguous restriction that may cause unexpected behavior.

### W-006: Missing context: fork on Agent-Bound Skill
**Check**: Every skill with an `agent:` field must also have `context: fork` in frontmatter.
**Data source**: `skills[*].frontmatter.agent` exists AND `skills[*].frontmatter.context` == "fork"
**Failure**: Skill binds to an agent but doesn't fork — the agent persona won't be loaded.

### W-007: Orchestrator Must Have Skill Tool
**Check**: Every agent whose name contains `orch-` must have `Skill` in its `tools` list.
**Data source**: `agents[*]` where name matches `*orch-*` → `frontmatter.tools` contains "Skill"
**Failure**: Orchestrator agent can't dispatch producer skills without the Skill tool.

### W-008: Orchestrator Roster Output Match (AR-001)
**Check**: For every orchestrator skill (`shipkit-orch-direction`, `shipkit-orch-planning`, `shipkit-orch-shipping`), parse its Roster table. For each row, the declared output artifact(s) must appear in the dispatched skill's `writes` set in DOC-025. Also check each reviewer skill's Required/Input artifact list against producer `writes` sets.
**Data source**: Orchestrator/reviewer SKILL.md body text (Roster tables + Required artifacts) parsed into `{skill: [artifacts]}` pairs → compared against `skills[skill].writes` in DOC-025.
**Failure**: Orch claims skill X produces artifact Y, but X doesn't write Y. The orch advances assuming Y exists; downstream skills hit missing file at runtime. Was the root cause of the vision.json contract drift that led to AR-001.
**Parser hint**: Roster rows typically follow `| /shipkit-{name} | {artifact} |` markdown. Split on `|` and trim. Handle multiple-artifact cells (e.g. "why.json + goals/strategic.json").
**Rationale**: Formalizes architectural rule AR-001 from DOC-015 — producer outputs must match what the orchestrator contracts for.

### W-009: Fork-Skill Prompts in Orchestrated Runs (AR-002)
**Check**: For every skill with `context: fork` AND `reachability == "orchestrated"` in DOC-025 (i.e. appears in some loop orchestrator's dispatch chain), scan the SKILL.md body for interactive-prompt patterns:
  - `Accept these\?`
  - `Ask user` (case-insensitive)
  - `View\s*/\s*Update\s*/\s*Replace\s*/\s*Cancel`
  - `Use this or regenerate`
  - `What should change`
  - `Confirm this .* blueprint`
  - `Ask user to confirm`
  - `Scan now\? \(yes/no\)`
  - `Rescan\? \(yes/no\)`
  - `Any folders I should skip`
  - `\?\n\s*-\s` (interrogative followed by a bulleted option list inside a prompt template)
**Data source**: Filesystem scan of `install/skills/*/SKILL.md` filtered by `frontmatter.context == "fork"` AND `skills[*].reachability == "orchestrated"` in DOC-025.
**Failure**: A forked skill that prompts inside an orchestrated run either hangs waiting or hallucinates an answer. The check covers both **producer** forks (fork + worker agent) AND **utility** forks (fork with no agent: field, e.g. project-context, codebase-index) when they're in an orchestrator's roster. Root cause of every hang fixed in the 2026-04-13 cleanup.
**Exception**: Skills with `reachability == "standalone"` (user-invocable, not orchestrator-dispatched) are allowed to prompt — e.g. `shipkit-communications`. Skills without `context: fork` at all (`shipkit-thinking-partner`, `shipkit-feedback-bug`, `shipkit-master`) run in caller context on purpose and can prompt. The check gates on reachability, not on agent type.
**Rationale**: Formalizes architectural rule AR-002 from DOC-015 — fork skills dispatched by an orchestrator must not prompt the user.

---

## WARN Severity (should fix)

### W-101: Model Mismatch
**Check**: If a skill specifies `model:` in frontmatter and its bound agent also specifies `model:`, they should match.
**Data source**: `skills[*].frontmatter.model` vs `agents[skills[*].frontmatter.agent].frontmatter.model`
**Note**: Skill-level model overrides agent-level, so this is informational — but mismatches may indicate an oversight.

### W-102: Turn Budget Sanity
**Check**: For orchestrator agents, their `maxTurns` should be >= (number of skills they dispatch) * 10.
**Data source**: `agents[orchAgent].frontmatter.maxTurns` vs count of `agents[orchAgent].dispatches` * 10
**Rationale**: Each dispatch costs ~10 turns overhead (skill invocation + artifact check + routing decision). An orchestrator with too few turns will exhaust budget before completing its loop.

### W-103: Orphaned Artifact
**Check**: Artifact appears in some skill's `writes` but never appears in any skill's `reads`.
**Data source**: `artifactFlow[*].writers` non-empty AND `artifactFlow[*].readers` empty
**Note**: May be intentional (e.g., final output artifacts) but worth flagging.

### W-104: Unreachable Skill
**Check**: Skill has `reachability: standalone` or no reachability classification, AND is not user-invocable, AND is not infrastructure.
**Data source**: `skills[*].reachability` + `skills[*].frontmatter.user-invocable`
**Failure**: Skill can't be reached by any dispatch chain and isn't user-invocable — effectively dead code.

### W-105: Agent Never Bound
**Check**: Agent exists in DOC-025's agents map but no skill references it via `agent:` field.
**Data source**: `agents[*].boundBySkills` is empty
**Failure**: Agent file exists but no skill loads it — agent persona is unused.

### W-106: Dispatch Without Fork
**Check**: An orchestrator skill dispatches another skill (via `/shipkit-*` in body), but the target skill doesn't have `context: fork`.
**Data source**: Orchestrator's `dispatches` → target skill's `frontmatter.context`
**Note**: Non-forked skills run inline in the orchestrator's context, which may be intentional for utility skills but unexpected for gateway skills.

### W-107: maxTurns Missing on Forked Skill/Agent
**Check**: A skill with `context: fork` + `agent:` should have `maxTurns` set (either on the skill or the agent).
**Data source**: `skills[*].frontmatter` where context=fork → agent's `frontmatter.maxTurns`
**Failure**: Forked agent without maxTurns has no budget limit — could run indefinitely.

### W-108: Artifact Consumption Completeness
**Check**: For each artifact in `artifactFlow` that has `expectedReaders` (derived from consumption rules), every expected reader must appear in `readers`.
**Data source**: `artifactFlow[*].expectedReaders` vs `artifactFlow[*].readers`
**Failure**: A skill that should logically consume an artifact doesn't list it in its reads — the skill operates with incomplete context. This means the skill's SKILL.md needs a reads reference added.
**Rules source**: Consumption rules are defined in the wiring-graph skill's `references/consumption-rules.md`. They derive expected readers from skill classification (reviewer, producer, goals, QA) and artifact type.
**Report format**: Group by skill, not by artifact — e.g., "shipkit-review-shipping missing reads: product-definition.json, engineering-definition.json, goals/product.json"

---

## NOTE Severity (informational)

### W-201: Shared Agent
**Check**: Agent is bound by more than one skill.
**Data source**: `agents[*].boundBySkills` has length > 1
**Note**: Expected for worker agents (e.g., visionary-agent bound by why-project, vision, stage, product-goals, engineering-goals). Flag for awareness, not action.

### W-202: Deep Dispatch Chain
**Check**: Dispatch chain from master to leaf exceeds depth 3.
**Data source**: `dispatchChains` tree depth
**Note**: DOC-023 confirmed 3-level nesting works (master → loop → worker). Depth > 3 is untested territory.
