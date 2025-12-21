---
name: subagent-driven-development
description: "DEPRECATED - Use /implement with subagent mode instead. This skill is for reference only."
---

# Subagent-Driven Development

## DEPRECATED

**This skill has been integrated into `/implement`.**

When running `/implement`, you'll be offered a choice:
```
Implementation has N tasks. How would you like to execute?

1. Direct mode - I execute each task (faster for small plans)
2. Subagent mode - Fresh agent per task (better for large plans)
```

**Choose subagent mode for:**
- 6+ tasks
- Large implementations
- Fresh context per task (no pollution)

---

## How /implement Subagent Mode Works

```
FOR EACH task:

1. CONTROLLER prepares task context
   └─→ Extract task, gather spec context

2. DISPATCH implementation subagent
   └─→ "Implement using TDD: [task details]"
   └─→ Subagent writes test, implements, commits

3. CONTROLLER reviews spec compliance
   └─→ Matches acceptance criteria?
   └─→ Nothing extra (YAGNI)?

4. CONTROLLER reviews code quality
   └─→ Clean code? Good names?

5. CONTROLLER verifies and marks complete
   └─→ Run full test suite
   └─→ Mark task [X] in tasks.md
```

**Benefits:**
- Fresh context per task
- Controller maintains overview
- Two-stage review (spec + quality)
- TDD enforced per task

**Use the standard workflow:**
```
/brainstorming → /specify → /plan → /tasks → /implement (subagent mode)
```
