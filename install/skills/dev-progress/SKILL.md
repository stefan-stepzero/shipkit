---
name: dev-progress
description: "Manual progress snapshot for session continuity. Updates based on conversation context (what we just worked on), not git history. Use when user asks 'update progress', 'track progress', or 'what did we accomplish'."
agent: dev-lead
---

# Development Progress Tracking

**Manual snapshot for session continuity - conversation-driven, not git-driven.**

---

## Overview

Maintains a living progress document (progress-current.md) that tracks development status based on conversation context. Archives old versions with timestamps.

**Core principle:** Manual snapshot based on what Claude and user just accomplished in the conversation.

**NOT automated:** Does not scan git history or directories. Claude updates based on conversation awareness.

---

## When to Use

**Manual trigger:**
- User says: "Update progress", "Track what we did", "Document progress"
- /dev-progress

**After significant work:**
- Completed a spec
- Finished implementation
- Merged a feature
- Completed a milestone

**Don't use if:**
- No meaningful progress to track
- Just starting project (no specs/work yet)

---

## Process

### Step 1: Read References

Read all files in the skill's references directory

### Step 2: Run Script

Script archives current progress-current.md with timestamp, creates fresh template, shows registry context

### Step 3: Claude Updates Progress

Based on conversation context - what did we just complete? Fill template with current status.

### Step 4: Write Progress File

Write to: .shipkit/skills/dev-progress/outputs/progress-current.md

### Step 5: Report to User

Show progress summary (X/Y complete), what's current, what's next, suggested next action

---

## Archives

Old progress files archived as progress-YYYY-MM-DD-HHMMSS.md
Current always: progress-current.md

---

## Manual Snapshot Approach

**NOT automated** - Does NOT scan git history, check file timestamps, or analyze directory structure

**Manual tracking** - Claude recalls conversation context and updates based on what we just worked on

**Why manual?** Conversation context is most accurate - user has final say on what's "complete"

---

## Integration with Registry

Uses registry.txt for total spec count, spec numbers/names, chronological order

---

## Constraints

**DO:** Update based on conversation context, archive old files with timestamps
**DON'T:** Scan git history, guess completion status, auto-update without user trigger

---

**Remember**: This is a manual snapshot based on conversation, not automated scanning. Claude updates based on what the user says was accomplished.
