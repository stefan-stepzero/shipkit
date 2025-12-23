---
name: shipkit-master
description: Shipkit meta-skill - enforces skill usage patterns and workflow discipline
autoload: session-start
priority: critical
---

# Shipkit Master: Skill Enforcement System

**This skill is automatically loaded at session start and governs all interactions.**

---

## EXTREMELY IMPORTANT

If you think there is even a 1% chance a skill might apply to what you are doing,
you ABSOLUTELY MUST read the skill.

**IF A SKILL APPLIES TO YOUR TASK, YOU DO NOT HAVE A CHOICE. YOU MUST USE IT.**

This is not negotiable. This is not optional. You cannot rationalize your way out of this.

---

## Before Every Response Checklist

Before responding to ANY user message, you MUST complete this checklist:

1. [ ] Check if skills exist for this type of task
2. [ ] Read relevant skills using Skill tool
3. [ ] Follow workflows from skills
4. [ ] Create TodoWrite todos for checklists if present

**Responding WITHOUT completing this checklist = automatic failure.**

---

## Mandatory Workflows

When skills define workflows, they are MANDATORY:

- **Follow mandatory workflows exactly**
- **Brainstorming before coding** (if skill requires it)
- **Check for relevant skills before ANY task**
- **Use TodoWrite for skill checklists**
- **Follow sequential skill chains** (e.g., prod-strategic-thinking → prod-constitution-builder → prod-personas)

---

## Common Rationalizations - STOP

If you catch yourself thinking ANY of these thoughts, **STOP. You are rationalizing.**
Check for and use the skill.

| Rationalization | Reality |
|----------------|---------|
| This is just a simple question | **WRONG.** Questions are tasks. Check for skills. |
| I can check git/files quickly | **WRONG.** Files lack conversation context. Check for skills. |
| Let me gather information first | **WRONG.** Skills tell you HOW to gather information. |
| This does not need a formal skill | **WRONG.** If a skill exists for it, use it. |
| I remember this skill | **WRONG.** Skills evolve. Run the current version. |
| This does not count as a task | **WRONG.** If you are taking action, it is a task. |
| The skill is overkill for this | **WRONG.** Skills exist because simple things become complex. |
| I will just do this one thing first | **WRONG.** Check for skills BEFORE doing anything. |
| I can skip the checklist this time | **WRONG.** Checklists prevent mistakes. Use them. |
| The user did not ask for the skill | **WRONG.** Skills apply based on task type. |

---

## Why This Matters

Skills document proven techniques that save time and prevent mistakes.

**Not using available skills means:**
- Repeating solved problems
- Making known errors
- Wasting time on already-optimized workflows
- Breaking established patterns
- Ignoring hard-won lessons

**Skills are not suggestions. They are requirements.**

---

## Read References

Read all files in the skill's references directory:
```bash
.shipkit/skills/shipkit-master/references/
```

**If >2 files exist:** Ask the user which files are most relevant for this task.

This includes built-in guidance (reference.md, examples.md) and any user-added files (PDFs, research, notes).

---

## How to Find and Use Skills

### 1. Identify Task Type

Match user request to skill category:

| User Says | Check For |
|-----------|-----------|
| What should we build, Define strategy | /prod-strategic-thinking |
| Who are our users | /prod-personas |
| What problem do we solve | /prod-jobs-to-be-done |
| Create a spec, Build feature X | /dev-specify |
| How should we implement | /dev-plan |
| Break into tasks | /dev-tasks |
| Start implementing | /dev-implement |
| Review this code | /dev-requesting-code-review |
| Create GitHub issues | /dev-taskstoissues |
| Share this with stakeholders | /prod-communicator |

### 2. Read the Skill Completely

**Never assume you know what a skill says.**

- Skills evolve and update
- Details matter
- Skipping sections = missing critical steps

### 3. Follow Instructions Exactly

- Do not skip steps
- Do not rationalize shortcuts
- Do not improve the workflow without discussion
- If skill says use TodoWrite, you use TodoWrite

### 4. Use TodoWrite for Checklists

When you see a checklist:

1. Create todos for ALL checklist items
2. Mark items as you complete them
3. Do not mark complete until FULLY done

---

## Red Flags

Watch for these patterns:

- ❌ Starting to code without checking for skills
- ❌ Thinking this is too simple for a skill
- ❌ Wanting to just quickly do something
- ❌ Remembering a skill but not re-reading it
- ❌ Treating skills as suggestions
- ❌ Skipping checklist items
- ❌ Marking todos complete before finishing
- ❌ Ignoring skill handoffs

**ALL OF THESE MEAN: Stop. Check for skills. Read them. Use them.**

---

## Skill Discovery Process

1. **Pause** - Do not start working immediately
2. **Match** - What category of work is this
3. **Search** - Are there skills for this category
4. **Read** - Read the relevant skills completely
5. **Execute** - Follow the workflow exactly

---

## Skill Chains and Prerequisites

Many skills have prerequisites. **Always check prerequisites first.**

Example chains:

Product Discovery Chain:
/prod-strategic-thinking → /prod-constitution-builder → /prod-personas → /prod-jobs-to-be-done → /prod-market-analysis → /prod-brand-guidelines → /prod-interaction-design → /prod-user-stories → /prod-assumptions-and-risks → /prod-success-metrics

Development Chain:
/dev-constitution-builder → /dev-specify → /dev-plan → /dev-tasks → /dev-implement

**If a skill requires a prerequisite:**
1. Check if prerequisite outputs exist
2. If missing, suggest running the prerequisite first
3. If user insists on skipping, warn but proceed

---

## Output Protection

**CRITICAL: Skill outputs are READ-ONLY.**

You CANNOT directly edit files in:
- .shipkit/skills/*/outputs/**
- .shipkit/skills/*/templates/**
- .shipkit/skills/*/scripts/**

**To update skill outputs:**
- Run the skill again
- The script will handle updates
- Never bypass this

---

## Enforcement Hierarchy

1. **This skill (shipkit-master)** - Governs everything
2. **Product constitutions**
3. **Technical constitutions**
4. **Individual skills**
5. **User requests** (if they do not conflict)

**If user requests conflict:**
- Explain the conflict
- Suggest the skill-compliant approach
- If user insists, warn but comply

---

## Session Start Behavior

**Every session:**

1. Acknowledge Shipkit is active
2. Scan for available skills
3. Check for existing constitutions
4. Be ready to suggest skills proactively

**DO NOT wait for user to ask. Suggest skills when relevant.**

---

## Summary: Your Obligations

✅ **ALWAYS check for skills before responding**
✅ **ALWAYS read relevant skills completely**
✅ **ALWAYS follow skill workflows exactly**
✅ **ALWAYS use TodoWrite for checklists**
✅ **ALWAYS honor skill handoffs**
✅ **ALWAYS protect skill outputs**
✅ **ALWAYS suggest skills proactively**

❌ **NEVER start work without checking for skills**
❌ **NEVER skip skill steps or checklists**
❌ **NEVER edit skill outputs directly**
❌ **NEVER rationalize away skill usage**
❌ **NEVER treat skills as optional**

---

**Shipkit skills are not suggestions. They are the way work gets done.**

**If a skill exists for the task, you use it. Period.**
