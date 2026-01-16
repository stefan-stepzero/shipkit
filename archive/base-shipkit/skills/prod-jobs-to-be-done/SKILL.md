---
name: prod-jobs-to-be-done
description: "Use when analyzing how users currently solve their problems (AS-IS state)"
---

# Jobs-to-be-Done

## Agent Persona

**Load:** `.claude/agents/discovery-agent.md`

Adopt: Curious about workarounds, digs into frustrations, uncovers hidden needs.

## Purpose
Document the **CURRENT STATE**: How users currently accomplish their goals, what tools they use, and why current solutions fall short.

**Focus**: AS-IS analysis, not future vision.

## When to Trigger
User says:
- "What job does this solve?"
- "Why would they use this?"
- "What are they doing today?"
- "How do users currently solve this problem?"

## Prerequisites
- Personas defined (`.prodkit/discovery/personas.md` exists)

## Inputs
- Personas (who has the job to be done)
- User research showing current workflows
- Optional uploads from `.prodkit/inputs/discovery/`

## Process

### Step 1: Read References

Read all files in the skill's references directory:
```bash
.shipkit/skills/prod-jobs-to-be-done/references/
```

**If >2 files exist:** Ask the user which files are most relevant for this task.

This includes built-in guidance (reference.md, examples.md) and any user-added files (PDFs, research, notes).

---

### Step 2: Check Product Constitution (Recommended)

**If product constitution exists:**
- Read `.shipkit/skills/prod-constitution-builder/outputs/product-constitution.md`
- Project type determines JTBD analysis depth:
  - **POC:** ONE job only (the core validation hypothesis), shallow analysis
  - **Side Project MVP:** 1-2 jobs (primary + maybe secondary), medium analysis
  - **B2C/B2B Greenfield:** 2-4 jobs per persona, deep analysis with full forces diagram
  - **Experimental:** Focus on job related to experiment hypothesis
  - **Existing Project:** Document jobs current product already serves

**If constitution doesn't exist:** Default to medium depth (2-3 jobs per persona)

---

### Step 3: For Each Persona, Define the Job

**Job Statement** (follow this format):
```
When I [situation]
I want to [motivation]
So that I can [expected outcome]
```

Example: "When managing a remote team across timezones, I want to quickly understand what happened overnight, so I can identify blockers and respond before EOD."

### Step 4: Document Current Solution

**Tools Used**: What do they use today?
- List all tools/platforms
- Note which is primary

**Workflow Steps**: Walk through their process
- Step-by-step current workflow
- Time spent on each step

**Pain Points**: What's broken/slow/frustrating?
- Specific problems
- Impact on productivity
- Emotional response

**Workarounds**: What hacks have they created?
- Manual processes
- Tools misused
- Spreadsheet solutions

### Step 5: Assess Context

**Frequency**: How often does this job arise?
- Daily / Weekly / Monthly
- Influences urgency

**Switching Costs**: What prevents them from changing?
- Team habits
- Existing integrations
- Learning curve
- Data migration

### Step 6: Call Script for Each Job

```bash
.prodkit/scripts/bash/create-jtbd.sh \
  --persona "Sarah the Engineering Manager" \
  --job "When managing remote team, want to catch up on progress, so team stays aligned" \
  --current-solution "Slack, email, Notion, 1-on-1 meetings" \
  --steps "1. Check Slack threads (30m), 2. Scan email (20m), 3. Review Notion (30m), 4. Message team members (40m)" \
  --pains "2 hours daily, context switching, information scattered, fear of missing critical updates" \
  --workarounds "Sets Slack reminders, uses search heavily, maintains personal tracking doc" \
  --frequency "Daily, first thing in morning (7-9 AM)" \
  --switching-costs "Team entrenched in current tools, integration complexity, trust in new approach"
```

Repeat for each persona's primary job.

## Outputs
- `.prodkit/discovery/jobs-to-be-done-current.md`

## Constraints
- **DO NOT** create files manually
- **ALWAYS** use `create-jtbd.sh` script
- **FOCUS** on CURRENT state, not ideal future
- **USE** real user quotes when available
- **ONE** primary job per persona (can have secondary jobs)

## Next Steps
After JTBD defined:
- Analyze market/competitors (what else exists to solve this job?)
- Later: interaction-design will define FUTURE state

## Context
This is **Step 3 of 9** in the ProdKit sequential workflow.
