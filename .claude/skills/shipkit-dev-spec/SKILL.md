---
name: shipkit-dev-spec
description: Specs framework changes for the Shipkit repo — new skills, agents, hooks, refactors, or architecture changes. Forces design decisions before implementation. Outputs structured spec to .claude/specs/. Use when planning any non-trivial framework change.
argument-hint: "<feature-name> [--from-opportunity OPP-xxx]"
---

# shipkit-dev-spec - Framework Change Specification

**Purpose**: Force explicit design decisions before implementing framework changes

**What it does**:
- Captures WHAT is being built/changed and WHY
- Validates against the Skill Value Test (from CLAUDE.md)
- Identifies all affected files using the 7-file integration model
- Produces a structured spec at `.claude/specs/{feature}.json`

---

## When to Invoke

**User says:**
- "Spec this framework change"
- "Design a new skill"
- "Spec the refactor"
- "What should this hook do?"
- "Plan what we're building"

**Automated trigger:**
- After selecting an opportunity from `/shipkit-ideator`
- Before running `/shipkit-dev-plan`

---

## Prerequisites

**Required**:
- Clear idea of what to build/change (user input or opportunity card)

**Helpful context**:
- `docs/development/opportunities.json` — if spec is from ideator output
- `CLAUDE.md` — Skill Value Test, framework rules
- `docs/development/SKILL-QUALITY-AND-PATTERNS.md` — quality standards
- `docs/development/SHIPKIT-7-FILE-INTEGRATION.md` — integration system

---

## Process

### Step 1: Identify Change Type

Ask the user (or infer from `--from-opportunity`):

| Type | What's changing |
|------|----------------|
| `new-skill` | Adding a skill to `install/skills/` |
| `new-agent` | Adding an agent to `install/agents/` |
| `new-hook` | Adding/modifying a hook in `install/shared/hooks/` |
| `skill-update` | Modifying an existing skill |
| `agent-update` | Modifying an existing agent |
| `settings-change` | Changing `install/settings/shipkit.settings.json` |
| `refactor` | Structural changes across multiple components |
| `new-local-skill` | Adding a local dev skill to `.claude/skills/` |
| `architecture` | Framework-wide design change |

### Step 2: Gather Requirements

**For all types, capture:**

1. **Goal** — What problem does this solve? (1-2 sentences)
2. **Motivation** — Why now? What triggered this? (opportunity ID, user request, bug, etc.)
3. **Scope** — What's IN scope and what's explicitly OUT of scope

**For `new-skill` — apply the Skill Value Test:**

> A skill is valuable if it:
> 1. Forces human decisions to be explicit
> 2. Creates persistence Claude lacks
>
> A skill is redundant if Claude does it well without instruction.

Ask: "Which value does this skill provide?" If neither, **stop and tell the user this doesn't need a skill.**

**For `new-skill` / `skill-update` — identify integration points:**
- Which of the 7 integration files are affected?
- Which other skills does it integrate with (before/after)?
- What `.shipkit/` context files does it read/write?

### Step 3: Define Acceptance Criteria

For each requirement, write concrete acceptance criteria:

```
AC-1: [Specific, testable condition]
AC-2: [Specific, testable condition]
...
```

Good: "The hook exits 2 with stderr message when build fails"
Bad: "The hook validates quality"

### Step 4: Identify Affected Files

Map all files that will be created or modified:

**For `new-skill` (7-file integration):**
1. `install/skills/shipkit-{name}/SKILL.md` — CREATE
2. `docs/generated/shipkit-overview.html` — MODIFY (add to list, update count)
3. `install/claude-md/shipkit.md` — MODIFY (add to reference)
4. `install/profiles/shipkit.manifest.json` — MODIFY (register)
5. `install/shared/hooks/shipkit-after-skill-router.py` — MODIFY (if detection needed)
6. `install/skills/shipkit-master/SKILL.md` — MODIFY (routing)
7. `install/settings/shipkit.settings.json` — MODIFY (permission)

**For `new-local-skill`:**
1. `.claude/skills/shipkit-{name}/SKILL.md` — CREATE
(No 7-file integration needed — local dev skills aren't distributed)

**For other types:** List all CREATE/MODIFY/DELETE operations.

### Step 5: Identify Risks

Consider:
- Could this break existing skills?
- Does it change shared infrastructure (hooks, settings)?
- Does it affect the installer?
- Is it backwards-compatible with installed user projects?
- Does it require a version bump?

### Step 6: Write Spec

Write `.claude/specs/{feature}.json`:

```json
{
  "$schema": "shipkit-dev-artifact",
  "type": "framework-spec",
  "version": "1.0",
  "createdAt": "2026-02-20T...",
  "source": "shipkit-dev-spec",
  "feature": "{feature-name}",
  "changeType": "new-skill|skill-update|refactor|...",
  "goal": "What this achieves",
  "motivation": "Why now",
  "scope": {
    "in": ["What's included"],
    "out": ["What's explicitly excluded"]
  },
  "valueTest": {
    "result": "pass|fail|not-applicable",
    "forcesExplicit": "What human decision it captures",
    "createsPersistence": "What memory it creates"
  },
  "acceptanceCriteria": [
    {"id": "AC-1", "description": "Testable condition"},
    {"id": "AC-2", "description": "Testable condition"}
  ],
  "files": {
    "create": ["path/to/new/file"],
    "modify": ["path/to/existing/file"],
    "delete": []
  },
  "integrations": {
    "dependsOn": ["skills this depends on"],
    "dependedBy": ["skills that will depend on this"],
    "contextReads": [".shipkit/ files read"],
    "contextWrites": [".shipkit/ files written"]
  },
  "risks": [
    {"risk": "Description", "severity": "high|medium|low", "mitigation": "How to handle"}
  ],
  "fromOpportunity": "OPP-xxx or null"
}
```

### Step 7: Confirm with User

Present a summary:

```
## Spec: {feature-name}

**Type**: {changeType}
**Goal**: {goal}
**Files**: {N} create, {N} modify, {N} delete

### Acceptance Criteria
- AC-1: ...
- AC-2: ...

### Risks
- {risk} (severity) — mitigation: {mitigation}

Ready to plan implementation? Run `/shipkit-dev-plan {feature-name}`
```

---

## Output Quality Checklist

- [ ] Goal is specific (not vague like "improve X")
- [ ] Skill Value Test applied for new skills
- [ ] Acceptance criteria are binary (pass/fail, not subjective)
- [ ] ALL affected files listed (no surprises during implementation)
- [ ] Risks identified with mitigations
- [ ] Scope clearly separates in/out

---

## When This Skill Integrates with Others

### Before This Skill
- `/shipkit-ideator` — Opportunity cards feed into specs
  - **Trigger**: User selects an opportunity to implement
  - **Why**: Opportunities need concrete specs before planning

### After This Skill
- `/shipkit-dev-plan` — Break spec into implementation steps
  - **Trigger**: Spec written and confirmed
  - **Why**: Spec defines WHAT, plan defines HOW

---

## Context Files This Skill Reads

- `CLAUDE.md` — Skill Value Test, framework rules
- `docs/development/opportunities.json` — If spec is from ideator
- `docs/development/SKILL-QUALITY-AND-PATTERNS.md` — Quality standards
- `docs/development/SHIPKIT-7-FILE-INTEGRATION.md` — Integration checklist
- `.claude/specs/*.json` — Previous specs (avoid duplicates)

## Context Files This Skill Writes

- `.claude/specs/{feature}.json` — Framework change specification
