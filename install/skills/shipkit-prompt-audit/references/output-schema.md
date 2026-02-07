# Prompt Audit Output Schema

This document defines the JSON schema for `.shipkit/prompt-audit.json` produced by the `shipkit-prompt-audit` skill.

---

## Full JSON Schema

```json
{
  "$schema": "shipkit-artifact",
  "type": "prompt-audit",
  "version": "1.0",
  "lastUpdated": "YYYY-MM-DD",
  "source": "shipkit-prompt-audit",

  "summary": {
    "totalPromptsAudited": 12,
    "totalIssuesFound": 8,
    "bySeverity": { "critical": 2, "shouldFix": 4, "minor": 2 },
    "integrationPoints": 12,
    "providers": ["OpenAI", "Anthropic"],
    "pipelines": { "singleStage": 8, "multiStage": 2 }
  },

  "prompts": [
    {
      "id": "pa-001",
      "location": "src/ai/generate-summary.ts:42",
      "provider": "OpenAI",
      "purpose": "Generate article summary from raw text",
      "pipelineType": "single",
      "score": 7,
      "issues": [
        {
          "id": "PA-SCH-001",
          "dimension": "schema-tightness",
          "severity": "critical",
          "title": "Unvalidated JSON output used in database write",
          "evidence": "JSON.parse on line 58 has no try/catch; result inserted into DB on line 62",
          "impact": "Malformed LLM response causes runtime crash and data corruption",
          "fix": "Wrap JSON.parse in try/catch, validate against Zod schema before DB insert",
          "antiPattern": "parse-and-pray"
        }
      ]
    }
  ],

  "patterns": {
    "antiPatterns": [
      {
        "name": "god-prompt",
        "instances": 2,
        "files": ["src/ai/process-all.ts", "src/ai/mega-prompt.ts"],
        "description": "Single prompt handling multiple unrelated concerns"
      },
      {
        "name": "parse-and-pray",
        "instances": 3,
        "files": ["src/ai/generate-summary.ts", "src/ai/classify.ts", "src/ai/extract.ts"],
        "description": "JSON.parse on LLM output without validation or error handling"
      }
    ],
    "positivePatterns": [
      {
        "name": "structured-output",
        "instances": 4,
        "description": "Using provider structured output mode with schema"
      }
    ]
  },

  "pipelines": [
    {
      "id": "pipeline-001",
      "name": "Content Generation Pipeline",
      "type": "chain",
      "stages": [
        { "id": "stage-001", "promptId": "pa-003", "provider": "OpenAI", "purpose": "Analyze tone", "location": "src/ai/content-pipeline.ts:15" },
        { "id": "stage-002", "promptId": "pa-003", "provider": "OpenAI", "purpose": "Extract SEO keywords", "location": "src/ai/content-pipeline.ts:45" },
        { "id": "stage-003", "promptId": "pa-003", "provider": "OpenAI", "purpose": "Generate content", "location": "src/ai/content-pipeline.ts:72" },
        { "id": "stage-004", "promptId": "pa-003", "provider": "OpenAI", "purpose": "Format output", "location": "src/ai/content-pipeline.ts:98" }
      ],
      "edges": [
        { "id": "edge-001", "source": "stage-001", "target": "stage-003", "dataFlow": "tone analysis", "validated": false },
        { "id": "edge-002", "source": "stage-002", "target": "stage-003", "dataFlow": "keywords", "validated": false },
        { "id": "edge-003", "source": "stage-003", "target": "stage-004", "dataFlow": "raw content", "validated": true }
      ],
      "issues": ["PA-DEC-001", "PA-PAR-001"]
    }
  ],

  "recommendations": [
    {
      "priority": "critical",
      "title": "Add schema validation to all LLM output parsing",
      "description": "3 integration points parse LLM JSON without validation. Add Zod schemas and wrap in try/catch.",
      "affectedFiles": ["src/ai/generate-summary.ts", "src/ai/classify.ts", "src/ai/extract.ts"],
      "effort": "low"
    },
    {
      "priority": "shouldFix",
      "title": "Decompose god prompts into focused sub-tasks",
      "description": "2 prompts handle multiple concerns. Break into single-responsibility prompt chains.",
      "affectedFiles": ["src/ai/process-all.ts", "src/ai/mega-prompt.ts"],
      "effort": "medium"
    }
  ]
}
```

---

## Field Reference

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `$schema` | string | yes | Always `"shipkit-artifact"` -- identifies this as a Shipkit-managed file |
| `type` | string | yes | Always `"prompt-audit"` -- artifact type for routing/rendering |
| `version` | string | yes | Schema version for forward compatibility |
| `lastUpdated` | string | yes | ISO date of last modification |
| `source` | string | yes | Always `"shipkit-prompt-audit"` |
| `summary` | object | yes | Aggregated counts for dashboard rendering |
| `summary.totalPromptsAudited` | number | yes | Total LLM integration points scanned |
| `summary.totalIssuesFound` | number | yes | Total issues across all severities |
| `summary.bySeverity` | object | yes | Counts by `critical`, `shouldFix`, `minor` |
| `summary.integrationPoints` | number | yes | Number of LLM call sites discovered |
| `summary.providers` | string[] | yes | LLM providers detected |
| `summary.pipelines` | object | yes | Counts by `singleStage`, `multiStage` |
| `prompts` | array | yes | Per-prompt audit results |
| `prompts[].id` | string | yes | Unique finding ID (e.g., `"pa-001"`) |
| `prompts[].location` | string | yes | File path and line number |
| `prompts[].provider` | string | yes | LLM provider/SDK used |
| `prompts[].purpose` | string | yes | What this prompt does |
| `prompts[].pipelineType` | enum | yes | `"single"` \| `"chain"` \| `"parallel"` |
| `prompts[].score` | number | yes | Quality score 1-10 (10 = no issues) |
| `prompts[].issues` | array | yes | Issues found for this prompt (empty if clean) |
| `prompts[].issues[].id` | string | yes | Dimension-prefixed ID (e.g., `"PA-SCH-001"`) |
| `prompts[].issues[].dimension` | string | yes | Which audit dimension flagged this |
| `prompts[].issues[].severity` | enum | yes | `"critical"` \| `"shouldFix"` \| `"minor"` |
| `prompts[].issues[].title` | string | yes | Short description of the issue |
| `prompts[].issues[].evidence` | string | yes | Tool output that proves this finding |
| `prompts[].issues[].impact` | string | yes | What happens if not fixed |
| `prompts[].issues[].fix` | string | yes | How to resolve the issue |
| `prompts[].issues[].antiPattern` | string | no | Matched anti-pattern name (if applicable) |
| `pipelines` | array | yes | Graph-ready pipeline topology for multi-stage chains |
| `pipelines[].id` | string | yes | Unique pipeline ID (e.g., `"pipeline-001"`) |
| `pipelines[].name` | string | yes | Human-readable pipeline name |
| `pipelines[].type` | enum | yes | `"chain"` \| `"parallel"` \| `"mixed"` |
| `pipelines[].stages` | array | yes | Ordered list of stages (nodes for graph) |
| `pipelines[].stages[].id` | string | yes | Unique stage ID within pipeline |
| `pipelines[].stages[].promptId` | string | yes | References `prompts[].id` for linking to audit findings |
| `pipelines[].stages[].provider` | string | yes | LLM provider for this stage |
| `pipelines[].stages[].purpose` | string | yes | What this stage does |
| `pipelines[].stages[].location` | string | yes | File:line reference |
| `pipelines[].edges` | array | yes | Data flow connections between stages (edges for graph) |
| `pipelines[].edges[].id` | string | yes | Unique edge ID |
| `pipelines[].edges[].source` | string | yes | Source stage ID |
| `pipelines[].edges[].target` | string | yes | Target stage ID |
| `pipelines[].edges[].dataFlow` | string | yes | What data flows along this edge |
| `pipelines[].edges[].validated` | boolean | yes | Whether data is validated between stages |
| `pipelines[].issues` | string[] | no | Issue IDs from `prompts[].issues[]` that affect this pipeline |
| `patterns` | object | yes | Cross-cutting pattern analysis |
| `patterns.antiPatterns` | array | yes | Anti-patterns found across prompts |
| `patterns.antiPatterns[].name` | string | yes | Anti-pattern identifier |
| `patterns.antiPatterns[].instances` | number | yes | How many occurrences found |
| `patterns.antiPatterns[].files` | string[] | yes | Files where pattern was found |
| `patterns.antiPatterns[].description` | string | yes | What this anti-pattern means |
| `patterns.positivePatterns` | array | yes | Good patterns observed |
| `patterns.positivePatterns[].name` | string | yes | Pattern identifier |
| `patterns.positivePatterns[].instances` | number | yes | How many occurrences found |
| `patterns.positivePatterns[].description` | string | yes | What this pattern does well |
| `recommendations` | array | yes | Prioritized action items |
| `recommendations[].priority` | enum | yes | `"critical"` \| `"shouldFix"` \| `"minor"` |
| `recommendations[].title` | string | yes | Action item title |
| `recommendations[].description` | string | yes | What to do and why |
| `recommendations[].affectedFiles` | string[] | yes | Files that need changes |
| `recommendations[].effort` | enum | yes | `"low"` \| `"medium"` \| `"high"` |

---

## Summary Object

The `summary` field MUST be kept in sync with the `prompts` array. It exists so the dashboard can render overview cards without iterating the full array. Recompute it every time the file is written.

---

## Priority Definitions

| Priority | Meaning | Example |
|----------|---------|---------|
| Critical | Will cause failures, security issues, or data corruption | Unvalidated LLM output used in database query; no fallback on payment-critical AI call |
| Should Fix | Quality/reliability issues, technical debt | God Prompt that should be decomposed; sequential calls that could parallelize |
| Minor | Suggestions, optimizations | Caching opportunity; slightly verbose context |

---

## Shipkit Artifact Convention

This skill follows the **Shipkit JSON artifact convention** -- a standard structure for all `.shipkit/*.json` files that enables mission control visualization.

**Every JSON artifact MUST include these top-level fields:**

```json
{
  "$schema": "shipkit-artifact",
  "type": "<artifact-type>",
  "version": "1.0",
  "lastUpdated": "YYYY-MM-DD",
  "source": "<skill-name>",
  "summary": { ... }
}
```

- `$schema` -- Always `"shipkit-artifact"`. Lets the reporter hook identify files to ship to mission control.
- `type` -- The artifact type (`"prompt-audit"`, `"goals"`, `"spec"`, etc.). Dashboard uses this for rendering.
- `version` -- Schema version. Bump when fields change.
- `lastUpdated` -- When this file was last written.
- `source` -- Which skill wrote this file.
- `summary` -- Aggregated data for dashboard cards. Structure varies by type.
