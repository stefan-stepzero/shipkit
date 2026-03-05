---
name: shipkit-wiring-graph
description: Generates DOC-025 wiring graph — machine-readable dispatch chains, artifact flow, and tool restrictions for all installed skills and agents. Dispatches 3 parallel agents for frontmatter extraction and body analysis.
argument-hint: "[--refresh] [--json-only]"
---

# shipkit-wiring-graph - Wiring Graph Generator

**Purpose**: Generate a comprehensive wiring graph (DOC-025) that maps all dispatch chains, artifact flows, and tool restrictions across installed Shipkit skills and agents.

**What it does**: Dispatches 3 parallel Sonnet agents to extract frontmatter and body references from all installed skills and agents, then aggregates into a machine-readable wiring graph.

---

## When to Invoke

**User says:**
- "Generate wiring graph"
- "Update DOC-025"
- "Map dispatch chains"
- "What dispatches what?"

**Use when:**
- After adding/removing skills or agents
- Before running `/shipkit-validate-wiring`
- During architecture review or pre-release validation

---

## Prerequisites

**Required**:
- Running from Shipkit framework repo root
- `install/skills/` directory exists
- `install/agents/` directory exists
- `install/profiles/shipkit.manifest.json` exists

---

## Process

### Step 0: Pre-checks (Inline)

1. Verify `install/skills/`, `install/agents/`, and `install/profiles/shipkit.manifest.json` exist
2. Read manifest to get canonical skill and agent rosters with counts
3. If `--refresh` flag is NOT present and DOC-025 JSON exists and is newer than all files in `install/`, report "DOC-025 is up to date" and stop (unless `--refresh` forces regeneration)

### Step 1: Dispatch 3 Parallel Agents

Launch ALL 3 agents simultaneously using the Agent tool. Each agent is `subagent_type: "general-purpose"` with `model: "sonnet"`. Each returns structured text output.

**IMPORTANT**: Launch all 3 in a single message with 3 parallel Agent tool calls.

---

#### Agent 1: Skill Frontmatter Extraction

**Prompt:**
```
Extract frontmatter from ALL skill SKILL.md files in install/skills/shipkit-*/ at P:\Projects2\sg-shipkit.

For EACH skill directory:
1. Read SKILL.md
2. Parse YAML frontmatter (between --- delimiters)
3. Extract these fields (use null if missing):
   - name
   - description
   - context (e.g., "fork")
   - agent (e.g., "shipkit-visionary-agent")
   - model
   - allowed-tools (list)
   - user-invocable (boolean)
   - disable-model-invocation (boolean)
   - hooks (any hook config)
   - skills (list of sub-skills)
   - argument-hint

Report as structured text — one block per skill:
SKILL: {directory-name}
  name: {value}
  context: {value}
  agent: {value}
  model: {value}
  allowed-tools: {comma-separated list or null}
  user-invocable: {value}
  disable-model-invocation: {value}
  skills: {comma-separated list or null}
---
```

---

#### Agent 2: Agent Frontmatter Extraction

**Prompt:**
```
Extract frontmatter from ALL agent .md files in install/agents/shipkit-*.md at P:\Projects2\sg-shipkit.

For EACH agent file:
1. Read the .md file
2. Parse YAML frontmatter (between --- delimiters)
3. Extract these fields (use null if missing):
   - name
   - model
   - tools (list)
   - disallowedTools (list)
   - maxTurns
   - permissionMode
   - memory
   - skills (list)

Report as structured text — one block per agent:
AGENT: {filename without .md}
  name: {value}
  model: {value}
  tools: {comma-separated list or null}
  disallowedTools: {comma-separated list or null}
  maxTurns: {value}
  permissionMode: {value}
  skills: {comma-separated list or null}
---
```

---

#### Agent 3: Body Text Analysis (Dispatch Targets + Artifact References)

**Prompt:**
```
Analyze the body text (below frontmatter) of ALL skill SKILL.md files and ALL agent .md files in install/skills/shipkit-*/ and install/agents/shipkit-*.md at P:\Projects2\sg-shipkit.

For EACH file, extract:

1. DISPATCH TARGETS: Find all /shipkit-* patterns (skill dispatch references)
   - Pattern: /shipkit-{name} or Skill("shipkit-{name}")
   - Report the source file and each dispatch target found

2. ARTIFACT REFERENCES: Find all .shipkit/*.json patterns (artifact file references)
   - Pattern: .shipkit/{path}.json or .shipkit/{path}/
   - Classify each as READ (appears in "reads", "consumes", "checks", "input") or WRITE (appears in "produces", "writes", "creates", "output")
   - If classification is ambiguous, report as READ

3. REFERENCES DIRECTORY: Check if {skill_dir}/references/ exists and list files in it

Report as structured text — one block per file:
FILE: {path}
  dispatches: {comma-separated /shipkit-* targets or "none"}
  reads: {comma-separated .shipkit/ paths or "none"}
  writes: {comma-separated .shipkit/ paths or "none"}
  references_dir: {comma-separated filenames or "none"}
---
```

---

### Step 2: Aggregate Results

After all 3 agents return, build the wiring graph:

1. **Skills map**: Merge Agent 1 frontmatter + Agent 3 body analysis per skill
2. **Agents map**: Merge Agent 2 frontmatter + Agent 3 body analysis per agent
3. **Dispatch chains**: Build tree from master through loops to leaf workers using:
   - Skill `agent:` field → which agent backs this skill
   - Body `/shipkit-*` references → which skills each orchestrator dispatches
4. **Artifact flow**: For each `.shipkit/*.json` artifact, list writers and readers
5. **Tool restriction map**: For each skill with `allowed-tools`, cross-reference with its bound agent's `disallowedTools`
6. **Reachability**: Classify each skill:
   - `orchestrated` — reachable from master via dispatch chain
   - `standalone` — user-invocable but not in any dispatch chain
   - `infrastructure` — system skills (update, get-skills, get-mcps)
   - `sub-dispatched` — dispatched by a non-orchestrator (e.g., QA skills dispatched by reviewer-shipping)

### Step 3: Write DOC-025

**JSON sidecar** (`docs/development/system-design/DOC-025-wiring-graph.json`):
```json
{
  "$schema": "shipkit-dev-artifact",
  "type": "wiring-graph",
  "id": "DOC-025",
  "title": "Wiring Graph",
  "generatedAt": "{timestamp}",
  "generatedBy": "shipkit-wiring-graph",
  "skills": {
    "{skill-name}": {
      "frontmatter": { "context", "agent", "model", "allowed-tools", ... },
      "dispatches": ["/shipkit-*", ...],
      "reads": [".shipkit/*.json", ...],
      "writes": [".shipkit/*.json", ...],
      "reachability": "orchestrated|standalone|infrastructure|sub-dispatched",
      "referencesDir": ["file1.md", ...]
    }
  },
  "agents": {
    "{agent-name}": {
      "frontmatter": { "model", "tools", "disallowedTools", "maxTurns", ... },
      "boundBySkills": ["skill-name", ...],
      "dispatches": ["/shipkit-*", ...],
      "reads": [".shipkit/*.json", ...],
      "writes": [".shipkit/*.json", ...]
    }
  },
  "dispatchChains": {
    "master": {
      "dispatches": ["shipkit-orch-direction", ...],
      "children": {
        "shipkit-orch-direction": {
          "dispatches": ["shipkit-why-project", ...],
          "children": { ... }
        }
      }
    }
  },
  "artifactFlow": {
    ".shipkit/why.json": {
      "writers": ["shipkit-why-project"],
      "readers": ["shipkit-vision", "shipkit-product-discovery", ...]
    }
  },
  "toolRestrictions": {
    "{skill-name}": {
      "skillAllowedTools": [...],
      "agentDisallowedTools": [...],
      "conflicts": [...]
    }
  }
}
```

**Markdown** (`docs/development/system-design/DOC-025-wiring-graph.md`) — unless `--json-only`:
- Human-readable summary with dispatch chain tree, artifact flow table, tool restriction notes
- Generated from the JSON sidecar data

### Step 4: Report Summary

Display:
- Total skills extracted / total agents extracted
- Dispatch chain depth (max nesting level)
- Orphaned artifacts (written but never read)
- Missing inputs (read but never written)
- Tool conflicts found
- Unreachable skills (no path from any entry point)

---

## Output Files

| File | Purpose |
|------|---------|
| `docs/development/system-design/DOC-025-wiring-graph.json` | Machine-readable wiring graph |
| `docs/development/system-design/DOC-025-wiring-graph.md` | Human-readable summary |

---

## When This Skill Integrates with Others

### Before This Skill
- After adding/removing/modifying skills or agents
- Before running `/shipkit-validate-wiring`

### After This Skill
- Run `/shipkit-validate-wiring --static` to check for wiring issues
- Run `/shipkit-validate-wiring --walkthrough` to simulate dispatch flows

### Related Skills
- `shipkit-validate-wiring` — Validates the wiring graph for contract violations
- `shipkit-framework-integrity` — Validates structural integrity (manifest, references, hooks)
