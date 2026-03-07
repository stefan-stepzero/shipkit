# Metrics Output Schema

Defines the JSON schema for `.shipkit/metrics/latest.json`.

## metrics/latest.json

```json
{
  "$schema": "shipkit-artifact",
  "type": "metrics",
  "version": "1.0",
  "lastUpdated": "YYYY-MM-DDTHH:MM:SSZ",
  "source": "shipkit-metrics",

  "measurements": [
    {
      "criterionId": "P-001",
      "value": "82%",
      "measuredAt": "YYYY-MM-DDTHH:MM:SSZ",
      "source": "analytics|manual|test-run|apm|user-feedback",
      "notes": "Optional context about this measurement"
    }
  ],

  "summary": {
    "totalMeasurements": 0,
    "byPrefix": { "P": 0, "E": 0, "S": 0 },
    "lastCaptureDate": "YYYY-MM-DD"
  }
}
```

## Measurement Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `criterionId` | string | Yes | Matches criterion ID from goals files (P-001, E-002, S-001) |
| `value` | string | Yes | Current measured value (e.g., "82%", "< 200ms", "4.2/5") |
| `measuredAt` | ISO timestamp | Yes | When this measurement was taken |
| `source` | enum | Yes | Where the data came from |
| `notes` | string | No | Additional context |

## Source Values

| Source | When to use |
|--------|------------|
| `analytics` | From analytics platform (GA, Mixpanel, PostHog) |
| `manual` | User-reported or manually observed |
| `test-run` | From test suite execution (coverage, pass rate) |
| `apm` | From application performance monitoring (response times, error rates) |
| `user-feedback` | From user surveys, interviews, support tickets |

## ID Convention

Criterion IDs match the goals they evaluate:

| Prefix | Defined by | Example |
|--------|-----------|---------|
| `P-` | `/shipkit-product-goals` | P-001: Task completion rate |
| `E-` | `/shipkit-engineering-goals` | E-001: Test coverage |
| `S-` | `/shipkit-stage` | S-001: Monthly active users |

## How Goals Skills Consume This

`/shipkit-product-goals --evaluate` and `/shipkit-engineering-goals --evaluate`:
1. Read `metrics/latest.json`
2. Match `measurements[].criterionId` to `criteria[].id` in goals files
3. Compare `value` against `threshold`
4. Update criterion `status`: `not-measured` → `below-threshold` | `at-threshold` | `exceeded`

## Shipkit Artifact Convention

Every JSON artifact MUST include: `$schema`, `type`, `version`, `lastUpdated`, `source`, `summary`.
