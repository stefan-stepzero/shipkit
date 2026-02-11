# Judgment Output Schema

The `judgment.json` file follows the Shipkit Artifact Convention.

## Schema

```json
{
  "$schema": "shipkit-artifact",
  "type": "semantic-qa-judgment",
  "version": "1.0",
  "lastUpdated": "YYYY-MM-DDTHH:MM:SSZ",
  "source": "shipkit-semantic-qa",

  "summary": {
    "suite": "string — suite name",
    "suiteType": "backend | frontend",
    "runId": "run-YYYY-MM-DDTHHMMSS",
    "totalInputs": "number",
    "passed": "number — inputs passing all must-pass criteria",
    "partial": "number — inputs with some criteria failing",
    "failed": "number — inputs failing must-pass criteria",
    "harnessErrors": "number — inputs that errored during run",
    "overallScore": "number 0-100",
    "criteriaScorecard": [
      {
        "id": "string — criterion ID",
        "name": "string",
        "weight": "must-pass | important | nice-to-have",
        "passRate": "string — e.g. '9/10'",
        "passPercent": "number 0-100"
      }
    ]
  },

  "evaluations": [
    {
      "inputId": "string",
      "inputFile": "string — relative path",
      "outputFile": "string — relative path",
      "overall": "pass | partial | fail | error",
      "criteria": [
        {
          "id": "string — criterion ID",
          "name": "string",
          "result": "pass | partial | fail",
          "evidence": "string — specific observation justifying the result",
          "severity": "null | critical | moderate | minor"
        }
      ]
    }
  ],

  "patterns": {
    "commonFailures": [
      {
        "criterionId": "string",
        "criterionName": "string",
        "failingInputs": ["string — input IDs"],
        "pattern": "string — what these failures have in common"
      }
    ],
    "strengths": ["string — things consistently passing well"]
  },

  "recommendations": [
    {
      "priority": "high | medium | low",
      "title": "string",
      "description": "string — actionable recommendation",
      "affectedInputs": ["string — input IDs"]
    }
  ],

  "previousComparison": {
    "previousRunId": "string | null",
    "scoreChange": "string — e.g. '+5' or '-3'",
    "newPasses": ["string — input IDs that now pass"],
    "newFailures": ["string — input IDs that now fail"],
    "resolvedIssues": ["string — issues from last run now fixed"]
  }
}
```

## Score Calculation

```
overallScore = weighted average of criteria pass rates

Weights:
  must-pass:    3x
  important:    2x
  nice-to-have: 1x

Example:
  must-pass criteria at 90% = 90 * 3 = 270
  important criteria at 80%  = 80 * 2 = 160
  nice-to-have at 100%       = 100 * 1 = 100

  overallScore = (270 + 160 + 100) / (3 + 2 + 1) = 88
```

## Per-Input Overall Result

| Result | Condition |
|--------|-----------|
| `pass` | All criteria pass |
| `partial` | No must-pass fails, but some important/nice-to-have fail |
| `fail` | Any must-pass criterion fails |
| `error` | Harness error — output not produced |
