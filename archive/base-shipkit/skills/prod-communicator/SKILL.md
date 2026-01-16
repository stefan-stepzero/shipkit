---
name: prod-communicator
description: "Transform product artifacts into polished HTML stakeholder communications. Use anytime after product discovery to create investor decks, team updates, executive summaries, customer announcements, or board presentations."
---

# Stakeholder Communication Generator

## Agent Persona

**Load:** `.claude/agents/prod-product-designer-agent.md`

## Purpose

Transform product discovery artifacts into polished, visually engaging HTML communications for stakeholders.

## When to Trigger

User says: "Create team update", "Make investor one-pager", "Generate executive summary", "Create customer announcement", "I need board deck"

## Communication Types

- **investor-one-pager** - Opportunity, traction, competitive advantage
- **exec-summary** - Strategic brief, business case, risks
- **team-update** - Product vision, roadmap, context
- **customer-announcement** - Product launch, value proposition
- **board-deck** - Strategic review, progress, decisions

## Process

### Step 1: Read References

Read all files in: `.shipkit/skills/prod-communicator/references/`

**If >2 files exist:** Ask user which are most relevant.

---

### Step 2: Run Script

```bash
.shipkit/skills/prod-communicator/scripts/create-communication.sh --type team-update
```

**Script behavior:**
1. Scans for available product artifacts
2. Archives old HTML: `update-*.html` → `archive-YYYY-MM-DD.html`
3. Creates timestamped HTML: `update-YYYY-MM-DD.html`
4. Tells Claude to EDIT the HTML file

---

### Step 3: Read Source Artifacts

Read available product artifacts that script identified.

**IMPORTANT:** Actually read files - dont invent content.

---

### Step 4: EDIT the HTML File

**CRITICAL:** EDIT the HTML file created by script - DO NOT create new file.

**File location:** `.shipkit/skills/prod-communicator/outputs/update-YYYY-MM-DD.html`

**What to do:**
1. Replace all `{{PLACEHOLDER}}` markers with actual content
2. Add content sections based on communication type
3. Enhance minimal CSS to make it beautiful (colors, spacing, hierarchy)
4. Ensure print-ready (good margins, readable fonts)

---

## Outputs

**Primary:** `.shipkit/skills/prod-communicator/outputs/update-YYYY-MM-DD.html`

**Archived:** `.shipkit/skills/prod-communicator/outputs/archive-YYYY-MM-DD.html`

---

## Constraints

- **ALWAYS** run script first
- **EDIT** HTML file created by script - never create new files
- **ALL CSS inline** - no external resources
- **FILE STAYS IN** `.shipkit/skills/prod-communicator/outputs/`

---

## Context

This is an **ASYNC** skill - can be called anytime after product artifacts exist.
